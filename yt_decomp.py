#!/usr/bin/env python3
from pytube import YouTube
import operator
import re
import os 
import youtube_dl

def stamp_to_sec(stamp):
    units = stamp.split(":")
    units = list(map(int, units))
    units.reverse()
    return sum(list(map(operator.mul, units, [1, 60, 3600])))
def process_chapters(vid):
    desc = YouTube(vid).description
    timestamp_regex = re.compile(r'[0-9]?[0-9]?:?[0-9]?[0-9]:[0-9][0-9]\s.*\n')
    stmp_list = timestamp_regex.findall(desc)
    stmp_list = map(lambda x : x.split(' ', 1), stmp_list)
    stmp_list = map(lambda x : [x[0], x[1][:-1]], stmp_list)
    return list(stmp_list)

def decompose(times, names, dir_name):
    i = 2
    start_time = 0
    end_time = times[1]
    for name in names:
        name_of_file = (name[1:] if name[0] == '-' else name).strip()
        name_of_file = str("\"" + dir_name + "/" + name_of_file + ".mp3\"")
        end_chunk = "-t " + str(end_time) if end_time != -1 else "" 
        command = "ffmpeg -ss " + str(start_time) + " -i audio.mp3 " + end_chunk + " " + name_of_file
        # print(command)
        os.system(command)
        start_time = end_time
        if i < len(times):
            end_time = times[i]
        else:
            end_time = -1
        i += 1
    
vid = input("Enter a YouTube Video URL: ")
dir = input("Enter name of directory to send to: ")
os.mkdir(dir)
chapters = process_chapters(vid)

times = list(map(stamp_to_sec, list(map(lambda x : x[0], chapters))))
names = list(map(lambda x : x[1], chapters))

ydl_opts = {
        'outtmpl':'audio.mp3',
        'format' : 'bestaudio/best',
        'postprocessors' : [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
}

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([vid])

decompose(times, names, dir)

os.system("rm -rf audio.mp3")
