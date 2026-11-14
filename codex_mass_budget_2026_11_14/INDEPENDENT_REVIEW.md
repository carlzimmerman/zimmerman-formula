# Independent review of the mass correction and transport continuation

2026-11-14. Reviewer: fresh subagent `/root/independent_final_review`, using
proof-audit and computation-audit. Raw source files were read before the
author's reports; the critical algebra and current signs were independently
derived. No existing scientific source or output was edited by this reviewer.

**Primary mathematical verdict: proved as written under the stated hypotheses.**
This verdict covers the corrected common-radius identities, static junction,
distributional current condition, and the revised continuity-only transport
theorem. It does not certify the field theory, dynamic settling, observational
selection, or an equality between every mode-B profile and the algebraic law.
The numerical work was audited against authenticated outputs, not rerun here.

## Original review and resolved findings

No remaining mathematical blocker was found. The original review identified
an overclaim in the new CJ1/PAPER72 correction: XJ1 was said to preserve the
"inner law." This has been corrected to preservation of the supplied B
interior, with algebraic-law equality explicitly separated
(`COMPLETED_FORM.md:60`, PAPER72 TeX line 413).

At a common radius, the premises give

    g_N = G M_b/r_200^2 = 10 H v_200/q,
    a0/g_N = q^2 vstar/v_200,
    M_deep/(q M_b) = sqrt(vstar/v_200),
    M_exact/(q M_b) = [1+sqrt(1+4q^2 vstar/v_200)]/(2q).

Thus the exact equality is v_200/vstar=q/(q-1)=1.184842884 for q=6.41.
The corrected inequality direction and its same-radius qualification are
correct. Eliminating a condensed source M_cond=eta M_b,patch also independently
gives v_intersection=eta a0/(10qH). The calculation correctly distinguishes
eta based on Mta from eta based on M200c; neither is promoted to a new switch.

| Obligation / dependency | Result |
|---|---|
| FRZ1 source definitions -> reconstructed B, FZS1 and JNT2 profiles | Passed code inspection; reconstruction and conserved-mass errors match saved results |
| Msun/h and comoving Mpc/h -> physical force residual | Passed; h and (1+z)^2 factors agree with raw FRZ1/CFG556 definitions |
| Retained baryons, all explicit Bar, cosmic patch cold, implemented non-Bar reservoir | Kept distinct; cluster outer-envelope baryons are disclosed |
| Reported mass tables and three worked examples | Match detailed CSV rows and summaries |
| Coverage | 10,272 mass/junction evaluations; 2,568 distinct source-scope cases; no extrapolation to untested populations |
| Static XJ1 matching | Follows from nonnegative t, continuity at R, common endpoint charge and spherical Newtonian force |
| Exact interface current | [J^r]-Rdot[J^t]=0; QX17 E3 current and E2 stationary-interior restriction match original source |
| Restricted no-go | Correct for the stated stationary, polarization-free exterior case; moving/full-current completions remain open |
| Newtonian N as advected and gravitating density | Conditional on the named COL1 reduction; no independent recertification of that reduction |
| Snapshot density counts | 7,110 selected profiles; numerical diagnostics, not tracked halo histories or abundance fractions |
| WLJ1 regressions | Seven tests passed; actual grader, realistic copied inputs, both footing directions, six historical outputs reproduced byte-for-byte |

WLJ1 was executed with `/private/tmp/forj0332-fit-venv/bin/python -I -B
test_wlj1_grade.py -v` from its lane directory: seven tests, 13.966 seconds,
exit 0. The tests exercise frozen/amended reference tolerance, failures of
non-reference known answers, unaffected opposite-footing gates, and stale
global summaries. They do not rerun upstream numerical stages.

Calculation stages 1-4 were read, including the late source-scope and figure
additions. Their v2 manifests validated against the actual repository root.
The single plotted galaxy example uses the correct saved row and physical
units; it is illustrative, not added coverage. Latest-review run_005 originally
validated, then became stale after the corrected CJ1 prose changed. Final
run_007 was separately validated and resolves that provenance issue.

The historical CJ1 snapshot matches source revision
759e17e27c01186d131e869aee6eb04de6f9bbb1 and SHA-256
46ec42b18d8da41acc5a29d14f07d7fd4e11c105fdda66f11e1fcdb0c527cc24.
The main PAPER72 audit requires committed source copies. Its final execution
in a genuine scoped Git checkpoint is the coordinator's verification, not a
success claimed by this independent review of the dirty shared checkout.

