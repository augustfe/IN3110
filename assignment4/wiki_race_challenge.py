"""
Script for finding the shortest path between two Wikipedia articles.

Uses asyncio and aiohttp in order to asynchronously call requests from
Wikipedia, reducing the total time spent waiting for a response. Increase
amount of workers (increase x in `for i in range(x)`) if program is slow,
decrease if it is too fast (aiohttp - too many requests). This is dependant
on internet speed, it is currently optimized for the Internet at
Vilhelm Bjerknes hus. Aim for around ~200 requests/s. It is also a bit random depending on which URLs are
checked first.
"""

import logging
import re
import sys
import time

from typing import List
import asyncio
import aiohttp
from aiohttp import ClientSession
from collections import defaultdict

logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    level=logging.DEBUG,
    datefmt="%H:%M:%S",
    stream=sys.stderr,
)
logger = logging.getLogger("areq")
logging.getLogger("chardet.charsetprober").disabled = True


async def fetch_html(url: str, session: ClientSession, **kwargs) -> str:
    """GET request wrapper to fetch page HTML.

    arguments:
        url (str): URL to fetch page HTML of
        session (ClientSession): The interface for making HTTP requests

    returns:
        html (str): The HTML of the URL

    kwargs are passed to `session.request()`.
    """
    resp = await session.request(method="GET", url=url, **kwargs)
    resp.raise_for_status()
    logger.info("Got response [%s] for URL: %s", resp.status, url)
    html = await resp.text()
    return html


class Node:
    """Node class for finding path back to the start URL."""

    def __init__(self, data: str):
        """Initialise Node Class.

        arguments:
            data (str): The URL associated with the Node
        usage:
            node = Node(URL) to instansiate the Node
            node.prev to set the previous Node
        """
        self.data = data
        self.prev = None


class Search:
    """Class for using a Breadth first search in order to find a path from two wikipedia articles."""

    def __init__(self, start: str, finish: str, printing: bool):
        """Initialise the Search class.

        arguments:
            start (str): The Wikipedia article to start from
            finish (str): The Wikipedia article to find
            printing (bool): Whether to activate printing as articles are checked, True by default
        """
        self.start = start
        self.target = finish
        self.printing = printing
        self.visited = defaultdict(lambda: False)
        self.count = 0
        self.trail = {}

    async def parse(self, url: str, session: ClientSession, **kwargs) -> set:
        """Parse through the HTML of a URL and find the articles within.

        arguments:
            url (str): The URL to parse through
            session (ClientSession): The interface for making HTTP requests

        returns:
            found (set): The URLs found

        kwargs are passed to `fetch_html`.
        """
        found = set()
        try:
            html = await fetch_html(url=url, session=session, **kwargs)

        except (
            aiohttp.ClientError,
            aiohttp.http_exceptions.HttpProcessingError,
        ) as e:
            logger.error(
                "aiohttp exception for %s [%s]: %s",
                url,
                getattr(e, "status", None),
                getattr(e, "message", None),
            )
            return found

        except Exception as e:
            logger.exception(
                "Non-aiohttp exception occured:  %s", getattr(e, "__dict__", {})
            )
            return found

        else:
            base_url = "https://en.wikipedia.org"
            long_pat = re.compile(
                r"(?<=href=\")((https\:\/\/en\.wikipedia.org\/wiki\/[^#\\\"]+)|(\/wiki[^#\"]+))"
            )

            for article in long_pat.findall(html):
                if article is not None:
                    if article[0][0] == "/":
                        article = base_url + article[0]

                    else:
                        article = article[0]

                    if ":" not in article[6:]:
                        found.add(article)

            return found

    async def add_to_queue(self, found: set, prev: str):
        """Add found URLs to the queue.

        arguments:
            found (set): URLs found withing the parent URL
            prev (str): The parent URL
        """
        for url in found:
            # If the target URL is encountered
            if url == self.target:
                # Stop workers
                self.quit = True
                logger.info(f"Found path for {self.target}.")

                node = Node(url)
                self.trail[url] = node
                node.prev = self.trail[prev]

            # If this is a new url, and it is different from the parent url
            if not self.visited[url] and url != prev:
                # If the url is not already in the path back
                if url not in self.trail:
                    # add the url to the back of the queue
                    await self.queue.put(url)
                    # create a linked list back to the previous url
                    # in order to trace back the path that was taken
                    node = Node(url)
                    self.trail[url] = node
                    node.prev = self.trail[prev]

    async def worker(
        self, name: str, queue: asyncio.Queue, session: ClientSession, **kwargs
    ):
        """Worker function for running in parallel.

        arguments:
            name (str): name of the worker
            queue (asyncio.Queue): Queue to retreieve URLs from
            session (ClientSession): The interface for making HTTP requests

        kwargs are passed to `parse`.
        """
        while not self.quit:
            # Get a url out of the queue.
            url = await queue.get()

            # Get the urls from the page and add them to the queue
            urls = await self.parse(url, session, **kwargs)
            await self.add_to_queue(urls, url)

            # Mark url as done
            queue.task_done()
            self.count += 1
            if self.printing:
                print(
                    f"{self.count}: {name} checked {url[30:]}, from {self.trail[url].prev.data[30:]}"
                )

    async def main(self) -> List[str]:
        """Search for the path from the start URL to the target URL.

        returns:
            path (List[str]): The path found from the start URL to the target URL
        """
        # Create a queue that we will use to store our URLs.
        self.queue = asyncio.Queue(maxsize=0)
        # Create a trail of Nodes, in order to trace our way back to the start URL.
        self.trail[self.start] = Node(self.start)
        # Default dictionary to check if we have encountered this URL before.
        self.visited[self.start] = True
        self.quit = False

        async with ClientSession(
            connector=aiohttp.TCPConnector(limit_per_host=100)
        ) as session:
            # Fill the queue with URLs found in the start article.
            urls = await self.parse(url=start, session=session)
            await self.add_to_queue(urls, self.start)
            for url in urls:
                if url != self.start:
                    self.queue.put_nowait(url)

            # Create workers to asynchronously work through the queue.
            self.tasks = []
            # creates 10 workers
            for i in range(10):
                task = asyncio.create_task(
                    self.worker(f"worker-{i}", self.queue, session)
                )
                self.tasks.append(task)

            # wait for a path to be found
            await asyncio.gather(*self.tasks)

            logger.info(f"Closing {len(self.tasks)} tasks.")

            # Close tasks after a path has been found.
            for task in self.tasks:
                task.cancel()

            # Trace backwards to find the path.
            path = [self.target]
            breadcrumbs = self.trail[self.target]
            while breadcrumbs.prev is not None:
                path.insert(0, breadcrumbs.prev.data)
                breadcrumbs = breadcrumbs.prev

            return path


