'use client'

import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import Link from 'next/link'
import * as THREE from 'three'
import Plot from '@/components/toscale/Plot'
import { allowAutoMotion, getDevice, guardContext, maxPixelRatio } from '@/components/common/device'
import type { GalaxyData, Kernel, Mode } from './engine'

const GYR_PER_UNIT = 0.9778

interface Data { built_from: string; G: number; a0_kms2_per_kpc: number; ups: number; kernel: Kernel; summary: { n: number; skipped: Record<string, number>; star_frac_rms_median: number; law_rms_dex_median: number; law_tab_rms_dex_median: number }; galaxies: GalaxyData[] }
interface Curve { R: number[]; V: number[] }
interface Meta { modes: Mode[]; L: number; R99: number; np: number; vc0: Curve[]; x0: Float32Array; y0: Float32Array }

const MODES: { id: Mode; title: string; blurb: string; color: string }[] = [
  { id: 'law', title: 'The law, a₀ fixed', blurb: 'baryons only, g = ν(g_N/a₀) g_N with a₀ = 9.36×10⁻¹¹ m/s², no fit', color: '#ea580c' },
  { id: 'halo', title: 'Standard picture: Newton + dark halo', blurb: 'a rigid halo fitted point by point to the observed curve', color: '#2563eb' },
  { id: 'newton', title: 'Baryons only, Newtonian', blurb: 'what the visible matter alone would do', color: '#6b7280' },
]

const VERT = /* glsl */ `
attribute vec3 color;
uniform float uSize;
varying vec3 vC;
void main() { vC = color; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); gl_PointSize = uSize; }`
const FRAG = /* glsl */ `
precision highp float;
uniform float uAlpha;
varying vec3 vC;
void main() { float r = length(gl_PointCoord - 0.5) * 2.0; if (r > 1.0) discard; float a = (1.0 - r * r) * uAlpha; gl_FragColor = vec4(vC * a, a); }`

const INFERNO = [[0, 0, 4], [22, 11, 57], [66, 10, 104], [106, 23, 110], [147, 38, 103], [188, 55, 84], [221, 81, 58], [243, 120, 25], [252, 165, 10], [246, 215, 70], [252, 255, 164]]
const ramp = (t: number) => { const x = Math.min(Math.max(t, 0), 0.999) * (INFERNO.length - 1), i = Math.floor(x), f = x - i; return INFERNO[i].map((v, k) => (v * (1 - f) + INFERNO[i + 1][k] * f) / 255) }
const interp = (xs: number[], ys: number[], x: number) => { if (x <= xs[0]) return ys[0]; let i = 0; while (i < xs.length - 2 && xs[i + 1] < x) i++; const u = Math.min(1, (x - xs[i]) / (xs[i + 1] - xs[i])); return ys[i] * (1 - u) + ys[i + 1] * u }

type Draw = (x: Float32Array, y: Float32Array) => void

