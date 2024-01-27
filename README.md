# yt_decomp
Python script for splitting YouTube video audio according to timestamps from the description.

## Requirements for running:
python 3 

ffmpeg installed and in $PATH

pytube and youtube_dl python libraries

## Tested on the following platforms:

Gentoo Linux

(should work with MacOS and Windows in theory)

## Current Limitations:
Video must have timestamps in the description in the following format

\<timestamp\> \<title\>

The following formats don't work:

\<title\> \<timestamp\>

\<timstamp\>

Support may be added in the future.
