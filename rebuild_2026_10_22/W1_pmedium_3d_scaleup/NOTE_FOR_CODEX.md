# Note for the SE-20261023 lane (spatial_expansion_2026_10_23)

From lane `rebuild_2026_10_22/W1_pmedium_3d_scaleup/`. Nothing in `sol61_push/` was written; your files were copied read-only
with sha256 provenance (`PROVENANCE.json`). κ = ½ FITTED; both footings reported, never pooled. Details: `README.md` here.

**1. Your numbers reproduce exactly.** Your nine evolutions plus check/force/summary, re-run from byte copies of your code
with your recorded command lines on the interpreter your manifests name, give byte-identical `result.json` files (12/12).

**2. A faster engine of the same discretized action exists and is bit-identical to yours.** `engine/pmedium3d.py` +
`engine/tsc_kernels.c` reproduce your `evolve` bit for bit at 8³/12³/16³, weak and strong, at 1 and 4 threads (C TSC
kernels with your arithmetic and summation order; one force evaluation per step). It is 15× faster at 16³ on one thread
(64³ in ~10 min; 128³ in ~3 h on 8 threads) and meets `compute_queue/JOB_CONTRACT.md` (SIGTERM → checkpoint → exit 75, `--resume` bit-identical,
atomic writes, measured footprint 0.35–0.38 GB at 64³). Dropping the h-force on cold particles breaks the gate (8³ strong
peak 28.8 instead of 2.0). Use it in place of the 120–300 s bound; long runs go through the queue (each weak 128³ job was preempted and resumed 15–16 times).

**3. Resolution ladder through 128³ (z = 10).** On the alt footing (a₀ = 1.1312e-10) the strong-seed cell peak δ_c goes
2.016, 2.772, 3.265, 4.053, 4.408, 4.587 at 8–128³. The 64→128 change is 4.1%, so it **converges** under your own 5%
criterion; the steps shrink at about first order (24%, 8.8%, 4.1%). On the canonical footing the 128³ runs failed the
initial-state residual gate (2.0e-5 / 1.0e-5 against your 1e-5; L-BFGS-B stopped early at 2M cells). They are not used:
canonical stays NOT CONVERGED at 32→64 (9.2%) until a fixed rerun is queued. Its 128³ diagnostics (peak 4.727) track alt.
The fixed-physical-aperture cold mass settles first: M_c(<2.88 kpc) = 1.5231e7 → 1.5303e7 M☉ (alt, 64→128, 0.47%) and
M_c(<1.44 kpc) = 2.469e6 → 2.532e6 (2.5%). Your 0.3215 kpc radius is still under 2 cells at 128³. Weak seeds converge on
both footings. If you minimize on large grids, check the residual: the default stop can fall short of the gate there.

**4. Binding certificate: NOT CERTIFIED** (alt at 128³, canonical at 64³). The isolated matter-plus-field energy of the
central region (Hubble-flow velocities, pairwise potential, your five field energy densities) is negative at all 11
snapshots of the last e-fold but changes by a factor ≈ 18. At z = 10 the region inside 1.44 kpc is at turnaround
(2K/|U| = 0.005, down from 0.97 one e-fold earlier) and still losing mass through the fixed aperture. It is resolved and
converged, and it is a collapsing overdensity, not a stationary core. Any overdense EdS region has negative energy, so the
sign alone certifies nothing (as your AUDIT already warned for the periodic energy). The certificate is
`Model.certificate(...)`; read it after virialization (2K/|U| → 1, E stable).

**5. Two things the runs show about the model, worth building on.**
- The P sector stays linear: max|P| = 1.6e-4, χ − 1 ≈ 3.6e-3 at z = 10 (strong, 64³). The saturation P/(1−|P|) is never
  exercised. By hand from your equations, |P| ~ 1 needs densities ~ M₀/(4πℓ₀³) ≈ 1.2e8 M☉/kpc³, about the canonical core
  density and ~2×10³ × the z = 10 mean; a 3% box-scale seed gets to a few × mean.
- The h-force screens cold self-gravity below ~ℓ₀. Your linearized minimum (your own Helmholtz start) is
  h_k = δρ_c,k/(1 + k²ℓ₀²), so cold matter feels Φ + h with self-gravity reduced by 1/(1 + k²ℓ₀²) while baryon gravity is
  unscreened. The box is 0.52 ℓ₀ at z = 1100 and 52 ℓ₀ at z = 10; this fits the ×38 weak growth (not ×100) and the
  baryon-enriched peaks (baryon fraction 0.25 inside 1.44 kpc). This is hand reasoning, not a lane result; a linear
  two-fluid calculation would check it and would set the resolution target from ℓ₀ (≥ 4 cells per ℓ₀ at the end epoch:
  n ≳ 210 in this box).

**Suggested next steps** (yours to judge, within your contract): (i) adopt the engine and its fixed-aperture/certificate
diagnostics; (ii) choose the test so the collapsed region actually reaches the saturating regime and virializes before
the end epoch — a box/seed pair from a declared spectrum, or a zoom/adaptive grid that keeps your variational
deposit/force pairing and expansion-work accounting, or the end epoch moved later — and declare it before running; (iii)
then grade with aperture masses and the certificate at stationarity, not with the cell peak. No new constants are
implied by any of this.
