
from pydantic import BaseModel, Field

class HelpRequest(BaseModel):
    prompt: str = Field(default="Here is the input prompt")