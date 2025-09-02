import pandas as pd
import streamlit as st
import plotly.express as px

def load_data():
    excel_file = "Dummy_Client_Analytics_Dataset.xlsx"
    clients = pd.read_excel(excel_file, sheet_name="Clients")
    projects = pd.read_excel(excel_file, sheet_name="Projects")
    tickets = pd.read_excel(excel_file, sheet_name="Tickets")
    resources = pd.read_excel(excel_file, sheet_name="Resources")
    return clients, projects, tickets, resources

# Load data
clients, projects, tickets, resources = load_data()

# Streamlit Dashboard
st.title("Client Analytics Dashboard")

st.subheader("Clients Table")
st.dataframe(clients)

st.subheader("Projects Table")
st.dataframe(projects)

st.subheader("Tickets Table")
st.dataframe(tickets)

st.subheader("Resources Table")
st.dataframe(resources)