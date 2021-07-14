import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import datetime
from dateutil.relativedelta import relativedelta

import warnings
warnings.filterwarnings(action='ignore')

st.title('에브리타임 분석')


col1, col2, col3 = st.beta_columns(3)
#add_selectbox = st.sidebar.selectbox("왼쪽 사이드바 Select Box", ("A", "B", "C"))

@st.cache(allow_output_mutation=True)


def load_data(nrows):
    data = pd.read_excel('C:/Users/User/everytime crawing main.xlsx', header=None)
    data.rename(columns={
        0: 'vote', 1: 'text', 2: 'date', 3: 'board'
    }, inplace=True)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    return data

with col1:
    data_load_state = st.text('Loading data...')
    data = load_data(10000)
    data_load_state.text("Done! (using st.cache)")


    if st.checkbox('Show raw data'):
        st.subheader('Raw data')
        st.write(data)


data_pre = pd.read_csv('C:/Users/User/et_pre.csv')
with col2:
    st.subheader('시간에 따른 HOT게시글 건수')
    data_pre_count = data_pre['date'].value_counts().to_frame().reset_index().rename(columns = {
        'index' : 'date',
        'date' : 'count'
    }).sort_values(by = 'date')

    fig = px.line(data_pre_count,
                x='date',
                y='count')
    st.plotly_chart(fig)
    format = 'MMM DD, YYYY'
    start_date = datetime.date(year=int(min(data_pre_count['date'])[:4]), month=int(min(data_pre_count['date'])[5:7]), day=int(min(data_pre_count['date'])[8:]))
    end_date = date time.date(year=int(max(data_pre_count['date'])[:4]), month=int(max(data_pre_count['date'])[5:7]), day=int(max(data_pre_count['date'])[8:]))
    max_days = end_date - start_date
    hour_to_filter = st.slider('Select date', min_value=start_date, value=end_date ,max_value=end_date, format=format)

    st.write(hour_to_filter)

with col3:
    st.subheader('HOT게시글 중 게시판 비율')
    data_pre_ratio = data_pre['board'].value_counts(normalize = True).to_frame().reset_index().rename(columns = {
        'index' : 'board' ,
        'board' : 'ratio'
    })
    fig2 = px.bar(data_pre_ratio,
                  x='board',
                  y='ratio')
    st.plotly_chart(fig2)



#hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0, 24))[0]
#st.bar_chart(hist_values)



#filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

#st.subheader('Map of all pickups at %s:00' % hour_to_filter)
#st.map(filtered_data)