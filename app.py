"""Sistema Solar 3D — Matemática & Contexto.
Projeto de Joice Souza Martins Santos.
Execute com: streamlit run app.py
"""
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Sistema Solar 3D | Matemática & Contexto", layout="wide", initial_sidebar_state="collapsed")
st.markdown("""<style>
.stApp, [data-testid="stAppViewContainer"] {background:#000;}
[data-testid="stMainBlockContainer"] {padding:0 !important; max-width:100% !important;}
[data-testid="stHeader"] {visibility:hidden;}
iframe {border:0; width:100%; height:100dvh !important; display:block;}
</style>""", unsafe_allow_html=True)

HTML = r'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sistema Solar 3D</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  html, body { width: 100%; height: 100%; overflow: hidden; background: #000; font-family: system-ui, sans-serif; color: #fff; }

  /* Fundo totalmente preto, sem estrelas */
  body {
    background: #000;
  }

  #scene {
    position: absolute; inset: 0;
    perspective: 1400px;
    cursor: grab;
    touch-action: none;
  }
  #scene.dragging { cursor: grabbing; }

  #system {
    position: absolute; left: 50%; top: 50%;
    width: 0; height: 0;
    transform-style: preserve-3d;
  }

  /* Órbitas */
  .orbit {
    position: absolute;
    border: 1px solid rgba(255, 255, 255, 0.18);
    border-radius: 50%;
    transform: rotateX(90deg);
    pointer-events: none;
  }

  /* Corpos celestes (sempre viradas para a câmera) */
  .body {
    position: absolute;
    border-radius: 50%;
    transform-style: preserve-3d;
  }
  .body .label {
    position: absolute; left: 50%; top: 100%;
    transform: translateX(-50%);
    margin-top: 4px;
    font-size: 11px; white-space: nowrap;
    color: rgba(255,255,255,.8);
    text-shadow: 0 0 4px #000;
    pointer-events: none;
  }

  .sun {
    background: radial-gradient(circle at 35% 35%, #fff7b0, #ffcc33 40%, #ff8800 80%, #e65100);
    box-shadow: 0 0 40px 15px rgba(255,170,0,.7), 0 0 120px 50px rgba(255,120,0,.35);
  }

  /* Planetas com sombreamento para parecerem esferas */
  .planet::after {
    content: ""; position: absolute; inset: 0; border-radius: 50%;
    background: radial-gradient(circle at 30% 30%, rgba(255,255,255,.35), transparent 45%, rgba(0,0,0,.65) 100%);
  }

  .ring {
    position: absolute; left: 50%; top: 50%;
    width: 190%; height: 190%;
    margin: -95% 0 0 -95%;
    border-radius: 50%;
    border: 5px solid rgba(220, 190, 140, .75);
    box-shadow: 0 0 0 4px rgba(200,170,120,.35), inset 0 0 0 3px rgba(200,170,120,.4);
    transform: rotateX(72deg);
    pointer-events: none;
  }

  /* Luas: posições e raios didáticos, não desenhados em escala real. */
  .satellite {
    position: absolute;
    border-radius: 50%;
    box-shadow: inset -2px -2px 3px rgba(0,0,0,.68), 0 0 3px rgba(255,255,255,.18);
    cursor: pointer;
    transform-style: preserve-3d;
  }
  .satellite::after {
    content: ""; position: absolute; inset: 0;
    border-radius: inherit;
    background: radial-gradient(circle at 30% 25%, rgba(255,255,255,.55), transparent 60%);
    pointer-events: none;
  }
  .moon-orbit {
    position: absolute;
    border: 1px solid rgba(204,218,232,.21);
    border-radius: 50%;
    pointer-events: none;
  }
  .moon-label {
    display: none;
    position: absolute;
    top: 100%; left: 50%; transform: translateX(-50%);
    margin-top: 3px;
    font-size: 10px; white-space: nowrap;
    color: rgba(235,240,249,.9);
    text-shadow: 0 1px 5px #000, 0 0 4px #000;
    pointer-events: none;
  }
  /* Painel científico de todos os corpos celestes, com boa leitura no celular. */
  .sun, .planet, .satellite { cursor: pointer; }
  .sun:focus-visible, .planet:focus-visible, .satellite:focus-visible {
    outline: 2px solid #95d5ff; outline-offset: 5px;
  }
  .satellite::before {
    content: ""; position: absolute; inset: -6px; border-radius: 50%;
  }
  #astroInfo {
    display: none;
    position: absolute; top: 72px; right: 16px;
    width: min(372px, calc(100vw - 32px));
    max-height: min(650px, calc(100dvh - 170px));
    overflow-y: auto; overscroll-behavior: contain;
    padding: 18px;
    background: linear-gradient(165deg, rgba(17,27,48,.98), rgba(5,10,23,.97));
    border: 1px solid rgba(138,174,216,.34);
    border-radius: 14px;
    box-shadow: 0 20px 55px rgba(0,0,0,.62);
    backdrop-filter: blur(18px); z-index: 8;
    font-size: 13px; line-height: 1.55;
  }
  #astroInfo.open { display: block; }
  #astroInfo .info-kicker { font-size: 10px; color: #90b9da; letter-spacing: 1.6px; text-transform: uppercase; }
  #astroInfo .info-head { display: flex; align-items: flex-start; justify-content: space-between; gap: 12px; margin: 5px 0 10px; }
  #astroInfo h2 { font-size: 24px; line-height: 1.12; font-weight: 700; letter-spacing: -.4px; }
  #closeAstroInfo { width: 30px; height: 30px; flex: 0 0 auto; border: 1px solid #3b4b62; background: #182439;
    border-radius: 8px; color: #d9e6f5; font-size: 20px; cursor: pointer; }
  #closeAstroInfo:hover { background: #273b59; }
  #astroInfo .info-intro { margin: 0 0 13px; color: #c5d3e2; }
  #astroInfo .info-stats { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin: 12px 0; }
  #astroInfo .info-stat { padding: 10px 11px; border: 1px solid rgba(143,180,225,.16);
    border-radius: 9px; background: rgba(125,160,210,.07); min-width: 0; }
  #astroInfo .stat-label { font-size: 10px; color: #91aac4; display: block; margin-bottom: 3px; }
  #astroInfo .stat-value { font-size: 13px; font-weight: 620; color: #f4f8ff; overflow-wrap: anywhere; }
  #astroInfo .distance-list { display: grid; gap: 7px; margin-top: 8px; }
  #astroInfo .distance-entry { padding: 9px 10px; border: 1px solid rgba(143,180,225,.18); border-radius: 8px; background: rgba(125,160,210,.06); }
  #astroInfo .distance-label { color: #a9bdd1; font-size: 11px; display: block; }
  #astroInfo .distance-decimal { color: #f4f8ff; font-size: 14px; font-weight: 600; display: block; font-variant-numeric: tabular-nums; }
  #astroInfo .distance-scientific { color: #a5d9ff; font-size: 14px; font-variant-numeric: tabular-nums; overflow-wrap: anywhere; }
  #astroInfo .distance-scientific sup { font-size: .75em; line-height: 0; }
  #astroInfo .distance-note { color: #a9b9ca; font-size: 11px; line-height: 1.5; margin-top: 8px; }
  #astroInfo .info-section { margin-top: 14px; padding-top: 12px; border-top: 1px solid rgba(174,198,225,.15); }
  #astroInfo h3 { font-size: 11px; font-weight: 650; color: #9dbedf; text-transform: uppercase; letter-spacing: .7px; margin-bottom: 5px; }
  #astroInfo .info-feature { color: #e3eaf3; }
  #astroInfo .info-moon-list { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 8px; }
  #astroInfo .moon-chip { border: 1px solid rgba(150,185,221,.35); background: rgba(31,49,75,.78);
    color: #e3ecf8; padding: 5px 9px; font-size: 11px; border-radius: 7px; cursor: pointer; }
  #astroInfo .moon-chip:hover, #astroInfo .moon-chip:focus-visible { background: #355677; }
  #astroInfo .info-foot { margin: 14px 0 0; color: #9aaac0; font-size: 11px; line-height: 1.5; }
  #astroInfo .source-link { display: inline-flex; margin-top: 8px; color: #a5d9ff; text-decoration: underline; text-underline-offset: 3px; }
  .belt-label { pointer-events: auto !important; cursor: pointer; border: 1px solid rgba(255,212,149,.35);
    background: rgba(20,18,15,.78); border-radius: 6px; padding: 5px 7px; }
  @media (max-width: 650px) {
    #ui { left: 8px; right: 8px; bottom: 8px; gap: 9px; padding: 9px; font-size: 12px; max-height: 190px; overflow-y: auto; }
    #ui button { padding: 6px 9px; font-size: 12px; }
    #ui input[type=range] { width: 86px; }
    #astroInfo { top: 64px; right: 8px; padding: 14px; width: min(360px, calc(100vw - 16px));
      max-height: calc(100dvh - 215px); }
    #title { top: 10px; left: 11px; font-size: 16px; }
    #hint { top: 34px; left: 11px; font-size: 10px; width: calc(100% - 22px); }
  }
  /* Cinturão de asteroides: partículas distribuídas no espaço 3D */
  .asteroid-belt {
    position: absolute;
    left: 0; top: 0;
    transform-style: preserve-3d;
    pointer-events: none;
  }
  .asteroid {
    position: absolute;
    border-radius: 35% 65% 50% 40%;
    clip-path: polygon(15% 4%, 74% 0%, 100% 33%, 85% 84%, 37% 100%, 0% 68%);
    box-shadow: inset -1px -1px 1px rgba(0,0,0,.35);
    opacity: .9;
    pointer-events: auto; cursor: pointer;
  }
  .belt-label {
    position: absolute;
    font-size: 10px;
    color: rgba(231,216,193,.80);
    white-space: nowrap;
    text-shadow: 0 1px 5px #000;
    pointer-events: none;
  }

  /* Interface */
  #ui {
    position: absolute; left: 16px; bottom: 16px;
    display: flex; flex-wrap: wrap; gap: 12px; align-items: center;
    padding: 10px 14px;
    background: rgba(10, 14, 35, .75);
    border: 1px solid rgba(255,255,255,.15);
    border-radius: 12px; backdrop-filter: blur(6px);
    font-size: 13px;
  }
  #ui button {
    background: #2a3a8a; color: #fff; border: 0; border-radius: 8px;
    padding: 6px 12px; cursor: pointer; font-size: 13px;
  }
  #ui button:hover { background: #3a4fb5; }
  #ui input[type=range] { vertical-align: middle; }
  #astroPicker { margin-left: 5px; border-radius: 7px; border: 1px solid rgba(162,194,223,.4);
    padding: 6px; color: #e9f3ff; background: #172743; width: 170px; max-width: 50vw; font-size: 12px; }
  #astroPicker option, #astroPicker optgroup { background: #172743; color: #e9f3ff; }
  .planet::before { content: ""; position: absolute; inset: -5px; border-radius: 50%; }
  .body .label, .moon-label { pointer-events: auto; cursor: pointer; }
  #ui { z-index: 5; }
  #title, #hint { z-index: 4; pointer-events: none; }

  #title { position: absolute; top: 14px; left: 16px; font-size: 18px; letter-spacing: .5px; opacity: .9; }
  #hint  { position: absolute; top: 40px; left: 16px; font-size: 12px; opacity: .6; }
