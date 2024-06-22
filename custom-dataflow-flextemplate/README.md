# Beam Data pipeline

Demonstration of a **apache beam** data engineering pipeline with Custom Flex Template support, runs on the local environment with `runner=DirectRunner` and deploy on google cloud `runner=DataflowRunner` at ease.


## Create custom container

```bash
gcloud artifacts repositories create appp \
  --repository-format=docker \
  --location=asia-south1 \
  --async
```

## Authenticate your container repository

```bash
gcloud auth configure-docker asia-south1-docker.pkg.dev
```

## Use Cloud build

```bash
gcloud config set builds/use_kaniko True
gcloud config set builds/kaniko_cache_ttl 600
gcloud beta builds submit --tag asia-south1-docker.pkg.dev/sounish-cloud-workstation/appp/dataflow/apppimg:v1 .
```

## Prebuild custom container sdk for dataflow job

```bash
export REGION=us-central1
export PROJECT_ID=sounish-cloud-workstation
export IMAGE_NAME=asia-south1-docker.pkg.dev/sounish-cloud-workstation/appp/dataflow/apppimg:v$(date +'%Y.%m.%d')

gcloud config set builds/use_kaniko True
gcloud config set builds/kaniko_cache_ttl 600
gcloud beta builds submit --tag $IMAGE_NAME .

python -m appp.main \
  --project=$PROJECT_ID \
  --region=$REGION \
  --temp_location=gs://sounish-cloud-workstation/dataflow/temp \
  --staging_location=gs://sounish-cloud-workstation/dataflow/staging \
  --runner=DataflowRunner \
  --experiments=use_runner_v2 \
  --sdk_container_image=$IMAGE_NAME \
  --sdk_location=container

```

## Build flex template and upload container

```bash
gcloud dataflow flex-template build gs://sounish-cloud-workstation/templates/appp/template-params \
  --image asia-south1-docker.pkg.dev/sounish-cloud-workstation/appp/dataflow/apppimg:v1 \
  --sdk-language PYTHON \
  --metadata-file job-metadata
```

## Run dataflow flex template

```bash
gcloud dataflow flex-template run basic-beam-pipeline-test-$(date +'%Y%m%d%H%M%S') \
--template-file-gcs-location gs://sounish-cloud-workstation/templates/appp/template-params \
--region us-central1 --temp-location=gs://sounish-cloud-workstation/dataflow/temp \
--staging-location=gs://sounish-cloud-workstation/dataflow/staging \
--num-workers 1 --worker-machine-type n1-standard-1 --worker-region us-central1 \
--parameters output=gs://sounish-cloud-workstation/apppdataflow-output/
```

## Continuous Deployments through Cloud build

```bash
export CLOUDSDK_PYTHON_SITEPACKAGES=1
gcloud beta builds submit --region=us-central1 --config cloudbuild.yaml
```
