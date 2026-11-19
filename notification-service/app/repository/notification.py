from app.models import NotificationModel
from app.schemas import NotificationCreateSchema
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


class NotificationRepository:
    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
    ) -> None:
        self.session_factory = session_factory

    async def get_all(self, db: AsyncSession) -> list[NotificationModel]:

        result = await db.scalars(select(NotificationModel))
        return list(result.all())

    async def get_one(
        self, db: AsyncSession, notification_id: str
    ) -> NotificationModel | None:

        return await db.get(NotificationModel, notification_id)

    async def create(
        self, db: AsyncSession, payload: NotificationCreateSchema
    ) -> NotificationModel:

        new_notification = NotificationModel(
            order_id=payload.order_id,
            user_id=payload.user_id,
            message=payload.message,
        )
        db.add(new_notification)
        await db.flush()

        return new_notification
