# Coupled matter constraints at the homogeneous clock fold

The tuned homogeneous dust history survives this calculation as a background solution. Its early upper branch has a negative reduced scalar kinetic coefficient at sufficiently long wavelengths, even after the ordinary-matter constraints are included. The acceleration response repairs that coefficient at large wave number and, for every nonzero wave number, at the background fold. With the undetuned response the negative band is entirely below the Hubble scale. These are exact constrained quadratic statements, not a demonstrated UV ghost, catastrophic vacuum decay, or a complete physical exclusion of the background history. The remaining discriminator is the coupled nonadiabatic mode evolution and a regular canonical description through the kinetic-zero surfaces.

## Action and assumptions

This health calculation is four dimensional, unlike the parent background theorem. Use Einstein coefficient M/2, c>0, H*>0, eta=c/(3M H*^2), and the exact parent positive-charge dust history. Restrict 0<eta<1, so H=H_star times h with h>1 implies Theta is never zero; H_star denotes the fixed H* parameter. The scalar functions are K=-c ln(X/Xref), G=-sqrt(2)c/(3H*) X^(-1/2), X=q^2/2>0, and L3=-G Box(phi). Ordinary matter is minimally coupled conserved dust. The same clock has the response M[kappa a_mu a^mu-2W(|a|;A)], finite A>0, W=O(|a|^3/A), kappa>0; kappa=1 is the original P2 repair and kappa=1-epsilon is a quadratic detuning. At quadratic order on homogeneous geodesic clocks the entire W term is absent. A remains free.

For a variable-q unitary clock, the exact scalar ADM action, up to spacetime boundary terms, is

`N sqrt(gamma)[2c ln N - V(t) - b theta ln N] - b sqrt(gamma) qdot/q`,

`b=2c/(3H*)`, `V(t)=rho_v+c ln(q(t)^2/(2Xref))`.

The last term is essential in the spatial background equation. It cannot be discarded as if q were constant. Perturbations use N=1+nu, gamma_ij=a_FRW^2 exp(2zeta)delta_ij, scalar shift N_i=partial_i beta, and t=Delta beta/a_FRW^2. A Fourier mode has physical wave number p=k/a_FRW; k is nonzero. Boundary integrations presume a periodic box or vanishing spatial boundary variations. The zero-wave-number homogeneous gauge/background sector is not included by taking the shift equation at k=0.

Direct K/G differentiation gives the actual evolving-background coefficients

`Theta=M H* (h-eta)`,

`Sigma=3M H*^2[eta(1+h)-h^2]`,

`G_S=3M+M^2 Sigma/Theta^2=3M eta(1+eta-h)/(h-eta)^2`.

The independent debraided derivative coefficient is

`D=K_X+2XK_XX+6Hq(G_X+XG_XX)+6X^2 G_X^2/M=c(1-h+eta)/X`,

and `G_S=X M^2 D/Theta^2`. Thus substituting the rolling-vacuum G_S into this early dust history would give the wrong sign.

## Exact dust action and all lapse/shift reactions

Start with the irrotational Schutz-Sorkin action `S_d=-integral[sqrt(-g) m n + J^mu partial_mu ell]`, where n=sqrt[-g_mu_nu J^mu J^nu]/sqrt(-g), rho=m n, and J is a vector density. Choose ell=-m(t+v), J^0=J_b(1+delta_J), with J_b=a_FRW^3 rho/m constant. Eliminating spatial J^i gives, to quadratic order,

`L_d/a_FRW^3 = pi(vdot-nu) -rho p^2 v^2/2 +rho v t`,

where `pi=rho delta_J=delta rho_phys+3rho zeta`. Pi is a canonical density momentum, not a new unconstrained multiplier to be called a ghost. This variable differs from a physical density perturbation because the spatial volume fluctuates.

The complete scalar quadratic action in this coordinate-density convention is

`L_2/a_FRW^3 = -3M zetadot^2 + S nu^2 +6Theta nu zetadot -2Theta nu t+2M zetadot t`

`+M p^2 zeta^2 +2M p^2 nu zeta +3rho zeta nu`

`+pi(vdot-nu)-rho p^2 v^2/2+rho v t`,

