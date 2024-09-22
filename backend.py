from flask import Flask, request, jsonify
import speech_recognition as sr
import openai
from deep_translator import GoogleTranslator
import os
import time
import pygame
from gtts import gTTS

app = Flask(__name__)

# Initialize the recognizer
r = sr.Recognizer()

# OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Global variables
current_language = 'en'
tts_enabled = False
current_voice = 'alloy'
live_text = ''
summary_text = ''
keywords = []

def get_speech():
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0.2)
            print("Listening now")
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            text = r.recognize_google(audio)
            return text.lower()
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
    except sr.UnknownValueError:
        print("Unknown error occurred")
    return ""

def translate_text(text, target_language):
    translator = GoogleTranslator(source='auto', target=target_language)
    return translator.translate(text)

def generate_summary(text):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Summarize the following text:\n\n{text}",
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text.strip()

def extract_keywords(text):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Extract important keywords from the following text:\n\n{text}",
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text.strip().split(", ")

def speak_text(text, language):
    if tts_enabled:
        tts = gTTS(text=text, lang=language)
        tts.save("output.mp3")
        pygame.mixer.init()
        pygame.mixer.music.load("output.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        os.remove("output.mp3")

@app.route('/change_voice', methods=['POST'])
def change_voice():
    global current_voice
    current_voice = request.json['voice']
    return jsonify({"status": "success"})

@app.route('/change_language', methods=['POST'])
def change_language():
    global current_language
    current_language = request.json['language']
    return jsonify({"status": "success"})

@app.route('/toggle_tts', methods=['POST'])
def toggle_tts():
    global tts_enabled
    tts_enabled = request.json['enabled']
    return jsonify({"status": "success"})

@app.route('/get_live_text', methods=['GET'])
def get_live_text():
    global live_text, keywords
    new_text = get_speech()
    if new_text:
        live_text += f" {new_text}"
        translated_text = translate_text(new_text, current_language)
        keywords.extend(extract_keywords(translated_text))
        speak_text(translated_text, current_language)
    return jsonify({"text": translate_text(live_text, current_language), "keywords": keywords})

@app.route('/get_summary', methods=['GET'])
def get_summary():
    global summary_text, keywords
    summary = generate_summary(live_text)
    summary_text += f" {summary}"
    translated_summary = translate_text(summary, current_language)
    summary_keywords = extract_keywords(translated_summary)
    keywords.extend(summary_keywords)
    speak_text(translated_summary, current_language)
    return jsonify({"text": translated_summary, "keywords": summary_keywords})

@app.route('/get_definition', methods=['GET'])
def get_definition():
    keyword = request.args.get('keyword')
    language = request.args.get('language')
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Provide a brief definition for the word or phrase '{keyword}' in {language} and include a hyperlink to more info:",
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.5,
    )
    definition = response.choices[0].text.strip()
    translated_definition = translate_text(definition, language)
    return jsonify({"definition": translated_definition})

if __name__ == '__main__':
    app.run(debug=True)