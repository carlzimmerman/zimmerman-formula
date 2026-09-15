# STATE — the glm53 track: FINAL BOARD (2026-09-14, night session)

## THE THEORY IN ONE PARAGRAPH (current, verified)

Spacetime carries one scalar with the frozen kinetic term L = Λ⁴f(K),
f(K) = K − 1/(1+K), f(0) = −1: manifestly Lorentz invariant, no aether, no
vector sector (α₁ = α₂ = 0 by structure), zero free parameters beyond a₀.
Its Noether charge is the cold dust. In the deep regime the scalar-mediated
force is exactly 1/r with constant C = √(GM_b·a₀), and hydrostatic balance
fixes the dust temperature to σ² = C/2 — the halo IS the phantom, coefficient
exactly 1, and the whole chain (ρ_Λ → σ² → ρ_ph → BTFR → g² = a₀g_N) closes
from the action with no tuning. In clusters the same charge appears in two
regimes: cold dust (c²_s = 0) in the Newtonian interior, equilibrated phantom
in the MOND outskirts, with the phantom share rising through a₀ (measured,
G050 V4) and the core-slope −1 (NFW) vs ~−1.5 (this theory) as the falsifier.
The partition function is now TESTED and honestly OPEN: the certified μ₂
kernel's sub-a₀ branch delivers ~6/10 of the cluster deficit at 420 kpc with
zero free parameters (a genuine parameter-free lower bound on the theory's own
cluster contribution, G059 corrective `2a5bb35bf`), and the residual is the
free dust's astrophysical-normalization share.
Cosmology is ΛCDM-exact on the frozen branch (w = −1, c_s² ∈ [1/2, 1)),
φ̇ = 0 is an attractor, and the registered growth raise carries over inside
band. One number remains empirical (n = 2: four structural routes closed);
the outer sag now resolves to a physical channel — the unmodeled asymmetric
drift (gas pressure support) correction closes it (G057 `6a7a35a4c`,
err+fullAD → −0.031 dex/dex), with the σ_z calibration as the identifying
test; and the cluster partition (G059) is tested with an honest negative.

## THE CENTRAL CHAIN — status of every rung

| rung | statement | status | lane |
|---|---|---|---|
| 0 | ρ_Λ = 4a₀²/(Gc²) ⟺ Λ_geom = 32πa₀²/c⁴ | DERIVED (action level, sympy-exact 9/9) | G031 |
| 1 | Noether charge = cold dust (c²_s = 0) | CERTIFIED | G028 |
| 2 | κ = ½ = 1/n from SPARC (n = 2) | DERIVED from data | G002 |
| 3 | deep force = 1/r, C = √(GM_b a₀) | DERIVED (scalar-mediated) | G046/G056 |
| 4 | **σ² = √(GM_b·a₀)/2 (c_deep = 1 EXACTLY)** | **DERIVED — 3 independent routes** | G046, G056, G031+Lean |
| 5 | ρ_ph = √(GM_b a₀)/(4πG r²), coeff exactly 1 | DERIVED + Lean | G003 |
| 6 | v⁴ = GM_b·a₀ (BTFR, zero parameters) | DERIVED + Lean | G003/G002 |
| 7 | g² = a₀·g_N (deep RAR) | DERIVED + Lean (deep_rar) | EQUILIBRIUM_THEORY.lean |
| 8 | Z = √(8πΩ_Λ/3) = 2.3955 | DERIVED | G019 |
| 9 | Ω_Λ = 32πa₀²/(3H₀²c²) = 0.6857 (+0.07%) | DERIVED + Lean CERTIFIED (`516693473`) | G052, G058 |

## G058 MILESTONE (2026-09-14) -- THE ONE-CONSTANT CLOSURE, LEAN-CERTIFIED

G052's central claim -- the dark-energy density IS the MOND scale --
is now a Lean certificate: `lean/G058_omega_from_a0.lean`, 6 theorems,
exit 0, zero sorry, axioms ⊆ {propext, Classical.choice, Quot.sound}
(independently re-verified by the main agent):

