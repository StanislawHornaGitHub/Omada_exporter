from src.Observability.Log.logger import logger
from opentelemetry.semconv.trace import SpanAttributes
from src.Observability.Trace.OpenTelemetry import *
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from prometheus_fastapi_instrumentator import Instrumentator


def opentelemetry_instrument(app):
    (
        FastAPIInstrumentor()
        .instrument_app(app)
    )


def prometheus_instrument(app):
    (
        Instrumentator()
        .instrument(app)
    )
