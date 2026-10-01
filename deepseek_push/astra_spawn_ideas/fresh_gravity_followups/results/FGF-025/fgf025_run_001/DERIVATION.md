# FGF-025: exact energy squares for a strictly increasing scale profile

2026-09-30. Conditional proof-only result, requiring independent review.
The identity route was proposed by /root; see ORIGIN.md. This worker derived
its signs, boundary requirements, coercivity and static elimination afresh.
No literature mechanism or historical novelty is asserted.

## 1. Precisely stated domain and inherited equations

Use the FGF-023 hydrostatic diagnostic Q/R slab on [0,d], d finite and positive,
with smooth regular background B>0,rho>0,g>0, a=a_ref exp chi, and
C=4piG>0, J>0, cs²>0, positive kinetic coefficients tau=K/c² and
sigma=J/v_chi². Use its cosh U=S0[cosh(2chi)-1]/4, S0>0.
For each law keep b=F^(-1), A=b_g>0, q=gA-B>0,
T=-W_chi, m=U''-T_chi=U''-2T+gq, M=m-q²/A.

  Q: F(B;a)=sqrt(B²+aB),
  RAR (label R): F(B;a)=B/[1-exp(-sqrt(B/a))].

Do not confuse the R law label with the coefficient R(x)=rho q/A used below.
The static equations, with no density subtraction or volume force canceler,
are B'=C rho, cs²rho'=-rho g, g=F(B;a), and J chi''=U'-T.
They imply A g'=C rho+q chi'. Total mass is fixed by impermeable walls.
Background endpoint fields and wall tractions are induced from an actual
regular solution, not empirically calibrated or arbitrarily preassigned.

New sign-domain hypothesis: w=chi' is strictly positive on the CLOSED interval.
Continuity then gives min w>0. No step divides by w at a zero; interior zeros,
endpoint zeros, negative w and sign-changing w are excluded, not diagnosed.
Regularity also bounds w,w',1/w,A,1/A and positive rho on this compact domain.
Perturbations xi,psi,eta belong to H1_0[0,d]. No zero-flux condition is added.
The background is held fixed while perturbations are evolved.

The FGF-023 IVP B_i,rho_i,w_i>0 and chi_i=0 provides actual nonempty examples
of this sign domain on sufficiently short intervals. The present theorem
applies at ANY finite length on which a solution remains regular with w>0.
It does not prove that a selected IVP can be extended to arbitrary lengths.
No continuation has been computed here; no interval beyond the older
sufficient condition is claimed to have been numerically exhibited.

## 2. Independent background differentiation and pointwise identity

Differentiate the scale equilibrium without freezing its coefficients:

  J w''=U'' w-[T_g g'+T_chi w]
        =m w-q(C rho+q w)/A=M w-C R,
  R=rho q/A>0.                                             (1)

There is no q' term in the total derivative of T(g,chi): T_g=q multiplies
g', while T_chi multiplies w. Adding a q' term would differentiate an already
differentiated perturbation expression instead of the background equation.

Set z=eta/w. Direct product-rule expansion gives

  J w² z'²+partial_x[J(w'/w)eta²]
      =J eta'²+J(w''/w)eta².

