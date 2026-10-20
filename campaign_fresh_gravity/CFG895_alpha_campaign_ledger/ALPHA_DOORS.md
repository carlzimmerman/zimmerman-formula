# Untried routes to the fine-structure constant, ranked (CFG895, 2026-10-20)

**None of these is a derivation, and none is expected to be one.** Each door is a computation that can kill a route, or can show that alpha is "allowed, not predicted".

A route is listed only if four things hold:
1. It is not in `ALPHA_ATTEMPTS_LEDGER.md`.
2. It has a stated forced-kernel candidate (kernel classes are defined in `ALPHA_CAMPAIGN_RULES.md` §2).
3. It has a concrete first computation.
4. It is not numerology in disguise.

Only **8 doors** survive that screen. The brief asked for 10–20; rather than pad the list, every idea that failed the screen is in the table "Considered and excluded" with its reason. Numbers marked "by construction" come from `cfg895_check.py`. References marked "recalled" were not opened in this lane, and the door's lane must read them before it freezes anything.

**Ranking criteria, in order:**
1. Kernel class (K1 above K2 above K3).
2. Whether the door can make a joint prediction. Only joint predictions can reach EVIDENCE at today's running precision (rules §4.3, check K9).
3. The precision ceiling.
4. Cost.
5. How distinct it is from the record.

**One structural fact governs everything below.** Any route that predicts the hypercharge coupling at a UV scale reaches alpha(0) through 1/alpha(0) ≈ 41/(24π f) + 1/alpha_2(M_P) + 32.6. Here f is the coefficient multiplying g in the beta function. So d(1/alpha(0))/d ln f = −55.2 at the value needed, and fixing alpha to 1% needs f to 2.5%. Because Y1's running error is 8.8e-4, a single-coupling UV route can reach CONSISTENT at best.

## Summary

| Rank | Door | Kernel | Joint prediction? | Cost | Best grade possible |
|---|---|---|---|---|---|
| 1 | D01: f_g from the fluctuation photon–graviton vertex | K1 | no (g_Y only) | medium | CONSISTENT |
| 2 | D02: A Higgs boundary condition (forced by AS, or MPP/Veltman) solved for g_Y | K1-conditional / K2 | **yes** (alpha with M_W) | low | EVIDENCE |
| 3 | D03: f_g with the record's own matter content | K1 | no | low | CONSISTENT |
| 4 | D04: Unimodular asymptotic safety f_g | K1 | no | low–medium | CONSISTENT |
| 5 | D05: Photon–curvature operators in the AS truncation | K1 | no | medium | CONSISTENT |
| 6 | D06: Einstein–Cartan–Holst (first-order) AS f_g | K1 | no | medium–high | CONSISTENT |
| 7 | D07: Noncommutative-geometry spectral action with a forced cutoff function | K2 | yes (three couplings) | low | expected KILLED (×18–26) |
| 8 | D08: Charged vector boson in dS₄, covariant completion (closes S1) | structural | no | medium | closure only (expected: no selection) |

---

## D01: f_g from the fluctuation photon–graviton vertex (beyond the background-field approximation)

* **Principle.** In asymptotically safe gravity, hypercharge flows to an interacting fixed point that attracts it in the IR, g_Y* = 4π sqrt(6 f_g/41). Its IR value is then fixed once f_g is known. AS1–AS4 computed f_g only in the background-field approximation, where the graviton two-point function stands in for the h–A–A vertex. This door is the record's own "untried rung" (`ALPHA_CHAIN_STATUS.md`, AS section). It is also the open item of the "Fine structure constant with Codex" chat: "f_g from the photon–graviton vertex, noted, not started".
* **Forced kernel (K1).** C(alpha) = 0 is the condition that g_Y sits at the IR-attractive zero of β_gY = −f_g g_Y + (41/6) g_Y³/(16π²). Here f_g is computed from the vertex flow, with a fluctuation Newton coupling g₃ for the AAh vertex and a graviton mass parameter μ_h.
* **Which alpha.** g_Y at the matching scale (M_P; the matching-scale systematic is carried). It is run to alpha(0) with lane B C5's downstream (`B_rg_asymptotic_safety/b3_forced_vs_required.py`) and Y1's error budget.
* **Starting code.**
  * `AS3_fg_cpr_reanchored/as3_gmat.py` and `as3_gcpr.py` supply the heat-kernel and trace machinery and the gates.
  * `AS4_fg_weyl2/as4_common.py` supplies the trace blocks.
  * The f_g = 5g(1 − 8λ)/(36π(1 − 2λ)²) structure is AS3's background result, kept as the reference.
