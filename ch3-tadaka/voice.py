from gtts import gTTS
import os

def speak(text='Sorry, I did not understand'):
    language = 'en'
    myobj = gTTS(text=text, lang=language, slow=False)
    myobj.save("data/welcome.mp3")
    print(text)
    os.system("mpg321 data/welcome.mp3 &> /dev/null")
