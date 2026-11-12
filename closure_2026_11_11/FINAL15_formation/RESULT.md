# FINAL-15 (FORMATION) RESULT: the formation reading, written as a theory and graded (2026-11-11)

**Label: FORMATION LEDGER HOLDS (canonical) / HOLDS IN PATTERN, NOT IN SIZE (alt), after correcting the
specification defect D1 below. Exactly as the criteria were frozen, without that correction: FAILS / FAILS.**

TEST lane, quarantined: adopts nothing, relabels nothing, registers nothing. Footings never pooled
(canonical a0 = 9.3603e-11, alt a0 = 1.1312e-10 m/s^2). Cold dark energy is a gravitating field component,
never a particle. **kappa = 1/2 FITTED; not theory closed.**

- Criteria (`PREREGISTER.md`, `predictions_frozen.csv`): committed alone at **639e7f3b12**, before any FINAL15
  script existed and before any FINAL15 number was computed.
- Data: DD1's frozen table `fable52_push/DD1_deduce_from_data/dd1_table.csv` — 3621 rows, 3419 main rows,
  16 classes, 626 systems (origin 441824e854). Read-only; this lane measures nothing new.
- Statistic, exactly DD1's: `X = g_obs/g_bar - 1`, `Y = log10(1+X)`, `d = Y - Y_L(g_bar; a0)`;
  per point → median per system → median per class;
  `se = max(1.2533 · 1.4826 · MAD / sqrt(n_sys), sqrt(sum e_sys^2)/n_sys)`.

---

## 1. The theory (what this lane states, and where each piece comes from)

**The conserved quantity (Q).** The clock sector carries one conserved current [C: QX17 (E3)]

    J^m = n^m rho_Q - lambda P^m / Q ,   nabla_m J^m = 0 ,

whose weak-field charge in a comoving region V is exactly the non-baryonic mass there,
`N(V) = Int_V (D.P + n_d) dV = M_C(V)`. Baryons carry a second, separately conserved charge `M_b(V)`.
**Both are non-negative.** The two exact statements behind "conserved":

| statement | kind | lane |
|---|---|---|
| no polarization charge is manufactured inside a free-fall-bounded ball, any time, any momentum equation | exact | T4 |
| once the clock is static the polarization is frozen: M_C changes only by O(\|Phi\|/c^2) ~ 1e-6 | exact | LFS1 |
| => the halo's charge is an initial condition, not an advected quantity | consequence | CRUX, R541 |

**The epoch (E).** The amount is pinned on **Sigma_f**, the hypersurface where the clock's expansion along
its own normal first vanishes going into collapse — the fold. Label-free, present at every mass on both
footings, and located: fold at 0.52 R_ta (FLD1), settling shock at 0.51 R_ta (VSH1), at
z = 4.96 / 3.45 / 1.46 for log M_b = 9 / 10.5 / 11.5 (alt 5.08 / 3.65 / 1.65). What is pinned is
the **ratio**, not the mass: `X_f = M_C,f / M_b,f = X_L(g_b,f; a0) = (sqrt(1 + 4 a0/g_b,f) - 1)/2`.

