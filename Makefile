run-main-local:
	uvicorn run.main.local:app --reload

run-main-real:
	uvicorn run.main.real:app --reload

run-admin-local:
	uvicorn run.admin.local:app --reload

run-admin-real:
	uvicorn run.admin.real:app --reload


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


admin_api_function_zip:
	rm -rf ./_admin_api_package || true
	poetry export --with lambda --without-hashes --format=requirements.txt > requirements-lambda.txt
	pip install --platform manylinux_2_17_aarch64 --implementation cp --only-binary=:all: -r requirements-lambda.txt --target ./_admin_api_package --upgrade
	rm requirements-lambda.txt
	rm -rf admin_api_lambda || true
	pip install boto3
	python generate_admin_env_file.py --env=$(env)
	mkdir admin_api_lambda
	cp .env ./admin_api_lambda
	cp lambda_admin_api_function.py ./admin_api_lambda/
	cp -R ./_admin_api_package/* ./admin_api_lambda
	rm -rf ./_admin_api_package
	cp -R ./application ./admin_api_lambda
	cp -R ./common ./admin_api_lambda
	mkdir ./admin_api_lambda/run
	cp -R ./run/admin ./admin_api_lambda/run/admin
	chmod +X ./admin_api_lambda/lambda_admin_api_function.py
	rm admin_api_lambda.zip || true
	cd admin_api_lambda && zip -r ../admin_api_lambda.zip ./
	rm -rf admin_api_lambda || true
