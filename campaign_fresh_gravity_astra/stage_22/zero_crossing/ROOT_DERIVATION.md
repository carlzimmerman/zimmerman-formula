# Local coupled Q crossing: existence and the regularity boundary

Exact diagnostic claim, 2026-09-30 16:31 UTC pass. Uses FGF035 and the pinned
FGF023 action; no new worker/auditor proof or formula preview read before this
file was fixed. No numerical experiment or external literature input.

## Definitions and signed extension

C=4piG>0, J,cs²,S0>0; a=a_ref exp(chi), a_ref>0 fixed in time;
U=S0(cosh(2chi)-1)/4. Set r=|g| (not density), b(r,a)=(sqrt(a²+4r²)-a)/2,
W(r,a)=integral_0^r b(v,a)dv, T=rb-2W=-W_chi. The spatial potential g=phi_x
is signed; its conjugate source flux is B=sgn(g)b(|g|,a). This sign extension
comes from the even energy W(|g|,a), not a new radial law. Thus

g=sgn(B)sqrt(B²+a|B|),  B_x=C rho,
rho_x=-rho g/cs²,  chi_x=w,  J w_x=U'(chi)-T(|g|,a),  phi_x=g.       (1)

These are the static Euler equations of the inherited field/fluid action.
There is no uniform-density subtraction or added central sheet. At x=0 take
B=0, rho=rho_*>0, chi=chi_*, w=w_*, phi=phi_* finite.

## Existence without differentiating a square root in spatial position

Let u=B be the independent coordinate. The proposed system is exactly

