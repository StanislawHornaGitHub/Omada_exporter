import src.Omada.Controller as Controller
import src.Model as Model
from src.Observability import *

tracer = trace.get_tracer("HealthCheckController-tracer")


class HealthCheck:

    @staticmethod
    @tracer.start_as_current_span("HealthCheck.get_status")
    def get_status() -> Model.HealthCheck:
        get_current_span()

        try:
            health_status: dict = Controller.HealthCheck.get()
            result = Model.HealthCheck(**health_status)
        except Exception as e:
            logger.exception(e, exc_info=True)
            raise e
        else:
            set_current_span_status()
            return result
