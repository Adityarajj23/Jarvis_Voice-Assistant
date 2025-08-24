import speech_recognition as sr
import webbrowser
import pyttsx3
import google.generativeai as genai
from genai import ask_gemini
from app_manager import open_app, list_apps

recognizer = sr.Recognizer()

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


if __name__ == "__main__":
    speak("Hello, I am Jarvis. Say 'Jarvis' to wake me up.")
    while True:
        with sr.Microphone() as source:
            print("Listening for wake word...")
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=4)
            try:
                wake_command = recognizer.recognize_google(audio).lower()
                print(f"You said: {wake_command}")
                if wake_command == "jarvis":
                    speak("Yes, how can I help you?")
                    with sr.Microphone() as source2:
                        print("Listening for your command...")
                        audio2 = recognizer.listen(source2, timeout=10, phrase_time_limit=6)
                        try:
                            command = recognizer.recognize_google(audio2).lower()
                            print(f"Command: {command}")
                            # ---- Open website ----
                            if "open website" in command:
                                speak("Which website would you like to open?")
                                audio3 = recognizer.listen(source2, timeout=10, phrase_time_limit=6)
                                website = recognizer.recognize_google(audio3).lower()
                                webbrowser.open(f"https://www.{website}.com")
                                speak(f"Opening {website}")

                              # ---- Open app ----
                            elif "open app" in command:
                                speak("Which app should I open?")
                                audio3 = recognizer.listen(source2, timeout=10, phrase_time_limit=6)
                                app_name = recognizer.recognize_google(audio3).lower()
                                open_app(app_name, speak)

                            # ---- List saved apps ----
                            elif "list apps" in command:
                                apps = list_apps()
                                if apps:
                                    speak("Here are the apps I know: " + ", ".join(apps))
                                else:
                                    speak("I don't have any apps saved yet.")
                            # ---- Exit ----
                            elif "exit" in command or "quit" in command or "stop" in command:
                                speak("Goodbye!")
                                break

                            else:
                                # Use Gemini for general questions
                                answer = ask_gemini(command)
                                print(f"Gemini: {answer}")
                                speak(answer)

                        except sr.UnknownValueError:
                            speak("Sorry, I did not catch that.")
                        except sr.RequestError as e:
                            speak(f"Could not request results; {e}")
                else:
                    print("Wake word not detected.")
            except sr.UnknownValueError:
                print("Could not understand audio.")
            except sr.RequestError as e:
                print(f"Could not request results; {e}")
