import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
from sklearn.decomposition import PCA
import plotly.express as px
from Project import data
# # Load the dataset
# file_path = '/mnt/data/cleaned_data.csv'  # Update with the actual path to your dataset
# data = pd.read_csv(file_path)

# Define visualization functions
def plot_jointplot(data, x, y):
    fig = sns.jointplot(x=x, y=y, data=data, kind="reg", height=8)
    st.pyplot(fig)

def plot_pairplot(data, columns):
    fig = sns.pairplot(data[columns], diag_kind='kde', markers='+')
    st.pyplot(fig)

# def plot_facetgrid(data, col, x):
#     g = sns.FacetGrid(data, col=col, col_wrap=4, height=3)
#     g.map(sns.histplot, x)
#     g.add_legend()
#     st.pyplot(g)

def plot_advanced_jointplot(data, x, y, hue):
    fig = sns.jointplot(x=x, y=y, data=data, kind="scatter", hue=hue, height=8)
    st.pyplot(fig)

def plot_pca(data):
    pca = PCA(n_components=2)
    components = pca.fit_transform(data.select_dtypes(include=['float64', 'int64']).dropna())
    pca_df = pd.DataFrame(data=components, columns=['Principal Component 1', 'Principal Component 2'])
    fig = px.scatter(pca_df, x='Principal Component 1', y='Principal Component 2', title='PCA of Numerical Features')
    st.plotly_chart(fig)

# Streamlit app layout
st.sidebar.header('Visualization Settings')

# Visualization type selection
visualization_type = st.sidebar.selectbox(
    'Select Visualization Type:',
    ['Joint Plot', 'Pair Plot', 'Advanced Joint Plot', 'PCA']
)

# Column selections for the visualizations
if visualization_type == 'Joint Plot':
    x_col = st.sidebar.selectbox('Select X axis:', data.select_dtypes(include=['float64', 'int64']).columns)
    y_col = st.sidebar.selectbox('Select Y axis:', data.select_dtypes(include=['float64', 'int64']).columns)
    st.title(f'Joint Plot of {x_col} vs {y_col}')
    plot_jointplot(data, x_col, y_col)

elif visualization_type == 'Pair Plot':
    selected_cols = st.sidebar.multiselect('Select columns for pair plot:', data.select_dtypes(include=['float64', 'int64']).columns)
    if selected_cols:
        st.title('Pair Plot')
        plot_pairplot(data, selected_cols)

# elif visualization_type == 'Facet Grid':
#     col = st.sidebar.selectbox('Select column for Facet Grid:', data.select_dtypes(include=['object']).columns)
#     x_col = st.sidebar.selectbox('Select column for histogram:', data.select_dtypes(include=['float64', 'int64']).columns)
#     st.title(f'Facet Grid by {col}')
#     plot_facetgrid(data, col, x_col)

elif visualization_type == 'Advanced Joint Plot':
    x_col = st.sidebar.selectbox('Select X axis:', data.select_dtypes(include=['float64', 'int64']).columns)
    y_col = st.sidebar.selectbox('Select Y axis:', data.select_dtypes(include=['float64', 'int64']).columns)
    hue_col = st.sidebar.selectbox('Select hue:', data.select_dtypes(include=['object']).columns)
    st.title(f'Advanced Joint Plot of {x_col} vs {y_col} colored by {hue_col}')
    plot_advanced_jointplot(data, x_col, y_col, hue_col)

elif visualization_type == 'PCA':
    st.title('PCA of Numerical Features')
    plot_pca(data)
