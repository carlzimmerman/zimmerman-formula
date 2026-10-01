# Independently frozen FGF040 force-domain and combined momentum derivation

Derived before reading new author/root proofs or previews. Proof-only; no numerical scan. Retain one fixed-reference Q crossing on I=(-d,d), ell=2d, mass M=int rho, and inherited positive C,cs²,tau,sigma,J,S0. Actual fields below are phi,chi; g=phi_x,w=chi_x,a=a_ref exp chi. Background is denoted phi0,chi0,rho. Scale perturbation is zero in the counterexample.

## One fixed-mass finite-energy force counterexample

Choose one fixed physical length 0<L0<d and positive potential amplitude P0. Put

 w_n(x)=1+(L0/abs(x))^(3/4) 1_(0<abs(x)<L0),
 Z_n=int_I w_n=ell+8L0,
 n(x)=M w_n(x)/Z_n.

Assign any finite nonnegative value at x=0; this single point changes no integral. This density is positive almost everywhere, has exact mass M and finite relative isothermal entropy, since abs(x)^(-3/4) times abs(log abs(x)) is locally integrable and rho is bounded positive.

Let zeta be a smooth cutoff compactly supported in (-L0,L0), equal to one on (-L0/2,L0/2), and set

 psi(x)=P0 sgn(x)(abs(x)/L0)^(2/3) zeta(x), psi(0)=0,
 phi=phi0+psi, chi=chi0, j=n v=0, phi_t=chi_t=0.

This continuous compactly supported psi is H1_0. Near zero its derivative is positive on BOTH sides and equals (2P0/(3L0))(abs(x)/L0)^(-1/3). The square is integrable, while the background gradient is bounded. Thus n phi_x is positive and comparable near zero to abs(x)^(-13/12), and is not L1_loc. There is no odd-sign cancellation or finite principal value rescuing this positive singularity.

Every exact energy component is finite. The internal energy follows from finite entropy; n(phi0+psi) is integrable since the potential is bounded; Q field energy obeys W(abs(phi_x),a)<=phi_x²/2; scale-gradient and U terms are unchanged finite background terms; all kinetic energies are zero. Density has no gradient-energy term in this action. Field endpoint perturbations vanish, mass is exact, the scale cap holds and zero fluid velocity is impermeable. These are energy-admissible data, not a claimed stationary or time-dependent solution. Static B_x=Cn is not an additional constraint on arbitrary initial configurations of the dynamic potential action. Failure of this force product does not prove global PDE ill-posedness.

## Smooth equations and exact momentum signs

For smooth positive-density solutions the inherited equations are

 n_t+(nv)_x=0,
 (nv)_t+(nv²+cs²n)_x=-n g,
 tau phi_tt-B_x=-C n,
 sigma chi_tt-J chi_xx=T-U',
 B=sgn(g)b(abs(g),a), W_x=B g_x-T w.

In particular B_x=Cn+tau phi_tt is the actual dynamic source relation. Define the field momenta with their physical translation signs

 p_phi=-tau phi_t g/C,
 p_chi=-sigma chi_t w/C.

Direct differentiation and the field equations give

 (p_phi)_t + partial_x[(tau phi_t²/2+gB-W)/C]
                          =n g+T w/C,
 (p_chi)_t + partial_x[(sigma chi_t²/2+Jw²/2-U)/C]
                          =-T w/C.

Indeed g B_x=partial_x(gB-W)-T w, fixing the scalar sign; the scale equation gives the opposite scale exchange. Adding matter momentum cancels BOTH n g and T w before any weak limit. Therefore

 partial_t P + partial_x S=0,
 P=nv-(tau phi_t phi_x+sigma chi_t chi_x)/C,
 S=nv²+cs²n+[tau phi_t²/2+gB-W+sigma chi_t²/2
                                     +J chi_x²/2-U]/C.

There is no separate n phi term in this final stress: the full matter/field equations have already accounted for that interaction in the force cancellation. The minus sign on U and plus signs on both field kinetic stresses and J chi_x²/2 are necessary. As a sign control on the original static equilibrium,

 partial_x[cs²rho+(gB-W+Jw²/2-U)/C]
   =-rho g+rho g+(T+Jw'-U')w/C=0.

