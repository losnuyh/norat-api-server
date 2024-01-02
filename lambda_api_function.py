from mangum import Mangum

from application.main import app


lambda_handler = Mangum(app, lifespan="off")