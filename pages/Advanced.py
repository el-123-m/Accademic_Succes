import pandas as pd
import seaborn as sns
import streamlit as st
from sklearn.decomposition import PCA
import plotly.express as px
from Main_Menu import data

def plot_jointplot(data, x, y, width, height):
    fig = sns.jointplot(x=x, y=y, data=data, kind="hex", height=height/100)
    st.pyplot(fig)

def plot_pairplot(data, columns, width, height):
    fig = sns.pairplot(data[columns], diag_kind='kde', markers='+', height=height/100)
    st.pyplot(fig)

def plot_advanced_jointplot(data, x, y, hue, width, height):
    fig = sns.jointplot(x=x, y=y, data=data, kind="scatter", hue=hue, height=height/100)
    fig = fig.plot_joint(sns.kdeplot)
    fig = fig.plot_marginals(sns.kdeplot, shade=True)
    st.pyplot(fig)

def plot_pca(data, width, height):
    pca = PCA(n_components=2)
    components = pca.fit_transform(data.select_dtypes(include=['float64', 'int64']).dropna())
    pca_df = pd.DataFrame(data=components, columns=['Principal Component 1', 'Principal Component 2'])
    fig = px.scatter(pca_df, x='Principal Component 1', y='Principal Component 2', title='PCA of Numerical Features', width=width, height=height)
    st.plotly_chart(fig)

st.sidebar.header('Visualization Settings')

width = st.sidebar.slider('Select plot width (pixels):', 400, 1600, 800)
height = st.sidebar.slider('Select plot height (pixels):', 300, 1200, 600)

visualization_type = st.sidebar.selectbox(
    'Select Visualization Type:',
    ['Joint Plot', 'Pair Plot', 'Advanced Joint Plot', 'PCA']
)

if visualization_type == 'Joint Plot':
    x_col = st.sidebar.selectbox('Select X axis:', data.select_dtypes(include=['float64', 'int64']).columns)
    y_col = st.sidebar.selectbox('Select Y axis:', data.select_dtypes(include=['float64', 'int64']).columns)
    st.title(f'Joint Plot of {x_col} vs {y_col}')
    plot_jointplot(data, x_col, y_col, width, height)

elif visualization_type == 'Pair Plot':
    selected_cols = st.sidebar.multiselect('Select columns for pair plot:', data.select_dtypes(include=['float64', 'int64']).columns)
    if selected_cols:
        st.title('Pair Plot')
        plot_pairplot(data, selected_cols, width, height)

elif visualization_type == 'Advanced Joint Plot':
    x_col = st.sidebar.selectbox('Select X axis:', data.select_dtypes(include=['float64', 'int64']).columns)
    y_col = st.sidebar.selectbox('Select Y axis:', data.select_dtypes(include=['float64', 'int64']).columns)
    hue_col = st.sidebar.selectbox('Select hue:', data.select_dtypes('object').columns)
    st.title(f'Advanced Joint Plot of {x_col} vs {y_col} colored by {hue_col}')
    plot_advanced_jointplot(data, x_col, y_col, hue_col, width, height)

elif visualization_type == 'PCA':
    st.title('PCA of Numerical Features')
    plot_pca(data, width, height)
