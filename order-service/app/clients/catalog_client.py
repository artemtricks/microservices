import httpx


class CatalogClient:
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

    async def get_product(self, product_id: str) -> dict:
        # response = httpx.get(f"{self.base_url}/products/{product_id}")
        # return response.json()

        response = await self.client.get(f"/products/{product_id}")
        response.raise_for_status()
        return response.json()
