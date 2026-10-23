# Z1_successor_design — FROZEN CRITERIA (committed alone with ASSUMPTION_LEDGER.md, before any script or number)

Lane `rebuild_2026_10_22/Z1_successor_design/`. Written 2026-10-23 at HEAD 00b0e13d0b. Rules: `rebuild_2026_10_22/BRIEF.md`
and `doors_push_2026_10_22/BRIEF.md`. κ = ½ FITTED. Footings a₀ = 9.3603e-11 (canonical) and 1.1312e-10 m/s² (alt),
reported separately, never pooled. No dark-matter particle (the cold sector is cold energy, a field or medium). Never
"theory closed"; never "the data favour the framework". Fix-forward only. No personal names or home paths.

## 0. The question

Find or construct the minimal covariant theory that meets every verified constraint at once. Every flavor scored so far
fails a structural test. This lane does design work: a requirements matrix, a family scorecard, one design, and a frozen
test plan. It runs no data pipeline and no simulation. Only sympy and small numerics (< 1 GB, one thread, `nice`).

## 1. Deliverables and their pass lines

### 1a. Requirements matrix (`REQUIREMENTS_MATRIX.md`)
- One row per hard constraint, each with its number and an evidence pointer `file:line` into a verified lane (a lane
  the coordinator reran or reproduced, per `covariant_push_2026_10_22/THEORY_V3_DRAFT.md` or
  `rebuild_2026_10_22/X0_explanation_map/MAP.md` §4).
- It must contain at least these 13 rows: GW speed; healthy, well-posed DOF (H4, I1, X3, the v3 algebra review); the
  n = 1 law / SPARC RAR, MeerKAT a₀, groups (P4); Solar-System screening (D7c, D7d, C6); outer globulars (D10); WB
  pending DR4; MW vertical force and outer slope (P4, S3, X5); TDGs and DF2/DF4 Newtonian (U1); satellites and Coma
  UDGs (S1, U1, X1); cluster cores (F1, S4, X2); linear growth within 5 % of dust, and BBN (F3, M1, Q6, Q7, X4); CMB
  TT/TE/EE (Q6, Q7); no isocurvature from the cold-sector origin (X1_seedfree_abundance); a₀ = κc√(Gρ_Λ).
- A **tension list**: each pair of rows that no single known mechanism meets together, with the theorem or lane that
  shows it.
- Pass line: every row has a number and a pointer. A row without one is marked `NO VERIFIED NUMBER` and is not used to
  rank anything.

### 1b. Family scorecard (`FAMILY_SCORES.md`)
- Families: v3 (and v3s, v3 with the switched stiffness of X3); v4 (AeST + γ_L); TeVeS / BIMOND; dipolar dark matter
  (Blanchet–Le Tiec, framed as a cold medium with an internal polarization vector); Codex's P-medium (cite lane Y1; do
  not re-score it); Khoury-type superfluid (a particle: reference only); "MOND from a CDM-like field with an
  environment-dependent phase" (generic).
- Cell classes: PASS / COND / FAIL / OPEN / UNTESTED / N-A. Every cell other than UNTESTED or N-A names its source.
- A cell resting only on literature read here is labelled PROV. A PROV cell is never shown better than COND.
- Key literature equations must be cross-checked by this lane's own sympy (checks K1–K3 below). If a sympy check
  contradicts the literature summary, the sympy result is reported and the cell follows it.

### 1c. Design (`DESIGN.md`)
A design is reported as **PROPOSED (CONDITIONAL)** only if all of D1–D6 hold. Otherwise the lane verdict is
**SCOPED NO-GO** (no design meets the U1 rows with the stated rules), with the obstruction named.
- **D1 static limit.** For an isolated owned system in steady state with the cold supply ≥ the law's demand, the
  design's static equations reduce to v3s's verified leaf equation ∇·[μ(|∇ψ|/a₀)∇ψ] = 4πGρ_b with μ = x/(1+x)
  (sympy residual exactly 0, spherical and planar reductions).
- **D2 linear kernel.** The linear growth kernel of the cold medium on FRW is derived from the design's action.
  Pass: s(k) = 1 for every k (pressureless dust) and δ ∝ a in EdS (sympy, exact).
- **D3 U1 mechanism.** Shown as algebra, not words: (i) an owned unit of baryons M_b and held medium M_h in a uniform
  host field g falls at exactly g (v3: g·M_b/(M_b + M_h)); (ii) medium released from the held state is gravitationally
  bound (specific energy < 0) in the system it leaves; (iii) the held state carries no extra mass beyond the law in an
  isolated system. Each is a sympy identity with residual 0.
- **D4 constants.** The count of fitted or free constants must not exceed v3's (κ, L★, cold abundance, μ_K). Every
  constant or rule added, removed or replaced is listed.
