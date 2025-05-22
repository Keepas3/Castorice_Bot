import asyncio
import starrailcard
async def main():
    async with starrailcard.Card() as card:
        data = await card.create(700649319, style=2)
    print(data)

asyncio.run(main())