import os
from dotenv import load_dotenv
load_dotenv()

BASE_URL = os.getenv("BASE_URL")
VERIFY_CERTIFICATE = os.getenv("VERIFY_CERTIFICATE")
SITE_NAME = os.getenv("SITE_NAME", None)


OMADA_USER = os.getenv("OMADA_USER")
OMADA_USER_PASSWORD = os.getenv("OMADA_USER_PASSWORD")

OMADA_CLIENT_ID = os.getenv('OMADA_CLIENT_ID')
OMADA_CLIENT_SECRET = os.getenv('OMADA_CLIENT_SECRET')
