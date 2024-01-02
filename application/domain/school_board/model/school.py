from dataclasses import dataclass


@dataclass(kw_only=True)
class SchoolVO:
    school_code: str  # SD_SCHUL_CODE
    name: str  # SCHUL_NM
    address: str  # ORG_RDNMA
