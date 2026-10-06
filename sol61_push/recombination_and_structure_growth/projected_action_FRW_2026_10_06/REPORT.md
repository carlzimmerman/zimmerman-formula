# Exact matter-and-radiation admission of the projected action

The projected-acceleration action admits a visible ordinary flat GR radiation/dust/vacuum history, together with an explicitly reconstructible second metric. Its homogeneous interaction remains pure vacuum; it cannot supply an additional homogeneous cold density on this branch. This extends the previous empty homogeneous construction to conserved own-metric matter and supplies a consistent background on which physical recombination can be calculated. It does not calculate atomic transport or the cosmological perturbation transfer.

Base: d9a31e78aaca27a616448f47112cf1d46680ee1c. This route uses the changed operator, not the older nonminimal curvature-carrier action. Claude's unresolved growth and external-field tests remain obligations; the ordinary GR background does not transfer their answers to this action.

## Derive both sources before matching histories

Use n>=3 spatial dimensions, signature −+++, positive lapses N,L, common monotone clock theta=t, flat scales a,b>0, K>0, M=2K, chi_n=(n−1)/[2(n−2)]. The actual inherited action is

S=K integral(Vg Rg+Vh Rh)+2K chi_n a0² integral(v M_eff(I))+S_m[g]+S_h[hatg],
v=sqrt(Vg Vh), I=(gamma_inverse+hatgamma_inverse)^{ij} r_i r_j/(2a0²), r=ln(N/L).

Every homogeneous configuration has I=0 and its first variation zero. With M_eff(0)=−A define Lambda0=chi_n a0² A/2. The interaction reduces to −4K Lambda0 v. Varying each metric, before imposing equality or lapse relations, yields

Tg_int=−M Lambda0 Q g, Th_int=−M Lambda0/Q hatg,
Q=v/Vg=sqrt(L b^n/(N a^n))>0.

Consequently rho_g,int=M Lambda0 Q and p_g,int=−rho_g,int. The hatted sector has the reciprocal factor. No homogeneous pressureless term appears. In particular, a canonical relative momentum is not a matter abundance.

Assume matter is minimally coupled separately to its own metric and obeys its own on-shell continuity equation. Its conservation plus each Einstein Bianchi identity implies Lambda0 Qdot=0. For nonzero Lambda0 this forces Qdot=0 on any smooth homogeneous branch, not just the empty coincident solution. The shared-clock equation is satisfied: the acceleration invariant has vanishing first variation and diagonal covariance is respected. Independent metric conservation is used on shell, not asserted as two independent off-shell interaction symmetries. A=0 is a separate degenerate case and is not covered by this constant-Q argument.

Thus the two physical cosmological constants are Lambda_g=Lambda0 Q and Lambda_h=Lambda0/Q, with constant Q. The interaction has exactly w=−1 on this branch. It cannot redshift as a^-n or generate positive cold matter. In restored units Lambda0=chi_n A a0²/(2c^4); the offset A and Q remain free.

## Construct a radiation/dust history and the second metric

Choose visible proper time N=1. Let ordinary visible conserved densities satisfy rho_r/M=R a^(-(n+1)) and rho_d/M=D a^(-n), R,D>=0; p_r=rho_r/n, p_d=0. Keep any photon/baryon fractions and their currents as separate physical inputs. Set hatted ordinary matter to zero. Define

H_g²=2[Lambda0 Q+R a^(-(n+1))+D a^(-n)]/[n(n−1)],
h²=2 Lambda0/[Q n(n−1)]>0.

For the expanding solution a(t)>0, reconstruct

b(t)^n=B0+n h Q² integral_(t0)^t a(s)^n ds,
L(t)=Q² a(t)^n/b(t)^n.

On every interval where b^n>0, the lapse is positive, Q is the stated constant, and H_h=bdot/(Lb)=h exactly. Thus both Friedmann equations, both acceleration equations and the own-metric continuity equations hold. The hatted metric is de Sitter in its own proper time. The visible background admits mixtures of radiation and ordinary dust, with no analogue of the old carrier's F=0 obstruction. This statement supplies neither finite-k health nor positivity of an extra cold sector.

The visible acceleration equation follows from differentiated Friedmann and continuity:

Hdot_g=−[(n+1)R a^(-(n+1))+n D a^(-n)]/[n(n−1)].

The hatted Hdot in its proper time vanishes. These are full homogeneous Einstein equations because the independently varied interaction sources above are constant vacuum sources. The relative lapse was never fixed before variation. B0 and Q are integration data, not selected constants.

For an exact radiation-only family set h_g²=2 Lambda0 Q/[n(n−1)], u=(n+1)h_g t/2 and

a=C sinh(u)^(2/(n+1)), R=Lambda0 Q C^(n+1).

Then H_g=h_g coth(u), rho_r/M=Lambda0 Q csch(u)². The analogous dust-only family has u=n h_g t/2, a=C sinh(u)^(2/n), D=Lambda0 Q C^n. These give admitted nonempty histories for every positive A and Q. The mixed history is the smooth positive ODE above; no closed form is required.

## Early-time and atomic consequences

On a radiation-dominated visible branch, a~t^(2/(n+1)). If b^n tends to a positive B0 at the visible big bang, L~t^(2n/(n+1)); the second metric approaches a finite positive scale. If B0=0 with the integral starting at that singular boundary, b^n~t^((3n+1)/(n+1)) and L~1/t. Each interior t>0 has positive finite lapses; no smooth extension of the visible big-bang endpoint is claimed. The two choices show that an early visible radiation era does not require equal metrics or equal proper times.

In n=3, a conserved thermal photon bath has T=T_ref/a and n_gamma proportional T³, while conserved hydrogen has n_H proportional a^-3. Therefore eta=n_H/n_gamma is constant. With the ordinary baryon/photon normalization fixed, physical atomic rates may now be evaluated against H_g(T) from this action, instead of interpreting the old carrier's arbitrary reference slice as today. This is an admission statement: helium, photon distribution, actual ionization/escape rates, Thomson visibility and relative-sector perturbation evolution are still required to calculate recombination/structure. The hydrogen binding scale is an external laboratory input and does not follow from a0 or A.

No homogeneous additional dust is generated by the interaction. A positive cold abundance would require an inhomogeneous/nonlinear averaged solution, additional matter, or a changed branch/operator. The finite-k signed pressureless mode is a different sector and cannot be extended to k=0 by dividing by its k² formulas. This route leaves Lambda/a0², Q and the ordinary abundances undetermined. It proves neither 32pi nor identification of dark energy beyond the actual homogeneous vacuum stress.

## Verification scope

Exact algebra checks source variation, reciprocal volumes, Bianchi conservation, reconstructed second-metric lapse and Friedmann/acceleration, general-n radiation/dust families, early exponents and photon/hydrogen matching. Controls wrongly keep a time-dependent Q vacuum, identify homogeneous vacuum as dust, or mis-reconstruct the second lapse. The derivation is uniform in n; finite symbolic checks corroborate it and do not establish full field health. Inputs and revisions are frozen in the standard run manifests. Fresh independent review remains required before integration.
