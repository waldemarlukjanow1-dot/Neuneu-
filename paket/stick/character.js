// "Kappi" – the stick figure with the blue cap. Fixed design reference for the whole series.
// Units: pixels at scale 1 (figure ≈ 600 px tall). Angles in radians; limbs: 0 = hanging straight down,
// positive = rotated towards the facing direction (front view: positive = outward).
export const DESIGN = {
  line: '#16181d', lineW: 12,
  head: '#fff6e6', headR: 64, headStroke: 9,
  cap: '#1f6bff', capDark: '#1450c8', capLight: '#5c95ff', capLogo: '#ffffff',
  gold: '#f6c445', goldDark: '#b8860b', goldLight: '#fff1b0',   // Goldkette – fester Teil des Designs
  blush: 'rgba(255,120,120,0.35)',
  torso: 185, neck: 14, upperArm: 100, foreArm: 95, thigh: 122, shin: 118,
};

const lerp = (a, b, t) => a + (b - a) * t;
export const ease = (t) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);
export const clamp01 = (t) => Math.max(0, Math.min(1, t));

export const POSES = {
  stand:   { torso: 0, head: 0, armL: [0.18, 0.1], armR: [0.18, 0.1], legL: [0.12, 0], legR: [0.12, 0] },
  wave:    { torso: 0, head: 0.05, armL: [0.18, 0.1], armR: [2.6, 0.6], legL: [0.12, 0], legR: [0.12, 0] },
  point:   { torso: 0.02, head: 0, armL: [0.15, 0.1], armR: [1.45, 0.05], legL: [0.12, 0], legR: [0.12, 0] },
  pointUp: { torso: 0, head: -0.1, armL: [0.15, 0.1], armR: [2.5, 0.2], legL: [0.12, 0], legR: [0.12, 0] },
  cheer:   { torso: 0, head: -0.08, armL: [2.7, 0.3], armR: [2.7, 0.3], legL: [0.25, 0], legR: [0.25, 0] },
  shrug:   { torso: 0, head: 0.1, armL: [0.5, 1.7], armR: [0.5, 1.7], legL: [0.12, 0], legR: [0.12, 0] },
  think:   { torso: 0, head: 0.12, armL: [0.3, 2.2], armR: [0.2, 0.1], legL: [0.12, 0], legR: [0.12, 0] },
  chest:   { torso: 0, head: 0, armL: [0.2, 0.1], armR: [0.55, 2.3], legL: [0.12, 0], legR: [0.12, 0] },
  hold:    { torso: 0, head: 0.05, armL: [0.18, 0.1], armR: [0.6, 1.4], legL: [0.12, 0], legR: [0.12, 0] },
  scared:  { torso: -0.06, head: -0.05, armL: [1.2, 1.6], armR: [1.2, 1.6], legL: [0.3, 0.1], legR: [0.3, 0.1] },
  flex:    { torso: 0, head: 0, armL: [1.5, 2.0], armR: [1.5, 2.0], legL: [0.2, 0], legR: [0.2, 0] },
  cough:   { torso: 0.35, head: 0.3, armL: [0.6, 2.3], armR: [0.3, 0.5], legL: [0.12, 0], legR: [0.12, 0] },
  sniff:   { torso: 0.06, head: -0.18, armL: [0.2, 0.1], armR: [0.9, 1.5], legL: [0.12, 0], legR: [0.12, 0] },
};
export function mixPose(a, b, t) {
  const o = {};
  for (const k of Object.keys(a)) o[k] = Array.isArray(a[k]) ? a[k].map((v, i) => lerp(v, b[k][i], t)) : lerp(a[k], b[k], t);
  return o;
}
// walk / run cycle (side view): returns pose overrides
export function walkPose(phase, run = 0) {
  const s = Math.sin(phase), c = Math.cos(phase);
  const amp = lerp(0.45, 0.9, run);
  return {
    torso: lerp(0.04, 0.22, run), head: lerp(0, -0.1, run),
    legL: [s * amp, Math.max(0, -c) * lerp(0.5, 1.4, run) + 0.05], legR: [-s * amp, Math.max(0, c) * lerp(0.5, 1.4, run) + 0.05],
    armL: [-s * amp * 0.8, lerp(0.3, 1.5, run)], armR: [s * amp * 0.8, lerp(0.3, 1.5, run)],
    bob: Math.abs(c) * lerp(6, 16, run),
  };
}

