import os
from dotenv import load_dotenv
load_dotenv()

SERVICE_NAME="Omada_Exporter"
ENVIRONMENT=os.getenv("ENVIRONMENT_TYPE", "dev")