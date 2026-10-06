# Inhomogeneous canonical cutoff: one-sign force and compact stationary obstruction

## Result and exact changed-premise scope

The SAME UV-normalized canonical cutoff completion has no stationary finite-modulus solution on a compact periodic slice, even allowing an arbitrary admitted finite inhomogeneous projected invariant, two different metrics, and stationary shifts. Spatial gradients cannot provide an integrated stabilizer: their current divergence integrates to zero while the exact interaction force is strictly positive. With time dependence and no spatial boundary flux, a precisely defined integrated canonical momentum is strictly decreasing. This is not a theorem that the average cutoff decreases, a healthy full-field evolution theorem, or a32pi selector.

The proof concerns the action declared in the frozen dynamical_cutoff_vacuum parent, not every scalar completion. Finite T>0, constant positive canonical coefficient f², K>0 and n>=3 are required. It is conditional on the interaction's admitted local fixed-invariant branch; no derivative is asserted at a parametric fold or across an unspecified global source extension. No additional potential, explicit modulus-matter/shear coupling or field-dependent kinetic coefficient is added.

## Same action and the fixed-invariant derivative

Let u=lnT denote the cutoff modulus, separately from the common timelike foliation clock theta. In c=1, use the exchange-even projected acceleration invariant I>=0 from the parent and

    S=K integral[ sqrt(-g)R_g+sqrt(-ghat)R_hat]
      +2K chi_n a0² integral v M(I,T)
      -(f²/4) integral[ sqrt(-g)g^mu nu+sqrt(-ghat)ghat^mu nu]
                               partial_mu u partial_nu u
      +S_m[g]+S_hat[ghat],
    chi_n=(n-1)/[2(n-2)]>0,
    v=[(-g)(-ghat)]^(1/4)>0.

Matter is minimally coupled and has no explicit u dependence. The independent fields are both metrics, theta and u; I does not explicitly depend on u. Both metric equations remain required. They cannot cancel a missing modulus Euler equation, and substituting metric solutions before varying u is not the calculation used here.

At fixed T the retained radial constitutive lift is

    b(y)=sqrt(1+1/y)-1, e(y,T)=b(y)T²/(T²+y²), d=ye,
    q(y,T)=2 integral_0^y t e(t,T)dt,
    x=y+2d, I=x²,
    M=q+2d²-A(T), A=2 integral_0^infinity t e(t,T)dt.

The q+2d² terms vanish at zero and approach A in the UV, so this is the actual UV normalization M(infinity,T)=0. It is only a spherical constitutive dictionary; I is the actual local invariant in the covariant field equation, not a generally Newtonian nonspherical y. Any local inverse branch with finite y>=0,T>0 and x_y!=0 suffices for the derivative proof. The healthy global fixed-T inverse around the numerical cutoff128.915 is a subset, not an inferred global inverse for all T.

Since q_y=2d and M_y=2d(1+2d_y)=2d x_y, fixed x gives y_T=-2d_T/x_y. Thus

    M_T|I=q_T+4d d_T+M_y y_T-A_T=q_T-A_T,
    M_u|I=T(q_T-A_T)
          =-2T integral_y^infinity t e_T(t,T)dt
          =-4T² integral_y^infinity t³b(t)/(T²+t²)²dt<0.

Here e_T=2T t²b/(T²+t²)²>0, and the tail behaves as1/(2t²), so it converges. At y=0 use the continuous endpoint M_u=-A_u<0. At any finite y the tail is strictly positive. At arbitrarily large y the force can be small, but does not vanish at a finite regular field. No hidden y_T term has been discarded. A fixed independent offset has zero u derivative; the FIELD-DEPENDENT UV offset A(T) is essential.

If one instead uses a constant A independent of T, the action changes: M_u=Tq_T>=0 and the vacuum y0 equation becomes degenerate. That abandons the retained kernel-to-vacuum-offset relation, rather than solving its selector problem. A new W or u-dependent kinetic/matter/shear coupling likewise changes the equation and its sign premise. Such new physics is not excluded by this result.

## Exact covariant Euler density, both lapses and shifts

Variation before gauge fixing gives the vector density

    J^mu=(f²/2)[sqrt(-g)g^mu nu+sqrt(-ghat)ghat^mu nu]partial_nu u,
    E_u=partial_mu J^mu+2K chi_n a0² v M_u=0,
    partial_mu J^mu=F,
    F=-2K chi_n a0² v M_u>0.

The factor f²/2 and the mixed volume v are retained; neither metric is replaced by the other. The Einstein terms carry no explicit u variation. The actual full source/clock/metric constraints may narrow the admitted configurations, but cannot invalidate this necessary equation on an admitted solution.

In common-clock coordinates theta=t, write the two ADM metrics with lapse N,L, shifts S,R, and spatial metrics gamma,hatgamma. Both clock gradients remain timelike; N,L>0. Let Dg u=udot-S^i partial_i u and Dh u=udot-R^i partial_i u. The exact current components are

    J0=-(f²/2)[sqrt(gamma)Dg u/N+sqrt(hatgamma)Dh u/L],
    Ji=(f²/2)[N sqrt(gamma)gamma^ij partial_j u
            +sqrt(gamma)S^i Dg u/N
            +L sqrt(hatgamma)hatgamma^ij partial_j u
            +sqrt(hatgamma)R^i Dh u/L].

