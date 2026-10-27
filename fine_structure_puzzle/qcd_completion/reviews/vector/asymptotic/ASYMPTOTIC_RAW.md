# Independent raw asymptotic derivation

Saved before reading the author's new asymptotic files, REPORT.md, DERIVATION.md,
or the coordinator's COORDINATOR_RANK_ARGUMENT.md.
Fresh derivation from the already audited actual derive-001/operator.json.
No coefficient is inferred from the finite determinant values.

## Conventions and exact local outer matrix

Use target raw tensor numbering B0,...,B9 (spatial rows, adjoint columns).
The Gram, boundary T,N and exact V are the frozen derive-001 matrices.
Set K=K'=0, h=1-1/t, h'=1/t². Exact symbolic extraction gives

Vout=P-2P/t+C/t², P²=P, [P,C]=0,
P,C self-adjoint in the angular Gram G.

Charged P=1 multiplicity6 has C eigenvalues (0,0,2,2,6,6).
Neutral P=0 multiplicity4 has C eigenvalues (0,2,2,6).
The neutral coefficient subspace is span(B2,B3,B6,B8).
Convenient eigenvectors are
v0=B2, C v0=0;
v2=B3-B2/3, C v2=6v2;
vs=B6, va=B8, each C=2.
Their Gram norms are |B6|²=2/3, |B8|²=1/3.
All these statements were checked exactly from the actual serialized operator.

The actual BPS K is exponentially small and h=1-1/t+O(e^-2t).
This alone does not mean every component of a growing charged solution differs
exponentially from the decoupled free basis: products K*e^t can force polynomial
neutral tails in charged-growing columns. Those tails are harmless to the
algebraic determinant expansion only after a genuine charged-growing/neutral
connection decomposition. That decomposition is a global hypothesis here.

## Charged growing first series

For one charged C eigenvalue c, -u''+(1-2/t+c/t²)u=0.
Write
u+(t)=e^t/t sum_(n>=0) b_n t^-n, b0=1.
Then
b_n=[n(n+1)-c]b_(n-1)/(2n).
Thus b1=1-c/2:
C=0: b1=1 (twice),
C=2: b1=0 (twice),
C=6: b1=-2 (twice).
The sum of charged first corrections is -2.

For C2, u+=e^t/t is exact. For C6,
u+=e^t/t(1-2/t) is exact. For C0, the growing solution has a
nonterminating asymptotic series; one exact normalization is
u+=4t e^-t Ei(2t)-2e^t,
whose series is e^t/t(1+1/t+3/(2t²)+...).
The independent decaying C0 solution is t e^-t.
One cannot describe all six growing channels as finite polynomials.

For the actual mixed normal wall,
u+'+u+/t=e^t/t[1+b1/t-b1/t²+...].
The universal -1/t from differentiating t^-1 cancels against the Robin term.
Hence the charged Dirichlet and Robin rows have the same first relative
correction b1/t. Any leading nonzero mixed-wall determinant receives trace
sum b1=-2 from the charged sector, with no additional first-order Robin shift.

## Translation, neutral growing complement and required ranks

The exact known regular translation has, to every algebraic order,
u_tr=(-B6+B8)/t = vtr/t.
It is an L² zero-energy solution on infinite space, with nonzero finite wall
traces. It must stay in the unprimed finite-ball determinant.

Let
vg=B6+2B8.
Then vtr^T G vg=0.
The constant Wronskian of any smooth regular solution with the regular
translation vanishes at the origin. In the neutral C2 sector, the growing
coefficient t² v must therefore satisfy vtr^T G v=0. Thus vg is the only
allowed growing direction in that two-dimensional neutral C2 subspace.

For a full leading determinant, the following global connection properties
are sufficient and are not established merely by the local outer matrix:

H1. The regular ten-dimensional solution space has charged-growing rank6.
H2. In its four-dimensional charged-nongrowing kernel, the neutral-growing
    map has rank3 with image span(t v0,t² vg,t³ v2).
H3. Its remaining one-dimensional kernel is the known translation and there
    is no additional zero-energy resonance requiring a different outer basis.
H4. The asymptotic expansion and remainder are compatible with this connection
    decomposition, so charged-neutral Schur corrections are exponentially small
    relative to the nonzero algebraic leading boundary determinant.

Equivalently, one can prove the L² kernel is exactly the translation, exclude
a neutral C0 resonance, and use dimensions/Wronskians to infer H1-H3. The
zero-energy resonance issue matters because u=constant in the neutral C0
channel is not L² (a=u/t~1/t); an L² index statement alone does not exclude it.

## Neutral C0 scattering can affect the coefficient

