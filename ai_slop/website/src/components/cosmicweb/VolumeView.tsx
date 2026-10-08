'use client'

import React, { useEffect, useRef, useState } from 'react'
import * as THREE from 'three'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js'
import { CosmicMeta, densityLut, divergingLut, fetchPreview } from './data'

export type View = 'res' | 's0' | 'diff'

const VERT = /* glsl */ `
out vec3 vOrigin;
out vec3 vDir;
void main() {
  vOrigin = (inverse(modelMatrix) * vec4(cameraPosition, 1.0)).xyz;
  vDir = position - vOrigin;
  gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
}`

const FRAG = /* glsl */ `
precision highp float;
precision highp sampler3D;
in vec3 vOrigin;
in vec3 vDir;
layout(location = 0) out highp vec4 outColor;
uniform sampler3D uA;     // framework log10 density (0..1)
uniform sampler3D uB;     // control
uniform sampler3D uF;     // switch field of the framework run
uniform sampler2D uLut;
uniform sampler2D uDiv;
uniform int uView;        // 0 framework, 1 control, 2 difference
uniform int uSwitch;
uniform float uCut;
uniform float uGain;
uniform float uSteps;
uniform float uRange;     // dex spanned by the 0..1 range
uniform float uDiffScale; // dex mapped to the full diverging colour

vec2 hitBox(vec3 o, vec3 d) {
  vec3 inv = 1.0 / d;
  vec3 t0 = (-0.5 - o) * inv, t1 = (0.5 - o) * inv;
  vec3 tmin = min(t0, t1), tmax = max(t0, t1);
  return vec2(max(max(tmin.x, tmin.y), tmin.z), min(min(tmax.x, tmax.y), tmax.z));
}
float hash(vec2 p) { return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453); }

void main() {
  vec3 d = normalize(vDir);
  vec2 t = hitBox(vOrigin, d);
  t.x = max(t.x, 0.0);
  if (t.x >= t.y) discard;
  float dt = (t.y - t.x) / uSteps;
  float s = t.x + dt * hash(gl_FragCoord.xy);
  vec4 acc = vec4(0.0);
  for (float i = 0.0; i < 600.0; i++) {
    if (i >= uSteps) break;
    vec3 q = (vOrigin + d * s + 0.5).zyx;     // textures are stored (width, height, depth) = (z, y, x)
    vec3 col; float a;
    float va = texture(uA, q).r;
    if (uView == 2) {
      float vb = texture(uB, q).r;
      float diff = (va - vb) * uRange / uDiffScale;
      a = smoothstep(uCut, uCut + 0.3, max(va, vb)) * smoothstep(0.03, 0.5, abs(diff));
      col = texture(uDiv, vec2(clamp(diff, -1.0, 1.0) * 0.5 + 0.5, 0.5)).rgb;
    } else {
      float v = uView == 0 ? va : texture(uB, q).r;
      a = smoothstep(uCut, uCut + 0.3, v) * (0.15 + v);
      col = texture(uLut, vec2(v, 0.5)).rgb;
    }
    a = clamp(a * uGain * dt * 7.0, 0.0, 1.0);
    if (uSwitch == 1) {
      float fa = smoothstep(0.08, 0.6, texture(uF, q).r);
      col = mix(col, vec3(0.2, 0.95, 0.85), fa * 0.8);
      a = max(a, fa * 0.5 * clamp(dt * 40.0, 0.0, 1.0));
    }
    acc.rgb += (1.0 - acc.a) * a * col;
    acc.a += (1.0 - acc.a) * a;
    if (acc.a > 0.97) break;
    s += dt;
  }
  outColor = vec4(acc.rgb / max(acc.a, 1e-4), acc.a);
}`

function tex3(data: Uint8Array, n: number) {
  const t = new THREE.Data3DTexture(data, n, n, n)
  t.format = THREE.RedFormat
  t.type = THREE.UnsignedByteType
  t.minFilter = THREE.LinearFilter
  t.magFilter = THREE.LinearFilter
  t.wrapS = t.wrapT = t.wrapR = THREE.ClampToEdgeWrapping
  t.unpackAlignment = 1
  t.needsUpdate = true
  return t
}

function lutTex(data: Uint8Array) {
  const t = new THREE.DataTexture(data, 256, 1, THREE.RGBAFormat)
  t.minFilter = t.magFilter = THREE.LinearFilter
  t.needsUpdate = true
  return t
}

interface Props {
  meta: CosmicMeta
  view: View
  showSwitch: boolean
  cut: number            // log10 of the density (x mean) below which samples are hidden
  gain: number
  rotate: boolean
}

