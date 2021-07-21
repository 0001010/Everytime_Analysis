# 👩🏼‍🤝‍🧑🏻 Everytime_Analysis
 
## 에브리타임 커뮤니티의 핫게시판을 크롤링하여 분석
- 학교마다 커뮤니티가 다르므로 재학중인 순천향대학교 커뮤니티의 핫게시판을 크롤링
   - sub_crawling과 main_crawling으로 나뉨
   - 데이터 2020.10.04 ~ 2021.03.04
- 크롤링후 텍스트를 전저리, 모델링
   - word2vec을 활용해서 검색 단어와 비슷한 위치에 있는 단어를 도출
- Streamlit을 활용해서 Dashboard제작(main.py)


![](./image/everytime_dash.gif)

### ✔추가 & 수정사항
- 실시간 크롤링과 클라우드 연결
- 실시간에 맞춘 word2vec 모델 업데이트