from fastapi import APIRouter, Response
import src.Controller as Controller
import src.Model as Model
HealthCheck = APIRouter()


@HealthCheck.get(path="/healthcheck",response_model=Model.HealthCheck)
def get_health():
    return Controller.HealthCheck.get_status()
