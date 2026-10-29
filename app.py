import streamlit as st
import streamlit.components.v1 as components

# 스트림릿 웹 페이지 기본 설정
st.set_page_config(page_title="MechCraft 3D", layout="wide")

st.sidebar.title("설정 메뉴")
st.sidebar.write("여기에 파이썬으로 데이터를 처리하거나")
st.sidebar.write("DB를 연결하는 버튼을 만들 수 있습니다.")

# 기존에 만든 HTML/JS 3D 화면을 스트림릿 안에 띄우기
# (참고: 실제 구동 시 CSS와 JS 코드를 HTML 안에 합치거나 정적 폴더로 라우팅해야 할 수 있습니다)
with open("index.html", "r", encoding="utf-8") as f:
    html_data = f.read()

st.title("기계 설계 프로그램 3D 뷰어")
# 3D 화면을 가로 전체 꽉 차게, 높이 800px로 렌더링
components.html(html_data, height=800)
