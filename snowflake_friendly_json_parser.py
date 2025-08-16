# Snowflake version with everything in one file and without the fun stuff.

import pandas as pd
import streamlit as st
import json
import random

# Function to load JSON data from a file
def load_json_from_file(filename):
    with open(filename, 'r') as file:
        return file.read()

# Load default JSON data from a text file
default_json = """
{
  "duck_species_info": [
    {
      "species_name": "Mallard",
      "conservation_status": "Least Concern",
      "typical_habitats": ["Wetlands", "Rivers", "Lakes", "Urban Parks", "Coastal Areas"]
    },
    {
      "species_name": "Wood Duck",
      "conservation_status": "Least Concern",
      "typical_habitats": ["Swamps", "Forested Wetlands", "Riverine Forests", "Floodplains", "Ponds"]
    },
    {
      "species_name": "Northern Pintail",
      "conservation_status": "Least Concern",
      "typical_habitats": ["Marshes", "Lakes", "Ponds", "Coastal Areas", "Grasslands"]
    },
    {
      "species_name": "Gadwall",
      "conservation_status": "Least Concern",
      "typical_habitats": ["Lakes", "Rivers", "Wetlands", "Marshes", "Estuaries"]
    },
    {
      "species_name": "American Black Duck",
      "conservation_status": "Least Concern",
      "typical_habitats": ["Forested Wetlands", "Coastal Marshes", "Mudflats", "Rivers", "Ponds"]
    }
  ],
  "duck_population_data": [
    {
      "id": 1,
      "species_name": "Mallard",
      "habitat": "Wetlands",
      "population": 1200,
      "data": {
        "average_weight": 1.5,
        "average_wingspan": 82,
        "migratory_patterns": ["North America", "Europe"]
      }
    },
    {
      "id": 2,
      "species_name": "Mallard",
      "habitat": "Rivers",
      "population": 950,
      "data": {
        "average_weight": 1.4,
        "average_wingspan": 80,
        "migratory_patterns": ["Asia", "Europe"]
      }
    },
    {
      "id": 3,
      "species_name": "Mallard",
      "habitat": "Lakes",
      "population": 1500,
      "data": {
        "average_weight": 1.6,
        "average_wingspan": 85,
        "migratory_patterns": ["North America", "Africa"]
      }
    },
    {
      "id": 4,
      "species_name": "Mallard",
      "habitat": "Urban Parks",
      "population": 800,
      "data": {
        "average_weight": 1.3,
        "average_wingspan": 78,
        "migratory_patterns": ["Europe", "South America"]
      }
    },
    {
      "id": 5,
      "species_name": "Mallard",
      "habitat": "Coastal Areas",
      "population": 1100,
      "data": {
        "average_weight": 1.5,
        "average_wingspan": 83,
        "migratory_patterns": ["Asia", "North America"]
      }
    },
    {
      "id": 6,
      "species_name": "Wood Duck",
      "habitat": "Swamps",
      "population": 600,
      "data": {
        "average_weight": 0.7,
        "average_wingspan": 73,
        "migratory_patterns": ["North America"]
      }
    },
    {
      "id": 7,
      "species_name": "Wood Duck",
      "habitat": "Forested Wetlands",
      "population": 750,
      "data": {
        "average_weight": 0.8,
        "average_wingspan": 76,
        "migratory_patterns": ["North America", "Central America"]
      }
    },
    {
      "id": 8,
      "species_name": "Wood Duck",
      "habitat": "Riverine Forests",
      "population": 900,
      "data": {
        "average_weight": 0.75,
        "average_wingspan": 75,
        "migratory_patterns": ["North America"]
      }
    },
    {
      "id": 9,
      "species_name": "Wood Duck",
      "habitat": "Floodplains",
      "population": 500,
      "data": {
        "average_weight": 0.7,
        "average_wingspan": 72,
        "migratory_patterns": ["North America"]
      }
    },
    {
      "id": 10,
      "species_name": "Wood Duck",
      "habitat": "Ponds",
      "population": 650,
      "data": {
        "average_weight": 0.7,
        "average_wingspan": 74,
        "migratory_patterns": ["North America", "Caribbean"]
      }
    }
  ]
}
"""

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

@st.dialog("About")
def about_dialog():
  about_text = f"""
  This is a tool for exploring and interacting with JSON data.

    **Features:**
    
    - **Load and Edit JSON**: Input or modify your JSON data using the provided text area.
    - **Table Exploration**: Automatically detect and display tables within your JSON data for navigation.
    - **Customizable Views**: Choose between a List or Table view to display your data.
    - **Column Selection**: Select which columns to display from each table.
    - **Search and Filter**: Use search terms to filter rows, and specify which columns to search in.
    - **Flexible Display Options**: Decide the number of rows to view and whether to display them sequentially or randomly."""
    
  st.markdown(about_text)

if st.sidebar.button("About"):
  about_dialog()
# Set up the Streamlit interface
col1, col2 = st.columns([3, 1]) 

st.title("JSON Explorer 🦆")


# Sidebar for configuration options and "About" button
st.sidebar.header("Configuration Options")
view_mode = st.sidebar.radio("Select view mode:", ("List", "Table"))
row_order = st.sidebar.radio("Select row order:", ("Sequential", "Random"))
num_rows = st.sidebar.slider("Number of rows to display", min_value=1, max_value=5, value=2)

# Input field for JSON text
json_text = st.text_area("Edit the JSON below:", default_json, height=300)

# Process the JSON input if it is provided
data = load_json_data(json_text)
if data and isinstance(data, dict):
    for table_name, rows in data.items():
        with st.expander(f"Table: {table_name}"):
            if rows and isinstance(rows, list) and all(isinstance(row, dict) for row in rows):
                all_columns = {key: type(value).__name__ for row in rows for key, value in row.items()}

                # Sidebar column selection updated for each table
                columns_to_display = st.sidebar.multiselect(
                    f"Select columns for {table_name}",
                    options=list(all_columns.keys()),
                    default=list(all_columns.keys())
                )

                # Search box for filtering rows
                search_term = st.text_input(f"Search in {table_name}", value="")
                search_columns = st.multiselect(f"Search columns for {table_name}", options=columns_to_display, default=columns_to_display)

                st.write("Columns:")
                for col, col_type in all_columns.items():
                    if col in columns_to_display:
                        st.write(f"- **{col}** ({col_type})")

                # Filter rows based on search term and columns
                filtered_rows = filter_rows(rows, search_term, search_columns)

                st.write(f"{row_order} sample of {num_rows} rows (if available):")
                display_rows(filtered_rows, columns_to_display, view_mode, num_rows, row_order)
            else:
                st.write("No columns found or invalid table structure")
else:
    st.error("Provided JSON is not a valid dictionary structure representing tables.")
