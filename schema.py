from pydantic import BaseModel

class SupportRequest(BaseModel):
    question: str

class SupportResponse(BaseModel):
    answer: str
