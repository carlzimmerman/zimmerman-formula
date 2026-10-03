# Recipe gate audit, 2026-10-03: G0–G12 against the current chassis

Documentary audit. No new calculation, no verdict upgraded. Every verdict below is quoted from a committed record
(STANDING_2026-09-29.md, LEDGER.md, closure_map/GATES_STATUS_2026-09-29.md, the lane READMEs/outputs named). κ = ½ is
FITTED; the cold mass is still required; nothing here says the theory is closed.

## What is being scored

- **The recipe:** `qwen_claude_field_theory/closure_2026/CRISPY_FRIED_CHICKEN_RECIPE.md` §5 (G0–G12), read with its
  2026-09-26 user decisions: the kernel is ν_mono (QUMOND, through the heat filter S = e^{(ξ²/2)Δ}); causality is
  criterion B; Z = 5.7888 is κ = ½ restated; two branches (B-νmono C-H/K and IC28), never pooled; the switch variable
  is "all doors". The recipe's G1 and V1 wording ("μ = 1 − e^{−y}") is superseded by the ν_mono decision; G1 is read
  with ν_mono below.
- **The current chassis:** the ungated filtered C-H/K khronon (L340, 9ea5ab2c6): GR + α_c a·a − c₂K² with β = 0,
  α_c ∈ [9.6e-14, 3.2e-9], c₂ = λ_K − 1 ∈ [7.29e-3, 0.0667], the leaf-average λ-term (L350 G5), ν_mono, ξ ≥ 0.031 pc
  (canonical) / 0.045 pc (alt).
- **Candidate B** = the law + ownership + the cold component. No committed action produces B (GATES 5.01 FAIL / OPEN).
  So a chassis pass is a pass for the chassis, not for B; B's population rows are effective-law results.

## Same cell ≠ same model: results that do NOT transfer to the chassis

- The recipe's §9 table (G3/G6/G7 PASS, G8 OPEN) belongs to the khronometric + MOND candidate with η = 2e^{−y}, which
  died 09-01 (FC-KH). Historical only.
- XR25 (pulsars, PPN, compact objects) and XR26 (CMB, BBN) score the derivation chain's FP14 core: c₂ → ∞ (CMC
  multiplier), an AQUAL-type scalar, FP13's separator and a dark field. Different action; none of its passes or fails
  transfer. FP2 and FP5 in the same directory ARE rooted in the ungated C-H/K core and are used below.
- DE1–DE3's growth/KiDS/forest passes use a prescribed vacuum gate; DE12/DE13 find that gate unstable as an action,
  and the V0 region gate is obstructed when varied (GATES 5.02). Those passes are not chassis passes.
- GATES §1–§3 rows (SPARC, clusters, KiDS isolated lenses, CMB "met by construction") are candidate B's effective law.

## Gate table

