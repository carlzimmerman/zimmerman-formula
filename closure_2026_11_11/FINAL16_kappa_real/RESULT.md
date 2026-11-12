# FINAL-16 (KAPPA_REAL) RESULT -- 2026-11-11

**Label: `KAPPA NOT DERIVED (FITTED) -- FORM OUTPUT`.**
Q1 (form) = **OUTPUT**. Q2 (kappa = 1/2) = **NO**.

Criteria: `PREREGISTER.md` (committed alone, before any FINAL16 script existed), amended by
`AMENDMENT_A1.md` (item J7 added **before** the run that produced these numbers).
Script `final16_kappa_real.py`; output `final16.out` / `final16.json`; twin `FINAL16_MUTATE=1` ->
`final16_MUTATE.out` / `final16_MUTATE.json`; Lean `FINAL16.lean` (`compile.txt`).
Runtime ~1 s, stdlib + sympy only. TEST lane, quarantined: adopts nothing, relabels nothing,
registers nothing, edits nothing outside this folder. Footings never pooled
(canonical a0 = 9.3603e-11, alt a0 = 1.1312e-10 m/s^2). **kappa = 1/2 FITTED; not theory closed.**

---

## The deciding number

**0.319 dex.**

That is how far kappa moves when you change only *which named cosmological epoch* the assembly event
is matched to -- today (kappa = 0.7368), matter–Lambda equality (0.5000), or acceleration onset
(0.3536). The observational tolerance is **0.0411 dex** (the footing spread). The route therefore
carries **7.8x more freedom than the precision it would need** to be a derivation. It lands on 1/2
because equality is the epoch that was chosen.

Second, and independent: the number the record calls kappa = 1/2 **is not the measured value**.
Against Planck rho_Lambda, the external RAR acceleration a_0 = 1.20e-10 m/s^2 gives
**kappa_REAL = 0.6414 ± 0.0107 (random) ± 0.1283 (systematic)**. kappa = 1/2 is realized only on
the record's canonical footing a_0 = 9.3603e-11, which sits 0.108 dex (22 %) below that central
value -- i.e. kappa = 1/2 is the *definition of a footing convention*, not a datum.

---

## The items

| item | what it asks | verdict | the number |
|------|--------------|---------|-----------|
| **J0** | is kappa = 1/2 a measurement? | **PASS** (as negative) | kappa_ext = 0.6414 ± 0.011 ± 0.128; internal record estimates span 0.187 dex (0.417±0.095 → 0.641±0.128) |
| **J1** | is the formation reading scale-covariant? | **PASS = NO-GO CONFIRMED** (exact) | G_lam: (a0,g) -> (lam a0, lam g) is an exact symmetry; kappa is the only charged quantity |
| **J2** | does any route break the covariance? | **FAIL = NO ROUTE PASSES** | epoch menu spans 0.3189 dex vs 0.0411 dex allowance (1.6095 dex including z_bind = 10.83) |
| **J3** | does the GF1/GF2 n = 2 hook derive it? | **FAIL = RESTATEMENT** | germ ratio 4.000406 (rel 1.0e-4), Z^2 = 33.510322 (1.1e-8) -- pins n, not rho_* |
| **J4** | where does the formation event sit? | **PASS** (as negative) | g_b,f = 2.6015e-14 m/s^2, i.e. 3.86 dex below c sqrt(G rho_L) |
| **J7** | is CONSERVATION load-bearing for kappa? | **PASS = CONFIRMED silent** | conservation is G_lam-covariant: it fixes the amount's history, not the coefficient |

Known answers **KA-1 .. KA-4 all PASS** (Z = sqrt(32 pi/3) = 5.788810 to 0.00e+00 on both footings;
rho_ref(can)/rho_L = 1.001183; rho_ref(alt)/rho_crit,0 = 1.001182; the quadratic closes to 1.4e-16).

