# VERIFY.md — Adversarial verification of the single-metric MI lensing confrontation

**Verifier:** independent session, 2026-07-17. Independent code: `verify_independent.py`
(this directory; exit 0, 22/22). Deliverables re-run first, then every load-bearing claim
re-derived on a separate code path (upper-metric variation route, different radial grid,
Simpson/cumtrapz integrator, own Brouwer loader).

## 1. Re-runs (deliverables, unmodified)

| script | exit | checks |
|---|---|---|
| `total_stress.py` | 0 | 20/20 |
| `lensing_solve.py` | 0 | 12/12 |
| `confront.py` | 0 | 9/9 |

All claimed numbers reproduced exactly: rail Δχ² **+722.2 / +753.7** (can/alt), full
**+1496.0 / +1564.6**, rail-edge 1.87 dex / 13.4σ single point, profiled ±0.3 dex
**715.4 / 720.6**, hot-CGM 793.8, doc-γ fork 4.1%, Noether residual 1.7e-16.

## 2. Independent re-derivation of the total stress tensor (the trap zone)

Re-derived from scratch by **two variation routes** (lower-metric with u^μ fixed = the doc
route; and the upper-metric route as a cross-check of the held-fixed bookkeeping):

- Matter legs: `2 dL_m/dg_mn = −ρsK u u − ρs(u·u)K′ aa/a0²` ⇒ on-shell
  α = −ρsK, β = +½ρsK, γ = +ρsK′/a0² — **MATTER_COUPLING.md §2c reproduced exactly** (A2).
- **Frame leg counted once, not zero, not twice** (A3): T^u = −λ u u with λ = −ρsK ⇒
  +ρsK u u, which **exactly cancels** the matter uu energy (A4). So the free-frame reading
  (Assembly I) leaves ½ρsK g + γ aa; with s = −1, K→1 the rest-frame anchor is
  ρ_e = +ρ/2, p = −ρ/2, ρ_e+3p = −ρ < 0: **matter would not gravitate** — the deliverable's
  "bookkeeping wound" finding is real, not manufactured (A5). Assembly II (dust closure)
  leaves zero energy: also fails. Assembly III (composite u = J/|J|; u·u = −1 identically
  for every metric ⇒ S_u ≡ 0, frame leg identically zero — *vanishes*, is not *dropped*):
  T^III = −½sρK uu + sρK′aa/a0², verified symbolically (A6). s = −1 gives attractive dust/2;
  Newton ×2 calibration ⇒ **T̂ = ρK uu − 2(ρK′/a0²) aa**. Confirmed.
- **Sign audit (the verdict-flipping trap):** s = +1 in Assembly III gives ρ_e = −ρ/2
  (anti-gravity, fails Newton) — s = −1 is the only Newton-consistent sign, and with it the
  dressing is a *suppression*. **No sign assignment produces over-lensing** (A7). The frame
  leg can only cancel matter's uu energy (worse) or vanish; it can never add O(ν).

## 3. Deep-MOND magnitudes (independent sympy + 8-point numeric, machine zero)

- On-shell (|a| = νg_bar): **K = 1/ν exactly** (collapsing radical 1+4(y²+y) = (2y+1)²) —
  suppression, both footings (a0 enters only via X). Verified symbolically after the radical
  collapse and numerically to 1e-16 at y ∈ [3e-3, 250] (B1).
- **2K′X/K = 1/(2y+1) ≤ 1 exactly** (B2). Deep MOND: K → |a|/a0, **K′X → K/2 = |a|/(2a0)**
  (B3) — exactly the task note. Every term is an **O(K) ≤ 1 correction; ν appears nowhere**.
  At y = 0.01 the needed factor is ν = 10.05; the derived source is K = 0.0995. The
  magnitude analysis in the deliverable is right, and it is derived, not assumed.

## 4. Independent F(y) (different grid, integrator, code)

| y | F indep (can) | deliv | F indep (alt) | deliv |
|---|---|---|---|---|
| 1.0 | 0.5638 | 0.563 | 0.5535 | 0.553 |
| 0.1 | 0.2115 | 0.211 | 0.2059 | 0.206 |
| 0.01 | 0.0640 | 0.064 | 0.0620 | 0.062 |

