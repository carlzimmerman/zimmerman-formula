# Independent audit of the six-gradient action and orbital sum rule

Primary verdict: **correct only after retaining the stated restrictions**.
No concrete algebraic error was found in the six-gradient Hessian, spherical
source inversion, normalization, compact bump construction, or orbital
integral. The result does not establish C=32pi, covariant health, or a measured
orbital bound. This is a separate subagent reconstruction, not a proof based
on agreement or the original script's check count.

Reviewed source hashes:

- `puzzle_32pi/breakthrough_2026_10_05/REPORT.md`:
  `c98adf3a605c42f20a8d42aacc2fd78203e8e96e1fa0c1f9c83434407191df1b`.
- `puzzle_32pi/breakthrough_2026_10_05/checks.py`:
  `584f3a9bcea8d7f717af082e46e898643647aae4245661c79e5fe6d2c49410a2`.

Both paths are relative to `sol61_push/`. These exact revisions are the audit
objects; later edits require checking the changed implications. No puzzle
files were edited or executions invoked that could write puzzle outputs.

## Claim card and dependencies

Fix positive a0,G, the static NR two-potential energy

    W(p,q)=|p|²+|q|²-a0² M(|p-q|²/a0²),

and L=-W/(8piG)-rho phi with no twin source. The response is nu=1+e>1,
with x=y(1+2e), z=x², m=M'(z)=e/(1+2e). Hypotheses for a global response
dictionary are differentiability, D=x'>0, x(0)=0, x(infinity)=infinity, and
the required convergent primitive/tail. The concrete cutoff kernels satisfy
these. The vacuum interpretation additionally assumes M(infinity)=0,
the stated symmetric proportional/identical-metric vacuum dictionary, and no
independent vacuum contribution.

The dependency graph is:

    independent variation -> source flux -> x,m dictionary
    independent six-variable differentiation -> Hessian
    D positivity + endpoint asymptotics -> global action primitive
    primitive boundary identity + vacuum convention -> C integral
    isolated exterior central force -> orbital ratio
    integration by parts + endpoint limits -> orbital integral
    monotone response -> finite-window lower bound.

Covariant dynamics and empirical spherical inference are separate unproved
leaves, not inputs supplied by NR convexity.

## 1. Full Hessian reconstruction

Put d=p-q, z=|d|²/a0² and

    A=2m I+4 M'' d d^T/a0².

Directly differentiating all six components, before any auxiliary elimination,
gives

    Hess W = [[2I-A, A], [A, 2I-A]].

Thus a common perturbation (h,h) has eigenvalue 2. A difference perturbation
(h,-h) has matrix 2I-2A. Splitting h parallel/perpendicular to d yields

    lambda_common=2                (multiplicity 3),
    lambda_transverse=2(1-2m)      (multiplicity 2),
    lambda_radial=2(1-2m-4zM'')    (multiplicity 1).

An independent Sympy differentiation of W produced radial pp entry
2-2m-4zM'', radial pq entry 2m+4zM'', transverse pp 2-2m and transverse pq
2m. Rotational covariance gives the displayed arbitrary-direction matrix;
this is a reconstruction from W, not acceptance of a reported eigenvalue list.

From y=x(1-2m), differentiating with respect to x gives

    dy/dx=1-2m-4zM''=1/D.

Also 1-2m=1/(1+2e). Consequently all six eigenvalues are positive at nonzero
d for these kernels. The zero-difference limit is not uniformly elliptic:
for e~y^-1/2, x~2sqrt(y), all three difference eigenvalues vanish.

The strict-convexity conclusion survives that isolated degeneracy. In rotated
variables u=(p+q)/sqrt2, v=(p-q)/sqrt2, the difference radial energy H(|v|)
has H'(s)=2s(1-2m)>0 for s>0 and H''(s)=2/D>0 there, with H'(0)=0.
This makes H(|v|) strictly convex, and |u|² supplies the common block. For
the concrete deep law the difference energy above its constant is
a0²x³/12+o(x³), a positive cubic. These are static facts, not a Lorentzian
kinetic or constraint-spectrum result.

## 2. Source inversion and normalization

Independent variation yields

    div[p-m(p-q)]=4piG rho,
    div[q+m(p-q)]=0.

Under isolated spherical matching conditions, the twin flux vanishes, so
q=-m d, p=(1-m)d and g_N/a0=(1-2m)x. Hence the stated nu source map is
correct. This restriction excludes curl fields, twin sources and differing
boundary fluxes; it is not a general algebraic map for arbitrary geometry.

Direct substitution gives

    m dz = 2y e D dy,
    m dz-2y e dy=d(2y²e²).

I independently expanded the latter symbolic expression; its residual is
exactly zero. Deep e~y^-1/2 gives y²e²~y at zero. The cutoff UV tail is
e~T²/(2y³), so y²e²~T^4/(4y^4) at infinity. Both endpoint terms vanish and
all required integrals converge. Thus J=2 integral y e dy, M(0)=-J, and
under the chosen vacuum convention C=J/2=integral y e dy.

