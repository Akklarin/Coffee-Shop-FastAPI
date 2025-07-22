from datetime import datetime, timedelta, timezone
from sqlalchemy import delete

from src.users.models import User
from src.core.database import get_session
from worker import celery_app


@celery_app.task(name="delete_unverified_users")
def delete_unverified_users():
    import asyncio
    asyncio.run(_delete_unverified_users_async())


async def _delete_unverified_users_async():
    async with get_session() as session:
        two_days_ago = datetime.now(timezone.utc) - timedelta(days=2)

        stmt = (
            delete(User)
            .where(User.is_verified.is_(False))
            .where(User.created_at < two_days_ago)
        )

        result = await session.execute(stmt)
        await session.commit()
        print(f"Deleted {result.rowcount} unverified users")
