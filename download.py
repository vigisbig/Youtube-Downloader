from pytubefix import YouTube, Playlist
import re
import os
from pytube.exceptions import VideoUnavailable

def sanitize_filename(filename):
    # Replace invalid characters with underscores
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def get_available_streams(video, download_type='V'):
    if download_type == 'A':
        # Audio-only streams, sorted by bitrate (highest first)
        return video.streams.filter(only_audio=True).order_by('abr').desc()
    return video.streams.filter(progressive=True, file_extension='mp4')

def choose_quality(streams, download_type='V'):
    print("Available quality options:")
    for i, stream in enumerate(streams):
        if download_type == 'A':
            print(f"{i + 1}. {stream.abr} - {stream.mime_type}")
        else:
            print(f"{i + 1}. {stream.resolution} - {stream.mime_type}")
    while True:
        try:
            choice = int(input("Enter the number corresponding to your preferred quality: "))
            if 1 <= choice <= len(streams):
                return streams[choice - 1]
            else:
                print(f"Please enter a number between 1 and {len(streams)}")
        except ValueError:
            print("Please enter a valid number")

def choose_download_type():
    while True:
        choice = input("Enter 'V' to download video or 'A' to download audio only: ").upper()
        if choice in ('V', 'A'):
            return choice
        print("Invalid choice. Please enter 'V' or 'A'.")

def download_single_or_playlist():
    choice = input("Enter 'S' to download a single video or 'P' to download a playlist: ").upper()
    download_type = choose_download_type()
    if choice == 'S':
        video_url = input("Enter the YouTube video URL: ")
        output_path = input("Enter the output path (default: '/home/vigisbig/PD Contents/Music'): ").strip() or '/home/vigisbig/PD Contents/Music'
        download_video(video_url, output_path, download_type)
    elif choice == 'P':
        playlist_url = input("Enter the YouTube playlist URL: ")
        output_path = input("Enter the output path (default: '/home/vigisbig/PD Contents/Music'): ").strip() or '/home/vigisbig/PD Contents/Music'
        download_playlist(playlist_url, output_path, download_type)
    else:
        print("Invalid choice. Please enter 'S' or 'P'.")

def download_playlist(playlist_url, output_path='/home/vigisbig/PD Contents/Music', download_type='V'):
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_path, exist_ok=True)
        playlist = Playlist(playlist_url)
        print(f"Downloading playlist: {playlist.title}")
        for video_url in playlist.video_urls:
            download_video(video_url, output_path, download_type)
        print("Playlist download complete.")
    except Exception as e:
        print(f"Error downloading playlist: {e}")

def download_video(video_url, output_path='/home/vigisbig/PD Contents/Music', download_type='V'):
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_path, exist_ok=True)
        yt = YouTube(video_url)
        video_title = yt.title
        label = "audio" if download_type == 'A' else "video"
        print(f"\nDownloading {label}: {video_title}")
        streams = get_available_streams(yt, download_type)
        if not streams:
            print(f"No {label} stream available. Skipping.")
            return
        selected_stream = choose_quality(streams, download_type)
        sanitized_title = sanitize_filename(video_title)
        # Download the video or audio
        print(f"Starting download...")
        if download_type == 'A':
            extension = selected_stream.mime_type.split('/')[-1]
            selected_stream.download(output_path=output_path, filename=f"{sanitized_title}.{extension}")
            print(f"✓ Audio download complete: {video_title} at {selected_stream.abr} quality.")
            print(f"  Saved to: {os.path.abspath(output_path)}/{sanitized_title}.{extension}\n")
        else:
            selected_stream.download(output_path=output_path, filename=f"{sanitized_title}.mp4")
            print(f"✓ Video download complete: {video_title} in {selected_stream.resolution} quality.")
            print(f"  Saved to: {os.path.abspath(output_path)}/{sanitized_title}.mp4\n")
    except VideoUnavailable:
        print(f"Video is unavailable or restricted to members-only. Skipping download.")
    except Exception as e:
        print(f"Error downloading video: {e}")

if __name__ == "__main__":
    download_single_or_playlist()