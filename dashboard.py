import streamlit as st
import sqlite3
import pandas as pd
import os

# Page configuration
st.set_page_config(page_title="🛡️ Spam Filter Analytics", layout="wide")
st.title("Spam Filter Analytics Dashboard")

# Define the path to your database
DB_PATH = "bot_data.db"

# Check if the database file exists
if not os.path.exists(DB_PATH):
    st.warning("Database file not found. Please start the Telegram bot first to initialize the system.")
else:
    try:
        # Use a context manager for the connection (better practice)
        with sqlite3.connect(DB_PATH) as conn:
            # Check if the 'warnings' table exists
            table_check = pd.read_sql_query(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='warnings'", conn
            )

            if table_check.empty:
                st.info("Database is initialized but no spam has been detected yet. Waiting for data...")
            else:
                # Load Data
                df = pd.read_sql_query("SELECT * FROM warnings", conn)

                # Create layout columns
                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("📊 Warning Distribution")
                    if not df.empty:
                        # Convert ID to string to avoid formatting issues in charts
                        df['user_id_str'] = df['user_id'].astype(str)
                        st.bar_chart(df.set_index("user_id_str")["count"])
                    else:
                        st.write("No warnings recorded yet.")

                with col2:
                    st.subheader("📋 Top Spammers (Raw Data)")
                    if not df.empty:
                        st.dataframe(df.sort_values(by="count", ascending=False), use_container_width=True)
                    else:
                        st.write("No data available.")

                # Summary metric
                st.divider()
                total_events = df['count'].sum() if not df.empty else 0
                st.metric(label="Total Spam Messages Blocked", value=total_events)
        
    except Exception as e:
        st.error(f"An error occurred while reading the database: {e}")

# --- Sidebar Logic (Fixed ternary operator issue) ---
st.sidebar.header("System Status")

if os.path.exists(DB_PATH):
    st.sidebar.success("Dashboard Connected")
else:
    st.sidebar.error("Database Offline")

st.sidebar.write("---")
st.sidebar.write("This dashboard monitors real-time moderation actions taken by the Telegram Spam Filter Bot.")
st.sidebar.info("Tip: If the bot is running but you see no data, trigger a spam detection in your group to populate the database.")