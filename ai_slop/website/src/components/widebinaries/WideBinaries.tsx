'use client'

import React, { useEffect, useMemo, useRef, useState } from 'react'
import Link from 'next/link'
import Plot from '@/components/toscale/Plot'

type Foot = 'canonical' | 'alt'
interface Fit { g: number; s: number; chi2: number; nb: number; kappa: number }
interface Res {
  inject: number
  first: { med: (number | null)[]; sig: (number | null)[]; cnt: number[]; deep: number; fit: Fit }
  gamma_hat: number[]; sigma_fit: number[]; mean: number; rms: number; mean_sigma: number
}
interface Ens {
  footing: Foot; a0: number; y_extN: number; n_data: number; K: number; master_pairs: number; edges: number[]; centres: number[]; vtcap: number
  thresholds: { newton: number; arm_b: number; arm_b_sigma: number; arm_b_kill: number; arm_a_falsified_below: number; noverdict_edge: number; kappa_window: number[]; arm_a_floor: number; arm_a_top: number; mond: number }
  results: Record<string, Res>; curves: Record<string, { gamma: number; med: (number | null)[] }>
  scaling: { n: number; mean: number; rms: number; mean_sigma: number; reps: number }[]
  seed: number; runtime_s: number; pair_ranges: { logy: number[]; vt: number[] }; pair_counts: number[]; pipeline: string
}

const BASE = '/data/wb'
const NAMES = ['Newton / Arm B', 'Arm A band floor', 'Arm A band top', 'MOND benchmark']
const COL: Record<string, string> = { 'Newton / Arm B': '#2563eb', 'Arm A band floor': '#ea580c', 'Arm A band top': '#b45309', 'MOND benchmark': '#7c3aed' }
const LABEL: Record<string, string> = {
  'Newton / Arm B': 'Newton (and Arm B)', 'Arm A band floor': 'Arm A, floor of the band', 'Arm A band top': 'Arm A, top of the band', 'MOND benchmark': 'MOND benchmark (not a framework number)',
}

function Seg<T extends string>({ value, onChange, options }: { value: T; onChange: (v: T) => void; options: [T, string][] }) {
  return (
    <div className="flex flex-wrap gap-2">
      {options.map(([v, l]) => (
        <button key={v} onClick={() => onChange(v)}
          className={`px-3 py-1.5 rounded-md border text-sm ${value === v ? 'bg-gray-900 text-white border-gray-900' : 'border-gray-300 text-gray-800 hover:bg-gray-50'}`}>{l}</button>
      ))}
    </div>
  )
}

function Stat({ label, value, note }: { label: string; value: string; note?: string }) {
  return (
    <div className="rounded-lg border border-gray-200 px-3 py-2">
      <div className="text-xs text-gray-500">{label}</div>
      <div className="text-lg font-semibold text-gray-900 font-mono">{value}</div>
      {note && <div className="text-xs text-gray-500">{note}</div>}
    </div>
  )
}

