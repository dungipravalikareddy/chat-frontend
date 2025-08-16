import streamlit as st

def init_state():
    if "history" not in st.session_state:
        st.session_state.history = []
    if "persona" not in st.session_state:
        st.session_state.persona = "Default"
    if "used_persona" not in st.session_state:
        st.session_state.used_persona = None
    if "used_temperature" not in st.session_state:
        st.session_state.used_temperature = None

def append_user(msg: str):
    st.session_state.history.append({"role": "user", "content": msg})

def append_assistant(msg: str):
    st.session_state.history.append({"role": "assistant", "content": msg})
