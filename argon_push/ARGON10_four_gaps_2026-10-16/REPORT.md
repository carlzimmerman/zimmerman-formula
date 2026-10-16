# ARGON10 RESULT — independent cross-check and extension of astra's four-gap pass (2026-10-16)

**Label.** Astra's quoted numbers on all four gaps **reproduce from independent code with zero disagreements**. Three extensions are new to the record
(S2 is classical; the lump/self-interaction consequence; the exact field-side/source-side cone reciprocal and criterion-B margin). The fourth gap,
**dark-energy normalization, gets no progress** beyond a sharper reason it is not fixed. Nothing here closes any gap. κ = ½ FITTED; footings never pooled;
"cold energy"; its mass is required; not "theory closed".

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (db69ec1a0). **Scripts:** `argon10_quantum.py`, `argon10_formation.py`, `argon10_gravity.py` (seconds, < 0.2 GB each; no 1024³ run was live for any run).
- **MUTATE:** M1 (wrong loop factor), M2 (portal dropped), M3 (gyroscopic coupling off, growth changes 833 %), M4 (F_YY sign flipped) all bite.
- **Source read, not edited:** `sol61_push/closure_particle_bridge_2026_10_16/` (potential, `FOUR_GAP_AUDIT.txt`, `CURRENT.txt`). Astra's numbers were used only as comparison targets.

## Reproduced (independent code)
| quantity | mine | astra |
|---|---|---|
| M=100 net quartic / β_net / β_m²/m² | −0.01 / 0.282730 / 506.707 | −0.01 / 0.28273 / 506.7 |
| μ-derivative of the CW potential vs TrH²/(32π²) | max rel. diff 3.5e-12 (5 points) | identity used |
| ε=1e-6 unit-log shifts (quartic, m²) | 2.8273e-5, 5.0671e-4 | 2.8273e-5, 5.0671e-4 |
| coexistence I*, ω*² for M=1,10,100,1000 | agree to ≤ 3e-7 / 1e-6 relative | table in MEDIATOR report |
| spinodal γ_max, M=100, s=0.1 / 0.5 | 0.04372 @ k 0.285 / 0.07436 @ 0.340 | 0.04369 @ 0.29 / 0.07436 @ 0.34 |
| s = 1, 2 stable on k ∈ [0,2] | max growth ~1e-14 | stable |
| cubic-response cone | 2(1+Cβp)/(1+2Cβp), exact symbolic identity | same |

Not tested: the weak-scaling identity S_ε = S_base/ε, the amplitude kinetic factor Z_f, the exterior-force factor 11, the a₀ = q_b³/(4πC³βG_lab) algebra.

## New results
**Quantum (Q2–Q4).**
- *Q3.* The galaxy-law sector (S2) is classical: gravitational loop parameter (l_P/L*)² ≤ 8.3e-105, ħ/(action of a 6e10 M☉ halo) ≈ 3.4e-102 (canonical) / 3.6e-102 (alt), zero-point scale of a P mode of mass ħ/(cL*) against ρ_DE c² ≤ 2.9e-88 (L* 5.75 pc, 24 pc, 1 kpc; both footings). **NEGLIGIBLE.** All quantum risk sits in the carrier completion and the vacuum energy.
- *Q2.* Leading-log span from M down to m_h, relative to the tuned tree value: at M = 100, unit coupling, the IR quartic can move by 130× its tuned value (−0.01) and the host mass by 2300× itself: **UNPROTECTED** both. Astra's weak route protects both only for ε ≲ 4.3e-4 (M = 100), 8.4e-2 (M = 10), 2.9e-6 (M = 1000); the price is an inventory ∝ 1/ε (×2300 at M = 100, ×3.5e5 at M = 1000).
- *Q4 (informative).* The partial MS-bar scalar vacuum value is 10^36.0 / 10^40.0 / 10^44.0 × ρ_DE c² for M = 10 / 100 / 1000 at m_h = 1 MeV (alt: 35.8 / 39.8 / 43.8). Nothing here supplies a cancellation.

