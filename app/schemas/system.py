from typing import Literal

from pydantic import BaseModel


class SystemInfoResponse(BaseModel):
    app_name: str
    version: str
    environment: Literal["development", "staging", "production"]
    debug: bool
