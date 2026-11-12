# Euclid/DESI continuation: substantive advances and the next decisive tests

12 November 2026. Continues the user-authorized release review and aggressive research search. Read this before treating any individual new calculation as a complete theory or a data pass. The first-phase [release/paper inventory and prior-prediction audit](../euclid_desi_release_review/HANDOFF.md) remains the source for what Euclid and DESI actually released. This phase develops consequences of those findings; it does not add a measured Euclid acceleration residual.

## What changed

The strongest theoretical lead is an explicit changed interpolation kernel that evades a known kinetic mixing failure on a declared background class. The strongest observational lead is an acceleration/gas quotient with a useful exact nuisance cancellation. These are separate partial results: the numerical observation-design calculations use the old simple-mu algebraic surrogate, while the candidate changes the force law and contains screening operators. Combining their successes would not establish one consistent theory.

### 1. A concrete way past the old kinetic obstruction

The proposed kernel is

    mu_*(x) = 1 - 1/sqrt(1+2x),
    a0² = kappa² G (X+V),
    X = -(partial phi)²/2.

Its deep limit retains mu~x. On exact homogeneous FRW, X+V is the canonical scalar density. Away from FRW this bare scalar function is not automatically the complete interacting dark-sector stress density. The coefficient kappa remains an input.

For an aligned timelike rolling scalar, the author and independent reviewer derive

    K_lock = 1 + epsilon [h - eta (p²/d - xp)/2],
    epsilon = kappa²/(8 pi), eta = 1+w,
    p=f', d=f'', h=2f-xf'.

The slow kernel has d>0 and the exact sufficient bound eta<=50/81 implies K_lock>=1 for every x>=0. Negative definiteness of the declared lapse/polarization constraint block then gives positive physical kinetic energy for both coupled modes at all propagation angles, for x>0. The khronon velocity is retained; this does not repeat CT13's erroneous static-clock reduction.

This is **a theorem about the specified leading post-Newtonian block**, with aligned scalar background and stated density/stiffness signs. It is not full finite-wavelength or covariant health. The x=0 clock limit is separate. Local scalar alignment, finite-potential/lapse/metric terms, sign interfaces, screened backgrounds, observational force shapes and cosmological perturbations remain obligations. A fast mode also lies outside the metric light cone in the specified unscreened limit; preferred-foliation causality and strong coupling remain open.

The price is a slower Newtonian tail. Its unscreened Solar correction is about 5e-7 m/s² at 1 AU, so a successful screened solution is essential. Physical Solar acceleration cannot simply be substituted for the screened khronon acceleration. Neither an automatic Solar rejection nor an inherited old Solar pass is justified. The accepted finite run corroborates the matrix algebra with 1,080 fixtures at 80 decimal digits and controls reproducing old and out-of-domain failures. Twenty-four frozen-force scalar-response solves are only toy sensitivity checks; they do not solve the coupled screening problem. [Exact action and scoped result](theory/THEORY_CHECKPOINT.md), [finite results and reproducibility](theory/RESULT.md), [independent derivation](theory/THEORY_INDEPENDENT_AUDIT.md).

The prior repository already contains CT7 potential coupling, CT10's X+V idea, CT14's coupled kinetic failure, separate-cuscuton attempts and a September cubic-polarization slow tail. Those ideas are not newly claimed here. A repository-wide textual search found no exact 50/81/kernel result, but that is bounded search evidence, not a global novelty theorem. The new contribution is the explicit changed kernel's scoped coupled-kinetic escape and its stated cost. It does not restore any retired theory or overwrite any earlier failure.

### 2. A better observable, with a sharply identified information shortage

For the fixed-geometry, scale-free algebraic force model, define

    T = D_A a0, A_gas = D_A gamma_gas,
    S = T/A_gas = a0/gamma_gas.

Multiplying the stellar coefficient, gas coefficient and T by the same lambda rescales intrinsic velocity squared by lambda. Compensating the velocity projection with sin(i)/sqrt(lambda) preserves the observed curve. S is invariant independently for each galaxy. If relative gas conversion is calibrated, S(z)/S(z_ref) measures a0(z)/a0(z_ref) without assigning absolute distance, sound horizon or global stellar M/L.

This exact cancellation does not remove inclination-dependent deprojection, arbitrary gas/stellar radial profiles, pressure, warps or external fields. A screened theory with an additional physical length need not retain the same homogeneity. Nor is S a unique new MOND prediction or an absolute determination of kappa.

We attacked the inverse problem with different positive injected and fitted M/L families, correlated dense population constraints, biased inclination priors and direct nonlinear S profiles. Even dense hypothetical population constraints left S broad in the three development galaxies. A precise-looking T measurement required independent angular-gas and inclination information; those assumptions reintroduced absolute scale and could be biased. The failed unregularized DDO154 optimization remains failed.

