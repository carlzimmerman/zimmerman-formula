# FINAL-15 (FORMATION) — the formation reading written as a theory, and graded (2026-11-11)

FINAL MILE, lane **FINAL-15 (FORMATION)**. TEST lane, quarantined. Adopts nothing, relabels nothing,
registers nothing. Footings never pooled (canonical a0 = 9.3603e-11, alt a0 = 1.1312e-10 m/s^2).
Cold dark energy is a gravitating field component; no particle is added anywhere.
**kappa = 1/2 FITTED; not theory closed.** This lane edits nothing outside its own folder.

**Lane id.** The brief names this lane FINAL-15 (FORMATION). Short id on files: **FINAL15**. Checked free:
no `closure_2026_11_11/FINAL15*` exists and no commit subject names FINAL15, FINAL-15 or formation_theory.

**Siblings consulted, not redone.** HIS1 (the history reading, 4 of 5 statements, DD1's table), HIS1R (blind
regrade, same label), DD1 (the frozen 626-system / 16-class table; "no rule among the candidates"), FINAL2
(EPOCH: which event dates the amount; the a0-channel is capped at ~+0.25 dex), FINAL3 (share derivation),
FINAL4 (GROWTH, R_set = r_ta), FINAL6 (KAPPA: is kappa an output), CRUX / T4 / LFS1 (the conservation cap),
CLS1 (no static-clock state in clusters), RB1 (retention), CFG936 / G2 (tidal dwarfs at Newton), DG1 (dwarf gas
history), ELA1 / M5 (no local solid), ONE1 / KO1 (KiDS).

**Committed alone, before any FINAL15 script exists and before any FINAL15 number is computed.**

---

## Honesty flag on the pre-registration

I wrote this file **after** reading DD1's `RESULT.md`, HIS1's `RESULT.md`, HIS1R's `COMPARISON.md` and
FINAL-2's `RESULT.md`, all of which print the measured per-class residuals, and after reading the task brief,
which prints them again (SPARC 0.00 to +0.02 dex; KiDS within errors; groups +0.16; X-COP and CLASH +0.5 to
+0.6 at 15 to 24 se; ultra-faints +0.5 to +0.6; tidal dwarfs and DF2/DF4 0.6 to 0.9 low). **This is
therefore not a blind pre-registration.** The *signs* below follow from the channel physics and were not
reverse-engineered, but the *normalisation* of the two free-channel factors (F_b for the accreting and
baryon-losing channels) was chosen as a round order-of-magnitude figure before scoring, and I cannot exclude
that the printed numbers steered the choice. What **is** clean: the theory statement (§1-§4), the degeneracy
breaker (§5), the prediction table (§6) — frozen in `predictions_frozen.csv`, read by the script, never
edited after this commit — and the scoring arithmetic, which never sees the prediction file's contents
except to compare. The arithmetic is not circular; the hypotheses may be.

---

## 1. The conserved quantity

The clock sector carries one conserved current [C: QX17 (E3)],

    J^m = n^m rho_Q - lambda P^m / Q ,    nabla_m J^m = 0 ,

whose weak-field charge inside a comoving region V is exactly the non-baryonic mass there:

    N(V) = Integral_V ( D.P + n_d ) dV  =  M_C(V) .

Baryons carry a second, separately conserved charge M_b(V). **Both are non-negative.** That pair of facts is
the whole content of "conserved":

| statement | kind | lane |
|---|---|---|
| no polarization charge is manufactured inside a free-fall-bounded ball, at any time, for any momentum equation | exact | T4 |
| once the clock is static the polarization is frozen: M_C changes only by O(\|Phi\|/c^2) ~ 1e-6 | exact | LFS1 |
| => the halo's charge is an initial condition, not an advected quantity | exact consequence | CRUX, R541 |

**What is conserved is therefore not "the amount of dark matter in a galaxy".** M_C(V) changes whenever charge
or baryons cross dV. What the formation reading adds is that the *ratio* is what the event pins, and that
afterwards only transport moves it:

    X  =  M_C/M_b  =  X_f * (F_C / F_b) ,    F_C = M_C(today)/M_C,f ,  F_b = M_b(today)/M_b,f .

---

## 2. The epoch

The amount is pinned on **Sigma_f**: the first hypersurface, going into collapse, on which the clock's
expansion along its own normal theta_K vanishes — the fold. It is label-free (defined by a field, not by a
class), it exists at every mass on both footings, and it has been located:

- the fold sits at **0.52 R_ta** (FLD1);
- the clock settles behind a shock at **0.51 R_ta** (VSH1), at z = 4.96 / 3.45 / 1.46 for
  log M_b = 9 / 10.5 / 11.5 (canonical / alt 5.08 / 3.65 / 1.65).

Pinned there, and nowhere else:

    X_f  =  M_C,f / M_b,f  =  X_L( g_b,f ; a0 )  =  ( sqrt(1 + 4 a0/g_b,f) - 1 ) / 2 .

**The epoch's date does not enter.** a0 = kappa c sqrt(G rho_DE) with rho_DE constant (w = -1), so the same a0
pins the ratio at every redshift; and FRZ2 closed every framework a0(z) it tried (P0 Delta chi^2 9916 / 9009;
P0.5 252 / 167; P1 13338 / 23421; H 20943 / 34390; gate <= 4), leaving at most
`0.5 log10(3.2) ~ +0.25 dex` of a0-driven offset even at z_f = 12. **The observed class-to-class spread is
~1.4 dex — a factor 4-6 beyond anything a date can buy.** So the theory's causal claim is:

> **T-epoch: the event's NATURE sets the amount; the event's DATE is nearly irrelevant.**
> What matters is whether the material in the system ran a collapse of its own. Material that was already
> settled inside a parent and was then removed (tidal debris, DF2/DF4) never crosses Sigma_f as an
> independent system: it carries **no** charge, because the charge is not attached to the baryons
> (T4 + LFS1: it is written on the assembly surface and frozen, not advected).

---

## 3. The ledger (the master equation, derived once, then used everywhere)

Take a comoving region V whose present enclosed baryons are M_b and whose formation baryons were M_b,f.
With theta-free transport factors F_C, F_b as above and g_bar = G M_b/r^2 at fixed profile,

    g_b,f  =  g_bar / F_b ,                       (the field was higher if baryons have since been lost)
    X_f    =  X_L( g_bar / F_b ) ,
    X      =  X_L( g_bar / F_b ) * F_C / F_b ,
    d      =  log10[ ( 1 + X ) / ( 1 + X_L(g_bar) ) ]        (dex of g_obs at fixed g_bar)

and in the deep regime (g_bar << a0, X_L ~ sqrt(a0/g_bar)),

    **d  ~=  log10 F_C  -  (1/2) log10 F_b .**

| channel | what happened | F_C | F_b | sign of d | prediction |
|---|---|---|---|---|---|
| **C** settled, closed, complete | collapsed once, kept everything | 1 | 1 | 0 | **d = 0.00** (the anchor) |
| **R** recycled | material was settled in a parent, then removed; no collapse of its own | 0 | 1 | − | **d = −Y_law** (the floor, X = 0) |
| **A** still accreting | baryons arrived after Sigma_f | 1 | > 1 | − | d ≈ −½ log10 F_b |
| **B** baryon loser | baryons expelled/stripped after Sigma_f | 1 | < 1 | + | d ≈ −½ log10 F_b |
| **S** charge-stripped | charge removed, baryons kept | < 1 | 1 | − | d = log10 F_C |
| **D** dust branch (hot) | no static-clock state (CLS1); the sector is still background dust at the cosmic share | — | — | + | X = 5.41/F_b, **parameter-free** |

Two structural predictions that any reading of the ledger must respect:

- **the floor.** Neither charge can be negative ⇒ X ≥ 0 ⇒ **d ≥ −Y_law(g_bar)**. A system can be at the floor
  or above it; never below.
- **the ceiling.** If the only upward channel is baryon loss and the law's normalisation is unchanged, then with
  F_C = 1 the inferred X rises as F_b falls but the cold pull cannot exceed a0: **d ≤ d_max(u) = log10[(1+u)/(1+X_L(u))]**, u = a0/g_bar. (FRM1 graded this: X-COP and CLASH sit **above** it, +0.496 ± 0.022 and
  +0.553 ± 0.023 against ceilings +0.310 and +0.219. That violation is a datum about the hot branch: it is
  why the hot classes are on branch **D**, outside the ledger, not a licence to ignore the ceiling on branch C.)

