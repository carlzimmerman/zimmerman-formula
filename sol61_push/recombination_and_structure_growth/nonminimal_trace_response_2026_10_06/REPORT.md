# Nonminimal cutoff: radiation leaves the minimum fixed, dust drives trace memory

The stabilized cutoff couples to the matter STRESS TRACE in its consistent common sector, rather than algebraically to total density. Ideal radiation admits an exactly constant cutoff at its vacuum minimum. Nonzero dust does not: it forces the scalar toward increasing cutoff. For a stable quadratic-curvature vacuum, the canonical scalar is light compared with cosmological friction. A controlled first-order conserved-dust response exhibits slowly decaying retarded memory, not generic instantaneous tracking of dust density. This does not solve real recombination, select32pi or calibrate the operational MOND scale.

## Same action, both metrics and frames

Use the frozen nonminimal-cutoff action, spatial n>=3, d=n+1, M0=4K>0, f²>0 and F(u)>0:

S=K integral F(u)[Vg Rg+Vhat Rhat+2chi_n a0²v M(I,exp u)]
 −f²/4 integral[Vg g_inv+Vhat hatg_inv]du du+S_m,g+S_m,hat.

The retained UV-normalized interaction has M(0,T)=−A(T); a0 is a constant Jordan-action parameter. On exact coincidence I=0 and the two metric equations agree with mirrored identical minimally coupled Jordan matter, each half of the displayed total density. Ordinary-only matter generally does not admit that coincidence. All results here concern homogeneous common/even fields, not the relative/foliation source sectors.

The summed Jordan action is M0 F R_J/2−f²(du)²/2−V0 F A+S_m[g_J], V0=2Kchi_n a0². Define

g_E=F^{2/(d−2)}g_J, A_m(u)=F^{-1/(d−2)},
U=V0 A F^{-beta}, beta=2/(d−2),
Z=f²/F+M0(d−1)/(d−2)(F_u/F)²,
dpsi/du=sqrt Z>0,
alpha_m=d ln A_m/dpsi=−(F_u/F)/[(d−2)sqrt Z].

Then the common action is M0 R_E/2−(partial psi)²/2−U(psi)+S_m[A_m²g_E]. Both independently varied metric rows supply half of the summed scalar/matter stress. The canonical orientation psi_u>0 fixes the force sign below. These classical equations require no hbar.

At any finite stable vacuum u0, U_psi=0 and p_A=beta q_F, q_F=F_u/F. Since1<p_A<3/2, q_F>0 and alpha_m,0<0. For a stable quadratic F=F0+c_F(u−uc)² with F0,c_F>0, the parent proves

0<mu²=m²/H_vac²<(d−2)/2=(n−1)/2,
m²=U_psipsi(u0), H_vac²=2U0/[M0 n(n−1)].

This bound applies to the declared quadratic class; it is not assumed for every positive nonminimal F. In d=4 it gives m<H_vac. It does not guarantee adiabatic following of a matter-dependent extremum.

## Actual matter variation and conservation

At fixed Einstein metric, delta g_J,mu nu=2alpha_m g_J,mu nu delta psi. The matter action variation is integral sqrt(-g_E) alpha_m T_E delta psi. Combining it with canonical scalar variation gives

Box_E psi−U_psi+alpha_m T_E=0,
nabla_mu T_m^{mu nu}=alpha_m T_E nabla^nu psi.

For an ideal barotropic fluid p=w rho, T_E=−rho+n p=−(1−nw)rho. Thus the actual homogeneous equations are

psiddot+nH_E psidot+U_psi=−alpha_m(1−nw)rho,
rhodot+nH_E(1+w)rho=alpha_m(1−nw)rho psidot,
H_E²=2[rho+psidot²/2+U]/[M0 n(n−1)],
H_Edot=−[psidot²+(1+w)rho]/[(n−1)M0].

For several mirrored perfect fluids, sum their traces and densities separately. The scalar energy equation has exchange −alpha_m(1−nw)rho psidot, exactly canceling the matter exchange. An Einstein-frame fluid is not minimally coupled just because the Jordan action is minimal.

