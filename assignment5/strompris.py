#!/usr/bin/env python3
"""
Fetch data from https://www.hvakosterstrommen.no/strompris-api
and visualize it.

Assignment 5
"""

import datetime

import altair as alt
import pandas as pd
import requests
import requests_cache
from typing import Optional

# install an HTTP request cache
# to avoid unnecessary repeat requests for the same data
# this will create the file http_cache.sqlite
requests_cache.install_cache()


# task 5.1:


def fetch_day_prices(
    date: Optional[datetime.date] = None, location: str = "NO1"
) -> pd.DataFrame:
    """Fetch one day of data for one location from hvakosterstrommen.no API.

    arguments:
        date (datetime.date, optional):
            The date to fetch prices from,
            if no argument is given todays date is fetched.
        location (str, optional):
            Location to get price from, chosen from ["NO1", "NO2", ..., "NO5"].
    returns:
        df (pd.DataFrame): Dataframe containing prices for the desired day.
    """
    if date is None:
        date = datetime.date.today()

    assert date > datetime.date.fromisoformat("2022-10-02")
    assert location in LOCATION_CODES

    url = f'https://www.hvakosterstrommen.no/api/v1/prices/{date.strftime("%Y/%m-%d")}_{location}.json'
    r = requests.get(url)

    df = pd.DataFrame.from_dict(r.json())
    df["time_start"] = pd.to_datetime(df["time_start"], utc=True).dt.tz_convert(
        "Europe/Oslo"
    )
    df["NOK_per_kWh"] = df["NOK_per_kWh"].astype("float")

    df = df[["NOK_per_kWh", "time_start"]]

    return df


# LOCATION_CODES maps codes ("NO1") to names ("Oslo")
LOCATION_CODES = {
    "NO1": "Oslo",
    "NO2": "Kristiansand",
    "NO3": "Trondheim",
    "NO4": "Tromsø",
    "NO5": "Bergen",
}

# task 1:


def fetch_prices(
    end_date: Optional[datetime.date] = None,
    days: int = 7,
    locations: tuple[str] = tuple(LOCATION_CODES.keys()),
) -> pd.DataFrame:
    """Fetch prices for multiple days and locations into a single DataFrame.

    arguments:
        end_date (datetime.date, optional): Last day to fetch price from,
            if None is given, todays date is chosen.
        days (int, optional): Number of days to fetch.
        locations (tuple[str], optional): Locations to fetch prices from,
            if none is given all prices are returned.
    returns:
        df (pd.DataFrame): Dataframe containing prices for all given regions,
            for all given days.
    """
    if end_date is None:
        end_date = datetime.date.today()

    df = pd.DataFrame()

    for i in range(days):
        date = end_date - datetime.timedelta(days=i)
        for location in locations:
            new_df = fetch_day_prices(date, location)
            new_df["location_code"] = location
            new_df["location"] = LOCATION_CODES[location]
            df = pd.concat([df, new_df])

    return df


# task 5.1:


def plot_prices(df: pd.DataFrame) -> alt.Chart:
    """Plot energy prices over time.

    x-axis should be time_start
    y-axis should be price in NOK
    each location should get its own line

    arguments:
        df (pd.DataFrame): Dataframe containing prices we want to plot,
            split across the given regions.
    returns:
        chart (alt.Chart): Plot generated from the given dataframe.
    """
    return (
        alt.Chart(df)
        .mark_line()
        .encode(
            alt.X("time_start:T", title="Time"),
            alt.Y("NOK_per_kWh:Q", title="Price per kWh"),
            alt.Color("location:N", title="Location"),
        )
    )


# Task 5.6

ACTIVITIES = {
    "shower": 30,
    "baking": 2.5,
    "heat": 1,
}


def plot_activity_prices(
    df: pd.DataFrame, activity: str = "shower", minutes: float = 10
) -> alt.Chart:
    """
    Plot price for one activity by name,
    given a data frame of prices, and its duration in minutes.

    arguments:
        df (pd.DataFrame): Dataframe containing prices.
        activity (str): Activity to calculate price of.
        minutes (float): Amount of minutes to price in.
    returns:
        chart (alt.Chart): Chart showing the price of the chosen activity.

    TODO:
        - Add handling for activies that take longer,
        i.e. charging an electric car.
    """
    if minutes > 60:
        raise NotImplementedError("TODO")
    if activity not in ACTIVITIES:
        raise ValueError("Please select a valid type.")

    df["NOK_per_activity"] = df["NOK_per_kWh"] * minutes / 60 * ACTIVITIES[activity]

    return (
        alt.Chart(df)
        .mark_line()
        .encode(
            alt.X("time_start:T", title="Time"),
            alt.Y("NOK_per_activity:Q", title=f"NOK for {activity} for {minutes} min"),
        )
    )


def main():
    """Allow running this module as a script for testing."""
    df = fetch_prices()
    chart = plot_prices(df)

    # showing the chart without requiring jupyter notebook or vs code for example
    # requires altair viewer: `pip install altair_viewer`
    chart.show()


if __name__ == "__main__":
    main()
