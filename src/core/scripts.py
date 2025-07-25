import asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.models import User
from src.core.database import AsyncSessionLocal
from .config import settings
from .security import hash_password


async def seed_admin(session: AsyncSession):
    result = await session.execute(select(User).where(User.email == settings.ADMIN_EMAIL))
    admin = result.scalar_one_or_none()

    if not admin:
        admin = User(
            email=settings.ADMIN_EMAIL,
            password_hash=hash_password(settings.ADMIN_PASSWORD),
            role="admin",
            is_verified=True,
        )
        session.add(admin)
        await session.commit()


if __name__ == "__main__":
    async def main():
        async with AsyncSessionLocal() as session:
            await seed_admin(session)

    asyncio.run(main())
