# CFG195 -- independent referee of CFG176 (door 11: the nature of dark energy in the flowing-vacuum picture)

Frozen criteria: `CFG195_FROZEN_CRITERIA.md` (sha256 4a895809..., committed as "CFG195: frozen criteria" before any script). Phase 2 ran the scripts exactly as frozen, with the deviations listed under "Deviations and kept failures" below. CFG176's scripts, .out and .json were opened only after CFG195's own main and MUTATE runs were saved and hashed (`CFG195_PHASE2_own_runs_SHA256.txt`, taken 2026-09-30T01:55Z; the file was re-issued after `CFG195_compare.py` was added, and the hashes of the earlier 34 files did not change). Nothing in the repo was edited. No new data, no network. No absolute home path appears in any output (`<repo>`).

## Bottom line (plain)

1. **CFG176's numbers reproduce.** Every load-bearing number I could recompute from its own definitions agrees with CFG176's committed results to 1e-5 (0.0490 / 0.0345 / 0.0781; 1+w0 percentiles; C; beta; Q3-I). My hand estimates made before the runs were right for 17 of 20 (one missed, one not run, one in range).
2. **The wording of the 0.078 bound is narrower than the headline.** 0.078 is the 97.5th percentile of the time-integrated column for a **perfect fluid** (factor 3/4), for **one NEC-respecting component**, using the CPL fits with the **phantom epochs clipped to zero carrying**, over the **three SN combinations in the repo**, as a **cosmic-mean** flow. Under the NEC alone (any anisotropic stress at fixed isotropic w), the maximum is (sqrt3/2)(1+w_iso), so the same integral is **0.0902 (Union3)**, not 0.078; still 3.2x below R = 0.293. The margin therefore stands for that family.
3. **What does not stand as worded:** "a real medium carries at most 0.078". A phantom compensator, a free-form NEC-respecting rho_DE(z) that mimics the CPL background, or a locally compacted medium all leave the DESI total w silent (details below). Those are SCOPE differences, not numeric disagreements. `A3` (the free-form attack) is a FAILED pass line of my own (kept).
4. **Not tested:** any DESI-alone or no-SN combination (not in the repo); a memory-based proxy for it was written into my frozen plan (I-7) and is **not run and not presented as a result**, following the coordinator's instruction. Q3-II (the decaying-vacuum accumulation) has no frozen pass line and was not re-derived. Observational shear and CMB-quadrupole limits, PPN/G_N of the aether, perturbations, the KURVS/KROSS data: not tested.

## Where independence stops

- **Shared data:** the three committed thinned DESI DR2 chains, the L273/L275 docstring numbers (paper values, H0, Omega_m per combination) and CFG174's definition of R. I re-read the chains with my own loader and my own weighted percentile. Because the definitions and the data are shared, bit-level agreement on Q4 (1e-5) says the code is right, not that the physics choice (clip, weight, 3/4) is the only sensible one; that is what the attacks probe.
- **Not independent of the README:** the perfect-fluid formulas (II-4) I re-derived with sympy, but the targets were read from the README first (labelled as targets, not blind predictions).
- **Own re-implementation, no CFG6 grid:** the thawing tracks (CLW system), the Q3-I ODE, the aether minisuperspace, PG river, Bianchi I, the NEC linear program (no CFG176 counterpart).
- **Memory, unverified:** the CLW equations, Hawking-Ellis types (I verified type III violates the NEC numerically on a family I constructed), T_CMB = 2.7255 K and N_eff = 3.044 (report only).

## Scoreboard: pass line -> verdict (REPRODUCES / PARTIAL / DISAGREES)

Verdict is against CFG176's statement, not against my own hand estimate. "Class" = frozen difference class.

