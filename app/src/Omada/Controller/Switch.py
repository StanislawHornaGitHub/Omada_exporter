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
    def get_port_info() -> list[Model.Ports.SwitchPort]:

        switch_port: list[Model.Ports.SwitchPort] = []

        for switch in Devices.switches:
            switch_port_response: dict = Connection.Request.get(
                Switch.__switch_port_info_path, {
                    "switchMac": switch.mac
                }
            )

            for port in switch_port_response:
                try:
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
                except:
                    pass

        return switch_port

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
