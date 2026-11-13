# Einstein-constrained scalar health of the density gate

This is a new derivation from the operative QX17 action, not a certification of the historical TPA/SCS labels. Units and target are in `CONTRACT.md`. `H` below denotes the gate Lagrangian; the expansion rate is `h`. Write `M2=1/(2K)` and use proper spatial wavenumber k. No extra matter perturbations are included; adding them adds physical modes and constraints.

## 1. Exact ADM action and the physical variable count

Use unitary clock gauge `tau=tau(t)`, `q=dot(tau)>0`, `Q=q/N`. Tangency gives `P^0=0`, and

```text
Pi = (sqrt(gamma))^-1 partial_i(sqrt(gamma) P^i).
```

Thus Pi has neither lapse nor shift, and P has no time derivative. It is useful to take the spatial vector density `J^i=sqrt(gamma) P^i` as the independent polarization variable. Integrating by parts in space gives the exact equality

```text
integral N sqrt(gamma) P^i partial_i ln N = -integral N sqrt(gamma) Pi.
```

Surface terms are retained as boundary data or vanish for compactly supported perturbations. The bulk action is therefore

```text
S = integral N sqrt(gamma) {
      M2/2 [R3 + Kij Kij - Ktrace^2 - 2 Lambda]
      + U(Q,Pi) - W(|P|) },
U(Q,Pi) = H(Q,Pi) - Pi - gamma Pi_+^2/2.
```

This form exposes both the lapse coupling of the polarization charge and the fact that the matter action has no shift dependence. The full momentum constraint is the Einstein momentum constraint, not an omitted equation. The lapse and three P components are auxiliary; transverse shift components impose the usual vector constraints. On the regular branches used below there are two tensor polarizations and one clock scalar. No new P kinetic mode has been assumed. Singular coefficient surfaces require a separate constraint reduction.

## 2. Exact flat-FRW scalar action, including S' and S''

The on-shell homogeneous solution has P=Pi=0 and obeys

```text
3 M2 h^2 = rho + M2 Lambda,       -2 M2 dot(h) = q H_Q,
rho = q H_Q - H,                 d(a^3 H_Q)/dt = 0.
```

All H derivatives in this section are at `(q,0)`. Set `N=1+alpha`, `gamma_ij=a^2 exp(2 zeta) delta_ij`, and scalar shift `N_i=partial_i beta`. For a smooth stiffness Hessian Gamma at zero define

```text
A0 = q^2 H_QQ,
c  = 1 - H_Pi + q H_QPi,
D  = H_PiPi - Gamma,             w = W_|P||P|(0) = K.
```

The original one-sided stiffness has no single Hessian at Pi=0. Here Gamma=0 means gamma=0 or the archive's smooth flat blend; Gamma=gamma would be an explicitly different, everywhere-quadratic stiffness. This distinction is not needed at the strictly positive-Pi backgrounds below.

Let `d=div(delta J)/a^3`. Direct expansion of the matter density gives, up to spatial boundaries,

```text
L2_matter/a^3 = A0 alpha^2/2 - c alpha d
                + D d^2/2 - w |delta P|^2/2.
```

The H_Pi term is essential: c is not merely `1+q H_QPi`. The exact gate contribution to alpha*d is `H_Pi-q H_QPi`; the `-Pi` term supplies the remaining -1. Terms involving zeta*d at Pi=0 cancel into a boundary.

The Einstein kinetic and shift terms before constraint elimination contain

```text
-3 M2 (dot(zeta)-h alpha)^2
-2 M2 k^2 beta (dot(zeta)-h alpha).
```

The nonzero-k momentum constraint is consequently `alpha=dot(zeta)/h` when h is nonzero. The P constraint eliminates d away from `w-D k^2=0`; the lapse equation determines beta. Substituting all constraints and using the background equations gives the exact one-scalar quadratic action

```text
S2 = 1/2 integral a^3/h^2 [ A(k,t) dot(zeta)^2 - q H_Q k^2 zeta^2 ],
A(k,t) = A0 + c^2 k^2/(w-D k^2).                              (1)
```

The tensor sector retains its positive Einstein kinetic term and unit speed. For the scalar, the time-dependent equation is

```text
d/dt [a^3 A/h^2 dot(zeta)] + a^3 q H_Q k^2/h^2 zeta = 0,       (2)
```

where `k=k_comoving/a`. The often written `omega^2=q H_Q k^2/A` is only a frozen-coefficient approximation to (2). If its frequency is comparable to h it cannot decide cosmological growth; a positive gradient coefficient for zeta is not a proof that density perturbations do not undergo Jeans growth.

For `A0>0,D>0,c!=0`, A is negative just above `k^2=w/D`. At the excluded polarization pole the unreduced equations must be used; a pole of one auxiliary block is not by itself a singularity theorem for the entire system. A negative reduced kinetic coefficient identifies an indefinite scalar Hamiltonian in this representation. Calling that alone a fundamental ghost, rather than an instability of a canonical conjugate variable, would overstate the result. An unbounded physical growth rate is a stronger, coordinate-independent obstruction, established below for an actual finite-density branch.

