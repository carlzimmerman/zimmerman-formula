# THE PREDICTIONS LEDGER — every testable prediction of the programme, in one place (2026-09-02)

Consolidates the four inventory sweeps of 2026-09-01 (`INVENTORY_1`, `INVENTORY_SWEEP2`, `SWEEP3`, `INVENTORY_4`), the rev. 6
STANDING block, and the 2026-09-02 closures. **Status words are the corpus's own** (IN FORCE / LIVE / RETRODICTION / NON-PREDICTION /
VOID / WITHDRAWN). Both a₀ footings everywhere a dimensionful number appears: canonical a₀ = ½c√(Gρ_Λ) = 9.36e-11 m/s², alt = 1.13e-10
(ρ_total). Ratios a₀(z)/a₀(0) are footing-independent. Kernel: Route A, ν(y) = 1/(1−e^{−√y}). Arm: modified gravity (AeST chassis).

---

## 0. The equations as they stand, and which numbers are fitted

| | equation | status of every constant |
|---|---|---|
| E-1 the scale | a₀ = κ c √(Gρ_DE), **κ = ½ FITTED** (measured 0.551 ± 0.043 distance-free, 0.465 ± 0.076 BTFR; four candidates inside 2σ) | κ: fitted, never derived (every lane dead, ledgered). ρ_DE: Planck input. |
| E-2 the law | g_obs = ν(g_bar/a₀) g_bar, ν = 1/(1−e^{−√y}) (spherical); AQUAL/QUMOND field equation off-symmetry | kernel shape: chosen (Route A) after α = 1, 2 failed the ephemeris; not derived |
| E-3 the clock | K(Q) with −K(Q₀) = M⁴ = ρ_Λ: **dark energy is the vacuum energy of a shift-symmetric clock field**; the conserved shift charge n = K′ ∝ a⁻³ is the cosmic dust ("dark charge") | M⁴: input (= Λ). β = 1 SELECTED not derived. ν₀ ∈ [2.14e-5, 1.77e-4] windowed by CMB + RAR |
| E-4 the well identity | matching theorem: a well of charge overdensity δ IS the background at (1+z)³ = δ, same sound speed, any K (DOI 22261001) | theorem, no constants |
| E-5 the static dust | p_d = (2πG/μ²)ρ_d², c_s² = \|Ψ\|c²; ∇²Ψ + μ²(Ψ−C) = 4πGρ_b is its hydrostatics | μ: free in AeST; C: fixed by charge conservation (09-02) |
| E-6 the evolution | a₀(z)/a₀(0) = √(ρ_DE(z)/ρ_DE(0)); derived law flat to <1e-4 at z = 3, MOND off at z ≳ 20 (v9 switch), 0.006 at recombination | the one distinctive prediction; footing-independent |

