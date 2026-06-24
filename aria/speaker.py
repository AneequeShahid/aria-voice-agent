"""Speaker: convert text to speech using pyttsx3."""

import threading

import pyttsx3


class Speaker:
    def __init__(self):
        self._lock = threading.Lock()
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 170)
        self.engine.setProperty("volume", 1.0)
        voices = self.engine.getProperty("voices")
        for v in voices:
            if "zira" in v.name.lower() or "female" in v.name.lower():
                self.engine.setProperty("voice", v.id)
                break

    def speak(self, text: str):
        if not text:
            return
        print(f"🔊 Speaking: {text}")

        def _run():
            with self._lock:
                try:
                    self.engine.say(text)
                    self.engine.runAndWait()
                except Exception as e:
                    print(f"[tts error] {e}")

        t = threading.Thread(target=_run, daemon=True)
        t.start()
        t.join(timeout=60)
        if t.is_alive():
            print("[tts warning] speech timed out, killing thread")
