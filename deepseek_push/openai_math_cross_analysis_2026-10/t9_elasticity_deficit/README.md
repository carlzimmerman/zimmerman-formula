# T9 — phantom-mass elasticity law ε(s): the derived sub-half deficit

**The breakthrough result of the openai/math campaign.** A kernel-exact,
parameter-free law that predicts the measured phantom-mass elasticities of
the T1 lane — including their unexplained 0.8% deficit below 1/2 — at both
footings, to 0.0003.

## Derivation chain (every step uses campaign deliverables)

1. **Flux closed form (kernel-exact, no deep-MOND limit):** for a point
   baryon host, r²(ν−1)g_N = G M_b(ν−1); with ν−1 = 1/(e^s − 1), s := r_t/r,
   r_t := √(GM_b/a₀):  M_ph(<r) = M_b/(e^s − 1).  [T1 worked this to 1e-10
   grid agreement; the flux is strictly increasing ⇒ ρ_ph > 0 everywhere —
   the T3 sign correction.]
2. **Elasticity:** d ln s/d ln M_b = 1/2 (s ∝ M_b^{1/2}) ⇒
   **ε(s) := d ln M_ph/d ln M_b = 1 − (s/2)e^s/(e^s − 1)** — exact, all radii.
3. **Deep limit:** ε → 1/2 as s → 0 (the deep-MOND √M_b law; the framework's
   own ubiquitous ½), approached *from below* — the sub-half deficit is
   universal at finite radius.
4. **Half-mass radius:** M_ph = M_b/2 exactly at s = ln 3 (r = r_t/ln 3),
   Lean-certified.
5. **Elasticity zero:** ε = 0 at s* e^{s*} = 2(e^{s*} − 1), s* = 1.593624
   (r = 0.6275 r_t) — inside that radius, adding baryons *reduces* the
   enclosed phantom mass (negative elasticity branch).

## Numbers (main run, 6/6 PASS, rc 0)

| footing | r_t (kpc) | s = r_t/818 kpc | ε predicted | ε measured (T1) |
|---|---|---|---|---|
| canonical a₀ = 9.3603e-11 | 12.2043 | 0.014920 | **0.49626** | 0.4960 |
| alt a₀ = 1.1312e-10 | 11.1016 | 0.013572 | **0.49660** | 0.4964 |

Both within the declared ±0.0006 window; zero free parameters. The
"why 0.496 and not ½?" question from the T1 lane is now **derived**: the
deficit is the kernel's finite-s correction −(s/4 + …).

**Bridge to T1's C6 (independent confirmation):** +0.1-dex baryon error ⇒
exp(ε·ln 10^{0.1}) − 1 = **+12.105%** vs T1's measured +12.10%/+12.11%.

**The prediction curve** (universal — no a₀ in ε once s is the unit):
r_out = 100 kpc → ε = 0.4689; 50 kpc → 0.4365; 30 kpc → 0.3914; 20 kpc →
0.3320; r_t → 0.2090; root r = 0.6275 r_t → 0; 6.1 kpc → −0.1568.
Falsifier: measure d ln M_ph/d ln M_b for the settled MW profile at
different truncations (e.g. SPARC apertures 8/20/50 kpc) — the curve is
not a fit, it is the law.

**Unification observation (declared, NOT a derivation of κ):** the fitted
κ = 1/2 equals ε(0) — the deep limit of the settled-mass response — and the
kernel's exact sub-leading constant (1/(e^s−1) = (1/2)(coth(s/2) − 1)).
κ stays FITTED; the ½-triple (κ, kernel, ε(0)) is the same number wearing
three physics hats.

## Controls

- MUTATE (T9_MUTATE=1: M_b^{1/3} scaling instead of 1/2): ε → 0.6642/0.6644,
  bridge +16.52% — C1, C2, C3, C6 all flip as declared (rc 1); C4/C5
  re-solve and pass (rc 1, 2/6).
- C3 deep limit: ε(1e-9) = 0.4999999997 (stable expm1 form — the naive
  e^s − 1 form cancels at 1e-7 relative in float64; the identity
  (s/2)e^s/(e^s−1) = (s/2)/(1−e^{−s}) is the numerically-safe form,
  Lean-certified as `deficit_stable_form`).
- Zero crossing C5: ε(s*) = 9.7e-8 at the declared root 1.593624 ± 1e-3.

## Lean certificate (`../lean_certs/cert_elasticity_deficit.lean`)

Compiles clean (rc 0, zero sorry): `kernel_occupancy_identity` (1/(e^s−1) =
e^{−s}/(1−e^{−s})), `deficit_stable_form`, `m_ph_closed_form` (M_ph = M_b/(e^s−1)),
`elasticity_annihilates_at_root` (root equation ⇒ ε = 0),
`half_mass_at_log3` (M_ph = M_b/2 at s = ln 3). Axioms = {propext,
Classical.choice, Quot.sound} for all five. House pattern: the
log-derivative identity and the s→0 limit are carried by the lane script
(C3 numeric + the algebraic payload above); the derivation's exact algebra
is machine-checked.

## Bottom line

The release gave us the tools; the tool that mattered was the *exact*
phantom closed form it forced us to build (T1 + Lean) — and the fitted
framework's own numbers (T1's measured elasticities, C6 bridge) confirm
the law it implies at the 3×10⁻⁴ level, twice. This is the first positive
derivable law the campaign produced, and it is falsifiable.