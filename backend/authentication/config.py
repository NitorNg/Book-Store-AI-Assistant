import os

from casdoor import CasdoorSDK
from dotenv import load_dotenv

load_dotenv()
# import casdoor's properties from .env file, everyone need to download casdoor and setup organization, application. Make sure to change your casdoor's port to 8001, so it is not conflict with fastapi's uv run.
with open(os.environ["CASDOOR_CERT_PATH"], encoding="utf-8") as f:
    _certificate = f.read()

sdk = CasdoorSDK(
    endpoint=os.environ["CASDOOR_ENDPOINT"],          # e.g. http://localhost:8001
    client_id=os.environ["CASDOOR_CLIENT_ID"],
    client_secret=os.environ["CASDOOR_CLIENT_SECRET"],
    certificate=_certificate,
    org_name=os.environ["CASDOOR_ORG"],
    application_name=os.environ["CASDOOR_APP"],
)