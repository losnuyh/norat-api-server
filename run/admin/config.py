import os
from dataclasses import fields

from dotenv import load_dotenv

from .config_scheme import AdminConfigScheme

load_dotenv()

app_config = AdminConfigScheme(
    **{key.name: os.environ[key.name] for key in fields(AdminConfigScheme) if key.name in os.environ},
)
