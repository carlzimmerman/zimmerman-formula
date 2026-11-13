# CLOSE-3 (A): the share X_s, derived from the formation reading and graded

Audit lane. TEST, quarantined: adopts nothing, relabels nothing, registers nothing. Footings graded
separately and never pooled (canonical a0 = 9.360324825027975e-11, alt a0 = 1.1312035414413022e-10 m/s^2).
Cold dark energy is a gravitating field component, never a particle. kappa = 1/2 FITTED; not theory closed.

Companion script: `close3_share_check.py` (arithmetic only; it re-derives every number below from
inputs quoted from other lanes and prints the grade). Re-run: `python3 close3_share_check.py`.

---

## 0. Did FINAL-3 land? No.

`closure_2026_11_11/FINAL3_share_derivation/` contains **one file: `PREREGISTER.md`** (12120 bytes,
2026-11-11 23:14). There is no `RESULT.md`, no `final3.py`, no `final3.json`, no `final3.out`.
The lane's own §9 lists what it was going to write and none of it exists.

**What FINAL-3 was asked to derive** (its `PREREGISTER.md` §0-§2, verbatim in substance):

> Derive the share instead of imposing it: state what is conserved, integrate it over the formation
> history of a halo, obtain `X_s(z, M_b)` as an **output**, then grade the derived value against the
> three lanes that used the frozen number.

The frozen number is `X_s = 59.5 M_b`, carried as a fixed input by **PD1**
(`closure_2026_11_09/PD1_phantom_is_dust`, criteria 0dc7929421), **ONE1**
(`fable52_push/ONE1_counted_once`, criteria a967a38851) and **SRH1**
(`closure_2026_11_10/SRH1_settled_radius_history`, criteria 5ed8a37ec6). FINAL-3's §0 states the
reason it exists: "None of them DERIVES it." Three pre-registered derivations (D1 collapsed core,
D2 the fold, D3 the basin), four kill conditions K1-K4, five known answers KA-PD1 / KA-CHARGE /
KA-COSMIC / KA-RFOLD / KA-G4, three MUTATE arms MU1-MU3. **None of it was run.**

So the share was never derived by the lane that was chartered to derive it. The rest of this file
does the derivation, in closed form where it is closed, and grades it.

---

## 1. Which quantity is conserved, and what epoch pins it

**The conserved quantity: the cold-sector charge, separately from the baryon charge.**
FINAL-15 (`closure_2026_11_11/FINAL15_formation/RESULT.md` §1) states it as the record's own closure:

    J^m = n^m rho_Q - lambda P^m / Q ,   nabla_m J^m = 0 ,
    N(V) = Int_V (D.P + n_d) dV = M_C(V)

i.e. the weak-field charge in a comoving region is exactly the non-baryonic mass there. Baryons
carry a second, separately conserved charge `M_b(V)`. **Both are non-negative** — that is what
produces FINAL-15's floor `d >= -Y_law`. The two exact statements behind "conserved" are T4 (no
polarization charge is manufactured inside a free-fall-bounded ball) and LFS1 (once the clock is
static the polarization is frozen, `M_C` changes only by `O(Phi/c^2) ~ 1e-6`). Consequence, per
CRUX and R541: **the halo's charge is an initial condition, not an advected quantity.**

Complement, from FINAL-3's own §1 (which is frozen and which I adopt): unprocessed cold dust is
neither created nor destroyed; `rho_c(z) = rho_c0 (1+z)^3`; the cold-to-baryon ratio carried by any
comoving fluid element is the cosmic one, `R = omega_d / omega_b`.

**The epoch that pins it: the fold, Sigma_f.**
FINAL-15 §1(E): Sigma_f is the hypersurface where the clock's expansion along its own normal first
vanishes going into collapse. It is located: FLD1 puts it at 0.52 R_ta today (0.46 at z 1,
0.43-0.44 at z 2, 0.31-0.33 at z 4); VSH1's settling shock at 0.51 R_ta; z_f = 4.96 / 3.45 / 1.46
for log M_b = 9 / 10.5 / 11.5 (alt 5.08 / 3.65 / 1.65).

**And the critical clause — what the epoch pins is the RATIO, not the mass:**

    X_f = M_C,f / M_b,f = X_L(g_b,f; a0) = ( sqrt(1 + 4 a0/g_b,f) - 1 ) / 2

This is the single most important sentence for the share, and it is why the share is not free and
also not `R`:

- FINAL-15 §2: for a settled, closed, complete system (`F_C = F_b = 1`) the formation reading and
  the force reading are **the same function** — `X = X_L(g_bar)`, `d = 0`. So the epoch pins the
  *profile and amplitude*, `nu(x) = 1 + X_L(a0/x^2)`. It does **not** pin where the halo stops.
