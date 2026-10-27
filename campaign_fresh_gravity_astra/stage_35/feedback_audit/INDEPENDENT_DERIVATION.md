# FGF048 independently frozen narrow density/feedback derivation

Role: /root/fgf048_feedback. Scope: conditional a priori estimates for actual
solutions on the stipulated compression interval; NOT a construction or a
uniform existence theorem. Primary verdict before author exposure:
**conditional on a named input** (the uniform scaled fluid derivative bounds
and actual classical existence stipulated below). No new stage35 author,
coordinator, or other reviewer proof or preview has been read.

The task hash is 028ae73e50048d0412fde4d5ddd88e1b94e8bd127d75b80fc952382fdeb4b377.
All eight task ancestry hashes matched their stated values. The old FGF047
derivation was read immediately before its hash check; this chronology is
disclosed rather than represented as checking before reading. Other scientific
content read was the task, common framework/result contract and old FGF047
reconciliation. Listing filenames did not expose new proof contents.

## 1. Claim card and precise premises

Keep every original equation, coefficient, profile and hydrostatic background
from the pinned FGF047 derivation. In particular c=cs>0, tau,sigma,J,C>0 are
fixed; g=phi_x>0, a=a_ref exp(chi), B=(sqrt(a^2+4g^2)-a)/2,
T=-W_chi, W_g=B. Put d=sqrt(J/sigma), b=sqrt(B_g/tau).
The original f=(1-y^2)^2 on |y|<1 and zero elsewhere stays C1,1.

Use fixed positive physical units once and express the following estimates in
those units. This makes norms of different field coordinates comparable and
allows bounds ell<=1, V>=1, t<=1 without changing physical coefficients. The
restored N powers below are invariant under that fixed unit choice.

Let ell=L N^-3, V=v0 N, epsilon=c/V, s=Vt/ell, y=(x-x*)/ell,
u=v/V and q=log(n/nref). For N>=N0 fixed once, suppose an actual solution in
the FGF047 C1 class with spatially Lipschitz first derivatives exists on a
backward-contained physical cone for 0<=s<=kappa. Assume on that cone

  P_+=u_y+epsilon q_y, P_-=u_y-epsilon q_y,
  max(|P_+|,|P_-|)<=M, max(Lip_y P_+,Lip_y P_-)<=H,       (1)

where M,H,kappa>0 are independent of N. Its fluid characteristic curves and
the field characteristic curves used below must stay in the controlled cone.
Initial background derivatives through third order are bounded on a fixed
larger physical patch, n0=rho is bounded above and below positively there,
g0 has a fixed positive margin, and chi0 is bounded. The solution starts with
p=phi_t=w=chi_t=0, g=g0, k=chi_x=chi0_x and chi=chi0.

The conclusions below can bootstrap field state/first-derivative bounds on
every such interval of existence. They do not supply (1), existence to its
endpoint, or a continuation theorem. No small energy implication is used.

## 2. Uniform density and its derivatives

Continuity in scaled coordinates is q_s+u q_y=-u_y. Along a fluid trajectory
Y(s), |u_y|<=M by (1), so exactly

  n(s,Y(s))=rho(x*+ell Y(0)) exp(-integral_0^s u_y dz).

Writing rho_- and rho_+ for the fixed patch extrema gives

  rho_- exp(-M kappa)<=n<=rho_+ exp(M kappa).              (2)

This is independent of N. It does not use a rectangle in v+cq,v-cq.
Pressure is still present in the velocity equation
u_s+u u_y+epsilon^2 q_y=-ell g/V^2.

Let Q1 be the physical initial bound ||q0_x||. Differentiating continuity
almost everywhere and integrating its linear characteristic equation gives

  ||q_y(s)|| <= exp(Ms)(ell Q1+s H) <= Q_*.               (3)

Indeed D_u q_y=-u_y q_y-u_yy, and |u_yy|<=H almost everywhere.
The C1,1 class permits this weak differentiation; characteristic integration
gives the estimate for the continuous q_y. It does not assert u_yy exists at
the polynomial joins. Thus |n_x|<=n_+ Q_*/ell.

The safe second-derivative estimate explicitly retains the inverse:

  Lip_y q_y<=H/epsilon,
  Lip_y n_y<=n_+(H/epsilon+Q_*^2).                        (4)

