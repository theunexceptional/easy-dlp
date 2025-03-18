import os
import ctypes
import sys
import time
import shutil
import subprocess

def show_notification(title, message):
    ctypes.windll.user32.MessageBoxW(0, message, title, 1)

def download_video():
    print("Welcome to yt-dlp downloader extension by Bhavya Khandelwal!")

    # Bulk download option
    bulk_download = input("Download multiple videos? (yes/no): ").strip().lower() == "yes"
    video_urls = []

    if bulk_download:
        print("Enter video URLs one by one. Press Enter without typing to finish.")
        count = 1
        while True:
            url = input(f"{count}: ").strip()
            if not url:
                break
            video_urls.append(url)
            count += 1
    else:
        video_urls.append(input("Enter the YouTube video URL: ").strip())

    # Audio/Video selection
    av_mode = "Audio Only" if input("Download Audio only? (yes/no): ").strip().lower() == "yes" else "Video + Audio"
    
    # Quality selection (only for Video + Audio)
    height = ""
    if av_mode == "Video + Audio":
        height = input("Enter video quality (1080, 720, etc.) or press Enter for default: ").strip() or "720"
    
    # Subtitle options
    embed_subs = input("Embed subtitles? (yes/no): ").strip().lower() == "yes"
    sub_lang_option = f"--sub-langs {input('Enter subtitle language (en/hi/auto): ').strip()}" if embed_subs else ""
    
    # SponsorBlock integration
    sponsorblock_option = "--sponsorblock-mark all" if input("Skip sponsors and intros? (yes/no): ").strip().lower() == "yes" else ""
    
    # Additional embedding options
    embed_options = []
    if input("Embed metadata? (yes/no): ").strip().lower() == "yes":
        embed_options.append("--add-metadata")
    if input("Embed chapters? (yes/no): ").strip().lower() == "yes":
        embed_options.append("--embed-chapters")
    if input("Embed thumbnails? (yes/no): ").strip().lower() == "yes":
        embed_options.append("--embed-thumbnail")
    if input("Split into chapters? (yes/no): ").strip().lower() == "yes":
        embed_options.append("--split-chapters")
    
    # Clip downloading
    clip_download = input("Download a specific clip? (yes/no): ").strip().lower() == "yes"
    clip_option = ""
    if clip_download:
        start_time = input("Enter start timestamp (HH:MM:SS or seconds): ").strip()
        end_time = input("Enter end timestamp (HH:MM:SS or seconds): ").strip()
        clip_option = f"--download-sections *{start_time}-{end_time}"
    
    embed_options_string = " ".join(embed_options)

    for video_url in video_urls:
        command = f'yt-dlp.exe -f "bestaudio" {sponsorblock_option} {embed_options_string} {sub_lang_option} {clip_option} "{video_url}"'
        if av_mode == "Video + Audio":
            command = f'yt-dlp.exe -f "bestvideo[height<={height}]+bestaudio" --merge-output-format mp4 {sponsorblock_option} {embed_options_string} {sub_lang_option} {clip_option} "{video_url}"'

        print("\nGenerated command and now, cross your fingers!:")
        print(command)
        os.system(command)
    
    show_notification("Download Complete", "Your downloads have finished successfully!")

if __name__ == "__main__":
    download_video()
