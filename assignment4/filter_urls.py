"""Script for finding urls and articles from a website."""

import re
from urllib.parse import urljoin

## -- Task 2 -- ##


def find_urls(
    html: str,
    base_url: str = "https://en.wikipedia.org",
    output: str = None,
) -> set:
    """Find all the url links in a html text using regex.

    Arguments:
        html (str): html string to parse
    Returns:
        urls (set) : set with all the urls found in html text
    """
    # create and compile regular expression(s)

    urls = set()
    # 1. find all the anchor tags, then
    a_pat = re.compile(r"<a[^>]+>", flags=re.IGNORECASE)
    # 2. find the urls href attributes

    # Pattern for finding urls starting with "https://", "/" and "//".
    href_pat = re.compile(r"(?<=href=\")((https\:\/\/[^#\\\"]+)|(\/[^\/][^#\"]+)|(\/\/[^#\"]+))", flags=re.IGNORECASE)
    for a_tag in a_pat.findall(html):
        href = href_pat.search(a_tag)

        if href is not None:
            if (href[0][0] + href[0][1] == "//"):
                href = "https:" + href[0]
            elif (href[0][0] == "/"):
                href = base_url + href[0]
            else:
                href = href[0]

            url_pat = re.compile(r"(?<=://)([^\s]+)")
            url = url_pat.search(href)
            if url is not None:
                url = url[0]
            if not ":" in url:
                urls.add(href)

    # Write to file if requested
    if output:
        print(f"Writing to: {output}")
        with open(output, "w") as outfile:
            for url in urls:
                outfile.write(url+"\n")

    return urls


def find_articles(html: str, output=None) -> set:
    """Find all the wiki articles inside a html text. Make call to find urls, and filter.

    arguments:
        - text (str) : the html text to parse
    returns:
        - (set) : a set with urls to all the articles found
    """
    urls = find_urls(html)
    # Pattern for collecting wikipedia links.
    pattern = re.compile(r"(?:(https\:\/\/en\.wikipedia\.org\/wiki[^\:]*))")
    articles = set()

    for url in urls:
        article = pattern.search(url)
        if article is not None:
            articles.add(article[0])

    # Write to file if wanted
    if output:
        print(f"Writing to: {output}")
        with open(output, "w") as outfile:
            for article in articles:
                outfile.write(article+"\n")
    return articles

## Regex example
def find_img_src(html: str):
    """Find all src attributes of img tags in an HTML string.

    Args:
        html (str): A string containing some HTML.

    Returns:
        src_set (set): A set of strings containing image URLs

    The set contains every found src attibute of an img tag in the given HTML.
    """
    # img_pat finds all the <img alt="..." src="..."> snippets
    # this finds <img and collects everything up to the closing '>'
    img_pat = re.compile(r"<img[^>]+>", flags=re.IGNORECASE)
    # src finds the text between quotes of the `src` attribute
    src_pat = re.compile(r'src="([^"]+)"', flags=re.IGNORECASE)
    src_set = set()
    # first, find all the img tags
    for img_tag in img_pat.findall(html):
        # then, find the src attribute of the img, if any
        src = src_pat.find(img_tag)
        src_set.add(src)
    return src_set
