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

    async def get_all(self) -> list[NotificationModel]:
        async with self.session_factory() as db:
            result = await db.scalars(select(NotificationModel))
            return list(result.all())

    async def get_one(self, notification_id: str) -> NotificationModel | None:
        async with self.session_factory() as db:
            return await db.get(NotificationModel, notification_id)

    async def create(self, payload: NotificationCreateSchema) -> NotificationModel:
        async with self.session_factory() as db:
            new_notification = NotificationModel(
                order_id=payload.order_id,
                user_id=payload.user_id,
                message=payload.message,
            )
            db.add(new_notification)

            return new_notification
