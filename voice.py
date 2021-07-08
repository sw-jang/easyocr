import pyttsx3

engine = pyttsx3.init()

def initialize_voice():
    #voice engine 'pyttsx3' initialization and setting
    engine.setProperty('rate', 180)
    rate = engine.getProperty('rate')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)

def read_text(text):
    engine.say(text)
    engine.runAndWait()
    
def stop_engine():
    engine.stop()