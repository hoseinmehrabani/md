import os
import tkinter as tk
from tkinter import filedialog, messagebox
from google.cloud import speech
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import threading

# تنظیم کلید API
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path_to_your_service_account.json"

def transcribe_audio(file_path, language_code):
    try:
        client = speech.SpeechClient()
        with open(file_path, "rb") as audio_file:
            content = audio_file.read()

        audio = speech.RecognitionAudio(content=content)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code=language_code,
            enable_word_time_offsets=True,
        )

        response = client.long_running_recognize(config=config, audio=audio)
        response = response.result(timeout=90)

        subtitles = []
        for result in response.results:
            for word_info in result.alternatives[0].words:
                start_time = word_info.start_time.total_seconds()
                end_time = word_info.end_time.total_seconds()
                transcript = word_info.word
                subtitles.append((start_time, end_time, transcript))

        return subtitles
    except Exception as e:
        messagebox.showerror("خطا", f"خطایی در پردازش صوت: {e}")

def add_subtitles_with_timestamps(video_path, subtitles_with_timestamps, font_size, color, position):
    video = VideoFileClip(video_path)
    clips = []

    current_text = ""
    current_start = 0
    current_end = 0

    for (start_time, end_time, text) in subtitles_with_timestamps:
        if current_text == "":
            current_text = text
            current_start = start_time
            current_end = end_time
        elif start_time <= current_end:
            current_text += " " + text
            current_end = end_time
        else:
            clips.append((current_start, current_end, current_text))
            current_text = text
            current_start = start_time
            current_end = end_time

    if current_text:
        clips.append((current_start, current_end, current_text))

    final_clips = []
    for (start, end, text) in clips:
        subtitle = TextClip(text, fontsize=font_size, color=color)
        subtitle = subtitle.set_pos('bottom' if position == 'bottom' else 'top').set_duration(end - start).set_start(start)
        final_clips.append(subtitle)

    final_video = CompositeVideoClip([video] + final_clips)
    final_video.write_videofile("output_video_with_timestamps.mp4", codec='libx264')

def save_srt(subtitles, output_file):
    with open(output_file, "w", encoding="utf-8") as f:
        for i, (start, end, text) in enumerate(subtitles):
            f.write(f"{i + 1}\n")
            f.write(f"{format_time(start)} --> {format_time(end)}\n")
            f.write(f"{text}\n\n")

def format_time(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours):02}:{int(minutes):02}:{seconds:06.3f}".replace('.', ',')

def process_files(audio_file_path, video_file_path, language_code, font_size, color, position):
    transcripts = transcribe_audio(audio_file_path, language_code)
    if transcripts:
        add_subtitles_with_timestamps(video_file_path, transcripts, font_size, color, position)
        save_srt(transcripts, "output_subtitles.srt")
        messagebox.showinfo("موفقیت", "زیرنویس‌ها با موفقیت تولید و ذخیره شدند.")

def main():
    root = tk.Tk()
    root.withdraw()

    audio_file_path = filedialog.askopenfilename(title="انتخاب فایل صوتی", filetypes=[("Audio Files", "*.wav;*.mp3")])
    if not audio_file_path:
        return

    video_file_path = filedialog.askopenfilename(title="انتخاب فایل ویدیویی", filetypes=[("Video Files", "*.mp4;*.avi")])
    if not video_file_path:
        return

    language_code = input("لطفاً کد زبان را وارد کنید (مثلاً 'fa-IR' برای فارسی، 'en-US' برای انگلیسی): ")
    font_size = int(input("لطفاً اندازه فونت زیرنویس را وارد کنید (مثلاً 24): "))
    color = input("لطفاً رنگ زیرنویس را وارد کنید (مثلاً 'white'): ")
    position = input("موقعیت زیرنویس را وارد کنید ('top' یا 'bottom'): ")

    # استفاده از threading برای پردازش
    threading.Thread(target=process_files, args=(audio_file_path, video_file_path, language_code, font_size, color, position)).start()

if __name__ == "__main__":
    main()
