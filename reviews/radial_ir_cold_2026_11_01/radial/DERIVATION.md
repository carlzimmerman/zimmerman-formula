# Actual radial coefficient and the local light-mode dictionary

The phase-current coefficient F of TP03 is not the radial coefficient A. In L=A(s)(partial s)^2+F(s)(partial theta)^2-U, a general broken-SUSY component action can have different finite values. This file fixes the actual component graph calculation in the original-X chart and identifies the limits of using it for charged dynamics.

## One-loop radial graph vertices

At fixed couplings a0 is constant, X_s=X and b_s=b. Let z_s=(X,0,bD). With canonical microscopic fields, differentiate the complete tree mass matrices along this vector. For real scalars the two-external-s bubble gives

    deltaA_scalar=sum_ordered |H_s,ij|²/(64pi²) I(mi²,mj²),
    I(x,y)=integral_0^1 dt t(1-t)/[tx+(1-t)y].

The diagonal i=j term is included, with I(x,x)=1/(6x). The scalar seagull has no external momentum dependence. Null-null vertices must vanish on the constant-rank tree valley; a nonzero physical vertex would be an IR obstruction.

In real symmetric signed-Majorana mass blocks use B=M_s, rotated into the signed mass eigenbasis. The scalar vertex gives

    deltaA_fermion=sum_ordered Bij²/L
       integral_0^1 dt t(1-t)[-3ln(Dij/Q²)-mu_i mu_j/Dij-1],
    L=16pi², Dij=t mu_i²+(1-t)mu_j².

The chirality-flip sign differs from the angular pseudoscalar graph. For one ungauged supersymmetric chiral mass proportional to X, the scalar finite constant m²/(3L) cancels the fermion's -m²/(3L), reproducing angular and radial equality. That is a useful unambiguous limit; it is not imposed on an off-shell gauged component slice with additional light moduli.

In linear Landau gauge the radial scalar-vector derivative vertex is

    -2sqrt(2)g(partial_mu s) A_a^mu C_radial,aI chi_I,
    C_radial=(Im[R_a z_s],-Re[R_a z_s]).

It has the same finite MS/DR component kernel as the angular SV graph, with the different actual scalar projection:

    deltaA_SV=g²/L sum C_radial,aI²[3 integral ln(D/Q²)+1/2].

The vector mass matrix also varies radially. Its two mass vertices give

    deltaA_VV=sum_ordered |(M_V²)_s,ab|²/(4L)
                [3I(x,y)+(3/4)K(x,y)],
    K(x,y)=ln(x/y)/(x-y), K(x,x)=1/x.

The extra K term is from the momentum-dependent transverse projectors: Tr P(k)P(k+p)=d-1-(d-1)p²/(d k²)+... . For a degenerate real vector of mass square x, the coefficient is 5[(mV²)_s]²/(16Lx). This p² bubble is UV finite; epsilon-vector multiplicities therefore do not add a pole-generated finite term. The usual SV projector finite +1/2 remains. Vector and scalar seagulls affect the potential but have no p² dependence. Linear Landau ghosts have no background-scalar vertex.

The local UV derivative is the same component-Landau wavefunction identity as for angular matching; the finite radial difference need not vanish. The isolated off-shell coefficient is gauge/scheme/coordinate dependent. The retained light direction is defined by the gauge-singlet X with the heavy invariant fields eliminated, not by treating a raw b Hessian as its physical mass.

## Vacuum pullback and charged-state limitation

The one-loop heavy vacuum shift gives b=b0+delta b, a=a0+delta a, with b0_s=b0 and a0_s=0. Its radial kinetic pullback to one-loop order is deltaA_h=60b0(delta b)_s. Since deltaF_h=60b0 delta b,

    deltaA_h=(deltaF_h)_s-deltaF_h.

The (delta a_s)^2 term starts at two-loop order in the kinetic coefficient. Direct graph matching and this geometric pullback are included once each. At the quantum vacuum m_radial²=V_ss/(2A_reduced); the canonical fluctuation is sigma=sqrt(2A_reduced) delta s. A local field redefinition changes A and V together, not the pole of a correctly matched gauge-invariant mode. A gauge-variation/nonlocal audit is still needed before claiming an exact physical pole from a fixed-gauge off-shell truncation.

For a circular state retain the previously matched classical four-derivative phase term L=A(partial s)^2+F Xtheta+(J/2)Xtheta²-V, Xtheta=(partial theta)^2. Put q=omega²,C=2F+6Jq,M=-2omega(Fs+Js q),N=Omega_ss,D=N+M²/C and vtheta²=(F+Jq)/(F+3Jq). With canonical local perturbations the determinant is

    (Omega_freq²-k²-N/(2A))
       (Omega_freq²-vtheta² k²)-[M²/(2AC)]Omega_freq²=0.

The nonzero k=0 gap is D/(2A), while the IR branch has c_s²=vtheta² N/D, agreeing with thermodynamics. For N<0,D>0 and positive A,C the unstable band is 0<k²<-N/(2A). At vtheta=1 the peak growth is |N/(2A)|/[2sqrt(M²/(2AC))]. General vtheta is handled by the exact quadratic roots.

This determinant uses the actual computed vacuum two-derivative A, but it is not automatically the entire next-order occupied derivative action. Eliminating tree heavy fields at nonzero q also induces four-derivative terms containing radial gradients; their q-activated corrections to A/mixing can be of the same relative order as the one-loop radial metric. They do not change the homogeneous EOS, and they are a separate matching obligation for precision charged-state gaps. Leading growth-sign and scale statements retain this explicit truncation.

## Small uncharged oscillations and phase amplification

Near the vacuum, let sigma(t)=Sigma cos(mt) be a small canonical radial oscillation. Canonical phase pi=sqrt(2F0)theta couples through g_sigma sigma(partial pi)^2, with

    g_sigma=Fs/(2F0 sqrt(2A0)), eta=g_sigma Sigma.

The lifetime researcher owns perturbative widths. The tree normalization gives g_sigma=1/(sqrt(2)v) and Gamma(sigma->phase phase)=m³/(64pi v²); finite coefficients change the coupling through the displayed derivative.

At harmonic small amplitude, the canonical phase mode satisfies, to leading order, y_ddot+[k²+eta m² cos(mt)]y=0. Its first narrow Mathieu band is centered at k=m/2, fractional half-width |eta|, and peak amplitude Floquet exponent mu_F=|eta|m/2. Cosmological redshifting sweeps a mode through the band; for m>>H and eta<<1 the integrated amplitude exponent is

    I_cross=pi eta² m/(4H).

The condition mu_F/H>>1 alone is insufficient: the mode spends only a fractional-band crossing time there. In terms of coherent energy rho=m²Sigma²/2,

    I_cross=pi g_sigma² rho/(2mH),
    I_cross/(Gamma_pert/H)=16pi² rho/m⁴.

This tests an actual phase-production channel, without choosing a density or scale. Expansion, coherence and escape matter. A mode needs gain over the available pump-coherence time and propagation distance. For a virialized coherent domain, estimates tau_coh~1/(m v²), ell_coh~1/(m v) give conditional gains mu_F tau_coh~eta/(2v²) and mu_F ell_coh~eta/(2v); random-phase transport across domains is not solved by these estimates. Homogeneous Minkowski Floquet growth is not itself a cosmological or halo depletion rate.
