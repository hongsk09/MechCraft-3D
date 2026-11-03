import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="MechCraft 3D Simulator", layout="wide")

st.sidebar.title("⚙️ MechCraft 3D Simulator")
st.sidebar.markdown("""
**[🔧 주요 업데이트]**
1. **사실적인 부품:** 모터가 [몸체+회전축]으로 분리되었고, 기어에 실제 톱니가 생겼습니다.
2. **크기 조절:** 우측 패널에서 물체의 크기를 마음대로 줄이고 키울 수 있습니다.
3. **결합(Attach) 기능:** 물체를 선택하고 `🔗결합`을 누른 뒤, 다른 물체(예: 모터)를 클릭하면 단단히 조립되어 함께 움직입니다.
""")

three_js_code = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <style>
        body { margin: 0; overflow: hidden; background-color: #1a1a1a; font-family: 'Segoe UI', sans-serif; color: white; user-select: none; }
        
        #top-bar { position: absolute; top: 15px; left: 50%; transform: translateX(-50%); z-index: 100; background: rgba(30, 30, 30, 0.9); padding: 10px 20px; border-radius: 8px; border: 1px solid #444; display: flex; gap: 10px; align-items: center; box-shadow: 0 4px 10px rgba(0,0,0,0.5); }
        #toolbar { position: absolute; top: 70px; left: 15px; z-index: 100; background: rgba(30, 30, 30, 0.9); padding: 15px; border-radius: 8px; border: 1px solid #444; width: 160px; box-shadow: 0 4px 10px rgba(0,0,0,0.5); }
        #right-panel { position: absolute; top: 70px; right: 15px; z-index: 100; background: rgba(30, 30, 30, 0.9); padding: 15px; border-radius: 8px; border: 1px solid #444; width: 220px; box-shadow: 0 4px 10px rgba(0,0,0,0.5); }

        h4 { color: #4daafc; margin: 0 0 10px 0; font-size: 14px; text-align: center; border-bottom: 1px solid #444; padding-bottom: 5px;}
        button { padding: 8px; background: #3a3d41; color: white; border: 1px solid #555; border-radius: 4px; cursor: pointer; transition: 0.2s; width: 100%; margin-bottom: 5px; font-weight: bold; }
        button:hover { background: #505357; }
        
        .btn-top { width: auto; padding: 8px 15px; }
        .btn-play { background: #2e7d32; border-color: #4caf50; }
        .btn-play:hover { background: #388e3c; }
        .btn-stop { background: #c62828; border-color: #ef5350; }
        .btn-stop:hover { background: #d32f2f; }
        .btn-attach { background: #d35400; border-color: #e67e22; }
        .btn-attach:hover { background: #e67e22; }
        .danger { background: #8a2a2a; border-color: #ff4c4c; }
        
        .active-mode { background: #4daafc; color: #000; border-color: #fff; }

        .prop-group { margin-bottom: 15px; font-size: 12px; }
        .prop-group label { display: block; margin-bottom: 5px; color: #ccc; }
        .prop-group input[type="color"] { width: 100%; height: 30px; border: none; cursor: pointer; border-radius:4px; }
        .prop-group input[type="range"] { width: 100%; cursor: pointer; }
    </style>
</head>
<body>
    <div id="top-bar">
        <button id="btn-translate" class="btn-top active-mode">✥ 이동</button>
        <button id="btn-rotate" class="btn-top">↻ 회전</button>
        <div style="width:20px;"></div>
        <button id="btn-play" class="btn-top btn-play">▶ 물리 실행</button>
        <button id="btn-stop" class="btn-top btn-stop" style="display:none;">⏹ 정지 및 초기화</button>
    </div>

    <div id="toolbar">
        <h4>구조물</h4>
        <button id="btn-cube">+ 육면체</button>
        <button id="btn-cylinder">+ 원기둥</button>
        <h4>기계 장치</h4>
        <button id="btn-motor">+ 구동 모터</button>
        <button id="btn-gear">+ 톱니 기어</button>
        <button id="btn-wheel">+ 고무 바퀴</button>
        <button id="btn-clear" class="danger" style="margin-top:20px;">모두 지우기</button>
    </div>

    <div id="right-panel">
        <h4>선택된 부품 속성</h4>
        <div id="prop-empty" style="font-size:12px; color:#aaa; text-align:center;">부품을 클릭하세요</div>
        <div id="properties-panel" style="display: none;">
            <div class="prop-group"><label>이름: <strong id="prop-name" style="color:#fff;"></strong></label></div>
            
            <div class="prop-group">
                <label>크기 조절 (Scale)</label>
                <input type="range" id="prop-scale" min="0.2" max="4" step="0.1" value="1">
            </div>

            <div class="prop-group">
                <label>색상 변경</label>
                <input type="color" id="prop-color" value="#888888">
            </div>

            <button id="btn-attach" class="btn-attach">🔗 다른 부품에 결합</button>
            <div id="attach-hint" style="display:none; color:#f39c12; font-size:11px; margin-bottom:10px; text-align:center; background:#442; padding:5px; border-radius:4px;">결합할 대상을 3D화면에서 클릭하세요!</div>
            
            <button id="btn-delete" class="danger" style="margin-top:10px;">이 부품 삭제</button>
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

        // 1. Scene 설정 (좀 더 부드럽고 금속 질감이 잘 보이도록 조명 강화)
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x1a1a1a);
        scene.add(new THREE.GridHelper(100, 100, 0x555555, 0x222222));

        const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.set(15, 15, 20);

        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.shadowMap.enabled = true;
        renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        document.getElementById('canvas-container').appendChild(renderer.domElement);

        scene.add(new THREE.AmbientLight(0xffffff, 0.5));
        const hemiLight = new THREE.HemisphereLight(0xffffff, 0x444444, 0.6);
        scene.add(hemiLight);
        const dirLight = new THREE.DirectionalLight(0xffffff, 1.2);
        dirLight.position.set(20, 30, 10);
        dirLight.castShadow = true;
        scene.add(dirLight);

        // 2. 컨트롤 (Orbit & Transform)
        const orbitControls = new OrbitControls(camera, renderer.domElement);
        orbitControls.enableDamping = true;

        const transformControls = new TransformControls(camera, renderer.domElement);
        scene.add(transformControls);
        let isDragging = false;
        transformControls.addEventListener('dragging-changed', (event) => {
            orbitControls.enabled = !event.value;
            isDragging = event.value;
        });

        // 3. 물리 엔진
        let physicsWorld;
        let isSimulating = false;
        let originalStates = []; 
        let physicsBodiesMap = new Map(); // Three.js Mesh와 Cannon.js Body 맵핑

        function initPhysics() {
            physicsWorld = new CANNON.World();
            physicsWorld.gravity.set(0, -9.82, 0);
            const groundMat = new CANNON.Material();
            const groundBody = new CANNON.Body({ type: CANNON.Body.STATIC, shape: new CANNON.Plane(), material: groundMat });
            groundBody.quaternion.setFromEuler(-Math.PI / 2, 0, 0);
            physicsWorld.addBody(groundBody);
        }

        // 4. 머티리얼 및 오브젝트 팩토리 (사실적인 질감)
        let objects = [];
        let selectedObject = null;
        let counts = { cube: 0, cylinder: 0, motor: 0, gear: 0, wheel: 0 };
        let boxHelper = null; 
        
        const matSteel = new THREE.MeshStandardMaterial({ color: 0xaaaaaa, metalness: 0.8, roughness: 0.3 });
        const matRedPaint = new THREE.MeshStandardMaterial({ color: 0xc0392b, metalness: 0.5, roughness: 0.6 });
        const matRubber = new THREE.MeshStandardMaterial({ color: 0x222222, metalness: 0.1, roughness: 0.9 });
        const matBrass = new THREE.MeshStandardMaterial({ color: 0xf1c40f, metalness: 0.7, roughness: 0.4 });

        function registerObject(mesh, type, name) {
            counts[type]++;
            mesh.userData = { name: `${name}_${counts[type]}`, type: type };
            mesh.position.set(Math.random()*4-2, 5, Math.random()*4-2);
            scene.add(mesh);
            objects.push(mesh);
            selectObject(mesh);
        }

        // 일반 도형
        document.getElementById('btn-cube').onclick = () => {
            const mesh = new THREE.Mesh(new THREE.BoxGeometry(2, 2, 2), matSteel.clone());
            mesh.castShadow = true; mesh.receiveShadow = true;
            registerObject(mesh, 'cube', '육면체');
        };
        document.getElementById('btn-cylinder').onclick = () => {
            const mesh = new THREE.Mesh(new THREE.CylinderGeometry(1, 1, 3, 32), matSteel.clone());
            mesh.castShadow = true; mesh.receiveShadow = true;
            registerObject(mesh, 'cylinder', '원기둥');
        };

        // 사실적 기계 부품 - 바퀴
        document.getElementById('btn-wheel').onclick = () => {
            const group = new THREE.Group();
            const tire = new THREE.Mesh(new THREE.TorusGeometry(1.2, 0.4, 16, 32), matRubber.clone());
            const rim = new THREE.Mesh(new THREE.CylinderGeometry(1.2, 1.2, 0.5, 32), matSteel.clone());
            rim.rotation.x = Math.PI / 2;
            group.add(tire, rim);
            group.castShadow = true;
            registerObject(group, 'wheel', '바퀴');
        };

        // 사실적 기계 부품 - 모터 (몸체 + 회전축 분리)
        document.getElementById('btn-motor').onclick = () => {
            const motor = new THREE.Group();
            const base = new THREE.Mesh(new THREE.BoxGeometry(2, 2, 3), matRedPaint.clone());
            const shaft = new THREE.Mesh(new THREE.CylinderGeometry(0.4, 0.4, 1.5, 16), matSteel.clone());
            shaft.rotation.x = Math.PI / 2;
            shaft.position.z = 2.0; // 앞쪽으로 돌출
            motor.add(base, shaft);
            motor.userData.shaft = shaft; // 회전축 데이터 저장 (결합 시 사용)
            registerObject(motor, 'motor', '모터');
        };

        // 사실적 기계 부품 - 톱니 기어 (ExtrudeGeometry)
        document.getElementById('btn-gear').onclick = () => {
            const shape = new THREE.Shape();
            const outerR = 2.0, innerR = 1.5, teeth = 12;
            for (let i = 0; i < teeth * 2; i++) {
                const r = i % 2 === 0 ? outerR : innerR;
                const a = (i / (teeth * 2)) * Math.PI * 2;
                if (i === 0) shape.moveTo(Math.cos(a)*r, Math.sin(a)*r);
                else shape.lineTo(Math.cos(a)*r, Math.sin(a)*r);
            }
            const geo = new THREE.ExtrudeGeometry(shape, { depth: 0.5, bevelEnabled: true, bevelSegments: 2, steps: 1, bevelSize: 0.1, bevelThickness: 0.1 });
            geo.center();
            const gear = new THREE.Mesh(geo, matBrass.clone());
            gear.castShadow = true;
            registerObject(gear, 'gear', '기어');
        };

        // 5. UI 및 결합(Attach) 로직
        let isAttachingMode = false;

        function selectObject(obj) {
            if (isSimulating) return; 
            selectedObject = obj;
            if (obj) {
                transformControls.attach(obj);
                if (!boxHelper) {
                    boxHelper = new THREE.BoxHelper(obj, 0x00ff00);
                    scene.add(boxHelper);
                } else boxHelper.setFromObject(obj);
                boxHelper.visible = true;
                
                document.getElementById('prop-empty').style.display = 'none';
                document.getElementById('properties-panel').style.display = 'block';
                document.getElementById('prop-name').textContent = obj.userData.name;
                document.getElementById('prop-scale').value = obj.scale.x;
                
                let matTarget = obj.isGroup ? obj.children[0] : obj;
                document.getElementById('prop-color').value = '#' + matTarget.material.color.getHexString();
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
            
            // 광선 추적 시 모든 부품 검사
            const intersects = raycaster.intersectObjects(objects, true);
            
            if (intersects.length > 0) {
                // 클릭된 메쉬의 가장 최상위 부모(root object)를 찾음
                let target = intersects[0].object;
                while (target.parent && target.parent !== scene && !target.userData.name && target.parent.type !== 'Scene') {
                    target = target.parent;
                }

                if (isAttachingMode) {
                    // 결합 로직: 선택된 객체를 클릭한 대상(Target)에 자식으로 넣음
                    if (target !== selectedObject) {
                        if (target.userData.type === 'motor') {
                            // 모터에 결합할 경우 가만히 있는 몸체가 아니라 '돌아가는 축(Shaft)'에 부착!
                            target.userData.shaft.attach(selectedObject);
                        } else {
                            // 일반 물체끼리는 그냥 부착
                            target.attach(selectedObject);
                        }
                    }
                    isAttachingMode = false;
                    document.getElementById('attach-hint').style.display = 'none';
                    if (boxHelper) boxHelper.setFromObject(selectedObject);
                } else {
                    selectObject(target);
                }
            } else {
                if (!isAttachingMode) selectObject(null);
            }
        });

        // 툴바 제어
        document.getElementById('btn-translate').onclick = (e) => { transformControls.setMode('translate'); e.target.classList.add('active-mode'); document.getElementById('btn-rotate').classList.remove('active-mode'); };
        document.getElementById('btn-rotate').onclick = (e) => { transformControls.setMode('rotate'); e.target.classList.add('active-mode'); document.getElementById('btn-translate').classList.remove('active-mode'); };
        
        // 속성 패널 제어
        document.getElementById('prop-scale').addEventListener('input', (e) => {
            if (selectedObject) {
                const s = parseFloat(e.target.value);
                selectedObject.scale.set(s, s, s);
                if (boxHelper) boxHelper.update();
            }
        });
        document.getElementById('prop-color').addEventListener('input', (e) => {
            if (selectedObject) {
                let target = selectedObject.isGroup ? selectedObject.children[0] : selectedObject;
                target.material.color.set(e.target.value);
            }
        });

        document.getElementById('btn-attach').onclick = () => {
            isAttachingMode = true;
            document.getElementById('attach-hint').style.display = 'block';
        };

        document.getElementById('btn-delete').onclick = () => {
            if (selectedObject) {
                if(selectedObject.parent) selectedObject.parent.remove(selectedObject);
                objects = objects.filter(o => o !== selectedObject);
                selectObject(null);
            }
        };
        document.getElementById('btn-clear').onclick = () => { objects.forEach(obj => { if(obj.parent) obj.parent.remove(obj); }); objects = []; selectObject(null); };

        // 6. 물리 시뮬레이션 제어 (스케일 및 결합 계층 완벽 지원)
        document.getElementById('btn-play').onclick = () => {
            isSimulating = true;
            selectObject(null);
            document.getElementById('btn-play').style.display = 'none';
            document.getElementById('btn-stop').style.display = 'block';
            document.getElementById('toolbar').style.opacity = '0.3'; document.getElementById('toolbar').style.pointerEvents = 'none';

            initPhysics();
            originalStates = [];
            physicsBodiesMap.clear();

            objects.forEach(mesh => {
                // 현재 물리 시작 전 상태 저장 (자식 객체도 월드 좌표로 복구하기 위해)
                originalStates.push({ obj: mesh, parent: mesh.parent, pos: mesh.position.clone(), quat: mesh.quaternion.clone(), scale: mesh.scale.clone() });

                // 실제 월드 크기를 계산하여 물리 박스 생성
                const box3 = new THREE.Box3().setFromObject(mesh);
                const size = new THREE.Vector3();
                box3.getSize(size);
                
                // 결합되어 다른 물체의 자식(Child)이 된 상태면 스스로 떨어지지 않고 부모를 따라감 (KINEMATIC)
                const isAttached = mesh.parent !== scene;
                const isMotor = mesh.userData.type === 'motor';
                
                const body = new CANNON.Body({
                    mass: (isAttached || isMotor) ? 0 : 5, 
                    type: (isAttached || isMotor) ? CANNON.Body.KINEMATIC : CANNON.Body.DYNAMIC,
                });

                if (mesh.userData.type === 'cube' || isMotor) {
                    body.addShape(new CANNON.Box(new CANNON.Vec3(size.x/2, size.y/2, size.z/2)));
                } else {
                    const q = new CANNON.Quaternion(); q.setFromAxisAngle(new CANNON.Vec3(1, 0, 0), -Math.PI/2);
                    body.addShape(new CANNON.Cylinder(size.x/2, size.x/2, size.y, 16), new CANNON.Vec3(), q);
                }

                // 월드 좌표 기준 배치
                const worldPos = new THREE.Vector3(); const worldQuat = new THREE.Quaternion();
                mesh.getWorldPosition(worldPos); mesh.getWorldQuaternion(worldQuat);
                body.position.copy(worldPos);
                body.quaternion.copy(worldQuat);
                
                physicsWorld.addBody(body);
                physicsBodiesMap.set(mesh, body);
            });
        };

        document.getElementById('btn-stop').onclick = () => {
            isSimulating = false;
            document.getElementById('btn-stop').style.display = 'none';
            document.getElementById('btn-play').style.display = 'block';
            document.getElementById('toolbar').style.opacity = '1'; document.getElementById('toolbar').style.pointerEvents = 'auto';

            // 모든 물체를 원래 구조와 위치로 복구
            originalStates.forEach(state => {
                state.parent.add(state.obj);
                state.obj.position.copy(state.pos);
                state.obj.quaternion.copy(state.quat);
                state.obj.scale.copy(state.scale);
            });
            physicsWorld = null;
            physicsBodiesMap.clear();
        };

        // 7. 실시간 애니메이션 루프
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
                
                // 1. 모터 회전 로직 (Three.js 내에서 회전시킴)
                objects.forEach(mesh => {
                    if (mesh.userData.type === 'motor') {
                        mesh.userData.shaft.rotation.y -= 5 * dt; // 축 회전 속도
                    }
                });

                // 2. 물리 맵핑 동기화
                objects.forEach(mesh => {
                    const body = physicsBodiesMap.get(mesh);
                    if (body) {
                        const isAttached = mesh.parent !== scene;
                        const isMotor = mesh.userData.type === 'motor';
                        
                        if (isAttached || isMotor) {
                            // 결합된 물체나 모터는 Three.js의 위치를 Cannon 물리 엔진으로 덮어씌움 (밀어내는 힘 발생)
                            const wp = new THREE.Vector3(); const wq = new THREE.Quaternion();
                            mesh.getWorldPosition(wp); mesh.getWorldQuaternion(wq);
                            body.position.copy(wp);
                            body.quaternion.copy(wq);
                        } else {
                            // 허공에 있는 일반 물체는 물리 엔진의 중력/충돌 결과를 Three.js 화면에 반영
                            mesh.position.copy(body.position);
                            mesh.quaternion.copy(body.quaternion);
                        }
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

components.html(three_js_code, height=900)
