import pandas as pd
import streamlit as st
import plotly.express as px

# -------------------- LOAD DATA --------------------
def load_data():
    excel_file = "Dummy_Client_Analytics_Dataset.xlsx"
    clients = pd.read_excel(excel_file, sheet_name="Clients")
    projects = pd.read_excel(excel_file, sheet_name="Projects")
    tickets = pd.read_excel(excel_file, sheet_name="Tickets")
    resources = pd.read_excel(excel_file, sheet_name="Resources")
    return clients, projects, tickets, resources

clients, projects, tickets, resources = load_data()

# -------------------- SIDEBAR NAVIGATION --------------------
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Analytics", "Tickets", "Resources"])

# -------------------- HOME PAGE --------------------
if page == "Home":
    st.title("🏠 Client Analytics Dashboard")

    st.subheader("Clients Table")
    st.dataframe(clients)

    st.subheader("Projects Table")
    st.dataframe(projects)

    st.subheader("Tickets Table")
    st.dataframe(tickets)

    st.subheader("Resources Table")
    st.dataframe(resources)


# -------------------- ANALYTICS PAGE --------------------
elif page == "Analytics":
    st.title("📊 Analytics Dashboard")

    # --- DATE FILTER ---
    st.sidebar.subheader("📅 Date Filter")

    if "created_at" in tickets.columns:
        min_date = pd.to_datetime(tickets["created_at"]).min()
        max_date = pd.to_datetime(tickets["created_at"]).max()

        start_date, end_date = st.sidebar.date_input(
            "Select Date Range:",
            value=[min_date, max_date],
            min_value=min_date,
            max_value=max_date
        )

        # Filter data based on selected range
        tickets_filtered = tickets[
            (pd.to_datetime(tickets["created_at"]) >= pd.Timestamp(start_date)) &
            (pd.to_datetime(tickets["created_at"]) <= pd.Timestamp(end_date))
        ]
    else:
        st.warning("⚠️ 'created_at' column not found in Tickets sheet.")
        tickets_filtered = tickets.copy()

    # --- ACTIVE PROJECTS BAR CHART ---
    if "client_id" in projects.columns:
        st.subheader("📁 Active Projects by Client")

        project_counts = projects["client_id"].value_counts().reset_index()
        project_counts.columns = ["Client ID", "Active Projects"]

        fig1 = px.bar(project_counts, x="Client ID", y="Active Projects",
                      color="Client ID", title="Active Projects by Client",
                      color_discrete_sequence=px.colors.sequential.Blues)
        st.plotly_chart(fig1)
    else:
        st.warning("⚠️ Missing 'client_id' column in Projects sheet.")

    # --- TICKETS RAISED VS RESOLVED LINE CHART ---
    if "created_at" in tickets_filtered.columns and "status" in tickets_filtered.columns:
        st.subheader("🎫 Tickets Raised vs Resolved Over Time")

        ticket_trends = tickets_filtered.groupby(
            [pd.to_datetime(tickets_filtered["created_at"]).dt.date, "status"]
        ).size().reset_index(name="Count")

        fig2 = px.line(ticket_trends, x="created_at", y="Count", color="status",
                       title="Tickets Raised vs Resolved",
                       markers=True)
        st.plotly_chart(fig2)
    else:
        st.warning("⚠️ Could not plot tickets trend. Check column names.")

    # --- SERVICE DEMAND PIE CHART ---
    st.subheader("📈 Service Demand by Industry")

    if "client_id" in projects.columns and "industry" in clients.columns:
        # Merge to get industry per project
        merged_data = projects.merge(clients[["client_id", "industry"]], on="client_id", how="left")

        industry_demand = merged_data["industry"].value_counts().reset_index()
        industry_demand.columns = ["Industry", "Project Count"]

        fig3 = px.pie(
            industry_demand,
            names="Industry",
            values="Project Count",
            title="Service Demand by Industry",
            hole=0.3,
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        st.plotly_chart(fig3)
    else:
        st.warning("⚠️ Missing 'client_id' or 'industry' column in data.")


# -------------------- TICKETS PAGE --------------------
elif page == "Tickets":
    st.title("🎫 Tickets Overview")
    st.dataframe(tickets)


# -------------------- RESOURCES PAGE --------------------
elif page == "Resources":
    st.title("👥 Resources Overview")
    st.dataframe(resources)



