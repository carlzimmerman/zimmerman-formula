# X50_floor_is_the_phantom — FROZEN CRITERIA (committed alone with the ledger, before any script or number of this lane)

**Hypothesis PF (the floor is the phantom).** In isolated galaxies, the cold dark energy halo that fits the data at the
a₀/(2πG) floor (X38: Burkert, ρ₀r₀ = Σ_a₀ ≡ a₀/(2πG) = 107 / 129 M☉ pc⁻²) is quantitatively the law's own phantom halo,

    ρ_ph = ∇·(ν(g_N/a₀) g_N)/(4πG) − ρ_b   (sign convention: g_N pointing inward, ρ_ph ≥ 0),

with the record's simple ν(y) = ½ + √(¼ + 1/y) (P4, EM1). If PF holds, "the law is fundamental" and "cold dark energy
settled at the floor" coincide in galaxies, and the tether reads "cold dark energy fills the phantom profile".

Standing rules: κ = ½ FITTED. Footings never pooled (canonical a₀ 9.3603e-11, alt 1.1312e-10 m s⁻²). No dark-matter
particle; cold dark energy is a gravitating w ≈ 0 field component, not matter. No new constant is fitted. Not "theory
closed". Nothing here may say the data favour the framework. Literature values are PROVISIONAL.

## 0. Step 0 (stop rule)

- **K0a:** X38's four SPARC rows reproduced by this lane's code (EM1 machinery executed read-only, X38's Burkert solver
  copied): rms 0.0795 / 0.0792 (canonical, bg A / B) and 0.0729 / 0.0729 (alt), |Δrms| < 1e-4, same median Υ
  (0.77 / 0.76 / 0.60 / 0.60).
- **K0b:** P4's law row reproduced: rms 0.054087 / 0.053718 at median Υ 0.52 / 0.44 (|Δ| < 1e-4).
- If either fails: verdict **UNDECIDED (step 0)**, no graded number is interpreted, exit 1.

## 1. Phantom definition used for the per-galaxy grade

The record's SPARC law is the algebraic g = ν(g_N/a₀) g_N on the spherical-equivalent g_N = V_bar²/R (P4: exact AQUAL
for a sphere; disc geometry shifts the in-plane g by −0.002 to −0.006 dex median, disclosed in the ledger). So per galaxy:

