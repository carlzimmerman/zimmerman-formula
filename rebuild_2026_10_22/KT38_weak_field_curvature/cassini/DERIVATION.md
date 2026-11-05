# Cassini reduction for the weak-field curvature variant

This is a new phenomenological choice within the generalized-action framework,
not Milgrom's equation 16 itself and not a claim of fundamental novelty. The
function Q, Q(0)=0, and frozen Solar constants are unchanged. The new invariants
in Solar rM/a0 units are

```
x=g.g, s=lambda^2 H:H, z=x+s^2, P=xQ(z)/z,
C=R-1+xR', beta=2lambda^2 s,
A=Cg, B=DH, D=beta xR', R=Q/z.
```

Both contributions S_ph=div A-double_div B are retained. No Gaussian field
filter is introduced; a Gaussian source only tests the point-source limit.

## Radial derivatives and Green kernels

For g=g0(r)n+eta e_z and H=gp nn+gt(I-nn), set
s=lambda^2(gp^2+2gt^2). Its first two radial derivatives follow directly
from gp=g0' and gt=g0/r. Then

```
z'=x'+2ss', z''=x''+2(s')^2+2ss'',
beta'=2lambda^2s', beta''=2lambda^2s''.
```

Define E=xR'. Full product differentiation gives

```
D=beta E,
D'=beta' E+beta[x'R'+xR''z'],
D''=beta''E+2beta'[x'R'+xR''z']
     +beta[x''R'+2x'R''z'+xR'''(z')^2+xR''z''].
```

Omitting either beta derivative would change the differential source.
The coefficient derivative C'=R'x'+(R'+xR'')z' is unchanged in form.

All geometric Green and differential-density identities from KT37 remain
valid after substituting these actual coefficients:

```
a=integral (3mu^2-1) C(g0+eta mu) dmu,
b=integral C[eta(3mu-5mu^3)+g0(1-3mu^2)] dmu,
d=integral (3mu^2-1) D dmu,
q_A=(3/2) integral b/r d(log r),
q_B=6 integral (gp-gt)d/r^2 d(log r).
```

For a point field gp=-2r^-3 and gt=r^-3, q_B=-18 integral d/r^5 d(log r).
The differential-density calculation independently forms the angular modes
of div A and double_div B using a',d',d'', including all new beta derivatives.
Outer surfaces and analytic finite-core contacts are retained.

The point grid can reach z about 1e143. To avoid artificial overflow in z^3
while its reciprocal is physically tiny, the implementation uses

```
d1=zR', d2=z^2R''=zQ''-2d1,
d3=z^3R'''=z^2Q'''-3zQ''+6d1,
f=x/z, u=z'/z, v=z''/z.
```

Then E=f d1, E'=(x'/z)d1+f d2u, and
E''=(x''/z)d1+2(x'/z)d2u+f d3u^2+f d2v. The algebra is identical;
no high-field cutoff or physical floor is used.

## Finite-core contacts

For a smooth radial core g0=kr+O(r^3), H=kI at the origin. Put
s0=3lambda^2k^2 and z0=eta^2+s0^2. Derivatives with respect to x hold H fixed,
so beta is also fixed. The geometric contact formulas are unchanged:

```
q_A,contact=8k eta^2 C_x/15,
C_x=2R'+xR'',
q_B,contact=-(8/3)k^3 eta^2 D_xx,
D_xx=2lambda^2s0(2R''+xR''').
```

The point field is defined through the shrinking regular Gaussian source,
not by squaring a distributional Hessian. For a Gaussian k proportional to
sigma^-3, z0 grows as lambda^4 sigma^-12. The simple-Q derivatives therefore
give both contacts O(eta^2 sigma^15/lambda^6), tending to zero.

## Uniform Gaussian-limit extension

The KT37 Rodrigues argument gives the same angular estimates
|b|<=C[eta^2g^3|C_xx|+eta^4g^3|C_xxx|] and
|d|<=C eta^2g^2|D_xx|. At large z,

```
|C_xx|<=Cz^-5/2, |C_xxx|<=Cz^-7/2,
|D_xx|<=C beta z^-5/2<=C lambda^2 z^-2.
```

The last inequality uses s<=sqrt(z). Also
z>=s^2>=4lambda^4g^4/r^4. With the Gaussian radial field
g=sigma^-2 f(r/sigma), f(v)~cv/3 at zero and f(v)~v^-2 at infinity,
the resulting uniform core bounds for every sigma<=delta are

```
|q_A(core)| <= C[eta^2delta^23/lambda^10
                 +eta^4delta^35/lambda^14],
|q_B(core)| <= C eta^2delta^15/lambda^6.
```

Explicitly, the rescaled integrands are v^9/f^7, v^13/f^11, and
v^6|f'-f/v|/f^6. All are O(v^2) at zero and have growth v^23, v^35,
and v^15 at infinity, respectively; integration against d(log v) gives
the displayed powers. As in KT37, Gaussian mean-density monotonicity gives
a uniform high-z core for fixed positive lambda and small delta.

Away from the origin the Gaussian fields converge to the point field.
For eta>0, the large-radius coefficient derivatives stay bounded; the A
integrand is O(r^-7) and the new B integrand is O(r^-15), because beta
is now O(r^-6). Dominated convergence outside a fixed core, the uniform
core bounds, and the vanishing contacts establish the Gaussian STF limit
for each fixed eta>0,lambda>0. This does not claim regulator independence
or a simultaneous lambda-to-zero limit.

## Prespecified numerical checks

Test physical lengths .3,1,3,5,10 kpc on both fixed footings, with base
8000x160 and refined 16000x320 radial/angular nodes and expanded domain.
Check ell=0 against the exact same-node KT33 QUMOND result, the finite-core
ell=0 contact, Q=z giving exactly zero, and eta=0 giving zero STF.
Check Gaussian source widths .5,.1,.01,.001,5e-7 rM at .3 kpc. Use the
previously resolved rmin=max(1e-10,.001sigma), retaining the analytic origin
contacts. Repeat broad cores at half and quarter of that inner radius.
Require relative flux-density/refinement errors<2e-4, and absolute
broad-core inner-radius changes<1e-10 q, without relaxing gates after a run.

These are finite constant-external-field quadrupole tests. They do not by
themselves validate a Galactic-gradient embedding, ephemeris likelihood,
Milky Way implementation, dwarf population, or dynamical health.
