import pyttsx3
import threading
import queue
import time

_engine = None
_queue = queue.Queue()
_worker_started = False


def _tts_worker():
    global _engine
    # Initialize COM on this thread for SAPI5 (helps pyttsx3 on Windows)
    try:
        import comtypes
        try:
            comtypes.CoInitialize()
        except Exception:
            pass
    except Exception:
        # comtypes may not be available; continue without explicit COM init
        pass
    try:
        _engine = pyttsx3.init("sapi5")
        _engine.setProperty("rate", 150)
        _engine.setProperty("volume", 1.0)
        voices = _engine.getProperty("voices")
        if voices:
            _engine.setProperty("voice", voices[0].id)
    except Exception as e:
        print(f"TTS init error: {e}")
        _engine = None
    print("TTS worker started")

    while True:
        try:
            text = _queue.get()
            if text is None:
                break
            print(f"TTS worker got text: {text}")
            if _engine is None:
                # try to reinitialize if engine was not available earlier
                try:
                    _engine = pyttsx3.init("sapi5")
                except Exception as e:
                    print(f"TTS reinit error: {e}")
                    continue

            try:
                _engine.say(text)
                _engine.runAndWait()
            except Exception as e:
                print(f"TTS speak error: {e}")
            finally:
                # small pause to avoid overlapping calls
                time.sleep(0.25)
        finally:
            _queue.task_done()
    # Uninitialize COM if possible
    try:
        import comtypes
        try:
            comtypes.CoUninitialize()
        except Exception:
            pass
    except Exception:
        pass
    print("TTS worker exiting")


def _ensure_worker():
    global _worker_started
    if not _worker_started:
        t = threading.Thread(target=_tts_worker, daemon=True)
        t.start()
        _worker_started = True


def speak(text):
    """Enqueue text to be spoken by the background TTS worker."""
    _ensure_worker()
    try:
        _queue.put(text)
    except Exception as e:
        print(f"speak enqueue error: {e}")


def speak_distraction_alert(focused_minutes, motivation_message):
    """Speaks the complete distraction alert message."""
    alert_text = f"You are distracted. You have focused for {focused_minutes} minutes. {motivation_message}"
    speak(alert_text)