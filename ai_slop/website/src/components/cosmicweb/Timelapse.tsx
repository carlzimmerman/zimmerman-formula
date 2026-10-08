'use client'

import React, { useEffect, useRef, useState } from 'react'
import * as THREE from 'three'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js'
import { allowAutoMotion, getDevice, guardContext, maxPixelRatio } from '@/components/common/device'
import { BASE, TimelineMeta, fmtBytes, fmtMass } from './data'
import { ageGyr, fmtAge } from './Timeline'

const VERT = /* glsl */ `
uniform float uSize;
uniform float uScale;
void main() {
  vec4 mv = modelViewMatrix * vec4(position, 1.0);
  gl_Position = projectionMatrix * mv;
  gl_PointSize = max(1.5, uSize * uScale / -mv.z);
}`
const FRAG = /* glsl */ `
precision highp float;
uniform vec3 uColor;
uniform float uAlpha;
void main() {
  float r = length(gl_PointCoord - 0.5) * 2.0;
  if (r > 1.0) discard;
  float a = (1.0 - r * r) * uAlpha;
  gl_FragColor = vec4(uColor * a, a);
}`

export default function Timelapse({ tl, frame }: { tl: TimelineMeta; frame: number }) {
  const host = useRef<HTMLDivElement>(null)
  const st = useRef<{ pts: THREE.Points[]; mats: THREE.ShaderMaterial[]; orbit: OrbitControls; dirty: () => void; set: (run: number, p: Float32Array) => void } | null>(null)
  const [data, setData] = useState<Int16Array | null>(null)
  const [started, setStarted] = useState(false)
  const [err, setErr] = useState('')
  const [physical, setPhysical] = useState(true)
  const [showFw, setShowFw] = useState(true)
  const [showCtl, setShowCtl] = useState(true)
  const [size, setSize] = useState(0.35)
  const [alpha, setAlpha] = useState(0.5)
  const [rotate, setRotate] = useState(() => allowAutoMotion(getDevice()))
  const hl = tl.halo, F = tl.frames, N = hl.n

  useEffect(() => {
    if (!started) return
    let dead = false
    fetch(`${BASE}/tl_halo.bin`).then(r => r.arrayBuffer()).then(b => {
      if (dead) return
      if (b.byteLength !== 2 * F * N * 6) throw new Error('Unexpected size for the halo time-lapse')
      setData(new Int16Array(b))
    }).catch(e => { if (!dead) setErr(String(e.message || e)) })
    return () => { dead = true }
  }, [started, F, N])

  useEffect(() => {
    if (!started) return
    const el = host.current!
    let renderer: THREE.WebGLRenderer
    try { renderer = new THREE.WebGLRenderer({ antialias: false, alpha: false, powerPreference: 'low-power' }) } catch { setErr('WebGL is not available in this browser.'); return }
    const pr = maxPixelRatio(getDevice())
    renderer.setPixelRatio(pr); renderer.setClearColor(0x070a12, 1)
    el.appendChild(renderer.domElement)
    const unguard = guardContext(renderer.domElement, () => setErr('The graphics context was lost. Reload the page to see this view.'))
    Object.assign(renderer.domElement.style, { width: '100%', height: '100%', display: 'block', touchAction: 'none' })
    const scene = new THREE.Scene()
    const camera = new THREE.PerspectiveCamera(45, 1, 0.05, 500)
    camera.position.set(14, 9, 16)
    const orbit = new OrbitControls(camera, renderer.domElement)
    orbit.enableDamping = true; orbit.dampingFactor = 0.08; orbit.enablePan = false; orbit.minDistance = 1; orbit.maxDistance = 120; orbit.autoRotateSpeed = 0.8
    const mk = (c: number) => new THREE.ShaderMaterial({
      vertexShader: VERT, fragmentShader: FRAG, transparent: true, depthWrite: false, depthTest: false,
      blending: THREE.CustomBlending, blendEquation: THREE.AddEquation, blendSrc: THREE.OneFactor, blendDst: THREE.OneFactor,
      uniforms: { uSize: { value: 0.35 }, uScale: { value: 500 }, uColor: { value: new THREE.Color(c) }, uAlpha: { value: 0.5 } },
    })
    const mats = [mk(0xff8a33), mk(0x3d9bff)]
    const pts = mats.map(m => { const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.BufferAttribute(new Float32Array(3 * N), 3)); const p = new THREE.Points(g, m); p.frustumCulled = false; scene.add(p); return p })
    let need = true, visible = true, raf = 0
    const dirty = () => { need = true }
    const resize = () => {
      const w = el.clientWidth, h = el.clientHeight
      renderer.setSize(w, h, false); camera.aspect = w / Math.max(h, 1); camera.updateProjectionMatrix()
      const sc = (h * pr) / (2 * Math.tan((camera.fov * Math.PI) / 360)); mats.forEach(m => (m.uniforms.uScale.value = sc / pr)); need = true
    }
    resize()
    orbit.addEventListener('change', dirty)
    const ro = new ResizeObserver(resize); ro.observe(el)
    const io = new IntersectionObserver(es => { visible = es[0].isIntersecting; need = true }, { threshold: 0 }); io.observe(el)
    const loop = () => { raf = requestAnimationFrame(loop); if (!visible || document.hidden) return; orbit.update(); if (need || orbit.autoRotate) { renderer.render(scene, camera); need = false } }
    loop()
    const set = (run: number, p: Float32Array) => { const at = pts[run].geometry.getAttribute('position') as THREE.BufferAttribute; (at.array as Float32Array).set(p); at.needsUpdate = true; need = true }
    st.current = { pts, mats, orbit, dirty, set }
    return () => {
      cancelAnimationFrame(raf); unguard(); ro.disconnect(); io.disconnect(); orbit.dispose()
      pts.forEach(p => p.geometry.dispose()); mats.forEach(m => m.dispose()); renderer.dispose()
      if (renderer.domElement.parentElement === el) el.removeChild(renderer.domElement)
      st.current = null
    }
  }, [started, N])

  useEffect(() => {
    const s = st.current
    if (!s || !data) return
    const k = (hl.scale / 32767) * (physical ? tl.a[frame] : 1)
    for (let run = 0; run < 2; run++) {
      const out = new Float32Array(3 * N), off = (run * F + frame) * N * 3
      for (let i = 0; i < 3 * N; i++) out[i] = data[off + i] * k
      s.set(run, out)
    }
  }, [data, frame, physical, hl.scale, tl.a, F, N])

  useEffect(() => {
    const s = st.current
    if (!s) return
    s.pts[0].visible = showFw; s.pts[1].visible = showCtl
    for (const m of s.mats) { m.uniforms.uSize.value = size * (physical ? 0.25 : 1); m.uniforms.uAlpha.value = alpha }
    s.orbit.autoRotate = rotate
    s.dirty()
  }, [showFw, showCtl, size, alpha, rotate, physical, started])

  if (!started) {
    return (
      <div className="rounded-xl border border-gray-300 bg-gray-50 p-6 text-sm text-gray-700 max-w-3xl">
        Follow {N.toLocaleString()} particles of the halo at the densest peak of the box ({fmtMass(hl.mass_msun_h)} M☉/h within 3 Mpc/h in the framework run today) back through all {F} frames, in both runs. The particles are picked from the framework run&apos;s halo at z = 0 and tracked by id.
        <div className="mt-3"><button onClick={() => setStarted(true)} className="px-4 py-2 rounded-lg bg-gray-900 text-white text-sm hover:bg-gray-700">Load the time-lapse ({fmtBytes(tl.bytes.tl_halo)})</button></div>
      </div>
    )
  }
  return (
    <div className="grid lg:grid-cols-[minmax(0,1fr)_17rem] gap-5 items-start">
      <div className="relative w-full rounded-xl overflow-hidden border border-gray-300 bg-[#070a12]" style={{ aspectRatio: '1 / 1' }}>
        <div ref={host} className="absolute inset-0" />
        {(!data || err) && <div className="absolute inset-0 flex items-center justify-center text-sm text-gray-300 bg-black/40 pointer-events-none">{err || 'Loading…'}</div>}
        <div className="absolute left-3 bottom-2 text-[11px] text-gray-400 pointer-events-none">
          z = {tl.z[frame].toFixed(2)} · {fmtAge(ageGyr(tl.a[frame]))} · drag to rotate, scroll to zoom
        </div>
      </div>
      <div className="space-y-3 text-sm text-gray-700">
        <label className="flex items-center gap-2"><input type="checkbox" checked={showFw} onChange={e => setShowFw(e.target.checked)} className="accent-gray-900" /> <span className="inline-block w-3 h-3 rounded-full" style={{ background: '#ff8a33' }} /> Framework run</label>
        <label className="flex items-center gap-2"><input type="checkbox" checked={showCtl} onChange={e => setShowCtl(e.target.checked)} className="accent-gray-900" /> <span className="inline-block w-3 h-3 rounded-full" style={{ background: '#3d9bff' }} /> Control run</label>
        <label className="flex items-center gap-2"><input type="checkbox" checked={physical} onChange={e => setPhysical(e.target.checked)} className="accent-gray-900" /> Physical sizes (shrink with the expansion)</label>
        <label className="flex items-center gap-2"><input type="checkbox" checked={rotate} onChange={e => setRotate(e.target.checked)} className="accent-gray-900" /> Auto-rotate</label>
        <label className="block"><span className="flex justify-between"><span>Dot size</span><span className="font-mono text-gray-900">{size.toFixed(2)}</span></span>
          <input type="range" min={0.05} max={1.5} step={0.05} value={size} onChange={e => setSize(parseFloat(e.target.value))} className="w-full accent-gray-900" /></label>
        <label className="block"><span className="flex justify-between"><span>Brightness</span><span className="font-mono text-gray-900">{alpha.toFixed(2)}</span></span>
          <input type="range" min={0.05} max={1} step={0.05} value={alpha} onChange={e => setAlpha(parseFloat(e.target.value))} className="w-full accent-gray-900" /></label>
        <p className="text-xs text-gray-500">
          It follows the frame slider above. Where a particle and its twin overlap, orange and blue add to white. Positions are relative to the halo&apos;s centre at z = 0, in {physical ? 'physical' : 'comoving'} Mpc/h. At z = 0 the framework run holds {hl.n_sphere_res.toLocaleString()} particles inside 3 Mpc/h of the centre and the control {hl.n_sphere_s0.toLocaleString()}.
        </p>
      </div>
    </div>
  )
}
