from setuptools import find_packages, setup

setup(
    name='teams_league_app',
    version='0.0.1',
    install_requires=[
        "apache-beam==2.55.1",
        "apache-beam[gcp]==2.55.1",
        "dacite==1.6.0",
        "toolz",
    ],
    packages=find_packages(exclude=["data", "tests"])
)