"""Streamlit chat UI — text input mode with conversation history."""

import os
import time

import streamlit as st
from dotenv import load_dotenv

from aria.brain import run_brain, build_agent

load_dotenv()

st.set_page_config(page_title="Aria Voice Agent", page_icon="🎙️", layout="centered")

st.title("🎙️ Aria Voice Agent")
st.caption("Personal AI assistant — text mode")


def get_session_id() -> str:
    return st.session_state.get("session_id", "streamlit")


if "session_id" not in st.session_state:
    st.session_state.session_id = f"streamlit-{int(time.time())}"
if "history" not in st.session_state:
    st.session_state.history: list[dict] = []

for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if user_input := st.chat_input("type your message to aria..."):
    st.session_state.history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            reply = run_brain(user_input, session_id=get_session_id())
        st.write(reply)

    st.session_state.history.append({"role": "assistant", "content": reply})

if st.button("Reset conversation"):
    st.session_state.history = []
    st.session_state.session_id = f"streamlit-{int(time.time())}"
    st.rerun()
