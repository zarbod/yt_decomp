#!/usr/bin/env python3
import re
import operator
from pytube import YouTube
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
    # fin_list = []
    # for x in stmp_list:
    #     if not (x in fin_list):
    #         fin_list.append(x)
    # 
    # return list(map(stamp_to_sec, fin_list))

vid = input("Enter a YouTube Video URL: ")

chapters = process_chapters(vid)

times = list(map(stamp_to_sec, list(map(lambda x : x[0], chapters))))
names = list(map(lambda x : x[1], chapters))

print(times)
print(names)

ydl_opts = {
        'format' : 'bestaudio/best',
        'postprocessors' : [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
}

