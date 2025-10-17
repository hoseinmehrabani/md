import tkinter as tk
import sounddevice as sd
import numpy as np
import wave
from pydub import AudioSegment

sample_rate = 44100
duration = 10


def record_audio():
    print("ضبط صدا آغاز شد...")
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=2, dtype='int16')
    sd.wait()
    print("ضبط صدا به پایان رسید.")

    with wave.open('recorded_audio.wav', 'wb') as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(audio_data.tobytes())

    audio = AudioSegment.from_wav('recorded_audio.wav')
    audio.export('recorded_audio.mp3', format='mp3')
    print("صدا به فرمت MP3 ذخیره شد.")


window = tk.Tk()
window.title("ضبط صدا")

label = tk.Label(window, text="میکروفون")
label.pack(pady=20)

record_button = tk.Button(window, text="ظبط صدا", command=record_audio)
record_button.pack(pady=20)

window.mainloop()
