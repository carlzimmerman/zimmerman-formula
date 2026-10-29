# Independent PN28-GRAD computation and interpretation audit

Reviewer `/root/theory_audit`, 2026-10-28. Requested base
`66c45c5082f651dd54e171f98c11acd9cb3d9086`; recorded run and observed review
HEAD `7954d48377463cafcae3e8dbb09454134aef384f`, with a dirty shared workspace.
Only this review is written. The computation-audit workflow is applied to
the existing evidence; the BVP experiment has not been rerun by this reviewer.

**Outcome: implementation and finite assertion audited, conditional on
floating-point tolerance and the external solver.** The six reported
solutions and two repeats support numerical stationary waterbags of the
declared static system. They do not establish exact infinite-domain
solutions, general existence, uniqueness, stability, vacuum-crossing
dynamics or vacuum-normalized pressure selection. One recorded central
curvature comparison does not meet the apparent solver tolerance and is
not an asserted check; it must not be described as independently passed.

## Frozen evidence

All paths in the following table are under
`pressure_selection_2026_10_28/` unless an absolute path is stated.

| Artifact | SHA256 |
|---|---|
| `finite_gradient/check_gradient.py` | `1f5cb1020eda2238f65a624a8eebac8a77ec2fb07f22fdfec9bd2dca8c562652` |
| `finite_gradient/contract.json` | `916b5d77bb02dfacbd5b75c4bda2e6ecaf503f3d6aa38fa5f3bbcc8594260d42` |
| `finite_gradient/run/manifest.json` | `6fe558e44b2eddf1d85d6329d9d4125e9986c00eacc8eccdc50dea3a460301b7` |
| `finite_gradient/run/result.json` | `239525486ad8bdc0484e9b47f9d54a111efc0487085ba8ae9fb09b6195f35dbf` |
| `finite_gradient/run/profiles.npz` | `58575ef832214690bbea696da306ed3af6998dc24a69ad39bcd66fc0067e9956` |
| `finite_gradient/run/stdout.txt` | `9fe0b4c3069bfe7445098fa1483a594664594121608da6f260a9a3de2d3aa262` |
| `finite_gradient/run/stderr.txt` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `finite_gradient/INPUT_PROVENANCE.json` (initial review) | `40bc14fae27cc2591021ffc2e8fb172b76a91390e0f765c3f332d21db1f8c5da` |
| `finite_gradient/INPUT_PROVENANCE.json` (reconciled) | `aa5399683446ad373ff68049b64c57f597a919916b171530ad34b12e0a8d5a87` |
| `finite_gradient/DERIVATION.md` (reconciled) | `8b6d501f0ddfa522c5a9cafe6c90592a007bb5b80575bbbf0d302d0135b0d970` |
| `finite_gradient/SOURCE_REVISION_DIFF.patch` | `8011b439471bd428d03fb247e625a3c6e339c02d5fd49125d80e54dbb7603e09` |
| `dispersion_coupling/STATIC_WATERBAG.md` | `0991516ad7331710c7d00fbfa5e1b198b70cab3220d94f949f4c1dc281760812` |
| `dispersion_coupling/EOS.md` | `05f919345cb73c8b96e3f07d5fdb421ae8ee1d24a01e177abc9551aab4092274` |
| `halo/DERIVATION.md` | `aa79f50d4b78ce204a805f4962e53b87778ed7a17d8ec5e30a7be3bea529991a` |

The manifest records execution of
`python3 pressure_selection_2026_10_28/finite_gradient/check_gradient.py pressure_selection_2026_10_28/finite_gradient/run/result.json`,
with Python 3.9.6, NumPy 1.26.2, SciPy 1.11.4, one requested thread,
180-second wall and 150-second CPU limits. It records status `completed`,
exit 0, elapsed 0.619692 seconds, empty stderr, and unchanged execution
inputs. I ran the installed manifest validator with `--root` set to this
repository; it returned a valid completed evidence record. Result, log and
profile hashes agree with that record.

