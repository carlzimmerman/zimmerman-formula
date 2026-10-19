# Independent asymptotic review of the actual full J1 determinant

Normalized claim: on the exact BPS background, with fixed asymptotic mass, the actual unprimed 7D+3R J1 vector determinant against the stated K=1,h=0 auxiliary reference has
log Dvec=6x-22log x+Cvec-2/x+O(x^-2);
the exact J1 ghost then gives
log Z_J1=-3x+15log x+Cz+3/x+O(x^-2).

**Primary verdict: conditional on the ordinary L² kernel/index input identified below.**
The local outer matrix, charged series, neutral scattering constraint, nonzero mixed-wall leading matrix, and Schur-tail estimates support the stated coefficient. The coordinator's rank argument is valid once that input is supplied. The separate kernel review supplies a primary weighted-index theorem plus a new internal bridge to the physical Coulomb domain; I audited the internal bridge and found no issue other than an explicit sign/chirality identification requested from that reviewer. I have not independently fetched the primary index PDFs. Once that source/domain identification is accepted, no additional global rank or local wall obstruction was found here.

The finite numerical table is not evidence for this coefficient and was not fitted or re-integrated. The completed finite review in the parent vector review folder remains unchanged.

## Independent derivation and exact artifacts

ASYMPTOTIC_RAW.md was saved before reading the author's new DERIVATION.md, REPORT.md, asymptotic code, or the coordinator's rank argument. It independently found:
- charged C=(0,0,2,2,6,6), neutral C=(0,2,2,6);
- charged growing correction sum=-2;
- raw full mixed-boundary growth e^(6x)x^-2 with nonzero leading factor;
- possible neutral L0 correction +9c0/(10x);
- the regular ghost-gradient route to c0=0;
- the Wronskian exclusion of a non-L² neutral L0 constant resonance.

Actual frozen Cartesian input is derive-001/operator.json, SHA256
4e98fa28d208693d6559c8bf5b2dd4b1c05e4d5b88827c38fb21230ac645f6bd.
The independent local-001 manifest validates with current inputs and records all these exact matrix checks. No author asymptotic input entered that run.

After the independent raw save, reviewed target artifacts were:
- check_asymptotic_v3.py SHA25664acfbe9445c7a84dfb9d7aa49f23d76454b61741a5efbcda74afde04b16ba19;
- asymptotic-003/result.json SHA256b37bccb476a7703218641a3d02e877660e50bb8850dcda89df013316b195034d;
- DERIVATION.md SHA256b3f589f37fa7f745d10dc7459802169f4b8ea2a0e8b70aaa2b49be5066bb96cd;
- REPORT.md SHA256a552bb8706d53e7f65f430bd48a8de23c0f2f718cbf806b1e41a24981b00ad4b;
- coordinator rank argument SHA256f9000cbb40e0e72f088320e8a82662c5fc702997bd14a8c95b561fe7b8200772;
- kernel RAW_DERIVATION_v1.md SHA256c891c02ed38ce255702fdac061c70c67c766b4b2739d7d56de94bbb9fb83421c;
- kernel SOURCES_v1.md SHA256897c88a834798563bdcabed551ebdd7e6df41858147d8f71a185335dd6746c27.

The target asymptotic-003 manifest validates against its current input and output hashes. Later author report edits are outside these recorded report hashes.

## Outer equation and charged asymptotics

The exact outer matrix extracted from the actual V is

Vout=P-2P/x+C/x², P²=P, [P,C]=0.

Both P and C are G-self-adjoint. The neutral space is span(B2,B3,B6,B8).
The stored normal projector PN=Z N is G-orthogonal and commutes with P.
These are exact algebraic facts, not scalar-copy assumptions.

A charged eigenchannel satisfies u''=(1-2/x+c/x²)u. Its growing series is

u+=e^x/x sum b_n x^-n,
b0=1, b_n=[n(n+1)-c]b_(n-1)/(2n).

Thus b1=1-c/2 and b2=(6-c)b1/4.
For c=0,2,6 these are respectively (1,3/2),(0,0),(-2,0).
Each occurs twice, giving sum b1=-2.

Exact growing representatives are
c0: 4x e^-x Ei(2x)-2e^x,
c2: e^x/x,
c6: e^x/x(1-2/x).
All three exact differential residuals vanish in the supplementary check.
The c0 growing series is nonterminating. Accordingly the q³/q⁴ terms printed
by asymptotic-003 from its a2-truncated ansatz must not be interpreted as
higher exact asymptotic coefficients. Its first- and second-order conclusions
remain within the declared truncation order.

The mixed normal wall is u'+u/x. Differentiating e^x/x cancels the universal
-x^-1 contribution against +u/x; through first order the value and normal
functional both have multiplier 1+b1/x. This gives the charged -2/x,
provided the leading full wall matrix is nonzero.

