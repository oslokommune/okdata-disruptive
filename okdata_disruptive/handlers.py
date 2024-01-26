import csv

from aws_xray_sdk.core import patch_all, xray_recorder
from okdata.aws.logging import logging_wrapper
from okdata.sdk.data.dataset import Dataset
from okdata.sdk.data.upload import Upload
from requests.exceptions import HTTPError

from okdata_disruptive.client import DisruptiveClient
from okdata_disruptive.util import getenv

patch_all()

# Projects to import data from.
PROJECT_IDS = [
    "c0vnqtm0c7bet3vics90",  # Bydel Grorud
    "c0vnqb5v4t6ssbpguueg",  # Bydel Vestre Aker
    "c17lkka9kmt7101g0ijg",  # Hovedlager Nydalen
    "c4iudupgt1qt96jhsjp0",  # Lahaugmoen
]


def _import_dataset(dataset_id, filename):
    dataset = Dataset()
    upload = Upload()

    try:
        version = dataset.get_latest_version(dataset_id)["version"]
    except HTTPError as e:
        if e.response.status_code == 404:
            print(f"Dataset '{dataset_id}' not found; skipping import")
            return
        raise

    edition = dataset.auto_create_edition(dataset_id, version)["Id"].split("/")[-1]
    upload.upload(filename, dataset_id, version, edition, 3)


@logging_wrapper
@xray_recorder.capture("import_data")
def import_data(event, context):
    disruptive_client = DisruptiveClient(
        getenv("SERVICE_ACCOUNT_EMAIL"),
        getenv("SERVICE_ACCOUNT_KEY_ID"),
        getenv("SERVICE_ACCOUNT_SECRET"),
    )
    with open("/tmp/disruptive_data.csv", "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "project_id",
                "project_name",
                "device_id",
                "device_name",
                "timestamp",
                "temperature",
            ],
        )
        writer.writeheader()
        for project_id in PROJECT_IDS:
            project = disruptive_client.get_project(project_id)
            for device in disruptive_client.list_devices(project_id):
                for events in disruptive_client.get_events(project, device):
                    writer.writerow(events)
        _import_dataset("disruptive", f.name)