with `S=Sigma+kappa M p^2`. The raw homogeneous ADM expansion gives the zeta*nu coefficient `3[3MH^2+2c-V-3bH]=3rho` by Friedmann. The zeta^2 term left after the temporal integration by parts is proportional to `3MH^2+2M Hdot-V-b qdot/q`, which vanishes by the actual dust Raychaudhuri equation. This checks the full time-dependent action, not only its velocity Hessian.

Equivalently use physical density contrast delta, pi=rho(delta+3zeta). A temporal integration by parts using a_FRW^3 rho constant converts the dust terms and cancels the explicit 3rho zeta nu. The matter contribution becomes `-rho v(deltadot+3zetadot)-rho delta nu-rho p^2v^2/2+rho v t`, matching the direct density formulation. Both conventions give the same constrained action.

Varying the shift gives exactly

`nu=d zetadot+e v`, `d=M/Theta`, `e=rho/(2Theta)`.

The lapse equation then determines t; its coefficient -2Theta is nonzero. Thus no lapse or scalar-shift constraint is being frozen or omitted. The response has no shift dependence at this order, so the momentum relation is unchanged, although its lapse equation changes. After substitution t disappears from the reduced action.

## Coupled kinetic matrix and exact dust limit

For a regular barotropic P(Y) matter field, define v=delta chi/chidot, R=rho+p_m>0, and C=R/(2c_m^2)>0. Its direct expansion has `C(vdot-nu)^2+R v t-R p^2v^2/2` plus terms with at most one temporal derivative. After both gravitational constraints are eliminated, the velocity matrix in (zeta,v), with L=K_AB qdot^A qdot^B+..., is

`K=[[K_c+C d^2, -C d],[-C d,C]]`,

`K_c=G_S+kappa M^3 p^2/Theta^2`, `det K=C K_c`.

The matter square is null on the velocity direction (1,d), so matter mixing cannot turn a negative K_c into a positive definite velocity matrix. The finite-c_m action is a regulator/control; at nonzero pressure it is not literally the parent dust background. The exact dust action above removes that qualification.

For dust perform the time-dependent canonical coordinate change w=v-d zeta. Since `vdot=wdot+d zetadot+ddot zeta`, the pi*zetadot mixing cancels exactly. The resulting action has `pi wdot+K_c zetadot^2` and only one-derivative or potential couplings. Wherever K_c is nonzero, its Legendre transform therefore has

`partial^2 H_red / partial P_zeta^2 = 1/(2 a_FRW^3 K_c)`.

This is a negative reduced momentum curvature when K_c<0, after lapse and shift have been removed. It is not inferred from the linearity of a dust multiplier. At K_c=0 this particular Legendre map loses rank; whether the original constrained system acquires a benign constraint, needs a different regular canonical chart, or becomes strongly coupled must be audited rather than decided from this formula alone.

The caution is substantive in the infrared. Eliminating the dust coordinate after integrating pi*vdot by parts involves the coefficient `B=S e^2-rho p^2/2`. Writing its linear zetadot coupling as L_z, the new density-coordinate kinetic block contains `K_c zetadot^2-(L_z zetadot-pidot)^2/(4B)`, whose determinant is `-K_c/(4B)`. At K_c=0, S=-3Theta^2/M and hence B=-3rho^2/(4M)-rho p^2/2<0. The density-coordinate elimination is therefore regular there. Its zeta-dot mixing coefficient before elimination is L_z=2e(Sd+3Theta)=rho K_c/M, so it also vanishes there. The density-variable velocity matrix still loses rank; a smooth invertible point-variable change cannot remove this quadratic rank loss. The remaining -d pi zetadot term and all potential terms must be retained for the null equation. A nonsingular full canonical or gauge completion has not been excluded.

This canonical coordinate/momentum exchange can change which direction is described as negative kinetic versus negative potential. It is not a removal of the full dynamics. The primary Jeans' Ghost example shows that an IR kinetic sign alone does not imply a catastrophic quantum instability; its spacelike anisotropic background is different, so it does not prove this timelike clock harmless either.

## Exact wavelength window and the fold

On this history,

`K_c/M = [3eta(1+eta-h)+kappa(p/H*)^2]/(h-eta)^2`.

For early upper-branch h>1+eta, the unitary-configuration velocity form is indefinite precisely in

`0<p^2< p_crit^2 =3eta H*^2(h-1-eta)/kappa`.