For the flat gate `S=exp(-u^3)`, `S'(0)=S''(0)=0`; (1) becomes `A=q^2 F''+k^2/K>0` on the positive F'' branch. This FRW result does not establish health where the gate is active.

## 3. Finite positive-Pi center: all constraint data supplied

Use a regular spherical initial slice, with spatially constant lapse `N=1`, constant q, constant expansion `Kij=h gamma_ij`, and conformally flat spatial metric `gamma_ij=psi(r)^4 delta_ij`. Let v(r) be the physical radial polarization magnitude. On the strictly positive branch,

```text
D(Q,Pi) = H_PiPi - gamma,
rho = q H_Q - H + Pi + gamma Pi^2/2 + W(v).
```

The complete initial Hamiltonian, momentum and polarization constraints reduce to the following local ODEs:

```text
psi'' + 2 psi'/r = psi^5 [6 h^2 - 4K rho]/8,
v' = psi^2 Pi - 2v/r - 4(psi'/psi)v,
Pi' = -W_v(v) psi^2/D.                                       (3)
```

The second line is the exact geometric divergence identity. The third follows from varying J in the ADM action: `partial_r[N(1+gamma Pi-H_Pi)] = N W_v psi^2`. With N and q constant this is `-D Pi'=W_v psi^2`. The momentum constraint vanishes exactly because h is spatially constant and the matter action has no shift. This is not a freely assigned off-shell P Hessian.

Set `psi(0)=1`, `psi'(0)=0`, `v(0)=0`, `Pi(0)=p>0` and `h^2=2K rho(0)/3` (Lambda=0). Then the intrinsic Ricci tensor vanishes at the center. Regular Taylor coefficients are

```text
v = p r/3 + O(r^3),
Pi = p - K p r^2/(6D0) - K^2 p^2 r^3/(27 a0 D0) + O(r^4),
psi = 1 + O(r^4).                                           (4)
```

For nonzero D0 and `K v<a0`, ordinary local ODE existence supplies a regular constraint solution. The cubic radial term comes from the original W's |P|^3 term; the construction is twice continuously differentiable at the center, not asserted Cartesian C-infinity. The numerical witnesses initialize the leading displayed terms, integrate (3), and independently differentiate the resulting fields to test the original constraints. They are local constrained initial data and consistent evolution jets, not a globally evolved halo or a nonlinear well-posedness theorem. The Einstein evolution equation fixes the central time derivative of h; it is not chosen to obtain the desired dispersion.

The central clock equation is compatible with these Einstein data. Write `B=1+gamma p-H_Pi`. The current and the normal P multiplier give `rho_Q=H_Q+Bp/q` and `lambda/q=d_t(B/q)`. In the clock equation, the time derivative of Bp/q cancels its corresponding multiplier-flux term, leaving

```text
q H_QQ dot(q) + c dot(p) + 3h n_eff = 0.
```

Direct differentiation of the Hamiltonian energy gives `dot(rho)=qH_QQ dot(q)+c dot(p)`, so this is exactly the central Einstein energy-conservation equation. It provides a compatible temporal-jet condition rather than an extra contradictory constraint. Neither this identity nor the initial-data integration is a simulation of the later evolution or a proof of a global spacetime extension.

## 4. GR-inclusive local principal scalar and active stiffness

At this regular center, P=0 but Pi=p>0. Use the same density variable J. Expanding Pi gives

```text
delta Pi = d - 3p zeta,
A0 = q^2 H_QQ,
c = 1 + gamma p - H_Pi + q H_QPi,
D = H_PiPi - gamma.
```

The extra zeta*d, alpha*zeta and zeta^2 terms are zeroth order in proper k after the P constraint is eliminated when D!=0. They cannot be discarded at finite wavelength, but do not alter the high-k characteristic derived here. Because N is spatially constant and the intrinsic Ricci tensor vanishes at the center, the leading scalar momentum constraint is the same `dot(zeta)-h alpha=0`. Thus the lapse/shift/P Schur complement has

```text
A(k) = A0 + c^2 k^2/(K-D k^2),
A_infinity = A0 - c^2/D,             D != 0.                  (5)
```

The local pressure must also be derived, not borrowed from a pure k-essence clock. Variation with respect to the spatial metric at fixed J gives, at the center,

```text
p_eff = H - p H_Pi + gamma p^2/2,
n_eff = rho+p_eff = q H_Q + p(1+gamma p-H_Pi),
dot(h) = -K n_eff.                                           (6)
```

The last relation is the central Einstein evolution equation (flat intrinsic curvature, constant lapse). The Einstein spatial-curvature terms are `M2 k^2 zeta^2+2M2 k^2 alpha*zeta`. After substituting alpha and integrating the time-dependent cross term by parts, they give `M2 dot(h) k^2 zeta^2/h^2`, hence the physical principal action

