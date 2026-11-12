# OUT-3 (COSMIC-SHARE FOLD) — PRE-REGISTERED CRITERIA

2026-11-12. Lane: **derive the footing AMOUNT**. Owner's brief: *is 5.41 fitted free (R541) or pinned
by something outside form B? Then attempt one construction — require that the settle-down at the fold
front happen exactly when the enclosed cold charge equals the cosmic share of the enclosed baryons, and
solve for what that forces on a_0.*

**Standing.** kappa = 1/2 FITTED; not theory closed. Footings graded separately, NEVER pooled
(canonical a0 = 9.3603e-11, alt 1.1312e-10 m/s^2). Cold dark energy is a gravitating field component,
never a particle. This lane adopts nothing, relabels nothing, registers nothing.

**Id checked free:** no `hy4_preview_push/OUT3_cosmic_share_fold*` path exists; the two neighbouring
OUT-3 lanes are `OUT3_scale_free_boundary` and `OUT-3_kappa_equality_fixed`, which are different
constructions (see §6).

---

## 0. ORDER DISCLOSURE (adverse; read this before the gates)

This pre-registration was written **after** reading `closure_2026_11_11/FINAL18_kappa_fold/RESULT.md`,
`closure_2026_11_10/R541_why_the_cold_share/NOTE.md`, `closure_2026_11_10/AMT1_amount_budget/AMOUNT_BUDGET.md`
and the two neighbouring OUT-3 lanes. **I therefore already know the number this construction is
expected to return:** FINAL18 graded the algebraically identical substitution as its mutation arm MU2
and reported `kappa_M = 0.0375` (REJECTED, 18.5x the 5% band), and FINAL18's table gives the four
`R_fold` values this lane needs.

Consequences, accepted now:

- **This lane is a REPLICATION with an added error bar, not a blind test.** Its only new content is
  (a) a propagated uncertainty on `kappa_S` from every input, and (b) the conservation gate G5, which
  FINAL18 folded into a prose rejection rather than grading. Nothing below was chosen after seeing a
  number *this lane* computed, but every number below was chosen knowing FINAL18's.
- Because the expectation is known, the gates are written so that a PASS cannot be manufactured:
  G1's band (5%) is FINAL16/FINAL18's frozen band, G2's allowance (0.0411 dex) is the frozen footing
  spread, and G5's threshold is a strict inequality on FLD1's own delivered share.
- **The pre-registered expectation is FAIL on G1, G2, G3.** A PASS on any of them would contradict a
  committed lane and must be treated as a bug in this lane's code until proven otherwise.

---

## 1. The construction under test, stated now

**(S) the cosmic-share settle-down condition.** The law's static halo is first established at the fold
front (FLD1 measured that surface: `R_fold(z, M_b)`, 0.52 R_ta today, growing roughly as `M_b^{1/3}`).
Require that where it is born, the halo it becomes encloses exactly the **cosmic share of the enclosed
baryons**:

>   M_c(< R_fold(t))  =  R_cosmic * M_b                                        (S)
>
>   R_cosmic := Omega_d / Omega_b  =  5.410 (canonical) / 5.412 (alt)   [F1A, `closure_2026_11_07/
>   F1A_primary_cmb_audit/RESULT.md:22`]

with the record's own exact halo (EQUATIONS.md sec. 6; the graded footing facts):

>   M_c(<r) = M_b X(x),   X(x) = (sqrt(1 + 4x^2) - 1)/2,   x = r/r_M,   r_M = sqrt(G M_b / a_0).

**(S) is one equation in one unknown (a_0), because `R_fold` is FLD1's measured front.** Closed form,
derived now and used with **no** deep-regime approximation: `X(1+X) = x^2` with `X = R` gives
`x^2 = R(1+R)`, so exactly

>   a_0^S  =  G M_b R_cosmic (1 + R_cosmic) / R_fold^2 ,
>   kappa_S = a_0^S / (c sqrt(G rho_Lambda)) ,   rho_Lambda = Omega_L rho_crit,0.