// ---------- drawing ----------
function limb(g, x, y, a1, a2, l1, l2, dirX) {
  // dirX: +1 limb rotates to the right for positive angles, -1 to the left
  const ex = x + Math.sin(a1) * l1 * dirX, ey = y + Math.cos(a1) * l1;
  const a = a1 + a2;
  const hx = ex + Math.sin(a) * l2 * dirX, hy = ey + Math.cos(a) * l2;
  g.beginPath(); g.moveTo(x, y); g.lineTo(ex, ey); g.lineTo(hx, hy); g.stroke();
  return { ex, ey, hx, hy, ang: a };
}

function drawCap(g, hx, hy, R, facing, tilt) {
  const D = DESIGN;
  g.save(); g.translate(hx, hy); g.rotate(tilt);
  // dome
  g.fillStyle = D.cap; g.strokeStyle = D.line; g.lineWidth = D.headStroke;
  g.beginPath();
  g.ellipse(0, -R * 0.36, R * 1.0, R * 0.8, 0, Math.PI * 1.02, Math.PI * 1.98);
  g.closePath(); g.fill(); g.stroke();
  // shade + seam
  g.save(); g.clip();
  g.fillStyle = D.capDark; g.beginPath(); g.ellipse(-facing * R * 0.4, -R * 0.1, R * 0.9, R * 0.9, 0, 0, Math.PI * 2); g.globalAlpha = 0.35; g.fill(); g.globalAlpha = 1;
  g.fillStyle = D.capLight; g.globalAlpha = 0.5; g.beginPath(); g.ellipse(facing * R * 0.25 + R * 0.1, -R * 0.75, R * 0.35, R * 0.12, -0.3, 0, Math.PI * 2); g.fill(); g.globalAlpha = 1;
  g.restore();
  g.strokeStyle = D.capDark; g.lineWidth = 4; g.beginPath(); g.moveTo(facing * R * 0.15, -R * 1.12); g.quadraticCurveTo(facing * R * 0.25, -R * 0.8, facing * R * 0.2, -R * 0.45); g.stroke();
  // button
  g.fillStyle = D.capDark; g.strokeStyle = D.line; g.lineWidth = 5; g.beginPath(); g.arc(0, -R * 1.15, R * 0.1, 0, Math.PI * 2); g.fill(); g.stroke();
  // logo "?" on the front panel
  const lx = facing * R * 0.42, ly = -R * 0.72;
  g.fillStyle = D.capLogo; g.beginPath(); g.arc(lx, ly, R * 0.24, 0, Math.PI * 2); g.fill();
  g.fillStyle = D.cap; g.font = `900 ${R * 0.36}px Inter`; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText('?', lx, ly + R * 0.02);
  // brim
  g.fillStyle = D.capDark; g.strokeStyle = D.line; g.lineWidth = D.headStroke;
  g.beginPath();
  if (facing === 0) {
    g.ellipse(0, -R * 0.38, R * 1.1, R * 0.17, 0, 0, Math.PI);
  } else {
    const bx = facing * R * 0.95;
    g.moveTo(facing * R * 0.2, -R * 0.42);
    g.quadraticCurveTo(bx + facing * R * 0.55, -R * 0.5, bx + facing * R * 0.62, -R * 0.3);
    g.quadraticCurveTo(bx + facing * R * 0.2, -R * 0.2, facing * R * 0.55, -R * 0.3);
  }
  g.closePath(); g.fill(); g.stroke();
  g.restore();
}

