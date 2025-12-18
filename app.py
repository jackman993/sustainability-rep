"""
ESG Report Generation System - Minimal Version
"""
import streamlit as st

st.set_page_config(
    page_title="ESG Report System",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session_state
if "current_step" not in st.session_state:
    st.session_state.current_step = 0

# Initialize mode manager state
if "execution_mode" not in st.session_state:
    st.session_state.execution_mode = "mock"

# Redirect to home page
st.switch_page("pages/0_Home.py")
