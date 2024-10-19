import os
from dotenv import load_dotenv
load_dotenv()

USE_LOKI = True
LOKI_IP = os.getenv("LOKI_IP","10.0.10.102")
LOKI_PORT = os.getenv("LOKI_PORT","3111")
LOG_LEVEL = os.getenv("LOG_LEVEL","INFO")
