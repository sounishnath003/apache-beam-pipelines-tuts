import setuptools


setuptools.setup(
    name="basic-elt-pipeline",
    version="0.0.1",
    description="a sample DoFn and DataQuality check pipeline on open source customers",
    author="sounish nath",
    author_email="flock.sinasini@gmail.com",
    packages=setuptools.find_packages(exclude=["tests"]),
    install_requires=[
        "apache-beam",
        "apache-beam[gcp]",
        "dacite",
        "google-cloud-storage",
        "google-cloud-bigquery",
    ],
)
