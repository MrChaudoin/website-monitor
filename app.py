import streamlit as st
from scraper import check_for_new_filings
import pandas as pd

st.set_page_config(page_title="Website Monitor", layout="wide")
st.title("🕵️ Senate Financial Disclosures Monitor")

if st.button("Check for Updates Now"):
    new_data = check_for_new_filings()
    if new_data:
        st.success(f"Found {len(new_data)} new filings!")
    else:
        st.info("No new filings found.")

# Load and show log data
try:
    df = pd.read_csv("data/log.csv")
    st.subheader("📋 Logged Filings")
    st.dataframe(df.sort_values(by='Filing Date', ascending=False), use_container_width=True)
except FileNotFoundError:
    st.warning("Log file not found. Run the checker at least once.")