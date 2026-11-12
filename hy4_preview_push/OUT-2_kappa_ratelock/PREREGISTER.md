# OUT-2 (KAPPA_RATELOCK) -- PRE-REGISTRATION, committed alone before any number

Date: 2026-11-12. Lane id `OUT-2`, label `CAPACITY FIX`.
Test lane. **Adopts nothing, relabels nothing, is not registered.**
`kappa = 1/2 FITTED; not theory closed` stands until a lane outputs a number that survives.
Footings graded separately, never pooled.

This file is written and committed **before** `out2.py`, `out2.out`, `OUT2RateLock.lean` or any
number exists. Nothing below was chosen after seeing a result.

---

## 0. The obstruction this lane must beat

`FRAMEWORK.md` §2 (commit `a12e36e397`): the formation physics depends only on `a0/g`, so

    G_lam : (a0, g) -> (lam*a0, lam*g)

is an **exact symmetry** and `kappa` is the only quantity charged under it. `kappa` is a flat
direction. FINAL-16 (form only), FINAL-17, FINAL-18 (fold matching, 1.2-2.2 dex miss), FINAL-19
(deep-field column, forces `kappa = sqrt(2 pi) = 2.5066`, 22 sigma) all failed to output it.

Consequence, taken as the design constraint: **no force term, no stress matching and no saturation
condition can fix `kappa`.** The only thing left to fix is the *normalisation of the clock rate
`Q`*, because `G_lam` acts on the potential, i.e. on `Q - 1`. This lane attacks exactly that, and
nothing else.

---

## 1. The mechanism (stated now, before any number)

**Prose.** The clock sector carries a rate `Q = d(tau)/dt`. Multiplying the rate deficit `(Q - 1)`
by a constant is the flat direction: it rescales `Phi`, hence `a0`, hence `kappa`, and leaves every
formation equation untouched. The new physics does **not** add a force. It **anchors** `Q`: the
vacuum is not an inert background but a state with an intrinsic period -- de Sitter space is
periodic in imaginary time with period `beta_Lam = 2 pi / H_Lam` (KMS), `H_Lam = c sqrt(Lam/3)` --
and the *settling* of the clock is the phase transition in which the clock's rate **locks** to that
period. Below the lock the sector is unpolarised (`P = 0`, `mu = 1`, Newtonian); at the lock the
polarisation turns on and the rate is pinned, so `Q` stops being a free normalisation and becomes a
boundary condition on the transition surface. The acceleration at which the lock happens **is**
`a0`. Because the lock is a condition on the *normalisation of `Q`* and not on the dynamics, the
law `g_N = g^2/(g + a0)`, the stress `Pi_ij`, the universal column `Sigma_c = a0/(2 pi G)` and the
formation ledger are untouched; only the flat direction is removed.

**Equations.**

```
(1)  Q = dtau/dt ,      a_mu = grad_mu ln Q ,      |a| = g / c^2        (static weak field)
(2)  vacuum:  beta_Lam = 2 pi / H_Lam ,   H_Lam^2 = Lam c^2 / 3 ,   Lam = 8 pi G rho_Lam / c^2
              ==>  H_Lam^2 = (8 pi / 3) G rho_Lam ,     R_Lam = c / H_Lam
(3)  LOCK (n:m phase lock of the clock to the vacuum period):
              a0 / c  =  (n/m) / beta_Lam  =  (n/m) H_Lam / (2 pi)
              equivalently   a0 / c^2 = (n/m) / (2 pi R_Lam)
(4)  kappa^2  :=  a0^2 / (c^2 G rho_Lam)  =  (n/m)^2 * 2 / (3 pi)
(5)  1:1 lock:  kappa = sqrt(2/(3 pi))            <-- the lane's output
```

Note `hbar` cancels: `beta_Lam = hbar/(k_B T_Lam)` with `T_Lam = hbar H_Lam/(2 pi k_B)`, so the
lock value is `hbar`-free even though the *mechanism* (thermal periodicity) is quantum. That is a
feature, and it is also the cost: this lane imports one piece of quantum vacuum physics into an
otherwise classical framework. Disclosed, not hidden.

---

## 2. What is frozen, and what is a free choice

| item | status |
|---|---|
| the lock equation (3) | **postulated here** (this is the new physics; the lane does not pretend to derive it from the framework) |
| `n/m` (winding of the lock) | **discrete**, pre-registered family `{2:1, 1:1, 1:2}` graded separately |
| the lock target (`H_Lam` = vacuum rate) vs (`H_0` = total rate) | **discrete**, 2 options, both graded |
| the `2 pi` (KMS period vs `1/H`) | fixed by (2); the no-2pi sibling is graded as mutation MU2 |
| `G`, `c`, `H_0`, `Omega_Lam` | measured inputs (Planck), never adjusted |
| `a0` measured, `kappa` measured | frozen from `CFG493` (`a12e36e397` era): `a0 = 7.8105e-11`, `kappa_can = 0.4172 +/- 0.0946`, `sigma_dex = 0.0985` |
| **continuous free parameters** | **0.** `kappa` is not fitted anywhere in this lane. |

---

## 3. Gates (thresholds frozen now)