M_eff(∞)/M_bar = 0.602/0.579 (deliv 0.601/0.578). F < 1/ν everywhere (C2): the theory
under-lenses by *more* than the trilemma 1/ν because the source itself is mass-weighted
dressed down. The "F ~ 0.6/ν" one-liner is accurate.

## 5. Brouwer exclusion arithmetic (own loader, README-checked conversion)

Conversion hand-checked against the release README (g_obs = 4·G_pc·(ESD/bias)·pc_per_m;
cov/bias-product): rail-edge point ESD 10.577/0.98531 → g_obs = 5.99e-12 ✓. Independent
χ² (full covariance): rail Δχ² = **722.2 / 753.7**, full **1496.0 / 1564.5** — match to
<0.1. Rail edge: MI 8.03e-14 vs 5.99e-12 = 1.87 dex, 13.4σ. Profiled ±0.3 dex: 715.4 ✓.
Caveat honestly carried by the deliverable: σ ≡ √Δχ² is labeled *formal* (χ²(F=1)=84/7 pts
unprofiled; profiling brings F=1 to 22.0 while MI stays ≈737 — the *slope* discrimination
is what the exclusion rests on, and that is sound).

## 6. Manufactured-save AND manufactured-kill hunt (equal effort)

- **Save hunt:** no conjured source anywhere — ρ_eff = ρK ≤ ρ (exact identity), aniso term
  bounded by ρK/2, dipole/connection legs bounded at the same O(K′X) order, frame leg zero
  or cancelling. The F=1 outcome was excluded by derivation, not assumed away. Clean.
- **Kill hunt:** (i) slip-sign flipped by hand (+Π instead of −Π): F(0.1) moves 0.2115 →
  0.2273 — verdict untouched (E1); the tension sign is not load-bearing. (ii) The Newton ×2
  calibration *helps* MI (removing it halves F) — anti-kill (E2). (iii) Assembly fork:
  adopting I/II instead would *un-gravitate matter* — III is the charitable choice. (iv)
  Doc-γ fork 4.1% ✓ (E5). (v) Galaxy-model rigging impossible: **model-free bound** — any
  baryonic source gives g_lens ≤ g_bar (ρ_eff ≤ ρ, |Π| ≤ ρ_eff), while the rail-edge datum
  needs g_obs/g_bar ≈ 46 (E3). No mass model, amplitude nuisance, or budget variant crosses
  that; the slope (g_lens ∝ g_bar vs measured √(a0 g_bar)) is wrong. The kill is real.

## 7. Both footings, Cassini, GW170817

Both a0 footings carried end-to-end (they enter only via X; verdict identical). Cassini:
1−K = 2K′X/K = 7.2e-7 / 8.7e-7 at Saturn (can/alt), vacuum slip exactly zero (Π ∝ ρ = 0
outside the source ⇒ Φ = Ψ, γ_PPN = 1) — safe, ~8 orders on the γ-type piece (E6).
GW170817: one metric ⇒ c_γ = c_GW is an identity of the construction. Both correct.

## VERDICT

**UPHELD, 22/22 independent checks.** The assembled total T̂ = ρK uu − 2(ρK′/a0²) aa is
correct (frame leg counted once — it cancels or vanishes, never enhances; s = −1 signs
audited, no flip to over-lensing possible); every term is an O(K) ≤ 1 suppression/correction
with no O(ν) structure; F(y) < 1/ν < 1 reproduced independently to <0.01; the Brouwer
arithmetic is exact (rail ~27σ formal both footings, robust to every nuisance tried, and
model-free at the slope level). No manufactured save, no manufactured kill found. The honest
completion statement stands: dynamics+cosmology sectors complete up to constants; **lensing
requires physics beyond the current action** — with the named doors (off-circular/nonlocal
closure, a lensing carrier beyond S_EH+S_u+S_matter, the free-frame S_u bookkeeping wound)
left open, per the no-"theory-closed" rail.
