from typing import List

from pydantic import BaseModel

from person.domain.model import PersonOperationRequestDto


class MatcherOperationResponseDto(BaseModel):
    error_code: int = None
    error: str = None
    matches: List[PersonOperationRequestDto] = None
