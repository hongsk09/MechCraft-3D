import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

// 1. 기본 씬, 카메라, 렌더러 설정
const container = document.getElementById('canvas-container');
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x1e1e1e);

// 그리드 헬퍼 (바닥 눈금자) 추가
const gridHelper = new THREE.GridHelper(50, 50, 0x444444, 0x222222);
scene.add(gridHelper);

const camera = new THREE.PerspectiveCamera(75, (window.innerWidth - 290) / window.innerHeight, 0.1, 1000);
camera.position.set(10, 10, 10);

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth - 290, window.innerHeight);
container.appendChild(renderer.domElement);

// 2. 마우스 컨트롤 (모든 방향 회전, 줌, 이동)
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true; 
controls.dampingFactor = 0.05;

// 3. 조명 설정
const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
scene.add(ambientLight);
const dirLight = new THREE.DirectionalLight(0xffffff, 0.8);
dirLight.position.set(20, 20, 10);
scene.add(dirLight);

// 배열을 생성하여 추가된 객체들을 관리
let objects = [];

// 4. 부품 생성 함수들
const materialBase = new THREE.MeshStandardMaterial({ color: 0x888888, metalness: 0.5, roughness: 0.5 });
const materialAccent = new THREE.MeshStandardMaterial({ color: 0x4daafc, metalness: 0.7, roughness: 0.2 });

function addCube() {
    const geometry = new THREE.BoxGeometry(2, 2, 2);
    const mesh = new THREE.Mesh(geometry, materialBase);
    mesh.position.y = 1;
    scene.add(mesh);
    objects.push(mesh);
}

function addCylinder() {
    const geometry = new THREE.CylinderGeometry(1, 1, 4, 32);
    const mesh = new THREE.Mesh(geometry, materialBase);
    mesh.position.y = 2;
    scene.add(mesh);
    objects.push(mesh);
}

function addSpring() {
    // 스프링(나선) 형태를 만들기 위한 곡선
    class CustomSinCurve extends THREE.Curve {
        constructor(scale = 1) { super(); this.scale = scale; }
        getPoint(t, optionalTarget = new THREE.Vector3()) {
            const tx = Math.cos(t * Math.PI * 10);
            const ty = t * 5;
            const tz = Math.sin(t * Math.PI * 10);
            return optionalTarget.set(tx, ty, tz).multiplyScalar(this.scale);
        }
    }
    const path = new CustomSinCurve(1);
    const geometry = new THREE.TubeGeometry(path, 100, 0.2, 8, false);
    const mesh = new THREE.Mesh(geometry, materialAccent);
    scene.add(mesh);
    objects.push(mesh);
}

function addMotor() {
    // 모터는 원기둥 몸체와 앞부분의 작은 축으로 구성된 그룹으로 생성
    const motorGroup = new THREE.Group();
    
    // 모터 몸체
    const bodyGeo = new THREE.CylinderGeometry(1.5, 1.5, 3, 32);
    const bodyMesh = new THREE.Mesh(bodyGeo, materialBase);
    bodyMesh.rotation.z = Math.PI / 2;
    motorGroup.add(bodyMesh);

    // 모터 축
    const shaftGeo = new THREE.CylinderGeometry(0.3, 0.3, 1, 16);
    const shaftMesh = new THREE.Mesh(shaftGeo, materialAccent);
    shaftMesh.rotation.z = Math.PI / 2;
    shaftMesh.position.x = 2;
    motorGroup.add(shaftMesh);

    motorGroup.position.y = 1.5;
    scene.add(motorGroup);
    objects.push(motorGroup);
}

// 5. 버튼 이벤트 리스너 연결
document.getElementById('btn-cube').addEventListener('click', addCube);
document.getElementById('btn-cylinder').addEventListener('click', addCylinder);
document.getElementById('btn-spring').addEventListener('click', addSpring);
document.getElementById('btn-motor').addEventListener('click', addMotor);

document.getElementById('btn-clear').addEventListener('click', () => {
    objects.forEach(obj => scene.remove(obj));
    objects = [];
});

// 6. 창 크기 조절 대응
window.addEventListener('resize', () => {
    const width = window.innerWidth - 290;
    const height = window.innerHeight;
    renderer.setSize(width, height);
    camera.aspect = width / height;
    camera.updateProjectionMatrix();
});

// 7. 애니메이션 루프 (렌더링)
function animate() {
    requestAnimationFrame(animate);
    controls.update();
    renderer.render(scene, camera);
}
animate();
