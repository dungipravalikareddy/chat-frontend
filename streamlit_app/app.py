import streamlit as st
import json
import requests

from core.config import (
    get_api_base_url,
    get_personas,
    get_default_persona,
    get_default_temperature,
)
from core.api import BackendClient

# -----------------------------
# Config
# -----------------------------
API_BASE = get_api_base_url()
client = BackendClient(API_BASE)
personas = get_personas()
default_persona = get_default_persona()
default_temp = get_default_temperature()

# -----------------------------
# Session State
# -----------------------------
if "token" not in st.session_state:
    st.session_state.token = None

if "histories" not in st.session_state:
    st.session_state.histories = {p: [] for p in personas}

if "persona" not in st.session_state:
    st.session_state.persona = default_persona

if "temperature" not in st.session_state:
    st.session_state.temperature = default_temp

if "logout_triggered" not in st.session_state:
    st.session_state.logout_triggered = False

if "page" not in st.session_state:
    st.session_state.page = "chat"   # default page


# -----------------------------
# Auth
# -----------------------------
def login(username, password):
    try:
        data = client.login(username, password)
        st.session_state.token = data["access_token"]

        # fetch backend histories for all personas
        for p in personas:
            st.session_state.histories[p] = client.get_history(p, st.session_state.token)

        st.success("✅ Logged in successfully!")
        st.rerun()

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            st.error("❌ Invalid username or password. Please try again.")
        elif e.response.status_code == 404:
            st.error("⚠️ Login endpoint not found. Check your API base URL.")
        else:
            st.error(f"⚠️ Login failed with status {e.response.status_code}: {e.response.text}")

    except requests.exceptions.ConnectionError:
        st.error("🌐 Could not connect to backend. Is the server running?")

    except Exception as e:
        st.error(f"⚠️ Unexpected error: {e}")


def logout():
    st.session_state.token = None
    st.session_state.histories = {p: [] for p in personas}
    st.session_state.logout_triggered = True


# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.header("⚙️ Settings")

if not st.session_state.token:
    st.sidebar.subheader("🔐 Login")
    username = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        login(username, password)
else:
    st.sidebar.success("✅ Logged in")
    st.sidebar.button("Logout", on_click=logout)

    # Navigation
    st.sidebar.subheader("📌 Navigation")
    st.session_state.page = st.sidebar.radio(
        "Go to", ["chat", "analytics"], index=0, format_func=lambda x: "💬 Chat" if x == "chat" else "📊 Analytics"
    )

    if st.session_state.page == "chat":
        st.session_state.persona = st.sidebar.selectbox(
            "Choose Persona", personas, index=personas.index(default_persona)
        )
        st.session_state.temperature = st.sidebar.slider(
            "Temperature", 0.0, 1.0, default_temp, 0.1
        )

        # Show chat history summary + download
        st.sidebar.subheader("💬 Chat History")
        for persona in personas:
            chats = st.session_state.histories.get(persona, [])
            if chats:
                st.sidebar.markdown(f"**{persona}** ({len(chats)//2} exchanges)")
                st.sidebar.download_button(
                    label=f"⬇️ Download {persona}",
                    data=json.dumps(chats, indent=2),
                    file_name=f"{persona.lower()}_chat_history.json",
                    mime="application/json",
                    key=f"download_{persona}"
                )


# -----------------------------
# Main UI
# -----------------------------
if st.session_state.page == "chat":
    st.title("💬 AI Chatbot")

    if not st.session_state.token:
        st.warning("Please log in to start chatting.")
    else:
        current_history = st.session_state.histories[st.session_state.persona]

        # Render bubbles
        for msg in current_history:
            if msg["role"] == "user":
                st.markdown(
                    f"<div style='text-align:right; background:#DCF8C6; "
                    f"padding:8px; border-radius:10px; margin:4px;'>{msg['content']}</div>",
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"<div style='text-align:left; background:#F1F0F0; "
                    f"padding:8px; border-radius:10px; margin:4px;'>{msg['content']}</div>",
                    unsafe_allow_html=True
                )

        # Clear chat button
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

                # Append new messages locally
                current_history.append({"role": "user", "content": user_input})
                current_history.append({"role": "assistant", "content": data["reply"]})

                st.rerun()
            except Exception as e:
                st.error(f"⚠️ Chat error: {e}")


elif st.session_state.page == "analytics":
    st.title("📊 Analytics Dashboard")

    if not st.session_state.token:
        st.warning("Please log in to view analytics.")
    else:
        try:
            analytics = client.get_analytics(st.session_state.token)

            col1, col2 = st.columns(2)
            col1.metric("Total Chats", analytics["total_chats"])
            col2.metric("Most Used Persona", analytics["most_used_persona"] or "—")

            st.subheader("🔥 Top Prompts")
            if analytics["top_prompts"]:
                st.bar_chart(analytics["top_prompts"])
                st.json(analytics["top_prompts"])
            else:
                st.info("No top prompts available yet.")

        except Exception as e:
            st.error(f"⚠️ Failed to load analytics: {e}")


# -----------------------------
# Handle Logout
# -----------------------------
if st.session_state.logout_triggered:
    st.session_state.logout_triggered = False
    st.info("Logged out")
    st.rerun()
