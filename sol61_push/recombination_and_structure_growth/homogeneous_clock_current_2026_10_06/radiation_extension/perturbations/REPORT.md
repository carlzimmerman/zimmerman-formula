# Radiation momentum preserves the generic clock pole at a simple kinetic crossing

The fully constrained dust–radiation–clock perturbation system has six canonical variables. On an analytic finite-time background where its clock kinetic coefficient has a simple zero, the actual six-state residue is nonzero rank one and nilpotent. Generic linear solutions have a logarithmic clock-slicing curvature perturbation and a pole in the gauge-invariant clock norm. Regular amplitudes form a codimension-one subspace. The radiation momentum enters this condition explicitly; it cannot be omitted by reusing the four-state dust result.

This is a conditional classical linear theorem for the same logKGB action with the finite-A response. It does not determine a nonlinear continuation, quantum vacuum decay, recombination transfer or a CMB fit. The radiation-era background remains an exact tuned homogeneous solution; the obstruction concerns promoting it to a generic regular linear cosmology for modes which encounter a simple kinetic zero.

## Retained action and actual time-dependent matter normalization

Use four dimensions, Einstein coefficient M/2, M>0, logKGB K=-c ln(X/Xref), G=-sqrt(2)c/(3H*) X^(-1/2), L3=-G Box(phi), q=phidot>0. The background is the parent tuned conserved dust+radiation history, 0<eta=c/(3M H*²)<1, H=H_star h, where H_star denotes the fixed H* parameter. Hence Theta=M H_star(h-eta) is nonzero. The response is M[kappa a_mu a^mu-2W(|a|;A)], kappa>0, fixed finite A>0, W=O(|a|³/A). Its quadratic term is kappa M(grad nu)²/a_FRW² and introduces no lapse temporal derivative in unitary clock gauge. W contributes no quadratic term.

Radiation is an independent minimally coupled positive P(Y)=lambda Y² field chi, Y=-g^(mu nu)chi_mu chi_nu/2>0, lambda>0. This is an irrotational barotropic perfect radiation fluid. It has rho_r=3P, enthalpy R_r=rho_r+p_r=4rho_r/3 and sound speed squared 1/3. Its homogeneous equation is `(a_FRW³ P_Y chidot)dot=0`; since P_Y chidot=lambda chidot³, chidot is proportional to a_FRW^-1. Thus for

`v_r=delta chi/chidot`, `s_r=delta chidot/chidot=dot(v_r)-H v_r`.

The -H v_r term is required by the actual radiation solution, not a discretionary slow-background correction. An independent dust Schutz-Sorkin density momentum is `pi=delta rho_d_phys+3rho_d zeta`. Its velocity potential is v_d. Both matter components are conserved and minimally coupled. We keep scalar irrotational modes; radiation entropy, vorticity and photon/free-streaming anisotropic stress are not represented by this matter model.

Let N=1+nu, gamma_ij=a_FRW² exp(2zeta)delta_ij, N_i=partial_i beta, t=Delta beta/a_FRW², and physical p=k/a_FRW, k nonzero. Fields may be taken in one real Fourier sector, with periodic boundaries or vanishing boundary variations.

## Full quadratic action before eliminating lapse and shift

The actual scalar coefficients are

`Theta=M H_star(h-eta)`,

`Sigma=3M H_star²[eta(1+h)-h²]`, `S=Sigma+kappa M p²`.

Set C_r=R_r/(2c_r²)=3R_r/2=2rho_r. Direct expansion of N sqrt(gamma)P(Y) gives

`L_r/a_FRW³=C_r(s_r-nu)²+3R_r zeta s_r-3rho_r zeta nu+(3/2)rho_r zeta²`

`-R_r p²v_r²/2+R_r v_r t`.

The radiation square is a full matter lapse reaction and kinetic mixing, not a frozen source. The term 3R_r zeta s_r is retained, including its -H v_r part.

The raw time-dependent unitary scalar action is, up to boundaries,

`N sqrt(gamma)[2c ln N-V(t)-b theta ln N]-b sqrt(gamma) qdot/q`,

`b=2c/(3H_star)`, `V=rho_v+c ln(q²/(2Xref))`.

Its gravity-plus-clock zeta*nu tadpole is 3(rho_d+rho_r)zeta nu by the actual Friedmann equation. After the temporal integration by parts its zeta² mass is -9p_r/2=-3rho_r/2 by the actual Raychaudhuri equation. Radiation cancels both its own zeta*nu part and this mass. The complete same-action quadratic action is therefore

