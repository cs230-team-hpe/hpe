import argparse
import csv
import os
import glob
import youtube_dl
from pathlib import Path
from moviepy.video.io.VideoFileClip import VideoFileClip

import youtube_dl



#
# Run this preprocess.py script on the original kinentics train.csv, test.csv, validate.csv
# to return a format that will be used for download.py
#


parser = argparse.ArgumentParser()
parser.add_argument('--csv', help='path to csv file containing url links to download')
parser.add_argument('--categories', help='path to file containing newline delimited names of categories for videos we want to download.', required=True)
args = parser.parse_args()

categories = dict()
if args.categories:
    with open(args.categories) as f:
        for line in f:
            categories[line.strip()] = 1

for category in categories:
    Path("videos/test/" + category).mkdir(parents=True, exist_ok=True)
    Path("videos/train/" + category).mkdir(parents=True, exist_ok=True)
    Path("videos/validate/" + category).mkdir(parents=True, exist_ok=True)
       
csvfile = "train.csv"
video_name = "youtube_dl-video"

if args.csv:
    csvfile = args.csv

print("Downloading videos from", csvfile)

with open(csvfile) as f:
    csv_reader = csv.reader(f, delimiter=',')
    for row in csv_reader:
        category, url, time_start, time_end, group = row
        if category in categories:
            print("{},{},{},{},{},{}".format(category, categories[category], url, time_start, time_end, group))            
            categories[category] += 1



