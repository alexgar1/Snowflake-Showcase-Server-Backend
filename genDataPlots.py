#!/usr/bin/python3

import getData, chooseData, glob, os, re, ast
from datetime import datetime

PATH = '/uufs/chpc.utah.edu/common/home/snowflake/public_html/LiveFeed/data/'

def getFlakes(storm):
    with open(PATH+'flakes'+str(storm)+'.txt', 'r') as flakes:
        try:
            date = flakes.readline().strip()
            line = flakes.readline().strip()
        except:
            date = 0
            line = '[0]'
    return date, ast.literal_eval(line)

def getList(storm):
    sizes = []
    times = []
    with open(PATH+'data'+str(storm)+'.txt', 'r') as f:
        for line in f:
            try:
                segments = line.split(',')

                size = float(segments[4].strip())
                time = float(segments[1].strip())
                # Appending sublist to main data list
                sizes.append(size)
                times.append(datetime.fromtimestamp(time))
            except:
                pass

    return sizes, times

def gen():
    pattern = os.path.join(PATH, 'data*.txt')
    
    storm = 1
    # Use glob to get all files matching the pattern
    files = glob.glob(pattern)
    # Extract the number from each filename and find the maximum
    for file_name in files:
        match = re.search(r'data(\d+).txt', os.path.basename(file_name))
        if match:
            number = int(match.group(1))
            storm = number
    
    sizes, times = getList(storm)
    getData.getData(sizes, times, storm)
    chooseData.call(storm)

def main():
    gen()

if __name__ == '__main__':
    main()