The PLUS signs in the shifted spatial current follow g^0i=S^i/N². At udot0 its own-metric spatial coefficient is N sqrt(gamma)[gamma^ij-S^iS^j/N²], and similarly hatted. This need not be spatially positive outside a timelike stationary-Killing patch. The integrated obstruction below does not require such positivity. A preflight deliberately exposed an erroneous shifted spatial-current sign; the direct inverse-metric calculation corrected it, and the failed version is preserved.

The invariant itself is exactly I=[(gamma^ij+hatgamma^ij)/2]partial_i ln(N/L)partial_j ln(N/L)/a0². It is independent of shifts in this foliation, but the canonical modulus current is not. The volume is v=sqrt(NL)[detgamma dethatgamma]^(1/4); setting N=L or dropping either lapse would erase part of the genuine density weighting.

Dimensions in c1 are [K]=[f²]=energy L^(2-n), [a0]=L^-1. F is energy L^-n and the integrated canonical momentum below has units energy times length (action), not mass or cold-particle number. No hbar enters. The general-n result uses only chi_n>0, not a numerical extrapolation from n3.

## Compact stationary theorem and stronger charge identity

Assume all admitted metric/clock-invariant coefficients and u are stationary in a common foliation chart, smooth and periodic on a compact spatial torus; more generally a compact slice without boundary works in current-form notation. They are finite and T>0 on the compact domain. Then J0 is stationary, and

    0=integral partial_i Ji d^n x=integral F d^n x>0,

a contradiction. Positivity is strict pointwise: finite continuous u gives positive upper/lower T bounds, finite x gives finite y, and v is positive. The only inputs are the necessary modulus equation and absence of boundary flux. Shift values, spatial ellipticity, the individual metric Einstein constraints and ordinary cold-source density cannot make a positive integral vanish. A constant modulus is actually impossible on ANY admitted finite-invariant geometry, since then J vanishes pointwise. On a zero-shift compact foliation, even time-dependent metric coefficients cannot support coordinate-stationary u, because J0=0 there as well.

For arbitrary time-dependent admitted fields define the weighted canonical momentum

    Q(t)=-integral J0 d^n x
        =(f²/2) integral[sqrt(gamma)Dg u/N
                        +sqrt(hatgamma)Dh u/L]d^n x.

Integrating the exact equation with no spatial flux gives

    Qdot=-integral F d^n x
        =2K chi_n a0² integral v M_u d^n x<0.

This flux formulation is invariant under spatial-coordinate changes; the time orientation is the common future foliation. It is not a conserved shift charge, since the potential explicitly breaks u shifts. It is not an average-u or average-T monotonicity theorem: weights, normal advection and field variations matter. It forbids exact periodic recurrence of u and all current-defining metric coefficients on that compact no-flux foliation. It does not show a stable attractor or regular global PDE evolution. In the coincident homogeneous limit Q=f² a^n udot and Qdot=-a^n V_u, recovering the parent homogeneous equation with V=2Kchi_n a0²A.

## Boundary exception and standard far-field restriction

With a boundary the exact identity is

    Qdot=-integral_D F+integral_boundary Ji n_i dS.

A stationary configuration REQUIRES positive outward J flux equal to the positive bulk force. Dirichlet walls or noncompact boundary conditions may supply it; this theorem does not exclude their boundary-value solutions. Such a boundary value is not a dynamical selector for T. The sign proof also does not apply to T0 at the u=-infinity boundary, infinite invariant y, or an undefined folded branch.

One useful further necessary gate is explicit rather than a blanket noncompact theorem. Suppose on R^n both stationary metrics and their coefficients tend to nondegenerate constants, I->0, u->u_infinity finite, and gradient u=o(r), uniformly on far spheres (ordinary C1 constant-modulus falloff is much stronger). Then F->F_infinity>0 and the volume integral is asymptotic to F_infinity Omega r^n/n. Bounded current coefficients make the surface flux o(r^n), a contradiction. Thus the usual finite-positive-T asymptotic vacuum falloff is excluded by this necessary equation alone. A growing boundary gradient, horizon/current flux, evolving scalar, shrinking/nonregular geometry or T->0 can evade these stated asymptotic hypotheses; their physical admissibility must be checked separately. No static de-Sitter-patch regularity claim is borrowed.

## Reproducible checks and unresolved implication

checks.py verifies the fixed-I chain exactly, derives both current components by direct ADM matrix inversion, independently computes positive tail integrals in original and transformed variables, and constructs a bounded smooth periodic static ADM fixture. Its divergence mean is approximately7.16e-18 while its positive interaction-force mean is approximately205.04 in declared dimensionless test units. This fixture is NOT an on-shell Einstein/clock solution and is not offered as one; its failure illustrates the necessary equation and cannot substitute for the analytic integral proof. Negative controls drop the UV derivative, claim a periodic gradient cancels the positive force, or reverse the canonical-momentum orientation. Contract/provenance and standard fresh manifests pin actual files and bounds; RUNS.json is separate. Historical preflight a retains the shifted-current sign failure.

This advances the canonical selector screen beyond homogeneous vacuum: a stationary inhomogeneous gradient or cold-density pattern cannot stabilize the retained UV-normalized modulus on a compact no-flux slice. No full covariant source solution, positive-energy theorem, cold identity or32pi selection follows. The earliest remaining physical route is an actual changed interaction/kinetic/boundary mechanism with its complete varied equations, or a regular rolling full-field extension of the existing canonical action. A stabilizing function chosen to force a target would be new input, not a result of this equation.
