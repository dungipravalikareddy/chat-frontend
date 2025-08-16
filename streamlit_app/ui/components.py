import streamlit as st
from typing import List, Dict

def chat_window(history: List[Dict[str, str]]):
    for m in history:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])
