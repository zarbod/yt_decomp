#!/usr/bin/env python3
from pytube import YouTube
import platform
import operator
import os 
import re
import youtube_dl

system_delim = '\\' if platform.system() == "Windows" else '/'

'''
converts timestamp string to its equivalent representation in seconds
'''
def stamp_to_sec(stamp):
    units = stamp.split(":")
    units = list(map(int, units))
    units.reverse()
    return sum(list(map(operator.mul, units, [1, 60, 3600]))) # multiply units of time by their appropriate weights to convert to seconds

'''
returns a list of lists of size 2, each of which
contains a name and a timestamp associated with that name
'''
def process_chapters(vid):
    desc = YouTube(vid).description

    # match all timestamps in the description using regex
    timestamp_regex = re.compile(r'[0-9]?[0-9]?:?[0-9]?[0-9]:[0-9][0-9]\s.*\n?')
    stmp_list = timestamp_regex.findall(desc)

    # split every string into timestamp and name
    stmp_list = map(lambda x : x.split(' ', 1), stmp_list)

    # clean up ends of the names of chapters
    stmp_list = map(lambda x : [x[0], x[1][:-1]] if x[1][:-1] == '\n' else x, stmp_list) 
    return list(stmp_list)

'''
Perform audio decomposition using ffmpeg
'''
def decompose(times, names, dir_name, file_name):
    i = 2
    start_time = 0
    end_time = times[1]
    for name in names:
        name_of_file = (name[1:] if name[0] == '-' else name).strip()
        name_of_file = str("\"" + dir_name + system_delim + name_of_file + ".mp3\"")
        end_chunk = " -t " + str(end_time - start_time) if end_time != -1 else ""  # determines how long to run the audio before cutting it.
        command = "ffmpeg -ss " + str(start_time) + " -i " + file_name + end_chunk + " " + name_of_file
        os.system(command)
        start_time = end_time
        if i < len(times):
            end_time = times[i]
        else:
            end_time = -1
        i += 1
    
vid = input("Enter a YouTube Video URL: ")
dir = input("Enter name of directory to send to: ")

if (not os.path.exists(dir)):
    os.mkdir(dir)

chapters = process_chapters(vid)

times = list(map(stamp_to_sec, list(map(lambda x : x[0], chapters))))
names = list(map(lambda x : x[1], chapters))

file_name = dir + system_delim + 'audio77788899911122qqqddfffeeee.mp3'

ydl_opts = {
        'outtmpl': file_name,
        'format' : 'bestaudio/best',
        'postprocessors' : [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
}

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([vid])

decompose(times, names, dir, file_name)

os.remove(file_name) # delete audio file for the entire video