function drawFace(g, hx, hy, R, facing, expr, mouthOpen, blink, tilt, look) {
  const D = DESIGN;
  g.save(); g.translate(hx, hy); g.rotate(tilt);
  const fx = facing * R * 0.28 + (look?.x || 0) * R * 0.08, fy = R * 0.12 + (look?.y || 0) * R * 0.06;
  const eyeDX = facing === 0 ? R * 0.32 : R * 0.26;
  const eyes = facing === 0 ? [-eyeDX, eyeDX] : [fx - eyeDX * 0.75, fx + eyeDX * 0.75];
  g.fillStyle = D.line; g.strokeStyle = D.line; g.lineCap = 'round';
  const e = EXPR[expr] || EXPR.neutral;
  // blush
  if (e.blush) { g.fillStyle = D.blush; for (const ex of eyes) { g.beginPath(); g.ellipse(ex + (ex > fx ? 6 : -6), fy + R * 0.3, R * 0.16, R * 0.09, 0, 0, Math.PI * 2); g.fill(); } g.fillStyle = D.line; }
  // eyes
  for (let i = 0; i < 2; i++) {
    const ex = eyes[i], ey = fy - R * 0.05;
    const h = R * e.eyeH * (1 - blink);
    if (e.eyeShape === 'happy') { g.lineWidth = 6; g.beginPath(); g.arc(ex, ey + R * 0.05, R * 0.11, Math.PI * 1.1, Math.PI * 1.9); g.stroke(); }
    else if (e.eyeShape === 'x') { g.lineWidth = 6; const s = R * 0.09; g.beginPath(); g.moveTo(ex - s, ey - s); g.lineTo(ex + s, ey + s); g.moveTo(ex + s, ey - s); g.lineTo(ex - s, ey + s); g.stroke(); }
    else if (h < 3) { g.lineWidth = 5; g.beginPath(); g.moveTo(ex - R * 0.08, ey); g.lineTo(ex + R * 0.08, ey); g.stroke(); }
    else {
      g.beginPath(); g.ellipse(ex, ey, R * e.eyeW, h, 0, 0, Math.PI * 2); g.fill();
      g.fillStyle = '#fff'; g.beginPath(); g.arc(ex + R * 0.03 + (look?.x || 0) * 3, ey - h * 0.35, Math.max(1.5, R * 0.035), 0, Math.PI * 2); g.fill(); g.fillStyle = D.line;
    }
    // brows
    g.lineWidth = 5.5;
    const side = i === 0 ? -1 : 1;
    const by = ey - R * 0.27 - R * e.browUp;
    g.beginPath(); g.moveTo(ex - R * 0.11, by + side * R * e.browTilt); g.lineTo(ex + R * 0.11, by - side * R * e.browTilt); g.stroke();
  }
  // mouth
  const mx = facing === 0 ? 0 : fx + facing * R * 0.05, my = fy + R * 0.36;
  const w = R * e.mouthW;
  const open = Math.max(e.open, mouthOpen * 0.9);
  g.lineWidth = 6;
  if (open > 0.08) {
    g.fillStyle = '#7a1f2b'; g.beginPath();
    g.moveTo(mx - w, my - R * 0.02 * e.smile);
    g.quadraticCurveTo(mx, my + R * (0.05 + 0.32 * open) + R * 0.1 * e.smile, mx + w, my - R * 0.02 * e.smile);
    g.quadraticCurveTo(mx, my - R * 0.05 * open, mx - w, my - R * 0.02 * e.smile);
    g.closePath(); g.fill(); g.stroke();
    if (open > 0.35) { g.fillStyle = '#ff7a8a'; g.beginPath(); g.ellipse(mx, my + R * 0.16 * open, w * 0.45, R * 0.06 * open, 0, 0, Math.PI * 2); g.fill(); }
  } else if (e.mouth === 'wavy') {
    g.beginPath(); g.moveTo(mx - w, my); for (let k = 1; k <= 4; k++) g.lineTo(mx - w + (k * 2 * w) / 4, my + (k % 2 ? -1 : 1) * R * 0.04); g.stroke();
  } else {
    g.beginPath(); g.moveTo(mx - w, my); g.quadraticCurveTo(mx, my + R * 0.2 * e.smile, mx + w, my); g.stroke();
  }
  // sweat drop
  if (e.sweat) { g.fillStyle = '#5cc8ff'; g.strokeStyle = D.line; g.lineWidth = 3; const sx = -facing * R * 0.75 + (facing === 0 ? R * 0.7 : 0), sy = -R * 0.15; g.beginPath(); g.moveTo(sx, sy - R * 0.2); g.quadraticCurveTo(sx + R * 0.14, sy + R * 0.02, sx, sy + R * 0.08); g.quadraticCurveTo(sx - R * 0.14, sy + R * 0.02, sx, sy - R * 0.2); g.fill(); g.stroke(); }
  g.restore();
}

