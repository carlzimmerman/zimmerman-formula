# Independent KT38 Milky Way implementation review

The local coefficients in `weak_model.py` correctly differentiate the stated
phantom energy. The required factor `2s` is present in B. The inherited
`generalized_v3.py` uses the compatible factored Hessian and its full weighted
transpose. I find no coefficient, sign, or off-diagonal multiplicity defect in
these files. This verdict concerns the finite action implementation and the
recorded controls, not overall health or observational viability.

Review scope: `weak_model.py`, `checks.py`, the inherited v3 field/source
operators, and `search.py`. No implementation or frozen input was changed.
The completed `checks_001`, `full_002` and `focused_001` manifests independently
validate. The fresh profile regrade below covers all 27,500 rows and finds zero
four-cut passes on both footings at each of ten sampled physical lengths. This
is not a continuous-length exclusion.

## Derivative reconstructed without assuming the code's answer

In the code's a0/kpc units, put

    F=P-x=x[R(z)-1],  x=g.g,  s=ell^2 H:H,  z=x+s^2.

Then, with both tensor off-diagonals included in H:H,

    delta x = 2 g.delta g,
    delta s = 2 ell^2 H:delta H,
    delta z = delta x + 2s delta s,
    delta F = 2[R-1+xR'] g.delta g
              + 4 ell^2 s xR' H:delta H.

Thus the half-derivatives used by the finite energy are exactly

    A=[R-1+xR']g,
    B=2 ell^2 s xR' H.

The code obtains `xR'=(x/z)(zR')`, retaining the stable primitive from KT37;
`B=(2*ell*ell*s*ratio*dd)*H` is the needed coefficient. Subtracting x in F
is essential and is present as `energy=x*(Rminus1)`. The static Newtonian
control returns zero phantom energy and zero A,B. At ell=0 the Hessian
coefficient vanishes and `R+zR'=Q'` gives the original simple-QUMOND gradient.

The four stored axisymmetric components rr,rtheta,thetatheta,phiphi have
Frobenius multiplicities 1,2,1,1. For the mixed component, the factor two
cancels the one-half in the symmetrized covariant Hessian. The factored
source in the inherited v3 class retains both mixed transposes, the radial
second transpose, the angular face stiffness transpose, the cotangent
connection stress difference, and both radial tangential stresses. Algebraically
this is `-W^-1[G^T W A+H^T W B]`. With `L` self-adjoint in W and
`delta psi=4pi L^-1 delta rho`, differentiating
`Eph=-(8pi)^-1 sum W F` gives `delta Eph=sum W phi_ph delta rho` with the
implemented source sign. No Gaussian operator or separately adjustable
response width enters this calculation.

The zero-jet assignment A=B=F=0 is a continuous extension; it does not remove
spatial derivatives of these quantities at a saddle. No claim of bounded
second derivatives at zero follows. The low-amplitude recovery is pointwise
at fixed nonzero g, not uniform near persistent saddles.

## What the recorded checks establish

The finite energy checks use a fixed linear Newtonian perturbation and
difference local energy densities before summing. This is the derivative
specified above, not a finite difference of an independently prescribed force.
For ell=1,3,10 kpc, the best recorded energy-gradient relative errors are
6.66e-9, 9.08e-9 and 4.58e-8. Reciprocity best relative errors are 2.15e-10,
6.22e-9 and 1.38e-8. The three decreasing perturbation sizes expose truncation
and cancellation instead of relying on a single favorable step.

The Newtonian phantom result is exactly zero. The ell=0 map agrees with the
unchanged KT33 plain-energy map to 2.46e-16 relative. Two-dimensional spherical
Plummer polar artifacts remain below 8.76e-9 over the tested grids. At the
finest grid, the radial force relative errors are 3.63e-4, 1.14e-3 and 1.76e-3
for ell=1,3,10, and decrease under refinement. The spherical force comparator
is the continuum reduction `A_r-B_rr'-2(B_rr-B_t)/r`; it uses the same local
coefficient routine but a separate radial divergence calculation. It checks
the PDE discretization, while the algebraic derivative review above checks
the local constitutive factor.

The observational script explicitly gates on the new KT38 checks and the
accepted KT37 v3 covariance record. It does not use the withdrawn KT37 v1
observational scores. It recomputes unchanged original cuts from each stored
force profile. Its requested grid contains five physical lengths, not a
continuous interval. The frozen full-run contract has a harmless wording
carryover saying “Six discrete lengths” in one non-claim; its actual declared
length list and execution are .3,1,3,5,10 kpc. This review does not edit that
frozen contract.

## Limits that remain material

Reciprocity establishes symmetry of the tested finite response derivative,
not positivity, ellipticity in every background, dynamical stability, or a
relativistic completion. The smooth test sources do not prove thin-disk
continuum convergence. The shared v3 implementation retains the explicit
KT37 boundary qualifications: composing a one-sided radial derivative twice
has nonvanishing pointwise quadratic error at the first/last radial rows;
physical observables require cutoff/domain checks. The MW half-domain imposes
equatorial reflection, so an axial-linear manufactured scalar is admissible
only in a full-domain test. These inherited limitations are disclosed in
KT37/mw/README.md and are not cured by changing the local coefficients.

## Reviewed input SHA-256

| Input | SHA-256 |
| --- | --- |
| KT38/mw/weak_model.py | ad616e81f9f0cf4a67096559307a87bb44fcf52abb4618ced988eb26f05a0fc5 |
| KT38/mw/checks.py | 695d79d02d2cc28f17b90c296e0f4f13d7f9aa56ec6424c5b7683d20f9124031 |
| KT38/mw/search.py | 8cd30bc0a515d03c4232291048efd49490bafdd18ba35a93bca9274298f6836b |
| KT38/mw/checks_001/results.json | 50fd5b6542d3eec65f8444c8c68ed3648e6325a0c374934e8566bb58b3aa7881 |
| KT38/mw/checks_001/manifest.json | 86418c415d1ad84200b2d1a3609f33541ab04d75f20a431bcbcd387b7a3b96f3 |
| KT37/mw/generalized_v3.py | 9eecef18bf2dc9d7aec27bd34a3107bad6e0c3e664e1d71d2c8a9b04035a5f13 |
| KT37/analytic/law.py | 7a7f4710cacb6b33a88e170147c64eb6554ba44f6fda1fc81104bea5a222740f |

Names in this table abbreviate their actual `rebuild_2026_10_22/KT37_generalized_action`
and `KT38_weak_field_curvature` prefixes. Manifest verification used the
mathbox computation-audit `validate_manifest.py --root .` against the recorded
checks manifest and exited zero. No check or input was edited after hashing.

## Population audit contract and interrupted artifact

The bounded independent regrade reads at most 13,750 saved rows, reconstructs
cK, cO, the log-K slope and D from the saved profiles and frozen data, and
compares every L1/L2a/L2b/L3/Lh flag and every population summary. It performs
no new field solve. It requires the original 1,375 cells in their original
order, separate footings and the five declared lengths. A 60-second alarm and
50 CPU-second limit bound the read/regrade command; only this review is written.
This verifies reported grading arithmetic, not continuum physical accuracy.

The first `full_001` manifest is **failed**, exit 1, after 136.4 seconds. The
alternative footing was computed but final JSON serialization encountered an
infinite h from a nonnegative fitted log-K slope. The retained JSON therefore
contains only the canonical footing. Its lack of alternative profiles and
final runtime marker prevents treating it as a completed two-footing scan.
The raw stdout summaries do not replace the missing profiles. A fresh version
must encode this defined infinite scale-height diagnostic explicitly while
preserving its failed strict-Lh flag; changing the data or suppressing the
case is unnecessary.

Independent reconstruction of all 6,875 retained canonical rows completed in
under one second with zero scalar/flag/summary mismatches. cK and cO were
recomputed by their frozen weighted sums of squared residuals; h used the
explicit centered covariance/variance slope rather than the production least
squares call; all cuts and D were then reconstructed directly. Maximum
relative scalar discrepancy was 1.336e-14. Four-cut and strict-intersection
counts are zero at all five sampled lengths. Best-D indices are respectively
963,1023,1354,1356,1350. This is a partial canonical-only regrade, not acceptance
of the failed overall run.

The retained canonical result hash is
`3807e7fd593dbeedb1ca072471571ef23b07f46347426830d890b50fca19f449`.


## Serialization fix review

`search_v2.py` copies each original score after all unchanged cuts have been
evaluated. It replaces only a positive-infinite h with JSON null plus the
explicit status “positive infinity: fitted log-K slope is nonnegative,” after
asserting that strict Lh is false. This preserves the mathematical diagnostic
and its failed strict cut. It does not clip h or alter any force or cut. NaN
and negative infinity are not silently accepted, and JSON still rejects other
nonfinite values. The completed fresh profile audit independently confirms a nonnegative fitted
slope for every encoded null.

Reviewed search_v2.py SHA-256: `1b3f99af9072b164cef03b023d6ca7e458f3d281c673d437afbd18f868c3d233`.

## Reproducible fresh-profile regrade

The fresh audit covers two distinct 13,750-row scans (27,500 rows total): the
five original lengths and the five explicitly adaptive lengths. It preserves
that selection distinction. The following read-only command body is executed
from the repository root; it has its own time/CPU caps and produces only a
compact JSON report on stdout. Run only after both manifests are complete.

```python
# BEGIN_REPRODUCIBLE_REGRADE
import sys, signal, resource, hashlib, json, subprocess
from pathlib import Path
signal.alarm(60)
resource.setrlimit(resource.RLIMIT_CPU, (50, 50))
sys.dont_write_bytecode = True
p = Path('rebuild_2026_10_22/KT38_weak_field_curvature/mw')
sys.path.insert(0, str(p.resolve()))
import weak_model as J
np, C = J.np, J.M.C
reports = []
for name, lengths in [('full_002', [.3, 1., 3., 5., 10.]),
                      ('focused_001', [1.5, 1.75, 2., 2.25, 2.5])]:
    mf = p / name / 'manifest.json'
    manifest = json.loads(mf.read_text())
    assert manifest['run']['status'] == 'completed'
    validator = '/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py'
    checked = subprocess.run([sys.executable, validator, '--root', '.', str(mf)],
                             capture_output=True, text=True)
    assert checked.returncode == 0, checked.stdout + checked.stderr
    f = p / name / 'results.json'
    d = json.loads(f.read_text())
    assert d['cells'] == J.E.population()
    assert d['selected_indices'] == list(range(1375))
    assert set(d['footings']) == {'canonical', 'alt'}
    assert d['runtime_seconds'] > 0
    count = 0
    maxerr = 0.
    max_grade_error = 0.
    max_slope_error = 0.
    infinities = []
    summaries = []
    for foot, data in d['footings'].items():
        assert [s['ell_kpc'] for s in data['scans']] == lengths
        for scan in data['scans']:
            rows = scan['rows']
            assert len(rows) == 1375
            good, strict, vals = [], [], []
            line_counts = {k: 0 for k in ['L1', 'L2a', 'L2b', 'L3', 'Lh']}
            for i, row in enumerate(rows):
                assert row['index'] == i and row['cell'] == d['cells'][i]
                assert row['ell_kpc'] == scan['ell_kpc']
                assert row['source_stats']['finite']
                q = row['corrected']
                K, vo, vc, K0 = np.array(q['K']), np.array(q['vc_Ou']), q['vc'], q['K0']
                ck = float(np.sum(((K-C.BR_K)/C.BR_E5)**2))
                co = float(np.sum(((vo-C.OV)/C.OE)**2))
                xx, yy = np.asarray(C.BR_R)-C.R0, np.log(np.maximum(K, 1e-9))
                slope = float(np.sum((xx-xx.mean())*(yy-yy.mean())) /
                              np.sum((xx-xx.mean())**2))
                h = -1/slope if slope < 0 else float('inf')
                flags = {
                    'L1': abs(vc-C.L.VC_BRIEF) <= C.L.VC_BRIEF_LINE and abs(vc-C.vE) <= 2*C.eE,
                    'L2a': ck <= C.LK, 'L2b': abs(K0-C.KZ) <= 2*C.KZE,
                    'L3': co <= C.LO, 'Lh': abs(h-C.HLIT) <= 2*C.HE}
                D = max(ck/C.LK, abs(vc-C.vE)/(2*C.eE), co/C.LO,
                        abs(K0-C.KZ)/(2*C.KZE))
                for k, v in flags.items():
                    assert bool(q[k]) == bool(v), (name, foot, scan['ell_kpc'], i, k)
                    line_counts[k] += bool(v)
                scalars = [('cK', ck), ('cO', co), ('D', D)]
                if q['h'] is None:
                    assert slope >= 0 and not flags['Lh']
                    assert q['h_status'] == 'positive infinity: fitted log-K slope is nonnegative'
                    infinities.append([foot, scan['ell_kpc'], i, slope])
                else:
                    assert np.isfinite(h)
                    scalars.append(('h', h))
                    max_slope_error = max(max_slope_error, abs(-1/q['h']-slope))
                for k, v in scalars:
                    error = abs(q[k]-v)/max(abs(v), 1.)
                    maxerr = max(maxerr, error)
                    if k != 'h': max_grade_error = max(max_grade_error, error)
                passed = all(flags[k] for k in ['L1', 'L2a', 'L2b', 'L3'])
                assert q['all_four'] == passed
                if passed: good.append(i)
                if passed and flags['Lh']: strict.append(i)
                vals.append((D, i))
                count += 1
            sm = scan['summary']
            assert good == sm['pass_indices'] and len(good) == sm['n_pass']
            assert len(strict) == sm['n_strict'] and sm['n_tested'] == len(rows)
            assert min(vals)[1] == sm['best_D_index']
            assert line_counts == sm['lines']
            summaries.append([foot, scan['ell_kpc'], len(good), len(strict),
                              min(vals)[1], min(vals)[0]])
    assert count == 13750 and max_grade_error < 2e-11 and max_slope_error < 1e-12
    reports.append(dict(run=name, result_sha256=hashlib.sha256(f.read_bytes()).hexdigest(),
                        manifest_sha256=hashlib.sha256(mf.read_bytes()).hexdigest(),
                        rows_regraded=count, mismatches=0,
                        max_relative_scalar_discrepancy=maxerr,
                        max_relative_grade_score_discrepancy=max_grade_error,
                        max_absolute_fitted_slope_discrepancy=max_slope_error,
                        positive_infinite_h_count=len(infinities),
                        positive_infinite_h_cases=infinities[:3], summaries=summaries))
print(json.dumps(reports, indent=2))
# END_REPRODUCIBLE_REGRADE
```


The first fresh regrade's blanket 2e-11 relative scalar comparison rejected
one adaptive row solely because h is ill-conditioned near a zero slope:
alt, ell=2.5, index724 has h=44426.527052554506 in the production least-squares
calculation and 44426.52705086486 with centered covariance. The relative
difference is 3.804e-11; all actual cuts, D, summary counts and other flags
agree. This is retained as an audit diagnostic. The final executable above
checks the fitted slope itself to absolute 1e-12 and cK/cO/D to relative
2e-11 while still reporting the largest h discrepancy. No scientific model,
force, cut, profile or frozen input changed to address this conditioning.


## Completed empirical regrade verdict

Both fresh manifests validate as completed, with every original input hash
unchanged. The exact executable above completed successfully in under two
seconds. All 27,500 profiles retain the original 1,375 baryon cells, all five
lengths in each run, separate acceleration footings and unchanged grading
constants. Every primary/strict flag, pass list, line count and best-D index
agrees with the reconstruction. cK, cO and D match exactly at float64 precision;
the independently fitted slopes differ by at most 1.388e-15 absolute.

| Run | Lengths (kpc) | Rows regraded | Four-cut passes, canonical / alt | Encoded positive-infinite h |
| --- | --- | ---: | --- | ---: |
| full_002 | .3,1,3,5,10 | 13,750 | 0 / 0 at every length | 24 |
| focused_001, adaptive | 1.5,1.75,2,2.25,2.5 | 13,750 | 0 / 0 at every length | 23 |

Every null h has the explicit positive-infinity status, a nonnegative
independently fitted log-K slope and strict Lh=false. The strict conjunction
with the four primary cuts is therefore also zero throughout. The original
five-length best D is 2.408152 (canonical, .3 kpc, index963) and 1.975204 (alt,
.3 kpc, index831). The adaptive-grid best D is 2.517874 (canonical, 1.75 kpc,
index1050) and 2.219403 (alt, 1.75 kpc, index834). These selected diagnostics
are not fitted continuum optima.

| Completed artifact | SHA-256 |
| --- | --- |
| full_002/results.json | 4e461408d70471e87e30e4c54b47a1051bb77d0c9cf22958bbcc37cf2144da66 |
| full_002/manifest.json | 0a4e67cd61b91733cb2cf14503c3ed54e531325a0f818d3eb7bd6d8eb2b6106a |
| focused_001/results.json | 76ba3d3d6a8444bf843bc545df4270234ac79f14c5c6496b10bcc07a978cb3d6 |
| focused_001/manifest.json | 088f1c7a2fa10f4cee7df25b7e16c4ef84b9ae4ff7128dc354e05a49b75bc92c |

The failed first run is retained as failed evidence; neither its missing
alternative profiles nor any invalid KT37 v1 score was promoted. The new
energy's local implementation is supported by the reviewed derivation and
finite checks, but these completed scans supply no Milky Way passing model
among the tested lengths. Nothing in this review excludes an untested length,
certifies thin-disk continuum convergence, or establishes action health.
