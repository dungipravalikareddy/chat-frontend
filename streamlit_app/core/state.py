import streamlit as st
from core.config import get_personas, get_default_persona, get_default_temperature

def init_state():
    if "token" not in st.session_state:
        st.session_state.token = None

    if "histories" not in st.session_state:
        st.session_state.histories = {p: [] for p in get_personas()}

    if "persona" not in st.session_state:
        st.session_state.persona = get_default_persona()

    if "temperature" not in st.session_state:
        st.session_state.temperature = get_default_temperature()

    if "logout_triggered" not in st.session_state:
        st.session_state.logout_triggered = False

    if "page" not in st.session_state:
        st.session_state.page = "chat"