- The share `X_s = M_C/M_b` is a *total*. Totals come from the conservation statement, not from the
  epoch. The epoch supplies `nu(x)`; conservation supplies the truncation `x_t`.

So there are exactly two places the share can come from, and the record contains both:

| | closure | result | where it is already printed |
|---|---|---|---|
| **D1** | conservation: settled region = collapsed region | `X_s = R` exactly | FINAL-3 §1 (frozen) |
| **D2** | the epoch: the halo ends at the fold | `X_s = X_L(g_b(R_fold))` = FLD1's `X_fold` | FLD1 `RESULT.md` |

D1's algebra, in one line (FINAL-3 §1 consistency cap). Let `M_h = M_b(1 + X_s)` be the collapsed
mass; if the swept Lagrangian patch *is* the collapsed patch, its cold content at cosmic composition
is `[R/(1+R)] M_h`:

    X_s M_b = [R/(1+R)] M_b (1 + X_s)  ==>  X_s (1+R) = R (1 + X_s)  ==>  X_s = R .

**They disagree, and that disagreement is the open question.** D1 gives 5.41; D2 gives 17.6-31.6.
A factor 3.3-5.8. No lane in the record reconciles them, and FINAL-3 — the lane chartered to — did
not run.

---

## 2. The numbers

**D1.** `R = omega_d / omega_b`, from A0Z1's form-B background (`a0z1_forest_<footing>.out`, line 2):
canonical `0.1209 / 0.02236 = 5.4070`; alt `0.1209 / 0.02234 = 5.4118`. FINAL-3's pre-registered
KA-COSMIC value is `5.4092 / 5.4107`; my recomputation from A0Z1 differs by 0.04 % / 0.02 %. I use
FINAL-3's frozen numbers below and treat the agreement as a passed check.

    X_s(D1) = 5.4092 (canonical) / 5.4107 (alt)
    end radius x_t = sqrt(X_s (X_s + 1)) = 5.888 / 5.890 r_M        [r_M = sqrt(G M_b / a0)]

**D2.** FLD1 `RESULT.md`: "A halo ending at R_fold(0) is ONE1's truncated halo with share
`X_fold = [-1 + sqrt(1 + 4 x^2)]/2`, `x = R_fold/r_M`. At the four KiDS masses X_fold is 31.6, 21.0,
19.1 and 17.6 (canonical; alt 34.8 to 19.4)." Mass nodes log M_b = 9.4 / 10.45 / 10.7 / 10.9.
FLD1 flags this as **a mapped reading, not a graded run** — ONE1's machinery takes one share for all
lenses and was not rerun. Same status here.

**The frozen value.** `X_s = 59.4861 / 59.5029` (PD1, quoted in FINAL-4 and FINAL-6's
FROZEN_CRITERIA). End radius `x_t = 59.98 / 60.00 r_M`.

---

## 3. Grade against ONE1's KiDS host-free gate

Gate (ONE1 `RESULT.md`, criteria a967a38851, 1.6 R_h veto): `|z| <= 2` for all / late / early,
profile `chi^2 <= 9.49`, type difference `|z| <= 2`. `z = (data - model)/sigma`, sigma the jackknife
error of the difference with `k` refitted in each sample.

ONE1 **already computed the bracket at the derived D1 value** — its `X = 5.41` row *is* the cosmic
share (`one1_kids_brackets.out` lines 19-33; `AMENDMENT_A2.md` line 34):

| share | footing | z all / late / early | profile chi^2 | gate |
|---|---|---|---|---|
| **D1, X = 5.4092** | canonical | **+4.85 / -0.08 / +4.93** | 23.7 | **FAIL** |
| **D1, X = 5.4107** | alt | **+4.93 / -0.07 / +5.00** | 24.4 | **FAIL** |
| frozen, X = 59.4861 | canonical | -1.14 / -1.46 / -0.65 | 1.9 | PASS |
| frozen, X = 59.5029 | alt | -0.23 / -1.23 / +0.21 | 0.9 | PASS |

Model `R_s` at X = 5.41 is 0.155 / 0.143 against the measured 0.811 +- 0.134 / 0.809 +- 0.133.
**The derived share is under-filled by a factor 5.2 (canonical) / 5.7 (alt) in the outer window.**
Margin of failure: 2.85 sigma (canonical), 2.93 sigma (alt) on "all lenses"; 2.93 / 3.00 sigma on
early types. Late types are uninformative at every share (their error at 1.6 R_h is 0.42).

Against the parent's own quoted measurement (1.4002 +- 0.2211 canonical / 1.2740 +- 0.2012 alt) and
the model at X = 5.41 from the same bracket run:

    z = (1.4002 - 0.155)/0.2211 = +5.63 (canonical)      FAIL
    z = (1.2740 - 0.143)/0.2012 = +5.62 (alt)            FAIL

