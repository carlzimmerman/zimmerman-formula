'use client'

import React, { useEffect, useMemo, useState } from 'react'
import Link from 'next/link'
import Plot from '@/components/toscale/Plot'
import { BASE, CosmicMeta, NC, TimelineMeta, fmtBytes } from './data'
import VolumeView, { View } from './VolumeView'
import LayerView from './LayerView'
import HaloView from './HaloView'
import Timeline from './Timeline'
import Timelapse from './Timelapse'
import Gate from '@/components/common/Gate'
import { getDevice } from '@/components/common/device'

function Section({ id, kicker, title, children }: { id: string; kicker: string; title: string; children: React.ReactNode }) {
  return (
    <section id={id} className="py-10 border-t border-gray-200">
      <div className="text-xs uppercase tracking-wider text-gray-500 mb-1">{kicker}</div>
      <h2 className="text-2xl font-semibold text-gray-900 mb-3">{title}</h2>
      {children}
    </section>
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

const median = (a: number[]) => { const b = [...a].sort((x, y) => x - y), m = b.length >> 1; return b.length % 2 ? b[m] : (b[m - 1] + b[m]) / 2 }

export default function CosmicWeb() {
  const [meta, setMeta] = useState<CosmicMeta | null>(null)
  const [tl, setTl] = useState<TimelineMeta | null | undefined>(undefined)
  const [metaErr, setMetaErr] = useState('')
  useEffect(() => {
    fetch(`${BASE}/meta.json`).then(r => r.json()).then(setMeta).catch(e => setMetaErr(String(e)))
    fetch(`${BASE}/timeline.json`).then(r => (r.ok ? r.json() : null)).then(setTl).catch(() => setTl(null))
  }, [])

  const [frame, setFrame] = useState(0)
  const [playing, setPlaying] = useState(false)
  // whole-box 3D
  const [view, setView] = useState<View>('res')
  const [cut, setCut] = useState(0.15)
  const [gain, setGain] = useState(3)
  const [rotate, setRotate] = useState(false)
  const [showSwitch, setShowSwitch] = useState(false)
  // layers
  const [sView, setSView] = useState<View>('res')
  const [sSwitch, setSSwitch] = useState(false)

  const pk = useMemo(() => {
    if (!meta) return null
    const a = meta.rec.res, b = meta.rec.s0
    const interp = (k: number) => {
      const j = b.k.findIndex(x => x >= k)
      if (j <= 0) return b.P[0]
      const u = (k - b.k[j - 1]) / (b.k[j] - b.k[j - 1]); return b.P[j - 1] * (1 - u) + b.P[j] * u
    }
    const x: number[] = [], y: number[] = []
    a.k.forEach((k, i) => { if (k <= 1 && k >= b.k[0]) { x.push(k); y.push((a.P[i] / interp(k) - 1) * 100) } })
    return { x, y }
  }, [meta])

  if (metaErr) return <div className="min-h-screen bg-white flex items-center justify-center text-gray-500">Could not load the simulation data.</div>
  if (!meta || tl === undefined) return <div className="min-h-screen bg-white flex items-center justify-center text-gray-500">Loading the simulation record…</div>

  const r = meta.rec.res, s = meta.rec.s0, pc = meta.particle_cmp, st = meta.stats
  const hrs = (r.runtime_s / 3600).toFixed(1)
  const bd = st.by_density_128
  const nav: [string, string][] = [...(tl ? [['timeline', '1 · timeline'] as [string, string]] : []), ['box', 'whole box'], ['layers', 'layers'], ['halo', 'inside a halo'], ['numbers', 'how they differ'], ['notes', 'what this is']]

  return (
    <div className="min-h-screen bg-white">
      <div className="max-w-6xl mx-auto px-4 md:px-6">
        <header className="pt-8 pb-6">
          <nav className="text-sm mb-6"><Link href="/" className="text-gray-600 hover:text-gray-900">← home</Link></nav>
          <h1 className="text-3xl md:text-4xl font-semibold text-gray-900 mb-3">The simulation behind the growth check</h1>
          <p className="text-gray-700 max-w-3xl">
            This is real output of the engine that tested the framework&apos;s growth rule (CFG425): the {hrs}-hour, {(NC ** 3).toLocaleString()}-particle run in a {meta.L} Mpc/h box, {tl ? `a ${tl.n}³ replay of the same engine to show it forming through time, ` : ''}
            and a Newtonian control started from identical initial conditions, so row <em>i</em> of both files is the same particle. It checks that the framework&apos;s rule does not break the cosmic web. It does not show that the framework is right,
            and a standard simulation looks the same by design.
          </p>
          <div className="flex flex-wrap gap-3 mt-4 text-sm">
            {nav.map(([id, l]) => (
              <a key={id} href={`#${id}`} className="px-3 py-1 rounded-full border border-gray-300 text-gray-800 hover:bg-gray-50">{l}</a>
            ))}
          </div>
        </header>

        {tl && (
          <Section id="timeline" kicker="through time" title="Structure forming, z = 49 to today">
            <p className="text-gray-700 max-w-3xl mb-4 text-sm">
              The same engine run again at {tl.n}³, the size CFG425 also used for its seeds, saving {tl.frames} frames. Press play, or drag the slider. The tracked halo below follows the same frame.
            </p>
            <Timeline tl={tl} frame={frame} setFrame={setFrame} playing={playing} setPlaying={setPlaying} />
            <div className="mt-8">
              <div className="text-sm font-medium text-gray-900 mb-2">One halo assembling, particle by particle</div>
              <Timelapse tl={tl} frame={frame} />
            </div>
            <div className="mt-6 text-xs text-gray-500 max-w-3xl space-y-1">
              <p>Does the replay reproduce the committed run? These checks were made when the files were built, against the numbers CFG425 and CFG411 saved for the same seed:</p>
              <ul className="list-disc pl-5">
                {tl.validation.map(v => (<li key={v.name}>{v.ok ? 'passed' : 'FAILED'}: {v.name} — {v.note} (limit {v.limit})</li>))}
              </ul>
            </div>
          </Section>
        )}

        <Section id="box" kicker="the whole box" title="The 512³ run today, in 3D">
          <p className="text-gray-700 max-w-3xl mb-4 text-sm">
            The real 512³ run at z = 0, averaged in blocks of 4 to a 128³ volume so it loads in 2 MB. The full-resolution cells are in the next section.
          </p>
          <Gate auto={!getDevice().low} label="Show the 3D box (2 MB)" note="This is a 3D ray-marched volume, the heaviest view on the page, so on phones and low-power devices it waits for you.">
          <div className="grid lg:grid-cols-[minmax(0,1fr)_17rem] gap-5 items-start">
            <VolumeView meta={meta} view={view} showSwitch={showSwitch} cut={cut} gain={gain} rotate={rotate} />
            <div className="space-y-3 text-sm text-gray-700">
              <Seg value={view} onChange={setView} options={[['res', 'Framework'], ['s0', 'Control'], ['diff', 'Difference']]} />
              {view === 'diff' && <div className="text-xs text-gray-500">Blue: control denser. Orange: framework denser. Full colour at ±0.15 dex.</div>}
              <label className="block">
                <span className="flex justify-between"><span>Hide below</span><span className="font-mono text-gray-900">{Math.pow(10, cut).toFixed(1)}× the mean</span></span>
                <input type="range" min={-1} max={2} step={0.05} value={cut} onChange={e => setCut(parseFloat(e.target.value))} className="w-full accent-gray-900" />
              </label>
              <label className="block">
                <span className="flex justify-between"><span>Brightness</span><span className="font-mono text-gray-900">{gain.toFixed(1)}</span></span>
                <input type="range" min={0.5} max={8} step={0.1} value={gain} onChange={e => setGain(parseFloat(e.target.value))} className="w-full accent-gray-900" />
              </label>
              <label className="flex items-center gap-2"><input type="checkbox" checked={rotate} onChange={e => setRotate(e.target.checked)} className="accent-gray-900" /> Auto-rotate</label>
              <label className="flex items-center gap-2"><input type="checkbox" checked={showSwitch} onChange={e => setShowSwitch(e.target.checked)} className="accent-gray-900" /> Show where the switch is on</label>
              <p className="text-xs text-gray-500">
                Colour is density relative to the cosmic mean, on a log scale from 0.03× to 300×. The switch is the framework run&apos;s rule for where its extra source acts:
                it is on in {(r.vol_on! * 100).toFixed(2)}% of the volume, which holds {(r.mass_on! * 100).toFixed(0)}% of the mass.
              </p>
            </div>
          </div>
          </Gate>
        </Section>

        <Section id="layers" kicker="full resolution" title="Single cells of the 512³ grid">
          <div className="flex flex-wrap items-center gap-4 mb-4">
            <Seg value={sView} onChange={setSView} options={[['res', 'Framework'], ['s0', 'Control'], ['diff', 'Difference']]} />
            <label className="flex items-center gap-2 text-sm text-gray-700"><input type="checkbox" checked={sSwitch} onChange={e => setSSwitch(e.target.checked)} className="accent-gray-900" /> Show where the switch is on</label>
          </div>
          <LayerView meta={meta} view={sView} showSwitch={sSwitch} />
        </Section>

        <Section id="halo" kicker="individual particles" title="Inside a halo">
          <p className="text-gray-700 max-w-3xl mb-4 text-sm">
            The first ten are the ten highest density peaks in the box and the last two are smaller systems (ranks 30 and 60). Each shows every {meta.halo_stride}th particle within {meta.halo_r} Mpc/h of the
            centre, in both runs, and each loads when you pick it ({fmtBytes(Math.min(...meta.halos.map(h => h.bytes)))}–{fmtBytes(Math.max(...meta.halos.map(h => h.bytes)))}). Inside a halo the particles are orbiting, so a small change in the force shifts their phase: the median particle
            sits {Math.round(Math.min(...meta.halos.map(h => h.moved_median_kpc_h)))}–{Math.round(Math.max(...meta.halos.map(h => h.moved_median_kpc_h)))} kpc/h from its twin in the other run. Single particle positions are not comparable there;
            the halo as a whole is. The control run holds fewer particles than the framework run inside the same sphere in {meta.halos.filter(h => h.n_control_sphere < h.n).length} of {meta.halos.length} halos
            (median {Math.abs(Math.round(median(meta.halos.map(h => (h.n_control_sphere / h.n - 1) * 100))))}% fewer, each run measured about its own halo centre).
          </p>
          <Gate auto={!getDevice().low} label="Show the halo viewer" note="Each halo is a few hundred thousand dots drawn in 3D, so on phones and low-power devices it waits for you."><HaloView meta={meta} /></Gate>
        </Section>

        <Section id="numbers" kicker="the comparison" title="How far apart the two runs are">
          <div className="grid lg:grid-cols-2 gap-8">
            <div>
              <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 mb-5">
                <Stat label="σ₈ framework" value={r.sigma8.toFixed(4)} />
                <Stat label="σ₈ control" value={s.sigma8.toFixed(4)} />
                <Stat label="ratio" value={st.s8_ratio.toFixed(4)} note="frozen cut: within 5%" />
                <Stat label="largest P(k) gap, k ≤ 1" value={`${(st.pk_max_dev * 100).toFixed(1)}%`} note="frozen cut: 10%" />
                <Stat label="density correlation" value={st.corr_log_density_128.toFixed(4)} note="log density, 128³ cells" />
                <Stat label="run time" value={`${hrs} h`} note={`${r.nsteps} steps`} />
              </div>
              {pk && (
                <>
                  <div className="text-sm font-medium text-gray-900 mb-1">Power spectrum: framework against control</div>
                  <Plot logX height={300} xLabel="k (h/Mpc)" yLabel="P framework / P control − 1 (%)" yMin={-12}
                    series={[
                      { label: 'measured at z = 0', color: '#ea580c', x: pk.x, y: pk.y },
                      { label: '+10% (frozen cut)', color: '#9ca3af', dash: '5 4', x: [pk.x[0], pk.x[pk.x.length - 1]], y: [10, 10] },
                      { label: '0', color: '#111827', width: 1, x: [pk.x[0], pk.x[pk.x.length - 1]], y: [0, 0] },
                      { label: '−10%', color: '#9ca3af', dash: '5 4', x: [pk.x[0], pk.x[pk.x.length - 1]], y: [-10, -10] },
                    ]} />
                </>
              )}
            </div>
            <div className="space-y-6 text-sm text-gray-700">
              <div>
                <div className="font-medium text-gray-900 mb-1">The same particle, in the two runs</div>
                <p className="mb-2">Half of all {pc.n.toLocaleString()} particles ended up within {(pc.median_mpc_h * 1000).toFixed(0)} kpc/h of where their twin sits in the other run.
                  {' '}{(pc.frac_gt_cell * 100).toFixed(0)}% differ by more than one {pc.cell_mpc_h.toFixed(2)} Mpc/h cell.</p>
                <table className="w-full text-xs border border-gray-200">
                  <thead className="bg-gray-50 text-gray-600"><tr><th className="text-left p-2">particle sits in a cell holding</th><th className="p-2 text-right">share</th><th className="p-2 text-right">median</th><th className="p-2 text-right">90th pct</th></tr></thead>
                  <tbody>
                    {Object.entries(pc.by_framework_cell_count).map(([k, v]) => (
                      <tr key={k} className="border-t border-gray-200"><td className="p-2">{k.replace('c0-2', '0–2 particles').replace('c3-30', '3–30').replace('c31+', '31 or more')}</td>
                        <td className="p-2 text-right font-mono">{(v.frac * 100).toFixed(0)}%</td>
                        <td className="p-2 text-right font-mono">{(v.median_mpc_h * 1000).toFixed(0)} kpc/h</td>
                        <td className="p-2 text-right font-mono">{(v.p90_mpc_h * 1000).toFixed(0)} kpc/h</td></tr>
                    ))}
                  </tbody>
                </table>
              </div>
              <div>
                <div className="font-medium text-gray-900 mb-1">Density, cell by cell (128³ cells)</div>
                <p className="mb-2">{(st.frac_cells_within_0p1dex_128 * 100).toFixed(1)}% of cells agree within 0.1 dex (a factor of 1.26). Where the gaps are, by how dense the cell is:</p>
                <table className="w-full text-xs border border-gray-200">
                  <thead className="bg-gray-50 text-gray-600"><tr><th className="text-left p-2">density (× mean)</th><th className="p-2 text-right">cells</th><th className="p-2 text-right">mean Δlog₁₀</th><th className="p-2 text-right">rms Δlog₁₀</th></tr></thead>
                  <tbody>
                    {Object.entries(bd).map(([k, v]) => (
                      <tr key={k} className="border-t border-gray-200"><td className="p-2">{k.replace('>=', '≥ ').replace('-', '–')}</td>
                        <td className="p-2 text-right font-mono">{(v.frac_cells * 100).toFixed(2)}%</td>
                        <td className="p-2 text-right font-mono">{v.mean_dlog10 >= 0 ? '+' : ''}{v.mean_dlog10.toFixed(3)}</td>
                        <td className="p-2 text-right font-mono">{v.rms_dlog10.toFixed(3)}</td></tr>
                    ))}
                  </tbody>
                </table>
                <p className="text-xs text-gray-500 mt-1">Positive: the framework run is denser. These gaps mix the model&apos;s effect with ordinary run-to-run divergence of non-linear halos; the record&apos;s test is the power spectrum above, not this table.</p>
              </div>
            </div>
          </div>
        </Section>

        <Section id="notes" kicker="read this" title="What this is, and what it is not">
          <ul className="list-disc pl-5 space-y-2 text-sm text-gray-700 max-w-3xl">
            <li>
              <strong>Nothing on this page is unique to the framework.</strong> The control is a standard Newtonian-plus-Λ particle-mesh run from the same standard initial conditions, and the two look the same because the rule was built to leave structure growth unchanged.
              The record says nothing in hand separates the framework from ΛCDM at 3σ. What is distinctive is the law itself: a₀ fixed by the cosmological constant, so flat in cosmic time. The deep-MOND Tully–Fisher zero-point at z ≈ 2.5 is the decisive future test
              (flat in the framework, +0.33 dex in ΛCDM-native), and Gaia DR4 wide binaries on 2 December 2026 test it against the bare MOND-type law. This simulation tests neither.
            </li>
            <li>It is a simulation of the model, not an observation of the sky. Nothing here compares to data.</li>
            <li>
              The growth check passed: σ₈ differs by {((st.s8_ratio - 1) * 100).toFixed(2)}% and the power spectrum by at most {(st.pk_max_dev * 100).toFixed(1)}% for k ≤ 1 h/Mpc, against cuts set beforehand
              at 5% and 10%. Passing means the rule does not break the cosmic web. It is not evidence that the framework is right.
            </li>
            <li>Initial conditions are the standard Eisenstein–Hu spectrum at z = {r.z_i}; that is the one ΛCDM input. κ = ½ is fitted, not derived, and f_b and ρ_Λ are inputs.</li>
            <li>In these runs the extra &ldquo;cold fluid&rdquo; is bookkeeping, not particles that move. The particles carry {(meta.m_particle_msun_h / 1e9).toFixed(2)}×10⁹ M☉/h each in the 512³ run (Ω_m ρ_crit per cell), and halo masses use that.</li>
            <li>Gravity is solved on the mesh, so structure inside about two cells (0.8 Mpc/h at 512³) is smoothed by it. Halo cores here are resolution-limited, and the particle views show where the particles are, not unresolved physics inside that scale.</li>
            <li>One box, one seed per run, the canonical a₀ footing only. The control is a single run, so how much of the dense-cell gap is chaos and how much is the model is not separated here. The timeline is a {tl ? `${tl.n}³` : '256³'} replay with seed 360, not the 512³ run itself.</li>
            <li>The heavy views are built to be gentle on ordinary machines: they draw only when something changes, stop when scrolled away or when the tab is hidden, render at lower resolution while you drag and lower their own quality if frames get slow, load only what you ask for, and on phones and low-power devices the 3D views wait for a click.</li>
            <li>The 512³ layers store counts exactly below 128 particles per cell and to within 4% above ({(meta.checks.res.frac_particles_in_cells_gt_127 * 100).toFixed(0)}% of particles sit in such cells). The 3D box is a 4×4×4 average. Halo views draw every {meta.halo_stride}th particle; their numbers use all of them.</li>
          </ul>
          <div className="mt-6 text-xs text-gray-500 space-y-1 max-w-3xl">
            <p>Build checks (run when these files were made): the 512³ particle counts sum to {meta.checks.res.count_sum.toLocaleString()}; the density grid built from the particles gives σ₈ = {meta.checks.res.sigma8_grid.toFixed(4)} against the run&apos;s own {meta.checks.res.sigma8_record.toFixed(4)} (control {meta.checks.s0.sigma8_grid.toFixed(4)} against {meta.checks.s0.sigma8_record.toFixed(4)}).</p>
            <p>
              Record: <a className="text-blue-600 hover:underline" href="https://github.com/carlzimmerman/zimmerman-formula/tree/main/campaign_fresh_gravity/CFG425_turnaround_catchment_confirm" target="_blank" rel="noopener noreferrer">CFG425</a> (verdict) ·{' '}
              <a className="text-blue-600 hover:underline" href="https://github.com/carlzimmerman/zimmerman-formula/tree/main/campaign_fresh_gravity/CFG424_turnaround_catchment" target="_blank" rel="noopener noreferrer">CFG424</a> (engine and rule) ·{' '}
              <a className="text-blue-600 hover:underline" href="https://doi.org/10.5281/zenodo.23240853" target="_blank" rel="noopener noreferrer">PAPER45</a>. Files are made by
              {' '}<code>ai_slop/website/scripts/build_cosmic_web_512.py</code> and <code>replay_frames_256.py</code>.
            </p>
          </div>
        </Section>
      </div>
    </div>
  )
}
