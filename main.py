import aiohttp
import asyncio
from itertools import product


async def check_website_availability(url, retry_interval=5, max_retries=1, timeout=1) -> str | None:
    """Асинхронная функция проверки адреса сайта с повторной проверкой."""
    retries = 0

    while retries <= max_retries:
        try:
            timeout_settings = aiohttp.ClientTimeout(total=timeout)
            async with aiohttp.ClientSession(timeout=timeout_settings) as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        return url
                    return None
        except asyncio.TimeoutError:
            retries += 1
            if retries > max_retries:
                return None
            await asyncio.sleep(retry_interval)
        except aiohttp.ClientError as e:
            return f"ClientError {url}: {e}"
        except Exception as e:
            return f"Unexpected error {url}: {e}"


async def main():
    """Главная асинхронная функция."""
    urls_packs = create_urls(n=4, chunk_size=2000, start_from="aaaa")

    for urls_pack in urls_packs:
        print(urls_pack)
        tasks = [check_website_availability(url) for url in urls_pack]
        results = await asyncio.gather(*tasks)
        output(results)
        print(results)
        await asyncio.sleep(1)


def create_urls(n=4, chunk_size=2000, start_from=None):
    """
    Функция генерации массива ссылок по комбинациям
    с последующим разбиением данных на чанки.
    """
    alphabet = (chr(i) for i in range(97, 123))
    data = [
        "https://" + "".join(combination) + ".narod.ru/"
        for combination in product(alphabet, repeat=n)
    ]
    start_index = 0

    if start_from:
        try:
            start_index = data.index("https://" + start_from + ".narod.ru/")
        except ValueError:
            raise ValueError(f"Начальная комбинация '{start_from}' отсутствует в данных.")

    data = data[start_index:]
    print(f"Общее количество комбинаций: {len(data)}")
    return [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]


def output(results):
    """Функция записи чанка данных в файл с дозаписью"""
    with open("file.txt", "a", encoding="UTF-8") as file:
        for result in results:
            if result:
                file.write(f"{result}\n")


if __name__ == "__main__":
    asyncio.run(main())