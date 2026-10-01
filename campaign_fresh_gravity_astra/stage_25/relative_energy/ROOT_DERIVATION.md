# Exact coupled relative-energy lower bound on a capped finite-action class

2026-09-30 19:31 UTC pass. Root proof frozen before reading any new author or
reviewer derivation or formula preview. Task038 suggests a scalar lower-bound
route. No computation or literature mechanism is used. Constants below are
conservative sufficient bounds, not sharp constants or measured radii.

Fix ONE inherited Q crossing and restrict it to I=(-l,l), with all central
data and positive physical coefficients C=4piG, cs²,J,S0,a_ref unchanged.
The inherited energy is
E=integral[e(rho)+rho phi+(W(|phi'|,a)+J chi'^2/2+U(chi))/C],
a=a_ref exp chi, U=S0(cosh(2chi)-1)/4, e''(rho)=cs²/rho.
Its actual equilibrium satisfies e'(rho)+phi=mu constant,
B'=C rho, and -J chi''+U'+W_chi=0. Here
B(g,a)=sgn(g)b(|g|,a), b(s,a)=(sqrt(a²+4s²)-a)/2,
W(s,a)=integral_0^s b(v,a)dv, A(g,a)=2|g|/sqrt(a²+4g²).
At the center g~sgn(x)const sqrt(|x|), rho>0, a>0, A~const sqrt(|x|).
The signed MOND flux, not a Newtonian Poisson source, is essential.

Admissible Eulerian states have rho_new=rho+r, phi_new=phi+psi,
chi_new=chi+eta, with integral r=0, |r|<=rho/2 a.e., psi,eta in H1_0(I),
and |eta|<=d=1/4 a.e. These are imposed caps, not claimed invariant regions.
Scale becomes a exp eta. In 1D the fields are bounded and all these exact
energies are finite; Q growth at bounded positive a makes psi' in L2 sufficient.
This is not a finite material-displacement parametrization.

## A global scalar lower bound, including sign reversal and large gradients

Let F_a(v)=W(|v|,a). Then F_a''(v)=A(v,a), continuously including v=0.
For all real g,h,
D_a(g,h)=F_a(g+h)-F_a(g)-B(g,a)h
        =h² integral_0^1 (1-t) A(g+th,a)dt.

For s>=0, A(s,a) is increasing and concave, since
A_s=2a²/(a²+4s²)^(3/2)>0,
A_ss=-24a²s/(a²+4s²)^(5/2)<=0.
Thus A(s/2,a)>=A(s,a)/2. If |h|<=2|g|, for t in [0,1/4]
|g+th|>=|g|/2 and integral_0^(1/4)(1-t)dt=7/32.
This gives D>=7 A(g,a)h²/64. If |h|>2|g|, for t in [3/4,1]
|g+th|>=t|h|-|g|>|g|/2, and integral_(3/4)^1(1-t)dt=1/32.
This gives D>=A(g,a)h²/64. For g=0 the same final bound is zero
and follows directly from convexity. Consequently, universally,

D_a(g,h)>= A(g,a)h²/64.                                      (1)

No small-h assumption or deep-MOND truncation was made. The constant is
intentionally weak. For a'=a exp eta with |eta|<=d,
A(g,a')>=exp(-d)A(g,a); hence D_a'(g,h)>=k A(g,a)h²,
where k=exp(-d)/64 is a fixed dimensionless positive constant.

## Exact matter and scale cancellation

Set h=psi'. Subtract every first variation of E, using the three equilibrium
equations, zero field traces and integral r=0. Integration by parts is valid
through the crossing: B is C1, chi is regular, and no central flux jump exists.
The exact remainder is

DeltaE=integral [H_e(rho,r)+r psi]
 +(1/C)integral [D_a'(g,h)+(B(g,a')-B(g,a))h
   +R_W(g,chi,eta)+J eta'^2/2+R_U(chi,eta)],                  (2)
H_e=e(rho+r)-e(rho)-e'(rho)r,
R_W=F_a'(g)-F_a(g)-W_chi(g,a)eta,
R_U=U(chi+eta)-U(chi)-U'(chi)eta.

In R_W only, F_a'(g) means F evaluated at a'=a exp eta, not differentiation;
the unambiguous expression is W(|g|,a exp eta)-W(|g|,a)-W_chi(|g|,a)eta.
The term rho psi cancels -B h/C after integration; e'(rho)r+phi r integrates
to zero. Scale-gradient and potential first variations cancel W_chi eta.
All mixed terms r psi and the exact finite scale change are retained.

For |r|<=rho/2, e''(rho+t r)>=2cs²/(3rho), giving H_e>=cs²r²/(3rho).
Since U''=S0 cosh(2chi)>=S0, R_U>=S0 eta²/2.
Define coefficient functions on the fixed background, with |theta|<=d,
qcap(x)=sup |partial_theta B(g(x),a(x)exp theta)|,
K_l=sup_(x,theta) |partial_theta² W(|g(x)|,a(x)exp theta)|,
L_l=sup_x qcap(x)²/A(g(x),a(x)), with its continuous zero value at x=0.
Taylor integration only in the bounded SCALE coordinate gives
|B(g,a')-B(g,a)|<=qcap |eta| and R_W>=-K_l eta²/2.
This does not assume a Taylor theorem in the failed weighted potential norm.

These constants tend to zero as l tends to zero on the SAME crossing.
Indeed |partial_theta B|=a_theta(1-a_theta/sqrt(a_theta²+4g²))/2
<=g²/a_theta. Bounded positive a_theta then gives qcap²/A=O(|g|³)=O(l^(3/2)).
For K_l, directly differentiating the integral defining W gives integrand
(2a_theta²/sqrt(a_theta²+4v²)-a_theta^4/(a_theta²+4v²)^(3/2)-a_theta)/2.
It is uniformly continuous on compact positive a_theta ranges and vanishes
at v=0. Its integral from 0 to |g| tends uniformly to zero. Thus K_l->0.
A quantitative asymptotic or numerical radius is unnecessary for existence.

Using ab<=epsilon a²/2+b²/(2epsilon), the finite scale cross term obeys
(B(g,a')-B(g,a))h >= -k A h²/2 -qcap² eta²/(2k A).
At the center both A and qcap vanish, so interpret the bound by continuity.
Together with (1), the exact field/scale remainder is bounded below by
k A h²/2 +J eta'^2/2 +(S0-K_l-L_l/k)eta²/2.                (3)
Choose the first explicit shortness gate

K_l+L_l/k <= S0/2.                                         (4)

## Full coupled lower bound

Let R_l=integral_I 1/A, P_l=2l R_l. The inherited crossing gives
R_l=O(sqrt(l)), P_l=O(l^(3/2)), and zero traces yield
integral psi² <= P_l integral A psi'^2.
Young's inequality gives
r psi >= -cs²r²/(6rho) -3rho psi²/(2cs²).
Choose the second gate

3 C rho_max P_l/cs² <= k/2.                                (5)

Equations (2)-(5) then prove for EVERY admissible capped finite-action state

DeltaE >= (1/6)integral cs² r²/rho
       +(k/(4C))integral A psi'^2
       +(J/(2C))integral eta'^2 +(S0/(4C))integral eta².      (6)

Both gates hold on all sufficiently short restrictions of the same central
solution, since rho is bounded and S0>0 is fixed. Walls and mass are induced
by restriction; no coefficient is retuned, and no numerical physical size is
specified. All terms have their original energy-per-transverse-area units.
For nonzero perturbations the right side is strictly positive: A>0 a.e.,
rho>0, and field traces remove constants. This is a restricted exact nonlinear
energetic minimum with explicit caps and sufficient coefficient gates.

## What is and is not established

This lower bound is compatible with FGF037: its smooth concentrated states
have large positive exact energy and small weighted distance. The reverse
upper bound and weighted continuity still fail; singular infinite-energy
states remain excluded here. No nonlinear existence, uniqueness, energy
conservation for weak solutions, invariance of density/scale caps, regularity
through the crossing, or actual nonlinear stability follows without further
proof. Linear weighted evolution need not preserve this finite-action class.
A conditional a-priori use of (6) along an energy-conserving admissible solution
is allowed, but is not a construction of that solution.

Both positive reference values a0=9.3619e-11 and 1.1279e-10 m/s² apply to
separate backgrounds; coefficients and crossing size are not identified across
them. Constant-vacuum reference, frozen a0 E(z), E²=.315(1+z)^3+.685, and evolving
H branches remain distinct. Evolving reference energy work needs a conserving
reservoir. The locally responsive scale is an added diagnostic hypothesis.
This is Q only, not RAR, M or filtered MONO, and establishes no physical
metric/photon/gravitational DOF result, calibrated observation or novelty.
