from dataclasses import dataclass


@dataclass
class PreSignedUrl:
    pre_signed_url: str
    key: str
