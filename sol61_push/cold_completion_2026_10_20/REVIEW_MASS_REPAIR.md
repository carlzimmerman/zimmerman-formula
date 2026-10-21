# Independent analytic review of the mass-ledger repair

20 October 2026. **Accepted under its stated Newtonian, spherical and endpoint assumptions.** No sign or double-counting error was found. This review checks the displayed identities; it does not validate the five source cases, rerun CFG932, edit its frozen criteria or regrade a result.

## Reviewed source

- Path: `sol61_push/cold_completion_2026_10_20/MASS_LEDGER_REPAIR.md`
- SHA256: `46ad85b2d87826e7f710868dbf1681b3be3138e5ad96cbb703a349e6ff50816f`
- Observed repository HEAD: `6a3978ee414b855305c388de6d520968ec96a0a6`
- Review timestamp UTC: `2026-10-20T19:52:47.809599+00:00`

The hash pins the working bytes, rather than asserting that the report is committed at that HEAD. The source was rechecked unchanged while preparing this review.

## Integration by parts and unmatched mass

Write Delta(r)=M_s(r)-M_p(r). The Stieltjes integration identity is

    integral_(0,R] e dDelta = e(R)Delta(R)-lim_(r->0) e(r)Delta(r)
                              -integral_(0,R] Delta de.

The source's differentiable expression follows when the central boundary term vanishes and e is continuously differentiable on the integration region. Dropping the outer term requires Delta(R)=0 (or an independently justified vanishing e(R)); absence of a crossing is not that condition. Replacing e by e+C changes an unmatched comparison by C[Delta(R)-Delta(0)]. Thus a destination must close the missing-mass energy reference; it cannot be erased by choosing a convenient additive constant.

A jump at R must be handled with one consistent endpoint convention. A jump strictly at R+ is outside an integral ending at R; taking an outer boundary beyond the jump includes its e(R)Delta M contribution. Interpreting the discontinuity as a shell supplies a possible measure-valued completion, not proof of the physical destination. Smooth derivative formulas omit its delta-function surface density.

The distinction between no positive cumulative surplus and positive cumulative surplus without an equal-mass outer boundary is therefore essential. Whether the corresponding physical cost is zero, undefined, infeasible or paid by an exterior receiver must follow from the completed mass/energy ledger, not from `Rx=None` alone.

## Shell gravitational energy and kinetic closure

For shell mass m=Delta M, radius R and a fixed spherical interior M_in, shell-interior interaction is exactly

    W_cross=-G M_in m/R.

It is counted once. The shell's interior potential is constant but contributes this interaction energy; zero interior force does not imply zero cross energy. The shell self-energy follows by assembly:

    W_self=-integral_0^m G m' dm'/R=-Gm^2/(2R).

Hence the stated W_total is correct. M_in excludes the added shell; otherwise its self-mass would be counted twice. The initial and final W_in must use the same full-system or cold-in-static-external-potential convention.

For the explicitly chosen circular shell, the averaged self-field gives

    v_c^2=G(M_in+m/2)/R,
    K_shell=m v_c^2/2=G M_in m/(2R)+Gm^2/(4R),
    K_shell+W_cross+W_self=-G M_in m/(2R)-Gm^2/(4R).

The signs and half-factors are correct. This is a conditional circular/virial construction. It is not the kinetic energy of an arbitrary radially escaping shell, a stationary/stable finite-thickness equilibrium proof or an energy transfer mechanism. The Newtonian pair-energy formulas also cannot be transferred unchanged to an unspecified nonlinear force action.

## Angular momentum and remaining physical inputs

Cauchy-Schwarz gives |J_orb|^2<=2 I K, with I the moment about the J axis. Material on the spherical shell satisfies I<=mR^2, yielding the source's |J_orb|<=R sqrt(2mK_shell). This is an optimistic necessary capacity bound. A uniform spherical distribution and an admissible orbit population generally prevent saturation; passing it does not construct a joint energy/J endpoint. Intrinsic spin and radiation require separate accounts.

The source correctly retains all remaining obligations: an actual mass destination, nonnegative inventory, the initial/final gravitational field, kinetic and charge flux, any binding/feedback reservoir, travel and return, angular-momentum direction and stellar response. A prescribed shell must not be described as independently formed or as repairing Sextans' profile/stock limitation or the four-dwarf selectivity problem.

Review provenance: independent derivation of the boundary, shell and Cauchy-Schwarz identities from the stated definitions. No source experiment or source case enumeration was executed. Only this review file was created; no Git, publication, criteria or shared-checkpoint mutation was performed.
