import streamlit as st
import pandas as pd
import glob
import base64
from PIL import Image
from io import BytesIO
import os
import re
import io

st.set_page_config(layout="wide")

#if 'df' not in st.session_state:
#    st.session_state.df = pd.DataFrame(data=pd.read_csv("data/data.csv"))

proj_csv = 'makerepo-pages-data.csv'

def update(edf):
    edf.to_csv(proj_csv, index=False)
    load_df.clear()

@st.cache_data(ttl='1d')
def load_df():
    new_df = pd.read_csv(proj_csv)
    new_df['Desc'] = new_df['Desc'].replace("No desc", None)
    return new_df

#df = pd.read_csv('makerepo-pages-data.csv')
#df = df.drop(columns=[df.columns[0]], axis=1)
#df['Desc'] = df['Desc'].replace("No desc", None)

#df['img'] = df['img'].apply(lambda st: st[st.find('*src="')+1:st.find('"*')])

#st.title("Maker Repo Projects")

df = load_df()
s = io.StringIO()

col1, col2, col3, col4 = st.columns(4)

with col1:
    img_only = st.checkbox("Images Only")
with col2:
    desc_only = st.checkbox("Descriptions Only")
with col3:
    tags_only = st.checkbox("Tags Only")

if img_only:
    df = df.dropna(subset="img")
if desc_only:
    df = df.dropna(subset="Desc")
if tags_only:
    df = df.dropna(subset="tags")
    #df = df.drop(df[df['img'] == None].index)

edf = st.data_editor(
    df,
    height=500,
    use_container_width=True,
    column_config={
        "Url": st.column_config.LinkColumn(
            "Link", 
            display_text="🔗",
            width="small"
        ),
        "Title": "Project Title",
        "Date": st.column_config.TextColumn(
            "Date Added", width="small"
        ),
        "Desc": st.column_config.TextColumn(
            "Description", width="large"
        ),
        "img": st.column_config.ImageColumn(
            "Image", help="The main project image.",
            width="small"
        ),
        "tags": st.column_config.TextColumn(
            "Tags"#, width="medium"
        ),
    },
    disabled=["Url", "Title", "Desc", "img", "tags"],
    column_order=("Url", "Candidate", "Title", "Desc", "img", "tags"),
    hide_index=True,
)

def get_df_string():
    edf.to_csv(s)

col4, col5, col6 = st.columns(3)
#tags_no_nans = [x for x in list(df['unique_tags']) if x != 'nan']
tags_no_nans = [x for x in list(df['unique_tags']) if type(x) != float] #list(df['unique_tags'])#.remove(None)[x for x in list(df['unique_tags']) if x is not None]
#print(type(tags_no_nans[200]))

with col4:
    st.write("Project Count: " + str(len(df)))

with col6:
    st.write(str(tags_no_nans))