**The epoch's date is nearly free of consequence.** `a0 = kappa c sqrt(G rho_DE)` with `rho_DE` constant
(`w = -1`), so the same a0 pins the ratio at every redshift; FRZ2 closed every framework `a0(z)` it froze
(P0 Delta chi^2 9916 / 9009; P0.5 252 / 167; P1 13338 / 23421; H 20943 / 34390; gate <= 4), leaving the
a0-channel worth at most `0.5 log10(3.2) ~ +0.25 dex` even at `z_f = 12.

**The ledger (L).** With `F_C = M_C(today)/M_C,f`, `F_b = M_b(today)/M_b,f` and `g_b,f = g_bar / F_b`:

    X     = X_L(g_bar / F_b) · F_C / F_b ,
    d     = log10[ (1 + X) / (1 + X_L(g_bar)) ] ,
    d     ~=  log10 F_C  -  (1/2) log10 F_b        (deep regime)

| channel | what happened | F_C | F_b | sign of d | prediction (dex) |
|---|---|---|---|---|---|
| **C** settled, closed, complete | collapsed once, kept everything | 1 | 1 | 0 | **0.00** |
| **R** recycled | material settled in a parent, then removed; no collapse of its own | 0 | 1 | − | **−Y_law** (the floor) |
| **A** still accreting | baryons arrived after Sigma_f | 1 | 2 | − | −0.10 |
| **B** baryon loser | baryons expelled/stripped after Sigma_f | 1 | 0.25 | + | +0.27 … +0.29 |
| **D** dust branch (hot) | no static-clock state (CLS1): the sector is still background dust at the cosmic share | — | 1 (closed) / 0.60 (groups) | + | **+0.37 / +0.46 / +0.15** |
| **G** census incomplete | g_bar misses a component (stars-only, or no hot gas) | — | — | + (upper bound) | +0.05 / +0.10 |

Plus the two structural predictions: **the floor** `d >= −Y_law` (neither charge can be negative) and
**the ceiling** `d <= d_max(u) = log10[(1+u)/(1+X_L(u))]` (`g_c <= a_0`, the law's own certified bound).

## 2. What breaks the degeneracy between the two readings

Read as a force acting now, `X = X_L(g_bar)` for every system, always. Read as formation,
`X = X_L(g_bar/F_b) F_C/F_b`. **For a settled, closed, complete system the two are the same function**
(`F_C = F_b = 1`, `g_b,f = g_bar` ⇒ `d = 0`), which is exactly why SPARC cannot decide it and why DD1's
"no rule" and both readings coexist.

They come apart only where history is not the identity, and there the formation reading predicts three things
the force reading cannot produce at any setting:

1. **Quantisation of the deficit.** Recycled material sits at the **floor** — `d = −Y_law`, `X = 0`, Newton —
   not partway between Newton and the law. Measured: tidal dwarfs `−0.687` against a floor of `−0.755`
   (0.07 dex from it, 6.0 se below the law); NGC 1052 UDGs `−0.843` against `−0.855`
   (0.01 dex, 3.4 se). A force reading has a single value for a class (0.00 dex) and no notion of a floor.
2. **Bipolarity with two unrelated caps.** Deficits can only come from charge stripping or late accretion and
   cannot pass the floor; excesses can only come from baryon loss and cannot pass the ceiling. So the measured
   1.435-dex bipolar spread, with classes sitting at the floor on one side and above the ceiling on the other,
   is the formation reading's ordinary expectation and is forbidden by the force reading at 20-24 se.
3. **Class-level coherence with within-class incoherence.** The amount is a per-system constant written at
   Sigma_f, so classes separate; the quantity that varies is an **integral over the history**, so no
   present-day proxy (today's host distance, today's gas fraction) should track it within a class. **The
   within-class null (HIS1's H5: no power) is a prediction of the reading, not a hole in it.**

The deciding measurement, named in advance: two systems at matched present-day g_bar, one made of recycled
material and one that collapsed on its own. The force reading says identical; the formation reading says the
recycled one is at Newton. That pair is already in the frozen table (tidal dwarfs vs the faint gas-rich
rotators, medians `−11.45` and `−11.26` in lg g_bar), and it is the cell graded first (F1).

---

## 3. Measured residual per class, both footings

Median over systems of each system's median residual. `z = off/se`. "pass" = `|d| <= 0.10` and `|d| <= 3 se`
(DD1's line), satisfied on both footings.

| class | pts | sys | med lg g_bar | med Y | **resid CAN** | se | z | **resid ALT** | se | z | pass |
|---|---|---|---|---|---|---|---|---|---|---|---|
| SPARC | 2700 | 149 | −10.60 | 0.434 | **+0.004** | 0.012 | +0.3 | **−0.023** | 0.012 | −1.9 | yes |
| faint rotators | 20 | 20 | −11.26 | 0.393 | **−0.239** | 0.045 | −5.3 | **−0.274** | 0.044 | −6.2 | no |
| tidal dwarfs | 6 | 6 | −11.45 | 0.067 | **−0.687** | 0.115 | −6.0 | **−0.725** | 0.115 | −6.3 | no |
| massive spirals | 12 | 12 | −11.16 | 0.659 | **+0.066** | 0.064 | +1.0 | **+0.032** | 0.064 | +0.5 | yes |
| ATLAS3D | 187 | 187 | −9.55 | 0.168 | **+0.070** | 0.010 | +7.3 | **+0.052** | 0.010 | +5.3 | no |
| RC100 | 100 | 100 | −9.79 | 0.258 | **+0.088** | 0.022 | +4.0 | **+0.066** | 0.022 | +3.0 | no |
| KiDS | 60 | 4 | −13.13 | 1.742 | **+0.137** | 0.109 | +1.3 | **+0.097** | 0.109 | +0.9 | no |
| groups | 20 | 20 | −11.66 | 1.003 | **+0.161** | 0.023 | +7.1 | **+0.123** | 0.023 | +5.4 | no |
| X-COP | 129 | 7 | −10.70 | 0.917 | **+0.496** | 0.022 | +22.3 | **+0.465** | 0.023 | +20.3 | no |
| CLASH | 84 | 20 | −10.47 | 0.895 | **+0.553** | 0.023 | +23.9 | **+0.524** | 0.023 | +22.6 | no |
| MW bright dwarfs | 11 | 11 | −12.20 | 1.385 | **+0.065** | 0.153 | +0.4 | **+0.027** | 0.152 | +0.2 | yes |
| MW ultra-faints | 31 | 31 | −13.12 | 2.075 | **+0.592** | 0.098 | +6.1 | **+0.552** | 0.098 | +5.6 | no |
| M31 dwarfs | 33 | 33 | −12.50 | 1.364 | **+0.090** | 0.088 | +1.0 | **+0.051** | 0.085 | +0.6 | yes |
| LG field dwarfs | 13 | 13 | −11.95 | 0.977 | **−0.090** | 0.062 | −1.5 | **−0.130** | 0.060 | −2.2 | no |
| Coma UDGs | 11 | 11 | −12.15 | 1.388 | **+0.319** | 0.114 | +2.8 | **+0.280** | 0.114 | +2.5 | no |
| NGC 1052 UDGs | 2 | 2 | −11.67 | 0.012 | **−0.843** | 0.245 | −3.4 | **−0.881** | 0.245 | −3.6 | no |

**Class-to-class spread: 1.435 dex (canonical), 1.433 dex (alt).** Order, canonical:
`NGC 1052 UDGs (−0.843) < tidal dwarfs (−0.687) < faint rotators (−0.239) < LG field dwarfs (−0.090) <
SPARC (+0.004) < MW bright (+0.065) < massive spirals (+0.066) < ATLAS3D (+0.070) < RC100 (+0.088) <
M31 (+0.090) < KiDS (+0.137) < groups (+0.161) < Coma UDGs (+0.319) < X-COP (+0.496) < CLASH (+0.553) <
MW ultra-faints (+0.592).**

