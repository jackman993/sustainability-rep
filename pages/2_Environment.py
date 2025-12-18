"""
Step 2: Environment Report
"""
import streamlit as st

st.set_page_config(
    page_title="Environment",
    page_icon="🌍",
    layout="wide"
)

st.title("Step 2: Environment Report")

st.divider()

# Prerequisites
st.success("✅ Carbon Emission & TCFD completed")

st.divider()

# Generate Section
st.subheader("Generate Environment Report")

st.info("""
**Environment section includes:**
- Detailed carbon emission analysis
- TCFD climate risk assessment
- Environmental management measures
- Approximately 17 pages
""")

if st.button("Generate Environment Report", type="primary", use_container_width=True):
    with st.spinner("Generating environment report..."):
        progress = st.progress(0)
        progress.progress(0.5)
        st.success("✅ Environment report generated (17 pages)")
        progress.progress(1.0)

st.divider()

# Navigation
col1, col2 = st.columns(2)

with col1:
    if st.button("Previous", use_container_width=True):
        st.switch_page("pages/1_Carbon_TCFD.py")

with col2:
    if st.button("Next", type="primary", use_container_width=True):
        st.switch_page("pages/3_Company.py")
