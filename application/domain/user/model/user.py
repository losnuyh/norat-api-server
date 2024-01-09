from dataclasses import dataclass
from datetime import date, datetime


@dataclass(kw_only=True)
class User:
    id: int | None = None
    account: str
    phone: str
    birth: date

    def get_current_age(self):
        current_year = datetime.now().year
        birth_year = self.birth.year
        return current_year - birth_year


@dataclass(kw_only=True)
class Guardian:
    child_id: int
    name: str
    birth: date
    ci: str
    di: str