The design provenance pins an earlier action-report version
`c4046a7d...`; the run manifest correctly pins the actual later input
`6deea173491b9c8e4d88b528ac0895faf2c6ec99273aa86c9d6e73d7c7d8537d`.
Those versions and their static/exterior qualification were already checked
in REVIEW_EOS_HALO.md. The design pin is not the execution pin. The new
STATIC_WATERBAG.md is independently pinned above as the mathematical object
used for this audit; it was not an input read by the computation script.

## Reconstructed mathematical object

Take the specified canonical energy waterbag with positive fixed phase
level, zero mean current and scalar momentum, and the explicit zero-mean
static exterior continuation. With
`psi=(mu-Phi)/h_*`, `h_*=5B/(2rho_*)`,
`ell^2=5B/(8pi G rho_*^2)`, and
`epsilon=C_s/(3B ell^2)`, direct momentum integration and scalar variation
give

    n=rho/rho_*=exp(3s) psi_+^(3/2),
    Delta psi=-n,
    epsilon Delta s=exp(3s)[1-psi_+^(5/2)]-1.

These are exactly the equations in `rhs`, including the signs and the
positive-part treatment beyond the matter edge. The supplied Jacobian
matches their partial derivatives. For the tested psi_c<1, the local
reference function and guess remain below its pole at psi=1.

In this model `f=f_* 1_(p^2/(2Z)+Phi<mu)` is a stationary solution of the
canonical Vlasov equation whenever these static fields solve their
equations: the distributional Poisson bracket of a function of the
Hamiltonian with that Hamiltonian is zero. The numerical field evidence
therefore supports a numerical stationary kinetic state, not merely an
arbitrary isotropic fluid profile. It remains a selected waterbag, with the
stated static vacuum continuation and approximate field solution.

## Center, outer boundary and gravity gauge

The state is `(psi,psi',s,s')`. The nonsingular `rhs` plus
`S=diag(0,-2,0,-2)` supplies the two spherical `-2 derivative/r` terms.
The four boundary conditions fix psi_c, both central first derivatives,
and the outer scalar relation. They are consistent with the necessary
center condition `S y(0)=0`.

I inspected the installed SciPy `_bvp.py` implementation at
`/Users/carlzimmerman/Library/Python/3.9/lib/python/site-packages/scipy/integrate/_bvp.py`,
SHA256 `d074e8018d6ec39589e2f939a042e0de86ebe9cfe4e20703fdd6e6173d126a4c`.
It projects the initial state onto the singular constraint and applies
`(I-S)^+` to the regular RHS at the center. Thus the factors 1/3 in
`psi''(0)=-n_c/3` and
`s''(0)=[exp(3s_c)(1-psi_c^(5/2))-1]/(3epsilon)` are handled by the
solver, rather than evaluating a literal division by zero.

Outside the first matter zero R, the code continues the nonlinear vacuum
scalar equation and harmonic gravity to L. It does not terminate the
scalar at R. Linearizing the scalar equation around s=0 gives inverse
length `kappa=sqrt(3/epsilon)`, with decaying spherical mode
`s=A exp(-kappa r)/r`. Hence the imposed condition

    s'(L)+(kappa+1/L)s(L)=0

is the correct linear exterior Robin condition. It is an approximation to
the nonlinear infinite-domain condition. All actual `|s(L)|` are at most
`1.3226e-11`, making the local nonlinear correction to `3s` tiny. That
smallness alone is not a bound on the interior error of a possibly
sensitive boundary problem. The two joint larger-domain/tighter-tolerance
repeats supply empirical control for their tested states.

No separate gravity value condition is missing: psi_c and regular gravity
determine the enclosed mass and the asymptotic constant. In the exterior
`psi=mu/h_*+m/r`, so the computed
`mu/h_*=psi(L)-m(R)/L` implements `Phi(infinity)=0`. All six values are
negative, consistent with a bound finite-support energy cutoff. Mass is
not a supplied boundary datum in these runs.

