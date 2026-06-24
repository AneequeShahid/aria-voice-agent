# aria-voice-agent

**An always-on personal AI voice automation agent.**
You speak to it, it understands your intent, executes real tasks (web search, file ops, answer questions), and speaks back. Built on pipecat-ai/pipecat and livekit/agents architecture patterns. Fully free, runs locally on Windows.

## Tech stack

- STT: OpenAI Whisper (local, free) — faster-whisper (tiny model)
- TTS: pyttsx3 (offline, free, Windows native)
- LLM: Groq API (llama3-8b-8192, free)
- Agent: LangGraph (tool-calling, memory)
- Web search: Tavily (free tier)
- Memory: ChromaDB (local persistent)
- Backend: FastAPI
- UI: Streamlit

## Architecture

```
User voice → [microphone]
               ↓
          faster-whisper (STT)
               ↓
        LangGraph / Groq (brain)
          ↙              ↘
    tavily search    local files ✅
               ↓
         ChromaDB (memory)
               ↓
          pyttsx3 (TTS → speakers)
               ↓
        Streamlit UI (text mode)
```

## Install

```bash
git clone https://github.com/AneequeShahid/aria-voice-agent.git
cd aria-voice-agent
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# edit .env with your free keys
```

Get keys:
- Groq (free): https://console.groq.com
- Tavily (free): https://tavily.com

## Run

```bash
# voice loop (mic + speaker)
python main.py

# streamlit UI (text mode)
streamlit run ui/app.py

# fastapi server
uvicorn api.app:app --host 0.0.0.0 --port 8000
```

## Phase roadmap

- Phase 1 (done):
  - Mic → whisper transcription
  - pyttsx3 voice output
  - Groq + LangGraph brain
  - Tavily web search
  - ChromaDB conversation memory
  - Streamlit chat UI
  - FastAPI `/chat` endpoint
- Phase 2:
  - Telegram bot integration
  - Voice messages over Telegram
- Phase 3:
  - Wake-word detection (always-on)
  - Multi-session support

## Demo

> ⚠️ Add screenshot / gif here after first successful run.
