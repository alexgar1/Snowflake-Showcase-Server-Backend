from bokeh.plotting import figure
import pandas as pd
from collections import Counter
from bokeh.io import output_file, save
from bokeh.layouts import gridplot
from datetime import datetime, timedelta
import numpy as np
from bokeh.models import FuncTickFormatter, LogAxis, FixedTicker, DatetimeTickFormatter, Dropdown, Range1d, ResetTool
from collections import defaultdict

PATH = '/uufs/chpc.utah.edu/common/home/snowflake3/showcase/'



def save_plot(plot, name):
    """
    Saves a Bokeh plot as an HTML file.

    Parameters:
    - plot: The Bokeh plot object to be saved.
    - name: The base name for the output file.
    """
    if plot:
        filename = f"{PATH+'data/'+name}.html"  # Construct the file name
        output_file(filename)  # Set the output file name
        save(plot)  # Save the plot

def plotProperties(p):
    # Set plot properties
    p.title.text_font_size = '16pt'
    p.xaxis.axis_label_text_font_size = '14pt'
    p.yaxis.axis_label_text_font_size = '14pt'
    p.xaxis.major_label_text_font_size = '12pt'
    p.yaxis.major_label_text_font_size = '12pt'
    return p


def mesoPlot(data, y, name):
    # Adjusted datetime format to match ISO 8601 format
    dates = [datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ') for date in data.keys()]
    values = list(data.values())

    # Create a DataFrame for easier plotting
    df = pd.DataFrame({'Date': dates, 'Value': values})

    # Create a new plot with a title and axis labels
    p = figure(title=name, x_axis_label='Date', y_axis_label='Value', x_axis_type='datetime',
    sizing_mode='stretch_both')

    # Add a line renderer with legend and line thickness
    p.line(df['Date'], df['Value'], line_width=1)

    #p.xaxis.formatter = FuncTickFormatter(code=tickStr())
    # p.xaxis.formatter = DatetimeTickFormatter(
    #     hours=["%d-%b %H:%M"],
    #     days=["%d-%b %H:%M"],
    #     months=["%d-%b %H:%M"],
    #     years=["%d-%b %H:%M"]
    # )

    p.yaxis.axis_label = y
    p.xaxis.axis_label = 'Time'
    p = plotProperties(p)

    return p

def deidPlot(data, units, which):
    
    print('Saving:', which)

    # Convert string keys to datetime objects
    dates = [datetime.fromtimestamp(date) for date in data.keys()]
    values = list(data.values())
    values = [float(v) for v in values]

    # Create a new plot with a title and axis labels
    p = figure(title=which, x_axis_label='Time', 
    y_axis_label=units, x_axis_type='datetime', 
    sizing_mode='stretch_both')

    # Add a line renderer with legend and line thickness
    p.line(dates, values, line_width=1)

    # Example of setting explicit ranges
    p.x_range = Range1d(start=min(dates), end=max(dates))
    p.y_range = Range1d(start=min(values) - 10, end=max(values) + 10)

    p.xaxis.axis_label_text_font_size = "1pt"
    p.yaxis.axis_label_text_font_size = "1pt"

    p.add_tools(ResetTool())# 
    p = plotProperties(p)

    return p


def getSizeTime(sizes: list, timestamps: list):

    if sizes==[] or timestamps == []:
        return None

    # Create buckets for 10-minute intervals
    buckets = [datetime(dt.year, dt.month, dt.day, dt.hour, 0) for dt in timestamps]

    # Initialize a dictionary to accumulate snowflake sizes and count the entries for averaging
    size_accumulator = defaultdict(lambda: {'total_size': 0, 'count': 0})

    for bucket, size in zip(buckets, sizes):
        size_accumulator[bucket]['total_size'] += size
        size_accumulator[bucket]['count'] += 1

    # Calculate average size for each bucket
    average_sizes = {bucket: size_info['total_size'] / size_info['count'] for bucket, size_info in size_accumulator.items()}

    start_time = min(buckets)
    end_time = max(buckets)

    # if no snowflakes mark data point at 0
    current_time = start_time
    while current_time <= end_time:
        if current_time not in average_sizes:
            average_sizes[current_time] = 0
        current_time += timedelta(minutes=60)

    # Sort and prepare data for plotting
    times, avg_sizes = zip(*sorted(average_sizes.items()))
    times = np.array(times, dtype=np.datetime64)
    avg_sizes = np.array(avg_sizes)

    # Create a Bokeh plot
    p = figure(x_axis_type="datetime", title="Average Snowflake Size", 
    sizing_mode='stretch_both')
    p.line(times, avg_sizes, line_width=1)


    #p.xaxis.formatter = FuncTickFormatter(code=tickStr())
    # p.xaxis.formatter = DatetimeTickFormatter(
    #     hours=["%d-%m %H:%M"],
    #     days=["%d-%m %H:%M"],
    #     months=["%d-%m %H:%M"],
    #     years=["%d-%m %H:%M"]
    # )

    p.xaxis.axis_label = 'Time'
    p.yaxis.axis_label = 'mm'
    p.xaxis.major_label_text_font_size = '4pt'
    p = plotProperties(p)

    return p


def getSizeHist(sizes: list):

    if not sizes or min(sizes) <= 0:
        print("Invalid or empty sizes list")
        # Handle this case appropriately
        return None
    

    min_size = max(min(sizes), 0.1)
    max_size = max(sizes)
    
    # Create bins dynamically based on the data range
    bins = np.linspace(min_size, max_size, 20)

    # Prepare the data
    hist, edges = np.histogram(sizes, bins=bins)

    # Create a new plot
    p = figure(title="Snowflake Size Distribution", background_fill_color="#fafafa", 
               x_axis_type="linear", y_axis_type="log",
               x_range=(0,10), y_range=(1, 5000),
               sizing_mode='stretch_both')

    # Add a quad glyph with log-scaled edges
    p.quad(top=hist, bottom=0.1, left=edges[:-1], right=edges[1:], fill_color="navy", line_color="white", alpha=0.7)



    # Custom tick formatter to replace 10^0 with 0
    p.yaxis.formatter = FuncTickFormatter(code="""
        if (tick == 1) {
            return '0';
        }
        return tick.toString();
    """)

    # Set plot properties
    p.xaxis.axis_label = 'Size in mm'
    p.yaxis.axis_label = 'Count (log)'
    p = plotProperties(p)

    # Explicitly use LogAxis for the x-axis
    p.xaxis[0] = LogAxis()

    return p

def getSnowRateHist(timestamps: list):
    if not timestamps:
        print("Empty timestamp list")
        return None

    buckets = [datetime(dt.year, dt.month, dt.day, dt.hour, 0) for dt in timestamps]
    frequency = Counter(buckets)

    start_time = min(buckets)
    end_time = max(buckets)

    # Generate a complete list of ten-minute intervals within the range
    current_time = start_time
    while current_time <= end_time:
        if current_time not in frequency:
            frequency[current_time] = 0
        current_time += timedelta(minutes=60)

    # Sort and prepare data for plotting, rest of the code as before
    times, counts = zip(*sorted(frequency.items()))
    times = np.array(times, dtype=np.datetime64)
    counts = np.array(counts)

    # Create a Bokeh plot
    p = figure(x_axis_type="datetime", title="Snowflake Count", 
    sizing_mode='stretch_both')
    p.line(times, counts, line_width=1)

    #p.xaxis.formatter = FuncTickFormatter(code=tickStr())
    # p.xaxis.formatter = DatetimeTickFormatter(
    #     hours=["%d-%m %H:%M"],
    #     days=["%d-%m %H:%M"],
    #     months=["%d-%m %H:%M"],
    #     years=["%d-%m %H:%M"]
    # )
    
    p.xaxis.axis_label = 'Time'
    p.yaxis.axis_label = 'Count'
    p.xaxis.major_label_text_font_size = '4pt'
    p = plotProperties(p)
    
    return p


def getData(sizes: list, times: list, storm: int, swe: dict, dens: dict, acc: dict, temp: dict, rh: dict, snowdepth: dict, wind: dict):
    if None not in [swe, dens, acc]:
        #deid
        try:
            p1swe = deidPlot(swe,'mm','SWE (Snow Water Equivalent)')
            p2dens = deidPlot(dens,'kg/m^3','Density')
            p3acc = deidPlot(acc,'mm','Snow Acculumation')
            save_plot(p1swe, f'SWE{storm}')
            save_plot(p2dens, f'density{storm}')
            save_plot(p3acc, f'acc{storm}')
        except:
            pass


    #masc
    p4sizes = getSizeHist(sizes)
    p5times = getSnowRateHist(times)
    p10sizeTime = getSizeTime(sizes, times)

    #meso
    p6temp = mesoPlot(temp, 'Celsius', 'Air Temperature')
    p7rh = mesoPlot(rh, '%', 'Relative Humidity')
    p8snowdepth = mesoPlot(snowdepth, 'mm', 'Snow Depth')
    p9wind = mesoPlot(wind, 'm/s', 'Wind Speed')

    # write
    save_plot(p4sizes, f'sizes{storm}')
    save_plot(p5times, f'rate{storm}')
    save_plot(p6temp, f'temp{storm}')
    save_plot(p7rh, f'rh{storm}')
    save_plot(p8snowdepth, f'snowdepth{storm}')
    save_plot(p9wind, f'wind{storm}')
    save_plot(p10sizeTime, f'sizeTime{storm}')
