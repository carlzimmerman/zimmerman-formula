# Constrained-Foliation (Cuscuton) MOND Gravity — frozen candidate 2026-08-22

## The action
S = (c^3/16piG) INT d^4x sqrt(-g) [ R + (2 a0(T)^2/c^4) F(X) ] + S_cusc + S_m
  S_cusc = INT d^4x sqrt(-g) [ mu^2 sqrt(-grad_a T grad^a T) - V(T) ]
  u_mu = -grad_mu T/sqrt(-grad T.grad T),  a_mu = u^nu grad_nu u_mu,  K = grad_mu u^mu
  X = a_mu a^mu / a0(T)^2 ,  a0(T) = (c/Z) q(T) ,  q(T) = V'(T)/mu^2
  F(X) = -2 sqrt(X) + 2 ln(1+sqrt(X))  =>  mu(x) = x/(1+x), x = |grad Phi|/a0.

## Why this replaces R+A^2+CMC
R+A^2 has lambda_eff = (1+beta/3)/(1+beta) = 2/3 at beta=1, and NO finite beta reaches the
kinetic-conformal 1/3 (needs 3=1).  So the Bellorin-Restuccia scalar-elimination theorem does
NOT apply, and (retraction test) the naive "zeta-dot^2 after CMC" flags a scalar even in pure
GR (+6), so it proved nothing.  R+A^2 also broke c_T (needed 2(3)R repair) and tangled three
coefficient conditions.  The cuscuton dissolves all of it.

## DERIVED (sympy-verified)
1. NON-DYNAMICAL SCALAR.  In unitary gauge T=t, sqrt(-grad T.grad T)=1/N, so
   L_cusc sqrt(-g) = [mu^2 - V N] sqrt(h): NO Tdot, NO hdot.  T is a constraint field, not a
   propagating scalar (Afshordi-Chung-Geshnizjani cuscuton property).  GR kinetic matrix
   UNTOUCHED => c_T = 1 automatically, no repair.
2. K = q(T) FROM THE EOM.  The cuscuton field equation is mu^2 K = V'(T), i.e. K = V'(T)/mu^2
   = q(T).  The CMC relation is the cuscuton's OWN equation of motion -- not an inserted
   Lam_C(K-q) multiplier.  This is the structural payoff.
3. a0 FROM EXPANSION.  FLRW T=t: K=3H => q=3H => a0 = 3cH/Z => a0(z) = a0,0 H(z)/H0.
   D_i q = 0 on a homogeneous-T slice => D_i a0 = 0 locally: the a0(r) source is gone.
4. MOND FROM THE ACTION.  F'(X) = -1/(1+sqrt X) => mu = 1 + F' = x/(1+x); Newtonian (x>>1,
   mu->1) and deep-MOND (x<<1, mu->x => g=sqrt(a0 g_N), v^4 = GM a0) both follow.  On FLRW
   a_mu=0, F(0)=0: MOND adds no dark energy.

## NOT PROVEN / NOT FIXED (honest)
- 2+0 DOF for the COUPLED GR+cuscuton+MOND(a_mu) system.  The bare cuscuton is established
  non-dynamical, but the MOND a_mu-coupling deforms the constraint; the Dirac count of the
  coupled system is the remaining structural gate.
- a0 NORMALISATION: Z ~ 21 fitted, not derived.  Only the SCALING a0 ~ H(z) is predicted.
- CASSINI: mu = x/(1+x) gives the constant sunward a0 excess and the ~10.7 sigma quadrupole
  (Route-1).  A phenomenological failure of the Simple interpolation, unchanged by the
  cosmological completion.  This is the empirical wall, separate from the DOF question.

## The falsifiable prediction that survives everything
a0(z) = a0,0 H(z)/H0.  During matter domination a0 rises as H; this is directly testable
against the a0(z) front and is DIFFERENT from a0^2 ~ rho_DE.

## REFINEMENT (Carl): protect the T-equation from MOND contamination
CORRECTION: "K=q(T) is the cuscuton EOM" holds for the BARE cuscuton only.  With a0(T) inside
F, T enters S_MOND twice -- via u_mu(T) (geometric) AND explicitly via a0(T) -- so
dS_MOND/dT gets a (da0/dT) E_a0 piece and K=q(T) is NOT automatically preserved once MOND is
coupled.

REPAIR: route a0 through an AUXILIARY q, not T.  Frozen refined action:
  S = (c^3/16piG) INT sqrt(-g) R
    + INT sqrt(-g) [ mu^2 sqrt(-grad T.grad T) - V(T) ]        (cuscuton, non-dynamical)
    + S_MOND[g, u, q, chi]   with  a0(q) = c q/Z               (a0 via q, NOT T)
    + INT sqrt(-g) Lambda ( q - V'(T)/mu^2 )                   (ties q to T algebraically)
    + S_m.
Now da0/dT = 0: the explicit channel is ELIMINATED.  Residual T-equation:
  (cuscuton) + [dS_MOND/dT via u] - Lambda V''(T)/mu^2 = 0,   Lambda = -dS_MOND/dq.
Two residual channels: (1) the geometric foliation coupling via u_mu(T) [present in ANY
preferred-foliation MOND]; (2) the multiplier back-reaction -Lambda V''/mu^2.  DESIGN HANDLE:
if the MOND auxiliary sector makes dS_MOND/dq = 0 on shell (a0-EOM stationary), then Lambda=0
and channel (2) dies, leaving only the geometric (1).  Whether that holds is part of gate 1.

## The three open gates (unchanged, #1 decisive)
1. coupled (T, q, MOND) constraint matrix -> exactly 2 tensor + 0 scalar?  [THE structural gate]
2. relativistic metric equations -> lensing / PPN limit?
3. V(T) chosen so a0(z) = a0,0 H(z)/H0 holds globally without pathology?
Plus the unchanged empirical wall: Cassini ~10.7 sigma (Simple mu), a0 normalisation Z~21 fitted.
This is the version to run the full Dirac calculation on.
