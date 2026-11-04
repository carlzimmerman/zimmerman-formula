# Signed Cassini kernel: analytic checkpoint

The corrected KT33 reciprocal Gaussian quadrupole is strictly negative for
every finite common width and every positive external field, for the simple
nu function. More generally, this holds whenever

```
A(h) = nu(h)-1 = integral_0^infinity (h^2+t)^(-1/2) dP(t)
```

for a nonzero nonnegative finite measure P. This is a sign result, not a
monotonicity theorem in width or a lower bound sufficient to exclude a
subthreshold island. The derivation below is new in this checkpoint and
self-reviewed; independent proof review is outstanding.

## Exact target and inherited definitions

Inputs are the unmodified `KT33_reciprocal_filter/cassini/cassini_v2.py` and
the KT34 Cassini README/review. Write eta=gext/a0>0, g(r)>0 for the radial
source Newtonian field, h^2=g^2+eta^2+2g eta mu, and

```
A_l = integral_-1^1 A(h) P_l(mu) dmu,
b = -2(g A_2 + eta A_3),
c = 2[g A_2 + eta(3 A_3+2 A_1)/5].
```

For positive outer Gaussian width, T=P(5/2,r^2/(2 sigma^2)) and
L=r T'/T. The corrected whole-space quantity is

```
q = integral_0^infinity T/(2r) [3b+L c] d(log r).
```

The origin and infinity surfaces vanish for these Gaussian inputs. The
zero-width case has T=1 and L=0 and the same vanishing surfaces. The physical
normalization remains Q2_signed=(3/2)(a0/rM)q; no constants or cuts change.

## Positive softened-Coulomb representation of simple nu

Let F(s)=A(sqrt(s)) on the plane cut along the negative real axis. Direct
evaluation of the upper boundary gives

```
-Im F(-t+i0) = k(t),
k(t) = (1/2) sqrt[(sqrt(1+16/t)-1)/2] = B(t)/sqrt(t),
B(t) = sqrt[(sqrt(t^2+16t)-t)/8].
```

Here B is strictly increasing from 0 to 1. For example,

```
B'(t) = 4/[B(t) sqrt(t^2+16t) (t+8+sqrt(t^2+16t))] > 0.
```

Cauchy's formula on a keyhole contour gives

```
F(s) = (1/pi) integral_0^infinity B(t)/[sqrt(t)(s+t)] dt, s>0.
```

This contour step needs no subtraction: F(z)=O(|z|^-1/2) at infinity and
O(|z|^-1/4) at the origin, so both circular contributions tend to zero.
The principal nested square roots are analytic off the stated cut; their
upper and lower boundary values are complex conjugates.

Define the nonnegative density

```
rho(t) = [1/(pi t)] integral_0^t sqrt(v) B'(v)/sqrt(t-v) dv.
```

Tonelli's theorem applies to these nonnegative integrands. The elementary
substitution t=v(1+y^2), followed by y=tan(theta), gives

```
(sqrt(v)/pi) integral_v^infinity
    dt/[t sqrt(t-v) sqrt(s+t)]
  = 2/(pi sqrt(s)) arctan(sqrt(s/v))
  = (1/pi) integral_v^infinity dt/[sqrt(t)(s+t)].
```

Multiplying by B'(v) and integrating proves
F(s)=integral rho(t)/sqrt(s+t) dt. Similarly, integrating rho alone gives
integral rho = integral B' = 1. Thus P has positive density and unit mass.
For a stable numerical reconstruction, set p=B(v); its inverse is
v=4p^4/(1-p^2). This yields the independent scalar identity

```
A(h) = 2/(pi h) integral_0^1
       arctan[h sqrt(1-p^2)/(2p^2)] dp.
```

## Signed angular reduction

For a single t>=0, put H=g^2+eta^2+t and

```
C=(H+sqrt(H^2-4g^2 eta^2))/2,
z=g eta/C.
```

Then C>=max(g^2,eta^2), so 0<z<=min(g/eta,eta/g)<=1. The usual generating
identity follows directly from the power series of
(1+2z mu+z^2)^(-1/2); orthogonality gives

```
A_l(t) = 2(-z)^l/[(2l+1)sqrt(C)].
```

At z=1 this is its integrable boundary limit. Therefore

```
g A_2(t)+eta A_3(t)
  = 2z^2/sqrt(C) [g/5-eta z/7] > 0,
g A_2(t)+eta A_1(t)
  = 2z/sqrt(C) [g z/5-eta/3] < 0.
```

The inequalities follow from eta z<=g and g z<=eta. Positive integration
against P preserves them. Consequently b<0 and

```
3b+5c = 4(g A_2+eta A_1) < 0.
```

For the Gaussian kernel, its positive integral representation gives

```
T(x) = sqrt(2/pi)/3 integral_0^x u^4 exp(-u^2/2) du,
T(x) >= sqrt(2/pi) x^5 exp(-x^2/2)/15,
0 < L=x T_x/T <= 5.
```

Hence 3b+Lc is a convex combination of the two strictly negative quantities
3b and 3b+5c. Every radial contribution is negative, proving q<0. For a
finite positive mixture, the same argument works whenever the source is
radial with g>0 and the integral converges, and the outer kernel has T>0
and 0<=rT'/T<=5. Equal source/outer widths are not needed for this sign lemma.

## Quantitative attempt and its failure

The algebra also gives

```
-(3b+Lc) >= (24g/35) integral z^2/sqrt(C) dP(t),
z^2/sqrt(C) >= g^2 eta^2/(g^2+eta^2+t)^(5/2),
-q >= (16 eta^2/35) integral [T g^3/r] F''(g^2+eta^2) d(log r),
F''(h^2)=(3h+10)/[4 h^(9/2)(h+4)^(3/2)].
```

For all widths 0<=epsilon<=E, one can replace g^3 by g_E^3, T by T_E,
and F''(g^2+eta^2) by F''(r^-4+eta^2), because F'' is decreasing.
This is an analytic uniform lower bound, but its numerical integral is only
about 0.00859 for canonical E=.32 and 0.00201 for alternate E=.47. The cuts
in q are about .044 and .033. The bound is too weak; do not promote it to
closure. The numerical evaluations are supplementary, not certified integrals.

Rejected shortcuts: c is not always negative (eta=2.05,g=5 gives c>0);
negative sign does not imply monotonicity in epsilon; finite sampling of the
positive formula cannot exclude a narrow magnitude dip. The next cheapest
old-model closure step would enclose the exact positive mixture kernel on a
finite radial patch, retaining the Gaussian L term, and discard the remaining
negative contributions. This was not completed before the newly authorized
response-law search took priority.

## Implication for a new response law

Every nonzero finite positive softened-Coulomb mixture has h A(h) increasing
to its total mass. It cannot have A(h)=o(1/h) at high field, and cannot make
signed Cassini cancellations under the stated radial/kernel hypotheses.
These restrictions do not rule out a sharper high-field transition outside
the mixture class, or a sufficiently small magnitude within it. They are
structural constraints, not an exclusion of all action-consistent responses.

## Reproducibility and review scope

`check_sign.py` checks the independent scalar mixture identity, exact-kernel
angular coefficients, and total-kernel signs over the declared finite grid,
plus reproduces the unsuccessful coarse magnitude bound. Its bounded run
contract and manifest distinguish floating verification from the analytic
argument. Original inputs remain read-only. No novelty claim is made.

Self-proofreading covered this new file and formulas; no mathematical-token
corrections to pre-existing artifacts were made. Independent review of the
new contour/mixture and sign argument remains outstanding.
