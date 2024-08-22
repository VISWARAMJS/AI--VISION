import webbrowser
import pyttsx3 as x3
import speech_recognition as sr
import pywhatkit as play


def listen_for_speech():
    reco = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("Detecting")
        audio = reco.listen(source)
    try:
        recognized_speech = reco.recognize_google(audio)
        print("USER : ", recognized_speech)
        return recognized_speech.lower()
    except sr.UnknownValueError:
        print("I can't detect your sentence")
        return ""


engine = x3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def commands(command):
    if "hello" in command:
        x3.speak("Hello! How can I assist you?")
    elif "open" in command:
        if "google" in command:
            webbrowser.open("https://www.google.com")
            x3.speak("Opening Google")

    elif "what" in command:
        if "your name" in command:
            x3.speak("My name is VISION, which stands for Vigilant Intelligent Superior Indomitable Operating Network.")

    elif "play" in command:
        if "games" in command:
            webbrowser.open("https://www.poki.com")
        else:
            song = command.replace('play', '')
            play.playonyt(song)

    elif "goodbye" in command or "exit" in command or "bye" in command:
        x3.speak("Goodbye! Have a great day.")
        exit()
    else:
        x3.speak("I'm not sure how to respond to that.")


def VISION():
    while True:
        command = listen_for_speech()
        commands(command)


if __name__ == "__main__":
    VISION()
