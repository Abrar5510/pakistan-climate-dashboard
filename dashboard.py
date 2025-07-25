import streamlit as st
import pandas as pd
import plotly.express as px

# Load Data
@st.cache_data
def load_data():
    data = [
        {'Date': '2022-03-15', 'City': 'Jacobabad', 'Province': 'Sindh', 'Max_Temp_C': 47.0, 'Min_Temp_C': 32.1, 'Avg_Temp_C': 39.55,
         'Rainfall_mm': 0, 'Humidity_Percent': 45, 'Heat_Index_C': 52.3, 'Heatstroke_Cases': 15, 'Heat_Deaths': 2, 'Livestock_Deaths': 34,
         'Water_Shortage_Level': 'High', 'year': 2022},
        {'Date': '2022-03-16', 'City': 'Jacobabad', 'Province': 'Sindh', 'Max_Temp_C': 47.5, 'Min_Temp_C': 32.8, 'Avg_Temp_C': 40.15,
         'Rainfall_mm': 0, 'Humidity_Percent': 43, 'Heat_Index_C': 53.1, 'Heatstroke_Cases': 18, 'Heat_Deaths': 3, 'Livestock_Deaths': 41,
         'Water_Shortage_Level': 'High', 'year': 2022},
        {'Date': '2022-04-15', 'City': 'Nawabshah', 'Province': 'Sindh', 'Max_Temp_C': 49.5, 'Min_Temp_C': 35.1, 'Avg_Temp_C': 42.3,
         'Rainfall_mm': 0, 'Humidity_Percent': 38, 'Heat_Index_C': 55.8, 'Heatstroke_Cases': 25, 'Heat_Deaths': 5, 'Livestock_Deaths': 67,
         'Water_Shortage_Level': 'Severe', 'year': 2022}
    ]
    return pd.DataFrame(data)

df = load_data()

# ---- Sidebar ----
st.set_page_config(page_title="Pakistan Heatwave Dashboard", layout="wide")
st.sidebar.title("⚙️ Filters")

dark_mode = st.sidebar.toggle("🌙 Dark Mode")
view_table = st.sidebar.toggle("📋 Show Tables")

selected_province = st.sidebar.selectbox("Select Province", ["All"] + sorted(df["Province"].unique().tolist()))
selected_city = st.sidebar.selectbox("Select City", ["All"] + sorted(df["City"].unique().tolist()))
selected_year = st.sidebar.selectbox("Select Year", ["All"] + sorted(df["year"].unique().tolist()))

# Filter
filtered_df = df.copy()
if selected_province != "All":
    filtered_df = filtered_df[filtered_df["Province"] == selected_province]
if selected_city != "All":
    filtered_df = filtered_df[filtered_df["City"] == selected_city]
if selected_year != "All":
    filtered_df = filtered_df[filtered_df["year"] == selected_year]

# ---- Main ----
st.title("🔥 Pakistan Heatwave Dashboard")

tab1, tab2 = st.tabs(["🌡️ Temperature Analytics", "🏥 Health & Risk Monitor"])

with tab1:
    st.subheader("Max Temperature vs Heat Index")

    if view_table:
        st.dataframe(filtered_df[["Date", "City", "Max_Temp_C", "Heat_Index_C", "Humidity_Percent"]])
    else:
        fig = px.line(filtered_df, x="Date", y=["Max_Temp_C", "Heat_Index_C"],
                      color_discrete_map={"Max_Temp_C": "red", "Heat_Index_C": "orange"},
                      title="Max Temperature vs Heat Index Over Time",
                      labels={"value": "°C", "Date": "Date", "variable": "Metric"})
        fig.update_layout(legend_title_text="Metric", template="plotly_dark" if dark_mode else "plotly")
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.subheader("Temperature Risk Zones")
    zone_counts = {
        'Extreme (>50°C)': len(filtered_df[filtered_df["Max_Temp_C"] > 50]),
        'Severe (45–50°C)': len(filtered_df[(filtered_df["Max_Temp_C"] >= 45) & (filtered_df["Max_Temp_C"] <= 50)]),
        'High (40–45°C)': len(filtered_df[(filtered_df["Max_Temp_C"] >= 40) & (filtered_df["Max_Temp_C"] < 45)]),
        'Moderate (<40°C)': len(filtered_df[filtered_df["Max_Temp_C"] < 40])
    }

    zone_df = pd.DataFrame({
        "Zone": list(zone_counts.keys()),
        "Count": list(zone_counts.values())
    })

    if view_table:
        st.dataframe(zone_df)
    else:
        pie = px.pie(zone_df, values="Count", names="Zone", title="Temperature Zone Distribution")
        pie.update_layout(template="plotly_dark" if dark_mode else "plotly")
        st.plotly_chart(pie, use_container_width=True)

with tab2:
    st.subheader("Heatstroke Cases vs Deaths")

    if view_table:
        st.dataframe(filtered_df[["Date", "City", "Heatstroke_Cases", "Heat_Deaths"]])
    else:
        bar = px.bar(filtered_df, x="Date", y=["Heatstroke_Cases", "Heat_Deaths"],
                     barmode="group", color_discrete_sequence=["orange", "red"],
                     title="Heatstroke Cases & Deaths Over Time")
        bar.update_layout(template="plotly_dark" if dark_mode else "plotly")
        st.plotly_chart(bar, use_container_width=True)

    st.divider()

    st.subheader("🚨 Critical Alerts (Deaths > 2)")
    critical = filtered_df[filtered_df["Heat_Deaths"] > 2]

    if not critical.empty:
        st.dataframe(critical[["Date", "City", "Heat_Deaths", "Max_Temp_C", "Heat_Index_C"]])
    else:
        st.info("No critical alerts based on current filters.")
