# FINAL-17 (KAPPA_A) RESULT -- 2026-11-11

**Label: `KAPPA NOT DERIVED (FITTED) -- CAPACITY DERIVED`.**
Q1 (capacity) = **DERIVED**. Q2 (kappa = 1/2) = **NO**.

Criteria: `PREREGISTER.md` (written alone, before any FINAL17 script existed), amended by
`AMENDMENT_A1.md` (KA-1 restated, A3 prediction corrected, MUTATE semantics made explicit).
Script `final17_kappa_A.py`; output `final17.out` / `final17.json`; twin `FINAL17_MUTATE=1` ->
`final17_MUTATE.out` / `final17_MUTATE.json`; Lean `FINAL17.lean` (`compile.txt`, 13 theorems,
exit 0). Runtime ~2 s, stdlib + sympy only. TEST lane, quarantined: adopts nothing, relabels
nothing, registers nothing, edits nothing outside this folder. Footings never pooled
(canonical a0 = 9.3603e-11, alt a0 = 1.1312e-10 m/s^2). **kappa = 1/2 FITTED; not theory closed.**

---

## The deciding number

**0.798 dex.**

That is how far `kappa` moves when you change only *which cosmic acceleration you declare the
capacity to be* -- the horizon rate `c H_Lambda` (kappa = 2.8944), the uniform-sphere
self-gravity at the horizon `c H_Lambda/2` (1.4472), the cosmic column `pi G rho_L R_Lambda`
(1.0854), its half (0.5427), or the Milgrom form `c H_Lambda/(2 pi)` (0.4607). The
observational tolerance is **0.0411 dex** (half the footing separation). The route therefore
carries **19.4x more freedom than the precision it would need** to be a derivation, and none of
the six arms lands in the 5 % band.

Second, and independent: the capacity condition is **the equation `a0 = a0`**. The whole
self-source/capacity structure -- law, Poisson, hydrostatic closure, capacity bound, universal
column -- is exactly invariant under `(a0, g) -> (lam a0, lam g)` at fixed `c, G, rho_Lambda`,
and `kappa -> lam kappa` is the **only** charged quantity. There is no invariant left in the
route's data to fix the orbit coordinate.

---

## The items

| item | what it asks | verdict | the number |
|------|--------------|---------|-----------|
| **KA-1** | is Z a control or a definition? | **PASS** (restated, A1.1) | `kappa` from Z = `kappa` direct to 1e-12; Z(Planck) = 5.785390 vs sqrt(32pi/3) = 5.788810 |
| **KA-2** | do both footings realize 1/2? | **PASS** | 0.500296 (can vs rho_L) / 0.500295 (alt vs rho_crit,0) |
| **KA-3** | is the quadratic a different theory? | **PASS** | n=1 residual 0; n=2 residual `gbar*g_ph = a0 g^3/(g+a0)^2 > 0` |
| **KA-4** | the 214 / 107 pair | **PASS** | 213.7 / 106.9 Msun/pc^2 |
| **A1** | the capacity identity | **PASS = IDENTITY** | u = a0 g/(g+a0); shape `nu/(1+nu)` is a0-free |
| **A1b** | does the self-sourced branch sit at capacity? | **PASS** | g_c = a0 exactly; Sigma_c = a0/(pi G) |
| **A1c** | is the self-source fixed point degenerate? | **PASS** | Poisson closes for **every** amplitude C (residual 0) |
| **A2** | branch distinctness (AG4 G3) | **PASS = CONFIRMED** | capacity = a0/n; n=1 canonical, n=2 quadratic |
| **A3** | does any cosmic-scale premise derive 1/2? | **PASS = NO ARM PASSES** | 0 / 6 in band; span 0.7982 dex = 19.4x allowance |
| **A4** | the structural no-go | **PASS = NO-GO CONFIRMED** | all 8 covariance residuals exactly 0 |
| **A5** | the footing ledger | **PASS** | can 0.500296 +- 0.004816; alt 0.604611 +- 0.005821 |
| **M1/M2/M3** | three false twins | **all REJECTED** | see §4 |

MAIN: 14 checks, 0 failing, exit 0. MUTATE: 14 checks, 1 failing (A3), exit 1.

---

## 1. What the record's two claims actually were (audited, not assumed)

### (a) GF1 / GF2 -- the "kappa = 1/2 self-source closure"

Both found and read: `deepseek_push/GF1_germ_flip/`, `deepseek_push/GF2_closure_half/`
(dated **2026-10-08** in-repo; the brief's "2026-11-08" is a **date discrepancy, flagged not
adjudicated**).