It is positive above that boundary. At the parent background fold h=1+eta, `K_c=kappa M p^2/H*^2>0` for every nonzero p. On the lower branch 1<h<1+eta it is positive for every p. Without the acceleration quadratic term the fold coefficient vanishes, and early G_S is negative. The response is therefore a real finite-wave-number kinetic repair, although sufficiently long early modes retain the sign issue.

A global bound supplies the scale interpretation:

`max_(h>1+eta) p_crit^2/H^2 =3eta/[4kappa(1+eta)]`,

attained at h=2(1+eta). For kappa=1 and 0<eta<1 this is below 3/8, so p_crit/H<sqrt(3/8). In the far early GR regime p_crit/H~sqrt(3eta/(kappa h)) tends to zero. No high-frequency/adiabatic approximation can be used to assign a rapid ghost growth rate to this band. Small kappa can enlarge it, and its physical acceptability is a separate question. At any fixed upper-branch epoch an unrestricted continuous spatial spectrum contains long modes with this coefficient; a finite volume or an imposed infrared domain could exclude some of them and must be specified explicitly.

For a fixed nonzero comoving k, however, the early dust asymptotics give p^2 proportional to a_FRW^(-2), while the negative numerator grows only as h proportional to a_FRW^(-3/2). Thus every fixed comoving mode is eventually kinetic-positive sufficiently far toward the early limit. Modes may instead encounter a finite intermediate negative interval and kinetic-zero crossings, then become positive before the background fold. The instantaneous band is not a claim of negativity throughout the past of any fixed mode. The mode-history envelope is a separate calculation.

Exact bounded controls at eta=1/2,kappa=1,M=H*=1: (h,p)=(10,0.3) gives K_c/M=-1266/9025; (10,10) gives 349/361; (1.5,0.3) gives 9/100; (1.1,0.3) gives 23/12. All h>1 values occur somewhere on the monotone tuned background. These points are checks of the constrained coefficient, not numerical perturbation histories.

## Full finite-time mode equations and remaining implication

The action gives an executable nonadiabatic system. Set `nu=d zetadot+e v` and

`R_nu=2S nu+6Theta zetadot+(2M p^2+3rho)zeta-pi`.

Then

`vdot=nu`,

`pidot+3H pi=e R_nu-rho p^2 v`,

`d/dt {a_FRW^3[-6M zetadot+6Theta nu+d R_nu]}=a_FRW^3[2M p^2 zeta+(2M p^2+3rho)nu]`.

The time dependencies H(a), q(a), rho(a), p=k/a and d,e,S are the actual tuned history. This calculation derives the full equations but does not integrate them through a K_c-zero surface or supply a gauge-invariant growth/decay transfer matrix. Freezing their Hubble-dependent coefficients in the infrared would not resolve that obligation. Complete health requires this coupled mode diagnosis, a regular original-constraint analysis at rank loss, gradient/potential terms and nonlinear strong-coupling scales. The report therefore does not exclude all healthy cosmological completions or declare the entire dust trajectory physically sick. It does demonstrate why the positive rolling-vacuum kinetic coefficient cannot be transplanted to the early dust solution.

## Evidence and provenance

SOURCES.md authenticates primary action/constraint procedures and the narrowly applicable IR interpretation counterexample. checks.py reconstructs K/G coefficients, eliminates raw matter constraints, checks the full coordinate-density tadpoles, the canonical dust momentum curvature, the density-coordinate exchange, wavelength maximum and bounded sign controls. Exact statements come from the written derivation; finite checks support it rather than substitute for it. The standard manifests pin the actual inputs; REPORT.md is intentionally not an execution input so prose clarifications cannot stale the calculation. Preflight directories are development checks, not authoritative provenance runs. No parent inputs or peer files were modified.


Authoritative bounded run: `runs/main_b` passes 35 exact checks. `control_mixing_b`, `control_vacuum_b`, and `control_response_b` each reject their intended mutation (respectively the matter Schur identity and the actual-background coefficient). All four b manifests pass the independent manifest validator. The a attempts were preserved as launch failures: the requested POSIX address-space cap failed in the host preexec hook before Python ran; they have no mathematical result and are not negative controls. The fresh b runs omit that unsupported memory limit and enforce the recorded wall time, CPU time and thread cap. No script or mathematical input changed between a and b.
