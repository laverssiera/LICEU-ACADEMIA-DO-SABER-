from nats.aio.client import Client as NATS
import json
import os


class FederationRuntime:
    def __init__(self):
        self.nc = NATS()

    async def connect(self):
        await self.nc.connect(servers=[os.getenv("NATS_URL")])
        print("ACADEMIA conectada a Federacao LICEU")

    async def publish(self, subject: str, payload: dict):
        await self.nc.publish(subject, json.dumps(payload).encode())


federation_runtime = FederationRuntime()