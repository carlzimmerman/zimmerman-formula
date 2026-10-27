# FGF048 narrow density and actual-field feedback audit

**Normalized claim:** On the actual classical C1/C1,1 solution interval
0<=t<=kappa N^-4 in the author's fixed dimensionless units, the author's
gates A<=a N^4, Bf<=beta, Htot<=C_H N^7 imply the stated N-independent
density/scale/g margins and actual-force bounds O(N^-4), O(N^-1) for the
force and its first spatial derivative, with the exact dynamic source,
constraints, pressure, profile joins, local domain and energy controls.

**Primary verdict: proved as written for this narrow implication.** The
full nonlinear existence/trace/restart theorem is out of this audit's scope.
The author provides a proof of that upstream theorem; its separate full audit
must determine acceptance. This is not a second full existence acceptance.
No correction to the author's density/feedback formulas is required.

## Provenance and exact target

Independent derivation SHA256
`a32ae38dc510428987324edcfb2efd26ffc2c870bdfba4cf98fdf50faa9e39e4`
was frozen at 04:43:43 UTC before new stage35 proof exposure. Freeze SHA256
`c34a6de05e275e76f44f579055dd8a9abaa62832308bf3250f0fc8eddb749ca8`.
At 04:48:59 UTC the final author DERIVATION.md pin
`010afcd5c5de6a1618272511e30371feae09f45195405373e15e68f8beb31de2`
and result.json pin
`661277e12a22bc33b4cac093dde1540f5a501f513eeb52d22230cb65e6a1bce2`
matched before either was read. FAILED_ESTIMATES.md later matched
`6cf3ae6f55e1a26e3c6bfdefde581300560d57854112260f1a81d9301b25147d`
before it was read. No coordinator or other current reviewer proof was read.
Old-source read-before-hash chronology remains disclosed in the frozen record.

## Dependency graph and decisive checks

Exact four equations + compatible classical interval
-> exact diagonal field system (2.1)
-> upstream norm gates A,Bf,Htot
-> density transport (4.3), refined q_x (6.2)
-> field derivative-Lipschitz estimate (6.3)
-> time-integrated feedback (6.1),(6.4)
-> restored physical rates (8.1).

The chart displacement, compatible constraints and characteristic cone give
positive-state margins and physical localization. The energy and zero-velocity
checks are independent direct identities within the same solution class.
No external theorem, numeric sample or initial Taylor jet is a leaf here.

1. **Density.** In the author's units |v_x|<=A<=a N^4. Along actual fluid
   trajectories q-q0(initial footpoint)=-integral v_x. Hence its absolute
   excursion is at most a kappa<=1/2, exactly as (4.1),(4.3) require. The
   physical density bounds nref exp(q_- -1/2), nref exp(q_+ +1/2) follow.
   There is no exp(O(N/c)) loss. The trajectories are legitimate on the
   auxiliary line; the final cone removes dependence on the exterior.

2. **Pressure and joins.** The actual fixed c>0 is retained in r=v+cq and
   s=v-cq. Their inverse q_x=(r_x-s_x)/(2c) has the exposed bound A/c.
   The exact initial C1,1 velocity has Lip(v_x)=8 N^7. The author's
   Htot(0)<=h0 N^7 and propagation retain this power. The pair-flow estimates
   do not require a classical f'' at the endpoints of support.

3. **Refined density derivative.** D_v q_x=-v_x q_x-v_xx holds a.e. in
   this regularity. |v_xx|<=Hf<=C_H N^7 leads to
   ||q_x||<=(||q0_x||+C_H N^7 t) exp(a N^4 t)<=C_q N^3.
   Characteristic integration and continuity supply the stated representative.
   Since n is uniformly bounded, this also implies ||n_x||=O(N^3).
   No uniformly bounded scaled q_yy is inferred from it.

4. **Field norm gates used by the feedback calculation.** For a diagonal
   field equation z_i,t+lambda_i(z)z_i,x=H_i(q,z), the Lipschitz derivative
   inequality contains 3L1 Bf Hz+L2 Bf^3 from transport and
   P(Hz+Hf/c)+Q(Bf+||q_x||)^2 from the source. This reproduces the relevant
   line of (5.1). The factor Hf/c is retained in (6.3); using q_x=O(N^3)
   changes its quadratic source bound to O(N^6), while the retained Hf/c
   term is O(N^7). Thus Hz<=[Hz(0)+D_z N^7 t]exp(E_z t) is valid with
   exactly the displayed D_z,E_z. All are fixed constants.

5. **Force itself.** The exact constraint gives g_t=p_x, with
   p=(Rplus+Rminus)/2, so ||p_x||<=Bf<=beta. Integrating yields
   ||g-g0||<=beta t<=beta kappa N^-4. It is an integral bound on the actual
   solution, and does not use vanishing initial field jets to assert a
   Taylor remainder estimate. Its conservatism is acknowledged correctly.

