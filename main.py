import streamlit as st

st.set_page_config(
    page_title="MechaLab 3D | 웹 기반 기계 시뮬레이터",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
      .block-container {padding: 0.35rem 0.65rem 0.6rem 0.65rem; max-width: 100%;}
      header[data-testid="stHeader"] {height: 0.2rem;}
      [data-testid="stToolbar"] {display: none;}
      footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

APP_HTML = r'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>MechaLab 3D</title>
<script type="importmap">
{
  "imports": {
    "three": "https://cdn.jsdelivr.net/npm/three@0.187.0/build/three.module.js",
    "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.187.0/examples/jsm/",
    "cannon-es": "https://cdn.jsdelivr.net/npm/cannon-es@0.20.0/dist/cannon-es.js"
  }
}
</script>
<style>
  :root {
    color-scheme: dark;
    --bg: #0c111b;
    --panel: #111a28;
    --panel2: #172235;
    --line: #26364d;
    --text: #e7edf7;
    --muted: #93a4bb;
    --accent: #48a9ff;
    --accent2: #1d75c9;
    --green: #34c98b;
    --red: #f07878;
  }
  * { box-sizing: border-box; }
  html, body { margin:0; width:100%; height:100%; overflow:hidden; background:var(--bg); color:var(--text); font-family:Inter, Pretendard, "Noto Sans KR", system-ui, sans-serif; }
  button, input { font:inherit; }
  .app { height:900px; min-height:680px; display:grid; grid-template-rows:58px 1fr 30px; border:1px solid #223149; background:var(--bg); overflow:hidden; }
  .topbar { display:flex; align-items:center; justify-content:space-between; gap:12px; padding:0 14px; background:#101827; border-bottom:1px solid var(--line); }
  .brand { display:flex; align-items:center; gap:10px; min-width:190px; }
  .logo { width:32px; height:32px; display:grid; place-items:center; border-radius:9px; background:linear-gradient(145deg,#2b8fe7,#14518f); font-size:18px; }
  .brand strong { display:block; font-size:14px; letter-spacing:.2px; }
  .brand small { color:var(--muted); font-size:10px; display:block; margin-top:2px; }
  .toolbar { display:flex; align-items:center; gap:6px; flex-wrap:wrap; justify-content:center; }
  .tool-btn, .action-btn, .part-btn, .list-btn { border:1px solid var(--line); color:#dbe7f7; background:#182438; border-radius:7px; cursor:pointer; transition:.15s ease; }
  .tool-btn { padding:7px 11px; font-size:12px; }
  .tool-btn:hover, .action-btn:hover, .part-btn:hover, .list-btn:hover { border-color:#4d86ba; background:#20334d; }
  .tool-btn.active { border-color:var(--accent); background:#123b62; color:#fff; box-shadow:inset 0 0 0 1px #237cc4; }
  .top-actions { display:flex; gap:7px; align-items:center; min-width:220px; justify-content:flex-end; }
  .action-btn { padding:7px 10px; font-size:12px; }
  .action-btn.primary { background:#1167a8; border-color:#2687d0; color:#fff; }
  .action-btn.danger { color:#ffb2b2; }
  .layout { min-height:0; display:grid; grid-template-columns:205px minmax(250px,1fr) 270px; }
  .side { min-height:0; overflow:auto; background:var(--panel); }
  .left { border-right:1px solid var(--line); padding:13px 11px; }
  .right { border-left:1px solid var(--line); padding:13px 12px; }
  .section-title { text-transform:uppercase; letter-spacing:.8px; color:#9cafc7; font-size:10px; font-weight:800; margin:2px 0 10px; }
  .part-grid { display:grid; grid-template-columns:1fr 1fr; gap:7px; }
  .part-btn { min-height:61px; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:5px; font-size:11px; }
  .part-btn .glyph { font-size:20px; line-height:1; }
  .hint { color:var(--muted); font-size:10px; line-height:1.55; margin:10px 1px 15px; }
  .divider { height:1px; background:var(--line); margin:13px 0; }
  .object-list { display:flex; flex-direction:column; gap:5px; }
  .list-btn { padding:8px; display:flex; align-items:center; justify-content:space-between; width:100%; text-align:left; font-size:11px; }
  .list-btn.selected { border-color:#348ed1; background:#123453; }
  .list-btn small { color:#8094ad; font-size:9px; }
  .viewport-wrap { min-width:0; min-height:0; position:relative; background:#0b121d; }
  #viewport { position:absolute; inset:0; }
  #viewport canvas { display:block; width:100%; height:100%; outline:none; }
  .view-badge { position:absolute; left:13px; top:12px; padding:6px 9px; border:1px solid #34445d; background:#111c2acc; border-radius:6px; color:#a9bbd1; font-size:10px; pointer-events:none; }
  .view-help { position:absolute; left:13px; bottom:12px; padding:7px 9px; background:#101a28d9; border:1px solid #30415a; color:#a6b6cb; border-radius:6px; font-size:10px; pointer-events:none; line-height:1.5; }
  .view-actions { position:absolute; right:12px; top:12px; display:flex; gap:5px; }
  .mini-btn { border:1px solid #34445d; color:#c9d7e9; background:#101a28dd; border-radius:6px; padding:6px 8px; font-size:10px; cursor:pointer; }
  .mini-btn:hover { background:#1c2d45; }
  .prop-empty { color:var(--muted); font-size:11px; line-height:1.6; padding:10px 1px; }
  .selected-name { font-size:13px; font-weight:750; margin-bottom:3px; }
  .selected-type { font-size:10px; color:var(--muted); margin-bottom:13px; }
  .field-title { color:#b9c8dc; font-size:10px; font-weight:700; margin:12px 0 6px; }
  .xyz-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:5px; }
  .field { min-width:0; }
  .field label { color:#7f94af; display:block; font-size:9px; margin:0 0 4px 2px; }
  .field input, .full-input { width:100%; min-width:0; padding:7px 6px; background:#0b1421; border:1px solid #2a3a52; border-radius:6px; color:#e3edf9; font-size:11px; outline:none; }
  .field input:focus, .full-input:focus { border-color:#4aa7ec; }
  input[type=color] { padding:2px; height:30px; cursor:pointer; }
  .full-row { display:grid; grid-template-columns:1fr auto; gap:6px; align-items:end; }
  .toggle-row { display:flex; align-items:center; gap:7px; font-size:10px; color:#b4c3d7; }
  .toggle-row input { accent-color:var(--accent); }
  .status { display:flex; align-items:center; justify-content:space-between; padding:0 12px; border-top:1px solid var(--line); background:#0f1724; font-size:10px; color:#9aabc1; }
  .status-left { display:flex; gap:15px; align-items:center; }
  .dot { display:inline-block; width:6px; height:6px; background:#78889e; border-radius:50%; margin-right:5px; }
  .dot.live { background:var(--green); box-shadow:0 0 7px #34c98b; }
  .status-right { color:#71839c; }
  .notice { margin-top:9px; color:#8ea2bc; font-size:9px; line-height:1.5; }
  @media (max-width:1000px) {
    .layout { grid-template-columns:165px minmax(220px,1fr) 230px; }
    .brand { min-width:150px; }
    .top-actions { min-width:160px; }
    .tool-btn { padding:6px 8px; }
  }
  @media (max-width:760px) {
    .app { height:900px; grid-template-rows:auto 1fr 30px; }
    .topbar { min-height:76px; flex-wrap:wrap; padding:8px; }
    .brand { min-width:0; }
    .toolbar { order:3; width:100%; }
    .top-actions { min-width:0; }
    .layout { grid-template-columns:130px minmax(180px,1fr); grid-template-rows:1fr 190px; }
    .left { grid-row:1 / 3; padding:9px 7px; }
    .right { grid-column:2; grid-row:2; border-left:0; border-top:1px solid var(--line); }
    .viewport-wrap { grid-column:2; grid-row:1; }
    .part-grid { grid-template-columns:1fr; }
    .part-btn { min-height:48px; flex-direction:row; }
  }
</style>
</head>
<body>
<div class="app">
  <header class="topbar">
    <div class="brand">
      <div class="logo">⚙</div>
      <div><strong>MechaLab 3D</strong><small>MECHANICAL DESIGN STUDIO</small></div>
    </div>
    <div class="toolbar" aria-label="변환 도구">
      <button class="tool-btn active" id="modeSelect">선택</button>
      <button class="tool-btn" id="modeMove">이동</button>
      <button class="tool-btn" id="modeRotate">회전</button>
      <button class="tool-btn" id="modeScale">크기</button>
    </div>
    <div class="top-actions">
      <label class="toggle-row" title="물리 기능 사용 여부"><input type="checkbox" id="physicsEnabled" checked> 물리 ON</label>
      <label class="toggle-row" title="중력 적용 여부"><input type="checkbox" id="gravityToggle" checked> 중력</label>
      <button class="action-btn primary" id="startBtn">▶ 실행</button>
      <button class="action-btn" id="stopBtn">초기화</button>
    </div>
  </header>
  <div class="layout">
    <aside class="side left">
      <div class="section-title">부품 생성</div>
      <div class="part-grid">
        <button class="part-btn" data-type="box"><span class="glyph">▣</span>육면체</button>
        <button class="part-btn" data-type="cylinder"><span class="glyph">◉</span>원기둥</button>
        <button class="part-btn" data-type="spring"><span class="glyph">〰</span>스프링</button>
        <button class="part-btn" data-type="gear"><span class="glyph">⚙</span>금속 기어</button>
        <button class="part-btn" data-type="wheel"><span class="glyph">◉</span>고무 바퀴</button>
        <button class="part-btn" data-type="motor"><span class="glyph">▤</span>구동 모터</button>
      </div>
      <div class="hint">부품을 추가한 뒤 화면에서 클릭해 선택하세요. 선택한 부품은 우측 패널이나 이동·회전·크기 기즈모로 편집할 수 있습니다.</div>
      <div class="divider"></div>
      <div class="section-title">장면 오브젝트</div>
      <div id="objectList" class="object-list"><div class="hint">아직 생성된 부품이 없습니다.</div></div>
      <div class="divider"></div>
      <button class="action-btn" id="attachBtn" style="width:100%">🔗 결합 모드</button>
      <button class="action-btn" id="detachBtn" style="width:100%;margin-top:6px">결합 해제</button>
      <div class="notice">결합 방법: 자식 부품을 먼저 선택하고 '결합 모드'를 누른 다음, 부모 부품을 선택하세요. 모터를 부모로 선택하면 모터 회전축에 연결됩니다.</div>
    </aside>

    <main class="viewport-wrap">
      <div id="viewport"></div>
      <div class="view-badge">3D VIEWPORT · PERSPECTIVE</div>
      <div class="view-actions">
        <button class="mini-btn" id="homeView">시점 초기화</button>
        <button class="mini-btn" id="gridToggle">그리드 숨김</button>
      </div>
      <div class="view-help">좌클릭 드래그: 회전 · 우클릭 드래그: 이동 · 휠: 확대/축소<br>오브젝트 클릭: 선택 · 기즈모 축 드래그: 변환</div>
    </main>

    <aside class="side right">
      <div class="section-title">속성 제어</div>
      <div id="properties"><div class="prop-empty">선택된 부품이 없습니다.<br>3D 화면 또는 오브젝트 목록에서 부품을 선택하세요.</div></div>
    </aside>
  </div>
  <footer class="status">
    <div class="status-left">
      <span><i class="dot" id="simDot"></i><span id="simStatus">설계 모드</span></span>
      <span id="objectCount">오브젝트 0개</span>
      <span id="selectionStatus">선택 없음</span>
    </div>
    <div class="status-right" id="statusMessage">준비 완료</div>
  </footer>
</div>

<script type="module">
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { TransformControls } from 'three/addons/controls/TransformControls.js';
import * as CANNON from 'cannon-es';

const $ = (id) => document.getElementById(id);
const viewport = $('viewport');
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0b121d);
scene.fog = new THREE.Fog(0x0b121d, 24, 90);

const camera = new THREE.PerspectiveCamera(48, 1, 0.1, 300);
camera.position.set(8, 7, 10);
camera.lookAt(0, 1, 0);

const renderer = new THREE.WebGLRenderer({ antialias:true, alpha:false });
renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.05;
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFShadowMap;
viewport.appendChild(renderer.domElement);

const orbit = new OrbitControls(camera, renderer.domElement);
orbit.enableDamping = true;
orbit.dampingFactor = 0.07;
orbit.target.set(0, 1, 0);
orbit.mouseButtons = {
  LEFT: THREE.MOUSE.ROTATE,
  MIDDLE: THREE.MOUSE.DOLLY,
  RIGHT: THREE.MOUSE.PAN
};

const hemi = new THREE.HemisphereLight(0xc8e2ff, 0x293344, 1.6);
scene.add(hemi);
const keyLight = new THREE.DirectionalLight(0xffffff, 3.0);
keyLight.position.set(7, 12, 8);
keyLight.castShadow = true;
keyLight.shadow.mapSize.set(2048, 2048);
keyLight.shadow.camera.left = -18;
keyLight.shadow.camera.right = 18;
keyLight.shadow.camera.top = 18;
keyLight.shadow.camera.bottom = -18;
keyLight.shadow.bias = -0.0002;
scene.add(keyLight);
const fillLight = new THREE.DirectionalLight(0x73a9e8, 1.0);
fillLight.position.set(-8, 5, -7);
scene.add(fillLight);

const floorMat = new THREE.MeshStandardMaterial({ color:0x172333, roughness:0.95, metalness:0.05 });
const floor = new THREE.Mesh(new THREE.PlaneGeometry(200, 200), floorMat);
floor.rotation.x = -Math.PI / 2;
floor.position.y = 0;
floor.receiveShadow = true;
scene.add(floor);
let grid = new THREE.GridHelper(100, 100, 0x3a536e, 0x27394f);
grid.position.y = -0.025;
scene.add(grid);

const transform = new TransformControls(camera, renderer.domElement);
scene.add(transform.getHelper());
transform.setSize(0.85);
transform.addEventListener('dragging-changed', (event) => { orbit.enabled = !event.value; });
transform.addEventListener('objectChange', () => {
  if (selectedId) syncPropertyInputs();
});

const objects = new Map();
let nextId = 1;
let selectedId = null;
let toolMode = 'select';
let pendingAttachId = null;
let physicsEnabled = true;
let physicsActive = false;
let running = false;
let physicsWorld = null;
let groundBody = null;
let accumulator = 0;
let lastFrame = performance.now();
let showGrid = true;
let selectionBox = null;
const raycaster = new THREE.Raycaster();
const pointer = new THREE.Vector2();
let pointerStart = null;

const COLOR_BY_TYPE = {
  box: '#4b9ee8', cylinder: '#93a8bd', spring: '#d5a64b',
  gear: '#9aa7b6', wheel: '#292f38', motor: '#3c506a'
};
const TYPE_NAME = {
  box:'육면체', cylinder:'원기둥', spring:'스프링', gear:'금속 기어', wheel:'고무 바퀴', motor:'구동 모터'
};

function mat(color, metalness=0.35, roughness=0.42) {
  return new THREE.MeshStandardMaterial({ color, metalness, roughness });
}
function castAndReceive(root) {
  root.traverse((child) => {
    if (child.isMesh) { child.castShadow = true; child.receiveShadow = true; }
  });
}
function tagOwner(root, id) {
  root.traverse((child) => { child.userData.ownerId = id; });
}
function makeGearGeometry(teeth=14, outer=0.82, rootR=0.67, depth=0.18) {
  const shape = new THREE.Shape();
  const pts = [];
  const perTooth = 4;
  for (let i=0; i<teeth; i++) {
    const a = (i / teeth) * Math.PI * 2;
    const step = Math.PI * 2 / teeth;
    pts.push([rootR*Math.cos(a), rootR*Math.sin(a)]);
    pts.push([outer*Math.cos(a+step*0.22), outer*Math.sin(a+step*0.22)]);
    pts.push([outer*Math.cos(a+step*0.70), outer*Math.sin(a+step*0.70)]);
    pts.push([rootR*Math.cos(a+step), rootR*Math.sin(a+step)]);
  }
  pts.forEach((p,i) => i===0 ? shape.moveTo(p[0],p[1]) : shape.lineTo(p[0],p[1]));
  shape.closePath();
  const hole = new THREE.Path();
  hole.absarc(0,0,0.22,0,Math.PI*2,true);
  shape.holes.push(hole);
  const geo = new THREE.ExtrudeGeometry(shape, { depth, bevelEnabled:true, bevelSegments:2, steps:1, bevelSize:0.025, bevelThickness:0.025, curveSegments:8 });
  geo.translate(0,0,-depth/2);
  geo.computeVertexNormals();
  return geo;
}
function makeSpring() {
  const pts = [];
  const turns = 8;
  const steps = 240;
  for (let i=0; i<=steps; i++) {
    const t = i/steps;
    const a = t*turns*Math.PI*2;
    pts.push(new THREE.Vector3(0.27*Math.cos(a), (t-0.5)*1.55, 0.27*Math.sin(a)));
  }
  const curve = new THREE.CatmullRomCurve3(pts);
  const tube = new THREE.Mesh(new THREE.TubeGeometry(curve, 240, 0.045, 10, false), mat('#d5a64b',0.82,0.25));
  const capMat = mat('#8b98a8',0.7,0.3);
  const capGeo = new THREE.CylinderGeometry(0.32,0.32,0.08,32);
  const top = new THREE.Mesh(capGeo,capMat); top.position.y=0.78;
  const bottom = new THREE.Mesh(capGeo,capMat); bottom.position.y=-0.78;
  const group = new THREE.Group();
  group.add(tube,top,bottom);
  return group;
}
function makeWheel() {
  const group = new THREE.Group();
  const tire = new THREE.Mesh(new THREE.TorusGeometry(0.65,0.18,24,72), mat('#20252d',0.05,0.88));
  tire.rotation.x = 0;
  group.add(tire);
  const rim = new THREE.Mesh(new THREE.CylinderGeometry(0.49,0.49,0.20,48), mat('#aeb9c5',0.82,0.25));
  rim.rotation.x = Math.PI/2;
  group.add(rim);
  const inner = new THREE.Mesh(new THREE.TorusGeometry(0.37,0.035,12,48), mat('#596c80',0.88,0.28));
  group.add(inner);
  const hub = new THREE.Mesh(new THREE.CylinderGeometry(0.15,0.15,0.28,32), mat('#d1d9e2',0.85,0.22));
  hub.rotation.x=Math.PI/2;
  group.add(hub);
  for (let i=0;i<8;i++) {
    const spoke = new THREE.Mesh(new THREE.BoxGeometry(0.055,0.69,0.045), mat('#8999aa',0.8,0.3));
    spoke.rotation.z = i*Math.PI/4;
    group.add(spoke);
  }
  return group;
}
function makeMotor() {
  const group = new THREE.Group();
  const body = new THREE.Mesh(new THREE.BoxGeometry(1.15,0.95,0.9), mat('#344a62',0.72,0.32));
  group.add(body);
  const end = new THREE.Mesh(new THREE.CylinderGeometry(0.39,0.39,0.12,40), mat('#8799ac',0.8,0.28));
  end.rotation.x=Math.PI/2;
  end.position.z=0.49;
  group.add(end);
  for (let i=0;i<7;i++) {
    const fin = new THREE.Mesh(new THREE.BoxGeometry(0.045,0.72,0.72), mat('#526a83',0.75,0.32));
    fin.position.x=-0.48+i*0.16;
    group.add(fin);
  }
  const shaftPivot = new THREE.Group();
  shaftPivot.position.set(0,0,0.56);
  const shaft = new THREE.Mesh(new THREE.CylinderGeometry(0.13,0.13,1.05,32), mat('#d1d8df',0.9,0.22));
  shaft.rotation.x=Math.PI/2;
  shaft.position.z=0.49;
  shaftPivot.add(shaft);
  const tip = new THREE.Mesh(new THREE.CylinderGeometry(0.16,0.16,0.12,32), mat('#8493a2',0.88,0.22));
  tip.rotation.x=Math.PI/2;
  tip.position.z=1.04;
  shaftPivot.add(tip);
  group.add(shaftPivot);
  group.userData.shaftPivot = shaftPivot;
  return group;
}

function buildVisual(type, color) {
  const root = new THREE.Group();
  let mesh;
  if (type==='box') {
    mesh = new THREE.Mesh(new THREE.BoxGeometry(1,1,1), mat(color,0.35,0.4));
    root.add(mesh);
  } else if (type==='cylinder') {
    mesh = new THREE.Mesh(new THREE.CylinderGeometry(0.5,0.5,1,48), mat(color,0.55,0.34));
    root.add(mesh);
  } else if (type==='spring') {
    root.add(makeSpring());
  } else if (type==='gear') {
    mesh = new THREE.Mesh(makeGearGeometry(), mat(color,0.88,0.24));
    root.add(mesh);
    const ring = new THREE.Mesh(new THREE.TorusGeometry(0.22,0.035,10,40), mat('#d3dbe5',0.9,0.2));
    root.add(ring);
  } else if (type==='wheel') {
    root.add(makeWheel());
  } else if (type==='motor') {
    const motorGroup = makeMotor();
    root.add(motorGroup);
    root.userData.shaftPivot = motorGroup.userData.shaftPivot;
  }
  return root;
}

function addObject(type) {
  if (physicsActive) stopSimulation(true);
  const id = `part-${nextId++}`;
  const color = COLOR_BY_TYPE[type] || '#8ba1b8';
  const root = buildVisual(type,color);
  root.position.set(((objects.size%4)-1.5)*1.55, type==='motor'?0.95:1.55, (Math.floor(objects.size/4)%3)*1.2);
  if (type==='motor') root.position.y=0.95;
  const record = {
    id, type, label:`${TYPE_NAME[type]} ${nextId-1}`, color,
    root, mass: type==='wheel'?1.4:1.0, motorSpeed:5.0,
    attachedTo:null, body:null, shaftBody:null, initial:null, initialParent:null,
    previousKinematicPosition:null
  };
  objects.set(id,record);
  scene.add(root);
  tagOwner(root,id);
  record.initial = saveTransform(root);
  selectObject(id);
  refreshObjectList();
  setStatus(`${record.label} 생성됨`);
}
function saveTransform(root) {
  return {
    position:root.position.clone(), quaternion:root.quaternion.clone(), scale:root.scale.clone(),
    rotation:root.rotation.clone()
  };
}
function restoreTransform(root, saved) {
  root.position.copy(saved.position);
  root.quaternion.copy(saved.quaternion);
  root.scale.copy(saved.scale);
  root.updateMatrixWorld(true);
}
function setStatus(message) { $('statusMessage').textContent=message; }
function updateCounts() {
  $('objectCount').textContent=`오브젝트 ${objects.size}개`;
  $('selectionStatus').textContent=selectedId ? `선택: ${objects.get(selectedId)?.label || ''}` : '선택 없음';
}
function refreshObjectList() {
  const list=$('objectList');
  if (!objects.size) {
    list.innerHTML='<div class="hint">아직 생성된 부품이 없습니다.</div>';
  } else {
    list.innerHTML='';
    for (const rec of objects.values()) {
      const btn=document.createElement('button');
      btn.className='list-btn'+(rec.id===selectedId?' selected':'');
      btn.innerHTML=`<span>${escapeHtml(rec.label)}</span><small>${TYPE_NAME[rec.type]}</small>`;
      btn.addEventListener('click',()=>selectObject(rec.id));
      list.appendChild(btn);
    }
  }
  updateCounts();
}
function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
}
function clearSelectionBox() {
  if (selectionBox) { scene.remove(selectionBox); selectionBox.geometry.dispose(); selectionBox.material.dispose(); selectionBox=null; }
}
function selectObject(id) {
  if (pendingAttachId && id && id!==pendingAttachId) {
    const child=objects.get(pendingAttachId);
    const parent=objects.get(id);
    if (child && parent) attachObjects(child,parent);
    pendingAttachId=null;
    $('attachBtn').classList.remove('primary');
    return;
  }
  selectedId=id;
  clearSelectionBox();
  const rec=objects.get(id);
  if (rec) {
    selectionBox=new THREE.BoxHelper(rec.root,0x56b7ff);
    scene.add(selectionBox);
    if (toolMode==='select' || physicsActive) transform.detach();
    else transform.attach(rec.root);
  } else {
    transform.detach();
  }
  refreshObjectList();
  updateProperties();
  updateCounts();
}
function attachObjects(child,parent) {
  if (child===parent || isAncestor(child.id,parent.id)) {
    setStatus('자기 자신 또는 하위 부품에는 결합할 수 없습니다.');
    return;
  }
  if (physicsActive) stopSimulation(true);
  const target = parent.type==='motor' ? parent.root.userData.shaftPivot : parent.root;
  if (!target) return;
  target.attach(child.root);
  child.attachedTo=parent.id;
  child.initial=saveTransform(child.root);
  tagOwner(child.root,child.id);
  if (selectedId!==child.id) selectedId=child.id;
  transform.detach();
  refreshObjectList();
  updateProperties();
  setStatus(`${child.label} → ${parent.label}${parent.type==='motor'?' 회전축':''} 결합 완료`);
}
function isAncestor(candidateId, possibleDescendantId) {
  let p=objects.get(possibleDescendantId);
  while (p && p.attachedTo) {
    if (p.attachedTo===candidateId) return true;
    p=objects.get(p.attachedTo);
  }
  return false;
}
function detachSelected() {
  const rec=objects.get(selectedId);
  if (!rec || !rec.attachedTo) { setStatus('선택한 부품은 결합된 상태가 아닙니다.'); return; }
  if (physicsActive) stopSimulation(true);
  scene.attach(rec.root);
  rec.attachedTo=null;
  rec.initial=saveTransform(rec.root);
  tagOwner(rec.root,rec.id);
  selectObject(rec.id);
  setStatus(`${rec.label} 결합 해제`);
}
function deleteSelected() {
  const rec=objects.get(selectedId);
  if (!rec) return;
  if (physicsActive) stopSimulation(true);
  // 삭제 대상의 자식은 월드 위치를 보존한 채 장면 루트로 분리한다.
  for (const child of objects.values()) {
    if (child.attachedTo===rec.id) {
      scene.attach(child.root);
      child.attachedTo=null;
      child.initial=saveTransform(child.root);
    }
  }
  if (rec.body && physicsWorld) physicsWorld.removeBody(rec.body);
  if (rec.shaftBody && physicsWorld) physicsWorld.removeBody(rec.shaftBody);
  if (rec.root.parent) rec.root.parent.remove(rec.root);
  disposeObject(rec.root);
  objects.delete(rec.id);
  selectedId=null;
  transform.detach();
  clearSelectionBox();
  refreshObjectList();
  updateProperties();
  setStatus('선택한 부품 삭제됨');
}
function disposeObject(root) {
  root.traverse(obj=>{
    if (obj.geometry) obj.geometry.dispose();
    if (obj.material) {
      const mats=Array.isArray(obj.material)?obj.material:[obj.material];
      mats.forEach(m=>m.dispose());
    }
  });
}

function syncPropertyInputs() {
  const rec=objects.get(selectedId);
  if (!rec) return;
  const p=rec.root.position, r=rec.root.rotation, s=rec.root.scale;
  const values={
    posX:p.x,posY:p.y,posZ:p.z,
    rotX:THREE.MathUtils.radToDeg(r.x),rotY:THREE.MathUtils.radToDeg(r.y),rotZ:THREE.MathUtils.radToDeg(r.z),
    scaleX:s.x,scaleY:s.y,scaleZ:s.z
  };
  for (const [id,value] of Object.entries(values)) {
    const el=$(id);
    if (el && document.activeElement!==el) el.value=Number(value).toFixed(2);
  }
}
function updateProperties() {
  const host=$('properties');
  const rec=objects.get(selectedId);
  if (!rec) {
    host.innerHTML='<div class="prop-empty">선택된 부품이 없습니다.<br>3D 화면 또는 오브젝트 목록에서 부품을 선택하세요.</div>';
    return;
  }
  const p=rec.root.position, r=rec.root.rotation, s=rec.root.scale;
  const isAttached=!!rec.attachedTo;
  host.innerHTML=`
    <div class="selected-name">${escapeHtml(rec.label)}</div>
    <div class="selected-type">${TYPE_NAME[rec.type]} · ${isAttached?'결합됨':'독립 부품'}</div>
    <div class="field-title">이름</div>
    <input class="full-input" id="propName" value="${escapeHtml(rec.label)}" ${physicsActive?'disabled':''}>
    <div class="field-title">위치 ${isAttached?'(부모 기준)':''}</div>
    <div class="xyz-grid">
      ${axisField('pos','X',p.x)}${axisField('pos','Y',p.y)}${axisField('pos','Z',p.z)}
    </div>
    <div class="field-title">회전 (도)</div>
    <div class="xyz-grid">
      ${axisField('rot','X',THREE.MathUtils.radToDeg(r.x))}${axisField('rot','Y',THREE.MathUtils.radToDeg(r.y))}${axisField('rot','Z',THREE.MathUtils.radToDeg(r.z))}
    </div>
    <div class="field-title">크기 배율</div>
    <div class="xyz-grid">
      ${axisField('scale','X',s.x)}${axisField('scale','Y',s.y)}${axisField('scale','Z',s.z)}
    </div>
    <div class="field-title">외관</div>
    <div class="full-row"><div class="field"><label>색상</label><input class="full-input" type="color" id="propColor" value="${rec.color}" ${physicsActive?'disabled':''}></div><div class="field"><label>질량 (kg)</label><input class="full-input" type="number" id="propMass" min="0.1" max="500" step="0.1" value="${rec.mass}" ${physicsActive || rec.type==='motor'?'disabled':''}></div></div>
    ${rec.type==='motor'?`<div class="field-title">모터 회전 속도 (rad/s)</div><input class="full-input" type="number" id="propSpeed" min="0" max="80" step="0.5" value="${rec.motorSpeed}" ${physicsActive?'disabled':''}>`:''}
    <div class="divider"></div>
    <button class="action-btn danger" id="deleteSelected" style="width:100%" ${physicsActive?'disabled':''}>선택 부품 삭제</button>
    ${isAttached?'<div class="notice">부모 부품의 움직임을 따라갑니다. 모터에 연결한 경우 모터 축 회전에 따라 함께 회전합니다.</div>':''}
  `;
  ['X','Y','Z'].forEach((axis,i)=>{
    const a=axis.toLowerCase();
    const pos=$(`pos${axis}`), rot=$(`rot${axis}`), scale=$(`scale${axis}`);
    [pos,rot,scale].forEach(el=>el.addEventListener('change',()=>{
      const current=objects.get(selectedId); if (!current || physicsActive) return;
      if (el===pos) current.root.position[a]=finiteValue(el.value,current.root.position[a]);
      else if (el===rot) current.root.rotation[a]=THREE.MathUtils.degToRad(finiteValue(el.value,0));
      else current.root.scale[a]=Math.max(0.05,Math.min(20,finiteValue(el.value,1)));
      current.root.updateMatrixWorld(true);
      if (selectionBox) selectionBox.update();
      updateProperties();
    }));
  });
  $('propName').addEventListener('change',e=>{
    rec.label=e.target.value.trim()||TYPE_NAME[rec.type];
    refreshObjectList(); updateProperties();
  });
  $('propColor').addEventListener('input',e=>{
    rec.color=e.target.value;
    rec.root.traverse(obj=>{
      if (obj.isMesh && obj.material && obj.material.color) obj.material.color.set(rec.color);
    });
  });
  $('propMass').addEventListener('change',e=>{ rec.mass=Math.max(0.1,Math.min(500,finiteValue(e.target.value,1))); });
  const speed=$('propSpeed');
  if (speed) speed.addEventListener('change',e=>{ rec.motorSpeed=Math.max(0,Math.min(80,finiteValue(e.target.value,5))); });
  $('deleteSelected').addEventListener('click',deleteSelected);
}
function finiteValue(value,fallback) {
  const n=Number(value);
  return Number.isFinite(n)?n:fallback;
}
function axisField(prefix,axis,value) {
  return `<div class="field"><label>${axis}</label><input id="${prefix}${axis}" type="number" step="0.1" value="${Number(value).toFixed(2)}" ${physicsActive?'disabled':''}></div>`;
}

function selectTool(mode) {
  toolMode=mode;
  ['Select','Move','Rotate','Scale'].forEach(name=>$(`mode${name}`).classList.remove('active'));
  const id={select:'modeSelect',translate:'modeMove',rotate:'modeRotate',scale:'modeScale'}[mode];
  $(id).classList.add('active');
  if (mode==='select' || physicsActive || !selectedId) transform.detach();
  else { transform.setMode(mode); transform.attach(objects.get(selectedId).root); }
}
function startAttachMode() {
  const rec=objects.get(selectedId);
  if (!rec) { setStatus('먼저 결합할 자식 부품을 선택하세요.'); return; }
  pendingAttachId=rec.id;
  $('attachBtn').classList.add('primary');
  setStatus(`${rec.label}: 결합 대상 부모 부품을 선택하세요.`);
}

function makePhysicsMaterial() {
  return new CANNON.Material({ friction:0.62, restitution:0.12 });
}
function correctionQuaternion(type) {
  const q=new CANNON.Quaternion();
  if (type==='gear' || type==='wheel') q.setFromEuler(Math.PI/2,0,0);
  return q;
}
function threeToCannonQuaternion(q3, type) {
  const q=new CANNON.Quaternion(q3.x,q3.y,q3.z,q3.w);
  if (type==='gear' || type==='wheel') {
    const fix=new CANNON.Quaternion(); fix.setFromEuler(Math.PI/2,0,0);
    q.mult(fix,q);
  }
  return q;
}
function cannonToThreeQuaternion(qc, type) {
  const q=new THREE.Quaternion(qc.x,qc.y,qc.z,qc.w);
  if (type==='gear' || type==='wheel') {
    const fix=new THREE.Quaternion().setFromEuler(new THREE.Euler(Math.PI/2,0,0));
    q.multiply(fix.invert());
  }
  return q;
}
function createShape(rec) {
  const s=rec.root.scale;
  if (rec.type==='box' || rec.type==='motor') {
    return new CANNON.Box(new CANNON.Vec3(0.5*s.x,0.5*s.y,0.5*s.z));
  }
  if (rec.type==='cylinder') {
    return new CANNON.Cylinder(0.5*Math.max(s.x,s.z),0.5*Math.max(s.x,s.z),1*s.y,24);
  }
  if (rec.type==='spring') {
    return new CANNON.Cylinder(0.31*Math.max(s.x,s.z),0.31*Math.max(s.x,s.z),1.62*s.y,16);
  }
  if (rec.type==='gear') {
    return new CANNON.Cylinder(0.83*Math.max(s.x,s.y),0.83*Math.max(s.x,s.y),0.23*s.z,24);
  }
  if (rec.type==='wheel') {
    return new CANNON.Cylinder(0.83*Math.max(s.x,s.y),0.83*Math.max(s.x,s.y),0.37*s.z,24);
  }
  return new CANNON.Box(new CANNON.Vec3(0.5,0.5,0.5));
}
function addGround(world) {
  const groundMat=new CANNON.Material({friction:0.78,restitution:0.08});
  groundBody=new CANNON.Body({mass:0,material:groundMat});
  groundBody.addShape(new CANNON.Plane());
  groundBody.quaternion.setFromEuler(-Math.PI/2,0,0);
  groundBody.position.set(0,0,0);
  world.addBody(groundBody);
  world.defaultContactMaterial.friction=0.65;
  world.defaultContactMaterial.restitution=0.12;
}
function getWorldPose(root) {
  root.updateWorldMatrix(true,false);
  const pos=new THREE.Vector3();
  const quat=new THREE.Quaternion();
  root.getWorldPosition(pos);
  root.getWorldQuaternion(quat);
  return {pos,quat};
}
function createBodyForRecord(rec) {
  if (rec.type==='motor') {
    const shape=new CANNON.Box(new CANNON.Vec3(0.575*rec.root.scale.x,0.475*rec.root.scale.y,0.45*rec.root.scale.z));
    const body=new CANNON.Body({mass:0,shape,material:makePhysicsMaterial()});
    body.collisionFilterGroup=2;
    body.collisionFilterMask=-1;
    const pose=getWorldPose(rec.root);
    body.position.set(pose.pos.x,pose.pos.y,pose.pos.z);
    body.quaternion.copy(threeToCannonQuaternion(pose.quat,'box'));
    physicsWorld.addBody(body);
    rec.body=body;

    const shaftShape=new CANNON.Cylinder(0.16,0.16,1.2,16);
    const shaft=new CANNON.Body({mass:0,shape:shaftShape,material:makePhysicsMaterial(),type:CANNON.Body.KINEMATIC});
    shaft.collisionFilterGroup=4;
    shaft.collisionFilterMask=-1;
    const pivot=rec.root.userData.shaftPivot;
    if (pivot) {
      const shaftPos=new THREE.Vector3(0,0,0.52);
      pivot.localToWorld(shaftPos);
      const shaftQuat=new THREE.Quaternion(); pivot.getWorldQuaternion(shaftQuat);
      const fix=new THREE.Quaternion().setFromEuler(new THREE.Euler(Math.PI/2,0,0));
      shaftQuat.multiply(fix);
      shaft.position.set(shaftPos.x,shaftPos.y,shaftPos.z);
      shaft.quaternion.set(shaftQuat.x,shaftQuat.y,shaftQuat.z,shaftQuat.w);
      shaft.updateMassProperties();
    }
    physicsWorld.addBody(shaft);
    rec.shaftBody=shaft;
    return;
  }
  const shape=createShape(rec);
  const parent=rec.attachedTo ? objects.get(rec.attachedTo) : null;
  // 모터 축에 결합된 바퀴는 동적 강체로 둬야 바닥과의 접촉 마찰로 굴러갈 수 있다.
  // 일반 결합 부품은 기존처럼 운동학적 물체로 부모 변환을 따라간다.
  const motorDrivenWheel=rec.type==='wheel' && parent?.type==='motor';
  const isAttached=!!rec.attachedTo && !motorDrivenWheel;
  const body=new CANNON.Body({
    mass:isAttached?0:rec.mass,
    shape,
    material:makePhysicsMaterial(),
    type:isAttached?CANNON.Body.KINEMATIC:CANNON.Body.DYNAMIC,
    linearDamping:0.015,
    angularDamping:motorDrivenWheel?0.035:0.12,
    allowSleep:!motorDrivenWheel,
    sleepSpeedLimit:0.12,
    sleepTimeLimit:1
  });
  const pose=getWorldPose(rec.root);
  body.position.set(pose.pos.x,pose.pos.y,pose.pos.z);
  const q=threeToCannonQuaternion(pose.quat,rec.type);
  body.quaternion.copy(q);
  if (motorDrivenWheel) {
    // 부모 모터/축과의 자기 충돌은 제외하되 바닥(기본 그룹) 및 다른 부품과는 충돌한다.
    body.collisionFilterGroup=8;
    body.collisionFilterMask=1 | 8;
    const pivot=parent.root.userData.shaftPivot;
    const axis=new THREE.Vector3(0,0,1);
    if (pivot) axis.applyQuaternion(pivot.getWorldQuaternion(new THREE.Quaternion())).normalize();
    body.angularVelocity.set(axis.x*parent.motorSpeed,axis.y*parent.motorSpeed,axis.z*parent.motorSpeed);
    body.wakeUp();
  }
  body.updateMassProperties();
  physicsWorld.addBody(body);
  rec.body=body;
  rec.previousKinematicPosition=pose.pos.clone();
}
function startSimulation() {
  if (!physicsEnabled) { setStatus('상단의 물리 ON을 켜야 시뮬레이션을 실행할 수 있습니다.'); return; }
  if (physicsActive) { running=true; setStatus('시뮬레이션 재개'); updateSimulationUI(); return; }
  physicsWorld=new CANNON.World({gravity:new CANNON.Vec3(0,$('gravityToggle')?.checked===false?0:-9.82,0)});
  physicsWorld.broadphase=new CANNON.SAPBroadphase(physicsWorld);
  physicsWorld.allowSleep=true;
  physicsWorld.solver.iterations=12;
  addGround(physicsWorld);
  for (const rec of objects.values()) {
    rec.initial=saveTransform(rec.root);
    rec.initialParent=rec.root.parent;
    if (rec.type==='motor' && rec.root.userData.shaftPivot) rec.root.userData.shaftPivot.rotation.z=0;
  }
  for (const rec of objects.values()) {
    const parent=rec.attachedTo ? objects.get(rec.attachedTo) : null;
    if (rec.type==='wheel' && parent?.type==='motor') {
      // 시뮬레이션 중에는 물리 바디가 바닥 접촉에 따라 움직일 수 있도록 장면 루트로 분리한다.
      // attachedTo 관계는 유지해 모터 속도를 계속 읽고, 정지 시 원래 축에 되돌린다.
      scene.attach(rec.root);
    }
    createBodyForRecord(rec);
  }
  physicsActive=true;
  running=true;
  accumulator=0;
  transform.detach();
  updateProperties();
  updateSimulationUI();
  setStatus('물리 시뮬레이션 실행 중');
}
function stopSimulation(reset=true) {
  if (physicsWorld) {
    for (const rec of objects.values()) {
      if (rec.body) physicsWorld.removeBody(rec.body);
      if (rec.shaftBody) physicsWorld.removeBody(rec.shaftBody);
      rec.body=null; rec.shaftBody=null; rec.previousKinematicPosition=null;
    }
    if (groundBody) physicsWorld.removeBody(groundBody);
  }
  physicsWorld=null; groundBody=null; physicsActive=false; running=false; accumulator=0;
  if (reset) {
    // 모터에 연결된 바퀴는 시뮬레이션 중 장면 루트로 분리했으므로 원래 부모로 복귀시킨다.
    for (const rec of objects.values()) {
      if (rec.initialParent && rec.initialParent !== scene && rec.root.parent !== rec.initialParent) {
        rec.initialParent.attach(rec.root);
      }
      if (rec.initial) restoreTransform(rec.root,rec.initial);
      const pivot=rec.root.userData.shaftPivot;
      if (pivot) pivot.rotation.set(0,0,0);
    }
  }
  if (selectedId && toolMode!=='select') transform.attach(objects.get(selectedId).root);
  updateProperties();
  updateSimulationUI();
  setStatus(reset?'시뮬레이션 정지 및 설계 상태 복원':'시뮬레이션 종료');
}
function updateSimulationUI() {
  $('simStatus').textContent=physicsActive?(running?'시뮬레이션 실행 중':'시뮬레이션 일시정지'):'설계 모드';
  $('simDot').classList.toggle('live',physicsActive&&running);
  $('startBtn').textContent=running?'Ⅱ 일시정지':(physicsActive?'▶ 재개':'▶ 실행');
  $('physicsEnabled').disabled=physicsActive;
}
function setGravityEnabled(enabled) {
  if (physicsWorld) physicsWorld.gravity.set(0,enabled?-9.82:0,0);
}
function syncKinematicBody(rec,dt) {
  if (!rec.body || rec.body.type!==CANNON.Body.KINEMATIC) return;
  const pose=getWorldPose(rec.root);
  const p=new CANNON.Vec3(pose.pos.x,pose.pos.y,pose.pos.z);
  const previous=rec.previousKinematicPosition || pose.pos;
  rec.body.velocity.set((p.x-previous.x)/Math.max(dt,1e-4),(p.y-previous.y)/Math.max(dt,1e-4),(p.z-previous.z)/Math.max(dt,1e-4));
  rec.body.position.copy(p);
  rec.body.quaternion.copy(threeToCannonQuaternion(pose.quat,rec.type));
  const parent=objects.get(rec.attachedTo);
  if (parent && parent.type==='motor' && parent.root.userData.shaftPivot) {
    const axis=new THREE.Vector3(0,0,1).applyQuaternion(parent.root.userData.shaftPivot.getWorldQuaternion(new THREE.Quaternion())).normalize();
    rec.body.angularVelocity.set(axis.x*parent.motorSpeed,axis.y*parent.motorSpeed,axis.z*parent.motorSpeed);
  } else {
    rec.body.angularVelocity.set(0,0,0);
  }
  rec.body.aabbNeedsUpdate=true;
  rec.previousKinematicPosition=pose.pos.clone();
}
function updateMotorShaft(rec,dt) {
  const pivot=rec.root.userData.shaftPivot;
  if (!pivot || !rec.shaftBody) return;
  pivot.rotation.z += rec.motorSpeed*dt;
  pivot.updateWorldMatrix(true,false);
  const pos=new THREE.Vector3(0,0,0.52);
  pivot.localToWorld(pos);
  const q=new THREE.Quaternion(); pivot.getWorldQuaternion(q);
  q.multiply(new THREE.Quaternion().setFromEuler(new THREE.Euler(Math.PI/2,0,0)));
  rec.shaftBody.position.set(pos.x,pos.y,pos.z);
  rec.shaftBody.quaternion.set(q.x,q.y,q.z,q.w);
  const axis=new THREE.Vector3(0,0,1).applyQuaternion(pivot.getWorldQuaternion(new THREE.Quaternion())).normalize();
  rec.shaftBody.angularVelocity.set(axis.x*rec.motorSpeed,axis.y*rec.motorSpeed,axis.z*rec.motorSpeed);
  rec.shaftBody.velocity.set(0,0,0);
  rec.shaftBody.aabbNeedsUpdate=true;
}
function stepSimulation(dt) {
  if (!physicsWorld || !running) return;
  // 모터 축과 결합 부품은 운동학적 물체로 갱신한 뒤 동적 물체와 충돌 계산을 한다.
  for (const rec of objects.values()) {
    if (rec.type==='motor') updateMotorShaft(rec,dt);
  }
  for (const rec of objects.values()) {
    if (rec.type!=='motor' && rec.attachedTo) syncKinematicBody(rec,dt);
    if (rec.type==='wheel' && rec.body && rec.body.type===CANNON.Body.DYNAMIC && rec.attachedTo) {
      const parent=objects.get(rec.attachedTo);
      if (parent?.type==='motor') {
        const pivot=parent.root.userData.shaftPivot;
        const axis=new THREE.Vector3(0,0,1);
        if (pivot) axis.applyQuaternion(pivot.getWorldQuaternion(new THREE.Quaternion())).normalize();
        // 모터의 회전 속도를 유지하면서 바닥 마찰이 바퀴 중심을 전진시키도록 한다.
        rec.body.angularVelocity.set(axis.x*parent.motorSpeed,axis.y*parent.motorSpeed,axis.z*parent.motorSpeed);
        rec.body.wakeUp();
      }
    }
  }
  physicsWorld.step(1/60,dt,6);
  for (const rec of objects.values()) {
    if (rec.type==='motor' || !rec.body || (rec.attachedTo && rec.body.type===CANNON.Body.KINEMATIC)) continue;
    rec.root.position.set(rec.body.position.x,rec.body.position.y,rec.body.position.z);
    const q=cannonToThreeQuaternion(rec.body.quaternion,rec.type);
    rec.root.quaternion.copy(q);
    rec.root.updateMatrixWorld(true);
  }
  if (selectionBox) selectionBox.update();
}

function onPointerDown(event) {
  pointerStart={x:event.clientX,y:event.clientY};
}
function onPointerUp(event) {
  if (!pointerStart) return;
  const moved=Math.hypot(event.clientX-pointerStart.x,event.clientY-pointerStart.y);
  pointerStart=null;
  if (moved>5 || transform.dragging || event.button!==0) return;
  const rect=renderer.domElement.getBoundingClientRect();
  pointer.x=((event.clientX-rect.left)/rect.width)*2-1;
  pointer.y=-((event.clientY-rect.top)/rect.height)*2+1;
  raycaster.setFromCamera(pointer,camera);
  const roots=[...objects.values()].map(rec=>rec.root);
  const hits=raycaster.intersectObjects(roots,true);
  if (hits.length) {
    let node=hits[0].object;
    let id=null;
    while (node && !id) { id=node.userData.ownerId; node=node.parent; }
    if (id) selectObject(id);
  } else if (!pendingAttachId) {
    selectObject(null);
  }
}
renderer.domElement.addEventListener('pointerdown',onPointerDown);
renderer.domElement.addEventListener('pointerup',onPointerUp);
renderer.domElement.addEventListener('contextmenu',e=>e.preventDefault());

$('modeSelect').addEventListener('click',()=>selectTool('select'));
$('modeMove').addEventListener('click',()=>selectTool('translate'));
$('modeRotate').addEventListener('click',()=>selectTool('rotate'));
$('modeScale').addEventListener('click',()=>selectTool('scale'));
document.querySelectorAll('.part-btn').forEach(btn=>btn.addEventListener('click',()=>addObject(btn.dataset.type)));
$('attachBtn').addEventListener('click',startAttachMode);
$('detachBtn').addEventListener('click',detachSelected);
$('startBtn').addEventListener('click',()=>{
  if (!physicsEnabled) { setStatus('물리 ON을 먼저 활성화하세요.'); return; }
  if (!physicsActive) startSimulation();
  else { running=!running; updateSimulationUI(); setStatus(running?'시뮬레이션 재개':'시뮬레이션 일시정지'); }
});
$('stopBtn').addEventListener('click',()=>stopSimulation(true));
$('physicsEnabled').addEventListener('change',e=>{
  physicsEnabled=e.target.checked;
  if (!physicsEnabled && physicsActive) stopSimulation(true);
  setStatus(physicsEnabled?'물리 기능 활성화':'물리 기능 비활성화');
});
$('gravityToggle').addEventListener('change',e=>{
  setGravityEnabled(e.target.checked);
  setStatus(e.target.checked?'중력 적용':'중력 해제');
});
$('homeView').addEventListener('click',()=>{
  camera.position.set(8,7,10); orbit.target.set(0,1,0); orbit.update();
});
$('gridToggle').addEventListener('click',()=>{
  showGrid=!showGrid; grid.visible=showGrid;
  $('gridToggle').textContent=showGrid?'그리드 숨김':'그리드 표시';
});

function resize() {
  const w=Math.max(1,viewport.clientWidth), h=Math.max(1,viewport.clientHeight);
  camera.aspect=w/h; camera.updateProjectionMatrix(); renderer.setSize(w,h,false);
}
const resizeObserver=new ResizeObserver(resize);
resizeObserver.observe(viewport);
resize();

function animate(now) {
  requestAnimationFrame(animate);
  const dt=Math.min((now-lastFrame)/1000,0.05);
  lastFrame=now;
  if (physicsActive && running) stepSimulation(dt);
  orbit.update();
  if (selectionBox) selectionBox.update();
  renderer.render(scene,camera);
}
requestAnimationFrame(animate);
updateSimulationUI();
updateProperties();
refreshObjectList();
setStatus('준비 완료 · 부품을 생성해 보세요.');

window.addEventListener('unhandledrejection',event=>{
  console.error(event.reason);
  setStatus('모듈 또는 시뮬레이션 오류: 브라우저 콘솔을 확인하세요.');
});
window.addEventListener('error',event=>{
  console.error(event.error || event.message);
  setStatus('렌더링 오류가 발생했습니다. 브라우저 콘솔을 확인하세요.');
});
</script>
</body>
</html>'''

st.title("MechaLab 3D")
st.caption("웹 기반 기계 부품 설계 및 기초 물리 시뮬레이터")
st.iframe(
    APP_HTML,
    height=930,
    tab_index=0,
    alt="MechaLab 3D 기계 부품 편집기 및 물리 시뮬레이터",
)

with st.expander("실행 및 사용 안내"):
    st.markdown(
        """
        1. 터미널에서 `pip install -r requirements.txt`를 실행합니다.
        2. 같은 폴더에서 `streamlit run main.py`를 실행합니다.
        3. 부품을 추가하고 선택한 뒤, 우측 속성 패널 또는 상단 기즈모로 편집합니다.
        4. 자식 부품을 먼저 선택하고 **결합 모드**를 누른 다음 부모 부품을 선택합니다.
        5. 물리 ON 상태에서 **실행**을 누르면 중력과 근사 충돌 시뮬레이션이 시작됩니다.
        6. **초기화**를 누르면 설계 단계의 배치로 돌아옵니다.

        **참고:** Three.js와 cannon-es는 브라우저에서 CDN으로 로드됩니다. 처음 실행할 때 인터넷 연결이 필요합니다.
        모터에 결합된 바퀴는 동적 물체로 처리해 바닥 접촉 마찰로 구르도록 합니다. 현재 물리 충돌체는 부품 형상에 맞춘 단순 근사 도형입니다. 스프링 변형, 정밀 기어 치합, 베어링·접촉 마찰, 모터 토크 전달을 해석하는 산업용 정밀 해석기는 아닙니다.
        """
    )
