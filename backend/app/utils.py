import secrets

from sqlalchemy.orm import Session

from .models import Meeting


def generate_meeting_code(db: Session) -> str:
    while True:
        code = str(secrets.randbelow(9 * 10**10) + 10**10)

        if not db.query(Meeting).filter_by(meeting_code=code).first():
            return code


def generate_passcode() -> str:
    return secrets.token_hex(3)


def generate_token() -> str:
    return secrets.token_urlsafe(24)


def format_meeting_code(code: str) -> str:
    if len(code) != 11:
        return code

    return f"{code[:3]} {code[3:7]} {code[7:]}"


def build_invite_link(
    frontend_url: str,
    code: str,
    passcode: str,
) -> str:
    return f"{frontend_url}/j/{code}?pwd={passcode}"