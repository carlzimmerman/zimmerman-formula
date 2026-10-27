# FGF047 independent compatibility and energy derivation

Author: /root/fgf047_compatibility. Narrow proof-audit route, derived before
exposure to the FGF047 author proof or any new reviewer proof. Source bytes
are recorded in input_sha256.json. No outside theorem or computation is used.

## Claim card and domain

For C=4pi G>0, tau,sigma,J,cs,S0>0 and a fixed positive a_ref, consider
classical one-dimensional fields in an open spacetime patch with n>0,
g>0 and finite chi. Write a=a_ref exp chi, D=sqrt(a^2+4g^2),
B=(D-a)/2, W=integral_0^g B(s,a) ds, T=-W_chi and
U=S0(cosh(2chi)-1)/4. All field coefficients use these fixed action
normalizations. In particular B_g=2g/D>0 and
B_chi=(a^2/D-a)/2=-aB/D. Define c=sqrt(B_g/tau)>0 and d=sqrt(J/sigma)>0.
The conclusion below is an exact characteristic-coordinate equivalence on
compatible data, with a full energy law. It is CONDITIONAL on an appropriately
regular solution of the displayed first-order system. Construction of that
solution, estimates, uniqueness, lifespan, extension independence and limit
regularity are outside this narrow audit.

Minimum useful regularity: reconstructed first-order variables C1, with
phi_t=p, chi_t=q and gradient equalities proved below, giving the second
field derivatives occurring in the original equations. C1,1 is sufficient.
No gradient constraint is assumed merely because a variable is named g or k.

## 1. Baseline first-order lift

Put r=log(n/nref), p=phi_t and q=chi_t, provisionally regarding g,k as
independent unknowns. One consistent off-constraint first-order extension is

