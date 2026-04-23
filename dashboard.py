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
            # Check if expected tables exist
            table_check = pd.read_sql_query(
                """
                SELECT name
                FROM sqlite_master
                WHERE type='table' AND name IN ('warnings', 'moderation_events')
                """,
                conn,
            )

            if table_check.empty:
                st.info("Database is initialized but no spam has been detected yet. Waiting for data...")
            else:
                warnings_df = pd.read_sql_query("SELECT * FROM warnings", conn)
                events_df = pd.read_sql_query(
                    """
                    SELECT created_at, user_id, chat_id, message_text,
                           base_score, profile_score, final_score, reasons, action_taken
                    FROM moderation_events
                    ORDER BY id DESC
                    """,
                    conn,
                )

                # Create layout columns
                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("📊 Warning Distribution")
                    if not warnings_df.empty:
                        # Convert ID to string to avoid formatting issues in charts
                        warnings_df["user_id_str"] = warnings_df["user_id"].astype(str)
                        st.bar_chart(warnings_df.set_index("user_id_str")["count"])
                    else:
                        st.write("No warnings recorded yet.")

                with col2:
                    st.subheader("📋 Top Spammers (Raw Data)")
                    if not warnings_df.empty:
                        st.dataframe(
                            warnings_df.sort_values(by="count", ascending=False),
                            use_container_width=True,
                        )
                    else:
                        st.write("No data available.")

                # Summary metric
                st.divider()
                total_events = warnings_df["count"].sum() if not warnings_df.empty else 0
                st.metric(label="Total Spam Messages Blocked", value=total_events)

                st.divider()
                st.subheader("🧪 Trigger Analysis")
                if events_df.empty:
                    st.write("No moderation events captured yet.")
                else:
                    metric1, metric2, metric3 = st.columns(3)
                    metric1.metric("Total Moderation Events", len(events_df))
                    metric2.metric("Average Final Score", round(events_df["final_score"].mean(), 2))
                    metric3.metric("Max Final Score", int(events_df["final_score"].max()))

                    action_counts = (
                        events_df.groupby("action_taken")
                        .size()
                        .reset_index(name="count")
                        .sort_values(by="count", ascending=False)
                    )
                    st.subheader("Action Breakdown")
                    st.bar_chart(action_counts.set_index("action_taken")["count"])

                    display_df = events_df.copy()
                    display_df["created_at"] = pd.to_datetime(
                        display_df["created_at"], errors="coerce"
                    ).dt.strftime("%Y-%m-%d %H:%M:%S")
                    display_df["message_text"] = display_df["message_text"].fillna("")
                    st.subheader("Event Log (What Triggered Warning/Delete)")
                    st.dataframe(
                        display_df[
                            [
                                "created_at",
                                "user_id",
                                "chat_id",
                                "message_text",
                                "base_score",
                                "profile_score",
                                "final_score",
                                "reasons",
                                "action_taken",
                            ]
                        ],
                        use_container_width=True,
                    )
        
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