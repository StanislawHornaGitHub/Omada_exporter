from pydantic import BaseModel, Field
import src.Omada.Model.Labels.Port as Port
import src.Omada.helpers.modelFields as modelFields


class AccessPointPort(BaseModel):
    name: str = Field(alias="accessPointName")
    mac: str = Field(alias="accessPointMac")
    uplinkMac: str = Field(default=None)
    uplinkDeviceType: str = Field(alias="type", default=None)
    linkSpeed: str = Field(alias="rate", default=None)
    duplex: str = Field(default=None)
    tx: int = Field(alias="upBytes", default=0)
    rx: int = Field(alias="downBytes", default=0)

    def __init__(self, **data):
        data = modelFields.map_data_values(data, Port.access_point_value_map)
        super().__init__(**data)