`L_2/a_FRW³=-3M zetadot²+S nu²+6Theta nu zetadot-2Theta nu t+2M zetadot t`

`+M p²zeta²+2M p²nu zeta+3rho_d zeta nu`

`+pi(dot(v_d)-nu)-rho_d p²v_d²/2+rho_d v_d t`

`+C_r(s_r-nu)²+3R_r zeta s_r-R_r p²v_r²/2+R_r v_r t`.

No scalar-only vacuum background equation is used in these cancellations. The physical dust density convention is recovered by substituting pi=rho_d(delta_d+3zeta) and integrating the dust temporal term by parts using a_FRW³rho_d constant.

## All constraints and canonical identities

Define d=M/Theta, e_d=rho_d/(2Theta), e_r=R_r/(2Theta). The shift variation gives

`nu=d zetadot+e_d v_d+e_r v_r`.

The lapse equation then solves t through its nonzero -2Theta coefficient. It is not an extra constraint on the three propagating scalar pairs. The exact lapse/shift elimination is legitimate for k nonzero and Theta nonzero.

The radiation per-volume canonical momentum is

`P_r=2C_r(s_r-nu)+3R_r zeta`,

so `dot(v_r)=H v_r+nu+(P_r-3R_r zeta)/(2C_r)`.

After this Legendre substitution set

`T=2M p²+3rho_d+3R_r`,

`R_nu=2S nu+6Theta zetadot+T zeta-pi-P_r`,

`A_c=3M+S d²=K_c`.

The per-volume clock momentum becomes exactly

`P_zeta=2A_c zetadot+[A_c/M](rho_d v_d+R_r v_r)+dT zeta-d pi-dP_r`.

The true canonical momenta include the volume factors a_FRW³. Using per-volume momenta is an analytic invertible normalization at finite positive a_FRW and produces the explicit Hubble terms below. The two-velocity matrix for (zetadot,dot(v_r)) has determinant C_r A_c. Dust retains its first-order canonical pair. These are three scalar degrees of freedom; radiation is not counted again as an independent density field.

The exact reduced first-order equations away from A_c=0 are

`dot(v_d)=nu`,

`dot(pi)+3H pi=e_d R_nu-rho_d p²v_d`,

`dot(v_r)=H v_r+nu+(P_r-3R_r zeta)/(2C_r)`,

`dot(P_r)+4H P_r=e_r R_nu-R_r p²v_r`,

`dot(P_zeta)+3H P_zeta=(2M p²-3R_r)zeta+T nu+P_r`,

with zetadot obtained from its momentum identity. The 4H, rather than 3H, radiation-momentum redshift follows from s_r=dot(v_r)-H v_r; discarding that term changes the full equations. These formulas retain the radiation pressure, lapse reaction and one-derivative terms which a velocity Schur calculation alone does not provide.

## Genuine six-state residue at a simple zero

Assume an analytic background at finite time t0 with a_FRW>0, q>0, rho_d>0, rho_r>0, M>0, Theta nonzero and nonzero k. Suppose `A_c=alpha tau+O(tau²)`, tau=t-t0, alpha nonzero. A tangent/double zero and the homogeneous sector are outside this theorem.

Use state `y=(zeta,v_d,v_r,pi,P_r,P_zeta)`. The coefficient of zetadot in each matter-momentum equation is respectively rho_d A_c/M and R_r A_c/M. Both are proportional to A_c, so neither matter momentum acquires a pole after the clock momentum is solved. The singular clock numerator is

`P_zeta-dT zeta+d pi+dP_r`.

The velocity terms multiplied by A_c contribute only regular coefficients. Consequently

`ydot=[N/tau+B(tau)]y`, B analytic,

`N=c r/(2alpha)`,

`c=(1,d,d,0,0,Td)^T`, `r=(-dT,0,0,d,d,1)`.

All residue coefficients are evaluated at t0. Directly `r c=0`, so N is nonzero rank one and N²=0. In particular the P_r component of r is essential; deleting it fails the residue calculated from the full action. The two matter coordinates share the lapse pole, while their momenta have no leading pole. This is an independent six-state reconstruction, not a transplanted dust-only formula.

For A_c nonzero these six equations are independent and carry arbitrary initial data in their three scalar pairs. Dust continuity and radiation conservation are the matter momentum equations, not missing additional constraints. Clock unitary gauge is admissible because q is nonzero; the spatial scalar gauge has already been fixed. No omitted lapse/shift constraint eliminates the singular direction before the crossing.