This also checks the scale exchange and pressure sign independently.

## Finite fluxes and the precise spacetime hypotheses

Use matter momentum j=nv as the weak variable, with kinetic density j²/(2n): set it to zero at n=j=0 and infinity at n=0,j!=0. Finite kinetic energy forces j=0 on vacuum, but does not exclude vacuum. For Q, abs(B)<=abs(g), 0<=gB-W<=g²/2, and 0<=T<=g²/2. The stress bound follows by differentiating s b-W with respect to s: its derivative is s A<=s. Also abs(U')<=2U+S0/2 for the inherited cosh potential. These inequalities bound all displayed fluxes/sources from positive finite-energy components.

At a single time, n in L1 with fixed mass, j²/n in L1, phi_t,g,chi_t,w in L2, and U in L1 imply P,S in L1(I). Cauchy gives int abs(j)<=sqrt(M int j²/n), and the field momentum products are L2 times L2. The counterexample has P=0 and integrable stress even though n g is not locally integrable; it is not thereby made a static solution of the combined equation.

Slice-wise finiteness alone does NOT imply spacetime integrability. A sufficient explicit condition on every compact time interval K is local time-integrability of the positive components:

 integral_(K x I) [j²/n+n+phi_t²+g²+chi_t²+w²+U(chi)] < infinity,

with fixed positive dimensional weights understood. Locally bounded component energies are a stronger sufficient condition. With the retained scale cap, bounded a permits g²<=4W+a_max², so the g² condition may instead be supplied by a time-integrable field-action bound. No bound on these separate components is silently inferred from a signed total energy without proof. The fields/coefficients and products must be measurable. Cauchy in spacetime now gives P,S in L1_loc and all sources in the weak field equations are locally integrable.

A meaningful CANDIDATE distributional system on the interior is continuity, the two field equations and the combined momentum law, with test identities

 int[n zeta_t+j zeta_x]=0,
 int[-tau phi_t zeta_t+B zeta_x+C n zeta]=0,
 int[-sigma chi_t zeta_t+J chi_x zeta_x+(U'-T)zeta]=0,
 int[P zeta_t+S zeta_x]=0

for smooth compactly supported spacetime tests (initial data handled separately if sought). This formulation uses only defined products under the stated bounds. It agrees with the separate smooth equations when they are regular enough to justify the algebra. For rough states it is a changed weak-system choice; neither derivation from an undefined n g product nor equivalence to separate matter momentum is proved. Writing it proves no existence, uniqueness, energy inequality/equality or convergence of approximations. Weak limits of quadratic products can require additional compactness and can carry defects.

## Boundary traces and global momentum

For smooth states, integration yields

 d/dt int_I P = S(left)-S(right).

Finite L1 interior fluxes have no automatic boundary traces. To assert this balance in a rough class one needs appropriate normal stress traces and temporal control of total momentum; sufficient stronger hypotheses include spatial W1,1 stress with integrable wall traces and suitable temporal weak continuity, or a separately specified boundary weak identity. H1 field values alone do not give traces for their L2 gradients or kinetic stresses, nor does density L1 give a pressure trace.

Even smooth fixed Dirichlet field walls and impermeable matter walls do NOT imply zero total momentum flux. They set wall velocities relevant to energy work, but pressure and static field/scale stress may transmit forces to the walls. Total momentum is conserved only if net wall traction vanishes/balances or the supporting walls are included in the system. No artificial center wall appears: the weak identity is on the entire interval with compact interior tests. A distributional derivative of an L1 flux is meaningful even when its separate formal force terms are not.

This is a domain counterexample and a smooth conservative identity, together with a well-defined candidate weak system under explicit spacetime bounds. It is not a nonlinear theory or physical metric/covariant conservation proof. Both a0 choices and separate constant-vacuum/frozen-H/evolving-H hypotheses remain; actual evolving reference work is not silently dropped. Q only; RAR/M, scale-vacuum, photon/DOF/calibration and physical closure remain open.