**What E-3 does and does not say about dark energy.** It says what it is in the chassis (the clock's vacuum energy) and ties the galaxy
scale to it (E-1). It does **not** say why M⁴ has its value or why κ = ½. A "new equation that explains dark energy" would have to
produce one of those two numbers from something else. None exists in this corpus; the attempts are in `RETRACTIONS.md` and the κ ledger.

---

## A. LIVE, DATED, PRE-REGISTERED (the ones that can still win or lose)

| id | prediction | number (canonical / alt) | data, when | what falsifies it | status |
|---|---|---|---|---|---|
| A-1 | **Wide-binary velocity boost** at 2–30 kAU, full nonlinear AQUAL-EFE solve (Amendment 10) | γ_v = **1.1614–1.1814** / **1.1917–1.2267**; Newton = 1.000 exactly; no-verdict edge 1.23, contamination guard 1.23–1.33 | Gaia DR4, ~Dec 2026; frozen pipeline `prep_2026/gaia_dr4_prep/` | a Newtonian result is evidence AGAINST at ≥ 5.8σ_tot (N = 30k, σ_sys = 0.02); must not be re-hedged. γ̂ > 1.23 = unscoreable (contamination). Reports raw γ̂ + both distances, never one verdict word | IN FORCE |
| A-2 | **a₀ does not evolve below z ≈ 5** (the sharp null) | a₀(3)/a₀(0) = 0.99997; a₀(5)/a₀(0) = 0.99963; ΛCDM-native emergent scale rises ×1.8 (z=2), ×2.1 (z=2.5), ×2.6 (z=3) | deep-MOND BTFR zero-point at z ≈ 2.5 to ±0.13 dex (decides at 20:1); none exists in any archive (census 09-02) | any robust evolution, EITHER sign, below z ≈ 5. A value BELOW 1 at z = 2–3 is drift-proof (no systematic can make it); a value at +0.3 dex kills FLAT | LIVE, undecided (present data prior-dominated; KLASS/MUSE/Ciocan lean against at face value) |
| A-3 | **DESI/Rubin w(z) gate**: the framework predicts dissolution to w = −1; under evolving DE, R = a₀(3)/a₀(0) declines | DESI DR2 input: R = 0.775 [0.68, 0.88], 2.0σ decline → UNDECIDED; Rubin forecast reaches 3.3σ | Rubin/LSST-DESC calibrated SN sample ~2027+; frozen `prep_2026/rubin_prereg/` | Verdict C (a₀ rises at ≥ 3σ) FALSIFIES; Verdict B (w → −1) dissolves to constant-a₀ MOND (safe core); a standing evolving-w detection is evidence against | IN FORCE (frozen 2026-07-21) |
| A-4 | **Directional external-field effect**: outer rotation-curve asymmetry pointed at the attractor, signed | A = +1–4% (AQUAL, x = 0.05–0.5, e = 0.03); Branch B 0.5–3.1%; null = 0 | WALLABY/MaNGA per-side kinematics + 2M++/MCXC field vectors. On record: n=16 Â = +2.95 (p = 0.03); **n=25 WALLABY Â = −1.70 ± 2.12 (p = 0.59)**, sensitivity 0.3σ | R1 detection at AQUAL amplitude (≥3σ from 0) → pure MI dead, both MG doors live; R3 deep null below 0.7% → AQUAL AND Branch B dead. Needs N ≥ 560 (detection-vs-null), ~1,160 (deep null) | LIVE, no signal either way |
| A-5 | **Oort-cloud comet anisotropy** keyed to the galactic external-field direction; the ν₀-correlated pair with A-1 | spike-position modulation 1.069 (7%), injection-rate 1.169 (17%); ν₀ floor → 16.7%, ceiling → larger | long-period comet catalogues; DOI 21966646 | isotropic comet injection at the 5% level; or A-1 and A-5 disagreeing on ν₀ | LIVE (prior art Pauco & Klacka 2016 owed) |
| A-6 | **Euclid cluster kink, exact null**: Branch B throttle predicts a slope break at g_bar = y_c a₀; pure MI and ΛCDM predict none | y_c = 2.894; g_bar(kink) = 2.71e-10 / 3.27e-10 | Euclid DR1 cluster lensing; `prep_2026/cluster_kink_spec/` | detection → Branch B supported; null does NOT separate MI from ΛCDM (stated up front) | IN FORCE (filed 2026-07-16) |
| A-7 | **Isolated-galaxy lensing stays on √(g_bar a₀) with NO dark-charge excess** to 1 Mpc | pure MOND χ²/dof 2.03 / 0.94 on KiDS; an accreting cold charge would multiply 100 kpc–1 Mpc by 3–20 (e_N = 0.03–0.1), Δχ² ≥ +106 for every AeST m² (09-02) | Euclid DR1 / LSST isolated-lens RAR (mid-2020s) | a ×2–3 excess at 100–300 kpc around isolated lenses = a cold component accreted into MOND wells = the AeST-class picture the framework excludes; both ways: ×2 is inside today's ±0.3 dex amplitude budget | LIVE |
| A-8 | **BIG-SPARC environmental fork**: per-galaxy a₀ tracks ρ_Λ, not ρ_local | decisive null 13–34σ on 175 SPARC; pipeline ready | BIG-SPARC (not public) | a₀ correlating with local density | LIVE (pipeline) |
| A-9 | **The crispy gap** (ΛCDM's side of A-2): to mimic a flat a₀, halo structure at fixed mass must dilute as c/c_Nbody ≈ (H/H₀)^{−2/3} | 0.61 at z=2, 0.40 at z=3, 0.12 at z=5; no NFW solution at z=5 | JWST/lensing halo concentrations at z ≥ 2 | concentrations at N-body values at z ≥ 2 while a₀ stays flat = the framework's a₀ is not emergent (framework); concentrations diluted as predicted = ΛCDM survives flat a₀ | LIVE (a ΛCDM-side prediction) |
| A-10 | **κ = ½ vs 1/(2π)** | Δχ² leans ½ at ~2.2σ (one shape) / 1.55σ (shape-free); distance-free path 7.2% → 3.0% | SPARC + TRGB distances; Gaia DR4 is NOT a κ-meter (dlnγ/dlnκ = 0.18) | ½ excluded at 3σ by the g_bar-axis distance-free estimator (floor 3.9%) | LIVE, no shape reaches 3σ |

## B. RETRODICTIONS (parameter-free, already confronted, hold)

| id | statement | number | data |
|---|---|---|---|
| B-1 | one acceleration scale, zero intrinsic per-galaxy spread, no mass trend | observed 0.275 dex spread / slope +0.07; framework mock 0.30 / +0.03; ΛCDM AM+NFW mock 0.45 / +0.23 | 147 SPARC rotation curves |
| B-2 | BTFR as a theorem of the law: v⁴ = G M_b a₀ | zero-fit baryon-mass predictor median M_pred/M_phot 1.15 / 0.97 | SPARC |
| B-3 | lensing = dynamics, γ_PPN = 1, no slip | residual 0.601σ (the pure-MI predecessor died at 21.2σ) | cluster + galaxy lensing |
| B-4 | Milky Way vertical force + Eilers slope from full AQUAL | f_M = 1.30 nails both; fails only the v_c normalisation (baryon budget) | Gaia/APOGEE |
| B-5 | solar system: exponentially small departure from Newton | fractional 2.7e-22 at the Sun; Cassini quadrupole, Earth/Mars ranging passed (α = 1, 2 both failed; Route A discharges) | ephemerides |
| B-6 | tensor speed c_T = c | exact in the chassis (GW170817) | LIGO/Virgo |
| B-7 | CMB indistinguishable from ΛCDM under the derived law; MOND off at recombination is an OUTPUT | a₀(z*)/a₀(0) = 0.006; \|1+w\| = 2.3e-5 at z = 2 | Planck (AeST-class background, any cold K) |
| B-8 | SN Ia host-mass step sits at a₀ | 6.9σ step reproduced; decisive tests underpowered (18%) | Pantheon+ (disfavoured-not-excluded reading) |
| B-9 | Lyman-α forest small-scale cutoff | sign robust, 0.4–0.9σ (the "6–8σ" WITHDRAWN); Murgia α < 0.03 h⁻¹Mpc passes at every z | XQ-100 / MIKE-HIRES |
| B-10 | Σ† = a₀/(πG) surface-density threshold (2× the usual quote) | 213.8 / 258.3 M☉ pc⁻² | SPARC |

## C. NON-PREDICTIONS (things the framework does NOT predict; do not sell them)

| id | statement |
|---|---|
| C-1 | S8: no prediction either way (linear order inherited unchanged; nonlinear sign adverse, unpriced) |
| C-2 | 21-cm / cosmic dawn: z_t ∈ [17, 35] sits in the EDGES window but there is NO linear signature |
| C-3 | halo abundance and early-galaxy counts: ΛCDM's (MOND contributes zero to linear growth at every z) |
| C-4 | collapse-timing speedup 1.1–2× at z = 6–25 is real but observationally inaccessible (needs Σ < Σ† rotators at z > 5) |
| C-5 | clusters: the framework does NOT close them by itself; η(R500) = 1.7–2.1 (kernel-named) is a standing liability, not a prediction |

## D. VOID / WITHDRAWN / SUPERSEDED (so nobody cites them as predictions)

| id | former statement | why it is dead |
|---|---|---|
| D-1 | s^TX SME boost dipole, \|s^TX\| = 8.7e-10 | α = 2 collapses it to 1.3e-15; DETECT/KILL bands VOID (Amendment 5) |
| D-2 | CPL a₀(z) bump +6% at z ≈ 0.4, decline 0.74 at z = 3 | superseded by the derived flat law (stage 17); low-z rise now counts fully against |
| D-3 | constant a₀/2 sunward planetary anomaly | α = 1 identity withdrawn (1279× the Earth ephemeris bound) |
| D-4 | wide-binary DEAD ZONE (Newton at 10–60 kAU, gate-shut) | reading AC withdrawn; γ_v ungated |
| D-5 | "21.6 a₀ at R500" cluster scale | wrong (that is the core scale; R500 sits at 0.33–0.58 a₀) |
| D-6 | "kernel removes 74–89% of cluster dark matter" | withdrawn (48% at R500) |
| D-7 | λ_J = 2.7 Mpc condensate Jeans scale; S8 relief | withdrawn / dead on scale (35× short) |
| D-8 | "pure MI predicts exactly zero directional asymmetry" | wrong (derived EFE gives 4–22%); arm closed anyway |
| D-9 | Tabby-star exo-Oort as a gravity instrument | dead (6.7 orders of slack) |
| D-10 | v9 single-field DBI dark sector; "the condensate's pressure keeps dark matter out of galaxies"; the CMC filter as a 2-DOF mechanism | all excluded 09-02 (`condensate_pincer_2026/`) |
| D-11 | AeST's free per-galaxy boundary constant as an escape | fixed by charge conservation; excluded for every m² on KiDS (09-02) |
| D-12 | κ = ½ derived (any route: dS-Unruh, entropy, graviton bath, action modulus) | never; fitted |

---

## E. What would make it a closed theory (one line)

Two numbers: A-1 landing inside its band in December, and A-2 measured flat at z ≈ 2.5 to ±0.13 dex. Either one landing the other way ends the
distinctive claim. Neither can be produced from data in hand.