| id | gate | PASS if | FAIL if |
|---|---|---|---|
| **G0** | input reproduction: this lane's `H_0, Omega_Lam, G, c` reproduce CFG493's `a0(cH_Lam/2pi) = 8.6257e-11` and `kappa_meas = 0.417214` | rel <= 2e-3 | rel > 2e-3 |
| **G1** | **independence**: the lock does not restate `kappa = 1/2`. Lean: `2/(3 pi) != 1/4`. | proven | unproven |
| **G2** | **capacity fix**: the lock is charged under `G_lam`. Lean: if `a0^2 = (c H_Lam/2pi)^2` and `a0 != 0`, then `(lam*a0)^2 = (c H_Lam/2pi)^2` forces `lam^2 = 1`. | proven | unproven |
| **G3** | derived `a0` vs measured `a0`, pull in dex `(log10 a0_lock - log10 a0_meas)/sigma_dex` | \|pull\| < 2 | \|pull\| > 3 |
| **G4** | does the lock **discriminate** from the fitted `1/2`? offset `= log10(kappa_lock/kappa_half)` | offset > 2 x 0.0985 dex (i.e. > 0.197 dex) | -- (report the precision needed) |
| **G5** | every discrete sibling (winding 2:1, 1:2; target `H_0`; no-2pi) graded, each with its pull | all reported | any omitted |
| **G6** | parameter count of the whole chain | 0 continuous | any continuous |
| **G7** | `8 pi` audit: does the chain secretly use the record identity `a0^2/(8 pi G) = rho_Lam c^2/(32 pi)` (which is *equivalent to* `kappa^2 = 1/4`, FINAL-19 `identity_iff_kappa_half`)? | uses only `Lam = 8 pi G rho_Lam/c^2` (Einstein's equation), not the identity | uses the identity |

---

## 4. Predicted label (written before the run)

> **PREDICTED: `kappa` becomes an OUTPUT with zero continuous free parameters, and the output is
> `sqrt(2/(3 pi)) = 0.460659` for the 1:1 vacuum lock. It does NOT reproduce the record's fitted
> `kappa = 1/2` (it is 8.5% below it, +0.043 dex in `a0`). The current `a0` error (0.0985 dex,
> 22.7%) cannot separate the two, so G4 is expected to return NOT DISCRIMINATED and the lane will
> report the precision a decisive test needs.**

Predicted per-gate: G0 PASS, G1 PASS, G2 PASS, G3 PASS (pull ~0.44), G4 NOT DISCRIMINATED
(offset 0.043 dex << 0.197 dex), G5 PASS, G6 PASS (0 continuous), G7 PASS.

**If the run disagrees with this paragraph, the run wins and the paragraph is quoted as a failed
prediction in RESULT.md.**

---

## 5. Mutation arms (each must bite, or the lane proves nothing)

| id | change | expected outcome |
|---|---|---|
| **MU1** | lock target `H_0` (total expansion rate) instead of `H_Lam` | `kappa = sqrt(2/(3 pi Om_Lam))` = 0.5567; pull ~1.27; **not excluded** -- reported as the residual ambiguity |
| **MU2** | drop the `2 pi` (lock to the angular rate `H_Lam`) | `kappa = sqrt(8 pi/3)` = 2.894; ~26 sigma; **excluded** |
| **MU3** | winding 2:1 | `kappa = 2 sqrt(2/(3 pi))` = 0.9213; ~5.3 sigma; **excluded** |
| **MU4** | the FINAL-19 capacity route (saturation of the DEC ceiling) | `kappa = sqrt(2 pi)` = 2.5066; **excluded** (already on the record) |
| **MU5** | **circularity twin**: replace the lock with the record identity `a0^2/(8 pi G) = rho_Lam c^2/(32 pi)` | recovers `1/2` trivially; must **FAIL G1** (Lean: the identity <=> `kappa^2 = 1/4`) |
| **MU6** | **vacuous twin**: declare the lock "just another flat direction" | must be rejected by **G2** (the lock is charged under `G_lam`) |
| **MU7** | winding 1:2 | `kappa = 0.2303`; ~2.0 sigma; reported, not decisive |

---

## 6. Self-punishing disclosure, pre-registered

`CFG493`'s candidate table **already contains** `c H_Lam / 2 pi = 8.6257e-11` with pull `0.4378`,
and it has the smallest pull of the five candidates CFG493 listed. This lane therefore constructs a
mechanism toward a value whose pull was already visible on the record. The 1:1 / vacuum / with-2pi
choice is **post-selected over 3 discrete options using that table**. The lane will report the
pull *as post-selected* (i.e. not as a 0.44-sigma confirmation) and will state the number of
discrete options tried. This is recorded here, before the run, so it cannot be softened later.

---

## 7. What this lane may not do

* may not adjust `a0`, `H_0`, `Omega_Lam`, `G`, `c` or any measured input;
* may not relabel `kappa = 1/2 FITTED` as derived;
* may not pool footings (canonical `rho_Lam` and alt `rho_crit` reported separately);
* may not claim the mechanism is derived from the framework -- it is **new physics, postulated**;
* may not commit anything (the parent commits).
