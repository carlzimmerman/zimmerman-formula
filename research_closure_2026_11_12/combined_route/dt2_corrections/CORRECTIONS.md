# HY4 corrections and DT2 checkpoint — 2026-11-12

This is a fix-forward record. Original files are copied byte-for-byte under
`originals/`, with SHA-256 hashes and the starting revision in
`originals_manifest.json`. Original criteria, numeric outputs and result bodies
are retained. Notices identify superseded interpretations; these corrections do
not retroactively make an experiment preregistered.

**Standing: kappa = 1/2 is not derived; the theory is not closed.**

## 1. Corrected DT2 time and growth coordinates

With `H = d ln(a)/dt`, the clock integral is `dt/d ln(a) = 1/H`.
`dt2_form.py` and `dt2_reach.py` previously integrated `1/(a H)` against
`d ln(a)`, introducing an extra factor `1/a`. Their elapsed time from z=10
to 0 was 30.4296 Gyr instead of 12.8857 Gyr in their own background
(`Omega_m=0.31`, `Omega_L=0.69`, `H0=70 km/s/Mpc`). Both maps are corrected.
The new tabulations agree with independent quadrature to 2.1e-8 relative.

For pressureless growth, conversion of
`delta_tt + 2H delta_t = 4 pi G rho_m F delta` to `ln(a)` gives
`delta'' + (2 + dlnH/dlna) delta' = 1.5 Omega_m F delta`.
The old coefficient 3 was incorrect. An independent Einstein-de Sitter
benchmark now returns the exact growing solution `delta proportional to a`;
the old code returned growth 4.21438 instead of 7 from a=1/7 to 1.

The corrected finite K1 calculation, with all other inputs unchanged, is:

| k_com [Mpc^-1] | D_DT2 | D_reference | ratio | old frozen ratio >= 0.50 |
|---|---:|---:|---:|---|
| 20/3 | 2.7033874 | 5.5085181 | 0.4907649 | FAIL |
| 2 | 3.6914661 | 5.5085181 | 0.6701378 | PASS |
| 0.2 | 4.5606518 | 5.5085181 | 0.8279272 | PASS |
| 0.02 | 5.4600183 | 5.5085181 | 0.9911955 | PASS |

Thus the original K1=PASS at 0.5509 is superseded by **K1=FAIL** at its
deciding wavenumber. The finite computation uses the lane's reduced growth
equation; it is not a complete perturbation calculation or data likelihood.

## 2. The present-day formation claim is withdrawn

The original `RESULT.md`/`lane_result.json` asserted `R_set(0)=0` and settled
residual 1. However, `dt2_run.out` actually prints `R_set` near 3000 kpc and
`cover PASS`, after absorbing collapsed material into a central point mass.
It also counts all interior dust as settled without checking its velocities.
Neither the summary nor that classification establishes the physical halo.

The corrected driver stops at the first inner-cutoff or shell-crossing event
by default. It records termination and whether z=0 was reached. The settling
diagnostic refuses truncated or absorbing runs. An inner boundary hit is now
called **central_cutoff**, not a proved caustic.

There is a further, unresolved physical limitation. The formation force at
uniform density and zero baryon point mass includes the cold background
`Omega_c=0.26`, but its H(a) uses total matter `Omega_m=0.31` and Lambda
`Omega_L=0.69`. In units of `H0^2 r` it gives `-Omega_c/(2a^3)` instead of
`-Omega_m/(2a^3)+Omega_L`. Homogeneous baryons and the Lambda force are absent.
The initial finite inner shell boundary is another departure from exact FRW.
No physical cosmological formation verdict is assigned to this reduced solver.

Six corrected, nonabsorbing **code diagnostics**, log10(M_b/Msun)=10.45:

| footing | shells | central-cutoff time [Gyr after z=10] | ending z |
|---|---:|---:|---:|
| canonical | 130 | 0.150867 | 8.09796 |
| canonical | 260 | 0.142012 | 8.18729 |
| canonical | 520 | 0.132972 | 8.28078 |
| alt | 130 | 0.134712 | 8.26260 |
| alt | 260 | 0.140117 | 8.20669 |
| alt | 520 | 0.129414 | 8.31823 |

All stop at the central cutoff, not a detected shell crossing. Canonical time
increments do not shrink across this ladder; alt is nonmonotone. Therefore
these are not converged physical event times. `R_set(0)` and settled-mass
residual are **UNAVAILABLE**, represented by null, not zero.

## 3. A bounded test of shifting the compressibility band

The contract named four supports before running this new diagnostic. Only
the support of the existing quintic family changes; M=400, L=8e-6 and the
original static cap q_well<=216 remain fixed. The results are:

| support q | q at x=4e-6 | static cap | growth ratio at 20/3 | growth gate | reachable by compression from q=1331? |
|---|---:|---|---:|---|---|
| [2,26], original | 14.000 | PASS | 0.490765 | FAIL | no |
| [30,216] | 122.991 | PASS | 0.529983 | PASS | no |
| [1500,5000] | 3240.512 | FAIL | 0.617883 | PASS | yes |
| [2000,10000] | 5970.555 | FAIL | 0.617883 | PASS | yes |

No scanned support passes all three requirements. This has a simple partial
explanation: if a single modified band starts above q=1331, then at q=216
the unmodified cold branch still has
`x(216)=n0*(216-1)/400=1.1428724e-8 < 4e-6`. Monotonicity forces
`q(4e-6)>216`. Moving this entire single band to early-collapse densities
cannot preserve the original static-density cap. This does not exclude
multiple bands, different early initial conditions, a changed cold slope,
or later formation; all would require additional justified physics.

