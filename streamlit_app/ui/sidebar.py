import streamlit as st
import pandas as pd
from core.config import get_personas, get_default_persona, get_default_temperature

def render():
    st.sidebar.header("⚙️ Settings")

    if not st.session_state.token:
        st.sidebar.info("Please log in.")
    else:
        st.sidebar.success("✅ Logged in")
        st.sidebar.button("Logout", on_click=logout)

        st.sidebar.subheader("📌 Navigation")
        st.session_state.page = st.sidebar.radio(
            "Go to", ["chat", "analytics"],
            index=0, format_func=lambda x: "💬 Chat" if x == "chat" else "📊 Analytics"
        )

        if st.session_state.page == "chat":
            # Persona + Temperature
            st.session_state.persona = st.sidebar.selectbox(
                "Choose Persona", get_personas(), index=get_personas().index(get_default_persona())
            )
            st.session_state.temperature = st.sidebar.slider(
                "Temperature", 0.0, 1.0, get_default_temperature(), 0.1
            )

            # -----------------------------
            # Chat History Downloads
            # -----------------------------
            st.sidebar.subheader("💬 Chat History")
            for persona, chats in st.session_state.histories.items():
                if chats:
                    st.sidebar.markdown(f"**{persona}** ({len(chats)//2} exchanges)")
                    st.sidebar.download_button(
                        label=f"⬇️ Download {persona}",
                        data=pd.Series(chats).to_json(indent=2),
                        file_name=f"{persona.lower()}_chat_history.json",
                        mime="application/json",
                        key=f"download_{persona}"
                    )

def logout():
    st.session_state.token = None
    st.session_state.histories = {p: [] for p in get_personas()}
    st.session_state.logout_triggered = True
