import speech_recognition as sr
recognize = sr.Recognizer()


with sr.Microphone() as source:
    print("listening ..")
    audio = recognize.listen(source)
txt = recognize.recognize_google_cloud(audio, language="fa_IR")
print(txt)