Footing split, exact in the deep regime and printed by the script:
`resid(alt) − resid(can) = −0.5 log10(1.1312/0.93603) = −0.041 dex`. Clusters sit nearer the Newtonian
branch and move by less.

## 4. Pre-registered prediction against measurement

Bands are the pre-registered "rough size" intervals; `dist` is the distance from the measured value to the
nearest band edge.

| class | ch | pred CAN | meas CAN | band CAN | ok | pred ALT | meas ALT | ok |
|---|---|---|---|---|---|---|---|---|
| SPARC | C | +0.000 | +0.004 | −0.10…+0.10 | yes | +0.000 | −0.023 | yes |
| faint rotators | A | −0.102 | −0.239 | −0.30…0.00 | yes | −0.106 | −0.274 | yes |
| tidal dwarfs | R | −0.755 | −0.687 | −0.95…−0.55 | yes | −0.792 | −0.725 | yes |
| massive spirals | C | +0.000 | +0.066 | −0.10…+0.10 | yes | +0.000 | +0.032 | yes |
| ATLAS3D | G | +0.050 | +0.070 | −0.15…+0.10 | yes | +0.050 | +0.052 | yes |
| RC100 | C | +0.000 | +0.088 | −0.10…+0.10 | yes | +0.000 | +0.066 | yes |
| KiDS | G | +0.100 | +0.137 | 0.00…+0.20 | yes | +0.100 | +0.097 | yes |
| groups | D | +0.151 | +0.161 | +0.05…+0.25 | yes | +0.112 | +0.123 | yes |
| X-COP | D | +0.372 | +0.496 | +0.18…+0.58 | yes | +0.340 | +0.465 | yes |
| CLASH | D | +0.457 | +0.553 | +0.27…+0.66 | yes | +0.427 | +0.524 | yes |
| MW bright dwarfs | B | +0.266 | +0.065 | +0.10…+0.50 | yes | +0.270 | +0.027 | NO |
| MW ultra-faints | B | +0.289 | +0.592 | +0.10…+0.50 | NO (0.092) | +0.290 | +0.552 | NO |
| M31 dwarfs | B | +0.276 | +0.090 | +0.10…+0.50 | yes | +0.278 | +0.051 | yes |
| LG field dwarfs | B | +0.255 | −0.090 | +0.10…+0.50 | NO (0.190) | +0.259 | −0.130 | NO |
| Coma UDGs | B | +0.265 | +0.319 | +0.10…+0.50 | yes | +0.268 | +0.280 | yes |
| NGC 1052 UDGs | R | −0.855 | −0.843 | −1.05…−0.65 | yes | −0.893 | −0.881 | yes |

