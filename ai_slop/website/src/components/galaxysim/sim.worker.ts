// Runs the disk simulations off the main thread so the page stays responsive on ordinary machines.
// Back-pressure: it only computes again after the page has drawn the previous frame (an 'ack'), so a hidden tab or a slow GPU never lets work pile up.
// CPU cap: at most ~20 ms of physics per 33 ms tick (about 60% of one core), always at least one step per tick.
import { DiskSim } from './engine'

const ctx: any = self      // the app's TypeScript config targets the DOM, not the worker scope
let sims: DiskSim[] = []
let running = false, acked = true, maxSteps = 4, gen = 0, token = 0, stepMs = 6, lastCurve = 0

const snap = (s: DiskSim) => ({ x: new Float32Array(s.x), y: new Float32Array(s.y) })
const sleep = (ms: number) => new Promise(r => setTimeout(r, ms))

ctx.onmessage = (e: MessageEvent) => {
  const m = e.data
  if (m.type === 'init') {
    running = false; gen++
    try {
      const t0 = performance.now()
      sims = (m.modes as string[]).map(mode => new DiskSim(m.gal, m.kernel, m.a0, mode as any, { N: m.N, np: m.np, Q: m.Q, seed: 1 }))
      const sn = sims.map(snap), x0 = new Float32Array(sims[0].x0), y0 = new Float32Array(sims[0].y0)
      ctx.postMessage({ type: 'ready', modes: m.modes, L: sims[0].L, R99: sims[0].R99, np: m.np, vc0: sims.map(s => s.vc0), curves: sims.map(s => s.curve()), x0, y0,
        xs: sn.map(s => s.x), ys: sn.map(s => s.y), initMs: performance.now() - t0 }, [x0.buffer, y0.buffer, ...sn.flatMap(s => [s.x.buffer, s.y.buffer])])
    } catch (err) { ctx.postMessage({ type: 'error', message: String(err) }) }
  } else if (m.type === 'run') { if (!running && sims.length) { running = true; acked = true; loop(gen, ++token) } }
  else if (m.type === 'pause') running = false
  else if (m.type === 'ack') acked = true
  else if (m.type === 'speed') maxSteps = m.value
}

async function loop(g: number, mine: number) {          // `mine` stops a stale loop from a pause/run pair running alongside the new one
  while (running && g === gen && mine === token) {
    if (!acked) { await sleep(16); continue }
    const t0 = performance.now()
    const n = Math.max(1, Math.min(maxSteps, Math.floor(20 / Math.max(stepMs * sims.length, 0.5))))
    for (let k = 0; k < n; k++) for (const s of sims) s.step()
    const now = performance.now()
    stepMs = 0.7 * stepMs + 0.3 * ((now - t0) / (n * sims.length))
    const sn = sims.map(snap); acked = false
    let curves: unknown = undefined
    if (now - lastCurve > 700) { curves = sims.map(s => s.curve()); lastCurve = now }
    ctx.postMessage({ type: 'frame', t: sims[0].t, stepMs, n, xs: sn.map(s => s.x), ys: sn.map(s => s.y), curves }, sn.flatMap(s => [s.x.buffer, s.y.buffer]))
    await sleep(Math.max(1, 33 - (performance.now() - t0)))
  }
}