| gate | recipe requirement (one line) | recorded verdict (lane, commit) | for which model | what would move it |
|---|---|---|---|---|
| **G0** | Structural order: put Φ → εΦ and order every source; different orders cannot cancel | **NOT RUN** on the chassis. The record's G0 kill (a9261161) is for an older auxiliary carrier. | none for the chassis | Order every chassis term under Φ → εΦ: the C-H constitutive term, δS (the filter's metric variation), the leaf average, the khronon |
| **G1** | Exact MOND reduction over the full MOND domain (now ν_mono, QUMOND, filtered) | Static chassis inherits C-H's static solutions exactly (L340 H5 PASS). SPARC RAR PASS, 0.1003 dex, RE-RUN-CLEAN (GATES 1.01). Derivation from the assembled action (gate + region kernel): **ORPHANED** (XR3 row 1(b)). B: 5.01 FAIL / OPEN. | chassis static sector: yes; B: no action | Derive the quasistatic law from one assembled action; settle the C^{1,1} splice (C² variant or a nonsmooth argument; XR3 step 0(b), an owner choice) |
| **G2** | Measured G_N derived; regular recovery with the same G in dynamics, lensing, cosmology | Derived on the ungated chassis: G_N = G/(1 − α_c/2), G_cos = G with the leaf average, growth coupling 1/(1 − α_c/2), no slip (FP2 D1–D3, 24aae971e; KM3 2f7ddacd2). Solar recovery only through the filter: bare ν_mono misses the planetary bound 2894–3620× (CFG185 568107b4f). Assembled action: **orphaned** (GATES 5.09; XR3 row 10). 4.01 passes via ownership (effective law). | ungated chassis | Measured G of the assembled action (region kernel with M = 0 in the Solar System, gate on) |
| **G3** | Tensor sector: Q_T > 0, c_T² = 1 | c_T² = 1/(1 − β) exactly, 1 at β = 0, GR's kinetic term (CFG292 T1, 918b33183; FP2 A3). GATES 5.07: "c_T = 1 in the reduced sector". TT on anisotropic gate-on backgrounds: **ORPHANED (low risk)** (XR3 row 6). | chassis | TT modes on anisotropic MOND backgrounds with the constitutive term and δS |
| **G4** | DOF from an actual Hamiltonian/characteristic analysis | Ungated chassis: **DERIVED** canonical count 2 tensor + 1 khronon scalar, 0 vector, N = 3; heat-filter pairs second class, no extra mode (FP5 G-2a, B1–B2, a26136bc4); same count from the characteristic determinant (CFG292 T1). Assembled action Dirac classification: **ORPHANED** (GATES 5.05; XR3 row 2). | ungated chassis | Spec reading, not a calculation: whether the khronon is the permitted, separately counted clock (I3a). Criterion B supports that reading but does not replace it (XR3 row 2). Then the assembled count |
| **G5** | No ghost, no gradient instability, for every propagating mode | Healthy on Minkowski and on static MOND backgrounds (FP2 C3); khronon kinetic coefficient (2 + 3c₂)/(2c₂) > 0 (FP5 B3); healthy for every field above y* a₀ (FP5 C1). **FAILS** at an open zero-field region, the ungated core's own FRW: α_eff = 2 + α_c > 2, Hadamard ill-posed linearisation; amplitude saturates near y ~ y* (FP5 G-2f, C2–C4). V0 region gate: **FAIL as varied** (GATES 5.02). | chassis (FP5); V0 assembled (5.02) | A nonperturbative treatment of the zero-field background (FP5 C4: FRW "is not a perturbative background"), or a construction that keeps the kernel off there (FP5 C6's priced c_CH = 2(1 − δ) exit, not adopted) |
| (G4/G5 Cauchy) | Criterion B; mixed elliptic–hyperbolic problem well-posed | CFG292: **OPEN under the literal frozen rule, CONDITIONAL by its own §2** (owner decides which stands); strongly hyperbolic in the τ gauge iff α_c > 0, β = 0; criterion B holds and the khronon leaves are forced. CFG294 (e92012b82): **CONDITIONAL, local in time**, A1–A5 assumed. CFG312 (b15bf423c): W ≤ 0 **PASS-WITH-EXCEPTIONS** (extreme GRB jets). | chassis | Prove A1–A5 (paradifferential estimates, constraint propagation); zero-field regions; β ≠ 0 not needed (β = 0) |
| **G6** | Derive Φ, Ψ; MOND dynamics and lensing; target Φ = Ψ | Static leading-order block has equal, independently solved potentials (L340 H5; ACTION.md; called "conditional"); γ = 1 for every C_eff (FP2 B3). GATES 4.03: **NS as derivation**. Assembled action: **ORPHANED** (XR3 row 3). Data side (B, effective): KiDS isolated lenses PASS at x_e = 0.4; KiDS early/late split B-specific failure (STANDING §3); CFG316 NOT DIAGNOSTIC. | chassis static: conditional; B: effective only | Φ, Ψ for nonspherical sources with δS and the region kernel; DES Y3 / HSC Y3 shapes for the split (owner decision) |
| **G7** | γ, β, α₁, α₂, α₃ computed explicitly | Ungated chassis with the C-H sector and filter live: γ = 1, α₃ = 0, α₁, α₂ in closed form, leakage ≤ 1e-11 at bound scales (FP2 B3–B4, L6a/L6c DERIVED); β = γ = 1 at 1PN (KM3). Over the window α₁ ≤ 1.28e-8; α₂'s top edge sits on the pulsar bound **by construction** (CFG291 5f1f07dc2). ζ_i, ξ: documentary (KM3 P4/P6). GATES 4.04: **NS for B**. | chassis | Full PPN of the assembled action (gate on, region kernel M = 0, filtered remainder computed) — XR3 row 4, low risk |
| **G8** | Λ_sc on the actual Solar-System background ≫ E | **Bounded pass at frozen-background decoupling scope**, M_sc ≥ 8.5e8 GeV (XC1, XC3); filter metric variation enters only soft legs (XC6 part 1, abbc58baf). Conditional at full-action scope (GATES 5.03). XC6 part 2 **not done**. | chassis | XC6 part 2: canonical couplings of soft-legged vertices on Sun + Galaxy at ξ = 0.031 pc; quartic contact/exchange with nonlinear U elimination; second metric variation |
| **G9** | Full relativistic matter conservation | GATES 5.06: **NS**. Assembled action: **ORPHANED** (XR3 row 5). For B's gated field the Noether identity is exact but reacts on baryons at 0.55–2.2 of their weight (CFG48 G1). Ungated chassis with minimal S_m[g, ψ]: no committed lane writes the identity. | none for the chassis | Write the generalized Bianchi identity of the ungated chassis including the heat-filter pair and the leaf average's global term |
| **G10** | FLRW, a₀ behaviour, cosmological G, perturbations, growth, CMB/ISW | Ungated chassis: **FAILS** linear cosmology, σ₈ = 18–27 (L341, e9f450b10); no linear FRW at zero gradient (FP2 D4; FP5 G-2f). Background is GR's Friedmann equation, c₂ root tension removed at linear order by the leaf average (FP2 D1–D2). Plain −c₂K² c₂ window excluded by Planck-era caps (L350). With the prescribed gate: growth, KiDS, forest restored (L359, DE2), but the gate is unstable as an action (DE12/13). GATES 5.10: **partial**. B: CMB "met by construction", growth "met by allowance". | chassis: FAIL; gated: prescribed only | A varied, stable switch on FRW at the actual B (XR3 row 8 (a)–(c), orphaned); the dark state at action level (5.11 OPEN) |
| **G11** | Compact objects, BHs, caustics | **CONDITIONAL** (CFG318, 91a1a7bcb): static BHs regular outside the horizon, margins ≥ 4.9e7; condition = Ramos & Barausse 2019 moving BHs (read as a proof for all α > 0 it would be KILL; owner's call). Pulsars: **PASS at the stated scope** (CFG311, 3303c9341; margin 4.9e5). | chassis | CFG319 (moving BHs), running — excluded from the ranking |
| **G12** | Is the screening relation technically stable or fine-tuned? | **NOT RUN.** XC1 lists "loops and naturalness (G12)" as not covered. No lane on the record. | none | A radiative-stability lane (below) |

### Two wording flags found in the audit (not corrected here)

1. `closure_map/status_picture_2026_10_03.py` draws "Gravity waves at light speed" and "Equations well-posed (high freq.)"
   as PASS with "CFG292". CFG292's recorded status is OPEN (literal frozen rule) / CONDITIONAL (its own §2), owner to
   decide (STANDING line 560). The c_T = 1 algebra itself is exact (T1; FP2 A3), but the tile cites a lane whose verdict is
   not PASS. Similarly "Solar-system PPN PASS · CFG291": CFG291 scores α₁, α₂ only; γ, α₃ come from FP2, β from KM3.
2. GATES 5.05 "N_grav = 2 orphaned" refers to the assembled action; the ungated count (FP5 G-2a, N = 3) is derived but
   not cited there. The open part is the spec reading of the khronon as a clock, not the count.

## Ranking: gates that are NOT RUN, or OPEN and runnable offline now

Excluded: G11 (CFG319 running). Excluded as needing an owner decision or data: the khronon-as-clock reading (G4), the
CFG292 reading, the C² splice choice, DES Y3 / HSC Y3 shapes (G6 data), a new gate architecture (G10).

| rank | gate | why this rank |
|---|---|---|
| 1 | **G12** naturalness and Lorentz-violation percolation | The only gate with no record at all. It can exclude part of the window: the chassis has c₂ ~ 1e-2 of gravitational Lorentz violation, and loops can feed that into matter, where bounds are far tighter. A loss here constrains every other pass. |
| 2 | **G5/G10** nonlinear evolution around an open zero-field region | FP5 records the chassis's own FRW linearisation as Hadamard ill-posed, but saturating near y*. Whether the nonlinear problem is well-posed there decides whether the ungated chassis has a cosmological Cauchy problem at all. CFG294 explicitly left this out. |
| 3 | **G8** full strong coupling (XC6 part 2) | The recipe's historical make-or-break. It holds only at decoupling scope. Part 2 is fully specified and offline, and could lower M_sc through the canonical dimensions of the hard legs. |
| 4 | **G9 + G0** chassis Bianchi identity and structural order | Both never run on the chassis. One sympy lane can cover both. Likely benign for minimal coupling, but the leaf average's global term and δS have not been checked. |
| 5 | **G6** Φ = Ψ with δS for nonspherical sources | Only the static leading-order block is checked. Low to moderate risk. |
| 6 | **G3** TT on anisotropic MOND backgrounds | Low risk (XR3 row 6). |
| 7 | **G7** remaining PPN (ζ_i, ξ, filtered remainder) on the chassis | Low risk (FP2 already has γ, α₁–α₃). |

## Lane specs for the top three

**1. G12, radiative stability of the chassis window (proposed id: next orchestrator block).**
Inputs come from committed files only: L340's window (α_c, c₂), XC1's M_sc ≥ 8.5e8 GeV as the EFT cutoff, ν_mono's δ = 0.05, and
ξ ≥ 0.031 / 0.045 pc. Freeze criteria first. Part A: one-loop corrections to α_c, c₂ and the ν_mono coefficients
from graviton/khronon loops and from matter loops, by power counting with the cutoff set to M_sc. Is α_c ~ 1e-13–1e-9
technically natural? That means checking whether α_c → 0 enlarges a symmetry, or whether loops generate α_c ~ c₂ (Λ/M_P)².
Part B: Lorentz-violation percolation. Estimate the matter-sector LV induced through gravitational loops, of order c₂ (Λ/M_P)², and compare it
with the strongest SME-type matter bounds. Declare all bound values PROVISIONAL (from memory; no download).
Part C: does the screening relation survive, i.e. is the heat filter's Gaussian stable under loops, or is a ξ-dependent
term generated that un-screens the Solar System? Decision rule: PASS if every window corner is stable within its band;
CONDITIONAL if a stated sub-window survives; FAIL if none does. Controls: reproduce a published Hořava/khronometric
percolation estimate in its α, β, λ → 0 limit; MUTATE with c₂ = 0.5 must fail Part B. Both footings (a₀ enters only
Part C).

**2. G5/G10, nonlinear evolution at an open zero-field region (extends CFG294 and FP5 C2–C4).**
The system is the ungated chassis on a periodic leaf. The background is FRW + Λ + dust with small inhomogeneous perturbations, so ∇Su ≈ 0
over open regions. Freeze criteria first. Step 1: reproduce FP5's linear band (k_max ξ = √ln(C/C*)) and C4's
saturation at y ~ y*. Step 2: evolve the reduced nonlinear system (lapse elliptic, U solved per leaf, khronon hyperbolic)
in 1+1 and 2+1, under at least two resolutions. Test continuous dependence on data, i.e. whether nearby initial data separate by a
bounded factor, and whether the saturated state is resolution-independent. Step 3: report the post-saturation y-distribution and
whether it is the √ε-Osgood failure (XC5 E6) or a regular state. Decision rule: CONDITIONAL if a regular saturated
state with continuous dependence exists for a stated data class; FAIL (KILL-class for the ungated chassis's own
cosmology) if solutions branch or depend discontinuously on data; OPEN if resolution does not converge.
Controls: the GR + dust limit (C → 0) must be well-posed, and the linear regime must match FP5's band. MUTATE: open the
zero-field region with μ_exp's turning kernel; it must fail. Scope: this is not growth or σ₈ (L341 stands).

**3. G8, full strong coupling, XC6 part 2.**
XC6's open list is the spec. (a) Canonically normalise every soft-legged δS vertex on the Sun + Galaxy background at
ξ = 0.031 pc (and 0.045), using D3's soft-leg bound for the derivative factors. Compute each vertex's strong-coupling
scale, including growth through canonical field dimensions with many hard legs. (b) Quartic contact and exchange terms
with U eliminated nonlinearly (XC2's convex leaf solve), not linearly. (c) Bound the second metric variation analytically
rather than sampling it (D4). Freeze criteria first. Decision rule: full-scope PASS if min M_sc over all classes is
≥ 1e3 × the relevant energy (the XC1 convention) at every window corner; CONDITIONAL if this holds only on a sub-window or with a stated
assumption; FAIL if any class falls below. Controls: reproduce XC1's 8.5e8 GeV and Gümrükçüoğlu–Saravani–Sotiriou eq.
15 in the filter-off limit, and XC6 D1's 0.8969 at K = 20. MUTATE with α_c = 0 must fail, as in XC1. Lean
certificates for the scalar inequalities, as XC6 did.

κ = ½ stays FITTED. A chassis pass is never a pass for candidate B, whose action does not exist (5.01).
