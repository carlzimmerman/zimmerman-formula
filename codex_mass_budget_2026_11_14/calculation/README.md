# Actual enclosed-mass audit of the FZS1/JNT2 prescription

2026-11-14. **Outcome: implementation and finite assertion verified on the stated grid. The existing prescription conserves its patch mass, but its inner profile does not generally satisfy the unscaled standing-clock force law.** This is a diagnostic of the prescribed profiles, not a dynamical derivation, a fit, or an adoption of a replacement theory.

Constructive follow-up: `BUDGET_BOUND.md` proves the exact pointwise raw-law charge inequality and its first-crossing consequence, with source-specific allowed radii on 64 representative actual halos in `run_006`. This constrains any claimed raw-law interior without proposing a new physical switching rule. `run_005` preserves a failed JSON-serialization attempt; the corrected bounded run is `run_006`.

## Contract, scope, and source conventions

`contract.json` was written before the calculation. `calculate.py` executes the actual JNT2 definitions before its run loop; those load the unmodified FZS1, FRZ1 and CFG556 prefixes. It runs all **321** halo masses, uniformly spaced in log10 M200m from 8 to 16 in Msun/h, at z = 0, 2.2, 3, 4.4, on canonical and alt separately, for f = 1.25, 2, 3, 5. This is **10,272 halo/junction evaluations**, each using the original 1,600 logarithmic radial points plus zero and inserted layout/junction nodes. No mass was skipped. There are no power-spectrum or box simulations. `source_contract.json` precedes the independent physical-unit check in `analyze_sources.py`.

Masses returned by the halo code are **Msun/h**; divide by h = 0.6736 for physical Msun. Radii are comoving Mpc/h; physical kpc are 1000 r / [h(1+z)]. The code uses a0/(1+z)^2 in the comoving force law. The original G is 4.30091e-9 Mpc (km/s)^2/Msun. The second calculation independently converts to physical kpc, Msun and G = 4.30091e-6.

There are three distinct mass ratios, which must not be substituted for one another:

- JNT2's crossing-speed lemma uses X = 5.41.
- The halo grid's cosmic cold/baryon ratio is omega_c/omega_b = 0.1200/0.02237 = 5.364327224. Its FB is 0.15712579897450307.
- The galaxy layout reads **Xsh = 59.486123715 / 59.502850378 at z = 0, and 55.715882477 / 55.731266185 at z >= 1**, canonical/alt. These are the medians of PD1's `share_over_Mb` Lagrangian-share tables, not the cosmic ratio. FRZ1 uses the z = 1 table at every z >= 1.

For the galaxy branch, the actual source assigned to the central baryon point is

    C_patch = (1-FB) Mta,
    Mb = C_patch/Xsh,
    Bar(r) = Mb + [FB Mta - Mb] M_NFW(r)/Mta.

`Mb_fold` equals this **retained central baryon proxy**, which is also the input to FLD1's radius interpolation. It is not a measured stellar mass and is not the total patch baryon mass FB Mta. The rest of the baryons remain distributed in `Bar`. For clusters, `Mb_fold = FB M200c`, while the instantaneous raw-law source is the distributed `Bar(r)`.

Another distinction matters on the cluster branch. FZS1 defines `C_R = M_R - Bar`, but `Bar(rta) = FB M200c`. Thus its implemented non-Bar reservoir is

    C_R(rta) = Mta - FB M200c
             = (1-FB) Mta + FB(Mta-M200c).

It includes nominal baryons in the outer NFW envelope. The CSV reports this reservoir, the true cosmic patch cold amount `(1-FB)Mta`, and the outer-baryon difference separately. The second run's “allbar” means all **explicit `Bar` baryons**; on clusters it does not silently reclassify the outer envelope as baryons. On every active high-z halo the branch is galaxy, so `Bar` is the complete modeled baryon source there.

## What was actually compared

For source baryon mass b(r), the unnormalized exact-law cold mass is the positive solution

    C_exact(r) = [sqrt(b(r)^2 + 4 b(r) a0 r^2/(G h)) - b(r)]/2.

