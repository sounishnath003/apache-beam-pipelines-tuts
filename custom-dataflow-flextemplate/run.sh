#!/usr/bin/env bash

clear

python -m black .

python3 -m appp.main --runner=DirectRunner --project=sounish-cloud-workstation --machine_type=n1-standard-1 --temp_location=gs://sounish-cloud-workstation/dataflow/temp --staging_location=gs://sounish-cloud-workstation/dataflow/staging --region=asia-south1 --experiment=use_unsupported_python_version --job_name=basic-beam-pipeline-$(date +'%Y%m%d%H%M%S') --setup_file=./setup.py --save_main_session
