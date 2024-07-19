import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from folium.features import GeoJsonTooltip
from folium.plugins import MiniMap
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns
import json

# Load the data
file_path = 'cleaned_data.csv'
data = pd.read_csv(file_path, index_col=0)

st.header('Academic Success', divider=True)
st.header('Dataset overview')

# Sidebar Elements
st.sidebar.header("Dashboard Controls")

def filter_data(data):
    """Apply filters based on sidebar selections and return filtered data."""
    if 'Nationality' in data.columns:
        nationalities = data['Nationality'].unique().tolist()
        selected_nationalities = st.sidebar.multiselect("Select Nationalities", nationalities, default=nationalities)
        data = data[data['Nationality'].isin(selected_nationalities)]

    if 'Gender' in data.columns:
        genders = data['Gender'].unique().tolist()
        selected_genders = st.sidebar.multiselect("Select Gender", genders, default=genders)
        data = data[data['Gender'].isin(selected_genders)]

    if 'Daytime/evening attendance' in data.columns:
        timede = data['Daytime/evening attendance'].unique().tolist()
        selected_time = st.sidebar.multiselect("Select time", timede, default=timede)
        data = data[data['Daytime/evening attendance'].isin(selected_time)]

    if 'Age at enrollment' in data.columns:
        min_age, max_age = int(data['Age at enrollment'].min()), int(data['Age at enrollment'].max())
        age_range = st.sidebar.slider("Select Age Range", min_age, max_age, (min_age, max_age))
        data = data[data['Age at enrollment'].between(age_range[0], age_range[1])]

    if 'Year' in data.columns:
        min_year, max_year = int(data['Year'].min()), int(data['Year'].max())
        year_range = st.sidebar.slider("Select Year Range", min_year, max_year, (min_year, max_year))
        data = data[data['Year'].between(year_range[0], year_range[1])]

    return data

# Apply Filters
filtered_data = filter_data(data)

# Define metrics
total_students = len(filtered_data)
male_students = len(filtered_data[filtered_data['Gender'] == 'male'])
female_students = len(filtered_data[filtered_data['Gender'] == 'female'])
average_age = filtered_data['Age at enrollment'].mean()

data
# Create two columns for layout
c1, c2, c3 = st.columns([1, 2, 1])
col1, col2 = st.columns([5, 10])  # Adjust column widths
with c1:
    fig_d_or_e = px.pie(filtered_data, names='Daytime/evening attendance', 
                        title='Daytime/evening attendance',
                        hole=0,
                        color_discrete_sequence=['yellow', 'black'])
    fig_d_or_e.update_layout(width=650, height=400)  # Set chart size and margins
    st.plotly_chart(fig_d_or_e)

with c2:
    # Pie chart for Gender Distribution
    fig_gender = px.pie(filtered_data, names='Target', 
                        title='Target',
                        hole=0,
                        color_discrete_sequence=['Red', 'Black', 'Lightblue'])
    fig_gender.update_layout(width=650, height=400)  # Set chart size and margins
    st.plotly_chart(fig_gender)

with c3:
    fig_gender = px.pie(filtered_data, names='Gender', 
                        title='Gender Distribution',
                        hole=0.4,
                        color_discrete_sequence=['Red', 'green'])
    fig_gender.update_layout(width=650, height=400)  # Set chart size and margins
    st.plotly_chart(fig_gender)


# Bar chart for Marital Status
with col1:
    # Display Metrics
    st.metric(label="Total Students", value=total_students)
    st.metric(label="Male Students", value=male_students)
    st.metric(label="Female Students", value=female_students)
    st.metric(label="Average Age", value=round(average_age, 2))


with col2:
    fig_scholarship = px.bar(
        filtered_data, 
        x='Course', 
        color='Course',
        title='Course', 
    )
    fig_scholarship.update_layout(
        xaxis_title='Course',
        xaxis_tickangle=-45,  # Rotate x-axis labels to -45 degrees
        width=1000, height=490  # Set chart size
    )
    st.plotly_chart(fig_scholarship)
image_url = 'https://get.wallhere.com/photo/1920x1080-px-flag-Portugal-1401747.jpg'

# Display the image
st.image(image_url, caption='Your Image Caption', use_column_width=True)



# Example dictionary mapping nationalities to countries
nationality_to_country = {
    'Portuguese': 'Portugal',
    'Santomean': 'São Tomé and Príncipe',
    'Brazilian': 'Brazil',
    'Guinean': 'Guinea',
    'Spanish': 'Spain',
    'Moldova (Republic of)': 'Moldova',
    'Angolan': 'Angola',
    'Cape Verdean': 'Cape Verde',
    'Italian': 'Italy',
    'Mexican': 'Mexico',
    'German': 'Germany',
    'Ukrainian': 'Ukraine',
    'Russian': 'Russia',
    'Mozambican': 'Mozambique',
    'Romanian': 'Romania',
    'Colombian': 'Colombia'
}

# Create a new column 'Country' based on the 'Nationality' column
filtered_data['Country'] = filtered_data['Nationality'].map(nationality_to_country)

# Load GeoJSON file for country boundaries
geojson_file = 'countries.geo.json'
with open(geojson_file) as f:
    geojson_data = json.load(f)

