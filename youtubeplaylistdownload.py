import os
import subprocess
from pytube import Playlist, YouTube
import time
import re
from urllib.error import HTTPError

def sanitize_filename(filename):
    return re.sub(r'[^\w\-_\. ]', '_', filename)

def download_and_merge(video, output_dir, max_retries=3):
    for attempt in range(max_retries):
        try:
            video_stream = video.streams.filter(adaptive=True, file_extension='mp4', only_video=True).order_by('resolution').desc().first()
            audio_stream = video.streams.filter(only_audio=True).order_by('abr').desc().first()
            
            if not video_stream or not audio_stream:
                print(f'No suitable streams found for {video.title}')
                return

            print(f'Downloading video: {video.title} (Resolution: {video_stream.resolution})')
            video_file = video_stream.download(output_path=output_dir, filename_prefix='video_')
            
            print(f'Downloading audio: {video.title} (ABR: {audio_stream.abr})')
            audio_file = audio_stream.download(output_path=output_dir, filename_prefix='audio_')
            
            safe_title = sanitize_filename(video.title)
            output_file = os.path.join(output_dir, f"{safe_title[:50]}.mp4")
            print(f'Merging video and audio: {output_file}')
            
            ffmpeg_command = f'ffmpeg -i "{video_file}" -i "{audio_file}" -c:v copy -c:a aac "{output_file}" -y'
            subprocess.run(ffmpeg_command, shell=True, check=True, stderr=subprocess.DEVNULL)
            
            os.remove(video_file)
            os.remove(audio_file)
            
            print(f'Successfully downloaded and merged: {output_file}')
            return
        except HTTPError as e:
            if e.code == 429:
                print(f"Rate limit exceeded. Waiting for {2**attempt} seconds before retrying...")
                time.sleep(2**attempt)
            else:
                print(f"HTTP Error {e.code}: {e.reason}")
                break
        except Exception as e:
            print(f'Error processing {video.title}: {str(e)}')
            if attempt < max_retries - 1:
                print(f"Retrying in {2**attempt} seconds...")
                time.sleep(2**attempt)
            else:
                print(f"Failed to download {video.title} after {max_retries} attempts.")
    
    time.sleep(2)  # Wait before processing the next video

def download_playlist(url, output_dir='downloads'):
    playlist = Playlist(url)
    os.makedirs(output_dir, exist_ok=True)

    for video_url in playlist.video_urls:
        try:
            video = YouTube(video_url)
            print(f'\nProcessing: {video.title}')
            download_and_merge(video, output_dir)
        except Exception as e:
            print(f'Error accessing video: {str(e)}')
        time.sleep(1)  # Wait between each video to avoid rate limiting

if __name__ == "__main__":
    playlist_url = 'https://www.youtube.com/playlist?list=PL22egh3ok4cP0T7UZRmP6TMLErZYWMN-l'#paste youtube playlist url
    download_playlist(playlist_url)
