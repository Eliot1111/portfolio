"""Persistent statistics for successful logins, available to administrators."""

from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import DateTime, ForeignKey, func, select
from sqlalchemy.orm import Mapped, Session, mapped_column

from app.database import Base
from app.dependencies import get_db, require_admin
from app.models import User


class LoginEvent(Base):
    __tablename__ = "login_events"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    logged_in_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None)
    )


class UserLoginStats(BaseModel):
    user_id: int
    username: str
    login_count: int
    last_login_at: datetime | None


class LoginStatsResponse(BaseModel):
    total_logins: int
    unique_users: int
    users: list[UserLoginStats]


router = APIRouter(prefix="/admin", tags=["Statistics"])


def record_successful_login(db: Session, user_id: int) -> None:
    db.add(LoginEvent(user_id=user_id))
    db.commit()


@router.get("/login-stats", response_model=LoginStatsResponse)
def read_login_stats(
    _: User = Depends(require_admin),
    db: Session = Depends(get_db),
) -> LoginStatsResponse:
    """Count successful logins since tracking began, including users with none."""
    rows = db.execute(
        select(
            User.id,
            User.username,
            func.count(LoginEvent.id),
            func.max(LoginEvent.logged_in_at),
        )
        .outerjoin(LoginEvent, LoginEvent.user_id == User.id)
        .group_by(User.id, User.username)
        .order_by(User.id)
    ).all()
    users = [
        UserLoginStats(
            user_id=user_id,
            username=username,
            login_count=count,
            # SQLite stores UTC without an offset; expose explicit UTC in JSON.
            last_login_at=last_login.replace(tzinfo=timezone.utc)
            if last_login is not None
            else None,
        )
        for user_id, username, count, last_login in rows
    ]
    return LoginStatsResponse(
        total_logins=sum(user.login_count for user in users),
        unique_users=sum(user.login_count > 0 for user in users),
        users=users,
    )