## Analytic solution and invariant linear breakdown

Seek an analytic matrix U with U(0)=I obeying `U'=(N U-U N)/tau+B U`. At each positive integer m, its coefficient is solved by `(mI-ad_N)U_m=sum_(j=0)^(m-1)B_j U_(m-1-j)`. Since N²=0, ad_N³=0, and the inverse is `m^-1[I+ad_N/m+ad_N²/m²]`. Its norm is bounded by a constant divided by m. Analytic coefficient bounds for B admit the usual scalar analytic majorant, proving convergence on a neighborhood. U is locally invertible. Thus on either side of zero,

`y=U(tau)[I+N ln|tau|]b_0`.

Generic amplitudes with r b_0 nonzero have `zeta=[r b_0/(2alpha)]ln|tau|+O(1)` and

`nu=d[r b_0/(2alpha tau)]+O(ln|tau|)`.

The v_d and v_r terms in the lapse are at most logarithmic and cannot cancel its pole. The scalar observable on clock surfaces is

`delta X_clock=delta X-(Xdot/q)delta phi`.

It is gauge invariant at first order. In unitary clock gauge it equals -q²nu, which has a generic nonzero pole because q and d are finite and nonzero. A smooth gauge or point-variable change does not remove this linear clock-norm divergence. A singular canonical representation can alter the displayed kinetic sign, but cannot erase this invariant of the same finite linear solution.

Regular analytic amplitudes obey exactly one independent condition

`P_zeta-dT zeta+d pi+dP_r=0`

on b_0, giving a five-dimensional subspace of the six real amplitudes per real Fourier sector. No mechanism that selects this subspace or continuation of generic nonlinear data is supplied. Perturbations become large before the formal pole, so the theorem establishes failure of generic finite linear continuation, not the nonlinear end state or a quantum instability.

## On-background bounded crossing and scope

On the actual eta=1/2, r_f=1/4 background, with a_f=M=H_star=kappa=1 and k_bar=0.1, the kinetic-zero calculation gives a_FRW/a_f approximately 0.994826382301121, h approximately 1.50673618727918, and alpha/(M H_star) approximately 2.88304489970533. The computed zero residual is about 4e-61 at 60-digit working precision. This illustrates a transverse crossing within a finite smooth radiation+dust history, where both fluids have positive densities and Theta nonzero. It is a bounded numerical witness, not interval certification or a universal theorem that every mode crosses simply.

The parent background theorem proves early-negative K_c for sufficiently small fixed comoving k in a radiation era and positive K_c at the background fold, so some zeros must be encountered by continuity. Whether a specified zero is simple is a distinct hypothesis; the theorem does not cover the tangent boundary mode. A restricted spectrum with no crossing is not obstructed by this result. Nor does it rule out operators changing the quadratic action, extra dynamics, or a nonlinear regular completion.

No radiation acoustic transfer, dust growth spectrum, free-streaming Boltzmann hierarchy, photon-baryon interaction, atomic recombination or CMB likelihood has been calculated. Homogeneous and quadratic response coefficients still leave the finite positive MOND scale A absent; the 32pi objective remains open. The next physical arrow is a nonlinear or spectrally restricted mechanism which preserves the same source/cosmological requirements and removes the generic crossing without merely imposing one finely selected amplitude relation on every affected mode.

## Evidence

SOURCES.md records the primary action/constraint dependencies and their bounded applicability. checks.py independently expands the radiation P(Y) action, derives the actual time-dependent field normalization, verifies gravity/radiation tadpole cancellation, varies the full action, reconstructs all six equations and their residue, checks nilpotency and its analytic-adjoint condition, and computes one bounded on-background crossing. Controls delete the radiation momentum, freeze its clock normalization, or discard its tadpole term. Universal local conclusions come from the analytic derivation, not the finite output. REPORT.md is not a runner input. No frozen parent files were modified.


Authoritative runs: main_a passes all 23 checks. control_clock_a, control_momentum_a and control_tadpole_a reject their intended changed action/constraint interpretations. All four standard manifests validate against current input and output hashes. The records enforce wall-time, CPU-time and numerical thread bounds; no unsupported address-space cap was requested. Preflight files are development results, not authoritative evidence. SPECTRUM_LINK.md separately gives an analytic connection from the conditional theorem to actual transverse mode levels on the radiation history; it is not a runner input.
