# Finite-k scalar constraints of the projected-acceleration action

The actual coincident de Sitter vacuum has one positive-kinetic relative metric scalar in its quadratic finite-k theory. Its exact reduced action has **no quadratic spatial restoring term**. The full shear and shift constraints are essential: removing the relative shear by an unavailable coordinate gauge would give a different result. This does not identify cold matter or close nonlinear scalar/clock health.

## Premise and fields before gauge fixing

This probes the parent action with K>0, χ_3=1, geometric-mean volume and M_eff(I)=−A+I/2−I^(3/2)/12+…, A>0. The **on-shell** coincident background is g=hatg=−dt²+a(t)²dx², a=exp(Ht), H²=a0² A/6 and Λ=3H²=a0² A/2. The cubic interaction does not enter the quadratic action. The calculation uses n=3 and k>0, H>0; it does not extrapolate rank to H=0 or k=0.

Keep θ=t+π, both lapse perturbations ν_g,ν_hat, both longitudinal shifts N_i=∂iβ_g and hatN_i=∂iβ_hat, and spatial metrics

γ_ij=a²[(1+2ζ_g)δ_ij+2∂i∂jE_g],
hatγ_ij=a²[(1+2ζ_hat)δ_ij+2∂i∂jE_hat].

The derivatives in E are comoving. Define z=ζ_g−ζ_hat, ν=ν_g−ν_hat, β=β_g−β_hat, e=Δ_coord(E_g−E_hat), p²=k²/a² and c=K a³ (a coordinate-cell/Fourier normalization is suppressed). All these relative linear variables are invariant under the common scalar coordinate transformations on a coincident background. There is only a diagonal coordinate symmetry, not two independent spatial gauges.

Before choosing θ=t or a common spatial gauge, the normal accelerations satisfy δa_g,i=∂i(ν_g−πdot) and the hatted analogue. Thus δA_i=∂iν, and I²order gives the interaction term c p²ν². The common π cancels. One can subsequently use the common time gauge for π and a common spatial gauge for mean E. This does not remove the relative e. The mean metric sector is the usual linear cosmological Einstein scalar constraint sector; the clock is an accidental quadratic flat direction, not a proved full nonlinear gauge mode.

## Reconstructing the complete quadratic action

For one Einstein metric with its individually matched cosmological constant, ADM expansion and time/spatial boundary integrations give

L_EH,scalar/(Ka³)=−6(ζdot−Hν)²+2p²ζ²+4p²νζ−4(ζdot−Hν)(p²β+e_dot).

The conformal curvature identity R_3=a^(−2)e^(−2ζ)[−4Δζ−2(∇ζ)²] gives the spatial terms; the homogeneous kinetic expansion is −6a³e^(3ζ)(H+ζdot)²/N. Its background and ζ² mass terms cancel against −2ΛN√γ on Λ=3H² after integration by parts. For a general scalar shear, each Einstein-plus-individual-Λ term is spatially diffeomorphism invariant: its shear appears through β−a²Edot, hence the displayed e_dot combination. This use of the separate Einstein identities is an algebraic derivation, not a relative gauge fixing of the full interaction.

The actual constant interaction is −4KΛv, whereas those two individual reference cosmological terms sum to −2KΛ(V_g+V_hat), V_g=√−g. Their difference is

2KΛ(V_g+V_hat−2sqrt(V_g V_hat)).

To quadratic order this equals (KΛ a³/2)(ν+3z+e)². The trace difference includes e. It is not a Fierz–Pauli potential and must not be dropped. Splitting mean and relative Einstein pieces gives the complete relative quadratic action

L_rel/c=−3f²−2f(e_dot+p²β)+p²z²+2p²νz
        +(3/2)H²D²+p²ν²,
f=z_dot−Hν, D=ν+3z+e.

All coefficients use the on-shell background relation. This expression retains both relative lapse and shift and their volume/background-curvature effects.

## Actual finite-k Euler reduction

Shift variation gives −2c p² f=0, hence ν=z_dot/H. Shear variation is

EL_e=3cH²D+2c(f_dot+3Hf)=0.

Since H>0, imposing the shift equation and its derivative forces D=0, or e=−3z−z_dot/H. The lapse equation then determines the shift:

β=−e_dot/p²−(z+ν)/H.

Thus the source-free auxiliary variables are fixed consistently; unchanged momentum rows alone would not have proved this preservation chain.

On these equations the raw action becomes c p²(z+z_dot/H)². Its cross/spatial part is the exact time boundary

d/dt[c p²z²/H]=c p²z²+2c p²z z_dot/H,

because c_dot=3Hc and (p²)_dot=−2Hp². The final reduced action is

L_phys=c p² z_dot²/H².

