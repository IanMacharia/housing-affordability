import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()
st.set_page_config(page_title="Housing Affordability Dashboard", layout="wide")
st.title("Housing Affordability Dashboard")
st.caption("Nairobi | Lagos | Johannesburg (prototype)")
st.write("Env:", os.getenv("ENV", "dev"))