- phantom pull g_ph(r) = (ν − 1) g_N; phantom enclosed mass M_ph(<r) = g_ph r²/G; ρ_ph = (4πG r²)⁻¹ d(r² g_ph)/dr;
- Υ is **P4's per-galaxy Υ** (the law's own best Υ on EM1's grid, EM1's weights and mask); the floor halo is **X38's**
  (EM1 relation a = 11.18, b = 0.90 on background A; R200 at 200 ρ_c with bg A's h; A1 compact root; Σ_a₀ per footing).
  X38's halo does not depend on Υ.
- Evaluation points: the galaxy's data radii that pass EM1's mask at that Υ (R ≤ R_last).
- Isolated: no external field (P4: Chae's g_e changes the rms by < 0.001 dex).

## 2. Analytic part (sympy, PYTHONHASHSEED=0; all reported, and checks K1–K3 below)

With y = g_N/a₀ and Q(y) ≡ y(ν − 1) = g_ph/a₀:

- **A1 (pull bound).** Q is monotone increasing with sup Q = 1 (y → ∞): |g_ph| < a₀ strictly (spherical/1D exact; QUMOND
  up to its curl field). In X47's peak-pull convention a Burkert floor core pulls at most c_B a₀, c_B = 0.254484, so the
  phantom's pull-equivalent surface density is bounded by 1/c_B = 3.93 Σ_a₀. Equivalently M_ph(<r)/(πr²) < 2 Σ_a₀.
- **A2 (central column of a thin disc, exact QUMOND on the axis).** Σ_ph(0) = Σ_M S(y_s), Σ_M ≡ a₀/(2πG) = Σ_a₀,
  y_s = 2πGΣ_b(0)/a₀, S(y) = ∫₀^y (ν(t) − 1) dt (derived in the script; the assumptions are reflection symmetry, a purely
  vertical field on the axis and |g_N| decreasing along it). Closed form, small-y and large-y limits, and y_s at which
  S = 1 (Σ_ph(0) = Σ_a₀) and S = π/2 (the floor Burkert's own central column, (π/2) Σ_a₀) are reported.
- **A3 (profile shape).** Point mass: ρ_ph series at r → ∞ (deep-MOND r⁻² with coefficient √(GMa₀)/(4πG)) and r → 0.
  Spherical-equivalent exponential disc and a cored baryon sphere: central log-slope of ρ_ph. Against Burkert (flat core,
  r⁻³ tail).
- **A4.** A one-line statement of exactly what Σ_ph,max is and in which convention it equals a₀/(2πG).

## 3. Per-galaxy comparison (SPARC, verdict-bearing; per footing)

For each galaxy (all galaxies EM1 loads):

- **M1 (mass).** log q = log₁₀[M_ph(<R_last)/M_X38(<R_last)].
  Gate: |median log q| ≤ 0.10 dex AND half-width (p84 − p16)/2 ≤ 0.20 dex.
- **M2 (surface density, primary; X47's peak-self-pull convention, which X47 shows equals the mean-enclosed measure by
  identity).** log s = log₁₀[max_data g_ph / max_data g_X38], both maxima over the same evaluation points.
  Gate: |median log s| ≤ 0.10 dex.
  Reported with it: max_data g_ph/(c_B a₀) (the phantom's pull-equivalent ρ₀r₀ in units of Σ_a₀, against the floor's 1).
- **M3 (shape within the data range).** Per galaxy, the rms over evaluation points of
  [log g_ph − log g_X38 − (its per-galaxy mean)]. Gate: median ≤ 0.10 dex.
- **Reported only:** effective outer density slope of each halo (least-squares d ln M/d ln r over the outer half of the
  points, minus 3); a free Burkert fit (ρ₀, r₀) to the phantom's M_ph(<r) on the points (ρ₀r₀/Σ_a₀); the A2 disc-centre
  column Σ_M S(y_s) with Σ_b(0) = Υ SBdisk (SPARC table, stars only) against the floor column (π/2) Σ_a₀; the phantom at
  X38's own per-galaxy Υ; X38 halos on background B; Spearman correlation of log s with log Σ_b(0); and X47's free
  per-galaxy Σ fit recomputed (same grid and rule) and its Spearman correlation with the phantom's pull-equivalent Σ.

## 4. Verdict classes (per footing; the lane class needs both footings to agree, else UNDECIDED)

- **PF HOLDS (the floor halo equals the phantom within errors):** M1, M2 and M3 gates all pass.
- **PF HOLDS IN SURFACE DENSITY ONLY (shapes differ):** M2 passes; M1 or M3 fails.
- **PF FAILS (state how):** M2 fails. The direction and size of the M2 offset and the M1/M3 results are stated.
- **UNDECIDED:** step 0 fails, any check K1–K4 fails, or the footings disagree.

## 5. Dwarfs and ultra-faints (frozen sub-question; does not enter the PF class)

X49's data, binary-corrected σ, r₁₂, M_b(<r₁₂) = M_b/2, error sdMC[Newton], bootstrap (10 000, seed 20261026) and classes,
read-only. Phantom prediction (isolated, an upper bound on the phantom; an external field only lowers it):
g_pred = ν(g_N/a₀) g_N at r₁₂. Per class: median E_ph, Z, and the median of M_ph(<r₁₂)/M_X49(<r₁₂) (X49's floor halo
recomputed with its solver).

UFD answer (per footing): **PHANTOM HEAVIER AND FITS** (median mass ratio > 1 and |Z_ph| < 2) / **PHANTOM HEAVIER, STILL
SHORT** (ratio > 1, |Z| ≥ 2) / **PHANTOM NOT HEAVIER** (ratio ≤ 1).

## 6. Clusters (reported only)

Phantom pull-equivalent Σ at X40b's committed cluster-core g_b/a₀ (KT tercile medians at r₀), Q(y)/c_B in Σ_a₀ units,
against X43's required core η Σ_coll (η = 14.8, Σ_coll at 1e14 / 1e15 M☉ from X43's committed table). If the phantom is
far below, the cluster excess must come from collapse (X43/X48 route); consistency is stated in words.

## 7. Checks (all must pass in the normal run)

- **K0:** step 0 (K0a and K0b).
- **K1:** sympy: Q(y) → 1 as y → ∞ and Q < 1 on a grid; S(y) closed form against numerical quadrature to 1e-8 at five y.
- **K2:** numerical exponential thin disc (Hankel-integral field, R and z components, finite-difference divergence near the
  axis plus the in-plane sheet term) reproduces the closed form Σ_M S(y_s) of the simple ν (always the record's ν, also in
  MUTATE) to 1e-3 relative at three central surface densities.
- **K3:** point mass: M_ph(<r)/(r √(G M a₀)/G) → 1 at r = 100 r_M within 1e-2, and ∫4πr²ρ_ph dr (quadrature of the
  analytic ρ_ph) returns (ν − 1)M to 1e-6.
- **K4:** peak RSS < 1 GB; one thread; `nice -n 15`.

## 8. MUTATE plan

`X50_MUTATE=1` replaces ν by 1 everywhere in this lane (sympy and numerics): no phantom. Named checks that MUST FAIL:
**K0b** (the "law" row becomes the Newtonian row), **K2** (the numerical column is 0 against the simple-ν Σ_M S),
**K3** (no deep tail; the reference is √(G M a₀), unmutated).
The MUTATE run must end **UNDECIDED (step 0)** with exit 1, writing separate `_MUTATE` outputs.
