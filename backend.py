import speech_recognition as sr
from openai import OpenAI
from deep_translator import GoogleTranslator
import os
import time
import playsound
import threading
import queue
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
openai_api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=openai_api_key)

# Global variables
audio_queue = queue.Queue()
translation_queue = queue.Queue()
summary_queue = queue.Queue()
current_language = 'en'
current_voice = 'alloy'

def speakText(command, voice):
    response = client.audio.speech.create(model="tts-1", voice=voice, input=command)
    response.write_to_file("output.mp3")
    playsound.playsound('output.mp3', True)
    os.remove("output.mp3")

def translateText(text, output_language):
    translated = GoogleTranslator(source='auto', target=output_language).translate(text=text)
    return translated

def getSpeech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.2)
        audio = r.listen(source, phrase_time_limit=7)
    try:
        text = r.recognize_google(audio)
        return text.lower()
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        return ""

def audioListener():
    while True:
        text = getSpeech()
        if text:
            audio_queue.put(text)

def translator():
    buffer = ""
    while True:
        if not audio_queue.empty():
            text = audio_queue.get()
            buffer += text + " "
            if len(buffer.split()) >= 20:
                translated = translateText(buffer, current_language)
                translation_queue.put(translated)
                buffer = ""

def summarizer():
    full_text = ""
    while True:
        time.sleep(60)  # Summarize every minute
        while not translation_queue.empty():
            full_text += translation_queue.get() + " "
        if full_text:
            summary = client.completions.create(
                model="text-davinci-002",
                prompt=f"Summarize the following text:\n{full_text}\n\nSummary:",
                max_tokens=100
            ).choices[0].text
            summary_queue.put(summary)
            full_text = ""

@app.route('/get_translation', methods=['GET'])
def get_translation():
    if not translation_queue.empty():
        return jsonify({"translation": translation_queue.get()})
    return jsonify({"translation": ""})

@app.route('/get_summary', methods=['GET'])
def get_summary():
    if not summary_queue.empty():
        return jsonify({"summary": summary_queue.get()})
    return jsonify({"summary": ""})

@app.route('/set_language', methods=['POST'])
def set_language():
    global current_language
    data = request.json
    current_language = data['language']
    return jsonify({"status": "success"})

@app.route('/set_voice', methods=['POST'])
def set_voice():
    global current_voice
    data = request.json
    current_voice = data['voice']
    return jsonify({"status": "success"})

@app.route('/speak_text', methods=['POST'])
def speak_text():
    data = request.json
    text = data['text']
    threading.Thread(target=speakText, args=(text, current_voice)).start()
    return jsonify({"status": "success"})

if __name__ == "__main__":
    threading.Thread(target=audioListener, daemon=True).start()
    threading.Thread(target=translator, daemon=True).start()
    threading.Thread(target=summarizer, daemon=True).start()
    app.run(port=5000)
