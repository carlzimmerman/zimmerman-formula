# Independent KT39 Milky Way audit

The local coefficients correctly differentiate the stated action, including
`B=p ell^2 s^(p-1) xR' H`. The complete compatible weighted Hessian transpose
is retained. The mutable module power is safe in the recorded fixed-power
searches and in the explicitly sequential refinement loop. This review does
not establish all-background action health or continuous parameter coverage.

Scope: power_model.py, checks.py, search.py, refine.py, the unchanged KT37 v3
operators, the new full tensor API, four power-specific control records,
five full-population runs and the selected literal-source refinement. No
production file or frozen input was changed. Only this review and its
read-only audit program, verify_review.py, are reviewer-owned.

## Completed empirical verdict

The independent regrade finds zero flag or summary mismatches in all **55,000
population profiles and 60 selected refinement rows**. The original 18
power/length choices and adaptive (p=1.25,ell=2.75 kpc) choice have no four-cut
passes on either footing. The adaptive **p=1.125,ell=3 kpc** choice has
**32 canonical and 20 alternate** scan-grid passes; the four-cut plus strict
Lh intersection is zero on both.

The frozen strongest witnesses, original indices1368 canonical and1287 alt,
pass all six literal/resolution/domain configurations each. Both fail strict
Lh throughout. The other eight selected cases fail the primary conjunction
in all six configurations each. Finest-grid witness values are:

| Footing | vc | K0 | cK | cO | h | D |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| canonical | 228.899072 | 69.112977 | 56.339849 | 15.344798 | 3.347210 | .835167 |
| alt | 229.263983 | 70.394394 | 60.254069 | 17.692245 | 3.524306 | .907817 |

The same selected cells pass at refinements2,3,4,5, half the inner cutoff,
and twice the outer radius. Across those configurations D ranges
.833368–.835167 canonical and .899995–.907817 alt. The largest relative
baseline literal-versus-production score difference over all ten selected
cases is 3.057e-10. These are observed numerical stability checks, not
certified continuum error bounds or refinement of every passing population
cell.

All cK/cO/D recomputations match exactly in float64; the largest independent
fitted-slope discrepancy is 1.388e-15 absolute. No positive-infinite h cases
occur in these particular KT39 outputs; the explicit representation branch
is nevertheless checked in code and the verifier would enforce it for any
such row. All ten relevant manifests (four controls, five population scans,
one refinement) validate. The 192 tensor probes give exact A/B/z agreement,
energy agreement within1.954e-16 relative, and exact direct MW endpoint
agreement with KT37 and KT38.

This supplies conditional MW evidence for the explicitly adaptive choice.
It does not make the choice preregistered, eliminate the separate strict
scale-height failure, establish satellite-EFE or other-galaxy performance,
prove action health, or exclude untested p/ell values.

## Full action linkage and endpoints

