# Independent nonminimal cutoff action audit

Accepted within the common-vacuum and conditional source scope. I independently reconstructed the two metric/scalar constant-vacuum equations, general-d Einstein-frame normalization, stability of the declared F families and the scalar/tensor force ratio. The retained slope lemma was freshly audited separately. A positive shifted quadratic can make any finite cutoff a stable common vacuum, so stabilization is not coefficient selection. No ordinary-only MOND source dictionary or full relative/clock health follows.

## Frozen pins and validated records

Author-observed HEAD `26fe6d3e05753ab87dfc53916e09cb6f174fa9ea`. Current inspected SHA-256:

- REPORT.md: `a072ecf1aa1cd3a23bb0a7ace1fe336dadd0fdc5706f8d7fd253adea24674bbb`
- checks.py: `2dff02342f67d8341f414c9efd460efb915c5721a640090f5059be818830bb82`
- contract.json: `086f0c0e22b4a41581bc4847ff1ec5dced62009fe975aac2d7f8956798e7df4c`
- provenance.json: `50d99e3b1cc402732f358711a0c05bb4fa6da97fd686be4b8565aa0b89f46843`

The retained cutoff report `1860ae1e...` and slope proof `8e3435d1...` are full-byte pinned in provenance. My fresh slope review is the sibling INDEPENDENT_REVIEW.md SHA `030f22118b0f0b527dfa875243deb1d405de82501189cfd0c08b3e73aa6eb525`; its theorem is −1/4<p_A'<0 for every finite u. I independently validated all four current a manifests: main_a, control_trace_a, control_minimum_a and control_EHonly_a. Main records29/29 and each declared control29/30 with its sole intended rejection. Numerical roots/quadratures corroborate, rather than prove, the universal assertions below. No author input was edited by this peer.

## Raw action and both-metric equations

With g=hatg, the action reduces exactly to M0 F R/2−f²(du)²/2−V0 F A, where M0=4K,V0=2K chi_n a0². The full metric variation must still be taken before declaring coincidence. Variation of v=sqrt(Vg Vhat) against one inverse metric is −v g_mu_nu/4; therefore its individual source is half the common potential. At constant u each metric equation is 2KF G_mu_nu=−V0 F A g_mu_nu/2. It gives Lambda=V0 A/M0=chi_n a0² A/2. F cancels this parameter ratio but does not cancel the scalar equation.

The independent constant-u scalar variation is 2K F_u R−V0(F_u A+F A_u)=0. In d dimensions the Einstein trace gives R=2d Lambda/(d−2). Substitution yields d q_F/(d−2)=q_F+p_A, hence p_A=2q_F/(d−2). Dropping the F_u R term would change that stationarity condition. The reported two-metric scalar density equation and nonconstant-F metric derivatives have the correct factors.

At fixed cutoff, direct static ADM integration also checks the critical cancellation. Taking N=e^nu and gamma_ij=e^(2zeta)delta_ij, the spatial curvature term after integration by parts is K(n−1)[(n−2)(grad zeta)²+2grad nu dot grad zeta]. Its constraint is zeta=−nu/(n−2). The two opposite relative lapses thus leave −K chi_n(grad nu_rel)², cancelled by the retained +K chi_n projected term. Both must carry F. An Einstein-only prefactor leaves K chi_n(1−F)(grad nu_rel)². The final report’s PLUS sign agrees with this raw derivation and the script; an earlier draft minus sign was pointed out and corrected before authoritative freeze. This constant-u cancellation is not preservation of the evolving ordinary-source solution.

## General-d frame and actual vacuum mass

Set beta=2/(d−2), g_E=F^beta g_J. The potential is U=V0 A F^(−beta). The curvature transformation yields the Einstein kinetic coefficient
Z_E=f²/F+M0(d−1)q_F²/(d−2)>0.
At equilibrium U_u=0, transforming to a canonical scalar gives m_psi²=U(p_A'−beta q_F')/Z_E. There is no extra derivative-of-Z term at a stationary point. The homogeneous common mode has the stated de-Sitter KG equation; its metric source starts quadratically since the equilibrium scalar is constant and U_psi=0. A negative mass squared therefore has a growing common homogeneous mode. A positive mass is only this sector’s vacuum minimum. Neither sign classifies relative metric or clock constraints.

For F=T^q, q_F'=0, so every finite stationary point is a maximum by the freshly verified p_A'<0. For positive finite monomial sums, differentiating the normalized weights gives q_F'=Var(q_i)>=0, hence the same negative mass bracket. Endpoint slopes and monotonicity justify the unique-root/existence qualifications. No arbitrary positive F theorem follows from these two families.

