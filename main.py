import streamlit as st
import streamlit.components.v1 as components

# 1. 스트림릿 기본 설정
st.set_page_config(page_title="MechCraft 3D Pro", layout="wide")

st.sidebar.title("🛠️ MechCraft 3D Pro")
st.sidebar.markdown("""
**[업데이트 된 기능]**
- **부품 목록:** 우측 패널에서 생성된 부품 확인
- **선택 및 편집:** 3D 화면에서 부품을 클릭하거나 목록에서 선택
- **속성 변경:** 선택한 부품의 색상 및 크기 실시간 조절
- **개별 삭제:** 원하는 부품만 선택하여 삭제 기능 추가
""")
st.sidebar.info("화면 내의 UI를 통해 모델링을 진행하세요. 마우스 좌클릭(회전), 휠(확대/축소), 우클릭(이동)이 가능합니다.")

# 2. Three.js 프론트엔드 코드 (UI 및 렌더링, Raycasting 선택 기능 포함)
three_js_code = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <style>
        body { margin: 0; overflow: hidden; background-color: #1e1e1e; font-family: 'Segoe UI', sans-serif; color: white; }
        
        /* 좌측: 부품 생성 툴바 */
        #toolbar { 
            position: absolute; top: 15px; left: 15px; z-index: 100; 
            background: rgba(30, 30, 30, 0.9); padding: 15px; 
            border-radius: 8px; border: 1px solid #444; width: 150px;
        }
        
        /* 우측: 객체 목록 및 속성 패널 */
        #right-panel {
            position: absolute; top: 15px; right: 15px; z-index: 100; 
            background: rgba(30, 30, 30, 0.9); padding: 15px; 
            border-radius: 8px; border: 1px solid #444; width: 200px;
            max-height: 90vh; overflow-y: auto;
        }

        h4 { color: #4daafc; margin: 0 0 15px 0; font-size: 14px; text-align: center; border-bottom: 1px solid #444; padding-bottom: 5px;}
        
        button { 
            width: 100%; padding: 8px; margin-bottom: 8px; 
            background: #3a3d41; color: white; border: 1px solid #555; 
            border-radius: 4px; cursor: pointer; transition: 0.2s;
        }
        button:hover { background: #505357; }
        .danger { background: #8a2a2a; border-color: #ff4c4c; }
        .danger:hover { background: #a83232; }

        /* 오브젝트 리스트 스타일 */
        #object-list { list-style: none; padding: 0; margin: 0 0 15px 0; }
        #object-list li { 
            padding: 5px; margin-bottom: 5px; background: #2a2a2a; 
            border-radius: 3px; cursor: pointer; font-size: 12px;
            border: 1px solid transparent;
        }
        #object-list li:hover { background: #3a3a3a; }
        #object-list li.active { border-color: #4daafc; background: #2c3e50; }

        /* 속성 조절 스타일 */
        .prop-group { margin-bottom: 10px; font-size: 12px; }
        .prop-group label { display: block; margin-bottom: 5px; color: #ccc; }
        .prop-group input[type="range"] { width: 100%; }
        .prop-group input[type="color"] { width: 100%; height: 30px; border: none; cursor: pointer; }
    </style>
</head>
<body>
    <!-- 좌측 패널 -->
    <div id="toolbar">
        <h4>부품 생성</h4>
        <button id="btn-cube">+ 육면체</button>
        <button id="btn-cylinder">+ 원기둥</button>
        <button id="btn-spring">+ 스프링</button>
        <button id="btn-motor">+ 모터(그룹)</button>
        <button id="btn-clear" class="danger" style="margin-top:20px;">모두 지우기</button>
    </div>

    <!-- 우측 패널 -->
    <div id="right-panel">
        <h4>오브젝트 목록</h4>
        <ul id="object-list"></ul>
        
        <div id="properties-panel" style="display: none;">
            <h4>속성 변경</h4>
            <div class="prop-group">
                <label>이름: <span id="prop-name" style="color:#fff;"></span></label>
            </div>
            <div class="prop-group">
                <label>전체 크기 (Scale)</label>
                <input type="range" id="prop-scale" min="0.1" max="5" step="0.1" value="1">
            </div>
            <div class="prop-group">
                <label>색상 (Color)</label>
                <input type="color" id="prop-color" value="#888888">
            </div>
            <button id="btn-delete" class="danger">선택 부품 삭제</button>
        </div>
    </div>
    
    <div id="canvas-container"></div>

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

        // 1. 기본 환경 설정
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x1e1e1e);
        scene.add(new THREE.GridHelper(50, 50, 0x444444, 0x222222));

        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.set(10, 10, 10);

        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.getElementById('canvas-container').appendChild(renderer.domElement);

        const controls = new OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;

        scene.add(new THREE.AmbientLight(0xffffff, 0.6));
        const dirLight = new THREE.DirectionalLight(0xffffff, 0.8);
        dirLight.position.set(20, 20, 10);
        scene.add(dirLight);

        // 2. 상태 관리 (객체 배열, 선택된 객체, 카운터)
        let objects = [];
        let selectedObject = null;
        let counts = { cube: 0, cylinder: 0, spring: 0, motor: 0 };
        
        // 선택 하이라이트용 테두리 헬퍼
        const boxHelper = new THREE.BoxHelper(new THREE.Object3D(), 0xffff00);
        scene.add(boxHelper);
        boxHelper.visible = false;

        // 3. UI 업데이트 함수
        function updateObjectList() {
            const list = document.getElementById('object-list');
            list.innerHTML = '';
            objects.forEach((obj) => {
                const li = document.createElement('li');
                li.textContent = obj.userData.name;
                if (selectedObject === obj) li.classList.add('active');
                
                // 리스트 클릭 시 객체 선택
                li.onclick = () => selectObject(obj);
                list.appendChild(li);
            });
        }

        function updatePropertiesPanel() {
            const panel = document.getElementById('properties-panel');
            if (selectedObject) {
                panel.style.display = 'block';
                document.getElementById('prop-name').textContent = selectedObject.userData.name;
                document.getElementById('prop-scale').value = selectedObject.scale.x;
                
                // 그룹(모터)인 경우 첫 번째 자식의 색상을, 단일 메쉬인 경우 본인의 색상을 표시
                if (selectedObject.isGroup) {
                    document.getElementById('prop-color').value = '#' + selectedObject.children[0].material.color.getHexString();
                } else {
                    document.getElementById('prop-color').value = '#' + selectedObject.material.color.getHexString();
                }
            } else {
                panel.style.display = 'none';
            }
        }

        function selectObject(obj) {
            selectedObject = obj;
            if (obj) {
                boxHelper.setFromObject(obj);
                boxHelper.visible = true;
            } else {
                boxHelper.visible = false;
            }
            updateObjectList();
            updatePropertiesPanel();
        }

        // 4. 객체 생성 함수들
        const randPos = () => Math.random() * 6 - 3;
        
        function createMaterial(colorHex) {
            return new THREE.MeshStandardMaterial({ color: colorHex, metalness: 0.5, roughness: 0.5 });
        }

        function addObjectToScene(mesh, type, namePrefix) {
            counts[type]++;
            mesh.userData.name = `${namePrefix}_${counts[type]}`;
            mesh.userData.isSelectable = true; // Raycaster 식별용
            mesh.position.set(randPos(), mesh.position.y || 1, randPos());
            scene.add(mesh);
            objects.push(mesh);
            updateObjectList();
            selectObject(mesh); // 생성 후 자동 선택
        }

        document.getElementById('btn-cube').onclick = () => {
            const mesh = new THREE.Mesh(new THREE.BoxGeometry(2, 2, 2), createMaterial(0x888888));
            addObjectToScene(mesh, 'cube', '육면체');
        };

        document.getElementById('btn-cylinder').onclick = () => {
            const mesh = new THREE.Mesh(new THREE.CylinderGeometry(1, 1, 4, 32), createMaterial(0x888888));
            mesh.position.y = 2;
            addObjectToScene(mesh, 'cylinder', '원기둥');
        };

        document.getElementById('btn-spring').onclick = () => {
            class SpringCurve extends THREE.Curve {
                getPoint(t, target = new THREE.Vector3()) {
                    return target.set(Math.cos(t * Math.PI * 10), t * 5, Math.sin(t * Math.PI * 10));
                }
            }
            const mesh = new THREE.Mesh(new THREE.TubeGeometry(new SpringCurve(), 100, 0.2, 8, false), createMaterial(0x4daafc));
            mesh.position.y = 0;
            addObjectToScene(mesh, 'spring', '스프링');
        };

        document.getElementById('btn-motor').onclick = () => {
            const group = new THREE.Group();
            const body = new THREE.Mesh(new THREE.CylinderGeometry(1.5, 1.5, 3, 32), createMaterial(0x888888));
            body.rotation.z = Math.PI / 2;
            const shaft = new THREE.Mesh(new THREE.CylinderGeometry(0.3, 0.3, 1, 16), createMaterial(0x4daafc));
            shaft.rotation.z = Math.PI / 2; shaft.position.x = 2;
            group.add(body); group.add(shaft);
            group.position.y = 1.5;
            addObjectToScene(group, 'motor', '모터');
        };

        // 5. 전체 삭제 및 개별 삭제
        document.getElementById('btn-clear').onclick = () => {
            objects.forEach(obj => scene.remove(obj));
            objects = [];
            counts = { cube: 0, cylinder: 0, spring: 0, motor: 0 };
            selectObject(null);
        };

        document.getElementById('btn-delete').onclick = () => {
            if (selectedObject) {
                scene.remove(selectedObject);
                objects = objects.filter(obj => obj !== selectedObject);
                selectObject(null);
            }
        };

        // 6. 속성 변경 이벤트
        document.getElementById('prop-scale').addEventListener('input', (e) => {
            if (selectedObject) {
                const s = parseFloat(e.target.value);
                selectedObject.scale.set(s, s, s);
                boxHelper.update(); // 헬퍼 테두리도 스케일에 맞게 업데이트
            }
        });

        document.getElementById('prop-color').addEventListener('input', (e) => {
            if (selectedObject) {
                const newColor = e.target.value;
                if (selectedObject.isGroup) {
                    // 그룹(모터)의 경우 모든 자식 메쉬의 색상 변경
                    selectedObject.children.forEach(child => child.material.color.set(newColor));
                } else {
                    selectedObject.material.color.set(newColor);
                }
            }
        });

        // 7. Raycaster (마우스 3D 화면 클릭 선택)
        const raycaster = new THREE.Raycaster();
        const mouse = new THREE.Vector2();

        renderer.domElement.addEventListener('pointerdown', (e) => {
            // 마우스 좌표를 -1 ~ 1 사이로 정규화
            mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
            mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;

            raycaster.setFromCamera(mouse, camera);
            // objects 배열 안의 객체들과 교차 검사 (자식 객체 포함 true)
            const intersects = raycaster.intersectObjects(objects, true);

            if (intersects.length > 0) {
                // 클릭된 메쉬가 그룹의 자식이면 부모 그룹을 선택, 아니면 메쉬 자체를 선택
                let clickedObj = intersects[0].object;
                if (clickedObj.parent && clickedObj.parent.userData.isSelectable) {
                    selectObject(clickedObj.parent);
                } else {
                    selectObject(clickedObj);
                }
            } else {
                // 빈 공간 클릭 시 선택 해제
                selectObject(null);
            }
        });

        // 8. 반응형 처리 및 애니메이션 루프
        window.addEventListener('resize', () => {
            renderer.setSize(window.innerWidth, window.innerHeight);
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
        });

        function animate() {
            requestAnimationFrame(animate);
            controls.update();
            if (boxHelper.visible && selectedObject) {
                boxHelper.update(); // 객체가 회전/이동할 때 테두리도 따라가도록 업데이트
            }
            renderer.render(scene, camera);
        }
        animate();
    </script>
</body>
</html>
"""

# 화면에 HTML 렌더링 (창 높이에 맞춰 850px 할당)
components.html(three_js_code, height=850)
