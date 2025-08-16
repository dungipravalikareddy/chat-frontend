import streamlit as st
from core import state
from ui import sidebar, auth, chat_page, analytics_page

# --------------------
# Init state
# --------------------
state.init_state()

# --------------------
# Sidebar
# --------------------
sidebar.render()

# --------------------
# Routing
# --------------------
if not st.session_state.token:
    auth.render_login()
else:
    if st.session_state.page == "chat":
        chat_page.render()
    elif st.session_state.page == "analytics":
        analytics_page.render()

# --------------------
# Handle logout
# --------------------
if st.session_state.logout_triggered:
    st.session_state.logout_triggered = False
    st.info("Logged out")
    st.rerun()
