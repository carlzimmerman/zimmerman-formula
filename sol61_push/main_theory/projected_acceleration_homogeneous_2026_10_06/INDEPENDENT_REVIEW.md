# Independent raw homogeneous reduction audit

Verdict: accepted for the stated both-expanding homogeneous metric sector. This is an actual constraint reduction with admitted homogeneous solutions; it is not a full spatial scalar/clock health result or a selected vacuum normalization.

Pinned REPORT SHA256 `666790069c45c844ebdb2e966879a474f7a5e3888e631512f7d4720dde7c213b`; checks SHA256 `1ce601b0afabc5f53f6982ffb51b1ba61cc50a3f40233af8882bf58a7140d5b8`. I reconstructed the following from the displayed two-Einstein action, rather than importing author functions or using the assertion count as proof.

## Raw action and lapse equations

Spatially flat ADM Einstein curvature, after its ordinary time boundary term, gives −K n(n−1)a^n alphadot²/N per metric. On homogeneous shared-clock configurations the projected acceleration invariant is zero for arbitrary positive N,L,a,b; its first variations vanish. A constant M(0)=−A with geometric-mean volume gives −2Kχa0²A sqrt(NL)(ab)^(n/2). These premises yield exactly the raw action in the report.

With tau=(alpha+beta)/2,zeta=alpha−beta,r=ln(N/L),ell=sqrt(NL), set B=K n(n−1), V=exp(n tau), v_plus=taudot+zetadot/2 and v_minus=taudot−zetadot/2. The kinetic factor is −BV[exp((n zeta−r)/2)v_plus²+exp(−(n zeta−r)/2)v_minus²]/ell. Its r derivative sets the two bracket terms equal. For v_plus,v_minus>0 this gives r=n zeta+2ln(v_plus/v_minus), and the sum is 2v_plus v_minus. The second r derivative is strictly negative, so this algebraic stationary point is isolated. The resulting relative kinetic sign is positive, whereas setting r=0 before varying does not perform this constraint reduction.

## Canonical and Dirac reconstruction

Before elimination the momenta in alpha,beta are p_alpha=−2Ba^n alphadot/N and p_beta=−2Bb^n betadot/L. Their Hamiltonian is ell times

C=−p_alpha² exp(r/2)/(4Ba^n)−p_beta² exp(−r/2)/(4Bb^n)+U.

The primaries are p_r=p_ell=0. The secondary r equation is C_r=0; at its zero, C_rr=−(X+Y)/4<0 for the two positive kinetic magnitudes X,Y. Thus p_r,C_r are a second-class pair. After their removal, p_ell and the common Hamiltonian constraint are first class. C has no ell dependence and its self Poisson bracket vanishes; no tertiary follows on this regular open patch. The metric phase-space count is 8−2−4=2, or one homogeneous configuration degree. This count removes the accidental clock flat direction of the homogeneous restriction and does not count finite-k clock or metric helicities. The separately mentioned algebraic modulus pair is conditional on the admitted vacuum auxiliary branch; it is not needed for the eliminated-envelope homogeneous metric result.

The reduced momenta are p_tau=−4BV taudot/ell and p_zeta=BV zetadot/ell. Legendre transformation gives C=−p_tau²/(8BV)+p_zeta²/(2BV)+U. For positive U, the expanding solution is p_tau=−2sqrt(p_zeta²+m²), m²=2BVU=4BKχa0²A exp(2n tau). Deparametrizing by monotone tau gives H_tau=2sqrt(p_zeta²+m²), with second p_zeta derivative 2m²/(p_zeta²+m²)^(3/2)>0. The corresponding relational Lagrangian is −2m sqrt(1−zeta_prime²/4), with second velocity derivative m/[2(1−zeta_prime²/4)^(3/2)]>0. These are reduced signs, not the unreduced conformal Einstein sign or the full-field Hamiltonian.

## Exact admission and offset

p_zeta is constant. Writing q=asinh[p_zeta/(m0 exp(n tau))], differentiation gives q_prime=−n tanh q. Hence zeta=zeta_infinity−2q/n solves zeta_prime=2p_zeta/sqrt(p_zeta²+m²), and |zeta_prime|<2. The lapse reconstruction uses (1+tanh q)/(1−tanh q)=exp(2q), giving r=n zeta_infinity+2q as claimed. Both metric expansion velocities and both lapses stay positive locally. The common constraint fixes positive ell from a chosen expanding tau parametrization. This supplies smooth actual homogeneous solution data, not just a nonzero off-shell Hessian.

At p_zeta=0,zeta_infinity=0, r=0 and both metrics coincide. Proper-time choice gives H²=χa0²A/[n(n−1)] and Λ=χa0²A/2. Every A>0 remains allowed. The reduction therefore cannot set an interaction offset, λ, or 32pi. Arbitrary zeta_infinity and matter/source matching remain separate issues.

## Evidence and limits

All three current manifests independently validate: main_a and the intended frozen-lapse/selected-offset controls. Validation establishes bounded execution provenance, not the above proof. The preserved earlier tanh simplification failure is distinguished from the exact exponential identity in the current script; it is not suppressed as successful evidence.

The action is a homogeneous acceleration-only restriction with geometric-mean constant interaction. Full spatial lapse constraints, scalar gradients, common-clock degeneracy, matter and source admission are not supplied by this calculation. The admitted positive homogeneous branch is compatible with the author operator report's missing scalar-health implication, rather than contradicting its zero quadratic common-clock observation.
