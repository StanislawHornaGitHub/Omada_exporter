from pydantic import BaseModel, Field
import src.Omada.Model.Labels.Port as Port
import src.Omada.helpers.modelFields as modelFields


class SwitchPort(BaseModel):
    name: str = Field(alias="switchName")
    mac: str = Field(alias="switchMac")
    port: int
    portName: str = Field(alias="name")
    disable: str
    profileName: str
    operation: str
    linkStatus: str
    linkSpeed: str
    duplex: str
    poe: str
    tx: int
    rx: int

    def __init__(self, **data):
        if data["linkStatus"] == 0:
            data["linkSpeed"] = -1
            data["duplex"] = -1

        data["poe"] = str(data["poe"])
        data["disable"] = str(data["disable"])
        data = modelFields.map_data_values(data, Port.switch_value_map)
        super().__init__(**data)
