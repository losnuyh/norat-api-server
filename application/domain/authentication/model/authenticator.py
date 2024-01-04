from dataclasses import dataclass
import bcrypt


@dataclass
class PasswordAuthenticator:
    user_account: str
    hashed_password: bytes

    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(
            password.encode(),
            self.hashed_password,
        )


def new_password_authenticator(
    user_account: str,
    user_password: str,
) -> PasswordAuthenticator:
    hashed_password = bcrypt.hashpw(
        user_password.encode(),
        bcrypt.gensalt(14),
    )
    return PasswordAuthenticator(
        user_account=user_account,
        hashed_password=hashed_password,
    )
