#!/bin/bash

set -eu
black .
clear

rm -fr logs

python3 -m etlpipelien.application.app \
    --job_name='basic-elt-pipeline-$$(date +%d%m%Y%H%M%S)' \
    --input_file="gs://sounish-cloud-workstation/data/customers.csv" \
    --schema="gs://sounish-cloud-workstation/data/schema/customer_schema.json" \
    --bq_table="./output/export-customers" \
    --staging_folder="./logs" \
    --runner=DirectRunner \
    --project=sounish-cloud-workstation \
    --region=asia-south1 \
    --machine_type=n2-standard-4 \
    --staging_location="gs://sounish-cloud-workstation/dataflow-logs/staging" \
    --temp_location="gs://sounish-cloud-workstation/dataflow-logs/temp" \
    --setup_file=./setup.py \
    --experiment use_unsupported_python_version

find . -name "__pycache__" -type d -exec rm -fr {} +;