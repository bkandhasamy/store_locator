import aioredis
import json

redis = aioredis.from_url("redis://redis:6379", decode_responses=True)


async def get_from_cache(key: str):
    value = await redis.get(key)
    if value:
        return json.loads(value)


async def set_in_cache(key: str, value: dict, ttl: int = 3600):
    await redis.set(key, json.dumps(value), ex=ttl)
