/**
 * ============================================================================
 * CELESTIAL METAPHYSICAL RITUAL SYSTEM (TỨ LINH QUY TỤ - BÁT QUÁI CỬU CUNG)
 * High-Fidelity 3D WebGL Metaphysical Ceremony for Imperial Tử Vi
 * Framework: Three.js (r128) - Procedural PBR & Dynamic Catmull-Rom Splines
 * ============================================================================
 */

(function () {
  "use strict";

  // Web Audio Context for Imperial Temple Soundscape
  let audioCtx = null;

  function initAudio() {
    try {
      if (!audioCtx && (window.AudioContext || window.webkitAudioContext)) {
        const AudioContextClass = window.AudioContext || window.webkitAudioContext;
        audioCtx = new AudioContextClass();
      }
      if (audioCtx && audioCtx.state === "suspended") {
        audioCtx.resume();
      }
    } catch (e) {
      console.warn("Web Audio not available:", e);
    }
  }

  // Synthesize Resonant Bronze Temple Bell (Chuông Đồng Cổ)
  function playTempleBell(freq = 216, duration = 4.2, vol = 0.45) {
    if (!audioCtx) initAudio();
    if (!audioCtx) return;

    try {
      const now = audioCtx.currentTime;
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();

      osc.type = "sine";
      osc.frequency.setValueAtTime(freq, now);
      osc.frequency.exponentialRampToValueAtTime(freq * 0.985, now + duration);

      gain.gain.setValueAtTime(0.001, now);
      gain.gain.linearRampToValueAtTime(vol, now + 0.04);
      gain.gain.exponentialRampToValueAtTime(0.0001, now + duration);

      osc.connect(gain);
      gain.connect(audioCtx.destination);

      osc.start(now);
      osc.stop(now + duration);
    } catch (e) {}
  }

  // Synthesize Ethereal Star Chime (Chuông Gió Vạn Tinh)
  function playStarChime() {
    if (!audioCtx) initAudio();
    if (!audioCtx) return;

    try {
      const notes = [587.33, 659.25, 880.0, 1046.5, 1318.51]; // D5, E5, A5, C6, E6
      notes.forEach((freq, idx) => {
        const now = audioCtx.currentTime + idx * 0.07;
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();

        osc.type = "triangle";
        osc.frequency.setValueAtTime(freq, now);

        gain.gain.setValueAtTime(0.001, now);
        gain.gain.linearRampToValueAtTime(0.12, now + 0.02);
        gain.gain.exponentialRampToValueAtTime(0.0001, now + 1.8);

        osc.connect(gain);
        gain.connect(audioCtx.destination);

        osc.start(now);
        osc.stop(now + 1.8);
      });
    } catch (e) {}
  }

  // Sacred Incantations for the HUD
  const celestialChants = [
    "✦ Bước 1/5: Khởi động Bát Trận Càn Khôn • Nạp Can Chi Tứ Trụ...",
    "✦ Bước 2/5: An vị 14 Chính Tinh & Tứ Hóa Phi Tinh (Lộc • Quyền • Khoa • Kỵ)...",
    "✦ Bước 3/5: Phối hợp Bát Tự Hà Lạc, Dụng Thần & Đại Vận 120 Năm...",
    "✦ Bước 4/5: Khắc xuất Sách Tử Vi Toàn Thư Hoàng Gia PDF & Bản Đồ Vận Mệnh...",
    "✦ Bước 5/5: Vạn Tinh Quy Tông • Chuẩn bị Khởi Mở Thiên Bàn Hoàng Gia! ✦"
  ];
  let chantIdx = 0;
  let chantInterval = null;
  let countdownSec = 10;
  let countdownInterval = null;

  // =========================================================================
  // THREE.JS 3D SCENE & RIG
  // =========================================================================
  let scene, camera, renderer, clock;
  let animId = null;
  let isConverging = false;
  let convergenceProgress = 0;
  let ceremonyTime = 0;
  let safetyTimeout = null;

  // Lifecycle State Machine
  let ceremonyActive = false;
  let ceremonyDismissed = false;
  let callbackFired = false;
  let pendingCallback = null;

  // Scene Objects
  let astrolabeGroup;
  let starField, floatingEmbers;
  let keyLight, fillLight, rimLight, centerLight;

  // Continuous Dragon Geometry & Rig
  const DRAGON_RINGS = 36;
  const DRAGON_RADIAL_SEGS = 10;
  let dragonGroup;
  let dragonBodyMesh, dragonBodyGeo;
  let dragonSpinePoints = [];
  let dragonDorsalFins = [];
  let dragonLegs = [];
  let dragonHeadGroup, dragonLowerJaw;
  let dragonWhiskersLeft = [], dragonWhiskersRight = [];
  let dragonTailFins = [];

  // Phoenix Geometry & Rig
  let phoenixGroup;
  let phoenixWings = { leftShoulder: null, leftElbow: null, rightShoulder: null, rightElbow: null };
  let phoenixTailRibbons = [];

  // Tortoise Geometry & Rig
  let turtleGroup, tortoiseFlippers = { fl: null, fr: null, bl: null, br: null }, tortoiseHead;

  // Generate soft circular luminous alpha texture for point particles
  function createSoftParticleTexture(activeThree) {
    try {
      if (typeof document === "undefined" || !document.createElement) return null;
      const canvas = document.createElement("canvas");
      if (!canvas || typeof canvas.getContext !== "function") return null;
      canvas.width = 64;
      canvas.height = 64;
      const ctx = canvas.getContext("2d");
      if (!ctx) return null;

      const grad = ctx.createRadialGradient(32, 32, 0, 32, 32, 30);
      grad.addColorStop(0.0, "rgba(255, 255, 255, 1.0)");
      grad.addColorStop(0.2, "rgba(254, 240, 138, 0.85)");
      grad.addColorStop(0.5, "rgba(245, 158, 11, 0.3)");
      grad.addColorStop(0.85, "rgba(217, 119, 6, 0.06)");
      grad.addColorStop(1.0, "rgba(0, 0, 0, 0.0)");

      ctx.fillStyle = grad;
      ctx.fillRect(0, 0, 64, 64);

      if (!activeThree || !activeThree.CanvasTexture) return null;
      const texture = new activeThree.CanvasTexture(canvas);
      texture.needsUpdate = true;
      return texture;
    } catch (e) {
      console.warn("createSoftParticleTexture error:", e);
      return null;
    }
  }

  // Generate crisp Taiji (Yin-Yang) texture on Canvas
  function createTaijiTexture() {
    try {
      const activeThree = window.THREE || (typeof THREE !== "undefined" ? THREE : null);
      if (typeof document === "undefined" || !document.createElement) return null;
      const canvas = document.createElement("canvas");
      if (!canvas || typeof canvas.getContext !== "function") return null;
      canvas.width = 512;
      canvas.height = 512;
      const ctx = canvas.getContext("2d");
      if (!ctx) return null;
      const cx = 256, cy = 256, r = 240;

      // Outer bronze border ring
      ctx.beginPath();
      ctx.arc(cx, cy, r + 8, 0, Math.PI * 2);
      ctx.strokeStyle = "#8c6d28";
      ctx.lineWidth = 14;
      ctx.stroke();

      // Dark Half (Deep Midnight Indigo)
      ctx.beginPath();
      ctx.arc(cx, cy, r, -Math.PI / 2, Math.PI / 2, false);
      ctx.fillStyle = "#0c1527";
      ctx.fill();

      // Light Half (Antique Burnished Bronze-Gold)
      ctx.beginPath();
      ctx.arc(cx, cy, r, Math.PI / 2, -Math.PI / 2, false);
      ctx.fillStyle = "#c49a3c";
      ctx.fill();

      // Top small curve (Light)
      ctx.beginPath();
      ctx.arc(cx, cy - r / 2, r / 2, 0, Math.PI * 2);
      ctx.fillStyle = "#c49a3c";
      ctx.fill();

      // Bottom small curve (Dark)
      ctx.beginPath();
      ctx.arc(cx, cy + r / 2, r / 2, 0, Math.PI * 2);
      ctx.fillStyle = "#0c1527";
      ctx.fill();

      // Dark dot in light
      ctx.beginPath();
      ctx.arc(cx, cy - r / 2, r / 6, 0, Math.PI * 2);
      ctx.fillStyle = "#0c1527";
      ctx.fill();

      // Light dot in dark
      ctx.beginPath();
      ctx.arc(cx, cy + r / 2, r / 6, 0, Math.PI * 2);
      ctx.fillStyle = "#c49a3c";
      ctx.fill();

      if (!activeThree || !activeThree.CanvasTexture) return null;
      const texture = new activeThree.CanvasTexture(canvas);
      texture.needsUpdate = true;
      return texture;
    } catch (e) {
      console.warn("createTaijiTexture warning:", e);
      return null;
    }
  }

  // Initialize Three.js Scene with PBR Lighting Rig
  function initThreeScene() {
    try {
      const activeThree = window.THREE || (typeof THREE !== "undefined" ? THREE : null);
      const canvas = document.getElementById("three-celestial-canvas");
      if (!canvas || !activeThree) {
        console.warn("Three.js or Canvas not available");
        return;
      }

      const width = window.innerWidth;
      const height = window.innerHeight;

      if (!scene) {
        scene = new activeThree.Scene();
        clock = new activeThree.Clock();

        camera = new activeThree.PerspectiveCamera(50, width / height, 0.1, 2000);
        camera.position.set(0, 26, 88);
        camera.lookAt(0, 12, 0);

        renderer = new activeThree.WebGLRenderer({
          canvas: canvas,
          alpha: true,
          antialias: true,
          powerPreference: "high-performance"
        });
        renderer.setSize(width, height);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));

        // Film-grade Color Pipeline for Three.js r128 (No blown-out neon yellow)
        if (activeThree.ACESFilmicToneMapping) {
          renderer.toneMapping = activeThree.ACESFilmicToneMapping;
          renderer.toneMappingExposure = 0.95;
        }
        if (activeThree.sRGBEncoding) {
          renderer.outputEncoding = activeThree.sRGBEncoding;
        }

        window.addEventListener("resize", onWindowResize);

        // 1. Cinema-grade Lighting Rig (Key, Fill, Rim, Ambient, Point)
        setupLightingRig(activeThree);

        // 2. Build 3D Metaphysical Elements
        buildCosmicStarField(activeThree);
        buildAstrolabeMandala(activeThree);
        buildSculptedImperialDragon(activeThree);
        buildSculptedImperialPhoenix(activeThree);
        buildSculptedSacredTortoise(activeThree);
      } else {
        renderer.setSize(width, height);
        camera.aspect = width / height;
        camera.updateProjectionMatrix();
        if (clock) clock.start();
      }

      // Reset runtime states
      ceremonyTime = 0;
      isConverging = false;
      convergenceProgress = 0;
      camera.position.set(0, 26, 88);
      camera.lookAt(0, 12, 0);
    } catch (err) {
      console.warn("initThreeScene warning:", err);
    }
  }

  function onWindowResize() {
    if (!camera || !renderer) return;
    const w = window.innerWidth;
    const h = window.innerHeight;
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
    renderer.setSize(w, h);
  }

  // Setup Three-Point PBR Lighting Rig
  function setupLightingRig(activeThree) {
    // Ambient Light: Deep celestial indigo/warmth
    const ambientLight = new activeThree.AmbientLight(0x161324, 0.9);
    scene.add(ambientLight);

    // Key Light: Warm golden sunlight from upper-front-right
    keyLight = new activeThree.DirectionalLight(0xfff6e8, 1.4);
    keyLight.position.set(35, 52, 42);
    scene.add(keyLight);

    // Fill Light: Soft celestial blue fill from opposite flank
    fillLight = new activeThree.DirectionalLight(0x527299, 0.65);
    fillLight.position.set(-40, 22, -30);
    scene.add(fillLight);

    // Rim Light: Amber backlight highlighting animal silhouettes
    rimLight = new activeThree.DirectionalLight(0xf59e0b, 1.15);
    rimLight.position.set(0, 42, -50);
    scene.add(rimLight);

    // Center Core Light: Breathing golden illumination from mandala center
    centerLight = new activeThree.PointLight(0xd97706, 0.95, 120, 1.8);
    centerLight.position.set(0, 5, 0);
    scene.add(centerLight);
  }

  // 1. Cosmic Deep Space Starfield & Ascending Embers (Circular Soft Alpha Particles)
  function buildCosmicStarField(activeThree) {
    const isMobile = (typeof window !== "undefined" && window.innerWidth <= 600);
    const starCount = isMobile ? 220 : 500;
    const starGeo = new activeThree.BufferGeometry();
    const starPos = new Float32Array(starCount * 3);
    const starColors = new Float32Array(starCount * 3);

    const palette = [
      new activeThree.Color(0xd4af37), // Antique Gold
      new activeThree.Color(0x93c5fd), // Soft Celestial Blue
      new activeThree.Color(0xfef3c7), // Warm Pearl White
      new activeThree.Color(0xb45309)  // Muted Amber
    ];

    for (let i = 0; i < starCount; i++) {
      const u = Math.random();
      const v = Math.random();
      const theta = u * 2.0 * Math.PI;
      const phi = Math.acos(2.0 * v - 1.0);
      const r = 180 + Math.random() * 420;

      starPos[i * 3] = r * Math.sin(phi) * Math.cos(theta);
      starPos[i * 3 + 1] = r * Math.sin(phi) * Math.sin(theta);
      starPos[i * 3 + 2] = r * Math.cos(phi);

      const col = palette[Math.floor(Math.random() * palette.length)];
      starColors[i * 3] = col.r;
      starColors[i * 3 + 1] = col.g;
      starColors[i * 3 + 2] = col.b;
    }

    starGeo.setAttribute("position", new activeThree.BufferAttribute(starPos, 3));
    starGeo.setAttribute("color", new activeThree.BufferAttribute(starColors, 3));

    const softParticleTex = createSoftParticleTexture(activeThree);

    const starMat = new activeThree.PointsMaterial({
      size: isMobile ? 0.85 : 1.25,
      vertexColors: true,
      transparent: true,
      opacity: 0.65,
      map: softParticleTex || null,
      depthWrite: false,
      blending: activeThree.AdditiveBlending
    });

    starField = new activeThree.Points(starGeo, starMat);
    scene.add(starField);

    // Ascending Ethereal Incense Embers
    const emberCount = isMobile ? 45 : 95;
    const emberGeo = new activeThree.BufferGeometry();
    const emberPos = new Float32Array(emberCount * 3);
    for (let i = 0; i < emberCount; i++) {
      emberPos[i * 3] = (Math.random() - 0.5) * 80;
      emberPos[i * 3 + 1] = Math.random() * 45;
      emberPos[i * 3 + 2] = (Math.random() - 0.5) * 80;
    }
    emberGeo.setAttribute("position", new activeThree.BufferAttribute(emberPos, 3));
    const emberMat = new activeThree.PointsMaterial({
      size: isMobile ? 0.95 : 1.35,
      color: 0xf59e0b,
      transparent: true,
      opacity: 0.5,
      map: softParticleTex || null,
      depthWrite: false,
      blending: activeThree.AdditiveBlending
    });
    floatingEmbers = new activeThree.Points(emberGeo, emberMat);
    scene.add(floatingEmbers);
  }

  // 2. Bát Quái Cửu Cung Ground Astrolabe (Fine Bronze Filigree & Slender Rings)
  function buildAstrolabeMandala(activeThree) {
    astrolabeGroup = new activeThree.Group();
    astrolabeGroup.position.set(0, 0, 0);

    const bronzeMat = new activeThree.MeshStandardMaterial({
      color: 0x5a421b,
      roughness: 0.62,
      metalness: 0.58
    });

    const goldMat = new activeThree.MeshStandardMaterial({
      color: 0x96772a,
      roughness: 0.55,
      metalness: 0.6
    });

    // Tier 1: Slender Outer Cloud & Lightning Rim (Vân Lôi Họa)
    const outerRingGeo = new activeThree.RingGeometry(38.0, 38.6, 64);
    const outerRing = new activeThree.Mesh(outerRingGeo, bronzeMat);
    outerRing.rotation.x = -Math.PI / 2;
    astrolabeGroup.add(outerRing);

    // Tier 2: Slender 12 Địa Chi Ring with bronze studs
    const midRingGeo = new activeThree.RingGeometry(26.0, 26.5, 64);
    const midRing = new activeThree.Mesh(midRingGeo, goldMat);
    midRing.rotation.x = -Math.PI / 2;
    astrolabeGroup.add(midRing);

    // 12 Stud Medallions around circumference
    for (let i = 0; i < 12; i++) {
      const ang = (i / 12) * Math.PI * 2;
      const stud = new activeThree.Mesh(
        new activeThree.CylinderGeometry(0.7, 0.75, 0.35, 12),
        goldMat
      );
      stud.position.set(Math.cos(ang) * 26.25, 0.18, Math.sin(ang) * 26.25);
      astrolabeGroup.add(stud);
    }

    // Tier 3: 8 Trigram Inner Bronze Ring (Bát Quái Bàn)
    const innerRingGeo = new activeThree.RingGeometry(16.0, 16.4, 64);
    const innerRing = new activeThree.Mesh(innerRingGeo, bronzeMat);
    innerRing.rotation.x = -Math.PI / 2;
    astrolabeGroup.add(innerRing);

    // 8 Sacred Trigram Tablets (☰ ☱ ☲ ☳ ☴ ☵ ☶ ☷)
    for (let i = 0; i < 8; i++) {
      const angle = (i / 8) * Math.PI * 2;
      const x = Math.cos(angle) * 21.0;
      const z = Math.sin(angle) * 21.0;

      const tablet = new activeThree.Mesh(
        new activeThree.BoxGeometry(1.8, 0.35, 2.4),
        goldMat
      );
      tablet.position.set(x, 0.22, z);
      tablet.rotation.y = -angle;
      astrolabeGroup.add(tablet);

      // Ethereal vertical light pillar rising from each trigram (subtle, non-glaring)
      const beamGeo = new activeThree.CylinderGeometry(0.08, 0.08, 16, 8);
      const beamMat = new activeThree.MeshBasicMaterial({
        color: 0xd4af37,
        transparent: true,
        opacity: 0.1,
        blending: activeThree.AdditiveBlending
      });
      const beam = new activeThree.Mesh(beamGeo, beamMat);
      beam.position.set(x, 8, z);
      astrolabeGroup.add(beam);
    }

    // Centerpiece: Taiji (Yin-Yang) Bronze Relief Disc
    const taijiTexture = createTaijiTexture();
    const taijiGeo = new activeThree.CylinderGeometry(8.5, 8.5, 0.45, 48);
    const taijiMat = new activeThree.MeshStandardMaterial({
      map: taijiTexture || null,
      color: taijiTexture ? 0xffffff : 0x96772a,
      roughness: 0.45,
      metalness: 0.5
    });
    const taijiMesh = new activeThree.Mesh(taijiGeo, taijiMat);
    taijiMesh.position.y = 0.22;
    taijiMesh.name = "taijiCenter";
    astrolabeGroup.add(taijiMesh);

    scene.add(astrolabeGroup);
  }

  // 3. HOÀNG LONG (Continuous Tapered Tube Mesh along Spline + Sculpted Head)
  function buildSculptedImperialDragon(activeThree) {
    dragonGroup = new activeThree.Group();
    dragonSpinePoints = [];
    dragonDorsalFins = [];
    dragonLegs = [];
    dragonWhiskersLeft = [];
    dragonWhiskersRight = [];
    dragonTailFins = [];

    const goldScaleMat = new activeThree.MeshStandardMaterial({
      color: 0xc4912b,
      roughness: 0.38,
      metalness: 0.65,
      side: activeThree.DoubleSide
    });

    const dorsalFinMat = new activeThree.MeshStandardMaterial({
      color: 0x9a3412,
      roughness: 0.45,
      metalness: 0.4
    });

    // -------------------------------------------------------------------------
    // A. Build Continuous Tube Geometry (ZERO Gaps, Silky Smooth Skin)
    // -------------------------------------------------------------------------
    const totalVertices = DRAGON_RINGS * DRAGON_RADIAL_SEGS;
    const vertexPositions = new Float32Array(totalVertices * 3);
    const vertexUvs = new Float32Array(totalVertices * 2);
    const indices = [];

    for (let r = 0; r < DRAGON_RINGS; r++) {
      const v = r / (DRAGON_RINGS - 1);
      for (let s = 0; s < DRAGON_RADIAL_SEGS; s++) {
        const u = s / DRAGON_RADIAL_SEGS;
        const vIdx = r * DRAGON_RADIAL_SEGS + s;
        vertexUvs[vIdx * 2] = u;
        vertexUvs[vIdx * 2 + 1] = v;

        if (r < DRAGON_RINGS - 1) {
          const nextS = (s + 1) % DRAGON_RADIAL_SEGS;
          const a = r * DRAGON_RADIAL_SEGS + s;
          const b = (r + 1) * DRAGON_RADIAL_SEGS + s;
          const c = (r + 1) * DRAGON_RADIAL_SEGS + nextS;
          const d = r * DRAGON_RADIAL_SEGS + nextS;

          indices.push(a, b, c);
          indices.push(a, c, d);
        }
      }
    }

    dragonBodyGeo = new activeThree.BufferGeometry();
    dragonBodyGeo.setAttribute("position", new activeThree.BufferAttribute(vertexPositions, 3));
    dragonBodyGeo.setAttribute("uv", new activeThree.BufferAttribute(vertexUvs, 2));
    dragonBodyGeo.setIndex(indices);

    dragonBodyMesh = new activeThree.Mesh(dragonBodyGeo, goldScaleMat);
    dragonGroup.add(dragonBodyMesh);

    // -------------------------------------------------------------------------
    // B. Dorsal Spines along the Continuous Skin
    // -------------------------------------------------------------------------
    for (let r = 1; r < DRAGON_RINGS - 2; r += 2) {
      const finGroup = new activeThree.Group();
      const finScale = (1.0 - (r / DRAGON_RINGS) * 0.65);
      const finMesh = new activeThree.Mesh(
        new activeThree.ConeGeometry(0.55 * finScale, 2.2 * finScale, 4),
        dorsalFinMat
      );
      finMesh.position.y = 1.0 * finScale;
      finMesh.rotation.x = -0.3;
      finGroup.add(finMesh);
      finGroup.userData = { ringIndex: r };

      dragonDorsalFins.push(finGroup);
      dragonGroup.add(finGroup);
    }

    // -------------------------------------------------------------------------
    // C. Articulated Forelegs & Hindlegs with Claws
    // -------------------------------------------------------------------------
    const leftForeleg = createDragonLeg(activeThree, goldScaleMat, true);
    const rightForeleg = createDragonLeg(activeThree, goldScaleMat, false);
    leftForeleg.userData = { ringIndex: 5, isLeft: true };
    rightForeleg.userData = { ringIndex: 5, isLeft: false };

    const leftHindleg = createDragonLeg(activeThree, goldScaleMat, true);
    const rightHindleg = createDragonLeg(activeThree, goldScaleMat, false);
    leftHindleg.userData = { ringIndex: 22, isLeft: true };
    rightHindleg.userData = { ringIndex: 22, isLeft: false };

    dragonLegs.push(leftForeleg, rightForeleg, leftHindleg, rightHindleg);
    dragonGroup.add(leftForeleg);
    dragonGroup.add(rightForeleg);
    dragonGroup.add(leftHindleg);
    dragonGroup.add(rightHindleg);

    // -------------------------------------------------------------------------
    // D. Flame Tuft at Tail Tip
    // -------------------------------------------------------------------------
    const tailTuftGroup = new activeThree.Group();
    tailTuftGroup.userData = { ringIndex: DRAGON_RINGS - 1 };
    for (let f = 0; f < 5; f++) {
      const tFin = new activeThree.Mesh(
        new activeThree.ConeGeometry(0.35, 3.8, 4),
        dorsalFinMat
      );
      tFin.position.set((f - 2) * 0.35, 0, -1.8);
      tFin.rotation.x = Math.PI / 2;
      tFin.rotation.z = (f - 2) * 0.28;
      tailTuftGroup.add(tFin);
    }
    dragonTailFins.push(tailTuftGroup);
    dragonGroup.add(tailTuftGroup);

    // -------------------------------------------------------------------------
    // E. Organic Sculpted Dragon Head (Ellipsoids & Tapered Snout - NO BOXES!)
    // -------------------------------------------------------------------------
    dragonHeadGroup = new activeThree.Group();

    // 1. Cranium: Smooth Ellipsoid Skull
    const craniumGeo = new activeThree.SphereGeometry(2.1, 16, 12);
    const craniumMesh = new activeThree.Mesh(craniumGeo, goldScaleMat);
    craniumMesh.scale.set(1.05, 0.85, 1.35);
    dragonHeadGroup.add(craniumMesh);

    // 2. Upper Snout: Tapered curved muzzle
    const snoutGeo = new activeThree.CylinderGeometry(1.2, 1.8, 3.2, 14);
    const snoutMesh = new activeThree.Mesh(snoutGeo, goldScaleMat);
    snoutMesh.rotation.x = Math.PI / 2;
    snoutMesh.scale.set(1.0, 0.65, 1.0);
    snoutMesh.position.set(0, -0.2, 2.5);
    dragonHeadGroup.add(snoutMesh);

    // Twin Bulbous Nostrils
    const nostrilGeo = new activeThree.SphereGeometry(0.52, 10, 8);
    const nostrilL = new activeThree.Mesh(nostrilGeo, goldScaleMat);
    nostrilL.scale.set(0.75, 0.6, 0.9);
    nostrilL.position.set(0.75, 0.22, 3.8);
    const nostrilR = new activeThree.Mesh(nostrilGeo, goldScaleMat);
    nostrilR.scale.set(0.75, 0.6, 0.9);
    nostrilR.position.set(-0.75, 0.22, 3.8);
    dragonHeadGroup.add(nostrilL);
    dragonHeadGroup.add(nostrilR);

    // 3. Layered Curved Brow Ridges (Casting Bold Dramatic Shadows)
    const browMat = new activeThree.MeshStandardMaterial({ color: 0x78350f, roughness: 0.45 });
    const eyeMat = new activeThree.MeshPhongMaterial({
      color: 0xdc2626,
      emissive: 0x991b1b,
      specular: 0xffe6a3,
      shininess: 95
    });

    const browGeo = new activeThree.CylinderGeometry(0.42, 0.58, 2.2, 10);
    const leftBrow = new activeThree.Mesh(browGeo, browMat);
    leftBrow.position.set(1.25, 0.62, 1.5);
    leftBrow.rotation.z = -0.4;
    leftBrow.rotation.y = 0.25;
    dragonHeadGroup.add(leftBrow);

    const rightBrow = new activeThree.Mesh(browGeo, browMat);
    rightBrow.position.set(-1.25, 0.62, 1.5);
    rightBrow.rotation.z = 0.4;
    rightBrow.rotation.y = -0.25;
    dragonHeadGroup.add(rightBrow);

    // Glowing Ruby Eyes recessed under brow
    const eyeGeo = new activeThree.SphereGeometry(0.46, 12, 12);
    const leftEye = new activeThree.Mesh(eyeGeo, eyeMat);
    leftEye.position.set(1.15, 0.35, 1.6);
    const rightEye = new activeThree.Mesh(eyeGeo, eyeMat);
    rightEye.position.set(-1.15, 0.35, 1.6);
    dragonHeadGroup.add(leftEye);
    dragonHeadGroup.add(rightEye);

    // 4. Articulated Lower Jaw (Pivoted Open in Mighty Roar)
    const jawGeo = new activeThree.CylinderGeometry(0.9, 1.4, 2.8, 12);
    dragonLowerJaw = new activeThree.Mesh(jawGeo, goldScaleMat);
    dragonLowerJaw.rotation.x = Math.PI / 2;
    dragonLowerJaw.scale.set(0.9, 0.45, 1.0);
    dragonLowerJaw.position.set(0, -0.9, 2.1);
    dragonLowerJaw.rotation.x += 0.26; // Open roar
    dragonHeadGroup.add(dragonLowerJaw);

    // Sharp Ivory Fangs (Nanh ngọc)
    const fangMat = new activeThree.MeshStandardMaterial({ color: 0xfffbeb, roughness: 0.25 });
    const fangGeo = new activeThree.ConeGeometry(0.22, 0.85, 6);
    for (let f = 0; f < 4; f++) {
      const fang = new activeThree.Mesh(fangGeo, fangMat);
      const isTop = f < 2;
      const isL = f % 2 === 0;
      fang.position.set(isL ? 0.85 : -0.85, isTop ? -0.55 : -0.65, 3.2);
      fang.rotation.x = isTop ? Math.PI : 0;
      dragonHeadGroup.add(fang);
    }

    // 5. Branching Dragon Antler Horns (Sừng hươu gạc rồng)
    const hornMat = new activeThree.MeshStandardMaterial({
      color: 0x9a7b2c,
      roughness: 0.42,
      metalness: 0.55
    });
    const leftHorn = createDragonAntler(activeThree, hornMat, true);
    leftHorn.position.set(1.1, 1.4, -0.6);
    const rightHorn = createDragonAntler(activeThree, hornMat, false);
    rightHorn.position.set(-1.1, 1.4, -0.6);
    dragonHeadGroup.add(leftHorn);
    dragonHeadGroup.add(rightHorn);

    // 6. Volumetric Flowing Flame Mane (Bờm lửa)
    for (let m = 0; m < 7; m++) {
      const maneGeo = new activeThree.ConeGeometry(0.55, 3.6, 4);
      const maneMesh = new activeThree.Mesh(maneGeo, dorsalFinMat);
      maneMesh.position.set(Math.sin(m * 0.9) * 0.6, 1.0 + m * 0.25, -1.2 - m * 0.4);
      maneMesh.rotation.x = -1.2;
      maneMesh.rotation.z = (m - 3) * 0.18;
      dragonHeadGroup.add(maneMesh);
    }

    dragonGroup.add(dragonHeadGroup);

    // 7. Sinuous Whiskers (10 nodes each)
    const whiskerMat = new activeThree.MeshBasicMaterial({ color: 0xfef08a });
    const whiskerGeo = new activeThree.SphereGeometry(0.16, 6, 6);
    for (let k = 0; k < 10; k++) {
      const wNodeL = new activeThree.Mesh(whiskerGeo, whiskerMat);
      const wNodeR = new activeThree.Mesh(whiskerGeo, whiskerMat);
      scene.add(wNodeL);
      scene.add(wNodeR);
      dragonWhiskersLeft.push(wNodeL);
      dragonWhiskersRight.push(wNodeR);
    }

    scene.add(dragonGroup);
  }

  // Helper: Create 3D Articulated Dragon Leg with Eagle Talons
  function createDragonLeg(activeThree, mat, isLeft) {
    const legGroup = new activeThree.Group();
    const sign = isLeft ? 1 : -1;

    // Thigh
    const thigh = new activeThree.Mesh(new activeThree.CylinderGeometry(0.75, 0.55, 3.2, 8), mat);
    thigh.position.set(sign * 1.5, -1.0, 0);
    thigh.rotation.z = sign * 0.65;
    legGroup.add(thigh);

    // Shin
    const shin = new activeThree.Mesh(new activeThree.CylinderGeometry(0.5, 0.35, 3.0, 8), mat);
    shin.position.set(sign * 2.8, -3.0, 0.4);
    shin.rotation.z = -sign * 0.45;
    legGroup.add(shin);

    // Eagle Claws (3 forward talons, 1 rear talon)
    const clawMat = new activeThree.MeshStandardMaterial({ color: 0x451a03, roughness: 0.3 });
    const clawGeo = new activeThree.ConeGeometry(0.18, 1.4, 5);

    for (let c = 0; c < 3; c++) {
      const claw = new activeThree.Mesh(clawGeo, clawMat);
      claw.position.set(sign * (2.8 + (c - 1) * 0.45), -4.4, 0.9 + c * 0.1);
      claw.rotation.x = Math.PI / 2 + 0.35;
      claw.rotation.z = sign * ((c - 1) * 0.3);
      legGroup.add(claw);
    }

    return legGroup;
  }

  // Helper: Create Majestic Dragon Antler Horn
  function createDragonAntler(activeThree, mat, isLeft) {
    const antler = new activeThree.Group();
    const sign = isLeft ? 1 : -1;

    // Main Beam (Thân sừng chính)
    const mainBeam = new activeThree.Mesh(new activeThree.CylinderGeometry(0.35, 0.6, 5.0, 8), mat);
    mainBeam.position.set(sign * 0.8, 2.2, -1.2);
    mainBeam.rotation.x = -0.55;
    mainBeam.rotation.z = sign * 0.45;
    antler.add(mainBeam);

    // Brow Tine (Gạc trước)
    const browTine = new activeThree.Mesh(new activeThree.CylinderGeometry(0.22, 0.38, 2.4, 6), mat);
    browTine.position.set(sign * 0.4, 1.4, 0.1);
    browTine.rotation.x = 0.55;
    browTine.rotation.z = sign * 0.3;
    antler.add(browTine);

    // Trez Tine (Gạc giữa)
    const trezTine = new activeThree.Mesh(new activeThree.CylinderGeometry(0.18, 0.32, 2.0, 6), mat);
    trezTine.position.set(sign * 1.5, 3.2, -1.5);
    trezTine.rotation.x = -0.3;
    trezTine.rotation.z = sign * 0.8;
    antler.add(trezTine);

    return antler;
  }

  // 4. HỎA PHỤNG (Broad Curved Leaf Feathers + Solid Wing Mantle + 5 Silk Ribbon Tails)
  function buildSculptedImperialPhoenix(activeThree) {
    phoenixGroup = new activeThree.Group();
    phoenixTailRibbons = [];

    const bodyMat = new activeThree.MeshStandardMaterial({
      color: 0x991b1b,
      roughness: 0.36,
      metalness: 0.52
    });

    const goldTrimMat = new activeThree.MeshStandardMaterial({
      color: 0xc4821c,
      roughness: 0.38,
      metalness: 0.65
    });

    // Aerodynamic Teardrop Torso
    const torso = new activeThree.Mesh(
      new activeThree.SphereGeometry(2.2, 14, 14),
      bodyMat
    );
    torso.scale.set(1.0, 1.25, 1.75);
    phoenixGroup.add(torso);

    // Imperial Golden Breastplate
    const breastPlate = new activeThree.Mesh(
      new activeThree.SphereGeometry(1.6, 12, 12, 0, Math.PI, 0, Math.PI),
      goldTrimMat
    );
    breastPlate.position.set(0, -0.4, 1.2);
    breastPlate.scale.set(0.9, 1.2, 0.6);
    phoenixGroup.add(breastPlate);

    // S-curved Graceful Neck
    const neckGroup = new activeThree.Group();
    neckGroup.position.set(0, 1.2, 2.8);
    for (let n = 0; n < 4; n++) {
      const nSeg = new activeThree.Mesh(
        new activeThree.CylinderGeometry(0.8 - n * 0.1, 0.95 - n * 0.1, 1.4, 8),
        bodyMat
      );
      nSeg.position.set(0, n * 1.0, n * 0.4);
      nSeg.rotation.x = -0.3;
      neckGroup.add(nSeg);
    }

    // Sculpted Head with Crest & Beak
    const head = new activeThree.Mesh(new activeThree.SphereGeometry(1.1, 12, 12), bodyMat);
    head.position.set(0, 4.4, 1.8);

    // Golden Raptor Beak
    const beak = new activeThree.Mesh(new activeThree.ConeGeometry(0.45, 2.2, 6), goldTrimMat);
    beak.position.set(0, -0.2, 1.5);
    beak.rotation.x = Math.PI / 2 + 0.35;
    head.add(beak);

    // Topaz Eyes
    const eyeMat = new activeThree.MeshPhongMaterial({ color: 0xf59e0b, specular: 0xffffff, shininess: 90 });
    const eyeL = new activeThree.Mesh(new activeThree.SphereGeometry(0.28, 8, 8), eyeMat);
    eyeL.position.set(0.85, 0.25, 0.6);
    const eyeR = new activeThree.Mesh(new activeThree.SphereGeometry(0.28, 8, 8), eyeMat);
    eyeR.position.set(-0.85, 0.25, 0.6);
    head.add(eyeL);
    head.add(eyeR);

    // Tri-plume Crown Crest (Tam hoa phụng quan)
    for (let c = 0; c < 3; c++) {
      const crestPlume = new activeThree.Mesh(
        new activeThree.ConeGeometry(0.25, 3.2 + (c === 1 ? 0.6 : 0), 4),
        goldTrimMat
      );
      crestPlume.position.set((c - 1) * 0.45, 1.2, -0.8 - c * 0.2);
      crestPlume.rotation.x = -0.9;
      crestPlume.rotation.z = (c - 1) * 0.25;
      head.add(crestPlume);
    }

    neckGroup.add(head);
    phoenixGroup.add(neckGroup);

    // -------------------------------------------------------------------------
    // Broad Curved Leaf Feathers + Solid Wing Mantle (Oriented Facing Camera)
    // -------------------------------------------------------------------------
    const wingFeatherMat = new activeThree.MeshPhongMaterial({
      color: 0x991b1b,
      specular: 0xd97706,
      shininess: 40,
      side: activeThree.DoubleSide
    });

    const wingTipMat = new activeThree.MeshStandardMaterial({
      color: 0xc4821c,
      roughness: 0.38,
      metalness: 0.65,
      side: activeThree.DoubleSide
    });

    // Broad Curved Leaf Feather Shape (Width = 4.2 units, Length = 9.8 units)
    const featherShape = new activeThree.Shape();
    featherShape.moveTo(0, 0);
    featherShape.quadraticCurveTo(2.4, 3.2, 1.4, 7.6);
    featherShape.quadraticCurveTo(0.3, 9.4, 0, 9.8);
    featherShape.quadraticCurveTo(-1.2, 7.2, -1.8, 3.6);
    featherShape.quadraticCurveTo(-1.0, 1.2, 0, 0);
    const featherGeo = new activeThree.ShapeGeometry(featherShape);

    // Solid Wing Mantle Base Shape (Connects Shoulder to Elbow for unbroken silhouette)
    const mantleShape = new activeThree.Shape();
    mantleShape.moveTo(0, 0);
    mantleShape.lineTo(6.0, -0.8);
    mantleShape.quadraticCurveTo(4.2, -4.5, 0, -3.2);
    mantleShape.closePath();
    const mantleGeo = new activeThree.ShapeGeometry(mantleShape);

    // Left Wing Rig
    const leftShoulder = new activeThree.Group();
    leftShoulder.position.set(1.6, 0.8, 1.2);

    // Leading edge arm bone
    const leftBone = new activeThree.Mesh(new activeThree.CylinderGeometry(0.65, 0.4, 5.8, 8), bodyMat);
    leftBone.position.set(2.8, 0, -0.4);
    leftBone.rotation.z = -1.45;
    leftShoulder.add(leftBone);

    // Solid wing base mantle
    const leftMantle = new activeThree.Mesh(mantleGeo, bodyMat);
    leftMantle.rotation.x = Math.PI / 2 - 0.45; // Broad face tilted toward camera
    leftShoulder.add(leftMantle);

    // 4 Broad Secondaries on Left Shoulder (Layered fan blades)
    for (let s = 0; s < 4; s++) {
      const fMesh = new activeThree.Mesh(featherGeo, wingFeatherMat);
      fMesh.position.set(s * 1.35, -0.2, -s * 0.6);
      fMesh.rotation.x = Math.PI / 2 - 0.52; // Tilted facing upward/camera
      fMesh.rotation.y = -0.25;
      fMesh.rotation.z = -0.45 - s * 0.12;
      fMesh.scale.set(0.72, 0.72, 0.72);
      leftShoulder.add(fMesh);
    }

    const leftElbow = new activeThree.Group();
    leftElbow.position.set(5.8, 0, -0.8);
    leftShoulder.add(leftElbow);

    // 5 Broad Primaries on Left Elbow (Sweeping majestic tips)
    for (let p = 0; p < 5; p++) {
      const fMesh = new activeThree.Mesh(featherGeo, p > 2 ? wingTipMat : wingFeatherMat);
      fMesh.position.set(p * 1.2, 0, -p * 0.6);
      fMesh.rotation.x = Math.PI / 2 - 0.52; // Tilted facing upward/camera
      fMesh.rotation.y = -0.32;
      fMesh.rotation.z = -0.8 - p * 0.14;
      fMesh.scale.set(0.92, 0.92, 0.92);
      leftElbow.add(fMesh);
    }

    // Right Wing Rig (Mirror of Left)
    const rightShoulder = new activeThree.Group();
    rightShoulder.position.set(-1.6, 0.8, 1.2);

    const rightBone = new activeThree.Mesh(new activeThree.CylinderGeometry(0.65, 0.4, 5.8, 8), bodyMat);
    rightBone.position.set(-2.8, 0, -0.4);
    rightBone.rotation.z = 1.45;
    rightShoulder.add(rightBone);

    const rightMantle = new activeThree.Mesh(mantleGeo, bodyMat);
    rightMantle.scale.set(-1, 1, 1);
    rightMantle.rotation.x = Math.PI / 2 - 0.45;
    rightShoulder.add(rightMantle);

    for (let s = 0; s < 4; s++) {
      const fMesh = new activeThree.Mesh(featherGeo, wingFeatherMat);
      fMesh.position.set(-s * 1.35, -0.2, -s * 0.6);
      fMesh.rotation.x = Math.PI / 2 - 0.52;
      fMesh.rotation.y = 0.25;
      fMesh.rotation.z = 0.45 + s * 0.12;
      fMesh.scale.set(-0.72, 0.72, 0.72);
      rightShoulder.add(fMesh);
    }

    const rightElbow = new activeThree.Group();
    rightElbow.position.set(-5.8, 0, -0.8);
    rightShoulder.add(rightElbow);

    for (let p = 0; p < 5; p++) {
      const fMesh = new activeThree.Mesh(featherGeo, p > 2 ? wingTipMat : wingFeatherMat);
      fMesh.position.set(-p * 1.2, 0, -p * 0.6);
      fMesh.rotation.x = Math.PI / 2 - 0.52;
      fMesh.rotation.y = 0.32;
      fMesh.rotation.z = 0.8 + p * 0.14;
      fMesh.scale.set(-0.92, 0.92, 0.92);
      rightElbow.add(fMesh);
    }

    phoenixWings.leftShoulder = leftShoulder;
    phoenixWings.leftElbow = leftElbow;
    phoenixWings.rightShoulder = rightShoulder;
    phoenixWings.rightElbow = rightElbow;

    phoenixGroup.add(leftShoulder);
    phoenixGroup.add(rightShoulder);

    // 5 Undulating Silk Tail Streamers (Ngũ Sắc Hỏa Vĩ)
    const tailColors = [0x991b1b, 0xd97706, 0xf59e0b, 0xd97706, 0x991b1b];
    for (let t = 0; t < 5; t++) {
      const ribbonNodes = [];
      const ribbonMat = new activeThree.MeshBasicMaterial({ color: tailColors[t] });
      const ribbonGeo = new activeThree.CylinderGeometry(0.24, 0.38, 1.2, 6);

      for (let n = 0; n < 10; n++) {
        const rNode = new activeThree.Mesh(ribbonGeo, ribbonMat);
        rNode.scale.set(1.0 - n * 0.05, 1.0, 1.0 - n * 0.05);
        phoenixGroup.add(rNode);
        ribbonNodes.push(rNode);

        // Terminal Gold Eyelet Medallion at end of ribbon
        if (n === 9) {
          const eyelet = new activeThree.Mesh(
            new activeThree.TorusGeometry(0.55, 0.14, 8, 16),
            goldTrimMat
          );
          eyelet.position.set(0, -0.6, 0);
          rNode.add(eyelet);
        }
      }
      phoenixTailRibbons.push(ribbonNodes);
    }

    scene.add(phoenixGroup);
  }

  // 5. KIM QUY (Sacred Metaphysical Tortoise / Domed Shell & Swimming Paddles)
  function buildSculptedSacredTortoise(activeThree) {
    turtleGroup = new activeThree.Group();
    turtleGroup.position.set(0, 7, 0);

    const carapaceMat = new activeThree.MeshStandardMaterial({
      color: 0x166534, // Imperial Emerald Green Jade
      roughness: 0.38,
      metalness: 0.58
    });

    const rimMat = new activeThree.MeshStandardMaterial({
      color: 0x96772a, // Antique Bronze Flange
      roughness: 0.45,
      metalness: 0.62
    });

    const skinMat = new activeThree.MeshStandardMaterial({
      color: 0x2e4b36,
      roughness: 0.65,
      metalness: 0.25
    });

    // Domed Carapace (Mai Rùa gồ cao vững chãi)
    const carapaceGeo = new activeThree.SphereGeometry(8.5, 24, 16, 0, Math.PI * 2, 0, Math.PI * 0.5);
    const carapaceMesh = new activeThree.Mesh(carapaceGeo, carapaceMat);
    carapaceMesh.scale.set(1.0, 0.48, 1.25);
    turtleGroup.add(carapaceMesh);

    // Outer Protective Rim Flange (Gờ mai đồng nổi)
    const rimGeo = new activeThree.TorusGeometry(8.6, 0.65, 10, 36);
    const rimMesh = new activeThree.Mesh(rimGeo, rimMat);
    rimMesh.rotation.x = Math.PI / 2;
    rimMesh.scale.set(1.0, 1.25, 0.45);
    turtleGroup.add(rimMesh);

    // Flat Ventral Plastron (Yếm rùa)
    const plastronGeo = new activeThree.CylinderGeometry(8.2, 8.2, 0.6, 24);
    const plastron = new activeThree.Mesh(plastronGeo, rimMat);
    plastron.position.y = -0.3;
    plastron.scale.set(1.0, 1.0, 1.22);
    turtleGroup.add(plastron);

    // Sacred Lạc Thư Jade Tablet on Tortoise Shell
    const tabletGeo = new activeThree.CylinderGeometry(3.8, 4.2, 0.7, 8);
    const tabletMat = new activeThree.MeshStandardMaterial({
      color: 0x96772a,
      roughness: 0.35,
      metalness: 0.65
    });
    const tablet = new activeThree.Mesh(tabletGeo, tabletMat);
    tablet.position.set(0, 4.2, 0.3);
    turtleGroup.add(tablet);

    // 9 Metaphysical Star Dots on Tablet
    const dotMat = new activeThree.MeshBasicMaterial({ color: 0xfef08a });
    const dotGeo = new activeThree.SphereGeometry(0.24, 8, 8);
    const dotPositions = [
      [0, 0], [-1.4, -1.4], [1.4, -1.4], [-1.4, 1.4], [1.4, 1.4],
      [0, -1.8], [0, 1.8], [-1.8, 0], [1.8, 0]
    ];
    dotPositions.forEach(dp => {
      const node = new activeThree.Mesh(dotGeo, dotMat);
      node.position.set(dp[0], 4.6, dp[1] + 0.3);
      turtleGroup.add(node);
    });

    // Sculpted Head & Neck
    const neck = new activeThree.Mesh(new activeThree.CylinderGeometry(1.2, 1.6, 4.0, 10), skinMat);
    neck.position.set(0, 1.2, 8.8);
    neck.rotation.x = Math.PI / 2 - 0.35;
    turtleGroup.add(neck);

    const head = new activeThree.Mesh(new activeThree.SphereGeometry(1.8, 14, 14), skinMat);
    head.scale.set(0.9, 0.75, 1.35);
    head.position.set(0, 2.4, 11.0);

    // Wise Dark Obsidian Eyes
    const tEyeMat = new activeThree.MeshPhongMaterial({ color: 0x0f172a, specular: 0xffffff, shininess: 95 });
    const tEyeL = new activeThree.Mesh(new activeThree.SphereGeometry(0.3, 8, 8), tEyeMat);
    tEyeL.position.set(1.0, 0.35, 0.6);
    const tEyeR = new activeThree.Mesh(new activeThree.SphereGeometry(0.3, 8, 8), tEyeMat);
    tEyeR.position.set(-1.0, 0.35, 0.6);
    head.add(tEyeL);
    head.add(tEyeR);
    tortoiseHead = head;
    turtleGroup.add(head);

    // 4 Swimming Paddle Flippers (Thao tác quạt mây)
    tortoiseFlippers.fl = createFlipper(activeThree, skinMat, true, true);
    tortoiseFlippers.fl.position.set(6.2, -0.2, 4.5);
    tortoiseFlippers.fr = createFlipper(activeThree, skinMat, false, true);
    tortoiseFlippers.fr.position.set(-6.2, -0.2, 4.5);

    tortoiseFlippers.bl = createFlipper(activeThree, skinMat, true, false);
    tortoiseFlippers.bl.position.set(5.5, -0.2, -4.5);
    tortoiseFlippers.br = createFlipper(activeThree, skinMat, false, false);
    tortoiseFlippers.br.position.set(-5.5, -0.2, -4.5);

    turtleGroup.add(tortoiseFlippers.fl);
    turtleGroup.add(tortoiseFlippers.fr);
    turtleGroup.add(tortoiseFlippers.bl);
    turtleGroup.add(tortoiseFlippers.br);

    // Short Pointed Tail
    const tail = new activeThree.Mesh(new activeThree.ConeGeometry(0.65, 2.5, 6), skinMat);
    tail.position.set(0, -0.2, -8.2);
    tail.rotation.x = -Math.PI / 2;
    turtleGroup.add(tail);

    scene.add(turtleGroup);
  }

  // Helper: Create Curved Swimming Flipper
  function createFlipper(activeThree, mat, isLeft, isFront) {
    const flipperGroup = new activeThree.Group();
    const sign = isLeft ? 1 : -1;
    const len = isFront ? 6.2 : 4.2;

    const fShape = new activeThree.Shape();
    fShape.moveTo(0, 0);
    fShape.quadraticCurveTo(sign * 1.5, len * 0.4, sign * 2.2, len);
    fShape.quadraticCurveTo(sign * 0.8, len * 0.85, 0, len * 0.6);
    fShape.quadraticCurveTo(0, 0, 0, 0);

    const fGeo = new activeThree.ShapeGeometry(fShape);
    const fMesh = new activeThree.Mesh(fGeo, mat);
    fMesh.rotation.x = Math.PI / 2;
    fMesh.rotation.z = sign * (isFront ? 0.45 : -0.3);
    flipperGroup.add(fMesh);

    return flipperGroup;
  }

  // Animation Loop (Framerate-Independent Delta-Time)
  function animate3D() {
    try {
      animId = (window.requestAnimationFrame || requestAnimationFrame)(animate3D);

      const dt = clock ? Math.min(clock.getDelta(), 0.08) : 0.02;
      ceremonyTime += dt;

      // 1. Slow Cosmic Deep-Space Drift
      if (starField) {
        starField.rotation.y = ceremonyTime * 0.015;
      }

      // 2. Ascending Incense Embers
      if (floatingEmbers && floatingEmbers.geometry && floatingEmbers.geometry.attributes.position) {
        const pos = floatingEmbers.geometry.attributes.position.array;
        for (let i = 1; i < pos.length; i += 3) {
          pos[i] += dt * 7.5;
          if (pos[i] > 48) pos[i] = 0;
        }
        floatingEmbers.geometry.attributes.position.needsUpdate = true;
        floatingEmbers.rotation.y = ceremonyTime * 0.035;
      }

      // 3. Astrolabe Rings Rotation & Taiji Counter-Spin
      if (astrolabeGroup) {
        astrolabeGroup.rotation.y = ceremonyTime * 0.075;
        const taiji = astrolabeGroup.getObjectByName("taijiCenter");
        if (taiji) {
          taiji.rotation.y = -ceremonyTime * 0.22;
        }
      }

      // 4. Convergence Progression
      if (isConverging) {
        convergenceProgress = Math.min(convergenceProgress + dt * 1.1, 1.0);
      }
      const convFactor = 1.0 - Math.pow(convergenceProgress, 2.2);

      // =======================================================================
      // 5. DRAGON CONTINUOUS TAPERED TUBE SPLINE KINEMATICS
      // =======================================================================
      if (dragonGroup && dragonBodyMesh && dragonBodyGeo) {
        const positions = dragonBodyGeo.attributes.position.array;
        const spine = [];
        const tangents = [];
        const normals = [];
        const binormals = [];

        // Sample 36 points along the dynamic 3D spline
        for (let i = 0; i < DRAGON_RINGS; i++) {
          const tDelay = ceremonyTime - i * 0.055;
          const theta = tDelay * 1.35;
          const rad = (31 + Math.sin(tDelay * 0.65) * 6.0) * convFactor + 0.2;

          const cx = Math.cos(theta) * rad + Math.cos(tDelay * 2.8) * 3.0 * convFactor;
          const cz = Math.sin(theta) * rad + Math.sin(tDelay * 2.8) * 3.0 * convFactor;
          const cy = (18 + Math.sin(tDelay * 1.7) * 8.0 + Math.cos(tDelay * 0.9) * 2.5) * convFactor + 1.2;

          spine.push(new THREE.Vector3(cx, cy, cz));
        }
        dragonSpinePoints = spine;

        // Compute Tangents & Frenet Frames along spline
        for (let i = 0; i < DRAGON_RINGS; i++) {
          const pPrev = spine[Math.max(0, i - 1)];
          const pNext = spine[Math.min(DRAGON_RINGS - 1, i + 1)];
          const tan = new THREE.Vector3().subVectors(pPrev, pNext).normalize();
          if (tan.lengthSq() < 0.001) tan.set(0, 0, 1);
          tangents.push(tan);

          let up = new THREE.Vector3(0, 1, 0);
          if (Math.abs(tan.dot(up)) > 0.9) up = new THREE.Vector3(1, 0, 0);
          const norm = new THREE.Vector3().crossVectors(tan, up).normalize();
          const binorm = new THREE.Vector3().crossVectors(tan, norm).normalize();
          normals.push(norm);
          binormals.push(binorm);
        }

        // Generate seamless vertices around each ring with smooth tapering
        for (let i = 0; i < DRAGON_RINGS; i++) {
          const u = i / (DRAGON_RINGS - 1);
          // Radius tapers from 2.0 at neck to 2.5 at torso down to 0.35 at tail
          const taper = (2.0 + Math.sin(u * Math.PI) * 0.55) * (1.0 - u * 0.82) * convFactor + 0.12;
          const center = spine[i];
          const norm = normals[i];
          const binorm = binormals[i];

          for (let s = 0; s < DRAGON_RADIAL_SEGS; s++) {
            const phi = (s / DRAGON_RADIAL_SEGS) * Math.PI * 2;
            const cosP = Math.cos(phi);
            const sinP = Math.sin(phi);

            const vx = center.x + (norm.x * cosP + binorm.x * sinP) * taper;
            const vy = center.y + (norm.y * cosP + binorm.y * sinP) * taper;
            const vz = center.z + (norm.z * cosP + binorm.z * sinP) * taper;

            const vIdx = (i * DRAGON_RADIAL_SEGS + s) * 3;
            positions[vIdx] = vx;
            positions[vIdx + 1] = vy;
            positions[vIdx + 2] = vz;
          }
        }

        dragonBodyGeo.attributes.position.needsUpdate = true;
        dragonBodyGeo.computeVertexNormals();

        // Position Head at ring 0 facing forward
        if (dragonHeadGroup && spine.length > 1) {
          dragonHeadGroup.position.copy(spine[0]);
          const headLookTarget = spine[0].clone().add(
            new THREE.Vector3().subVectors(spine[0], spine[1]).multiplyScalar(2.0)
          );
          dragonHeadGroup.lookAt(headLookTarget);

          // Waving Whiskers
          for (let k = 0; k < dragonWhiskersLeft.length; k++) {
            const wlX = spine[0].x + Math.sin(ceremonyTime * 5 + k * 0.35) * 1.2 + (k * 0.22);
            const wlY = spine[0].y - (k * 0.16) + Math.cos(ceremonyTime * 4 + k) * 0.35;
            const wlZ = spine[0].z - (k * 0.32);

            dragonWhiskersLeft[k].position.set(wlX, wlY, wlZ);
            dragonWhiskersRight[k].position.set(wlX - 2.4, wlY, wlZ);
          }
        }

        // Position Dorsal Fins along the continuous spine
        for (let d = 0; d < dragonDorsalFins.length; d++) {
          const fin = dragonDorsalFins[d];
          const rIdx = fin.userData.ringIndex;
          if (rIdx < spine.length) {
            fin.position.copy(spine[rIdx]);
            if (rIdx > 0) fin.lookAt(spine[rIdx - 1]);
          }
        }

        // Position Legs along spine rings
        for (let l = 0; l < dragonLegs.length; l++) {
          const leg = dragonLegs[l];
          const rIdx = leg.userData.ringIndex;
          if (rIdx < spine.length) {
            leg.position.copy(spine[rIdx]);
            if (rIdx > 0) leg.lookAt(spine[rIdx - 1]);
          }
        }

        // Position Tail Tuft at the tip
        for (let t = 0; t < dragonTailFins.length; t++) {
          const tuft = dragonTailFins[t];
          const rIdx = tuft.userData.ringIndex;
          if (rIdx < spine.length) {
            tuft.position.copy(spine[rIdx]);
            if (rIdx > 0) tuft.lookAt(spine[rIdx - 1]);
          }
        }
      }

      // =======================================================================
      // 6. PHOENIX AVIAN WINGBEATS & 5-TAIL SILK RIBBON UNDULATION
      // =======================================================================
      if (phoenixGroup) {
        // Counter-spiral flight trajectory (Clear visible interaction with Dragon)
        const pTheta = -ceremonyTime * 1.15 + Math.PI;
        const pRad = (28 + Math.cos(ceremonyTime * 0.75) * 5.0) * convFactor + 0.2;

        const px = Math.cos(pTheta) * pRad;
        const pz = Math.sin(pTheta) * pRad;
        const py = (20 + Math.cos(ceremonyTime * 2.1) * 7.0) * convFactor + 1.5;

        phoenixGroup.position.set(px, py, pz);
        phoenixGroup.rotation.y = -pTheta + Math.PI / 2;
        phoenixGroup.rotation.z = Math.sin(ceremonyTime * 3.8) * 0.16;

        // Organic 2-Tier Wing Flap
        const wingBeat = ceremonyTime * 4.8;
        const shoulderAngle = Math.sin(wingBeat) * 0.52;
        const elbowAngle = Math.sin(wingBeat - 0.42) * 0.36;

        if (phoenixWings.leftShoulder) {
          phoenixWings.leftShoulder.rotation.z = -shoulderAngle;
          phoenixWings.leftElbow.rotation.z = -elbowAngle;
          phoenixWings.rightShoulder.rotation.z = shoulderAngle;
          phoenixWings.rightElbow.rotation.z = elbowAngle;
        }

        // 5 Tail Ribbons Floating Fluidly in Slipstream
        for (let t = 0; t < phoenixTailRibbons.length; t++) {
          const ribbon = phoenixTailRibbons[t];
          const tOffset = (t - 2) * 0.85;

          for (let n = 0; n < ribbon.length; n++) {
            const nDelay = (n + 1) * 0.085;
            const waveX = Math.sin(ceremonyTime * 4.2 - nDelay * 2) * (1.1 + n * 0.18) + tOffset;
            const waveY = -n * 1.15 + Math.cos(ceremonyTime * 2.8 - nDelay) * 0.55;
            const waveZ = -n * 1.85;

            ribbon[n].position.set(waveX, waveY, waveZ);
          }
        }
      }

      // =======================================================================
      // 7. SACRED TORTOISE CLOUD OCEAN SWIMMING
      // =======================================================================
      if (turtleGroup) {
        turtleGroup.position.y = (7.0 + Math.sin(ceremonyTime * 0.75) * 1.2) * convFactor + 1.0;
        turtleGroup.rotation.y = -ceremonyTime * 0.045;

        const swimCycle = ceremonyTime * 2.2;
        const flipperAngle = Math.sin(swimCycle) * 0.32;

        if (tortoiseFlippers.fl) {
          tortoiseFlippers.fl.rotation.y = flipperAngle;
          tortoiseFlippers.fr.rotation.y = -flipperAngle;
          tortoiseFlippers.bl.rotation.y = -flipperAngle * 0.4;
          tortoiseFlippers.br.rotation.y = flipperAngle * 0.4;
        }

        if (tortoiseHead) {
          tortoiseHead.position.y = 1.0 + Math.sin(swimCycle) * 0.18;
        }
      }

      // =======================================================================
      // 8. CAMERA CINEMATIC FRAMING (Centered to display Dragon & Phoenix)
      // =======================================================================
      if (camera) {
        const camX = Math.sin(ceremonyTime * 0.32) * 8 * convFactor;
        const camY = 26 - convergenceProgress * 12;
        const camZ = 88 - convergenceProgress * 30;
        camera.position.set(camX, camY, camZ);
        camera.lookAt(0, 12, 0); // Framed so beasts occupy central view
      }

      if (renderer && scene && camera) {
        renderer.render(scene, camera);
      }
    } catch (loopErr) {
      console.warn("animate3D loop warning:", loopErr);
    }
  }

  // =========================================================================
  // PUBLIC RITUAL LIFECYCLE API
  // =========================================================================

  // Skip Ceremony Immediately (Invoked by Skip Button or Fallback)
  window.skipCelestialSummon = function () {
    if (!ceremonyActive && ceremonyDismissed) return;
    ceremonyDismissed = true;
    ceremonyActive = false;

    if (safetyTimeout) {
      clearTimeout(safetyTimeout);
      safetyTimeout = null;
    }
    if (chantInterval) {
      clearInterval(chantInterval);
      chantInterval = null;
    }
    if (countdownInterval) {
      clearInterval(countdownInterval);
      countdownInterval = null;
    }
    if (animId) {
      (window.cancelAnimationFrame || cancelAnimationFrame)(animId);
      animId = null;
    }

    const overlay = document.getElementById("celestial-summon-overlay");
    if (overlay) {
      overlay.style.display = "none";
      overlay.classList.remove("active", "fade-out");
    }

    if (typeof window.onCelestialSummonSkipped === 'function') {
      try { window.onCelestialSummonSkipped(); } catch (e) {}
    }

    // Call any pending callback exactly once!
    if (pendingCallback && !callbackFired) {
      callbackFired = true;
      const cb = pendingCallback;
      pendingCallback = null;
      try { cb(); } catch (e) { console.error("Callback error on skip:", e); }
    }
  };

  // Primary API: Start Ceremony (Invoked when user clicks submit)
  window.startCelestialSummon = function (onReadyCallback) {
    try {
      initAudio();
      playTempleBell(180, 5.0, 0.55);

      ceremonyActive = true;
      ceremonyDismissed = false;
      callbackFired = false;
      pendingCallback = null;

      // Check Accessibility: prefers-reduced-motion
      if (window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
        if (onReadyCallback) onReadyCallback();
        return;
      }

      const overlay = document.getElementById("celestial-summon-overlay");
      if (overlay) {
        overlay.style.display = "flex";
        overlay.classList.remove("fade-out");
        void overlay.offsetWidth; // Force reflow
        overlay.classList.add("active");
      }

      // Initialize 3D Scene
      isConverging = false;
      convergenceProgress = 0;
      initThreeScene();
      if (animId) {
        (window.cancelAnimationFrame || cancelAnimationFrame)(animId);
        animId = null;
      }
      animate3D();

      // Countdown Timer (10s -> 9s -> ... -> 1s)
      countdownSec = 10;
      const countdownEl = document.getElementById("celestial-countdown-num");
      if (countdownEl) countdownEl.innerText = countdownSec;
      if (countdownInterval) clearInterval(countdownInterval);
      countdownInterval = setInterval(() => {
        if (countdownSec > 1) {
          countdownSec--;
          if (countdownEl) countdownEl.innerText = countdownSec;
        } else {
          if (countdownEl) countdownEl.innerText = "1";
        }
      }, 1000);

      // HUD Step Updates: 5 steps across 10 seconds (~2s per step)
      chantIdx = 0;
      const statusText = document.getElementById("celestial-status-text");
      const progressFill = document.getElementById("celestial-progress-fill");
      if (statusText) statusText.innerText = celestialChants[0];
      if (progressFill) progressFill.style.width = "18%";

      if (chantInterval) clearInterval(chantInterval);
      chantInterval = setInterval(() => {
        chantIdx = (chantIdx + 1) % celestialChants.length;
        if (statusText) {
          statusText.style.opacity = "0";
          setTimeout(() => {
            statusText.innerText = celestialChants[chantIdx];
            statusText.style.opacity = "1";
          }, 180);
        }
        if (progressFill) {
          const pct = Math.min(18 + (chantIdx + 1) * 16, 96);
          progressFill.style.width = pct + "%";
        }
      }, 1950);

      // Auto-safety fallback (25s): Never trap the user on screen
      if (safetyTimeout) clearTimeout(safetyTimeout);
      safetyTimeout = setTimeout(() => {
        window.skipCelestialSummon();
      }, 25000);
    } catch (e) {
      console.warn("startCelestialSummon warning:", e);
    }

    if (onReadyCallback) onReadyCallback();
  };

  // Primary API: Finish Ceremony when Backend data arrives
  window.finishCelestialSummon = function (callback) {
    if (safetyTimeout) {
      clearTimeout(safetyTimeout);
      safetyTimeout = null;
    }
    if (countdownInterval) {
      clearInterval(countdownInterval);
      countdownInterval = null;
    }
    const countdownEl = document.getElementById("celestial-countdown-num");
    if (countdownEl) countdownEl.innerText = "0";

    // Helper: Safely invoke callback exactly once
    function invokeCallbackOnce(cb) {
      if (cb && !callbackFired) {
        callbackFired = true;
        try { cb(); } catch (cbErr) { console.error("Callback error:", cbErr); }
      }
    }

    // CASE A: User has ALREADY skipped, timed out, or ceremony was already dismissed
    if (ceremonyDismissed || !ceremonyActive) {
      if (callback) {
        invokeCallbackOnce(callback);
      }
      return;
    }

    // Register pending callback
    if (callback) {
      pendingCallback = callback;
    }

    const overlay = document.getElementById("celestial-summon-overlay");
    const flash = document.getElementById("celestial-flash");
    const progressFill = document.getElementById("celestial-progress-fill");
    const statusText = document.getElementById("celestial-status-text");

    if (progressFill) progressFill.style.width = "100%";
    if (statusText) statusText.innerText = "✦ VẠN TINH QUY TÔNG • THIÊN BÀN VIÊN THÀNH! ✦";

    if (chantInterval) {
      clearInterval(chantInterval);
      chantInterval = null;
    }

    // Trigger inward 3D convergence
    isConverging = true;

    // Culmination sound: Bell + Chime
    playTempleBell(288, 4.5, 0.45);
    playStarChime();

    setTimeout(() => {
      // Trigger warm royal golden flash
      if (flash) {
        flash.classList.add("trigger-flash");
      }

      // Execute data update at peak of flash (EXACTLY ONCE)
      if (pendingCallback) {
        invokeCallbackOnce(pendingCallback);
        pendingCallback = null;
      }

      setTimeout(() => {
        if (overlay) {
          overlay.classList.remove("active");
          overlay.classList.add("fade-out");
        }

        if (animId) {
          (window.cancelAnimationFrame || cancelAnimationFrame)(animId);
          animId = null;
        }

        ceremonyActive = false;
        ceremonyDismissed = true;

        setTimeout(() => {
          if (overlay) {
            overlay.style.display = "none";
            overlay.classList.remove("fade-out");
          }
          if (flash) flash.classList.remove("trigger-flash");

          // Trigger chamber blessing ripple on the 12 houses
          triggerChamberBlessingWave();
        }, 320);
      }, 340);
    }, 280);
  };

  // Chamber blessing cascade ripple across the 12 houses
  function triggerChamberBlessingWave() {
    try {
      const chamberElements = document.querySelectorAll(".chamber-card");
      if (!chamberElements || chamberElements.length === 0) return;

      chamberElements.forEach((card, idx) => {
        setTimeout(() => {
          card.classList.add("chamber-blessed");
          setTimeout(() => {
            card.classList.remove("chamber-blessed");
          }, 1200);
        }, idx * 75);
      });
    } catch (e) {}
  }

  // Replay / Preview Ritual anytime button (Không cần nhập thông tin cá nhân)
  window.replayCelestialSummon = function () {
    window.startCelestialSummon(() => {
      setTimeout(() => {
        window.finishCelestialSummon();
      }, 3800);
    });
  };
})();
