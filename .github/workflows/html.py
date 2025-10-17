import asyncio
from urllib import response

import aiohttp as aiohttp
import requests
import bs4


def get_html_text(course_id: int):
    url = f'https://toplearn.com/c/{course_id}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


def get_title_from_html_text(html: str):
    soup = bs4.BeautifulSoup(html, 'html.parser')
    header = soup.select_one(".right_side h1")
    if not header:
        return 'not'
    return header.text.strip()


async def get_title_from_toplearn_old_version():
    for course_id in range(6130, 6140):
        hrml = await get_html_text(course_id)
        title = get_title_from_html_text(hrml)
        print(title)


async def get_title_from_toplearn():
    tasks = []
    for n in range(6130, 6140):
        tasks.append(n, asyncio.create_task(get_html_text(n)))
    for n,t in tasks:
        html=await t
        title=get_title_from_html_text(html)
        print(title)
    for course_id in range(6130, 6140):
        hrml = await get_html_text(course_id)
        title = get_title_from_html_text(hrml)
        print(title)


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_title_from_toplearn())


if __name__ == "__main__":
    main()