Inserting (1) and expanding the second square proves the exact identity

  J eta'²+M eta²+C R(w xi²+2xi eta)
   =J w²[(eta/w)']²+(C R/w)(eta+w xi)²
        +partial_x[J(w'/w)eta²].                         (2)

This is an algebraic identity on the background, not a sampled spectrum.
It retains every derivative of the nonuniform scale through w and (1).

## 3. Complete energy and endpoints

The inherited FGF-023 potential factorization was

  2V=integral {cs²rho xi'²
       +(A/C)[psi'+(C rho xi-q eta)/A]²
       +(J eta'²+M eta²)/C+R(w xi²+2xi eta)} dx
       +[cs²rho'xi²-2rho xi psi]_0^d.

Substitution of (2) yields

  2V=integral {cs²rho xi'²
       +(A/C)[psi'+(C rho xi-q eta)/A]²
       +(J/C)w²[(eta/w)']²
       +(R/w)(eta+w xi)²} dx
       +[cs²rho'xi²-2rho xi psi+(J/C)(w'/w)eta²]_0^d.     (3)

All endpoint terms vanish under xi=psi=eta=0, since w stays bounded away
from zero at the endpoints. Each integral term is nonnegative. If V=0,
xi'=0 and xi=0 at the walls give xi=0. The third term gives eta/w constant;
its Dirichlet endpoints give eta=0. Finally the second term gives psi'=0,
so psi=0. Thus V>0 for every nonzero admissible triple. The R/w term is
strictly nonnegative as well; no sign of M alone is needed.

Coercivity is also available, not merely a pointwise absence of zero modes.
The first term controls xi in H1_0. The third controls z=eta/w in H1_0 by
Poincare; bounded positive w and bounded w' then control eta in H1_0. The
second controls psi', using the already controlled xi and eta and bounded
A,1/A,rho,q. Dirichlet Poincare controls psi itself. The positive kinetic
form integral[rho xi_t²+(tau psi_t²+sigma eta_t²)/C]dx therefore defines a
positive self-adjoint longitudinal eigenproblem on this finite wall domain.
No unstable longitudinal eigenmode occurs within these hypotheses. The coercivity constant depends on the particular interval and background; no positive lower bound uniform in d or as min w approaches zero is asserted.

The conserved quadratic energy flux remains the complete FGF-023 expression,
with r=delta rho=-(rho xi)':

 d(K2+V)/dt=[(A psi'-q eta)psi_t/C+J eta' eta_t/C
                    -rho xi_t(cs²r/rho+psi)]_0^d=0.       (4)

The factorization does not remove kinetic degrees of freedom or introduce
new boundary conditions. It proves linear fixed-wall stability only.

## 4. Exact static elimination and its positivity gate

Write h=C rho xi-q eta and Z=integral_0^d 1/A dx>0. Minimizing the second
square in (3) over Dirichlet psi gives A psi'+h=k with
k=(integral h/A)/Z. Its exact residual is

  [integral h/A dx]²/(C Z),                            (5)

not zero in general. The minimizing psi is the integral of (k-h)/A from
0 to x; the choice of k enforces both endpoints. Thus the exact psi-reduced
form is the other three positive squares in (3), plus (5). It is positive
without a spectrum search for every nonzero (xi,eta) in this sign domain.

For completeness, further eta elimination can now be justified rather than
assumed. Let l=q/A, b=C rho/A, F_xi=integral b xi dx, and define the complete
Dirichlet operator, including its nonlocal term,

  L_eta=-J partial_x²+M+(l tensor l)/Z,
  [(l tensor l)eta](x)=l(x) integral l(s)eta(s)ds.

At xi=0, (2) with zero endpoints implies

  <eta,L_eta eta>=integral[J w²((eta/w)')²+(C R/w)eta²]dx
                            +(integral l eta)²/Z>0

for nonzero eta. The preceding coercivity argument proves a well-defined
positive inverse in the Dirichlet variational sense. This conclusion uses
w>0 and the exact background equation; U''>0 or the homogeneous Schur
identity alone would not justify it.

With s_xi=C R xi-l F_xi/Z, the eta-dependent part is
<eta,L_eta eta>/C+2<s_xi,eta>/C. Its minimizer is
eta_*=-L_eta^(-1)s_xi and the fully reduced form is

  2V_min=integral[cs²rho xi'²+R w xi²]dx+F_xi²/(C Z)
                  -<s_xi,L_eta^(-1)s_xi>/C.             (6)

Despite its subtraction, (6) is positive for nonzero Dirichlet xi, since
the exact attained minimum equals the already positive squares and retains
at least integral cs²rho xi'². This is static energy minimization only;
tau,sigma>0 do not permit instantaneous dynamic elimination.

## 5. Exact controls and excluded extrapolations

1. Product-rule check: the mixed derivatives -2J(w'/w)eta eta' from the
   first square cancel +2J(w'/w)eta eta' in the total derivative exactly.
   The remaining eta² coefficient is Jw''/w+CR/w=M.
2. Background-sign mutant: changing (1) to Jw''=Mw+CR leaves an erroneous
   extra 2CR eta²/w on the right of (2). It fails for any nonzero eta and
   R>0. This checks the attractive source sign independently of eigenvalues.
3. Coupling mutant: omitting 2R xi eta from the inherited energy disagrees
   with (3) by exactly 2 integral R xi eta. On an actual w>0 slab choose
   xi=sin(pi x/d), eta=w xi (both Dirichlet); that integral is strictly
   positive. The omission cannot be hidden in endpoints.
4. Boundary mutant: as a purely algebraic fixture, take J=C=R=1,
   w=e^x, M=1+e^-x, xi=0, eta=w on [0,d]. It satisfies (1) but NOT the
   fixed eta boundary condition. Equation (2)'s derivative integrates to
   e^(2d)-1, which is nonzero. Dropping that endpoint term gives a false
   identity. This fixture is not asserted to be a full hydrostatic solution.
5. Dirichlet compatibility: (5) survives whenever integral h/A is nonzero.
   Setting psi'=-h/A would then violate its endpoint values. Its inclusion
   in L_eta and s_xi checks the nonlocal coefficient and signs in (6).
6. Frozen sector: eta=0 alone leaves R w xi² in (3), matching FGF-023.
   Constant chi would mean w=0, outside this transformed identity; recovering
   the separately fixed-scale FGF-015 model requires its original formula.
   The actual constant-chi positive-density SD1 obstruction still applies.

All controls above are exact algebraic statements, not executed numerical
experiments. No numerical tolerance, seed, runtime or computation manifest
is claimed. Negative/zero w defeats this positive-square argument; it does
NOT on its own prove an unstable mode. Singular division is not evidence.

## 6. What this closes, and what remains open

The old alpha,beta,R sufficient shortness bound is unnecessary on every
regular closed interval satisfying chi'>0. Equations (3)-(6) prove actual
all-mode linear longitudinal positivity in that conditional sign domain,
not merely positivity of a finite discretization. The sufficient-bound versus
true-sign question is thereby closed for this domain irrespective of whether
the older margin can be numerically certified.

No computed continuation or explicit example with a FAILED older margin has
been produced. Thus no strict enlargement of the realized IVP length range
is claimed. Physical systems, zero/sign-changing slopes, endpoints with w=0,
free boundaries, transverse/3D modes, nonlinear stability, arbitrary global
boundary existence and observed endpoint calibration remain unresolved.

The reference acceleration may separately be a0=9.3619e-11 or
1.1279e-10 m/s², with a_ref=kappa c sqrt(G rho_Lambda,ref). Each constant-
vacuum reference family is distinct from a frozen comparison
 a_ref=a0 sqrt[.315(1+z)^3+.685]. The theorem is dimensional and holds for
either reference; no time-dependent H(z) evolution is inferred. Actual
 a(x)=a_ref exp chi(x) varies, so it still violates literal pointwise
constant-vacuum identification of actual a. This stability result does not
repair that physical incompatibility.

Source flux is B'=C rho with g=F(B;a) in the selected Q or R law. No Newtonian
missing-mass substitution is made. No M local action is registered here,
so no M stability statement is supplied. No operative filtered-MONO, metric,
photon, cosmological, observational-likelihood or theory-closure result follows.
The next discriminating boundary is chi'=0 or a sign change on an actual
continued equilibrium, where a nonsingular formulation is required.

A further scope control from the parent: chi=w=0 at an interior initial point gives w_prime=-T/J<0. Local two-sided existence preserves B,rho>0, and the older FGF-023 Poincare theorem ensures stability on a sufficiently short induced symmetric patch. Thus a turning point itself does not imply instability. The next task must study the same full continued domain, not replace it by a newly shortened stable neighborhood.
