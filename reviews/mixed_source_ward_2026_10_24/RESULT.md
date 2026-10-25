# Full-source symmetry test: covariant mixing and the missing Ward identity

## Status

No symmetry selecting the requested vacuum/force ratio has been found. This audit closes a specific gap in the previous direct-portal analysis: it keeps the gravitational mixing and lapse constraint, rather than applying positive scalar spectral weights to a constrained gravitational variable. It identifies the exact cancellation and source-matching identities a new symmetry must enforce. Ordinary covariance and scalar shift do not enforce them. A local transformation inferred only from the null quadratic matrix is not a symmetry of the cubic, sourced theory.

Frozen criteria commit 5b477f2ae9; base f71cf5ac6f. Kappa=1/2 remains FITTED. CFG493 kappa_Lambda=0.417 +/- 0.095 and kappa_crit=0.345 +/- 0.078 are distinct and unused. This is an analytic audit, not a numerical prediction, loop computation, or full stability proof. Units c=hbar=1; no microscopic hbar cancellation or second parameter-free observational prediction is claimed.

## 1. Covariant starting point and constrained static reduction

The primary reference is [Skordis and Zlosnik, 2007.00082v3](https://arxiv.org/html/2007.00082v3), equations (5)-(6), version dated 2021-10-14. It provides a unit-vector/scalar gravitational theory with metric-only matter coupling and a sourced scalar through mixing. We generalize the coefficients to test what its stated covariance and constant-scalar-shift symmetries permit; this deformation analysis is our calculation, not a claim made by the paper.

Let N be a positive fixed normalization of mass dimension two, U a unit timelike vector, J^mu=U^nu nabla_nu U^mu, F_mu nu=2 nabla_[mu U_nu], and Y=(g^mu nu+U^mu U^nu)partial_mu chi partial_nu chi. Here chi and metric potentials are dimensionless. Consider

    S = N integral sqrt(-g) [zeta R - k F^2/2 + 2h J.grad chi
                            - d Y - F_rest(Y,Q) - constraint] + S_m[g].

The source theory has zeta=1 and h=d=2-k. The temporal sector and the vector constraint are retained in the covariant definition. The following reduction assumes the same aligned, weak-field, quasistatic and mass-negligible regime as the parent audit; it is not valid across the source theory's mass-controlled outer transition.

Use g_00=-(1+2 Psi) and g_ij=(1-2 Phi)delta_ij. In three spatial dimensions the quadratic static gradient Lagrangian, before eliminating Phi, is

    L_grad/N = 2 zeta |grad Phi|^2 - 4 zeta grad Phi.grad Psi
               + k |grad Psi|^2 + 2h grad Psi.grad chi - d |grad chi|^2.

This follows from the Einstein term after integration by parts, F^2=-2|grad Psi|^2 and J.grad chi=grad Psi.grad chi at the order used. Matter contributes -rho Psi. Variation of Phi imposes Delta(Phi-Psi)=0 for zeta nonzero; the usual decaying boundary condition sets Phi=Psi. Thus

    L_stat = -N[(2 zeta-k)|grad Psi|^2 - 2h grad Psi.grad chi
                 + d |grad chi|^2 + F_rest] - rho Psi.

An independent change of zeta changes the first coefficient while leaving the mixing and scalar terms unchanged. This is an explicit allowed Einstein-Hilbert deformation. It is not an estimate of its generated loop coefficient or sign. The equality Phi=Psi remains the static constraint for this deformation in the stated limit.

## 2. Solve the source and cancellation together

Write the remaining static energy, now naming the physical lapse potential Phi,

    E = [A|grad Phi|^2 - 2B grad Phi.grad chi + C|grad chi|^2]/2
        + alpha |grad chi| + gamma |grad chi|^3/3 + rho Phi + V,

with A=2N(2 zeta-k), B=2Nh, C=2Nd, and A>0. Assume B>0 by scalar orientation and gamma>0. The cubic normalization includes its coefficient in N F_rest. In any spatial dimension completing the square gives

    Phi_hat = Phi - g chi,           g = B/A,
    beta_eff = C - B^2/A,

    E = A|grad Phi_hat|^2/2 + beta_eff |grad chi|^2/2
        + alpha |grad chi| + gamma |grad chi|^3/3
        + rho(Phi_hat+g chi) + V.

Thus the source strength and residual stiffness cannot be audited separately. The exact zero-stiffness condition is

    A C - B^2 = 0,

while a nonzero baryonic scalar source requires B nonzero. A null quadratic determinant by itself does not make chi unphysical: its cubic equation still carries the source.

For alpha=beta_eff=0, a spherical mass m in n spatial dimensions gives

    S_(n-1) r^(n-1) gamma (chi')^2 = g m,
    a_chi = g chi'.

In n=3, with high-acceleration G_N calibrated separately,

    a_chi^2 = a0 G_N m/r^2,
    a0 = g^3/(4 pi G_N gamma).

The diagonal potential has Newton coefficient 1/(4 pi A), which need not equal the measured high-acceleration G_N. Equating them without a high-gradient completion would silently remove a real matching obligation.

For comparison to the earlier canonical parameters, if the temporal coefficient is K>0, set chi_c=sqrt(K)chi. Then g_c=g/sqrt(K) and gamma_c=gamma/K^(3/2), so g_c^3/gamma_c=g^3/gamma. None of the following conclusions is a field-normalization artifact.

## 3. A covariant deformation breaks the cancellation

Start on C=B^2/A. Change only A to A+delta A with A+delta A>0. Exact completion of the new square yields

    g_new = B/(A+delta A),
    beta_new = B^2 delta A/[A(A+delta A)].

A positive delta A generates positive quadratic stiffness and retains a nonzero scalar source. In the covariant action delta A=4N delta zeta, with B and C fixed. Thus both covariance and scalar shift survive a deformation that destroys exact low-gradient MOND. If the source action's rank-one form is restored by changing d or h as well, that is an additional correlated matching condition; it does not follow from simply redefining Newton's constant.

This demonstrates absence of protection by the listed symmetries, not that every microscopic completion necessarily generates a nonzero delta zeta or that the complete deformed cosmological theory is stable. No gravitational spectral positivity assumption has been used.

## 4. Does the null direction define the missing gauge symmetry?

On beta_eff=0 the quadratic static energy depends only on Phi-g chi. Its null transformation is

    delta chi=epsilon(x),       delta Phi=g epsilon(x),

with g constant. The quadratic gradient part is invariant. But for a compactly supported epsilon on a nonzero-gradient patch, the rest varies as

    delta E_integrated = integral [gamma |grad chi| grad chi.grad epsilon
                                  + g rho epsilon]
                      = integral epsilon[-gamma div(|grad chi|grad chi)+g rho].

This vanishes on solutions because it is the scalar field equation. Gauge invariance would require an off-shell identity, not that equation. Even in the absence of matter, the cubic variation is generically nonzero. A temporal kinetic term supplies further conditions, not a repair of this static failure.

Therefore promoting this quadratic null direction alone to a local gauge symmetry fails. This does not exclude a nonlinear symmetry with additional transforming fields, or a gauge-invariant physical scalar combination. Such a completion must be specified and tested; a Stueckelberg label does not establish the required identity.

There is a second restricted exclusion. For ordinary constant linear internal transformations Q -> S Q preserving a positive temporal kinetic metric H, invariance requires S^T H S=H. The spatial operator sum_i (partial_i Q)^T H(partial_i Q) is then invariant too. Constant shifts also preserve it. Such internal symmetries alone cannot forbid all quadratic spatial stiffness while retaining that positive temporal metric. This argument excludes neither spacetime-dependent/nonlinear transformations nor constrained gauge systems; it identifies why an ordinary multiplet assignment is insufficient.

## 5. Exact conditions a successful Ward identity must supply

For infinitesimal variations of microscopically admissible matched coefficients, holding field conventions fixed, the zero-stiffness surface has tangent condition

    delta C - 2g delta B + g^2 delta A = 0.

Protection of the other missing term additionally requires delta alpha=0 at alpha=0. These conditions must hold for all allowed corrections if the zero surface is to be invariant. They do not alone set its initial matching value.

The physical vacuum/force ratio is

    kappa = a0/sqrt(G_N V)
          = (B/A)^3/[4 pi gamma G_N^(3/2) sqrt(V)].

For its value to be unchanged across admissible microscopic choices, the further condition is

    3(delta B/B - delta A/A) - delta gamma/gamma
      - (3/2)delta G_N/G_N - (1/2)delta V/V = 0.

At fixed measured G_N the third term in G_N vanishes. In canonical variables this is exactly the condition for fixed R=u^3/(v sqrt(e)); it is not a new value of R. Renormalization-scale independence of a correctly computed observable is also not a prediction: different theories may each have scale-independent observables with different values. A Ward identity must both restrict physical microscopic variations and select the absolute ratio, not merely express that bookkeeping invariance.

The original covariant/shift symmetries allow independent volume, Y and Y^(3/2) operators, and also Y^(1/2) on the nonanalytic static branch when such local response functions are admitted. The latter requires care at Y=0, as does the desired cubic; no differentiable vacuum effective action is assumed to admit it automatically. The key point is that ordinary scalar shift does not distinguish their coefficients. Independent cubic and volume deformations already defeat amplitude selection even if the two lower-gradient coefficients have been arranged to vanish.

## 6. What has narrowed and what remains open

The result removes three insufficient explanations for protection: covariance alone, an apparent local gauge freedom inferred from the quadratic null direction, and ordinary constant linear internal multiplets with positive temporal metric. It does not find the extra symmetry the user requested or reduce the surviving continuous amplitude to a number.

A surviving construction must produce a genuinely nonlinear/spacetime symmetry, constrained matching identity or microscopic dynamics that enforces all the displayed relations in the full sourced theory. Previous Weyl and conformal examples are not re-counted as fresh solutions; their independent amplitude and source obstructions remain recorded in formal/geometric_source/WEYL_SOURCE.md and formal/symmetry_protection/CRITICAL_SYMMETRY.md under why_4_puzzle/W4_08_positive_mond_amplitudes/.

The unresolved dependency is now explicit: an actual transformation law and complete action whose off-shell identity fixes the source and response matching, and whose stable positive vacuum selects V together with gamma. General covariance gives stress conservation, but the Einstein-Hilbert deformation above shows that it is not that missing identity.

Evidence is analytic and self-reviewed in REVIEW.md. No independent review, loop matching, full halo stability or parameter-free a0 has been established.
