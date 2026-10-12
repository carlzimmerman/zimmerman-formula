# CFG642 — FROZEN CRITERIA: non-numerology symbolic regression for Ω_c/Ω_b

Committed alone, before any search code exists and before any search number is seen.
(ID note: CFG639, CFG640, CFG641 are taken; 642 is the next free ID; 600–619 never used.)

## Question

Owner request: find Ω_c/Ω_b = 5.364 "using symbolic regression like I did my original formula but not
numerology". A naive two-term scan over {1..10, π, e, φ, √2, √3, ln2} already puts ~49 of ~16k expressions
within 1σ (e + √7 = 5.3640 is one). This lane is built to REJECT such chance matches. It reuses the
discipline of project_atomos (constrained SR + FDR Gate A with its 10-bit ≈ p < 1e-3 threshold + the
interlock Gate B) and the record's standing rules: particle numerology walled; the 32π campaign found no
derivation; κ is underivable (κ = ½ FITTED); CLOSURE AUDIT L258 (the Ω_Λ-from-a₀ rung is circular) — so any
candidate that reaches Ω_c through the flatness identity is circular by construction and is gated out.

## 1. Target and error

- Primary: Planck 2018 (TT,TE,EE+lowE+lensing) ω_c = 0.1200 ± 0.0012, ω_b = 0.02237 ± 0.00015.
  R = ω_c/ω_b = 5.3643, σ_R = 0.0646 (errors added in quadrature as uncorrelated; the Planck ω_b–ω_c
  covariance is not on disk — disclosed). Relative precision 1.204%. R is h-independent.
- Independent Ω_b (on disk, used in gate d1): Cooke, Pettini & Steidel 2018 D/H = (2.527 ± 0.030)e-5,
  inverted with CAMB 1.6.6's PRIMAT 2024 table (primary; its sig(D/H) theory error added in quadrature)
  and the PArthENoPE 2017 table (bracket, reported). The BBN-route target is 0.1200/ω_b^BBN.
- No independent Ω_c route is used (none on disk that is free of the CMB fit); this is disclosed.

## 2. Inputs (physical, with units) and the grammar

Primitive inputs (Planck 2018 unless stated): ω_b; ω_γ from T_CMB = 2.7255 K (ω_γ = 2.4728e-5 (T/2.7255)^4);
ω_r = ω_γ (1 + 0.2271·3.046); ω_ν = 0.06 eV/93.14 eV (counted as matter late); h = 0.6736; Ω_Λ = 0.6847;
ω_c (needed only to build H(a) and z_eq — the contamination gate measures how much each candidate leans on it);
a₀ in two footings, NEVER pooled (separate searches): canonical 9.360e-11 = κc√(Gρ_DE), alt 1.131e-10 =
κc√(Gρ_crit) (values from real_research/derivation_chain_2026/FP0_core_postulates_results.json); κ = ½ (FITTED).
ħ and k_B are NOT inputs (they would open the walled microphysics/Planck-unit sector); T_CMB enters only
through ρ_r.

Buckingham-π basis at a named epoch with scale factor a (all quantities evaluated at that epoch):
  g1 = Gρ_b(a)/H(a)²,  g2 = Gρ_r(a)/H(a)²,  g3 = Gρ_DE/H(a)²,  g4 = a₀/(c H(a)),  g5 = κ,
with H(a)² = H₀²(Ω_r a⁻⁴ + Ω_m a⁻³ + Ω_Λ) (flat; a₀ and ρ_DE constant — the FLAT law).
Candidate: F = P · g1^n1 g2^n2 g3^n3 g4^n4 g5^n5,
  n_i ∈ {−2, −3/2, −1, −1/2, 0, 1/2, 1, 3/2, 2}  (9^5 = 59,049 exponent vectors),
  P ∈ {1, 2^±1, π^±1, (4π)^±1, (8π)^±1, (8π/3)^±1}  (11 declared geometric factors; NO e, φ, √7, ln 2 or
  arbitrary integers),
  epochs E ∈ {today z = 0; recombination z* = 1089.92; matter–radiation equality z_eq = (ω_b+ω_c)/ω_r − 1;
  BBN deuterium bottleneck T = 0.07 MeV, 1+z = T/(k_B·2.7255 K)}.
2,598,156 members per footing. Positive-control requirement on the grammar: it can express the original law
(a₀/(cH₀) = κ·g3^½ at today, P = 1) — checked in the code.

Complexity C = Σ 2|n_i| + [P ≠ 1]. MDL score (bits) L = log2 N_eff(≤C) + z²/(2 ln 2), z = (F − R)/σ_R,
where N_eff(≤C) is the number of DISTINCT values (log10 rounded to 1e-10) with complexity ≤ C.
N_eff = number of distinct values in the whole footing search; also reported: distinct values in [1, 10].

## 3. Epoch rule (Ω's are time-dependent)