```text
S2_principal = 1/2 integral a^3/h^2
              [A_infinity dot(zeta)^2 - n_eff k^2 zeta^2],
omega^2 = (n_eff/A_infinity) k^2 + lower-order terms.         (7)
```

Both the lapse/shift reduction and the time derivative of the cross coefficient are load-bearing. Merely freezing the coefficient of `alpha*zeta` before varying time gives the wrong gradient sign. For a packet whose wavelength is much shorter than the curvature and polarization variation lengths, the omitted terms are lower order. Tensor characteristics remain the Einstein light cone. The only additional propagating characteristic is this scalar, not an unconstrained P perturbation.

There is an independent principal reduction. The exact polarization equation is `partial_i(N U_Pi)=-N W_Pi`; at P=0 the W Hessian is finite. At high k the longitudinal derivative term dominates, so each nonzero-k mode obeys `delta(N U_Pi)=0` to leading order. Fix the local spatial integration function `chi(t)=N U_Pi` and eliminate Pi from the partial Legendre density `N U-chi Pi`. The subtracted `chi*sqrt(gamma)*Pi` is a spatial boundary for spatially constant chi. Implicit differentiation gives `Pi_N=c/D` at N=1 and

```text
d²(N U-chi Pi)/dN² = q²H_QQ-c²/D = A_infinity.
```

Its pressure is `U-Pi U_Pi` and its lapse energy is `qH_Q-U`, reproducing (6). Thus the high-k theory is an Einstein lapse-potential scalar with precisely the coefficients in (7). This derivation also explains why the physical Schur complement, rather than the fixed-Q P Hessian, controls the scalar. Spatial variation of the background integration function and W corrections are lower order for the specified regular-center packet. It does not replace the finite-k P equation with zero everywhere on the background.

Regular, positive-energy scalar principal conditions in this construction are

```text
A_infinity > 0,  n_eff > 0,  D != 0,
```

along with nonsingularity of the constraint operators on the chosen spatial domain. If `n_eff>0` and `A_infinity<0`, a physical scalar mode grows at `|Im omega| ~ sqrt(n_eff/|A_infinity|) k`. This is an unbounded short-wavelength instability, not ordinary H-scale Jeans growth. If both coefficients are negative, real characteristics alone do not provide positive energy. Degenerate cases `D=0`, `A_infinity=0`, h=0 and finite-wavelength constraint zeros require separate reductions; this calculation does not silently divide through them.

If D<0 and H_QQ>0, (5) guarantees positive A_infinity. If D>0, positive A_infinity requires `A0 D>c^2`; positivity of the fixed-charge P block instead requires the opposite sign at large k. There is no general implication from the sign of the P block alone. Positive A_infinity is only a principal necessary condition; the finite-wavelength spectrum, preserved state domain, nonlinear evolution and observational matching remain separate.

## 5. Hamiltonian comparison and why a partial Legendre transform is insufficient

In a locally normalized scalar kinetic sector write

```text
L = A dot(s)^2/2 + c dot(s) d - (w/k^2-D)d^2/2.
```

The momentum n gives

```text
E(n,d) = (n-cd)^2/(2A) + (w/k^2-D)d^2/2.
```

The fixed-n curvature in d is `c^2/A+w/k^2-D`, which can be positive even when `w/k^2-D<0`. Eliminating d gives `E_nn=(w-Dk^2)/[A w+(c^2-A D)k^2]`, the inverse of the actual reduced kinetic coefficient. Its sign is not determined by fixed-n curvature alone. Conversely, a negative reduced phase kinetic term can be represented as a negative potential for the conjugate density; terminology must be tied to the physical dispersion and Hamiltonian signature. Equation (7), when negative and proportional to k^2, avoids confusing this effect with a bounded Jeans instability.

## 6. Surviving route and exact scope

The flat gate does evade the FRW quadratic problem. It does not guarantee a healthy theory on all of its allowed finite-density states: the constrained examples in `result.json` exhibit an unbounded scalar instability with `q-1=10^-6` and strictly active positive stiffness. A second example has D<0, positive A_infinity and n_eff, so this calculation does not rule out a restricted healthy principal domain. It specifies what such a domain must preserve.

The next mathematical obligation is to derive and preserve that domain using the same action and transport/background solution. An independently justified cutoff or a different stiffness law changes the question; neither is inferred from this calculation. No kappa normalization, EFE matching, global formation mechanism or all-wavelength stability is derived here.

The analytic extension to general strictly positive flat-origin gates is in `FAMILY_OBSTRUCTION.md`; its independent-review status is stated there. Standard Einstein/clock normalization checks against primary papers are recorded separately in `SOURCE_CHECK.md` and are not treated as proofs of the new polarization calculation.
