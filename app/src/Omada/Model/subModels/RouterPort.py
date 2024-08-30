from pydantic import BaseModel, Field
import src.Omada.helpers.modelFields as modelFields


value_map: dict[str, dict] = {
    "linkSpeed": {
        0: "Auto",
        1: "10M",
        2: "100M",
        3: "1000M",
        4: "2500M",
        5: "10G",
        6: "5G",
    },

    "duplex": {
        0: "Auto",
        1: "Half",
        2: "Full",
    },

    "mirrorMode": {
        0: "ingress",
        1: "egress",
        2: "ingress and egress",
    },
}


class RouterPort(BaseModel):
    port: int
    linkSpeed: str
    duplex: str
    mirrorEnable: bool = Field(default=False)
    mirroredPorts: list[int] = Field(default=None)
    mirrorMode: str = Field(default=None)
    pvid: int | str = Field(default="wan")

    def __init__(self, **data):
        data = modelFields.map_data_values(data, value_map)
        super().__init__(**data)
