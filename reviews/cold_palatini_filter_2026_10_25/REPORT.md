# A real escape from the mass bound, and a conditional density filter

**The independent-connection variant evades the previous metric mass bound.** It also provides a potential physical environmental filter: the mass of scalar excitations rises in the restored high-density phase. This is more specific than imposing a cold retention fraction. It is not yet a successful reservoir theory: the same construction forces a large matter coupling at the desired vacuum mass, and its transition/filter densities depend on coefficients the symmetry does not determine.

The new exact result is broader than either gravitational formulation. For the same one-field potential and matter coupling, changing any positive two-derivative kinetic normalization cannot independently tune the mass and coupling:

    m_E²/(H_E² alpha²) = 24(1-s)²/(r s²).

This identity is a constraint on the stated model, not on all modified gravity or multifield completions.

## 1. Change one structural premise

Continue the action tested at cb2f5f134b, but vary a torsion-free gravitational connection independently of the metric. Assume matter has no dependence on that independent connection:

    S = int sqrt(-g) [F(phi) R(g,Gamma)/2 - (partial phi)²/2 - U(phi)] + S_b[g,b],
    F=M²-xi phi²,  U=V0+lambda(phi²-v²)²/4,
    D=DeltaV=lambda v^4/4, r=V0/D, s=xi v²/M².

This is a different gravitational theory, not a change of coordinates in the old one. Independent connection variation gives compatibility with h_mu_nu=(F/M²)g_mu_nu. In that Einstein metric the scalar kinetic factor is K_P=M²/F, the potential is W=M^4U/F², and the matter coupling is A=M/sqrt(F). There is no metric-formulation contribution 3M² F'²/(2F²). The assumptions about the connection and matter are substantive, not a derived microscopic symmetry. For context on Palatini scalar-tensor frames see [Kozak & Borowiec (2019)](https://link.springer.com/article/10.1140/epjc/s10052-019-6836-y); our restricted action and following identities are explicit here.

The vacuum stationary point is unchanged:

    y=phi²/v²=[1-s(1+r)]/(1-s),
    f=F/M²=1-sy, u=U/D=r+(1-y)²,
    0<s<1/(1+r),  H_E²=D u/(3M² f²).

It has positive K_P, F and scalar mass. These checks do not establish quantum health, screening or a full cosmological solution.

## 2. Heavy mass is possible, but its coupling is linked

At that stationary point,

    m_E² = 8D y(1-s)/(v² f²),
    alpha² = [M d ln A/d chi]² = s² M² y/(v² f).

Both can grow without bound as v/M decreases at fixed r,s. Consequently the previous metric bound m_E/H_E<=2(1-s)/(s sqrt(r)) is genuinely evaded. We do not falsely carry it into Palatini gravity.

However, for ANY positive kinetic factor K in a single-field two-derivative Einstein action, m_E²=W''/K and alpha²=M²(ln A)'²/K at a vacuum stationary point. K cancels. Substituting this potential gives the exact displayed mass/coupling identity. The derivative-of-K term in canonical W'' vanishes because W'=0. Adding only a different positive kinetic coefficient cannot break the relation. Changing the potential, matter coupling, degrees of freedom or derivative structure can evade its hypotheses and must be analyzed separately.

An illustrative matching point uses r=1,s=1/4 and the inherited eta=1500 pc km/s at H_reference=1.8e-18 s^-1. These are sensitivity inputs, not predictions. Requiring m/H=c²/(eta H_reference)=1.07877e12 yields

    v/M = 3.04638e-12,
    alpha = 7.34007e10.

That very large linear matter coupling cannot be ignored. It is not alone an observational exclusion: range, environment, nonlinear screening and the validity of perturbation theory matter. This calculation does not simply apply an unscreened long-range force formula to a heavy scalar. Nor does it assert quantum perturbativity at this point.

## 3. Derive a density filter instead of assigning retention

Let rho denote external pressureless Jordan-frame ENERGY density (use rho_mass c² for mass units). In a locally uniform, slowly varying patch, neglect gradients of the background scalar. The trace and field balances are

    F R = rho + 4U,
    U' + xi R phi = 0.