| pass line | result (CFG195) | vs CFG176 | verdict | class |
|---|---|---|---|---|
| I-1 chains vs paper values | means (w0, wa): DESY5 -0.752, -0.862; Pantheon+ -0.838, -0.617; Union3 -0.665, -1.090; Om 0.3191/0.3114/0.3276; sd and rho(w0,wa) -0.91/-0.90/-0.93 | as CFG6 | REPRODUCES | |
| I-2 1+w0 97.5th; today 3/4(1+w0) | 0.362/0.274/0.511; 0.272/0.205/0.383; wa<0 at 97.5th; p(w0<-1) 0 / 1.3e-3 / 5e-5; p(wa>0) 0 / 6.4e-4 / 0 | identical | REPRODUCES | |
| I-3 crossing | fraction 0.9998/0.9978/0.9998; median z_cross 0.405/0.356/0.444 | README 0.41/0.36/0.44 (2 dp) | **PARTIAL** (my unrounded line 0.36-0.44 fails by 0.004: kept as FAIL) | LABEL |
| I-4 the 0.078 | F(k=3/4) 97.5th = **0.0490 / 0.0345 / 0.0781** (bootstrap se 0.0002-0.0003, N=2000, seed 195001; Union3 95% interval [0.0776, 0.0787]); means 0.0316/0.0186/0.0472; fraction with F >= R: 0 | 0.04901/0.03452/0.07814 | REPRODUCES | |
| I-4b F below R at 97.5th | R/97.5th = 6.0 / 8.5 / 3.75 | H2 | REPRODUCES | |
| I-5 treatment dependence | k=1/2: 0.033/0.023/0.052 (identical to CFG176's isotropic); k=sqrt3/2: 0.0566/0.0399/**0.0902**; rho weight 1: 0.052/0.037/0.079; only z<=3 or z<=1: same (carrying is all at z<0.5); fixed Om=0.3111: 0.056/0.040/0.088; margin >= 3.2x in every variant | CFG176 has k=1/2 and 3/4 only | REPRODUCES (margin holds) | SCOPE for "any NEC medium" wording |
| I-6a thawing, NEC-respecting best node | F(k=3/4) 0.0299/0.0163/0.0291 (lambda 0.8/0.6/0.8, distance to the chain mean 3.3/2.7/3.4 sigma) | 0.0389/0.0164/0.0194 (lambda 0.9/0.6/0.65) | **PARTIAL** | LABEL (node-selection rule differs; all far below R) |
| I-7 no-SN / DESI-alone | **NOT RUN** | not in repo | not tested | -- |
| I-8 R with each combination's own cosmology | R canonical 0.301/0.291/0.313 (alt 0.364/0.351/0.378); within 10% of 0.293; verdict unchanged (F/R at 97.5th: 0.16/0.12/0.25) | CFG181 already flagged the mixed cosmology | REPRODUCES | |
| II-1 NEC derivation | T_kk = T00 -+ 2 T0x + Txx in both signatures; |T0x| <= (T00+Txx)/2 (sympy) | S3 | REPRODUCES | |
| II-2 NEC-only maximum (LP) | **g_max/e = 0.86603 (1+w_iso)** at six values of 1+w_iso from 0.02 to 1; g_max = 0 at w_iso = -1; LP infeasible for w_iso < -1 | README states only the necessary bound (1+w_par)/2 | **PARTIAL** | SCOPE: README's inequality true but not sufficient, w_par is not DESI's w |
| II-3 type IV | eigenvalues -rho +/- i q; min_k T_kk = -2q | S3 | REPRODUCES | |
| II-4 perfect fluid at beta | 1+w_eff = R(1/beta + beta/3), rest-frame formula, min 4R/3 = 0.390/0.472; 1+w(600 km/s) = 146; DEC needs beta >= 0.150/0.183; attraction beta > 0.845 (w = -0.75) | S5 | REPRODUCES | |
| II-5 anisotropic / types II, III | 1000 random NEC tensors never exceed 0.866 (max found 0.736: my "reach 0.99" expectation FAILED and is kept); null dust + Lambda saturates 3/4 exactly; 5000/5000 type-III members violate the NEC | not in CFG176 | REPRODUCES (a, b, c); expectation a' failed | |
| II-7 phantom side | median CPL sample is phantom (NEC-violating even at rest) for 0.654/0.705/0.675 of cosmic time; 99.9% of the weight has a phantom epoch at z<=2.5 | README OPEN item names it; headline and the table row do not | **PARTIAL** | SCOPE |
| II-8 Lambda + flow | (1/2)(1+w_f) e_f = (1/2)(1+w_tot) e_tot | not in CFG176 | REPRODUCES (my identity) | |
| III-1 energy equation | u_nu grad_mu T^{mu nu} = -[u.grad rho + (rho+p) div u]; rho = K n^{1+w} | S2 | REPRODUCES | |
| III-2 vacuum rigidity | div(-rho g) = -grad rho: rho constant **iff** the vacuum sector is separately conserved | S2 ("for w=-1 conservation reads d_t rho = d_x rho = 0") | **PARTIAL** | SCOPE: premise P1 (no exchange) must be stated; A5 |
| IV-1 aether minisuperspace | K1..K4 = 3, 9, 3, 0 H^2; E_N = a^3/(8 pi G) x [(1+beta/2) 3H^2 - 8 pi G (rho_m+rho_L)]; acceleration equation follows; w_aether = w_total | S6 | REPRODUCES | |
| IV-2 H(z) shape | E^2/E^2_LCDM = 1/(1+beta/2), constant | H5 | REPRODUCES | SCOPE: constant c_i only (IV-3) |
| IV-3 F(K) aether | F=K gives a constant rescaling; F=K^{3/2}, K^2 do not | CFG176 scopes to c1..c4 | REPRODUCES (scope confirmed) | SCOPE |
| IV-4 C and |beta| | C = 3.59e5 / 1.13e5 / 3.59e4 / 1.13e4 (canonical, 1e9..1e12), 4.77e5 ... 1.51e4 (alt); rho_c equals the P2 phantom density at r_M (1e-11); C range 1.13e4-4.77e5 spans both footings; **|beta| >= 1.55e4 - 4.91e5 canonical, 1.55e4 - 6.53e5 both footings**; compression 1.7e16-5.2e22 | C identical; |beta| printed 1.6e4-4.9e5 | REPRODUCES numbers; **PARTIAL** on label | LABEL (the |beta| range is canonical-only while C's range is both footings) |
| IV-5 Q5 numbers | Omega_null 0.202/0.244; z_dom 0.542/0.276; H(2.5) x1.777/x1.900; PG cross-term 219-1234 rho_L (H_L = H0 sqrt(Omega_L)); pull 0.0008-0.0046 a0 | identical | REPRODUCES | |
| IV-6 Q3-I | H0 t0 1.0302; w0 -1.6471; CPL (-1.7028, -0.5159); H(0.5) -13.1%; a0 -0.339/-0.533/-0.752 dex; distances 36.1/34.0/27.5 sigma (LCDM 4.3/3.0/3.8) | identical to 1e-9 | REPRODUCES | |

## What the 0.078 bound needs (plain answers)

- **Perfect fluid vs NEC-only.** 0.078 uses k = 3/4, the boosted perfect fluid at beta -> 1 (or null dust + Lambda, exactly 3/4). The NEC alone, at fixed isotropic w, allows g/e up to (sqrt3/2)(1+w_iso) = 0.866(1+w_iso) (LP, deterministic, six values of 1+w_iso; the optimum has 1+w_par = 2(1+w_iso) and 1+w_perp = (1+w_iso)/2). The integrated 97.5th percentile becomes **0.0566 / 0.0399 / 0.0902** (ratio 1.1547 exactly), and today's rate alone would reach R in 6.1% / 0.06% / **48.0%** of DESY5 / Pantheon+ / Union3 posteriors (vs 0.9% / 0.01% / 26% for the perfect fluid and 0 / 0 / 0.3% for w_par = w_iso). All are still integrated well below R (max 0.0902 vs 0.293).
- **Single component vs phantom compensator (A6, epoch by epoch).** For a Lambda-like or NEC component plus a phantom one with w_ph >= -2, the flowing part can carry R at total 1+w = 0.05 when the phantom fraction is 0.29 (1+w_f = 0.47), and at total 1+w = 0 when it is 0.34. With w_ph >= -1.5 the fractions are 0.58 / 0.68; with w_ph >= -3 they are 0.14 / 0.17. With no compensator (w_ph = -1) R is never reached. So the DESI total w bounds a flow only if every dark-energy component is NEC-respecting. This is an epoch-by-epoch scope statement, not a fit.
- **The dataset combination.** The repo holds only DESI BAO + CMB (Planck low-l, NPIPE CamSpec, ACT DR6 lensing) + one of DESY5 / Pantheon+ / Union3. The 0.078 is the Union3 value; DESY5 0.049, Pantheon+ 0.035, and the bootstrap noise is ~0.0003. No DESI-alone or no-SN combination is in the repo, so **the dependence on dropping the SN sample is not tested**. Across the three that are present, a shift from 0.035 to 0.078 already comes from swapping the SN sample.
- **The phantom side and parametrisation.** The CPL posterior has a phantom epoch at z < 2.5 in 99.9% of the weight, over 65-71% of cosmic time. CFG176 clips those epochs to zero carrying (my M7, with |1+w| counted instead, gives 0.151/0.126/0.196 for k=3/4, still below R but that rule is arbitrary). The healthy thawing families (NEC-respecting everywhere) carry 0.016-0.039. **A free-form NEC-respecting rho_DE(z)** (nodes z = 0, 0.3, 0.6, 1, 1.5, 2.5, 5; w in [-1, 1]) that reproduces a chain sample's E(z_j) and D_C(z) within eps: with Omega_m free in the chain 95% range, F_max = 0.33-1.02 (eps = 1%) and 0.47-1.17 (2%), i.e. **above R**; with Omega_m held at the sample's value and the test point z = 5 included, eps = 0.5% and 1% are infeasible in 5 of 6 cases (the CPL background cannot be reproduced with w >= -1 to that precision), and at eps = 2% F_max = 0.24-0.30 in the 5 feasible cases (one, 0.297, just above R), **near R**. The result is tolerance- and parameterisation-dependent and cannot be settled without the likelihood (not in the repo): my frozen A3 line is a FAIL, kept. The first run without the z = 5 node (which let early dark energy absorb the freedom) is kept in `CFG195_freeform_RUN1_without_z5_constraint.out`; a second, with z = 5 and free Omega_m only, in `..._RUN2_free_Om_only.out`.
- **A1 (chain-free):** on the (w0, wa) grid at the chain-mean Omega_m the region F(k=3/4) >= R is 5.60 / 5.37 / 5.37 Mahalanobis sigma from the DESY5 / Pantheon+ / Union3 means (5.46 / 5.19 / 5.23 for k = sqrt3/2), at the grid edge w0 = -1, wa ~ +0.3 (a different kind of model, w rising into the past). PASS.
- **Cosmic-mean vs local (A7).** For a medium already compacted to C rho_L the same column needs only 1+w_loc >= 2R/C = 1.2e-6 to 5.2e-5, but compaction to C by volume compression n needs 1+w = 0.68-5.7 for n <= 1e6. The momentum column is not the binding requirement for a locally compacted medium; the compaction (rho ~ n^{1+w}, S2) is. My frozen A7 expectation ("compaction 1+w ~ 0.8-5") failed at the low end (0.68) and is kept.

## Does "a Lambda vacuum cannot be compacted" need separate conservation? Yes.

`div(-rho g)^nu = -d^nu rho` (sympy). So rho is constant only if T_DE is conserved on its own (P1), of the pure Lorentz-invariant form (P2), in GR with minimal coupling (P3). If P1 is dropped, rho(x) can vary only with an exchange current J^nu = -d^nu rho (a gradient), and dust then feels an acceleration a^nu = P^nu_sigma d^sigma rho / rho_m (A5, sympy): a scalar-potential force, which is what "compacted by matter" would be. CFG176's S2 states the rigidity "for w = -1 conservation reads d_t rho = d_x rho = 0", and its OPEN list names the non-minimal case; the README bottom line ("cannot ... be compacted anywhere") does not state P1. Class SCOPE (wording), not MATH.

## C and |beta| by footing

| footing | M_b = 1e9 | 1e10 | 1e11 | 1e12 |
|---|---|---|---|---|
| canonical C | 3.587e5 | 1.134e5 | 3.587e4 | 1.134e4 |
| canonical \|beta\| >= 2 C Omega_L | 4.912e5 | 1.553e5 | 4.912e4 | 1.553e4 |
| alt C | 4.766e5 | 1.507e5 | 4.766e4 | 1.507e4 |
| alt \|beta\| | 6.526e5 | 2.064e5 | 6.526e4 | 2.064e4 |

CFG176 quotes C = 1.1e4-4.8e5 (both footings) and |beta| = 1.6e4-4.9e5 (canonical only). Same formula rho_c = a0/(4 sqrt2 pi G r_M) (checked against the P2 phantom density (1/4 pi G r^2) d(r^2 g_ph)/dr at r_M to 1e-11; H0 = 67.4, Omega_L = 0.6847, rho_L = 5.8424e-27).

## Attacks (results)

| attack | result | meaning |
|---|---|---|
| A1 nearest (w0, wa) with F >= R | 5.4-5.6 sigma (k=3/4), 5.2-5.5 (k=sqrt3/2); Omega_m fixed | PASS |
| A2 NEC LP | 0.86603 (1+w_iso); random tensors <= 0.736; null dust 3/4 | analytic optimum reproduced |
| A3 free-form NEC-respecting rho_DE(z) | F_max above R (Omega_m free), 0.24-0.30 at 2% (Omega_m fixed), infeasible at <=1% (Omega_m fixed) | **frozen line FAILS (kept)**: parameterisation/tolerance-dependent (SCOPE) |
| A4 phantom side | phantom time fraction 0.675/0.705/0.654 (weighted); 99.9% of weight has a phantom epoch at z<=2.5; LP infeasible for 1+w_iso < 0 | SCOPE: bound is conditional on NEC everywhere |
| A5 exchange current | gradient-only exchange, a^nu = P d rho/rho_m | needs P1 |
| A6 compensated two-component | R reachable with a phantom compensator (table above) | SCOPE: single component only |
| A7 local vs cosmic | needs 1+w_loc >= 1e-6-5e-5 vs compaction 1+w 0.7-5.7 | SCOPE |
| A8 bootstrap of 0.078 | Union3 [0.0776, 0.0787] | PASS |
| A9 Bianchi I | G^x_x - G^y_y = D' + 3HD (sympy); D(t0)/H0 = 0.555 x (p_par - p_perp)/rho, sigma_1/H0 = 0.370 Delta at Om = 0.3111 (CFG176's 0.370) | REPRODUCES; the "4-11% anisotropy" is defined against today's 1+w0 (2R - 0.511), not against the integrated 3.8x shortfall (SCOPE, wording) |
| A10 H1 | momentum zero iff w = -1 | trivial PASS |

## MUTATE outcomes (7 controls; exit 1 = the control bites)

| control | script | outcome |
|---|---|---|
| M1 NEC sign flip | `nec_lp` (rc 1), `sympy_algebra` (rc 1) | BITES: II-2, II-2c fail; II-1 direction reverses |
| M2 chain (w0, wa) shifted by (+0.45, +0.5) | `desi_bound` (rc 1) | BITES: I-1..I-4b, A1, I-5 fail (1+w0 ~ 0.7, almost no crossing) |
| M3 dust inertia rho for (rho+p) | `desi_bound` (rc 1) | BITES: F 97.5th = 0.99 / 0.99 / 1.02 > R; k=3/4-equivalent 0.743/0.742/0.762 equals CFG176's MUTATE=1 chain value to 1e-6 |
| M4 isotropic pressure only | `nec_lp` (rc 1) | BITES: 0.5 (1+w) instead of 0.866 (1+w) |
| M5 beta = c1 + c2 + c3 | `sympy_algebra` (rc 1) | BITES: IV-1b fails |
| M6 axis-aligned null vectors only | `nec_lp` (rc 1) | BITES: 1.5 (1+w) (necessary, not sufficient) |
| M7 no clip (|1+w| carries) | `desi_bound` (rc 1) | BITES only through the lines that compare with the README numbers: F 97.5th = 0.151/0.126/0.196 still below R; this control shows the clip does not by itself keep F below R under that arbitrary rule (kept) |

## Deviations and kept failures

- **I-7 (memory-based no-SN proxy):** frozen in Phase 1, **not run**, per the coordinator's Phase-2 instruction not to present a memory-based proxy as a result. The dataset dependence is therefore untested beyond the three SN samples.
- **First `desi_bound` run:** the scipy.quad control Q0 passed vacuously (its reference integral diverged and the rows were skipped). Fixed (log-variable integral, at least 8 rows compared: max rel diff 1.1e-5) before any saved result. One MUTATE=2 run crashed (no crossing samples); fixed with a guard and rerun.
- **`freeform` first run** omitted E(z = 5) in the constraint (a coding deviation from the frozen node set). Kept as `..._RUN1_...`; the frozen definition (with z = 5) is the main run. A further variant with Omega_m fixed (A3c) was added to expose the Omega_m freedom.
- **Failed own lines, kept:** I-3 (median z_cross 0.356 / 0.444 vs 0.36-0.44, rounding, exit 1 of `desi_bound` main); A3 (exit 1 of `freeform` main); II-5a' (random tensors reach 0.85 of the optimum, not 0.99); A7 (compaction 1+w_min = 0.68 not >= 0.8); Q0 vacuous first pass. Wrong hand estimates: E6 (thawing DESY5 0.045 estimated, 0.030 in my node, 0.039 in CFG176); the I-6a node mismatch; my E20 normalisation (sigma = D/sqrt3 vs the sigma_1 = (2/3)D convention, LABEL).
- Hand estimates (Phase 1, all recorded before runs): E1, E2, E3, E4, E5, E7, E8 (48%/5.7%/0.07% vs 48.0%/6.1%/0.06%), E9, E10, E11, E13-E19 matched; E6 missed; E12 not run; E20 in range.
- **Mains' exit codes:** `nec_lp` 0, `sympy_algebra` 0, `q3_q5_numbers` 0, `compare` 0, `desi_bound` 1 (I-3), `freeform` 1 (A3). All mains were run twice: byte-identical `.out` and `.json`.

## Not tested (explicit)

DESI-alone and BAO+CMB-without-SN combinations; Q3-II (decaying vacuum, wa > 0); the observational anisotropy/shear bound; PPN and G_N of the aether, perturbations (G2); real DESI/CMB likelihood for a free-form w(z); CFG174's KURVS/KROSS comparison; the flow's non-minimal coupling (the door-11 variants CFG171-173); the "cosmological mean" assumption for a focused flow beyond the A7 numbers.

## Files (all `CFG195_*`)

Scripts: `CFG195_common.py`, `CFG195_desi_bound.py`, `CFG195_nec_lp.py`, `CFG195_sympy_algebra.py`, `CFG195_q3_q5_numbers.py`, `CFG195_freeform.py`, `CFG195_compare.py`.
Outputs: `CFG195_<script>.out`, `CFG195_<script>_results.json`; MUTATE: `CFG195_desi_bound_MUTATE{2,3,7}`, `CFG195_nec_lp_MUTATE{1,4,6}`, `CFG195_sympy_algebra_MUTATE{1,5}` (`.out` and `_results.json`); `CFG195_freeform_RUN1_without_z5_constraint.out`, `CFG195_freeform_RUN2_free_Om_only.out`; `CFG195_compare.out`, `CFG195_compare_results.json`; `CFG195_PHASE2_own_runs_SHA256.txt`; `CFG195_FROZEN_CRITERIA.md`; this `README.md`.

## Re-run (from the directory holding the scripts; if it is not inside the repo, `export ZF_REPO=<repo>`)

```
for s in nec_lp sympy_algebra q3_q5_numbers freeform desi_bound; do python3 CFG195_$s.py; done   # rc: 0 0 0 1(A3) 1(I-3); desi_bound ~90 s
MUTATE=1 python3 CFG195_nec_lp.py; MUTATE=4 python3 CFG195_nec_lp.py; MUTATE=6 python3 CFG195_nec_lp.py
MUTATE=1 python3 CFG195_sympy_algebra.py; MUTATE=5 python3 CFG195_sympy_algebra.py
MUTATE=2 python3 CFG195_desi_bound.py; MUTATE=3 python3 CFG195_desi_bound.py; MUTATE=7 python3 CFG195_desi_bound.py   # each rc 1
python3 CFG195_compare.py                                                                          # rc 0 (reads CFG176's committed results JSON)
```

Standing rules kept: kappa = 1/2 is FITTED; nothing here says the data favour the framework or that the theory is closed; the outcome is a scoped picture of one bound and its conditions, and a set of controls that bite.

## In-place re-run (orchestrator)

`bash run_all.sh` was re-run in this directory with `ZF_REPO` set (`run_all.out`): nec_lp, sympy_algebra and q3_q5_numbers exit 0; freeform and desi_bound exit 1 (the referee's kept failures A3 and I-3); all eight MUTATE runs exit 1 (bite); the compare script (opened after all of the above) exits 0. Every `.out` and `.json` is identical to the referee's apart from timing lines. `CFG195_freeform_RUN1_without_z5_constraint.out` is the referee's first free-form run (it omitted the E(z = 5) constraint), kept as produced. The frozen criteria are `../CFG195_FROZEN_CRITERIA.md` (b9e5a0a12). I-7 (DESI-alone and no-SN combinations) was withheld because the repo holds no such chain; nothing in this lane rests on a memory-based proxy.