and against KO1's law-level line 0.891 (= 10^-0.05, `KO1_kids_outer_points/FROZEN_CRITERIA.md`
lines 108-113): the derived share's model `R_s` is 0.174 / 0.160 **of** that line, i.e. the halo
carries 17 % / 16 % of the amplitude the law-level clause asks for. The frozen share gives 1.126 /
0.951 of it.

*(The two measurements — 0.811 in ONE1's own table and 1.4002 in the parent's summary — are
different constructions of the same KiDS host-free statistic. I report both rather than pick one;
the derived share fails by 4.9 sigma against the first and 5.6 sigma against the second.)*

**D2 has no graded KiDS row.** FLD1 says only: "That is below the range ONE1's frozen statistic
accepts at 1.6 R_h (the census cap 53.64 through 59.5)." Mapped, not rerun.

---

## 4. Grade against SRH1's four gates G1-G4

SRH1's family is `R_set = f * R_fold(z, M_b)` with FLD1's `R_fold` and FZS1's junction; the law's
layout holds inside `R_set`, the cold reference's outside. Its result: **WINDOW EMPTY / WINDOW
EMPTY.** G1 (forest) `f <= 0.70`, edge 0.722 / 0.725. G4 (KiDS lensing) `f >= 1.25`, edge 1.004 /
1.050. Gap 1.39 / 1.45. G2 (RC100 at 2.2 R_e) `f >= 0.391 / 0.391`. G3(a) coverage `f >= 0.467 /
0.467`, with G3's rms line holding below that.

Map a share to `f` by FLD1's own `x = R_fold / r_M` row — `f = 1` is `X = X_fold` — so
`f(X) = sqrt(X(X+1)) / sqrt(X_fold(X_fold+1))`. Output of `close3_share_check.py`:

| log M_b | X_fold (f=1), can | **f(D1)** | G1 | G2 | G3(a) | G4 |
|---|---|---|---|---|---|---|
| 9.4 | 31.6 | 0.183 | PASS | FAIL | FAIL | FAIL |
| 10.45 | 21.0 | 0.274 | PASS | FAIL | FAIL | FAIL |
| 10.7 | 19.1 | 0.301 | PASS | FAIL | FAIL | FAIL |
| 10.9 | 17.6 | 0.325 | PASS | FAIL | FAIL | FAIL |
| 9.4 / 10.9 | 34.8 / 19.4 (alt) | 0.167 / 0.296 | PASS | FAIL | FAIL | FAIL |

**D2 is `f = 1.000` by construction**, at every mass and both footings:

| | G1 (<= 0.722 / 0.725) | G2 (>= 0.391) | G3(a) (>= 0.467) | G4 (>= 1.004 / 1.050) |
|---|---|---|---|---|
| **D2, f = 1** | **FAIL** (SRH1: Delta chi^2 38.7 at f=1, gate 4) | PASS | PASS | **FAIL** (SRH1: early-type z +2.003 can / +2.04 alt) |

**The finding.** Neither derived share lands in a passing window, and they fail at opposite ends:

- **D1 (conservation, `X_s = R`) sits at f ~ 0.17-0.33.** It passes the forest and fails everything
  else: G4 by 2.85-2.93 sigma, G2 by a factor 1.2-2.2 below its edge, G3(a) coverage by a factor
  1.4-2.8 below. FLD1 independently corroborates G2: at `f = 1` the fold covers RC100 with the worst
  galaxy at 0.39 of `R_fold`, so a settled region at 0.18-0.33 of `R_fold` cannot.
- **D2 (the epoch, halo ends at the fold) sits at f = 1 — inside SRH1's empty window**
  (0.722 < 1 < 1.004 canonical; 0.725 < 1 < 1.050 alt). It fails G1 by `Delta chi^2` 38.7 against a
  gate of 4, and it fails G4 by **0.003 sigma on canonical and 0.04 sigma on alt** — i.e. it is
  within rounding of the line, on the wrong side of it, on both footings.
- **The frozen 59.5 sits at f ~ 1.9-4.2** (FLD1: "Form B's own cap lies 1.1 to 4.2 times beyond
  R_fold(0) for log M_b 8 to 11.5"). It passes G4 and fails G1 by `Delta chi^2` 452 to 9916.

So the three contenders bracket SRH1's gap without filling it: frozen at f ~ 1.9-4.2 (too big),
D2 at f = 1 (in the gap), D1 at f ~ 0.2-0.3 (too small). **The derivation moves the share into the
middle of the empty window rather than out of it.** The gap 1.39 / 1.45 is unchanged by anything
here.

Caveat I did not resolve: the `f(D1)` mapping above is at `z = 0`. `X_s = R` is redshift-independent
(a ratio), so `R_set = 5.89 r_M` is fixed, while FLD1's `R_fold` shrinks with `z` (log M_b 10.45:
139 / 76 / 48 / 17.2 kpc at z 0 / 1 / 2 / 4). `f(z)` therefore *rises* with `z` and would cross G1's
edge at forest redshifts. I did not rerun the forest; this is a caveat on the G1 PASS, not a graded
number. FINAL-3's own KA-RFOLD (FLD1's `R_fold(z)`) is the piece that would settle it.

