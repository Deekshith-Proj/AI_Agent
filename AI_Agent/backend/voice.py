import whisper
import sounddevice as sd
import numpy as np
import tempfile

model = whisper.load_model("base")

def record_and_transcribe(duration=5):
    print("Recording...")
    audio = sd.rec(int(duration*16000), samplerate=16000, channels=1, dtype=np.float32)
    sd.wait()

    # Save to temp WAV
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        np.save(tmp.name, audio)

    result = model.transcribe(tmp.name)
    return result["text"]