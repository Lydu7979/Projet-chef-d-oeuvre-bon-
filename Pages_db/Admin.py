from Base_données.DB2sqlite import bdd_sql
import streamlit as st

def admin():
    st.write(bdd_sql())
    