**Equivalence of the two readings of the brief, recorded so the ambiguity cannot be exploited later.**
"the enclosed cold charge" may be read as (i) the halo's `M_ph(R_fold)` (the left side of FINAL18's
matching) or (ii) the charge the clock delivered across the front (its right side). Both give
`X_fold = R_cosmic`, hence the same `a_0^S`. The lane computes one number. Reading (ii) additionally
has to satisfy G5; reading (i) does not, and is the weaker claim. **Both are graded.**

**Where `R_cosmic` sits in the record (the first half of the brief).** R541 §1-2: `R_cosmic` is the CMB
acoustic-peak fit (F1A), and in the adopted action (A) the cosmic cold amount is an **integration
constant** `C0` — "No equation of the action sets it." R541 §8: five lanes, four EXCLUDED, one TRADES.
AMT1 §4: KiDS rejects `X = 5.41` for the halo at **+4.85 / +4.93 sigma**. R541 §6: X-COP clusters give
an independent *measurement* `M_dark/M_bar = 5.73 +- 0.68`, reported, never pooled. Nothing outside
form B pins it.

## 2. Conventions

SI in printed kappa; internal work in kpc, km/s, Msun (G = 4.30091e-6, TU = 0.977792 Gyr) as in
COL1/FLD1. `rho_Lambda = Omega_L * 3 H0^2/(8 pi G)` on the footing's own background (Planck 2018
TT,TE,EE+lowE+lensing: H0 = 67.36, Om = 0.3153, OL = 0.6847). Fold inputs read from FLD1's committed
runs (`fable52_push/FLD1_fold_reach/runs/*.json`, origin bce6d61451), N = 2400, z_i = 10, law on,
`hubble_*` mode. No refit of a_0, no new sector, no new data, no download.

## 3. Pre-registered gates (the label is decided by G1-G5)

| gate | statement | PASS condition |
|---|---|---|
| **G0** (exact inversion) | `X = R` in `X(1+X) = x^2`, `X,x >= 0` ⟺ `x^2 = R(1+R)`. sympy `simplify` to 0. | exact; PASS is required for the lane to be admissible at all |
| **G1** (the number) | `kappa_S` at z = 0, log M_b = 10.45, both footings. | `abs(kappa_S - 1/2) <= 0.025` on **both** footings (the frozen 5% band) |
| **G2** (universality in mass) | `kappa_S` on the frozen grid log M_b = 6.5, 7, 8, 9, 9.4, 10, 10.45, 10.7, 10.9, 11.2, 11.5, 12, both footings. | dex span `<= 0.0411` (the frozen footing spread) |
| **G3** (universality in epoch) | `kappa_S(z)` at z = 0, 1, 2, 4 from the fold series, log M_b 10.45. | drift `<= 0.0411 dex` (a static halo is continuously born at the moving front, so one a_0 must serve every epoch) |
| **G4** (the error bar) | Propagate every input uncertainty to `kappa_S` (§4). | reported regardless of outcome; **the bar is a report, not a gate that can rescue G1-G3** |
| **G5** (the conservation blocker) | Compare `R_cosmic` against FLD1's delivered shares at the same front: `q_front`, `q_crossed`, `q_turned` (`charge_turned_around_over_Mb`). FINAL3's (H): *settling rearranges cold charge, it does not create it*. | `q >= R_cosmic` for the reading to be physically available. **Pre-registered expectation: FAIL** (FLD1 delivers 0.66-1.06 M_b against a demand of 5.41) |

**G4's rule, pre-registered so it cannot be argued later:** an error bar is uncertainty about one
number. G2 and G3 are spreads of *different* numbers across mass and epoch. **No error bar can absorb
a G2 or G3 failure.** If G2 or G3 fails, the lane reports a falsification, not a value with a wide bar.

## 4. The error budget (frozen before the run)

`a_0^S ∝ M_b R(1+R) R_fold^{-2}`, `kappa_S ∝ a_0^S / sqrt(rho_Lambda)`.

