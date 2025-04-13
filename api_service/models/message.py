from sqlmodel import SQLModel


class MessageResponse(SQLModel):
    message: str
    

class ErrorDetail(SQLModel):
    detail: str