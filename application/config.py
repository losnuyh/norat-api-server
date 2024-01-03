import sys
import os
from dataclasses import fields

from dotenv import load_dotenv

from .config_scheme import ApplicationConfigScheme

load_dotenv()
print(os.listdir(sys.path[0]))


app_config = ApplicationConfigScheme(
    **{key.name: os.environ[key.name] for key in fields(ApplicationConfigScheme) if key.name in os.environ},
)
