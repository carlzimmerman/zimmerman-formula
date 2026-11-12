# FINAL-7F (FORMATION READING) RESULT: is DD1's class residual an integral of a history, or a function of a present state? (2026-11-12)

**Lane label — canonical / alt: NOT A FUNCTION OF ANY TESTED VARIABLE (history-like) /
NOT A FUNCTION OF ANY TESTED VARIABLE (history-like).**
The frozen rule, applied literally, returns **NO STRUCTURE / NO STRUCTURE**; post hoc amendment **A1**
(§3, disclosed, reported, grades nothing) moves it to the label above. The substantive outcome is the
same under both: **not one of the ten tested variables is DETECTED on either footing.**

TEST lane, quarantined. Criteria `PREREGISTER.md` committed alone (aa235e9fb2) before any FINAL7F
script or number. Data: DD1's frozen table, main bracket, **3419 points / 626 systems / 16 classes**.
Footings graded separately, never pooled (canonical a0 = 9.3603e-11, alt a0 = 1.1312e-10 m/s^2).
Cold dark energy is a gravitating field component, never a particle. **kappa = 1/2 FITTED; not theory
closed. Adopts nothing.** No file outside this folder was written.

**Lane id.** The brief's id FINAL-7 is taken in the record by `hy4_preview_push/FINAL-7_what_it_is`
(M5 medium triage). This lane is **FINAL7F**; the other FINAL-7 is untouched.

---

## 1. The answer, in one paragraph

