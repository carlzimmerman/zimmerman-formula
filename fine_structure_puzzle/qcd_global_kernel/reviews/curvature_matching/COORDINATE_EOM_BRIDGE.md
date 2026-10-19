# A minimal explicit coordinate/EOM bridge

This is a posttarget extension of the saved pretarget derivation. It establishes
why a potential-only off-shell pole cannot automatically be assigned to the
printed full k15 beta function. It does not claim the full source-basis bridge
has been calculated.

Kubis-Meissner v2 equation (2.3) uses sigma-model pion coordinates,

    U=sqrt(1-r squared)+i tau.r, r=pi/F.

In this coordinate patch the target-space metric and inverse are

    g_ij=delta_ij+r_i r_j/(1-r squared),
    g^ij=delta_ij-r_i r_j, sqrt(det g)=(1-r squared)^(-1/2).

The contracted Christoffel symbol is exactly `g^ij Gamma^k_ij=3r_k`.
Consequently, for any potential V,

    Tr H_cov = F^-2[(delta_ij-r_i r_j) partial_i partial_j V
                                  -3 r_i partial_i V],
    Tr H_plain = F^-2(delta_ij-r_i r_j) partial_i partial_j V,
    Tr H_cov-Tr H_plain = -3 r_i partial_i V/F2.

The right-exponential split U0 exp(i tau.pi/F) used for the compact mode
computes the covariant target-space Hessian at constant background. A naive
sigma-coordinate expansion with its quadratic kinetic metric computes the
plain Hessian unless its connection, field-coordinate, source and measure
terms are completed consistently. The two explicit potential traces are

| Potential | Covariant/geodesic trace | Plain sigma-coordinate trace |
|---|---|---|
| -F2 M2 a0 | 3 M2 a0 | 3 M2/a0 |
| u C s | (uC/F2)(4-8s) | (uC/F2)(4-2s) |

Here a0=sqrt(1-r squared) and s=r1 squared+r2 squared. In the sigma coordinates
the EM potential is exactly quadratic, which the source explicitly observes;
the right-exponential expansion instead contains background-dependent higher
pion vertices. This is a coordinate difference in an off-shell calculation.

For d=4-2eps, the linear-curvature part of the potential-loop determinant is
R Tr H/(192pi2 eps). The difference of the two displayed potential-only
curvature poles is therefore

    Gamma_div,cov-Gamma_div,plain
      = -integral sqrt(g_spacetime) R r_i partial_i V/(64pi2 eps F2).

For constant background this is the potential part of a local field redefinition

    delta r_i = -R r_i/(64pi2 eps F2).

The full variation is `delta S2=integral delta r_i E_i`, with E_i the complete
LO Euler-Lagrange derivative, not just partial_i V. Define
alpha=1/(64pi2 eps F2). Varying the kinetic action gives, in addition,

    delta S_kin = -(alpha F2/2) integral sqrt(g_spacetime)
        R [r_k partial_k g_ij+2g_ij] partial_mu r_i partial^mu r_j
      -alpha F2 integral sqrt(g_spacetime)
        (partial_mu R) g_ij (partial^mu r_i) r_j.

The last term vanishes for round S4 but belongs to the general local source
basis. The derivative terms, the definition of the off-shell source/background,
and any measure/collective-coordinate Jacobian must accompany the potential
shift. A legitimate field redefinition of the full functional also changes
the measure/source representation. It is not valid to change just the s
coefficient and discard these partners.

Using the same bare pole convention, the **geodesic potential-only** s pole
would assign beta15,pot=4Z/3, whereas the **plain sigma potential-only** s pole
would assign Z/3. Neither is the source's printed full result 1/2+2Z/3. The
calculation thus demonstrates the coordinate/EOM sensitivity, but it does not
identify which completed combination of derivative loops, redundant operators,
field renormalization, photon/mixing/ghost terms and local source contacts maps
the collective-background action to the published form-factor basis.

The source's beta11=1/6 multiplying a curvature-kinetic operator makes that
kinetic completion load-bearing when an on-shell matrix element is used to
identify curvature-potential couplings. Its beta13=1/8 and charged mass
splitting fix useful normalizations but do not by themselves establish the
complete electromagnetic basis map. A purely U-independent gravitational
counterterm cannot repair an orientation-dependent mismatch by itself.

The exact identities above were checked independently in check_curvature.py.
They give a concrete partial EOM bridge, not a proof of equality with the
printed running and not evidence that the source is erroneous. A full common
off-shell basis, its redundant operators and its finite scheme conversion are
the remaining matching obligation.
