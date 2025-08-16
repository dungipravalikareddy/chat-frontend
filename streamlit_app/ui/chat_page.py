import streamlit as st
from core.api import BackendClient
from core.config import get_api_base_url
from ui.components import chat_bubble

client = BackendClient(get_api_base_url())

def render():
    st.title("💬 Chatbot")

    current_history = st.session_state.histories[st.session_state.persona]

    # Render bubbles
    for msg in current_history:
        chat_bubble(msg)

    # Clear chat
    if st.button("🗑️ Clear Chat"):
        client.clear_history(st.session_state.persona, st.session_state.token)
        st.session_state.histories[st.session_state.persona] = []
        st.rerun()

    # Chat input
    user_input = st.chat_input("Type your message...")
    if user_input:
        try:
            data = client.chat(
                user_input,
                st.session_state.persona,
                current_history,
                st.session_state.temperature,
                st.session_state.token,
            )
            current_history.append({"role": "user", "content": user_input})
            current_history.append({"role": "assistant", "content": data["reply"]})
            st.rerun()
        except Exception as e:
            st.error(f"⚠️ Chat error: {e}")
