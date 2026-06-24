"""Main voice loop: listen → transcribe → think → speak → repeat."""

import threading
import time

from aria.listener import MicListener
from aria.speaker import Speaker
from aria.brain import run_brain


def main_loop(session_id: str = "default"):
    listener = MicListener(model_size="tiny")
    speaker = Speaker()
    speaker.speak("Aria is online. How can I help?")
    print("🟢 Aria online — press Ctrl+C to exit")

    while True:
        try:
            text = listener.listen()
            if not text:
                print("[main] no speech detected, retrying...")
                continue
            print("💭 Thinking...")
            response = run_brain(text, session_id=session_id)
            print("🗣️ ", response)
            speaker.speak(response)
        except KeyboardInterrupt:
            print("\n👋 Shutting down Aria.")
            speaker.speak("Goodbye.")
            break
        except Exception as e:
            print(f"[main error] {e}")
            time.sleep(1)


if __name__ == "__main__":
    main_loop()
