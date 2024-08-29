import src.Omada.Model as Model
import src.Omada.Connection as Connection
import src.Prometheus as Prometheus


class Devices:
    gateways: list[Model.Device]
    switches: list[Model.Device]
    access_points: list[Model.Device]

    __device_list_path: str = "/openapi/v1/{omadacId}/sites/{siteId}/devices"

    @staticmethod
    def init() -> None:
        Devices.get_list()

    @staticmethod
    def get_list() -> Model.Device:
        response: dict = Connection.Request.get(Devices.__device_list_path)
        devices: list[Model.Device] = [
            Model.Device(**item)
            for item in response
        ]
        Devices.__update_device_cache(devices)

        return devices

    @staticmethod
    def __update_device_cache(devices: list[Model.Device]):
        Devices.gateways = [item for item in devices if item.type == "gateway"]
        Devices.switches = [item for item in devices if item.type == "switch"]
        Devices.access_points = [item for item in devices if item.type == "ap"]

Devices.init()