The exact local design criterion projects the T response out of the remaining amplitude/source-contrast nuisance space. A practical target is gas-force-dominated transition shape over a resolved radial range. The full existing SPARC scan checks this clue using fixed baseline parameters rather than selecting on gravity-law agreement. All 175 galaxies were scored, with 3,389 valid rows and separate bulge nuisances where present. None has a radius with gas-force fraction >0.5 and 0.3<g_b/a0<3. NGC2403 has the most ideal single-galaxy quotient information, corresponding to 0.0768 dex before additional source uncertainty; none meets the illustrative 0.05-dex marker. These are baseline design results, not a necessary gas-cut theorem, a measured uncertainty or a bound on joint ensemble inference. [Inverse report and provenance errata](inverse/REPORT.md), [independent quotient audit](inverse/QUOTIENT_ROOT_AUDIT.md), [full-catalog design scan](target_scan/REPORT.md), [independent scan recomputation](target_scan/SCAN_INDEPENDENT_AUDIT.md).

The release implication is specific: Euclid morphology and stellar-population information can improve geometry/source constraints, but those products do not supply the missing resolved gas-force calibration and dynamical field by themselves. The ECLIPSE metadata pool is still not a ready-made set of complete acceleration tests. No 39-object dynamical validation is claimed.

### 3. Background agreement alone cannot identify the dark-energy coupling

Let F=(H r_d/c)², Q=(a0 r_d/c²)² and u=1+z. Density and canonical-potential portals can share F and Q even when w evolves and both use the same fixed coupling coefficient C. An explicit positive family is

    Q=P+R u³,
    F=C P+(A_density+C R)u³,
    A_potential=A_density-C R>=0.

Both interpretations assign positive evolving scalar density, but different amounts to conserved clustering matter. Therefore merely adding more exact background measurements cannot distinguish them. This is a matter-assignment ambiguity, not measurement noise. Pressure coupling has its own derived interval condition. [Portal classification](portals/REPORT.md), [same-coefficient counterexample](portals/FIXED_COEFFICIENT_ADDENDUM.md).

With an added, fixed GR + smooth-dark-energy growth closure, the same F and the same nonzero growth shape require the same matter coefficient. The derivative-free relation

    Delta[pY] = C0 I0 + A_m I1,
    Y = f sigma8, p = a² sqrt(F)

profiles the unknown initial growth product C0. Two independent interval rows identify A_m; a third yields an overdetermined null. The integrals require between-bin F and Y, their measurement windows and correlated uncertainties. A free effective gravitational coupling or clustered scalar source restores degeneracy. [Full growth definitions and audit](portals/GROWTH_IDENTIFIABILITY_AUDIT.md).

This result motivates a joint geometry/acceleration/growth test only after the action's perturbation closure and a validated likelihood are supplied. Existing growth NO VERDICT rows remain NO VERDICT. A familiar GR growth equation cannot be imported as a demonstrated prediction of the new screened candidate.

### 4. Positive source density gives a separate force-shape gate

Arbitrary stellar gradients do not erase every constraint: an isolated spherical force curve must invert to a nondecreasing enclosed baryonic mass. Exact local and finite-shell bounds were derived for both simple-mu and quadratic laws. DESI Milky Way central proxy values imply negative inferred baryonic shells at the usual acceleration footings, but explicit positive profiles exist inside the published marginal error intervals. Without their joint covariance this is not a calibrated exclusion. It is also conditional on the spherical isolated model and the published effective-mass proxy. [Bounds, witness construction and limitations](positivity/REPORT.md).

An imposed isothermal lens model sits at a slope where this positivity bound has no upper-a0 leverage. Flexible measured slopes and independent baryon information matter. For a fixed entire metric with no slip, adding another gravitational probe cannot distinguish alternative source assignments that produce that same metric. The joint information must come from a different metric response or an independently constrained source/perturbation sector.

## Next decisive work, in order

1. **Theory:** solve a screened background for the changed kernel, including its local scalar response, and derive the full constrained perturbation operator on that solution. Freeze the sign, boundary and parameter footing before a Solar/galaxy score. A successful reduced kinetic lemma does not establish these gates.
2. **Observations:** obtain resolved gas conversion/shape, geometry and dynamics in systems with informative transition response. Fit the actual observables with radial-source and field-equation nuisance parameters. Do not substitute Euclid colours for total IMF constraints or a synthetic injection for a released-data result.
3. **Cosmology:** establish the candidate's perturbation closure and validate the growth likelihood against known answers before combining with BAO. Avoid double counting correlated DESI products.

These are concrete open implications. The current work identifies them and supplies new tools to attack them; it does not claim the requested all-gate breakthrough has already been achieved.

## Publication and integrity

Publication branch: `codex/euclid-desi-review-2026-11-12`. Phase-1 final ancestor: `8db464d4bc256b981d5812c199d6bdff8705b765`. Phase-2 checkpoints already pushed include `b6b023ac375c27268a525f387034565fb7770f14` and `9dd75a7c8b82eaf7d60566bba525f5ae0fb76aac`. Subsequent branch history carries the integrated theory/scan evidence. Commits use an isolated index and never stage unrelated shared-checkout work. Raw input bytes, failed runs, contracts, hashes and independent reviews remain available beside each route.

The integrated integrity check verifies 305 manifest artifact references and thirteen additional archived theory sources. The nineteen execution records contain fifteen completed runs and four preserved failures. See [integrity evidence](INTEGRITY_AUDIT.json), [verification script](check_integrity.py) and [reproduction notes](REPRODUCING.md). These counts describe execution/provenance, not nineteen independent scientific validations.
