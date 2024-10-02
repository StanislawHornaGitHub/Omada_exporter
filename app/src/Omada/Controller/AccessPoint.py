import datetime
import src.Omada.Model as Model
import src.Omada.Connection as Connection
from src.Omada.Controller.Devices import Devices
from src.Observability import *

tracer = trace.get_tracer("AccessPoint-tracer")


class AccessPoint:
    __access_point_info_path: str = "/openapi/v1/{omadacId}/sites/{siteId}/aps/{apMac}"
    __access_point_port_info_path: str = "/openapi/v1/{omadacId}/sites/{siteId}/aps/{apMac}/wired-uplink"
    __access_point_radio_info_path: str = "/openapi/v1/{omadacId}/sites/{siteId}/aps/{apMac}/radios"
    __access_point_radio_stats_path: str = "/api/v2/sites/{siteId}/stat/{apMac}/5min?type=ap"

    @staticmethod
    @tracer.start_as_current_span("AccessPoint.get_info")
    def get_info() -> list[Model.AccessPoint]:

        get_current_span()
        ap_devices: list[Model.AccessPoint] = []
        error: bool = False
        logger.info(
            "Getting AccessPoint info",
            extra={
                "devices": [item.mac for item in Devices.access_points]
            }
        )

        for ap in Devices.access_points:
            try:
                ap_info: dict = Connection.Request.get(
                    AccessPoint.__access_point_info_path, {
                        "apMac": ap.mac
                    }
                )
                ap_object = Model.AccessPoint(
                    **ap_info
                )
                ap_devices.append(
                    ap_object
                )
            except Exception as e:
                error = True
                logger.exception(
                    e,
                    exc_info=True,
                    extra={
                        "access_point_name": ap.name,
                        "access_point_mac": ap.mac
                    }
                )

        set_current_span_status(error)
        return ap_devices

    @staticmethod
    @tracer.start_as_current_span("AccessPoint.get_port_info")
    def get_port_info() -> list[Model.Ports.AccessPointPort]:

        access_point_port: list[Model.Ports.AccessPointPort] = []
        error: bool = False
        get_current_span()

        logger.info(
            "Getting AccessPoint port info for {num} APs".format(
                num=len(Devices.access_points)
            ),
            extra={
                "devices": [item.mac for item in Devices.access_points]
            }
        )
        for ap in Devices.access_points:
            try:
                ap_port_response: dict = Connection.Request.get(
                    AccessPoint.__access_point_port_info_path, {
                        "apMac": ap.mac
                    }
                )
            except Exception as e:
                error = True
                logger.exception(
                    e,
                    exc_info=True,
                    extra={
                        "access_point_name": ap.name,
                        "access_point_mac": ap.mac
                    }
                )
                continue

            try:
                ap_port_object = Model.Ports.AccessPointPort(
                    **{
                        "accessPointName": ap.name,
                        "accessPointMac": ap.mac,
                        **ap_port_response.get("wiredUplink"),
                    }
                )
                access_point_port.append(
                    ap_port_object
                )
            except Exception as e:
                error = True
                logger.warning(
                    e,
                    exc_info=True,
                    extra={
                        "access_point_name": ap.name,
                        "access_point_mac": ap.mac
                    }
                )

        logger.info(
            "Found {num} AccessPoint ports".format(
                num=len(access_point_port)
            ),
            extra={
                "devices": [item.mac for item in Devices.access_points]
            }
        )
        set_current_span_status(error)
        return access_point_port

    @staticmethod
    @tracer.start_as_current_span("AccessPoint.get_radio_info")
    def get_radio_info() -> list[Model.Ports.AccessPointRadio]:

        access_point_radio: list[Model.Ports.AccessPointRadio] = []
        error: bool = False
        get_current_span()
        logger.info(
            "Getting AccessPoint radio info for {num} APs".format(
                num=len(Devices.access_points)
            ),
            extra={
                "devices": [item.mac for item in Devices.access_points]
            }
        )

        for ap in Devices.access_points:
            try:
                ap_radio_response: dict = Connection.Request.get(
                    AccessPoint.__access_point_radio_info_path, {
                        "apMac": ap.mac
                    }
                )
            except Exception as e:
                error = True
                logger.exception(
                    e,
                    exc_info=True,
                    extra={
                        "access_point_name": ap.name,
                        "access_point_mac": ap.mac
                    }
                )
                continue

            try:
                ap_radio_object = Model.Ports.AccessPointRadio(
                    **{
                        "accessPointName": ap.name,
                        "accessPointMac": ap.mac,
                        **ap_radio_response,
                    }
                )
                access_point_radio.append(
                    ap_radio_object
                )
            except Exception as e:
                logger.warning(
                    e,
                    exc_info=True,
                    extra={
                        "access_point_name": ap.name,
                        "access_point_mac": ap.mac
                    }
                )
        logger.info(
            "Found {num} AccessPoint radios".format(
                num=len(access_point_radio)
            ),
            extra={
                "devices": [item.mac for item in Devices.access_points]
            }
        )
        set_current_span_status(error)
        return access_point_radio