## Independently reconstructed stress, mass and virial diagnostics

Define `a=exp(3s)psi_+^(5/2)` and
`u=exp(3s)-3s-1`. Relative to the constant exterior vacuum pressure, the
dimensionless radial and tangential stresses are

    p_r=a-u+(3/2)epsilon s'^2,
    p_t=a-u-(3/2)epsilon s'^2.

The scalar and kinetic forces cancel in their sum, giving

    p_r'+2(p_r-p_t)/r=(5/2)n psi'.

This verifies the numerical force-check coefficient and sign. The code
differentiates the assembled stress by a five-point finite difference,
rather than merely substituting the solver RHS into the identity. It is
an orthogonal consistency check using the same interpolated solution,
not an independent BVP solver or a rigorous pointwise error bound.

The mass equation gives the two correct estimates

    m(R)=-R^2 psi'(R)=integral_0^R r^2 n dr.

In units of `4pi B ell^3`, set

    E_rel=(3/2) integral r^2 a dr,
    U_ex=integral r^2 u dr,
    E_grad=(3/2)epsilon integral r^2 s'^2 dr,
    W=(5/2) integral_0^R r^3 n psi' dr <0.

Multiplication of radial force balance by r^3 and integration gives

    2E_rel-3U_ex-E_grad+W-L^3 p_r(L)=0.

The script includes precisely this boundary term and the negative scalar
gradient contribution. Its second gravitational-energy expression is
also correct:

    W=(5/4) integral_0^R r^2 n [mu/h_*-psi(r)] dr.

Finally, the integrated scalar identity is
`epsilon L^2 s'(L)=integral_0^L r^2[exp(3s)(1-psi_+^(5/2))-1] dr`.
All normalizations agree. Quadrature is of the numerical interpolant;
its internal error estimates are not retained, and very small invariant
residuals should not be reported as equally small field-error bounds.

## Actual coverage and finite results

The executed iterator is exactly the Cartesian product
`psi_c in {0.8,0.95,0.99}` and `epsilon in {1e-4,1e-2}`. All six result
rows have solver status 0. The two repeat rows are precisely
`(psi_c,epsilon)=(0.99,1e-4)` and `(0.99,1e-2)`, also status 0. There
is no wider parameter scan or case reduction theorem.

The column reported by the code is
`C=sqrt(5/2)n_c r_(1/4)`, so that
`rho_c R_(1/4)=C sqrt(B/(4pi G))`. Its comparison with the local solution
is at fixed central psi, not at fixed central density or fixed total mass.

| psi_c | epsilon | central density change | column change |
|---|---:|---:|---:|
| 0.80 | 1e-4 | -0.02331% | -0.006029% |
| 0.80 | 1e-2 | -2.11445% | -0.54653% |
| 0.95 | 1e-4 | -0.48417% | -0.013770% |
| 0.95 | 1e-2 | -22.55137% | -0.89389% |
| 0.99 | 1e-4 | -9.52285% | +0.50727% |
| 0.99 | 1e-2 | -69.96106% | +1.75108% |

The largest recorded normalized collocation RMS residual is `9.9507e-7`.
Across all eight solutions, the largest mass quadrature relative mismatch
is `7.894e-9`, scalar integrated scaled mismatch `3.635e-11`, sampled
radial-force scaled mismatch `7.439e-8`, virial scaled mismatch
`4.326e-12`, and gravitational-energy relative mismatch `4.089e-9`.
All satisfy their declared thresholds. The maximum relative change among
radius, mass, central density and column in either repeat is `6.818e-9`.
The domain and tolerance are changed together, so their separate error
contributions are not isolated. Only these two states have this repeat.

The baseline runs save 1600-point profiles for all six cases. The repeats
save summary rows but not full repeat profiles. No reported baseline case
was dropped or replaced in the result artifact.