# Prepare data for Choropleth
data_map = filtered_data['Country'].value_counts().reset_index()
data_map.columns = ['Country', 'Count']
data_map['Count'] = data_map['Count'].astype(int)  # Convert int64 to int for JSON serialization

# Define coordinates for the center of each country
country_coords = {
    'Portugal': [39.3999, -8.2245],
    'São Tomé and Príncipe': [0.1864, 6.6131],
    'Brazil': [-14.2350, -51.9253],
    'Guinea': [9.9456, -9.6966],
    'Spain': [40.4637, -3.7492],
    'Moldova': [47.4116, 28.3699],
    'Angola': [-11.2027, 17.8739],
    'Cape Verde': [16.5388, -23.0418],
    'Italy': [41.8719, 12.5674],
    'Mexico': [23.6345, -102.5528],
    'Germany': [51.1657, 10.4515],
    'Ukraine': [48.3794, 31.1656],
    'Russia': [61.5240, 105.3188],
    'Mozambique': [-18.6657, 35.5296],
    'Romania': [45.9432, 24.9668],
    'Colombia': [4.5709, -74.2973]
}

# Create and customize the map
def create_map(data_map, geojson_data):
    m = folium.Map(
        location=[20, 0], 
        zoom_start=2, 
        max_zoom=20, 
        min_zoom=2, 
        scrollWheelZoom=True,
        maxBounds=[[-60, -180], [85, 180]],  # South-West and North-East corners
        tiles='cartodb positron',
        attr='Map tiles by CartoDB, under CC BY 3.0. Data by OpenStreetMap, under ODbL.'
    )

    choropleth = folium.Choropleth(
        geo_data=geojson_data,
        name='choropleth',
        data=data_map,
        columns=['Country', 'Count'],
        key_on='feature.properties.name',
        fill_color='RdBu',
        fill_opacity=0.7,
        line_opacity=0.5,  # Thicker boundary lines
        line_color='lime',  # Boundary color
        legend_name='Student Contribution by Country'
    ).add_to(m)

    # Ensure data is correctly being passed to the Choropleth layer
    for feature in choropleth.geojson.data['features']:
        country_name = feature['properties']['name']
        feature['properties']['Count'] = int(data_map.set_index('Country').loc[country_name]['Count']) if country_name in data_map['Country'].values else 'No data'

    # Add tooltips to the choropleth
    tooltip = GeoJsonTooltip(
        fields=['name', 'Count'],
        aliases=['Country', 'Count'],
        localize=True,
        sticky=False,
        labels=True,
        style="""
            background-color: #F0EFEF;
            border: 2px solid black;
            border-radius: 3px;
            box-shadow: 3px;
        """
    )
    choropleth.geojson.add_child(tooltip)
    folium.LayerControl().add_to(m)

    # Decorative elements
    for country, coord in country_coords.items():
        if country in data_map['Country'].values:
            folium.Marker(
                location=coord,
                popup=f'Students from {country}',
                icon=folium.Icon(icon='info-sign', color='blue')
            ).add_to(m)

    # Add minimap
    minimap = MiniMap(toggle_display=True)
    m.add_child(minimap)

    return m

m = create_map(data_map, geojson_data)

# Display map in an expander
with st.expander("View Map", expanded=False):
    # Save map to an HTML file and display in Streamlit
    map_html = "map.html"
    m.save(map_html)
    with open(map_html, 'r') as f:
        map_html_content = f.read()
    st.components.v1.html(map_html_content, width=670, height=500)

st.header("Heatmap of numeric categories")

plt.figure(figsize=(10, 8))
sns.heatmap(data.corr(numeric_only=True), cmap='coolwarm', center=0)
st.pyplot(plt)

# Select numeric columns for PCA
numeric_cols = filtered_data.select_dtypes(include=['float64', 'int64']).columns
numeric_data = filtered_data[numeric_cols]

# Apply PCA
pca = PCA(n_components=2)
pca_result = pca.fit_transform(numeric_data)

# Create a DataFrame for the PCA results
pca_df = pd.DataFrame(pca_result, columns=['PC1', 'PC2'])
if 'Target' in filtered_data.columns:
    pca_df['Target'] = filtered_data['Target'].values

# Placeholder for dropdown or any other UI elements if needed
if st.button('Show Summary Statistics of Old Data with NaN values vs Cleaned Data'):
    # Load the original dataset
    original_data = pd.read_csv('Academic_Success.csv', index_col=0)
    
    # Summary statistics for original data
    st.header('Summary Statistics: Original Data with NaN Values')
    st.write(original_data.iloc[:1000].describe())
    
    # Summary statistics for cleaned data
    st.header('Summary Statistics: Cleaned Data')
    st.write(data.describe())

if st.button('Show correlation of old data vs cleaned data'):
    # Load the original dataset
    original_data = pd.read_csv('Academic_Success.csv', index_col=0)
    
    # Summary statistics for original data
    st.header('Correlation: Original Data with NaN Values')
    st.write(original_data.iloc[:1000].select_dtypes('number').corr())
    
    # Summary statistics for cleaned data
    st.header('Correlation: Cleaned Data')
    st.write(data.select_dtypes('number').corr())
