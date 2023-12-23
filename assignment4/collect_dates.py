"""Script for finding all dates in a text, returning a list with dates in YMD format."""

import re
from typing import Tuple

## -- Task 3 (IN3110 optional, IN4110 required) -- ##

# create array with all names of months
month_names = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]

def get_date_patterns() -> Tuple[str, str, str]:
    """Return strings containing regex pattern for year, month, day.

    arguments:
        None
    return:
        year, month, day (tuple): Containing regular expression patterns for each field
    """
    # Regex to capture days, months and years with numbers
    # year should accept a 4-digit number between at least 1000-2029
    year = r"(?P<year>[0-9]{4})"
    # month should accept month names or month numbers
    jan = r"\b[jJ]an(?:uary)?\b"
    feb = r"\b[fF]eb(?:ruary)?\b"
    mar = r"\b[mM]ar(?:ch)?\b"
    apr = r"\b[aA]pr(?:il)?\b"
    may = r"\b[mM]ay\b"
    jun = r"\b[jJ]un(?:e)?\b"
    jul = r"\b[jJ]ul(?:y)?\b"
    aug = r"\b[aA]ug(?:ust)?\b"
    sep = r"\b[sS]ep(?:tember)?\b"
    oct = r"\b[oO]ct(?:ober)?\b"
    nov = r"\b[nN]ov(?:ember)?\b"
    dec = r"\b[dD]ec(?:ember)?\b"
    month = rf"(?P<month>(?:{jan}|{feb}|{mar}|{apr}|{may}|{jun}|{jul}|{aug}|{sep}|{oct}|{nov}|{dec}))"
    # day should be a number, which may or may not be zero-padded
    day = r"(?P<day>[0-9]{1,2})"
    return year, month, day


def convert_month(s: str) -> str:
    """Convert a string month to number (e.g. 'September' -> '09'.

    You don't need to use this function,
    but you may find it useful.

    arguments:
        month_name (str) : month name
    returns:
        month_number (str) : month number as zero-padded string
    """
    # If already digit do nothing
    if s.isdigit():
        return s

    # Convert to number as string
    for i in range(1, 13):
        if s == month_names[i-1]:
            if i < 10:
                return "0" + str(i)
            return str(i)


def zero_pad(n: str) -> str:
    """Zero-pad a number string.

    turns '2' into '02'

    You don't need to use this function,
    but you may find it useful.
    """
    if len(n) < 2:
        return "0" + n
    return n


def find_dates(text: str, output: str = None) -> list:
    """Find all dates in a text using regex.

    arguments:
        text (string): A string containing html text from a website
    return:
        results (list): A list with all the dates found in YMD format
    """
    year, month, day = get_date_patterns()

    # Date on format YYYY-MM-DD - ISO
    iso_month = r"(?P<iso_month>[0-9]{1,2})"
    ISO = rf"{year}-{iso_month}-{day}"

    # Date on format DD Month YYYY
    DMY = rf"{day}\s{month}\s{year}"

    # Date on format Month DD, YYYY
    MDY = rf"{month}\s{day},\s{year}"

    # Date on format YYYY Month DD
    YMD = rf"{year}\s{month}\s{day}"

    # list with all supported formats
    formats = [rf"{ISO}", rf"{DMY}", rf"{MDY}", rf"{YMD}"]
    dates = []

    # find all dates in any format in text
    for format in formats:
        unformatted_dates = re.findall(format, text)
        for date_element in unformatted_dates:
            # print(date_element)
            if format == rf"{ISO}":
                y, m, d = date_element
                m = zero_pad(m)
                d = zero_pad(d)
                dates.append(f"{y}/{m}/{d}")
            if format == rf"{DMY}":
                d, m, y = date_element
                m = convert_month(m)
                d = zero_pad(d)
                dates.append(f"{y}/{m}/{d}")
            if format == rf"{MDY}":
                m, d, y = date_element
                m = convert_month(m)
                d = zero_pad(d)
                dates.append(f"{y}/{m}/{d}")
            if format == rf"{YMD}":
                y, m, d = date_element
                m = convert_month(m)
                d = zero_pad(d)
                dates.append(f"{y}/{m}/{d}")
            
    # Write to file if wanted
    if output:
        print(f"Writing to: {output}")
        with open(output, "w") as outfile:
            for date in dates:
                outfile.write(date+"\n")
                
    return dates
