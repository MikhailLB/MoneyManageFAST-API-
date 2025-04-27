from fastapi import HTTPException


class TokenExpiredException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=401, detail=detail)

class TokenInvalidException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=401, detail=detail)
