from pytube import YouTube, Playlist
import re
from pytube.exceptions import VideoUnavailable

def sanitize_filename(filename):
    # Replace invalid characters with underscores
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def get_available_streams(video):
    return video.streams.filter(progressive=True, file_extension='mp4')

def choose_quality(streams):
    print("Available quality options:")
    for i, stream in enumerate(streams):
        print(f"{i + 1}. {stream.resolution} - {stream.mime_type}")

    choice = int(input("Enter the number corresponding to your preferred quality: "))
    return streams[choice - 1]

def download_single_or_playlist():
    choice = input("Enter 'S' to download a single video or 'P' to download a playlist: ").upper()

    if choice == 'S':
        video_url = input("Enter the YouTube video URL: ")
        output_path = input("Enter the output path (default: 'downloads'): ") or 'downloads'
        download_video(video_url, output_path)
    elif choice == 'P':
        playlist_url = input("Enter the YouTube playlist URL: ")
        output_path = input("Enter the output path (default: 'downloads'): ") or 'downloads'
        download_playlist(playlist_url, output_path)
    else:
        print("Invalid choice. Please enter 'S' or 'P'.")

def download_playlist(playlist_url, output_path='downloads'):
    playlist = Playlist(playlist_url)

    print(f"Downloading playlist: {playlist.title}")

    for video_url in playlist.video_urls:
        download_video(video_url, output_path)

    print("Playlist download complete.")

def download_video(video_url, output_path='downloads'):
    try:
        yt = YouTube(video_url)
        video_title = yt.title
        print(f"Downloading video: {video_title}")

        streams = get_available_streams(yt)
        if not streams:
            print("No progressive stream available. Skipping video.")
            return

        selected_stream = choose_quality(streams)
        sanitized_title = sanitize_filename(video_title)
        download_path = f"{output_path}/{sanitized_title}.mp4"
        selected_stream.download(output_path=output_path, filename=sanitized_title)

        print(f"Video download complete: {video_title} in {selected_stream.resolution} quality.")
    except VideoUnavailable:
        print(f"Video {video_title} is unavailable or restricted to members-only. Skipping download.")

if __name__ == "__main__":
    download_single_or_playlist()
