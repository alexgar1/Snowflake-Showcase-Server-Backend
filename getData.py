from bokeh.plotting import figure
import pandas as pd
from bokeh.io import output_file, save
from bokeh.layouts import gridplot
from datetime import datetime, timedelta
import numpy as np
from bokeh.models import FuncTickFormatter, LogAxis, FixedTicker, DatetimeTickFormatter, Dropdown

PATH = '/uufs/chpc.utah.edu/common/home/snowflake/public_html/LiveFeed/'

def getSizeHist(sizes: list):

    if not sizes:
        sizes = [0]
    

    min_size = max(min(sizes), 0.1)
    max_size = max(sizes)
        # Adjust base of logarithm to make scale less extreme
    log_base = 2  # For example, base 2
    num_bins = 20  # Adjust number of bins as needed

    # Using logarithmic bins with a different base
    bins = np.logspace(np.log(min_size) / np.log(log_base), np.log(max_size) / np.log(log_base), num_bins, base=log_base)

    # Prepare the data
    hist, edges = np.histogram(sizes, bins=bins)

    # Create a new plot
    p = figure(title="Snowflake Size Distribution", background_fill_color="#fafafa", y_axis_type="log",x_axis_type="log", x_range=(0.2,18), y_range=(1, 2000))

    # Add a quad glyph with log-scaled edges
    p.quad(top=hist, bottom=0.1, left=edges[:-1], right=edges[1:], fill_color="navy", line_color="white", alpha=0.7)


    # Adding specific ticks at 200, 500, and 1000
    specific_ticks = [1,5,10,20,50,100,200, 500, 1000,2000]
    p.yaxis.ticker = FixedTicker(ticks=specific_ticks)

    # Custom tick formatter to replace 10^0 with 0
    p.yaxis.formatter = FuncTickFormatter(code="""
        if (tick == 1) {
            return '0';
        }
        return tick.toString();
    """)

    # Set plot properties
    p.xaxis.axis_label = 'Size in mm (log scale)'
    p.yaxis.axis_label = 'Count'
    p.title.text_font_size = '16pt'
       
       # Set specific tick at 0.2
    p.xaxis.ticker = FixedTicker(ticks=[0.2,0.5,1,2,4,8,16])

    # Explicitly use LogAxis for the x-axis
    p.xaxis[0] = LogAxis()

    return p

def getSnowRateHist(timestamps: list):
    #if not timestamps:
    #    tirestamps = [datetime.fromtimestamp(0.0)]
    # Converting the list of timestamps to a DataFrame
    df = pd.DataFrame(timestamps, columns=['timestamp'])

    # Counting the number of events in each 10-minute interval
    df.set_index('timestamp', inplace=True)
    resampled_df = df.resample('10T').size().reset_index(name='count')

    resampled_df['count'] = resampled_df['count'].replace(0, 0.1)

        # Rounding the current time down to the nearest 10 minutes
    current_time = datetime.now().replace(second=0, microsecond=0, minute=(datetime.now().minute // 10) * 10)

    # Check if the latest interval is in the data
    if resampled_df['timestamp'].max() < current_time:
        # Append a row with the current time and a count of 0
        resampled_df = resampled_df.append({'timestamp': current_time, 'count': 0}, ignore_index=True)

    # Create a Bokeh plot
    p = figure(x_axis_type="datetime", title="Snowflake Count per 10 Minute Interval", y_range=(0, 500))
    p.line(resampled_df['timestamp'], resampled_df['count'], line_width=4)

    # Set the DatetimeTickFormatter to display ticks every 10 minutes
    p.xaxis.formatter = DatetimeTickFormatter(
        minutes=["%m/%d %H:%M"],
        hours=["%m/%d %H:%M"],
        days=["%m/%d %H:%M"]
    )


    p.xaxis.axis_label = 'Time'
    p.yaxis.axis_label = 'Count'
    p.title.text_font_size = '16pt'
    return p


def getData(sizes: list, times: list, storm: int):
    
    p1 = getSizeHist(sizes)
    p2 = getSnowRateHist(times)

    # Arrange the plots in a grid layout
    grid_layout = gridplot([[p1, p2]])

    storms = []
    for i in range(storm):
        storms.append('data'+str(storm)+'.html')


    # Create dropdown
    drop = Dropdown(label='Select Storm', menu=storms)

    output_file(PATH+'data'+str(storm)+'.html')
    save(grid_layout)

