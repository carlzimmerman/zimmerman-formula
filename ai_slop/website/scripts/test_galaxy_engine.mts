// Headless check of src/components/galaxysim/engine.ts on real SPARC galaxies. Run: node ai_slop/website/scripts/test_galaxy_engine.mts [NAME ...]
import { readFileSync } from 'node:fs'
import { DiskSim, GYR_PER_UNIT } from '../src/components/galaxysim/engine.ts'
const d = JSON.parse(readFileSync(new URL('../public/data/sparc_sim.json', import.meta.url), 'utf8'))
const names = process.argv.slice(2).length ? process.argv.slice(2) : ['NGC3198']
for (const name of names) {
  const gal = d.galaxies.find((g: any) => g.name === name)
  if (!gal) { console.log(name, 'not in the disk-only set'); continue }
  console.log(`\n== ${name}: Rd ${gal.Rd} kpc, Vflat ${gal.Vflat}, M* ${gal.Mstar.toExponential(2)}, data points ${gal.R.length}`)
  for (const mode of ['law', 'newton', 'halo'] as const) {
    const t0 = performance.now()
    const s = new DiskSim(gal, d.kernel, d.a0_kms2_per_kpc, mode, { N: 128, np: 60000 })
    const tInit = performance.now() - t0
    // equilibrium curve vs data
    const interp = (xs: number[], ys: number[], x: number) => { let i = 0; while (i < xs.length - 2 && xs[i + 1] < x) i++; const u = (x - xs[i]) / (xs[i + 1] - xs[i]); return ys[i] * (1 - u) + ys[i + 1] * u }
    let ss = 0, n = 0
    gal.R.forEach((R: number, i: number) => { if (R > s.vc0.R[0] && R < s.vc0.R[s.vc0.R.length - 1]) { const v = interp(s.vc0.R, s.vc0.V, R); ss += Math.log10(v / gal.Vobs[i]) ** 2; n++ } })
    const L0 = s.angularMomentum(), r0 = s.halfMassRadius(), tt = performance.now()
    const nsteps = Math.round(1.0 / GYR_PER_UNIT / s.dt)       // ~1 Gyr
    for (let k = 0; k < nsteps; k++) s.step()
    const ms = (performance.now() - tt) / nsteps
    const c = s.curve(); let ss2 = 0, n2 = 0
    gal.R.forEach((R: number, i: number) => { if (R > c.R[0] && R < c.R[c.R.length - 1]) { const v = interp(c.R, c.V, R); ss2 += Math.log10(v / gal.Vobs[i]) ** 2; n2++ } })
    console.log(`${mode.padEnd(6)} box ${s.L.toFixed(1)} kpc cell ${s.h.toFixed(3)} dt ${(s.dt * GYR_PER_UNIT * 1000).toFixed(2)} Myr | init ${tInit.toFixed(0)} ms, step ${ms.toFixed(1)} ms | curve vs data at start ${Math.sqrt(ss / n).toFixed(3)} dex, after ${(s.t * GYR_PER_UNIT).toFixed(2)} Gyr ${Math.sqrt(ss2 / n2).toFixed(3)} dex | Lz drift ${(((s.angularMomentum() - L0) / L0) * 100).toFixed(2)}% | half-mass r ${r0.toFixed(2)} -> ${s.halfMassRadius().toFixed(2)} kpc`)
  }
}
