import os
import setuptools

setuptools.setup(
    name="appp",
    description="apppp is a simple beam pipeline",
    version="0.0.1",
    packages=setuptools.find_packages(exclude=["tests", "data", "logs"]),
    install_requires=[
        "apache-beam[gcp]==2.56.0",
        "google-cloud-storage",
        "google-cloud-bigquery",
        "google-api-python-client",
    ],
)