| input | uncertainty | exponent into kappa_S | shift in kappa_S |
|---|---|---|---|
| `R_cosmic = 5.410` | +- 0.065 (Planck 2018 fallback width, R541 part E) | `d ln a_0/d ln R = (1+2R)/(1+R) = 2.00` | +- 2.4 % = +- 0.0103 dex |
| `R_fold` | FLD1 at-rest vs Hubble-flow reading, +22.3 % (OUT3 arm A) | `-2` | -0.175 / +0.175 dex |
| `R_fold` | FLD1 start redshift 20/30, +1.4 % | `-2` | 0.012 dex |
| `R_fold` | FLD1 shell N 1200 -> 4800, +0.07 % | `-2` | 0.0006 dex |
| `rho_Lambda` | +- 1.5 % (Planck) | `-1/2` | 0.0032 dex |
| `M_b` (KiDS/SPARC mass scale) | not an error on one galaxy; carried as the G2 grid | +1 | — |

Total, added in quadrature on the log: **pre-registered expectation +- 0.10 dex** (matching OUT3 arm
A's independently derived bar), dominated by the at-rest/Hubble-flow convention on `R_fold`.

## 5. MUTATE — three false twins the same machinery must reject

- **MU1 — "the cosmic-share settle-down derives kappa = 1/2."** Must be rejected by G1: expected
  `kappa_S ~ 0.0375`, band miss ~ 0.46 against a 0.025 band.
- **MU2 — "the miss is inside the error bar."** Must be rejected by the §3 G4 rule: the bar is
  +- 0.10 dex, the miss is ~ 1.1 dex, and G2's 1.83 dex of mass drift is a spread of different
  numbers, not an uncertainty on one.
- **MU3 — "5.41 is only a convention; use the X-COP value 5.73 +- 0.68 and it lands."** Must be
  rejected by G1 arithmetically (`kappa_S ∝ R(1+R)`, so 5.73 buys 12 % — the miss is 13x) and by
  record hygiene: X-COP is reported, never pooled (R541 §6).

## 6. What this lane is not

- Not `OUT3_scale_free_boundary` (that lane matched formation normalisations N_f to vacuum values N_v
  in three unit slots and recorded (F3,V3) share-vs-cosmic-share as INADMISSIBLE unit-mismatched; it
  never imposed a *radius* condition at the fold).
- Not `OUT-3_kappa_equality_fixed` (that lane's settle-down radius is `rho_c(r_sd) = rho_Lambda`, a
  **cosmic-vacuum** boundary, and its ratio is `M_c/M_Lambda`; it found K in [3/2, 3], so 1/2 is not
  in range. This lane's boundary is the **baryon** share at FLD1's fold, a different condition).
- Not a reopening of FINAL18. FINAL18 asked `M_ph(R_fold) = Q_fold` with `Q_fold` measured; this lane
  fixes the share to the cosmic value and asks what a_0 must be. The algebra coincides with FINAL18's
  MU2 arm **by construction**, which is why this lane is declared a replication in §0.
- No refit, no new sector, no new data, no download, no CLASS run. Literature attributions PROVISIONAL.

## 7. Labels

- **AMOUNT DERIVED (COSMIC-SHARE FOLD).** G1, G2, G3, G5 PASS on both footings.
- **AMOUNT NOT DERIVED (FALSIFIED).** G1 and/or G2 and/or G3 FAIL, with the number and its bar printed.
  *Pre-registered expectation.*
- **AMOUNT NOT DERIVED (UNAVAILABLE).** G5 FAIL such that the required share is not physically
  deliverable at the front, so (S) is not merely wrong but cannot be posed.
- **OPEN** if G0 fails or a numerical step fails.

**Standing, whatever the outcome: kappa = 1/2 stays FITTED unless a route outputs it, and 5.41 stays a
fitted initial condition unless a route outputs it.**

## 8. Files to be produced

`PREREGISTER.md` (this file), `out3csf.py`, `out3csf.out`, `out3csf.json`, `RESULT.md`.