## Addendum: constructive transport

The initial transport statement allowed any differentiable schedule. The
review found that insufficient for ordinary weak conservation: a bounded,
differentiable schedule can have a time derivative that is not locally
integrable. The author restricted `TRANSPORT_PATH.md:25` to continuously
differentiable schedules. This is a substantive hypothesis restriction,
now satisfied by the proposed exponential schedule.

For the revised theorem, let Delta=C_E-C_R. Independent calculation gives

    C_t + v C_r = a_dot Delta - a_dot Delta = 0,
    4 pi r^2 N v = -a_dot Delta.

Absolute continuity and common zero/T endpoints make Delta continuous with
zero boundary traces. The flux therefore matches across fixed density jumps
and vanishes through the origin and outer boundary. Convexity preserves
nonnegative density; C_R'>0 almost everywhere makes every finite-time
mixture positive almost everywhere. These statements justify weak spherical
continuity without assuming the interior already stands still.

For a=1-exp(-t/tau), tau>0,

    |v| <= |Delta|/(tau C_R') <= B/tau

holds essentially wherever the stated B is finite. Positivity alone does
not imply this bound. On a target plateau C_E'=0 with Delta nonzero,
v=-Delta/(tau C_R') need not tend to zero although density and flux do.
The theorem explicitly states this caveat. Its linear-schedule divergence
and restriction to this fixed interpolation family are also correct.

The 36 exact rational trace checks cover both sides of the capped example's
density jump. They support the implementation of the identities; the uniform
claim follows from the written proof, not sample counts. Run_007 records
those checks and the unchanged 7,110-profile audit, status `completed`,
runtime 8.964337 seconds. Its manifest validated against the current root.

No remaining addendum blocker. The strongest safe conclusion is existence
of this positive, charge-conserving kinematic path under its hypotheses,
with a conditional essential velocity bound and asymptotic target arrival.
Tau is arbitrary. QX17/COL1 force and constitutive relations, stress, energy,
stability, and a derived target/caustic selector remain open. The next useful
check is a field-equation residual for one specified path and actual source
budget; another survey gate cannot supply those missing implications.

## Exact reviewed versions

The shared HEAD advanced during review; per-file SHA-256 values identify the
versions reviewed. Paths in the first six rows are repository-relative; the
remaining paths are relative to `codex_mass_budget_2026_11_14/`.

| Artifact | SHA-256 |
|---|---|
| closure_2026_11_13/CJ1_candidate_completion/COMPLETED_FORM.md | caeab2fe7f6cd061b36ed3b161e3b58dae2a1ea84bf75befc3d41e6b15c3a189 |
| closure_2026_11_13/CJ1_candidate_completion/SCORECARD.md | feac7362d27c3e0fd103f413d5d1ab21bfe5db00239c3fe7bc76a4fb5b02a085 |
| qwen_claude_field_theory/papers_2026/PAPER72_audit.py | dd46c6bfb4c3fbd4abe826eec86dd12efa51f0fdad6f824bb4324667a4759e4c |
| qwen_claude_field_theory/papers_2026/PAPER72_law_with_cold_dark_energy_counted_once_2026.tex | fe386f6cf5c4732c28b72e71b3ad58f57d2be78d77fa1f28be73ea8b2c549bd8 |
| closure_2026_11_13/WLJ1_power_and_lensing_amplitude_with_split/test_wlj1_grade.py | def3f269d3ca2d30e5d2d2b1fa6a7f2c49dc5bcd70b22cbb95cd9d5f5dca5889 |
| closure_2026_11_13/WLJ1_power_and_lensing_amplitude_with_split/wlj1_grade.py | c77e6f2dd41084287ff102066d77ceb38e6f0c52c1bade62cb4251e3e2b5bb80 |
| calculation/calculate.py | 012a11800cb29cf12825bdf6c5506c66428f4c3f78296a58ba7b65c9425f5852 |
| calculation/analyze_sources.py | 540dd2d35077aae0d8ca420f3549b55ac8e4b679221557de65589391dc2693a0 |
| calculation/check_crossing_scope.py | a50bb8f4d6d8889aca2a03af5d08a8da544db29d93cb11503a2f60715c8b965c |
| calculation/plot_example.py | e41e66dbf3802a097dafa7d77878f73711b261025ca907fd83a1f329fded847d |
| calculation/README.md | 76fa4b8ef28776e02ebbffb8bd19884bc6884cf69f9e183e4f48c7ba384345c0 |
| calculation/run_001/manifest.json | 4b01f32f4364fcee9de32706d2e9cbba0a69b573f18aa2937d5de3f43772988f |
| calculation/run_002/manifest.json | 2c6f6b0267bc68f07b28143a1a43e1f199fe866745834245c8bd2b36a53b5526 |
| calculation/run_003/manifest.json | 1aad45796290f9a381baa4d683a9dce3da961a089c492297993375231b7175f4 |
| calculation/run_004/manifest.json | 6396b06652c87d319bd32ffd6416b718b58e6d1981cbba549a296298b1e2425a |
| latest_review/JUNCTION_THEOREM.md | adb8f749a593be6d810805173410cdedc7e9984aedc92fcdb35ae3c24eb9163b |
| latest_review/TRANSPORT_PATH.md | 118075248aa07e210ea9bd495474915656b340f3f915fd059a9e0cafa2f829f3 |
| latest_review/check_junction.py | f5d4e490422b7d5e887615dfd170c7b1887fdb4ed88026b9f5b0745141cd4176 |
| latest_review/REVIEW.md | 954bd6c0b59a1a7619b28c1cbd334075d172d06ff57dedd7be0fdbfabe62f414 |
| latest_review/run_007/manifest.json | 6e4d75100fc5fdcab2df40cba37305ca0210d9151ee755c8e2a13e75f952c913 |

Self-proofreading of this review covered all new prose, formulas and source
locators. No mathematical-token correction was required during proofreading;
the substantive C1 restriction above was a proof-audit finding, accepted and
implemented by the author before the final review.

## Final addendum: finite-charge radius bound

Independently reviewed `calculation/BUDGET_BOUND.md` and
`budget_bound_v2.py`. No blocker: the pointwise criterion and first-crossing
consequence are proved under the stated hypotheses. For fixed b>=0,
F(x)=x(x+b) is strictly increasing on x>=0, so

    C(C+b)=(a0/G)b r^2,
    C<=Q iff (a0/G)b r^2<=Q(Q+b).

For fixed b>0 this gives R_budget=sqrt[GQ(Q+b)/(a0 b)]. The partial
derivatives in the proof are correct; strict radial positivity requires
r>0 and b>0. Their coordinatewise monotonicity and continuity justify the
composite result for continuous nondecreasing b(r), without differentiating
b. A positive-charge crossing is unique. The allowed set can instead be
the whole finite patch, and the identically zero source has C=0. The fixed-b
formula is correctly distinguished from a distributed-source implicit root.

The code uses physical kpc/Msun, actual analytic baryon-source functions,
cosmic patch cold Q, and explicitly separate retained/all-Bar conventions.
Its 64 representative halos produce 128 source rows, with 76 inside-patch
crossings. All eight displayed example rows match the saved results.
The two root formulations agree to 9.92e-13 relative and the maximum charge
residual is below 1.02e-12. The v2 change only converts NumPy scalars for
JSON; the failed run_005 is preserved. The final run_006 manifest was
independently revalidated against the current root after that source split.
No numerical experiment was rerun by this reviewer.

The result is a necessary budget condition, not a sufficient settling,
stability, or field-equation solution, and it does not adopt a minimum of
caustic and budget radii as a physical switch. Earlier hash records above
are preserved; this addendum records the later README revision separately.

| Artifact, relative to codex_mass_budget_2026_11_14/ | SHA-256 |
|---|---|
| calculation/BUDGET_BOUND.md | ca5d5586eb7b9bf1c4ac2cf9a5f9da311bde241534312ceb3240ab0b99f53afe |
| calculation/budget_bound_v2.py | f7d6d7472c5f2e66e0f085d9814ad698939f53938959c59ce74a0faf5c1b64f6 |
| calculation/run_006/manifest.json | b1f43a7fa7c13938f2ab88e94eed7744ecd70dcb77778e00d02a0c5f48200f35 |
| calculation/run_006/results.json | 12bd552692216c9e4e7b7d0659bddc09a28d58adada4acebcf2905ae5dba88ad |
| calculation/README.md | ce60edb44ffa69268e061374dff8125f74b8885c429941bb69c704ec60585ffc |

Self-proofreading of this addendum found no further mathematical-token or
prose correction. The numerical coverage remains representative and finite.