/** one face-on view: draws only when the worker hands it a new frame, so an idle page costs nothing */
function Panel({ meta, gal, color, byRadius, register, onLost }: { meta: Meta; gal: GalaxyData; color: string; byRadius: boolean; register: (d: Draw | null) => void; onLost: () => void }) {
  const host = useRef<HTMLDivElement>(null)
  const st = useRef<{ col: THREE.BufferAttribute; redraw: () => void } | null>(null)
  useEffect(() => {
    const el = host.current!, dev = getDevice()
    let renderer: THREE.WebGLRenderer
    try { renderer = new THREE.WebGLRenderer({ antialias: false, alpha: false, powerPreference: 'low-power' }) } catch { onLost(); return }
    const pr = maxPixelRatio(dev)
    renderer.setPixelRatio(pr); renderer.setClearColor(0x070a12, 1)
    el.appendChild(renderer.domElement); Object.assign(renderer.domElement.style, { width: '100%', height: '100%', display: 'block' })
    const unguard = guardContext(renderer.domElement, onLost)
    const half = meta.R99 * 1.55, np = meta.np
    const cam = new THREE.OrthographicCamera(-half, half, half, -half, -1, 1), scene = new THREE.Scene()
    const geo = new THREE.BufferGeometry(), pos = new Float32Array(3 * np), col = new Float32Array(3 * np)
    const pa = new THREE.BufferAttribute(pos, 3), ca = new THREE.BufferAttribute(col, 3)
    geo.setAttribute('position', pa); geo.setAttribute('color', ca)
    const mat = new THREE.ShaderMaterial({ vertexShader: VERT, fragmentShader: FRAG, transparent: true, depthTest: false, depthWrite: false, blending: THREE.CustomBlending, blendEquation: THREE.AddEquation, blendSrc: THREE.OneFactor, blendDst: THREE.OneFactor, uniforms: { uSize: { value: 2 * pr }, uAlpha: { value: 0.55 } } })
    const pts = new THREE.Points(geo, mat); pts.frustumCulled = false; scene.add(pts)
    const ring = new THREE.LineLoop(new THREE.BufferGeometry().setFromPoints(Array.from({ length: 129 }, (_, i) => new THREE.Vector3(Math.cos((i / 128) * 2 * Math.PI) * gal.Rd, Math.sin((i / 128) * 2 * Math.PI) * gal.Rd, 0))), new THREE.LineBasicMaterial({ color: 0x2b3550 }))
    scene.add(ring)
    let lastX: Float32Array = meta.x0, lastY: Float32Array = meta.y0
    const redraw = () => { for (let i = 0; i < np; i++) { pos[3 * i] = lastX[i]; pos[3 * i + 1] = lastY[i] } pa.needsUpdate = true; renderer.render(scene, cam) }
    const draw: Draw = (x, y) => { lastX = x; lastY = y; redraw() }
    const resize = () => { renderer.setSize(el.clientWidth, el.clientHeight, false); redraw() }
    st.current = { col: ca, redraw }
    const ro = new ResizeObserver(resize); ro.observe(el); resize()
    register(draw)
    return () => { register(null); unguard(); ro.disconnect(); geo.dispose(); mat.dispose(); ring.geometry.dispose(); renderer.dispose(); if (renderer.domElement.parentElement === el) el.removeChild(renderer.domElement); st.current = null }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [meta, gal])
  useEffect(() => {   // colours are fixed per particle: by starting radius, or one warm tone
    const s = st.current; if (!s) return
    const base = new THREE.Color(color), c = s.col.array as Float32Array
    for (let i = 0; i < meta.np; i++) {
      const rgb = byRadius ? ramp(Math.hypot(meta.x0[i], meta.y0[i]) / (meta.R99 * 1.3)) : [base.r * 0.55 + 0.45, base.g * 0.55 + 0.35, base.b * 0.55 + 0.25]
      c[3 * i] = rgb[0]; c[3 * i + 1] = rgb[1]; c[3 * i + 2] = rgb[2]
    }
    s.col.needsUpdate = true; s.redraw()
  }, [byRadius, color, meta])
  return <div ref={host} className="w-full h-full" />
}

export default function GalaxySim() {
  const dev = useMemo(() => getDevice(), [])
  const auto = allowAutoMotion(dev)
  const [data, setData] = useState<Data | null>(null)
  const [name, setName] = useState('NGC3198')
  const [np, setNp] = useState(dev.low ? 15000 : 40000)
  const [grid, setGrid] = useState(dev.low ? 64 : 128)
  const [Q, setQ] = useState(1.8)
  const [active, setActive] = useState<Record<Mode, boolean>>({ law: true, halo: true, newton: false })
  const [byRadius, setByRadius] = useState(true)
  const [playing, setPlaying] = useState(auto)                 // weak devices and reduced-motion visitors start paused
  const [resetKey, setResetKey] = useState(0)
  const [building, setBuilding] = useState(true)
  const [meta, setMeta] = useState<Meta | null>(null)
  const [curves, setCurves] = useState<Record<string, Curve>>({})
  const [tNow, setTNow] = useState(0)
  const [speed, setSpeed] = useState(dev.low ? 2 : 4)
  const [onScreen, setOnScreen] = useState(true)
  const [hidden, setHidden] = useState(false)
  const [notice, setNotice] = useState('')
  const [lost, setLost] = useState(false)
  const [err, setErr] = useState('')
  const gridRef = useRef<HTMLDivElement>(null), worker = useRef<Worker | null>(null), draws = useRef(new Map<Mode, Draw>()), last = useRef<{ xs: Float32Array[]; ys: Float32Array[] } | null>(null)
  const slow = useRef(0), stateRef = useRef({ playing, onScreen, hidden, speed })
  stateRef.current = { playing, onScreen, hidden, speed }

  useEffect(() => { fetch('/data/sparc_sim.json').then(r => r.json()).then(setData).catch(e => setErr(String(e))) }, [])
  const gal = useMemo(() => data?.galaxies.find(g => g.name === name) ?? null, [data, name])
  const modes = useMemo(() => MODES.filter(m => active[m.id]), [active])

  useEffect(() => {          // run only while the panels are on screen and the tab is visible
    const el = gridRef.current; if (!el) return
    const io = new IntersectionObserver(es => setOnScreen(es[0].isIntersecting), { threshold: 0.05 }); io.observe(el)
    const vis = () => setHidden(document.hidden); document.addEventListener('visibilitychange', vis); vis()
    return () => { io.disconnect(); document.removeEventListener('visibilitychange', vis) }
  }, [meta])

  const send = (msg: unknown) => worker.current?.postMessage(msg)

  // (re)build in the worker: terminating the old one frees its memory at once
  useEffect(() => {
    if (!data || !gal || !modes.length) return
    setBuilding(true); setMeta(null); setErr(''); last.current = null; slow.current = 0
    worker.current?.terminate()
    let w: Worker
    try { w = new Worker(new URL('./sim.worker.ts', import.meta.url)) } catch (e) { setErr('This browser cannot run the live simulation (no Web Worker support).'); return }
    worker.current = w
    w.onmessage = (ev: MessageEvent) => {
      const m = ev.data
      if (m.type === 'ready') {
        const cv: Record<string, Curve> = {}
        m.modes.forEach((id: string, i: number) => { cv[id] = m.curves[i] })
        last.current = { xs: m.xs, ys: m.ys }
        setCurves(cv); setTNow(0); setMeta({ modes: m.modes, L: m.L, R99: m.R99, np: m.np, vc0: m.vc0, x0: m.x0, y0: m.y0 }); setBuilding(false)
        w.postMessage({ type: 'speed', value: stateRef.current.speed })
        if (stateRef.current.playing && stateRef.current.onScreen && !stateRef.current.hidden) w.postMessage({ type: 'run' })
      } else if (m.type === 'frame') {
        last.current = { xs: m.xs, ys: m.ys }
        requestAnimationFrame(() => { modes.forEach((md, i) => draws.current.get(md.id)?.(m.xs[i], m.ys[i])); w.postMessage({ type: 'ack' }) })
        setTNow(m.t)
        if (m.curves) { const cv: Record<string, Curve> = {}; modes.forEach((md, i) => { cv[md.id] = m.curves[i] }); setCurves(cv) }
        // a device that cannot keep up gets a lighter simulation instead of a stuttering page
        slow.current = m.stepMs * modes.length > 40 ? slow.current + 1 : 0
        if (slow.current > 12) {
          slow.current = 0
          if (grid > 64) { setGrid(64); setNp(n => Math.min(n, 15000)); setNotice('This device is slow, so the simulation switched to a lighter setting (64² grid, 15,000 particles).') }
          else { setPlaying(false); setNotice('This device cannot run the simulation smoothly even in the lightest setting, so it is paused. Try one run at a time or fewer particles.') }
        }
      } else if (m.type === 'error') setErr(m.message)
    }
    w.onerror = () => setErr('The simulation worker stopped unexpectedly.')
    w.postMessage({ type: 'init', gal, kernel: data.kernel, a0: data.a0_kms2_per_kpc, modes: modes.map(m => m.id), N: grid, np, Q })
    return () => { w.terminate(); if (worker.current === w) worker.current = null }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [data, gal, modes, grid, np, Q, resetKey])

  useEffect(() => { send({ type: playing && onScreen && !hidden && meta ? 'run' : 'pause' }) }, [playing, onScreen, hidden, meta])   // eslint-disable-line react-hooks/exhaustive-deps
  useEffect(() => { send({ type: 'speed', value: speed }) }, [speed])                                                           // eslint-disable-line react-hooks/exhaustive-deps

  const register = useCallback((id: Mode) => (d: Draw | null) => {
    if (d) { draws.current.set(id, d); const i = modes.findIndex(m => m.id === id); if (last.current && i >= 0) d(last.current.xs[i], last.current.ys[i]) } else draws.current.delete(id)
  }, [modes])

  const rms = useCallback((cv?: Curve) => {
    if (!cv || !gal) return null
    let s = 0, n = 0
    gal.R.forEach((R, i) => { if (R <= cv.R[0] || R >= cv.R[cv.R.length - 1] || gal.Vobs[i] <= 0) return; s += Math.log10(Math.max(interp(cv.R, cv.V, R), 1) / gal.Vobs[i]) ** 2; n++ })
    return n ? Math.sqrt(s / n) : null
  }, [gal])

  if (err && !data) return <div className="min-h-screen bg-white flex items-center justify-center text-gray-500 px-6 text-center">{err}</div>
  if (!data || !gal) return <div className="min-h-screen bg-white flex items-center justify-center text-gray-500">Loading the SPARC disks…</div>
  const tGyr = tNow * GYR_PER_UNIT
  const vd = meta ? interp(meta.vc0[0].R, meta.vc0[0].V, gal.Rd) : 100
  const orbits = (tNow * vd) / (2 * Math.PI * gal.Rd)
  const sc = (id: string) => MODES.find(m => m.id === id)!.color
  const lawIdx = meta ? meta.modes.indexOf('law') : -1
  return (
    <div className="min-h-screen bg-white">
      <div className="max-w-6xl mx-auto px-4 md:px-6">
        <header className="pt-8 pb-6">
          <nav className="text-sm mb-6"><Link href="/" className="text-gray-600 hover:text-gray-900">← home</Link></nav>
          <h1 className="text-3xl md:text-4xl font-semibold text-gray-900 mb-3">A real galaxy, live, under the law</h1>
          <p className="text-gray-700 max-w-3xl">
            Pick one of {data.summary.n} real SPARC disk galaxies. Its stars become {np.toLocaleString()} particles sampled from the measured surface brightness, and the page integrates them in your browser.
            With the law and a₀ fixed by the cosmological constant, nothing is fitted to the rotation curve. Beside it runs the standard picture, where a dark halo has to be fitted to that curve point by point.
          </p>
          {!auto && <p className="mt-3 text-sm text-gray-600 max-w-3xl">{dev.reduce ? 'Your device asks for reduced motion' : 'This looks like a phone or a low-power machine'}, so the simulation starts paused and in a lighter setting. Press Start when you are ready; it pauses by itself when you scroll away.</p>}
        </header>

        {(notice || err || lost) && <div className="mb-4 text-sm rounded-md border border-amber-300 bg-amber-50 text-amber-900 px-3 py-2 max-w-3xl">{lost ? 'The graphics context was lost. Reload the page to continue.' : err || notice}</div>}

        <div className="flex flex-wrap items-end gap-4 mb-4 text-sm text-gray-700">
          <label className="block">Galaxy
            <select value={name} onChange={e => setName(e.target.value)} className="block mt-1 border border-gray-300 rounded-md px-2 py-1.5 bg-white text-gray-900 max-w-[18rem]">
              {data.galaxies.map(g => <option key={g.name} value={g.name}>{g.name} — {g.Vflat > 0 ? `Vflat ${g.Vflat.toFixed(0)} km/s` : 'no flat part'}, M* {g.Mstar.toExponential(1)}</option>)}
            </select>
          </label>
          <label className="block">Particles
            <select value={np} onChange={e => setNp(parseInt(e.target.value))} className="block mt-1 border border-gray-300 rounded-md px-2 py-1.5 bg-white text-gray-900">
              {[15000, 20000, 40000, 60000, 100000].map(n => <option key={n} value={n}>{n.toLocaleString()}</option>)}
            </select>
          </label>
          <label className="block">Grid
            <select value={grid} onChange={e => setGrid(parseInt(e.target.value))} className="block mt-1 border border-gray-300 rounded-md px-2 py-1.5 bg-white text-gray-900">
              <option value={64}>64² (light)</option><option value={128}>128² (standard)</option><option value={256}>256² (fine, 4× the work)</option>
            </select>
          </label>
          <label className="block w-40">Toomre Q at the start <span className="font-mono text-gray-900">{Q.toFixed(1)}</span>
            <input type="range" min={1.2} max={3} step={0.1} value={Q} onChange={e => setQ(parseFloat(e.target.value))} className="w-full accent-gray-900" />
          </label>
          <label className="block w-32">Speed <span className="font-mono text-gray-900">{speed}×</span>
            <input type="range" min={1} max={8} step={1} value={speed} onChange={e => setSpeed(parseInt(e.target.value))} className="w-full accent-gray-900" />
          </label>
          <button onClick={() => { setNotice(''); setPlaying(!playing) }} className="px-4 py-2 rounded-lg bg-gray-900 text-white hover:bg-gray-700 w-24">{playing ? 'Pause' : tNow > 0 ? 'Resume' : 'Start'}</button>
          <button onClick={() => { setNotice(''); setResetKey(k => k + 1) }} className="px-4 py-2 rounded-lg border border-gray-300 hover:bg-gray-50">Restart</button>
          <label className="flex items-center gap-2"><input type="checkbox" checked={byRadius} onChange={e => setByRadius(e.target.checked)} className="accent-gray-900" /> Colour by starting radius</label>
          <span className="text-xs text-gray-500 self-center">{playing && !onScreen ? 'paused while off-screen' : playing && hidden ? 'paused while the tab is hidden' : ''}</span>
        </div>
        <div className="flex flex-wrap gap-4 mb-4 text-sm text-gray-700">
          {MODES.map(m => (
            <label key={m.id} className="flex items-center gap-2"><input type="checkbox" checked={active[m.id]} onChange={e => setActive(a => ({ ...a, [m.id]: e.target.checked }))} className="accent-gray-900" />
              <span className="inline-block w-3 h-3 rounded-full" style={{ background: m.color }} /> {m.title}</label>
          ))}
          <span className="text-xs text-gray-500">each run costs about the same again; one run is the lightest</span>
        </div>

        <div ref={gridRef} className={`grid gap-4 ${modes.length === 1 ? 'grid-cols-1 max-w-xl' : modes.length === 2 ? 'sm:grid-cols-2' : 'sm:grid-cols-3'}`}>
          {modes.map(m => (
            <div key={m.id}>
              <div className="text-sm font-medium text-gray-900">{m.title}</div>
              <div className="text-xs text-gray-500 mb-1">{m.blurb}</div>
              <div className="relative w-full rounded-lg overflow-hidden border border-gray-300 bg-[#070a12]" style={{ aspectRatio: '1 / 1' }}>
                {meta && meta.modes.includes(m.id) && <Panel meta={meta} gal={gal} color={m.color} byRadius={byRadius} register={register(m.id)} onLost={() => setLost(true)} />}
                {building && <div className="absolute inset-0 flex items-center justify-center text-sm text-gray-300 bg-black/40">building the disk…</div>}
                <div className="absolute left-2 bottom-1 text-[11px] text-gray-400 pointer-events-none">face-on · ring = one disk scale length ({gal.Rd.toFixed(2)} kpc)</div>
              </div>
              <div className="text-xs text-gray-600 mt-1 font-mono">curve vs data now: {rms(curves[m.id])?.toFixed(3) ?? '–'} dex</div>
            </div>
          ))}
        </div>

        <div className="grid lg:grid-cols-[minmax(0,1fr)_20rem] gap-6 mt-6 items-start">
          <div>
            <div className="text-sm font-medium text-gray-900 mb-1">Rotation curve of the simulated disks, against the measured one</div>
            <Plot height={340} xLabel="radius (kpc)" yLabel="circular speed (km/s)" yMin={0}
              series={[
                { label: 'SPARC data', color: '#111827', points: true, x: gal.R, y: gal.Vobs, err: gal.eV },
                ...modes.filter(m => curves[m.id]).map(m => ({ label: m.title, color: m.color, x: curves[m.id].R, y: curves[m.id].V, dash: m.id === 'newton' ? '5 4' : undefined })),
              ]} />
          </div>
          <div className="space-y-3 text-sm">
            <div className="grid grid-cols-2 gap-3">
              <div className="rounded-lg border border-gray-200 px-3 py-2"><div className="text-xs text-gray-500">simulated time</div><div className="text-lg font-semibold font-mono text-gray-900">{tGyr < 1 ? `${Math.round(tGyr * 1000)} Myr` : `${tGyr.toFixed(2)} Gyr`}</div><div className="text-xs text-gray-500">{orbits.toFixed(1)} orbits at R_d</div></div>
              <div className="rounded-lg border border-gray-200 px-3 py-2"><div className="text-xs text-gray-500">baryon mass</div><div className="text-lg font-semibold font-mono text-gray-900">{gal.Mstar.toExponential(1)}</div><div className="text-xs text-gray-500">M☉ stars, Υ = {data.ups}</div></div>
            </div>
            <div className="rounded-lg border border-gray-200 px-3 py-2">
              <div className="text-xs text-gray-500 mb-1">free parameters used to match the observed curve</div>
              <div className="text-gray-900"><span className="font-semibold" style={{ color: sc('law') }}>the law: none</span> (a₀ is fixed; Υ is the record&apos;s 0.61, shared by every run)</div>
              <div className="text-gray-900"><span className="font-semibold" style={{ color: sc('halo') }}>the halo: {gal.R.length}</span>, one value of its field per data radius</div>
            </div>
            <p className="text-xs text-gray-500">On this galaxy the law, with nothing fitted, reproduces the curve to {lawIdx >= 0 ? rms(meta!.vc0[lawIdx])?.toFixed(3) : '–'} dex at the start. Over the whole disk-only SPARC set, the law on these model baryons is as good as on SPARC&apos;s own tabulated curves ({data.summary.law_rms_dex_median.toFixed(3)} against {data.summary.law_tab_rms_dex_median.toFixed(3)} dex, unweighted per-galaxy medians).</p>
          </div>
        </div>

        <section className="py-8 mt-8 border-t border-gray-200">
          <h2 className="text-2xl font-semibold text-gray-900 mb-3">What this is, and what it is not</h2>
          <ul className="list-disc pl-5 space-y-2 text-sm text-gray-700 max-w-3xl">
            <li><strong>It is not unique to the framework.</strong> This is the MOND-type law, which fits rotation curves without a halo. What is specific here is the value of a₀, tied to the cosmological constant and held fixed. The record&apos;s κ = ½ is fitted, and a₀ itself is not derived from first principles.</li>
            <li><strong>Both runs match the curve, for different reasons.</strong> The halo run matches it because the halo was fitted to it, so that match is not a test. The law run matches it with nothing fitted, so its match is a prediction; on this one galaxy that is a small piece of the record&apos;s whole-sample result (rms 0.10 dex over SPARC).</li>
            <li><strong>The law is applied in a simplified form.</strong> The boost is the algebraic law of the record, applied to the azimuthally averaged field at each radius and recomputed every step. For an axisymmetric disk that is exactly the law fitted to SPARC. It is not QUMOND, which solves a curl-free phantom field in three dimensions, and a pointwise version drifted in angular momentum (+12% in 1 Gyr) before it was changed to this one (about 2%). Treat bars, spiral arms and any difference between the runs as indicative, not as results.</li>
            <li>The gas is not live. SPARC&apos;s own tabulated gas contribution is used as a fixed field, so there is no star formation, no gas inflow and no hydrodynamics. Galaxies with a bulge ({data.summary.skipped.bulge}) and short rotation curves ({data.summary.skipped.short}) are left out. The disk is thin, with SPARC&apos;s own thickness correction applied to the force; the stellar force reproduces SPARC&apos;s stellar curve to {(data.summary.star_frac_rms_median * 100).toFixed(1)}% (median).</li>
            <li>The particles are initialised on circular orbits plus a Toomre-set velocity dispersion, without a full equilibrium solution, so a little settling happens in the first orbit. Particle number, grid and Q change the details; the 64² grid is coarse, with cells of order a kiloparsec for large galaxies.</li>
            <li><strong>It is built to be gentle on ordinary machines.</strong> The physics runs in a background thread so the page never freezes, uses at most about 60% of one core, stops when you scroll away or switch tabs, and starts paused on phones and low-power devices. If your device cannot keep up it drops to a lighter setting by itself.</li>
          </ul>
          <p className="mt-6 text-xs text-gray-500 max-w-3xl">Data: SPARC (Lelli, McGaugh &amp; Schombert 2016) via the repository copy, Υ_disk = 0.61, the record&apos;s kernel ν_mono, a₀ canonical. Files are made by <code>ai_slop/website/scripts/build_sparc_sim.py</code>; the engine is <code>src/components/galaxysim/engine.ts</code> and is tested headless by <code>scripts/test_galaxy_engine.mts</code>.</p>
        </section>
      </div>
    </div>
  )
}
