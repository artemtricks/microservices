from app.api.dependencies import get_notification_service
from app.schemas import NotificationCreateSchema, NotificationReadSchema
from app.service.notification import NotificationService
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/notification")
async def get_all_notifications(
    notification_service: NotificationService = Depends(get_notification_service),
) -> list[NotificationReadSchema]:
    return await notification_service.get_all()


@router.get("/notification/{notification_id}")
async def get_notification(
    notification_id: str,
    notification_service: NotificationService = Depends(get_notification_service),
) -> NotificationReadSchema:
    return await notification_service.get(notification_id)


@router.post("/notification")
async def create_notification(
    payload: NotificationCreateSchema,
    notification_service: NotificationService = Depends(get_notification_service),
) -> NotificationReadSchema:
    return await notification_service.create(payload)