## Neutral scattering and why it does not change 1/x

Use neutral vectors
v0=B2,
v6=(3B3-B2)/sqrt2,
vplus=(B6+2B8)/sqrt2,
vminus=-B6+B8.
They are G-orthonormal, with centrifugal eigenvalues0,6,2,2.

The exact translation has u=vminus/x plus exponential corrections.
Its zero Wronskian with every regular solution forces the neutral C2 growing
direction to be vplus. Translation remains in the finite determinant.

A neutral L0 scattering constant cannot simply be discarded. If the normalized
regular L0 column were (x+c0)v0, direct actual mixed-wall algebra would give

log Dvec first inverse coefficient=-2+9c0/10.

This potential contribution was independently present in the blind raw derivation.

It is removed by an exact regular ghost gradient. In the ghost RE block,
two smooth regular columns have one charged-growing row. That row has rank
one: otherwise one could cancel the neutral-growing row and obtain a nonzero
L² ghost zero, contradicting positivity. Its one-dimensional kernel has a
nonzero neutral growing coefficient for the same reason. Normalize its ghost to

cghost=n(n.p)[x+A/x²]+O(poly(x)e^-x).

The vector gradient has reduced tail

g0=x v0-sqrt2 A v6/x²+O(poly(x)e^-x),

with no L0 constant and no other neutral growing coefficient. Set
gamma=-sqrt2 A. The actual normalized L0 vector column can be taken as g0.

For its neutral C6-growing companion, let
h=x³v6+b v0+delta v6/x².
The zero regular-origin Wronskian is W(g0,h)=5gamma-b, forcing b=5gamma.
Thus all remaining neutral scattering contributions start at relative x^-3.
Likewise in the translation block the independent neutral growing column is
(x²+eta/x)vplus modulo adding translation, a relative x^-3 correction.

The independent second-002 check retains arbitrary gamma,delta,eta and evaluates
the actual neutral projected wall matrix. Its determinant is

5(eta+x³)(gamma²-2sqrt2 gamma x³+2x6)/(3x5)
=(10/3)x4[1+O(x^-3)].

It is nonzero at leading order. In particular no neutral x^-1 or x^-2 term
survives, and delta cancels from this boundary determinant. This is a stronger
check than omitting all neutral scattering by assumption.

## Connection ranks: the exact remaining global input

Let L be the ten-dimensional smooth-origin zero-solution space and S the
ten-dimensional no-growing space at infinity: six charged decays, neutral
C0 constant, two C2 decays x^-1, and C6 decay x^-2. Both are Lagrangian for
the conserved G-Wronskian. The outer construction and remainder estimates
below justify these exact asymptotic spaces.

For s in L intersection S, W(g0,s)=0 eliminates its only non-L² branch,
the C0 constant. Hence L intersection S equals the ordinary L² kernel.

If that kernel is the translation line per magnetic quantum number, the
growing projection of L has rank9. Its sole annihilator is W(translation,.).
Translation has a nonzero neutral C2 decay, so this annihilator contains a
neutral-growing coefficient. It cannot be a relation supported only on the
six charged growing rows. Those rows have rank6, and their four-dimensional
kernel has neutral-growing rank3 with translation kernel. This is the
coordinator's valid symplectic argument; it is not a finite-rank numerical test.

The ordinary L²-kernel statement is the only source-dependent count.
The kernel agent's cited Kottke weighted index4, framed charge-one domain,
must be connected to the actual Coulomb Hessian. Its internal bridge correctly:
1. identifies the hybrid domain X=Hb1(neutral) plus x Hsc1(charged),
   common target Y=xL², with x=1/r;
2. rescales the weighted gauge output by the specified isometry;
3. obtains the Coulomb gauge row plus a compact charged O(1/r) correction
   and exponentially small off-diagonal corrections;
4. kills the weighted cokernel using chi/r in L² and a Caccioppoli cutoff;
5. proves the ordinary L² kernel lies in X using a massive charged estimate
   applied to r a_ch and a flat neutral Dirac estimate applied to coordinate
   multiples of a_neutral.

These arguments are coherent. In particular the weighted adjoint prefactor
rho is retained; the ordinary unweighted operator is not incorrectly declared
Fredholm at the neutral threshold. The no-cokernel estimate uses only
chi/r in L², enough to force the annular cutoff energy to zero. The reverse
kernel inclusion follows from uniform cutoff estimates, not a silent domain
identification.

The kernel note begins in B=+D Phi convention, whereas the target uses
B=-D Phi. This is harmless after an explicit chirality/sign transfer, but the
source-to-target identification must state that transfer. I requested it from
the kernel reviewer. The primary theorem itself is treated here as the exact
authenticated external input in its SOURCES_v1.md; I did not perform a second
primary-source literature audit.

## Exact outer basis and charged-induced neutral tails

