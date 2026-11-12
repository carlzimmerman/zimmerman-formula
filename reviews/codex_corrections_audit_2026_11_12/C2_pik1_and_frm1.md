# C2 audit: the uncommitted corrections to PIK1 (pi-gated dust) and FRM1 (formation theory), 2026-11-12

Auditor C2. Read-only on every lane, notice and PAPER72 file. Checks run on copies in a scratch folder.
"Independent" below means my own sympy script or my own SI arithmetic; "reproduced" means I re-ran the notice's own script.

## Verdict table

| item | grade | one line |
|---|---|---|
| PIK1 notice: "universal linear invisibility REFUTED" | CORRECT | The quadratic action gains B alpha div P + (D/2)(div P)^2. PIK1 itself discarded the dQ dPi term as "second order", but that term is what sets the linear equations. Independent 3-D sympy check. |
| PIK1 notice: "universal NO VALUE NOT ESTABLISHED" | CORRECT WITH LIMITS | Right, but mainly for a reason the notice gives only in passing: no frozen row (3-7), no known answer and no Lean file was ever computed. The cluster-ordering argument does not use invisibility, and corrected numbers make it stronger. |
| PIK1 notice: exponential gate has a negative-kinetic band above k^2 = K/D | CORRECT WITH LIMITS | Fixed metric, frozen background, gamma_L = 0, as the notice says. My estimate puts the threshold at k_* = sqrt(2) xi mu_K a^3, so the band is not safely in the ultraviolet (see check 3). |
| PIK1 notice: flat gate (exp(-u^3)) and the stiffness bound | CORRECT | B = D = 0 at FRW. S'' > 0 somewhere for any nonneg, nonincreasing, nonconstant C2 gate (proof checked). The bound on the P block is scoped correctly as "not a ghost theorem". |
| PIK1 notice: r_M misprint (122 / 386 kpc, not 387 / 1220) | CORRECT, INCOMPLETE | The density column is wrong too: 2.6e4 (group) and 2.1e4 (cluster) Msun/kpc^3, not 5.1e3 and 6.5e3. The u ratio cluster/galaxy is about 17, not 5.3. The ordering gets stronger, not weaker. |
| PIK1 pik1.py, pik1_var.py edited in place | REWRITES IN PLACE (recoverable) | Both are now 13-line runpy dispatchers to an UNTRACKED checker. The originals are kept byte-identical in historical_drafts/ (sha256 matches the notice) and in HEAD. No committed outputs existed, so none go stale. |
| corrective RESULT: "runnable replacement for the broken variation draft" | OVERSTATED | check_quadratic.py is a 1-D unitary-gauge quadratic check. It does not redo row 0's C0-C3 (covariant variation against g^mn, tau and P_m; current conservation; leafwise stress). |
| PIK1 RESULT, second notice (CP02 continuation) | NOT CHECKED | Its scope is closure_push_02 (another slice). It says the full constrained calculation "establishes an instability" of the flat-gate family, while CORRECTION_2026_11_12.md says the opposite ("does not prove the full constrained system has a ghost"). The two notices on one file need reconciling before commit. |
| FRM1 notice: ceiling X <= a0/g_bar holds only for fixed profile and f_C <= 1 | CORRECT WITH LIMITS | Algebra checked. The committed text already says "with f_C = 1" (line 84) but generalises in lines 35-36, 196-199 and 205-206, against its own line 24 (merging, f_C > 1). The counterexamples are formal, and the second one is the free-formation-field escape the committed text already reports (lines 90-94). |
| FRM1 notice: class bands are retrospective | CORRECT | DD1's RESULT.md (282ce34e8d, 11-10) prints the per-class offsets. FRM1's criteria (462eaa806d, 11-11 21:34) disclose seeing them and hand-estimate "14 of 16 ... HOLDS EXCEPT". Committed line 195, "predicted 14 of 16 ... before the table was read", is false as written. |
| README / CLOSURE notice paragraphs on PIK1 and FRM1 | CORRECT | They accurately summarise the two corrections and claim no pass, rescue or completed theory. |
| Rule breaches in the new text | none found | No "cold dark matter", no kappa / 5.41 derivation claim, no home paths (manifests also clean), no personal references. |

No notice in this slice claims a pass, a derivation, a rescue or a completed theory. There are no hits to re-grade.

## Decisive checks

