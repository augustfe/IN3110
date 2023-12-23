# Assignment 4: Web scraping
Created by Augustfe (Augustfe@mail.uio.no) \
https://github.uio.no/IN3110/IN3110-augustfe/tree/main/assignment4
## Required dependencies
### Packages used
The programs were run on conda 22.9.0 with Python 3.9.12.final.0 on an M1 mac. The following packages were used. Required packages can be installed with either `pip3 install <package>` or `conda install <package>`.
- re
- typing
- os
- urlib.parse
- numpy
- bs4
- matplotlib
- requests
- copy
- dataclasses
- pandas
#### Wikirace dependecies
- logging
- sys
- time
- asyncio
- aiohttp
- collections

## How to run the scripts
The main scripts from the assignment are pretty straight forward, and pass all tests when `pytest -vv tests` is called.

## Bonus task - Wiki Race with URLs
I quickly got a working implementation going using a Breadth First Search and the functions created for other tasks, but I found it quite slow. During the tinkering of this, i created multiple Jupyter Notebooks, which can be found in the `Notebooks`-folder. In doing this, i used `lprun` in order to find out why the program was so slow. Here i found that about 98% of the time was being spent waiting for a response from Wikipedia, which was when I started looking around for different methods to bypass this waiting time.

I tried using the Wikipedia API directly from `https://en.wikipedia.org/w/api.php`, but struggeled to get anything useful out of it. I then got a bit of a speedup from using `requests.session` instead of using `requests.get` directly, but I wasn't quite satisfied. I tried using both `@jit` from `numba` and `@jitclass` from `numba.experimental` but I couldn't get it to work. I also tinkered with `concurrent.futures` in order to run the search in parallel, which led me to discover `asyncio` and `aiohttp`. These modules let me request websites and parse in parallel, effectively removing the wait time.

This got me to my final version, where i asynchronously request and parse through the websites, using modified versions of the functions I had previously written. This included changing the way I get the articles within a page from first getting all URLs and then getting the articles, to just getting the articles directly. I considered trying to speed up the other functions, but as I was already hitting the maximum of 200 requests/s from Wikipedia, I didn't think it was necessary.

The script is run with `python3 wiki_race_challenge.py`, with the start and finish articles set in the `if __name__ == '__main__':` statement. I tested it from `https://en.wikipedia.org/wiki/Nobel_Prize` to `https://en.wikipedia.org/wiki/Array_data_structure`, and found it uses between 15 seconds and 45 seconds to find a path, usually checking through between 3000-6000 articles. The time is a bit random, depending on which URLs are checked first. In writing this, I ran it again and got the results
```python
Used 26.422s to find path
['https://en.wikipedia.org/wiki/Nobel_Prize', 'https://en.wikipedia.org/wiki/Free_license', 'https://en.wikipedia.org/wiki/Database', 'https://en.wikipedia.org/wiki/Array_data_structure']
```
I verified the results using [Six Degrees of Wikipedia](https://www.sixdegreesofwikipedia.com/?source=Nobel%20Prize&target=Array%20(data%20structure)), and found that the path was the correct length.

## Additional notes
I found that there is a built in function in `pandas` for reading a table from `HTML`, namely
```python
df = pd.read_html(str(table))[0][["Date", "Venue", "Type"]]
```
which effectively does the entirety of Task 5, but I opted for following the code skeleton in order to follow the spirit of the task.