**Formation (F2, estimate; F3, post hoc).**
- Free quanta at M = 100, unit coupling: σ/m = 0.87 (same charge) / 1.9 (opposite charge) cm²/g at m_h = 1 MeV, inside the repo's self-interaction window (CFG725) for m_h ≈ 0.44–2.0 MeV. In the weak route this falls as ε² (8.7e-7 at ε = 1e-3): collisionless.
- Spinodal lumps (λ_f = 2π/k_s = 22 m_h⁻¹, R_f ≈ 6.6 m_h⁻¹, Q_f ≈ 1.0e5/ε): σ/m ≈ 1.2e3 ε cm²/g (s = 0.1; 8.6e2 ε for s = 0.5) at m_h = 1 MeV, ×(MeV/m_h)³ and ×[0.5, 2] for λ_f. At unit coupling that is EXCLUDED; it falls into the window only through ε.
- *F3 (not frozen).* At each M's protection limit, the lumps land in [0.105, 10] cm²/g for m_h ≈ 4.7–21 MeV (M = 10), 0.37–1.7 MeV (M = 100), 32–147 keV (M = 1000). m_h is free, so this is a relation between ε and m_h, not a constraint on ε; but a 2 MeV carrier at M = 100 sits at or just beyond the upper edge (1.7 MeV nominal; about 2.1 MeV at the generous λ_f bracket).

**Gravity–response (G1–G2).**
- For one static law D(E), the field-side attachment (nonlinearity in the potential gradient: scalar, AQUAL-type) and the source-side attachment (nonlinearity in D: electrodynamic-type L(F)) have **exactly reciprocal characteristic speeds**: c_L² = d ln D/d ln E and v² = d ln E/d ln D, so c_L² v² = 1 for any D(E) (sympy; checked also by linearising both field equations).
- For the repo's law D = g²/(g + a₀): c_L² = (2+x)/(1+x) ∈ (1, 2] (superluminal everywhere), v² = (1+x)/(2+x) ∈ [½, 1) (subluminal everywhere).
- *G2.* A common time function exists iff the medium speed obeys v < c/c_L,max = 0.707 c = 2.1e5 km/s. The largest speed in the record (Bullet merger, 4700 km/s) is 45× inside. So astra's "fails common metric-cone requirement" is **criterion A (strict); the owner's criterion B (09-26) holds with margin**.

**Dark-energy normalization (D1): NOT FIXED.** ħa₀/c = 2.06e-34 eV (canonical; 2.48e-34 alt) is 2.1e-40 of an MeV carrier mass; any derivation must let the Hubble scale enter, i.e. cosmological boundary or flux data. Counting parameters (q_b, C, β, G_lab; Q, ΔF, ⟨τ⟩) against the one observed ratio leaves ≥ 6 free directions; astra's (Q, ΔF) = (1, 2.5) vs (2, 1) degeneracy is an explicit example. No route was re-run; no numerology.

## What this does not show
- Q2 is a leading-log MS-bar sensitivity, not a pole observable or a proof of tuning; finite threshold matching is not computed.
- F2/F3 use the linear spinodal scale, hard-sphere cross-sections and a coherent charged initial state (an INPUT in astra's own report). Nonlinear fragmentation, merging and the lump size distribution would change σ/m.
- G: the source-side (D-side) attachment is subluminal at the characteristic level only. Its sign (a vector medium repels like charges), lensing/metric coupling and hyperbolic health with a dynamical medium are not established; astra's cone result for the scalar attachment stands.
- Nothing touches the frozen 10-14 theory, the sealed predictions, or any observation.

## Disclosures
- Two scratch calculations (β at M = 100; spinodal spectrum at M = 100) were run to settle definitions before freezing; thresholds are astra's own gates or round numbers.
- A unit-print bug in the informative D1 line (ρ_DE^{1/4} printed as 0.000 meV; true 2.24 meV) was fixed before anything was committed. MUTATE outputs are written per mutation (`_MUTATE_M1`, `_M2`, `_M3`, `_M4`).
- The first-principles linearisation check in G1 and the F3 block were added after the freeze; the first tightens a gate, the second carries no verdict. The elimination in the electrodynamic linearisation is short and was done by hand, then encoded.
- Overlap: the scalar cone formula is standard and CFG122 G5.3 / CFG231 treat related gates; no novelty is claimed for it.
