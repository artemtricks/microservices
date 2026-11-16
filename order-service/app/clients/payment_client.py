import httpx


class PaymentClient:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url

    def create_payment(self, order_id: str, user_id: str, amount: int) -> dict:
        json_data = {"order_id": order_id, "user_id": user_id, "amount": amount}
        response = httpx.post(f"{self.base_url}/payment", json=json_data)
        return response.json()
