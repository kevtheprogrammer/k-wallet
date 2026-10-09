from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import (
    String,
    ForeignKey,
    Numeric,
    DateTime,
)
from sqlalchemy.orm import Mapped, mapped_column

from database.connection import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    nrc: Mapped[str] = mapped_column(
        String(30), unique=True, nullable=False
    )
    address: Mapped[str] = mapped_column(String(300), nullable=False)

    phone: Mapped[str] = mapped_column(
        String(20), unique=True, nullable=False
    )
    email: Mapped[str | None] = mapped_column(
        String(255), unique=True, nullable=True
    )

    # Store the hash, never the original PIN.
    pin_hash: Mapped[str] = mapped_column(String(255), nullable=False)


class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False, index=True
    )
    account_number: Mapped[str] = mapped_column(
        String(20), unique=True, nullable=False
    )
    account_type: Mapped[str] = mapped_column(
        String(20), nullable=False, default="PERSONAL"
    )
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="ACTIVE"
    )
    balance: Mapped[Decimal] = mapped_column(
        Numeric(12, 2), nullable=False, default=Decimal("0.00")
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    account_id: Mapped[int] = mapped_column(
        ForeignKey("accounts.id"), nullable=False, index=True
    )
    amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2), nullable=False
    )
    transaction_type: Mapped[str] = mapped_column(
        String(50), nullable=False
    )
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )


class Card(Base):
    __tablename__ = "cards"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False
    )
    card_number: Mapped[str] = mapped_column(
        String(16), unique=True, nullable=False
    )
    expiry_date: Mapped[str] = mapped_column(String(5), nullable=False)