export default function VolumeView({ meta, view, showSwitch, cut, gain, rotate }: Props) {
  const host = useRef<HTMLDivElement>(null)
  const st = useRef<{ mat: THREE.ShaderMaterial; orbit: OrbitControls; dirty: () => void } | null>(null)
  const [err, setErr] = useState('')
  const [ready, setReady] = useState(false)
  const [loaded, setLoaded] = useState(false)

  useEffect(() => {
    const el = host.current!
    let renderer: THREE.WebGLRenderer
    try {
      renderer = new THREE.WebGLRenderer({ antialias: false, alpha: false, powerPreference: 'high-performance' })
    } catch {
      setErr('WebGL2 is not available in this browser.')
      return
    }
    if (!renderer.capabilities.isWebGL2) { setErr('WebGL2 is not available in this browser.'); return }
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.5))
    renderer.setClearColor(0x070a12, 1)
    el.appendChild(renderer.domElement)
    Object.assign(renderer.domElement.style, { width: '100%', height: '100%', display: 'block', touchAction: 'none' })

    const scene = new THREE.Scene()
    const camera = new THREE.PerspectiveCamera(40, 1, 0.05, 20)
    camera.position.set(1.5, 1.1, 1.6)
    const orbit = new OrbitControls(camera, renderer.domElement)
    orbit.enableDamping = true; orbit.dampingFactor = 0.08; orbit.enablePan = false; orbit.minDistance = 0.7; orbit.maxDistance = 4
    orbit.autoRotateSpeed = 0.7

    const blank = new Uint8Array(8)
    const mat = new THREE.ShaderMaterial({
      glslVersion: THREE.GLSL3,
      vertexShader: VERT, fragmentShader: FRAG, side: THREE.BackSide, transparent: true, depthWrite: false,
      uniforms: {
        uA: { value: tex3(blank, 2) }, uB: { value: tex3(blank, 2) }, uF: { value: tex3(blank, 2) },
        uLut: { value: lutTex(densityLut()) }, uDiv: { value: lutTex(divergingLut()) },
        uView: { value: 0 }, uSwitch: { value: 0 }, uCut: { value: 0.4 }, uGain: { value: 3 }, uSteps: { value: 260 },
        uRange: { value: meta.log_hi - meta.log_lo }, uDiffScale: { value: 0.15 },
      },
    })
    const box = new THREE.Mesh(new THREE.BoxGeometry(1, 1, 1), mat)
    scene.add(box)
    const edges = new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.BoxGeometry(1, 1, 1)), new THREE.LineBasicMaterial({ color: 0x3b4663 }))
    scene.add(edges)

    let need = true, visible = true, raf = 0
    const dirty = () => { need = true }
    const resize = () => {
      const w = el.clientWidth, h = el.clientHeight
      renderer.setSize(w, h, false); camera.aspect = w / Math.max(h, 1); camera.updateProjectionMatrix(); need = true
    }
    resize()
    orbit.addEventListener('change', dirty)
    const ro = new ResizeObserver(resize); ro.observe(el)
    const io = new IntersectionObserver(es => { visible = es[0].isIntersecting; need = true }, { threshold: 0 }); io.observe(el)
    const loop = () => {
      raf = requestAnimationFrame(loop)
      if (!visible) return
      orbit.update()
      if (need || orbit.autoRotate) { renderer.render(scene, camera); need = false }
    }
    loop()
    st.current = { mat, orbit, dirty }
    setReady(true)
    return () => {
      cancelAnimationFrame(raf); ro.disconnect(); io.disconnect(); orbit.dispose()
      for (const k of ['uA', 'uB', 'uF', 'uLut', 'uDiv']) mat.uniforms[k].value.dispose()
      mat.dispose(); box.geometry.dispose(); edges.geometry.dispose(); renderer.dispose()
      if (renderer.domElement.parentElement === el) el.removeChild(renderer.domElement)
      st.current = null; setReady(false)
    }
  }, [meta])

  useEffect(() => {
    if (!ready) return
    let dead = false
    Promise.all([fetchPreview('vol128_res.u8.gz'), fetchPreview('vol128_s0.u8.gz'), fetchPreview('swi128.u8.gz')])
      .then(([a, b, f]) => {
        if (dead || !st.current) return
        const u = st.current.mat.uniforms
        for (const k of ['uA', 'uB', 'uF']) u[k].value.dispose()
        u.uA.value = tex3(a, 128); u.uB.value = tex3(b, 128); u.uF.value = tex3(f, 128)
        setLoaded(true); st.current.dirty()
      })
      .catch(e => { if (!dead) setErr(String(e.message || e)) })
    return () => { dead = true }
  }, [ready])

  useEffect(() => {
    const s = st.current
    if (!s) return
    const u = s.mat.uniforms
    u.uView.value = view === 'res' ? 0 : view === 's0' ? 1 : 2
    u.uSwitch.value = showSwitch ? 1 : 0
    u.uCut.value = (cut - meta.log_lo) / (meta.log_hi - meta.log_lo)
    u.uGain.value = gain
    s.orbit.autoRotate = rotate
    s.dirty()
  }, [view, showSwitch, cut, gain, rotate, loaded, ready, meta])

  return (
    <div className="relative w-full rounded-xl overflow-hidden border border-gray-300 bg-[#070a12]" style={{ aspectRatio: '16 / 10' }}>
      <div ref={host} className="absolute inset-0" />
      {(err || !loaded) && <div className="absolute inset-0 flex items-center justify-center text-sm text-gray-300 bg-black/40 pointer-events-none px-6 text-center">{err || 'Loading 2 MB of the real 512³ run…'}</div>}
      <div className="absolute left-3 bottom-2 text-[11px] text-gray-400 pointer-events-none">
        drag to rotate · scroll to zoom · box = {meta.L} Mpc/h per side · 512³ run at z = 0, averaged to 128³
      </div>
    </div>
  )
}