/** one mock catalog: every pair is a dot, with the binned medians and the pipeline's forward-model curves on top */
function Scatter({ ens, pairs, inj }: { ens: Ens; pairs: Uint16Array | null; inj: number }) {
  const cv = useRef<HTMLCanvasElement>(null)
  const name = NAMES[inj]
  const res = ens.results[name]
  useEffect(() => {
    const c = cv.current
    if (!c) return
    const dpr = Math.min(window.devicePixelRatio || 1, 2), W = c.clientWidth, H = Math.round(W * 0.62)
    c.width = W * dpr; c.height = H * dpr; c.style.height = `${H}px`
    const g = c.getContext('2d')!
    g.setTransform(dpr, 0, 0, dpr, 0, 0); g.clearRect(0, 0, W, H)
    const m = { l: 48, r: 12, t: 10, b: 38 }, [x0, x1] = ens.pair_ranges.logy, y0 = 0, y1 = 2.2
    const X = (v: number) => m.l + ((v - x0) / (x1 - x0)) * (W - m.l - m.r), Y = (v: number) => H - m.b - ((v - y0) / (y1 - y0)) * (H - m.t - m.b)
    g.strokeStyle = '#e5e7eb'; g.fillStyle = '#6b7280'; g.font = '11px sans-serif'; g.lineWidth = 1
    for (let v = -1; v <= 2; v++) { g.beginPath(); g.moveTo(X(v), m.t); g.lineTo(X(v), H - m.b); g.stroke(); g.textAlign = 'center'; g.fillText(String(v), X(v), H - m.b + 15) }
    for (let v = 0; v <= 2; v += 0.5) { g.beginPath(); g.moveTo(m.l, Y(v)); g.lineTo(W - m.r, Y(v)); g.stroke(); g.textAlign = 'right'; g.fillText(v.toFixed(1), m.l - 6, Y(v) + 4) }
    g.fillStyle = '#374151'; g.textAlign = 'center'; g.fillText('log₁₀ y  (y = Newtonian acceleration at the projected separation / a₀;  left = wider, weaker pairs)', (m.l + W - m.r) / 2, H - 4)
    g.save(); g.translate(13, (m.t + H - m.b) / 2); g.rotate(-Math.PI / 2); g.fillText('ṽ = v⊥ / v_circ', 0, 0); g.restore()
    if (pairs) {
      const off = ens.pair_counts.slice(0, inj).reduce((a, b) => a + b, 0), n = ens.pair_counts[inj]
      g.fillStyle = COL[name] + '38'
      for (let i = 0; i < n; i++) {
        const lx = pairs[(off + i) * 2] / 65535 * (x1 - x0) + x0, v = pairs[(off + i) * 2 + 1] / 65535 * ens.vtcap
        if (v > y1) continue
        g.fillRect(X(lx) - 0.6, Y(v) - 0.6, 1.4, 1.4)
      }
    }
    // pipeline forward-model curves (noise-convolved), then this catalog's medians
    for (const nm of NAMES) {
      const cu = ens.curves[nm]; g.strokeStyle = COL[nm]; g.lineWidth = nm === name ? 2.2 : 1.2; g.setLineDash(nm === name ? [] : [5, 4]); g.beginPath()
      let started = false
      cu.med.forEach((v, i) => { if (v == null) return; const px = X(ens.centres[i]), py = Y(v); if (!started) { g.moveTo(px, py); started = true } else g.lineTo(px, py) })
      g.stroke()
    }
    g.setLineDash([])
    res.first.med.forEach((v, i) => {
      if (v == null) return
      const px = X(ens.centres[i]), s = res.first.sig[i] ?? 0
      g.strokeStyle = '#111827'; g.lineWidth = 1.5; g.beginPath(); g.moveTo(px, Y(v - 2 * s)); g.lineTo(px, Y(v + 2 * s)); g.stroke()
      g.fillStyle = '#111827'; g.beginPath(); g.arc(px, Y(v), 3.5, 0, 2 * Math.PI); g.fill()
    })
  }, [ens, pairs, inj, name, res])
  return <canvas ref={cv} className="w-full block rounded-lg border border-gray-200 bg-white" />
}

