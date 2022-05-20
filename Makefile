up_app:
	docker-compose up -d

up_sync_jobs:
	docker-compose run web python -Wd manage.py sync_jobs

up_flow_wallet:
	cd flow-wallet-api
	docker-compose up -d

up: up_app up_sync_jobs up_flow_wallet
