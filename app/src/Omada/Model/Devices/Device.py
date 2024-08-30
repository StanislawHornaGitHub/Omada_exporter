from pydantic import BaseModel, Field, field_serializer
import datetime
import src.Omada.helpers.timeFunctions as timeHelpers

import src.Omada.helpers.modelFields as modelFields

value_map: dict[str, dict] = {
    "status": {
        0: "Disconnected",
        1: "Connected",
        2: "Pending",
        3: "Heartbeat Missed",
        4: "Isolated",
    }
}


class Device(BaseModel):

    mac: str
    name: str
    type: str
    model: str
    ip: str
    uptime: str
    status: str
    lastSeen: datetime.datetime
    cpuUtil: int
    memUtil: int
    tagName: str = Field(default=None)

    def __init__(self, **data):

        data["lastSeen"] = timeHelpers.get_last_seen(data["lastSeen"])
        data = modelFields.map_data_values(data,value_map)

        super().__init__(**data)

    @field_serializer('lastSeen')
    def serialize_lastSeen(self, lastSeen: datetime.datetime, _info) -> str:
        return timeHelpers.datetime_to_string(lastSeen)
