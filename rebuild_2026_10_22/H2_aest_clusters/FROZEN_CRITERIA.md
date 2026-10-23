# H2_aest_clusters — FROZEN CRITERIA (before any script or number)

Rules: `rebuild_2026_10_22/BRIEF.md`, `covariant_push_2026_10_22/BRIEF.md`, `doors_push_2026_10_22/BRIEF.md`, `BRIEF_E_AUDIT.md`.
κ = ½ FITTED. Both footings (canonical 9.3603e-11, alt 1.1312e-10 m/s²), never pooled. No dark-matter particle.
Never "theory closed"; never "the data favour the framework". Inputs and classes: `ASSUMPTION_LEDGER.md`.

## Question

F1 (f1803b0256) found A_MID = data / law = 1.68–1.72 (canonical) / 1.54–1.58 (alt) in 326 eRASS1 × KiDS cluster cores, with
OUTER at ~0.87–0.95. Can AeST's quasi-static sector supply the missing lensing in MID (0.46–1.42 Mpc, F1 bins 3–5) without
overshooting OUTER (1.42–3 Mpc, bins 6–7)?

## The model (external theory input, on disk)

VSZ = Verwayen, Skordis & Boehm, arXiv:2304.05134, `main.tex` eqs. (Phi-Orig), (Chi-Orig) [L294–L305]; SZ21 = arXiv:2007.00082
`newRMONDLett.tex` eq. (NT_quasi_Phi) [L362–L379], μ = √(2K₂/(2−K_B)) Q₀:

    ∇²Φ̃ + μ²Φ = 4πG ρ_b ,   ∇·[𝒥′ ∇χ] = ∇²Φ̃ ,   Φ = Φ̃ + χ ,   Ψ = Φ (lensing = dynamics),

at β₀ = 0 (λ_s → ∞) with C1's capped 𝒥, so that in spherical symmetry |∇Φ| = AQUAL_{μ=x/(1+x)}(|∇Φ̃|) exactly (C1 K2).
Spherical form solved here (exact, no linearisation): with M_eff(r) = M_b(r) − (μ²/G)∫₀^r Φ r′² dr′,
Φ′ = sgn(M_eff) · g_AQUAL(G|M_eff|/r², a₀). At μ = 0 this is F1's law exactly.

