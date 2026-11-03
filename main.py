import streamlit as st
import streamlit.components.v1 as components

# 1. 스트림릿 페이지 설정
st.set_page_config(page_title="MechCraft 3D Simulator", layout="wide")

st.sidebar.title("⚙️ MechCraft 3D Simulator")
st.sidebar.markdown("""
**[사용 방법]**
1. **자유 변환:** 상단 툴바에서 '✥ 이동' 또는 '↻ 회전' 선택 후 물체를 클릭하여 원하는 위치와 각도로 조절하세요.
2. **물리 엔진:** '▶ 물리 실행'을 클릭하면 중력이 켜지고, 모터가 회전하며, 물체들이 부딪힙니다.
3. **기계 장치 조립:** 모터를 허공에 배치하고 그 위에 기어나 바퀴를 올려둔 뒤 물리 실행을 해보세요.
""")

# 2. Three.js 프론트엔드 코드 (시작 """ 부터 끝 """ 까지 절대 잘리면 안 됩니다)
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
        button { padding: 8px; background: #3a3d41; color: white; border: 1px solid #555; border-radius: 4px; cursor: pointer; transition: 0.2s; width: 100%; margin-bottom: 5px; }
        button:hover { background: #505357; }
        
        .btn-top { width: auto; padding: 8px 15px; font-weight: bold; }
        .btn-play { background: #2e7d32; border-color: #4caf50; }
        .btn-play:hover { background: #388e3c; }
        .btn-stop { background: #c62828; border-color: #ef5350; }
        .btn-stop:hover { background: #d32f2f; }
        .danger { background: #8a2a2a; border-color: #ff4c4c; }
        
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
        <div id="prop-empty" style="font-size:12px; color:#aaa; text-align:center;">부품을 클릭하세요</div>
        <div id="properties-panel" style="display: none;">
            <div class="prop-group"><label>이름: <strong id="prop-name" style="color:#fff;"></strong></label></div>
            <div class="prop-group">
                <label>색상 변경</label>
                <input type="color" id="prop-color" value="#888888">
            </div>
            <button id="btn-delete" class="danger">부품 삭제</button>
        </div>
    </div>
    
    <div id="canvas-container"></div>

    <script async src="https://unpkg.com/es-module-shims@1.6.3/dist/es-module-shims.js"></script>
    <script type="importmap">
      {
        "imports": {
          "three": "https://unpkg.com/three@0.150.1/build/three.module.js",
          "three/addons/": "https://unpkg.com/three@0.150.1/examples/jsm/",
          "cannon-es": "https://cdn.jsdelivr.net/npm/cannon-es@0.20.0/dist/cannon-es.js"
        }
      }
    </script>
    
    <script type="module">
        import * as THREE from 'three';
        import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
        import { TransformControls } from 'three/addons/controls/TransformControls.js';
        import * as CANNON from 'cannon-es';

        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x1e1e1e);
        scene.add(new THREE.GridHelper(50, 50, 0x444444, 0x222222));

        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.set(10, 10, 15);

        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.shadowMap.enabled = true;
        document.getElementById('canvas-container').appendChild(renderer.domElement);

        scene.add(new THREE.AmbientLight(0xffffff, 0.4));
        const dirLight = new THREE.DirectionalLight(0xffffff, 0.8);
        dirLight.position.set(20, 20, 10);
        dirLight.castShadow = true;
        scene.add(dirLight);

        const orbitControls = new OrbitControls(camera, renderer.domElement);
        orbitControls.enableDamping = true;

        const transformControls = new TransformControls(camera, renderer.domElement);
        scene.add(transformControls);
        
        let isDragging = false;
        transformControls.addEventListener('dragging-changed', (event) => {
            orbitControls.enabled = !event.value;
            isDragging = event.value;
        });

        let physicsWorld;
        let isSimulating = false;
        let originalStates = []; 

        function initPhysics() {
            physicsWorld = new CANNON.World();
            physicsWorld.gravity.set(0, -9.82, 0);
            
            const groundBody = new CANNON.Body({
                type: CANNON.Body.STATIC,
                shape: new CANNON.Plane(),
            });
            groundBody.quaternion.setFromEuler(-Math.PI / 2, 0, 0);
            physicsWorld.addBody(groundBody);
        }

        let objects = [];
        let selectedObject = null;
        let counts = { cube: 0, cylinder: 0, motor: 0, gear: 0, wheel: 0 };
        let boxHelper = null; 

        function createMaterial(colorHex) {
            return new THREE.MeshStandardMaterial({ color: colorHex, metalness: 0.6, roughness: 0.4 });
        }

        function spawnObject(mesh, type, name) {
            counts[type]++;
            mesh.userData = { name: `${name}_${counts[type]}`, type: type, isSelectable: true };
            mesh.position.set(Math.random()*4-2, 5, Math.random()*4-2);
            mesh.castShadow = true;
            mesh.receiveShadow = true;
            scene.add(mesh);
            objects.push(mesh);
            selectObject(mesh);
        }

        document.getElementById('btn-cube').onclick = () => spawnObject(new THREE.Mesh(new THREE.BoxGeometry(2, 2, 2), createMaterial(0x888888)), 'cube', '육면체');
        document.getElementById('btn-cylinder').onclick = () => spawnObject(new THREE.Mesh(new THREE.CylinderGeometry(1, 1, 3, 32), createMaterial(0x888888)), 'cylinder', '원기둥');
        
        document.getElementById('btn-wheel').onclick = () => {
            const wheel = new THREE.Mesh(new THREE.CylinderGeometry(1.5, 1.5, 0.5, 32), createMaterial(0x333333));
            wheel.rotation.z = Math.PI / 2; 
            spawnObject(wheel, 'wheel', '바퀴');
        };

        document.getElementById('btn-motor').onclick = () => {
            const motor = new THREE.Mesh(new THREE.BoxGeometry(1.5, 1.5, 2), createMaterial(0xd32f2f));
            spawnObject(motor, 'motor', '모터');
        };

        document.getElementById('btn-gear').onclick = () => {
            const gear = new THREE.Mesh(new THREE.CylinderGeometry(2, 2, 0.5, 12), createMaterial(0x4daafc));
            spawnObject(gear, 'gear', '기어');
        };

        function selectObject(obj) {
            if (isSimulating) return; 
            selectedObject = obj;
            
            if (obj) {
                transformControls.attach(obj);
                if (!boxHelper) {
                    boxHelper = new THREE.BoxHelper(obj, 0x00ff00);
                    scene.add(boxHelper);
                } else {
                    boxHelper.setFromObject(obj);
                }
                boxHelper.visible = true;
                
                document.getElementById('prop-empty').style.display = 'none';
                document.getElementById('properties-panel').style.display = 'block';
                document.getElementById('prop-name').textContent = obj.userData.name;
                document.getElementById('prop-color').value = '#' + obj.material.color.getHexString();
            } else {
                transformControls.detach();
                if (boxHelper) boxHelper.visible = false;
                document.getElementById('prop-empty').style.display = 'block';
                document.getElementById('properties-panel').style.display = 'none';
            }
        }

        const raycaster = new THREE.Raycaster();
        const mouse = new THREE.Vector2();
        renderer.domElement.addEventListener('pointerdown', (e) => {
            if (isSimulating || isDragging) return;
            mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
            mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;
            raycaster.setFromCamera(mouse, camera);
            const intersects = raycaster.intersectObjects(objects);
            if (intersects.length > 0) selectObject(intersects[0].object);
            else selectObject(null);
        });

        document.getElementById('btn-translate').onclick = (e) => {
            transformControls.setMode('translate');
            e.target.classList.add('active-mode');
            document.getElementById('btn-rotate').classList.remove('active-mode');
        };
        document.getElementById('btn-rotate').onclick = (e) => {
            transformControls.setMode('rotate');
            e.target.classList.add('active-mode');
            document.getElementById('btn-translate').classList.remove('active-mode');
        };

        document.getElementById('prop-color').addEventListener('input', (e) => {
            if (selectedObject) selectedObject.material.color.set(e.target.value);
        });
        
        document.getElementById('btn-delete').onclick = () => {
            if (selectedObject) { scene.remove(selectedObject); objects = objects.filter(o => o !== selectedObject); selectObject(null); }
        };
        
        document.getElementById('btn-clear').onclick = () => {
            objects.forEach(obj => scene.remove(obj)); objects = []; selectObject(null);
        };

        document.getElementById('btn-play').onclick = () => {
            isSimulating = true;
            selectObject(null);
            document.getElementById('btn-play').style.display = 'none';
            document.getElementById('btn-stop').style.display = 'block';
            document.getElementById('toolbar').style.opacity = '0.5';
            document.getElementById('toolbar').style.pointerEvents = 'none';

            initPhysics();
            originalStates = [];

            objects.forEach(mesh => {
                originalStates.push({ obj: mesh, pos: mesh.position.clone(), quat: mesh.quaternion.clone() });

                mesh.geometry.computeBoundingBox();
                const size = mesh.geometry.boundingBox.getSize(new THREE.Vector3());
                
                const isMotor = mesh.userData.type === 'motor';
                const body = new CANNON.Body({
                    mass: isMotor ? 0 : 5, 
                    type: isMotor ? CANNON.Body.KINEMATIC : CANNON.Body.DYNAMIC,
                });

                if (mesh.userData.type === 'cube' || mesh.userData.type === 'motor') {
                    const shape = new CANNON.Box(new CANNON.Vec3(size.x/2, size.y/2, size.z/2));
                    body.addShape(shape);
                } else {
                    const shape = new CANNON.Cylinder(size.x/2, size.x/2, size.y, 16);
                    const q = new CANNON.Quaternion();
                    q.setFromAxisAngle(new CANNON.Vec3(1, 0, 0), -Math.PI / 2);
                    body.addShape(shape, new CANNON.Vec3(), q);
                }

                body.position.copy(mesh.position);
                body.quaternion.copy(mesh.quaternion);
                
                if (isMotor) {
                    body.angularVelocity.set(0, 5, 0); 
                }

                physicsWorld.addBody(body);
                mesh.userData.physicsBody = body;
            });
        };

        document.getElementById('btn-stop').onclick = () => {
            isSimulating = false;
            document.getElementById('btn-stop').style.display = 'none';
            document.getElementById('btn-play').style.display = 'block';
            document.getElementById('toolbar').style.opacity = '1';
            document.getElementById('toolbar').style.pointerEvents = 'auto';

            originalStates.forEach(state => {
                state.obj.position.copy(state.pos);
                state.obj.quaternion.copy(state.quat);
                delete state.obj.userData.physicsBody;
            });
            physicsWorld = null;
        };

        const clock = new THREE.Clock();
        function animate() {
            requestAnimationFrame(animate);
            orbitControls.update();
            
            if (boxHelper && boxHelper.visible && selectedObject && !isSimulating) {
                boxHelper.update();
            }

            if (isSimulating && physicsWorld) {
                const dt = clock.getDelta();
                physicsWorld.step(1 / 60, dt, 3);
                
                objects.forEach(mesh => {
                    if (mesh.userData.physicsBody) {
                        mesh.position.copy(mesh.userData.physicsBody.position);
                        mesh.quaternion.copy(mesh.userData.physicsBody.quaternion);
                    }
                });
            } else {
                clock.getDelta(); 
            }

            renderer.render(scene, camera);
        }
        animate();
    </script>
</body>
</html>
"""

# 3. Streamlit에 컴포넌트 마운트
components.html(three_js_code, height=900)
