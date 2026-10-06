# CFG353 tidal continuation: zero-point repair, geometric false positives and missing phase

This independently builds on the actual CFG353 README and its pre-script frozen criteria. Claude's numerical/Lean/data outcomes are inspected assertions, not authenticated by rerunning them here. Its zero-point route is explicitly scoped as failed; the tidal suggestion is explicitly an uncomputed next door. The calculations below concern that suggestion, not a claim that Claude already tested it. The owner has relaxed MS1 to allow total cold+baryon mass; under the original MS1 this reader remains inadmissible. Neither switch construction determines cold microphysics or selects the already fitted kappa=1/2.

## Exact signed tidal estimator

Let H_ij=partial_i partial_j Phi_d and order its eigenvalues lambda1<=lambda2<=lambda3. For a spherical potential,

    H=(gprime-g/r)nn^T+(g/r)I,
    eigenvalues={gprime,g/r,g/r}.

The repeated tangential value is always the middle eigenvalue, independent of the ordering of gprime. Gauss gives g/r=(4piG/3)(rho_enc-rho_bar). Therefore

    rho_tidal=3lambda2/(4piG)=rho_enc-rho_bar

exactly for ANY spherical radial density, not merely a point-mass exterior. This removes the potential zero point and does not need the host's infinity. Use the signed value for a threshold rho_tidal>(Delta_ta-1)rho_bar; taking its absolute value would again turn density deficits into positive readings. This is a geometric enclosed-density estimator under spherical symmetry, not yet a dynamical boundness estimator.

A precision restriction in the original potential estimator should be preserved. For signed sources/general leaf gauge, its unconditional identity is rho_est=|rho_enc-rho_bar| eta with eta=r|g|/|Phi|=|dln|Phi|/dlnr|. The un-absolute enclosed-overdensity formula and eta=-dln|Phi|/dlnr require positive enclosed overdensity and the negative-potential attractive convention. That convention is appropriate for an isolated positive host zeroed at infinity, but is not automatic in E0. This does not change the scoped failed-route verdict.

## Uniform filament and sheet discriminator

An infinite uniform positive cylindrical overdensity delta_rho has interior Phi=piG delta_rho(x²+y²)+constant. Its eigenvalues are0,2piG delta_rho,2piG delta_rho. Hence inside it

    rho_tidal=(3/2)delta_rho.

A compensated cylindrical cell can preserve this interior Hessian: exterior concentric compensation changes the potential offset but not the interior force. Therefore an axially unturned filament still fires when delta_f>(2/3)(Delta_ta-1). In EdS Delta_ta=9pi²/16, this threshold is about3.035; the proposed frozen filament contrasts5 and10 would cross it. At the stated z0 threshold11.806, the corresponding limit is7.204, so delta_f10 still crosses. These are algebraic consequences of the assumed threshold, not independent astronomical validation or a rerun of its shell ODE.

Outside a line mass, Phi=2G lambda log(r_perp) has eigenvalues{-2G lambda/r_perp²,0,+2G lambda/r_perp²}; its middle value is zero. Inside a uniform plane/slab, Hessian={0,0,4piG delta_rho}, also middle zero for positive overdensity. Thus the pointer correctly rejects ideal external lines and ideal sheets, but not dense filament interiors. Requiring all three eigenvalues positive instead would reject the filament yet also reject ordinary point-mass exteriors, whose radial tidal eigenvalue is negative. That simple stricter replacement loses the required spherical halo reading.

## Harmonic contamination and ownership

Adding an external harmonic field changes no local density but adds any trace-free symmetric tidal matrix. For example Phi_ext=(t x²+t y²-2t z²)/2 has zero Laplacian and middle eigenvalue t>0 of arbitrary amplitude. Shift invariance alone does not remove it. Conversely the point-mass Hessian diag(-2t,t,t) can be canceled by trace-free diag(2t,-t,-t). The latter is physically realizable at a point using equal positive external mass pairs along y and z; pair symmetry cancels their gradient while their Hessians sum to that matrix. Thus potential-offset removal leaves actual environmental tides, rather than resolving host ownership.

There is a sharp local spectral obstruction. Any Hessian scalar S invariant under EVERY external harmonic addition must satisfy S(H+T)=S(H) for every trace-free T. Taking T=(trH)I/3-H shows S can depend only on trH. But point-mass exteriors and empty background both have trace zero, while their enclosed mean densities differ. No such universally tide-insensitive local Hessian estimator can also recover spherical enclosed density in an exterior. A restricted environment or physical source partition is an additional premise.

Recovering the own-host field requires a center, source membership or boundary prescription and subtraction of external mass/tides. A nonlocal Poisson solve of the entire instantaneous leaf density supplies a field, but not the source ownership partition. A center chosen from phase-space groups/history is new information; satellites and flybys otherwise read the host environment. This reader's admission of cold mass does not by itself solve that ownership problem.

## Independent root phase-information audit

The linked [root phase lemma](../../main_theory/claude_cfg353_2026_10_06/ROOT_PHASE_INFORMATION_LEMMA.md) is correct in its declared Newtonian pressureless spherical setting. With n>=3,

    U=-mu/[(n-2)R^(n-2)]-H²R²/2,
    -Uprime=-mu/R^(n-1)+H²R,
    Rs=(mu/H²)^(1/n), Umax=-nH²Rs²/[2(n-2)].

Uprime is positive below Rs and negative above it; Rs is the unique maximum. At fixed R0<Rs and identical mass/density/potential, rest gives E=U(R0)<Umax and inward acceleration. An outward speed squared greater than2[Umax-U(R0)] gives E>Umax and no outer turning point in this Newtonian model. Uniform homologous dust supplies independent velocity initial data without changing the initial Poisson field. The n3 mu=H=1,R0=1/2 example gives U0=-17/8,Umax=-3/2, and outward speed2 gives E=-1/8 above the barrier.

Thus even complete instantaneous spatial density/potential information cannot classify all these phases. This is stronger than a local tidal counterexample, but it is not an assertion that GR momentum/extrinsic-curvature data are identical. A cosmological growing-mode restriction can tie velocity to density and permit a conditional spherical-collapse threshold; it supplies the missing phase premise. Actual velocity/expansion, phase-space history or dynamical boundary data are alternatives. Adding that information still needs a varied action, conservation/reaction and ownership analysis.

## Checkpoint and limits

The middle eigenvalue is a real repair of the zero-point defect. Its exact spherical success, dense-filament failure, arbitrary external-tide contamination and phase limitation are now derived. The next viable construction must state source ownership and the physical velocity/history restriction while excluding the frozen unbound geometries; a renamed scalar density threshold does not supply them.

Our own checks.py contains exact symbolic controls only and never executes or edits Claude's scripts. Fresh provenance runs below runs test these identities, including a mutation that incorrectly assigns zero middle eigenvalue inside the filament. Analytic arguments above establish the scoped results; check counts do not certify Claude's numerical, Lean or data claims. SOURCE_PROVENANCE.json records actual inspected hashes and whether current frozen criteria match the named frozen commit.

Authoritative own runs: main_a9/9; filament_zero_a7/9 (wrong interior filament eigenvalue and its normalization fail). Both version-2 manifests validate, unchanged inputs, retained logs. Caps wall30s,CPU20s/process,1MiB logs,one cooperative thread; no memory/affinity cap.
