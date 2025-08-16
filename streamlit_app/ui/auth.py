import streamlit as st
from core.api import BackendClient
from core.config import get_api_base_url, get_personas

client = BackendClient(get_api_base_url())
personas = get_personas()

def render_login():
    st.title("🔐 Login")
    username = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        try:
            data = client.login(username, password)
            st.session_state.token = data["access_token"]

            # preload histories
            for p in personas:
                st.session_state.histories[p] = client.get_history(p, st.session_state.token)

            st.success("✅ Logged in successfully!")
            st.rerun()
        except Exception as e:
            st.error(f"⚠️ Login failed: {e}")