/** histogram of the gamma recovered from the independent mock catalogs, per injected value, with the registered thresholds */
function Hist({ ens }: { ens: Ens }) {
  const W = 760, H = 300, m = { l: 44, r: 12, t: 16, b: 44 }, lo = 0.94, hi = 1.4, nb = 56
  const X = (v: number) => m.l + ((v - lo) / (hi - lo)) * (W - m.l - m.r)
  const bins = NAMES.map(n => { const b = new Array(nb).fill(0); ens.results[n].gamma_hat.forEach(g => { const i = Math.floor(((g - lo) / (hi - lo)) * nb); if (i >= 0 && i < nb) b[i]++ }); return b })
  const ymax = Math.max(...bins.flat()) * 1.12, Y = (v: number) => H - m.b - (v / ymax) * (H - m.t - m.b)
  const t = ens.thresholds
  const marks: [number, string, string][] = [[t.newton, 'Newton', '#2563eb'], [t.arm_a_falsified_below, 'Arm A falsified below', '#9ca3af'], [t.arm_b_kill, 'Arm B killed above', '#9ca3af'], [t.noverdict_edge, 'no-verdict edge', '#9ca3af']]
  return (
    <svg viewBox={`0 0 ${W} ${H}`} className="w-full h-auto" role="img" aria-label="Distribution of the recovered gamma for each injected value">
      <rect x={X(t.arm_a_floor)} y={m.t} width={X(t.arm_a_top) - X(t.arm_a_floor)} height={H - m.t - m.b} fill="#ea580c" opacity={0.12} />
      {[1.0, 1.1, 1.2, 1.3, 1.4].map(v => (<g key={v}><line x1={X(v)} x2={X(v)} y1={m.t} y2={H - m.b} stroke="#e5e7eb" /><text x={X(v)} y={H - m.b + 15} fontSize="11" textAnchor="middle" fill="#6b7280">{v.toFixed(1)}</text></g>))}
      {marks.map(([v, l, c], i) => (<g key={l}><line x1={X(v)} x2={X(v)} y1={m.t} y2={H - m.b} stroke={c} strokeDasharray="4 4" /><text x={X(v) + 3} y={m.t + 10 + i * 11} fontSize="10" fill="#4b5563">{l} {v.toFixed(v === 1 ? 2 : 3)}</text></g>))}
      {NAMES.map(n => {
        const b = bins[NAMES.indexOf(n)]
        const d = b.map((c, i) => `${i ? 'L' : 'M'}${X(lo + (i / nb) * (hi - lo)).toFixed(1)},${Y(c).toFixed(1)}L${X(lo + ((i + 1) / nb) * (hi - lo)).toFixed(1)},${Y(c).toFixed(1)}`).join('')
        return <path key={n} d={d} fill="none" stroke={COL[n]} strokeWidth={2} />
      })}
      <line x1={m.l} x2={W - m.r} y1={H - m.b} y2={H - m.b} stroke="#9ca3af" />
      <text x={(m.l + W - m.r) / 2} y={H - 6} fontSize="12" textAnchor="middle" fill="#374151">recovered γ (the deep-regime velocity boost) from one mock DR4 catalog of {ens.n_data.toLocaleString()} pairs</text>
      <text x={14} y={(m.t + H - m.b) / 2} fontSize="12" textAnchor="middle" fill="#374151" transform={`rotate(-90 14 ${(m.t + H - m.b) / 2})`}>catalogs (of {ens.K})</text>
    </svg>
  )
}