x_u=1/(C rho), rho_u=-g(u,chi)/(C cs²), chi_u=w/(C rho),
w_u=[U'(chi)-T(|g(u,chi)|,a)]/(JC rho), phi_u=g(u,chi)/(C rho).        (2)

On a compact state box with rho bounded positively away from zero and finite
chi,w, the right hand side is continuous in u including u=0 and locally
Lipschitz in the state, uniformly for small u. To see the nontrivial part,
let v=|u|. Then |g|=sqrt(v²+av) and

partial_chi |g|=av/[2sqrt(v²+av)]=O(sqrt(v)),

extended as zero at v=0. T(g,a) is smooth in a for g>0 and its composition
with sqrt(v²+av) is O(v^(3/2)), with chi derivative O(v^(3/2)) on this box.
This also follows directly from W=a² w(g/a), w(x)=x³/3+O(x⁵), since the
composed expression and its chi derivatives have uniform small-v expansions.
All other state derivatives in (2) are bounded on the box. The derivative
with respect to u need not be bounded; it is not used for the Lipschitz claim.

The integral map Y(u)=Y(0)+integral_0^u RHS(t,Y(t))dt maps a sufficiently
short two-sided closed interval and state ball into itself, and contracts in
the uniform norm when its length times this state Lipschitz bound is <1.
Successive iterates therefore converge to a unique C1 solution in u, on both
sides. This is an explicit local existence argument, not an invocation of
smooth spatial ODE coefficients. Since x_u>0, it has a C1 monotone inverse
u=B(x), with B_x=C rho. Substituting gives (1) on a two-sided spatial patch.
Uniqueness holds among nearby solutions of these equations with continuous
positive density and the prescribed center data; it is not a uniqueness
statement for arbitrary rough distributional objects or unrelated wall data.

## Local regularity and no delta source

Write a_*=a_ref exp(chi_*), k=sqrt(a_* C rho_*). Continuity first gives
B=C rho_* x+o(x), a=a_*+O(x), hence g=sgn(x)k sqrt(|x|)(1+o(1)).
Integrating gives the exact hydrostatic relation and leading terms

phi-phi_*=(2k/3)|x|^(3/2)+o(|x|^(3/2)),
rho=rho_* exp[-(phi-phi_*)/cs²]
    =rho_*[1-(2k/(3cs²))|x|^(3/2)+o(|x|^(3/2))].                    (3)

The equations then improve B=C rho_* x+O(|x|^(5/2)), while a=a_*+O(x).
Consequently g=sgn(x)k sqrt(|x|)[1+O(|x|)]. Away from zero, differentiating
the exact signed expression, on BOTH sides, gives

g_x=[(2|B|+a)C rho+B a_x]/(2|g|)
   =k/(2sqrt(|x|))+O(sqrt(|x|)).                                  (4)

This formula, not differentiation of an unqualified little-o remainder,
establishes the nonintegrable square of g_x. The spatial g is C^(0,1/2),
locally absolutely continuous, with g_x in Lp for 1<=p<2, but not in L2
on any neighborhood of the crossing. Thus phi is C^(1,1/2) and W^(2,p)
for p<2 but not H2. Density is C^(1,1/2); its second derivative has the
same nonzero inverse-square-root singularity through rho_x=-rho g/cs²,
so rho is also W^(2,p), p<2, and not H2 locally. These are local statements.

The source T(|g|,a)=|g|³/(3a)+O(|g|⁵/a³)=O(|x|^(3/2)). Its first spatial
derivative is continuous and O(sqrt(|x|)) near zero; use T_r=r b_r-b=O(r²)
and (4), with bounded chi_x. Thus T is C^(1,1/2), and chi_xx=(U'-T)/J
bootstraps chi to C^(3,1/2) locally. No C4 claim is made. In particular
chi_xx(0)=U'(chi_*)/J; the scale source vanishes at the crossing.

B is continuously differentiable with B_x=C rho and has no jump. Therefore
its distributional derivative contains no delta sheet. phi, chi, their fluxes
and the hydrostatic pressure obey the weak equations by integration by parts,
with the usual induced endpoint data. W=O(|x|^(3/2)); J chi_x²/2,U and the
fluid energy/coupling are bounded on this short patch with positive rho.
The static local total energy is finite. A non-square-integrable phi_xx is
not itself infinite energy, since the action contains W(phi_x), not phi_xx².

## Full Hessian and the norm which fails

For general perturbations (xi,psi,eta), set d=delta rho=-(rho xi)_x. On a
finite patch with zero endpoint perturbations, fixed mass gives integral d=0.
The continuous full quadratic form inherited from the action is

Q0=integral {cs² d²/rho+2d psi
 +[A psi_x²-2q_s eta psi_x+J eta_x²+(U''-S)eta²]/C}dx,               (5)

A=b_r(|g|,a), q_s=sgn(g)(|g|A-b), S=T_chi at fixed |g|=2T-|g|q,
q=|g|A-b>=0. The signed cross term is essential. The even gradient energy is
C2 at g=0, with all its gradient/chi second derivatives continuous there;
A=q_s=S=0 at that point. Coefficients in (5) are bounded on the patch, so it
extends continuously to H1_0 triples. For smooth directions, differentiating
the energy twice gives (5); hydrostatic balance makes higher density variations
multiply a constant chemical potential, removed by fixed mass. No smooth H2
background theorem or division by A at zero is used for this statement.

For Q, in terms of signed B,

A=2sqrt(B²+a|B|)/(a+2|B|), q_s=aB/(a+2|B|).

Thus A~(2k/a_*)sqrt(|x|), q_s=O(x). Choose nonzero smooth compactly supported
f in (-1,1), psi_delta(x)=sqrt(delta) f(x/delta), and xi=eta=0, with delta
small enough that support lies inside the patch. Then

||psi_delta'||²=||f'||², ||psi_delta||²=delta²||f||²,
Q0[0,psi_delta,0]<=C^-1 sup_(|x|<=delta)A * ||f'||²=O(sqrt(delta)).

The same conclusion holds with any fixed positive dimensional reference
weights defining the product H1 norm. Hence no c0>0 can give Q0>=c0||.||_H1²
on all these perturbations. Every nonzero one of these test energies is still
positive. This proves loss of standard-H1 coercivity only; it neither finds a
negative direction nor disproves a positive bound in a weighted energy norm
or an L2 kinetic spectral gap. A local positive kinetic term is not a ghost.
It does not prove nonlinear stability or ill-posedness of the evolving system.

## Scope and remaining implication

The construction is a local induced-wall/mass family, not a prescribed endpoint
BVP or FGF034's fixed-mass/fixed-wall C1 H2 branch. The zero crossing is unique
locally since B_x>0; total flux difference is C times the patch mass, retaining
MOND source accounting. No spherical mass estimate or observation is computed.
Both a_ref=9.3619e-11 and1.1279e-10 m/s² are admitted separately; k and the
energy restore their physical factors. Constant-vacuum reference and frozen
a0 E(z), E²=.315(1+z)^3+.685, remain different hypotheses. Evolving H is not
stationary and requires the prior explicit work balance. Actual local a varies
with chi, an extra diagnostic premise not a derived pointwise vacuum identity.
Q only here; no RAR/M/filtered-MONO transfer, physical V, metric/photon action,
gravitational degree count, historical novelty or theory closure.

A distinct next question is whether a natural weighted form domain, rather
than standard H1 coercivity, supplies a positive closed coupled energy and
linear operator on sufficiently short zero-crossing slabs. Here 1/A is locally
integrable, so weighted trace and Poincare estimates may be available. No such
positivity, domain completion, transmission or spectral theorem is proved here.
