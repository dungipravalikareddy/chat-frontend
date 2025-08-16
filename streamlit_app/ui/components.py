import streamlit as st

def chat_bubble(msg):
    if msg["role"] == "user":
        st.markdown(
            f"<div style='text-align:right; background:#DCF8C6; padding:8px; border-radius:10px; margin:4px;'>{msg['content']}</div>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"<div style='text-align:left; background:#F1F0F0; padding:8px; border-radius:10px; margin:4px;'>{msg['content']}</div>",
            unsafe_allow_html=True
        )
