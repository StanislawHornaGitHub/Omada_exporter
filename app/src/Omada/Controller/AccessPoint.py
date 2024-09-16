import datetime
import src.Omada.Model as Model
import src.Omada.Connection as Connection
from src.Omada.Controller.Devices import Devices


class AccessPoint:
    __access_point_info_path: str = "/openapi/v1/{omadacId}/sites/{siteId}/aps/{apMac}"
    __access_point_port_info_path: str = "/openapi/v1/{omadacId}/sites/{siteId}/aps/{apMac}/wired-uplink"
    __access_point_radio_info_path: str = "/openapi/v1/{omadacId}/sites/{siteId}/aps/{apMac}/radios"
    __access_point_radio_stats_path: str = "/api/v2/sites/{siteId}/stat/{apMac}/5min?type=ap"

    @staticmethod
    def get_info() -> list[Model.AccessPoint]:

        result = [
            Model.AccessPoint(
                **Connection.Request.get(
                    AccessPoint.__access_point_info_path, {
                        "apMac": item.mac
                    }
                )
            )
            for item in Devices.access_points
        ]
        return result

    @staticmethod
    def get_port_info() -> list[Model.Ports.AccessPointPort]:
        access_point_port: list[Model.Ports.AccessPointPort] = []

        for ap in Devices.access_points:
            ap_port_response: dict = Connection.Request.get(
                AccessPoint.__access_point_port_info_path, {
                    "apMac": ap.mac
                }
            )
            try:
                access_point_port.append(
                    Model.Ports.AccessPointPort(
                        **(
                            {
                                "accessPointName": ap.name,
                                "accessPointMac": ap.mac,
                                **ap_port_response.get("wiredUplink"),
                            }
                        )
                    )
                )
            except:
                pass

        return access_point_port

    @staticmethod
    def get_radio_info() -> list[Model.Ports.AccessPointRadio]:
        access_point_radio: list[Model.Ports.AccessPointRadio] = []

        for ap in Devices.access_points:
            ap_radio_response: dict = Connection.Request.get(
                AccessPoint.__access_point_radio_info_path, {
                    "apMac": ap.mac
                }
            )

            access_point_radio.append(
                Model.Ports.AccessPointRadio(
                    **(
                        {
                            "accessPointName": ap.name,
                            "accessPointMac": ap.mac,
                            **ap_radio_response,
                        }
                    )
                )
            )

        return access_point_radio