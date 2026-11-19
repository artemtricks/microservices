from app.repository.notification import NotificationRepository
from app.schemas import NotificationCreateSchema, NotificationReadSchema
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


class NotificationService:
    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
    ) -> None:
        self.session_factory = session_factory
        self.notification_repository = NotificationRepository(session_factory)

    async def get_all(
        self,
    ) -> list[NotificationReadSchema]:
        async with self.session_factory() as db:
            notifications_orm = await self.notification_repository.get_all(db=db)
            for notification in notifications_orm:
                if notification.is_read == False:
                    notification.is_read = True
            await db.commit()
            return [
                NotificationReadSchema.model_validate(notification)
                for notification in notifications_orm
            ]

    async def get(self, notification_id: str) -> NotificationReadSchema:
        async with self.session_factory() as db:
            notification_orm = await self.notification_repository.get_one(
                db=db, notification_id=notification_id
            )
            if not notification_orm:
                raise HTTPException(404, f"Notification id {notification_id} not found")
            if notification_orm.is_read == False:
                notification_orm.is_read = True
                await db.commit()

            return NotificationReadSchema.model_validate(notification_orm)

    async def create(self, payload: NotificationCreateSchema) -> NotificationReadSchema:
        async with self.session_factory() as db:
            notification_orm = await self.notification_repository.create(
                db=db, payload=payload
            )
            await db.commit()
            await db.refresh(notification_orm)
            return NotificationReadSchema.model_validate(notification_orm)