After the six charged-growing amplitudes have been removed and the three
neutral-growing amplitudes normalized, allow the L0 column

u0=(t+c0)v0+lower channels,
ug=t² vg+lower channels,
u2=t³ v2+lower channels,
utr=vtr/t+exponentially small terms.

Here c0 is the same-channel neutral L0 scattering constant. Adding the
translation to a growing column is a harmless triangular basis change.
Neutral off-diagonal scattering terms enter at relative orders at least t^-2
after these leading powers are normalized; the same-channel L0 constant
is the only possible first-order neutral contribution.

The neutral wall factors are explicit. In the gradient/radial block (v0,v2),
Dirichlet tangent and normal Robin produce

[t+c0, -t³/3;
 2+c0/t, 8t²/3],

with determinant (10/3)t³+3c0 t²
=(10/3)t³[1+9c0/(10t)].

In the spatial-curl/A4 block (vg,vtr), the two Dirichlet rows give

[t²,-1/t; 2t²,1/t],

with determinant3t. Thus the neutral four-column wall determinant is
10t4[1+9c0/(10t)].
It is nonzero at leading order. The neutral C0 constant does not vanish
automatically from the mixed Robin condition.

## Full local boundary determinant

Using a G-orthonormal exact eigenbasis of the six charged outer channels and
the neutral columns (v0,vg,v2,vtr) in that order, the actual stored T,N give

det Fout(t)=(135/4)e^(6t)t^-2
 [1+(-2+9c0/10)/t+O(t^-2)].

The nonzero coefficient135/4 depends on the explicit local channel ordering
and normalization. A nonzero global regular-to-outer connection determinant
multiplies it. The known free boundary determinant is (5103/8)t20. Therefore,
under H1-H4 and this normalization,

Dvector(t)=L e^(6t)t^-22
 [1+(-2+9c0/10)/t+O(t^-2)], L!=0.

The exact static J1 ghost comparison has logDghost=2t-6logt+constant
plus exponentially small terms. Consequently the unprimed Gaussian has

log Z_J1=-3t+15logt+constant
 +(3-27c0/20)/t+O(t^-2).

This is a conditional formula; it does not follow from fitting finite points.

## Independent route that could force c0=0

The exact gauge-gradient identity suggests a direct internal argument.

For static J1 ghosts, there are three smooth regular zero-energy columns and
at most two charged-growing amplitudes. Hence a nonzero smooth regular ghost
exists with no charged-growing amplitude. If its neutral-growing coefficient
also vanished, its only tails would be neutral t^-1 reduced (c~t^-2) and
charged decaying; it would be L². Positivity of
integral(|D c|²+|Phi cross c|²) and integration by parts at infinity then gives
D c=0, Phi cross c=0, and the decay gives c=0. Thus this cannot happen.
The charged-growing map on the regular ghost space has rank exactly2, with
one-dimensional kernel and nonzero neutral-growing coefficient.

After normalization, such a ghost has
cghost=n(n.p)[t+b/t²]+exponentially small terms,
since its reduced neutral component is t²+b/t.
Its exact gradient has
u_vector=t B2 + b t^-2(B2-3B3)+exponentially small terms.
It is smooth, H u=0, and has no charged-growing term.
It has exactly zero neutral L0 constant c0.

If H1-H3 identify the unique normalized L0 growing vector column modulo
other neutral-growing channels and translation, this gradient fixes c0=0.
Then the local coefficient becomes -2 in logDvector and +3 in logZ_J1.

The same gauge-gradient can exclude a neutral C0 resonance: a regular
solution with no growing charged or neutral coefficients would have only
constant v0 plus decaying neutral powers. Its zero Wronskian with the
gradient's t v0 tail forces that constant to vanish; it is then L².
Thus ordinary L² kernel dimension1 per p, together with this scalar argument
and asymptotic classification, could establish H1-H3. Any source connecting
a weighted index to that ordinary L² kernel must be audited separately.

I have not read the coordinator's rank proof or the author's asymptotic
derivation at this point. The c0 argument above is an independently derived
candidate proof, whose asymptotic/functional-analytic hypotheses remain explicit.

## Reproducible local exact check

Contract and code were saved before execution:
COMPUTATION_CONTRACT_v1.json and check_asymptotic_v1.py.
Run runs/local-001 completed in2.38 child seconds; its v2 manifest validates
against the immutable operator and script hashes.
Exact results: charged C=(0,0,2,2,6,6), neutral C=(0,2,2,6),
charged correction trace=-2, nonzero scaled wall coefficient135/4,
first relative wall coefficient9c0/10-2.
No author asymptotic file, finite-value fit, or numerical ODE run entered it.

