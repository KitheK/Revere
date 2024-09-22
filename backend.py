import speech_recognition as sr
from openai import OpenAI
from deep_translator import GoogleTranslator
import os
import time
import playsound
import threading


client = OpenAI(api_key="") # Replace with your OpenAI API key

# Initialize the recognizer
r = sr.Recognizer()

# Global variables for text and language
liveText = ""
summaryText = ""
current_language = "en"

# Define voices for text-to-speech
voices = {
    "alloy": "alloy",
    "echo": "echo",
    "shimmer": "shimmer",
    "onyx": "onyx",
}

def getSpeech():
  """Listens to audio input and returns recognized text."""
  try:
    with sr.Microphone() as source2:
      r.adjust_for_ambient_noise(source2, duration=0.2)
      print("Listening now")
      audio = r.listen(source2)
      MyText = r.recognize_google(audio, language=current_language)
      MyText = MyText.lower()
      return MyText
  except sr.RequestError as e:
    print("Could not request results; {0}".format(e))
  except sr.UnknownValueError:
    print("unknown error occured")
  return ""

def speakText(command, voice):
  """Converts text to speech using OpenAI's TTS API."""
  response = client.audio.speech.create(model="tts-1", voice=voice, input=command)
  response.write_to_file("output.mp3")
  time.sleep(1)
  playsound.playsound('output.mp3', True)
  os.remove("output.mp3")

def translateText(text, output_language):
  """Translates text using Google Translate."""
  translated = GoogleTranslator(source='en', target=output_language).translate(text=text)
  return translated

def updateLiveText():
  """Updates the live translation text with recognized speech."""
  global liveText
  recognized_text = getSpeech()
  if recognized_text:
    liveText += recognized_text + " "
    liveTextElement = document.getElementById('liveText')
    liveTextElement.innerHTML = liveText
    # Check if text reached bottom and shift page if necessary
    if liveTextElement.scrollHeight > liveTextElement.clientHeight:
      window.scrollBy(0, 20)

def updateSummaryText():
  """Updates the summary text with the translated live text."""
  global summaryText
  if liveText:
    translated_summary = translateText(liveText, current_language)
    summaryText += translated_summary + " "
    summaryTextElement = document.getElementById('summaryText')
    summaryTextElement.innerHTML = summaryText
    # Scroll to bottom of summary
    summaryTextElement.scrollTop = summaryTextElement.scrollHeight
    liveText = ""

def startSpeechRecognition():
  """Starts a separate thread for continuous speech recognition."""
  threading.Thread(target=updateLiveText).start()

def changeLanguage():
  """Handles language selection and updates the translation and TTS."""
  global current_language
  current_language = document.getElementById('languageSelect').value
  print(f"Language changed to: {current_language}")

def changeVoice():
  """Handles voice selection for text-to-speech."""
  selectedVoice = document.getElementById('voiceSelect').value
  print(f"Voice changed to: {selectedVoice}")

def toggleTTS():
  """Toggles text-to-speech functionality."""
  ttsEnabled = document.getElementById('ttsToggle').checked
  print(f"Text-to-Speech {ttsEnabled ? 'enabled' : 'disabled'}")

def toggleDarkMode():
  """Toggles dark mode."""
  document.body.classList.toggle('dark-mode')

def showDefinition(keyword):
  """Displays a definition popup for a keyword."""
  # Implement definition logic here based on your keyword database
  document.getElementById('definitionText').textContent = f"Definition of {keyword}: ... "
  document.getElementById('definitionPopup').style.display = 'block'

def closeDefinition():
  """Closes the definition popup."""
  document.getElementById('definitionPopup').style.display = 'none'

# Start speech recognition when the page loads
startSpeechRecognition()

# Update summary every minute
setInterval(updateSummaryText, 60000) 

# Initialize dark mode
document.body.classList.add('dark-mode')