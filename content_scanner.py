from asyncio import ensure_future, gather, run
from argparse import ArgumentParser
from aiohttp import ClientSession
from requests import get
from sys import exit

class ContentScanner:

    def __init__(self, worldlist_path: str) -> None:
        self.__words = self.__get_words(worldlist_path)

    async def __get_resp(self, session: ClientSession, word: str, url: str) -> None:
        async with session.get(url + "/" + word) as resp:
            if resp.status == 200:
                print(word)

    async def scan(self, url: str) -> None:
        tasks = []
        try:
            get(url)
        except:
            exit("Problem with url given")
        print("Found:")
        async with ClientSession() as session:
            for word in self.__words:
                tasks.append(ensure_future(self.__get_resp(session, word, url)))
            await gather(*tasks)

    def __get_words(self, worldlist_path: str) -> list:
        try:
            with open(worldlist_path, "r") as file:
                return file.read().splitlines()
        except:
            exit("Something gone wrong while opening wordlist file")

async def main(args):
    content_scanner = ContentScanner(r'' + args.path)
    await content_scanner.scan(args.url)

if __name__ == "__main__":
    parser = ArgumentParser(description='Web Content Scanner.')
    parser.add_argument("path", help="wordlist's path")
    parser.add_argument('--path', default=False, action="store_true", required=True, help="wordlist's path")
    parser.add_argument("url", help="website's url")
    parser.add_argument('--url', default=False, action="store_true", required=True, help="website's url")
    run(main(parser.parse_args()))
