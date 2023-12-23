"""FastAPI app for interactively visualizing power prices accross Norway."""

import datetime
from typing import List, Optional

import altair as alt
from fastapi import FastAPI, Query, Request
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from strompris import (
    ACTIVITIES,
    LOCATION_CODES,
    fetch_day_prices,
    fetch_prices,
    plot_activity_prices,
    plot_prices,
)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# `GET /` should render the `strompris.html` template
# with inputs:
# - request
# - location_codes: location code dict
# - today: current date


@app.get("/")
def strompris_html(request: Request):
    """Render the strompris.html template

    arguments:
        request (Request): Request object with data
    """
    return templates.TemplateResponse(
        "strompris.html",
        {
            "request": request,
            "location_codes": LOCATION_CODES,
            "today": datetime.date.today(),
        },
    )


# GET /plot_prices.json should take inputs:
# - locations (list from Query)
# - end (date)
# - days (int, default=7)
# all inputs should be optional
# return should be a vega-lite JSON chart (alt.Chart.to_dict())
# produced by `plot_prices`
# (task 5.6: return chart stacked with plot_daily_prices)


@app.get("/plot_prices.json")
def prices_plot_json(
    locations: tuple = Query(default=tuple(LOCATION_CODES.keys())),
    end: datetime.date = datetime.date.today(),
    days: int = 7,
):
    """Create altair chart of prices.

    arguments:
        locations (tuple): tuple with locations to plot prices of
        end (datetime.date): end date to plot prices from
        days (int): amount of days to plot
    returns:
        chart (dict): dictionary of plot, converted to json
    """
    df = fetch_prices(end, days, locations)
    chart = plot_prices(df)
    return alt.Chart.to_dict(chart)


# Task 5.6:
# `GET /activity` should render the `activity.html` template
# activity.html template must be adapted from `strompris.html`
# with inputs:
# - request
# - location_codes: location code dict
# - activities: activity energy dict
# - today: current date


@app.get("/activity")
def activity_html(request: Request):
    """Render the activity.html template

    arguments:
        request (Request): Request object with data
    """
    return templates.TemplateResponse(
        "activity.html",
        {
            "request": request,
            "location_codes": LOCATION_CODES,
            "activities": ACTIVITIES,
            "today": datetime.date.today(),
        },
    )


# Task 5.6:
# `GET /plot_activity.json`
#  should return vega-lite chart JSON (alt.Chart.to_dict())
# from `plot_activity_prices`
# with inputs:
# - location (single, default=NO1)
# - activity (str, default=shower)
# - minutes (int, default=10)


@app.get("/plot_activity.json")
def prices_plot_activity_json(
    location: str = "NO1",
    activity: str = "shower",
    minutes: int = 10,
):
    """Create altair chart of prices of activity.

    arguments:
        location (str): location to plot prices of
        activity (str): activity to plot price for
        minutes (int): amount of minutes to price activity for
    returns:
        chart (dict): dictionary of plot, converted to json
    """
    df = fetch_day_prices(location=location)
    chart = plot_activity_prices(df, activity, minutes)
    return alt.Chart.to_dict(chart)


# mount your docs directory as static files at `/help`

app.mount("/help", StaticFiles(directory="docs/_build/html"), name="help")

if __name__ == "__main__":
    # use uvicorn to launch your application on port 5000

    from threading import Thread
    import uvicorn

    def run_app():
        uvicorn.run(app, host="127.0.0.1", port=5000)

    app_thread = Thread(target=run_app)
    app_thread.start()