**Lean** (`FINAL16.lean`, `compile.txt`, exit 0, 51 s): four theorems, zero `sorry`, no new axioms --
`XL_quadratic` (KA-3, the formation law is the positive root of `g X (1+X) = a0`), `XL_covariant`
(J1 i, invariance under `(a0,g) -> (lam*a0, lam*g)`), `XL_quadratic_weight` (J1 ii, the quadratic
carries weight 1, so `kappa -> lam*kappa`), `ratio_invariant` (J1 iii, the law is a function of `a0/g`
alone -- which is precisely why no kappa can be extracted from it).

---

## 1. What the formation reading DOES output (Q1 = YES)

Conservation plus universality is stronger than FINAL6's K1 alone:

- **F3 (universality)** rules out every mass-bearing monomial: a_0 cannot depend on M.
- **F1 (conservation)** rules out every epoch-bearing density: if rho_* = rho_crit(z_f) or rho_m(z_f),
  then a_0(z_f) = kappa c sqrt(G rho_*(z_f)) is epoch-dependent, and two galaxies that assembled at
  different z_f would show different a_0 -- which is FINAL6's K5 refutation (spread > 0.5 dex).
- The only epoch-independent cosmic density is **rho_Lambda**. Hence
  **`a_0 = kappa * c * sqrt(G * rho_Lambda)` is an output of the reading, with kappa undetermined.**

