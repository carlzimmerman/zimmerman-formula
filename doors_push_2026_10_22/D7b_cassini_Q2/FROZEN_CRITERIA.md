# D7b_cassini_Q2 — FROZEN CRITERIA (written before any script or number)

Door: A4's open item 2 / D7's "What this does not show": the **Cassini quadrupole Q₂** of the canonical
law `g_N = g²/(g+a₀)` (ν−1 = (√(1+4/y)−1)/2, y = |g_N|/a₀) with and without the strong-field turn-off P5,
`ν_fix − 1 = (ν−1)/(1+(y/y_t)²)`, in the Solar System embedded in the Galaxy's field.

## Record checked before freezing

- `deepseek_push/DS_FINAL_2026_10_21/` A4_ppn (closure, y_t = 66.2999, "No Cassini Q₂"), A30 (a_P),
  A22 (isolated monopole), A60 (Sun embedded in the Galaxy: g_N,gal = 6.913e-11, g_gal = 1.221e-10 at 8 kpc).
- `doors_push_2026_10_22/D7_turnoff_yt/` README + script (Q₂ listed as uncomputed; y_t roots 66.2999 /
  66.3803 / 46.0148 / 77.876; band [60,140] ↔ κ ∈ [0.3415, 0.5267]).
- Prior Q₂ work, **none with P5**: `hunt_2026/k01_solar_efe_quadrupole.py` (simple kernel −1.945e-26 canonical,
  ~6.5× an order-of-magnitude bound), `hunt_2026/f24_*` (STANDING.md:257: QUMOND 6.2×/6.8×, AQUAL 7.7×/8.8× of
  the Park ceiling), `real_research/reviews/branchB_q2_gate_2026/` (Milgrom/Desmond eq-12 kernel, /√D bug
  corrected, grid solver, framework-ν 4.8×/6.4× of 5.2e-27), `prep_2026/planetary_doors/BOUNDS.md` §1.1
  (Hees 2014, Park 2026, BN11 Table 1 values), DOOR_SCOREBOARD.md §2.
- So the class result (the bare p=1 law fails Q₂ by several ×) is already on record. **What is new here is
  only P5**: does the turn-off change Q₂, and does Q₂ constrain y_t?

## Method (fixed now)

QUMOND, Sun (point mass) + uniform Newtonian external field g_N,e; phantom density
ρ_ph = −∇·[(ν_fix−1) g_N]/4πG; Q₂ is the l = 2 interior coefficient, convention δΦ = ½ Q₂ (z² − r²/3)·(sign
fixed so BN11's MOND values are positive). Two independent routes:
- **Route M**: Milgrom 2009 / Desmond+2024 eq-12 double integral (no /√D), `Q₂ = −(3a₀^{3/2}/2√GM)·q`,
  integrated to v = ∞ (tail by substitution), not truncated.
- **Route G**: axisymmetric (log r × Gauss–Legendre) closed-form ρ_ph, P₂ projection, radial Green integrals,
  Q₂ evaluated at the origin and at Saturn (9.58 AU).

## Inputs (all labelled)

- a₀ = 9.36e-11 (canonical) and 1.13e-10 m/s² (alt), never pooled. GM_⊙ = 1.32712440018e20 m³/s².
- y_t ∈ {60, 66.3803 (κ = ½ via I(y_t) = 8π/κ² = 32π), 77.876 (thermal κ = Z/4π, 8π/κ² = 118.435), 140}, plus
  "no turn-off" (y_t = ∞). The quoted-Λ root 66.2999 is reported beside 66.3803. Same y_t grid on both footings.
- External field (four values; QUMOND needs the Newtonian g_N,e; a total g_e is inverted via g_N,e·ν_fix(g_N,e/a₀) = g_e):
  - **E0** framework MW model (A60, Hernquist 6e10 M⊙, a = 3 kpc, R = 8 kpc): g_N,e = 6.913e-11 m/s² (direct).
  - **E1/E2/E3** kinematic total field, record band (branchB lane): g_e = {1.9, 2.2, 2.6} × 9.36e-11 m/s².
- Bounds: **primary Hees et al. 2014 (PRD 89 102002, arXiv:1402.6950): Q₂ = (3 ± 3)e-27 s⁻²**, 2σ upper
  **9.0e-27** (the MOND prediction is positive in this convention). Secondary: Park+2026 (arXiv:2602.17884)
  (1.6 ± 1.8)e-27, 2σ 5.2e-27. Both are external inputs as transcribed in `prep_2026/planetary_doors/BOUNDS.md`;
  not re-verified from the papers here (no network).
- Validation anchors (external, as transcribed in the record): Desmond+2024 simple-ν |q|(g_e/a₀ = 1, 1.5, 2) =
  0.094, 0.159, 0.221; BN11 Table 1 AQUAL μ₁ (simple): Q₂ = 3.8e-26 at a₀ = 1.2e-10, g_e = 1.9e-10.

## Checks (validation; script exit 0 iff all PASS)

- **K1 analytic limit.** For ν−1 = 1/y exactly (the canonical tail alone, a₀·ĝ_N), the eq-12 integral is
  exact via the Legendre generating function: **q = −(16/49)√e_N**. Route M within 1e-3 relative at e_N ∈ {0.5, 2, 8}.
- **K2** Route G reproduces the same analytic limit within 1 % (e_N = 2).
- **K3** Route M vs Route G on the canonical law: agree within 2 % at every (footing, y_t, E) point.
- **K4** published anchors: simple ν, no turn-off, |q| within 3 % of 0.094 / 0.159 / 0.221.
- **K5** BN11 AQUAL μ₁ = 3.8e-26: our QUMOND/BN11 ratio in [0.70, 1.05] (QUMOND–AQUAL difference ≲ 30 %, record ~0.8).
- **K6** limits: g_N,e = 0 ⇒ |Q₂| < 1e-6 of the E2 value; y_t = 1e8 reproduces no-turn-off within 1e-5.
- **K7** closure roots: y_t(32π) = 66.3803, y_t(quoted Λ) = 66.2999, y_t(thermal) = 77.876, each to 1e-3 relative.
- **K8** convergence: Route M tail split moved ×2 changes Q₂ < 0.5 %; Route G grid doubled changes < 1 %.

## Result lines (frozen; the physics outcome, not part of exit code)

For each (footing, y_t): **PASS** if Q₂ ≤ 9.0e-27 at **all four** E values; **FAIL** if Q₂ > 9.0e-27 at all
four; **E-DEPENDENT** otherwise. Same table vs 5.2e-27 reported as secondary.

Outcome statements:
- If the verdict changes across y_t ∈ [60, 140] ⇒ "**the turn-off band is cut to [y_lo, y_hi]**", mapped to κ
  through the closure κ = √(8π/F_can(y_t)).
- If the verdict is the same at all y_t (incl. no turn-off) **and** |Q₂(60) − Q₂(140)| < σ_Hees = 3e-27 at every
  (footing, E) ⇒ "**Q₂ cannot see y_t**"; the verdict itself (PASS or FAIL) is then a statement about the
  canonical law, not about P5.
- Turn-off effect reported as Q₂(y_t)/Q₂(no turn-off) − 1 per point.

## Mutation

`--mutate`: re-introduce the record's /√D transcription bug in Route M (branchB lane note). Must break K1, K3 or K4.

## What this cannot show

Static, uniform external field (no Galactic tide, no time dependence); QUMOND only (AQUAL differs by ≲ 30 %,
K5); the bound is the published fitted Q₂, not a refit with this law's full field.
