# D7d_screened_q2 — FROZEN CRITERIA (written before any script or number)

Door: D7b found the **unscreened** canonical law fails the Cassini quadrupole by 1.7–4.0×. The record's own
action (DSF-21 THEORY.md §2 / A33) carries the stiffness `γ = K L*²/2` that screens small systems
(CFG691, CFG740, CFG820). Question: with the stiffness on, in the Galaxy's field, what is Q₂ at
L* = 24, 50, 90 pc, both footings, and what is the smallest L* that passes Cassini?

## Record checked before freezing

- D7b (`doors_push_2026_10_22/D7b_cassini_Q2/`): QUMOND, unscreened, E0–E3, Q₂ 1.52–3.61e-26; K5 QUMOND/BN11-AQUAL 0.737.
- DSF-21 THEORY.md §1–2, A33 MASTER_ACTION.md §1–5 (P equation (P), lapse equation (L), `γ_F = γ_L`, slip O(ε²)).
- A22/A30: isolated hedgehog, `a_P = GM/L*²` sunward, `∇²(D·P) = −(K/γ)ρ`; "No EFE" stated as open (A22 report:234).
- CFG691: isolated spherical profile S(s), s = r/ℓ_γ, ℓ_γ = L*²/(2 r_M); table in `cfg691_results.json`.
- CFG820: L*_95 = 23.96 (canonical) / 24.72 pc (alt) from `cfg820_results.json` (the brief's 23.64/24.48 was not found in
  the record; the json values are used and the difference is reported).
- CFG740: sealed envelope γ_v − 1 = ½(s/L*)² (isolated inner limit).
- **CFG770 (already on record):** Cassini Q₂ of the same one-field stiffened action by linear response about the Galactic
  background: |Q₂| = 1.1–1.8e-32 (negative sign) at L* = 5.75 pc, ∝ L*⁻³. CFG832 then quotes a "Cassini lower gate
  0.087 pc" from the L*⁻³ extrapolation. **New here:** (i) an independent re-derivation from the DSF-21 action with D7b's
  E0–E3 fields; (ii) a **nonlinear** solve that connects the screened answer to the unscreened L* → 0 limit (the linear
  route is invalid there), so the Cassini lower bound on L* is computed, not extrapolated; (iii) the AQUAL vs QUMOND
  identity of the L* → 0 limit.

## Field equations (fixed now; derivation in the script header and README)

Static, weak field, `f = 1`, O(ε): drop `(1+γd)` and the lapse weight (O(ε²), A33 §3.3), `Φ = Ψ` (A12). With
`p ≡ K P` (acceleration units), `Φ = ln N`:

- (L) `∇²Φ = Kρ + ∇·p`, i.e. `∇Φ = g_N + Π_L p`;
- (P) `∇Φ + (L*²/2) ∇²p = a₀ p /(a₀ − |p|)` (vector Laplacian; `γ_F = γ_L` makes `γ[∇(∇·P) − ∇×∇×P] = γ∇²P`).

At L* = 0 this is AQUAL with μ = x/(1+x) (A33 K4), **not** QUMOND. So L* → 0 reproduces the AQUAL value, which
differs from D7b's QUMOND number by the known AQUAL/QUMOND factor (D7b K5: 0.737 against BN11).

Background: uniform Galactic field, `p_e = u_e ê`, `u_e = a₀ g_e/(a₀+g_e)`, `g_Ne = g_e − u_e`. The Sun's perturbation is
solved by two routes.

- **Route F (linear, Fourier, exact for L* ≫ r_M).** `[(k²L*²/2) I + J − k̂k̂] δp̂ = δĝ_N`, `J = diag(1+x_e, 1+x_e, (1+x_e)²)`,
  `x_e = g_e/a₀`. Then `δΦ̂_a = Φ̂_N χ(k)`, `χ = k̂·A⁻¹k̂`, and
  `Q₂ = (2GM/5π L*³) ∫₀^∞ κ² χ₂(κ) dκ` (κ = kL*, χ₂ the P₂ projection), up to the convention sign below. Valid while
  `GM/L*² ≪ u_e`.
- **Route N (nonlinear, axisymmetric grid).** Unknowns ψ (anomalous potential minus background) and q = p − p_e on a
  (ln r, θ) grid. Newton iteration with a sparse direct solve and damping that keeps |p| < a₀. Inner boundary
  r_in = 1e-5 r_M: ψ regular per Legendre mode, ∂q/∂ln r = 0. Outer boundary r_out = 1e4·max(1, L*/r_M) r_M: ψ decaying per
  mode, q = 0 (isolated mode: ∂ψ/∂r = q_r, q_r ∝ 1/r). Works at any L*, including L* = 0 (algebraic P equation).
