import pandas as pd
import streamlit as st
import plotly.express as px
import folium
from folium.features import GeoJsonTooltip
from sklearn.decomposition import PCA
import json
from Project import data

st.title('3D Scatter Plot of Student Data')

# Dropdowns to select features for the axes
x_axis = st.selectbox('Select X-axis feature', data.columns)
y_axis = st.selectbox('Select Y-axis feature', data.columns)
z_axis = st.selectbox('Select Z-axis feature', data.columns)
color = st.selectbox('Select feature for color', data.columns)

# Create 3D scatter plot using Plotly
fig = px.scatter_3d(data, x=x_axis, y=y_axis, z=z_axis, color=color)
st.plotly_chart(fig)