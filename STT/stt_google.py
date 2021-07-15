import speech_recognition as s
sr = s.Recognizer()
print("*recording*")
with s.Microphone() as m:
    audio = sr.listen(m)
    query=sr.recognize_google(audio,language='en')
    print(query)
    