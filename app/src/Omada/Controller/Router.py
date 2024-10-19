import datetime
import src.Omada.Model as Model
import src.Omada.Connection as Connection
from src.Omada.Controller.Devices import Devices
from src.Observability import *


tracer = trace.get_tracer("Router-tracer")


class Router:

    __router_info_path: str = (
        "/openapi/v1/{omadacId}/sites/{siteId}/gateways/{gatewayMac}"
    )
    __router_port_stats_path: str = (
        "/api/v2/sites/{siteId}/stat/{gatewayMac}/5min?type=gateway"
    )
    __router_port_info_path: str = "/api/v2/sites/{siteId}/gateways/{gatewayMac}"

    @staticmethod
    @tracer.start_as_current_span("Router.get_info")
    def get_info() -> list[Model.Router]:

        router_devices: list[Model.Router] = []
        error: bool = False
        get_current_span()
        logger.info(
            "Getting Router info",
            extra={"devices": [item.mac for item in Devices.gateways]},
        )

        for router in Devices.gateways:
            try:
                router_info: dict = Connection.Request.get(
                    Router.__router_info_path, {"gatewayMac": router.mac}
                )
                router_object = Model.Router(**{"name": router.name, **router_info})
                router_devices.append(router_object)
            except Exception as e:
                error = True
                logger.exception(
                    e,
                    exc_info=True,
                    extra={"router_name": router.name, "router_mac": router.mac},
                )

        set_current_span_status(error)
        return router_devices

    @staticmethod
    @tracer.start_as_current_span("Router.get_port_info")
    def get_port_info() -> list[Model.Ports.RouterPort]:

        router_port: list[Model.Ports.RouterPort] = []
        error: bool = False
        get_current_span()

        logger.info(
            "Getting Router port info for {num} Routers".format(
                num=len(Devices.gateways),
            ),
            extra={"devices": [item.mac for item in Devices.switches]},
        )

        for router in Devices.gateways:
            try:
                router_port_response: dict = Connection.Request.get(
                    Router.__router_port_info_path, {"gatewayMac": router.mac}
                )
            except Exception as e:
                error = True
                logger.exception(
                    e,
                    exc_info=True,
                    extra={"router_name": router.name, "router_mac": router.mac},
                )
                continue

            for port in router_port_response.get("portStats"):
                try:
                    router_port_object = Model.Ports.RouterPort(
                        **{
                            **port,
                            "gatewayName": router.name,
                            "mac": router.mac,
                        }
                    )
                    router_port.append(router_port_object)
                except Exception as e:
                    error = True
                    logger.warning(
                        e,
                        exc_info=True,
                        extra={
                            "router_name": router.name,
                            "router_mac": router.mac,
                            "port": port.get("port", None),
                        },
                    )

        logger.info(
            "Found {num} router ports".format(num=len(router_port)),
            extra={"devices": [item.mac for item in Devices.gateways]},
        )
        set_current_span_status(error)
        return router_port
