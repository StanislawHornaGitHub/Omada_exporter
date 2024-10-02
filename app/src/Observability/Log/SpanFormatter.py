from opentelemetry import trace
from loki_logger_handler.loki_logger_handler import LoggerFormatter
from src.Observability.Trace.OpenTelemetry import get_trace_id, get_span_id
import src.Config as Config


class SpanFormatter(LoggerFormatter):
    def format(self, record):

        record.trace_id = get_trace_id()
        record.span_id = get_span_id()
        record.deployment_environment = Config.ENVIRONMENT

        return super().format(record)
