run-local:
	uvicorn application.local:app --reload

api_function_zip:
	rm -rf ./_api_package || true
	poetry export --with lambda --without-hashes --format=requirements.txt > requirements-lambda.txt
	pip install --platform manylinux_2_17_aarch64 --implementation cp --only-binary=:all: -r requirements-lambda.txt --target ./_api_package --upgrade
	rm requirements-lambda.txt
	rm -rf api_lambda || true
	pip install boto3
	python generate_env_file.py --env=$(env)
	mkdir api_lambda
	ls -A .
	cp .env ./api_lambda
	cp lambda_api_function.py ./api_lambda/
	cp -R ./_api_package/* ./api_lambda
	rm -rf ./_api_package
	cp -R ./application ./api_lambda
	chmod +X ./api_lambda/lambda_api_function.py
	rm api_lambda.zip || true
	ls -A .
	cd api_lambda && zip -r ../api_lambda.zip ./*
	ls api_lambda
	rm -rf api_lambda || true
