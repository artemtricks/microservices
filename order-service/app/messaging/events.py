from datetime import UTC, datetime
from uuid import uuid4


def build_order_paid_event(
    user_id: str,
    order_id: str,
) -> dict:
    return {
        "event_id": str(uuid4()),
        "created_at": datetime.now(UTC).isoformat(),
        "user_id": user_id,
        "order_id": order_id,
    }
