from datetime import datetime
from sqlalchemy import BigInteger, String, Boolean, DateTime, Integer, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=True)
    first_name: Mapped[str] = mapped_column(String, nullable=True)
    language: Mapped[str] = mapped_column(String, default="uz")
    joined_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    subscribed_channel: Mapped[bool] = mapped_column(Boolean, default=False)
    watched_free_lesson: Mapped[bool] = mapped_column(Boolean, default=False)
    registered_webinar: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Tariff info
    tariff: Mapped[str] = mapped_column(String, nullable=True)  # LITE, PRO, VIP
    payment_status: Mapped[str] = mapped_column(String, default="none")  # none, partial, full
    payment_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    
    # Seminar access
    seminar_access_code: Mapped[str] = mapped_column(String, nullable=True)  # SEM-XXXX
    seminar_payment_confirmed: Mapped[bool] = mapped_column(Boolean, default=False)

class Payment(Base):
    __tablename__ = 'payments'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.user_id'))
    tariff: Mapped[str] = mapped_column(String)  # LITE, PRO, VIP
    amount: Mapped[int] = mapped_column(Integer)
    type: Mapped[str] = mapped_column(String)  # full, partial_1, partial_2
    status: Mapped[str] = mapped_column(String, default="pending")  # pending, confirmed, rejected
    receipt_photo: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class UserProgress(Base):
    __tablename__ = "user_progress"
    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    current_lesson: Mapped[str] = mapped_column(String, default="0.1")
    completed_lessons: Mapped[str] = mapped_column(String, default="[]") # JSON string of list
    homework_status: Mapped[str] = mapped_column(String, default="none") # none, submitted, approved, rejected
    homework_lesson: Mapped[str] = mapped_column(String, nullable=True)
    homework_file_id: Mapped[str] = mapped_column(String, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
