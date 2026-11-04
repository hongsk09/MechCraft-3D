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