- **Q₂ extraction.** Least-squares Legendre fit (l = 0..6) of ψ on each shell, interpolated to Saturn (9.58 AU):
  `Q₂ = s·3ψ₂(r_Sat)/r_Sat²` (from ½Q₂(z² − r²/3) = (Q₂ r²/3) P₂). The sign s is fixed once in the code: the BN11/Hees
  convention in which the unscreened MOND value is positive (checked by K3 sign agreement with D7b).

## Inputs (all labelled)

- a₀ canonical 9.36e-11, alt 1.13e-10 (never pooled); GM_⊙ = 1.32712440018e20; r_M = √(GM/a₀).
- E0–E3 exactly as D7b's `d7b_cassini_q2_results.json` (y_t = none): per footing, g_Ne and total g_e. The P5 turn-off
  is not a term of the action (A33 §6.3); D7b showed it moves Q₂ ≤ 0.7 %. Not used.
- L* = 24, 50, 90 pc (window, A33 table row 7). Globular bound from CFG820 json.
- Bounds (as transcribed in `prep_2026/planetary_doors/BOUNDS.md`): Hees 2014 Q₂ = (3 ± 3)e-27 → 2σ band
  **[−3.0e-27, 9.0e-27]**; Park 2026 (1.6 ± 1.8)e-27 → **[−2.0e-27, 5.2e-27]**. Two-sided, because the screened sign may be
  negative (CFG770). Per-planet constant-acceleration bounds (BOUNDS.md §1.2): Mars 1.4e-15, Earth 8.7e-15, Saturn 7.0e-15 m/s².
- BN11 Table 1 μ₁ (simple μ, AQUAL): Q₂ = 3.8e-26 at a₀ = 1.2e-10, g_e = 1.9e-10 (external, as transcribed).

## Checks (validation; exit 0 iff all PASS)

- **K1 (derivation, sympy).** (a) At L* = 0 the two equations give g_N = g²/(g+a₀) on a spherical configuration;
  (b) isolated spherical reduction with u ≪ a₀ gives CFG691's parameter-free equation −[q″+2q′/s−2q/s²]+q² = 1/s² with
  ℓ = L*²/(2r_M) and g_an = √(GMa₀)/r · s q(s).
- **K2 (Route F, L* = 0).** 1 + χ equals the linear AQUAL EFE response 1/[μ_e(1 + L₀c²)], L₀ = 1/(1+x_e), to 1e-12 on a grid of c, x_e.
- **K3 (Route N machinery vs D7b).** Route N in QUMOND mode (ψ from ∇²ψ = ∇·[(ν−1)g_N − background], ν−1 = (√(1+4/y)−1)/2)
  reproduces D7b's Route M Q₂ (y_t = none) within **2 %** (D7b's own K3 tolerance) at all 4 E, both footings, same sign.
- **K4 (L* = 0 is AQUAL).** Route N at L* = 0 with a₀ = 1.2e-10, g_e = 1.9e-10 gives BN11's 3.8e-26 within **10 %**.
- **K5 (CFG691/CFG820 profile).** Route N, isolated (g_e = 0), L* = 100 r_M: S(s) = u r/√(GMa₀) at s = 0.01, 0.1, 0.3, 1, 3, 10
  matches CFG691's table within **1 %** relative at each s.
- **K6 (routes agree where both apply).** Route N vs Route F at L* = 30 r_M and 100 r_M (canonical, E0 and E3):
  |N/F − 1| ≤ **5 %**, same sign.
- **K7 (limits).** (a) Route N at L* = 10⁻² r_M vs L* = 0: within 2 %. (b) Route F: |Q₂(L* = 10⁴ pc)| < 1e-9 × |Q₂_AQUAL(L*=0)|.
- **K8 (convergence).** Route N: doubling N_r and N_θ and halving r_in changes Q₂ < 2 % at L* = 0 and L* = 3 r_M (canonical E2).
  Route F: doubling the κ and c quadrature changes Q₂ < 1e-6 relative.
- **K9 (linear validity at the physical L*).** GM/L*² / u_e < 1e-4 at L* = 24 pc for every E and footing.
- **K10 (record reproduction).** Route F at CFG770's own inputs (g_e = 2.00/2.32/2.64e-10, a₀ 9.3603e-11/1.1312e-10,
  L* = 5.75 pc) reproduces its six Q₂ values within **1 %**, same sign.

## Result lines (frozen; the physics outcome, not in the exit code)

1. Q₂(footing, L*, E) at L* = 24, 50, 90 pc from Route F (Route N reported beside where run). **PASS** iff inside the Hees
   2σ band; Park band secondary.