The same conservation can be reconstructed without a stress-sign mnemonic: rho_E=A_m^d rho_J, a_J=A_m a_E and dt_J=A_m dt_E. Jordan conservation rho_J proportional to a_J^{-n(1+w)} therefore gives rho_E proportional to A_m^{1−nw}a_E^{-n(1+w)}. This agrees with the exchange row. Pressure transforms with the same factor, so w itself is unchanged. H_J=[H_E+alpha_m psidot]/A_m; frame conversion is not optional when interpreting a cosmological rate.

## Exact radiation and nonzero dust gate

For ideal radiation w=1/n, the trace and exchange vanish identically. Therefore psi=psi0, psidot=0 is an exact homogeneous solution with positive radiation and the unchanged vacuum minimum:

rho_r proportional to a_E^{-(n+1)},
H_E²=H_vac²+2rho_r/[M0 n(n−1)].

A_m is constant on this branch, so Jordan and Einstein rates differ only by that constant conversion. Radiation can dominate total density while the cutoff stays fixed; total density alone is not the stabilizer's scalar source.

For dust w=0 at the same finite vacuum minimum, the scalar residual is −alpha_m,0 rho_d>0. Thus psi cannot remain constant when rho_d>0. With psi_u>0 it initially moves toward larger u and T. This is an actual scalar field equation, not assignment of a new cutoff from rho_total. A putative instantaneous matter-dependent extremum must solve U_psi+alpha_m rho_d=0; rho_d itself depends on psi through A_m and evolves by the conservation row. Algebraic elimination without a heavy/adiabatic regime is not justified. Added explicit matter couplings, nonmirrored sources or altered F change this premise.

## Controlled conserved trace forcing

There is a precise small-source calculation that does not freeze away a matter equation. Start the exact constant-psi radiation-plus-vacuum branch. Add initial mirrored dust density rho_d,1=epsilon U0 at N=ln(a_E/a_initial)=0, with epsilon>0 small; give the scalar its vacuum initial value and zero velocity. This is permitted initial data with the Friedmann metric correction, not external matter creation or an equilibrium assumption.

To first order, rho_d,1=epsilon U0 exp(-nN), because alpha_m rho_d psidot is order epsilon². The radiation remains trace-free. Scalar kinetic and potential stress perturbations about a minimum start at order epsilon²; first-order metric changes sourced by dust multiply the zero background scalar velocity and affect its forced equation only at order epsilon². Thus the first-order scalar equation on the exact background is controlled:

delta psiddot+nH_bar delta psidot+m²delta psi=−alpha_m,0 rho_d,1.

Let R(N)=rho_r/U0=R0 exp[-(n+1)N], H_bar²=H_vac²(1+R), x=delta psi/sqrt(M0). Then

x_NN+[n−(n+1)R/(2(1+R))]x_N+mu²x/(1+R)
 =−alpha_m,0 sqrt(M0) n(n−1)epsilon exp(-nN)/[2(1+R)].

This keeps radiation expansion and the actual conserved dust forcing, with zero initial x,x_N. It is a first-order-in-epsilon cosmological response, not a large matter-dominated solution or complete perturbation/growth calculation.

## Exact vacuum-limit retarded solution and generic memory

For R0=0, use X=x/epsilon and S=−alpha_m,0 sqrt(M0)n(n−1)/2>0. The exact equation is X_NN+nX_N+mu²X=S exp(-nN). Its roots are

lambda_+=(−n+sqrt[n²−4mu²])/2,
lambda_-=(−n−sqrt[n²−4mu²])/2,
Delta=lambda_+−lambda_->0.

The quadratic-vacuum bound gives real negative roots. More sharply −1/2<lambda_+<0: the characteristic polynomial is positive at0 and negative at−1/2 since mu²<(n−1)/2. The retarded solution is

X=(S/mu²)[exp(-nN)−(lambda_+/Delta)exp(lambda_+N)
                    +(lambda_-/Delta)exp(lambda_-N)].