export default function WideBinaries() {
  const [foot, setFoot] = useState<Foot>('canonical')
  const [inj, setInj] = useState(1)
  const [ens, setEns] = useState<Record<Foot, Ens | null>>({ canonical: null, alt: null })
  const [pairs, setPairs] = useState<Record<Foot, Uint16Array | null>>({ canonical: null, alt: null })
  const [err, setErr] = useState('')
  useEffect(() => {
    for (const f of ['canonical', 'alt'] as Foot[]) fetch(`${BASE}/ensemble_${f}.json`).then(r => r.json()).then(d => setEns(e => ({ ...e, [f]: d }))).catch(e => setErr(String(e)))
  }, [])
  useEffect(() => {
    if (pairs[foot]) return
    fetch(`${BASE}/pairs_${foot}.bin`).then(r => r.arrayBuffer()).then(b => setPairs(p => ({ ...p, [foot]: new Uint16Array(b) }))).catch(e => setErr(String(e)))
  }, [foot, pairs])
  const E = ens[foot]
  const sep = useMemo(() => {
    if (!E) return null
    const r = (n: string) => E.results[n]
    const newton = r(NAMES[0]), fl = r(NAMES[1]), tp = r(NAMES[2]), md = r(NAMES[3])
    const s = Math.max(newton.rms, fl.rms)
    return { floor: (fl.mean - newton.mean) / s, top: (tp.mean - newton.mean) / s, mond: (md.mean - newton.mean) / s, mondVsTop: (md.mean - tp.mean) / Math.max(md.rms, tp.rms), arm: (tp.mean - fl.mean) / Math.max(tp.rms, fl.rms), sigma: s }
  }, [E])
  const other = ens[foot === 'canonical' ? 'alt' : 'canonical']
  const footSep = useMemo(() => (E && other ? (other.results[NAMES[1]].mean - E.results[NAMES[1]].mean) / Math.max(other.results[NAMES[1]].rms, E.results[NAMES[1]].rms) : null), [E, other])
  if (err) return <div className="min-h-screen bg-white flex items-center justify-center text-gray-500">Could not load the mock-sky data.</div>
  if (!ens.canonical || !ens.alt || !E) return <div className="min-h-screen bg-white flex items-center justify-center text-gray-500">Loading the mock sky…</div>
  const name = NAMES[inj], res = E.results[name], t = E.thresholds
  const sc = E.scaling
  return (
    <div className="min-h-screen bg-white">
      <div className="max-w-6xl mx-auto px-4 md:px-6">
        <header className="pt-8 pb-6">
          <nav className="text-sm mb-6"><Link href="/" className="text-gray-600 hover:text-gray-900">← home</Link></nav>
          <h1 className="text-3xl md:text-4xl font-semibold text-gray-900 mb-3">What Gaia DR4 will see: a mock wide-binary sky</h1>
          <p className="text-gray-700 max-w-3xl">
            Gaia DR4 is due on 2 December 2026. Wide binary stars, pairs a few thousand to thirty thousand AU apart, feel such weak gravity that a MOND-type law would make them orbit faster than Newton allows.
            This page runs the repository&apos;s <em>frozen pre-registered pipeline</em> on synthetic catalogs: the same population, the same Gaia DR4-level errors, the same estimator and fit, with different laws injected.
            It shows what the data would look like, and what the pipeline would return. It is a forecast, not a measurement.
          </p>
        </header>

        <section className="py-8 border-t border-gray-200">
          <div className="text-xs uppercase tracking-wider text-gray-500 mb-1">one mock catalog</div>
          <h2 className="text-2xl font-semibold text-gray-900 mb-3">{E.n_data.toLocaleString()} wide binaries</h2>
          <p className="text-gray-700 max-w-3xl mb-4 text-sm">
            Each dot is one mock pair (Keplerian orbit, random orientation, thermal eccentricities, Gaia errors, the frozen selection). The vertical axis is its relative speed in units of the Newtonian circular speed;
            Because only the sky-projected speed is seen, Newton puts the median near 0.53 at every separation. A boost lifts the left side, where gravity is weakest, by roughly the factor γ. Black points are this catalog&apos;s median per bin, with ±2σ; lines are the pipeline&apos;s own forward models for each law.
          </p>
          <div className="flex flex-wrap gap-4 mb-3">
            <Seg value={String(inj)} onChange={v => setInj(parseInt(v))} options={NAMES.map((n, i) => [String(i), LABEL[n]] as [string, string])} />
            <Seg value={foot} onChange={setFoot} options={[['canonical', 'a₀ canonical 9.36×10⁻¹¹'], ['alt', 'a₀ alt 1.13×10⁻¹⁰']]} />
          </div>
          <Scatter ens={E} pairs={pairs[foot]} inj={inj} />
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mt-4">
            <Stat label="injected γ" value={res.inject.toFixed(4)} note={LABEL[name]} />
            <Stat label="recovered from this catalog" value={`${res.first.fit.g.toFixed(4)} ± ${res.first.fit.s.toFixed(4)}`} note={`${((res.first.fit.g - 1) / res.first.fit.s).toFixed(1)}σ above Newton`} />
            <Stat label="pairs in the deep bins" value={res.first.deep.toLocaleString()} note="y < 0.3, where the boost lives" />
            <Stat label="nuisance κ" value={res.first.fit.kappa.toFixed(3)} note={`window ${t.kappa_window[0]}–${t.kappa_window[1]}`} />
          </div>
        </section>

        <section className="py-8 border-t border-gray-200">
          <div className="text-xs uppercase tracking-wider text-gray-500 mb-1">repeat it {E.K} times</div>
          <h2 className="text-2xl font-semibold text-gray-900 mb-3">If nature is this, what does DR4 return?</h2>
          <p className="text-gray-700 max-w-3xl mb-4 text-sm">
            {E.K} independent mock catalogs for each injected law, each fitted by the pipeline. The orange band is the in-force Arm A prediction (Amendment 10). Newton and the covariant Arm B both sit on the left curve.
          </p>
          <Hist ens={E} />
          <div className="flex flex-wrap gap-x-4 gap-y-1 text-xs text-gray-700 mt-1">
            {NAMES.map(n => (<span key={n} className="flex items-center gap-1.5"><span className="inline-block w-4 h-0.5" style={{ background: COL[n] }} />{LABEL[n]}: {E.results[n].mean.toFixed(3)} ± {E.results[n].rms.toFixed(3)}</span>))}
          </div>
          {sep && (
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mt-4">
              <Stat label="Arm A floor vs Newton" value={`${sep.floor.toFixed(1)}σ`} note={`σ = ${sep.sigma.toFixed(3)} per catalog`} />
              <Stat label="Arm A top vs Newton" value={`${sep.top.toFixed(1)}σ`} />
              <Stat label="Arm A top vs MOND benchmark" value={`${sep.mondVsTop.toFixed(1)}σ`} note="a different law, told apart" />
              <Stat label="canonical vs alt footing" value={footSep == null ? '–' : `${Math.abs(footSep).toFixed(1)}σ`} note="floor of the band; not separable" />
            </div>
          )}
        </section>

        <section className="py-8 border-t border-gray-200">
          <div className="text-xs uppercase tracking-wider text-gray-500 mb-1">how many pairs</div>
          <h2 className="text-2xl font-semibold text-gray-900 mb-3">The statistical error shrinks as 1/√N</h2>
          <div className="grid lg:grid-cols-2 gap-8 items-start">
            <div>
              <Plot logX logY height={300} xLabel="pairs in the catalog" yLabel="error on the recovered γ" xMarks={[{ x: 8611, label: '8.6k: Banik+24 strict DR3' }, { x: 30000, label: '30k registered' }]}
                series={[
                  { label: 'pipeline fit error σ_fit', color: '#ea580c', x: sc.map(s => s.n), y: sc.map(s => s.mean_sigma) },
                  { label: 'scatter of the recovered γ', color: '#111827', dash: '5 4', x: sc.map(s => s.n), y: sc.map(s => s.rms) },
                  { label: 'a 3σ detection of the Arm A floor', color: '#9ca3af', dash: '2 3', x: [sc[0].n, sc[sc.length - 1].n], y: [(t.arm_a_floor - 1) / 3, (t.arm_a_floor - 1) / 3] },
                ]} />
            </div>
            <div className="text-sm text-gray-700 space-y-2">
              <p>Counting only the statistical error, the Arm A floor ({t.arm_a_floor.toFixed(4)}) crosses 3σ above Newton at roughly {Math.round(Math.pow((3 * (sc.find(s => s.n === E.n_data)?.mean_sigma ?? 0.017)) / (t.arm_a_floor - 1), 2) * E.n_data / 100) * 100} pairs on this population, and is well past it at the registered {E.n_data.toLocaleString()}.</p>
              <p>For scale: 8,611 pairs is the size of the strict Gaia DR3 sample of Banik et al. 2024 (MNRAS 527, 4573), whose cuts the pre-registration largely adopts; the looser DR3 selection of Chae 2023 has about 26,000. The record notes that their disagreement is about exactly these selection choices.</p>
              <p>The registered systematic allowance is 0.02 on γ, comparable to the statistical error at 30,000 pairs, so the real margin is smaller than these numbers suggest. The two a₀ footings differ by only {Math.abs((ens.alt.thresholds.arm_a_floor - ens.canonical.thresholds.arm_a_floor)).toFixed(3)} in γ, which this sample size cannot resolve: the record keeps that fork undecided.</p>
            </div>
          </div>
        </section>

        <section className="py-8 border-t border-gray-200">
          <div className="text-xs uppercase tracking-wider text-gray-500 mb-1">read this</div>
          <h2 className="text-2xl font-semibold text-gray-900 mb-3">What this is, and what it is not</h2>
          <ul className="list-disc pl-5 space-y-2 text-sm text-gray-700 max-w-3xl">
            <li><strong>Only Arm A is testable here.</strong> The record has two arms: Arm A, modified gravity, predicts the orange band; Arm B, the covariant candidate, predicts {t.arm_b.toFixed(4)} ± {t.arm_b_sigma} with this estimator and is registered as <em>not testable</em> by it (Amendment 12). A Newtonian result would falsify Arm A (below {t.arm_a_falsified_below}); it would not touch Arm B.</li>
            <li><strong>Not unique to the framework.</strong> A speed-up of wide binaries is what any MOND-type law predicts, and Newton and ΛCDM predict none. What is specific here is the band itself, which comes from the framework&apos;s kernel and external-field treatment with a₀ tied to the cosmological constant. The record notes that γ constrains that prescription, not the a₀ value: a 22% change in a₀ moves γ by about 3%.</li>
            <li><strong>It is the pipeline testing itself.</strong> The mock catalogs come from the same code that defines the estimator, so recovering the injected value is a self-consistency check. The boost is the pipeline&apos;s phenomenological injection (a velocity scaling at fixed orbit, applied at the true acceleration), not a self-consistent modified-orbit integration, which the record lists as the upgrade path.</li>
            <li>The Gaia error model is approximate and cited in the pipeline; the real DR4 catalog will bring its own contamination (hidden companions, chance alignments), which the registered cuts try to remove and the registered systematic allowance tries to bound. A DR3-era dry run of the same estimator on a public catalog exists in the record, with its own caveats, and is not a DR4 test.</li>
            <li>Settings are the pipeline&apos;s: {E.master_pairs.toLocaleString()} pairs in the model master MC, N = {E.n_data.toLocaleString()}, seed {E.seed}, {E.K} catalogs per law. Injected values and thresholds are read from the pipeline&apos;s constants, not typed in.</li>
          </ul>
          <p className="mt-6 text-xs text-gray-500 max-w-3xl">
            Record: <a className="text-blue-600 hover:underline" href="https://github.com/carlzimmerman/zimmerman-formula/blob/main/prep_2026/gaia_dr4_prep/wide_binary_pipeline.py" target="_blank" rel="noopener noreferrer">wide_binary_pipeline.py</a> ·{' '}
            <a className="text-blue-600 hover:underline" href="https://github.com/carlzimmerman/zimmerman-formula/blob/main/prep_2026/gaia_dr4_prep/PREREGISTRATION_DR4.md" target="_blank" rel="noopener noreferrer">the DR4 pre-registration</a>. Files are made by <code>ai_slop/website/scripts/build_wb_mock_sky.py</code>, which imports the pipeline unchanged.
          </p>
        </section>
      </div>
    </div>
  )
}
