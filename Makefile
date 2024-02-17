run-local:
	uvicorn run.main.local:app --reload

run-local-with-worker:
	uvicorn run.main.local:app --workers=4

main_api_function_zip:
	rm -rf ./_api_package || true
	poetry export --with lambda --without-hashes --format=requirements.txt > requirements-lambda.txt
	pip install --platform manylinux_2_17_aarch64 --implementation cp --only-binary=:all: -r requirements-lambda.txt --target ./_api_package --upgrade
	rm requirements-lambda.txt
	rm -rf api_lambda || true
	pip install boto3
	python generate_main_env_file.py --env=$(env)
	mkdir api_lambda
	cp .env ./api_lambda
	cp lambda_api_function.py ./api_lambda/
	cp -R ./_api_package/* ./api_lambda
	rm -rf ./_api_package
	cp -R ./application ./api_lambda
	cp -R ./common ./api_lambda
	mkdir ./api_lambda/run
	cp -R ./run/main ./api_lambda/run/main
	chmod +X ./api_lambda/lambda_api_function.py
	rm api_lambda.zip || true
	cd api_lambda && zip -r ../api_lambda.zip ./
	rm -rf api_lambda || true