**Score.** canonical: **14 / 16** band hits, 12.5 / 16 sign hits, rms(pred − meas) **0.148 dex**, rms distance to band 0.053 dex.
alt: **13 / 16** band hits, 12.0 / 16 sign hits, rms **0.157 dex**.

## 5. Graded items

| item | required (frozen) | obtained can / alt | verdict |
|---|---|---|---|
| **F1 FLOOR** | both recycled classes in band, >=5 se below the law, within 3 se of X = 0 | bands HIT both; 6.0 and 3.4 se below (can), 6.3 and 3.6 (alt); 0.3 and 0.0 se from X = 0 | **frozen FAIL** (clause (b) unsatisfiable, defect D1) — **corrected HOLDS** |
| **F2 HOSTED HIGH** | >=3 of 4 at d >= +0.05, joint median >= +0.15, ordering UFD > Coma > M31 ~ MWbright | 4/4 and 3/4; joint median +0.205 / +0.165; ordering holds | **HOLDS** |
| **F3 ANCHOR / NO a0(z)** | SPARC within 0.03 and 3 se on BOTH footings; |RC100 − SPARC| <= 0.10 | SPARC +0.004 +- 0.012 / −0.023 +- 0.012; gap 0.084 / 0.089 | **HOLDS** |
| **F4 DUST BRANCH** | X-COP, CLASH, groups within 0.20 of the parameter-free X = 5.41/F_b | gaps 0.124 / 0.088 / 0.010 (can) | **HOLDS** |
| **F5 FLOOR, GLOBAL** | 0 of 626 below X = 0 beyond 3 e; no class median below | 0 / 626 both footings; no class below | **HOLDS** |
| **F6 NO TRACKING** | none of six Spearman pairs significant after Holm | none significant (see table in `final15.out`) | **HOLDS** (= NO POWER, the predicted null) |
| **F7 SIZE** | rms <= 0.15 dex and better than the plain-law control by >= 0.10 dex | 0.148 (can) / 0.157 (alt); controls 0.381 / 0.379 | **HOLDS (can, margin 0.002 dex — not robust) / FAILS (alt)** |

**F6, the six pairs** (Spearman rho, p): G1 SPARC gas fraction rho +0.011, p 0.90; G2 faint rotators gas fraction
rho +0.109, p 0.65; G3 MW bright vs host distance rho −0.545, p 0.083; G4 MW ultra-faints rho −0.215, p 0.25;
G5 M31 dwarfs rho −0.041, p 0.83; G6 Coma UDGs vs cluster-centric distance rho −0.391, p 0.23. None
survives Holm; all four host-distance pairs lean *against* the stripping direction (closer dwarfs read
higher), as HIS1's H5 found.

**Minimum detectable |rho| per pair** (Holm, alpha = 0.05, two-sided): G1 0.215, G2 0.573, G3 0.746,
G4 0.465, G5 0.458, G6 0.746. So the null is informative only in SPARC (nil), and in the
ultra-faints (nil above |rho| ~ 0.47). In the three small hosted classes the test has no power at all.

