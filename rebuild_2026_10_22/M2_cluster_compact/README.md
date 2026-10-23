# M2_cluster_compact: does the stiffness length L★ rescue K1's tidal-charge term?

The question: K1's C2 term (the owner's "black hole on the brane" idea, a tidal charge per baryon mass element) came
closest on the cluster-core profile. But it overshot dwarfs by 2.4 dex and the planets by 10²⁰–10²³. Can the theory's own
small-scale screening, set by L★, switch it off in small systems and leave it on in clusters?

## Verdict: FAILS (frozen rule), on both footings, at L★ = 24, 50 and 90 pc

- **Cluster cores: unchanged from K1, so still FAIL.** Clusters are far too massive to be screened. Their screening length
  ℓ_g is 9e-4 to 1.4e-2 pc, so S differs from 1 by at most 1.9e-4 anywhere beyond 1 kpc.
  - ℓ_Q = 1.19 / 1.03 Mpc (canonical / alt, h 0.672), the same as K1 to all printed digits.
  - OUTER data/pred is 0.745–0.795 (Z −2.8 to −4.0, line |Z| ≤ 2).
  - Profile χ² is 7.0 / 10.5 (h 0.672) and 11.5 / 16.0 (h 0.686), against a line of 11.07.
  - INNER is overshot (data/pred 0.62–0.73).
- **Isolated galaxies: PASS, as in K1.** The term is at most 0.098–0.133 of the law (line 0.14). Here 1 − S ≤ 1.9e-6.
- **Dwarf satellites: FAIL, and the overshoot persists.** The median residual (needed: |r′| ≤ 0.26 dex) is:
  - −2.06 to −2.15 dex at L★ = 24 pc;
  - −1.66 to −1.74 at 50 pc;
  - −1.17 to −1.25 at 90 pc.
  - The reason: dwarfs sit at s = r₁₂/ℓ_g ≈ 0.1–10. There S is only 0.53–0.54 (24 pc) to 0.062–0.066 (90 pc). That removes
    0.3–1.2 dex from an overshoot of about 3 dex.
  - A larger L★ also screens the law's own boost in dwarfs. The baseline then rises from +0.91–0.95 to +1.56–1.59 dex.
- **Planets: FAIL, by 2e2 to 6e4 on the lenient reading.**
  - This is graded on the perihelion-equivalent anomaly, which is what the per-planet bounds measure.
  - Mars sits at 3.9e4–5.9e4 × its bound at 24 pc, 2.1e3–3.1e3 at 50 pc and 2.0e2–3.0e2 at 90 pc.
  - Mars would need L★ ≈ 340–370 pc, well outside the 22–90 pc window.
  - On K1's raw reading (any anomaly counts) Mars is still 1.6e13–3.1e14 × its bound.
