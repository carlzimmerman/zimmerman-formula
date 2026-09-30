# A local parent for slow surface modes

Original 32pi goal remains OPEN. Base, hierarchy and limits: [SLOW_WALL_CONTRACT.md](SLOW_WALL_CONTRACT.md). The recorded computation passes 35/35 checks. This route addresses the earlier fractional free-band causality obstruction; it does not supply a complete gravitational theory.

## Local bulk operator and localized sheet

Use seven Hermitian anticommuting 8x8 matrices Gamma1 through Gamma7, with three momentum matrices and four mass matrices. An explicit tensor-product representation is in slow_wall_modes.py. In a chosen preferred frame, let

H = -iv(Gamma1 partial_x+Gamma2 partial_y)-ivz Gamma3 partial_z+g chi(z) Gamma4+y sum_i p_i Gamma_(i+4).

Here 0<v,vz<=1 and g>0. This is a local first-order operator. Its principal characteristic cone has maximum speed max(v,vz); nonderivative real bounded mass backgrounds do not change that cone. The tree scalar has its standard light cone. No dynamics or covariant completion for the auxiliary p or preferred frame has been derived.

Take U(chi)=lambda(chi²-f²)²/4, chi=f tanh(z/L), L=sqrt(2)/(sqrt(lambda)f). With C=i Gamma3 Gamma4, the C=+1 subspace has dimension four. Its normal envelope

psi(z) proportional to cosh(z/L)^(-g f L/vz)

solves vz partial_z psi+g chi psi=0 and decays exponentially at both ends. The remaining five Gamma matrices commute with C and give the surface Hamiltonian

H_surface=v(kx Gamma1+ky Gamma2)+y p_i Gamma_(i+4),

H_surface²=(v² k_parallel²+y²|p|²)I.

Thus the prior four-band surface model is obtained from a local parent instead of fractional spatial kinetics. The complete parent includes continuum and other bound modes. Only the massless surface branch is used in the following cubic calculation; the full bulk vacuum determinant, analytic counterterms and backreaction are not calculated. Projecting onto a normal envelope is nonlocal in the normal coordinate; the isolated projected branch must not be mistaken for the full local bulk field.

Masslessness is not fully protected by the internal rotation group alone: i Gamma1 Gamma2 commutes with its generators and the wall projector but anticommutes with the two surface kinetic matrices. It is an allowed rotation-singlet surface mass. A further physical symmetry or dynamics must exclude this operator. The kink index alone does not prove the isotropic response sector is gapless under every allowed perturbation.

## Speed scaling and a controlled locality window

Changing variables l=v k_parallel in the sheet integral gives, after the same analytic subtraction as the earlier sheet calculation,

rho_sheet(P)=nu y³ P³/(6pi v²),

alpha=2Gnu y³/(3ell v²), a0=ell v²/(2Gnu y³).

Area per volume is 1/ell. The quadratic gravitational matching remains assumed. For the one four-band flavor, nu=2, the uniform finite-mass kernels obey DeltaPi_v(q)=y² DeltaPi_1(vq)/v². Their small-q stiffnesses are y²q²/(6pi m) and y²q²/(4pi m), independent of v. Their massless limit is y²|q|/(4v). Therefore the derivative expansion requires vq<<m=yP, rather than q<<m.

For P~A/r, its dimensionless parameter is epsilon=v/(yA). At fixed A a small positive mode velocity improves the hierarchy; increasing radius does not improve this particular parameter. The example A=(200 km/s divided by c)², y=1, v=1e-9 gives epsilon about 0.00225. This is a hypothetical hierarchy, not an astrophysically identified medium or a selected velocity.

## Leading nonuniform correction under plane averaging

For a dense isotropic ensemble of thin locally planar sheets, the mean in-plane momentum squared is 2q²/3. Assume the wavelength exceeds sheet separation and thickness, and assume epsilon<<1. In the same normalization as the polarization functional, the leading gradient energy for nu=2 is

E_grad=(AL/(2P))|grad P|²+(AT P/2)|grad n|²,

AL=4Gy/(9ell), AT=2Gy/(3ell), n=p/P.

For n=rhat, |grad n|²=2/r². Varying this energy and putting P=A/r gives

f_grad=AL P'^2/(2P²)-AL(P''+2P'/r)/P+AT/r²=8Gy/(9ell r²).

Combining g=P+P²/a0+f_grad and g-P=GM/r² gives the formal leading-gradient branch

A²=G a0 [M-8y/(9ell)].

The derivative correction relative to the cubic term is 2epsilon²/9. It is small in the declared slow-mode regime. The apparent mass offset must not be extrapolated to a minimum galaxy mass: near vanishing A, epsilon ceases to be small and the derivation fails. Higher derivative terms, sheet geometry, network statistics and a full nonuniform determinant remain uncomputed. This is a more local controlled regime, not an exact BTFR proof.

## The same walls fail the vacuum-stress requirement

The scalar kink first integral gives positive tree tension sigma=2sqrt(2)sqrt(lambda) f³/3. A static flat wall has normal pressure zero and two tangential pressures minus its energy density. Isotropic orientation averaging gives w=-2/3. A boost at normal speed u gives w=-2/3+u²; no real u makes w=-1 for positive-tension walls. The speed u of the wall is distinct from v of its fermion modes.

For frozen comoving walls, ell proportional to scale factor a, rho_wall=sigma/ell proportional to a^-1, while the surface response a0 is proportional to a at fixed couplings and mode velocity. Consequently 8pi G rho_wall/a0² is proportional to a^-3. It does not give a constant relation to a cosmological constant.

Even if one ignored that stress failure and defined a density proxy Lambda_proxy=8pi G sigma/ell, the coefficient would be

Lambda_proxy/a0²=32pi G³nu²y⁶sigma/(ell³v⁴).

The multiplicative factor is undetermined; setting it to one is not a derivation. The real bulk vacuum minimum can also be shifted by an independent constant without changing the tree kink tension or surface cubic. The unmodified positive-tension network therefore fails the requested common galaxy/vacuum mechanism, even though the local surface response survives.

## Evidence and continuation

Self-review verdict: correct only under the stated local probe, one-loop branch and derivative assumptions; the wall stress obstruction is exact for positive-tension wall ensembles. No independent reviewer was used. Symbolic checks include the Clifford projector, normal profile, singlet mass, kink equation, determinant scaling, gradient variation, stress and cosmological scalings. Eight bubble quadratures check the speed rescaling. Proofreading covered these new files; no failed run or mathematical-token correction occurred.

SciSpace supplied domain-wall discovery candidates. Primary source checked: Stojkovic, [Fermionic Zero Modes on Domain Walls, hep-ph/0007343v2](https://arxiv.org/pdf/hep-ph/0007343), 30 January 2001, Sections II–III, including the scalar kink and fermion equations. It supports the sign-changing-mass method, not the exact eight-band operator or our velocity/stress claims, which are derived above. No source cache was created. The attempted HTML for arXiv:1010.3195v2 was unavailable and supplies no evidence here.

Open continuation: a covariant medium with a physical symmetry excluding the singlet gap, critical matching, selected density/speed and genuinely vacuum-like total stress. The present wall network is closed as a sole source of Lambda under its positive-tension assumptions. Additional matter or energy exchange may change its stress, but would require a new action and a recalculation of a0 rather than relabeling this result.