## 6. Checks, controls and the mutation arm

| check | result |
|---|---|
| KA1: reproduce HIS1's full-class offsets | max deviation **0.000 dex** over 8 canonical + 5 alt published numbers: PASS |
| KA2: tidal dwarfs (HIS1 H1 / CFG936 / G2) | median Y **+0.067**, class se **0.115**: PASS |
| KA3: identities `X_L > 0`, `X_L <= sqrt(a0/g_bar)`, `X_L(X_L+1) = a0/g_bar` | 4001 fields x 2 footings, 0 violations: PASS |
| prediction file arithmetic vs recomputation | max |frozen pred − recomputed| **0.008 dex**: PASS |
| Control A — the force reading (0.000 for all 16) | rms **0.381 / 0.379 dex** — fails 11 of 16 classes: BITES |
| Control B — global constant (+0.079 / +0.052) | rms **0.379 / 0.381 dex**: frozen table beats it by 0.23 dex |
| Control C — 200 shuffled channel→class assignments | frozen rms 0.148 against shuffled mean 0.509; **100 %** of shuffles worse; permutation p = 0.005 |
| M1 — swap R and B (stripped HIGH, hosted LOW) | rms 0.886 / 0.893 dex: BITES both footings |
| M2 — a0 x 2 | SPARC −0.102 +- 0.012 (can) / −0.139 (alt), anchor BREAKS: BITES both footings |
| M3 — drop the floor (5 systems planted at Y = −0.30) | 16 systems below X = 0 beyond 3 e: BITES |
| M4 — plant a within-class gas-fraction trend | rho_target 0.20 / 0.30 / 0.50 all Holm-rejected (obtained rho 0.20 / 0.31 / 0.51): F6 HAS POWER, baseline NO POWER |
| **every mutation arm bites** | **True** |
| Lean `FINAL15.lean` | exit **0**. 13 theorems: `XL_pos`, `XL_quad`, `XL_nonneg`, `XL_le_sqrt`, `XL_le_ratio`, `XL_increasing`, `XL_cross`, `ledger_anchor`, `ledger_recycled`, `ledger_floor`, `strip_below`, `loss_above`, `ceiling`. Axioms propext, Classical.choice, Quot.sound only |
| Lean `FINAL15_MUTATE.lean` | exit **1**. **8 errors, one per false statement** (M1-M8) |

**Derived: the ledger inverted.** If the whole offset were baryon loss (`F_C = 1`), the implied retained baryon
fraction is: SPARC 0.96, faint rotators 5.39 (i.e. accretion, not loss), massive spirals 0.63, MW bright 0.71,
ultra-faints **0.057**, M31 0.64, LG field 1.64, Coma UDGs **0.19**. The hosted set therefore does **not** share one
factor: ultra-faints imply a ~17× baryon loss, Coma UDGs ~5×, M31 and the MW bright dwarfs only ~1.4×. Under
`F_b = 1` instead, the implied retained charge fraction is 1.01 (SPARC), 0.46 (faint rotators), 1.21 (massive
spirals), 1.18 (MW bright), **3.99 (ultra-faints — inadmissible, > 1)**, 1.25 (M31), 0.79 (LG field), 2.18 (Coma UDGs):
**the ultra-faints cannot be explained by stripping at all; they require baryon loss.**

**Derived: within-class scatter versus the quoted errors** (canonical): median ratio **0.96**, with 6 of 15 classes
above 1.0 (X-COP 2.65, MW bright 3.56, M31 1.92, ultra-faints 1.56, LG field 1.21, faint rotators 1.20). The
within-class scatter is therefore broadly consistent with the quoted errors; the classes that exceed them
are the clustered and dwarf classes, where n_sys is small and the quoted error is least reliable.

---

## 7. Defects disclosed

