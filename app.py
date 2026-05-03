import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

from matching.scoring import compute_simple_score
from matching.priority import build_compatibility_matrix

st.set_page_config(page_title="WCB Experiment Revision 1", layout="wide")

# -----------------------------
# 1. LOAD DATA
# -----------------------------
adopters_df = pd.read_excel("data/WCB Adopters April 2026.xlsx")
dogs_df = pd.read_excel("data/wcb dogs.xlsx")
dogs_df["Age"] = pd.to_numeric(dogs_df["Age"], errors="coerce")

adopters_df["App Submitted Date"] = pd.to_datetime(
    adopters_df["App Submitted Date"], errors="coerce"
)

# -----------------------------
# 2. CLEANING FUNCTIONS
# -----------------------------
def clean_yes_no(value):
    if pd.isna(value):
        return "Unknown"
    v = str(value).strip().lower()
    if v in ["yes", "y", "ok", "good"]:
        return "Yes"
    if v in ["no", "n"]:
        return "No"
    if "older" in v:
        return "Older/Respectful"
    if "slow" in v or "selective" in v:
        return "Selective"
    return value

def clean_status(value):
    if pd.isna(value):
        return "Unknown"
    v = str(value).lower()
    if "available" in v:
        return "Available"
    if "medical" in v:
        return "On Hold – Medical"
    if "behavior" in v:
        return "On Hold – Behavior"
    if "training" in v:
        return "In Training"
    if "no longer" in v:
        return "Not Being Surrendered"
    return value

def parse_date(value):
    try:
        return pd.to_datetime(value, errors="coerce")
    except:
        return None

# Apply cleaning
dogs_df["Status"] = dogs_df["Status"].apply(clean_status)
dogs_df["Good with Cats"] = dogs_df["Good with Cats"].apply(clean_yes_no)
dogs_df["Good with Dogs"] = dogs_df["Good with Dogs"].apply(clean_yes_no)
dogs_df["Good with Kids"] = dogs_df["Good with Kids"].apply(clean_yes_no)
dogs_df["Intake Date"] = dogs_df["Intake Date"].apply(parse_date)

# Create DogID
dogs_df["DogID"] = dogs_df.index + 1

# Days in care
dogs_df["Days in Care"] = (datetime.now() - dogs_df["Intake Date"]).dt.days

def matchmaking_dashboard(adopters_df, dogs_df):
    st.title("Matchmaking Dashboard")

    st.markdown("""
    This dashboard automatically matches adopters to dogs using a simple rule-based 
    compatibility score, then ranks adopters for each dog by oldest application date 
    to determine FIL (First in Line), NIL (Next in Line), and TIL (Third in Line).
    """)

    min_score = st.slider("Minimum compatibility score", 0, 100, 60, 5)

    compat_df = build_compatibility_matrix(adopters_df, dogs_df)

    st.subheader("Compatibility Matrix")
    st.dataframe(compat_df, use_container_width=True)

    priority_df = build_priority_table(compat_df, min_score=min_score)

    st.subheader("FIL / NIL / TIL Rankings")
    st.dataframe(priority_df, use_container_width=True)


# -----------------------------
# 3. SIDEBAR NAVIGATION
# -----------------------------
st.sidebar.title("WCB Experiment Revision 1")
page = st.sidebar.radio(
    "Navigate",
    [
        "Dashboard Overview",
        "Dog Directory",
        "Dog Profiles",
        "Analytics",
        "Matchmaking Dashboard"
    ]
)


# -----------------------------
# -----------------------------
# 4. DASHBOARD OVERVIEW
# -----------------------------
if page == "Dashboard Overview":
    st.title("📊 WCB Experiment Revision 1 — Overview")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Dogs", len(dogs_df))
    col2.metric("Available", sum(dogs_df["Status"] == "Available"))
    col3.metric("On Hold – Medical", sum(dogs_df["Status"] == "On Hold – Medical"))
    col4.metric("On Hold – Behavior", sum(dogs_df["Status"] == "On Hold – Behavior"))

    st.subheader("Dogs by Status")
    st.bar_chart(dogs_df["Status"].value_counts())

    st.subheader("Dogs by Age")
    st.bar_chart(dogs_df["Age"].value_counts())


    st.subheader("Days in Care Distribution")
    st.line_chart(dogs_df["Days in Care"])



# -----------------------------

# 5. DOG DIRECTORY
# -----------------------------
elif page == "Dog Directory":
    st.title("🐶 Dog Directory")

    status_filter = st.multiselect(
        "Filter by Status",
        options=dogs_df["Status"].unique(),
        default=dogs_df["Status"].unique()
    )

    filtered = dogs_df[dogs_df["Status"].isin(status_filter)]

    for _, row in filtered.iterrows():
        with st.expander(f"{row['Name']} — {row['Status']}"):
            st.write(f"**Age:** {row['Age']}")
            st.write(f"**Weight:** {row['Weight']}")
            st.write(f"**Breed:** {row['Breed']}")
            st.write(f"**Good with Dogs:** {row['Good with Dogs']}")
            st.write(f"**Good with Kids:** {row['Good with Kids']}")
            st.write(f"**Good with Cats:** {row['Good with Cats']}")
            st.write(f"**Days in Care:** {row['Days in Care']}")
            st.write(f"**Notes:** {row['Jansen/Angela/Foster Comments']}")
# -----------------------------
# 6. DOG PROFILES

elif page == "Dog Profiles":
    st.title("📘 Dog Profiles")

    dog_names = dogs_df["Name"].unique()
    selected = st.selectbox("Select a Dog", dog_names)

    d = dogs_df[dogs_df["Name"] == selected].iloc[0]

    st.header(d["Name"])
    st.write(f"**Status:** {d['Status']}")
    st.write(f"**Age:** {d['Age']}")
    st.write(f"**Weight:** {d['Weight']}")
    st.write(f"**Breed:** {d['Breed']}")
    st.write(f"**Sex:** {d['Sex']}")
    st.write(f"**Good with Dogs:** {d['Good with Dogs']}")
    st.write(f"**Good with Kids:** {d['Good with Kids']}")
    st.write(f"**Good with Cats:** {d['Good with Cats']}")
    st.write(f"**Days in Care:** {d['Days in Care']}")
    st.write("### Notes")
    st.write(d["Jansen/Angela/Foster Comments"])


# -----------------------------
# 7. ANALYTICS
# -----------------------------
elif page == "Analytics":
    st.title("📈 Analytics & Insights")

    st.subheader("Good with Kids")
    st.bar_chart(dogs_df["Good with Kids"].value_counts())

    st.subheader("Good with Dogs")
    st.bar_chart(dogs_df["Good with Dogs"].value_counts())

    st.subheader("Good with Cats")
    st.bar_chart(dogs_df["Good with Cats"].value_counts())

    st.subheader("Status Breakdown")
    st.bar_chart(dogs_df["Status"].value_counts())

    st.subheader("Average Days in Care by Status")
    st.write(dogs_df.groupby("Status")["Days in Care"].mean())


elif page == "Matchmaking Dashboard":
    matchmaking_dashboard(adopters_df, dogs_df)

