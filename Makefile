
install:
	clear
	python3 -m poetry add \
	"apache-beam" \
	"apache-beam[gcp]" \
	"google-cloud-storage" \
	"google-cloud-bigquery" \
	"google-cloud-pubsub" \
	"dacite" \
	"black"

lint:
	clear
	python3 -m poetry run black .


run: lint
	python3 -m team_league_dataflow_pipeline.applications.team_league_app \
	--project=sounish-cloud-workstation \
	--project_id=sounish-cloud-workstation \
	--input_subscription=None \
	--input_json_file="gs://sounish-cloud-workstation/data/data.json" \
	--job_name=team-league-python-job-$$(date +'%d%m%Y%H%M%S') \
	--runner=DataflowRunner \
	--staging_location=gs://sounish-cloud-workstation/dataflow/staging \
	--region="asia-south1" \
	--machine_type='n2-standard-4' \
    --temp_location=gs://sounish-cloud-workstation/dataflow/temp \
    --team_leaugue_dataset="sample_dataset" \
    --team_stats_table="team_stats" \
    --bq_write_method=FILE_LOADS \
	--setup_file=./setup.py

	find . -name "__pycache__" -type d -exec rm -fr {} +


test: lint
	python3 -m team_league_dataflow_pipeline.applications.team_league_app \
	--project=sounish-cloud-workstation \
	--project_id=sounish-cloud-workstation \
	--input_subscription=None \
	--input_json_file="gs://sounish-cloud-workstation/data/data.json" \
	--job_name=team-league-python-job-$$(date +'%d%m%Y%H%M%S') \
	--runner=DataflowRunner \
	--staging_location=gs://sounish-cloud-workstation/dataflow/staging \
	--region="asia-south1" \
	--machine_type='n2-standard-4' \
    --temp_location=gs://sounish-cloud-workstation/dataflow/temp \
    --team_leaugue_dataset="sample_dataset" \
    --team_stats_table="team_stats" \
    --bq_write_method=FILE_LOADS \
	--setup_file=./setup.py

	find . -name "__pycache__" -type d -exec rm -fr {} +