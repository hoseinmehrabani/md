import sounddevice as sd 
def record_sound(filename):
    fs = 44100 # نرخ نمونه برداری هر ثانیه (هر ثانیه 44,100 نمونه برداری صورت میگیرد) 
    duration = 5 # مدت زمان ضبط (ثانیه) 
    print('Recording...')
    sd = open("welcome.wav", "a")
    recording = sd.rec(int(duration * fs), channels=2, blocking=True, dtype='float64')
    print('Recording done.') 
    sd.write(filename, recording, fs)
def play_sound(filename): 
    wave_obj = sa.WaveObject.from_wave_file(filename) 
    play_obj = wave_obj.play()
    play_obj.wait_done() 
# ضبط صدا 
record_sound('welcome.wav') 
# پخش صدا 
play_sound('welcome.wav')