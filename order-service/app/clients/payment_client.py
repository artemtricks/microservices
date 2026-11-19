import httpx


class PaymentClient:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url
        self.client: httpx.AsyncClient

    async def start(self):
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=10.0,
        )

    async def close(self):
        if self.client:
            await self.client.aclose()

    async def create_payment(
        self,
        order_id: str,
        user_id: str,
        amount: int,
    ) -> dict:

        response = await self.client.post(
            "/payment",
            json={
                "order_id": order_id,
                "user_id": user_id,
                "amount": amount,
            },
        )

        response.raise_for_status()

        return response.json()