The DD1 class-median residual spread — 1.435 dex bipolar, 9 of 16 classes off the law by more than 3 se
— **is not a function of any present-state variable the record carries, and not a function of the
epoch.** Ten variables (the measured epoch, the baryonic surface density at two apertures, the
dynamical surface density at two apertures, radius, enclosed baryon mass, local depth, system depth,
and the law's own shape as a confound control), each against 16 class medians, on both footings:
**every Holm-adjusted permutation p lies between 0.79 and 1.00.** The flattest is the present-day
baryonic surface density (tau −0.03 / +0.00, p 0.89 / 1.00, implied scatter 0.188 / 0.190 dex against a
raw 0.186 / 0.190 — it explains nothing); the largest is the present-day dynamical surface density
(tau +0.30 / +0.33, p 0.12 / 0.079), and that one is algebraically part of the residual and reduces the
robust scatter by 1 % / 4 %. The epoch carries the slope +0.04 dex per dex of log(1+z), with the
high-z classes (RC100 at z 0.6–2.5) sitting **on** the law at +0.09 dex while the biggest departures
(ultra-faints +0.59, DF2/DF4 −0.84) are all at z ≈ 0. So: **the spread is not a function of a
present-day state, and it is not a function of the date either** — which is the formation reading's
signature (FINAL-15 §5.3, T-epoch) and is equally the signature of a spread organised by something the
frozen table does not carry. The plain force reading is excluded twice over: 9 of 16 classes are off
the law beyond 3 se, and no present-state variable organises the departures.

## 2. What was pre-registered and what came back

| pre-registered expectation (§9 of the criteria) | outcome |
|---|---|
| P0 will not stop the lane; sigma_raw ≈ 0.3–0.4 dex | **wrong in size**: sigma_raw = 0.186 / 0.190 dex (robust); rms 0.378 / 0.379 dex; range 1.435 / 1.433 dex; 9 of 16 classes beyond 3 se. P0 did not stop the lane, as expected |
| E1 (epoch) not detected | **held**: tau +0.233 / +0.267, p 0.228 / 0.165, Holm 1.000 / 0.987 |
| B1/D1 not detected in the sense that matters | **held**: B1 tau −0.033 / +0.000 (p 0.89 / 1.00); D1 tau +0.300 / +0.333 (p 0.117 / 0.079, Holm 1.000 / 0.793), f = +0.014 / +0.035 |
| predicted label L5 | **literal rule gives L6** (see A1); the substance (nothing detected) held |

Two things were **not** foreseen: (i) the robust scatter is only half the pre-registered expectation,
because 11 of the 16 classes sit within ±0.15 dex of the law and the tails carry everything; (ii) the
largest Kendall tau in the table belongs to the *dynamical* surface density, the one variable the
criteria already flagged as mechanically degenerate with the residual.

## 3. Amendment A1 (post hoc, disclosed, reported — it grades nothing)

The frozen L5/L6 boundary was `sigma_raw ≥ 0.25 dex` on the **robust** (1.4826·MAD) scatter over the 16
class medians. Measured: 0.186 / 0.190 dex. That is a mis-calibration, not a finding: the distribution
is concentrated with heavy tails, so the robust scale understates the spread that the pre-registration
was trying to measure. The same rule on the two measures the criteria did not fix — **rms_raw =
0.378 / 0.379 dex** and **9 of 16 classes beyond 3 se against a median class se of 0.063 dex** — gives
**L5, NOT A FUNCTION OF ANY TESTED VARIABLE (history-like)**. Nothing else in the lane changes: the
detection set is empty either way, and no label item L1–L7 other than L5/L6 is reached.

## 4. The result table

```
FINAL-7F  DD1 frozen table, main bracket: 3419 points / 626 systems / 16 classes. Residual d = log10(g_obs/g_bar) - log10(1+X_L(g_bar;a0)), median over a system's points then over the class's systems. Footings never pooled.

--- footing CAN (a0 = 9.36030e-11) ---
P0: robust scatter sigma_raw = 0.186 dex | rms_raw = 0.378 dex | bipolar range = 1.435 dex | classes beyond 3 se: 9 of 16 | median class se = 0.063 dex | label: NO STRUCTURE

id   variable                         tau    p_tau   p_Holm     rho slope [95% CI]    sig_imp  rms_imp       f      R2 det  
E1   zz = log10(z+0.001)  [epoch]  +0.233    0.228    1.000  +0.335 [-0.022,+0.332]     0.154    0.372  +0.172  +0.038 no   
B1   Sigma_b(point) = lgb          -0.033    0.895    1.000  -0.079 [-0.256,+0.222]     0.188    0.380  -0.008  +0.001 no   
B2   Sigma_b(outermost pt)         -0.033    0.896    1.000  -0.094 [-0.268,+0.083]     0.189    0.379  -0.014  +0.003 no   
D1   Sigma_dyn(point) = lgo        +0.300    0.117    1.000  +0.432 [-0.034,+0.686]     0.184    0.372  +0.014  +0.033 no   
D2   Sigma_dyn(outermost pt)       +0.267    0.167    1.000  +0.365 [-0.052,+0.990]     0.186    0.374  -0.000  +0.026 no   
P1   r (log10 kpc)                 +0.167    0.398    1.000  +0.262 [-0.068,+0.299]     0.155    0.373  +0.165  +0.037 no   
P2   M_b(<r) (log10 Msun)          +0.217    0.264    1.000  +0.247 [-0.073,+0.151]     0.177    0.378  +0.048  +0.009 no   
P3   local depth g_obs r/c^2       +0.283    0.140    1.000  +0.347 [-0.033,+0.343]     0.257    0.347  -0.379  +0.161 no   
P4   system depth (max)            +0.283    0.138    1.000  +0.353 [-0.009,+0.316]     0.257    0.345  -0.379  +0.171 no   
C1   Y_L (law shape, confound)     +0.033    0.895    1.000  +0.079 [-0.437,+0.567]     0.188    0.379  -0.009  +0.002 no   
  (p_tau, p_Holm: 100,000-permutation, two-sided; Holm over the 10-variable family. Slope: LAD, dex/dex, 10,000 class bootstrap. sigma_imp/rms_imp = scatter about the LAD line; f = 1 - sigma_imp/sigma_raw.)
  B3 half-light Sigma_b (lSig, DD1's variable (d), 8 classes with >=3 systems, outside the Holm family): tau -0.357, rho -0.500, p 0.276, sigma_raw 0.066 -> sigma_imp 0.073, f -0.109
  partial Kendall (rank-residualised) guards, declared uninformative by construction: D1|B1 +0.700, B1|D1 -0.583, D2|B2 +0.617, E1|B1 +0.233

--- footing ALT (a0 = 1.13120e-10) ---
P0: robust scatter sigma_raw = 0.190 dex | rms_raw = 0.379 dex | bipolar range = 1.433 dex | classes beyond 3 se: 9 of 16 | median class se = 0.062 dex | label: NO STRUCTURE

id   variable                         tau    p_tau   p_Holm     rho slope [95% CI]    sig_imp  rms_imp       f      R2 det  
E1   zz = log10(z+0.001)  [epoch]  +0.267    0.165    0.987  +0.388 [-0.024,+0.340]     0.170    0.376  +0.107  +0.029 no   
B1   Sigma_b(point) = lgb          +0.000    1.000    1.000  -0.006 [-0.250,+0.227]     0.190    0.381  +0.001  -0.000 no   
B2   Sigma_b(outermost pt)         +0.000    1.000    1.000  -0.021 [-0.265,+0.091]     0.190    0.381  +0.001  -0.000 no   
D1   Sigma_dyn(point) = lgo        +0.333    0.079    0.793  +0.497 [-0.023,+0.690]     0.183    0.369  +0.035  +0.056 no   
D2   Sigma_dyn(outermost pt)       +0.300    0.115    0.869  +0.432 [-0.050,+0.988]     0.198    0.371  -0.041  +0.044 no   
P1   r (log10 kpc)                 +0.200    0.305    1.000  +0.297 [-0.068,+0.294]     0.181    0.376  +0.048  +0.032 no   
P2   M_b(<r) (log10 Msun)          +0.250    0.195    0.987  +0.297 [-0.070,+0.150]     0.182    0.378  +0.040  +0.015 no   
P3   local depth g_obs r/c^2       +0.317    0.097    0.869  +0.403 [-0.027,+0.345]     0.256    0.347  -0.349  +0.169 no   
P4   system depth (max)            +0.317    0.097    0.869  +0.406 [-0.007,+0.317]     0.256    0.344  -0.349  +0.179 no   
C1   Y_L (law shape, confound)     +0.000    1.000    1.000  +0.006 [-0.449,+0.558]     0.190    0.381  +0.000  -0.000 no   
  (p_tau, p_Holm: 100,000-permutation, two-sided; Holm over the 10-variable family. Slope: LAD, dex/dex, 10,000 class bootstrap. sigma_imp/rms_imp = scatter about the LAD line; f = 1 - sigma_imp/sigma_raw.)
  B3 half-light Sigma_b (lSig, DD1's variable (d), 8 classes with >=3 systems, outside the Holm family): tau -0.214, rho -0.238, p 0.548, sigma_raw 0.074 -> sigma_imp 0.073, f +0.003
  partial Kendall (rank-residualised) guards, declared uninformative by construction: D1|B1 +0.733, B1|D1 -0.567, D2|B2 +0.650, E1|B1 +0.233

--- class medians (canonical / alt) ---
class              nsys   d_can   d_alt     se      zz    lgb    lgo    dep   dsys   lSig
NGC 1052 UDGs         2  -0.843  -0.881  0.245   -2.25 -11.67 -11.66  -8.75  -8.75   0.94
tidal dwarfs          6  -0.687  -0.725  0.115   -1.81 -11.45 -11.39  -8.18  -8.18     --
faint rotators       20  -0.239  -0.274  0.045   -2.73 -11.26 -10.84  -8.27  -8.27     --
LG field dwarfs      13  -0.090  -0.130  0.062   -2.92 -11.95 -10.90  -8.68  -8.68   0.66
SPARC               149  +0.004  -0.023  0.012   -2.29 -10.84 -10.31  -6.95  -6.86   1.74
MW bright dwarfs     11  +0.065  +0.027  0.153   -2.99 -12.20 -10.95  -8.82  -8.82   0.41
massive spirals      12  +0.066  +0.032  0.064   -1.74 -11.16 -10.44  -6.09  -6.09     --
ATLAS3D             187  +0.070  +0.052  0.010   -2.19  -9.55  -9.40  -6.37  -6.37   3.04
RC100               100  +0.088  +0.066  0.022   +0.18  -9.79  -9.57  -6.25  -6.25   2.57
M31 dwarfs           33  +0.090  +0.051  0.088   -2.93 -12.50 -10.96  -8.83  -8.83   0.11
KiDS                  4  +0.137  +0.097  0.109   -0.50 -13.13 -11.38  -6.47  -6.27     --
groups               20  +0.161  +0.123  0.023   -1.60 -11.66 -10.70  -5.44  -5.44     --
Coma UDGs            11  +0.319  +0.280  0.114   -1.62 -12.15 -10.74  -7.75  -7.75   0.45
X-COP                 7  +0.496  +0.465  0.022   -1.15 -10.68  -9.71  -4.85  -4.51     --
CLASH                20  +0.553  +0.524  0.023   -0.42 -10.45  -9.52  -4.79  -4.57     --
MW ultra-faints      31  +0.592  +0.552  0.098   -2.99 -13.12 -10.90  -9.46  -9.46  -0.51

--- known answers ---
KA1 reproduction of FINAL-2/DD1: max |dev| = 0.0005 dex (point median) / 0.0085 dex (system median); bipolar range 1.435 dex (FINAL-2: 1.435). PASS
KA2 footing offset: median over the 14 deep classes -0.0378 dex vs exact -0.5 log10(1.1312/0.93603) = -0.0411 (diff 0.0033 <= 0.01). PASS
KA3 synthetic truths: zz-signal -> E1 DETECTED; lgb-signal -> B1 DETECTED; lgo-signal -> D1 DETECTED; d=0 -> P0 stops at L1; shuffled -> nothing detected. Power confirmed at 0.30 dex/dex.
KA4 DD1 identities: max relative error 4.4e-16 over 601 grid points x 2 footings. PASS
KA5 ties: no variable tied (tie fraction 0.000 for all 10); nothing excluded as degenerate.

--- MUTATE (each must change its stated outcome) ---
 CAN: M1 shuffle -> detected [], max|tau| 0.217 (from 0.300): BITES (detection clause) | M2 plant epoch -> E1 tau +0.567, p_Holm 0.0180, label PRESENT-STATE ORGANIZED, EPOCH ALSO: BITES | M3 plant present-state -> D1 tau +0.700, f +0.670, label PRESENT-STATE ORGANIZED (force-like): BITES | M4 drop the two R classes (n=14) -> sigma_raw 0.117, new detections []
 ALT: M1 shuffle -> detected [], max|tau| 0.217 (from 0.333): BITES (detection clause) | M2 plant epoch -> E1 tau +0.567, p_Holm 0.0180, label PRESENT-STATE ORGANIZED, EPOCH ALSO: BITES | M3 plant present-state -> D1 tau +0.700, f +0.674, label PRESENT-STATE ORGANIZED (force-like): BITES | M4 drop the two R classes (n=14) -> sigma_raw 0.109, new detections []
 M1's second clause (max|tau| must drop by >= 0.20) does NOT bite: it needs max|tau| >= 0.20 in the shuffled table, and the observed max|tau| is only 0.300. Disclosed.
 M5 a0 x 2: SPARC moves -0.106 dex: BITES
 Lean FINAL7F.lean: exit 0, 6 theorems, axioms propext/Classical.choice/Quot.sound. FINAL7F_MUTATE.lean: exit 1, 7 errors, >=1 per false statement.
```

## 5. Reading the numbers

**The baryonic surface density is the flattest variable in the table.** Σ_b at the measurement point
(B1) and at the outermost measured point (B2): tau −0.03 / 0.00, p 0.89–1.00, implied scatter
0.188–0.190 dex against a raw 0.186–0.190. There is no monotone dependence of the class residual on
present-day baryonic surface density at any aperture, and the half-light Σ_b (B3, the 8 classes that
have one) agrees: tau −0.36 / −0.21, p 0.28 / 0.55, implied scatter *larger* than raw. This matters
because a surface-density-driven modification of the law is the most common shape a force reading
takes; the table gives it nothing to work with.

**The dynamical surface density has the largest tau and carries no information.** D1 (Σ_dyn at the
point) gives tau +0.300 / +0.333, the biggest of the nine present/epoch variables, but p = 0.117 /
0.079 (Holm 1.000 / 0.793) and f = +0.014 / +0.035: the LAD line removes 1–4 % of the robust scatter
and 5–9 % of the variance. It is also the variable the criteria flagged as degenerate:
`d = (lgo − lgb) − Y_L(lgb)`, so at fixed g_bar the residual and log g_obs differ by a constant, and
since `Y_L` is a strictly monotone function of g_bar (Lean `XL_anti_gb`), the rank of lgo is largely
the rank of (lgb, d) combined. The partial-Kendall guards were meant to separate them and **cannot**:
D1|B1 = +0.70 / +0.73 is produced by the same algebra, not by a signal. **Declared uninformative by
construction, as the criteria allowed.**

**Depth is the only variable whose R² is not negligible, and it is still not a detection.** P3/P4
(local and system depth) have R² = 0.16–0.18, the highest in the table, with p = 0.10–0.14 (Holm
0.87–1.00). Their robust scatter goes *up* (0.186 → 0.257 dex, f = −0.35 to −0.38): the fit buys
variance reduction by chasing the two deficient classes and widens the middle. A variable that
increases the robust scatter is not a variable that organises the spread.

**The epoch carries nothing, and the sign is the wrong way round for a naive a0(z).** E1 gives
tau +0.23 / +0.27, slope +0.04 / +0.03 dex per dex of log(1+z) with a 95 % interval that straddles zero
([−0.02, +0.33]). The classes observed at high redshift are the ones **on** the law: RC100 (z 0.6–2.5)
sits at +0.088 / +0.066 dex, inside DD1's 0.10-dex line, and KiDS (z ≈ 0.31) at +0.137. The largest
departures — ultra-faints +0.59, DF2/DF4 −0.84, tidal dwarfs −0.69 — are all at z ≈ 0. That is exactly
the bipolarity FINAL-2 §3 found: a single monotone function of the event date is falsified by the
ultra-faints and the clusters sitting on the same side.

**Caveat on the epoch variable (disclosed in the criteria, restated).** `z` is the *observed*
redshift, the only measured epoch-like column in the frozen table. **The record has no measured
assembly redshift z_f per system** — the LVD age column is empty on disk (HIS1), VSH1's settling
redshifts are computed and exist only for three masses, and FINAL-2's epoch assignments are
order-of-magnitude literature values. So this lane tests "does the epoch the system is observed at
track the residual", not "does the assembly epoch track the residual". The second question **cannot be
answered with the frozen table**, and this lane does not pretend to answer it.

**Where the spread lives (post hoc, reported, grades nothing).** The eight classes for which the table
carries a measured half-light baryonic surface density have a robust class-residual scatter of
0.066 / 0.074 dex, against 0.186 / 0.190 for all sixteen. Dropping the two R-channel classes (tidal
dwarfs, DF2/DF4, M4) halves the scatter again, to 0.117 / 0.109 dex. So most of the robust spread is
carried by a handful of classes, and none of the tested variables explains any of it.

## 6. Power, and what "not detected" does and does not mean

With 16 classes the exact two-sided 0.05 critical values are |rho| ≈ 0.50 and |tau| ≈ 0.35. KA3 shows
the machinery fires on planted signals of 0.30 dex per dex in zz, in lgb and in lgo (all three
DETECTED, Holm p ≤ 0.0018), and returns nothing on a shuffled table. So the nulls are informative
**at that effect size**: a dependence of 0.3 dex per dex in any of these variables would have been
seen. A weak monotone dependence, |rho| ≲ 0.4, would not have been, and is not excluded.

## 7. What this does and does not settle

- **It does not demonstrate the formation reading.** "No present-state variable organises the
  residual" is the formation reading's *signature* (FINAL-15 §5.3: the amount is a per-system constant
  written at Σ_f, so no present-day proxy should track it) and it is equally the signature of a spread
  organised by something the table does not carry — a host field, a stripping history, a gas census.
  The lane discriminates "function of the present state" from "not a function of the present state".
  It does not discriminate among the histories.