- **GF2 derives `sigma^2 / v_flat^2 = 1/2`** -- exactly, in three lines from the committed
  static branch `Phi = C ln r` + Poisson + stationarity/barotropy, with a premise ledger
  counting entries carrying the number 1/2: **0**. Plus a uniqueness lemma (gamma = 2 is the
  unique self-sourced hydrostatic equilibrium).
- **What that is:** a **ratio internal to the halo**. It is `M_b`-free and it contains **no
  `rho_Lambda` anywhere**. GF2's own border (iii) says so: *"the vacuum coupling (why a_0's
  VALUE is the vacuum's scale) -- OUT of scope here."*
- **GF1 reduces** every spelling of the tie to one integer `n` via `a0 = c sqrt(G rho_L)/n`,
  `Z = n sqrt(8 pi/3)`, `kappa := a0/s` with `s := n a0`. Given `s := n a0`, `kappa = 1/n` is a
  **theorem of the definition**. The content is the measurement of `n` -- and the step that puts
  `rho_Lambda` under the root is the tie itself.
- **This lane's independent confirmation of the gap:** (A1 ii/vi) `u/a0 = nu/(1+nu)` is
  `G_lam`-invariant and a0-free; (FINAL-16 KA-2, cited) `sigma^2/v_f^2 = 1/2` holds for
  kappa = 1/3 as well as 1/2, i.e. **the 1/2 does not move with kappa**.
- **Verdict: the record derives the INDEX/SHAPE. It does not derive `a0/(c sqrt(G rho_L))`.**
  Same verdict as FINAL-16's J3 (`FAIL = RESTATEMENT`), reached here through the capacity
  channel.

### (b) Sigma107v214 / AG4 branch a -- the "n = 2 half-capacity variant, certified distinct"

- **No file or lane named `Sigma107v214` exists in the repo** (searched filenames and content,
  case-insensitively, for `Sigma107`, `SIGMA107`, `Sigma 107`, `v214`). The identifier resolves
  to **AG4's capacity pair** in `argon_push/AG4_law_from_action/FROZEN_CRITERIA.md` G3:
  `n = 1` (canonical) ⇒ `g_ph < a0`, `Sigma_bar_max = a0/(pi G) ~ 214 Msun/pc^2` (PAPER49's
  anchor); `n = 2` (quadratic) ⇒ `g_ph < a0/2`, "**~ 107 in the same convention**".
  AG4 landed **BRANCH (a) CONFIRMED**: the unique static rest state of the frozen S2 action IS
  the canonical law; the quadratic is a different theory.
- **This lane re-verified it independently** (sympy, and Lean T11/T12/T13): the canonical law's
  own `g_ph` solves `u^2 + gbar u = a0 gbar` with residual **0**, and leaves
  `u^2 + 2 gbar u - a0 gbar = a0 g^3/(g+a0)^2 > 0` in the n = 2 member. Capacity = `a0/n`.
- **A trap the record does not flag, and this lane does:** the record's deep **universal column**
  `Sigma_c = a0/(2 pi G)` prints at **106.9 Msun/pc^2** -- numerically the **n = 2** capacity
  ceiling, *not* the canonical one (213.7). The number 107 therefore appears in two different
  roles. Using `Sigma_c ~ 107` to argue for `kappa = 1/2` in the **canonical** branch is a
  branch mix. Flagged, not used (twin M2).

---

## 2. What the capacity route DOES derive (Q1 = YES)

From the canonical law `g_N = g^2/(g+a0)`, with `u := g - g_N`:

1. **`u = a0 g/(g+a0)`** and **`a0 - u = a0^2/(g+a0) > 0`**, so `0 < u < a0` for all `g > 0`:
   the cold component's own self-gravity **saturates at `a0`, and at nothing else**.
   (Lean `phantom_capacity`, `phantom_deficiency`.)
2. **The saturated self-sourced branch sits exactly at the capacity.** With
   `rho_c = a0/(2 pi G r)` the enclosed mass is `M_c(r) = (a0/G) r^2`, and then
   `dM_c/dr = 4 pi r^2 rho_c` (Poisson, Lean `saturated_poisson`),
   `G M_c/r^2 = a0` for **every** r (Lean `saturated_field`), and
   `M_c/(pi r^2) = a0/(pi G) = 213.7 Msun/pc^2` (Lean `saturated_column`).
   The three are one statement, and they are `a0`-free in shape.
3. **The branch split is certified**: capacity `a0` (canonical, n=1) vs `a0/2` (quadratic,
   n=2); columns 214 vs 107.

None of this touches cosmology, and none of it evaluates `a0`.