## Unshifted quadratic and arbitrary-cutoff counterfamily

For F=F0+alpha u² with F0,alpha>0, q_F=2alpha u/(F0+alpha u²). The stationarity condition p_A=beta q_F>1 requires u>0 and u<2beta=4/(d−2). The retained integral bound h(y)<1/2 gives A(T)<pi T/2. In d=4 this implies Lambda/a0²=A/2<pi e²/4. This is an action-parameter vacuum dictionary, not a measured a0 calibration.

At alpha/F0>9/(4beta²) the log-potential derivative is positive at u=0, negative at u=sqrt(F0/alpha), and positive at u=2beta. Thus a sign-changing minimum exists among at least two extrema. Strict positive curvature for sufficiently large ratios follows from the limiting function p_A−2beta/u: it has a unique zero in (4beta/3,2beta), and derivative p_A'+2beta/u²>−1/4+1/(2beta)>0 for d>=4. The implicit-function theorem applies on this positive-u neighborhood. This is a genuine local minimum construction, not a global attractor theorem or interval-certified numerical root claim.

For any given finite u0, write p=p_A(u0), v0=4beta/(3p), u_c=u0−v0 and alpha/F0=9p²/(8beta²). Then z=alpha v0²/F0=2, q_F=p/beta and q_F'=−p²/(4beta²). The actual common stationarity condition holds and p_A'+p²/(4beta)>−1/4+p²/(4beta)>0, since p>1,beta<=1. Thus every finite cutoff can be stabilized within this positive shifted-quadratic family. The free origin and coefficients encode the chosen cutoff. This is an exact counterfamily to selection by stability, not a microscopic explanation of a particular value.

For any stable positive quadratic, shifted or not, let z=alpha(u−u_c)²/F0. At equilibrium q_F'=q_F²(1−z)/(2z), so the mass bracket is C=p_A'+p_A²(z−1)/(2beta z). Stability forces z>1 and 0<C<p_A²/(2beta). Combining Z_E>M0(d−1)p_A²/[(d−2)beta²] with H_E²=2U/[M0(d−1)(d−2)] gives
0<m_psi²/H_E²<2C/p_A²<1/beta=(d−2)/2.
This is the actual stationary common vacuum mass, distinct from the rolling tracker’s bare A_uu curvature. In d=4 it is below H_E²; the minimum does not establish a rapid-oscillation cold component. At constant F the corresponding Jordan mass/Hubble ratio is identical under the constant frame rescaling. No other cold mechanism is excluded.

## Newton and fifth-force scope

The individual tensor equation has Einstein coefficient 2KF. The trace-reversed nonrelativistic equation in n=d−1 spatial dimensions gives Delta Phi=(n−2)rho/[(n−1)2KF]. Therefore the Gauss convention Delta Phi=Omega_(n−1) G_N rho yields the stated individual G_N,tensor. The common/mirrored total source has coefficient4KF and half this normalization; these source conventions cannot be interchanged.

In the restricted Einstein-frame common-source problem, ln matter conformal factor=−ln F/(d−2), and the canonical scalar charge per unit mass is −q_F/[(d−2)sqrt(Z_E)]. Dividing its static exchange coefficient by the Einstein tensor coefficient (d−3)/[(d−2)M0] gives the relative boost M0 q_F²/[(d−2)(d−3)Z_E], with the momentum screening factor p_E²/(p_E²+m_psi²). The positive kinetic bound makes the unscreened boost strictly below1+1/[(d−1)(d−3)]. This is a locally frozen, stable-vacuum, high-momentum common-source calculation. Ordinary-visible-only matter excites the omitted relative/clock sector. It does not authenticate the full visible measured Newton constant, MOND acceleration law or an observational32pi dictionary.

## Remaining interpretation

The constructive result is real finite-cutoff stabilization in a declared action, accompanied by failure of the unshifted quadratic to reach the target conditional coefficient and a stable arbitrary-cutoff counterfamily when its free origin is allowed. The numerical maximum/minimum candidates are independently precision-checked residuals, not certified root isolation. The revised minimum control uses the computed retained negative slope derivative rather than a hardcoded rejection flag. The pre-execution contract rejection is preserved and excluded from evidence.

Full relative/clock health, ordinary-source conservation and admission, evolving cutoff dynamics, microscopic fixation of F and operational calibration remain unproved. Stabilization therefore advances the vacuum mechanism without selecting32pi or deriving a physical cold abundance.
