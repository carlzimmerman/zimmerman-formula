# Density relaxation: a conditional bridge and its dynamical failure

Base: 0374ab1f68a6139d5a50df21fe751e468c764654. This is a new common-energy probe following the closed-ensemble obstruction. It uses an extended planar free-band response, not finite spheres. The original target is still a consistent physical theory selecting exactly 32pi; the construction below does not meet it.

## Assumed energy, derived response

Use c=hbar=1. Let q>0 be area per volume, P=|p|, and K=nu y^3/(6pi v^2). Assume

E(q,P)=U(q)+KqP^3, U(q)=A/q^2+Bq^2, A,B>0.

The positive inverse-square and compression terms are a tractable test of density feedback, not a derived microscopic network energy. With q and P of mass dimension one, A has dimension six, B dimension two, and K is dimensionless. At each uniform P, treat q as a freely relaxing variable. Conservation and spatial compatibility are not imposed in this minimization; they are tested separately below.

The energy is strictly convex in q and diverges at both ends, so it has one global minimum. It satisfies

-2A/q^3+2Bq+KP^3=0,

q0=(A/B)^(1/4), U0=2sqrt(AB), U''(q0)=8B.

At small P,

q(P)=q0-KP^3/(8B)+O(P^6),

E_min(P)=U0+Kq0P^3-K^2P^6/(16B)+O(P^9).

Retain the earlier assumed critical matching W=P^2/2+4pi G[E_min(P)-U0] in W_total=g_field^2/2-g_field dot p+W. The homogeneous constitutive relation is then

g_field=P+b(P), b(P)=12pi G K q(P) P^2,

a0_bare=1/(12pi G K q0)=v^2/(2G nu y^3 q0).

Envelope differentiation is legitimate because the q minimizer is unique and U''>0. Moreover

db/dP=12pi G K P [6A/q^3+10Bq]/[6A/q^4+2B]>0.

Thus the uniform static relation is single valued and monotone at every P>0. This is a useful full-field improvement over an isolated cubic expansion. It is not a dynamical stability proof or a nonuniform galaxy solution.

At large P, q(P)~(2A/K)^(1/3)/P, so b(P)~DP with

D=12pi G(2AK^2)^(1/3)>0.

The asymptotic induction fraction is mu_infinity=b/g_field=D/(1+D). If the spherical source law remains b=GM/r^2, the Newton constant inferred at large field is G_N=G/mu_infinity. The observational deep acceleration scale is therefore a0_N=mu_infinity*a0_bare, obtained by writing the small-field law g_field^2=G_N M a0_N/r^2. Using bare G and a0 interchangeably with their Newton-calibrated values would give the wrong coefficient.

## What stationarity removes, and what it leaves free

Define Lambda_proxy=8pi G U0. It equals a physical vacuum curvature only if a covariant completion actually sustains vacuum stress U0. That condition fails for the simplest material implementation below, so this name is essential.

With no added constant in U,

Lambda_proxy/a0_bare^2 = (2/3)D^3,

Lambda_proxy/a0_N^2 = (2/3)D(1+D)^2.

These identities follow from q0^2 U0=2A and the expressions above; the compression coefficient B cancels. In the microscopic surface notation the bare ratio is 64pi G^3 A nu^2 y^6/v^4. Stationarity removes B and the equilibrium density from the ratio, while leaving the independent dimensionless combination in D. It therefore makes the missing coefficient-selection problem more explicit, rather than solving it.

The desired value 32pi would require D(1+D)^2=48pi, or D approximately 4.67775639 after Newton calibration. This is a necessary target condition, not a predicted D, and no parameter is set to it in the model or tests. A permitted additive constant rho_constant changes Lambda_proxy by 8pi G rho_constant without changing q(P), a0 or D. No symmetry forbidding that constant has been supplied. The exact ratio hence depends on a second vacuum-sector assumption even if D were selected.

## Covariant conserved-material test

