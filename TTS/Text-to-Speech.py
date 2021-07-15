from gtts import gTTS

import os

mytext="my name is rahul"

language='en'

output= gTTS(text=mytext,lang=language,slow=False)

output.save("output.mp3")

os.system("mpg123 output.mp3")