'use client'

import React, { useEffect, useMemo, useRef, useState } from 'react'
import * as THREE from 'three'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js'
import Plot from '@/components/toscale/Plot'
import { BASE, CosmicMeta, HaloInfo, fmtBytes, fmtMass } from './data'

type Mode = 'fw' | 's0' | 'both' | 'move' | 'switch'
const MODES: [Mode, string][] = [['fw', 'Framework'], ['s0', 'Control'], ['both', 'Both overlaid'], ['move', 'Colour by how far each moved'], ['switch', 'Where the switch is on']]

const VERT = /* glsl */ `
attribute float aMove;
attribute float aF;
uniform float uSize;
uniform float uScale;
uniform int uMode;
uniform vec3 uColor;
varying vec3 vCol;
void main() {
  vec4 mv = modelViewMatrix * vec4(position, 1.0);
  gl_Position = projectionMatrix * mv;
  gl_PointSize = max(1.6, uSize * uScale / -mv.z);
  if (uMode == 3) {
    float t = clamp((log2(max(aMove, 1e-4)) + 7.0) / 9.0, 0.0, 1.0);    // 8 kpc/h .. 4 Mpc/h
    vec3 lo = vec3(0.15, 0.45, 1.0), mid = vec3(1.0, 0.9, 0.3), hi = vec3(1.0, 0.15, 0.1);
    vCol = t < 0.5 ? mix(lo, mid, t * 2.0) : mix(mid, hi, (t - 0.5) * 2.0);
  } else if (uMode == 4) {
    vCol = aF > 0.5 ? vec3(0.2, 0.95, 0.85) : vec3(0.55, 0.42, 0.35);
  } else {
    vCol = uColor;
  }
}`
const FRAG = /* glsl */ `
precision highp float;
uniform float uAlpha;
varying vec3 vCol;
void main() {
  float r = length(gl_PointCoord - 0.5) * 2.0;
  if (r > 1.0) discard;
  float a = (1.0 - r * r) * uAlpha;
  gl_FragColor = vec4(vCol * a, a);
}`

interface Parsed { fw: Float32Array; s0: Float32Array; f: Float32Array; move: Float32Array; n: number }

function parse(buf: ArrayBuffer, h: HaloInfo, scale: number): Parsed {
  const n = h.n_shown, k = scale / 32767
  const a = new Int16Array(buf, 0, 3 * n), b = new Int16Array(buf, 6 * n, 3 * n), f8 = new Uint8Array(buf, 12 * n, n)
  const fw = new Float32Array(3 * n), s0 = new Float32Array(3 * n), f = new Float32Array(n), move = new Float32Array(n)
  for (let i = 0; i < n; i++) {
    let m = 0
    for (let c = 0; c < 3; c++) { fw[3 * i + c] = a[3 * i + c] * k; s0[3 * i + c] = b[3 * i + c] * k; const d = fw[3 * i + c] - s0[3 * i + c]; m += d * d }
    move[i] = Math.sqrt(m)
    f[i] = f8[i] / 255
  }
  return { fw, s0, f, move, n }
}

/** density / cosmic mean in each shell from the stored radial counts (every particle of that run, about that run's own centre) */
function profile(counts: number[], edges: number[], cell: number) {
  const x: number[] = [], y: number[] = []
  counts.forEach((c, i) => {
    const r1 = edges[i], r2 = edges[i + 1], v = (4 / 3) * Math.PI * (r2 ** 3 - r1 ** 3)
    x.push(Math.sqrt(r1 * r2)); y.push((c / v) * cell ** 3)
  })
  return { x, y }
}

