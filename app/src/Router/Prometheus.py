from fastapi import APIRouter, Response, HTTPException
from prometheus_client import generate_latest
from src.Observability import *
import src.Controller as Controller

Prometheus_router = APIRouter()


@Prometheus_router.get(path="/metrics")
def get_metrics():
    _ = get_current_span()
    headers = get_response_headers()
    try:
        Controller.PrometheusMetrics.update()
        response = Response(
            content=generate_latest(Controller.PrometheusMetrics.registry),
            media_type="text/plain",
            headers={
                "trace_id": get_trace_id()
            }
        )
    except Exception as e:
        logger.exception(e,exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=headers,
            headers=headers
        )
    else:
        set_current_span_status()
        return response

@Prometheus_router.get(path="/appmetrics")
def get_app_metrics():
    _ = get_current_span()
    headers = get_response_headers()
    try:
        response = Response(
            content=generate_latest(),
            media_type="text/plain",
            headers=headers
        )
    except Exception as e:
        logger.exception(e,exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=headers,
            headers=headers
        )
    else:
        set_current_span_status()
        return response
