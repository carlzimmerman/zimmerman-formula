# Latest Claude work: Lean certification, 2026-11-07

**Verdict: proved mathematical statements under explicit model assumptions;
the web-side numerical CMB-lensing premises remain on hold pending their reread.**
This follow-up certifies kernel algebra, scalar stiffness-variation steps and a
universal spherical positivity theorem. It does not certify every numerical
RESULT label or the complete covariant theory. Kappa = 1/2 FITTED; not theory closed.

Proof-development base: `d0c3692fc62c7177af78d9795e2ae6d9fd9d50e4` (through GL2's
independent kernel audit). Integrated GL1's reread at `4699adbbd7` before
publication; final verification pins its input hashes too. Review provenance: Codex self-review. The numerical
GL2 rebuild is evidence from Claude's committed source/output, not a computation
rerun or an independent numerical audit performed by this follow-up. Exact
input and compiler-output hashes are in `verification.json`.

## 1. Limber-kernel correction

Sources: `GL2_limber_k4_audit/RESULT.md`, `gl2.py`, and QX3 iter2's `limber_ratio`.
Given the lensing-potential Poisson factor `1/k^4` and `k=ell/chi`, where
`ell=L+1/2`, `LimberKernel.lean` proves

```
1/k^4 = (chi/ell)^4.
old_weight = (chi_source-chi)^2 (1+z)^2 P /
             (chi_source^2 H chi^4).
corrected_weight = (chi_source-chi)^2 (1+z)^2 P /
                   (chi_source^2 H ell^4).
```

All denominators needed for these cancellations are assumed nonzero. The
geometric weight is transcribed explicitly in Lean. The physical Limber
approximation and Poisson-to-density-spectrum identification are inputs, not
derived in these statements.

At fixed ell, the common `ell^-4` factor cancels in a ratio. The slice-dependent
`chi_i^4` factor remains inside both sums. An exact two-slice counterexample
changes the ratio from 1/2 to 16/17. A constant response is also proved invariant
under reweighting, so a kernel correction does not by itself prove that any
particular observational label moves. A covariance identity states the exact
condition for invariance. Common-factor cancellation is also proved for
continuous integrals.

The file additionally proves a power bound: for nonnegative normalized weights,
response in [0,1], and suppression confined to slices S, the total suppression
lies between 0 and the total weight of S. Applying this to PR4 requires the
correct weights and affected slices; no numerical weight fraction is supplied
by the theorem.

GL2 reports CONFIRMED for the missing factor, with agreement against CLASS.
The repository's `HOLD_KERNEL_REREAD_2026_11_07.md` identifies affected numerical
premises, including EW2's scale window and the SV5/FA3 web lines. Those premises
must be re-read by their assigned lanes. GL1 has now reported its sector-side
results; the web-side GL3 remains pending in the integrated record. This
certificate neither rewrites lane labels nor removes the publication hold.

GL1 (4699adbbd7) reports QX3 iter3 gains one passing member, QX7 iter_3 gains
its lensing window, QX10 iter_1 passes its former J1 block, and CE2's GL gate
loses discriminating power. KD1/SE1's wall remains because BBN is still the
binding side; the revised lensing scale 631 remains above the reported galaxy
ceiling 79.43. These are attributed numerical findings, not new Lean-derived
empirical bounds or a numerical rerun by this review.

## 2. QX17D: stiffness stress coefficient

Source: `QX17D_blend_field_equations/RESULT.md` and its generic-F script.
`StiffnessStress.lean` proves the scalar chain-rule leaf

```
d/dlambda [-F(Pi/lambda)] at lambda=1 = Pi F'(Pi).
```

For the quadratic control `F=Pi^2/2`, `Pi F'=2F`. For `F=A Pi^6`, `Pi F'=6F`,
so retaining `2F` misses `4F`; the two coefficients differ whenever A>0 and
Pi is nonzero. For QX17D's generic test polynomial
`F=Pi^2/2+(3/10)Pi^4-(1/7)Pi^6`, the discrepancy is
`(3/5)Pi^4-(4/7)Pi^6`, with an exact counterexample at Pi=1. Derivatives of
these functions are proved, not supplied as opaque assumptions.

The inverse-scaling chain rule supports the corrected coefficient but is **not**
a formal covariant variation of Pi or the metric. QX17D's full tensor identity
continues to rest on its SymPy/direct-variation checks, which are not rerun here.
The adopted layer's complete piecewise formula is not formalized by this file.

