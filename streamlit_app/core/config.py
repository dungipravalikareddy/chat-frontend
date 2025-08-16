import os
import streamlit as st

def get_api_base_url() -> str:
    return st.secrets.get("API_BASE_URL", os.getenv("API_BASE_URL", "http://127.0.0.1:8000"))

def get_personas() -> list[str]:
    raw = st.secrets.get("PERSONAS", os.getenv("PERSONAS", "Default,Tutor,Therapist"))
    return [p.strip() for p in raw.split(",")]

def get_default_persona() -> str:
    return st.secrets.get("DEFAULT_PERSONA", os.getenv("DEFAULT_PERSONA", "Default"))

def get_default_temperature() -> float:
    try:
        return float(st.secrets.get("DEFAULT_TEMPERATURE", os.getenv("DEFAULT_TEMPERATURE", 0.7)))
    except ValueError:
        return 0.7
