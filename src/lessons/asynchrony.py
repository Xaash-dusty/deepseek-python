import asyncio

import httpx

URL = "https://jsonplaceholder.typicode.com/posts/{}"


async def fetch(client, post_id):
    r = await client.get(URL.format(post_id), timeout=5)
    r.raise_for_status()
    return r.json()


async def main_a(client):
    try:
        await asyncio.gather(
            fetch(client, 1),
            fetch(client, 999999),
            fetch(client, 3),
        )
    except httpx.HTTPStatusError as e:
        print(f"Ошибка: {e.response.status_code}")


async def main_b(client):
    results = await asyncio.gather(
        fetch(client, 1),
        fetch(client, 999999),
        fetch(client, 3),
        return_exceptions=True,
    )
    for r in results:
        if isinstance(r, Exception):
            print(f"{type(r).__name__}: {r}")
        else:
            print(f"id: {r['id']}, title: {r['title']}")


async def main_c(client):
    try:
        await asyncio.wait_for(fetch(client, 10), timeout=0.001)
    except asyncio.TimeoutError:
        print("Время вышло")


async def main():
    async with httpx.AsyncClient() as client:
        await main_a(client)
        print("-" * 40)
        await main_b(client)
        print("-" * 40)
        await main_c(client)


asyncio.run(main())
