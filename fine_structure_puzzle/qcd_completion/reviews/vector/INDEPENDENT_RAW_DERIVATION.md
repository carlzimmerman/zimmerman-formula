# Independent raw Cartesian J=1 vector derivation

Saved before opening the target full-vector implementation or numerical outputs.
Provenance: fresh independent subagent derivation, 2026-10-19 UTC.
Scope: fixed external polarization p, |p|=1, J=1 static adjoint vector sector on a ball. No QCD completion or alpha claim.

## Definitions and conventions

Let r=t, n=x/r, q=n.p, w=n cross p, and identify spatial/color Cartesian frames e_i.
A_i=(1-K)(e_i cross n)/r, Phi=A_4=h n,
K=r/sinh r, h=coth r-1/r, D_mu=partial_mu+A_mu cross, partial_4=0.
K'=-Kh and h'=(1-K^2)/r^2.
With F_ij=partial_i A_j-partial_j A_i+A_i cross A_j, these signs give
B_i=(1/2)epsilon_ijk F_jk=-D_i Phi, NOT +D_i Phi.
Write b=h' and c=Kh/r=-K'/r. Then
M_i=D_i Phi=c e_i+(b-c)n_i n,
F_i4=M_i, F_ij=-epsilon_ijk M_k.
Near zero b=c=1/3+O(r^2); A_i=(e_i cross x)/6+O(r^3), Phi=x/3+O(r^3).
These fields are analytic in Cartesian x.

## Seven spatial tensors

Use color-first indices (a,i), and define:
T1_ai=q delta_ai,
T2_ai=n_a p_i,
T3_ai=p_a n_i,
T4_ai=q n_a n_i,
T5_ai=(e_i cross p)_a=epsilon_aij p_j,
T6_ai=q(e_i cross n)_a,
T7_ai=n_a w_i.
Every SO(3)-equivariant Cartesian a_i linear in p has seven independent coefficients
a_i=sum_(A=1)^7 f_A(r) T_Ai. Angular Gram positivity below proves independence.

Representation count: spatial spin 1 tensor color spin 1 is 0+1+2.
Coupling to total J=1 allows L=1 for internal spin0; L=0,1,2 for spin1;
L=1,2,3 for spin2. Hence seven copies for each fixed m/p.

Using normalized sphere average (integral/(4pi)), the Gram blocks are
G_odd (T1,T2,T3,T4) =
[1,1/3,1/3,1/3;
 1/3,1,1/3,1/3;
 1/3,1/3,1,1/3;
 1/3,1/3,1/3,1/3].
G_even (T5,T6,T7) =
[2,2/3,-2/3;
 2/3,2/3,0;
 -2/3,0,2/3].
Odd/even cross blocks vanish by n parity. Both blocks are positive definite.

Orbital Laplacian:
L^2 T1=2T1, L^2 T2=2T2, L^2 T3=2T3,
L^2 T4=12T4-2(T1+T2+T3),
L^2 T5=0,
L^2 T6=6T6-2T5,
L^2 T7=6T7+2T5.
Thus T1,T2,T3 are L1; T4-(T1+T2+T3)/5 is L3;
T5 is L0; T6-T5/3 and T7+T5/3 are L2.
Spatial multiplicities L0:1,L1:3,L2:2,L3:1.

## Three A4 vectors

Q1=p, Q2=q n, Q3=w, with A4=sum g_A Q_A.
Their normalized Gram is
[1,1/3,0;1/3,1/3,0;0,0,2/3].
Q1 is L0, Q2-Q1/3 is L2, Q3 is L1.
Combined ten-channel L multiplicities are (2,4,3,1) for L=(0,1,2,3).
Each fixed-p solution represents one m of total J1, and determinant multiplicity is 2J+1=3.

## Smooth origin, not merely bounded origin

For pure orbital harmonics, Cartesian smooth/analytic regular profiles have
f_l(r)=r^l sum_(k>=0) a_k r^(2k). With reduced u=r f, regular leading exponents
are rho=l+1 with multiplicities rho1:2,rho2:4,rho3:3,rho4:1;
irregular exponents are -l.
In the mixed polynomial tensor basis, columns must be transformed by the exact
orbital eigenvectors above. Starting all channels with a common r power is invalid.

