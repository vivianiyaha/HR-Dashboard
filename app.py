import streamlit as st
import pandas as pd
import plotly.express as px

from auth import login_user, create_user
from database import create_tables, c, conn
import models

create_tables()

st.set_page_config(layout="wide")

# ------------------------
# SESSION STATE
# ------------------------
if "user" not in st.session_state:
    st.session_state.user = None

# ------------------------
# AUTH PAGE
# ------------------------
if not st.session_state.user:

    st.title("🔐 HR AI Suite Login")

    menu = ["Login", "Sign Up"]
    choice = st.selectbox("Menu", menu)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if choice == "Login":
        if st.button("Login"):
            user = login_user(username, password)
            if user:
                st.session_state.user = username
                st.success("Logged in")
            else:
                st.error("Invalid login")

    else:
        if st.button("Create Account"):
            create_user(username, password)
            st.success("Account created")

# ------------------------
# MAIN APP
# ------------------------
else:
    st.sidebar.write(f"👤 {st.session_state.user}")

    page = st.sidebar.radio("Menu", ["Dashboard", "Predict", "Admin"])

    # ------------------------
    # PREDICTION PAGE
    # ------------------------
    if page == "Predict":

        st.title("Run All Models")

        if st.button("Run Prediction"):

            attrition = models.predict_attrition()
            performance = models.predict_performance()
            kpi = models.predict_kpi()
            decision = models.decision()

            # Risk Score
            risk_score = (attrition * 0.5) + ((1-performance) * 0.3) + ((1-kpi) * 0.2)

            # Save to DB
            c.execute("INSERT INTO predictions VALUES (?,?,?,?,?)",
                      (st.session_state.user, attrition, performance, kpi, decision))
            conn.commit()

            st.success("Prediction Saved")

            st.write({
                "Attrition": attrition,
                "Performance": performance,
                "KPI": kpi,
                "Decision": decision,
                "Risk Score": round(risk_score,2)
            })

    # ------------------------
    # DASHBOARD
    # ------------------------
    elif page == "Dashboard":

        st.title("📊 HR Analytics Dashboard")

        df = pd.read_sql("SELECT * FROM predictions", conn)

        if not df.empty:

            col1, col2 = st.columns(2)

            with col1:
                fig = px.histogram(df, x="attrition", title="Attrition Distribution")
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                fig2 = px.histogram(df, x="performance", title="Performance Distribution")
                st.plotly_chart(fig2, use_container_width=True)

        else:
            st.warning("No data yet")

    # ------------------------
    # ADMIN PANEL
    # ------------------------
    elif page == "Admin":

        st.title("👑 Admin Dashboard")

        users = pd.read_sql("SELECT * FROM users", conn)
        data = pd.read_sql("SELECT * FROM predictions", conn)

        st.subheader("Users")
        st.dataframe(users)

        st.subheader("Predictions")
        st.dataframe(data)
