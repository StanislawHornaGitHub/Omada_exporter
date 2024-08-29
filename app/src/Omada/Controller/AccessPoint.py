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
    def get_port_info():
        access_point_port: list[Model.Ports.AccessPointPort] = []

        for ap in Devices.access_points:
            ap_port_response: dict = Connection.Request.get(
                AccessPoint.__access_point_port_info_path, {
                    "apMac": ap.mac
                }
            )

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

        return access_point_port

    @staticmethod
    def get_radio_info():
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

    @staticmethod
    def get_radio_stats():
        access_point_radio_stat: list[Model.Ports.AccessPointRadioStats] = []
        current_time = int(datetime.datetime.now().timestamp())
        for ap in Devices.access_points:
            ap_radio_response: dict = Connection.Request.post(
                AccessPoint.__access_point_radio_stats_path, {
                    "apMac": ap.mac
                },
                {
                    "attrs": [
                        "tx2g",
                        "rx2g",
                        "tx5g",
                        "rx5g",
                        "rxRetryPkts2g",
                        "txRetryPkts2g",
                        "rxRetryPkts5g",
                        "txRetryPkts5g",
                    ],
                    "start": current_time - 301,
                    "end":   current_time
                }
            )[-1]
            try:
                access_point_radio_stat.append(
                    Model.Ports.AccessPointRadioStats(
                        **{
                            "accessPointName": ap.name,
                            "accessPointMac": ap.mac,
                            "frequency": "2.4 GHz",
                            **ap_radio_response.get("traffic2g")
                        }
                    )
                )
            except:
                pass
            try:
                access_point_radio_stat.append(
                    Model.Ports.AccessPointRadioStats(
                        **{
                            "accessPointName": ap.name,
                            "accessPointMac": ap.mac,
                            "frequency": "5 GHz",
                            **ap_radio_response.get("traffic5g")
                        }
                    )
                )
            except:
                pass
        return access_point_radio_stat