Integer exponent differences cause formal Frobenius resonances. For an operator
derived from the smooth Cartesian background, its Taylor-degree filtration forces
the regular resonance compatibility conditions: a homogeneous source of degree d
cannot have orbital harmonic degree d+2. Smooth regular solutions therefore need
no logarithmic terms. This does not license a naive recurrence that divides by a
singular matrix; kernel freedom and compatibility must be imposed explicitly.
A finite-order seed should be checked against the full Cartesian equation and
against the ten-dimensional smooth solution space.

## Exact translation solution and sign benchmark

Translate in direction p and compensate by gauge parameter -p.A:
a_mu=p_j F_jmu (the overall translation convention may reverse all signs).
Then
a_i=c(e_i cross p)-(b-c)n w_i = c T5_i-(b-c)T7_i,
a4=c p+(b-c)q n = c Q1+(b-c)Q2.
The radial spatial trace is a_r=n_i a_i=c w.
The tangential trace is
a_i^T=c(e_i cross p)-c n_i w-(b-c)n w_i.
The temporal trace is a4=c(p-q n)+b q n.

Background YM implies G=D_mu a_mu=p_j D_mu F_jmu=0.
The Hessian H_munu=-D^2 delta_munu-2 ad(F_munu) therefore obeys H a=0,
by differentiating YM and using the compensating gauge transformation.
This is an exact all-r identity, not only an asymptotic check.
At r=0, a_i=(e_i cross p)/3+O(r^2), a4=p/3+O(r^2), entirely L0.

At any finite R>0, b>0,c>0. The translation has nonzero Dirichlet wall traces,
so it is NOT an exact zero mode in the relative-wall domain.
As R grows, c is exponentially small and b~1/R^2. Its leading a4 trace is
q n/R^2 and its leading tangent spatial trace is -n w_i/R^2.
Any resulting finite-ball quasi-zero eigenvalue must remain in an unprimed determinant.

## Relative mixed boundary domain

Set P_ij=delta_ij-n_i n_j. The relative wall is
P_ij a_j=0, A4=0, G=D_i a_i+Phi cross A4=0 at r=R.
The seven spatial channels have a three-dimensional radial trace space:
a_r=(f1+f2+f4)q n+f3 p+(f5)w
(the n contraction of T6 vanishes and T7 has w.n=0).
[Correction within raw derivation: n_i T1_ai=q n_a, n_i T2_ai=q n_a,
n_i T3_ai=p_a, n_i T4_ai=q n_a, n_i T5_ai=w_a,
n_i T6_ai=0, n_i T7_ai=0.]
Thus spatial tangential Dirichlet imposes four independent radial coefficient
conditions, and A4 imposes three: seven Dirichlet rows total.
On these Dirichlet traces, A_r=0 and A4=0 give G=(partial_r+2/R)a_r.
The three remaining conditions are radial Robin rows, seven D plus three R.
The coupled coefficient basis may hide these rows but cannot change their rank.

For an unbroken free reference A=Phi=0 (if this is the intended reference),
the same angular basis and mixed wall domain must be retained. Free origin
solutions are r^l in the unreduced fields, and the full boundary determinant,
including its R powers and all basis normalization factors, is the reference.
Changing the wall to all-Dirichlet is a different determinant.

## Gauge-image / ghost pairing

On a YM background,
H_munu D_nu c=D_mu(-D^2 c).
Indeed [D^2,D_mu]c=ad(D_nu F_numu)c-2ad(F_munu)D_nu c.
For a Dirichlet ghost eigenfunction (-D^2)c=lambda c with c|R=0,
a_mu=D_mu c satisfies a_tangent|R=0, a4|R=0, and
G|R=D^2 c|R=-lambda c|R=0. Hence it belongs to the vector mixed domain,
with the same eigenvalue. The same identity holds for the free reference.
The three ghost angular channels have L0,L1,L2 origin branches as Q above.
For J1 only, the usual one-loop log weight is
3*(1/2 log det H_vector - log det H_ghost).
Gauge pairing alone does not establish an all-channel self-dual isospectrality
with these boundary conditions.

## Audit obligations fixed in advance

Compare target conventions to the B=-D Phi benchmark; test the exact translation
and gauge-image identities, angular Gram symmetry, ten origin exponents,
resonance compatibility, seven D plus three R wall rank, matched free reference,
m=3 multiplicity, unprimed quasi-zero retention, and current input/output hashes.
Finite R integration accuracy is distinct from the controlled large-R coefficient.
A handful of fitted radii alone does not bound that coefficient.

