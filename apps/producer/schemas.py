from typing import Dict

from pydantic import BaseModel

class IncomingMessage(BaseModel):
    taskid: str
    description: str
    params: Dict[str, str]