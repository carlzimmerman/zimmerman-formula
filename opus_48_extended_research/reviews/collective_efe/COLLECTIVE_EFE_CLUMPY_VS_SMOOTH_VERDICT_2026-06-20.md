# Carl's collective-EFE idea — DISCRETE-clumpy vs SMOOTH total QUMOND phantom — VERDICT (2026-06-20)

**Route 1 ("clumpy_vs_smooth"): real QUMOND/AQUAL computation of whether the overlapping
deep-MOND fields of the member galaxies give the cluster core MORE total phantom (gravitating)
mass than the smooth-baryon cluster-MOND estimate — closing part of the ~30-49% residual with
NO new particle.** Scripts in `collective_efe/`. a0=9.36e-11 (framework, INPUT not derived; quarantine held).

## HEADLINE (both ways, computed not asserted): REDISTRIBUTES-ONLY, mildly SUB-ADDITIVE.
The discrete-clumpy total core phantom does NOT exceed the smooth-baryon estimate. Across four
independent methods the clumpy/smooth ratio of the TOTAL phantom inside the core (420 kpc) is
**0.96-1.00, i.e. ≤1**, converging to 1.000 as resolution rises and as the integration boundary
encloses all the baryons. **Carl's collective effect on the total core gravitating mass is
essentially ZERO and its sign is NEGATIVE (sub-additive), not a positive ADD.** It closes
**0%** (formally ~−1% — the wrong way) of the residual. This is NOT high-priest dismissal: the
enclosed-mass theorem and deep-MOND sub-additivity both KILL it, and the calc confirms both.

## THE FOUR METHODS (all agree)

1. **Spherical enclosed-mass theorem (analytic, exact).** In spherical symmetry
   g=ν(g_N/a0)·g_N with g_N=GM_bar(<r)/r², so M_app(<r)=ν·g_N·r²/G depends ONLY on M_bar(<r).
   Any spherical rearrangement of the same enclosed baryon mass → identical phantom. So a
   collective ADD would have to come from NON-sphericity (discreteness). This is the
   redistribute-only baseline.

2. **N point-clumps vs 1 blob, exact analytic Newtonian field (grid only for the QUMOND div).**
   M_tot=1e13 M☉ split into N=1,8,27,100,300 equal clumps inside ±150 kpc, total phantom
   integrated in a sphere R=800 kpc that ENCLOSES all clumps: phantom = **6.062e13 M☉ for
   every N, identical to 4 significant figures (collective effect = 0.0%, ratio 0.9998-1.0000).**
   Once the boundary encloses all the baryons, clumpiness is invisible to the total phantom.
   (`two_body_subadditivity.py`)

3. **Divergence-theorem (analytic, the WHY).** M_app inside a surface S = (1/4πG)∮ ν(|g_N|/a0)
   g_N·dA. For a sphere enclosing all baryons, the only clumpiness handle is the surface |g_N|
   ANISOTROPY ε (multipoles, suppressed as (r_gal/R)^ℓ). Because ν is CONCAVE in the deep-MOND
   regime (ν~√(a0/g)), **Jensen's inequality fixes the sign NEGATIVE**: anisotropy REDUCES the
   total phantom. Even at an unrealistic ε=0.40 the phantom drops only −0.4%; at the realistic
   core ε~0.15 (from 80 in-core galaxies) it is **−0.06%**, and it averages out over azimuth
   (shot noise, not a systematic). (`divergence_theorem_proof.py`)

4. **Radial cut + realistic gas (the configuration the standard calc actually uses).** Rich-cluster
   core = smooth ICM β-model gas (Mgas(<core)=5.7e12) + 80 discrete member galaxies
   (Mstar,core=9e12, BCG-heavy), vs the SAME mass with galaxies smeared into identical spherical
   M_gal(<r): phantom **discrete 3.36e13 vs smeared 3.49e13 M☉, ratio 0.963 (−3.7%), Δ=−1.28e12 M☉
   = −0.95% of the 1.357e14 residual target.** Converged (cell 9-19 kpc → ratio 0.957→0.968,
   rising toward 1 with resolution) and realization-robust (0.972 ± 0.005 over 5 seeds).
   Cutting the boundary THROUGH the distribution (R=150-250 kpc) makes it MORE sub-additive
   (ratio 0.77-0.95) — the deep-MOND √-law biting. (`realistic_cluster_with_gas.py`,
   `radial_and_intergalaxy.py`, `conv_check.py`)

