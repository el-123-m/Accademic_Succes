import streamlit as st
import plotly.express as px
from Project import data

st.title('3D Scatter Plot of Student Data')

x_axis = st.selectbox('Select X-axis feature', data.columns)
y_axis = st.selectbox('Select Y-axis feature', data.columns)
z_axis = st.selectbox('Select Z-axis feature', data.columns)
color = st.selectbox('Select feature for color', data.columns)

fig = px.scatter_3d(data, x=x_axis, y=y_axis, z=z_axis, color=color)
st.plotly_chart(fig, use_container_width=False, width=1200, height=800)