# PARAMRED lane E (FREE): FROZEN CRITERIA (written before any script and before any derivation)

Date 2026-10-16. Lane dir: `campaign_fresh_gravity/PARAMRED_2026-10-16/E_FREE/`. No CFG id taken (orchestrator assigns).
Task: constraint intersection for the free (untethered) cold-energy component. Not model building, not fitting.
kappa = 1/2 FITTED; Omega_c/Omega_b = 5.364 measured; both footings (9.3603e-11 canonical / 1.1312e-10 alt) never pooled;
no dark-matter particle species; raw data or framework-native only. This is not "theory closed".

## 0. Disclosure (what was seen before this freeze)
- The ledger rows listed in section 1 and the CFG782 / CFG784 / CFG785 lane files (criteria, README, cfg782.out, cfg782.py) were
  READ before freezing. The freeze therefore fixes the arithmetic, the families tested, the pass rules and the controls;
  it is NOT a blind prediction. Every outcome below is labelled "constraint extraction", never "prediction".
- CFG782 is recorded DEAD in the ledger and its README (S1 PASS, S2 FAIL). This lane does not re-run CFG782 as a test of that
  verdict; T1 asks a different question (does ANY multiplier on c_s, i.e. any value of the sqrt2 and any T_IGM, open a window).

## 1. Pre-registered condition list (IDs are fixed; margins are tabulated in CONDITIONS.md, taken from the cited ledger rows)
WHERE
- W1 cluster MID band 0.48-1.24 Mpc carries the excess; OUTER 1.2-3 Mpc already matches the law (CFG687, CFG686)
- W2 cluster INNER must not be overfilled; framework splashback caustic sits INNER (CFG727, CFG818, CFG819)
- W3 the persistent excess is a component the cubic push does not act on (untethered) (CFG776, CFG777)
- W4 early types: excess at 50-100 kpc, +0.280 +- 0.083 dex; carrier colour/Sersic undecided; age NOT a condition (CFG669, CFG721 colour row, CFG667)
- W5 UFDs: inside the dispersion-estimator radius, not tidal (CFG28)
- W6 galaxy halos: derived catchment supply suffices to 0.31 Mpc; a sharp settled edge is excluded (CFG801, CFG804)
HOW MUCH
- A1 UFD +0.325 dex (3.5-3.9 sigma) after binaries (CFG28, CFG259); law phantom exceeds native cold share x3.5 (CFG336)
- A2 early types: free mass 0.55-0.80 M* inside 100 kpc (log M* 10.8) (CFG745); early-late differential +0.280 (CFG669)
- A3 clusters: eRASS1 A_MID 1.91/1.75; X-COP missing mass 3.0 (1.9-4.5) M_b; terciles after H-EX 1.27/1.59/0.96 (CFG687, CFG745, CFG815, CFG817)
- A4 groups: shift below the 2-sigma line 0.0645 dex; eFEDS passes the law (CFG745, CFG727)
- A5 late types / SPARC: zero free (rms 0.1009 / 0.0994 dex) (CFG695, CFG658)
- A6 massive clusters (ACCEPT): not overshot (CFG727, CFG815)
MUST NOT
- N1 young tidal dwarfs Newtonian; old TDG NGC 5557-E1 decides (CFG441, CFG763, CFG785 frozen only)
- N2 no capture channel (CFG744, CFG760-762, CFG749)
- N3 Bullet: collisionless, sigma/m <= 0.708 cm2/g, instant-response class excluded (CFG720, CFG722, CFG725)
- N4 conserved budget: supply 5.364 x own catchment baryons, own host only, so a free fraction F <= 1 (CFG647, CFG804, CFG727 control C1)
- N5 not capacity overflow (CFG721 H-OF = H-OF2)
- N6 not P-wave export or heating (CFG741, CFG760-762)
- N7 cold-to-DE conversion costs KiDS growth (CFG780; CFG779)
- N8 Solar System and wide binaries (CFG770, CFG740) [constrain the tether and the stiffness, not a distant free halo]
- N9 universal expelled-share rule at galaxy scale: F = 1 excluded; early-late +0.013 vs +0.280 (CFG810, CFG811)
- N10 merger memory, impulsive unbinding, unrelaxed placement, splashback: all NULL or FAIL (CFG726, CFG812, CFG818, CFG819)
SCALES WITH
- S1 hot gas: C = k M_hot, k = 2.9-3.6; state-blind k M_b fails groups (CFG745, CFG746)
- S2 host temperature: V < sqrt2 c_s(T_IGM) selector (CFG782)
- S3 binding in the tether frame: cold energy bound only by baryons, v >= 0.3 V_flat unbound; freed cold energy stays bound (CFG749, CFG812)
- S4 settling time: deficits fill and surpluses are expelled in ~50-100 t0, <= 1.4 Gyr in galaxies (CFG743, CFG747, CFG748, CFG776)
- S5 within-cluster mass dependence: tercile pattern non-monotonic; outer shear ~ M_gas^0.90 +- 0.21 (CFG687, CFG815, CFG817)
- S6 formation clock tau in [0.72, 3.47] Gyr for tethering (CFG763)

## 2. The three questions and their pass rules
- Q1 (pin): the conditions pin ONE functional form M_free = F x S for all of U (UFDs), E (early types), C (clusters) iff the needed-F
  intervals built in T2 (family A) or the needed-k intervals built in T3 (family B) have a NON-EMPTY common intersection that also
  satisfies N4 (F <= 1) and the E-differential of N9. Otherwise Q1 = NO and the pairs with empty pairwise intersection are named.
- Q2 (one constant): Q2 = YES iff Q1 = YES and the surviving constant (F or k) is a pure number or a function of {a0, Sigma_bar = a0/(pi G),
  M_b, tether-frame binding energy, c_s(T_IGM)} with no new dimensional scale. T5 (dimensional analysis) decides the "no new scale" part.
- Q3 (selector forced): Q3 = YES iff T1 finds a non-empty V_th window for BOTH footings and sqrt2 c_s(T_IGM) with T_IGM in [1e4, 2e4] K
  lies inside it for both, and R_ind enters with no free input. Otherwise Q3 = NO and R_ind is counted as an external input.

## 3. Pre-registered tests (trial count = 5; no others will be reported as tests)
### T1 selector window (CFG782 definitions, CFG317 per-object inputs)
- V_init = (G R_ind M_b,now a0)^(1/4), R_ind = CFG317 per-object leaky-box value (nominal yield -0.2) where it exists, else the CFG782
  OLS relation fitted on the same per-object table; R_ind >= 1. Flag SUDDEN iff V_init < V_th.
- S1: >= 90% of MW UFDs flagged. S2: <= 10% of each of MW classicals, M31 Collins, M31 LVD, LV field flagged. (SPARC omitted: it can only
  tighten S2, so an empty window without SPARC is empty with SPARC.)
- Exact window: lower bound L = the ceil(0.9 N_UFD)-th smallest UFD V_init; upper bound U_g = the (floor(0.1 N_g)+1)-th smallest V_init of group g.
  Window = (L, min_g U_g]. Report per footing, with the name of the object that sets each bound, and the implied multiplier
  lambda = V_th / c_s(T) at T = 1e4, 1.5e4, 2e4 K (mu = 0.59). sqrt2 corresponds to lambda = 1.4142.
- Control K1: at V_th = sqrt2 c_s(1.5e4 K), canonical, the group fractions reproduce `CFG782_unbinding_selector/cfg782_results.json` (UFD, classicals, Collins, LVD, field) to 1e-9.
- MUTATE: R_ind = 1 for all objects (as CFG782's MUTATE). The window must change; if it does not, T1 is void.

### T2 family A: M_free = F x 5.364 x M_exp (expelled-share family, the H-EX form), F universal
Needed-F intervals (all inputs below are frozen; ranges are the quoted ranges, not fitted):
- U: delta = 0.325 dex, sigma = 0.325/3.5 = 0.0929 dex (the weakest quoted significance). Ratio r_U = 10^(2 delta) - 1 = M_free(<r)/M_law(<r)
  (CFG784's estimator, sigma^2 proportional to enclosed mass). M_law(<r)/M_b,now = 1 + q x 5.364 with q = 3.5 (CFG336 median; declared factor-2 range
  0.5 q ... 2 q because the ledger row gives only the median). m_U = r_U x M_law/M_b. Supply S_U = 5.364 (R_ind - 1) M_b with R_ind = 10^2.07
  (CFG317 leaky-box median; PRIMARY), brackets R_ind = 6-30 (CFG336 lead) and R_ind = 10^3.65 (CFG317 R_need, different accounting).
  Because UFD data constrain only M_free inside r, F_U from this is a LOWER bound.
- E (amount): needed 0.55-0.80 M* inside 100 kpc (CFG745) over S_E = 5.364 (N - 1) M_b with N = 1/f_ret = 5.6-10 (CFG804) and M_b = M* (gas negligible).
  This assumes late types carry F = 0 (A5).
- E (differential): H-EX at F = 1 predicts early-late +0.013 dex against +0.280 +- 0.083 (CFG811). Small-signal linearity in F: F_diff = delta_obs / 0.013
  (range from +-0.083). F_diff must be <= 1 (N4).
- C: X-COP missing mass 3.0 (1.9-4.5) M_b (CFG745, canonical; alt median 2.74 reported only) over S_C = 5.364 (1/f_eff - 1) M_b with f_eff = 0.636-0.686 (CFG814).
  Intersect with F <= 1.
- Universal F exists iff the U (lower bound), E (amount) and C intervals intersect AND F_diff <= 1. Report all pairwise intersections.

### T3 family B: M_free = k x M_hot
- C: k = 2.88-3.62 (CFG745, four brackets). E: required M_hot 0.17-0.25 M* (CFG745) is a prediction (sealed CFG746), scored as PENDING, not as a pass.
- U: present hot gas = 0 so k_U is undefined (needed m_U > 0 against M_hot = 0): reported as a violation of family B as stated. Declared alternative
  reading (labelled post-hoc, one line): M_hot -> R_ind M_b ("ever-hot"); then k_U >= m_U / (R_ind M_b).
- Family B is "single-constant" iff k_U (alternative reading) and k_C overlap and M_hot,present reading is not needed.

### T4 single power law F proportional to M_b^p through U, E, C
- log M_b: U = median over the CFG317 UFD table (computed), E = 10.8, C in [13.0, 14.0] (eRASS1/X-COP gas-mass range, declared).
- p_EC range from the T2 intervals; p_UE upper bound from F_U lower bound and F_E upper bound. A single power law needs p_EC and p_UE ranges to overlap.

### T5 dimensional analysis
- The exponent matrix of (G, a0, M_b) in (L, M, T) has a null space of dimension 0 (no dimensionless combination). With c appended, one combination (G M_b a0 / c^4).
  With c_s appended, V_flat / c_s. Report V_flat = (G M_b a0)^(1/4) at the E and C masses, both footings, to size the break.
- A break between E and C, if required by T2/T4, needs a scale outside {G, a0, M_b}; it is counted as one new scale unless it is c_s(T_IGM) or c.

## 4. Verdict rule for the lane
- REDUCTION DERIVED: Q1, Q2 and Q3 all YES (a unified rule, no new constant, selector constants forced).
- CONSTRAINT TIGHTENED: at least one family branch is killed or one postulate case is shown to be a corollary, with the margin read from the results JSON.
- NO REDUCTION: neither. Then name the observation that would decide each open item.
- Incompatible pair: two conditions whose needed-quantity intervals under a common family have an empty intersection; name both CFG ids.

## 5. Negative controls
- T1: K1 reproduction + MUTATE R_ind = 1 (window must change).
- T2-T4: control N2: replace the E interval by the C interval; the overlap code must then report a non-empty intersection. If it does not, the interval logic is void.
- T5: control with a known case: (G, M, r) gives one combination (G M / r c^-2 style) when c is appended; the nullspace code must return it.

## 6. Compute gate
One process, <= 300 MB RSS, <= 60 s, nice -n 19, OMP_NUM_THREADS=1, inputs = small JSON/text only. The pgrep + chain.log check is run immediately before the script.
If it blocks, the script is delivered unrun and reported as queued.
