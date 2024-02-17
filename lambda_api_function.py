from mangum import Mangum

from run.main.real import app

lambda_handler = Mangum(app, lifespan="off")
