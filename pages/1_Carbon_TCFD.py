"""
Step 1: Emission & TCFD
"""
import streamlit as st
from shared.engine.carbon import render_calculator

st.set_page_config(
    page_title="Emission & TCFD",
    page_icon="🌱",
    layout="wide"
)

st.title("Step 1: Emission & TCFD")

st.divider()

# Sub-steps
st.subheader("Sub-steps")

tab1, tab2 = st.tabs(["1.1 Emission", "1.2 TCFD Tables"])

with tab1:
    # Embed emission calculator component
    # Compact mode: no title (page already has title), show region selection
    render_calculator(
        show_title=False,      # Don't show calculator title (page already has title)
        show_region=True,       # Show region selection
        compact_mode=True,      # Compact mode for better fit in tab
        default_region="TW"     # Default region
    )
    
    # Show calculation summary if available
    if st.session_state.get("carbon_calc_done") and st.session_state.get("carbon_emission"):
        st.divider()
        st.success("✅ Emission calculation completed! Results are saved and can be used in subsequent steps.")

with tab2:
    st.write("**TCFD Climate Risk Tables**")
    
    if st.button("Generate TCFD Tables", type="primary", use_container_width=True):
        st.success("✅ TCFD tables generated")

st.divider()

# Navigation
col1, col2 = st.columns(2)

with col1:
    if st.button("Previous", use_container_width=True):
        st.switch_page("pages/0_Home.py")

with col2:
    if st.button("Next", type="primary", use_container_width=True):
        st.switch_page("pages/2_Environment.py")