6. **First spatial derivative.** Lip(p_x)<=Hz and the initial force is g0.
   Distributional differentiation of g-g0=integral p_x, followed by the
   continuous representative of g_x-g0_x, gives
   ||g_x-g0_x||<=exp(E_z kappa)[Hz(0)t+(D_z/2)N^7 t^2].
   At t<=kappa N^-4, the two terms are O(N^-4),O(N^-1); for N>=1 their
   sum is bounded by the coefficient stated in (6.5) times N^-1. Including
   Hz(0) is conservative because the estimate bounds all field gradients,
   although p_x initially vanishes. There is no missing initial term.

7. **Physical units.** With x_physical=L X, t_physical=(L/v0)theta and
   g_physical=(v0^2/L)g, the force bound becomes
   (v0^3/L^2)beta t_physical, and the force-gradient prefactor is v0^2/L^2.
   Both formulas in (8.1) have the correct factors and N powers.

8. **Scale and constraints.** The author includes B_chi k/tau,
   h_chi(w-bk) and -h_chi(w+bk). The scale pair propagates chi_x=k;
   subtracting the R pair then gives g_t=p_x, and adding it gives
   p_t=b^2 g_x+A+b h_chi(chi_x-k). The latter extra term vanishes only
   after the scale constraint has been established. Reconstruction gives
   phi_x=g. Therefore B_x=Cn+tau phi_tt is the actual evolving source.
   The fixed compact chart displacement <=delta/2 propagates chi and g
   margins; a=a_ref exp chi remains positive with N-independent bounds.
   The author makes no stronger quantitative scale response-rate claim.

9. **Domain.** |v|<=N+c Q0+gbar and fixed bounded field speeds imply
   speeds strictly below S_N. For t<=kappa N^-4,
   S_N t<=s0 kappa N^-3<=R/4. The shrinking cone therefore contains the
   stated fixed core and all backward/vertical segments stay in the same
   regular physical patch. Exterior independence is correctly restricted
   to common backward domains and each extension's own kappa. The force
   g>0 margin is not confused with an additional assumption g0_x>0.

10. **Energy/control.** Matter plus interaction contributes +np, Q
    contributes -np-Tw/C and scale contributes +Tw/C. Fluxes -pB/C and
    -Jwk/C are both present. Moving-boundary energy terms have the correct
    signs. The hydrostatic zero-velocity tuple solves all four equations
    locally with zero flux; extension uniqueness confines that control to
    its causal footprint. Initial O(N^-1) kinetic excess is not used as a
    regularity argument.

## Comparison with the frozen independent route

The author's variables satisfy the frozen sufficient bounds as follows:

  u_y+(c/N)q_y=N^-4 r_x,
  u_y-(c/N)q_y=N^-4 s_x,
  Lip_y(u_y±(c/N)q_y)=N^-7 Lip_x(r_x or s_x).

Consequently, **if the separately audited uniform interval and author's
upstream estimates are accepted**, the author's a and C_H furnish the frozen
M,H. The stronger frozen O(N^-5) force route on a hydrostatic-contained
physical cone is therefore compatible with those gates. It uses subtraction
of the stationary background and estimates the field derivative difference;
the author instead uses the simpler total-gradient bound beta and only
claims O(N^-4). This audit does not silently replace the author's theorem
or publish an unconditional stronger rate. Its primary target is exactly the
author's stated conservative estimates.

The frozen first-derivative bound retained epsilon^-1=N/c through
Lip_y q_y<=H/epsilon. The author's retained Hf/c=O(N^7/c) is the same
loss in unscaled coordinates and correctly leads to the same O(N^-1)
force-gradient power. Neither derivation justifies an O(N^-2) rate by
pretending the scaled q_yy norm is uniform.

## Obligation matrix

| Obligation | Verdict |
|---|---|
| Independent derivation freeze before author exposure | Passed, immutable pins above |
| Final author hashes before reading | Passed |
| Density and pressure treatment | Passed |
| Exact joins and gradient regularity | Passed for estimates used here |
| Actual dynamic MOND source and chi terms | Passed |
| Claimed force and force-gradient rates | Passed from the stated upstream gates |
| Positive margins/domain/extension scope | Passed from the stated gates |
| Full energy and hydrostatic control | Passed |
| Uniform nonlinear existence, trace and restart | Out of scope; separate full audit |
| Stronger frozen O(N^-5) route | Preserved separately, conditional as stated |
| Endpoint, shock, crossing or global transfer | Out of scope and not claimed |

No discrepancy was found in the scoped final author formulas. The exact
remaining dependency for whole-task acceptance is the independent full audit
of the upstream construction/continuation theorem. This audit used zero
mathematical executable computations, no external source, and no observational
input. It applies separately to the two positive a_ref normalizations and
each fixed frozen comparison background; no evolving protocol or physical
vacuum/DOF/metric/photon/MONO/criterion-B/closure claim is accepted here.

Self-proofreading: reviewed all formulas, coefficients, N powers, source pins
and scope language in this comparison. No mathematical-token correction to
the author's files was made; no author file was edited.
