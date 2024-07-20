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

# Accademic succes - loyihamizni boshlaymiz
st.set_page_config(
    page_title="Accademic Success",
    page_icon=":dart:",
    layout="wide",
    initial_sidebar_state="expanded")

file_path = 'cleaned_data.csv'
data = pd.read_csv(file_path, index_col=0)

st.header('Academic Success :mortar_board:', divider=True)
st.header('Dataset overview')

st.sidebar.header("Dashboard Controls")

# Filterlar uchun alohida funksiya yozib olamiz
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

filtered_data = filter_data(data)

total_students = len(filtered_data)
male_students = len(filtered_data[filtered_data['Gender'] == 'male'])
female_students = len(filtered_data[filtered_data['Gender'] == 'female'])
average_age = filtered_data['Age at enrollment'].mean()

data

c1, c2, c3 = st.columns([1, 2, 1])
col1, col2 = st.columns([5, 10])  
with c1:
    fig_d_or_e = px.pie(filtered_data, names='Daytime/evening attendance', 
                        title='Daytime/evening attendance',
                        color_discrete_sequence=['yellow', 'green'])
    fig_d_or_e.update_layout(width=650, height=400)  
    st.plotly_chart(fig_d_or_e)

with c2:
    fig_gender = px.pie(filtered_data, names='Target', 
                        title='Target',
                        color_discrete_sequence=['Red', 'Black', 'Lightblue'])
    fig_gender.update_layout(width=650, height=400) 
    st.plotly_chart(fig_gender)

with c3:
    fig_gender = px.pie(filtered_data, names='Gender', 
                        title='Gender Distribution',
                        color_discrete_sequence=['Red', 'green'])
    fig_gender.update_layout(width=650, height=400) 
    st.plotly_chart(fig_gender)


with col1:
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
        xaxis_tickangle=-45,  
        width=1000, height=490  
    )
    st.plotly_chart(fig_scholarship)

# image_url = 'https://get.wallhere.com/photo/1920x1080-px-flag-Portugal-1401747.jpg'

# # Display the image
# st.image(image_url, caption='Your Image Caption', use_column_width=True)

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

filtered_data['Country'] = filtered_data['Nationality'].map(nationality_to_country)

geojson_file = 'countries.geo.json'
with open(geojson_file) as f:
    geojson_data = json.load(f)

data_map = filtered_data['Country'].value_counts().reset_index()
data_map.columns = ['Country', 'Count']
data_map['Count'] = data_map['Count'].astype(int) 

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

def create_map(data_map, geojson_data):
    m = folium.Map(
        location=[20, 0], 
        zoom_start=2, 
        max_zoom=20, 
        min_zoom=2, 
        scrollWheelZoom=True,
        maxBounds=[[-75, -200], [100, 200]], 
        # tiles='cartodb positron',
        # attr='Map tiles by CartoDB, under CC BY 3.0. Data by OpenStreetMap, under ODbL.'
    )

    choropleth = folium.Choropleth(
        geo_data=geojson_data,
        name='choropleth',
        data=data_map,
        columns=['Country', 'Count'],
        key_on='feature.properties.name',
        fill_color='RdBu',
        fill_opacity=0.7,
        line_opacity=0.5, 
        line_color='lime',
        legend_name='Student Contribution by Country'
    ).add_to(m)

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
            border: 2px solid yellow;
            border-radius: 6px;
            box-shadow: 10px;
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
                icon=folium.Icon(icon='star', color='green')
            ).add_to(m)

    # Minimap qo'shamiz
    minimap = MiniMap(toggle_display=True)
    m.add_child(minimap)

    return m

m = create_map(data_map, geojson_data)

# Expander orqali mapni chiqaramiz
with st.expander("View Map :eyes:", expanded=False):
    # Xaritani HTLM filega saqlaymiz va streamlitda namoish qilamiz
    map_html = "map.html"
    m.save(map_html)
    with open(map_html, 'r') as f:
        map_html_content = f.read()
    st.components.v1.html(map_html_content, width=920, height=500)

# Heatmap chiqaramiz
st.header("Heatmap of numeric categories")

plt.figure(figsize=(10, 8))
sns.heatmap(data.corr(numeric_only=True), cmap='Spectral', center=0)
st.pyplot(plt)

# Orginal datasetni o'zgaruvchiga yuklab olamiz
original_data = pd.read_csv('Academic_Success.csv', index_col=0)

# Eski tozalanmagan ma'lumotlar va tozalangan ma'lumotlarni solishitiramiz
if st.button('(D) Statistics of old data with NaN values vs cleaned cata :large_blue_diamond:'):
    # Descriptive statistikalar orginal dataset uchun
    st.header('Summary Statistics: Original Data with NaN Values')
    st.write(original_data.describe())
    
    # Descriptive statistikalar cleaned dataset uchun 
    st.header('Summary Statistics: Cleaned Data')
    st.write(data.describe())

    # Piechartlar hosil qilamiz Gender bo'yicha o'zgarishni solishtirish uchun
    c_1, c_2 = st.columns([3, 3], gap = 'medium')

    with c_1:
        # Eski dataset uchun gender (NaN valuelari bilan)
        fig_d_or_e = px.pie(original_data, names='Gender', 
                            title='Gender with Nan values',
                            hole = 0.6,
                            color_discrete_sequence=['yellow', 'green'])
        fig_d_or_e.update_layout(width=650, height=400) 
        st.plotly_chart(fig_d_or_e)

    with c_2:
        # Tozalangan dataset uchun gender 
        fig_gender = px.pie(data, names='Gender', 
                            title='Gender',
                            hole = 0.6,
                            color_discrete_sequence=['Red', 'Black'])
        fig_gender.update_layout(width=650, height=400)
        st.plotly_chart(fig_gender)

    st.write('### Bu yerda Nan qiymatlardan tozalanmagan datasetdagi talablarning jinsi va Keyingi ya\'ni tozalangan datasetdagi talabalarning jinsi bo\'yicha solishtiruvchi piechartlar chiqarildi')


if st.button('Correlation of old data with NaN values vs cleaned data :large_orange_diamond:'):
    # Original dataset korrelatsiyasi
    st.header('Correlation: Original Data with NaN Values')
    st.write(original_data.select_dtypes('number').corr())
    
    # Tozalangan dataset korrelatsiyasi
    st.header('Correlation: Cleaned Data')
    st.write(data.select_dtypes('number').corr())

    cmp_1, cmp_2 = st.columns([3, 3], gap = 'medium')
    with cmp_1:
        st.header("Heatmap eski dataset uchun")

        plt.figure(figsize=(10, 8))
        sns.heatmap(original_data.corr(numeric_only=True), cmap='Spectral', center=0)
        st.pyplot(plt)

    with cmp_2:
        st.header("Heatmap tozalangan dataset")

        plt.figure(figsize=(10, 8))
        sns.heatmap(data.corr(numeric_only=True), cmap='Spectral', center=0)
        st.pyplot(plt)

    st.write('### Bu yerda Nan qiymatlardan tozalanmagan dataset va keyingi ya\'ni tozalangan datasetlarning korrelatsiyalari chiqarildi')
    