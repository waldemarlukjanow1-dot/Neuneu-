// shared helpers for the satisfying loops: 1080x1920, 60 fps, dark neon look (same system as the reference video)
export const W = 1080, H = 1920, FPS = 60, DUR = 8;
export const cv = document.createElement('canvas'); cv.width = W; cv.height = H; document.body.appendChild(cv);
export const g = cv.getContext('2d');
export const clamp01 = (x) => Math.max(0, Math.min(1, x));
export const lerp = (a, b, t) => a + (b - a) * t;
export const ease = (t) => t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
export function rng(seed) { let s = seed >>> 0; return () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; }
export const hue = (h, l = 60) => `hsl(${((h % 360) + 360) % 360},100%,${l}%)`;
export function bg() {
  g.fillStyle = '#060708'; g.fillRect(0, 0, W, H);
  const gr = g.createRadialGradient(540, 900, 50, 540, 900, 900); gr.addColorStop(0, 'rgba(40,44,52,0.35)'); gr.addColorStop(1, 'rgba(0,0,0,0)'); g.fillStyle = gr; g.fillRect(0, 0, W, H);
}
export function glowDot(x, y, r, col, a = 1) {
  g.save(); g.globalAlpha = a; g.shadowColor = col; g.shadowBlur = r * 2.2; g.fillStyle = col; g.beginPath(); g.arc(x, y, r, 0, 7); g.fill();
  g.shadowBlur = 0; g.fillStyle = 'rgba(255,255,255,0.55)'; g.beginPath(); g.arc(x - r * 0.3, y - r * 0.3, r * 0.35, 0, 7); g.fill(); g.restore();
}
export function counter(txt, y = 1500, size = 64) {
  g.save(); g.font = `800 ${size}px Inter, sans-serif`; g.textAlign = 'center'; g.fillStyle = '#fff'; g.shadowColor = 'rgba(255,255,255,0.5)'; g.shadowBlur = 12; g.fillText(txt, 540, y); g.restore();
}
export function finish(renderFn, frames, events, extra = {}) {
  window.renderFrame = (f) => { renderFn(f / FPS, f); return cv.toDataURL('image/jpeg', 0.93); };
  window.info = { frames, duration: frames / FPS, fps: FPS, events, ...extra };
  window.ready = true;
}
