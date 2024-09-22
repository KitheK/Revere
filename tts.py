from openai import OpenAI
from deep_translator import GoogleTranslator
import os
import time
import playsound
client = OpenAI(api_key="")
def speakText(command, voice):
    response = client.audio.speech.create(model="tts-1", voice=voice, input=command)
    response.write_to_file("output.mp3")
    time.sleep(1)
    playsound.playsound('output.mp3', True)
    
    os.remove("output.mp3")
    
def translateText(text, output_language):
    translated = GoogleTranslator(source='en', target=output_language).translate(text=text)
    return translated