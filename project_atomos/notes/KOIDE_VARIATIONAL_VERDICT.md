# The Koide Variational / Fixed-Point Door — VERDICT: NULL (the last door, closed)

**Date:** 2026-06-25
**Task:** The circularity theorem proved "force r=√2" ≡ "assume Q=2/3" (any DIRECT forcing is the
167th re-labeling). The opening it left: an *independent* principle — defined WITHOUT mentioning
Koide / 2/3 / r=√2 / cos²=3/4 — whose **extremum / fixed-point / stable configuration** LANDS the
charged-lepton √-mass vector at the 45° (r=√2) configuration would be non-circular, exactly as
gravity forces √(8π/3) for ITS OWN reasons independent of the observed a₀. Four candidate
independent principles tested.

## VERDICT: NULL — all-smuggle-or-null. No route survives.

Across four genuinely-distinct independent principles (S3/A4 flavor potential, entropy/information
extremum, IR-RG/flavor-gauge fixed point, marginal-stability/special-geometry), **none** has its
extremum/fixed-point at r=√2 from independent ingredients. Every apparent hit either (a) smuggles
2/3 through the privileged choice of variable, (b) requires codimension-2 coupling tuning, (c) is
structurally obstructed at renormalizable level, or (d) is flavor-blind and cross-fermion-falsified
with no derived lepton-specific selector. The framework hosts the **shape** (the S3/triality 1+2
democratic+doublet decomposition Koide needs) but **no dynamics forces the amplitude** r. The
variational door is now closed alongside the dS-Unruh IR loop, the EJA/Dirac normalization, the
equipartition steelman, and the relational exhaustion.

