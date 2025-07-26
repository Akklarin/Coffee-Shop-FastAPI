from datetime import datetime, timedelta, timezone
from sqlalchemy import delete, select

from src.users.models import User, ValidationCode
from src.core.database import SessionLocal
from worker import celery_app


@celery_app.task(name="delete_unverified_users")
def delete_unverified_users():
    two_days_ago = datetime.now(timezone.utc) - timedelta(days=2)

    stale_emails_subq = (
        select(ValidationCode.email)
        .where(ValidationCode.created_at < two_days_ago)
        .subquery()
    )

    stmt = (
        delete(User)
        .where(User.is_verified.is_(False))
        .where(User.email.in_(select(stale_emails_subq.c.email)))
    )

    with SessionLocal() as sync_session:
        result = sync_session.execute(stmt)
        sync_session.commit()
        print(f"[celery] Deleted {result.rowcount} unverified users")
