from typing import Optional

import uvicorn
from fastapi import FastAPI
from person.domain.driver.factory import get_manager
from person.domain.driver.ports import PersonManager
from person.domain.model import PersonOperationRequestDto, PersonOperationResponseDto, Person

app = FastAPI()


class Adapter(PersonManager):
    def handle_save(self, rq: PersonOperationRequestDto) -> PersonOperationResponseDto:
        return get_manager().handle_save(rq)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/person/save/")
def save_person(name: str,
                surname: str,
                first_child: Optional[PersonOperationRequestDto] = None,
                partner: Optional[PersonOperationRequestDto] = None,
                right_sibling: Optional[PersonOperationRequestDto] = None) -> PersonOperationResponseDto:
    dto = PersonOperationRequestDto()
    dto.name = name
    dto.surname = surname
    dto.first_child = first_child
    dto.partner = partner
    dto.right_sibling = right_sibling

    result = Adapter().handle_save(dto)
    return result


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