The implementation uses its rationalized equivalent, and checks it against FRZ1's original `phantom` and against the force-law polynomial. It then compares five different objects at the exact inserted R_set node:

1. `C_exact`, with the source actually passed to FRZ1's law term;
2. `C_B = M_B - Bar`, the existing form-B profile, including its cap, leftover, and cluster components;
3. `C_R = M_R - Bar`, the reference enclosed profile;
4. the final FZS1/JNT2 enclosed mass;
5. the true cosmic patch charge and the implemented non-Bar reservoir.

The galaxy form-B cold profile is `min(C_exact,C_patch) + rem*r/rta`, with `rem = max(C_patch-C_exact(rta),0)`. The cluster version additionally contains the pre-collapsed NFW contribution, pressure factor W, and the outer envelope. Therefore “unscaled B” and “unscaled exact law” are already different objects in some cases, even before FZS1's rescaling.

FZS1's exact junction prescription is

    s = C_R(R_set)/C_B(R_set),
    C_S(r) = s C_B(r),  r <= R_set,
           = C_R(r),    r > R_set.

JNT2 uses this below its speed threshold and the reference profile at all radii above it. The CSV records nominal R_set even for above-threshold halos, but their **effective JNT2 R_set is zero**. Summary tables labeled active include only below-threshold halos.

The force residual is `epsilon = g^2/[g_N(a0+g)] - 1`. It vanishes for an exact standing-clock-law solution. Both source choices are disclosed: retained source used by the FRZ1 phantom term, and all explicit `Bar` baryons. The second run also isolates the retained-core-plus-scaled-cold contribution, removing the uncondensed baryon force. None is conflated with a charge-conservation test.

## Finite results

Every actual FZS1 and JNT2 profile conserves total patch mass to relative **6.67e-16** on this grid. The independently reconstructed B profile agrees to **4.58e-16** of Mta; independently reconstructed FZS1 and JNT2 agree to **2.04e-16**. All checked total profiles are nondecreasing up to roundoff. The raw-law polynomial residual is at most **1.12e-15**. The independent physical-unit residual differs from the comoving calculation by at most **8.89e-15**.

These numerical checks establish that the following changes to the force law are features of the prescription, not conversion or reconstruction errors.

The active-halo `s` range at f = 2 is:

| z | canonical active | canonical s | alt active | alt s |
|---|---:|---:|---:|---:|
| 0 | 240 | 0.5703–1.0455 | 250 | 0.5656–1.0000 |
| 2.2 | 151 | 0.4817–1.7110 | 161 | 0.4378–1.6948 |
| 3 | 129 | 0.6004–1.7055 | 139 | 0.5454–1.6861 |
| 4.4 | 98 | 0.7386–1.6310 | 108 | 0.6694–1.5988 |

The number of active halos for which the **raw law with the retained source actually used by FRZ1** exceeds the entire cosmic patch cold amount at R_set is:

| z, footing | active | f=1.25 | f=2 | f=3 | f=5 |
|---|---:|---:|---:|---:|---:|
| 0 canonical | 240 | 87 | 172 | 213 | 240 |
| 0 alt | 250 | 101 | 186 | 228 | 250 |
| 2.2 canonical | 151 | 0 | 0 | 41 | 96 |
| 2.2 alt | 161 | 0 | 0 | 52 | 106 |
| 3 canonical | 129 | 0 | 0 | 0 | 57 |
| 3 alt | 139 | 0 | 0 | 0 | 68 |
| 4.4 canonical | 98 | 0 | 0 | 0 | 0 |
| 4.4 alt | 108 | 0 | 0 | 0 | 0 |

This does **not** say the implemented profiles exceed their budgets: the cap and junction prevent that. It says a literal raw standing-law extension to the prescribed R_set is sometimes unavailable from the assigned patch charge. In the point-source galaxy case the exact necessary budget bound is

    R_set <= R_charge = sqrt[G C_patch(C_patch+Mb)/(Mb a0)]