After increasing N0 so epsilon<=1, (4) is O(epsilon^-1), not O(1).
Consequently ||n_x||<=K/ell and Lip_x n_x<=K/(epsilon ell^2).
All K here and below are N independent but depend on M,H,kappa, the fixed
units, physical coefficients and background bounds. Replacing (4) by a
uniform bound would require a new argument. The pressureless limiting flow
has derivative discontinuities associated with f'' at the joins, so that
replacement is especially unsafe.

## 3. Actual moving field estimate, including chi dependence

Use h_g=b, h(g,chi)=integral_{g_*}^g b(z,chi) dz and field coordinates

  z=(p+h,p-h,w+d k,w-d k,chi).

Their equations are diagonal with speeds (-b,b,-d,d,0) and right sides

  B_chi k/tau-Cn/tau+h_chi(w-bk),
  B_chi k/tau-Cn/tau-h_chi(w+bk),
  D,D,w,   D=(T-U')/sigma.                                (5)

Both h_chi terms, scale response and the dynamic source are retained.
The stationary background z0(x),n0(x) solves these equations exactly.
On a fixed compact field chart separated from g=0, let delta=z-z0 and
eta=n-n0. Subtraction gives

  delta_t+Lambda(z)delta_x=G(delta,eta,x),                 (6)

where G=F(z,n)-F(z0,n0)-(Lambda(z)-Lambda(z0))z0_x,
G(0,0,x)=0. On this chart G and Lambda have fixed smooth derivative bounds;
G is affine in eta. This comparison removes background transport terms
without setting the fields stationary. All field characteristic speeds are
bounded independently of V inside the chart.

For E0=||delta||, E1=||delta_x||, E2=Lip_x(delta_x), the characteristic
equation and its first derivative give, on E0<=delta_* and E1<=1,

  E0(t)<=K integral_0^t [E0+||eta||] dz,
  E1(t)<=K integral_0^t [E1+E0+||eta||+||eta_x||] dz.       (7)

Before this restriction the first derivative inequality contains an E1^2
term; it is not discarded without a bootstrap. For example differentiating
(6) introduces -Lambda_x delta_x, with Lambda_x bounded by K(1+E1).
The background contributes fixed derivative constants. Equations (2)-(3)
and zero initial delta imply

  E0(t)<=K t, E1(t)<=K t/ell.                             (8)

To justify E2, compare the first-derivative equations along pairs of field
characteristics and divide by their separation. The separation distortion
is bounded by exp(Kt) on the E1 bootstrap. Differentiating their coefficients
as spatial Lipschitz functions produces a term K E2 and terms bounded by
K(E0+E1+E1^2+||eta||+||eta_x||+Lip eta_x). Thus

  E2(t)<=K integral_0^t [E2+1/(epsilon ell^2)] dz
       <=K t/(epsilon ell^2).                           (9)

No pointwise second derivative at the original joins is needed. The constants
in (7)-(9) include smooth inverse-chart bounds and background derivatives.
Since t<=kappa ell/V, t/ell<=kappa/V, choose N0 large (or kappa smaller) so
K t<delta_*/2 and K t/ell<1/2. A usual first-exit argument then closes the
field chart and E1 bootstrap on the stipulated interval of existence. It
does not prevent a failure of the unproved fluid bounds (1).

The exact compatibility g_t=p_x and the fact p0=0 improve (8):

  ||g(t)-g0|| <= K t^2/ell,
  ||g_x(t)-g0_x|| <= K t^2/(epsilon ell^2).                (10)

For the second inequality use Lip_x p_x from (9), integrate in time and use
continuity of g_x. Smooth inversion of z also costs terms O(E0)+O(E1)^2,
which are absorbed in (9). At t<=T_N=kappa ell/V, these are respectively

  K kappa^2 L/v0^2 N^-5,
  K kappa^2/(c v0) N^-1.                                (11)

The original force itself, phi_x, therefore retains a positive lower margin
for sufficiently large N within the stipulated solution. Even the weaker
O(t)=O(N^-4) bound from the chart estimate suffices for this purpose.
The weaker first derivative estimate O(t/ell)=O(N^-1) follows already from
(8), independent of (9); (9)-(11) do not improve its N power, but expose the
exact join-related inverse factor rather than claiming O(N^-2).

Scale is dynamically controlled as well. From the fixed-speed equations for
w±dk, subtraction of the background yields forcing D(g,chi)-D(g0,chi0).
Using (10) and chi_t=w yields, after Gronwall on a fixed short interval,

  ||w||+||k-k0|| <= K t^3/ell,
  ||chi-chi0|| <= K t^4/ell.                              (12)

These estimates are in fixed normalized units and are conservative. They
imply positive uniform a=a_ref exp chi margins. Their use requires field
characteristic containment; no static elliptic inversion has been used.
The first-order constraints are chi_x=k and phi_x=g, propagated as in the
pinned construction, and are prerequisites for identifying (5) with the
original four equations. In particular B_x=Cn+tau phi_tt throughout.

## 4. Domains, controls and exact remaining input

For a fixed physical K0 inside the old regular patch, a cone shrinking at
speed S_N=A V+B contains all fluid speeds |v|+c and field speeds if |u| is
uniformly bounded and the field chart is retained. Its lost physical width
S_N T_N=A kappa ell+B kappa ell/V tends to zero. Thus a fixed inner interval
is contained for all sufficiently large N. The additional |u| bound follows
from any uniform bound for u±epsilon q, or from integrating u's equation
using (3), but must be stated in an existence proof. Uniqueness on common
backward domains implies extension independence, not a universal lifetime
for arbitrary uncontrolled exterior extensions.

The full energy identity has density
nv^2/2+c^2 n[log(n/nref)-1]+n phi+
[tau p^2/2+W+sigma w^2/2+J k^2/2+U]/C,
and flux nv[v^2/2+c^2 log(n/nref)+phi]-(p B+Jwk)/C.
Its divergence vanishes by the exact +np/-np and -Tw/+Tw cancellations.
Moving endpoints contribute their endpoint velocity times energy. The exact
hydrostatic control with v=0 has delta=eta=0 and all estimates vanish. Neither
the control nor small initial kinetic energy proves (1).

Missing implication for unconditional FGF048: construct actual C1,C1,1
solutions through s=kappa with N-independent M,H in (1), or supply another
uniform set of norms sufficient to replace them, together with the stated
domain and continuation gates. For finitely many admissible N<N0, the old
fixed-N theorem can cover a common positive kappa after taking a finite
minimum, but this only helps once the large-N theorem is established.

## 5. Obligation matrix and failed estimates

| Obligation | Status in this narrow derivation |
|---|---|
| Density bound from actual continuity | Passed conditional on (1), existence |
| Pressure retained | Passed; no zero-pressure substitution |
| Force feedback with dynamic source | Passed conditional on the same premises |
| First spatial force derivative | Passed with explicit epsilon^-1 loss |
| Uniform solution existence/continuation | Not addressed; named missing input |
| Exact C1,1 joins | Retained, pair-characteristic estimates only |
| Field chart/positive scale and g margins | Conditional bootstrap closes |
| Physical cone/extension independence | Conditional on uniform u bound and existence |
| Energy/hydrostatic control | Direct algebra, inherited compatible class |
| Full nonlinear author theorem | Awaiting final pins; unexposed |

Unsuccessful or insufficient estimates preserved:
(i) an independent rectangle in r=v+cq,s=v-cq permits q=O(V/c), producing
an artificial exp(O(N)) density bound; (2) avoids this.
(ii) a naive uniform q_yy bound ignores the inverse epsilon in (4), and would
spuriously improve the g_x response to N^-2; no such improvement is claimed.
(iii) a pointwise initial Taylor jet cannot establish any of (8)-(12) on the
whole interval; all are characteristic integral estimates.
(iv) fixed-N existence plus bounded initial energy does not prove the needed
scaled norms or their continuation. Failed estimates are not counterexamples.

Apply separately to both a_ref=9.3619e-11 and 1.1279e-10 and their fixed
backgrounds, and separately to each frozen a0 E(z) comparison. No evolving H,
vacuum completion, RAR/M/MONO transfer, observational, DOF or closure claim.

Proof-only: zero mathematical executable computations, zero external sources.
Hash checks and file writes are administrative operations. Self-proofreading
reviewed this file's notation, signs, hypotheses and displayed estimates;
no external manuscript was edited. Exact raw task/source pins are retained
in INPUT_PINS.txt. The cheapest next check is whether the final author proof
actually supplies the independent uniform premises (1), not whether its
formal initial response agrees with (11).