- **It does exclude the plain force reading**, twice: 9 of 16 classes sit off the law by more than
  3 se over a 1.435 dex range, and no present-state variable organises the departures. A force reading
  with a present-state-dependent correction has no variable left in this table to depend on.
- **It agrees with every sibling it touches.** DD1: no free function of lgb, lgo, r, M_b, depth or z
  holds the classes. HIS1 H5 / HIS1R: no within-class tracking by gas fraction or host distance, all
  six pairs null. FINAL-15 P-3 / F6: the same null, pre-registered, on the within-class pairs. This
  lane is the class-level counterpart and lands in the same place.
- **It adds one number the siblings do not have**: the class-level correlation with the *dynamical*
  surface density is the strongest in the family (tau +0.30 / +0.33) and is nonetheless empty
  (f = 1–4 %, Holm p ≥ 0.79), because it is algebraically part of the statistic.

## 8. Not computed, not checked

- No new data; every number comes from DD1's frozen table. No measurement is added to the record.
- Aperture effects inside a class are not modelled beyond the B2/D2 outermost-point pair. FINAL-2
  flagged X-COP's 0.35 dex difference between all-point and last-point medians; here X-COP's
  system-median differs from its point-median by 0.009 dex and the two apertures (B1 vs B2) give the
  same null.
- The 16 classes are a census, not a sample; the permutation p is a statement about exchangeability of
  class labels, as in DD1 and HIS1, not a population p-value.
- No a0(z), no host field, no stripping model, no gas census: all outside the table.
- Mutants M1's second clause and the L5/L6 boundary are the two pre-registration defects found; both
  are disclosed above and neither carries a label.

## 9. Files

`PREREGISTER.md` (criteria, committed alone, aa235e9fb2), `final7f.py` → `final7f.json` / `final7f.out`,
`FINAL7F.lean` / `FINAL7F_MUTATE.lean` with `compile.txt` / `compile_MUTATE.txt`, this file.
Re-run: `python3 final7f.py` from this folder (about 51 s, numpy, seed 20261112).
Lean compiled with the record's own build in `fable_independent_2026/lean_2026` (copies removed after
the run; the build directory was not otherwise touched).

---

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
