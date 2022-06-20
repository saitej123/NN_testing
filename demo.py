from pyparsing import col
import streamlit as st
import pdf2image
import requests
import pandas as pd
import cv2
import numpy as np
from utils import format_response, write_bbox_image
from PIL import Image
import warnings
import io
warnings.filterwarnings("ignore")

def api_output(data):
    url = 'https://app.nanonets.com/api/v2/OCR/Model/8f2f2102-1389-4009-b5af-4dccc25b1329/LabelFile/?async=false'
    warnings.filterwarnings("ignore")
    response = requests.post(url, auth=requests.auth.HTTPBasicAuth('wo-nziyLTjqvdVtKVgBp2rYMPkIQ6iB4', ''), files=data, verify=False)
    return response.json()

def image_to_byte_array(image: Image) -> bytes:
    imgByteArr = io.BytesIO()
    image.save(imgByteArr, format=image.format)
    imgByteArr = imgByteArr.getvalue()
    return imgByteArr

st.set_page_config(layout = "wide")
st.markdown(
    """
    <style> [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        width: 150px; }[data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        width: 100px; margin-left: -100px; }.css-qrbaxs, .streamlit-expanderHeader{font-size: 17px
    } body { color: #fff;background-color: #4F8BF9;} </style>  """,
    unsafe_allow_html=True,
)

c1, _,_,_,_, c5 = st.columns(6)
c1.image("skense.jpg", width = 150)
c5.image("wns.png", width = 150)
st.header("Invoice API Demo")
uploaded_file = st.file_uploader('Choose your file', type=['jpg','jpeg','png','pdf'])
col1, _ , col2 = st.columns([9,1,9])


if uploaded_file is not None:
    if uploaded_file.type == "application/pdf":
        images = pdf2image.convert_from_bytes(uploaded_file.read(),poppler_path=r'.\poppler-0.68.0\bin')
        page = col1.selectbox('Select the page number', ( _ for _ in range(len(images))))
        with col1:
            st.text("")
            st.text("")
            st.image(images[page], use_column_width=True)
            images[page].save("input.jpg")
        with col2:
            
            chk= st.checkbox("Show Results")
            st.text("")
            st.text("")
            data = {'file': open("input.jpg", 'rb')}
            # data = {'file': io.BytesIO(images[page].tobytes())}

            if chk:
                output_df = format_response(api_output(data))
                output_image = st.image(write_bbox_image(images[page], output_df))
                st.text("")
                output_df.to_excel("output.xlsx",index=False)
        st.subheader('Extracted Information')
        c=st.checkbox("Show Extracted Results")
        try :

            df=pd.read_excel('output.xlsx')
        except : pass
        if c:
            st.table(df)

    else:
        with col1:
            st.image(uploaded_file, use_column_width=True)
            i=Image.open(uploaded_file).convert('RGB')
            i.save("input.jpg")

        with col2:
            chk= st.checkbox("Show Results")
            st.text("")
            st.text("")
            st.text("")
            st.text("")
            data = {'file': open("input.jpg", 'rb')}
            if chk:
                output_df = format_response(api_output(data))
                output_image = st.image(write_bbox_image(i, output_df))
                st.text("")
                output_df.to_excel("output.xlsx",index=False)
        st.subheader('Extracted Information')
        c=st.checkbox("Show Extracted Results")
        try:
             df=pd.read_excel('output.xlsx')
        except :pass
        if c:
           st.table(df)




