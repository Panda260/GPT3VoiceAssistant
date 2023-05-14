import os
import openai
import pyttsx3
import speech_recognition as sr
import time

from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(
        index, name))

# initialize the text-to-speech engine
engine = pyttsx3.init()


def transcribe_audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio, language='de-DE')
    except:
        print("Error: Could not recognize audio")


def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response['choices'][0]['text']


def speak_text(text):
    engine.say(text)
    engine.runAndWait()


def main():
    while True:
        # wait for user to say PC
        print("Listening... Say PC")
        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            audio = recognizer.listen(source)
            try:
                transcription = recognizer.recognize_google(
                    audio, language='de-DE')
                if transcription.lower() == "pc":
                    filename = "input.wav"
                    print("Sag deine Frage...")
                    with sr.Microphone() as source:
                        recognizer = sr.Recognizer()
                        source.pause_threshold = 1
                        audio = recognizer.listen(
                            source, phrase_time_limit=None, timeout=None)
                        with open(filename, "wb") as f:
                            f.write(audio.get_wav_data())

                    # transcribe audio to text
                    text = transcribe_audio_to_text(filename)
                    if text:
                        print("Du hast gesagt: ", text)

                        # generate response using GPT-3
                        response = generate_response(text)
                        print("AI: ", response)

                        # Read response using text-to-speech
                        speak_text(response)
            except Exception as e:
                print(e)


if __name__ == "__main__":
    main()
