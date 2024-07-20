import pandas as pd
import streamlit as st
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler, MaxAbsScaler, QuantileTransformer, Normalizer
from Project1 import data

# Funksiyalar skaling uchun
def apply_scaling(data, scaling_method):
    numeric_cols = data.select_dtypes(include=['float64', 'int64']).columns
    scaler = None

    if scaling_method == 'Standard Scaling':
        scaler = StandardScaler()
    elif scaling_method == 'Min-Max Scaling':
        scaler = MinMaxScaler()
    elif scaling_method == 'Robust Scaling':
        scaler = RobustScaler()
    elif scaling_method == 'MaxAbs Scaling':
        scaler = MaxAbsScaler()
    elif scaling_method == 'Quantile Transformation':
        scaler = QuantileTransformer()
    elif scaling_method == 'Normalizer':
        scaler = Normalizer()

    if scaler:
        data[numeric_cols] = scaler.fit_transform(data[numeric_cols])
    return data

# Funksiya scalingni generatsiya qilish uchun
def generate_visualizations(data):
    st.sidebar.header('Visualization Settings')

    # Scaling usullari
    scaling_method = st.sidebar.selectbox(
        'Select Scaling Method:',
        ['None', 'Standard Scaling', 'Min-Max Scaling', 'Robust Scaling', 'MaxAbs Scaling', 'Quantile Transformation', 'Normalizer']
    )

    # Scaling usuli jonatilgan murojat qilinsin
    if scaling_method != 'None':
        data = apply_scaling(data, scaling_method)

    # Visualization turi
    visualization_type = st.sidebar.radio(
        'Select Visualization Type:',
        ['Summary Statistics', 'Histogram', 'Scatter Plot', 'Box Plot', 'Pie/Donut Chart', 'Boxen Plot', 'Violin Plot', 'Bar Plot']
    )

    if visualization_type == 'Summary Statistics':
        st.title('Summary Statistics')
        st.write(data.describe())

    elif visualization_type == 'Histogram':
        st.sidebar.subheader('Histogram Settings')
        hist_column = st.sidebar.radio('Select column for histogram:', data.select_dtypes(include=['float64', 'int64']).columns)
        
        st.title(f'Distribution of {hist_column}')
        fig = px.histogram(data, x=hist_column, title=f'Distribution of {hist_column}')
        st.plotly_chart(fig)

    elif visualization_type == 'Scatter Plot':
        st.sidebar.subheader('Scatter Plot Settings')
        scatter_x = st.sidebar.radio('Select X axis for scatter plot:', data.select_dtypes(include=['float64', 'int64']).columns)
        scatter_y = st.sidebar.radio('Select Y axis for scatter plot:', data.select_dtypes(include=['float64', 'int64']).columns)
        
        st.title(f'Scatter Plot: {scatter_x} vs {scatter_y}')
        fig = px.scatter(data, x=scatter_x, y=scatter_y, title=f'Scatter Plot: {scatter_x} vs {scatter_y}')
        st.plotly_chart(fig)

    elif visualization_type == 'Box Plot':
        st.sidebar.subheader('Box Plot Settings')
        box_x = st.sidebar.radio('Select X axis for box plot:', data.select_dtypes(include=['object']).columns)
        box_y = st.sidebar.radio('Select Y axis for box plot:', data.select_dtypes(include=['float64', 'int64']).columns)
        
        st.title(f'Box Plot: {box_y} by {box_x}')
        fig = px.box(data, x=box_x, y=box_y, title=f'Box Plot: {box_y} by {box_x}')
        st.plotly_chart(fig)

    elif visualization_type == 'Pie/Donut Chart':
        st.sidebar.subheader('Pie/Donut Chart Settings')
        pie_column = st.sidebar.radio('Select column for pie/donut chart:', data.select_dtypes(include=['object']).columns)
        pie_hole = st.sidebar.slider('Select hole size for donut chart:', 0.0, 0.5, 0.4)
        
        st.title(f'Donut Chart: {pie_column}')
        fig = px.pie(data, names=pie_column, title=f'Donut Chart: {pie_column}', hole=pie_hole)
        st.plotly_chart(fig)

    elif visualization_type == 'Boxen Plot':
        st.sidebar.subheader('Boxen Plot Settings')
        boxen_x = st.sidebar.radio('Select X axis for boxen plot:', data.select_dtypes(include=['object']).columns)
        boxen_y = st.sidebar.radio('Select Y axis for boxen plot:', data.select_dtypes('number').columns)
        
        st.title(f'Boxen Plot: {boxen_y} by {boxen_x}')
        fig, ax = plt.subplots()
        sns.boxenplot(x=boxen_x, y=boxen_y, data=data, ax=ax)
        plt.xticks(rotation=90)
        st.pyplot(fig)

    elif visualization_type == 'Violin Plot':
        st.sidebar.subheader('Violin Plot Settings')
        violin_x = st.sidebar.radio('Select X axis for violin plot:', data.select_dtypes(include=['object']).columns)
        violin_y = st.sidebar.radio('Select Y axis for violin plot:', data.select_dtypes(include=['float64', 'int64']).columns)
        
        st.title(f'Violin Plot: {violin_y} by {violin_x}')
        fig, ax = plt.subplots()
        sns.violinplot(x=violin_x, y=violin_y, data=data, ax=ax)
        plt.xticks(rotation=90)
        st.pyplot(fig)

    elif visualization_type == 'Bar Plot':
        st.sidebar.subheader('Bar Plot Settings')
        bar_x = st.sidebar.radio('Select X axis for bar plot:', data.select_dtypes(include=['object']).columns)
        bar_y = st.sidebar.radio('Select Y axis for bar plot:', data.select_dtypes(include=['float64', 'int64']).columns)
        
        st.title(f'Bar Plot: {bar_y} by {bar_x}')
        fig, ax = plt.subplots()
        sns.barplot(x=bar_x, y=bar_y, data=data, ax=ax)
        plt.xticks(rotation=90)
        st.pyplot(fig)

generate_visualizations(data)