These are local adiabatic balances, not a globally static dust/de Sitter solution. The external source must be distinguished from the scalar's own stress, already included in the equations; it cannot be counted twice as rho. Pressure replaces rho by the appropriate trace combination.

The nonzero branch obeys

    y(rho)=1 - s[r + rho/(4D)]/(1-s).

It reaches the origin at

    rho_crit = 4D[(1-s)/s-r].

Above this threshold the origin has positive scalar mass squared. Linear excitations there have

    m_in,J² = xi (rho-rho_crit)/M².

At phi=0, F=M² and the Einstein/Jordan mass units coincide. Outside, in the broken vacuum, m_out,J²=f m_out,E². Thus the local physical mass comparison is

    m_in,J²/m_out,J² = s f [rho/D-rho_crit/D] / [8y(1-s)].

A growing local excitation mass is a potential barrier for sufficiently slow scalar waves or WKB particles. This supplies an explicit reason a sufficiently dense region might admit little cold material. It does not yet prove which astronomical systems are excluded: clusters also contain dense regions, and an interface, incoming spectrum and baryonic density profile have not been solved.

### Compare conserved energy, not masses in different local clocks

For a static background the relevant rest-energy threshold is m_J sqrt(-g_Jtt)=m_E sqrt(-g_Ett), not the local Jordan mass alone. The conformal lapse can be appreciable. If the Einstein lapse variation is negligible, the interior to exterior squared rest-energy ratio is

    m_in,E²/m_out,E² = s f² [rho/D-rho_crit/D]/[8y(1-s)].

This distinction matters even in the illustrative point r=1,s=1/4:

- symmetry restoration: rho/D=8;
- equality of local Jordan masses: rho/D=27.2;
- equality of conserved rest-energy thresholds for constant Einstein lapse: rho/D=31.04.

The exterior conformal shift is Delta ln A=-ln(f)/2=0.09116. Treating the Jordan lapse as unchanged would therefore give the wrong filter threshold. No physical interface or gravitational redshift has been solved here; 31.04 is explicitly conditional on the Einstein-lapse approximation. Finite incoming kinetic energy raises the threshold. Nonadiabatic transmission and particle production require a wave calculation. The output distinguishes these quantities instead of reporting a spurious capture fraction.

## 4. What has and has not been gained

There is now an explicit candidate filter: **density-dependent scalar rest energy**, arising from the action rather than a chosen halo temperature. The Palatini kinetic structure also removes a specific previous obstruction. These are constructive advances.

They do not achieve the user's no-free-parameter target. Z2 allows independent V0,lambda,xi,v; neither r nor s is fixed. The illustrative equal-energy choice and s=1/4 merely locate an example. The density threshold varies with those choices. A field transition has not generated a normalized abundance or momentum spectrum, and the baryon coupling has not been shown to preserve the galaxy law. This is still a new candidate, not a covariant derivation of the CCT force split or a MOND amplitude.

A full continuation must solve the density interface and production on one common cosmological state, with stress-energy conservation, then test the actual galaxy and cluster profiles. In particular, if the threshold selected by a microscopic theory excludes the cluster gas environments as well as galaxies, the filter fails. Moving the threshold by choosing s after examining those systems would be a fit, not the requested selection.

The generic mass/coupling identity tells us exactly what a deeper completion must change if it needs a heavy scalar with small linear matter coupling: the invariant relation between W and A, or the one-field/two-derivative assumptions. A mere rescaling or new positive K does not suffice. We have not selected such a completion or claimed that it is impossible.

## 5. Verification and status

Symbolic derivatives verify the identity for arbitrary positive K, the Palatini formulas, restoration threshold and common-frame mass comparison. Numerical checks cover 27 vacuum combinations and 108 restored-density combinations. Omitting the Jordan mass conversion deliberately fails the independent ratio check. Both bounded-run manifests validate, including the expected failure record. No observations are newly fitted or classified. Results have self-review only.

Artifacts: `FROZEN_CRITERIA.md`, `contract.json`, `check.py`, `run/result.json`, and normal/mutation manifests. The filter's scalar background, wave transmission, actual gas-density comparison and production are OPEN. The microscopic selection of coefficients and a0 remains OPEN. Do not promote the illustrative point, or the existence of a filter, to a parameter-free solution.