**Note on the record's wording.** FINAL-2 §(ii) and CRUX write the transport line as `X_today = X_f * f_b`
with `f_b = M_b(present at t_f)/M_b(enclosed today) > 1` for baryon loss. That is the reciprocal of the F_b
used here; with the present definition the line is `X = X_f / F_b`. FINAL-2's own printed
`resid = +0.5 log10(f_b)` agrees with the `−½ log10 F_b` above (their f_b = 1/F_b), so the arithmetic in
the record is right and only the intermediate line is inverted. Restated here so the sign is unambiguous.

---

## 4. What the theory says, class by class — the channel assignment

Frozen here, from each class' documented astrophysics (hosted or not; gas-rich and still assembling, or quenched;
hot or cold). **Not** from its residual. The 16 classes are DD1's, on DD1's frozen table.

| class | branch | channel | why (record basis) |
|---|---|---|---|
| SPARC | settled | **C** | undisturbed discs; SHP1's sample; the anchor |
| faint rotators (McQuinn+22) | settled | **A** | gas-dominated (f_gas 0.6-0.9), still star-forming, curves still rising |
| tidal dwarfs (Lelli+15) | settled | **R** | made of gas torn out of a parent that had already settled |
| massive spirals (Di Teodoro+23) | settled | **C** | settled rotating discs, closed |
| ATLAS3D | settled | **G** | census is **stars only** (no cold, no hot gas) ⇒ d is an upper bound |
| RC100 | settled | **C** | settled discs at z 0.6-2.5 ⇒ the no-a0-evolution test |
| KiDS (B21) | settled | **G** | census is stars + cold gas, **hot gas omitted** ⇒ d is an upper bound |
| groups (Lovisari+15) | dust | **D**, F_b = 0.60 | open: ~40 % of baryons now outside R500 (GO1, RB1) |
| X-COP | dust | **D**, F_b = 1.00 | closed in the record's ledger: it kept the whole share |
| CLASH | dust | **D**, F_b = 1.00 | closed |
| MW bright dwarfs | settled | **B** | hosted, quenched, gas-free |
| MW ultra-faints | settled | **B** | hosted, quenched at reionization, gas-free |
| M31 dwarfs | settled | **B** | hosted, quenched at infall |
| LG field dwarfs | settled | **B** | quenched, gas-poor, but **stars-only census** ⇒ upper bound |
| Coma UDGs (Freundlich+22) | settled | **B** | hosted in the cluster, gas stripped |
| NGC 1052 UDGs (DF2/DF4) | settled | **R** | collision debris / stripped; a past loss no lane has located (HIS1 H2, G2) |

**Frozen normalisations for the two channels that need one** (order of magnitude, chosen now, applied
uniformly to every class in the channel — no per-class fitting at any point):

