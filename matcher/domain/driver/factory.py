from matcher.application.use_cases import MatchSiblingsUseCase
from matcher.domain.driver.ports import MatcherManager
from matcher.domain.model import MatcherOperationResponseDto
from matcher.infrastructure.factory import create_mongo_matcher_manager
from person.domain.model import PersonOperationRequestDto, person_from_dto, person_to_dto


def get_manager() -> MatcherManager:
    return DefaultManager()


class DefaultManager(MatcherManager):
    def handle_match_siblings(self, rq: PersonOperationRequestDto) -> MatcherOperationResponseDto:
        person = person_from_dto(rq)
        res = MatcherOperationResponseDto()

        try:
            matches = MatchSiblingsUseCase(manager=create_mongo_matcher_manager()).execute(person=person)
            parsed_matches = []
            if matches:
                for person in matches:
                    parsed_matches.append(person_to_dto(person))
            res.matches = parsed_matches
        except Exception as e:
            print("Exception: ", e)
            res.error = e
            res.error_code = 500

        return res