**Independently re-verified this session** (from-scratch sympy/mpmath dps≥40, not trusting the route
scripts' printed conclusions): all four routes' load-bearing claims reproduce.

---

## The unforced content (the entire stake), sympy-exact

Brannen circulant √m_k = M(1 + r·cos(φ + 2πk/3)) gives, **phase-exact** (residual 0, verified
independently at φ = 0, 0.3, 1, 2, 1.7):

    Q = Σm / (Σ√m)² = 1/3 + r²/6 ,   Q = 2/3  ⟺  r = √2  ⟺  cos²(v,(1,1,1)) = 1/2.

In elementary-symmetric invariants Q = (c−2)/c with c = e1²/e2: democratic Q=1/3 ⟺ c=3, biaxial
Q=1/2 ⟺ c=4, **Koide Q=2/3 ⟺ c=6 exactly**, uniaxial Q=1 ⟺ c→∞. "Force Koide" = "force c=6" =
"force r=√2." All routes must produce c=6 / r=√2 from a definition that does NOT contain it.

Cross-fermion (PDG, re-derived): **leptons Q=0.66666 (c=6.000, r=1.4142)**; up Q=0.84898 (c=13.24);
down Q=0.73143 (c=7.45). Only charged leptons sit at the target — any flavor-blind forcing of 45°
is falsified by the quarks.

---

## ROUTE 1 — S3/A4-invariant flavor POTENTIAL. Verdict: no-extremum-there.

Defined purely from S3 invariants e1, q=Σp², c=Σp³, t=p1p2p3 (no 2/3 in any V). The minima of every
natural renormalizable S3-invariant polynomial potential land at **residual-subgroup alignments with
RATIONAL r**: (1,1,1)→r=0 (Q=1/3); (1,1,0)→r=1 (Q=1/2); (0,0,1)→r=2 (Q=1); (1,1,−1)→r=4 (Q=3).
**Re-verified:** on the S2 branch (a,a,b), r=√2 requires the irrational ratio b/a = 4−3√2 =
−0.24264, which imposes **two explicit coupling equations** (a codimension-2 tuned surface in
(m²,L,h,k)) — r drifts continuously through √2 only on a measure-zero surface, not forced. Scanning
the cubic coupling h gives stationary r ∈ {0, 1} only; √2 is never hit generically.

- **Steelman (credited):** the ONE natural invariant whose extremum lands at r=√2 exactly with no
  2/3 in its definition is the degree-0 AM-GM balance ratio f2 = d²s²/q², extremized at d=s
  (Lagrange-verified). **But** it is not a renormalizable potential, its "balance d and s" content
  is logically "set d=s" = "set r=√2" (smuggle), and it is flavor-blind → quark-falsified
  (re-verified: equal-split forces Q=2/3 universally; up at 1.759, down at 1.545).
- **Lepton-specificity: FAILS.** No S3/A4 invariant carries a sector label.

## ROUTE 2 — Entropy / information extremum. Verdict: smuggles-2/3-dead.

Five+ natural info functionals from only v=(√m_k), the masses, the democratic direction, and
standard info quantities (no 2/3/√2/3/4 in any definition). **Re-ran the full script + coordinate
killer test.** Q(r)=1/3+r²/6 is a featureless monotone convex parabola — 2/3 is a generic interior
value, no extremum/inflection. Unconstrained max-ent → r=0 (uniform); constrained max-ent leaves r a
free function of λ (non-diagnostic). Shannon H(p), H(q), Fisher I_F: no stationary point at √2. The
Renyi-2 IPR Σq_k² is **IDENTICALLY Q** (sympy residual 0) → "IPR=1/2" is "Q=2/3" verbatim.

- **The one hit:** F3 = D·(1−D) with D = cos²(v,(1,1,1)) = 1/(3Q) peaks at r=√2 EXACTLY (genuine
  MAX, F3''=−1/4). **Killed by the coordinate-covariance test (re-reproduced):** the argmax of
  g·(1−g) moves off √2 for every other equally-natural [0,1] concentration measure — D²→0.910,
  √D→2.449, exp(−CV²)→1.177, Shannon-H/log3→1.522. Only the pre-privileged g=D=1/(3Q) (whose
  half-value IS Q=2/3) pulls back to √2. The smuggle is the *choice of variable*, not a literal
  token.
- **Lepton-specificity: FAILS** (flavor-blind; quarks off the D(1−D) max).

## ROUTE 3 — IR-RG / flavor-gauge fixed point. Verdict: no-extremum-there.

Three nested versions (SM 1-loop charged-lepton Yukawa RGE; Pendleton-Ross IR fixed ratio; Sumino
gauged-O(3) yukawaon), each defined without 2/3. **Re-ran the full script.** SM Yukawa running shifts
Q by ~1e-4% monotonically, no fixed point at 2/3. Pendleton-Ross fixes the Yukawa LENGTH, not the
DIRECTION/angle Koide encodes.

- **The decisive structural obstruction (independently re-derived from scratch):** for the
  renormalizable O(3) potential V = m²P2 + λ_A P2² + λ_B P4, the gradient factorizes as
  **dV/ds_i = 2s_i(m² + 2λ_A P2 + 2λ_B s_i²) = 0**. Subtracting two stationarity equations gives
  **2λ_B(s_i² − s_j²) = 0** → every nonzero eigenvalue shares s_i² → the nonzero block is **fully
  degenerate**. The only stationary VEV directions are (a,a,a), (a,a,0), (a,0,0), giving Q ∈
  {1/3, 1/2, 1} ONLY. **A stationary VEV with 3 distinct √-masses does not exist at renormalizable
  level** — Q=2/3 (c=6) is structurally UNREACHABLE as a fixed VEV. Sumino pins c=6 by imposing
  condition (34) e2=e1²/6 BY HAND (= the circularity theorem verbatim).
- **Lepton-specificity: FAILS** (a flavor-gauge fixed point is flavor-universal; its symmetric
  attractor is democratic Q=1/3, runaway Q=1; 2/3 is merely transited).

## ROUTE 4 — Marginal stability / special geometry (the genuinely-distinct angle). Verdict: no-extremum-there.

A fixed point can be selected by being **definition-free** intrinsic structure — a positivity
boundary, a symmetry-enhancement (stabilizer/orbit jump), a Hessian zero-mode / bifurcation, a
second-order transition — none of which needs a 2/3 input. **Re-ran r4e + r4d, and independently
re-derived the geometry from scratch.** The intrinsic special points of the circulant flavor
geometry are:

- **r=1** — all-phase positivity boundary (worst cos=−1 → 1−r=0), Q=1/2;
- **r=2** — one √-mass vanishes (phase φ=0: component 1−r/2=0), Q=1, max breaking;
- **r=0** — full S3 (democratic), Q=1/3, the only symmetry-enhancement.

**r=√2 is strictly between 1 and 2, an ordinary interior value.** No stabilizer/orbit jump at √2
(symmetry enhances only at r=0). No Hessian zero / inflection / bifurcation at ANY r — Q''=1/3 and
the shape length P''=1 are constant-positive everywhere. The ONLY sense r=√2 is special is
|std|=|dem| (equal rep-length, |std|²/|dem|²=r²/2=1) — which is **exactly cos²=1/2 = Q=2/3 restated**
(re-labeling).

- **Lepton-specificity: FAILS decisively, with a sharp new falsifier.** QCD-running detuning does
  NOT pull quark Q toward 2/3 (up stays ~0.78–0.85, down ~0.73–0.74 across scales; neither →2/3).
  SO(10) 16-universality would PREDICT quark Koide (false). And the killer: **neutrinos are colorless
  too and are NOT Koide** (Q free in m₁: 0.586 at m₁=0, 0.382 at 0.01 eV, 0.336 at 0.05 eV). So
  "colorless / absence of QCD" cannot be the selector — it would have to distinguish charged-lepton
  from neutrino, which is exactly the un-derived Yukawa structure. Lepton specificity is post-hoc/fit,
  not derived.

---

## SMUGGLE AUDIT (the 168th-re-labeling test) — clean at the definition level

Grep of every route's functional/potential/RGE/geometry **definition** lines: NO literal 2/3 / √2 /
3/4 / "Koide" enters any V, F, D, IPR, RGE, or geometry definition. The only non-comment `sqrt2`
token (route2 L106) is the *comparison target* (`compare to √2`), not a functional input. The 2/3/√2
tokens elsewhere are all a-posteriori labels, `<== sqrt2` flags, and Q=2/3-relabeling traces. The
two subtle smuggles are NOT literal tokens:
- **Route 2 F3:** 2/3 re-enters through the *choice of the variable D=1/(3Q)* whose half-value is
  Q=2/3 — caught by coordinate-covariance (the peak moves under any other measure).
- **Route 1 f2 / Route 3 Sumino (34):** "set d=s" / "impose e2=e1²/6" are logical restatements of
  "set r=√2" / "set c=6" — caught by the AM-GM-is-balance trace and the by-hand condition (34).

Quarantine HELD: a₀ / Z / κ / Koide never asserted derived; 2/3 and r=√2 entered only as the
empirical/algebraic target.

---

## Is 2/3 extremal? NO — the structural heart of the null.

**r=√2 / Q=2/3 / cos²=3/4 is an interior, non-extremal value of every natural shape functional.**
Q(r)=1/3+r²/6 is a featureless monotone convex parabola with constant positive curvature: no
maximum, no minimum (except trivial r=0), no inflection, no bifurcation, no marginal point anywhere.
The intrinsic definition-free special points of the flavor geometry are the **rational** values
r ∈ {0, 1, 2} (democratic / positivity boundary / one-mass-vanishes); r=√2 is the lone **irrational**
interior point, special only as the equal-rep-length / equal-partition point — which IS the Koide
target. No independent principle has its extremum there; every selector that lands at √2 either
privileges the variable whose half-value is 2/3 (Route 2), tunes a codim-2 coupling surface (Route
1), is structurally forbidden at renormalizable level (Route 3), or restates equal-partition (Route
4). **The framework hosts the SHAPE but no dynamics forces the AMPLITUDE.**

---

## Both-ways ledger

- **Not a manufactured deficit (each "it fails" verified as hard as a win):** real exact hits were
  found and traced honestly, not waved off — Route 2's F3=D(1−D) IS a genuine exact maximum at √2;
  Route 1's f2 AM-GM ratio DOES extremize at d=s with zero 2/3 in its definition. Both were killed by
  the same coordinate-covariance / flavor-blindness / structural rigor one would demand of a claimed
  win. The structural obstruction in Route 3 was re-derived from scratch (gradient factorization →
  forced degeneracy), not asserted. The framework genuinely lives in the RIGHT symmetry home
  (S3/triality/O(3) gives the 1+2 democratic+doublet decomposition; democratic Q=1/3 IS a real RG
  attractor; the flow does transit 2/3).
- **Not a manufactured win:** the decisive results are negative and sharp — Q is non-extremal, the
  O(3) yukawaon cannot host a 3-distinct stationary VEV, and the lepton-selection has no derived
  ingredient (neutrinos colorless yet non-Koide). Consistent with the banked KOIDE_DIRAC_BRIDGE
  (167th re-labeling), RELATIONAL_THEOREM (Koide unique but kernel-free), KOIDE_FROM_DSUNRUH
  (four-leg kill), and the cross-fermion falsifier.

**No maximal-re-verification flag** — this is the honest expected null, not a hit.

---

## What it would have taken to survive (for the record)

A genuine non-circular derivation would need: an independent principle (no 2/3/√2/c=6 in its
definition) whose extremum/fixed-point lands at r=√2 **(a)** robustly under coordinate change,
**(b)** without codim-2 tuning, **(c)** allowed by the renormalizable structure (i.e. evading the
O(3)-degeneracy obstruction — e.g. a *non-renormalizable* or *explicitly S3-but-not-O(3)* potential
with a protected 3-distinct VEV), and **(d)** carrying a *derived* charged-lepton-specific ingredient
that splits charged-lepton from neutrino (not just colorless, which neutrinos share). No tested route
clears even one of these cleanly. The structural obstruction (c) and the neutrino falsifier (d) are
the hardest walls.

## Files (verification scripts, all re-run this session)

- Route 1: `opus_48_extended_research/reviews/koide_dsunruh/route1_{geometry,s3_potential,minimize,alignments,continuity,falsify,bothways,verdict}.py`
- Route 2: `.../route2_entropy_extremum.py` + `ROUTE2_ENTROPY_EXTREMUM_VERDICT.md`
- Route 3: `.../route3_flavor_rg_fixedpoint.py`
- Route 4: `.../route4/r4{a,b,c,d,e}_*.py`
- Independent from-scratch re-verification (this session): `/tmp/indep_verify.py`, `/tmp/r4e_indep.py`
- Priors: `project_atomos/notes/{RELATIONAL_THEOREM,KOIDE_DIRAC_BRIDGE}.md`

**The last door (variational / fixed-point / marginal-stability in the FLAVOR sector) is CLOSED.
r=√2 is a free modulus. The SM mass sector stays WALLED.**