For the switch's pure sixth-power neighborhood, both the energy profile and
the recorded slope profile are zero at the switch and tend to zero there.
The switched sixth-power function itself is proved differentiable at the
branch point with derivative zero, by gluing the two one-sided derivatives.
The first-piece coefficient obeys the exact relation
`30*(122363904/44610575)=734183424/8922115`. Consequently this energy term has
zero latent jump across the branch point. This does not prove that no dynamical
energy transfer can occur, or that a carrier cannot be added to another action.

## 3. CK2: universal spherical positivity

Source: `CK2_release_speed/ck2.py` and its spherical simple-nu census.
For a>0, G>0, r>0, enclosed mass M(r)>0 and M'(r)>=0, set

```
s(r) = sqrt(1/4 + a r^2/(G M(r))),
M_ph(r) = M(r) (s(r)-1/2).
```

`SphericalPhantom.lean` differentiates this definition and proves exactly

```
M_ph'(r) = M'(r) (s-1/2)^2/(2s) + a r/(G s) > 0.
rho_ph(r) = M_ph'(r)/(4 pi r^2) > 0.
```

This extends the positivity result beyond CK2's sampled point, Plummer,
Hernquist and mixed profiles to every differentiable spherical profile with
the stated local mass assumptions. With rho_DE>0 it proves both
`rho_ph/rho_DE>0` and `2+rho_ph/rho_DE>0`, the static switch signs used by v3s
and AC2q. It does not prove the finite-grid minimum as a uniform lower bound.

Excluded cases remain explicit: r=0, M(r)=0, negative mass derivative,
nonspherical fields, external-field lobes, and dynamical collapse. In
particular, two positive static endpoint signs do not rule out a transient
branch crossing. No theorem here asserts CK2's broader action-content label
NO RELEASE TERM without qualification.

## Dependency and coverage matrix

| Target | Mathematical dependencies | Reading |
|---|---|---|
| Corrected kernel and fixed-ell cancellation | Explicit rational weight, nonzero denominators, supplied k^-4 identification | Proved algebra; physical projection inputs remain conditional |
| Reweighting effect and suppression bound | Finite sums; nonnegative normalized weights and response bounds where stated | Proved; no PR4 label inferred |
| General stiffness coefficient | Differentiability of F and specified Pi/lambda scaling | Scalar chain rule proved; covariant metric variation not addressed |
| Quadratic/sixth/generic tests | Explicit real polynomials | Derivatives and discrepancies proved |
| Zero latent jump | Continuous sixth-power energy neighborhood and zero branch values | Proved for that term; dynamics not addressed |
| Spherical phantom density and static switch signs | Explicit simple-nu mass, positive a/G/r/M, nonnegative M' | Proved universally in this spherical class |
| CK3 group slope, CK4 cosmology, KX1/CE2/RS3/UA1 data labels | Numerical pipelines, unit choices, empirical likelihoods | Not certified here |

CK3 records a unit/extrapolation issue and a non-robust frozen FAIL. CK4 records
a NO VERDICT because its GL mutation lacks power. These numerical limitations
are not repaired by algebraic certification. The latest freeze-only lanes do
not acquire a RESULT from this review.

## Verification and remaining work

The three files contain 34 new theorems. Every theorem has a printed axiom
report; the verifier accepts only `propext`, `Classical.choice`, and `Quot.sound`,
checks source/evidence hashes before and after compilation, and records exit
codes and logs. Counterexamples are proved statements, not rejected proof
attempts. The earlier 107- and 48-theorem sources are checked for unchanged
hashes; they are not needlessly recompiled.

```sh
python3 closure_2026_11_07/LEAN_LATEST_CERTIFICATION/verify.py
```

If the local dependency tree is not built, pass
`--library-project /absolute/path/to/matching/lean_2026`. This mode checks the
pinned toolchain and dependency manifest before using a prebuilt Mathlib tree.
It compiles these source files, not copies from the library checkout.

Next obligations: complete GL3's web-side reread and incorporate the reported
GL1 changes before using affected bounds as physical premises; formalize the covariant Pi variation to lift the
stiffness chain-rule leaf to a tensor theorem; supply a dynamical theorem if
transient branch crossings matter. The spherical result is already a complete
proof in its stated class and needs no enlargement of the profile grid.
Self-proofreading covers the new Lean files and this report. No paper, frozen
criterion, lane label, adoption decision or deposit is changed by this review.

The concurrent unification statement and outside-solver/AK1 proposal are not
formalized as full unification or an exhaustion theorem here. A dimensional
release-speed construction is not an action-level derivation; AK1 has frozen
criteria, not a confirmed release mechanism, at this checkpoint.
