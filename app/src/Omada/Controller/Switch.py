import src.Omada.Model as Model
import src.Omada.Connection as Connection
from src.Omada.Controller.Devices import Devices
from src.Observability import *

tracer = trace.get_tracer("Switch-tracer")


class Switch:

    __switch_info_path: str = "/openapi/v1/{omadacId}/sites/{siteId}/switches/{switchMac}"
    __switch_port_stats_path: str = "/api/v2/sites/{siteId}/stat/switches/{switchMac}/5min"
    __switch_port_info_path: str = "/api/v2/sites/{siteId}/switches/{switchMac}/ports"

    @staticmethod
    @tracer.start_as_current_span("Switch.get_info")
    def get_info() -> list[Model.Switch]:

        switch_devices: list[Model.Switch] = []
        error: bool = False
        get_current_span()
        logger.info(
            "Getting Switch info",
            extra={
                "devices": [item.mac for item in Devices.switches]
            }
        )

        for switch in Devices.switches:
            try:
                switch_info: dict = Connection.Request.get(
                    Switch.__switch_info_path, {
                        "switchMac": switch.mac
                    }
                )
                switch_object = Model.Switch(
                    **{
                        "name": switch.name,
                        **switch_info
                    }
                )
                switch_devices.append(
                    switch_object
                )
            except Exception as e:
                error = True
                logger.exception(
                    e,
                    exc_info=True,
                    extra={
                        "switch_name": switch.name,
                        "switch_mac": switch.mac
                    }
                )

        set_current_span_status(error)
        return switch_devices

    @staticmethod
    @tracer.start_as_current_span("Switch.get_port_info")
    def get_port_info() -> list[Model.Ports.SwitchPort]:

        switch_port_result: list[Model.Ports.SwitchPort] = []
        error: bool = False
        get_current_span()

        logger.info(
            "Getting Switch port info for {num} Switches".format(
                num=len(Devices.switches)
            ),
            extra={
                "devices": [item.mac for item in Devices.switches]
            }
        )

        for switch in Devices.switches:
            try:
                switch_port_response: list[dict] = Connection.Request.get(
                    Switch.__switch_port_info_path, {
                        "switchMac": switch.mac
                    }
                )
            except Exception as e:
                error = True
                logger.exception(
                    e,
                    exc_info=True,
                    extra={
                        "switch_name": switch.name,
                        "switch_mac": switch.mac
                    }
                )
                continue

            for port in switch_port_response:
                try:
                    switch_port_details: dict = Switch.__get_port_detail(port)
                    switch_port_object = Model.Ports.SwitchPort(
                        **{
                            **switch_port_details,
                            "switchName": switch.name
                        }
                    )
                    switch_port_result.append(
                        switch_port_object
                    )
                except Exception as e:
                    error = True
                    logger.warning(
                        e,
                        exc_info=True,
                        extra={
                            "switch_name": switch.name,
                            "switch_mac": switch.mac,
                            "port": port.get("port", None)
                        }
                    )

        logger.info(
            "Found {num} switch ports".format(
                num=len(switch_port_result)
            ),
            extra={
                "devices": [item.mac for item in Devices.switches]
            }
        )
        set_current_span_status(error)
        return switch_port_result

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