export default function HaloView({ meta }: { meta: CosmicMeta }) {
  const [sel, setSel] = useState(0)
  const [mode, setMode] = useState<Mode>('both')
  const [size, setSize] = useState(0.02)
  const [alpha, setAlpha] = useState(0.1)
  const [rotate, setRotate] = useState(true)
  const [data, setData] = useState<Parsed | null>(null)
  const [err, setErr] = useState('')
  const host = useRef<HTMLDivElement>(null)
  const st = useRef<{ fw: THREE.Points; s0: THREE.Points; mats: THREE.ShaderMaterial[]; orbit: OrbitControls; dirty: () => void; set: (p: Parsed) => void } | null>(null)
  const h = meta.halos[sel]
  const cell = meta.L / meta.N

  useEffect(() => {
    let dead = false
    setData(null); setErr('')
    fetch(`${BASE}/halo_${h.id}.bin`).then(r => r.arrayBuffer()).then(b => {
      if (dead) return
      if (b.byteLength !== h.bytes) throw new Error(`Unexpected size for halo ${h.id}`)
      setData(parse(b, h, meta.halo_scale))
    }).catch(e => { if (!dead) setErr(String(e.message || e)) })
    return () => { dead = true }
  }, [h, meta.halo_scale])

  // scene
  useEffect(() => {
    const el = host.current!
    let renderer: THREE.WebGLRenderer
    try { renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false }) } catch { setErr('WebGL is not available in this browser.'); return }
    const pr = Math.min(window.devicePixelRatio || 1, 2)
    renderer.setPixelRatio(pr); renderer.setClearColor(0x070a12, 1)
    el.appendChild(renderer.domElement)
    Object.assign(renderer.domElement.style, { width: '100%', height: '100%', display: 'block', touchAction: 'none' })
    const scene = new THREE.Scene()
    const camera = new THREE.PerspectiveCamera(45, 1, 0.01, 50)
    camera.position.set(4.6, 3.0, 5.4)
    const orbit = new OrbitControls(camera, renderer.domElement)
    orbit.enableDamping = true; orbit.dampingFactor = 0.08; orbit.enablePan = false; orbit.minDistance = 0.3; orbit.maxDistance = 30; orbit.autoRotateSpeed = 0.9
    const mk = () => new THREE.ShaderMaterial({
      vertexShader: VERT, fragmentShader: FRAG, transparent: true, depthWrite: false, depthTest: false,
      blending: THREE.CustomBlending, blendEquation: THREE.AddEquation, blendSrc: THREE.OneFactor, blendDst: THREE.OneFactor,
      uniforms: { uSize: { value: 0.02 }, uScale: { value: 500 }, uMode: { value: 0 }, uColor: { value: new THREE.Color(1, 0.55, 0.2) }, uAlpha: { value: 0.1 } },
    })
    const mats = [mk(), mk()]
    const fw = new THREE.Points(new THREE.BufferGeometry(), mats[0]); fw.frustumCulled = false
    const s0 = new THREE.Points(new THREE.BufferGeometry(), mats[1]); s0.frustumCulled = false
    scene.add(fw, s0)
    const ring = new THREE.LineLoop(new THREE.BufferGeometry().setFromPoints(Array.from({ length: 129 }, (_, i) => new THREE.Vector3(Math.cos((i / 128) * 2 * Math.PI) * meta.halo_r, 0, Math.sin((i / 128) * 2 * Math.PI) * meta.halo_r))), new THREE.LineBasicMaterial({ color: 0x2b3550 }))
    scene.add(ring)

    let need = true, visible = true, raf = 0
    const dirty = () => { need = true }
    const resize = () => {
      const w = el.clientWidth, hh = el.clientHeight
      renderer.setSize(w, hh, false); camera.aspect = w / Math.max(hh, 1); camera.updateProjectionMatrix()
      const sc = (hh * pr) / (2 * Math.tan((camera.fov * Math.PI) / 360)); mats.forEach(m => (m.uniforms.uScale.value = sc / pr)); need = true
    }
    resize()
    orbit.addEventListener('change', dirty)
    const ro = new ResizeObserver(resize); ro.observe(el)
    const io = new IntersectionObserver(es => { visible = es[0].isIntersecting; need = true }, { threshold: 0 }); io.observe(el)
    const loop = () => { raf = requestAnimationFrame(loop); if (!visible) return; orbit.update(); if (need || orbit.autoRotate) { renderer.render(scene, camera); need = false } }
    loop()
    const set = (p: Parsed) => {
      const g = (pos: Float32Array) => {
        const geo = new THREE.BufferGeometry()
        geo.setAttribute('position', new THREE.BufferAttribute(pos, 3))
        geo.setAttribute('aMove', new THREE.BufferAttribute(p.move, 1)); geo.setAttribute('aF', new THREE.BufferAttribute(p.f, 1))
        return geo
      }
      fw.geometry.dispose(); s0.geometry.dispose(); fw.geometry = g(p.fw); s0.geometry = g(p.s0); need = true
    }
    st.current = { fw, s0, mats, orbit, dirty, set }
    return () => {
      cancelAnimationFrame(raf); ro.disconnect(); io.disconnect(); orbit.dispose()
      fw.geometry.dispose(); s0.geometry.dispose(); mats.forEach(m => m.dispose()); ring.geometry.dispose(); renderer.dispose()
      if (renderer.domElement.parentElement === el) el.removeChild(renderer.domElement)
      st.current = null
    }
  }, [meta])

  useEffect(() => { if (data && st.current) st.current.set(data) }, [data])
  useEffect(() => {
    const s = st.current
    if (!s) return
    const [a, b] = s.mats
    const m = mode === 'move' ? 3 : mode === 'switch' ? 4 : 0
    a.uniforms.uMode.value = m; b.uniforms.uMode.value = 0
    a.uniforms.uColor.value.set(mode === 'both' ? 0xff8a33 : 0xffa860)
    b.uniforms.uColor.value.set(0x3d9bff)
    s.fw.visible = mode !== 's0'; s.s0.visible = mode === 's0' || mode === 'both'
    if (mode === 's0') { b.uniforms.uColor.value.set(0x8fc4ff) }
    for (const x of s.mats) { x.uniforms.uSize.value = size; x.uniforms.uAlpha.value = alpha }
    s.orbit.autoRotate = rotate
    s.dirty()
  }, [mode, size, alpha, rotate, data])

  const prof = useMemo(() => ({ fw: profile(h.prof_fw, h.prof_edges, cell), s0: profile(h.prof_s0, h.prof_edges, cell) }), [h, cell])
  const loadBytes = h.bytes

  return (
    <div>
      <div className="flex flex-wrap gap-2 mb-3">
        {meta.halos.map((x, i) => (
          <button key={x.id} onClick={() => setSel(i)}
            className={`px-3 py-1.5 rounded-lg border text-left text-xs leading-tight ${i === sel ? 'bg-gray-900 text-white border-gray-900' : 'border-gray-300 hover:bg-gray-50 text-gray-800'}`}>
            <div className="font-semibold">{x.id}</div>
            <div className="font-mono opacity-80">{fmtMass(x.mass_msun_h)} M☉/h</div>
          </button>
        ))}
      </div>
      <div className="grid lg:grid-cols-[minmax(0,1fr)_17rem] gap-5 items-start">
        <div>
          <div className="relative w-full rounded-xl overflow-hidden border border-gray-300 bg-[#070a12]" style={{ aspectRatio: '1 / 1' }}>
            <div ref={host} className="absolute inset-0" />
            {(!data || err) && <div className="absolute inset-0 flex items-center justify-center text-sm text-gray-300 bg-black/40 pointer-events-none">{err || `Loading ${h.n_shown.toLocaleString()} particles (${fmtBytes(loadBytes)})…`}</div>}
            <div className="absolute left-3 bottom-2 text-[11px] text-gray-400 pointer-events-none">
              each dot is one simulation particle (every 8th) · ring = {meta.halo_r} Mpc/h · drag to rotate, scroll to zoom
            </div>
          </div>
        </div>
        <div className="space-y-3 text-sm text-gray-700">
          <div className="flex flex-col gap-1.5">
            {MODES.map(([m, l]) => (
              <button key={m} onClick={() => setMode(m)} className={`px-3 py-1.5 rounded-md border text-left ${mode === m ? 'bg-gray-900 text-white border-gray-900' : 'border-gray-300 hover:bg-gray-50'}`}>{l}</button>
            ))}
          </div>
          <label className="block"><span className="flex justify-between"><span>Dot size</span><span className="font-mono text-gray-900">{(size * 1000).toFixed(0)} kpc/h</span></span>
            <input type="range" min={0.005} max={0.12} step={0.005} value={size} onChange={e => setSize(parseFloat(e.target.value))} className="w-full accent-gray-900" /></label>
          <label className="block"><span className="flex justify-between"><span>Brightness</span><span className="font-mono text-gray-900">{alpha.toFixed(2)}</span></span>
            <input type="range" min={0.01} max={1} step={0.01} value={alpha} onChange={e => setAlpha(parseFloat(e.target.value))} className="w-full accent-gray-900" /></label>
          <label className="flex items-center gap-2"><input type="checkbox" checked={rotate} onChange={e => setRotate(e.target.checked)} className="accent-gray-900" /> Auto-rotate</label>
          <p className="text-xs text-gray-500">
            {mode === 'both' && 'Orange: framework run. Blue: the same particles in the control run. Where a particle and its twin overlap the colours add to white; inside halos most do not.'}
            {mode === 'move' && 'Each framework particle is coloured by the distance to its own position in the control run: blue under about 10 kpc/h, yellow near 200 kpc/h, red above about 1 Mpc/h.'}
            {mode === 'switch' && 'Teal: particles in cells where the framework run’s switch is on. Brown: switch off.'}
            {mode === 'fw' && 'The framework run (CFG425 R3).'}
            {mode === 's0' && 'The Newtonian control, same particles.'}
          </p>
        </div>
      </div>
      <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-3 mt-5 text-sm">
        {[
          ['Particles within 3 Mpc/h', h.n.toLocaleString(), `${fmtMass(h.mass_msun_h)} M☉/h of total matter (${(meta.m_particle_msun_h / 1e9).toFixed(2)}×10⁹ per particle). The view draws every ${meta.halo_stride}th (${h.n_shown.toLocaleString()} dots); the numbers use all.`],
          ['Same sphere in the control', h.n_control_sphere.toLocaleString(), `${((h.n_control_sphere / h.n - 1) * 100).toFixed(1)}% vs the framework run (every particle of the control about its own centre)`],
          ['How far these particles moved', `${h.moved_median_kpc_h.toFixed(0)} kpc/h`, `median between the two runs; rms ${h.moved_rms_kpc_h.toFixed(0)} kpc/h`],
          ['Switch on', `${(h.frac_switch_on * 100).toFixed(0)}%`, 'of these particles sit in switched-on cells'],
        ].map(([a, b, c]) => (
          <div key={a} className="rounded-lg border border-gray-200 px-3 py-2">
            <div className="text-xs text-gray-500">{a}</div>
            <div className="text-lg font-semibold text-gray-900 font-mono">{b}</div>
            <div className="text-xs text-gray-500">{c}</div>
          </div>
        ))}
      </div>
      {(
        <div className="mt-6 max-w-2xl">
          <div className="text-sm font-medium text-gray-900 mb-1">Density profile of these particles</div>
          <Plot logX logY height={280} xLabel="radius from the halo centre (Mpc/h)" yLabel="density / cosmic mean"
            series={[
              { label: 'framework run', color: '#ea580c', x: prof.fw.x, y: prof.fw.y },
              { label: 'control', color: '#2563eb', x: prof.s0.x, y: prof.s0.y, dash: '5 4' },
            ]} />
          <p className="text-xs text-gray-500 mt-1">
            Each curve counts every particle of its own run, about that run&apos;s own halo centre (the two centres are {h.centre_offset_kpc_h.toFixed(0)} kpc/h apart).
            Density is in units of the cosmic mean. Forces in this run are computed on the {meta.N}³ mesh ({cell.toFixed(2)} Mpc/h cells), so inside roughly two cells (0.8 Mpc/h) the profile is set by the mesh, not by physics.
          </p>
        </div>
      )}
    </div>
  )
}
