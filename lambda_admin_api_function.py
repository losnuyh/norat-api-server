from mangum import Mangum

from run.admin.real import app

lambda_handler = Mangum(app, lifespan="off")
