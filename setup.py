from setuptools import find_packages, setup

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="okdata-disruptive",
    version="0.1.0",
    author="Oslo Origo",
    author_email="dataspeilet@oslo.kommune.no",
    description="Batch job for loading Disruptive sensor data into the Origo dataplatform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/oslokommune/okdata-disruptive",
    packages=find_packages(),
    install_requires=[
        "aws-xray-sdk",
        "disruptive",
        "okdata-aws>=2,<3",
        "requests",
    ],
    python_requires=">=3.11",
)
