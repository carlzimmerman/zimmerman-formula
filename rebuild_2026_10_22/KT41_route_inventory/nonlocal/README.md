# Nonlocal route inventory — read-only prior-work audit

This audit found substantial prior work on every broad kernel family suggested: corrected Gaussian, positive action mixtures, Helmholtz/Yukawa and squared resolvents, tensor diffusion coefficients, field-dependent coefficients, high-pass environmental filtering, and covariant heat-filter auxiliaries. None of those names identifies a new route. The exact **curvature-only filtering of the KT39 constitutive argument**, keeping its gradient unfiltered and varying the full composite action, was not found in the inspected matches. This is a bounded repository distinction, not a proof of global absence or scientific novelty.

The audit made no new physical computation and changed no prior research file. A separate authorized KT42 calculation, if undertaken, must identify the exact change and preserve all baryons/cuts.

## Search coverage and gaps

`SEARCH_MANIFEST.json` records three repository-root searches with `rg --hidden --no-ignore -l -I`. They include hidden/ignored text. Kernel/resolvent search found 3327 paths; nonlocal-action/filter search 1240; environmental/spectral-mixture search 1358. `FOCUSED_SEARCH_MANIFEST.json` records curvature/filter proximity (213), continuous-mixture/dual-certificate (104), and filtered-Hessian-symbol searches (122). `hessian_filter_paths.txt` is an additional initial 181-path reconnaissance list, not a fully provenance-recorded run. Full path lists are retained. Source records below concern actual inspected formulas, not merely filename hits.

Excluded: `.git`, node_modules, virtual environments, __pycache__, and our own KT41 audit tree. Binary detection remained enabled; symlinks were not followed; compressed archives, binary PDFs and historical Git objects were not extracted/searched. Readable extracted literature and old generated candidate indexes were included, but every matching file was not reviewed line by line. All six recorded searches returned 2 with 743 permission-error lines under malformed extracted-source filenames in `real_research/alpha_principle_2026/AS4_fg_weyl2/as4_scratch/0902.4630/x/`. Their full stderr is preserved. This is an explicit coverage hole. The shared working tree was changing concurrently; `SOURCE_PINS.json` captures inspected-file hashes at audit write time, not a frozen-repository snapshot.

Therefore the user's desired “for sure nowhere in the repo” cannot be certified. What is defensible is an auditable exact-neighbor comparison and a stated searched scope. No external literature novelty claim was attempted.

## Actual nearest work

| Prior route | Actual mathematical object | Existing result / distinction |
|---|---|---|
| KT33, KT34 corrected Gaussian | U=U_N+U_ph[S rho], Phi=N rho+S*Phi_ph[S rho] | Fixed epsilon .5 fails both MW and Cassini. Common-epsilon MW/Cassini windows separate; exhaustive rounded-width states plus analytic large-width MW tail. Dense numerical Cassini coverage remains short of interval certification. Repeating epsilon is not new. |
| KT36 universal fixed length | Same full reciprocal action, one physical length | 3 kpc has MW primary survivors and tiny bounded Solar signal, but isolated dwarfs only 4/24 and 5/24 versus plain 19/24. Strict vertical-height cuts fail. This is not curvature-only filtering. |
| KT36 positive action mixtures | U_N+sum w_j U_ph[S_j rho], w>=0,sum w=1 | All weights on 15 epsilon supports reduced to simplex/Cassini vertices. Refined selected best speeds 216.949794/218.209629 <219.9. Full population uses mixed-resolution arrays, so not a rigorous all-width continuum exclusion. Applying one mixed filter inside one nonlinear energy is a different model, already explicitly distinguished. |
| NV1 nonlocal variable | Admissible Gaussian-process response on (log y, log ell, f, E) | E2 basin feature fitted; no useful monotone separation, holdout gates fail. E1/E3/E4 insufficient coverage. This is an environmental-feature regression, not a nonlocal variational spatial operator. |
| P2/AZ2 | A=I-div(D grad), S=A^-1; D prescribed positive symmetric tensor | Mass/constants/positivity/reciprocity controls pass. Tensor-valued D is already allowed explicitly. No gravity action or derived D. |
| P2/AZ8 | J[u]=int[(u-rho)^2/2+D(u)|grad u|²/2] up to source-only constants | Varying D adds D'|grad u|²/2. Plug-in conservative equation misses it; manufactured mismatch .00687223 and integrated source excess .00785398. Separate-field D(Phi) leaves additional gravitational stresses uncomputed. |
| P2/AZ9 | First resolvent kernel exp(-r/xi)/(4pi xi²r) | Point-source central cusp; all absolute quadrupole convergence checks fail. Huge cutoff-sensitive ratios are not a physical exclusion. |
| P2/AZ10–13 | S_hat=(1+xi²k²)^-2, K=exp(-r/xi)/(8pi xi³) | Conditional Cassini .104500/.266319 passes, but same monopole yields orbit-averaged Saturn Z=6.983944/11.329246. SPARC canonical fails and alternate only limited gates pass. Full varied field-local coefficient remains unfinished. Another xi/power scan would repeat the known architecture. |
| sol61 nonlocal_response + CFG653 | P=1-Gaussian, E=int[g²/(8piG)+ec(|P g|)+rho Phi], full outer P | Exactly blind to uniform added gradient and conditionally convex. Curved host fields leak. CFG653 derives scale-separation obstruction and tests physical/fixed L; satellites fail, SPARC can be repulsive, effective monopole vanishes under stated isolated boundary assumptions. Environmental high-pass filtering is explicitly old. |
| filtered_tidal_relation | QUMOND on grad S u, with outer S*; H denotes central **output observable** | Linear-response ratio Q2/D independent of isotropic filter scale/shape under stated assumptions. Does not filter H within KT39 E(g,H). |
| common_action ACTION_REPORT, XC3 | Covariant heat S=exp(b Delta_h), nonlinear q(|D S w|²), lapse-weighted adjoints, gate/carrier sectors | Explicit covariant trial and filter/foliation variations exist; ACTION_REPORT is superseded and contains disclosed obstructions. They are architectural prior art, not an accepted exact present action or inherited observational/health pass. |
| H013, G03 spec, hunt addendum | Helmholtz auxiliary/localization and constraint-only variants | Old proposals with mode-count/host issues. A source's broad “no covariant smoothed action on record” wording cannot erase these explicit trials; distinguish absence of accepted closure from absence of a written action. |
| FN1b fixed-length static | Same reciprocal Gaussian checked against MW, dwarfs, SPARC and Solar/planets at six physical lengths | No tested joint length. D3R code already computes angular vector-nu phantom monopole and outer smoothing for EFE dwarf virial. Merely adding a uniform external field to the corrected Gaussian is not new. Small-width numerical controls and canonical 2 kpc MW survivors have disclosed unresolved/refinement issues. |

