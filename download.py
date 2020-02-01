import argparse
import csv
import os
import glob
import youtube_dl
from pathlib import Path
from moviepy.video.io.VideoFileClip import VideoFileClip
import youtube_dl


#
# Run this script on the file generated by preprocess.py
# This script will download a section of the videos that are specified by the given args.csv
# The exact range that this process will download will depend on the number of total jobs, args.jobs, and the id of this job, args.id that are provided.
# 
# To download all of the files specified in the csv file, set use options: --jobs 1 --id 0
#


def download_webfile(url, filename=None, **ydl_opts):
    try:
        if filename is not None:
            ydl_opts["outtmpl"]= filename
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return True
    except:
        return False


parser = argparse.ArgumentParser()
parser.add_argument('--csv', help='path to modified csv file containing url links to download')
parser.add_argument('--categories', help='path to csv file containing url links to download')
parser.add_argument('--jobs', help='Number of different jobs to split the download into', required=True)
parser.add_argument('--id', help='the job id of this download, a number from 0 - (jobs - 1), determines which files this process should d/l', required=True)
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

process_id = int(args.id)
processes = int(args.jobs)

video_name = "youtube_dl-" + str(process_id)


print("Downloading videos from", csvfile)

#####
##### These two numbers need to be updated for each csv file.
##### Would be nicer to make these automatic by 
##### 

total_videos = 0
with open(csvfile) as f:
    csv_reader = csv.reader(f, delimiter=',')
    total_videos = len(csv_reader)

# Split into these number of download sections


left = total_videos/processes * process_id
right = total_videos/proceses * (process_id+1)


print("left ", str(left))
print("right ", str(right))
print("video_name ", video_name)

with open(csvfile) as f:
    csv_reader = csv.reader(f, delimiter=',')
    next(csv_reader)
    line_number = 0 
    for row in csv_reader:
        if (left <= line_number < right):
            line_number += 1
            print("processing video", line_number)
        else:
            line_number += 1
            continue
            


        category, video_id, url, time_start, time_end, group = row

        if category in categories:
            
            if not download_webfile(url, video_name):
                # Could fail due to private video file, no permissions
                continue
            
            video_files = glob.glob(video_name + '.*')
            if len(video_files) == 0:
                print("Unexpected error, cannot find video or d/l failed for", category, url)
                break
            
            video_file = video_files[0]
            try:
                with VideoFileClip(video_file) as video:
                    output_video = "videos/" + group + "/" + category + "/"  + video_id + ".mp4"
                    new = video.subclip(float(time_start), float(time_end))
                    new.write_videofile(output_video, audio=False)
            except:
                print("Failed to clip video for", category, url)

            if os.path.exists(video_file):
                os.remove(video_file)