def find_path(start: str, finish: str, printing: bool = True) -> List[str]:
    """Find the shortest path from `start` to `finish`.

    Arguments:
        start (str):Wikipedia article URL to start from
        finish (str): Wikipedia article URL to stop at
        printing (bool): Whether to activate printing as articles are checked, True by default
                         (used to verify the program is working)

    Returns:
        urls (list[str]):
            List of URLs representing the path from `start` to `finish`.
            The first item should be `start`.
            The last item should be `finish`.
            All items of the list should be URLs for wikipedia articles.
            Each article should have a direct link to the next article in the list.
    """
    started_at = time.monotonic()

    # instantiate the Search class and event loop
    instance = Search(start, finish, printing)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    # run the program
    path = asyncio.run(instance.main())
    finished_at = time.monotonic()
    elapsed_time = finished_at - started_at

    # verify the start and end are correct
    assert path[0] == start
    assert path[-1] == finish
    print(f"Used {elapsed_time:.3f}s to find path")
    return path


if __name__ == "__main__":
    # logger.propgate = True # If logging is desirable.
    logger.propagate = False
    # start = "https://en.wikipedia.org/wiki/Nobel_Prize"
    # finish = "https://en.wikipedia.org/wiki/Array_data_structure"

    # Shorter example path used for verify everything works.
    # start = "https://en.wikipedia.org/wiki/The_Emoji_Movie"
    # finish = "https://en.wikipedia.org/wiki/Vietnam_War"

    # start = "https://en.wikipedia.org/wiki/Python_(programming_language)"
    # finish = "https://en.wikipedia.org/wiki/Peace"

    start = "https://en.wikipedia.org/wiki/Python_(programming_language)"
    finish = "https://en.wikipedia.org/wiki/Peace"

    path = find_path(start, finish, printing=True)
    print(path)
