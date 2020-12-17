from pydantic import BaseModel


class SensorSuccessResponse(BaseModel):
    numRows: int