That comes with a real, falsifiable prediction: **a_0(z) = a_0(0) exactly** (printed E(z) table in
`final16.out`, J5; FINAL2's own bound stands and is not graded here).

## 2. Why nothing outputs kappa (Q2 = NO) -- four independent reasons

**(a) J1 -- the no-go.** The formation law only ever sees the ratio a_0/g. Verified exactly in sympy:
`X_L(lam*y ; lam*a0) - X_L(y ; a0) = 0`. F2 is the *only* relation of F that is not invariant, and
that is because it *defines* kappa, so kappa -> lam*kappa. There is no G_lam-invariant left in the
formation data ({X, M_b, rho_*, c, G} are all fixed) that could fix the orbit coordinate.
**kappa is a flat direction of the formation physics.** The reading can say "kappa is the same number
for every galaxy and every epoch"; no equation in it can say which number.

**(b) J2 -- the epoch menu.** C1 (equality) is the only route inside the 5 % band, and it is a
*chosen* epoch, not a derived one. Moreover it is circular: kappa = 1/2 <=> beta = 1 <=> z_f = z_L,
while the record's canonical footing *defines* rho_ref := 4 a0^2/(c^2 G) ~ rho_L -- so "freeze-out
at equality" and "kappa = 1/2" are the same sentence. C5 (delta_c tie) gives kappa = 6066; the exact
turnaround condition C6 gives a_0 ∝ M_b^{1/3} (a 0.95 dex miss at M_b = 6e10 Msun), excluded by
universality -- confirming FINAL6's K5 by a different, sharper route.

**(c) J3 -- the n = 2 hook.** GF1/GF2's certified `kappa = a_0/s = 1/n` with the integer n = 2
measured a_0-free (germ ratio 4.000406, Z^2 = 32pi/3) is real, and it is the record's best
normalisation channel. But (i) it is algebraically a theorem given `s := n a_0`; (ii) it constrains the
**ratio a_0/s**, i.e. the response's index; (iii) the step that puts **rho_Lambda** under the square root
is F2 itself. So n = 2 transports the exponent/index; it does not select the cosmic density, and it is
not formation physics. **RESTATEMENT, not a formation output.**

**(d) J4 -- the event carries no cosmic magnitude.** From F1's exact quadratic,
g_b,f = a_0/[X(1+X)] = 2.6015e-14 m/s^2, i.e. **3.86 dex below** c sqrt(G rho_L) and 4.40 dex below
c H_0. The assembly event is fixed by the galaxy, not by cosmology; the gap is bridged by X ~ 59.49,
which is itself the law's output. Any route that must supply this gap from cosmology is circular.

## 3. The "REAL" in KAPPA_REAL -- the kappa budget

| entry | kappa | ±1σ | note |
|-------|-------|-----|------|
| adopted normalisation | 0.500 | – | an **input** (the record's footing tie) |
| CFG493 combined | 0.417 | 0.095 | 0.87σ from 1/2 |
| KAPPA_LEDGER fit | 0.551 | 0.043 | superseded (mixed H0 convention) |
| MNRAS v3.1 shape-only | 0.580 | 0.180 | 0.44σ from 1/2 |
| external: a_0 = 1.20e-10 vs Planck rho_L | **0.641** | 0.011 rand / 0.128 sys | 1.10σ_sys from 1/2 |

The record's own kappa estimates span **0.187 dex**. The 5 % band needed to call 1/2 a derivation is
0.021 dex. **kappa is not currently measured to one ninth of the precision the claim would require.**
kappa = 1/2 is admissible; it is not confirmed, and it is not derived.

---

## 4. MUTATE

Three false twins, each required to be rejected by the same machinery. **All three rejected**
(`final16_MUTATE.out`, 11 PASS / 2 FAIL, the 2 FAILs being J2 and J3 -- the honest negatives, which
must fail for the label to be honest):

- **M1** "kappa = 1/(2 pi) is derived by the formation reading" -- band miss 0.341 = 13.6x the band.
- **M2** "the z_f = z_L hit derives kappa = 1/2" -- rejected by the spread test (7.8x too free).
- **M3** "kappa = 1/2 is a measurement" -- rejected by J0 (adopted by footing convention; external
  central value 0.641).

MUTATE VERDICT: **PASS (the machinery discriminates).**

---

## 5. THE FLOOR

Stated as the strongest claim the printed numbers support.

> **FLOOR.** Under the formation reading -- the amount is set at the assembly event and conserved --
> the *form* of the normalisation is an output and the *coefficient* is not.
>
> What survives: **universality + conservation force a_0 to be epoch-independent, and rho_Lambda is the
> unique epoch-independent cosmic density, so `a_0 = kappa c sqrt(G rho_Lambda)` is derived, together
> with the falsifiable prediction `a_0(z) = a_0(0)` exactly.**
>
> What does not survive: **the value kappa = 1/2.** (i) The formation relations are exactly invariant
> under `(a_0, g_b) -> (lambda a_0, lambda g_b)`, and kappa is the only quantity that transforms
> under it, so kappa is a flat direction of F: no equation of the reading can evaluate it. (ii) The one
> route that appears to output 1/2 -- matching freeze-out to matter–Lambda equality -- picks the epoch;
> the same machinery gives 0.7368 for "today" and 0.3536 for "acceleration onset", 0.3189 dex of
> freedom against a 0.0411 dex allowance, and equality is circular because the canonical footing
> *defines* rho_ref ~ rho_L. (iii) The certified `kappa = 1/n` channel pins the *index* (n = 2, measured
> a_0-free to ~1 %), not the *density*. (iv) Conservation is load-bearing for the amount -- it is what
> makes X ~ 59 rather than ~6 -- and completely silent about the normalisation.
>
> And the empirical floor: **kappa = 1/2 is not a measurement.** Against Planck rho_L the observed a_0
> gives 0.641; the record's own kappa estimates span 0.187 dex, nine times coarser than the 5 % band that
> a derivation would have to hit. kappa = 1/2 is a fitted normalisation convention, realized on one
> footing by construction.

Nothing here overturns FINAL6 (same label, reached from a different side: a symmetry no-go plus an
epoch-freedom bound rather than an exhaustion scan) or NPJ1 (no sector is graded here).
The ledger's kappa = 1/2 stays **FITTED**. Row for the register: KAPPA_REAL, TEST, p_exact = 0 for
class audit; family VM audits excluded from trials.

---

## Files

- `PREREGISTER.md` -- criteria, committed alone before the script.
- `AMENDMENT_A1.md` -- item J7, added before the reported run.
- `final16_kappa_real.py` -- the run (`FINAL16_MUTATE=1` for the twin).
- `final16.out`, `final16.json`, `final16_MUTATE.out`, `final16_MUTATE.json`.
- `FINAL16.lean`, `compile.txt` -- the exact J1 / KA-3 statements.
- `RESULT.md` -- this file.