## Numerical qualification requiring explicit wording

The script records both `3*sol.sol(0,2)[2]` and the scalar-equation value
of the center Laplacian. This comparison is not included in `checks`.
Its largest relative discrepancy is `2.04478e-4` at `(0.8,0.01)`.
At `(0.99,0.01)` the discrepancy is `1.27608e-4` and remains essentially
unchanged in the tighter/longer-domain repeat. Thus the output does not
show that the stored spline second derivative satisfies the center
equation to `1e-6` or `2e-7` relative accuracy.

The first mesh spacing is extremely small and the solver uses a cubic
interpolant for each state component; cancellation in the second
derivative of the s component is a plausible explanation. It has not
been established by this read-only audit and should not be asserted as
a demonstrated diagnosis. A derivative of the s' state, or a resolved
small-radius expansion, would be a more relevant targeted diagnostic;
the endpoint derivative imposed by the solver itself would not be an
independent check.

This discrepancy does not contradict the reported ten asserted case
checks, and it does not on its own defeat the numerical interior-state
evidence. It limits a stronger claim of verified center curvature.
Likewise the monotonicity tests are finite sampling with tolerances,
and the radial-force residual uses a global scale floor of 1 rather than
pointwise relative error. Neither is a uniform analytical certificate.

## Interpretation

The finite evidence supports the survival of the constructed pressure
mechanism in these six static finite-gradient numerical waterbags, under
the declared rest-frame exterior continuation and Newtonian assumptions.
The small column changes coexist with much larger central-density
changes, so they should not be summarized as uniformly small changes to
the full density profile. The signs of column changes also vary across
the sampled states.

No general infinite-domain existence or uniqueness theorem, isotropization
or formation result, gravitational/kinetic stability result, covariant
completion or arbitrary vacuum-crossing Hamiltonian has been established.
Rest-mass dominance and negligible cosmological force remain separate
physical scale conditions. Existence evidence is numerical and restricted
to the stated cases and boundary prescription. The separate analytic
lemma below proves finiteness conditional on an existing regular decaying
branch.

V is absent from these excess-energy static equations. Changing the
constant vacuum energy at fixed B, phase level and gradient coefficient
does not change any computed profile. The computation therefore cannot
select B/V, even if its numerical field solutions were exact.

## Author derivation and new conditional finite-radius lemma

I subsequently read `finite_gradient/DERIVATION.md`, SHA256
`6bdc1c3012c16b1c9154e1e225b55138133bc7c1ff474ec3c95ceca1b11f0cff`.
Its equations, numerical table, fixed-psi comparison, and explicit
unverified-center-curvature qualification agree with the audit above.
Its input table is a design snapshot rather than the later run's action
report hash; the distinction was communicated to the coordinator for
clarification. The run manifest remains the execution provenance.

Its new finite-radius assertion is conditional on an existing globally
regular spherical solution with `psi_c in (0,1)` and `s(infinity)=0`.
Here is an independent proof of the needed implications.

First, Poisson gives `psi'=-m/r^2<=0`, and therefore
`0<=psi_+<=psi_c<1`. At any negative scalar minimum,
`exp(3s)(1-psi_+^(5/2))-1<0`, contrary to the nonnegative Laplacian.
At a scalar maximum greater than
`s_max=-ln(1-psi_c^(5/2))/3`, the scalar RHS is positive, contrary to
the nonpositive Laplacian. The limit s=0 at infinity and regularity at
the radial center justify taking these extrema. Consequently

    0<=s<=s_max,
    n<=exp(3s_max)psi_c^(3/2),
    n>=psi^(3/2) wherever psi>0.

