# Direct ultraviolet sphere response

FSP-008; coordinator derivation, separate from the pion and proton routes. This evaluates a global sphere observable in a different controlled regime. It does not transfer a small sphere to the cosmological radius.

## Theory, source and conventions

Take massless fixed-nf=3 SU(3) QCD plus one photon, with quark charges (2/3,-1/3,-1/3), u=e^2=4pi alpha, strong coupling g, and W=-log Z on round S4. Set V=Omega/H^4, Omega=8pi^2/3, and vary H at fixed renormalized g,u and subtraction scale mu. Then rho=-H partial_H W/(4V). This is a weak-coupling, small-sphere expansion, H large compared with the strong scale. It has no asserted continuation through confinement to H approaching zero. Physical massive thresholds require their own matching.

Primary input is De Cesare, Di Pietro and Serone, [arXiv:2212.11848v1](https://arxiv.org/abs/2212.11848v1), equations (4.1), (4.30), (4.39)-(4.44), (4.46). The source computes gauge-fixed global vacuum diagrams, including gauge volume and ghost zero-mode factors. Its stated finite constants use numerical reconstruction; the logarithmic coefficient used here is independently checked against its pole and one-loop beta coefficient. No reconstructed finite constant enters rho at this order.

## The full radius derivative of the two-loop term

Write N_V=N_c^2-1, b0=(11C_A-4nf T_F)/3 and L=gamma+log(4pi mu^2/H^2). The source's G2 is the signed sum, not its separately named positive fermion contribution. It gives

G2_fin=N_V { C_A[49+33L]/(144pi^2) - nf T_F[5+3L]/(36pi^2) },
W_int=-(g^2/2) G2_fin.

Consequently H partial_H G2_fin=-N_V b0/(8pi^2), and

rho_strong,int=-N_V b0 g^2/(64pi^2 V).

Here the renormalized expression has a fixed mu. Differentiating along a simultaneous running-parameter path instead would be a different operation. The source's log(g0^2 R^(4-d)) normalization and coupling pole cancel the UV pole at order g^2; no residual local curvature pole is added at that order. A finite local Euler or curvature-squared action is independent of H on S4 and cannot change this fixed-parameter derivative. We are not imposing the d=4+2epsilon fixed-point relation in (4.49).

For the photon keep only the fermion exchange graph, replacing its group trace N_V nf T_F by S=N_c sum_f Q_f^2. This is an abelianization of that graph's two vertices, not the invalid replacement SU(N_c) by SU(1). The photon has no non-Abelian self-interaction. Thus, up to radius-independent order-u constants,

W_photon,int=u S [5+3L]/(72pi^2),
rho_photon,int=u S/(48pi^2 V),
partial_alpha rho_photon,int=S H^4/(32pi^3).

This is the leading massless, zero-strong-coupling electromagnetic term. At nonzero strong coupling the mixed and higher diagrams have not been computed here. The graph includes all three quark flavors and color trace in this ultraviolet regime, without an empirical alpha.

The source pole normalization gives an independent check. Its gauge-loop pole cancels the pole from -N_V log g0, and RG invariance gives the same order-g^2 radius coefficient from beta_g partial_g(-N_V log g). For the photon beta_e=S e^3/(12pi^2), producing the same positive radius coefficient S u/(12pi^2) in R partial_R W. The source gravitational beta has no order-g^2 term. These checks retain the gauge-volume convention consistently; a coupling-dependent finite Euler redefinition changes the RG bookkeeping together and leaves the metric derivative invariant.

## Numerical-free coefficients for the declared theory

The free Euler coefficient is a=(62N_vectors+11N_Dirac)/360. There are nine vectors (eight gluons and one photon) and nine four-component Dirac color-flavor components, giving a=73/40. The logarithmic free determinant obeys H partial_H W_free=-4a and rho_free=a/V. With b0=9 and S=2 the result is

rho_UV(H)=H^4 { 219/(320pi^2) + [u-27g^2]/(64pi^4) + O(g^4,u^2,u g^2) },

partial_alpha rho_UV|_(g fixed)=H^4/(16pi^3) + higher orders.

All parameters and free-field normalizations are declared. A common flat vacuum subtraction in this massless perturbative scheme is scaleless. Higher loops, nonperturbative terms, physical mass/threshold and matching effects remain outside this formula. No proton has been computed in the weak-coupling sphere expansion. Dividing this expression by an assumed proton mass, or extending its H^4 behavior down to H=0, would not determine A_rho/m_p^3.

## Independent scalar spectral check

Before reading the pion agent's completed derivation, the coordinator reconstructs the scalar heat coefficients from its standard S4 spectrum. For n=l+3/2, degeneracy (n^3-n/4)/3 and eigenvalue n^2-9/4,

K(x)=exp(9x/4)/3 { 1/(2x^2)-1/(8x) + sum_(k>=0) (-x)^k/k! [zeta(-3-2k,3/2)-zeta(-1-2k,3/2)/4] }.

This is an asymptotic expansion; it is not summed as a convergent series. Exact rational coefficients through x^3 are checked in the bounded computation. The first four are 1/6,1/3,29/90,37/189. In the pion agent's declared decoupling subtraction through x^0, Watson's asymptotic expansion gives a per-real-scalar leading stress 37 H^6/(2016pi^2 M^2). Establishing the exact global determinant and remainder remains that route's independent task. This coefficient check does not supply full QCD or a uniform all-sector radius theorem.

## Outcome

This is an evaluated global weak-coupling sphere response and an independent scalar coefficient check. It supplies a second controlled radius regime with explicit charge dependence. The infrared global QCD functional, its matching to the individual proton and a principle selecting alpha remain open.
