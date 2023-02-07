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

def process_times(vid):
    desc = YouTube(vid).description
    timestamp_regex = re.compile(r'[0-9]?[0-9]?:?[0-9]?[0-9]:[0-9][0-9]')
    stmp_list = timestamp_regex.findall(desc)
    fin_list = []
    for x in stmp_list:
        if not (x in fin_list):
            fin_list.append(x)
    
    return list(map(stamp_to_sec, fin_list))


vid = input("Enter a YouTube Video URL: ")

times_list = process_times(vid)

print(times_list)


