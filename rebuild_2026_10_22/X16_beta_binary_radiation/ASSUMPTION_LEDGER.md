# X16_beta_binary_radiation: ASSUMPTION LEDGER (committed with FROZEN_CRITERIA.md, before any script or number)

Classes: RAW / FRAMEWORK-NATIVE / SURVEY-CALIBRATION / LCDM-PROCESSED / STANDARD-MOND-MACHINERY / LITERATURE-INPUT, plus
FITTED (κ = ½, L★), ILLUSTRATIVE (round model values, not data), ADOPTED (a posed choice, not derived), ESTIMATE and METHOD.

## A. What the question rests on (the record)

| ingredient | class | where | used here as |
|---|---|---|---|
| v3s action (BS khronon, J_x, K(Q), clock term, W(u), switched stiffness γ_L = KL★²/2) | FRAMEWORK-NATIVE (J_x, stiffness POSTULATED; K(Q) LITERATURE-INPUT via BS24) | V3_FULL_PICTURE §1; THEORY_V3_DRAFT §0–1 | the theory under test |
| C1 operator −βK²/(4K), B = β/(2 + 3β); window β ∈ [1.9935e-6 / 2.1976e-6, 1.0049e-5] (μ_K 0.1), ≤ 1.1168e-4 (μ_K 0.03) | FRAMEWORK-NATIVE record (X14 SYMPY/NUM; upper edge rests on C5's IR-band estimate) | X14 JSON `classes.C1.FT_window`; X15 S0-2 | the completion under test; S0-2 |
| X15's linear unitary-gauge system (GR + P sector + switched stiffness + C1), its dispersion ω² = βk²(M − 1 + ΘL★²k²/2)/(2 + 3β), α₁(k) = −4η(k), α₂(k) = η(η(1+2β) − β)/(β(2 − η)) | FRAMEWORK-NATIVE (SYMPY record, reproduced by the coordinator) | X15 script `lagrangian`, README D1/D2, S0-3 | this lane's starting system (copied with provenance); sensitivity bracket σ1 |
| C8 K7: conservative orbit change ε = (a/L★)² ≤ 3.2e-14 of the double pulsar's precision; "no radiative channel" at β = 0 | FRAMEWORK-NATIVE record (NUM) | C8 README, script L433–461 | S0-4 target; conservative dynamics unchanged |
| P3: double-pulsar π-metric mixing ≤ 2.0e-9 at β = 0; NS radius 12 km in the record | FRAMEWORK-NATIVE record (NUM) | P3 README, JSON | reported context; R_NS |
| Pulsar timing summaries: J0737 0.999963(63); B1913 0.9983(16); J1738 Ṗ_int −25.9(32)e-15 vs GR −27.7e-15; J0348 1.05 ± 0.18; masses, P_b, e | LITERATURE-INPUT, record transcriptions (not re-verified; no download) | ledger L181–189; C8 L436–441; CFG291 L91–98; mi_sign L63–66 | §2 bounds and inputs |
| CFG291's Barausse 2019 transcription (khronometric α₁, α₂ at β_BPS = 0; flux form), Foster 2007 eq. 70, Barausse's s → 0 at α = β_BPS = 0, Yagi PRL "up to 200 %", |Ω/m|_max = 0.3 | LITERATURE-INPUT (record transcription, PROVISIONAL in the record) | CFG291 FROZEN §3, §5 | X-LIT's α₁, α₂; sensitivity brackets σ1–σ3, σX |

## B. This lane's ingredients

| ingredient | class | source |
|---|---|---|
| a₀ = 9.3603e-11 / 1.1312e-10 m/s² | FITTED (κ = ½) | doors BRIEF |
| L★ = 21.682 / 22.849 pc (switched D10 floor) | FITTED | X3 D4 via X14/X15 |
| native H₀ = 67.2 km/s/Mpc (only inside X14's β_max formula) | FRAMEWORK-NATIVE | X14 |
| screened radiation zone: Θ = 1 (D·P > 0), M ∈ {1, 100} isotropic | ADOPTED; M = 100 ILLUSTRATIVE upper value of the Galactic (1 + x)² (the Galactic P background is anisotropic, M_T = 1 + x, M_L = (1 + x)²; treated as an isotropic bracket) | X15 FROZEN §1; P3 erratum (x_e ≈ 1–3) |
| μ_K term and khronon charge transport (ρ_τ) dropped in the radiation system | METHOD (ADOPTED), checked by P-LIN | — |
| general source coupling −ρn − Tψ + J·N (½h_μνT^μν expanded) | METHOD (standard; X15's point-mass coupling is the special case) | X15 §1 |
| TT tensor sector (1/16K)[ḣ² − (∂h)²] + ½h_ijT^ij | METHOD (standard quadratic Einstein–Hilbert in TT gauge), validated by D-GR | — |
| power formula P = (ω/2)∫S†[(𝒢 − 𝒢†)/2i]S d³k/(2π)³ | METHOD (derived in-lane from dE_field/dt = ⟨∫J·Φ̇⟩), validated by D-GR (GR quadrupole) and X-LIT | — |
| binary source at leading order in k·a, conserved for s = 0; virial ∫T^ij = ½Ï_ij; total-momentum CM frame | METHOD (standard effective conserved source: matter + gravitational stress) | — |
| sensitivity coupling: J_eff = Σm_a(1 + s_a)v_a (from −m(γ_rel)dτ, γ_rel = −u·v) | METHOD (Foster/Yagi definition s = −d ln m/d ln γ); s-weighted quadrupole terms bounded with mapped literature coefficients | LITERATURE_MAP L1, L3 |
| NS sensitivities: not computed; brackets σ0–σ3 (σ3 = envelope incl. the P-hedgehog self-energy G m/(c²L★)), σX counterfactual | ADOPTED brackets / ESTIMATE | FROZEN §5 |
| R_NS = 12 km, |Ω/m|_max = 0.3, white-dwarf s = 0 | ILLUSTRATIVE (record values: C8/P3, CFG291) | — |
| Galactic phantom ≤ 1e-21 kg/m³ (P-LIN margin only) | ILLUSTRATIVE (as X15) | — |
| Kepler orbit, FFT harmonics (N = 8192, n ≤ 400) | METHOD, validated by H-PM | — |
| Peters–Mathews f(e) = (1 + 73e²/24 + 37e⁴/96)/(1 − e²)^{7/2}; ⟨1/r⁴⟩ = (1 + e²/2)/(a⁴(1 − e²)^{5/2}) | LITERATURE-INPUT [mem] / record (CFG291 F7, F8) | — |
| V_CM = 369 km/s; w = 369 km/s tilted slice (R2, R3) | ILLUSTRATIVE (CMB dipole) | — |
| G, c, GM☉, T☉, pc, Mpc | RAW constants | as X15 / CFG291 |

## C. Not used

- No survey data, no SURVEY-CALIBRATION, no LCDM-PROCESSED input, no STANDARD-MOND-MACHINERY (no QUMOND, no EFE formula).
  Data enter only as the record's transcribed binary-pulsar summaries.
- No new fitted constant; β is scanned only across X14's frozen window; no knob scan to make anything pass; no simulation;
  no downloads. Record scripts (X15, X14, C8) are executed only as byte-identical, sha-checked copies inside this lane's
  directory; their own directories are not written to.