ρ_c/ρ_b is constant in a, and the CMB measures it at z*. A candidate "set" at epoch E must therefore be set at
or before recombination (z_E ≥ z*). A candidate whose value changes with a (|d ln F/d ln a| > 0.01 at its
epoch) and is stated at E = today FAILS the epoch gate (it would hold only now, after the ratio was already
measured at z*). Epoch-invariant candidates pass at any epoch.

## 4. Honesty gates (all must pass for anything but "chance")

(a) FDR / look-elsewhere, on the WHOLE declared search of each footing (primary) and, secondary, on the
    rule-selected clean subspace (members passing (c) and the epoch rule — selected by rule, not by result):
    statistic = best (minimum) MDL score L over the search.
    - 4000 random decoy targets, log-uniform on [1, 10], rounded to 4 significant figures, σ = 1.204% of value;
    - 2000 shuffled-input controls on the real target: ω_b, ω_γ, Ω_Λ, a₀ each × 10^U(−1,1), κ × 10^U(−½,½),
      everything (epochs, H(a)) rebuilt; the complexity code table of the real inputs is reused.
    p = (1 + #{controls with best L ≤ real best L})/(N + 1). PASS requires p < 0.0005 for BOTH control types
    (0.001 Bonferroni-split over the two footings).
(b) INTERLOCK (declared in advance): b1 — a candidate containing a₀ (n4 ≠ 0) must also hold within 1σ in the
    OTHER footing, evaluated separately (never pooled); b3 — a second, independently measured quantity the
    candidate's mechanism predicts and was not fitted to. The SR grammar supplies no mechanism, so b3 is
    UNAVAILABLE for every grammar candidate: no grammar candidate can pass (b) without an added mechanism.
    Reported for information only (NOT counted as an interlock, because it follows from the fitted value):
    b2 — Ω_m^pred = (ω_b(1+F) + ω_ν)/h² vs DESI DR2 BAO-alone Ω_m = 0.2975 ± 0.0086 (on disk:
    nbody_2026/routeB_dust_to_dark_energy_2026.py), within 2σ combined with the h error propagated.
(c) No circularity: elasticity ε_c = ∂ln F/∂ln ω_c through the input provenance (Ω_Λ = 1 − Ω_m − Ω_r with
    ω_b, ω_ν, ω_r, h fixed; H(a); z_eq; z* via the Hu & Sugiyama 1996 fit; canonical a₀ through ρ_DE; alt a₀
    through ρ_crit only) must satisfy |ε_c| ≤ 0.05 (the target's own elasticity is 1). This catches the L258
    flatness route (Ω_Λ carries ε = −Ω_c/Ω_Λ ≈ −0.39).
(d) Stability: d1 — re-evaluated with ω_b^BBN (PRIMAT inversion) in the inputs, within 1σ of the BBN-route
    target (σ from both); d2 — re-evaluated at h = 0.7304 (SH0ES, on disk in CFG493) with ω's fixed and
    flatness, within 1σ of R (R is h-independent, so a physical formula must be too).

Controls: TRUE-VALUE control (F ≡ R, a constant) through b2, d1, d2; injected positive controls (200 grammar
members with C ≤ 6, allowed epochs, |ε_c| ≤ 0.05, used as targets) at the real 1.204% precision with Gaussian
noise and at 0.001% precision (with matching 0.001% decoys) — gate (a) power at each precision; MUTATE=1
run (separate outputs) replaces the target with one planted grammar member at 0.001% precision — gate (a)
must PASS there (the machine can certify when precision allows).

Illustration (not a gate): the naive space — atoms {1..10, π, e, φ, √2, √3, ln 2} with unary {x, √x} and
binary {+, −, ×, ÷} — its 1σ hit count, the z of e + √7, and the decoy p of its best match (best-|z|
statistic, same 4000 decoys).

## 5. Pre-search power statement (analytic, computed before any search)

A single fixed number lands within ±1σ of a log-uniform [1,10] decoy with probability 2(0.01204)/ln 10 ≈ 0.0105.
To reach p < 0.0005 a SINGLE pre-declared expression must land within |z| < 0.048; with N in-range distinct
values the closeness required scales as ~0.048/N — far below what a 1.2% measurement can certify. At this
precision gate (a) is structurally unpassable for any search with more than a handful of in-range values
(the atomos bit cap: ~1.9 known digits ≈ 6.3 bits < the 10-bit threshold). Expected verdict: CHANCE-LEVEL.

## 6. Verdict rule

- CHANCE-LEVEL: the global best fails (a) in both footings.
- SURVIVOR WITHOUT INTERLOCK (not a result): passes (a), (c), epoch, (d) but not (b).
- HYPOTHESIS NEEDING A MECHANISM: passes all gates (never "derived").
Never "theory closed"; never a derivation of 5.364 from a fit. κ = ½ FITTED.

Compute: one process, nice -n 10, < 1.5 GB. No downloads.
