# TP03 renormalized vacuum master integrals

The requested float API is implemented in `master_integrals.py`:

    I(x,y,z,Q2=1), J(x,Q2=1), J2(x,y,Q2=1),
    fSSS, fSS, fFFS, fbarFFS.

All mass arguments are **squared masses**, Q2 is the squared subtraction
scale, and all loop factors are excluded. J and I return ordinary floats
with bounded LRU caches. `I_mp` and `J_mp` use the active mpmath precision.
Negative/nonfinite masses and nonpositive Q2 are rejected. No negative
physical eigenvalue is clipped or absolute-valued in this API.

The authenticated primary definitions are Martin,
[hep-ph/0111209v2](https://arxiv.org/pdf/hep-ph/0111209v2), §2.3,
Eqs. (2.17)–(2.28), including the specified complex branches. The four
nonvector graph functions use Eqs. (4.12)–(4.15); they are unchanged in
the paper's supersymmetric DRbar-prime scheme. No PDF was downloaded.

The implementation sorts the largest positive mass into z. The square
root R has positive real value or positive imaginary value, and the
dilogarithms use the principal branches. Rationalizing their arguments
avoids subtraction of nearly equal terms. Exact zero-mass branches are
implemented separately; equal positive masses require no singular
continuation. Extreme hierarchies fall back to 60-digit evaluation. A
resolved imaginary residual triggers the high-precision path rather than
being silently discarded.

## Finite validation

`contract.json` preceded execution. `run_001/manifest.json` records a
completed, current-input-validated run with 48 float/mp60 cases and 180
permutation evaluations. Cases include positive, negative and zero
discriminant; either side of a zero discriminant; exact zero/equal masses;
finite hierarchies; scale covariance; explicit subtraction-scale derivatives;
and massless continuity. Maximum normalized float discrepancy is
2.84×10⁻¹⁴, where normalization is max(1,sum of masses,|reference I|).
This is not a uniform relative-error or interval certificate. Permutation
tests confirm API sorting; the source establishes the underlying symmetry.

An additional check is independent of the closed dilogarithm evaluation.
For positive masses, differentiating the convergent Schwinger-parameter
representation three times gives

    ∂x∂y∂z I = −integral_simplex abc/[U²(ax+by+cz)²] da db,
    a+b+c=1, U=ab+bc+ca.

The mixed derivative removes the single-mass UV subtractions. Using
a=u,b=(1−u)v,c=(1−u)(1−v), its real two-dimensional quadrature agrees with
the analytic master derivative at (1,1,1),(1,2,2),(1,2,9) to relative
differences 2.0×10⁻¹⁴ through 6.8×10⁻¹⁴. The quadrature's own error
estimates and actual numerical differences remain in the result file;
they are not rigorous bounds. This tests normalization, sign and the
real/complex discriminant branches through a different representation.

The run took 3.78 s with 61,276,160 bytes observed RSS. Supported
wall/CPU/thread caps were used; no unsupported macOS affinity or address-
space enforcement is claimed. The tested domain is bounded; no assertion
of all-input accuracy, tachyon continuation or physical two-loop matching
follows from the master checks alone.

## Formula and implementation reviews

`VERTEX_AUDIT.md` independently reconstructs the real-scalar cubic/quartic
and Weyl/gaugino vertices and their graph prefactors. `CURRENT_FORMULA_AUDIT.md`
independently derives the scalar, signed-Majorana and Landau scalar-vector
finite current kernels, including the evanescent finite +1/2 term. These
reviews use the actual raw component action and saved controls, not a
small-F Kähler approximation or a radial mass surrogate. Their precise
input hashes and current evidence validation are recorded separately.
