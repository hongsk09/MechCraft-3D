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
        현재 물리 충돌체는 부품 형상에 맞춘 단순 근사 도형입니다. 스프링 변형, 정밀 기어 치합, 베어링·접촉 마찰, 모터 토크 전달을 해석하는 산업용 정밀 해석기는 아닙니다.
        """
    )