export const EXPR = {
  neutral:   { eyeW: 0.075, eyeH: 0.11, browUp: 0, browTilt: 0, mouthW: 0.18, smile: 0.3, open: 0 },
  happy:     { eyeW: 0.075, eyeH: 0.11, browUp: 0.04, browTilt: -0.02, mouthW: 0.24, smile: 1, open: 0, blush: true },
  joy:       { eyeShape: 'happy', eyeW: 0.08, eyeH: 0.1, browUp: 0.08, browTilt: -0.03, mouthW: 0.26, smile: 1, open: 0.55, blush: true },
  surprised: { eyeW: 0.09, eyeH: 0.15, browUp: 0.1, browTilt: 0, mouthW: 0.12, smile: 0, open: 0.6 },
  worried:   { eyeW: 0.075, eyeH: 0.11, browUp: 0.05, browTilt: 0.06, mouthW: 0.18, smile: -0.6, open: 0, mouth: 'wavy', sweat: true },
  determined:{ eyeW: 0.08, eyeH: 0.09, browUp: -0.02, browTilt: -0.07, mouthW: 0.2, smile: 0.2, open: 0 },
  thinking:  { eyeW: 0.075, eyeH: 0.1, browUp: 0.04, browTilt: 0.04, mouthW: 0.12, smile: -0.2, open: 0 },
  sick:      { eyeShape: 'x', eyeW: 0.075, eyeH: 0.1, browUp: 0, browTilt: 0.05, mouthW: 0.2, smile: -0.5, open: 0.3 },
  proud:     { eyeShape: 'happy', eyeW: 0.075, eyeH: 0.11, browUp: 0.02, browTilt: -0.04, mouthW: 0.24, smile: 1, open: 0, blush: true },
  talk:      { eyeW: 0.075, eyeH: 0.11, browUp: 0.03, browTilt: 0, mouthW: 0.2, smile: 0.5, open: 0 },
};

// gold chain: loops around the neck (back strand behind the neck line), front strand hangs onto the chest,
// round "?" pendant rests on the torso line. Always worn.
function chainGeom(facing) {
  const side = facing === 0 ? 1 : 0.45, sh = facing === 0 ? 0 : facing * 9;
  const top = -9, depth = 62, nW = 13 * side, bulge = 30 * side;
  const pts = [], n = 16;
  for (let i = 0; i <= n; i++) {
    const t = i / n, sgn = t < 0.5 ? -1 : 1, u = t < 0.5 ? t * 2 : (1 - t) * 2;  // u: 0 at top, 1 at bottom
    const q = 1 - u;
    const x = sgn * (q * q * nW + 2 * q * u * bulge) + u * u * sh + (2 * q * u) * sh * 0.5;
    const y = q * q * top + 2 * q * u * (depth * 0.55) + u * u * depth;
    pts.push([x, y]);
  }
  return { pts, top, nW, depth, sh };
}
function drawChainBack(g, nx, ny, torso, facing) {
  const D = DESIGN, { top, nW } = chainGeom(facing);
  g.save(); g.translate(nx, ny); g.rotate(torso * (facing === 0 ? 0 : facing));
  g.strokeStyle = D.goldDark; g.lineWidth = 5; g.lineCap = 'round';
  g.beginPath(); g.moveTo(-nW, top); g.quadraticCurveTo(0, top - 7, nW, top); g.stroke();
  g.restore();
}
function drawChain(g, nx, ny, torso, facing) {
  const D = DESIGN, { pts, depth, sh } = chainGeom(facing);
  g.save(); g.translate(nx, ny); g.rotate(torso * (facing === 0 ? 0 : facing));
  for (let i = 0; i < pts.length; i++) {
    const [x, y] = pts[i]; const a = pts[Math.min(pts.length - 1, i + 1)], b = pts[Math.max(0, i - 1)];
    g.save(); g.translate(x, y); g.rotate(Math.atan2(a[1] - b[1], a[0] - b[0]));
    g.fillStyle = D.gold; g.strokeStyle = D.goldDark; g.lineWidth = 2.2;
    g.beginPath(); g.ellipse(0, 0, i % 2 ? 7.5 : 6.5, i % 2 ? 4.2 : 5.4, 0, 0, Math.PI * 2); g.fill(); g.stroke();
    g.fillStyle = D.goldLight; g.beginPath(); g.ellipse(-1.8, -1.4, 2.6, 1.2, 0, 0, Math.PI * 2); g.fill();
    g.restore();
  }
  // pendant hanging from the lowest link, resting on the chest
  const px = sh, py = depth + 19;
  g.strokeStyle = D.goldDark; g.lineWidth = 3; g.beginPath(); g.moveTo(px, depth + 3); g.lineTo(px, py - 17); g.stroke();
  g.fillStyle = D.gold; g.strokeStyle = D.line; g.lineWidth = 3.5;
  g.beginPath(); g.arc(px, py, 17, 0, Math.PI * 2); g.fill(); g.stroke();
  g.fillStyle = D.goldLight; g.beginPath(); g.arc(px - 5, py - 5, 4.5, 0, Math.PI * 2); g.fill();
  g.fillStyle = D.goldDark; g.font = '900 22px Inter'; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText('?', px + 0.5, py + 1.5);
  g.restore();
}