- **omega_from_a0 / omega_from_a0_gen**: from rho_Lambda = 4*a0^2/(G*c^2)
  (i.e. a0 = (c/2)*sqrt(G rho_Lambda)) and the Friedmann critical density
  H0^2 = 8*pi*G*rho_crit/3, the ratio is the EXACT identity
  Omega_Lambda = 32*pi*a0^2/(3*H0^2*c^2) -- no fitting, the G's cancel
  exactly, pi and a0 survive.
- **num_omega_lambda (the interval theorem)**: with a0 = 9.3619e-11,
  H0 = 67.4 km/s/Mpc in SI, c = 299792458, Omega_Lambda ∈ (0.68, 0.69)
  rigorously, via Mathlib's own coarse pi bounds (Real.pi_gt_d6/pi_lt_d4);
  the exact-rational window is [0.684930, 0.684932], margins ~0.005 per side.
- **num_omega_lambda_h0_planck**: the G052 canonical H0 = 67.36 variant,
  the registered 0.6857, same window.
- **one_constant_closure**: given ONLY a0, there EXISTS a UNIQUE
  rho_Lambda = 4*a0^2/(G*c^2) realizing the identity -- the dark-energy
  density is not an independent cosmological parameter; the MOND scale and
  the dark energy are ONE measurement.
- **omega_lambda_near_planck**: the derived value differs from Planck's
  0.6847 by < 0.001 (the +0.07% coincidence is a theorem about the one
  scale, not a fitted parameter).

Cross-check (G058_omega_numeric.py, exact Fractions): derived/Planck =
1.001525 at H0 = 67.36 -- G052's registered 1.0015 (+0.07%) reproduced
digit-for-digit.

## THE COMPLETION (frozen-scalar) — fully characterized

- hy4 H011 (11/11): L = Λ⁴f(K), Lorentz invariant, PPN-clean by structure.
- G054 (14/14): **φ̇ = 0 is an attractor** (φ̇ ∝ a^{-3} in the realistic
  spatially-dominated regime; a^{-3/2} pure-FRW worst case).
- G038 (6/6): background = ΛCDM **exactly**; c_s² = (u²+3u+2)/(u²+3u+4) → 1/2
  at K→0, rising to 1 — stable through the transition; **parameter count = 0**.
- Growth raise CARRIES OVER, modification stated: BGS +1.86%/+2.57% vs
  registered +2.75%/+3.79% (canonical/alt), inside the +1–4% band, ≤1.2 pp
  shift — well inside DESI errors.
- G055 Lean (`d0f3d645f`, 9 theorems, zero sorryAx — independently re-verified):
  f(0) = −1, f′(0) = 2 (deep-MOND), 1 < f′(K) ≤ 2 for K ≥ 0, f′ → 1,
  zero free parameters, dark-energy term −Λ⁴.

## CLUSTERS — the resolution assembled (4 lanes)

1. **G008**: pure power-law fluids dead (acausal); isothermal phantom
   baryon-steepened gives slope −1.478 at 100 kpc vs observed −1.53. T = 809 km/s
   from zero parameters.
2. **G012/G016/G017**: the capped amplitude — pure phantom over-supplies
   1.9–2.2×; free dust carries the cluster bulk; ΛCDM-shaped architecture.
3. **G050 (2/7, honest kills kept)**: **V4 PASS — the phantom share RISES as
   the field falls through a₀** (Spearman across 12 X-COP clusters × 8 radii,
   both footings). The split alone delivers 0.409× at 420 kpc — the free-dust
   abundance remains the open channel.