---

## 5. FINAL-3's two qualifiers

- **"KiDS is share-driven, not radius-driven" — FIRES.** The statistic tracks the amount
  monotonically and the radius follows from it (`x_t^2 = X(X+1)`), so the two cannot be separated by
  this test:

  | X | 5.41 | 10.82 | 53.64 | 59.49 |
  |---|---|---|---|---|
  | x_t / r_M | 5.89 | 11.31 | 54.14 | 59.98 |
  | z(all), canonical | +4.85 | +4.34 | -0.59 | -1.14 |

- **"The 59.5 is a baryon depletion of 1/11" — FIRES, exactly.**
  `5.4092 / 59.4861 = 0.09093` and `5.4107 / 59.5029 = 0.09093`; `1/11 = 0.09091`. Deviation
  0.03 %, against the 10 % the qualifier allows. **The frozen share is 11.0x the derived cosmic
  share.** For PD1's number to be right, a halo must hold 11 times its cosmic cold complement:
  either the baryons are depleted 11-fold against the cosmic ratio, or the halo drew cold charge
  from a Lagrangian volume 11 times its collapsed patch. No lane in the record derives either.

---

## 6. Label

By FINAL-3's own §4 rules, which are frozen and which I apply as written:

- **D1 (the primary, parameter-free closure): SHARE DERIVED AND REFUTED.** The derivation closes in
  closed form with no free parameter (`X_s = R`), so K1 (convergence) passes trivially — it is an
  identity, not an iteration. It **fails K2** (ONE1's KiDS host-free row, +4.85 / +4.93 sigma) and
  therefore fails K4's C2/C4 rows by inheritance, and it fails SRH1's G2, G3(a) and G4. In FINAL-3's
  vocabulary that is **SHARE NOT DERIVED** ("no closure passes K1-K4").
- **D2 (the fold): SHARE DERIVED AND REFUTED**, differently — it fails G1 by `Delta chi^2` 38.7 and
  G4 by 0.003 / 0.04 sigma.
- **D3 (the basin, PD1's rule iterated): NOT COMPUTED.** It needs the record's shell solver
  (PD1/WL1) and FLD1's shells; I did not run it. D3 one-shot is PD1's own convention and reproduces
  the frozen 59.4861 / 59.5029 by construction — it is the input rule, not a derivation.
- **Lane-level: NO VERDICT.** FINAL-3 §4 routes an unevaluated row, an unrun known answer or an
  unbitten MUTATE arm to NO VERDICT. KA-CHARGE, KA-RFOLD, KA-G4, MU1, MU2, MU3 and D3 were not
  executed here, so the lane's own "no closure passes K1-K4" clause cannot be asserted with the
  certainty the criteria demand.

**Therefore: FINAL-3 DID NOT LAND. Audit label NO VERDICT; D1 and D2 each DERIVED and each
REFUTED.** The share is not free and not 59.5 — it is pinned to the cosmic ratio `R` by charge
conservation (5.4092 / 5.4107), pinned to `X_L(g_b(R_fold))` = 17.6-31.6 by the fold epoch, and
**those two pinned values disagree by a factor 3.3-5.8 while both fail the data.** That
disagreement, not the number, is what is open.

---

## 7. What counts against this audit

- Nothing here is a new measurement. Every number is quoted from a lane in this repo; the script
  does arithmetic on them.
- `f(D1)` and `f(D2)` are **mapped** through FLD1's `X_fold` row, not reruns of SRH1's pipeline.
  FLD1 says the same of its own mapped ONE1 reading.
- The `z = 0` caveat on `f(D1)` (§4) is unresolved; the forest is at z 2.2-4.4.
- D3, KA-CHARGE, KA-RFOLD, KA-G4 and MU1-MU3 were not run. FINAL-3's MUTATE arms in particular are
  what would show the derivation bites; without them the refutation is a grade, not a controlled
  result.
- Spherical symmetry and monotone first infall, inherited from WL1's / FLD1's shells, as in every
  lane that reuses them.
- The joint — the equation that takes falling dust to a settled halo — stays missing, exactly as in
  SRH1 and GRW2. This is bookkeeping, not a mechanism.

## 8. Files

- `CLOSE3_A_SHARE_DERIVATION.md` (this file)
- `close3_share_check.py` -> stdout (the derivation, the grade, the qualifiers)
- `PREREGISTER.md` (FINAL-3's own frozen criteria; the only file the lane produced)