- **Cassini Q₂ (from the Galaxy's own C2 field at the Sun): PASS.** Q₂ = 3.1–3.9e-28 s⁻², which is 0.035–0.043 of the
  Hees 2σ line and 0.060–0.074 of Park's.
- **Wide binaries: PASS, but only if stellar masses are calibrated dynamically.**
  - With dynamically calibrated masses, γ_v − 1 is 0.015–0.019 at 20 kAU. That comes from the Galaxy's C2 tide, which is
    3.0–3.7 % of g_N and orientation-dependent.
  - Against masses that are not dynamically calibrated, γ_v = 3.5–14.5.

No L★ in the window passes R3 or R5a, and O1 fails everywhere. So neither PARTIAL branch is met.
- κ = ½ is FITTED. Footings 9.3603e-11 and 1.1312e-10 m/s², never pooled.
- No dark-matter particle. The theory is not closed. Nothing here says the data favour the framework.

## Why the screening cannot do it

- **ℓ_g = L★²/(2 r_M) falls as M^{−1/2}.** Clusters and galaxies are therefore unscreened. The term's cluster shape is
  exactly K1's: compact, but with the wrong radial profile. Its lensing mass over the gas mass, at 0.5 / 1 / 2 / 3 Mpc, is
  5.5 / 2.7 / 1.4 / 1.7 (canonical). What is needed is ≈ 1.4–1.8 inside 1 Mpc and ≈ 0 beyond. Screening cannot change a
  shape it never touches.
- **Deep inside ℓ_g, S ≈ s/2 turns the C2 term (∝ r⁻³) into a pure 1/r² force.**
  - That is a change of the object's GM by the factor 1 + ℓ_Q/ℓ_g.
  - For the Sun, G_eff/G − 1 = 126–172 at 24 pc and 9.0–12.2 at 90 pc. For the Earth it is 0.22–0.30 and 0.016–0.021.
  - Orbits cannot see a pure 1/r² term, since it is absorbed into GM☉. What they do see is the next term,
    GMℓ_Q A/(r ℓ_g²), with A = q′(0) = −0.190 from the profile. That term fails Mars.
  - The GM change itself would show up wherever a star or planet is weighed without using its orbit (stellar structure,
    or laboratory G against the Earth's GM). That is not tested here, because no such data are on disk. A 10–170-fold
    solar GM excess is not a small claim.
- **Dwarfs are in the transition zone.** There S(s) is linear-ish and never small enough. Bringing the median dwarf to zero
  at 24 pc would need S ≈ 0.54 × 7.8/934 ≈ 5e-3 at r₁₂ (hand arithmetic on the JSON medians, not a scan). The record's
  profile reaches that only for ℓ_g ≈ 100 r₁₂, far outside the window.

## What the component physically is (counted)

It is not part of the theory. The theory's field content is the Khronon, the P vector and the Blanchet–Skordis K(Q) dust,
with no 5D bulk and no E_μν. This term is a **postulated** add-on (ledger):
- the DMPR closure P = −2U, applied per baryon mass element (+1);
- the rule Q ∝ dm (+1);
- adding it to the law's acceleration (+1);
- screening it with the P field's isolated profile S(s) (+1, new; the record derives S(s) only for P's own response);
- the object-mass rule that defines ℓ_g (+1, new);
- ℓ_Q being a physical length (+1, used only in R7);
- **one constant, ℓ_Q**, calibrated on F1 MID, plus the existing L★.

Per-object screening has no action and breaks linear superposition.

## Cosmology (R7, reported)

- **BBN-safe at the background level.** The term is the half-Laplacian of the baryon density, ρ_eff = (πℓ_Q/2)(−∇²)^{1/2}ρ_b.
  Its homogeneous (k = 0) mode is zero, so it adds no mean density: no ΔN_eff and no H(z) change.
  - Equivalently, on FRW isotropy forces the Weyl anisotropic stress to vanish, so the closure P = −2U forces U = 0. There
    is no dark-radiation background.
- **Not safe for growth.**
  - Linear modes are unscreened, because their masses give ℓ_g ≪ 1/k.
  - With ℓ_Q a physical length, G_eff/G − 1 = (π/2)(k/a)ℓ_Q f_b. That is 0.020 at k = 0.1 h/Mpc today but 22.5 at z = 1100.
  - From z = 99 alone (E-886 background, ℓ_Q = 1.19 Mpc), D_W/D_GR at z = 0 is 1.13, 2.83 and 563 at k = 0.01, 0.1 and
    1 h/Mpc.
  - By the frozen reading this is **growth-breaking on linear scales unless the term is absent on FRW**. A rule that
    removes it on FRW would be one more postulate.

## What this does not show

- **The external field.** The screening used is the isolated, multiplicative S(s), as the coordinator specified (CFG691,
  CFG820, E3). D7d and D10 show that in the Galaxy's field the response is not multiplicative, and that the screening
  length becomes L★ itself. Without an action for the C2 term, its external-field screening cannot be derived. A different
  form changes R5a's next-order term, not the cluster or galaxy results.
- **The GM change** (10–170× for the Sun) is graded nowhere, because the dynamical tests here cannot see it. It is an open
  and probably fatal consequence.
- **The wide-binary pass** depends on dynamically calibrated mass–luminosity relations. If photometric masses come from
  stellar models, the reading γ_v = 3.5–14.5 applies.
- **Dwarfs** use E3's central values and SPS M★ (E1's soft flag). The L★ = 50 and 90 pc baselines rescale E3's Monte Carlo
  B_scr by E3's central B_scr ratio (amendment A1). At 24 pc, E3's central and Monte Carlo values agree to 0.002 dex
  (median) and 0.012 dex (max).
- **Not modelled:** asphericity, satellites' screening of the host's field, baryon pressure in R7, and anything before
  z = 99.

## Checks, runs, files

Checks 7/7 PASS, exit 0. The run takes 6 s on one thread under nice 15, with a peak RSS of 0.68 GB.
- M1: the profile re-solved, matching CFG691's table to 4.7e-4, with A = −0.18974.
- M2: F1 reproduction, dev 0, sha 961ea4fc…e720; my projector against F1's agrees to 1.3e-4.
- M3: K1 C2 reproduced exactly with S ≡ 1.
- M4: E3 baseline (central vs Monte Carlo B_scr: 0.002 / 0.012 dex; K9 medians exact).
- M5: screened point-mass limits.
- M6: tide quadrature against −8GMℓ/R⁴, agreeing to 1.3e-3.
- M7: EdS growth.

`--mutate` (the scalar Laplacian in the profile ODE) gives M1 and M5 FAIL, 5/7, exit 1.

Files:
- `FROZEN_CRITERIA.md` and `ASSUMPTION_LEDGER.md` (15f797cbaa, committed alone first), plus amendment A1 (pre-result,
  4c6f49523c).
- `m2_cluster_compact.py`, which writes `.out` and `_results.json` (every number above).
- `*_MUTATE.*`.

Run:
`OMP_NUM_THREADS=1 nice -n 15 python3 m2_cluster_compact.py <dir holding F1's f1_meas.pkl> [--mutate]`.

Record checked: K1 (C2 kernel, slip, calibration, R1 point-source formula), F1, F2, E3 (B_scr recipe, CSV), CFG691 (S(s)
ODE), CFG820, D7d, D10 (L★ floor 21.68 / 22.85 pc; external-field screening length), C6 (planet bounds, Q₂ lines),
`prep_2026/planetary_doors/BOUNDS.md` (bounds are perihelion-derived), and C2 (E-886 background). No lane had screened the
C2 term.