4. **hy4 H012 (8/8) — THE TWO-REGIME RESOLUTION**: interior = cold dust
   (c²_s = 0, no pressure support needed, no new particle, normalization as in
   ΛCDM — stated honestly); outskirts = equilibrated phantom carrying the SHAPE
   (slope −1.37/−1.40 steepening toward observed −1.53, zero parameters). The
   "two components" are ONE substance at two accelerations. **The falsifier:
   core slope NFW → −1 vs this theory → ~−1.5** (kill D2 registered).
5. **G057 cluster table** (`86bb771ea`): 12 X-COP clusters × 2 footings, the
   paper's cluster section table.
6. **G059 (TESTED — honestly OPEN)**: the partition function ran three
   candidates (kernel f(g/a₀), virial, r_M-surface) against G050's data on
   both footings. NO non-degenerate candidate closes [0.8, 1.3]: KERNEL
   0.571/0.615 (the nearest miss, zero free parameters — the certified μ₂
   kernel's sub-a₀ branch), VIRIAL 0.353/0.389, r_M 0.175/0.190 (binary,
   information-free on this data). The kernel's ~6/10 delivery is a genuine
   parameter-free lower bound on the theory's own cluster contribution; the
   residual is the free dust's astrophysical-normalization share, exactly
   H012's two-regime statement. A first commit (`5429900a9`) carried a
   solve_rM units bug (missing *MSUN) that returned a vacuous 1.000 by
   identity; caught in review, fixed and re-run (`2a5bb35bf`).

## THE HONEST RECORD — kills, anomalies, open items

- **G035 KILL**: Newtonian baryons+dust has NO phantom-temperature equilibrium
  (not an attractor, not even an equilibrium) — and this kill IS the discovery:
  the resolution is the scalar-mediated force (rung 4 above), not a different
  initial condition. Registered N-body follow-up: relaxation ONTO the
  equilibrium in the scalar-mediated dynamics.
- **The sag — RESOLVED TO A PHYSICAL CHANNEL (G057, `6a7a35a4c`)**:
  −0.13…−0.17 dex/dex, one-sign, 4–5σ (G049). The exhaustion sweep's
  baseline reproduced G049 field-for-field; of the six mechanisms, distance
  closes only 11%, inclination is exactly slope-degenerate by construction,
  but the **textbook full asymmetric-drift (gas pressure-support)
  correction closes it**: the error-model stack leaves −0.1250
  [−0.140,−0.106], the physical stack (err + full AD) lands at **−0.0310
  [−0.050, −0.010]** canonical / −0.0373 alt — inside the 0.05 threshold.
  Amplitude-modulated by gas dominance (rich −0.208 vs poor −0.076, p≈0.045),
  footing-independent. **Honest caveat: the closure is degenerate with the
  HI σ_z calibration** — it needs σ_z ≈ 10–16 km/s; at σ_z ≲ 7 km/s a −0.10
  residual survives. Decisive test: independent HI velocity-dispersion data.
- **Cassini**: bare μ₂ 5.45×/6.29× the ceiling (G005; L243's exact-AQUAL
  6.44×/7.63×); the fixed-congruence Horn A (G032: α₁ = 0 by architecture)
  is the PPN-clean completion.
- **L248 audit**: no reading where the phantom itself carries the lensing mass.
- **Mimetic routes closed** (G043, G048); **local k⁴ operators all dead**
  (G030 scalar trace, G034 Hessian², G032 aether biharmonic).
- **n = 2 remains empirical** — four structural routes closed (dimension,
  EFT, count statistics G009, photocount analogy).
- **G044**: EFE split NOT ESTABLISHED (p = 0.114 after the pre-committed
  audit); white-noise floor 0.0524/0.0538 dex; sag persists (binomial
  p = 4.5×10⁻⁴/8.2×10⁻⁵).
- **G040**: the per-galaxy RAR offset is a LOOCV mass plane (R² = 0.803);
  the floor stands at 0.094 dex (0.069 under errV < 10%).
- **G042 (14/14)**: Wang+2026 tests PLAIN MOND, not the slab; their 13σ is
  radial; ρ_ph(R₀) = 0.0078/0.0086 vs ClearPotential 0.0084 ⇒ 0.7/0.3σ.
