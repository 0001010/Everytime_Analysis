import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import datetime
from collections import Counter
from wordcloud import WordCloud
from matplotlib import font_manager, rc
from gensim.models import KeyedVectors
import warnings
warnings.filterwarnings(action='ignore')

st.set_option('deprecation.showPyplotGlobalUse', False)
st.set_page_config(layout="wide")
st.title('에브리타임 분석')

# 웹 페이지 col 수
col1, col2, col3 = st.beta_columns(3)

@st.cache(allow_output_mutation=True)

# 데이터 로드 함수
def load_data(nrows):
    data = pd.read_excel('C:/Users/User/everytime crawing main.xlsx', header=None)
    data.rename(columns={
        0: 'vote', 1: 'text', 2: 'date', 3: 'board'
    }, inplace=True)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    return data

# 워드 카운트 함수
def counter_word(input_data):
    word = []
    input_data.dropna(inplace = True)

    for i in input_data:
        word.append(i.split())
    word = sum(word, [])
    word_count = Counter(word)
    return word_count

# 워드 클라우드 함수
def word_cloud(word_count):
    font_location = 'C:/Windows/Fonts/malgun.ttf'
    font_name = font_manager.FontProperties(fname=font_location).get_name()
    rc('font', family=font_name)

    f, ax = plt.subplots(figsize=(3,3))

    wc = WordCloud(font_path='C:/Windows/Fonts/malgun.ttf',
                   background_color='white',
                   width=300,
                   height=150,
                   max_words=100,
                   max_font_size=750,
                   random_state=123).generate_from_frequencies(word_count)
    plt.imshow(wc)
    plt.axis("off")
    plt.show()
    st.pyplot()

# 에브리타임 데이터 로드
data_pre = pd.read_csv('C:/Users/User/et_pre.csv')
data_pre_2 = data_pre.dropna()

# col1에 대한 내용
with col1:
    data_load_state = st.text('Loading data...')
    data = load_data(10000)
    data_load_state.text("Done! (using st.cache)")

    if st.checkbox('Show raw data'):
        st.subheader('Raw data')
        st.write(data)

    # Word2Vec + 예외처리

    st.subheader('Word To Vec')
    values = st.text_input('Word To Vec 단어를 입력해주세요')

    while True:
        try:
            embedding_model = KeyedVectors.load_word2vec_format('everytime_wtv')
            sim = embedding_model.most_similar(positive=[values])
            sim = pd.DataFrame(sim).rename(columns={
                0: 'Word',
                1: 'Similar'
            })

            fig = px.bar(sim, x='Similar', y='Word', orientation='h')
            fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                              marker_line_width=1.5, opacity=0.6)
            fig.update_layout(yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig)
            break

        except KeyError:
            st.write('에브리타임에 단어가 없습니다. 다시 입력해주세요')
            break

# col2에 대한 내용
with col2:
    st.subheader('시간에 따른 HOT게시글 건수')

    # 시간에 따른 핫 게시글 dataframe
    data_pre_count = data_pre['date'].value_counts().to_frame().reset_index().rename(columns = {
        'index' : 'date',
        'date' : 'count'
    }).sort_values(by = 'date')

    # yyyy,mm,dd로 변환후 ploting
    format = 'MMM DD, YYYY'
    start_date = datetime.date(year = int(min(data_pre_count['date'])[:4]), month = int(min(data_pre_count['date'])[5:7]), day = int(min(data_pre_count['date'])[8:]))
    end_date = datetime.date(year = int(max(data_pre_count['date'])[:4]), month = int(max(data_pre_count['date'])[5:7]), day = int(max(data_pre_count['date'])[8:]))
    max_days = end_date - start_date
    hour_to_filter = st.slider('Select date', min_value=start_date, value=end_date ,max_value=end_date, format=format)

    st.write(hour_to_filter)

    hour_to_filter_str = str(hour_to_filter)
    data_filltered = data_pre_count[data_pre_count['date']<=hour_to_filter_str]
    fig = px.line(data_filltered,
                x='date',
                y='count')
    st.plotly_chart(fig)

# col3에 대한 내용
with col3:
    # 핫게시판 비율
    st.subheader('HOT게시글 중 게시판 비율')
    data_pre_ratio = data_pre['board'].value_counts(normalize = True).to_frame().reset_index().rename(columns = {
        'index' : 'board',
        'board' : 'ratio'
    })
    fig2 = px.bar(data_pre_ratio,
                  x='board',
                  y='ratio')

    st.plotly_chart(fig2)

    # 게시판별 워드클라우드
    option = st.selectbox('Please select in selectbox!',
                          tuple(data_pre['board'].unique()))

    st.write('You selected:', option)

    data_filltered2 = data_pre[data_pre['board']==option]
    word_count = counter_word(data_filltered2['text'])
    word_cloud(word_count)