in physical consistent units. That is FRZ1's existing truncation radius, not JNT2's crossing-speed criterion. The second CSV records the radius and R_set/R_charge. For a distributed cluster source the same fixed-source radius is only a diagnostic, as explicitly marked in its result.

If instead the exact law is required for **all explicit Bar baryons**, the cold-charge demand at R_set is larger. At f = 2 its range and number above the cosmic patch budget are:

| z | canonical demand / patch | canonical exceeding | alt demand / patch | alt exceeding |
|---|---:|---:|---:|---:|
| 0 | 1.081–8.633 | 240/240 | 1.059–9.496 | 250/250 |
| 2.2 | 0.474–1.978 | 81/151 | 0.469–2.179 | 91/161 |
| 3 | 0.386–1.122 | 30/129 | 0.382–1.237 | 44/139 |
| 4.4 | 0.164–0.316 | 0/98 | 0.162–0.349 | 0/108 |

For example, on canonical at z = 0, M200m = 10^12 Msun/h, f = 1.25, the retained Mb is 3.45546e10 physical Msun and R_set = 186.3869 kpc. In Msun/h, raw exact cold and B cold are 5.932716e11, while reference and final cold are 5.677156e11; the patch cold amount is 1.384596e12. Here s = 0.9569235. Despite exact patch conservation, the final force residual at the join is +0.2372479 against the retained source and -0.7591404 against all explicit Bar baryons. At f = 3, the raw cold becomes 1.439923e12, above the patch amount; B caps it at 1.384596e12, and FZS1 reduces the join mass to 9.498363e11, s = 0.6860026.

At z = 2.2, M200m = 10^11 Msun/h, f = 1.25, canonical has R_set = 31.5901 kpc. Raw/B cold are 3.883192e10 Msun/h, reference/final cold 5.502957e10, and patch cold 2.036278e11. Here s = 1.4171219: the junction increases the inner cold profile despite ample total patch charge. The all-Bar force residual remains -0.3121197. Both suppression and enhancement occur in the actual grid.

## Common-r200 benchmark and XJ1 boundary

For the independent common-r200 benchmark only, write q = 1+X, M200 = q Mb, and vstar = a0/(10 q H). Then

    M_law,deep(<r200)/M200 = sqrt(vstar/v200),
    M_law,exact(<r200)/M200 = [1+sqrt(1+4q^2 vstar/v200)]/(2q).

At v200/vstar = 0.5, 1, 2, the exact ratios are 1.494366, 1.081041, 0.789399. The exact equality is at v200/vstar = q/(q-1) = 1.184842884. Thus the common-radius comparison has **greater demand below**, not above, the speed crossing. This benchmark is checked independently in SI for both footings and all four redshifts. It does not establish a global budget statement and does not replace the actual R_set calculation above.

There is also a conditional source-scope identity. If the baryons used in the flat-speed law are condensed baryons `M_cond = eta M_b,patch`, while `M_patch = q M_b,patch`, then equating

    v^3 = 10 G (q/eta) M_cond H,
    v^4 = G M_cond a0

gives **v_intersection = eta a0/(10 q H)**. The original unmodified speed requires eta = 1 under that common-patch convention, or applying the law to the entire patch baryon mass. `run_003` verifies the identity in 32 SI cases (both footings, four redshifts, eta = .05, .1, .5, 1) to 6.67e-16 and records the actual mass-scope ratios for all 2,568 distinct halo/redshift/footing cases.

For the actual galaxy layouts,

    eta_lagrangian = Mb/[FB Mta] = [(1-FB)/FB]/Xsh,
    eta_200c = Mb/[FB M200c] = eta_lagrangian Mta/M200c.