The useful next formation calculation is a background-consistent initial
value problem with a stated continuation through crossings, independently
specified charge and baryon catchment, and a mass-retention prediction.
No late halo amount should be inferred from central absorption or assigned
to every galaxy using the cosmic mean ratio alone.

## 4. Physical symmetry and coefficient claims

**FRAMEWORK / FINAL-17.** The identity
`X(lambda*a0,lambda*g_N)=X(a0,g_N)` is algebraic covariance. It is not a
physical gauge at fixed G,M_b,r, since `g_N=G*M_b/r^2` is then fixed.
FINAL-17's old transformation simultaneously scaled g_N and held its source
fixed; its Poisson check separately used g proportional to sqrt(a0).
Those are not one common transformation. The physical-gauge/no-go reading
and the assertion that all histories are observationally identical are
withdrawn. The capacity identity still supplies no independent coefficient.
The Lean proof terms are unchanged; their comments now state their scope.

**OUT5.** `rhoPinDeepOf(dsg,G,_a0)=dsg/(4*pi*G)` ignores its last argument.
Its theorem proves only fixed-field expression independence. On the solved
deep branch at fixed M_b,r, `rho_c=sqrt(G*M_b*a0)/(4*pi*G*r^2)`, which varies
as sqrt(a0). The claim that no halo observable changes is withdrawn. The
separate fixed-mu_K early-coldness/halo-matching obstruction is not repaired.

**OUT-2.** The rate-lock equation `a0/c=H_Lambda/(2*pi)` is an added physical
postulate, not a consequence of KMS periodicity supplied by this record.
Given this postulate and Friedmann's relation, the Lean algebra correctly
yields `kappa^2=2/(3*pi)`, a different value from 1/4. The mechanism still
requires independent derivation of its clock-vacuum coupling and selection
of target/winding. The original disclosure of post-selection remains.

**OUT-3 equality-fixed.** Under tau->2tau with the metric fixed, Q->2Q and
the spatial leaf measure is unchanged, so V_Sigma/Q halves. It is not
invariant as the candidate charter asserted. Furthermore the existing
term `mu_K^2*(Q-1)^2/(2K)` changes from zero at Q=1 to mu_K^2/(2K).
The assumed clock relabeling is not a symmetry of that action. The
candidate's numerical failure remains a conditional exercise, not a gauge
fixing argument. Its original charter is left intact below a notice.

**Two kernels.** Law B, `g^2=g_N^2+a0*g_N`, and law S,
`g_N=g^2/(g+a0)`, are different. At g_N=a0 they give sqrt(2)*a0 and
the golden ratio times a0. They have a common deep limit but cannot be
interchanged in exact action claims. Their outer-halo profiles are close
at the cited KiDS radii; this correction alone does not fix the amount.

## 5. H062 normalization and selection

The mode-count family uses `Y=g/s` and `mu_n(Y)=1-(1+Y)^(-n)`.
Its asymptotic scale is `a0=s/n`. A Cassini calculation using x=g/a0
therefore needs `mu_n(x/n)`, not `mu_n(x)`. The original code used the
latter with a0=s/n, introducing the factor n twice. `nu_mandel_mond`
now supplies the correct callback. Tests verify `y*nu(y)^2 -> 1` and
`nu_MOND(y)=nu_raw(y/n)` for n=1,2,3,5.

The old selection check accepted n=3 as reproducing n=2 because it allowed
`abs(bestB-2)<=1`. It now requires exact n=2. Historical data selected n=3;
that is an adverse result, not a successful replication. The two kernel
families in `H062_TWO_FINDINGS.md` also cannot share one Cassini n bound.
No exhaustive kernel-class exclusion is claimed by this finite scan.

The corrected full run retains the historical calibration and ceiling. It
returns Q_zz/ceiling = 6.84 at n=2, 4.05 at n=3, 1.24 at n=5, and 0.67 at
n=6; the passing scanned set is {6,8,10,20}. The joint scanned set remains
empty. The run exits 1 because the honest n=2 reproduction check fails
(5/6 checks pass). Its manifest records `failed`, not successful closure.
Quadrature still emits roundoff/bad-integrand warnings, and the inherited
QUMOND-to-AQUAL calibration has not been independently audited here. These
numbers are conditional pipeline diagnostics, not certified exclusion bounds.

## 6. Reproduction and provenance

From the repository root:

```
python3 -B research_closure_2026_11_12/combined_route/dt2_corrections/test_dt2_regression.py
python3 -B research_closure_2026_11_12/combined_route/dt2_corrections/test_h062_normalization.py
```

Before/after regression outputs are retained. `contract.json` states the
DT2 finite assertion and non-claims; `run_001/manifest.json` is a validated
v2 computation record with unchanged input hashes, completed status and
`results.json`. Exact runner arguments, software and limits are in that
manifest. `contract_h062.json` and `h062_run_001/manifest.json` record the
separate finite H062 rerun, including its real process status and warnings.
No original numeric output was overwritten. Scripts have changed; the
old .out/.json files describe the old revision and must not be treated as
outputs of the corrected source.

The complete local regression suite contains four tests and passes.
FINAL17.lean and OUT5.lean were freshly compiled at their actual paths with
`lake env lean` in `fable_independent_2026/lean_2026`; both exit 0. Only
comments changed in those Lean sources. `final17_lean_verify.out` and
`out5_lean_verify.out` preserve the fresh output. The mathematical prose
self-review covers this record and the seven new notices; no theorem or
proof term was changed as a proofreading edit.