Zero point. The μ²Φ term makes the value of Φ physical. AeST leaves it as an integration constant (VSZ §"Boundary conditions":
Δ; Mistele+23's per-object chemical potential, record transcription). Parametrised by VSZ's Δ: in the MOND exterior
χ(r) = s[λ + ln(r/r_M)], s = √(G M a₀), r_M = √(G M/a₀), λ = λ_max + Δ, λ_max = (2/3)(1 − ln(3√2/(μ r_M))) (VSZ eq_chioutmax),
M = M_b(< 3 Mpc), imposed on the μ = 0 solution at r = 3 Mpc (Φ = −GM/r + χ there), then integrated with μ from r = 1e-3 Mpc.
**Primary: Δ = 0** (VSZ's fiducial, maximum r_C). **Envelope:** one universal Δ ∈ [−8, +2] step 0.25 — this is a free
constant (rule 1: counted +1 if it is what makes a cell pass).

## Grids

- μ allowed: 0.1, 0.3, 0.5, 0.7, 1.0 Mpc⁻¹. Upper end: SZ21 L382 / VSZ L311 "μ⁻¹ ≳ 1 Mpc" (on disk) = C3's L_eq = √2/μ ≥ 1.41 Mpc.
- μ probes beyond the bound (labelled EXCLUDED, used only to report the μ needed): 1.58 (μ² = 2.5 Mpc⁻², the record's
  transcription of Mistele+23's cluster requirement), 2.0, 3.0 Mpc⁻¹.
- Cells: footing {canonical, alt} × h {0.672, 0.686} on F1's PRIMARY recipe (AQUAL, gas rescaled, β-model G0, f* = 0.20, data
  boost, catalogue miscentring). The A1 boost-clipped primary is also reported.

## Statistic

F1's exactly: A_band = Σ W D / Σ W P over clusters and band bins, jackknife over 30 RA-ordered patches (F1's per-cluster
measurement, read-only from F1's scratch cache `f1_meas.pkl`, sha256 recorded). Z_MID = (A_MID − 1)/σ, Z_OUT = (A_OUT − 1)/σ.

## Checks (script prints `K# PASS|FAIL value threshold`)

- K1 reproduction: at μ = 0 my pipeline gives F1's PRIMARY A_MID and A_OUTER in all 4 cells (2 footings × 2 h) to ≤ 0.01.
- K2 projector: my signed (linear-interpolation) projector + miscentring + binning agrees with F1's log projector at μ = 0,
  per-cluster binned ΔΣ, median |ratio − 1| ≤ 2e-3 and max ≤ 2e-2 in MID/OUTER bins.
- K3 homogeneous Helmholtz: ρ_b = 0, a₀ → Newtonian, Φ(0) = Φ_c gives Φ = Φ_c sin(μr)/(μr) to ≤ 1e-6 relative (r ≤ 10/μ).
- K4 sourced Helmholtz: Newtonian top-hat (a = 0.3 Mpc) against the analytic interior/exterior solution, ≤ 1e-5 relative in Φ′.
- K5 μ → 0: μ = 1e-6 Mpc⁻¹ reproduces the μ = 0 binned prediction to ≤ 1e-6.
- K6 peak RSS < 1 GB.
- `--mutate`: the mass term's sign is flipped (μ² → −μ², Yukawa); K3 and K4 must FAIL. Outputs `*_MUTATE.*`.

## Verdict rule (the four primary cells, both footings; footing split reported, the weaker verdict taken)

A cell **passes** at (μ, Δ) if |Z_MID| ≤ 2 AND Z_OUT ≥ −2 (the model may not exceed the OUTER data by more than 2σ) AND the
galaxy-RAR guard holds: an isolated Hernquist galaxy, M_b = 1e11 M☉, a_h = 3 kpc, solved with the same (μ, Δ) rule, has
|g_AeST/g_law − 1| ≤ 0.10 for all r ≤ 200 kpc (VSZ L765 "r_C larger than the virial radius of the Milky Way (~200 kpc)").

- **AeST CAN SUPPLY IT**: all four cells pass at Δ = 0 for some allowed μ ≤ 1 Mpc⁻¹ (report μ and margins).
- **CAN ONLY WITH A FITTED ZERO POINT**: fails at Δ = 0, but one universal Δ passes all four cells at some allowed μ
  (report Δ, μ; counted as +1 fitted constant; not a cure under rebuild rule 4).
- **CANNOT**: no allowed (μ, Δ) passes all four cells. Report why (too weak / wrong shape) with the factor: the best A_MID
  reached while Z_OUT ≥ −2, and the smallest probe μ (if any) at which a cell passes.
- **UNDECIDED**: K1–K5 not all pass, or the cells split such that neither rule above applies; name the missing input.

Separately reported, never graded:
- (b) the dust sector: what is computable without a simulation (hydrostatic identity μ²Φ = −4πG δρ_dust, derived from SZ21
  on disk; the Thomas–Fermi radius π/μ), and the ΛCDM-like branch as an upper-bound context, cited from F1's addendum
  (ΛCDM-PROCESSED, not recomputed); what a native simulation would need.
- Cosmology: the SZ21 L412 relation w₀ = 3H₀²Ω₀/(2(2−K_B)μ²) and its implied μ floor; C2's K_B < 0.078 (BBN) only enters via 2−K_B.
- Mistele+23 weak-lensing bound (μ² ≤ 1 Mpc⁻² to a_b ≥ 1e-13): record transcription only (paper not on disk), flagged.
- Durakovic & Skordis 2023 (arXiv:2312.00889): NOT on disk; only the record's transcription is cited, flagged.

## Script

`h2_aest_clusters.py <F1 scratch cache dir> [--mutate]` → `h2_aest_clusters{,_MUTATE}.out`, `..._results{,_MUTATE}.json`;
ends `H2_AEST_CLUSTERS COMPLETE: N/M checks PASS.`, exit 0 iff all pass. `OMP_NUM_THREADS=1 nice -n 15`, < 1 GB RSS, minutes.

## AMENDMENTS (append-only)

- **A0 (implementation, post-result, no physics change):** the first full run (kept as `h2_aest_clusters_RUN1_rss.out`) failed
  K6 (macOS ru_maxrss 1.116 GB; physical footprint 0.38 GB). The script now holds one h's projection operators at a time and
  hands freed blocks back to the OS between chunks (`malloc_zone_pressure_relief`). Every scan line is byte-identical to RUN1.
- **A1 (POST-RESULT; the frozen verdict is kept and printed first):** the frozen OUTER clause was one-sided (Z_OUT ≥ −2, written
  against an overshoot only). In the oscillatory regime the AeST prediction can go *below* the OUTER data or negative in one
  OUTER bin while the band sum cancels; the frozen rule then passes μ = 0.7, Δ = −0.25 with A_OUT = 1.85 (canonical), i.e. the
  prediction at 54 % of the OUTER data and negative in the 2.07–3 Mpc bin. The brief's target is "outer bins at ~1". A1 adds,
  for every (μ, Δ, cell): (i) two-sided |Z_OUT| ≤ 2; (ii) a profile test over bins 3–7: residual stack
  s_j = Σ_i W_ij (D_ij B_j − P_ij) / Σ_i W_ij, jackknife covariance over the same 30 patches, Hartlap factor (30−5−2)/29,
  pass if χ² ≤ 11.07 (5 bins, p = 0.05); the law's own χ² is printed for scale. A cell passes A1 if it passes the frozen
  conditions and (i) and (ii). A1 verdict uses the frozen wording with "passes" read as "passes A1". Reported only (not graded):
  the force at 1 Mpc around the 1e11 M☉ guard galaxy under the same (μ, Δ).
