import openai
import pyttsx3
import speech_recognition as sr
from gtts import gTTS
import pyaudio
from playsound import playsound



openai.api_key = "api-key"


engine = pyttsx3.init('dummy')


def transcribe_audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
        try:
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            print('Google Speech Recognition could not understand audio')
        except sr.RequestError as e:
            print(f'Could not request results from Google Speech Recognition service; {e}')

def generate_response(prompt):
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=4000,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text.strip()

def speak_text(text):
    engine.say(text)
    engine.runAndWait()
    playsound('sample.mp3')
    
    

def main():
    while True:
        print('Say "Hello" to start recording your question...')
        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            audio = recognizer.listen(source)
            try:
                transcription = recognizer.recognize_google(audio)
                if transcription.lower() == "hello":
                    filename = "input.wav"
                    print("Say your question...")
                    with sr.Microphone() as source:
                        recognizer = sr.Recognizer()
                        source.pause_threshold = 1
                        audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
                        with open(filename, "wb") as f:
                            f.write(audio.get_wav_data())
                    text = transcribe_audio_to_text(filename)
                    if text:
                        print(f"You said: {text}")
                        response = generate_response(text)
                        print(f"GPT-3 says: {response}")
                        tts = gTTS(text=response, lang='en')
                        tts.save("sample.mp3")
                        speak_text(response)
            except Exception as e:
                print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