---

## 3. Why nothing in the route outputs kappa (Q2 = NO) -- four independent reasons

**(a) The capacity condition is one equation `a0 = a0`.** `sup_g u = a0` where `a0` is the
scale in the law. It says the ceiling is the scale; it does not say which scale.

**(b) The self-source fixed point is degenerate.** For `g_c = C/r`, Poisson is satisfied by
`rho_c = C/(4 pi G r^2)` for **every** `C > 0` (sympy residual 0; A1c). Self-sourcing is a
fixed point, not a normalisation.

**(c) The whole structure is `G_lam`-covariant, and kappa is the only charge** (A4, all 8
residuals exactly 0; Lean `phantom_covariant`, `phantom_shape_invariant`,
`capacity_bound_covariant`). The law, `u`, the bound `u < a0`, the deficiency, the hydrostatic
closure `sigma^2 = C/2`, the ratio `sigma^2/v_flat^2 = 1/2`, the Poisson branch (weight 1/2 on
both sides, `C := sqrt(G M_b a0)`) and the universal column all carry the *same* weight as
`a0` -- so none of them can evaluate `a0`, and no `G_lam`-invariant remains to fix the orbit.

**(d) Every cosmic reading of the capacity is a menu choice** (A3). Six frozen premises built
from `c, G, rho_Lambda` alone give `kappa` = 2.8944 / 1.4472 / 1.0854 / 0.5427 / 0.4607 /
0.4607 -- a **0.7982 dex** spread against the 0.0411 dex the route would need. The nearest arm
(C3/C6, `a0 = c H_Lambda/(2 pi)`) gives

> **kappa = 0.460659 +- 0.004435 (cosmology only)**, i.e. `a0 = 8.619e-11 m/s^2`,
> which is **0.0393** from 1/2 = **1.57x the 5 % band**, and **0.0356 dex** from the canonical
> footing -- inside the 0.0411 dex footing half-allowance, so it cannot even discriminate the
> footings, let alone prove the coefficient.

**Error propagation** (all inputs stated; `G` cancels **exactly** in
`kappa = a0 sqrt(8 pi/(3 Omega_L))/(c H0)`, verified symbolically):
`d ln kappa/d ln a0 = +1`, `d ln kappa/d ln H0 = -1`, `d ln kappa/d ln Omega_L = -1/2`;
`sigma/kappa = sqrt((0.54/67.36)^2 + (0.0073/(2*0.6847))^2) = 0.963 %`.
`sigma(H0) = 0.54` and `sigma(Omega_L) = 0.0073` are Planck 2018 values **from memory --
flagged**. The central `H0`, `Omega_L`, `rho_Lambda` are from the record
(FINAL-16 PREREGISTER §2). Source-lane systematic: swapping to the GF1/F05 register cosmology
(`rho_c = 8.5332e-27`, `Omega_L = 0.685`) moves `kappa(can)` from 0.500296 to 0.499878,
i.e. **0.00036 dex** -- negligible.

---

## 4. The footing question (part 3 of the brief)

| entry | kappa | +-1sigma | vs 1/2 |
|-------|-------|----------|--------|
| canonical 9.3603e-11 against `rho_Lambda` | **0.500296** | 0.004816 | 0.059 % (footing round-off) |
| canonical 9.3603e-11 against `rho_crit,0` | 0.413978 | – | – |
| alt 1.1312e-10 against `rho_Lambda` | **0.604611** | 0.005821 | **0.0822 dex away** |
| alt 1.1312e-10 against `rho_crit,0` | 0.500295 | – | 0.059 % |
| external RAR 1.20e-10 (PROVISIONAL) | 0.641384 | 0.0107 rand / 0.1283 sys | 0.108 dex |

**The route selects NEITHER footing.** Pre-registered rule (PREREGISTER §3 A5): a footing is
selected only if some A3 arm both lands inside `|kappa - 1/2| <= 0.025` **and** has its premise
*derived from the route*. No arm clears either test -- the nearest is 1.57x outside the band and
is menu item C3, a choice. The 0.0356 dex near-miss to canonical is reported as information, not
promoted to a selection.

**What the tie itself does, if you grant it:** `a0 = (1/2) c sqrt(G rho_Lambda)` is realized
**only** by the canonical footing (0.500296). The alt footing reaches `kappa = 1/2` only by
swapping the reference density to `rho_crit,0` (0.500295) -- i.e. each footing defines its own
reference density so that 1/2 holds. That is a **definition, not a selection**: the tie cannot
choose between `rho_Lambda` and `rho_crit,0`, and the capacity route supplies nothing that
could. Against `rho_Lambda` the alt footing is excluded at 0.0822 dex (20.9 %).