**1. Linear invisibility (PIK1 section 4).** The committed proof writes L_K = C(Qbar-1)^2 dPi + O(pert^2) and drops "dQ dPi" as second order. A first-order action term that is a boundary only means the background stays a solution. The linear field equations come from the second-order action. My script (scratch my_quad.py) uses unitary gauge, 3 spatial dimensions, N = 1+alpha, sqrt(h) = e^{3 zeta}, Q = q/N, P^0 = 0 and Pi = (sqrt h)^-1 d_i(sqrt h P^i), with a general gate S - 1 = S1 u + S2 u^2/2. It finds:
- the first-order action has zero Euler operators (it is a boundary, as PIK1 said);
- the second-order action equals B alpha div P + (D/2)(div P)^2 up to a divergence (all Euler residuals 0), with B = C(1-q^2)S'(0)/Pi_c and D = C(q-1)^2 S''(0)/Pi_c^2;
- the Euler operators of that piece are nonzero (lapse: B div P; polarization: -B grad alpha - D grad div P; zeta: 0);
- keeping the mixed term alone fails the comparison.

Shift and traceless metric perturbations cannot enter at this order, because Q sqrt(-g) = q sqrt(h) and Pi sees h only through its determinant. **Result: the gate is invisible at linear order about FRW if and only if S'(0) = S''(0) = 0.** For q != 1, S'(0) != 0 gives B != 0 and S''(0) != 0 gives D != 0. Higher derivatives of S enter only at cubic order. PIK1's theorem therefore holds for flat-origin gates and fails for e^{-u}, (1+u)^{-p} and every gate its own section 6 table names. Its "MK1's row 2 line mu_K >= 2.512e4 stands unchanged" is not established for those gates.

I also reproduced the notice's scripts on copies (sha256 match the notice's table): check_quadratic 27/27, check_finite_density PASS, check_stiffness_bound PASS. legacy_witness fails as intended. The drop-mixed and drop-divergence-square mutations give 4 and 3 FAIL lines respectively.