The first is 0.0901778 / 0.0901524 at z = 0 and 0.0962800 / 0.0962535 at z >= 1. The second varies with mass: 0.1615–0.2069 / 0.1615–0.2086 on the z = 0 galaxy branches, and 0.2340–0.3286 / 0.2340–0.3321 at z = 4.4. JNT2 uses M200c for its speed but assigns the galaxy law's Mb from Mta. Therefore replacing eta_200c with the constant eta_lagrangian would introduce another scope mismatch. For illustration only, inserting the actual z = 0 M200c/Mb ratios into the conditional identity gives 108.8–139.3 / 131.4–169.8 km/s rather than 668.5 / 807.9. These are **not proposed replacement switches**: the identity assumes a common patch/radius and flat-speed law, while the actual code has a distributed baryon component, truncation, differing Mta/M200c scopes, and slightly different FRZ1/JNT2 cosmologies. The purpose is to expose the missing source identification in the claimed derivation.

XJ1's newer exact-junction formula leaves **B** unchanged inside and rescales the exterior instead:

    t = [C_R(rta)-C_B(R_set)]/[C_R(rta)-C_R(R_set)].

`halo_masses.csv` records this formula as `exact_B_junction_outer_t`; this audit does not rerun XJ1's observation or shell analyses. Provided B is already monotone and capped, t is nonnegative. Preserving B fixes FZS1's additional s-rescaling problem but does not undo B's pre-existing truncation, leftover, cluster components, or retained-versus-total-baryon distinction. It cannot by itself establish that the raw unscaled force equation holds throughout the inner region. A meaningful next check must specify the baryon source and enforce its actual charge bound before testing any repaired junction.

## Artifacts, commands, and provenance

- `run_001/halo_masses.csv`: all 10,272 detailed actual-code evaluations, with source and budget quantities, both force residuals, and actual/nominal radii.
- `run_001/results.json`: coverage, constants, checks, all 32 cell summaries, independent SI common-r200 benchmarks.
- `run_001/representative_profiles.npz`: 128 radial profiles (8 chosen grid masses × 4 redshifts × 2 footings × f=1.25,3); column definitions are in the JSON. These are diagnostics, not the coverage population.
- `run_002/source_comparisons.csv` and `results.json`: physical-unit all-Bar calculation and source isolation on all 10,272 rows.
- `run_003/scope_rows.csv` and `results.json`: conditional condensed/patch baryon identity and all 2,568 actual distinct scope ratios.
- `run_004/mass_budget_example.png` and `.svg`: one representative slow halo comparing all the enclosed profiles and both baryon-source residuals; `figure_context.json` pins the selected row.
- `run_006/budget_bounds.csv` and `results.json`: exact raw-law charge-radius bound on 64 representative halos with two source conventions. See `BUDGET_BOUND.md` for the proof and the distinction from a physical boundary.
- The four original manifests and `run_006/manifest.json` are **v2, run.status completed**; `run_005/manifest.json` is **v2, run.status failed** because of JSON serialization, retained for provenance. Each records observed before/after input SHA-256, output SHA-256, software versions, actual argv, runtime and bounds. They validate against the current root. `SHA256SUMS` additionally covers all files in this calculation directory except itself.

From the repository root, fresh bounded reproductions are:

```bash
python3 codex_mass_budget_2026_11_14/calculation/reproduce.py --stage 1 --run-name reproduce_stage1
python3 codex_mass_budget_2026_11_14/calculation/reproduce.py --stage 2 --run-name reproduce_stage2
python3 codex_mass_budget_2026_11_14/calculation/reproduce.py --stage 3 --run-name reproduce_stage3
python3 codex_mass_budget_2026_11_14/calculation/reproduce.py --stage 4 --run-name reproduce_stage4
```

Stages 2–4 deliberately read the preserved `run_001` tables. To validate the original evidence, run this command for each manifest (substitute `run_002`, `run_003`, or `run_004` as appropriate):

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py codex_mass_budget_2026_11_14/calculation/run_001/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

The repository was dirty and advancing while this work ran. The manifests preserve the actual run revision and input hashes; they are not claims of an otherwise clean checkout. No existing lane was edited. No universal force-law result, dynamic settling mechanism, medium identification, stability, preferred fit, or theory closure follows from these finite checks.