---

## 5. MUTATE

Three false twins. MAIN rejects all three; MUTATE (band widened to 20 %, premise test off)
accepts all three, and the mutation arm's own gate **A3 FAILS** (band hits C3, C5, C6), flipping
the lane label to the false `KAPPA DERIVED (CAPACITY)`. `MAIN exit=0`, `MUTATE exit=1`.

- **M1** "the Milgrom-form capacity derives kappa = 1/2" -- rejected on the band
  (0.0393 = 1.57x) and on the premise test (menu item C3).
- **M2** "Sigma_c = a0/(2 pi G) ~ 107 confirms kappa = 1/2 via the half-capacity" -- rejected:
  107 is the **n = 2** capacity ceiling; the canonical ceiling is 213.7. The equality is an
  identity of the column convention and carries no cosmology.
- **M3** "kappa = 1/2 is a measurement, realized on the alt footing too" -- rejected:
  kappa(alt vs rho_L) = 0.604611, 0.0822 dex from canonical; 1/2 on the alt footing requires
  swapping the reference density.

---

## 6. THE FLOOR

Stated as the strongest claim the printed numbers support.

> **FLOOR.** The self-source / capacity route derives the **capacity** and the **shape** of the
> cold component's response, and it derives **nothing** about the normalisation.
>
> What survives: **the cold component's own field saturates at `a0` and at nothing else
> (`0 < u < a0`, `a0 - u = a0^2/(g+a0)`); the self-sourced configuration sits exactly at that
> capacity (`rho_c = a0/(2 pi G r)` <=> `g_c = a0` <=> `Sigma_c = a0/(pi G) = 213.7 Msun/pc^2`);
> the response shape `u/a0 = nu/(1+nu)` is `a0`-free; and the two branches are certified
> distinct (canonical capacity `a0`, column 214; quadratic capacity `a0/2`, column 107).**
> All of that is exact (sympy residuals 0, Lean 13/13) and none of it uses cosmology.
>
> What does not survive: **the value `kappa = 1/2`.** (i) The capacity condition is the equation
> `a0 = a0`. (ii) The self-source fixed point holds for every amplitude `C`, so self-sourcing
> fixes no scale. (iii) The entire route is invariant under `(a0, g) -> (lam a0, lam g)` at
> fixed `c, G, rho_Lambda`, and `kappa` is its only charged quantity -- there is no invariant
> left to fix it. (iv) Every attempt to nail the capacity to a cosmic scale is a menu choice,
> and the frozen menu spans 0.7982 dex against a 0.0411 dex allowance.
>
> **The record's `kappa = 1/2` is neither derived nor measured by this route.** The nearest
> honest arm gives `kappa = 0.460659 +- 0.004435` (1.57x outside the 5 % band, inside the
> footing half-allowance). The record's own value 0.500296 is the **definition of the canonical
> footing**: `kappa` and `Z = c H_Lambda/a0` are the same number, and
> `Z = sqrt(32 pi/3)` holds iff `kappa = 1/2` exactly.
>
> **Cross-lane note for the parent:** FINAL-16's KA-1 (`Z = sqrt(32pi/3)` to 0.00e+00) is
> circular -- it builds `H_Lambda` from `rho_ref := 4 a0^2/(c^2 G)`, a footing-defined density.
> Any control of that shape verifies the footing's definition, not the tie.

Row for the register: **KAPPA_A, FINAL-17, TEST, capacity route; Q1 DERIVED, Q2 NOT DERIVED;
family-VM class audit, p_exact = 0 (excluded from determinate trials).** Nothing here
overturns FINAL-16 (same label from a third channel), GF1/GF2 (their 1/2 is the shape/index,
certified as such) or AG4 (branch (a) re-verified, not re-adjudicated). The ledger's
`kappa = 1/2` stays **FITTED**.

---

## Files

- `PREREGISTER.md` -- criteria, written alone before the script.
- `AMENDMENT_A1.md` -- KA-1 restated, A3 prediction corrected, MUTATE semantics; declared in full.
- `final17_kappa_A.py` -- the run (`FINAL17_MUTATE=1` for the twin).
- `final17.out`, `final17.json`, `final17_MUTATE.out`, `final17_MUTATE.json`.
- `FINAL17.lean`, `compile.txt` -- 13 theorems, exit 0, `error|sorryAx` count 0,
  axioms ⊆ {propext, Classical.choice, Quot.sound} for every headline theorem.
- `RESULT.md` -- this file.