## WHY (the physics, both ways)
- **The honest pro-Carl piece is real but doesn't add mass:** clumpiness genuinely changes WHERE
  the phantom sits (more concentrated near each galaxy, deficit in the inter-galaxy medium). The
  galaxies DO each reach out with a 1/r deep-MOND field and they DO overlap.
- **But the overlap is SUB-ADDITIVE, not additive:** two masses at distance give a field ~√(2M) <
  2√(M); the phantom density between discrete masses is NEGATIVE (Milgrom 1986) — the overlapping
  fields partially CANCEL between galaxies. The deficit in the inter-galaxy medium exactly offsets
  (slightly over-offsets) the concentration near the galaxies.
- **The TOTAL enclosed phantom is set by the TOTAL enclosed baryonic mass**, the QUMOND
  generalization of the spherical theorem via the divergence theorem: clumpiness only enters
  through the boundary-field anisotropy, which is multipole-suppressed AND Jensen-negative.
- **Is Carl's effect already in the standard cluster-MOND residual calc? YES.** The standard calc
  uses the total baryon M(<r) through the same ν; the discrete-clumpy total phantom is ≤ that, so
  there is no extra clumpy/overlap term it misses. If anything the smooth estimate is a slight
  (~1-4%) OVER-estimate of the discrete reality.

## THE FOUR GATES
- **G1 SUFFICIENCY: FAILS.** Closes 0% of the ~30-49% residual (formally −1%, wrong sign). The
  ~6-7.5e13 M☉ irreducible residual stays at full weight.
- **G2 GALAXY-VETO: SAFE (trivially).** Adds no mass anywhere → cannot break the SPARC RAR. (And
  it is consistent with the banked finding that the residual is GAS-tracking, not galaxy-tracking:
  a collective ADD would have tracked the galaxies, which the data already excludes.)
- **G3 NO-NEW-PARTICLE: satisfied** — it is pure MOND nonlinearity, the framework's own field. But
  with zero net mass it doesn't help.
- **G4 DATA: n/a** — no new observable; the existing gas-tracking core-shape (A2029/RXJ1347)
  already rules out the galaxy-tracking signature a collective ADD would have produced.

## STANDING / RELATION TO BANKED LEDGERS
Confirms FINAL-DOOR item (iv) "EFE on the core — WRONG SIGN" but via a stronger, more complete
argument: not merely "the EFE decreases a member's internal boost" (that is about the members'
internal dynamics) but the COLLECTIVE/total-phantom statement Carl actually asked about — the
overlapping inter-galaxy field sources NO net extra core mass (enclosed-mass theorem + Jensen-
negative sub-additivity). The cluster-core residual stays the shared relativistic-MOND soft-spot.
No third no-particle ingredient here. Quarantine held; both ways honored — Carl's idea was hunted
with a real QUMOND calc (four methods, convergence + realization scatter), not dismissed, and the
null is the computed enclosed-mass theorem, not a manufactured one.

**Key numbers:** clumpy/smooth core-phantom ratio 0.963 (realistic gas+galaxies), 0.972±0.005 (5
seeds), 0.9998-1.0000 (point clumps enclosed), →1.000 as resolution↑; divergence-theorem
anisotropy term −0.06% at realistic ε~0.15, −0.4% at ε=0.40; inter-galaxy phantom sub-additive
(negative). Collective ADD = −1.28e12 M☉ = −0.95% of the 1.357e14 residual target. **Scripts:**
`collective_efe/{two_body_subadditivity,divergence_theorem_proof,radial_and_intergalaxy,realistic_cluster_with_gas,conv_check}.py`.
