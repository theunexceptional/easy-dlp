import os
import ctypes
import sys
import subprocess
import threading
import tkinter as tk
from tkinter import ttk, filedialog
from tkinter import messagebox

# Function to show a Windows notification popup
def show_notification(title, message):
    ctypes.windll.user32.MessageBoxW(0, message, title, 1)

# Function to update the progress bar
def update_progress(process, progress_var):
    while process.poll() is None:
        progress_var.set(progress_var.get() + 10)
        root.update_idletasks()
    progress_var.set(100)
    show_notification("Download Complete", "Your downloads have finished successfully!")

# Function to start the download process
def start_download():
    video_urls = video_url_entry.get("1.0", tk.END).strip().split("\n")
    if not video_urls or video_urls == ['']:
        messagebox.showerror("Error", "Please enter at least one video URL.")
        return

    av_mode = "bestaudio" if audio_var.get() else f"bestvideo[height<={quality_var.get()}]+bestaudio"
    format_option = "--merge-output-format mp4" if not audio_var.get() else ""
    sponsorblock_option = "--sponsorblock-mark all" if sponsor_var.get() else ""

    embed_options = []
    if metadata_var.get():
        embed_options.append("--add-metadata")
    if chapters_var.get():
        embed_options.append("--embed-chapters")
    if thumbnail_var.get():
        embed_options.append("--embed-thumbnail")
    if split_var.get():
        embed_options.append("--split-chapters")
    embed_options_string = " ".join(embed_options)

    sub_lang_option = ""
    if embed_subs_var.get():
        sub_lang_option = f"--sub-langs {sub_lang_entry.get().strip()}"
    
    clip_option = ""
    if clip_var.get():
        clip_option = f"--download-sections *{start_time_entry.get()}-{end_time_entry.get()}"
    
    for video_url in video_urls:
        command = f'yt-dlp.exe -f "{av_mode}" {format_option} {sponsorblock_option} {embed_options_string} {sub_lang_option} {clip_option} "{video_url}"'
        process = subprocess.Popen(command, shell=True)
        threading.Thread(target=update_progress, args=(process, progress_var)).start()

# GUI Setup
root = tk.Tk()
root.title("YouTube Downloader by Bhavya Khandelwal")
root.geometry("600x500")

# Video URL Input
tk.Label(root, text="Enter YouTube Video URLs (one per line):").pack(anchor="w", padx=10, pady=5)
video_url_entry = tk.Text(root, height=3, width=70)
video_url_entry.pack(padx=10, pady=5)

# Audio or Video Selection
audio_var = tk.BooleanVar()
tk.Checkbutton(root, text="Download Audio Only", variable=audio_var).pack(anchor="w", padx=10)

# Video Quality Selection
tk.Label(root, text="Select Video Quality:").pack(anchor="w", padx=10)
quality_var = tk.StringVar(value="720")
ttk.Combobox(root, textvariable=quality_var, values=["144", "240", "360", "480", "720", "1080", "1440", "2160"]).pack(anchor="w", padx=10, pady=5)

# Additional Options
sponsor_var = tk.BooleanVar()
metadata_var = tk.BooleanVar()
chapters_var = tk.BooleanVar()
thumbnail_var = tk.BooleanVar()
split_var = tk.BooleanVar()
embed_subs_var = tk.BooleanVar()
clip_var = tk.BooleanVar()

tk.Checkbutton(root, text="Skip Sponsors & Intros", variable=sponsor_var).pack(anchor="w", padx=10)
tk.Checkbutton(root, text="Embed Metadata", variable=metadata_var).pack(anchor="w", padx=10)
tk.Checkbutton(root, text="Embed Chapters", variable=chapters_var).pack(anchor="w", padx=10)
tk.Checkbutton(root, text="Embed Thumbnails", variable=thumbnail_var).pack(anchor="w", padx=10)
tk.Checkbutton(root, text="Split Video into Chapters", variable=split_var).pack(anchor="w", padx=10)
tk.Checkbutton(root, text="Embed Subtitles", variable=embed_subs_var, command=lambda: sub_lang_entry.pack() if embed_subs_var.get() else sub_lang_entry.pack_forget()).pack(anchor="w", padx=10)

sub_lang_entry = tk.Entry(root)
sub_lang_entry.pack(anchor="w", padx=10)
sub_lang_entry.pack_forget()

tk.Checkbutton(root, text="Download Specific Clip", variable=clip_var, command=lambda: clip_frame.pack() if clip_var.get() else clip_frame.pack_forget()).pack(anchor="w", padx=10)

# Clip Frame
clip_frame = tk.Frame(root)
tk.Label(clip_frame, text="Start Time:").pack(side="left", padx=5)
start_time_entry = tk.Entry(clip_frame, width=10)
start_time_entry.pack(side="left", padx=5)
tk.Label(clip_frame, text="End Time:").pack(side="left", padx=5)
end_time_entry = tk.Entry(clip_frame, width=10)
end_time_entry.pack(side="left", padx=5)
clip_frame.pack(anchor="w", padx=10, pady=5)
clip_frame.pack_forget()

# Progress Bar
progress_var = tk.IntVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100, length=580)
progress_bar.pack(pady=10)

# Download Button
tk.Button(root, text="Download", command=start_download, height=2, width=80).pack(pady=30)
root.mainloop()