For `F=P-x=x[R(z)-1]`, `x=g.g`, `s=ell^2 H:H`, `z=x+s^p`, ordinary variation gives

    delta F = 2[R-1+xR']g.delta g
              + 2p ell^2 s^(p-1) xR' H:delta H.

Thus the source half-derivatives are exactly the implemented A and B.
The stable product `(x/z)(zR')` is xR', and the phantom energy density is
`x*(R-1)`. The off-diagonal Hessian multiplicity is two in both the norm and
transpose contraction. The inherited factored source is
`-W^-1[G^T W A+H^T W B]`, not a first-gradient-only surrogate. Self-adjointness
of the fixed Poisson inverse in W gives the energy-to-density derivative
`delta Eph=sum W phi_ph delta rho`, with the implemented sign.

At p=1, `s^0=1` gives the KT37 coefficient, including at H=0; its multiplication
by H has the correct regular limit. At p=2, the factor becomes 2s and recovers
KT38. At ell=0, the identity `R+zR'=Q'` gives the original simple-QUMOND
energy/response. Newtonian Q=z gives exactly zero phantom response. The
joint zero jet is assigned the continuous zero values without a physical
floor; this does not imply zero differentiated source at every saddle.

The reproducible local probes cover eight deterministic float64 jets, four
lengths 0,.1,3,10 and six powers 1,1.125,1.25,1.5,1.75,2: 192 comparisons to
the independent full 3x3 tensor API, including off-diagonal components,
zero fields, zero Hessians, and small/large unequal scales. The physical
energy is compared after adding back x to the phantom energy. Direct MW
endpoint comparisons also use the unchanged KT37 and KT38 coefficient
implementations, not just the new API's endpoint labels. Exact errors and
input hashes appear in the generated record below.

The low-level MW coefficient helper expects floating-point field arrays,
as produced by every recorded field operator. Integer synthetic arrays are
not a supported direct API input because zeros_like preserves their dtype;
the independent probe explicitly uses float64. This does not affect the
recorded numerical grids or tensor API, which casts physical inputs.

## Power setting and source state

Each population/control process calls set_power once before constructing
or evaluating a model, records that p, and checks the control record's p
against the requested value. The guard restricts finite p to [1,2]. No
search loop mutates p after initialization. Different p searches run in
separate processes.

In refine.py, one geometry/Poisson model is reused while set_power is called
immediately before each selected source calculation. This is safe here:
the model stores only p-independent grid, gradient, Hessian and Poisson
operators; fields and coefficients are recomputed for every call; there is
no cached A, B, energy or phantom potential. The source dynamically invokes
the current coefficient function. Each case is evaluated serially before
the next power change. The saved refine2 literal results are independently
compared to their separate-process population scores in this audit. This
API would not be safe for simultaneous mixed-power calls sharing one module;
no such execution occurs in these records.

## Independent grading and provenance contract

Run from the repository root:

    python3 rebuild_2026_10_22/KT39_power_curvature/mw/verify_review.py --require-complete --update-review

The command verifies every manifest and its current hashes, checks exact
population order and power/length coverage, and independently reconstructs
cK, cO, h, D and every cut from saved force profiles. The h slope uses a
centered covariance/variance formula rather than the production least-squares
call. It checks the fitted slope to absolute 1e-12, cK/cO/D to relative
2e-11, and every cut/summary exactly. Near a flat slope h itself is
ill-conditioned; its largest relative discrepancy is reported without
confusing it with a change in a physical cut. Every encoded null h must
have a nonnegative reconstructed slope, the explicit positive-infinity
reason and strict Lh=false.

The original search has 18 p/length choices: three powers and six lengths.
The two additional choices are explicitly adaptive in ../ADAPTIVE_PLAN.md.
All use 1,375 original cells per footing, for 55,000 population profiles.
The selected refinement has ten cases and six grid/domain configurations,
for 60 rows; it cannot certify the entire population's pass counts. Every
refinement row is regraded independently, the frozen selected cells are
matched to the corresponding original best-D records, and the baseline
literal-source calculation is checked against its production counterpart.
No force solve is rerun by this audit. The command has a 180-second wall
alarm and 150-second CPU limit, no randomness, and writes only this review.

The compatible-Hessian qualification remains unchanged: radial edge rows do
not have uniformly convergent composed one-sided quadratic Hessians; actual
witnesses need cutoff/domain checks. The half-domain assumes equatorial
reflection. Smooth-source covariance, reciprocity and finite energy checks
are valuable controls, not thin-disk convergence theorems, positive response
proofs, full satellite predictions, or relativistic/dynamical validation.

<!-- GENERATED_AUDIT -->
## Reproducible audit record

```json
{
  "scope": "Independent finite-coefficient and saved-profile audit; no field solve rerun.",
  "limits": {
    "wall_alarm_seconds": 180,
    "cpu_seconds": 150,
    "randomness": false
  },
  "complete": true,
  "pending": [],
  "tensor_API": {
    "cases": 192,
    "powers": [
      1,
      1.125,
      1.25,
      1.5,
      1.75,
      2
    ],
    "lengths_kpc": [
      0,
      0.1,
      3,
      10
    ],
    "max_relative_tensor_API_discrepancies": {
      "A": 0.0,
      "B": 0.0,
      "energy": 1.9531232530844867e-16,
      "z": 0.0
    },
    "MW_endpoint_discrepancies": {
      "1.0": 0.0,
      "2.0": 0.0
    }
  },
  "controls": [
    {
      "run": "checks_1125_001",
      "power": 1.125,
      "all_checks_pass": true,
      "worst_best_energy_relative": 5.611136476294627e-08,
      "worst_best_reciprocity_relative": 2.158198277981473e-08,
      "max_spherical_polar_relative": 1.5690769336628102e-08
    },
    {
      "run": "checks_125_001",
      "power": 1.25,
      "all_checks_pass": true,
      "worst_best_energy_relative": 1.0165079643612056e-07,
      "worst_best_reciprocity_relative": 2.412261491121179e-08,
      "max_spherical_polar_relative": 1.2652008291712849e-08
    },
    {
      "run": "checks_150_001",
      "power": 1.5,
      "all_checks_pass": true,
      "worst_best_energy_relative": 2.6017783646751515e-07,
      "worst_best_reciprocity_relative": 2.7706688314706798e-08,
      "max_spherical_polar_relative": 2.3671039184741055e-08
    },
    {
      "run": "checks_175_001",
      "power": 1.75,
      "all_checks_pass": true,
      "worst_best_energy_relative": 7.141132686010745e-08,
      "worst_best_reciprocity_relative": 1.8580084255935487e-08,
      "max_spherical_polar_relative": 8.447631288729612e-09
    }
  ],
  "population_runs": [
    {
      "run": "full_125_001",
      "rows_regraded": 16500,
      "positive_infinite_h_count": 0,
      "max_grade_scalar_relative_error": 0.0,
      "max_fitted_slope_absolute_error": 1.3322676295501878e-15,
      "max_h_relative_error": 5.40381248009892e-15,
      "flag_or_summary_mismatches": 0
    },
    {
      "run": "full_150_001",
      "rows_regraded": 16500,
      "positive_infinite_h_count": 0,
      "max_grade_scalar_relative_error": 0.0,
      "max_fitted_slope_absolute_error": 1.3877787807814457e-15,
      "max_h_relative_error": 7.628558894785562e-15,
      "flag_or_summary_mismatches": 0
    },
    {
      "run": "full_175_001",
      "rows_regraded": 16500,
      "positive_infinite_h_count": 0,
      "max_grade_scalar_relative_error": 0.0,
      "max_fitted_slope_absolute_error": 1.27675647831893e-15,
      "max_h_relative_error": 9.663647136949837e-15,
      "flag_or_summary_mismatches": 0
    },
    {
      "run": "adaptive_125_mid_001",
      "rows_regraded": 2750,
      "positive_infinite_h_count": 0,
      "max_grade_scalar_relative_error": 0.0,
      "max_fitted_slope_absolute_error": 1.27675647831893e-15,
      "max_h_relative_error": 5.138405393223822e-15,
      "flag_or_summary_mismatches": 0
    },
    {
      "run": "adaptive_1125_001",
      "rows_regraded": 2750,
      "positive_infinite_h_count": 0,
      "max_grade_scalar_relative_error": 0.0,
      "max_fitted_slope_absolute_error": 1.3322676295501878e-15,
      "max_h_relative_error": 5.288042543247122e-15,
      "flag_or_summary_mismatches": 0
    }
  ],
  "population_summaries": [
    {
      "run": "full_125_001",
      "selection": "original",
      "footing": "canonical",
      "power": 1.25,
      "ell_kpc": 1.5,
      "n_pass": 0,
      "n_strict": 0,
      "best_D_index": 1077,
      "best_D": 1.6911871810471528
    },
    {
      "run": "full_125_001",
      "selection": "original",
      "footing": "canonical",
      "power": 1.25,
      "ell_kpc": 2.0,
      "n_pass": 0,
      "n_strict": 0,
      "best_D_index": 1101,
      "best_D": 1.2463490349868624
    },
    {
      "run": "full_125_001",
      "selection": "original",
      "footing": "canonical",
      "power": 1.25,
      "ell_kpc": 2.5,
      "n_pass": 0,
      "n_strict": 0,
      "best_D_index": 1317,
      "best_D": 1.0243572389979363
    },
    {
      "run": "full_125_001",
      "selection": "original",
      "footing": "canonical",
      "power": 1.25,
      "ell_kpc": 3.0,
      "n_pass": 0,
      "n_strict": 0,
      "best_D_index": 1356,
      "best_D": 1.0337885029655935
    },
    {
      "run": "full_125_001",
      "selection": "original",
      "footing": "canonical",
      "power": 1.25,
      "ell_kpc": 3.5,
      "n_pass": 0,
      "n_strict": 0,
      "best_D_index": 1349,
      "best_D": 1.1161526004604834
    },
    {
      "run": "full_125_001",
      "selection": "original",
      "footing": "canonical",
      "power": 1.25,
      "ell_kpc": 4.0,
      "n_pass": 0,
      "n_strict": 0,
      "best_D_index": 1349,
      "best_D": 1.4436008446319146
    },
    {
      "run": "full_125_001",
      "selection": "original",
      "footing": "alt",
      "power": 1.25,
      "ell_kpc": 1.5,
      "n_pass": 0,
      "n_strict": 0,
      "best_D_index": 915,
      "best_D": 1.6325733849194275
    },
    {
      "run": "full_125_001",
      "selection": "original",
      "footing": "alt",
      "power": 1.25,
      "ell_kpc": 2.0,
      "n_pass": 0,
      "n_strict": 0,
      "best_D_index": 966,
      "best_D": 1.152546551311859
    },
    {
      "run": "full_125_001",
      "selection": "original",
      "footing": "alt",
      "power": 1.25,
      "ell_kpc": 2.5,
      "n_pass": 0,
      "n_strict": 0,
      "best_D_index": 1182,
      "best_D": 1.156594426451743
    },
    {
      "run": "full_125_001",
      "selection": "original",
      "footing": "alt",
      "power": 1.25,
      "ell_kpc": 3.0,
      "n_pass": 0,
      "n_strict": 0,
      "best_D_index": 1335,
      "best_D": 1.0858123632331151
    },
    {
      "run": "full_125_001",
      "selection": "original",
      "footing": "alt",
      "power": 1.25,
      "ell_kpc": 3.5,
      "n_pass": 0,
      "n_strict": 0,
      "best_D_index": 1350,
      "best_D": 1.0460461281158864
    },
    {
      "run": "full_125_001",
      "selection": "original",
      "footing": "alt",
      "power": 1.25,
      "ell_kpc": 4.0,
      "n_pass": 0,
      "n_strict": 0,
      "best_D_index": 1348,
      "best_D": 1.264179121316525
    },
    {
      "run": "full_150_001",
      "selection": "original",
      "footing": "canonical",
      "power": 1.5,
      "ell_kpc": 1.5,
      "n_pass": 0,
      "n_strict": 0,
      "best_D_index": 1077,
      "best_D": 2.0268915718455425
    },
    {
      "run": "full_150_001",
      "selection": "original",
      "footing": "canonical",
      "power": 1.5,
      "ell_kpc": 2.0,
      "n_pass": 0,
      "n_strict": 0,
      "best_D_index": 1101,
      "best_D": 1.455360115041162
    },
    {
      "run": "full_150_001",
      "selection": "original",
      "footing": "canonical",
      "power": 1.5,
      "ell_kpc": 2.5,
      "n_pass": 0,
      "n_strict": 0,
      "best_D_index": 1359,
      "best_D": 1.3947239183915496
    },
    {
      "run": "full_150_001",
      "selection": "original",
      "footing": "canonical",
      "power": 1.5,
      "ell_kpc": 3.0,
      "n_pass": 0,
      "n_strict": 0,
      "best_D_index": 1348,
      "best_D": 1.592463668103916
    },
    {
      "run": "full_150_001",
      "selection": "original",
      "footing": "canonical",
      "power": 1.5,
      "ell_kpc": 3.5,
      "n_pass": 0,
      "n_strict": 0,
      "best_D_index": 1348,
      "best_D": 2.3438104844809255
    },
    {
      "run": "full_150_001",
      "selection": "original",
      "footing": "canonical",
      "power": 1.5,
      "ell_kpc": 4.0,
      "n_pass": 0,
      "n_strict": 0,
      "best_D_index": 1348,
      "best_D": 3.1324135914552826
    },
    {
      "run": "full_150_001",
      "selection": "original",
      "footing": "alt",
      "power": 1.5,
      "ell_kpc": 1.5,
      "n_pass": 0,
      "n_strict": 0,
      "best_D_index": 828,
      "best_D": 2.000894110103025
    },
    {
      "run": "full_150_001",
      "selection": "original",
      "footing": "alt",
      "power": 1.5,
      "ell_kpc": 2.0,
      "n_pass": 0,
      "n_strict": 0,
      "best_D_index": 912,
      "best_D": 1.4895955360367747
    },
    {
      "run": "full_150_001",
      "selection": "original",
      "footing": "alt",
      "power": 1.5,
      "ell_kpc": 2.5,
      "n_pass": 0,
      "n_strict": 0,
      "best_D_index": 1374,
      "best_D": 1.5843772635866504
    },
    {
      "run": "full_150_001",
      "selection": "original",
      "footing": "alt",
      "power": 1.5,
      "ell_kpc": 3.0,
      "n_pass": 0,
      "n_strict": 0,
      "best_D_index": 1350,
      "best_D": 1.5888001958847808
    },
    {
      "run": "full_150_001",
      "selection": "original",
      "footing": "alt",
      "power": 1.5,
      "ell_kpc": 3.5,
      "n_pass": 0,
      "n_strict": 0,
      "best_D_index": 1348,
      "best_D": 2.0673685454212722
    },
    {
      "run": "full_150_001",
      "selection": "original",
      "footing": "alt",
      "power": 1.5,
      "ell_kpc": 4.0,
      "n_pass": 0,
      "n_strict": 0,
      "best_D_index": 1348,
      "best_D": 2.9356314993337116
    },
    {
      "run": "full_175_001",
      "selection": "original",
      "footing": "canonical",
      "power": 1.75,
      "ell_kpc": 1.5,
      "n_pass": 0,
      "n_strict": 0,
      "best_D_index": 1050,
      "best_D": 2.3769239343648474
    },
    {
      "run": "full_175_001",
      "selection": "original",
      "footing": "canonical",
      "power": 1.75,
      "ell_kpc": 2.0,
      "n_pass": 0,
      "n_strict": 0,
      "best_D_index": 1068,
      "best_D": 1.909826792458605
    },
    {
      "run": "full_175_001",
      "selection": "original",
      "footing": "canonical",
      "power": 1.75,
      "ell_kpc": 2.5,
      "n_pass": 0,
      "n_strict": 0,
      "best_D_index": 1350,
      "best_D": 2.155690171273664
    },
    {
      "run": "full_175_001",
      "selection": "original",
      "footing": "canonical",
      "power": 1.75,
      "ell_kpc": 3.0,
      "n_pass": 0,
      "n_strict": 0,
      "best_D_index": 1354,
      "best_D": 3.1010715950499206
    },
    {
      "run": "full_175_001",
      "selection": "original",
      "footing": "canonical",
      "power": 1.75,
      "ell_kpc": 3.5,
      "n_pass": 0,
      "n_strict": 0,
      "best_D_index": 1354,
      "best_D": 4.710177574756811
    },
    {
      "run": "full_175_001",
      "selection": "original",
      "footing": "canonical",
      "power": 1.75,
      "ell_kpc": 4.0,
      "n_pass": 0,
      "n_strict": 0,
      "best_D_index": 1351,
      "best_D": 5.960057147979434
    },
    {
      "run": "full_175_001",
      "selection": "original",
      "footing": "alt",
      "power": 1.75,
      "ell_kpc": 1.5,
      "n_pass": 0,
      "n_strict": 0,
      "best_D_index": 831,
      "best_D": 2.1598040738638833
    },
    {
      "run": "full_175_001",
      "selection": "original",
      "footing": "alt",
      "power": 1.75,
      "ell_kpc": 2.0,
      "n_pass": 0,
      "n_strict": 0,
      "best_D_index": 915,
      "best_D": 1.8857333332987127
    },
    {
      "run": "full_175_001",
      "selection": "original",
      "footing": "alt",
      "power": 1.75,
      "ell_kpc": 2.5,
      "n_pass": 0,
      "n_strict": 0,
      "best_D_index": 1086,
      "best_D": 2.3785850994110835
    },
    {
      "run": "full_175_001",
      "selection": "original",
      "footing": "alt",
      "power": 1.75,
      "ell_kpc": 3.0,
      "n_pass": 0,
      "n_strict": 0,
      "best_D_index": 1354,
      "best_D": 2.617093342628075
    },
    {
      "run": "full_175_001",
      "selection": "original",
      "footing": "alt",
      "power": 1.75,
      "ell_kpc": 3.5,
      "n_pass": 0,
      "n_strict": 0,
      "best_D_index": 1354,
      "best_D": 4.148434202479544
    },
    {
      "run": "full_175_001",
      "selection": "original",
      "footing": "alt",
      "power": 1.75,
      "ell_kpc": 4.0,
      "n_pass": 0,
      "n_strict": 0,
      "best_D_index": 1354,
      "best_D": 5.836035460887706
    },
    {
      "run": "adaptive_125_mid_001",
      "selection": "adaptive",
      "footing": "canonical",
      "power": 1.25,
      "ell_kpc": 2.75,
      "n_pass": 0,
      "n_strict": 0,
      "best_D_index": 1368,
      "best_D": 1.01630314687225
    },
    {
      "run": "adaptive_125_mid_001",
      "selection": "adaptive",
      "footing": "alt",
      "power": 1.25,
      "ell_kpc": 2.75,
      "n_pass": 0,
      "n_strict": 0,
      "best_D_index": 1344,
      "best_D": 1.0984777562406671
    },
    {
      "run": "adaptive_1125_001",
      "selection": "adaptive",
      "footing": "canonical",
      "power": 1.125,
      "ell_kpc": 3.0,
      "n_pass": 32,
      "n_strict": 0,
      "best_D_index": 1368,
      "best_D": 0.8333679968169017
    },
    {
      "run": "adaptive_1125_001",
      "selection": "adaptive",
      "footing": "alt",
      "power": 1.125,
      "ell_kpc": 3.0,
      "n_pass": 20,
      "n_strict": 0,
      "best_D_index": 1287,
      "best_D": 0.8999953099681948
    }
  ],
  "refinement": {
    "rows_regraded": 60,
    "positive_infinite_h_count": 0,
    "max_grade_scalar_relative_error": 0.0,
    "max_fitted_slope_absolute_error": 8.881784197001252e-16,
    "max_h_relative_error": 4.871302975605002e-15,
    "flag_or_summary_mismatches": 0,
    "max_coarse_literal_relative_error": 3.0567027340272155e-10,
    "selected": [
      {
        "footing": "alt",
        "power": 1.125,
        "ell_kpc": 3.0,
        "index": 1287,
        "pass_configurations": 6,
        "strict_configurations": 0,
        "min_D": 0.8999953099332005,
        "max_D": 0.9078168771316215,
        "finest": {
          "vc": 229.26398331231528,
          "K0": 70.39439425937914,
          "cK": 60.25406869553288,
          "cO": 17.692245380148172,
          "h": 3.524305996274863,
          "D": 0.9078168771316215,
          "all_four": true,
          "Lh": false
        }
      },
      {
        "footing": "alt",
        "power": 1.25,
        "ell_kpc": 2.75,
        "index": 1344,
        "pass_configurations": 0,
        "strict_configurations": 0,
        "min_D": 1.0984777563895614,
        "max_D": 1.1110713400843217,
        "finest": {
          "vc": 233.62939001468422,
          "K0": 71.28871389637102,
          "cK": 71.81928080864327,
          "cO": 22.404368162365838,
          "h": 3.7433244011929743,
          "D": 1.1110713400843217,
          "all_four": false,
          "Lh": false
        }
      },
      {
        "footing": "alt",
        "power": 1.25,
        "ell_kpc": 3.5,
        "index": 1350,
        "pass_configurations": 0,
        "strict_configurations": 0,
        "min_D": 1.0460461281038214,
        "max_D": 1.0475454271999438,
        "finest": {
          "vc": 229.25063153250227,
          "K0": 69.8799824738424,
          "cK": 70.66673143792244,
          "cO": 36.172394583725755,
          "h": 3.520937061792942,
          "D": 1.0475454271999438,
          "all_four": false,
          "Lh": false
        }
      },
      {
        "footing": "alt",
        "power": 1.5,
        "ell_kpc": 2.0,
        "index": 912,
        "pass_configurations": 0,
        "strict_configurations": 0,
        "min_D": 1.488402120490752,
        "max_D": 1.4967491819876597,
        "finest": {
          "vc": 224.54794651789712,
          "K0": 72.98569640074571,
          "cK": 100.32866119496303,
          "cO": 81.91812589318295,
          "h": 4.8403702671324425,
          "D": 1.4967491819876597,
          "all_four": false,
          "Lh": false
        }
      },
      {
        "footing": "alt",
        "power": 1.75,
        "ell_kpc": 2.0,
        "index": 915,
        "pass_configurations": 0,
        "strict_configurations": 0,
        "min_D": 1.8857333332442565,
        "max_D": 1.9031413503651249,
        "finest": {
          "vc": 227.39175583991863,
          "K0": 74.77382194160656,
          "cK": 126.9996238241505,
          "cO": 89.99667039979227,
          "h": 6.538178784576765,
          "D": 1.9031413503651249,
          "all_four": false,
          "Lh": false
        }
      },
      {
        "footing": "canonical",
        "power": 1.125,
        "ell_kpc": 3.0,
        "index": 1368,
        "pass_configurations": 6,
        "strict_configurations": 0,
        "min_D": 0.8333679968096336,
        "max_D": 0.8351674143759037,
        "finest": {
          "vc": 228.89907170680618,
          "K0": 69.11297694165924,
          "cK": 56.339849179773346,
          "cO": 15.344798406826644,
          "h": 3.347210230955883,
          "D": 0.8351674143759037,
          "all_four": true,
          "Lh": false
        }
      },
      {
        "footing": "canonical",
        "power": 1.25,
        "ell_kpc": 2.5,
        "index": 1317,
        "pass_configurations": 0,
        "strict_configurations": 0,
        "min_D": 1.0243572389644133,
        "max_D": 1.0260347663020597,
        "finest": {
          "vc": 228.44736925467413,
          "K0": 70.8488102180988,
          "cK": 69.2156362803729,
          "cO": 19.220955109662494,
          "h": 3.7076227285060446,
          "D": 1.0260347663020597,
          "all_four": false,
          "Lh": false
        }
      },
      {
        "footing": "canonical",
        "power": 1.25,
        "ell_kpc": 2.75,
        "index": 1368,
        "pass_configurations": 0,
        "strict_configurations": 0,
        "min_D": 1.0163031468647528,
        "max_D": 1.0193480467010294,
        "finest": {
          "vc": 229.99420047806566,
          "K0": 69.34610125336539,
          "cK": 68.76455453634797,
          "cO": 10.66981628087434,
          "h": 3.5036265519420127,
          "D": 1.0193480467010294,
          "all_four": false,
          "Lh": false
        }
      },
      {
        "footing": "canonical",
        "power": 1.5,
        "ell_kpc": 2.5,
        "index": 1359,
        "pass_configurations": 0,
        "strict_configurations": 0,
        "min_D": 1.394723917965224,
        "max_D": 1.4225406686172577,
        "finest": {
          "vc": 231.96720315568973,
          "K0": 72.65917894191594,
          "cK": 94.46543990593231,
          "cO": 12.475544407495711,
          "h": 4.048695462752714,
          "D": 1.4225406686172577,
          "all_four": false,
          "Lh": false
        }
      },
      {
        "footing": "canonical",
        "power": 1.75,
        "ell_kpc": 2.0,
        "index": 1068,
        "pass_configurations": 0,
        "strict_configurations": 0,
        "min_D": 1.9098267924859091,
        "max_D": 1.9480767497715556,
        "finest": {
          "vc": 227.83127085865777,
          "K0": 74.97153769899485,
          "cK": 128.18363442669056,
          "cO": 98.54995167146784,
          "h": 6.073954035156907,
          "D": 1.9480767497715556,
          "all_four": false,
          "Lh": false
        }
      }
    ]
  },
  "input_sha256": {
    "rebuild_2026_10_22/KT39_power_curvature/mw/checks_1125_001/manifest.json": "924ed315ec7b49a2078c5800d2e5650061358ef61199d56c004ef45eb00b5dcb",
    "rebuild_2026_10_22/KT39_power_curvature/mw/checks_1125_001/results.json": "91a9017cd04aabcae243cd2703271929f77e0b57d15bd7a7b8a0a897f26091e4",
    "rebuild_2026_10_22/KT39_power_curvature/mw/checks_125_001/manifest.json": "6d1bb40519b440455aba8b5c3eb188a424bf3888e600647e881850a450b53a02",
    "rebuild_2026_10_22/KT39_power_curvature/mw/checks_125_001/results.json": "bef0656ef019fa0c9c25fe8195445b41de6d45f0fab390da03bb692cd47ae141",
    "rebuild_2026_10_22/KT39_power_curvature/mw/checks_150_001/manifest.json": "1be929272f692418ebb82698c409a775d4455add831d2a36fcbb1bc38914ef82",
    "rebuild_2026_10_22/KT39_power_curvature/mw/checks_150_001/results.json": "b46825a8252f432d4cb5e98f21b83a98a25ecea47527cf95cb31e33ae4451083",
    "rebuild_2026_10_22/KT39_power_curvature/mw/checks_175_001/manifest.json": "467f640041afed03f0b3d7c917a9a78950b1fcc18acefb00a3b630284318df0a",
    "rebuild_2026_10_22/KT39_power_curvature/mw/checks_175_001/results.json": "79370a49bffdad428d491b05ee17f89b6fa718e5797869b4d219a2b438edb368",
    "rebuild_2026_10_22/KT39_power_curvature/mw/full_125_001/manifest.json": "689350814fdf760aa43dcb8865b85d3f56979a550039d42984d5feafbf50eb4c",
    "rebuild_2026_10_22/KT39_power_curvature/mw/full_125_001/results.json": "98dda4cb36e40d483ef0f8dfb0aa6696a3c046bd7886f44f0bffadb1a877cd9f",
    "rebuild_2026_10_22/KT39_power_curvature/mw/full_150_001/manifest.json": "237d955f60bb8863c101645af58f3dd3e4e04c394281fcc43ee87c321ccfd7d7",
    "rebuild_2026_10_22/KT39_power_curvature/mw/full_150_001/results.json": "e1f49b28d4202794a0f5817d7762ef575761f3c0a11c0cd9bf6bfd4cc2b2f4d2",
    "rebuild_2026_10_22/KT39_power_curvature/mw/full_175_001/manifest.json": "bcc613d67a180db63cd4826401d3c25a5da302ecb871fc8be8097dccaba434eb",
    "rebuild_2026_10_22/KT39_power_curvature/mw/full_175_001/results.json": "390959ecd3546ad6f266dd1ac6c4722eb92fae3e803f91f30b5327f4b1882a2c",
    "rebuild_2026_10_22/KT39_power_curvature/mw/adaptive_125_mid_001/manifest.json": "2dddbcd93e44c3de49229ffb1b3a10c3b610f66e38a67ed27928e11c08117860",
    "rebuild_2026_10_22/KT39_power_curvature/mw/adaptive_125_mid_001/results.json": "1db440c906b125f9091b13243e63bea344d20731b655292f0cfe670dcf8bdad4",
    "rebuild_2026_10_22/KT39_power_curvature/mw/adaptive_1125_001/manifest.json": "fe6eee1f96dfd286d043ec3b6231adf1da9503a0344cd3f49b42b87fed8ddb52",
    "rebuild_2026_10_22/KT39_power_curvature/mw/adaptive_1125_001/results.json": "43b098d13d55a07c32266ee827993a0f9b20d9fb8c095b95fb94f4523491b6ee",
    "rebuild_2026_10_22/KT39_power_curvature/mw/refine_001/manifest.json": "96c584a454b42b18de4e41af783883875eb7652c4726aff1ee89f0619e7be791",
    "rebuild_2026_10_22/KT39_power_curvature/mw/refine_001/results.json": "49f5ebce930fcc657d25a1128cefe3af9d9a6a74aad4b91e660c4c86e6068b88",
    "rebuild_2026_10_22/KT39_power_curvature/mw/power_model.py": "65ea05e7e18dd98624f37340fc9169447d06faecbb819a07d13438f5603dddbf",
    "rebuild_2026_10_22/KT39_power_curvature/mw/checks.py": "82190775f178c8d7e205c1c6337b282bd84acbb439153a9af2f5cb197b39458d",
    "rebuild_2026_10_22/KT39_power_curvature/mw/search.py": "c6a96ec31afbd19e7d85e20c99ef6b310216a9d3c1a3ac4ecf062a2b8654ed96",
    "rebuild_2026_10_22/KT39_power_curvature/mw/refine.py": "5462d3df569433b32522e27da6fee5295b0b8ceee4aa4f4de2debcca7a4b7e4f",
    "rebuild_2026_10_22/KT39_power_curvature/mw/selection.json": "19759ddb1c0999dd1d19ce123505e969e4a67cbb8781b729d4ab893b4af05b2b",
    "rebuild_2026_10_22/KT39_power_curvature/mw/verify_review.py": "6962ea0278d256745fb137b29ef6c8ec7a04c0099ccb38da9f3f9a42210d5b12",
    "rebuild_2026_10_22/KT39_power_curvature/PLAN.md": "52c3bfa59f22cf53768f5dc7cd7280945da95ebd327eddcf126bb08ff3007332",
    "rebuild_2026_10_22/KT39_power_curvature/ADAPTIVE_PLAN.md": "c32018e520b07805190dd92e5a5107ff425ba1132fd65de1ef27926ebb5a9678",
    "rebuild_2026_10_22/KT39_power_curvature/analytic/law.py": "52a5f9bece8f46aa307f320fe2bb8418b04d581e7d53801518d8448ea2952390",
    "rebuild_2026_10_22/KT37_generalized_action/mw/generalized_v3.py": "9eecef18bf2dc9d7aec27bd34a3107bad6e0c3e664e1d71d2c8a9b04035a5f13",
    "rebuild_2026_10_22/KT37_generalized_action/analytic/law.py": "7a7f4710cacb6b33a88e170147c64eb6554ba44f6fda1fc81104bea5a222740f"
  }
}
```