r_t+v r_x+v_x=0,
v_t+v v_x+cs^2 r_x=-g,
p_t-c^2 g_x=f,             f=(B_chi k-C n)/tau,
g_t-p_x=0,
q_t-d^2 k_x=h,             h=(T-U')/sigma,
k_t-q_x=0,
phi_t=p,                  chi_t=q.

The defects xi=g-phi_x and eta=k-chi_x obey xi_t=eta_t=0.
Thus compatible initial data make this extension exactly the requested
second-order PDE. Off-constraint it has p_t-(B(g,chi))_x/tau+Cn/tau
=B_chi eta/tau, and the Euler force is -g instead of -phi_x. These are
explicit extension choices, not identities for arbitrary original fields.

## 2. Diagonal characteristic variables and all chain-rule terms

Fix an arbitrary positive g_star within the coordinate patch and set

H(g,chi)=integral_{g_star}^g c(s,chi) ds,   H_g=c>0,
L=H_chi.

This has a local smooth inverse g=G(H,chi) since H_g>0.
Its chi dependence is real: c_chi=-c a^2/[2(a^2+4g^2)], so L cannot
be discarded on an open g interval. Choosing H(g_star,chi)=0 merely makes
L vanish at that one g value.

Let R_plus=p+H, R_minus=p-H; S_plus=q+d k, S_minus=q-d k;
and Z_plus=v+cs r, Z_minus=v-cs r. Their speeds, with the indicated
labels, are respectively -c,+c,-d,+d,v+cs,v-cs.
For the baseline lift, EXACT transformation before imposing constraints gives

(R_plus)_t-c(R_plus)_x = f+L(q-c chi_x),
(R_minus)_t+c(R_minus)_x = f-L(q+c chi_x),
(S_plus)_t-d(S_plus)_x = h,
(S_minus)_t+d(S_minus)_x = h,
(Z_plus)_t+(v+cs)(Z_plus)_x = -g,
(Z_minus)_t+(v-cs)(Z_minus)_x = -g.

Both q terms and both chi_x terms are required. A fully diagonal system
with sources depending only on the unknown state may replace chi_x by k
in these two R sources, retaining phi_t=p and chi_t=q. This gives

(R_plus)_t-c(R_plus)_x = f+L(q-c k),
(R_minus)_t+c(R_minus)_x = f-L(q+c k).                 (D)

This replacement changes the off-constraint extension. Adding/subtracting
(D), while using H_t=c g_t+L q and H_x=c g_x+L chi_x, gives exactly

p_t=c^2 g_x+f+c L(chi_x-k),
g_t=p_x,
q_t=d^2 k_x+h,
k_t=q_x.                                            (O)

In particular the p equation's extra c L(chi_x-k) term MUST be displayed
when reconstructing off-constraint equations from (D). The diagonal
extension still obeys xi_t=eta_t=0 and is therefore equivalent to the
original equations for compatible initial data. The fact that its
p equation differs off-constraint from the baseline lift is harmless once
this is proved; claiming exact equivalence off-constraint is false.

Alternatively a genuinely exact diagonal-plus-derivative-coupling transform
can retain chi_x in the R equations, giving the baseline lift itself.
One must identify which extension is used in an iteration argument.

The coordinate inverse is
v=(Z_plus+Z_minus)/2, r=(Z_plus-Z_minus)/(2cs),
p=(R_plus+R_minus)/2, H=(R_plus-R_minus)/2,
q=(S_plus+S_minus)/2, k=(S_plus-S_minus)/(2d).
Keeping chi and phi as zero-speed variables yields a local invertible map.
Coincident numerical speeds across separate blocks cause no loss of this
basis. No globally constant diagonalization is asserted.

Negative control: if both induced L terms are deleted and one uses
(R_plus)_t-c(R_plus)_x=f=(R_minus)_t+c(R_minus)_x,
reconstruction instead gives g_t=p_x-L q/c. Then xi_t=-L q/c, so
compatible initial data need not remain compatible once q evolves. This
is an exact symbolic failure, not a numerical counterexample to existence.

## 3. Dynamic MOND source and constraint feedback

For (D), multiply the reconstructed p equation by tau and compare with
B_x=B_g g_x+B_chi chi_x:

B_x=Cn+tau p_t-(B_chi-tau c L)eta.                    (Moff)

On eta=0 and xi=0, p=phi_t, g=phi_x and hence

B_x=Cn+tau phi_tt,
B(t,x2)-B(t,x1)=C integral_{x1}^{x2}n dx
                         +tau integral_{x1}^{x2}phi_tt dx.

Static source inversion is invalid unless the time acceleration term is
actually zero. The eta term in (Moff) is another explicit way to detect
an incorrect off-constraint reconstruction of the diagonal system.

## 4. Full energy, flux and off-constraint residual

Let e(n)=cs^2 n[log(n/nref)-1], P=cs^2 n and
E_m=n v^2/2+e(n). Define

E=E_m+n phi+[tau p^2/2+W(g,chi)+sigma q^2/2+J k^2/2+U]/C,
S=(E_m+P+n phi)v-[p B+J q k]/C.

Using continuity and Euler with force -g gives

(E_m+n phi)_t+[(E_m+P+n phi)v]_x
       =n p+n v(phi_x-g).

For the scalar Q field in (O), W_t=B p_x-T q, so

[tau p^2/2+W]_t-(p B)_x
       =-Cn p-T q+p(B_chi-tau c L)eta.

For the scale field,

[sigma q^2/2+J k^2/2+U]_t-(J q k)_x=T q.

Thus the precise off-constraint identity for the chosen diagonal system is

E_t+S_x=-n v xi+[p(B_chi-tau c L)/C]eta.              (Eoff)

For compatible data, all defects vanish and E_t+S_x=0. The matter-potential
work n p cancels the scalar field work -n p, and the internal scale
exchange -T q cancels +T q. Both field fluxes have NEGATIVE signs in S.
Neither dropping n phi nor omitting one field flux gives the stated law.
For an interval, d/dt integral E=-S(right)+S(left). A restricted local patch
usually has boundary flux; no closed global energy follows from the local
identity. Energy need not be positive because of gravitational interaction.

The baseline extension in section 1 instead has Eoff residual
-nv xi+p B_chi eta/C. This distinction vanishes on compatible states but
must not be mixed when checking off-constraint algebra.

## 5. Zero-velocity hydrostatic control

Let smooth rho>0, phi0,chi0 solve the inherited exact hydrostatic equations
cs^2(log rho)_x=-g0, B(g0,chi0)_x=C rho,
J(chi0)_xx+T(g0,chi0)-U'(chi0)=0, g0=(phi0)_x>0.
Take n=rho, v=p=q=0, g=g0, k=(chi0)_x and stationary phi0,chi0.
All original equations then hold, xi=eta=0, E is stationary and S=0.
This checks a genuine responsive scale equilibrium; k need not vanish.
In characteristic coordinates, R_plus=H, R_minus=-H, so their left sides
are -c H_x, matching f-cLk because hydrostatics gives f=-c^2 g_x.
S_plus=d k and S_minus=-d k have left sides -d^2 k_x=h;
Z_plus=cs r and Z_minus=-cs r have left sides cs^2 r_x=-g.
Thus even a stationary control checks the induced spatial L terms.
For the requested nonzero FGF046 velocity, this control is a separate datum;
it does not assert stationary behavior of that perturbed evolution.

## Dependency graph, obligations and limits

Pinned action and task -> B,W,T coefficient identities -> invertible local
coordinate map -> exact chain rule and off-constraint system -> homogeneous
gradient-defect propagation -> original dynamic source and energy identity.
All leaves used here are direct algebra or pinned definitions; no external
PDE theorem is invoked. Positivity/invertibility, induced terms, defect
propagation, source, both fluxes and hydrostatic control: passed by the
calculations above. Local existence/iteration, actual lifespan, regularity
preservation, physical patch and exterior independence: not addressed.

Strongest safe statement: every sufficiently regular solution of (D), the
scale/fluid characteristic equations, phi_t=p and chi_t=q, starting from
compatible positive data and staying within the regular coefficient patch,
reconstructs a solution of the inherited PDE and obeys its local energy law.
No converse to the existence premise is supplied. No claim is made about
crossing g=0, walls, global evolution, finite-time breakdown, physical pointwise
vacuum closure, two gravitational degrees of freedom, metrics/photons, M,
filtered MONO, cluster calibration, evolving H, cosmology, or novelty.
Either fixed reference value 9.3619e-11 or 1.1279e-10 is allowed separately;
frozen H comparisons remain separate from a driven reference, whose energy
would carry the protocol work established by pinned FGF032.
