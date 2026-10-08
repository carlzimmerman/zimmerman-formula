'use client'

import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import Plot from '@/components/toscale/Plot'
import { TimelineMeta, densityLut, divergingLut, fmtBytes, loadAtlas } from './data'

const H = 0.6736, OM = (0.02237 + 0.12) / H ** 2, OL = 1 - OM            // the engine's cosmology (cfg424_pm.py)
/** cosmic age in Gyr at scale factor a (flat LCDM) */
export const ageGyr = (a: number) => (9.778 / H) * (2 / (3 * Math.sqrt(OL))) * Math.asinh(Math.sqrt(OL / OM) * Math.pow(a, 1.5))
export const fmtAge = (g: number) => (g < 1 ? `${Math.round(g * 1000)} Myr` : `${g.toFixed(2)} Gyr`)
const FIXED_LO = -1.2, FIXED_HI = 1.6          // log10 of the slab-averaged density for the fixed colour scale
const DIFF_DEX = 0.1

interface Props { tl: TimelineMeta; frame: number; setFrame: (f: number) => void; playing: boolean; setPlaying: (p: boolean) => void }

export default function Timeline({ tl, frame, setFrame, playing, setPlaying }: Props) {
  const [started, setStarted] = useState(false)
  const [res, setRes] = useState<Uint8Array | null>(null)
  const [s0, setS0] = useState<Uint8Array | null>(null)
  const [swi, setSwi] = useState<Uint8Array | null>(null)
  const [err, setErr] = useState('')
  const [fixed, setFixed] = useState(false)
  const [showSwitch, setShowSwitch] = useState(false)
  const cRes = useRef<HTMLCanvasElement>(null), cS0 = useRef<HTMLCanvasElement>(null), cDiff = useRef<HTMLCanvasElement>(null)
  const lut = useMemo(() => densityLut(), [])
  const div = useMemo(() => divergingLut(), [])
  const n = tl.n, rows = Math.ceil(tl.frames / tl.cols), W = tl.cols * n, Hh = rows * n

  useEffect(() => {
    if (!started) return
    loadAtlas('tl_res.png', W, Hh).then(setRes).catch(e => setErr(e.message))
    loadAtlas('tl_s0.png', W, Hh).then(setS0).catch(e => setErr(e.message))
    loadAtlas('tl_swi.png', W, Hh).then(setSwi).catch(e => setErr(e.message))
  }, [started, W, Hh])

  const ready = !!(res && s0 && swi)

  const draw = useCallback(() => {
    if (!ready) return
    const r0 = Math.floor(frame / tl.cols), c0 = frame % tl.cols
    const lo = [tl.range.res[frame][0], tl.range.s0[frame][0]], hi = [tl.range.res[frame][1], tl.range.s0[frame][1]]
    const paint = (cv: HTMLCanvasElement | null, f: (i: number, j: number, p: number) => [number, number, number]) => {
      if (!cv) return
      cv.width = n; cv.height = n
      const g = cv.getContext('2d')!, img = g.createImageData(n, n), o = img.data
      for (let i = 0; i < n; i++) for (let j = 0; j < n; j++) {
        const p = (r0 * n + i) * W + c0 * n + j, [R, G, B] = f(i, j, p), q = (i * n + j) * 4
        o[q] = R; o[q + 1] = G; o[q + 2] = B; o[q + 3] = 255
      }
      g.putImageData(img, 0, 0)
    }
    const logr = (a: Uint8Array, p: number, k: number) => lo[k] + (a[p] / 255) * (hi[k] - lo[k])
    const toLut = (v: number, k: number) => {
      const t = fixed ? (v - FIXED_LO) / (FIXED_HI - FIXED_LO) : (v - lo[k]) / Math.max(hi[k] - lo[k], 1e-9)
      return Math.max(0, Math.min(255, Math.round(t * 255))) * 4
    }
    paint(cRes.current, (i, j, p) => {
      const li = toLut(logr(res!, p, 0), 0)
      let R = lut[li], G = lut[li + 1], B = lut[li + 2]
      if (showSwitch && swi![p] > 40) { const m = Math.min(1, swi![p] / 160) * 0.85; R = R * (1 - m) + 50 * m; G = G * (1 - m) + 242 * m; B = B * (1 - m) + 218 * m }
      return [R, G, B]
    })
    paint(cS0.current, (i, j, p) => { const li = toLut(logr(s0!, p, 1), 1); return [lut[li], lut[li + 1], lut[li + 2]] })
    paint(cDiff.current, (i, j, p) => {
      const d = (logr(res!, p, 0) - logr(s0!, p, 1)) / DIFF_DEX
      const li = Math.round((Math.max(-1, Math.min(1, d)) * 0.5 + 0.5) * 255) * 4
      return [div[li], div[li + 1], div[li + 2]]
    })
  }, [ready, frame, fixed, showSwitch, res, s0, swi, tl, n, W, lut, div])
  useEffect(() => { draw() }, [draw])

  // playback
  useEffect(() => {
    if (!playing) return
    const id = window.setInterval(() => setFrame(Math.min(tl.frames - 1, frame + 1)), 380)
    if (frame >= tl.frames - 1) setPlaying(false)
    return () => window.clearInterval(id)
  }, [playing, frame, tl.frames, setFrame, setPlaying])

  const a = tl.a[frame], z = tl.z[frame]
  const s8r = tl.sigma8.res[frame], s8s = tl.sigma8.s0[frame]
  const kmax = tl.k.findIndex(k => k > 1)
  const nk = kmax < 0 ? tl.k.length : kmax
  const pk = tl.k.slice(0, nk).map((k, i) => ({ k, y: (tl.P.res[frame][i] / tl.P.s0[frame][i] - 1) * 100 }))
  const span = (k: number) => `${Math.pow(10, tl.range[k === 0 ? 'res' : 's0'][frame][0]).toFixed(2)}–${Math.pow(10, tl.range[k === 0 ? 'res' : 's0'][frame][1]).toFixed(2)}×`

  if (!started) {
    return (
      <div className="rounded-xl border border-gray-300 bg-gray-50 p-6 text-sm text-gray-700 max-w-3xl">
        A replay of the same engine at {tl.n}³ ({(tl.n ** 3 / 1e6).toFixed(1)} million particles), framework run and control from the same initial conditions, with {tl.frames} frames from z = {tl.z[0].toFixed(0)} to today.
        <div className="mt-3">
          <button onClick={() => setStarted(true)} className="px-4 py-2 rounded-lg bg-gray-900 text-white text-sm hover:bg-gray-700">Load the timeline ({fmtBytes(tl.bytes.tl_res + tl.bytes.tl_s0 + tl.bytes.tl_swi)})</button>
        </div>
      </div>
    )
  }
  const Panel = ({ title, cv, note }: { title: string; cv: React.RefObject<HTMLCanvasElement>; note: string }) => (
    <div>
      <div className="text-sm font-medium text-gray-900 mb-1">{title}</div>
      <div className="relative w-full rounded-lg overflow-hidden border border-gray-300 bg-[#070a12]" style={{ aspectRatio: '1 / 1' }}>
        <canvas ref={cv} className="w-full h-full block" />
        {!ready && <div className="absolute inset-0 flex items-center justify-center text-xs text-gray-300">{err || 'loading…'}</div>}
      </div>
      <div className="text-xs text-gray-500 mt-1">{note}</div>
    </div>
  )
  return (
    <div>
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <Panel title="Framework run" cv={cRes} note={fixed ? 'fixed colour scale' : `colours span ${span(0)} the mean`} />
        <Panel title="Newtonian control" cv={cS0} note={fixed ? 'fixed colour scale' : `colours span ${span(1)} the mean`} />
        <Panel title="Difference (framework − control)" cv={cDiff} note={`blue: control denser, orange: framework denser; full colour at ±${DIFF_DEX} dex`} />
      </div>
      <div className="mt-4 flex flex-wrap items-center gap-4">
        <button onClick={() => { if (frame >= tl.frames - 1) setFrame(0); setPlaying(!playing) }} className="px-4 py-2 rounded-lg bg-gray-900 text-white text-sm hover:bg-gray-700 w-24">{playing ? 'Pause' : frame >= tl.frames - 1 ? 'Replay' : 'Play'}</button>
        <input type="range" min={0} max={tl.frames - 1} step={1} value={frame} onChange={e => { setPlaying(false); setFrame(parseInt(e.target.value)) }} className="flex-1 min-w-[12rem] accent-gray-900" />
        <label className="flex items-center gap-2 text-sm text-gray-700"><input type="checkbox" checked={fixed} onChange={e => setFixed(e.target.checked)} className="accent-gray-900" /> Same colour scale every frame</label>
        <label className="flex items-center gap-2 text-sm text-gray-700"><input type="checkbox" checked={showSwitch} onChange={e => setShowSwitch(e.target.checked)} className="accent-gray-900" /> Show where the switch is on</label>
      </div>
      <div className="mt-4 grid grid-cols-2 sm:grid-cols-4 gap-3 text-sm">
        {[
          ['redshift z', z.toFixed(z > 10 ? 1 : 2), `scale factor a = ${a.toFixed(3)}`],
          ['age of the universe', fmtAge(ageGyr(a)), `frame ${frame + 1} of ${tl.frames}`],
          ['σ₈ framework / control', `${s8r.toFixed(3)} / ${s8s.toFixed(3)}`, `ratio ${(s8r / s8s).toFixed(4)}`],
          ['switch on', `${(tl.diag.vol_on[frame] * 100).toFixed(2)}% of volume`, `${(tl.diag.mass_on[frame] * 100).toFixed(0)}% of the mass`],
        ].map(([t, v, c]) => (
          <div key={t} className="rounded-lg border border-gray-200 px-3 py-2">
            <div className="text-xs text-gray-500">{t}</div>
            <div className="text-lg font-semibold text-gray-900 font-mono">{v}</div>
            <div className="text-xs text-gray-500">{c}</div>
          </div>
        ))}
      </div>
      <p className="text-xs text-gray-500 mt-2">
        Each image is a {tl.slab_mpc_h[1] - tl.slab_mpc_h[0]} Mpc/h thick slab through the {tl.n}³ box, averaged along its depth. Early on, the contrast is a fraction of a percent, so by default every frame is stretched to its own range; tick the box to see the true scale.
      </p>
      <div className="grid md:grid-cols-3 gap-6 mt-6">
        <div>
          <div className="text-sm font-medium text-gray-900 mb-1">Growth of clustering</div>
          <Plot logX logY height={260} xLabel="scale factor a" yLabel="σ₈" xMarks={[{ x: a, label: 'now' }]}
            series={[{ label: 'framework', color: '#ea580c', x: tl.a, y: tl.sigma8.res }, { label: 'control', color: '#2563eb', dash: '5 4', x: tl.a, y: tl.sigma8.s0 }]} />
        </div>
        <div>
          <div className="text-sm font-medium text-gray-900 mb-1">σ₈, framework / control − 1</div>
          <Plot logX height={260} xLabel="scale factor a" yLabel="difference (%)" yMin={-1} xMarks={[{ x: a, label: 'now' }]}
            series={[{ label: 'framework − control', color: '#ea580c', x: tl.a, y: tl.sigma8.res.map((v, i) => (v / tl.sigma8.s0[i] - 1) * 100) }]} />
        </div>
        <div>
          <div className="text-sm font-medium text-gray-900 mb-1">Power spectrum at this frame</div>
          <Plot logX height={260} xLabel="k (h/Mpc)" yLabel="P framework / P control − 1 (%)" yMin={-12}
            series={[
              { label: 'this frame', color: '#ea580c', x: pk.map(d => d.k), y: pk.map(d => d.y) },
              { label: '±10% (frozen cut)', color: '#9ca3af', dash: '5 4', x: [pk[0]?.k ?? 0.03, pk[pk.length - 1]?.k ?? 1], y: [10, 10] },
              { label: '', color: '#9ca3af', dash: '5 4', x: [pk[0]?.k ?? 0.03, pk[pk.length - 1]?.k ?? 1], y: [-10, -10] },
            ]} />
        </div>
      </div>
    </div>
  )
}