The positive coefficient is finite for every fixed p>0,H>0. Its equation is z_ddot+H z_dot=0, with z=z_0(k)+z_1(k)e^(−Ht). The principal high-frequency characteristic has only ω²=0; no p² restoring term or nonzero scalar sound speed is generated. In real space the equation is Δ_coord(z_ddot+H z_dot)=0, and the k>0/appropriate spatial boundary restriction removes the harmonic ambiguity. Positivity of this quadratic temporal energy is not uniform coercivity of static spatial fluctuations or a full nonlinear well-posedness theorem.

## Canonical constraints rather than lapse-only inference

The canonical momenta are P_e=−2cf and P_z=c[−6f−2(e_dot+p²β)]. The (z,e) velocity block is invertible before imposing constraints. With lapse and shift momenta initially zero the actual canonical Hamiltonian is

H_can=HνP_z−P_zP_e/(2c)+3P_e²/(4c)−p²βP_e
      −c[p²z²+2p²νz+(3/2)H²D²+p²ν²].

The lapse secondary C_ν=∂H_can/∂ν has derivative −c(2p²+3H²)≠0. Therefore P_ν,C_ν are a second-class pair. Their solution is

ν=[HP_z/c−2p²z−3H²(3z+e)]/(2p²+3H²).

After their removal the remaining (z,e) brackets stay canonical. Define

D_bar=[HP_z/c+2p²(2z+e)]/(2p²+3H²).

The shift primary P_β gives secondary P_e=0; preserving P_e gives 3cH²D_bar=0. Preserving D_bar gives a fourth constraint C_4 which fixes β, because its β coefficient is −2p^4/(2p²+3H²)≠0. Here p^4 means (p²)². Also {P_e,D_bar}=−2p²/(2p²+3H²)≠0. The antisymmetric matrix for (P_β,P_e,D_bar,C_4) has determinant {P_β,C_4}²{P_e,D_bar}²>0: the other brackets cannot change that determinant since the P_β row has only its C_4 entry. Preserving C_4 fixes the primary shift multiplier. There is no extra tertiary beyond this completed four-member chain.

Consequently the four relative configurations (z,e,ν,β), eight phase coordinates, lose six second-class constraints and leave **one quadratic relative metric configuration degree**. This is a linear finite-k count, separate from the mean Einstein gauge sector and accidental clock flat direction; it is not the nonlinear full-theory count.

On P_e=D_bar=0, e=−2z−HP_z/(2cp²) and the raw physical Hamiltonian is H²P_z²/(4cp²)−HzP_z. The boundary transformation F=cp²z²/H sets Π=P_z−2cp²z/H, yielding

H_phys=H²Π²/(4cp²)≥0, with strictly positive quadratic coefficient,

with the explicit time derivative F_t=cp²z² included. This is the same reduced action sign, not the indefinite unreduced conformal Einstein kinetic sign.

## Exceptional limits and first missing implication

The homogeneous k=0 branch cannot use the shift/shear chain above: e=ΔE vanishes identically, and p² divisions are forbidden. The separately reviewed positive homogeneous reduction is therefore compatible with this finite-k result. The finite-k kinetic coefficient tends to zero at k→0, so no uniform inference is made.

At A=0 the admitted flat background has H=0. Its raw quadratic action instead has shift equation z_dot=0; substituting ν=z_dot/H is invalid. The flat rank branch must be analyzed directly. The present de Sitter reduction diverges as H→0 at fixed p and does not produce a uniform positive-clock propagator there.

At coincidence the common clock has no quadratic interaction action. Finite-k relative positive temporal kinetics plus zero restoring term do not settle the nonlinear clock degree, cubic gradient dynamics, sourced boundary conditions, EFT cutoff or full scalar stability. No cold density, primordial amplitude, lensing/source response or 32pi normalization is inferred. The next physical arrow is the nonlinear/spatial constraint and sourced scalar response on this degenerate background, not an imported fluid dictionary.

## Reproducible evidence

checks.py reconstructs the Legendre transform and constraints from the displayed raw Lagrangian without importing parent functions. It checks lapse/shift/shear preservation, the four-constraint determinant, time-dependent boundary transformation, volume square, common-clock cancellation and separate flat shift equation. The three negative controls falsely erase the physical relative shear, assert a positive restoring term and extend the reduced H>0 formula uniformly to flat H=0. Standard bounded manifests and counts are recorded separately in RUNS.json.

The initial development preflight is preserved under preflight/: 24/25. Its only failure came from asking symbolic replacement of an expanded f=z_dot−Hν expression to enforce f=0. The final check substitutes the actual equation ν=z_dot/H, obtaining zero without changing the mathematical formula. It is not counted as passed evidence. Final proof uses all displayed equations rather than a test count. No external classification theorem or full Dirac field theorem is invoked.