## Candidate with an exact mathematical difference

Let T_a be a fixed normalized isotropic convolution, acting on Cartesian tensor components, and retain unfiltered g=grad psi. Define

    Hbar=T_a Hess psi,
    x=g.g/a0², s=ell² Hbar:Hbar/a0²,
    E_a(g,Hbar)=g.g R(x+s^p), p=9/8, ell=3 kpc.

The distinct action is I=int[-rho Phi-(2 grad Phi.grad psi-E_a)/(8piG)]. It filters only the curvature argument. Neither a source-only filter nor U_ph[T_a rho] equals this action because x remains unfiltered.

Full variation requires

    A=(R-1+xR')g,
    Bbar=p ell² s^(p-1)xR' Hbar,
    Delta Phi=Delta psi+div A-partial_i partial_j(T_a*Bbar)_ij.

No extra source split, source-dependent a, or neglected return filter is allowed. If a depends on fields, new variation terms are mandatory and this becomes a different experiment.

Why this is useful: the local KT40 dangerous frozen high-k Hessian term is multiplied by |T_hat(k)|²; Gaussian or resolvent decay removes its unbounded k² amplification. That does not establish positive finite-k response, stable gas/collisionless dynamics, or an acceptable full action. The practical deciding checks are the original outward MW point and negative Draco EFE virial, then retained MW/Cassini gates.

A scale conflict is plausible: a large enough to affect 0.1–0.3 kpc gas/dwarf structure can erase the small-scale Solar curvature that supplied KT39 screening. This is a hypothesis to calculate, not a derived exclusion. Uniform background H=0 remains unchanged, so a filtered-Hessian construction is not automatically EFE-blind.

Under external dominance, the leading positive anomalous energy is U_H=C int|T_a H|^(2p), C>0. Fixed-mass source compression gives U_H(lambda)=lambda^(6p-3)U_H(lambda a), hence

    W_H= -[(6p-3) U_H+a partial_a U_H].

This formal scaling identity explains the required discriminator: smoothing changes the virial scaling but does not by itself make the curvature stress attractive. At a=0 the existing negative KT40 term returns. A finite run must retain this filter-scale derivative, equivalently pair Bbar with T_a delta H in the homology integral.

## Other closure sub-obligations, without pretending they are new models

1. Extend KT36's finite positive-mixture dual inequality to all epsilon supports with controlled numerical error and an analytic tail. A proposed certificate would establish v²(epsilon,cell)<=A+B c(epsilon), B>=0, for every allowed cell and epsilon, with A+B<219.9². Signed Cassini signals require two constraints if their sign changes. Existing support lines only cover stored component data. No complete continuous-support certificate was located in inspected matches. This could close an already-known family; it does not fix KT40 outward force/EFE.
2. P2's fully varied D(Phi) completion is explicitly open, not a new suggestion. It needs actual field equations including coefficient stresses, not another prescribed kernel or exponent. Only a concrete previously uncomputed equation/obstruction would justify work under the user's novelty condition.
3. A covariant realization of the exact curvature-only action is unclosed. Existing heat/localization work must be used as prior art and audited for its own failures; replacing a kernel name does not resolve causality, degrees of freedom, or empirical closure.

The highest-value fresh application is the curvature-only composite action at the inherited KT39 parameters, using a small frozen length grid to test whether it repairs **both** the observed MW outward force and the negative EFE virial while retaining Solar screening. This is a decisive diagnostic, not a claim that the route survives.
