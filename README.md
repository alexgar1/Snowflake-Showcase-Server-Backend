# Snowflake Showcase

## Overview

The Snowflake Showcase is a web-based visualization platform for displaying snowflake images captured by the University of Utah’s Multi-Angle Snowflake Camera (MASC) and corresponding meteorological data. It integrates DEID (Differential Emissivity Imaging Disdrometer) data and Synoptic MesoWest station data from instruments located near the Alta Ski Resort.

This platform provides an interactive interface to explore snowflake images, snowfall accumulation, and weather conditions in real time.

## Features

Live Snowflake Image Feed: View high-resolution snowflake images captured in freefall.

Historical Data Archive: Browse past storm events and corresponding images.

DEID Snowpack Data: Visualize snowfall accumulation, SWE (Snow Water Equivalent), and snow density over time.

Synoptic Weather Data: Access real-time and historical weather data including temperature, humidity, wind speed, and snow depth.

Interactive Plots: Explore data through dynamically generated plots.

## Data Sources

1. Multi-Angle Snowflake Camera (MASC)

The MASC captures high-speed images of individual snowflakes at multiple angles, providing insights into their structure and formation.

2. Differential Emissivity Imaging Disdrometer (DEID)

The DEID measures snow accumulation and density at the study site. The processed data includes:

SWE (Snow Water Equivalent) - Measured in millimeters.

Snow Accumulation - Measured in millimeters.

Density - Measured in kg/m³.

3. Synoptic/MesoWest Data

Weather data is retrieved from the Alta Ski Resort Synoptic station (ATH20) using the Synoptic API. The collected data includes:

Air Temperature (°C)

Relative Humidity (%)

Snow Depth (mm)

Wind Speed (m/s)

Project Structure

/snowflake_showcase/
│── /data/                 # Data storage for plots and text files
│── /images/               # Snowflake image storage
│── /css/                  # Stylesheets for frontend
│── /js/                   # JavaScript files for interactive components
│── /scripts/              # Python scripts for data processing
│── index.html             # Main HTML page
│── genDataPlots.py        # Main backend script for processing data
│── genImages.py           # Create grid of snowflake images
│── getSynoptic.py         # Downloads data from synoptic API
│── makePlot.py            # Creates html bokeh plots

Backend Processing

The genDataPlots.py script is responsible for fetching, processing, and visualizing the data.

Data Processing Workflow

Retrieve DEID Data:

Parses CSV files containing DEID snowfall data.

Extracts SWE, snow accumulation, and density.

Fetch Synoptic Weather Data:

Uses the Synoptic API to fetch MesoWest station data for temperature, humidity, wind, and snow depth.

Process Snowflake Image Data:

Extracts snowflake image metadata (timestamp, size, etc.).

Generates an HTML gallery for browsing images.

Generate Plots:

Uses Bokeh to create interactive plots for SWE, density, accumulation, temperature, humidity, snow depth, and wind speed.

Generate Webpage:

Creates an interactive index.html page with dropdown options to explore different storms.

Example Code Snippets

Convert Time to Float

def convertTimeToFloat(time):
    """ Convert a timestamp to a float representation """
    time_format = "%d-%b-%Y %H:%M:%S"
    dt_obj = datetime.strptime(time, time_format).timestamp()
    return dt_obj

Fetch Synoptic Weather Data

def get_station_timeseries(token, station_id, start, end, variables, units='metric'):
    base_url = "https://api.synopticdata.com/v2/stations/timeseries"
    params = {
        'token': token,
        'stid': station_id,
        'start': start,
        'end': end,
        'vars': variables,
        'units': units
    }
    response = requests.get(base_url, params=params)
    return response.json() if response.status_code == 200 else None

Generate Snowflake Image Gallery

def generate_html_page(options, storm, imageshtml):
    return f"""
    <html>
    <head>
        <title>Snowflake Showcase</title>
        <link rel="stylesheet" type="text/css" href="../css/data.css">
    </head>
    <body>
        <h1>SNOWFLAKE SHOWCASE</h1>
        <select id="pageSelector">{options}</select>
        <div id="plotContainer"></div>
    </body>
    </html>
    """