Try to implement q with three material-coordinate scalar fields phi^I using B_material^{IJ}=g^{mu nu}partial_mu phi^I partial_nu phi^J and q=(det B_material)^(1/6), on the positive spatial branch. Overall normalization can be absorbed into the material coordinates; identifying this q with the planar area density is itself a coarse-graining assumption. Take the density-only action L=-U(q), minimally coupled to gravity. The determinant form has fluid symmetry and no shear rigidity; it is not the full polarization action.

On an isotropic background, direct metric variation gives

rho=U(q), pressure=-U(q)+qU'(q)/3.

At q=q0 the stress is vacuum-like. But with conserved homogeneous material labels phi^I=q_comoving x^I in an FLRW spacetime,

q=q_comoving/a(t), dot q=-Hq.

Consequently an expanding universe cannot hold q=q0. A constant rescaling of the labels only changes q_comoving. A time-dependent rescaling is a different moving configuration, not the same conserved homogeneous medium. For this U,

pressure=-5A/(3q^2)-Bq^2/3.

The inverse-density contribution grows as a^2, whereas the compression contribution falls as a^-2. Vacuum stress at the minimum is an instant along this branch, not a de Sitter attractor. The continuity equation dot rho+3H(rho+pressure)=0 holds exactly; the failure is not an omitted conservation term.

Local fluctuations expose a second problem. In a flat local rest frame write phi^I=q(x^I+pi^I). For a spatially uniform time perturbation, det B_material=q^6(1-dot pi^2), so

L^(2)_time = [qU'(q)/6] dot pi^2 = [(rho+pressure)/2] dot pi^2.

At q0 this kinetic coefficient vanishes, while U''(q0)>0 leaves a nonzero compression cost. Ordinary propagating-phonon perturbation theory loses its Gaussian time evolution there. For q<q0, which continued expansion reaches, the coefficient is negative: this leading local material action has a wrong-sign phonon time kinetic term. Extra fields or higher derivative dynamics could change the conclusion, but would require a new calculation of the background, stress and coefficient. A minimum of a static energy is insufficient to certify a healthy vacuum medium.

Primary framework check: Endlich, Nicolis and Wang, [Solid inflation, arXiv:1210.0569v1](https://arxiv.org/html/1210.0569), Section 2 equations 2.9-2.13 and Section 3 equations 3.3 and 3.12. These establish the material-coordinate determinant action, stress and suppressed phonon kinetic term near the vacuum equation of state. The particular density potential, constitutive bridge and local determinant expansion above are our own calculations. This does not import a theorem excluding all solids, all preferred-clock media, or all dark-energy models. SciSpace supplied discovery candidates only, with no theorem used from its abstracts.

## Evidence, decision and next requirement

The bounded run passes 35 checks: symbolic stationarity, monotone force expression, coefficient calibration and shift freedom, exact conservation, and a direct determinant expansion for the phonon kinetic term; bracketed roots and independently differenced force slopes for two positive parameter sets over P=1e-4 to 1e4. Maximum root residual is about 8.8e-13; maximum relative force-slope discrepancy about 1.9e-11. The algebraic proof, not the finite parameter grid, establishes positivity for all positive parameters.

Self-review: the formal uniform-energy bridge is valid with the stated potential, subtraction, free relaxation and critical matching. Physical Lambda, independent selection of D and the vacuum constant, homogeneous cosmological persistence, and a healthy density dynamics are not established. The conserved material-coordinate implementation fails the last two requirements. This prevents promoting the proxy identity to the requested groundbreaking physical equation.

The constructive continuation must change the failed density implementation, not merely retune A or B. A nonconserved order parameter or an explicit creation/clock sector might keep physical area density stationary and supply kinetic energy; its full stress and interactions must be included. The constant-energy freedom and D selection remain independent obligations. The current route is open with those changes, while the unmodified conserved-density completion is closed as a consistent vacuum solution.
