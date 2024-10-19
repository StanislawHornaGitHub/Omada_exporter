import src.Omada.Model as Model
import src.Omada.Connection as Connection
from src.Observability import *

tracer = trace.get_tracer("Device-tracer")


class Devices:
    gateways: list[Model.Device]
    switches: list[Model.Device]
    access_points: list[Model.Device]

    __device_list_path: str = "/openapi/v1/{omadacId}/sites/{siteId}/devices"

    @staticmethod
    @tracer.start_as_current_span("Device.init")
    def init() -> None:
        get_current_span()

        try:
            Devices.get_list()
        except Exception as e:
            logger.exception("Cannot fetch device list", exc_info=True)
        else:
            set_current_span_status()

        return None

    @staticmethod
    @tracer.start_as_current_span("Device.get_list")
    def get_list() -> Model.Device:

        get_current_span()
        try:
            response: dict = Connection.Request.get(Devices.__device_list_path)
            devices: list[Model.Device] = [Model.Device(**item) for item in response]
        except Exception as e:
            logger.exception(e, exc_info=True)
            raise e
        else:
            logger.info("Found {num} devices".format(num=len(devices)))
            Devices.__update_device_cache(devices)
            set_current_span_status()

        return devices

    @staticmethod
    def __update_device_cache(devices: list[Model.Device]):
        Devices.gateways = [item for item in devices if item.type == "gateway"]
        logger.info("Gateways: {num}".format(num=len(Devices.gateways)))

        Devices.switches = [item for item in devices if item.type == "switch"]
        logger.info("Switches: {num}".format(num=len(Devices.switches)))

        Devices.access_points = [item for item in devices if item.type == "ap"]
        logger.info("Access Points: {num}".format(num=len(Devices.access_points)))


Devices.init()
