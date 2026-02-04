import threading
import pyttsx3
import pythoncom
from audio_manager import SystemVolume

def speak(message):
    def run():
        pythoncom.CoInitialize()
        volume = SystemVolume()

        try:
            volume.mute()   # 🔇 lower system sound

            engine = pyttsx3.init(driverName="sapi5")
            engine.setProperty("rate", 165)

            voices = engine.getProperty("voices")
            if len(voices) > 1:
                engine.setProperty("voice", voices[1].id)

            engine.say(message)
            engine.runAndWait()
            engine.stop()

        except Exception as e:
            print("Voice error:", e)

        finally:
            volume.restore()   # 🔊 restore sound
            pythoncom.CoUninitialize()

    threading.Thread(target=run, daemon=True).start()