</style>
</head>
<body>

<div id="title">☀️ Sistema Solar 3D</div>
<div id="hint">Arraste para girar • Zoom com scroll/pinça • Toque em qualquer astro para conhecê-lo</div>

<div id="scene">
  <div id="system"></div>
</div>

<div id="ui">
  <button id="btnPause">⏸ Pausar</button>
  <label>Velocidade <input id="speed" type="range" min="0" max="10" step="0.1" value="1"></label>
  <label><input id="chkOrbits" type="checkbox" checked> Órbitas</label>
  <label><input id="chkLabels" type="checkbox" checked> Nomes</label>
  <label><input id="chkAsteroids" type="checkbox" checked> Cinturão de asteroides</label>
  <label><input id="chkMoons" type="checkbox" checked> Luas</label>
  <label><input id="chkMoonNames" type="checkbox"> Nomes das luas</label>
  <button id="btnReset">Reiniciar vista</button>
  <label class="pick-label">Consultar <select id="astroPicker" aria-label="Escolha um corpo celeste para ver sua ficha"><option value="">Escolha um astro…</option></select></label>
</div>

<aside id="astroInfo" aria-live="polite" aria-label="Ficha do corpo celeste" aria-hidden="true">
  <div class="info-kicker" id="astroCategory">Exploração astronômica</div>
  <div class="info-head"><h2 id="astroTitle"></h2><button id="closeAstroInfo" type="button" aria-label="Fechar ficha">×</button></div>
  <p class="info-intro" id="astroIntro"></p>
  <div class="info-stats" id="astroStats"></div>
  <section class="info-section" id="distanceSection">
    <h3>Distâncias · notação científica</h3>
    <div class="distance-list" id="distanceList"></div>
    <p class="distance-note" id="distanceNote"></p>
    <a class="source-link" href="https://solarsystem.nasa.gov/planet-compare/" target="_blank" rel="noopener noreferrer">Dados orbitais: NASA</a>
    <a class="source-link" href="https://ssd.jpl.nasa.gov/sats/elem/" target="_blank" rel="noopener noreferrer">Dados das luas: JPL</a>
  </section>
  <section class="info-section"><h3>O que vale saber</h3><p class="info-feature" id="astroFeature"></p></section>
  <section class="info-section" id="astroRelatedSection" hidden><h3 id="astroRelatedTitle"></h3><div class="info-moon-list" id="astroRelated"></div></section>
  <p class="info-foot">Dados astronômicos aproximados. Tamanhos, distâncias e movimentos desta animação são ilustrativos, não estão em escala.</p>
  <a class="source-link" id="astroSource" href="https://science.nasa.gov/solar-system/" target="_blank" rel="noopener noreferrer">Consultar fonte: NASA ↗</a>
