'use client'

import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import { COUNT_DECODE, CosmicMeta, NC, densityLut, divergingLut, fmtBytes, loadAtlas } from './data'
import type { View } from './VolumeView'

const A = 4 * NC               // atlas side: 4 x 4 layers of 512 x 512 cells
const DIFF_DEX = 0.3

interface Props { meta: CosmicMeta; view: View; showSwitch: boolean }

export default function LayerView({ meta, view, showSwitch }: Props) {
  const [started, setStarted] = useState(false)
  const [res, setRes] = useState<Uint8Array | null>(null)
  const [s0, setS0] = useState<Uint8Array | null>(null)
  const [swi, setSwi] = useState<Uint8Array | null>(null)
  const [err, setErr] = useState('')
  const [k, setK] = useState(7)
  const [hover, setHover] = useState('')
  const canvas = useRef<HTMLCanvasElement>(null)
  const off = useRef<HTMLCanvasElement | null>(null)
  const tf = useRef({ s: 1, x: 0, y: 0 })
  const drag = useRef<{ x: number; y: number } | null>(null)
  const lut = useMemo(() => densityLut(), [])
  const div = useMemo(() => divergingLut(), [])
  const cell = meta.L / NC
  const needS0 = view !== 'res', needRes = view !== 's0'

  useEffect(() => {
    if (!started) return
    if (needRes && !res) loadAtlas('layers_res.png', A, A).then(setRes).catch(e => setErr(e.message))
    if (needS0 && !s0) loadAtlas('layers_s0.png', A, A).then(setS0).catch(e => setErr(e.message))
    if (!swi) loadAtlas('layers_swi.png', A, A).then(setSwi).catch(e => setErr(e.message))
  }, [started, needRes, needS0, res, s0, swi])

  const ready = view === 'res' ? !!res : view === 's0' ? !!s0 : !!(res && s0)

  const draw = useCallback(() => {
    const cv = canvas.current
    if (!cv || !ready) return
    if (!off.current) { off.current = document.createElement('canvas'); off.current.width = NC; off.current.height = NC }
    const oc = off.current, og = oc.getContext('2d')!
    const img = og.createImageData(NC, NC), o = img.data
    const r = Math.floor(k / 4), c = k % 4
    const map = (cnt: number) => (cnt < 0.02 ? 0 : Math.max(0, Math.min(255, Math.round(((Math.log10(cnt) - meta.log_lo) / (meta.log_hi - meta.log_lo)) * 255))))
    for (let i = 0; i < NC; i++) {
      const base = (r * NC + i) * A + c * NC
      for (let j = 0; j < NC; j++) {
        const p = base + j
        let R: number, G: number, B: number
        if (view === 'diff') {
          const d = (Math.log10(COUNT_DECODE[res![p]] + 0.25) - Math.log10(COUNT_DECODE[s0![p]] + 0.25)) / DIFF_DEX
          const li = Math.round((Math.max(-1, Math.min(1, d)) * 0.5 + 0.5) * 255) * 4
          R = div[li]; G = div[li + 1]; B = div[li + 2]
        } else {
          const li = map(COUNT_DECODE[(view === 'res' ? res! : s0!)[p]]) * 4
          R = lut[li]; G = lut[li + 1]; B = lut[li + 2]
        }
        if (showSwitch && swi && swi[p] > 100) { const m = Math.min(1, swi[p] / 220) * 0.8; R = R * (1 - m) + 50 * m; G = G * (1 - m) + 242 * m; B = B * (1 - m) + 218 * m }
        const q = (i * NC + j) * 4
        o[q] = R; o[q + 1] = G; o[q + 2] = B; o[q + 3] = 255
      }
    }
    og.putImageData(img, 0, 0)
    const dpr = Math.min(window.devicePixelRatio || 1, 2)
    const W = Math.round(cv.clientWidth * dpr)
    if (cv.width !== W) { cv.width = W; cv.height = W }
    const g = cv.getContext('2d')!
    g.setTransform(1, 0, 0, 1, 0, 0); g.fillStyle = '#070a12'; g.fillRect(0, 0, W, W)
    g.imageSmoothingEnabled = false
    const t = tf.current, sc = (W / NC) * t.s
    g.drawImage(oc, 0, 0, NC, NC, t.x * dpr, t.y * dpr, NC * sc, NC * sc)
  }, [ready, k, view, showSwitch, swi, res, s0, lut, div, meta])

  useEffect(() => { draw() }, [draw])
  useEffect(() => { const f = () => draw(); window.addEventListener('resize', f); return () => window.removeEventListener('resize', f) }, [draw])

  const clampPan = (w: number) => { const t = tf.current; t.x = Math.min(0, Math.max(w - w * t.s, t.x)); t.y = Math.min(0, Math.max(w - w * t.s, t.y)) }
  useEffect(() => {
    const cv = canvas.current
    if (!cv) return
    const h = (e: WheelEvent) => {
      e.preventDefault()
      const rc = cv.getBoundingClientRect(), t = tf.current
      const mx = e.clientX - rc.left, my = e.clientY - rc.top
      const ns = Math.max(1, Math.min(48, t.s * (e.deltaY < 0 ? 1.25 : 1 / 1.25)))
      t.x = mx - ((mx - t.x) / t.s) * ns; t.y = my - ((my - t.y) / t.s) * ns
      t.s = ns; clampPan(rc.width); draw()
    }
    cv.addEventListener('wheel', h, { passive: false })
    return () => cv.removeEventListener('wheel', h)
  }, [draw, started])

  const onMove = (e: React.PointerEvent) => {
    const rc = canvas.current!.getBoundingClientRect(), t = tf.current
    if (drag.current) {
      t.x += e.clientX - drag.current.x; t.y += e.clientY - drag.current.y; drag.current = { x: e.clientX, y: e.clientY }
      clampPan(rc.width); draw(); return
    }
    if (!ready) return
    const css = rc.width / NC
    const j = Math.floor((e.clientX - rc.left - t.x) / (css * t.s)), i = Math.floor((e.clientY - rc.top - t.y) / (css * t.s))
    if (i < 0 || j < 0 || i >= NC || j >= NC) { setHover(''); return }
    const p = (Math.floor(k / 4) * NC + i) * A + (k % 4) * NC + j
    const num = (a: Uint8Array | null) => { if (!a) return '–'; const c = COUNT_DECODE[a[p]]; return c < 127.5 ? String(Math.round(c)) : `~${Math.round(c)}` }
    setHover(`x ${(i * cell).toFixed(1)}, y ${(j * cell).toFixed(1)} Mpc/h · cell holds ${view === 's0' ? num(s0) : num(res)} particles${view === 'diff' ? ` (framework) and ${num(s0)} (control)` : view === 's0' ? ' (control)' : ' (framework)'}`)
  }

  const zc = meta.layers[k]
  const need = (needRes ? meta.bytes.layers_res : 0) + (needS0 ? meta.bytes.layers_s0 : 0) + meta.bytes.layers_swi
  if (!started) {
    return (
      <div className="rounded-xl border border-gray-300 bg-gray-50 p-6 text-sm text-gray-700 max-w-3xl">
        Sixteen full-resolution layers of the real 512³ run, one for every 12.5 Mpc/h of depth. Each pixel is one {cell.toFixed(2)} Mpc/h cell and you can zoom until you see single cells and their exact particle counts.
        <div className="mt-3">
          <button onClick={() => setStarted(true)} className="px-4 py-2 rounded-lg bg-gray-900 text-white text-sm hover:bg-gray-700">Load the layers ({fmtBytes(need)})</button>
        </div>
      </div>
    )
  }
  return (
    <div className="grid lg:grid-cols-[minmax(0,1fr)_17rem] gap-5 items-start">
      <div>
        <div className="relative w-full rounded-xl overflow-hidden border border-gray-300 bg-[#070a12]" style={{ aspectRatio: '1 / 1' }}>
          <canvas ref={canvas} className="w-full h-full block cursor-grab active:cursor-grabbing touch-none" style={{ imageRendering: 'pixelated' }}
            onPointerDown={e => { drag.current = { x: e.clientX, y: e.clientY }; (e.target as HTMLElement).setPointerCapture(e.pointerId) }}
            onPointerUp={() => { drag.current = null }}
            onPointerMove={onMove}
            onPointerLeave={() => setHover('')}
            onDoubleClick={() => { tf.current = { s: 1, x: 0, y: 0 }; draw() }} />
          {!ready && <div className="absolute inset-0 flex items-center justify-center text-sm text-gray-300 bg-black/40 pointer-events-none">{err || `Loading ${fmtBytes(need)}…`}</div>}
        </div>
        <div className="text-xs text-gray-600 mt-1 min-h-[1rem] font-mono">{hover || 'scroll to zoom up to 48×, drag to pan, double-click to reset'}</div>
      </div>
      <div className="space-y-3 text-sm text-gray-700">
        <label className="block">
          <span className="flex justify-between"><span>Layer</span><span className="font-mono text-gray-900">{k + 1} of 16 · z = {(zc * cell).toFixed(1)} Mpc/h</span></span>
          <input type="range" min={0} max={meta.layers.length - 1} step={1} value={k} onChange={e => setK(parseInt(e.target.value))} className="w-full accent-gray-900" />
        </label>
        <p className="text-xs text-gray-500">
          One pixel is one grid cell, 0.39 Mpc/h across, coloured by how many of the 134 million particles sit in it (log scale, 0.03× to 300× the mean of 1).
          {view === 'diff' && ` Difference: blue where the control has more particles, orange where the framework run has more; full colour at ±${DIFF_DEX} dex. Single cells are noisy, so expect speckle.`}
          {showSwitch && ' Cyan: where the framework run’s switch is on.'}
        </p>
      </div>
    </div>
  )
}
