import streamlit as st
import streamlit.components.v1 as components

# 스트림릿 페이지 설정
st.set_page_config(page_title="MechCraft 3D Simulator", layout="wide")

st.sidebar.title("⚙️ MechCraft 3D Simulator")
st.sidebar.markdown("""
**[사용 방법]**
1. **자유 변환:** 상단 툴바에서 '✥ 이동' 또는 '↻ 회전' 선택 후 물체를 클릭하여 원하는 위치와 각도로 조절하세요.
2. **물리 엔진:** '▶ 물리 실행'을 클릭하면 중력이 켜지고, 모터가 회전하며, 물체들이 부딪힙니다.
3. **기계 장치 조립:** 모터를 허공에 배치하고 그 위에 기어나 바퀴를 올려둔 뒤 물리 실행을 해보세요.
""")
st.sidebar.info("✔ 백지 화면 버그 및 물리엔진 충돌 오류가 해결된 안정화 버전입니다.")

# Three.js 프론트엔드 코드
three_js_code = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <style>
        body { margin: 0; overflow: hidden; background-color: #1e1e1e; font-family: 'Segoe UI', sans-serif; color: white; user-select: none; }
        
        #top-bar {
            position: absolute; top: 15px; left: 50%; transform: translateX(-50%); z-index: 100;
            background: rgba(30, 30, 30, 0.9); padding: 10px 20px; border-radius: 8px; border: 1px solid #444;
            display: flex; gap: 10px; align-items: center;
        }
        
        #toolbar { 
            position: absolute; top: 70px; left: 15px; z-index: 100; 
            background: rgba(30, 30, 30, 0.9); padding: 15px; border-radius: 8px; border: 1px solid #444; width: 160px;
        }
        
        #right-panel {
            position: absolute; top: 70px; right: 15px; z-index: 100; 
            background: rgba(30, 30, 30, 0.9); padding: 15px; border-radius: 8px; border: 1px solid #444; width: 200px;
        }

        h4 { color: #4daafc; margin: 0 0 10px 0; font-size: 14px; text-align: center; border-bottom: 1px solid #444; padding-bottom: 5px;}
        button { padding: 8px; background: #3a3d41; color: white; border:
