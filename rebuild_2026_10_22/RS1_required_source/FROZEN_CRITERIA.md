# RS1_required_source: FROZEN CRITERIA, committed alone before any script or number

Owner's standing go for search lanes, 2026-11-02. Inverts rather than guesses. κ = ½ FITTED. Footings 9.3603e-11 and 1.1312e-10 m/s², never pooled. Raw or native inputs; HSE, SIS, PROVISIONAL and ASSUMED-GAS tags kept. A closed form found here is a description: no action, no field equation, no particle adopted. Not theory closed. Nothing here says the data favour the framework.

**Not blind.** Read before this: BF1's script, BF2's README, BF3's criteria, HF1's and VW1's results, the law's failures, CRG1's loaders. No RS1 number exists. Expected, on record: required source positive and large on clusters, near zero or negative on discs at Υ 0.5, negative at the Milky Way and IC 1613; Stage 1 finds no form passing all classes (90 %).

## How it differs from the record
- **SL2** (A_req) is a ratio on a cold-core rule by scale. **GS4, LF1, NU1, MG1, DW2** ask about gas, retention, ordinary mass, peak position, and processes. None inverts the law row by row across all classes into one source.
- **BF1, BF2, BF3** search multipliers H on g over y, ell, f. BF3 protects stars-only systems by construction; BF1's wrapper W2 is close to this lane's source form. This lane differs in: the target is a mass M_x added to the Newtonian source, required non-negative everywhere; gas and stars enter as separate leaves; system-scale leaves are added (mu, x below); four mass bases; dwarfs, LITTLE THINGS, groups and galaxy lensing are gated at Stage 1 and not only afterwards. Overlap is accepted and stated: a W2 form can reappear here.

## Part 1: the requirement map
From g = g_N (1/2 + sqrt(1/4 + a0/g_N)), the law's inverse is g_N,req = g_obs^2 / (g_obs + a0). **M_x(r) = (g_N,req - g_b) r^2 / G.** Spherical. Row sets:

| Class | g_obs | Baryons | Tag |
|---|---|---|---|
| SPARC, Q <= 2... all rows Q < 3, Inc >= 30 | V^2/R | Υ 0.5/0.7; low reading 0.41/0.574, the level VW1 reads by eye | |
| LITTLE THINGS | V^2/R at R_max | measured gas + stars | |
| Groups, 63 | 3 sigma^2 / r12, r12 = 4/3 Re | lM/2 inside r12 | ASSUMED-GAS f 0.3, 0.6 |
| X-COP, 7, x 0.1-0.7 | G M_HSE/r^2 | measured gas + stars | HSE |
| Galaxy lensing, 4 bins, R <= 0.3 Mpc | 4 G dSigma | bin's mean M_star plus assumed gas | SIS, ASSUMED-GAS f 0.2, PROVISIONAL |
| Dwarfs, 5 classes | 3 sigma^2 / r12 | M*/2 | gas 0, stated |
| Milky Way, IC 1613 | not a spherical inversion | | law's own K_z and E rows, read as the sign the source would need; reported, not searched |

Cluster keys aren't inverted: they compare shear and temperatures through a model, so there's no row-by-row g_obs. Keys enter only at Stage 2.

For each class, each footing, each reading, reported: median and 16-84 % of M_x/M_b; share of rows with M_x < 0; share with |M_x| above 2 of its error where a row error exists; mean density rho_x = M_x / (4 pi r^3 / 3), rho_x/rho_b, local rho from dM_x/dr on SPARC and X-COP; phase density Q = rho_x / sigma^3, sigma = V_max,obs / sqrt 2 or the system's dispersion. Spearman of M_x with M_gas and M_star, per class and within mass bands, partial where both vary.

**Circularity, stated.** M_x and sigma both come from g_obs, so correlations with sigma or Q are partly forced. They are descriptive only. No observed velocity is a search leaf.

**Collapse test.** One variable at a time from y_g, y_s, y, f, ell, mu, x, rho_b in a0 units, plus Q (descriptive): on rows with M_x > 0, rms of lg(M_x/M_b) about a monotone (isotonic) fit, against its rms about the mean, all classes, classes weighted equally. Also the between-class share of the variance left. **COLLAPSES:** residual rms <= 0.20 dex, and every class's median within 0.20 dex of the curve. Otherwise DOES NOT COLLAPSE. The monotone fit is free, so this is generous, and a pass here is only a clue. The same on shuffled variable, 200 draws, for a null.

## Part 2: the search
Dimensionless leaves, from baryons only: y_g = max(g_gas, 0)/a0, y_s = g_star/a0, f = gas share of enclosed baryons in [0, 1], ell = r a0/c^2, mu = G M_bt a0/c^4 with M_bt the system's total measured baryons, x = r / sqrt(G M_bt / a0). Constants 1, 2, 1/2, pi. Unary sqrt, log1p, inv1p, square. Binary + - * /. No other float. Level-2 pool by value dedupe as BF1, ranked by nodes then lexical, cap 6,000. Form: **M_x = base x T,** T = a op b on pool pairs, base in M_b, M_gas, M_star, M_bt. T must be finite and base x T >= 0 on every row. A cap is a limit, reported.

Prediction: g = law(g_b + G M_x / r^2, a0). Residual d = log10(g_obs / g).

**Arms:** canonical Υ 0.5, canonical low reading, alt Υ 0.5, alt low reading. Each is searched on its own.

**Split.** X-COP positions 0, 2, 4, 6 train, as BF1. SPARC odd names train, as BF1. Others: sorted names, even index train, odd holdout; lensing bins 1, 3 train, 2, 4 holdout. Evaluation on train uses all train rows, with SPARC subsampled to 240 frozen by seed 20261102 for the first pass, then every SPARC train row for survivors.

**Stage 1 gates, all on train, lines from real errors:**
- **X (HSE):** |mean d| <= 0.05, rms <= 0.10, BF1's. Tighter than the HSE term alone; RQ3's looser line (0.12 dex hydrostatic) is reported beside.
- **S:** rms <= 1.05 x law's on the same rows, |median| <= 0.03, BF1's.
- **LT:** |median| <= 0.10, the record's line.
- **G:** |mean| <= 2 sqrt(se^2 + 0.10^2), the 0.10 dex mass term, kept in g so generous, at f 0.3 and 0.6 both.
- **D:** each dwarf class with at least 2 train rows, |median| <= 2 sd, sd = 1.2533 rms(row s)/sqrt N.
- **L:** each train bin, |mean d| <= 2 sqrt(se^2 + 0.05^2), BF3's 0.05 dex; se from the published covariance's diagonal in dex over points used.
The law, T = 0, is scored the same way, on the same table.

**Stage 2:** survivors on the holdout rows, same lines; then 15 keys on measured gas +0.005 through CRG1's code if the path can be built; stated NOT RUN otherwise. Bullet: M_x on local gas puts mass on gas, so expected DEAD for gas-local forms; stated beside any hit, not graded.

**Near misses.** Score = largest of value/line across gates. Top 50 per arm kept. Best per combination of gates dropped one at a time. Labelled NEAR MISS, with gates failed named. Never a hit.

**Labels.** **SOURCE FORM** passes all Stage 1 and holdout gates on all four arms, or names which arms. **NO SOURCE FORM** within this grammar and cap: says nothing beyond it. **NOT ABOVE CONTROL** goes in the title if hits per expression don't beat the shuffled control by a factor of 3.

## Part 3: HF1's open reading, a map, not a rule
HF1's R4 solver, a private copy with sigma x s and fair share x r: s in 0.3, 0.4, 0.5, 0.6, 0.7, 0.85, 1.0; r in 0.2, 0.4, 0.6, 0.8, 1.0; X-COP 7, m 5 and 11.8 eV, omega_f as HF1's cells, both footings. Reported: mean, rms, residual by x, and the cells with |mean| <= 0.05, rms <= 0.10. Beside them, whether s and r are physically available: the s needed against the system's measured dispersion. A clearing cell is a requirement. HF1's label doesn't move. Gate 1 fails regardless (VW1).

## Controls
K1 T = 0 reproduces, on this lane's rows: X-COP +0.467, 0.476; SPARC canonical BF1 statistic as BF2's K values where recorded; LT -0.025; dwarf UFD Z +5.22 within 0.05. Groups and lensing estimators are this lane's own, so their law values are printed, compared with CRG1's Z +0.31 and BF3's, and differences stated. K2 inversion round trip: law(g_N,req, a0) = g_obs to 1e-10. K3 planted: mock g_obs on every class from a form in the grammar, its true form must be recovered and pass. K4 shuffled: leaves permuted jointly across all train rows, seed 20261102, same search; count reported. K5 Part 3 at s 1, r 1 reproduces HF1's X-COP +0.159 at m 5 and +0.178 at m 11.8 within 0.002.
**MUTATE, separate outputs, must fail:** a0 x 2 in the inversion and prediction only (K1 breaks), and lines x 1e-6 on the planted mock (nothing recovered). Exit 1.

## Compute and rules
Nice 10, at most 2 processes, under 1 GB each, lane directory only. Wall budget per arm 3 hours, jobs in rank order, coverage reported. Post-result changes go in a disclosed amendment. No downloads. No deletes.