- **D5 honesty.** Every ingredient that is not derived from an action is named and labelled NON-VARIATIONAL.
- **D6 coverage.** Every row of the matrix gets a status for the design: INHERITED (a cited verified lane computed the
  same equation), PREDICTED (a number or sign the design fixes, untested), OPEN, or FAIL.

### 1d. Test plan (`TEST_PLAN.md`)
- Frozen before any test is run. Every matrix row maps to an existing verified pipeline (lane and script) that can
  score it, with its pass/fail line written before any run.
- Order: decisive × cheap first. This lane runs none of them.

## 2. Checks (`z1_successor_design.py`; one line per check, `K<n> PASS|FAIL <value> <threshold>`)

| id | what | pass line |
|---|---|---|
| K1 | Blanchet–Le Tiec (BLT) non-relativistic Lagrangian per unit mass L = ½v² + s·v·ξ̇ + U(x) + ξ·∇U − W(σξ)/σ, with the mixing sign s chosen so the Euler–Lagrange equations reproduce BLT's printed Eqs. (85)–(86) (minus the σ-gradient term) | EL residuals 0 for exactly one sign s; kinetic Hessian of that s has det < 0 (one negative-energy direction) |
| K2 | BLT dielectric matching: W = W₀ + ½W₂Π² + ⅙W₃Π³, W′(Π) = g, χ = −4πGΠ/g | χ = −1 + g/a₀ + O(g²) iff W₂ = 4πG and W₃ = 32π²G²/a₀ (residual 0) |
| K3 | BLT linear sector: (a) the anchor x stays at rest at linear order iff W₂ = 4πG; (b) the variable y = x + ξ is geodesic dust to first order in ξ; (c) the cubic term equals the quadratic one when the polarization's own field 4πGΠ equals a₀ | (a), (b): residual 0; (c): threshold = a₀ exactly |
| K4 | Design static owner limit (D1): spherical and planar reductions of the owner's leaf equation | residual 0 against v3s's AQUAL with μ = x/(1+x) |
| K5 | Capacity split (D3 iii, cluster form): with held = min(demand, supply), the total enclosed mass is M_b + M_ph where supply ≥ demand, and M_b + M_supply where supply < demand; deep-limit supply radius r_s = f_s·r_M | identities, residual 0 |
| K6 | Owned fall rate (D3 i) and absence of a host term in the owner's law argument | a = g exactly (residual 0); v3 control a = g M_b/(M_b+M_h) < g |
| K7 | Release (D3 ii): held medium is at rest in the owner frame; on release its specific energy in the owner's capacity-truncated potential is < 0 | sign proven for every r inside the owner (sympy on the closed-form potential) and checked numerically on a grid for both footings |
| K8 | Linear kernel (D2) from the mimetic-dust action, NR limit | s(k) = 1 ∀k; EdS growing mode δ ∝ a (residual 0) |
| K9 | Retention map (prediction, no data): deep-limit Δlog g = ½ log(M_b,orig/M_b,now) for an owned system that lost baryons after holding | identity, residual 0 |
| K10 | Supply crossing mass M_× (prediction, no data): the baryon mass at which the deep-limit supply radius equals the owner radius, both footings, for each stated radius convention | finite, positive; both footings reported, never pooled |

Lane verdict: the checks are mathematics. A FAIL in K1–K3 changes the dipolar family's cells, not the design. A FAIL in
K4–K9 means D1–D3 are not met and the verdict is SCOPED NO-GO.

## 3. MUTATE

`Z1_MUTATE=1` writes `z1_successor_design_MUTATE.out` and `z1_successor_design_results_MUTATE.json`. It
(i) replaces the owner frame by v3's global foliation (the held medium feels the host's hold, U1 T3), and
(ii) flips the BLT mixing sign. At least K1 and K6 must FAIL under MUTATE; the script exits 1 in MUTATE mode if they do
not.

## 4. Verdict classes for README

`DESIGN PROPOSED (CONDITIONAL)` / `SCOPED NO-GO` / `NOTHING NEW`, followed by the constant count and the first three
decisive tests.

## 5. Stop rules and disclosures

- No knob scans. No new fitted constant may be introduced to make a row pass. Numbers are forecasts from stated inputs,
  never fits to data.
- No downloads. Literature read here via arXiv abstract / ar5iv pages is PROVISIONAL.
- Not blind: while reading the record and designing, the author made hand estimates before this file: a supply-crossing
  baryon mass of order 5e13 M☉ (200ρ_c convention, canonical); supply radii of roughly 0.4 / 0.76 / 1.2 Mpc for X2's
  tercile median gas masses; member-galaxy phantoms of order 5 % of a 1e14 M☉ cluster's law mass; the BLT ghost
  structure; and the retention relation of K9. They are disclosed here and recomputed by the script.
- Y1 (`rebuild_2026_10_22/Y1_pmedium_flavor/`) scores Codex's P-medium. This lane cites Y1 and does not duplicate it.