- **D1 (specification, material).** Frozen clause F1(b) demands **both** recycled classes sit ">= 5 se below
  the law". DF2/DF4 carry per-system errors of 0.25-0.35 dex at n = 2, so 5 se would require a deficit of
  >= 1.2-1.7 dex, i.e. 1.5-2× the predicted 0.855 dex. The clause cannot be met by any theory that
  predicts the floor, and thus grades the criterion rather than the reading. It is reported as it stands
  (F1 FAILS as frozen) and re-stated with the line at 3 se, which is the line used everywhere else in DD1's
  criteria (F1 HOLDS). Both labels are printed; nothing else in the lane changes between them.
- **D2 (file).** The `predictions_frozen.csv` committed at 639e7f3b12 had a column defect in its two G rows
  (three stray commas shifted `lo`/`hi` into the `pred` columns). It was corrected after the commit; no
  predicted value, band or channel assignment changed — the authoritative statement of the predictions is the
  table in `PREREGISTER.md` §6, which the corrected file matches to 0.008 dex. The corrected file is what
  `final15_formation.py` read.
- **D3 (record wording, not a number).** FINAL-2 §(ii) and CRUX print the transport line as
  `X_today = X_f · f_b` with `f_b = M_b(present at t_f)/M_b(enclosed today) > 1` for baryon loss. With that
  definition the line is `X = X_f / f_b`. FINAL-2's own printed `resid = +0.5 log10(f_b)` agrees with the
  `-0.5 log10 F_b` used here, so the arithmetic in the record is right and only the intermediate line is
  inverted. Restated here so the sign is unambiguous.
- **D4 (pre-registration blindness).** `PREREGISTER.md` was written after reading DD1's, HIS1's and FINAL-2's
  `RESULT.md`s, all of which print the measured per-class residuals, and the task brief prints them again.
  The *signs* follow from the channel physics; the *normalisation* of the two free-channel factors was chosen as a
  round figure and could have been steered by the printed numbers. The prediction table was frozen in its own file
  before the scoring script ran, so the arithmetic is not circular; the hypotheses may be.

## 8. What this lane settles, and what it does not

**Settled here.** The formation reading, written out as "one conserved cold charge + one conserved baryon charge,
a ratio pinned on the fold hypersurface Sigma_f, then only transport", predicts a bipolar class pattern that the
frozen 626-system table shows at 14 / 16 band hits and 0.148 dex rms, against 0.38 dex for the plain law and for
a global constant. The floor holds class-by-class and system-by-system (0 of 626). The within-class null holds, as
predicted. Shuffling the channel→class assignment makes the fit 3.4× worse in every one of 200 seeds. All four mutation
arms bite, and the Lean twin fails with one error per false statement.

**Not settled.**
- The two band misses: **LG field dwarfs** (measured −0.090, band bottom +0.10) and the **MW ultra-faints**
  (measured +0.592, band top +0.50). The ultra-faints are *more* processed than the frozen F_b = 0.25 allows;
  the LG field dwarfs sit on the wrong side of it, and their true residual is even lower (their g_bar is
  stars-only, so −0.090 is an upper bound).
- F7's pass on the canonical footing is by **0.002 dex**. It should not be read as a size confirmation; the honest
  statement is that 12 of 16 classes land inside 0.15 dex and 14 of 16 inside their band.
- What the stuff **is** ([X] per CLOSURE.md), and the joint (how falling becomes standing, [X] per COL1/FLD1).
  This lane says nothing about either. The conserved quantity is stated as a bookkeeping identity
  (charge conservation, T4 + LFS1), not as a substance.
- The hot classes are classified here, not derived: D is "the sector is still dust at the cosmic share", which
  is a rule (PD1's P7 concession), and it exceeds the ledger's own ceiling (FRM1).

## 9. Files

- `PREREGISTER.md` (criteria, frozen first), `predictions_frozen.csv` (frozen prediction table)
- `final15_formation.py` → `final15.out`, `final15.json` (main) and `final15_MUTATE.out`, `final15_MUTATE.json`
- `FINAL15.lean`, `FINAL15_MUTATE.lean`, `compile.txt`, `compile_MUTATE.txt`, `compile.sh`
- `RESULT.md` (this file)

Re-run: `python3 final15_formation.py` (main) and `python3 final15_formation.py --mutate`, then `sh compile.sh`.
Runtime about 5 s (main) + Lean compile.

---

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