</aside>

<script>
  // ---- Dados: raio da órbita (px), tamanho (px), período (dias), cor
  const bodies = [
    { name: "Mercúrio", orbit: 90,  size: 10, period: 88,    color: "#a8a29e" },
    { name: "Vênus",    orbit: 135, size: 16, period: 225,   color: "#e8c27a" },
    { name: "Terra",    orbit: 180, size: 17, period: 365,   color: "#2e86de" },
    { name: "Marte",    orbit: 225, size: 13, period: 687,   color: "#d9532c" },
    { name: "Júpiter",  orbit: 300, size: 42, period: 4333,  color: "#d8a878" },
    { name: "Saturno",  orbit: 385, size: 34, period: 10759, color: "#e3c98f", ring: true },
    { name: "Urano",    orbit: 455, size: 24, period: 30687, color: "#7fd6e0" },
    { name: "Netuno",   orbit: 515, size: 23, period: 60190, color: "#3f5fd9" }
  ];

  // Luas selecionadas, e não a contagem total de satélites conhecidos.
  // Períodos siderais aproximados (dias terrestres); dados para fins didáticos.
  // "radius" e "size" são medidas VISUAIS em pixels, não valores astronômicos.
  const moonsByPlanet = {
    "Terra": [
      {name:"Lua", period:27.322, radius:23, size:5.8, color:"#c6c8c6", inclination:5}
    ],
    "Marte": [
      {name:"Fobos", period:0.319, radius:15, size:3.3, color:"#a6a19b", inclination:2},
      {name:"Deimos", period:1.263, radius:24, size:2.8, color:"#b6a99c", inclination:3}
    ],
    "Júpiter": [
      {name:"Io", period:1.769, radius:29, size:5.0, color:"#d8c477", inclination:1},
      {name:"Europa", period:3.551, radius:39, size:4.8, color:"#c5bda5", inclination:2},
      {name:"Ganimedes", period:7.155, radius:50, size:6.4, color:"#8c8577", inclination:3},
      {name:"Calisto", period:16.689, radius:64, size:5.7, color:"#726e69", inclination:4}
    ],
    "Saturno": [
      {name:"Encélado", period:1.370, radius:27, size:3.5, color:"#e7e8e9", inclination:2},
      {name:"Dione", period:2.737, radius:37, size:4.2, color:"#c9c8be", inclination:2},
      {name:"Reia", period:4.518, radius:47, size:4.8, color:"#c3bdb1", inclination:3},
      {name:"Titã", period:15.945, radius:58, size:6.2, color:"#d9a85f", inclination:4},
      {name:"Jápeto", period:79.321, radius:70, size:4.4, color:"#968a7b", inclination:7}
    ],
    "Urano": [
      {name:"Miranda", period:1.413, radius:22, size:3.2, color:"#b5b9bb", inclination:4},
      {name:"Ariel", period:2.520, radius:30, size:4.0, color:"#d5d7ce", inclination:3},
      {name:"Umbriel", period:4.144, radius:39, size:4.0, color:"#737981", inclination:2},
      {name:"Titânia", period:8.706, radius:48, size:5.1, color:"#aaa7a3", inclination:3},
      {name:"Oberon", period:13.463, radius:57, size:4.9, color:"#888789", inclination:4}
    ],
    "Netuno": [
      {name:"Proteu", period:1.122, radius:25, size:3.5, color:"#797d83", inclination:3},
      {name:"Tritão", period:5.877, radius:39, size:6.2, color:"#c8b7ad", inclination:8, retrograde:true}
    ]
  };

  const system = document.getElementById("system");
  const scene  = document.getElementById("scene");

  // ---- Sol
  const sun = document.createElement("div");
  sun.className = "body sun";
  sun.style.width = sun.style.height = "60px";
  sun.style.left = sun.style.top = "-30px";
  sun.innerHTML = '<span class="label">Sol</span>';
  system.appendChild(sun);
  sun.title = "Abrir ficha do Sol";
  sun.setAttribute("role", "button"); sun.setAttribute("aria-label", "Informações sobre o Sol");
  sun.tabIndex = 0;
  sun.addEventListener("click", e => { e.stopPropagation(); showAstroInfo("Sol", "sun"); });
  sun.addEventListener("keydown", e => {
    if (e.key === "Enter" || e.key === " ") { e.preventDefault(); showAstroInfo("Sol", "sun"); }
  });

  // ---- Órbitas e planetas
  const orbitEls = [];
  bodies.forEach(b => {
    const o = document.createElement("div");
    o.className = "orbit";
    o.style.width = o.style.height = b.orbit * 2 + "px";
    o.style.left = o.style.top = -b.orbit + "px";
    system.appendChild(o);
    orbitEls.push(o);

    const p = document.createElement("div");
    p.className = "body planet";
    p.style.width = p.style.height = b.size + "px";
    p.style.left = p.style.top = -b.size / 2 + "px";
    p.style.background = b.color;
    p.innerHTML = '<span class="label">' + b.name + '</span>';
    if (b.ring) { const r = document.createElement("div"); r.className = "ring"; p.appendChild(r); }
    system.appendChild(p);
    b.el = p;
    b.angle = Math.random() * Math.PI * 2;
    p.title = `Abrir ficha de ${b.name}`;
    p.style.cursor = "pointer";
    p.setAttribute("role", "button");
    p.tabIndex = 0;
    p.setAttribute("aria-label", `Informações sobre ${b.name}`);
    p.addEventListener("click", event => { event.stopPropagation(); showAstroInfo(b.name, "planet"); });
    p.addEventListener("keydown", event => {
      if (event.key === "Enter" || event.key === " ") { event.preventDefault(); showAstroInfo(b.name, "planet"); }
    });
  });

  // A Lua e os satélites dos demais planetas orbitam seus respectivos planetas.
  const allMoons = [];
  const moonOrbitEls = [];
  for (const b of bodies) {
    b.moons = moonsByPlanet[b.name] || [];
    b.moons.forEach((m, i) => {
      const orbit = document.createElement("div");
      orbit.className = "moon-orbit";
      orbit.style.width = orbit.style.height = 2 * m.radius + "px";
      orbit.style.left = orbit.style.top = -m.radius + "px";
      system.appendChild(orbit);
      moonOrbitEls.push(orbit);
      m.orbitEl = orbit;

      const el = document.createElement("div");
      el.className = "satellite";
      el.style.width = el.style.height = m.size + "px";
      el.style.left = el.style.top = -m.size / 2 + "px";
      el.style.background = m.color;
      el.title = `${m.name} — lua de ${b.name}`;
      el.innerHTML = `<span class="moon-label">${m.name}</span>`;
      system.appendChild(el);
      el.setAttribute("role", "button"); el.setAttribute("aria-label", `Informações sobre ${m.name}, lua de ${b.name}`);
      el.tabIndex = 0;
      el.addEventListener("keydown", event => {
        if (event.key === "Enter" || event.key === " ") { event.preventDefault(); showAstroInfo(m.name, "moon", b.name); }
      });
      m.el = el;
      m.b = b;
      m.angle = (i * 1.77 + bodies.indexOf(b) * .72) % (2*Math.PI);
      // A animação foi deliberadamente desacelerada: períodos reais curtos
      // tornariam várias luas rápidas demais para observar neste modelo.
      m.visualSecondsPerOrbit = 5 + 2 * Math.sqrt(m.period);
      el.addEventListener("click", event => {
        event.stopPropagation();
        showAstroInfo(m.name, "moon", b.name);
      });
      allMoons.push(m);
    });
  }

  // Catálogo didático: valores físicos da NASA, independentes da escala visual.
  // Fontes: https://nssdc.gsfc.nasa.gov/planetary/factsheet/
  //         https://science.nasa.gov/solar-system/moons/facts/
  //         https://science.nasa.gov/sun/facts/
  const planetFacts = {
    "Mercúrio": {type:"Planeta rochoso", intro:"O menor planeta e o mais próximo do Sol. Sua superfície está marcada por crateras.",
      diameter:"4.879 km", distance:"57,9 milhões km", rotation:"58,6 dias", gravity:"3,7 m/s²",
      feature:"Sua atmosfera é extremamente tênue. Como quase não retém calor, a diferença entre as temperaturas do dia e da noite é enorme."},
    "Vênus": {type:"Planeta rochoso", intro:"Um mundo envolto em nuvens espessas e o planeta mais quente do Sistema Solar.",
      diameter:"12.104 km", distance:"108,2 milhões km", rotation:"243 dias (retrógrada)", gravity:"8,9 m/s²",
      feature:"Uma atmosfera densa, dominada por dióxido de carbono, intensifica o efeito estufa. A superfície atinge cerca de 464 °C."},
    "Terra": {type:"Planeta rochoso", intro:"Nosso planeta é o único mundo onde a vida foi confirmada até hoje.",
      diameter:"12.756 km", distance:"149,6 milhões km", rotation:"23 h 56 min", gravity:"9,8 m/s²",
      feature:"Possui oceanos de água líquida, atmosfera rica em nitrogênio e oxigênio e um campo magnético global."},
    "Marte": {type:"Planeta rochoso", intro:"Conhecido como planeta vermelho por causa dos óxidos de ferro em seu solo.",
      diameter:"6.792 km", distance:"228 milhões km", rotation:"24 h 37 min", gravity:"3,7 m/s²",
      feature:"Abriga o Olympus Mons, um vulcão gigantesco, e evidências de água líquida em seu passado distante."},
    "Júpiter": {type:"Gigante gasoso", intro:"O maior planeta do Sistema Solar, dominado por hidrogênio e hélio.",
      diameter:"142.984 km", distance:"778,5 milhões km", rotation:"9 h 56 min", gravity:"23,1 m/s²",
      feature:"A Grande Mancha Vermelha é uma tempestade persistente. Suas quatro grandes luas galileanas incluem mundos vulcânicos e oceânicos."},
    "Saturno": {type:"Gigante gasoso", intro:"Reconhecido por seu extenso sistema de anéis feitos principalmente de gelo e fragmentos rochosos.",
      diameter:"120.536 km", distance:"1,432 bilhão km", rotation:"10 h 42 min", gravity:"9,0 m/s²",
      feature:"Sua densidade média é menor que a da água. Titã possui lagos de metano e etano, enquanto Encélado lança plumas de gelo ao espaço."},
    "Urano": {type:"Gigante de gelo", intro:"Um planeta azul-esverdeado, com metano na atmosfera e eixo de rotação muito inclinado.",
      diameter:"51.118 km", distance:"2,867 bilhões km", rotation:"17 h 14 min (retrógrada)", gravity:"8,7 m/s²",
      feature:"Seu eixo é inclinado cerca de 98°: o planeta gira quase de lado. Também possui anéis e numerosas luas geladas."},
    "Netuno": {type:"Gigante de gelo", intro:"O planeta mais distante do Sol entre os oito planetas reconhecidos.",
      diameter:"49.528 km", distance:"4,515 bilhões km", rotation:"16 h 06 min", gravity:"11,0 m/s²",
      feature:"Apresenta ventos extremamente intensos e tempestades na atmosfera. Sua maior lua, Tritão, tem órbita retrógrada."}
  };
  const moonFacts = {
    "Lua": {diameter:"≈ 3.475 km", feature:"Sua gravidade influencia as marés da Terra. A mesma face fica voltada para nós devido à rotação sincronizada."},
    "Fobos": {diameter:"≈ 22,5 km", feature:"A maior das duas luas de Marte. Orbita tão perto do planeta que seu movimento orbital é mais rápido que a rotação marciana."},
    "Deimos": {diameter:"≈ 12,4 km", feature:"A menor e mais distante das duas luas de Marte. Tem formato irregular e superfície coberta por regolito."},
    "Io": {diameter:"≈ 3.643 km", feature:"É o mundo com maior atividade vulcânica conhecida no Sistema Solar, aquecido por forças de maré."},
    "Europa": {diameter:"≈ 3.122 km", feature:"Sua crosta de gelo provavelmente cobre um oceano salgado. É um dos alvos mais importantes na busca por ambientes habitáveis."},
    "Ganimedes": {diameter:"≈ 5.268 km", feature:"A maior lua do Sistema Solar, maior até que Mercúrio. É a única lua conhecida com campo magnético próprio."},
    "Calisto": {diameter:"≈ 4.821 km", feature:"É uma das superfícies mais crateradas do Sistema Solar e pode guardar um oceano profundo sob o gelo."},
    "Encélado": {diameter:"≈ 504 km", feature:"Jatos de vapor de água e partículas de gelo emergem de seu polo sul. Há um oceano sob sua crosta gelada."},
    "Dione": {diameter:"≈ 1.123 km", feature:"Lua gelada de Saturno com falhas, penhascos brilhantes e numerosas crateras."},
    "Reia": {diameter:"≈ 1.528 km", feature:"A segunda maior lua de Saturno, formada principalmente por gelo e rochas, com superfície muito craterada."},
    "Titã": {diameter:"≈ 5.150 km", feature:"Possui atmosfera espessa de nitrogênio e rios e lagos de metano e etano líquidos em sua superfície."},
    "Jápeto": {diameter:"≈ 1.469 km", feature:"Tem dois hemisférios de brilho muito diferente e uma longa cadeia de montanhas próxima ao equador."},
    "Miranda": {diameter:"≈ 472 km", feature:"Conhecida por seus enormes cânions, falhas e terrenos que parecem ter sido reorganizados."},
    "Ariel": {diameter:"≈ 1.158 km", feature:"Entre as grandes luas de Urano, destaca-se pela superfície relativamente brilhante e por extensos vales."},
    "Umbriel": {diameter:"≈ 1.169 km", feature:"Uma das grandes luas mais escuras de Urano; conserva muitas crateras antigas."},
    "Titânia": {diameter:"≈ 1.578 km", feature:"A maior lua de Urano, com indícios de fraturas e antigos processos geológicos."},
    "Oberon": {diameter:"≈ 1.523 km", feature:"Lua gelada com grande quantidade de crateras e pouca evidência de atividade recente."},
    "Proteu": {diameter:"≈ 420 km", feature:"É a segunda maior lua de Netuno, muito escura e de forma irregular, descoberta pela Voyager 2."},
    "Tritão": {diameter:"≈ 2.706 km", feature:"Orbita Netuno no sentido retrógrado e apresenta sinais de atividade criovulcânica. Provavelmente foi capturada."}
  };

  const infoPanel = document.getElementById("astroInfo");
  const sunFact = {type:"Estrela — tipo G2 V", intro:"A estrela no centro do nosso Sistema Solar. Sua gravidade mantém planetas, asteroides e cometas em órbita.",
    stats:[["Diâmetro", "≈ 1,39 milhão km"], ["Idade", "≈ 4,6 bilhões de anos"],
           ["Temperatura da fotosfera", "≈ 5.500 °C"], ["Composição", "Hidrogênio e hélio"]],
    feature:"No núcleo, a fusão de hidrogênio em hélio libera a energia que chega à Terra na forma de luz e calor.",
    source:"https://science.nasa.gov/sun/facts/"};
  const beltFact = {type:"Região de pequenos corpos", intro:"Uma extensa região de asteroides que orbitam o Sol principalmente entre Marte e Júpiter.",
    stats:[["Localização", "Entre Marte e Júpiter"], ["Faixa aproximada", "2,1 a 3,3 UA"],
           ["Corpos", "Rochosos e metálicos"], ["Objeto de destaque", "Ceres (planeta anão)"]],
    feature:"Os asteroides estão separados por grandes distâncias. Neste modelo, eles aparecem mais densos para que o cinturão seja fácil de observar.",
    source:"https://science.nasa.gov/solar-system/solar-system-facts/"};

  // Semieixos maiores aproximados (km), NASA Planet Compare; não são os raios em pixels.
  const solarKm = {"Mercúrio":57910000,"Vênus":108200000,"Terra":149600000,"Marte":227900000,
    "Júpiter":778300000,"Saturno":1427000000,"Urano":2871000000,"Netuno":4498000000};
  // Semieixos maiores dos satélites (km), NASA/JPL Planetary Satellite Mean Elements.
  const lunarKm = {"Lua":384400,"Fobos":9375,"Deimos":23457,"Io":421800,"Europa":671100,
    "Ganimedes":1070400,"Calisto":1882700,"Encélado":238400,"Dione":377700,"Reia":527200,
    "Titã":1221900,"Jápeto":3561700,"Miranda":129846,"Ariel":190930,"Umbriel":265980,
    "Titânia":436298,"Oberon":583511,"Proteu":117700,"Tritão":354800};
  const earthKm = solarKm.Terra;
  // Média em fase relativa uniforme de duas órbitas circulares coplanares.
  // d(θ) = sqrt(a² + b² − 2ab cos θ). Soma de pontos médios em 2048 ângulos.
  function meanEarthKm(a) {
    let sum = 0;
    const n = 2048;
    for (let i=0; i<n; i++) {
      const theta = 2*Math.PI*(i+.5)/n;
      sum += Math.hypot(a*Math.cos(theta)-earthKm,a*Math.sin(theta));
    }
    return Number((sum/n).toPrecision(3));
  }
  const earthMean = Object.fromEntries(Object.entries(solarKm).map(([name,a])=>[name,name==="Terra" ? 0 : meanEarthKm(a)]));
  const kmFormat = new Intl.NumberFormat("pt-BR",{maximumFractionDigits:0});
  function scientificKm(n) {
    if (n===0) return "0";
    const [coef, exp] = n.toExponential().split("e");
    return `${coef.replace(".",",")} × 10<sup>${Number(exp)}</sup>`;
  }
  function distanceRow(label, values) {
    const div = document.createElement("div"); div.className="distance-entry";
    const lbl = document.createElement("span"); lbl.className="distance-label"; lbl.textContent=label;
    const dec = document.createElement("span"); dec.className="distance-decimal";
    const sci = document.createElement("span"); sci.className="distance-scientific";
    const nums = Array.isArray(values) ? values : [values];
    dec.textContent = (nums[0]===0 && nums.length===1 ? "" : "≈ ")+nums.map(n=>kmFormat.format(n)).join(" a ")+" km";
    // Somente números internos, sem texto do usuário, entram neste HTML.
    sci.innerHTML = nums.map(scientificKm).join(" a ")+" km";
    div.append(lbl,dec,sci); return div;
  }
  function renderDistances(name, category, host) {
    let rows, note;
    const modelNote="A distância à Terra varia com as órbitas. A média é estimada por órbitas circulares no mesmo plano, não por efemérides em tempo real.";
    if(category==="sun") {
      rows=[["Distância ao Sol (centro)",0],["Distância média à Terra",earthKm]];
      note="Distâncias entre os centros dos astros. A distância Terra–Sol é aproximada pelo semieixo maior da órbita terrestre.";
    } else if(category==="belt") {
      rows=[["Faixa orbital em relação ao Sol",[314000000,494000000]], ["Faixa possível em relação à Terra (modelo)",[165000000,643000000]]];
      note="Faixa aproximada de 2,1 a 3,3 UA. Os limites terrestres usam órbitas circulares; o cinturão não é um único corpo e não tem uma distância média única.";
    } else if(category==="moon") {
      rows=[["Distância média ao Sol (aprox.)",solarKm[host]], ["Distância média à Terra"+(host==="Terra"?"":" (aprox.)"),host==="Terra"?lunarKm[name]:earthMean[host]]];
      if(host!=="Terra") rows.push([`Distância orbital a ${host}`,lunarKm[name]]);
      note=host==="Terra"?"A distância ao Sol é aproximada pela órbita da Terra. A distância Terra–Lua usa o semieixo maior lunar.":"As distâncias ao Sol e à Terra são aproximadas pelas do planeta de origem; a distância ao planeta usa o semieixo maior da órbita lunar. "+modelNote;
    } else {
      rows=[["Distância média ao Sol",solarKm[name]],["Distância média à Terra (modelo)",earthMean[name]]];
      note=name==="Terra"?"A distância ao próprio planeta é zero. Zero não possui uma representação normalizada em notação científica.":modelNote;
    }
    document.getElementById("distanceList").replaceChildren(...rows.map(([label,km])=>distanceRow(label,km)));
    document.getElementById("distanceNote").textContent=note;
  }

  function stat(label, value) {
    const cell = document.createElement("div"); cell.className = "info-stat";
    const lbl = document.createElement("span"); lbl.className="stat-label"; lbl.textContent=label;
    const val = document.createElement("span"); val.className="stat-value"; val.textContent=value;
    cell.append(lbl, val); return cell;
  }
  function relatedButton(name, category, planet) {
    const btn = document.createElement("button");
    btn.type="button"; btn.className="moon-chip"; btn.textContent=name;
    btn.onclick=() => showAstroInfo(name, category, planet);
    return btn;
  }
  function showAstroInfo(name, category="planet", hostPlanet=null) {
    const title = document.getElementById("astroTitle");
    const stats = document.getElementById("astroStats");
    const related = document.getElementById("astroRelated");
    const relatedSection = document.getElementById("astroRelatedSection");
    const relatedTitle = document.getElementById("astroRelatedTitle");
    const source = document.getElementById("astroSource");
    let entry, entries, sourceUrl, parentName=null;
    if (category === "sun") {
      entry = sunFact; entries = entry.stats; sourceUrl=entry.source;
    } else if (category === "belt") {
      entry = beltFact; entries = entry.stats; sourceUrl=entry.source;
    } else if (category === "moon") {
      const moon = (moonsByPlanet[hostPlanet] || []).find(m => m.name === name);
      if (!moon) return;
      entry = moonFacts[name]; parentName = hostPlanet;
      entries = [["Diâmetro aproximado",entry.diameter], ["Planeta",hostPlanet],
                 ["Período orbital", moon.period.toLocaleString("pt-BR", {maximumFractionDigits:3}) + " dias terrestres"],
                 ["Sentido da órbita",moon.retrograde ? "Retrógrado" : "Prógrado (no modelo)"]];
      entry = {...entry, type:"Satélite natural", intro:`${name} é uma lua de ${hostPlanet}.`};
      sourceUrl = "https://science.nasa.gov/solar-system/moons/facts/";
    } else {
      entry = planetFacts[name]; if (!entry) return;
      const b = bodies.find(p=>p.name===name);
      entries = [["Diâmetro",entry.diameter],
                 ["Ano (órbita solar)", b.period.toLocaleString("pt-BR") + " dias terrestres"],
                 ["Rotação",entry.rotation], ["Gravidade",entry.gravity]];
      sourceUrl = "https://science.nasa.gov/solar-system/planets/";
    }
    title.textContent=name;
    document.getElementById("astroCategory").textContent=entry.type;
    document.getElementById("astroIntro").textContent=entry.intro;
    document.getElementById("astroFeature").textContent=entry.feature;
    stats.replaceChildren(...entries.map(([l,v]) => stat(l,v)));
    renderDistances(name,category,hostPlanet);
    related.replaceChildren(); relatedSection.hidden=true;
    if (category === "planet") {
      const moons = moonsByPlanet[name] || [];
      relatedSection.hidden=false;
      relatedTitle.textContent = moons.length ? `Luas mostradas (${moons.length})` : "Satélites naturais";
      if (moons.length) {
        moons.forEach(m=>related.appendChild(relatedButton(m.name,"moon",name)));
      } else {
        const note = document.createElement("p"); note.textContent = "Nenhuma lua natural conhecida."; note.style.color="#c5d3e2"; related.appendChild(note);
      }
    } else if (category === "moon") {
      relatedSection.hidden=false;
      relatedTitle.textContent = "Sistema de origem";
      related.appendChild(relatedButton(hostPlanet,"planet"));
    }
    source.href = sourceUrl;
    infoPanel.classList.add("open"); infoPanel.setAttribute("aria-hidden","false");
    infoPanel.scrollTop=0;
  }
  function closeAstroInfo() {
    infoPanel.classList.remove("open"); infoPanel.setAttribute("aria-hidden","true");
  }
  // Lista alternativa para telas pequenas, onde um astro pode ocupar poucos pixels.
  const astroPicker = document.getElementById("astroPicker");
  function addPickerGroup(label, items) {
    const group=document.createElement("optgroup"); group.label=label;
    for (const [name,cat,host] of items) {
      const option=document.createElement("option");
      option.value=JSON.stringify([name,cat,host || null]); option.textContent=name;
      group.appendChild(option);
    }
    astroPicker.appendChild(group);
  }
  addPickerGroup("Estrela e cinturão", [["Sol","sun"],["Cinturão de asteroides","belt"]]);
  addPickerGroup("Planetas", bodies.map(b=>[b.name,"planet"]));
  for (const b of bodies) {
    const moons=moonsByPlanet[b.name] || [];
    if (moons.length) addPickerGroup(`Luas de ${b.name}`,moons.map(m=>[m.name,"moon",b.name]));
  }
  astroPicker.addEventListener("change",()=>{
    if (!astroPicker.value) return;
    const [name,category,planet]=JSON.parse(astroPicker.value);
    showAstroInfo(name,category,planet);
    astroPicker.selectedIndex=0;
  });
  document.getElementById("closeAstroInfo").onclick=closeAstroInfo;
  document.addEventListener("keydown", e=>{ if (e.key==="Escape") closeAstroInfo(); });

  // ---- Cinturão principal (entre Marte e Júpiter)
  // Visualização didática: posições e tamanhos não estão em escala real.
  // Em vez de um anel sólido, criamos muitas rochas independentes em 3D.
  const belt = document.createElement("div");
  belt.className = "asteroid-belt";
  system.appendChild(belt);

  // Gerador pseudoaleatório reproduzível: mesma distribuição a cada execução.
  let seed = 21891;
  function randomAsteroid() {
    seed = (Math.imul(1664525, seed) + 1013904223) >>> 0;
    return seed / 4294967296;
  }

  const asteroidColors = ["#998b7a", "#c4ae92", "#847b73", "#b7a18a", "#77736e", "#d0b69a"];
  const asteroidCount = matchMedia("(max-width: 700px)").matches ? 350 : 850;
  const asteroids = [];
  const tau = Math.PI * 2;

  for (let i = 0; i < asteroidCount; i++) {
    // Faixa radial: órbita de Marte = 225 px; órbita de Júpiter = 300 px.
    const radius = 244 + randomAsteroid() * 35;
    const angle = tau * (i + (randomAsteroid() - .5) * .85) / asteroidCount;
    const inclination = (randomAsteroid() - .5) * .045; // até ~1,3 grau
    const node = randomAsteroid() * tau;
    const size = randomAsteroid() < .045 ? 3.6 : 1 + randomAsteroid() * 1.65;

    const el = document.createElement("div");
    el.className = "asteroid";
    el.style.width = size + "px";
    el.style.height = size * (.65 + randomAsteroid() * .55) + "px";
    el.style.background = asteroidColors[Math.floor(randomAsteroid() * asteroidColors.length)];
    belt.appendChild(el);

    asteroids.push({
      el, radius, angle, inclination, node,
      // Aproximação kepleriana usando os raios da própria visualização.
      period: 365 * Math.pow(radius / 180, 1.5)
    });
  }

  belt.addEventListener("click", e => {
    if (e.target.classList.contains("asteroid")) { e.stopPropagation(); showAstroInfo("Cinturão de asteroides", "belt"); }
  });
  const beltLabel = document.createElement("div");
  beltLabel.className = "belt-label label";
  beltLabel.textContent = "Cinturão de asteroides";
  belt.appendChild(beltLabel);
  beltLabel.setAttribute("role", "button"); beltLabel.tabIndex = 0;
  beltLabel.title = "Abrir ficha do cinturão de asteroides";
  beltLabel.addEventListener("click", e => { e.stopPropagation(); showAstroInfo("Cinturão de asteroides", "belt"); });
  beltLabel.addEventListener("keydown", e => {
    if (e.key === "Enter" || e.key === " ") { e.preventDefault(); showAstroInfo("Cinturão de asteroides", "belt"); }
  });
  let showAsteroids = true;

  // ---- Câmera
  let rx = -62, ry = 0;
  let zoom = matchMedia("(max-width: 500px)").matches ? 0.34
           : matchMedia("(max-width: 900px)").matches ? 0.65 : 0.9;
  const initial = { rx, ry, zoom };
  // Seleção estável: memoriza o astro no início do toque e não depende
  // do evento click (o corpo pode mudar de posição entre pressionar e soltar).
  const targets = new Map([[sun, ["Sol", "sun"]], [beltLabel, ["Cinturão de asteroides", "belt"]]]);
  bodies.forEach(b => targets.set(b.el, [b.name, "planet"]));
  allMoons.forEach(m => targets.set(m.el, [m.name, "moon", m.b.name]));
  function getTarget(el) {
    const element = el.closest(".planet, .satellite, .sun, .asteroid, .belt-label");
    return element && (targets.get(element) || (element.classList.contains("asteroid") ? ["Cinturão de asteroides", "belt"] : null));
  }
  const pts = new Map();
  let gesture = null, pinch = 0;
  const clampZoom = v => Math.max(0.25, Math.min(3, v));
  scene.addEventListener("pointerdown", e => {
    if (e.pointerType === "mouse" && e.button !== 0) return;
    pts.set(e.pointerId, {x:e.clientX, y:e.clientY});
    if (pts.size === 1) {
      gesture = {id:e.pointerId, x:e.clientX, y:e.clientY, lastX:e.clientX, lastY:e.clientY,
                 moved:false, target:getTarget(e.target)};
    } else {
      if (gesture) gesture.moved = true;
      const [a,b] = [...pts.values()];
      pinch = Math.hypot(a.x-b.x,a.y-b.y);
    }
    scene.setPointerCapture(e.pointerId);
  });
  scene.addEventListener("pointermove", e => {
    if (!pts.has(e.pointerId)) return;
    pts.set(e.pointerId, {x:e.clientX, y:e.clientY});
    if (pts.size >= 2) {
      const [a,b] = [...pts.values()];
      const d = Math.hypot(a.x-b.x,a.y-b.y);
      if (pinch > 0) zoom = clampZoom(zoom * d/pinch);
      pinch = d;
      if (gesture) gesture.moved = true;
      return;
    }
    if (!gesture || gesture.id !== e.pointerId) return;
    if (Math.hypot(e.clientX-gesture.x,e.clientY-gesture.y) > 7) gesture.moved=true;
    if (gesture.moved) {
      scene.classList.add("dragging");
      ry += (e.clientX-gesture.lastX)*.3;
      rx = Math.max(-90, Math.min(90, rx-(e.clientY-gesture.lastY)*.3));
    }
    gesture.lastX=e.clientX; gesture.lastY=e.clientY;
  });
  function finishGesture(e, cancelled=false) {
    if (!pts.has(e.pointerId)) return;
    if (!cancelled && pts.size === 1 && gesture && gesture.id === e.pointerId && !gesture.moved &&
        Math.hypot(e.clientX-gesture.x,e.clientY-gesture.y)<=7 && gesture.target) {
      showAstroInfo(...gesture.target);
    }
    pts.delete(e.pointerId);
    if (scene.hasPointerCapture(e.pointerId)) scene.releasePointerCapture(e.pointerId);
    if (pts.size === 0) { gesture=null; scene.classList.remove("dragging"); }
    pinch=0;
  }
  scene.addEventListener("pointerup", e=>finishGesture(e));
  scene.addEventListener("pointercancel", e=>finishGesture(e,true));
  scene.addEventListener("lostpointercapture", e=>finishGesture(e,true));
  // Captura de ponteiro redireciona o clique ao cenário; evita ações duplicadas.
  scene.addEventListener("click",e=>{if(e.detail>0){e.stopPropagation();}},true);
  scene.addEventListener("wheel", e => {
    e.preventDefault();
    zoom=clampZoom(zoom*(e.deltaY<0?1.08:.92));
  }, {passive:false});

  // ---- Controles
  let paused = false, speed = 1;
  let showMoons = true;
  const btnPause = document.getElementById("btnPause");
  btnPause.onclick = () => { paused = !paused; btnPause.textContent = paused ? "▶ Continuar" : "⏸ Pausar"; };
  document.getElementById("speed").oninput = e => speed = parseFloat(e.target.value);
  document.getElementById("chkOrbits").onchange = e => {
    orbitEls.forEach(o => o.style.display = e.target.checked ? "" : "none");
    moonOrbitEls.forEach(o => o.style.display = e.target.checked && showMoons ? "" : "none");
  };
  document.getElementById("chkMoons").onchange = e => {
    showMoons = e.target.checked;
    allMoons.forEach(m => m.el.style.display = showMoons ? "" : "none");
    moonOrbitEls.forEach(o => o.style.display = showMoons && document.getElementById("chkOrbits").checked ? "" : "none");
  };
  document.getElementById("chkMoonNames").onchange = e => {
    document.querySelectorAll(".moon-label").forEach(label => label.style.display = e.target.checked ? "block" : "none");
  };
  document.getElementById("chkAsteroids").onchange = e => {
    showAsteroids = e.target.checked;
    belt.style.display = showAsteroids ? "" : "none";
  };
  document.getElementById("chkLabels").onchange = e =>
    document.querySelectorAll(".label").forEach(l => l.style.display = e.target.checked ? "" : "none");
  document.getElementById("btnReset").onclick = () => { rx = initial.rx; ry = initial.ry; zoom = initial.zoom; };

  // ---- Animação
  let last = performance.now();
  function frame(now) {
    const dt = (now - last) / 1000; last = now;

    if (!paused && pts.size === 0) {
      bodies.forEach(b => {
        // 1 segundo real ≈ 20 dias simulados na velocidade 1
        b.angle += (2 * Math.PI / b.period) * 20 * speed * dt;
      });
      allMoons.forEach(m => {
        const direction = m.retrograde ? -1 : 1;
        m.angle = (m.angle + direction * tau * dt * speed / m.visualSecondsPerOrbit) % tau;
      });
      asteroids.forEach(a => {
        a.angle += (tau / a.period) * 20 * speed * dt;
        if (a.angle >= tau) a.angle %= tau;
      });
    }

    system.style.transform = `scale(${zoom}) rotateX(${rx}deg) rotateY(${ry}deg)`;

    // Billboard: cancela a rotação da câmera para os astros ficarem sempre "de frente"
    const face = `rotateY(${-ry}deg) rotateX(${-rx}deg)`;
    sun.style.transform = face;

    bodies.forEach(b => {
      const x = Math.cos(b.angle) * b.orbit;
      const z = Math.sin(b.angle) * b.orbit;
      b.el.style.transform = `translate3d(${x}px, 0, ${z}px) ${face}`;
    });

    // Órbitas lunares acompanham o planeta. A Lua não gira ao redor do Sol
    // como satélite independente: sua posição é relativa à posição terrestre.
    if (showMoons) {
      for (const m of allMoons) {
        const x = Math.cos(m.b.angle) * m.b.orbit;
        const z = Math.sin(m.b.angle) * m.b.orbit;
        const incl = m.inclination * Math.PI / 180;
        const dx = Math.cos(m.angle) * m.radius;
        const dz = Math.sin(m.angle) * m.radius * Math.cos(incl);
        const dy = Math.sin(m.angle) * m.radius * Math.sin(incl);
        m.el.style.transform = `translate3d(${(x + dx).toFixed(2)}px, ${dy.toFixed(2)}px, ${(z + dz).toFixed(2)}px) ${face}`;
        m.orbitEl.style.transform = `translate3d(${x.toFixed(2)}px, 0px, ${z.toFixed(2)}px) rotateX(${90 - m.inclination}deg)`;
      }
    }

    // Cada asteroide segue sua própria trajetória circular levemente inclinada.
    // O cinturão respeita os controles de pausa, velocidade e visibilidade.
    if (showAsteroids) {
      for (const a of asteroids) {
        const x = Math.cos(a.angle) * a.radius;
        const z = Math.sin(a.angle) * a.radius;
        const y = Math.sin(a.angle - a.node) * a.radius * Math.sin(a.inclination);
        a.el.style.transform = `translate3d(${x.toFixed(2)}px, ${y.toFixed(2)}px, ${z.toFixed(2)}px) ${face}`;
      }
      // Uma única legenda discreta, posicionada na borda da faixa.
      const labelAngle = -.38;
      beltLabel.style.transform = `translate3d(${Math.cos(labelAngle)*266}px, -10px, ${Math.sin(labelAngle)*266}px) ${face}`;
    }

    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
</script>
</body>
</html>
'''

components.html(HTML, height=850, scrolling=False)
