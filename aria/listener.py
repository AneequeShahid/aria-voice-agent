"""Listener: record microphone audio and transcribe with faster-whisper."""

import os
import queue
import threading

import numpy as np
import sounddevice as sd
from faster_whisper import WhisperModel

LISTENING_STATUS = ""


class MicListener:
    def __init__(self, model_size: str = "tiny", sample_rate: int = 16000):
        self.sample_rate = sample_rate
        self.audio_queue: queue.Queue[np.ndarray] = queue.Queue()
        self._recording = False
        self.model = WhisperModel(model_size, device="cpu", compute_type="int8")

    def _audio_callback(self, indata, frames, time_info, status):
        if status:
            print(f"[audio warning] {status}")
        if self._recording:
            self.audio_queue.put(indata.copy())

    def listen(self, max_seconds: int = 30) -> str:
        """Record mic, auto-stop on silence, return transcript."""
        self._recording = True
        q = self.audio_queue
        chunks = []

        print("🎙️  Listening...")

        def stop_after_silence():
            silence_threshold = 0.02
            silence_frames = 0
            max_silence = int(2.0 * (self.sample_rate / 1024))

            while self._recording:
                try:
                    chunk = q.get(timeout=0.1)
                except queue.Empty:
                    continue
                chunks.append(chunk)
                rms = np.sqrt(np.mean(chunk ** 2))
                if rms < silence_threshold:
                    silence_frames += 1
                else:
                    silence_frames = 0
                if silence_frames >= max_silence and len(chunks) > 5:
                    self._recording = False

        stopper = threading.Thread(target=stop_after_silence, daemon=True)
        stopper.start()

        try:
            with sd.InputStream(
                samplerate=self.sample_rate,
                channels=1,
                dtype="float32",
                blocksize=1024,
                callback=self._audio_callback,
            ):
                while self._recording:
                    sd.sleep(100)
        except Exception as e:
            print(f"[mic error] {e}")
        finally:
            self._recording = False
            stopper.join(timeout=2)

        print("✅ Audio captured. Transcribing...")

        if not chunks:
            return ""

        audio = np.concatenate(chunks, axis=0).flatten().astype(np.float32)

        # Write temp file for whisper
        import tempfile, wave

        tmp_path = os.path.join(tempfile.gettempdir(), "aria_listen.wav")
        with wave.open(tmp_path, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(self.sample_rate)
            pcm = (audio * 32767).astype(np.int16)
            wf.writeframes(pcm.tobytes())

        try:
            segments, info = self.model.transcribe(
                tmp_path, beam_size=5, vad_filter=True
            )
            text = " ".join(seg.text.strip() for seg in segments).strip()
            print(f"[whisper] {text}")
            return text
        except Exception as e:
            print(f"[whisper error] {e}")
            return ""
        finally:
            try:
                os.remove(tmp_path)
            except OSError:
                pass


def listen_once(model_size: str = "tiny") -> str:
    listener = MicListener(model_size=model_size)
    return listener.listen()
