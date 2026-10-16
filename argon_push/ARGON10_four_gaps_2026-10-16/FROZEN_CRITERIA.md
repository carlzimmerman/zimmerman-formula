# ARGON10 — independent cross-check and extension of astra's four-gap pass (quantum, formation, gravity-response, dark-energy normalization). FROZEN CRITERIA

2026-10-16. Committed alone, before any scored script. Lives in `argon_push/` (my folder). No file of astra's (`sol61_push/`) is edited;
astra's numbers are read as COMPARISON TARGETS only. κ = ½ FITTED; footings 9.3603e-11 / 1.1312e-10 m/s² are never pooled; "cold energy";
its mass is required; this is not "theory closed" and no ΛCDM / standard-MOND yardstick enters any verdict.

**Source read before freezing (not re-derived here):** `sol61_push/closure_particle_bridge_2026_10_16/` — `MEDIATOR_COMPLETION_AND_VALIDITY.tex`
(the potential), `FOUR_GAP_AUDIT.txt`, `CURRENT.txt` (CPB-QFG, 2026-10-16). The potential (m_h = 1 unit, M ≥ 1):
V = I + L I² + a χ I + M²χ²/2 − (M/8) χ³ + χ⁴/4, L = 2 − 1/M, a = 2M, I = |Ψ|², canonical complex Ψ and real χ.
Weak route (astra's definition): L, λ_χ → εL, ελ_χ; a, μ → √ε a, √ε μ; masses fixed.

**Disclosure of scratch checks.** Before freezing I ran two scratch calculations only to settle *definitions* (one-loop β of the 3-real-scalar model
at M = 100; the rotating-frame fluctuation spectrum at M = 100). They matched astra's quoted values. They are not the scored runs, and no threshold
below was set from their outputs: thresholds are astra's own gates (1 %, 0.1) or round numbers.

## Part Q — quantum corrections
**Q1 (independent reproduction).** Hessian of V in (φ1, φ2, χ), I = (φ1²+φ2²)/2; β_V = Tr H²/(32π²); couplings read off by coefficient.
β_net ≡ d(L − a²/(2B))/d ln μ with B = M²; β_m² ≡ d m²/d ln μ. Independent identity check: μ-derivative of the MS-bar Coleman–Weinberg
potential V1 = Σ h²(ln(h/μ²) − 3/2)/(64π²), by finite difference in ln μ, at 5 random (I, χ) points.
- **AGREES** iff |β_net(M=100) − 0.28273| ≤ 5e-5, |β_m²/m² − 506.7| ≤ 0.05, and the identity holds to 1e-6 relative. Otherwise **DISAGREES** (report both, find cause before any claim).
- MUTATE M1: 16π² in place of 32π²; M2: drop the portal a. Each must break AGREES.

**Q2 (radiative sensitivity span, my extension).** For M ∈ {10, 100, 1000} and weak-route ε ∈ {1, 1e-3, 1e-6}:
Δ_net = |β_net| ln(M/m_h) / |L − a²/(2B)|, Δ_m = β_m² ln(M/m_h) / m_h². (The span from the mediator scale down to the host scale; astra used a unit log.)
- **UNPROTECTED** if Δ > 10; **MARGINAL** if 1 < Δ ≤ 10; **PROTECTED** if Δ ≤ 1. Reported separately for the quartic and the mass.
- This is a leading-log MS-bar sensitivity, not a pole observable; it says how far the IR value can move relative to the tuned tree value. Not a tuning proof.

**Q3 (classicality of the S2 sector, new to this record).** For L* ∈ {5.75 pc, 24 pc, 1 kpc}; halo M_b = 6e10 M☉, M_c = 5.364 M_b, V_f⁴ = G M_b a₀, r_M = √(G M_b/a₀), t = r_M/V_f, both footings:
(a) g_loop = (l_P/L*)²; (b) g_act = ħ/(M_c V_f² t); (c) g_zp = 3ħc/(64π² L*⁴) / (4 a₀²/G) (zero-point scale of a P mode of mass ħ/(cL*) against ρ_DE c² at κ = ½).
- **NEGLIGIBLE** iff all of (a)–(c) < 1e-30 for every L* and both footings. Otherwise **NOT NEGLIGIBLE** (report which).
- Reading if NEGLIGIBLE: quantum risk sits entirely in the carrier completion and the vacuum energy, not in the galaxy-law sector.

**Q4 (vacuum-energy scale, informative, no verdict).** |V1(0)| at μ = M for m_h = 1 MeV, M ∈ {10, 100, 1000} (partial MS-bar scalar value, scheme-dependent), as log10 of its ratio to ρ_DE c² (4a₀²/G, both footings). Reported as the size of the cancellation any completion must supply. No mechanism claimed.

## Part F — formation
**F1 (independent reproduction).** Rotating-frame quadratic fluctuation operator about Ψ = √I₀ e^{iωt}, χ₀ solving U′(χ₀) + aI₀ = 0 (unique), ω² = 1 + 2LI₀ + aχ₀;
I₀ = s I*, I*(M=100) = 48.989310 (astra's table). Growth rate γ(k) = max Re of the first-order generator on k ∈ [0, 2], step 0.005.
- **AGREES** iff for M = 100: s = 0.1 → |γ_max − 0.04369| ≤ 2e-4 and |k − 0.29| ≤ 0.02; s = 0.5 → |γ_max − 0.07436| ≤ 2e-4 and |k − 0.34| ≤ 0.02; s = 1 and 2 → max γ ≤ 1e-8. Otherwise **DISAGREES**.
- MUTATE M3: set the gyroscopic (ω) coupling to zero; the s = 0.1 growth rate must change by > 10 %.

**F2 (consequence for the repo's own self-interaction window, ESTIMATE).** Compare with CFG725: low-end bracket σ/m ≥ 0.105–0.82 cm²/g (thermalisation), merger bound 0.45–10 cm²/g (fragile; frozen primary 0.708).
- *Gas channel* (free quanta, tree, threshold t = u = 0): same-charge M = −4L + 2a²/B, σ = |M|²/(128π m_h²); opposite-charge M = −4L + a²/(B−4m_h²) + a²/B, σ = |M|²/(64π m_h²). Weak route: L, a² → εL, εa².
- *Lump channel* (fragments of the spinodal): λ_f = 2π/k_s at the fastest-growing k_s of F1 (s = 0.1 and 0.5); lump charge Q_f = n₀ λ_f³ with n₀ = 2ω s I* ; lump radius from Q_f = n* (4π/3) R_f³, n* = 2ω* I*; σ_geo = 4π R_f²; m_f = m_h Q_f. Weak route: n ∝ 1/ε at fixed R_f, so σ/m ∝ ε. Bracket: λ_f × [0.5, 2].
- Output: dimensionless S = (σ/m) m_h³; σ/m in cm²/g at m_h = 1 MeV (1 cm²/g = 0.1 m²/kg); the m_h range (keV–GeV) landing in [0.105, 10] cm²/g. Classes: BELOW (< 0.105), LOW-EDGE (0.105–0.82), ABOVE-LOW (0.82–10), EXCLUDED (> 10).
- This is an order-of-magnitude estimate from the linear scale, not a nonlinear formation result; it is labelled ESTIMATE and carries no pass/fail weight beyond the class.

## Part G — gravity–response coupling
**G1 (reproduction + duality lemma).** Static spatial-gradient background (∂φ = (0, y, 0, 0)).
(a) k-essence scalar L = −F(Y), Y = (∂φ)²: effective metric G^{μν} = F_Y η^{μν} + 2F_YY ∂^μφ ∂^νφ ⇒ longitudinal c_L² = 1 + 2Y F_YY/F_Y = d ln D/d ln E, with D ≡ 2yF_Y and E ≡ y.
(b) nonlinear electrodynamics L(F), F = (E² − B²)/2, B = 0 background: wave with δE ∥ E has v² = L_F/(L_F + E² L_FF) = d ln E/d ln D (D = L_F E); the other polarization has v = 1.
(c) Law: D = g²/(g + a₀) ⇒ c_L² = (2 + x)/(1 + x), v² = (1 + x)/(2 + x), x = g/a₀. Astra's cubic-response cone 2(1 + Cβp)/(1 + 2Cβp).
- **AGREES** iff sympy and numerics give c_L²·v² = 1 identically (1e-12), the law formula holds, and astra's cone formula equals (a) to 1e-12 on a grid. Otherwise **DISAGREES**.
- MUTATE M4: flip the sign of the F_YY term; the astra-cone match and the duality must both break.
- Overlap disclosure: the scalar-cone formula is standard; CFG122 G5.3 / CFG231 treat related gates. No novelty claimed; the exact reciprocal between field-side and source-side attachment is the point.

**G2 (criterion B margin).** A time function dt is compatible with the response cone of a medium moving at v along the gradient iff G^{μν}u_μu_ν < 0, i.e. v² < 1/c_L². With max c_L² from G1, report v_max/c and the margin over the largest speed in the record (Bullet merger 4700 km/s; CFG725).
- **B PASSES** iff v_obs < c/c_L,max. Criterion A (cone inside the light cone) is reported as FAILS if c_L,max > 1. This reconciles astra's "fails common metric-cone requirement" with the owner's criterion B (09-26).

## Part D — dark-energy normalization (bookkeeping only)
**D1.** Hierarchy table: ħa₀/c against m_h c² (1 MeV, 2 MeV); against ρ_DE^{1/4} (2.25 meV and astra's μ_Q = 2.6757 meV); parameter count of astra's a₀ = q_b³/(4πC³βG_lab) and B_eff = Q²/2 + ΔF + <τ>/4 versus the single observed ratio κ.
- **NOT FIXED** is the expected reading (agreeing with astra); it is overturned only if the parameter count shows the family has no free direction after one relation. No numerology; no route from the O6 screen is re-run.

## Outputs and conduct
`argon10_quantum.py`, `argon10_formation.py`, `argon10_gravity.py` → `*.out`, `*_MUTATE.out`; `REPORT.md`; `HANDOFF_TO_ASTRA.md`. Each script prints its gates. A MUTATE that does not bite is reported as such, not rescued. All inputs (constants, astra's quoted numbers) are listed in the scripts. Nothing is downloaded. Compute is seconds and < 0.2 GB; checked no 1024³ run is live before each run.
