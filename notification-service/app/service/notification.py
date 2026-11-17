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
        notifications_orm = await self.notification_repository.get_all()
        return [
            NotificationReadSchema.model_validate(notification)
            for notification in notifications_orm
        ]

    async def get(self, notification_id: str) -> NotificationReadSchema:
        notification_orm = await self.notification_repository.get_one(notification_id)
        if not notification_orm:
            raise HTTPException(404, f"Notification id {notification_id} not found")

        return NotificationReadSchema.model_validate(notification_orm)

    async def create(self, payload: NotificationCreateSchema) -> NotificationReadSchema:
        async with self.session_factory() as db:
            notification_orm = await self.notification_repository.create(
                payload=payload
            )
            await db.commit()
            return NotificationReadSchema.model_validate(notification_orm)

    # async def complete_notification(
    #     self,
    #     notification: NotificationModel,
    #     exchange: AbstractExchange,
    #     amount: int,
    #     order_id: str,
    # ) -> NotificationReadSchema:
    #     await asyncio.sleep(4)
    #     notification.status = "succeeded"

    #     await self.db.commit()

    #     event = build_notification_succeeded_event(
    #         notification_id=notification.id, order_id=order_id, amount=amount
    #     )
    #     await event_publish_json(
    #         exchange=exchange,
    #         routing_key=settings.notification_succeeded_routing_key,
    #         data=event,
    #     )

    #     return NotificationReadSchema.model_validate(notification)
