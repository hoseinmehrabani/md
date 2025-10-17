import os
import pygame
import tkinter as tk
from tkinter import filedialog, Listbox, Scrollbar, messagebox, ttk
from pydub import AudioSegment
from pydub.playback import play
import threading
import numpy as np

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Music Player")
        pygame.mixer.init()

        # Tabs
        self.tab_control = ttk.Notebook(root)
        self.tab1 = ttk.Frame(self.tab_control)
        self.tab2 = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab1, text='Music Player')
        self.tab_control.add(self.tab2, text='Favorites')
        self.tab_control.pack(expand=1, fill='both')

        self.create_music_tab()
        self.create_favorites_tab()
        self.is_paused = False

        # Load tracks
        self.tracks = []

    def create_music_tab(self):
        self.track_list = Listbox(self.tab1, selectmode=tk.SINGLE)
        self.track_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = Scrollbar(self.tab1)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.track_list.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.track_list.yview)

        self.play_button = tk.Button(self.tab1, text="Play", command=self.play)
        self.play_button.pack()
        self.pause_button = tk.Button(self.tab1, text="Pause", command=self.pause)
        self.pause_button.pack()
        self.stop_button = tk.Button(self.tab1, text="Stop", command=self.stop)
        self.stop_button.pack()
        self.load_button = tk.Button(self.tab1, text="Load Music", command=self.load_music)
        self.load_button.pack()

        self.volume_label = tk.Label(self.tab1, text="Volume")
        self.volume_label.pack()
        self.volume_scale = tk.Scale(self.tab1, from_=0, to=1, resolution=0.1, orient=tk.HORIZONTAL, command=self.set_volume)
        self.volume_scale.set(0.5)
        self.volume_scale.pack()

        self.dark_mode_var = tk.BooleanVar()
        self.dark_mode_check = tk.Checkbutton(self.tab1, text="Dark Mode", variable=self.dark_mode_var, command=self.toggle_dark_mode)
        self.dark_mode_check.pack()

        self.skip_silence_var = tk.BooleanVar()
        self.skip_silence_check = tk.Checkbutton(self.tab1, text="Skip Silence", variable=self.skip_silence_var)
        self.skip_silence_check.pack()

        self.crossfade_label = tk.Label(self.tab1, text="Crossfade Duration (ms)")
        self.crossfade_label.pack()
        self.crossfade_entry = tk.Entry(self.tab1)
        self.crossfade_entry.pack()
        self.crossfade_entry.insert(0, "500")  # Default crossfade duration

    def create_favorites_tab(self):
        self.favorites_list = Listbox(self.tab2, selectmode=tk.SINGLE)
        self.favorites_list.pack(fill=tk.BOTH, expand=True)
        self.add_to_favorites_button = tk.Button(self.tab2, text="Add to Favorites", command=self.add_to_favorites)
        self.add_to_favorites_button.pack()

    def load_music(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            for filename in os.listdir(folder_path):
                if filename.endswith(('.mp3', '.wav')):
                    self.track_list.insert(tk.END, os.path.join(folder_path, filename))
                    self.tracks.append(os.path.join(folder_path, filename))

    def play(self):
        try:
            selected_track = self.track_list.curselection()[0]
            track_path = self.track_list.get(selected_track)

            if self.skip_silence_var.get():
                track_path = self.skip_silence(track_path)

            pygame.mixer.music.load(track_path)
            pygame.mixer.music.play()
            self.is_paused = False
        except IndexError:
            messagebox.showwarning("Warning", "Select a track to play.")

    def pause(self):
        pygame.mixer.music.pause()
        self.is_paused = True

    def stop(self):
        pygame.mixer.music.stop()
        self.is_paused = False

    def add_to_favorites(self):
        try:
            selected_track = self.track_list.curselection()[0]
            track = self.track_list.get(selected_track)
            if track not in self.favorites_list.get(0, tk.END):
                self.favorites_list.insert(tk.END, track)
            else:
                messagebox.showinfo("Info", "Track already in favorites.")
        except IndexError:
            messagebox.showwarning("Warning", "Select a track to add to favorites.")

    def set_volume(self, volume):
        pygame.mixer.music.set_volume(float(volume))

    def toggle_dark_mode(self):
        if self.dark_mode_var.get():
            self.root.config(bg='black')
            for widget in self.root.winfo_children():
                widget.config(bg='black', fg='white')
        else:
            self.root.config(bg='white')
            for widget in self.root.winfo_children():
                widget.config(bg='white', fg='black')

    def skip_silence(self, track_path):
        audio = AudioSegment.from_file(track_path)
        audio = audio.strip_silence(silence_len=1000, silence_thresh=-16)  # 1 second silence
        temp_file = "temp.wav"
        audio.export(temp_file, format="wav")
        return temp_file

if __name__ == "__main__":
    root = tk.Tk()
    player = MusicPlayer(root)
    root.mainloop()
#######################
from pydub import AudioSegment
from pydub.playback import play
import os


def crossfade_tracks(track1_path, track2_path, duration):
    # بارگذاری آهنگ‌ها
    track1 = AudioSegment.from_file(track1_path)
    track2 = AudioSegment.from_file(track2_path)

    # تعیین مدت زمان Crossfade
    duration_ms = duration  # in milliseconds
    if duration_ms > len(track1) or duration_ms > len(track2):
        raise ValueError("Crossfade duration is longer than one of the tracks.")

    # برش آهنگ‌ها برای ترکیب
    track1_end = track1[-duration_ms:]  # آخرین بخش از آهنگ اول
    track2_start = track2[:duration_ms]  # اولین بخش از آهنگ دوم

    # ایجاد اثر Crossfade
    combined = track1[:-duration_ms] + track1_end.fade_out(duration_ms) + track2_start.fade_in(duration_ms) + track2[
                                                                                                              duration_ms:]

    # پخش آهنگ ترکیبی
    play(combined)


if __name__ == "__main__":
    track1 = input("Enter the path for the first track: ")
    track2 = input("Enter the path for the second track: ")
    duration = int(input("Enter crossfade duration in milliseconds: "))

    if not os.path.exists(track1) or not os.path.exists(track2):
        print("One or both of the track paths are invalid.")
    else:
        crossfade_tracks(track1, track2, duration)