**2. Dispersion.** I took the principal Lagrangian F'' pi_dot^2/2 - (F'/q)|grad pi|^2/2 + (1-B) pi_dot div P/q - K|P|^2/2 + D(div P)^2/2. Its "1" comes from QX17 action (A)'s P^m A_m with A_i = -d_i pi_dot/q, and its -K|P|^2/2 from the small-p expansion of W. Solving the 2x2 Fourier determinant independently, I get omega^2 = -3/2 at the notice's witness (q 2, C K Pi_c 1, B 3, D 1, k^2 3/2), matching the notice.

**3. Where the exponential-gate band sits (my arithmetic, not a lane; same fixed-metric scope).** MK1's background is q - 1 = I0/(2 mu_K^2 a^3). With Pi_c = xi c^2 rho_d0, K Pi_c = xi I0/2. Then:
- B = 1/(xi a^3) (to leading order);
- k_*^2 = K/D = 2 xi^2 mu_K^2 a^6.

PIK1's own table needs xi of order 1 for the gate to cut the galaxy dust by 1e-9. At mu_K = 2.512e4 per Mpc that puts lambda_* = 2 pi/k_* at about 0.18 kpc today. The threshold falls as a^3 into the past, so near recombination every sub-horizon mode lies above it. There B >> 1, and K_eff stays negative for all k > k_*. The mixing B is order 1 today, not a small correction. This sharpens the notice's point. It is not a coupled-gravity result.

**4. The cluster ordering (PIK1 section 6).** The ordering argument uses the ratio f_S^cl/f_S^gal >= (1.53/1.00)^2 = 2.34, which does not depend on mu_K. It therefore survives the loss of invisibility. In SI (canonical a0):
- r_M is 12.2, 122.0 and 385.9 kpc for 1e11, 1e13 and 1e14 Msun;
- rho_halo is 1.22e3 (galaxy at 730 kpc), 2.61e4 (group at 500 kpc) and 2.06e4 (cluster at 1 Mpc) Msun/kpc^3;
- so u xi is 36, 776 and 614.

The committed table's group and cluster rows look shifted by one mass decade. Corrected, u_cl/u_gal is about 17. Three things weaken a strict proof:
- endpoint ordering does not by itself order mass-weighted means (the notice's point);
- the cluster rows read rho_halo from the data, not from the deep law;
- the galaxy bound must hold at every r out to 1000 kpc and for 1e10 to 1e12 Msun.

Three things support it:
- for self-similar weights (u proportional to r^-2, weight r dr) the u-distributions are scaled copies (density proportional to u^-2 above u_min), so a decreasing S gives f_S^cl < f_S^gal pointwise;
- the binding galaxy is the 1e10 one at 1 Mpc, with u xi of about 6, which is lower still;
- the corrected numbers widen the gap.

My reading: for a decreasing gate the starvation is a strong heuristic, not a graded row. The non-monotone shape failure was asserted, not computed.

**5. What the committed PIK1 label rests on.** Per git, FROZEN_CRITERIA.md, RESULT.md and both scripts were added in ONE commit (f639380e36, 11-11 23:39), which contradicts "committed alone, before any number" on line 3. The committed pik1.py parses but is a 56-line stub that defines constants and nothing else. pik1_var.py has a SyntaxError at line 58. No .out, .json or PIK1.lean was ever made. Known answers KA1 and KA6 are marked PASS "see section 10", and section 10 says nothing was run. Under its own frozen section 3, the label cannot be graded from computed rows. NO VALUE is an analytic reading. As a frozen-criteria grade it is NOT EVALUATED. The correction notices do not mention the single-commit freeze breach.

**6. Script edits.** HEAD's pik1.py and pik1_var.py (sha256 e99c3d2e... and b72b1e91...) are byte-identical to historical_drafts/*.py.txt. Both new dispatchers run the same check_quadratic.py from the untracked research_closure_2026_11_12/. If they were committed without that folder they would fail, and either way they overwrite lane filenames. Recommendation:
- restore both scripts to HEAD;
- add the dispatchers under new names (for example pik1_correction_check.py);
- drop historical_drafts/, because git already holds those bytes.

**7. FRM1.**
- The ceiling algebra is right. With f_C = 1, X = [sqrt(1+4u f_b)-1]/(2 f_b) = 2u/[1+sqrt(1+4u f_b)] <= u.
- Both counterexamples check: sqrt5 - 1 = 1.236 > 1 and (sqrt401 - 1)/2 = 9.51 > 1.
- The first counterexample needs charge supplied from outside. Within a closed union of pieces, each formed at its own field, the merged X is bounded by the pieces' own X. So the counterexample shows a missing hypothesis, not a viable channel.
- Commit order: criteria 462eaa806d (21:34), amendment fed1bc94a4 (21:37), script and outputs b414a1d1d8 (21:58), result 04f69b8b6f (22:01). The freeze chronology against FRM1's own numbers holds. The bands were still set with DD1's class offsets in view: DD1's RESULT lines 73-74 give X-COP +0.57/+0.48/+0.50 and the ultra-faints +0.51/+0.60/+0.59, and the criteria hand-estimate the outcome.
- The headline HOLDS EXCEPT exists only after F2(a) was voided post hoc. The clause is unsatisfiable: 3 se = 1.03 dex against a floor at -0.84. Voiding it is reasonable, but the frozen-line label is FAILS / FAILS.
- What is left: F1 and F5 hold; F2 holds only under the amended clause; F3's 14/16 (alt 13/16) is retrospective consistency; F4 fails.
- The cluster excess over the restricted ceiling (canonical LOCO: X-COP +0.50 against +0.32, CLASH +0.55 against +0.23) stands. Note that committed line 214 quotes "+0.18 to +0.25 dex", which mixes the miss against the band with the miss against the ceiling; CLASH sits 0.33 dex above its ceiling.
- The notice touched only RESULT.md. frm1.py, the JSON files and the Lean files are unchanged.

## PAPER72 recommendations

**Open item 3 (PIK1, line 162)**, once the notice is committed:
"Version 1.2: a dust term gated on the law's own halo density (PIK1) reads NO VALUE on both footings as committed, from an analytic argument; none of its frozen rows was computed. A forward correction shows that its linear-invisibility step fails. About FRW the gate adds B alpha div P + (D/2)(div P)^2, with B proportional to S'(0) and D to S''(0), so it is invisible at linear order only for gates flat at the origin. For other gates the 2.51e4 per Mpc growth line does not carry over unchanged, and for S = e^{-u} a fixed-metric calculation finds a negative-kinetic band. NO VALUE is therefore not established. For a decreasing gate the cluster-starvation ordering remains a heuristic, not a graded row."
If the notice is withdrawn, keep the committed sentence, but add "no row was computed".

**Section 8.2 (FRM1, line 249)**, once the notice is committed:
"FRM1 reads FAILS on both footings on its frozen line, and HOLDS EXCEPT after voiding one clause that no data could satisfy. Its 14 of 16 (alt 13 of 16) class bands were set after DD1's per-class offsets had been seen, so they are retrospective consistency, not predictions. Its cluster ceiling X <= a0/g_bar holds for baryon loss at a fixed profile with no incoming charge. X-COP (+0.50) and CLASH (+0.55) sit above it (+0.32, +0.23; canonical, LOCO). The reading awaits an independent re-grade."
Drop "predicted ... before the table was read" anywhere it is echoed.

## Not checked

- The CP02 (closure_push_02) claims carried in PIK1's first notice and in CLOSURE.md.
- The full coupled metric-clock-polarization spectrum (nobody has computed it).
- Any numeric X-COP, KiDS or SPARC row with the gate.
- FRM1's frm1.py numbers (not re-run; the notice does not dispute them).
- The alt-footing ceilings.
- research_closure_2026_11_12/combined_route/CORRECTIONS.md beyond its three PIK1/FRM1 rows.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
