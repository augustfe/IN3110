"""Tasks 5, 6 and 7."""

import re
from copy import copy
from dataclasses import dataclass
from typing import List

import bs4
import pandas as pd
from bs4 import BeautifulSoup
from requesting_urls import get_html

## --- Task 5, 6, and 7 ---- ##

# Dict over all types of events
event_types = {
    "DH": "Downhill",
    "SL": "Slalom",
    "GS": "Giant Slalom",
    "SG": "Super Giant slalom",
    "AC": "Alpine Combined",
    "PG": "Parallel Giant Slalom",
}


def time_plan(url: str) -> str:
    """Parse a table from html text and extract desired information and saves in betting slip markdown file.

    arguments:
        url (str) : URL for page with calendar table
    return:
        markdown (str) : string containing the markdown schedule
    """
    # Get the page
    html = get_html(url)
    # parse the HTML
    soup = BeautifulSoup(html, "html.parser")
    # locate the table
    calendar = soup.find(id="Calendar")
    soup_table = calendar.find_next("table", {"class": "wikitable"})
    # extract events into pandas data frame
    df = extract_events(soup_table)

    # Write the schedule markdown
    return render_schedule(df)


@dataclass
class TableEntry:
    """Data class representing a single entry in a table.

    Records text content, rowspan, and colspan attributes
    """

    text: str
    rowspan: int
    colspan: int


def extract_events(table: bs4.element.Tag, wanted: List[str]=["Date", "Venue", "Type"]) -> pd.DataFrame:
    """Get the events from the table.

    arguments:
        table (bs4.element.Tag) : Table containing data
        wanted (List[str])
    return:
        df (DataFrame) : DataFrame containing filtered and parsed data
    """
    # Gets the table headers and saves their labels in `keys`
    headings = table.find_all("th")
    labels = [th.text.strip() for th in headings]
    data = []

    # Extracts the data in table, keeping track of colspan and rowspan
    rows = table.find_all("tr")
    rows = rows[1:]
    for tr in rows:
        cells = tr.find_all("td")
        row = []
        for cell in cells:
            colspan = 1
            rowspan = 1
            if re.search("colspan", str(cell)):
                m = re.search(r'colspan="(\d+)"', str(cell))
                colspan = int(m.group(1))
            if re.search("rowspan", str(cell)):
                m = re.search(r'rowspan="(\d+)"', str(cell))
                rowspan = int(m.group(1))
            text = cell.get_text(strip=True)
            row.append(
                TableEntry(
                    text=text,
                    rowspan=rowspan,
                    colspan=colspan,
                )
            )
        data.append(row)
    # at this point `data` should be a table (list of lists)
    # where each item is a TableEntry with row/colspan properties
    # expand TableEntries into a dense table
    all_data = expand_row_col_span(data)

    # Filter data and create pandas dataframe
    filtered_data = filter_data(labels, all_data, wanted)

    df = pd.DataFrame(filtered_data, columns=wanted)
    
    # Pandas function which replace this script
    # df = pd.read_html(str(table))[0][["Date", "Venue", "Type"]]

    return df


def render_schedule(data: pd.DataFrame) -> str:
    """Render the schedule data to markdown.

    arguments:
        data (DataFrame) : DataFrame containing table to write
    return:
        markdown (str): the rendered schedule as markdown
    """

    def expand_event_type(type_key):
        """Expand event type key (SL) to full name (Slalom).

        Useful with pandas Series.apply
        """
        return event_types.get(type_key[:2], type_key)

    data["Type"] = data["Type"].apply(expand_event_type)
    return data.to_markdown(index=False)


def strip_text(text: str) -> str:
    """Get rid of cruft from table cells, footnotes and setting limit to 20 chars.

    It is not required to use this function,
    but it may be useful.

    arguments:
        text (str) : string to fix
    return:
        text (str) : the string fixed
    """
    text = text[:20]  # 20 char limit
    text = re.sub(r"\[.*\]", "", text)
    return text


def filter_data(keys: list, data: list, wanted: list):
    """Filter away the columns not specified in wanted argument.

    It is not required to use this function,
    but it may be useful.

    arguments:
        keys (list of strings) : list of all column names
        data (list of lists) : data with rows and columns
        wanted (list of strings) : list of wanted columns
    return:
        filtered_data (list of lists) : the filtered data
            This is the subset of data in `data`,
            after discarding the columns not in `wanted`.
    """
    indexes = [i for i, key in enumerate(keys) if key in wanted]

    new_data = []
    for row in data:
        new_row = []
        for i in indexes:
            new_row.append(strip_text(row[i]))
        new_data.append(new_row)

    return new_data


def expand_row_col_span(data):
    """Apply row/colspan to tabular data.

    It is not required to use this function,
    but it may be useful.

    - Copies cells with colspan to columns to the right
    - Copies cells with rowspan to rows below
    - Returns raw data (removing TableEntry wrapper)

    arguments:
        data_table (list) : data with rows and cols
            Table of the form:

            [
                [ # row
                    TableEntry(text='text', rowspan=2, colspan=1),
                ]
            ]
    return:
        new_data_table (list): list of lists of strings
            [
                [
                    "text",
                    "text",
                    ...
                ]
            ]

            This should be a dense matrix (list of lists) of data,
            where all rows have the same length,
            and all values are `str`.
    """
    # first, apply colspan by duplicating across the column(s)
    new_data = []
    for row in data:
        new_row = []
        new_data.append(new_row)
        for entry in row:
            for _ in range(entry.colspan):
                new_entry = copy(entry)
                new_entry.colspan = 1
                new_row.append(new_entry)

    # apply row span by inserting copies in subsequent rows
    # in the same column
    for row_idx, row in enumerate(new_data):
        for col_idx, entry in enumerate(row):
            for offset in range(1, entry.rowspan):
                # copy to row(s) below
                target_row = new_data[row_idx + offset]
                new_entry = copy(entry)
                new_entry.rowspan = 1
                target_row.insert(col_idx, new_entry)
            entry.rowspan = 1

    # now that we've applied col/row span,
    # replace the table with the raw entries,
    # instead of the TableEntry objects
    return [[entry.text for entry in row] for row in new_data]

if __name__ == "__main__":
    # test the script on the past few years by running it:
    for year in range(20, 23):
        url = (
            f"https://en.wikipedia.org/wiki/20{year}–{year+1}_FIS_Alpine_Ski_World_Cup"
        )
        print(url)
        md = time_plan(url)
        print(md)

