from fastapi import Request


def get_notification_service(request: Request):
    """Функция для инъекции зависимости NotificationService"""
    return request.app.state.notification_service
