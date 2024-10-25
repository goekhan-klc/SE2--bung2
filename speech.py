import speech_recognition as sr
import pyttsx3
import requests
from bs4 import BeautifulSoup

r = sr.Recognizer()
engine = pyttsx3.init()

def response():
    # create a recognizer object
    response = requests.get("https://wetter.com")


    # use the default microphone as the audio source
    with sr.Microphone() as source:
        audio = r.listen(source)
        print("Listening...")

    try:
        text = r.recognize_google(audio)
        print("Du sagtest " + text)

        #Hallo
        if "hello" in text:
            engine.say("Hallo! Wie geht es dir!")
            engine.runAndWait()
            main()
            return

        #Wetter
        if "weather" in text:
            api_url = "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current=temperature_2m,windspeed_10m&hourly=temperature_2m,relativehumidity_2m,windspeed_10m"

            response = requests.get(api_url)

            if response.status_code == 200:
                data = response.json()
                current_temperature = data['current']['temperature_2m']
                
                engine.say("Die aktuelle Temperatur ist " + str(current_temperature) + " Grad Celsius")
                engine.runAndWait()
                main()
                return
            else:
                print("Failed to retrieve data from the API.")
                main()
        
        #Other
        else:
            engine.say("Ich habe dich nicht verstanden")
            engine.runAndWait()
            main()

        main()
    except sr.UnknownValueError:
        print("Google Speech Recognition konnte dich nicht verstehen")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))


def main():

    print("Sage etwas")
    # use the default microphone as the audio source
    with sr.Microphone() as source:
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        print("Du sagtest " + text)

        if "hey" in text:
            engine.say("Ja bitte?")
            engine.runAndWait()
            response()
        else:
            engine.say("Ich habe dich nicht verstanden")
            engine.runAndWait()
            main()

    except sr.UnknownValueError:
        print("Google Speech Recognition konnte dich nicht verstehen")
        main()
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        main()


if __name__ == "__main__":
    main()