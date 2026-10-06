# Homogeneous admission for an acceleration-only interaction

The geometric-mean-volume two-Einstein action with a positive vacuum offset admits a smooth expanding homogeneous branch after BOTH lapse equations are retained. Its relative scale variable has positive kinetic curvature after reducing the algebraic relative lapse and common Hamiltonian constraint. This is a construction in a homogeneous sector, not a full scalar/gradient health theorem. It leaves the offset arbitrary and does not fix32pi.

Base checkpoint: `4882e2ec62` (full execution revision in the bounded manifests). This is a separate calculation from the simultaneously authored projected-acceleration operator. Its raw premise is only that the interaction invariant and its first variation vanish on homogeneous shared-clock configurations. Actual normal acceleration has this property. No unfinished peer report is used as a proof leaf.

Let n>=3, K,a0,A>0, chi=(n−1)/[2(n−2)], and B=K n(n−1). Both metrics are spatially flat, with scale factors a=exp(alpha), b=exp(beta), and positive lapses N,L. The Einstein terms have the conventional healthy tensor sign. On the zero-acceleration homogeneous branch the action per fixed coordinate cell is

    L = −B[a^n alphadot²/N+b^n betadot²/L]
        −2K chi a0² A sqrt(NL)(ab)^(n/2).

An algebraic source modulus with potential lambda T²/2 has T=0 here and a positive vacuum curvature; it can be removed as its usual second-class pair. No modulus kinetic degree is inserted. A spatially homogeneous monotone shared clock has zero normal acceleration for either metric for any time parametrization; its homogeneous equation is identically satisfied. Its accidental freedom in this restricted sector is NOT a full-field clock constraint/degree count.

## Retain the relative lapse

Set tau=(alpha+beta)/2, zeta=alpha−beta, r=ln(N/L), ell=sqrt(NL)>0 and U(tau)=2K chi a0² A exp(n tau). The exact lagrangian becomes

    L = −B exp(n tau)/ell [exp((n zeta−r)/2)(taudot+zetadot/2)²
                           +exp(−(n zeta−r)/2)(taudot−zetadot/2)²]−ell U.

On the open both-expanding patch taudot>0 and |zetadot|<2taudot, the algebraic r equation has the unique solution

    r=n zeta+2ln[(taudot+zetadot/2)/(taudot−zetadot/2)].

Its second r derivative is negative and nonzero. A lapse equation need not minimize a physical auxiliary energy; r is a nondynamical gravitational constraint variable. Substitution, or equivalent second-class Hamiltonian reduction, gives

    L_red=−2B exp(n tau)(taudot²−zetadot²/4)/ell−ell U.

Holding r=0 before variation would miss this positive relative sign. The admissible patch and lapse positivity matter; no absolute-value simplification is asserted across contracting/mixed-sign branches.

## Canonical constraint and local solution

Write V=exp(n tau). Momenta are p_tau=−4BV taudot/ell and p_zeta=BV zetadot/ell. The common constraint is

    C=−p_tau²/(8BV)+p_zeta²/(2BV)+U=0.

In the unreduced homogeneous metric sector, p_r=0 and C_r=0 form a second-class pair on this patch: in alpha/beta canonical coordinates C_r=−X/2+Y/2 with X,Y positive kinetic magnitudes, so C_rr=−(X+Y)/4<0. The pair removes r and p_r. The remaining common-lapse primary and C are first class; their preservation introduces no tertiary constraint. Together with the separately removed modulus pair, the four metric homogeneous configurations (alpha,beta,r,ell) leave one configuration degree. This is not a count of finite-k field helicities or of a clock mode outside the restricted sector.

Define m(tau)²=4BK chi a0² A exp(2n tau). On the expanding branch p_tau=−2sqrt(p_zeta²+m²). Using tau as a local relational time gives

    H_tau=2sqrt(p_zeta²+m(tau)²),
    d zeta/d tau=2p_zeta/sqrt(p_zeta²+m²),  d p_zeta/d tau=0.

Since m>0, |d zeta/d tau|<2, retaining both-expanding scales and positive reconstructed lapses. These smooth equations and the positive Friedmann constraint give local homogeneous admission. A useful exact solution is

    zeta(tau)=zeta_infinity−(2/n)asinh[p_zeta/(m0 exp(n tau))],
    r(tau)=n zeta_infinity+2asinh[p_zeta/(m0 exp(n tau))],
    m0=2sqrt(BK chi a0² A).

Here zeta_infinity is an integration constant, not an imposed matching condition. The relative velocity tends to zero at large tau in this vacuum homogeneous solution. No matter or source boundary matching is proved.

Eliminating ell at its positive constraint solution yields the relational Lagrangian

    L_tau=−2m(tau)sqrt(1−zeta_prime²/4),
    L_tau,zeta_prime,zeta_prime=m/[2(1−zeta_prime²/4)^(3/2)]>0.

Equivalently H_tau,p_zeta,p_zeta=2m²/(p_zeta²+m²)^(3/2)>0. These signs are AFTER the relative-lapse and common constraint reductions. They establish only the homogeneous relative-scale kinetic sign, not the full field Hamiltonian.

At p_zeta=0,zeta_infinity=0, both metrics coincide with N=L=1 in a proper-time chart and

    H²=chi a0² A/[n(n−1)],    Lambda=chi a0² A/2.

Thus every positive A admits this common vacuum. The relation is dimensionally consistent with c=1 and reproduces the inherited arbitrary-offset dictionary. It does not supply an independently motivated A, a source-to-vacuum bridge, a cold abundance or an additional observational prediction.

## Scope and next implication

The new diagnostic removes the earlier inference that adding lapse derivatives is necessary for every tensor/source repair: an acceleration-only interaction leaves them algebraic in this sector, with an admitted positive reduced relative-scale branch. Full inhomogeneous constraints, gradients, the common-clock degeneracy and matter/source matching remain the next load-bearing obligations. A positive homogeneous sign cannot replace them. Exact SymPy checks corroborate the displayed uniform algebra; bounded manifests record their actual inputs and controls. No literature novelty or all-bimetric theorem is asserted.
