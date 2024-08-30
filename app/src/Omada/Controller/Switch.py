import datetime
import src.Omada.Model as Model
import src.Omada.Connection as Connection
from src.Omada.Controller.Devices import Devices


class Switch:

    __switch_info_path: str = "/openapi/v1/{omadacId}/sites/{siteId}/switches/{switchMac}"
    __switch_port_stats_path: str = "/api/v2/sites/{siteId}/stat/switches/{switchMac}/5min"
    __switch_port_info_path: str = "/api/v2/sites/{siteId}/switches/{switchMac}/ports"

    @staticmethod
    def get_info() -> list[Model.Switch]:

        result = [
            Model.Switch(
                **{
                    "name": item.name,
                    **Connection.Request.get(
                        Switch.__switch_info_path, {
                            "switchMac": item.mac
                        }
                    )
                }
            )
            for item in Devices.switches
        ]
        return result

    @staticmethod
    def get_port_info() -> tuple[list[Model.Ports.SwitchPort], list[Model.Ports.SwitchPortStats]]:

        switch_port: list[Model.Ports.SwitchPort] = []
        switch_port_stats: list[Model.Ports.SwitchPortStats] = []

        for switch in Devices.switches:
            switch_port_response: dict = Connection.Request.get(
                Switch.__switch_port_info_path, {
                    "switchMac": switch.mac
                }
            )

            for port in switch_port_response:
                switch_port.append(
                    Model.Ports.SwitchPort(
                        **(
                            {
                                **Switch.__get_port_detail(port),
                                "switchName": switch.name
                            }
                        )
                    )
                )
            switch_port_stats = switch_port_stats + Switch.__get_port_stats(
                switch.mac, switch.name, len(switch_port_response)
            )

        return switch_port, switch_port_stats

    @staticmethod
    def __get_port_stats(switch_mac: str, switch_name: str, port_count: int):

        switch_port_stats: list[Model.Ports.SwitchPortStats] = []

        current_time = int(datetime.datetime.now().timestamp())
        switch_port_stats_response: dict = Connection.Request.post(
            Switch.__switch_port_stats_path, {
                "switchMac": switch_mac
            },
            {
                "attrs": [
                    "txRate",
                    "rxRate"
                ],
                "ports": list(range(1, port_count +1)),
                "start": current_time - 301,
                "end":   current_time
            }
        ).get("statList")[-1]

        for stats in switch_port_stats_response.get("ports"):
            try:
                switch_port_stats.append(
                    Model.Ports.SwitchPortStats(
                        **(
                            {
                                **stats,
                                "switchMac": switch_mac,
                                "switchName": switch_name
                            }
                        )
                    )
                )
            except:
                pass

        return switch_port_stats

    @staticmethod
    def __get_port_detail(port: dict):
        '''
        Put contents of port status to depth level 0 in JSON struct.
        Convert this:
            {
                "port": 1,
                "profileName": "All",
                "portStatus": {
                    "port": 1,
                    "linkStatus": 1,
                    "linkSpeed": 2,
                    "duplex": 2,
                    "poe": false,
                    "tx": 16826893482,
                    "rx": 488690848,
                    "stpDiscarding": false
                }
            }

        To this:
            {
                "port": 1,
                "profileName": "All",
                "linkStatus": 1,
                "linkSpeed": 2,
                "duplex": 2,
                "poe": false,
                "tx": 16826893482,
                "rx": 488690848,
                "stpDiscarding": false
            }
        '''
        port_status: dict = port["portStatus"]
        return {
            **port,
            **({k: v for k, v in port_status.items()})
        }
