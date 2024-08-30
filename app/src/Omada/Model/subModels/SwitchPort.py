from pydantic import BaseModel, Field
import src.Omada.helpers.modelFields as modelFields

value_map: dict[str, dict] = {
    "poeMode": {
        0: "off",
        1: "on(802.3at/af)",
    },
    "status": {
        0: "off",
        1: "on",
        None: None
    }
}


class SwitchPort(BaseModel):
    port: int
    port_name: str = Field(alias="name")
    profileId: str
    profileName: str
    profileOverrideEnable: bool
    poeMode: str
    lagPort: bool
    status: str = Field(default="lag_port")

    def __init__(self, **data):
        data = modelFields.map_data_values(data, value_map)
        super().__init__(**data)
