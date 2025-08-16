import os
import streamlit as st

def get_api_base_url() -> str:
    return st.secrets.get("BACKEND_URL", os.getenv("BACKEND_URL", "http://127.0.0.1:8000"))

def get_personas() -> list[str]:
    # Persona names must match backend keys
    return ["Default", "Tutor", "Therapist"]

def get_default_persona() -> str:
    return "Default"

def get_default_temperature() -> float:
    try:
        return float(st.secrets.get("DEFAULT_TEMPERATURE", os.getenv("DEFAULT_TEMPERATURE", 0.7)))
    except ValueError:
        return 0.7
