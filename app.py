import streamlit as st
import pandas as pd
import plotly.express as px
from io import StringIO

# Set the page configuration
st.set_page_config(page_title="Tutor LMS Support Dashboard", layout="wide", page_icon="📊")

# Load the CSV file
@st.cache_data
def load_data():
    df = pd.read_csv("tutor_plugin_support_threads.csv")
    return df

df = load_data()

# Define categories
categories = {
    "Course": ["course", "lesson", "content", "add course", "drip"],
    "Monetization": ["checkout", "payment", "cart", "pay"],
    "User Access": ["login", "register", "access", "account"],
    "Quiz": ["quiz", "question", "assignment", "grade"],
    "Assignment": [ "assignment", "grade"],
    "Critical Error": ["error", "bug", "problem", "crash", "not working", "broken", "critical", "down"],
    "Conflict": ["plugin", "wordpress", "shortcode", "theme compatibility", "conflict"],
    "Video": ["video", "audio", "playback", "streaming"],
    "Responsive": ["mobile", "tablet", "ios", "android"],
    "Page Builder": ["droip", "elementor", "divi", "oxygen", "bricks"],
    "Themes": ["themes", "theme", "skillate", "tutorstarter", "tutor starter"],
    "Others": []  # Default fallback
}

# Classify threads based on their titles
def classify_title(title):
    title_lower = title.lower()
    for category, keywords in categories.items():
        if category == "Others":
            continue
        for keyword in keywords:
            if keyword in title_lower:
                return category
    return "Others"

df["Issue Category"] = df["Thread Title"].apply(classify_title)

# Reorder to have Others last
category_order = list(categories.keys())
category_counts = df["Issue Category"].value_counts().reindex(category_order, fill_value=0)

# Color mapping for categories
category_colors = {
    "Course": "#FF5733",
    "Monetization": "#33FF57",
    "User Access": "#3357FF",
    "Quiz": "#F5A623",
    "Assignment": "#900C3F",
    "Critical Error": "#1D3557",
    "Conflict": "#6A4C93",
    "Video": "#F4A261",
    "Responsive": "#2A9D8F",
    "Page Builder": "#E76F51",
    "Themes": "#2F4F4F",
    "Others": "#D4AF37",
}

# Charts
bar_fig = px.bar(
    x=category_counts.index,
    y=category_counts.values,
    labels={"x": "Issue Category", "y": "Number of Threads"},
    title="Support Issue Categorization",
    color=category_counts.index,
    color_discrete_map=category_colors
)
bar_fig.update_layout(
    xaxis_tickangle=-45,
    template="plotly_dark",  # Dark theme for charts
    plot_bgcolor="#f4f4f4",  # Light background for the chart
    title_x=0.5
)

pie_fig = px.pie(
    names=category_counts.index,
    values=category_counts.values,
    title="Distribution of Issues",
    color=category_counts.index,
    color_discrete_map=category_colors
)
pie_fig.update_layout(template="plotly_dark", plot_bgcolor="#f4f4f4", title_x=0.5)

# Sidebar - Filter
with st.sidebar:
    st.header("🔍 Filter Options")
    selected_category = st.selectbox("Select a Category", options=["All"] + category_order)

# Apply filter to the data
if selected_category == "All":
    filtered_df = df
else:
    filtered_df = df[df["Issue Category"] == selected_category]

# Search functionality
search_query = st.text_input("Search Threads", "")
if search_query:
    filtered_df = filtered_df[filtered_df["Thread Title"].str.contains(search_query, case=False, na=False)]

# Display metrics in cards
col1, col2 = st.columns(2)

with col1:
    st.metric(label="Total Threads", value=len(df))

with col2:
    st.metric(label=f"'{selected_category}' Threads", value=len(filtered_df))

# Display charts
st.markdown("### 📈 Data Visualization")

col1, col2 = st.columns([2, 1])

with col1:
    st.plotly_chart(bar_fig, use_container_width=True)

with col2:
    st.plotly_chart(pie_fig, use_container_width=True)

# Thread list section with search filter
st.markdown(f"### 🔍 Threads in '{selected_category}'")

# Display the filtered thread list in a more interactive way
st.write(filtered_df[["Thread Title", "Thread URL"]].reset_index(drop=True))

# CSV export feature
@st.cache_data
def convert_df_to_csv(df):
    return df.to_csv(index=False)

csv = convert_df_to_csv(filtered_df)

# CSV Export button
st.download_button(
    label="Download Filtered Data as CSV",
    data=csv,
    file_name="filtered_threads.csv",
    mime="text/csv",
)

# Footer section with styling
st.markdown("---")
st.markdown("<center><i>Tutor LMS WP Support Forum Issues</i></center>", unsafe_allow_html=True)