The bump's integral is exactly

    integral_0^1 (1+t)t³(1-t)³ dt = 3/280.

Its first two derivatives vanish at both endpoints. Thus the coefficient
shift is 3 epsilon Y²/280, while the low-response law and asymptotic tail
remain fixed. The primitive below the bump changes by a constant; the report
correctly acknowledges this rather than claiming an unchanged full action.

The analytic D bound checks out: for y>=1 the negative term is bounded by
1/(2y), and for y<=1 it is bounded by 4/T². Hence T²>=8 gives D>=1/2.
The bump perturbation bound |delta D|<=25|epsilon|/32 is valid, albeit loose.
The reported monotonicity bound legitimately uses a(2Y), 2y>=2Y and the
largest denominator on [Y,2Y]; it is not an invalid minimum of a nonmonotone
product. Excess positivity for the negative bump also follows from the
displayed strict lower bound. The two-sided family therefore exists in this
NR class.

For an additive shift M->M+b, the source law and Hessian do not change but
C->C-b/2. The orbital integral measures C+b/2, not the shifted physical C.
An independent matter vacuum term is another excluded contribution.

External leaf checked directly: [Milgrom, arXiv:0912.0790v2, 25 January
2010](https://arxiv.org/html/0912.0790v2), equations (1)-(2) match the NR action
and flux structure. Equations (24) and (84)-(87), evaluated at identical
metrics with f(1)=1,f'(1)=0 and alpha=beta=1, give the conditional -M(0)/2
vacuum normalization. This authenticates that dictionary; it does not supply
a selector for M(0). No new primary-source cache was written.

## 3. Orbital ratio, endpoints and finite-window bound

For an isolated exterior spherical force g(r)=GM_b nu(y)/r²,
y=GM_b/(a0r²), fix the orbit's specific angular momentum j. The radial
equation is rddot=j²/r³-g(r). At a circular radius j²=r³g and linearizing
gives

    Omega²=g/r, kappa_r²=g'+3g/r,
    R=kappa_r²/Omega²=1-2y nu'/nu.

Independent differentiation reproduced this ratio. Positive monotone nu
gives R>=1, radial stability and retrograde infinitesimal-eccentricity
precession. The stated 2pi(R^-1/2-1) is exact for this linearized radial
oscillation problem, not an exact formula for finite-eccentricity orbits.

With [y²e]_0^infinity=0, integration by parts gives

    integral y e dy = -(1/2) integral y²e' dy
                   = (1/4) integral y nu(R-1) dy.

The origin term is O(y^(3/2)); the UV term is O(1/y). Both vanish for the
cutoff family. This endpoint condition differs from the J-I endpoint
condition and both were checked separately. Monotonicity is necessary for
the finite-window lower bound: the integrand equals -2y²nu'>=0. Without
monotonicity outside the measured interval, omitted negative contributions
could invalidate that bound. Under the stated hypotheses the coefficient
and inequality direction are correct.

Independent 45-digit quadrature, defining the cutoff directly rather than
importing checks.py, gave

    C = 100.530964914878612327371278677246656994078552,
    C-32pi = 5.2286965666904e-12,
    orbital-integral minus C = -1.12e-44,
    compact-bump delta C = 0.01.

These numerical checks corroborate the analytic identities; they are not
their proof.

Two practical scope qualifications should remain visible. A fixed spherical
body of nonzero radius samples exterior y only up to its surface value;
the full 0-to-infinity identity is a response-function sum rule, not the
measured exterior spectrum of that one body. A finite certified interval
within its actual exterior range can still supply the stated bound.
Likewise actual cosmological/relativistic forces, external fields and
multipoles are excluded by the exact NR central-force premises. They cannot
be silently inserted into the idealized orbital formula. The report already
discloses the principal observational restrictions.

## Obligation matrix and surviving conclusion

| Obligation | Verdict |
|---|---|
| Full six-gradient Hessian and source map | Passed under specified NR/spherical source assumptions |
| Global inverse and primitive for the explicit family | Passed analytically |
| Strict static convexity, nonzero-field ellipticity | Passed |
| Uniform ellipticity at zero difference | Failed and explicitly excluded |
| Endpoint and additive convention accounting | Passed |
| Independent action/vacuum source extraction | Passed for the specified source version and symmetric dictionary |
| Orbital factor, precession sign and integration normalization | Passed in the exterior NR infinitesimal-oscillation regime |
| Finite-window inequality | Passed with global monotonicity and sector-only vacuum identification |
| Full covariant health, total physical vacuum and measured bound | Conditional/not established |

The strongest safe statement is a constructive two-sided family of strictly
convex NR static actions with the same low-acceleration response and the same
complete UV tail, but different convention-fixed C, together with a conditional
orbital-response sum rule. No strengthened NR criterion in this package selects
32pi. The smallest remaining implication is a covariant admissibility/selection
mechanism or a certified isolated-spherical partial integral. No mathematical
correction to the audited report is required.