* **First computation.**
  1. Expand the EH + Maxwell action to third order in h around flat space, and derive the h–A–A vertex with sympy.
  2. Derive the flow of the photon anomalous dimension η_A from the vertex. Use the Litim regulator and the gauge fixing of the gate source.
  3. **Gate.** Reproduce a published fluctuation computation of the gravitational contribution to the abelian β function to its printed digits. Candidate (recalled): Christiansen and Eichhorn, arXiv:1702.07724. Also read Eichhorn, Held and Wetterich, arXiv:1711.02949 ("Quantum-gravity predictions for the fine-structure constant", recalled) and compare it with the record's 91–96 before freezing.
  4. Evaluate f_g at the fluctuation fixed point (g, μ_h, g₃) with SM matter, then predict 1/alpha(0).
  5. Report the critical exponent θ_Y = −2f_g as the scheme-robust quantity.
* **Option space.** Two vertex identifications (g₃ = g, "effective universality", or g₃ from its own flow) × two gauges, with one regulator: **K = 4**. The graded trial is picked in the pre-registration (one trial). The other three are reported.
* **By construction.**
  * 137 needs f_g = 0.0098 (a one-loop reconstruction gives 0.009845; the record's downstream gives 0.009805).
  * The background-field values are 0.037–0.048.
  * At AS3's g* = 0.967, the λ that would give 0.0098 is 0.107 or −7.83 (AS3 found −1.22).
* **Ceiling.** Single coupling, so CONSISTENT at best (K9). To be EVIDENCE the hit would also need D02's joint test.
* **Cost.** Medium: 2–5 agent-days of single-core symbolic work, plus reading the gate sources. Downloads need the owner's approval.
* **Distinct because** AS1–AS4 all use the background-field approximation (AS1 pre-registration, line 29), and lane B reproduced Eichhorn–Versteegen's EH computation only.
* **Kill.** The predicted 1/alpha(0) lies outside 137.036 ± (the lane's own declared error), or the gate fails twice.
* **Honest expectation.** As recalled, not checked: the published "effective universality" studies find vertex and background couplings agreeing to tens of percent, not a factor of 4. The likely outcome is another 90–110.

## D02: A Higgs-sector boundary condition solved for the hypercharge, jointly with M_W

* **Principle.** Three variants:
  1. **AS-forced.** In asymptotic safety the Higgs quartic is irrelevant when its gravitational anomalous dimension is positive. Then λ(M_P) ≈ 0 and β_λ(M_P) ≈ 0 are forced by AS rather than chosen. This is the Shaposhnikov–Wetterich mechanism (arXiv:0912.0208, recalled), which predicted m_H ≈ 126 GeV.
  2. **Postulated multiple point principle** (Froggatt–Nielsen, recalled: m_H = 135 ± 9 GeV).
  3. **Veltman condition** (vanishing quadratic divergence, one-loop form 6λ + (9/4)g² + (3/4)g'² − 6y_t² = 0, recalled and to be re-derived).

  Each variant is one or two equations involving g'. With measured m_H, m_t and alpha_s the equations are solved for g_Y. With two equations at M_P, they are solved for (g_Y, g_2) **jointly**, which predicts alpha(0) and M_W together.
* **Forced kernel.** K1 if variant 1 is used and AS with A_λ > 0 is accepted (conditional on the AS scenario). Otherwise K2 (a postulated principle).
* **Which alpha.** g_Y(M_Z), hence alpha(0), from the Y1 run with measured inputs other than alpha.
* **Starting code.** `Y1_running_precision/`: validated 4-loop gauge and 3-loop y_t, λ running from an NNLO-matched boundary, which reproduces Buttazzo's Planck-scale couplings.
* **First computation: a leverage pre-flight** (rules §1.6).
  1. Compute ∂λ(M_P)/∂ ln g_Y and ∂β_λ(M_P)/∂ ln g_Y at fixed measured m_H, m_t, alpha_s and M_W.
  2. Propagate σ(m_t), σ(alpha_s) and σ(m_H) (PDG, cited) into σ(1/alpha(0)).
  3. Declare NON-DIAGNOSTIC and stop if σ(1/alpha(0)) > 1.37 (1%).

  Only after that: solve the pre-registered conditions.
* **Option space.** Variants (a) λ = β_λ = 0 at a common free μ*; (b) λ(M_P) = 0; (c) β_λ(M_P) = 0; (d) the Veltman condition at M_P. Joint pairs are drawn from {(b), (c), (d)}, at the scales {M_P, M_red}. **K ≤ 8**, every member pre-declared.
* **Ceiling.** The joint (g_Y, g_2) version multiplies P values: at Y1 precision P_single ≈ 9e-8 for a joint hit, so EVIDENCE is reachable (K9). Variant 1 is the only route on this list that could ever give EVIDENCE for a K1 kernel.
* **Wall note.** It reads measured SM masses as labelled inputs and derives none. It is a test of a boundary principle, not a reopening of the mass sector.
* **Cost.** Low: CPU seconds with Y1's code, plus about a day to pre-register.
* **Distinct because** B1–B4 tested the gauge-lattice MPP, and U3 and X1 put boundary rules on the gauge couplings only. No Higgs-sector condition has ever been solved for g_Y in the record.
* **Kill.** NON-DIAGNOSTIC on the pre-flight, or the joint prediction misses M_W or alpha(0) by more than its propagated error.
* **Honest expectation.** g' enters β_λ only through (3/8)(g² + g'²)²-type terms, and the m_t uncertainty dominates λ(M_P). The pre-flight will probably declare the single-condition variants NON-DIAGNOSTIC. The joint version is the one worth running.

## D03: f_g with the record's own matter content

* **Principle.** f_g depends on the gravitational fixed point (g*, λ*), and that fixed point depends on the matter content. 137 needs λ* to move from −1.22 to 0.107 or −7.83 (by construction, at fixed g*). The record fixes content beyond the SM in two places:
  * The conditional FS11 swampland door says Λ implies Dirac neutrinos, so 3 ν_R (project_atomos).
  * The canonical theory's dark sector (THEORY_CANONICAL_2026-10-18.md; no DM particle) counts only if it specifies elementary fields.
* **Forced kernel (K1).** As D01, with the content fixed by the record before computing.
* **First computation.**
  1. With AS3's code, compute ∂(g*, λ*, f_g)/∂(N_S, N_D, N_V). This is a diagnostic map and is not graded.
  2. Then grade the pre-declared content sets.
* **Option space.** {SM + 3 ν_R; SM + 3 ν_R + the canonical dark fields, if they are elementary}: **K = 2**. The SM-only set is AS3's reference. No other content is allowed: free content is a knob under X1's zero-knob rule.
* **Ceiling.** CONSISTENT. **Cost.** Low (hours).
* **Distinct because** AS3 and AS4 used SM matter only.
* **Honest expectation.** 3 Weyl fermions are about 7% of the SM's 45, so the shift will be small. The value of the door is that it closes the content loophole and measures the sensitivity.

## D04: Unimodular asymptotic safety

* **Principle.** In unimodular gravity Λ is an integration constant that does not run. That fits the programme's treatment of Λ as given. The graviton sector loses its conformal mode, and AS3 found that only TT gravitons couple to the Maxwell term anyway.
* **Forced kernel (K1).** As D01, in the unimodular theory.
* **By construction (to be confirmed, not assumed).** If the TT-only structure carries over with λ absent, then f_g = 5g*/(36π), and 137 needs g* = 0.222 (AS3's EH + SM value is 0.967).
* **First computation.**
  1. Derive the unimodular EH flow (TT plus transverse vector) and the gravitational contribution to f_g with AS3's machinery.
  2. **Gate:** reproduce a published unimodular fixed point (Eichhorn, arXiv:1301.0879 or 1501.05848, recalled).
  3. Add SM matter and predict 1/alpha(0).
* **Option space.** 2 gauges × 1 regulator: **K = 2**.
* **Ceiling.** CONSISTENT. **Cost.** Low–medium.
* **Distinct because** there is no unimodular lane anywhere in the record.

## D05: Photon–curvature operators in the AS truncation

* **Principle.** AS1–AS4 used minimal Maxwell coupling. Gravity fluctuations induce the dimension-6 operators R F², R_μν F^μα F^ν_α and C_μνρσ F^μν F^ρσ, plus (F²)² and (F F̃)². At an interacting fixed point those operators feed back into η_A and so shift f_g.
* **Forced kernel (K1).** The fixed-point condition in the enlarged truncation.
* **First computation.**
  1. Add the three curvature–F² operators to AS3's truncation and compute their induced fixed-point values (they cannot be set to zero consistently).
  2. Recompute f_g.
  3. Gate on the minimal-coupling limit reproducing AS3 exactly.
* **Option space.** Operator subsets {R F²}, {R F², Ric F F}, {all three}: **K = 3**. The graded trial is "all three".
* **Ceiling.** CONSISTENT. **Cost.** Medium.
* **Distinct because** all four AS lanes use minimal coupling.

## D06: Einstein–Cartan–Holst (first-order) asymptotic safety

* **Principle.** The record's gauge-theory gravity is first-order: MacDowell–Mansouri SO(4,1) in N3. Einstein–Cartan AS with the Immirzi parameter γ has its own fixed point (g*, λ*, γ*), and a different graviton propagator enters f_g. Minimal Maxwell coupling does not see torsion, so any change comes only through the graviton sector.
* **Forced kernel (K1).** As D01, at the Einstein–Cartan fixed point. γ* is fixed by the flow, not chosen.
* **First computation.**
  1. **Gate:** reproduce a published Einstein–Cartan AS fixed point (Daum–Reuter, arXiv:1301.5135; Benedetti–Speziale, arXiv:1104.4028; both recalled).
  2. Compute the graviton contribution to η_A in that propagator.
  3. Predict 1/alpha(0).
* **Option space.** 2 published schemes: **K = 2**.
* **Ceiling.** CONSISTENT. **Cost.** Medium–high (spin-connection fluctuations).
* **Distinct because** AS1–AS4 are metric (second-order) only. Plain MacDowell–Mansouri needs no separate lane: it equals EH + Λ + Gauss–Bonnet, which is topological in 4D, so it gives AS3's f_g (see the excluded table).

## D07: Noncommutative-geometry spectral action with a forced cutoff function

* **Principle.** The spectral action fixes the three gauge couplings at the unification scale as g² f₀/(2π²) = 1/4 (Chamseddine–Connes–Marcolli, hep-th/0610241, recalled). Here f₀ is a moment of the cutoff function. Usually f is free, which is K0. In the "entropy and the spectral action" construction (Chamseddine–Connes–van Suijlekom, arXiv:1809.02944, recalled) f is fixed as the fermionic entropy function, which gives f₀ = h(0) = ln 2 (recalled). That makes f₀ a forced number.
* **Forced kernel (K2).** The spectral action principle together with the entropy identification.
* **By construction.** 1/alpha_unif = 8f₀/π = 1.77 (entropy function) or 2.55 (characteristic function), against 1/alpha_2 ≈ 46.1 at the g_2 = g_3 crossing (one-loop run from Y1's M_P value). That is a miss of **×26 or ×18**. Z1 has already shown that the SM ratio condition fails without new fields.
* **First computation.**
  1. Read both sources and verify the three recalled facts.
  2. Recompute f₀.
  3. Compare with Y1's couplings at the g_2 = g_3 crossing and at the alpha_1 = alpha_2 crossing.
* **Option space.** **K = 2**.
* **Cost.** Low (hours). **Distinct because** the record never tested NCG for alpha; only W1's division algebras are related.
* **Expected.** KILLED by an order of magnitude if the recalled formulas hold. Its value is closing a door that has a genuinely forced cutoff function.

## D08: Charged vector boson in dS₄, covariant completion (closes S1)

* **Principle.** This is the last open item of the horizon route (`ALPHA_PLAIN_SUMMARY.md`, "What is still open"). S1 found no finite renormalised current for the coupled {W_x, W_z} block.
* **First computation.**
  1. Use a covariant regulator (Pauli–Villars or point-splitting) with a Higgs/Goldstone completion (R_ξ gauge).
  2. Obtain the finite σ/H = alpha G_v(μ).
  3. Check the large-μ logarithm against the W running coefficient 7 (g = 2).
* **Option space.** 2 regulators: **K = 2**.
* **Cost.** Medium.
* **Expected.** No selection. AH3's structural theorem applies to any observable that depends on e and E only through eE/H². Its value is closure of the record's last open dS item.

---

## The handoff from the "Fine structure constant with Codex" chat (FSP-010 and FSP-011): what is concrete

| Item | Status | Door? |
|---|---|---|
| f_g from the photon–graviton vertex | noted, not started | **Yes: D01** |
| Handoff item 1: full proton response | FSP-011 (7db7931cf) reduced it to one isoscalar functional N0(μ0). That needs an e = 0 lattice production job: four-point nucleon functions with the same-loop and split-even sea, at least three spacings | A real computation, but **not an alpha door**. The selection equation it feeds has leverage d ln R/d ln alpha = O(5e-4), so it is NON-DIAGNOSTIC by construction (rules §1.6; check K8). A lattice job is the owner's decision. |
| Handoff item 2: smooth-sphere QCD vacuum | open | Same leverage problem. It is physics worth doing only for its own sake. |
| Handoff item 3: joint ratio and selection | open | No selection equation with O(1) alpha leverage exists. The observables with O(1) leverage are isospin-breaking differences (m_n − m_p, the pion splitting), and these have no selection principle except an anthropic one. |
| FSP-011 navigation note | the live STATUS, HANDOFF and HISTORY files still describe FSP-010 | A job for the FSP coordinator, not a door. |

## Considered and excluded

| Idea | Why excluded |
|---|---|
| Spectral dimension d_s → 2 in the UV as the source of the fixed point | Same structure as AS with f = (4 − d_s)/2 = 1: **102× the required 0.0098** (by construction). Pre-killed. |
| Higher f(R) polynomial AS truncations | AS3 showed that f_g depends only on (g*, λ*), because R² drops out (only TT gravitons couple). Polynomial f(R) moves (g*, λ*) by tens of percent (recalled), not the ×4 needed. Deprioritised; this is not a proof. |
| MacDowell–Mansouri SO(4,1) asymptotic safety | Equal to EH + Λ + Gauss–Bonnet, and Gauss–Bonnet is topological in 4D, so it gives AS3's f_g. Already covered. |
| A Λ-term in the gravitational correction to the charge running (Toms type) | Proportional to GΛ ~ 2.85e-122 (AH5's x). N3 found it tied to GΛ. Negligible. |
| Secular graviton corrections to the photon in dS | Proportional to GH² ~ 1e-122 per e-fold. Negligible. |
| Festina Lente / dS charged-mass bounds | An inequality. The electron satisfies it by about 16 orders (m_e²/(√6 e M_P H) = 1.9e16, by construction). No selection. |
| Gravitational positivity and causality bounds with photons | Inequalities on cutoff scales (K3) with no forced saturation. Lane A's class. |
| Coleman big fix / Hartle–Hawking extremum | Covered by I3: the extremum depends on the counterterm scale μ. In AS, Λ is a relevant (free) direction. |
| Chiral (hypercharge) ladder critical coupling | W2's vector alpha_c = 1.0477 is about 140× the Thomson value. Chiral corrections of O(1) cannot bridge that. |
| Gauge-lattice MPP continued (a first-principles U(1) enhancement factor) | The door is closed by B4 (SU(3) FAIL, z +3.6) under the stop rule. |
| Isospin-breaking observables (m_n − m_p, π± − π⁰) as selectors | Their leverage is O(1), but no selection principle exists beyond an anthropic one. Given QCD, they measure alpha. |
| Litim–Sannino gauge-Yukawa asymptotic safety without gravity | Needs new vector-like matter with free masses, which X1's zero-knob rule forbids. |
| Explicit string moduli stabilisation | A landscape distribution, not a value, and out of cost. |
| EDT or CDT lattice gravity with a U(1) field | Out of the compute budget while 1024³ runs are live. |
| The cold-energy medium as a dielectric | FSP-H gives about 1e-78. Negligible. |
| Any new formula or rule search (κ, Z, π, integers, primes, octonion constants) | The budget is spent: 78.6M rule-search trials (A1, A2, atomos). Nothing can be significant (rules §3). |
| Emergence or species counting with N fixed by anomalies | Lanes C, J, N2 and N4 already showed that Λ/μ or the count stays free. |
| dS₂ Schwinger-model criticality (e²/H² = π/4) | N5 found it holds only for an exactly massless fermion. |

## Support items (not doors)

* **S1.** An exact two-loop, threshold-complete map 1/alpha(0)(f) with an error budget, so that every AS door is graded on one map. AS3's systematics are +0.50 at two loops and −1.75 from the matching scale. Cost is low; build it from Y1's code.
* **S2.** Grade the unaudited Singh J₃(O) formula (`project_atomos/notes/KOIDE_DIRAC_BRIDGE.md`) with lane D's checker, so that the ledger's EXT rows are complete.
* **S3.** Owner decision on the public pages that still carry old alpha claims (listed at the end of `ALPHA_ATTEMPTS_LEDGER.md`).
