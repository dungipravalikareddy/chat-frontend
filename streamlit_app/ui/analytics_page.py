import streamlit as st
import pandas as pd
from core.api import BackendClient
from core.config import get_api_base_url

client = BackendClient(get_api_base_url())

def render():
    st.title("📊 Chat Analytics")

    if not st.session_state.token:
        st.warning("Please log in to view analytics.")
        return

    try:
        analytics = client.get_analytics(st.session_state.token)

        # Summary metrics
        col1, col2 = st.columns(2)
        col1.metric("Total Chats", analytics["total_chats"])
        col2.metric("Most Used Persona", analytics["most_used_persona"] or "—")

        # Top Prompts
        st.subheader("🔥 Top Prompts")
        if analytics["top_prompts"]:
            df = pd.DataFrame(analytics["top_prompts"], columns=["Prompt"])
            st.bar_chart(df["Prompt"].value_counts())
            st.dataframe(df)
        else:
            st.info("No top prompts available yet.")

    except Exception as e:
        st.error(f"⚠️ Failed to load analytics: {e}")