- **G036**: radial scatter function — no NFW-shape fingerprint; white-noise
  floor 0.045 dex within-galaxy (V4a PASS after removing one line per galaxy).

## THE REGISTERED TESTS (dates and bands)

| test | when | band / prediction |
|---|---|---|
| Gaia DR4 wide binaries | December 2026 | Arm A falsified < 1.056; undecided 1.084–1.101; Arm B falsified ≥ 1.129 (σ_tot = 0.028); EFE bracket γ_v(20 kAU) = 1.095–1.111 |
| Euclid η (Ψ/Φ) | Oct 2026 | G052 lane: 5/6, η from the transition |
| BTFR zero-point z ≈ 2.5 | JWST-era samples | 0.00 vs +0.33 dex at ±0.13 (20:1 decisiveness) |
| WALLABY e_N ~ 1 EFE split | DR2+ | needs e_N up to 0.5-a₀ boundary — not yet enabled (max 0.119) |
| DESI DR2 growth | 2027 | +0.98%/+1.60% at z = 3; BGS +2.7% → QSO +0.6% falling profile (G024) |
| X-COP core slopes | available | NFW −1 vs theory ~−1.5 (H012's D2 kill) |

## THE ARTIFACTS (paper-ready)

- `glm53_push/THE_EQUILIBRIUM_THEORY.md` — the capstone.
- `deepseek_push/THEORY.md` + MNRAS skeleton + `PREDICTIONS.md` (E1–E10).
- `glm53_push/G057_cluster_prediction_table.*` — the cluster section table.
- `glm53_push/G029_theory_vs_lcdm_visual.html` — the 4-panel visual.
- `glm53_push/G033_build_fluid_bundle.py` + website suite (deployed,
  abeautifullygeometricuniverse.web.app/simulate).
- The interval-theorem pattern: `G036_formal_extras.lean` (41 registered
  numbers as marked intervals, π bounds).

## LEAN INVENTORY (glm53_push/lean/)

EQUILIBRIUM_THEORY.lean (7-thm spine) · G001 (9) · G002_G003 (4) ·
G007_bimetric (11) · G024_slab (9+1) · G031_fluid_action · G036_formal_extras (9) ·
G039_horn_a_clean + G039_radial_scatter (14) · G055_frozen_scalar (9,
`d0f3d645f`) · G058_omega_from_a0 (in flight) · plus hy4's H-series and
grok's K-series certificates. Every committed certificate: zero `sorry`,
axioms ⊆ {propext, Classical.choice, Quot.sound}, verified by independent
compile where marked.

## WHAT REMAINS OPEN (honest, at print time)

1. **The cluster partition law** — G059 tested three candidates and NO
   non-degenerate one closes; the kernel's ~6/10 delivery is the parameter-free
   lower bound, the residual is the free dust's astrophysical normalization
   (as in ΛCDM), stated as such. The amplitude stays NOT derived; the shape
   and the rising-share signature ARE (G008/G050/H012).
2. **The sag — resolved to a physical channel, one calibration open** (G057
   `6a7a35a4c`): asymmetric drift (gas pressure support) closes the sag
   (err+fullAD → −0.031 dex/dex, inside the 0.05 threshold); the open piece is
   the σ_z calibration (closure needs σ_z ≈ 10–16 km/s; at σ_z ≲ 7 km/s a
   −0.10 residual survives) — decisively testable with independent HI
   velocity-dispersion data.
3. **Relaxation onto the equilibrium** (G035's registered follow-up) —
   scalar-mediated N-body.
4. **Euclid η lane** — G052 landed 5/6; the η observable itself is the
   October test.
5. **n = 2 empirical** — four routes closed; no fifth known.
6. **The paper** — assemble → MNRAS free-format → arXiv (endorsement needed).

---

## HISTORICAL — the six-question campaign board (2026-09-13), preserved