The last inequality is sufficient for the mass estimate; monotonicity of
s or density is not needed for this proof. If matter occupied every
radius, the nonincreasing positive psi would have limit zero (a positive
limit forces cubic mass growth and a zero of psi). It would follow that

    psi(r)>=m(r)/r,
    m(r)>=r^3 psi(r)^(3/2)/3,
    psi(r)<=9/r^4,
    psi(r)>=m(r0)/r for each fixed r0>0.

This is the same incompatible pair of asymptotic bounds as in the
auxiliary theorem. The finite first matter zero R follows. Bounded
density gives finite enclosed mass; `psi'(R)<0` and finite s(R) give
the stated `(R-r)^(3/2)` density edge.

The finite exterior scalar energy can also be justified without assuming
an exact linear tail at finite R. Set `kappa=sqrt(3/epsilon)` and
`q(s)=exp(3s)-1`. In the exterior, `q(s)>=3s`. The comparison function

    w(r)=s(R) R exp[-kappa(r-R)]/r

has the same boundary value at R and satisfies
`(Delta-kappa^2)w=0`. Since
`(Delta-kappa^2)s=[q(s)-3s]/epsilon>=0`, the maximum principle gives
`0<=s(r)<=w(r)`. This supplies an exponential upper bound. Unless the
tail vanishes identically, `s'<0` there: a nonnegative derivative would
make `r^2 s'` subsequently increase, preventing decay to zero. The
increasing quantity `r^2 s'` has limit zero; a negative limiting value
would force a 1/r lower tail, contradicting the exponential bound.
Integration of the scalar equation then gives

    -epsilon r^2 s'(r)=integral_r^infinity t^2 q(s(t)) dt.

On the bounded scalar range, `q(s)<=C s`. The exponential bound on s
therefore bounds its derivative by the same exponential scale for large
r. Both `integral r^2 s'^2 dr` and the excess potential integral are
finite. This proves the claimed finite-energy consequence for an
existing regular decaying branch; it is not a new existence theorem.

Finally, the formal small-epsilon center correction in the author text
is correctly evaluated at fixed psi_c. At fixed psi, the derivative of
`exp(3s)(1-psi^(5/2))-1` with respect to s is exactly 3 on the
auxiliary branch, while `delta psi_c=0`. Hence
`delta s_c=(epsilon/3)Delta s_0(0)=-(5/18)epsilon n_0^2` at leading
formal order. This is a different constraint from holding K or density
fixed. No uniform expansion through a growing-concentration limit is
established.

## Final provenance reconciliation

After the preceding audit, the author corrected the input table and
metadata, preserving the design snapshot separately. I read the corrected
DERIVATION.md at `8b6d501f0ddfa522c5a9cafe6c90592a007bb5b80575bbbf0d302d0135b0d970`
and INPUT_PROVENANCE.json at
`aa5399683446ad373ff68049b64c57f597a919916b171530ad34b12e0a8d5a87`.
Their actual execution hash now agrees with the unchanged run manifest.
The original derivation hash above remains as review history.

I independently parsed the three added blocks in SOURCE_REVISION_DIFF.patch
and removed them from the current report in memory. The result hashes
exactly to the recorded design source `c4046a7d...`. Removing only the
energy-asymptote block gives the intervening `ddf6da56...` source. Thus
the delta is exactly the two static/domain qualifications plus the added
energy asymptote, with no pre-existing action, EOS, gradient, mode or BVP
equation altered. The asymptote is valid additional algebra:
`n=y-3/5+O(1/y)` implies
`W_min-V=(5B/2)n-B ln n-B+o(1)`.

The source script, contract, manifest and numerical outputs were not
changed by this reconciliation, and no numerical rerun was needed.
The old REVIEW_EOS_HALO.md chronology was also corrected with coordinator
authorization; its current SHA256 is
`2bbf5f6028a63134722eb173ac31b55965913aea9aecc850f25f9577196381af`.
The shared HEAD advanced during review to
`361eb5476c8014fee6ff0775281bb09df55bfb6d`; the exact subject hashes,
rather than that unrelated HEAD movement, identify this audit's scope.
