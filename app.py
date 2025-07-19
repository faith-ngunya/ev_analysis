import streamlit as st
import pandas as pd
import plotly.express as px



# Page settings
st.set_page_config(page_title='Electric Vehicle Dashboard', layout='wide')
st.title('🚗 Electric Vehicle Data Dashboard')

# Load data with caching
@st.cache_data
def load_data():
    df = pd.read_csv('electric_vehicles_spec_2025.csv')
    # Avoid chained assignment by assigning back directly
    df['torque_nm'] = df['torque_nm'].fillna(0)
    df['towing_capacity_kg'] = df['towing_capacity_kg'].fillna(0)
    df['number_of_cells'] = df['number_of_cells'].fillna(df['number_of_cells'].median())
    df['fast_charge_port'] = df['fast_charge_port'].fillna('Unknown')
    return df

df = load_data()

# Sidebar filters
st.sidebar.header('🔍 Filter Options')
brands = sorted(df['brand'].dropna().unique())
selected_brand = st.sidebar.multiselect('Select Brand(s)', options=brands, default=brands)

body_types = sorted(df['car_body_type'].dropna().unique())
selected_body = st.sidebar.multiselect('Select Car Body Type(s)', options=body_types, default=body_types)

# Filter data based on selections
filtered_df = df[
    df['brand'].isin(selected_brand) & 
    df['car_body_type'].isin(selected_body)
]

# KPIs
st.subheader('📈 Key Performance Indicators (KPIs)')
col1, col2, col3 = st.columns(3)
col1.metric('Total Models', len(filtered_df))
col2.metric('Average Battery Capacity (kWh)', round(filtered_df['battery_capacity_kWh'].mean(), 2))
col3.metric('Average Range (km)', round(filtered_df['range_km'].mean(), 2))

# Display filtered data
st.subheader(f'🛠️ Filtered Electric Vehicles Data ({len(filtered_df)} records)')
st.dataframe(filtered_df)

# Plot 1: Battery Capacity vs Range (Interactive Scatter Plot)
st.subheader('🔋 Battery Capacity vs Range (Interactive)')
fig1 = px.scatter(
    filtered_df,
    x='battery_capacity_kWh',
    y='range_km',
    color='car_body_type',
    hover_data=['brand', 'model'],
    labels={'battery_capacity_kWh': 'Battery Capacity (kWh)', 'range_km': 'Range (km)'},
    title='Battery Capacity vs Driving Range'
)
st.plotly_chart(fig1, use_container_width=True)

# Plot 2: Top Brands by Number of Models (Interactive Bar Plot)
st.subheader('🏆 Top 10 Brands by Number of Models')
top_brands = filtered_df['brand'].value_counts().head(10)
fig2 = px.bar(
    top_brands,
    x=top_brands.values,
    y=top_brands.index,
    orientation='h',
    labels={'x': 'Number of Models', 'index': 'Brand'},
    title='Top 10 Brands by Model Count'
)
st.plotly_chart(fig2, use_container_width=True)

# Plot 3: Battery Capacity Distribution (Interactive Histogram)
st.subheader('⚡ Battery Capacity Distribution')
fig3 = px.histogram(
    filtered_df,
    x='battery_capacity_kWh',
    nbins=20,
    title='Distribution of Battery Capacity (kWh)',
    labels={'battery_capacity_kWh': 'Battery Capacity (kWh)'}
)
st.plotly_chart(fig3, use_container_width=True)
