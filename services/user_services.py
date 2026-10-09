
import re
import secrets

import bcrypt
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from database.connection import SessionLocal
from database.models import User, Account


def hash_pin(pin: str) -> str:
    if not re.fullmatch(r"\d{4}", pin):
        raise ValueError("PIN must contain exactly 4 digits.")

    return bcrypt.hashpw(
        pin.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")


def generate_account_number(session) -> str:
    while True:
        number = str(secrets.randbelow(9_000_000_000) + 1_000_000_000)

        existing = session.scalar(
            select(Account.id).where(
                Account.account_number == number
            )
        )

        if existing is None:
            return number


def register_user(
    first_name: str,
    last_name: str,
    nrc: str,
    address: str,
    phone: str,
    pin: str,
    email: str | None = None,
) -> dict:
    # Basic input validation
    first_name = first_name.strip()
    last_name = last_name.strip()
    nrc = nrc.strip()
    address = address.strip()
    phone = phone.strip()
    email = email.strip().lower() if email else None

    if not all([first_name, last_name, nrc, address, phone]):
        raise ValueError("Please complete all required fields.")

    if email and not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        raise ValueError("Please enter a valid email address.")

    pin_hash = hash_pin(pin)

    with SessionLocal() as session:
        try:
            # Check identifiers before creating the user
            if session.scalar(
                select(User.id).where(User.phone == phone)
            ):
                raise ValueError("This phone number is already registered.")

            if session.scalar(
                select(User.id).where(User.nrc == nrc)
            ):
                raise ValueError("This NRC is already registered.")

            if email and session.scalar(
                select(User.id).where(User.email == email)
            ):
                raise ValueError("This email is already registered.")

            user = User(
                first_name=first_name,
                last_name=last_name,
                nrc=nrc,
                address=address,
                phone=phone,
                email=email,
                pin_hash=pin_hash,
            )

            session.add(user)
            session.flush()  # Assigns user.id without committing

            account = Account(
                user_id=user.id,
                account_number=generate_account_number(session),
                account_type="PERSONAL",
                status="ACTIVE",
            )

            session.add(account)
            session.flush()

            result = {
                "user_id": user.id,
                "account_number": account.account_number,
                "full_name": f"{user.first_name} {user.last_name}",
            }

            session.commit()
            return result

        except Exception:
            session.rollback()
            raise
