# app.py — Beyond the Message (full merged version)

import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
import json
from datetime import datetime

# Load environment variables from .env
load_dotenv()

# Initialize OpenAI client with your API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Pick model (from .env or default to gpt-4.1)
MODEL = os.getenv("BTM_MODEL", "gpt-4.1")

# ---------------- Streamlit Setup ----------------
st.set_page_config(page_title="Beyond the Message", page_icon="✝️")
st.title("Beyond the Message — Biblical References (KJV)")

# ---------------- Helper Functions ----------------
def need_key():
    if not os.getenv("OPENAI_API_KEY"):
        st.warning("No OPENAI_API_KEY detected. Set it first in .env")
        st.stop()

def ai_bible_answer(prompt: str, week_meta: dict, mode: str = "brief") -> str:
    """Generate a biblical study answer using OpenAI chat completions."""
    need_key()

    system = (
        "You are a careful Bible study helper for a Christian men's study called 'Beyond the Message'. "
        "Always ground answers in King James Version (KJV) Scripture references (Book Chapter:Verse). "
        "Stay orthodox; avoid speculation. Prefer Holman Study Bible, Matthew Henry, Vine’s, Strong’s. "
        "If unsure, admit it and give the nearest biblical principle."
    )

    # Core formatting rules
    style_rules = [
        "Format:",
        "- Summary (2–4 sentences)",
        "- Key passages (bulleted, Book Chap:Verse — one-line insight)",
        "- Cross-references (TSK / Matthew Henry style)",
        "- Practical application (workplace)"
    ]

    # Extra depth if user requests "deeper"
    if mode == "deeper":
        style_rules += [
            "- Timeline thread (how related passages connect)",
            "- Word study (brief notes using Vine’s/Strong’s)",
            "- Reflection questions (2–3 for group or self-study)"
        ]

    user = (
        f"Week: {week_meta.get('tag','')}\n"
        f"Anchor Scripture: {week_meta.get('scripture','')}\n"
        f"Prompt: {prompt}\n"
        f"Apply style rules:\n{chr(10).join(style_rules)}"
    )

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content.strip()

# ---------------- Streamlit UI ----------------
q = st.text_input("Your question:")
col1, col2 = st.columns(2)
with col1:
    run = st.button("Get biblical references")
with col2:
    run_deeper = st.button("More (dig deeper)")

if (run or run_deeper) and q:
    with st.spinner("Searching Scripture…"):
        try:
            # Right now week_meta is simple — expand later if using week JSON files
            week_meta = {"tag": "general", "scripture": ""}
            mode = "deeper" if run_deeper else "brief"
            st.markdown(ai_bible_answer(q, week_meta, mode=mode))
        except Exception as e:
            st.error(f"API error: {e}")
            st.caption("If you see 401, check OPENAI_API_KEY in your .env file.")

