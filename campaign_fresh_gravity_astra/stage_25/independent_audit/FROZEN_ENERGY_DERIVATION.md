# Independently frozen FGF038 exact lower-energy proof

Derived before reading any new author/root proof or formula preview. Proof-only, no computation. Fix the Q crossing on I=(-h0,h0), length ell, with the inherited positive physical constants C,cs²,J,S0 and positive density rho. Use Eulerian (r,psi,eta): integral r=0, |r|<=rho/2, psi,eta in H1_0, ||eta||infinity<=kappa=1/4. Actual scale changes from a=a_ref exp chi to a exp eta. All new states have finite exact energy: a and a exp eta are bounded positive, g+psi' is L2, density bounded positive, potentials/scale fields bounded. No exact material-displacement identification of r is used.

## A global scalar lower bound

Write F_a(v)=W(|v|,a), A(v,a)=2|v|/sqrt(a²+4v²), B=F_a'(g). This is C2 in signed v, with nonnegative A. The exact identity

 D_a(g,h)=F_a(g+h)-F_a(g)-B h
        =h² integral_0^1(1-t)A(g+t h,a)dt

is valid without any pointwise smallness assumption. For g=0 the target A(g)h² is zero and convexity suffices. For g!=0: if |h|<=2|g|, then |g+t h|>=|g|/2 for 0<=t<=1/4. If |h|>2|g|, then |g+t h|>|g|/2 for 3/4<=t<=1. Monotonicity in |v| and A(g/2,a)>=A(g,a)/2 give lower constants 7/64 and 1/64 respectively. Thus globally, for both signs and arbitrary h,

    D_a(g,h) >= A(g,a) h²/64.

This is deliberately nonoptimal and remains valid at g=0 or h=0. It is not a uniform upper/Taylor approximation.

## Finite scale response

Put s=|g|. At fixed signed g, partial_chi F=-T, partial_chi B=-sgn(g)q,
q=s A-b=a b/sqrt(a²+4s²)>=0, and S=partial_chi T=2T-sq.
Direct Q inequalities give 0<=q<=b<=s²/a. Since T_s=q and T(0)=0,
0<=T<=s³/(3a), and S<=2s³/(3a). These are global bounds in s, not small-gradient truncations.

For |eta|<=kappa, A(g,a exp eta)>=exp(-kappa)A(g,a). Set c0=exp(-kappa)/64.
Decompose the field relative term exactly:

 R_F=F_(a exp eta)(g+h)-F_a(g)-B_a(g)h+T_a(g)eta
    =D_(a exp eta)(g,h)
     +[B_(a exp eta)(g)-B_a(g)]h
     +F_(a exp eta)(g)-F_a(g)+T_a(g)eta.

The first term is >=c0 A h². The flux difference is bounded in absolute value by exp(kappa)s²|eta|/a. Exact one-dimensional Taylor integration in eta bounds the final scale remainder below by -exp(kappa)s³ eta²/(3a), since second chi derivative of F is -S. Young's inequality then gives

 R_F >= (c0/2) A h² - K(x) eta²,
 K(x)=exp(2kappa)s^4/[2c0 a² A]+exp(kappa)s³/(3a).

The quotient is set to zero at s=0, its continuous extension. Since A~2s/a at the crossing, K=O(s³)=O(|x|^(3/2)), and its maximum on a shortened patch is finite and tends to zero. No evaluation of the constitutive coefficients at the possibly large new gradient is needed in K; the global scalar bound handles that gradient.

## Exact complete relative energy and stationarity

Let e(rho)=cs²rho(log(rho/rho_ref)-1), U=S0(cosh(2chi)-1)/4. The exact relative entropy is

 R_e=e(rho+r)-e(rho)-e'(rho)r
    =cs²rho[(1+r/rho)log(1+r/rho)-r/rho].

Because e''(rho+t r)>=2cs²/(3rho), R_e>=cs²r²/(3rho). Let U_rel=U(chi+eta)-U(chi)-U'(chi)eta; U''>=S0 gives U_rel>=S0 eta²/2.

The exact static energy difference is

 DeltaE=int [R_e+r psi+(R_F+J eta'²/2+U_rel)/C].

To obtain this identity retain all first variations: (e'(rho)+phi)r integrates to zero by constant hydrostatic multiplier and integral r=0; int rho psi+int B psi'/C cancels by signed MOND B'=C rho and outer zero trace; int[J chi' eta'+(U'-T)eta]/C vanishes by J chi''=U'-T and fixed scale walls. There is no source replacement g'=C rho and no removal of r psi. The perturbations need not be new equilibria; they are admissible finite-action states with the stated constraints.

## Full short-patch lower bound

Define E_r=int cs²r²/rho, E_p=int A psi'²/C, E_eta=int J eta'²/C, R=max rho, P=ell int_I 1/A, and Kmax=max_I K. Weighted endpoint Cauchy gives ||psi||²<=P int A psi'²; ordinary endpoint integration gives ||eta||²<=ell² int eta'². Young's inequality on the matter coupling yields

 |int r psi| <= E_r/6 + [3R/(2cs²)]||psi||².

Hence, with alpha=3 C R P/(2cs²) and gamma=Kmax ell²/J,

 DeltaE >= E_r/6 + (c0/2-alpha)E_p
                  +(1/2-gamma)E_eta + S0/(2C)int eta².

Sufficient explicit gates are alpha<=c0/4 and gamma<=1/4. Under them,

 DeltaE >= E_r/6 + (c0/4)E_p + E_eta/4 + S0/(2C)int eta².

They hold for all sufficiently short restrictions of the SAME central solution: R remains bounded positive, P=O(ell^(3/2)) and Kmax=O(ell^(3/2)); gamma=O(ell^(7/2)). The dimensionless gates are C R P/cs² and Kmax ell²/J; all energy terms have energy-per-transverse-area units. The constants depend only on inherited physical coefficients, fixed cap kappa, and the actual background through these displayed functions. There is no numerical length, fitted potential or scan.

This lower bound is uniform for the stated finite-action capped class, including arbitrarily large potential gradients. Vanishing distances imply r=psi=eta=0 by positivity away from the single center and zero outer traces. It is a restricted strict energetic minimum. It is not a cap-preservation theorem, nonlinear Cauchy theorem, conservative evolution construction or dynamical stability statement. Both a0 values and separate vacuum/frozen-H/actual evolving-H hypotheses remain; Q only. FGF037's infinite-energy completed directions are excluded by the finite-action premise, and its smooth high-energy concentrations are compatible with this lower bound. No uniform upper/Taylor bound is restored. No physical metric/photon, scale-vacuum, RAR/M or empirical transfer is asserted.
