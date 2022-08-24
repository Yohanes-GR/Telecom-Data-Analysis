import pandas as pd
import numpy as np
import seaborn as sns 
import streamlit as st
import matplotlib.pyplot as plt
from IPython.display import Image
import plotly.express as px
import plotly.io as pio
from plotly.subplots import make_subplots
import plotly.graph_objects as go  


def hist(df:pd.DataFrame, column:str, color:str)->None:
    plt.figure(figsize=(9, 7))
    sns.displot(data=df, x=column, color=color, kde=True, height=7, aspect=2)
    plt.title(f'Distribution of {column}', size=20, fontweight='bold')
    plt.show()


def box_plot(df: pd.DataFrame, x_col: str, title: str)->None:
    plt.figure(figsize=(12, 7))
    sns.boxplot(data=df, x=x_col)
    plt.title(title, size=20)
    plt.xticks(rotation=90, fontsize=14)
    plt.show()


def plot_scatter(df: pd.DataFrame, x_col: str, y_col: str, title: str, hue: str, style: str) -> None:
    plt.figure(figsize=(10, 8))
    sns.scatterplot(data=df, x=x_col, y=y_col, hue=hue, style=style)
    plt.title(title, size=20)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.xlim(0, 10000)
    plt.ylim(0, 10000)
    plt.show()


def plot_heatmap(df: pd.DataFrame, title: str, cbar=False) -> None:
    plt.figure(figsize=(15, 12))
    sns.heatmap(df, annot=True, cmap='viridis', vmin=0,
                vmax=1, fmt='.2f', linewidths=.7, cbar=cbar)
    plt.title(title, size=18, fontweight='bold')
    plt.show()
    

def fix_outlier(df, column):
    df[column] = np.where(df[column] > df[column].quantile(0.95), df[column].mode(),df[column])
    
    return df[column]


def plot_bar(column, title, xlabel, ylabel):
    plt.figure(figsize=(10,5))
    sns.barplot(x=column.index, y=column.values) 
    plt.title(title, size=14, fontweight="bold")
    plt.xlabel(xlabel, size=13, fontweight="bold") 
    plt.ylabel(ylabel, size=13, fontweight="bold")
    plt.xticks(rotation=90)
    plt.show() 

def mult_hist(sr, rows, cols, title_text, subplot_titles, interactive=False):
    fig = make_subplots(rows=rows, cols=cols, subplot_titles=subplot_titles)
    for i in range(rows):
        for j in range(cols):
            x = ["-> " + str(i) for i in sr[i+j].index]
            fig.add_trace(go.Bar(x=x, y=sr[i+j].values), row=i+1, col=j+1)
    fig.update_layout(showlegend=False, title_text=title_text)
    if(interactive):
        fig.show()
    else:
        return Image(pio.to_image(fig, format='png', width=1200))


def plot_hist(df: pd.DataFrame, column: str, color: str) -> None:
    plt.figure(figsize=(9, 7))
    sns.displot(data=df, x=column, color=color, kde=True, height=7, aspect=2)
    plt.title(f'Distribution of {column}', size=20, fontweight='bold')
    plt.show()


def scatter2d(df, x, y, c=None, s=None, mx=None, my=None, af=None, fit=None, interactive=False):
    fig = px.scatter(df, x=x, y=y, color=c, size=s, marginal_y=my,
                     marginal_x=mx, trendline=fit, animation_frame=af)
    if(interactive):
        st.plotly_chart(fig)
    else:
        st.image(pio.to_image(fig, format='png', width=1200))


def scatter3D(df, x, y, z, c=None, s=None, mx=None, my=None, af=None, fit=None, rotation=[1, 1, 1], interactive=False):
    fig = px.scatter_3d(df, x=x, y=y, z=z, color=c, size=s,
                        animation_frame=af, size_max=18)

    fig.update_layout(scene=dict(camera=dict(eye=dict(x=rotation[0], y=rotation[1], z=rotation[2]))),
                      )
    if(interactive):
        st.plotly_chart(fig)
    else:
        st.image(pio.to_image(fig, format='png', width=1200))