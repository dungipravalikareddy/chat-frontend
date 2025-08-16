import streamlit as st
import requests
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

        except requests.exceptions.HTTPError as http_err:
            if http_err.response.status_code == 401:
                st.error("❌ Invalid username or password. Please try again.")
            elif http_err.response.status_code == 403:
                st.error("🚫 Access forbidden. Contact admin.")
            elif http_err.response.status_code == 500:
                st.error("⚠️ Server error. Please try again later.")
            else:
                st.error(f"⚠️ Unexpected error: {http_err.response.status_code}")

        except requests.exceptions.ConnectionError:
            st.error("🌐 Could not connect to the backend. Check if the server is running.")

        except Exception as e:
            st.error(f"⚠️ Something went wrong: {e}")
