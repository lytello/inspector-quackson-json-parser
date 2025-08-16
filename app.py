import pandas as pd
import streamlit as st
import json
import random
import time
from collections.abc import Mapping

# Function to load JSON data from a file
def load_json_from_file(filename):
    with open(filename, 'r') as file:
        return file.read()

# Load default JSON data from a text file
default_json = load_json_from_file('resources/data/default_data.json')

# Function to load JSON data
def load_json_data(json_text):
    try:
        return json.loads(json_text)
    except json.JSONDecodeError as e:
        st.error(f"JSON Decode Error: {str(e)}")
        return None

# Function to filter rows based on search term and selected columns
def filter_rows(rows, search_term, search_columns):
    if search_term:
        return [
            row for row in rows
            if any(search_term.lower() in str(row.get(col, '')).lower() for col in search_columns)
        ]
    return rows

# Function to display rows
def display_rows(rows, columns_to_display, view_mode, num_rows, row_order):
    if view_mode == "List":
        if row_order == "Random":
            sample_rows = random.sample(rows, min(num_rows, len(rows)))
        else:
            sample_rows = rows[:num_rows]
        for row in sample_rows:
            row_display = {col: row.get(col, None) for col in columns_to_display}
            st.write(row_display)
    elif view_mode == "Table":
        df = pd.DataFrame(rows)
        if row_order == "Random":
            sample_df = df[columns_to_display].sample(n=min(num_rows, len(df)))
        else:
            sample_df = df[columns_to_display].head(num_rows)
        st.dataframe(sample_df)

# Function to explore JSON structures and use sidebar for navigation
def explore_json(data):
    if isinstance(data, Mapping):
        # Use sidebar for navigation
        keys = list(data.keys())
        # Generate display labels with type info
        key_labels = [
            f"**{key}** ({get_type_label(data[key])})" for key in keys
        ]
        # Create a mapping from display label back to key
        label_to_key = {label: key for label, key in zip(key_labels, keys)}
        selected_label = st.sidebar.radio("Select a section to view", key_labels)
        selected_key = label_to_key[selected_label]
        explore_json_content(data[selected_key], selected_key)

# Helper function to get type label
def get_type_label(value):
    if isinstance(value, Mapping):
        return "Object"
    elif isinstance(value, list):
        if all(isinstance(item, dict) for item in value):
            return "List of Objects"
        return "List"
    else:
        return type(value).__name__.capitalize()

def explore_json_content(data, parent_key="Root", level=0):
    """
    Recursively explore and display JSON data without nesting expanders.
    """
    indent = "&nbsp;" * 4 * level  # Indentation based on nesting level

    if isinstance(data, list):
        if all(isinstance(item, dict) for item in data):
            st.markdown(f"{indent}**{parent_key}** (List of Objects)", unsafe_allow_html=True)
            all_columns = {key: type(value).__name__ for row in data for key, value in row.items()}
            columns_to_display = list(all_columns.keys())

            selected_columns = st.multiselect(f"Columns to display for {parent_key}", options=columns_to_display, default=columns_to_display)
            search_term = st.text_input(f"Search in {parent_key}", value="")
            search_columns = st.multiselect(f"Search columns for {parent_key}", options=selected_columns, default=selected_columns)

            filtered_rows = filter_rows(data, search_term, search_columns)
            st.write(f"{row_order} sample of {num_rows} rows (if available):")
            display_rows(filtered_rows, selected_columns, view_mode, num_rows, row_order)

        else:
            st.markdown(f"{indent}**{parent_key}** (List)", unsafe_allow_html=True)
            for idx, item in enumerate(data):
                st.markdown(f"{indent}- Item {idx+1}:")
                explore_json_content(item, f"{parent_key}[{idx}]", level+1)

    elif isinstance(data, Mapping):
        st.markdown(f"{indent}**{parent_key}** (Object)", unsafe_allow_html=True)
        for key, value in data.items():
            explore_json_content(value, key, level+1)

    else:
        st.markdown(f"{indent}<b>{parent_key}:</b> {data}", unsafe_allow_html=True)

# About dialog
@st.dialog("About")
def about_dialog():
    try:
        with open("resources/data/about.txt", "r") as file:
            about_text = file.read()
    except FileNotFoundError:
        about_text = "About file missing!!"
    st.markdown(about_text)

# App

st.set_page_config(
    page_title="Inspector Quackson",
    page_icon="resources/images/detective_duck.png",
    layout="wide"
)

if st.sidebar.button("About"):
    about_dialog()

# Set up the Streamlit interface
col1, col2 = st.columns([3, 1]) 

with col1:
    st.markdown("<h1><span style='color:#008000;'>Inspector Quackson</span>: <span style='color:#FFD000;'> JSON Explorer</span></h1>", unsafe_allow_html=True)
with col2:
    images = [
        "resources/images/detective_duck.png",
        "resources/images/detective_duck2.png"
    ]
    with st.spinner(""):
        image_placeholder = st.empty()
        for i in range(6):
            img_path = images[i % len(images)]
            image_placeholder.image(img_path)
            time.sleep(0.5)

# Sidebar for configuration options
st.sidebar.header("Configuration Options")
view_mode = st.sidebar.radio("Select view mode:", ("List", "Table"), horizontal=True)
row_order = st.sidebar.radio("Select row order:", ("Sequential", "Random"), horizontal=True)
num_rows  = st.sidebar.slider("Number of rows to display", min_value=1, max_value=5, value=2)

# Input field for JSON text
json_text = st.text_area("Enter your JSON below:", default_json, height=300)

# Process the JSON input
data = load_json_data(json_text)
if data is not None:
    # If the root is a list of dicts, treat it as a single table
    if isinstance(data, list) and all(isinstance(row, dict) for row in data):
        explore_json_content(data, parent_key="Root Table")
    else:
        explore_json(data)
else:
    st.error("Invalid JSON input.")
