import threading
import pyttsx3
import pythoncom
from audio_manager import SystemVolume


def speak(message, rate=165, voice_index=1):
    """
    Speak a message using text-to-speech.
    
    Args:
        message: Text to speak
        rate: Speech rate (default: 165)
        voice_index: Voice to use (0=male, 1=female if available)
    """
    def run():
        pythoncom.CoInitialize()
        volume = SystemVolume()

        try:
            volume.mute()   # 🔇 lower system sound

            engine = pyttsx3.init(driverName="sapi5")
            engine.setProperty("rate", rate)

            voices = engine.getProperty("voices")
            if len(voices) > voice_index:
                engine.setProperty("voice", voices[voice_index].id)

            engine.say(message)
            engine.runAndWait()
            engine.stop()

        except Exception as e:
            print("Voice error:", e)

        finally:
            volume.restore()   # 🔊 restore sound
            pythoncom.CoUninitialize()

    threading.Thread(target=run, daemon=True).start()


def speak_alert(focused_minutes, motivation):
    """
    Speak an alert message with focus time and motivation.
    
    Args:
        focused_minutes: Minutes user was focused
        motivation: Motivational message to speak
    """
    message = f"Alert! You were focused for {focused_minutes} minutes. {motivation}"
    speak(message, rate=150)


def speak_confirmation(intent):
    """Confirm the selected intent via voice."""
    message = f"Okay, monitoring {intent} mode. Stay focused!"
    speak(message, rate=160)