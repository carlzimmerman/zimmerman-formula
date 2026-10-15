# ARGON02 — The settled-halo lensing ESD: a parameter-free prediction from the law + GF2 + supply rule

**Date:** 2026-10-15. **Home:** `argon_push/ARGON02_settled_halo_esd_2026-10-15/`.
**Pre-registration:** `FROZEN_CRITERIA.md` (committed alone, `964f2ea33`, before any script).
**Run:** `OMP_NUM_THREADS=1 timeout 100 python3 settled_halo_esd.py` → 0 FAIL, exit 0, wall 0.4 s,
1 thread, max RSS 112 MB. Canonical footing a₀ = 9.3603e-11 only (alt never pooled). κ = ½ FITTED.
Lensing-to-mass coupling = the repo's established working assumption (minimal metric coupling
certification 2026-10-13; CFG723 E2/E3); the relativistic completion itself stays open (canonical §3).

## The prediction (four statements, zero free halo parameters)

**P1 — Locked ESD amplitude (deep window).** The settled phantom of an isolated disk is the law's exact
phantom, M_c(r)/M_b = (√(1+4r²/r_M²) − 1)/2 with r_M = √(GM_b/a₀), whose GF2-verified dispersion is
σ² = √(GM_b a₀)/2. Its projected ESD is

  ΔΣ(R) → √(GM_b a₀)/(4GR) = 167.9 M☉ pc⁻² · (r_M/R)   (M_b = 10¹¹, canonical)   as R/r_M → ∞,

approaching the isothermal r⁻¹ law with the amplitude fixed by (M_b, a₀) alone — **no NFW concentration,
no halo mass, no free parameter** (amp = 0.938/0.969/0.984 at 10/20/40 r_M, monotone → 1 as 1 − 0.6/x).

**P2 — The exact ESD curve is the prediction, not the asymptote.** The projection of the cored phantom
(ρ_c = M_b/(2πr_M²r√(1+4r²/r_M²))) deviates from r⁻¹ systematically inside ~5 r_M: ΔΣ = 52/45/36/30
M☉ pc⁻² at 2.5/3/4/5 r_M (0.78–0.88 of the asymptotic value), and inside r_M the ESD is suppressed to
13–54% of the r⁻¹ extrapolation (0.2/0.5/1.0 r_M). The whole shape is fixed; stacked GGL bins at
[0.2, 5] r_M test it with no freedom.

**P3 — The ESD breaks at the supply edge, r_e = 5.84 r_M.** Each halo settles its own supply
(Ω_c/Ω_b = 5.364): M_c(r_e) = 5.364 M_b ⇒ r_e = √(((2·5.364+1)²−1)/4)·r_M = 5.84 r_M — 71 kpc for
M_b = 10¹¹, 57 kpc for the MW (M_b = 6.5×10¹⁰). Beyond r_e the settled ESD ends (log-slope
|d ln ΔΣ/d ln R| > 1.05); only baryons and any S4-freed debris continue. This sharpens CFG261's stack,
which truncates the phantom at r_e = 0.40 r_ta (≈ 100 kpc for a 250 kpc tidal radius): the derived edge is
smaller, sharper and parameter-free. The edge moves with the supply: ±10% supply ⇒ 5.30/6.38 r_M.

**P4 — The MW/LG consequence.** The settled MW halo ends at ~57 kpc with M_c = 3.49×10¹¹ (M_dyn ≈ 4.1×10¹¹
inside). Any enclosed-mass requirement ≫ 4×10¹¹ at 100–300 kpc (satellite kinematics, LG timing) must be
carried by the **S4 free component** (Gaia–Enceladus-era merger debris) — never by the settled halo. This
turns the known outer-MW mass into a decomposition test of S4, not a contradiction: the framework predicts
the outer MW mass is dominated by freed cold energy, with the settled halo strictly capped at 5.364 M_b.

## Kill tests (data)
- (a) NFW-like ESD with a free concentration in [1, 5] r_M → the locked-amplitude claim dies.
- (b) No break at 5.8 r_M for merger-free isolated disks → the supply-rule edge dies.
- (c) Inner shape [0.2, 1] r_M off the exact formula by > 3σ in stacked bins (baryon model included) → the
  cored-phantom projection dies.
- (d) MW enclosed mass > ~4.1×10¹¹ at 100 kpc with no S4 debris budget → S4's cap dies.

## Gates (all machine-checked, 0 FAIL)
G1 amplitude locking (monotone → 1, 3.1% at 20 r_M); G2 edge 5.843 ± 1e-3; G3 exactness (sympy: closed-form
ρ_c ≡ dM_c/dr/(4πr²); deep M_c → r/r_M − ½; cored r→0); G4 projection honesty (singularity-free Abel
substitution r = √(R²+t²); SIS identity ΔΣ = Σ asymptotically); G6 mutations (supply ±10% → 5.30/6.38 r_M;
alt footing scales amplitude by √(a₀_alt/a₀) = 1.0993, never pooled).

## Corrigendum to the frozen criteria
The criteria's mutation line ("5.55/6.12 r_M") was miscalculated by hand; the exact formula gives
5.303/6.381 r_M. The physics (break shifts with the supply) is unchanged; the script carries the correct
numbers and this report supersedes the criteria's arithmetic.

## What this does NOT establish
- It does not close the relativistic completion (canonical §3): the prediction is conditional on the
  established lensing-to-mass coupling, and passing (a)–(c) would be evidence FOR that coupling, not a
  derivation of it.
- No statement about the free component's profile (S4): P4 only caps the settled halo; the debris profile
  is unmodelled here (CFG621–623 territory).
- Inner ESD (r ≲ 0.2 r_M) needs a baryon (disk+bulge) model; the phantom part is exact, the total is not
  predicted without one.
- Footings never pooled; κ = ½ remains FITTED.

## Verdict
**PASS — the framework now makes a parameter-free lensing statement** (amplitude-locked r⁻¹ ESD, exact
cored transition curve, supply-rule break at 5.84 r_M, S4-capped MW halo), with four named kill tests.
It is the sharpest falsifiable content of the lensing coupling currently on the record: one curve, zero
knobs.