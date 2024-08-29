import src.Omada.Connection as Connection
from src.Omada.Controller.Devices import Devices

class HealthCheck:
    
    __controller_name: str = ""
    __controller_version: str = ""

    __web_api_endpoint: str = "/api/v2/maintenance/controllerStatus"

    @staticmethod
    def get():
        return {
            "UserSession": HealthCheck.__test_web_api_endpoint(),
            "OpenAPI": HealthCheck.__test_open_api_endpoint(),
            "ControllerName": HealthCheck.__controller_name,
            "ControllerVersion": HealthCheck.__controller_version,
        }

    @staticmethod
    def __test_web_api_endpoint() -> str:
        try:
            result: dict = Connection.Request.get(
                HealthCheck.__web_api_endpoint
            )
            HealthCheck.__controller_name = result.get("name")
            HealthCheck.__controller_version = result.get("controllerVersion")
            return True
        except:
            return False

    @staticmethod
    def __test_open_api_endpoint() -> str:
        try:
            Devices.get_list()
            return True
        except:
            return False