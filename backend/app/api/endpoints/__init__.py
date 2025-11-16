import enum 
from fastapi import HTTPException

class TimeFrame(enum.Enum):
    ONE_MONTH = "1m"
    SIX_MONTH = "6m"
    ONE_YEAR = "1y"


class HarkonnenException(HTTPException):
    def __init__(self, status_code: int, error_code: str, message: str, context: dict = None):
        detail = {
            "error_code": error_code,
            "message": message
        }
        if context:
            detail["context"] = context

        super().__init__(status_code=status_code, detail=detail)
