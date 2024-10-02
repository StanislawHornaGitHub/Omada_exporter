from fastapi import APIRouter, Response, HTTPException
import src.Controller as Controller
import src.Model as Model
from src.Observability import *

HealthCheck = APIRouter()


@HealthCheck.get(path="/healthcheck", response_model=Model.HealthCheck)
def get_health():
    _ = get_current_span()
    headers = get_response_headers()
    try:
        status: Model.HealthCheck = Controller.HealthCheck.get_status()
        response = Response(
            content=status.model_dump_json(indent=4),
            headers=headers
        )
    except Exception as e:
        logger.exception(e, exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=headers,
            headers=headers
        )
    else:
        set_current_span_status()
        return response
