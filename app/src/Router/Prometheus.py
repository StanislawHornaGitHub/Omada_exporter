from fastapi import APIRouter, Response
from prometheus_client import generate_latest
import src.Controller as Controller

Prometheus_router = APIRouter()


@Prometheus_router.get(path="/metrics")
def get_metrics():
    Controller.PrometheusMetrics.update()
    return Response(
        content=generate_latest(),
        media_type="text/plain"
    )
