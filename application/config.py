import os
from dataclasses import fields

from .config_scheme import ApplicationConfigScheme


app_config = ApplicationConfigScheme(
    **{key.name: os.environ[key.name] for key in fields(ApplicationConfigScheme) if key.name in os.environ},
)
