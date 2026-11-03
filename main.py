import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="MechCraft 3D Simulator", layout="wide")

st.sidebar.title("⚙️ MechCraft 3D Simulator")
st.sidebar.markdown("""
**[핵심 업데이트 기능]**
1. **자유 변환:** 상단 툴바에서 '이동(Translate)' 또는 '회전(Rotate)' 선택 후 물체 제어
2. **물리 엔진:** '▶ 물리 실행' 클릭 시 중력, 충돌 및 기계 작동 시작
3. **기계 장치 추가:** 회전하는 모터, 맞물릴 수 있는 기어, 굴러가는 바퀴 추가
""")
st.sidebar.info("물리 실행 중에는 변환 도구가 일시 비활성화되며, 정지하면 다시 배치 모드로 돌아옵니다.")

three_js_code = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <style>
        body { margin: 0; overflow: hidden; background-color: #1e1e1e; font-family: 'Segoe UI', sans-serif; color: white; user-select: none; }
        
        /* 상단: 물리 및 변환 제어 바 */
        #top-bar {
            position: absolute; top: 15px; left: 50%; transform: translateX(-50%); z-index: 100;
            background: rgba(30, 30, 30, 0.9); padding: 10px 20px; border-radius: 8px; border: 1px solid #444;
            display: flex; gap: 10px; align-items: center;
        }
        
        /* 좌측: 부품 생성 툴바 */
        #toolbar { 
            position: absolute; top: 70px; left: 15px; z-index: 100; 
            background: rgba(30, 30, 30, 0.9); padding: 15px; border-radius: 8px; border: 1px solid #444; width: 160px;
        }
        
        /* 우측: 속성 패널 */
        #right-panel {
            position: absolute; top: 70px; right: 15px; z-index: 100; 
            background: rgba(30, 30, 30, 0.9); padding: 15px; border-radius: 8px; border: 1px solid #444; width: 200px;
        }

        h4 { color: #4daafc; margin: 0 0 10px 0; font-size: 14px; text-align: center; border-bottom: 1px solid #444; padding-bottom: 5px;}
        button { padding: 8px; background: #3a3d41; color: white; border: 1px solid #555; border-radius: 4px; cursor: pointer; transition: 0.2s; width: 100%; margin-bottom: 5px; }
        button:hover { background: #505357; }
        
        .btn-top { width: auto; padding: 8px 15px; font-weight: bold; }
        .btn-play { background: #2e7d32; border-color: #4caf50; }
        .btn-play:hover { background: #388e3c; }
        .btn-stop { background: #c62828; border-color: #ef5350; }
        .btn-stop:hover { background: #d32f2f; }
        .danger { background: #8a2a2a; border-color: #ff4c4c; }
        
        /* 활성화된 모드 버튼 스타일 */
        .active-mode { background: #4daafc; color: #000; border-color: #fff; }

        .prop-group { margin-bottom: 10px; font-size: 12px; }
        .prop-group label { display: block; margin-bottom: 5px; color: #ccc; }
        .prop-group input[type="color"] { width: 100%; height: 30px; border: none; cursor: pointer; }
    </style>
</head>
<body>
    <div id="top-bar">
        <button id="btn-translate" class="btn-top active-mode">✥ 이동</button>
        <button id="btn-rotate" class="btn-top">↻ 회전</button>
        <div style="width:20px;"></div>
        <button id="btn-play" class="btn-top btn-play">▶ 물리 실행</button>
        <button id="btn-stop" class="btn-top btn-stop" style="display:none;">⏹ 초기화</button>
    </div>

    <div id="toolbar">
        <h4>구조물</h4>
        <button id="btn-cube">+ 육면체</button>
        <button id="btn-cylinder">+ 원기둥</button>
        <h4>기계 장치</h4>
        <button id="btn-motor">+ 구동 모터</button>
        <button id="btn-gear">+ 기어(톱니)</button>
        <button id="btn-wheel">+ 바퀴</button>
        <button id="btn-clear" class="danger" style="margin-top:15px;">모두 지우기</button>
    </div>

    <div id="right-panel">
        <h4>선택된 부품</h4>
        <div id="prop