- Channel **A**: F_b = 2 (the system's enclosed baryons have doubled since Sigma_f). Sensitivity band
  F_b in [1.5, 3].
- Channel **B**: F_b = 0.25 (the system retains a quarter of the baryons present at Sigma_f; the rest was
  expelled or stripped). Sensitivity band F_b in [0.125, 0.5].

Everything else is parameter-free: **C** is exactly 0, **R** is exactly −Y_law, **D** is exactly
log10[(1 + 5.41/F_b)/(1 + X_L(g_bar))].

---

## 5. What breaks the degeneracy between the two readings

**The degeneracy.** Read the law as a force acting now: X = X_L(g_bar) for every system, always. Read it as
formation: X = X_L(g_bar/F_b) F_C/F_b. For a **settled, closed, complete** system — F_C = F_b = 1, g_b,f = g_bar —
the two are the *same function*. No observation of a healthy isolated disc, at any radius, any mass, any
redshift, can tell them apart. That is why SPARC passes under both, and why DD1's "no rule" result is compatible
with both: 149 SPARC galaxies sit at 0.00 dex and both readings say they should.

**The break.** They differ only where a system's history is not the identity, and there the formation reading
makes three predictions the force reading cannot make at all:

1. **Quantisation of the deficit, not just a deficit.** Recycled material sits at the **floor** — d = −Y_law,
   X = 0, i.e. Newton — not partway between Newton and the law. A force reading has no such value: every
   class is at 0.00 dex, so a class at −0.85 dex is ×10.9 off in g_obs, ≈7 se, and there is no
   "partial force" that produces it. A stripping story that removed only part of the charge would sit
   between; the prediction is that it does not.
2. **Bipolarity with two unrelated caps.** The force reading is a point prediction, so departures in either
   direction are equally fatal and equally meaningless. The formation reading predicts departures in **both**
   directions with **different** causes and **different** caps: deficits stop at the floor (F_C → 0), excesses
   stop at the baryon-loss ceiling d_max(u) (F_b → 0 with g_c ≤ a0). Observing classes at −0.7 to −0.85
   **and** classes at +0.5 to +0.6 in the same table — a 1.4 dex bipolar spread — is the formation
   reading's ordinary expectation and is forbidden by the force reading at >20 se.
3. **Class-level coherence with within-class incoherence.** The amount is a per-system constant written at
   Sigma_f, so classes separate; but the quantity that varies is an **integral over the history**, so no
   present-day proxy (today's host distance, today's gas fraction) should track it within a class. **That the
   within-class tests come back with no power (HIS1 H5) is the reading's signature, not a hole in it.**

**The one measurement that decides it, named now.** Two systems at matched present-day g_bar, one made of
recycled material and one that collapsed on its own: the force reading says identical; the formation reading
says the recycled one is at Newton. That pair is already in the frozen table (tidal dwarfs vs the faint
gas-rich rotators at similar g_bar) — and it is the cell the lane grades first (F1).

---

## 6. Pre-registered predictions: sign and rough size, per class

**Sign convention.** `+` = excess non-baryonic mass over the law's value at that g_bar; `−` = deficit.
Sizes in dex of g_obs at fixed g_bar. `pred` is the frozen point value; `[lo, hi]` the pre-registered "rough
size" band. Prediction computed **by hand here**, from DD1's published per-class median lg g_bar and the
channel rule of §3:

| class | ch | **pred can** | band can | **pred alt** | band alt | |
|---|---|---|---|---|---|---|
| SPARC | C | **0.000** | −0.10 … +0.10 | **0.000** | −0.10 … +0.10 | anchor |
| faint rotators | A | **−0.102** | −0.30 … 0.00 | **−0.106** | −0.30 … 0.00 | still assembling |
| tidal dwarfs | R | **−0.753** | −0.95 … −0.55 | **−0.790** | −0.99 … −0.59 | at the floor, X = 0 |
| massive spirals | C | **0.000** | −0.10 … +0.10 | **0.000** | −0.10 … +0.10 | settled, closed |
| ATLAS3D | G | **+0.050** | −0.15 … +0.10 | **+0.050** | −0.15 … +0.10 | stars-only census |
| RC100 | C | **0.000** | −0.10 … +0.10 | **0.000** | −0.10 … +0.10 | z 0.6-2.5: no a0 evolution |
| KiDS | G | **+0.100** | 0.00 … +0.20 | **+0.100** | 0.00 … +0.20 | hot gas omitted |
| groups | D | **+0.152** | +0.05 … +0.25 | **+0.114** | +0.02 … +0.21 | 5.41 / 0.60 |
| X-COP | D | **+0.380** | +0.18 … +0.58 | **+0.347** | +0.15 … +0.55 | 5.41, closed |
| CLASH | D | **+0.465** | +0.27 … +0.66 | **+0.435** | +0.24 … +0.63 | 5.41, closed |
| MW bright dwarfs | B | **+0.267** | +0.10 … +0.50 | **+0.270** | +0.10 … +0.50 | |
| MW ultra-faints | B | **+0.289** | +0.10 … +0.50 | **+0.290** | +0.10 … +0.50 | |
| M31 dwarfs | B | **+0.276** | +0.10 … +0.50 | **+0.279** | +0.10 … +0.50 | |
| LG field dwarfs | B | **+0.256** | +0.10 … +0.50 | **+0.259** | +0.10 … +0.50 | upper bound |
| Coma UDGs | B | **+0.265** | +0.10 … +0.50 | **+0.268** | +0.10 … +0.50 | |
| NGC 1052 UDGs | R | **−0.853** | −1.05 … −0.65 | **−0.892** | −1.09 … −0.69 | at the floor, X = 0 |

**The three headline predictions, made in advance, with size:**

- **P-1 (stripped sit LOW).** tidal dwarfs and NGC 1052 UDGs: **negative**, |d| ≈ 0.75 / 0.85 dex — i.e. at
  Newton, X ≈ 0, and ≈6-7 se below the law. Band ±0.15 dex.
- **P-2 (hosted sit HIGH).** MW bright dwarfs, MW ultra-faints, M31 dwarfs, Coma UDGs: **positive**,
  d ≈ +0.27 to +0.29 dex from a 4× baryon loss (band +0.10 … +0.50). Ordering prediction, frozen now:
  **ultra-faints > Coma UDGs > M31 dwarfs ≈ MW bright dwarfs**, because the excess is set by how much of the
  baryon reservoir was removed, and that scales with how deeply processed the system is.
- **P-3 (no within-class tracking).** Six Spearman pairs (gas fraction in SPARC and in the faint rotators; host
  distance in MW bright dwarfs, MW ultra-faints, M31 dwarfs; cluster-centric distance in Coma UDGs): **none
  significant after Holm, in either direction.** The formation reading *predicts* this — it is the only
  prediction here that is a null.

Plus, pre-registered secondary: **P-4 (the date does not matter).** RC100 (z 0.6-2.5) must sit within 0.10 dex
of SPARC (z ≈ 0), because a0 does not evolve; this is the discriminating test against every a0(z) reading.

---

## 7. Pre-registered graded items

Statistic, exactly DD1's: X = g_obs/g_bar − 1, Y = log10(1+X), resid = Y − Y_L(g_bar; a0), **median over each
system's main-table points, then median over systems in the class**; `se = max(1.2533·1.4826·MAD/√n_sys,
√(Σe_sys²)/n_sys)`. Pass line: |d| ≤ 0.10 dex **and** |d| ≤ 3 se (DD1's LINE_DEX / LINE_SIG). Both footings,
never pooled.

| item | required (frozen now) |
|---|---|
| **F1 FLOOR** | tidal dwarfs and NGC 1052 UDGs: both within their frozen band (±0.15 dex), both ≥ 5 se below the law, and both within 3 se of X = 0 |
| **F2 HOSTED HIGH** | the four hosted classes: ≥ 3 of 4 at d ≥ +0.05, **and** their joint median ≥ +0.15 dex, **and** the frozen ordering UFD > Coma UDG > M31 ≈ MW bright holds in sign |
| **F3 ANCHOR / NO a0 EVOLUTION** | SPARC passes (|d| ≤ 0.03 and ≤ 3 se) on **both** footings; RC100 within ±0.10 dex of SPARC's value |
| **F4 DUST BRANCH** | X-COP, CLASH, groups within 0.20 dex of the parameter-free X = 5.41/F_b prediction |
| **F5 FLOOR, GLOBAL** | 0 of 626 systems below X = 0 beyond 3 e; no class median below X = 0 |
| **F6 NO TRACKING** | the six Spearman pairs: none significant after Holm in either direction ⇒ outcome **NO POWER** |
| **F7 SIZE** | rms(pred − meas) over 16 classes ≤ 0.15 dex, and better than the plain-law control (pred 0 for all 16) by ≥ 0.10 dex |

**Decision rule, pre-registered now.** If F1-F7 all pass the label is **FORMATION LEDGER HOLDS**; if F1 and F2
pass but F7 fails, **HOLDS IN PATTERN, NOT IN SIZE**; if F1 or F2 fails, **FAILS**.

## 8. Controls and mutation arms (each must bite)

- **Control A — the force reading.** Predict d = 0.00 for all 16 classes. Must fail.
- **Control B — global constant.** Every class at the joint median of the 16 class medians. Must be worse than the
  frozen table on rms.
- **Control C — shuffled channels.** Permute the channel→class assignment (200 seeds). The frozen assignment must
  beat ≥ 95 % of them.
- **M1** — swap R and B (stripped predicted HIGH, hosted predicted LOW). Must change a label.
- **M2** — a0 × 2. Must break F3.
- **M3** — remove the floor (allow X < 0): the F1/F5 test must stop holding on a table in which five systems are
  placed below Newton. Must bite.
- **M4** — plant a within-class gas-fraction trend in SPARC of the strength the formation reading would need
  (|rho| ≈ 0.5, n = 149). F6 must then reject NO POWER ⇒ demonstrates F6 has power at the effect size the
  reading would need.
- **Lean**: `FINAL15.lean` must compile; `FINAL15_MUTATE.lean` (each structural statement negated) must fail with
  one error per false statement.

## 9. Files

- `PREREGISTER.md` (this file, frozen first, committed alone)
- `predictions_frozen.csv` (the 16-row prediction table, read by the script, never edited after)
- `final15_formation.py` → `final15.json` / `final15.out`, `final15_MUTATE.json` / `final15_MUTATE.out`
- `FINAL15.lean`, `FINAL15_MUTATE.lean`, `compile.txt`, `compile_MUTATE.txt`
- `RESULT.md`

---

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
