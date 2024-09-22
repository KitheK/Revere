import speech_recognition as sr
# Initialize the recognizer
r = sr.Recognizer()
def getSpeech():
    try:
        with sr.Microphone() as source2:
            r.adjust_for_ambient_noise(source2, duration=0.2)
            
            print("Listening now")
            audio = r.listen(source2)
            MyText = r.recognize_google(audio)
            MyText = MyText.lower()
            return MyText
    
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
    
    except sr.UnknownValueError:
        print("unknown error occured")