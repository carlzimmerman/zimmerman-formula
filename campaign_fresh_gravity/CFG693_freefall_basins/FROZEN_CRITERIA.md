# CFG693 — the gap: each system reads its own free-fall basin (equivalence principle + merge tree) (frozen criteria)

Block CFG690–699. Written before any CFG693 script or number. Committed alone. κ = ½ fitted; both footings, never pooled; the
cold energy's mass is required; no particle species; not theory closed.

## Why
CFG692: a polarizable vacuum supplies lensing, the ledger and stability, but a medium that reads the local field |g| has an
external-field effect (satellite boost 102 → 6–12). This fails S2 (PAPER44: no-EFE χ² 0.7 vs EFE 99.5; "ownership", no phantom
in a bound satellite, 131.6). CFG48 lists "a covariant definition of the equipotential-enclosed-mass functional" as OPEN.

## The proposed definition (named before scoring)
- **Free-fall potential.** For a system whose centre falls freely along a worldline, Φ_F is the potential in its non-rotating
  free-fall frame: the external field's value and uniform gradient are removed (equivalence principle; in GR, g₀₀ in Fermi
  normal coordinates). The external field enters only through its tidal tensor.
- **Basin.** The system's basin is the largest closed level surface of Φ_F around its minimum, bounded by the first saddle. The
  basins of all systems form a merge tree (Morse theory / watershed segmentation).
- **Reading.** Each tree node contributes its own law response, computed from its own enclosed baryons and Gauss's flux density
  ḡ = 4πG m_b/A over its level surfaces. Responses superpose over nodes. In CFG692 language, the susceptibility at x is set per
  node by ḡ, not by the local |g|.

## Tests
- **T1 (sympy). Equivalence principle ⇒ S2.** A uniform external field contributes zero flux through every closed surface and
  is removed from Φ_F by construction. So a node's ḡ and its boost are independent of a uniform g_e. PASS iff both hold
  symbolically.
- **T2 (sympy). Where the basin ends, against the data's aperture.** SIS satellite (V_s) at radius R in a host with
  ρ_h ∝ R^{−α}. The free-fall saddle along the stretching direction is at r_J with V_s²/r_J = T_h r_J, T_h = (α − 1)GM_h(R)/R³.
  Compare with the density-match radius r_bg (ρ_s(r_bg) = ρ_h(R), Sifón et al.'s definition used by PAPER44).
  - **PASS iff r_J/r_bg = 1 at α = 2** (the deep-law isothermal host). Then the satellite's own boost holds across the whole
    lensing aperture, and the construction reproduces PAPER44's no-EFE fit there, not the excluded ownership model.
  - Report r_J/r_bg as a function of α, and the plain (non-free-fall) static saddle R V_s²/(V_s² + V_h²), to show why the
    equivalence principle is needed.
- **T3 (numbers). The Sun.**
  - Free-fall basin radius r_J = (GM☉/T)^{1/3}, with T = g_ext/R, g_ext = 2.146e-10 m/s² (PAPER44's value), R = 8.18 kpc
    (radial tide of a flat curve).
  - Wide binaries (≤ 0.1 pc) lie inside, so the law applies with the binary's own mass, with no EFE. This is the opposite of
    CFG691's screening.
  - Cassini: the Sun's own node has no quadrupole. The Galaxy node's field at the Sun is smooth, and its tidal quadrupole is
    ~T. PASS iff T < 5.2e-27 s⁻² (the record's Q2 ceiling).
- **T4 (reported). The cost.** A node's contribution ends at its saddle. Report:
  - the jump in the satellite's own phantom acceleration across r_J (as a fraction of g there);
  - the time-jump when two basins merge (a parent node appears).

  Persistence weighting (topological data analysis) is named as the candidate smoothing; it is not built here.

## Verdict
- **THE GAP IS DEFINED** iff T1, T2 (α = 2) and T3 pass: a covariant, origin-free, constant-free "own baryons" functional that
  is EFE-blind, ends at the data's aperture, and clears Cassini.
- This is a definition, not a derived action. R0 is unchanged: it supplies the switch, not the law. B1 (from an action) and M1a
  stay open. Momentum: the functional depends only on Φ_F and ρ_b, so it is translation-invariant. Conservation then follows
  from Noether if an action is built from it; that is not done here.

## MUTATE (`CFG693_MUTATE=1`, exit 1 iff all bite)
- **M1:** plain static potential (no free-fall subtraction). T1 must fail (ḡ or the basin depends on g_e), and the T2 ratio at
  α = 2 must be ≠ 1.
- **M2:** read the local |g| instead of ḡ. T1 must fail.
