# Generalized action: exact variation and numerical conventions

This is Milgrom's existing Eq. (16), specialized to the inherited simple nu;
it is not a new action architecture. The primary source is
[2305.01589v2](https://arxiv.org/html/2305.01589v2), dated 4 October 2023,
Eqs. (6), (14), (16), and Section III.1.1, authenticated 4 November 2026.
The source supplies the action framework; the formulas and implementation
below are derived directly for the specified Q. No source result supplies an
observational pass or complete dynamical/relativistic health.

## Definition and units

Let g=grad psi, H=Hess psi, a0>0 and ell>=0. The Cartesian tensor contraction
H:H=sum_ij H_ij^2 includes both off-diagonal entries. Define

    x=|g|^2/a0^2, z=(|g|^2+ell^2 H:H)/a0^2,
    Q(0)=0, Q'(z)=nu_simple(sqrt(z)),
    nu_simple(y)=1/2+sqrt(1/4+1/y),
    R(z)=Q(z)/z, P=x R(z), E=a0^2 P=|g|^2 R(z).

The static action, including the usual minimally coupled matter potential, is

    I=int {-rho Phi-[2 grad Phi.grad psi-E(g,H)]/(8 pi G)} d^3x.

The symbol P is dimensionless; E is dimensional. Thus A=.5 E_g-g and
B=.5 E_H. Writing .5 P_g instead without a0^2 would lose a dimensional
factor. The API returns the dimensional E and its physical A,B.

g and a0 have acceleration units, H acceleration/length, ell length,
E acceleration squared, A acceleration, and B acceleration times length.
All terms in div A-double_div B have inverse-time-squared units. In a code
using g/a0 and a dimensionless radius, ell must be converted by the same
radius unit. A physical ell=.1 kpc is not .1 in Solar r_M units.

This model has one new common physical length ell, not an object mass or
epsilon-dependent Gaussian width. The proposed .03,.1,.3,1 kpc values are
test inputs, not a derived scale. Both original a0 footings remain separate.

## Full variation

Varying Phi gives Delta psi=4 pi G rho. Let R'=dR/dz. Direct differentiation
of E with all dependencies retained gives

    .5 E_g = [R+xR'] g,
    .5 E_H = ell^2 x R' H,
    A = [R+xR'-1]g, B=ell^2 xR'H.

Varying psi and integrating once/twice by parts gives

    Delta Phi = div([R+xR']g)-partial_i partial_j B_ij,
    Delta(Phi-psi) = div A-partial_i partial_j B_ij.

The Hessian term has a minus sign in the source. It is of the same variational
status as the gradient term; it cannot be omitted and then interpreted as
the field equation of this action. In particular, this is not KT26–32's
substitution of a tidal width into a pre-existing smoothed-source equation.

For compactly supported test function v, the phantom source has weak form

    int v S_ph = -int grad(v).A-int Hess(v):B.

Thus a consistent finite source on cell volume matrix W is

    S_ph,h=-W^-1 G_h^T W A-W^-1 H_h^T W B.

The complete discrete Hessian, its component convention, metric factors,
parity and boundary contributions must all enter H_h and its transpose.
Symmetrizing a continuum tensor after taking unrelated grid derivatives
does not automatically produce the derivative of the chosen finite energy.

## Boundary terms and matter coupling

For a smooth bounded region, the boundary part of delta int E is

    int_boundary n_i[(E_gi-partial_j E_Hij) delta psi
                     +E_Hij partial_j(delta psi)] dS.

This formula uses symmetric H and B. It vanishes for compactly supported
variations or suitable boundary data, for example fixing psi and its normal
derivative while its tangential variation also vanishes. A finite energy
method must retain its actual boundary terms and test moving the boundary;
one must not assume ordinary Poisson boundary treatment removes all Hessian
terms. The first Poisson solve still fixes psi from rho, so extra arbitrary
physical data cannot be freely assigned to psi just to improve a fit.

The translation-invariant static functional gives reciprocal source variation
when the Green operator, derivatives and boundary realization are paired
consistently. This does not prove full relativistic matter conservation,
causality, stable propagating degrees of freedom or a dynamical completion.

## Primitive and stable evaluation

Put u=z^(1/4), y=sqrt(z)=u^2. Integrating Q' with Q(0)=0 gives

    Q(z)=z/2 + u(u^2+2)sqrt(u^2+4)/2 - 4 asinh(u/2).

The two last terms cancel to low order at small u. The small-u series is

    Q=4u^3/3+u^4/2+u^5/10-u^7/224+u^9/2304
      -5u^11/90112+7u^13/851968-7u^15/5242880+... .

In `law.py`, the series is evaluated for u<.25, through eight corrections
after the leading term. Its coefficients follow the binomial series of
sqrt(1+u^2/4), integrated term by term. For larger u, use

    d=sqrt(1+4/y)-1=4/[y(sqrt(1+4/y)+1)],
    R-1=d/2+1/y+d/y-4 asinh(u/2)/z,
    D=z R'=Q'-R=d/2-(R-1).

The rationalized d and R-1 retain the small phantom response at high z.
The stable physical coefficients use f=x/z:

    A=[R-1+f D]g, B=ell^2 f D H.

This avoids forming the potentially overflowing R' before multiplying by x.
The code also exposes Q'', R'', computed from

    Q''=-1/[2u^5 sqrt(u^2+4)], R''=(Q''-2R')/z.

The integration constant is essential. Replacing Q by Q+C changes P by
C x/z, which is not a constant in this generalized action and changes the
field equations. Q(0)=0 is part of the model, not a numerical convenience.

## Limits and regularity

- Newtonian mutation Q(z)=z: R=1,R'=0, so A=B=0 exactly.
- ell=0: z=x and R+xR'=Q', hence A=(nu(|g|/a0)-1)g and B=0, exactly
  ordinary simple-nu QUMOND with the same unfiltered Newtonian source.
- H=0 with g nonzero also gives the QUMOND constitutive response. A constant
  field produces no local source, although its addition to a varying field
  changes this nonlinear response. Uniform external-field blindness is not
  asserted.
- z large: R=1+2/sqrt(z)+O(log(z)/z), D=-1/sqrt(z)+O(log(z)/z), so the
  constitutive corrections vanish relatively. A pointwise small correction
  does not alone bound a rapidly varying double divergence.
- z small: Q~(4/3)z^(3/4), E~(4/3)|g|^2 z^(-1/4). Under simultaneous
  scaling (g,ell H)->lambda(g,ell H), this energy is O(lambda^(3/2)),
  and its first derivatives are O(lambda^(1/2)). Thus E,A,B extend
  continuously by zero at joint zero field and Hessian. Bare R and R'
  diverge, and second derivatives need not remain bounded; this is not a
  uniform ellipticity or smooth-Hessian theorem.

At a nondegenerate saddle g=0,H!=0, z>0 for ell>0. Although A=B=0 at the
point, their derivatives need not vanish. In the local quadratic potential
with constant H, the exact source at the saddle is

    S_ph(0)=(R(z0)-1)tr H-(2ell^2/a0^2)R'(z0)tr(H^3),
    z0=ell^2 tr(H^2)/a0^2.

This can be nonzero even for a vacuum saddle tr H=0. Setting the entire
source to zero wherever g=0 would therefore be a different and incorrect
implementation. No positive z floor is introduced: such a floor would be a
new parameter and require a changed action or an explicit limiting study.

The original exponential/sech-squared disc profiles can have midplane density
kinks. H contains density information; subsequent source derivatives may
create distributions or thin layers at derivative discontinuities. A weak
energy implementation can represent their integrated effect, but pointwise
finite differences can create grid-sensitive peaks. Changing baryon smoothing
to remove them would violate the frozen-baryon comparison unless separately
authorized and explicitly treated as a new diagnostic.

## Spherical sources

For a smooth spherical Newtonian gradient g(r), put a=g', b=g/r. Then

    H=a nn+b(I-nn), H:H=a^2+2b^2,
    A_r=[R-1+xR']g,
    B_r=ell^2 xR' a, B_t=ell^2 xR' b.

Regular-center radial integration gives

    g_ph=A_r-B_r'-2(B_r-B_t)/r.

Any central integration constant is fixed by the actual source and boundary
problem, not fitted; a point source requires its own origin limit. For a
uniform-density central core g=k r, H=k I, define z0=3ell^2 k^2/a0^2.
The leading total gradient is

    g_total=k r [R(z0)-(2/3)z0 R'(z0)]+O(r^3).

Thus at fixed nonzero ell and k the central response is harmonic, with a
finite density-dependent multiplier. It is not the same central behavior as
the ell=0 QUMOND limit; the r->0 and ell->0 limits need not commute.

Outside a bounded spherical mass, H:H=6g^2/r^2. For r>>ell, the Hessian
term is small and the asymptotic deep-MOND gradient approaches
sqrt(G M a0)/r with the original a0 normalization. For a point source at
r->0 with fixed ell>0, direct expansion of both response terms gives

    g_ph = a0 r/(3 sqrt(6) ell)+o(r).

Dropping B gives a different leading coefficient, illustrating why the full
variation matters even where both corrections look individually small.