Small coefficients alone are insufficient: K times a growing e^x/x mode can
produce polynomial neutral components. The following control is needed and
is available from the actual equations.

In charge/neutral coordinates, use the explicit charged Coulomb pairs
above and the neutral Euler pairs x^(l+1),x^-l for l=0,1,2.
Their Wronskians are nonzero constants. The exact coefficients differ from
the outer equation by exponential functions times finite powers of x.
Variation of parameters therefore yields:

- charged-growing columns have charge parts e^x/x times the displayed inverse
  series, plus exponential-relative corrections; their neutral parts may be
  polynomial, possibly with logarithms;
- columns with no charged growth have charged parts O(poly(x)e^-x);
  their neutral parts are combinations of the exact Euler powers plus
  exponentially small corrections, including differentiated remainders;
- charged-decaying columns can be chosen with vanishing neutral free-power
  coefficients and exponentially small neutral parts.

One concrete construction solves the neutral Euler inhomogeneous equation
for the forced polynomial tail of a charged-growing mode, then substitutes
it back into the gapped charged equation. Each charged-to-neutral-to-charged
loop contains two exponential off-diagonal factors. The explicit scalar
Green kernels have only polynomial center factors, so these loops are
bounded by poly(R)e^-2R on an exterior [R,infinity); choose R large to
obtain a convergent correction. The charged homogeneous growing amplitude
is fixed by its e^x/x normalization. On the no-charged-growth space the
unstable Green integral runs from infinity, while the stable component
runs from R; polynomial forcing resonant with e^-x can add powers/logarithms
but preserves O(poly(x)e^-x). The remaining neutral feedback is exponential,
so it adds no algebraic Euler powers or logarithms beyond the chosen free
neutral coefficients. This supplies the exact outer decomposition used above.

For the boundary determinant make the constant invertible row change
from [T u;N(u'+u/x)] to

Wwall(u)=PD u+PN(u'+u/x).

Because [P,PN]=0, its rows split into charge6 and neutral4. After a constant
regular-column change using the now-established connection ranks, write

[ Cc  Cn;
  Nc  Nn ].

Here Cc=(e^x/x)[A0+O(1/x)], A0 invertible, hence
Cc^-1=O(poly(x)e^-x). The neutral wall traces Nc of the six charged-growing
columns are at most polynomial/logarithmic. The charged traces Cn of the
four no-charged-growth columns are O(poly(x)e^-x). Therefore

Nc Cc^-1 Cn=O(poly(x)e^-2x).

The neutral leading boundary matrix Nn has a nonzero Laurent leading
determinant, verified exactly above; its inverse grows at most polynomially
by the adjugate formula. Thus this Schur correction remains exponential
after multiplication by Nn^-1 and cannot affect 1/x or 1/x².
There is no unexamined asymptotic ill-conditioning or leading wall zero
that promotes the charged-induced neutral polynomial tails into 1/x.

## Coefficient and supplementary second order

The first independent local run, with unnormalized neutral vg and v2 choices,
finds F~(135/4)e^(6x)x^-2 times a nonzero global connection constant.
The exact reference is (5103/8)x20. This gives the x^-22 ratio power.

With c0=0, charged trace sum=-2 and neutral first correction0, so

log Dvec=6x-22log x+Cvec-2/x+O(x^-2),
log Z_J1=-3x+15log x+Cz+3/x+O(x^-2).

The supplementary check also verifies the claimed absence of a logarithmic
x^-2 term. Put A1=P-PC/2 and A2=(6P-PC)A1/4. Exact actual-matrix traces are

tr A1=-2, tr A2=3, tr(PN A1)=-2, tr(A1²)=10.

The charged logarithmic second coefficient is
tr A2-tr(PN A1)-tr(A1²)/2=3+2-5=0.
The neutral second coefficient is zero as above. This second-order result
does not authenticate q³ or higher from the truncated polynomial.

The auxiliary pure-SU2/fixed-circle/fixed-asymptotic-mass comparison and its
boundary path remain the precise scope. No full QCD subtraction, electric
charge normalization, or alpha result follows.

## Computation and review record

- local-001: completed,2.38 child seconds, validated v2 manifest.
- second-001: resource-limit at the declared CPU cap; no result file.
  It attempted a large expanded symbolic10x10 determinant with three neutral
  scattering parameters. Preserved as resource-inconclusive, not evidence.
- second-002: completed,0.29 child seconds, validated v2 manifest.
  Immutable v2 code uses [P,PN]=0, charged traces and a4x4 neutral determinant.
  It checks exact charged Ei/polynomial solutions, neutral Wronskian, all
  scattering parameters, and the first two mixed-wall inverse coefficients.

No target file or earlier completed review was edited. All computations had
saved contracts and immutable code before execution. This addendum's math
proofreading self-review covered its own notation, signs, powers, domain
qualification and first-versus-second-order claims; no mathematical-token
correction to a target artifact was made.