2. **Cassini lower bound L*_C.** Route N on the grid L*/r_M = 0 and 10^(−1.5 … 2.0) in 0.25 dex steps (15 values), plus Route F
   above 100 r_M. Per footing, L*_C = the smallest grid L* above which every grid point passes Hees 2σ at all four E,
   refined by log-linear interpolation of the crossing. Reported in pc, against CFG820's 23.96/24.72 pc and CFG691's 5.75 pc.
3. Outcome: if L*_C ≤ 24 pc on both footings ⇒ "**screened theory passes Cassini for L* ≥ L*_C; consistent with the
   globulars**". If not ⇒ "**screening does not rescue Q₂**" with the mechanism. If the screened Q₂ passes but the L*_C
   bound is set by another gate, say which (Saturn monopole, CFG691).

## Consequences (reported only)

- Wide binary, 1.5 M☉ (CFG740's mass), 20 kAU: γ_v − 1 = ½ (radial anomalous / Newtonian) from Route F's monopole in the
  Galactic field, at L* = 24/50/90 pc; against CFG740's isolated ½(s/L*)² and against D2's unscreened 1.175/1.210.
- Inner planets: the constant sunward anomaly GM/L*² (A30) with its Route F EFE correction, against the Mars/Earth/Saturn
  bounds; beside the unscreened law-first tail (algebraic, with and without P5) at the same planets.

## Mutation

`--mutate`: Route N uses the scalar Laplacian on the spherical components of q (drops −2q_r/r², −(2/r²sinθ)∂θ(sinθ q_θ),
−q_θ/(r²sin²θ), +(2/r²)∂θq_r). Must break K5 or K6.

## What this cannot show

Uniform, static Galactic field over the screening region (the Galaxy's gradient on ~L* scales is ignored); O(ε) static
limit only; no planets' own fields; the published Q₂ is a fitted coefficient, not a refit of the ephemeris with this field.
κ = ½ FITTED. Not theory closed.

## AMENDMENT 1 (PRE-RESULT for every Cassini/physics line; written after prototype solver runs, 2026-10-22)

Disclosure: before this amendment, prototype runs were made at the canonical footing, E2 only, on coarse grids
(validation anchors K3/K4/K5, and a coarse Λ sweep while debugging the solver). No pass/fail line, bound, input or
tolerance is changed. What changes is the numerical method, for reasons found while debugging:

1. **Route N variables.** Newton in p fails near the cap |p| → a₀. Route N is solved in v = h(p) = a₀p/(a₀−|p|)
   (so p = v/(1+|v|/a₀), no cap constraint). Same equations.
2. **Production estimator = Richardson.** Route N is 2nd order in both directions; at (30 pts/decade, N_θ = 48) the
   QUMOND-mode error vs D7b is ~3 %, at (60, 96) ~0.8 %, and (120, 192) does not fit the memory budget. Every Route N
   number used in K3, K4, K6, K8 and the bound is the Richardson value R = (4Q(60,96) − Q(30,48))/3.
   **K8 is restated**: |R − Q(60,96)|/|R| < 2 % (the residual discretization correction) at L* = 0 and L* = 3 r_M, and
   halving r_in at (60,96) changes Q₂ < 2 %.
3. **K5 runs with Π_L p = p imposed exactly** (true for a spherical configuration). Reason: with a collocated ψ the
   O(dx²) mismatch between ∇ψ and p (~1e-4 relative) exceeds the isolated nonlinearity u/a₀ ~ 1e-4–1e-6 at
   L* = 100 r_M (prototype failed for this reason, not for physics). In the Galactic field the same term is O(1)
   (J − Π_L has eigenvalues x_e and (1+x_e)² − 1), so production runs are unaffected; K6 tests that coupling.
4. **The L*_C scan.** The prototype showed a genuinely singular band: for L* < r_M the hedgehog saturates the cap at the
   Sun (radial balance (1 − L*²/r_M²)/r²), and for L* < r_M√(1+x_e) the linear screened core p_e + (GM/L*²) r̂ would
   exceed the cap on the Galactic-field side. Newton does not converge in between. The scan is therefore run as two
   continuation sweeps on the frozen Λ grid (upward from L* = 0, downward from 100 r_M) at (30, 48), each point flagged
   converged (scaled residual < 1e-9 within 60 iterations) or not. **L*_C is reported as a bracket**
   [largest converged failing L*, smallest converged passing L* above which all converged points pass]; the passing
   endpoint is re-run with the Richardson estimator. Non-converged points are listed, never scored.
5. Sign: the prototype shows Route N (QUMOND) and D7b agree with s = −1 on 3ψ₂/r² (Φ = ordinary potential). CFG770's
   printed negative Q₂ is in the Φ convention (its formula is the same integral); K10 compares in that convention and
   the README states both.
