# YouTube Playlist Downloader

## Project Overview
This Python script downloads and merges video and audio streams from YouTube playlists using Pytube and FFmpeg.

## Features
- Downloads video and audio streams separately for best quality
- Merges video and audio using FFmpeg
- Handles rate limiting with exponential backoff
- Sanitizes filenames
- Supports downloading entire playlists

## Prerequisites
- Python 3.x
- FFmpeg installed and accessible from the command line
- Required Python libraries: `pytube`

## Installation
1. Clone this repository or download the `youtubeplaylistdownload.py` file.
2. Install the required Python library:
   ```
   pip install pytube
   ```
3. Ensure FFmpeg is installed and accessible from the command line.

## Usage
1. Open the `youtubeplaylistdownload.py` file.
2. Modify the `playlist_url` variable with your desired YouTube playlist URL.
3. Run the script:
   ```
   python youtubeplaylistdownload.py
   ```

## Limitations
- Depends on the Pytube library, which may break if YouTube changes its structure.
- Requires a stable internet connection for downloading large playlists.
- Download speed may be affected by YouTube's rate limiting.
- It downloads at a maximum quality of 1080p.
