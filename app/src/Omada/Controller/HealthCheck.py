import src.Omada.Connection as Connection
from src.Omada.Controller.Devices import Devices
from src.Observability import *

tracer = trace.get_tracer("HealthCheck-tracer")

class HealthCheck:
    
    __controller_name: str = ""
    __controller_version: str = ""

    __web_api_endpoint: str = "/api/v2/maintenance/controllerStatus"

    @staticmethod
    @tracer.start_as_current_span("HealthCheck.get")
    def get() -> dict[str,str]:
        get_current_span()
        
        try:
            result = {
                "UserSession": HealthCheck.__test_web_api_endpoint(),
                "OpenAPI": HealthCheck.__test_open_api_endpoint(),
                "ControllerName": HealthCheck.__controller_name,
                "ControllerVersion": HealthCheck.__controller_version,
            }
        except Exception as e:
            logger.exception(e,exc_info=True)
            raise e
        else:
            set_current_span_status()
        finally:
            return result

    @staticmethod
    @tracer.start_as_current_span("HealthCheck.__test_web_api_endpoint")
    def __test_web_api_endpoint() -> str:
        current_span = trace.get_current_span()
        current_span.set_status(status=trace.StatusCode(2))
        
        try:
            result: dict = Connection.Request.get(
                HealthCheck.__web_api_endpoint
            )
            HealthCheck.__controller_name = result.get("name")
            HealthCheck.__controller_version = result.get("controllerVersion")
            current_span.set_status(status=trace.StatusCode(1))
            return True
        except Exception as e:
            logger.exception(e, exc_info=True)
            return False

    @staticmethod
    @tracer.start_as_current_span("HealthCheck.__test_open_api_endpoint")
    def __test_open_api_endpoint() -> str:
        get_current_span()
        
        try:
            Devices.get_list()
        except:
            return False
        else:
            set_current_span_status()
            return True