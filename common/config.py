import os
from dataclasses import fields

from dotenv import load_dotenv

from .config_scheme import CommonConfigScheme

load_dotenv()

app_config = CommonConfigScheme(
    **{key.name: os.environ[key.name] for key in fields(CommonConfigScheme) if key.name in os.environ},
)
