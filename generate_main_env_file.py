import argparse
from dataclasses import fields

from boto3 import client

from common.config_scheme import CommonConfigScheme
from run.main.config_scheme import ApplicationConfigScheme

parser = argparse.ArgumentParser(
    prog=".env file generator",
)
parser.add_argument("-e", "--env", required=True, choices=["dev", "prod"])
parser.add_argument("-d", "--destination", default=".env")
args = parser.parse_args()

env = args.env
file_destination = args.destination
ssm_client = client("ssm")
names = [f"/second/MAIN/{env}/{key.name}" for key in fields(ApplicationConfigScheme)]
names += [f"/second/COMMON/{env}/{key.name}" for key in fields(CommonConfigScheme)]

size = 10
cursor = 0
values = {}

while True:
    parameters = ssm_client.get_parameters(
        Names=names[cursor : cursor + size],
        WithDecryption=True,
    )["Parameters"]
    for param in parameters:
        values[param["Name"].rsplit("/", maxsplit=1)[-1]] = param["Value"]
    cursor += size
    if cursor > len(names):
        break

env_file = ""
for key, value in values.items():
    line = f'{key}="{value}"\n'
    env_file += line


with open(file_destination, "w") as f:
    f.write(env_file)