// side characters: hair / accessories instead of cap + chain. extra: { hair: 'short'|'ponytail'|'kid'|'none', color, tag, shirt }
function drawExtra(g, hx, hy, R, facing, ex) {
  const D = DESIGN; const col = ex.color || '#3a2a1e';
  g.save(); g.translate(hx, hy); g.fillStyle = col; g.strokeStyle = D.line; g.lineWidth = 6;
  if (ex.hair === 'short' || ex.hair === 'kid') {
    g.beginPath(); g.arc(0, 0, R, Math.PI * 1.08, Math.PI * 1.92); g.quadraticCurveTo(R * 0.2, -R * 0.45, -R * 0.95, -R * 0.25); g.closePath(); g.fill(); g.stroke();
    if (ex.hair === 'kid') { g.beginPath(); g.moveTo(0, -R); g.quadraticCurveTo(R * 0.25, -R * 1.45, R * 0.35, -R * 1.2); g.stroke(); }
  } else if (ex.hair === 'ponytail') {
    g.beginPath(); g.arc(0, 0, R, Math.PI * 1.02, Math.PI * 1.98); g.quadraticCurveTo(0, -R * 0.35, -R, -R * 0.1); g.closePath(); g.fill(); g.stroke();
    const sx = facing === 0 ? R * 0.95 : -facing * R * 0.95;
    g.beginPath(); g.ellipse(sx + (facing === 0 ? R * 0.25 : -facing * R * 0.25), R * 0.1, R * 0.28, R * 0.6, 0.3, 0, Math.PI * 2); g.fill(); g.stroke();
  }
  g.restore();
}

// state: { x, y (ground), scale, facing (-1|0|1), pose, expr, mouth (0..1), blink (0..1), look:{x,y}, bob, squash, hold: fn(g, hand) }
// optional muscles (st.muscle 0..1): bulges along a limb segment, drawn in line colour
function bulge(g, x1, y1, x2, y2, w, m) {
  if (m <= 0) return;
  const mx = (x1 + x2) / 2, my = (y1 + y2) / 2, L = Math.hypot(x2 - x1, y2 - y1);
  g.save(); g.fillStyle = DESIGN.line; g.beginPath(); g.ellipse(mx, my, L * 0.42, w * m, Math.atan2(y2 - y1, x2 - x1), 0, Math.PI * 2); g.fill(); g.restore();
}

