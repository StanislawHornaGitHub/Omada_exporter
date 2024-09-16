import datetime
import src.Omada.Model as Model
import src.Omada.Connection as Connection
from src.Omada.Controller.Devices import Devices


class Router:

    __router_info_path: str = "/openapi/v1/{omadacId}/sites/{siteId}/gateways/{gatewayMac}"
    __router_port_stats_path: str = "/api/v2/sites/{siteId}/stat/{gatewayMac}/5min?type=gateway"
    __router_port_info_path: str = "/api/v2/sites/{siteId}/gateways/{gatewayMac}"

    @staticmethod
    def get_info() -> list[Model.Router]:

        result = [
            Model.Router(
                **{
                    "name": item.name,
                    **Connection.Request.get(
                        Router.__router_info_path, {
                            "gatewayMac": item.mac
                        }
                    )
                }
            )
            for item in Devices.gateways
        ]
        return result

    @staticmethod
    def get_port_info() -> list[Model.Ports.RouterPort]:
        router_port: list[Model.Ports.RouterPort] = []

        for router in Devices.gateways:
            router_port_response: dict = Connection.Request.get(
                Router.__router_port_info_path, {
                    "gatewayMac": router.mac
                }
            )
            for port in router_port_response.get("portStats"):
                try:
                    router_port.append(
                        Model.Ports.RouterPort(
                            **(
                                {
                                    "gatewayName": router.name,
                                    "mac": router.mac,
                                    **port,
                                }
                            )
                        )
                )
                except:
                    pass
            # Needed to fix Omada bug, that it records traffic on port with disconnected cable
            port_status = {}
            for port in router_port:
                port_status[port.port] = port.linkSpeed

        return router_port
