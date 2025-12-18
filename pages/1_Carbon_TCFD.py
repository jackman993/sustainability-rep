"""
Step 1: Carbon Emission & TCFD
"""
import streamlit as st

st.set_page_config(
    page_title="Carbon & TCFD",
    page_icon="🌱",
    layout="wide"
)

st.title("Step 1: Carbon Emission & TCFD")

st.divider()

# Sub-steps
st.subheader("Sub-steps")

tab1, tab2 = st.tabs(["1.1 Carbon Emission", "1.2 TCFD Tables"])

with tab1:
    st.write("**Carbon Emission Calculation**")
    
    # Industry
    industry = st.selectbox(
        "Industry",
        ["Manufacturing", "Technology", "Services", "Retail", "Finance", "Other"]
    )
    
    # Monthly Electricity
    monthly_electricity = st.number_input(
        "Monthly Electricity Cost (USD)",
        min_value=0,
        value=10000,
        step=1000
    )
    
    if st.button("Calculate Emissions", type="primary"):
        st.success("✅ Carbon emission calculated")

with tab2:
    st.write("**TCFD Climate Risk Tables**")
    
    if st.button("Generate TCFD Tables", type="primary"):
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