export function drawKappi(g, st) {
  const D = DESIGN, s = st.scale ?? 1, f = st.facing ?? 0;
  const p = st.pose;
  g.save();
  g.translate(st.x, st.y); g.scale(s, s);
  // ground shadow
  g.fillStyle = 'rgba(0,0,0,0.13)'; g.beginPath(); g.ellipse(0, 6, 95, 16, 0, 0, Math.PI * 2); g.fill();
  const bob = (p.bob || 0) + (st.bob || 0);
  const legLen = D.thigh + D.shin;
  const hipY = -legLen * 0.985 - bob + (st.squash || 0) * 30;
  g.strokeStyle = D.line; g.lineWidth = D.lineW; g.lineCap = 'round'; g.lineJoin = 'round';
  const dir = f === 0 ? 1 : f;
  // legs
  const legDirL = f === 0 ? -1 : dir, legDirR = f === 0 ? 1 : dir;
  const hipOff = f === 0 ? 14 : 0;
  const lL = limb(g, -hipOff, hipY, p.legL[0], -p.legL[1], D.thigh, D.shin, legDirL);
  const lR = limb(g, hipOff, hipY, p.legR[0], -p.legR[1], D.thigh, D.shin, legDirR);
  if (st.muscle) { bulge(g, -hipOff, hipY, lL.ex, lL.ey, 20, st.muscle); bulge(g, hipOff, hipY, lR.ex, lR.ey, 20, st.muscle); }
  // torso
  const tx = Math.sin(p.torso) * D.torso * dir, ty = -Math.cos(p.torso) * D.torso;
  const nx = tx, ny = hipY + ty;
  g.beginPath(); g.moveTo(0, hipY); g.lineTo(nx, ny); g.stroke();
  const mus = st.muscle || 0;
  if (mus > 0) {   // V-shaped upper body with rounded shoulders
    const sw = 58 * mus, top = ny + 20, wy = lerp(ny, hipY, 0.7);
    g.fillStyle = D.line; g.beginPath(); g.moveTo(nx - sw, top); g.quadraticCurveTo(nx, top - 8, nx + sw, top); g.quadraticCurveTo(nx + sw * 0.9, lerp(top, wy, 0.5), 14, wy); g.lineTo(-14, wy); g.quadraticCurveTo(nx - sw * 0.9, lerp(top, wy, 0.5), nx - sw, top); g.closePath(); g.fill();
    for (const sd of [-1, 1]) { g.beginPath(); g.arc(nx + sd * sw * 0.92, top + 6, 20 * mus, 0, Math.PI * 2); g.fill(); }
  }
  // arms (from shoulder slightly below neck)
  const sx = lerp(0, nx, 0.92), sy = lerp(hipY, ny, 0.9);
  const armDirL = f === 0 ? -1 : dir, armDirR = f === 0 ? 1 : dir;
  // in side view draw the far arm first (thinner/darker look by order)
  const aL = limb(g, sx, sy, p.armL[0], p.armL[1], D.upperArm, D.foreArm, armDirL);
  bulge(g, sx, sy, aL.ex, aL.ey, 30, mus); bulge(g, aL.ex, aL.ey, aL.hx, aL.hy, 17, mus);
  // head
  const hang = p.torso + p.head;
  const hx = nx + Math.sin(hang) * (D.neck + D.headR) * dir, hy = ny - Math.cos(hang) * (D.neck + D.headR);
  const isKappi = !st.extra;   // side characters (st.extra) never get Kappi's cap or chain
  if (isKappi) drawChainBack(g, nx, ny, p.torso, f);
  g.strokeStyle = D.line; g.lineWidth = D.lineW;
  g.beginPath(); g.moveTo(nx, ny); g.lineTo(nx + Math.sin(hang) * D.neck * dir, ny - Math.cos(hang) * D.neck); g.stroke();
  if (isKappi) drawChain(g, nx, ny, p.torso, f);
  g.strokeStyle = D.line;
  g.fillStyle = D.head; g.lineWidth = D.headStroke; g.beginPath(); g.arc(hx, hy, D.headR, 0, Math.PI * 2); g.fill(); g.stroke();
  drawFace(g, hx, hy, D.headR, f, st.expr || 'neutral', st.mouth || 0, st.blink || 0, hang * dir * 0.6, st.look);
  if (isKappi) drawCap(g, hx, hy, D.headR, f, hang * dir * 0.6); else drawExtra(g, hx, hy, D.headR, f, st.extra);
  g.strokeStyle = D.line; g.lineWidth = D.lineW;
  const aR = limb(g, sx, sy, p.armR[0], p.armR[1], D.upperArm, D.foreArm, armDirR);
  bulge(g, sx, sy, aR.ex, aR.ey, 30, mus); bulge(g, aR.ex, aR.ey, aR.hx, aR.hy, 17, mus);
  if (f === 0 && isKappi) { drawChain(g, nx, ny, p.torso, f); g.strokeStyle = D.line; g.lineWidth = D.lineW; }   // front view: chain lies over the arm roots
  // hands
  g.fillStyle = D.line; for (const h of [aL, aR]) { g.beginPath(); g.arc(h.hx, h.hy, 9, 0, Math.PI * 2); g.fill(); }
  if (st.hold) st.hold(g, aR, aL);
  g.restore();
  return { head: { x: st.x + hx * s, y: st.y + hy * s }, handR: { x: st.x + aR.hx * s, y: st.y + aR.hy * s }, handL: { x: st.x + aL.hx * s, y: st.y + aL.hy * s } };
}
