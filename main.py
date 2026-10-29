import streamlit as st
import streamlit.components.v1 as components

# 1. 스트림릿 페이지 기본 설정 (전체 화면 사용)
st.set_page_config(page_title="3D 기계 설계 프로그램", layout="wide")

# 2. 스트림릿 사이드바 (프로젝트 관리용 메뉴)
st.sidebar.title("🛠️ 기계 설계 메뉴")
st.sidebar.write("이곳은 파이썬으로 동작하는 영역입니다.")
st.sidebar.button("프로젝트 저장 (준비중)")
st.sidebar.button("설계 데이터 내보내기 (준비중)")
st.sidebar.info("3D 화면 내의 버튼을 눌러 부품을 생성하고, 마우스로 화면을 돌려보세요.")

st.title("⚙️ 웹 기반 3D 기계 설계 뷰어")
st.write("마우스 **왼쪽 클릭**으로 회전, **휠**로 확대/축소, **오른쪽 클릭**으로 화면을 이동할 수 있습니다.")

# 3. 3D 뷰어 핵심 코드 (Three.js를 이용한 HTML/JS 코드를 통합)
three_js_code = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <style>
        body { margin: 0; overflow: hidden; background-color: #1e1e1e; font-family: sans-serif; }
        /* 3D 화면 내부의 자체 부품 생성 툴바 */
        #toolbar { 
            position: absolute; top: 15px; left: 15px; z-index: 100; 
            background: rgba(40, 40, 40, 0.9); padding: 15px; 
            border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.5);
            width: 150px;
        }
        h4 { color: #4daafc; margin-top: 0; margin-bottom: 15px; font-size: 14px; text-align: center; }
        button { 
            width: 100%; padding: 8px; margin-bottom: 8px; 
            background: #3a3d41; color: white; border: 1px solid #555; 
            border-radius: 4px; cursor: pointer; transition: 0.2s;
        }
        button:hover { background: #505357; }
        .danger { background: #8a2a2a; border-color: #ff4c4c; margin-top: 10px; }
        .danger:hover { background: #a83232; }
    </style>
</head>
<body>
    <div id="toolbar">
        <h4>부품 생성</h4>
        <button id="btn-cube">+ 육면체</button>
        <button id="btn-cylinder">+ 원기둥</button>
        <button id="btn-spring">+ 스프링</button>
        <button id="btn-motor">+ 모터</button>
        <button id="btn-clear" class="danger">모두 지우기</button>
    </div>
    
    <div id="canvas-container"></div>

    <!-- Three.js 라이브러리 로드 -->
    <script async src="https://unpkg.com/es-module-shims@1.6.3/dist/es-module-shims.js"></script>
    <script type="importmap">
      {
        "imports": {
          "three": "https://unpkg.com/three@0.150.1/build/three.module.js",
          "three/addons/": "https://unpkg.com/three@0.150.1/examples/jsm/"
        }
      }
    </script>
    
    <script type="module">
        import * as THREE from 'three';
        import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

        // 씬, 카메라, 렌더러 초기화
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x1e1e1e);
        scene.add(new THREE.GridHelper(50, 50, 0x444444, 0x222222));

        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.set(10, 10, 10);

        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.getElementById('canvas-container').appendChild(renderer.domElement);

        // 마우스 컨트롤
        const controls = new OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;

        // 조명
        scene.add(new THREE.AmbientLight(0xffffff, 0.6));
        const dirLight = new THREE.DirectionalLight(0xffffff, 0.8);
        dirLight.position.set(20, 20, 10);
        scene.add(dirLight);

        // 부품 리스트 및 재질
        let objects = [];
        const matBase = new THREE.MeshStandardMaterial({ color: 0x888888, metalness: 0.5, roughness: 0.5 });
        const matAccent = new THREE.MeshStandardMaterial({ color: 0x4daafc, metalness: 0.7, roughness: 0.2 });

        // 생성 위치를 겹치지 않게 약간씩 흩뿌리기 위한 함수
        const randPos = () => Math.random() * 6 - 3;

        function addCube() {
            const mesh = new THREE.Mesh(new THREE.BoxGeometry(2, 2, 2), matBase);
            mesh.position.set(randPos(), 1, randPos());
            scene.add(mesh); objects.push(mesh);
        }

        function addCylinder() {
            const mesh = new THREE.Mesh(new THREE.CylinderGeometry(1, 1, 4, 32), matBase);
            mesh.position.set(randPos(), 2, randPos());
            scene.add(mesh); objects.push(mesh);
        }

        function addSpring() {
            class SpringCurve extends THREE.Curve {
                getPoint(t, target = new THREE.Vector3()) {
                    return target.set(Math.cos(t * Math.PI * 10), t * 5, Math.sin(t * Math.PI * 10));
                }
            }
            const mesh = new THREE.Mesh(new THREE.TubeGeometry(new SpringCurve(), 100, 0.2, 8, false), matAccent);
            mesh.position.set(randPos(), 0, randPos());
            scene.add(mesh); objects.push(mesh);
        }

        function addMotor() {
            const group = new THREE.Group();
            const body = new THREE.Mesh(new THREE.CylinderGeometry(1.5, 1.5, 3, 32), matBase);
            body.rotation.z = Math.PI / 2;
            const shaft = new THREE.Mesh(new THREE.CylinderGeometry(0.3, 0.3, 1, 16), matAccent);
            shaft.rotation.z = Math.PI / 2; shaft.position.x = 2;
            group.add(body); group.add(shaft);
            group.position.set(randPos(), 1.5, randPos());
            scene.add(group); objects.push(group);
        }

        // 버튼 이벤트 연결
        document.getElementById('btn-cube').onclick = addCube;
        document.getElementById('btn-cylinder').onclick = addCylinder;
        document.getElementById('btn-spring').onclick = addSpring;
        document.getElementById('btn-motor').onclick = addMotor;
        document.getElementById('btn-clear').onclick = () => {
            objects.forEach(obj => scene.remove(obj));
            objects = [];
        };

        // 창 크기 조절 대응
        window.addEventListener('resize', () => {
            renderer.setSize(window.innerWidth, window.innerHeight);
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
        });

        // 렌더링 루프
        function animate() {
            requestAnimationFrame(animate);
            controls.update();
            renderer.render(scene, camera);
        }
        animate();
    </script>
</body>
</html>
"""

# 4. Streamlit 화면에 Three.js 3D 화면을 임베딩 (높이 700 픽셀 지정)
components.html(three_js_code, height=700)