It obeys both zero initial conditions and the exact forcing equation. Its retarded Green kernel [exp(lambda_+N)−exp(lambda_-N)]/Delta is positive for N>0; positive dust forcing gives positive departure. The slow homogeneous coefficient −S lambda_+/(mu²Delta) is nonzero and positive, so late memory decays more slowly than a_E^-1/2, while dust decays as a_E^-n.

The instantaneous linear extremum X_inst=S exp(-nN)/mu² is, unusually, also an exact particular solution of this constant-H equation, because its derivative/friction terms cancel. It requires precisely prepared scalar initial data. It is NOT the zero-displacement/zero-velocity retarded solution or a generic forced attractor in relative-to-dust amplitude. X/X_inst grows without bound for the retarded preparation. Thus the light-mass bound is not used to falsely exclude all special tracking solutions; it explains why ordinary retarded memory cannot be replaced by algebraic total-density tracking. Finite radiation history changes the memory coefficient and is treated numerically below, not assumed to share a closed-form solution.

## Declared four-dimensional example and bounded evidence

Use the parent's unshifted positive quadratic F0=1,c_F=10 with gamma=f²/M0=.1. No target cutoff is inserted: the stable root of the exact retained integral gives

u0=1.8465747794506064, T0=6.338073002657167,
alpha_m,0 sqrt(M0)=−0.4078985562644278,
mu²=0.9104089386628805,
lambda_+=−0.34259295779871834, lambda_-=−2.6574070422012817.

Canonical normalization and the curvature coupling are free new action parameters; this is an example, not a selector. The script evaluates A,p_A,p_A' from independent stable integrals and solves the same finite stable-vacuum stationarity equation.

DOP853 solves the controlled N equation for R0=0 and10 over8 e-folds at two tolerances, with a4000-RHS combined guard per two-tolerance case. For epsilon=10^-5, peak modulus displacement |delta u| is about8.22e−7 and3.17e−7 respectively. End X is0.0128354 and0.00549817. The corresponding retarded/instantaneous-extremum ratios are about2.53e8 and1.08e8; the large ratio reflects the faster decay of the tiny denominator, not a large physical field or measured density. The vacuum run also agrees with its independent exact retarded solution. These are bounded numerical corroborations with first-order truncation, not rigorous finite-epsilon error bounds or a nonlinear background fit.

checks.py verifies the general-d trace/exchange signs and exact frame-density exponent, the stable root/coupling/light ratio, exact retarded initial conditions/ODE, and the bounded radiation-history forcing. Controls replace radiation trace by total density, retain a frozen cutoff in dust, or equate the retarded solution with the instantaneous extremum. Current standard records are authoritative and separately summarized in RUNS.json; no photon/atomic data or external tracking theorem is imported.

## Density preference, early-cosmos clue and remaining implication

The same action discriminates trace from density: ideal radiation leaves the vacuum scalar fixed even at high density; dust drives it with history-dependent retardation. Recombination changes ionization and opacity, not this perfect-fluid trace argument. Actual baryons, photons, neutrinos, trace anomalies, thermal histories and atomic transport have not been derived here. In particular this report does not demonstrate recombination or identify microscopic cold matter.

The action a0 remains a fixed Jordan parameter. The dynamical cutoff T, Planck prefactor F and frame units can change. An operational measured Newton/MOND a0 requires the new sourced relative/clock equations and source calibration, being studied separately; no a0 proportional to sqrt(total density) or constant a0/H is inferred. A(u)/F vacuum stationarity and mirrored-matter trace response are not a preference extracted from galaxy distance subsets.

The first remaining implication for real early cosmology is an ordinary-visible-only matter/relative-clock completion and a conserved physical source/force dictionary, followed by actual perturbation transfer and atomic transport. Common-sector trace forcing and a light stable scalar do not supply a cold abundance or select32pi. Different F origins still stabilize arbitrary cutoffs, and the matter density/initial conditions remain independent input.
