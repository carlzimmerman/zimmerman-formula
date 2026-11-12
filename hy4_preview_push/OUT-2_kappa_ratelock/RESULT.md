# OUT-2 (KAPPA_RATELOCK) RESULT: the clock-rate lock makes kappa an OUTPUT -- and the output is not 1/2

Date: 2026-11-12. Test lane. **Adopts nothing, relabels nothing, is not registered.**
`kappa = 1/2 FITTED; not theory closed.` Footings graded separately, never pooled.
Criteria: `PREREGISTER.md`, committed **alone** before `out2.py`, `OUT2RateLock.lean` or any number
existed. Predicted label in §4 of that file: the run agrees with it except for one mis-stated
number (defect D1).

---

## 1. The one-line answer

**Yes to the assignment, no to the value.** Anchoring the clock rate `Q` to the vacuum's de Sitter
period removes the `G_lam` flat direction and turns `kappa` into a derived pure number with **zero
continuous free parameters**:

```
kappa = sqrt(2/(3 pi)) = 0.460659          (exact; no measurement error enters it)
a0    = c H_Lam / (2 pi) = (8.6257 +/- 0.0830) e-11 m/s^2   (Planck inputs only, 0.96 %)
```

It is **7.87 % below the record's fitted `kappa = 1/2`** (−0.0356 dex in `a0`), i.e. the two
predictions are separated by only 0.415σ *in units of the measurement's own `kappa` error*
(0.0946), while the measurement carries 25.5 %: **the data cannot tell them apart, so the lane
neither confirms the fit nor refutes the lock.** What the lane does
claim is that `kappa` is no longer a fit at all, and that a decisive test needs `a0` to **4.18 %**.

---

## 2. The mechanism

**Prose.** The clock sector carries a rate `Q = dtau/dt`. Rescaling the rate deficit `(Q − 1)` is the
`G_lam` flat direction: it rescales `Phi`, hence `a0`, hence `kappa`, and leaves every formation
equation invariant. So the fix cannot be a force term, a stress or a saturation condition (FINAL-19
tried the last of these and got `kappa = sqrt(2 pi) = 2.5066`, 22σ out). The new physics **anchors
`Q`**: the vacuum is not inert — de Sitter space is periodic in imaginary time with period
`beta_Lam = 2 pi / H_Lam` (KMS), `H_Lam = c sqrt(Lam/3)` — and the *settling* of the clock is the
phase transition in which the clock's rate **locks** to that period. Below the lock the sector is
unpolarised (`P = 0`, `mu = 1`, Newtonian); at the lock the polarisation turns on and the rate is
pinned, so `Q` stops being a free normalisation and becomes a boundary condition on the transition
surface. The acceleration at which the lock happens **is** `a0`. Because the lock is a condition on
the *normalisation of `Q`* and not on the dynamics, the law `g_N = g^2/(g + a0)`, the anisotropic
stress `Pi_ij`, the universal column `Sigma_c = a0/(2 pi G)` and the formation ledger are all
untouched. Only the flat direction is removed.

**Equations.**

```
(1)  Q = dtau/dt ,   a_mu = grad_mu ln Q ,   |a| = g / c^2            (static weak field)
(2)  vacuum:  beta_Lam = 2 pi / H_Lam ,   H_Lam^2 = Lam c^2/3 ,   Lam = 8 pi G rho_Lam / c^2
              ==>  H_Lam^2 = (8 pi/3) G rho_Lam ,   R_Lam = c / H_Lam = 5374 Mpc
(3)  LOCK (n:m phase lock of the clock to the vacuum period):
              a0/c = (n/m) / beta_Lam = (n/m) H_Lam / (2 pi)
              equivalently  a0/c^2 = (n/m) / (2 pi R_Lam)
(4)  kappa^2 := a0^2 / (c^2 G rho_Lam) = (n/m)^2 * 2/(3 pi)
(5)  1:1 lock:  a0 = c H_Lam/(2 pi),  kappa = sqrt(2/(3 pi)) = 0.460659,
                c^2/a0 = 2 pi R_Lam   (verified numerically to 1e-9 relative)
```

`hbar` cancels: `beta_Lam = hbar/(k_B T_Lam)` with `T_Lam = hbar H_Lam/(2 pi k_B)`, so the output is
`hbar`-free even though the *mechanism* is quantum. That is the lane's central cost and it is
disclosed: **one piece of quantum vacuum physics is imported into an otherwise classical framework.**

---

## 3. The derivation of kappa (four lines, no fit)

```
a0^2   = c^2 H_Lam^2 / (4 pi^2)                    [1:1 lock, eq (3)]
H_Lam^2 = (8 pi/3) G rho_Lam                       [Einstein's equation, eq (2)]
------------------------------------------------------------------
a0^2   = (2/(3 pi)) * c^2 G rho_Lam
kappa^2 = a0^2 / (c^2 G rho_Lam) = 2/(3 pi)        [definition of kappa]
kappa  = sqrt(2/(3 pi)) = 0.460658866              Q.E.D.
```

`2 pi` appears once, as the KMS period; `8 pi` appears once, as Einstein's. Neither is adjusted.
**The `8 pi` audit (G7):** under the lock `a0^2/(8 pi G) = rho_Lam c^2/(12 pi^2)`, **not** the
record's `rho_Lam c^2/(32 pi)`. Ratio 0.8488 ≠ 1. The chain never uses the record identity — which
is the identity that is *equivalent to* `kappa^2 = 1/4` (Lean T9, and FINAL-19's
`identity_iff_kappa_half`).

---

## 4. The number, with its error bar

| quantity | value | error | source of the error |
|---|---|---|---|
| `kappa` (output) | **0.460659** | **exact** | none — a pure number, `sqrt(2/(3 pi))` |
| `a0` (derived) | **8.6257e-11 m/s²** | **± 0.0830e-11 (0.96 %)** | Planck `H_0 ± 0.54`, `Omega_L ± 0.0073` |
| `a0/(c H_0)` | 0.131724 | ± 0.00127 | same |
| `a0/(c H_Lam)` | **1/(2 pi) = 0.159155** | exact | none |
| bracket (Lean) | `2/5 < kappa < 1/2` | proven | `pi < 4`, `pi > 3` |

**Against the measurement** (CFG493: `a0 = 7.8105e-11`, `sigma_dex = 0.0985`):

| footing | measured `kappa` | pull of the lock |
|---|---|---|
| canonical (`rho_Lam`) | 0.4172 ± 0.0946 | **+0.46σ** (dex pull on `a0`: **+0.44σ**) |
| alt (`rho_crit,0`) | 0.3452 ± 0.0783 | +1.47σ |

Footings are **not pooled**. The lock output is footing-**invariant** (a pure number); the
measurement is footing-dependent. That asymmetry is a feature of the output, not a defect of the
data.

**Provenance of the pull, honestly:** `CFG493`'s candidate table already contained
`c H_Lam/2 pi = 8.6257e-11` with pull `0.4378`, the smallest of the five candidates it listed. This
lane built a mechanism toward a value whose pull was already visible. The 1:1 / vacuum-rate /
with-2pi choice is **post-selected over 3 discrete options** using that table (pre-registered §6).
Read the 0.44σ as a consistency check, **not** as a 0.44σ confirmation.

---

## 5. What it predicts that is not yet measured

1. **`a0 = c H_Lam/(2 pi) = 8.6257e-11` m/s², i.e. `a0/(c H_Lam) = 1/(2 pi)` exactly.** No free
   parameter. To separate this from the record's fitted `kappa = 1/2` (8.54 % away) at 2σ needs
   `a0` to **4.18 %**. Today: combined 25.5 %; CFG493's route floor 8.9 % (S_gas-dominated); its
   own power label for that floor is **"NOT POSSIBLE"**. **No existing route can decide it.**
2. **The lock target is the vacuum's rate `H_Lam`, not the total `H_0`.** These give 0.4607 vs
   0.5566 — a 20.8 % split, decidable at ~5 % on `a0`. Today 0.44σ vs 1.27σ: undecided.
3. **If dark energy is dynamical, `a0` tracks it:** `a0(z)/a0(0) = (rho_DE(z)/rho_DE(0))^{1/2}`,
   i.e. `(1+z)^{1.5(1+w)}` for constant `w`. `w = −1` gives exactly the framework's flat law
   (0.000 dex); DESI-like `w0 ≈ −0.8` gives a few ×0.01 dex at `z ≈ 1`, an order of magnitude under
   the ±0.2–0.35 dex systematics of every published TFR zero point. L276 grades the whole arm
   **UNDECIDED**; this lane claims no number for it.
4. **The lock is a phase transition, so the rate is pinned, not smoothed:** it predicts a universal
   non-analyticity at `g = a0` — a kink in `Q`, hence in the RAR — against the null of the analytic
   crossover `mu = u/(1+u)`. The RAR's shape within a factor ~2 of `g = a0` is unmeasured.
   **(Weakest item: see defect D7.)**
5. **Falsification in one number:** the winding is 1:1, so any measured `a0/(c H_Lam)` differing
   from `1/(2 pi)` by more than ~5 % kills the mechanism outright.

**What it does not touch:** the amount (11× over budget), clusters (+0.5 dex), hosted dwarfs
(+0.5–0.6 dex), discs in an external field. All are unchanged and still open.

---

## 6. Gates

| gate | result | verdict |
|---|---|---|
| G0 input reproduction vs CFG493 | `a0(cH_Lam/2pi)` rel **3e-16**; `kappa_meas` rel 2.2e-4 (canonical), 3.1e-6 (alt) | **PASS** |
| G1 independence (`2/(3 pi) ≠ 1/4`) | Lean `lock_kappaSq_ne_quarter`; also `kappa < 1/2` proven | **PASS** |
| G2 capacity fix (charged under `G_lam`) | Lean `lock_charged_under_Glambda` (`lam^2 = 1`) | **PASS** |
| G3 pull vs measured `a0` | +0.44σ (dex), +0.46σ canonical / +1.47σ alt on `kappa` | **PASS** |
| G4 discriminates from `1/2`? | offset 0.0356 dex; 2σ of the current error is 0.197 dex | **NOT DISCRIMINATED** (needs 4.18 %) |
| G5 discrete siblings | 7 graded, none omitted | **PASS** |
| G6 parameter count | 0 continuous, 2 discrete, 1 postulate | **PASS** |
| G7 `8 pi` audit | `a0^2/(8 pi G) = rho c^2/(12 pi^2)` ≠ `rho c^2/(32 pi)`; ratio 0.8488 | **PASS** |

`OUT-2 COMPLETE: 7/8 gates PASS; G4 returns NOT DISCRIMINATED (a pre-registered outcome, not a
rescue).`

---

## 7. Mutation arms (8/8 bite)

| arm | change | outcome |
|---|---|---|
| MU1 | lock to `H_0` not `H_Lam` | `kappa` 0.4607 → 0.5566 (+20.8 %), pull 0.44 → 1.27σ — **not excluded** (residual ambiguity, D5) |
| MU2 | drop the `2 pi` (angular rate) | `kappa` = `sqrt(8 pi/3)` = 2.894, **+8.54σ** — excluded |
| MU3 | winding 2:1 | `kappa` = 0.9213, **+3.49σ** — excluded |
| MU4 | FINAL-19 DEC saturation | `kappa` = `sqrt(2 pi)` = 2.507, **+7.91σ** — excluded (already on the record) |
| MU5 | record identity as input | Lean twin fails: `identity_is_independent_FALSE`, `linarith failed to find a contradiction` |
| MU6 | "still a flat direction" | Lean twin fails: `lock_not_charged_FALSE` / `lock_scale_invariant_FALSE`, `unsolved goals: a0^2*4 = a0^2` |
| MU7 | winding 1:2 | `kappa` = 0.2303, −2.62σ — marginal, not decisive |
| MU8 | sign of the offset | lock is **below** 1/2 (`a0_lock/a0_half = 0.9213`), not above |

---

## 8. Lean certificate

`OUT2RateLock.lean`, compiled at its own path inside the Lake project
(`cd fable_independent_2026/lean_2026 && lake env lean <abs path>/OUT2RateLock.lean`):

```
EXIT = 0     errors: 0     warnings: 0
sorry (proof terms): 0     admit: 0     sorryAx: 0
12 theorems; every #print axioms line reads [propext, Classical.choice, Quot.sound]
```

| theorem | what it certifies |
|---|---|
| `vacuum_rate_sq` | `H_Lam^2 = (8 pi/3) G rho` from `Lam = 8 pi G rho/c^2` (Einstein's `8 pi`, the only one used) |
| `kappaSq_from_lock` | **the output**: `kappa^2 = 2/(3 pi)` |
| `lock_kappaSq_pos` | the output is a real positive number |
| `lock_kappaSq_ne_quarter` | **G1**: the lock is not a restatement of `kappa = 1/2` |
| `lock_kappa_lt_half` | **stronger G1**: `kappa_lock < 1/2` (from `pi > 3`) |
| `lock_kappa_gt_two_fifths` | `kappa_lock > 2/5` (from `pi < 4`) → `0.4 < kappa < 0.5` |
| `lock_charged_under_Glambda` | **G2, the capacity fix**: `a0` and `lam*a0` both on the lock ⟹ `lam^2 = 1` |
| `kappaSq_from_lock_winding` | the family `kappa^2 = n^2 * 2/(3 pi)` (MU3, MU7) |
| `identity_iff_kappaSq_quarter` | **MU5**: the record identity ⟺ `kappa^2 = 1/4` (circular) |
| `lock_pressure` | **G7**: under the lock, `a0^2/(8 pi G) = rho c^2/(12 pi^2)` |
| `twelve_pi_sq_ne_thirty_two_pi` | `12 pi^2 ≠ 32 pi` (`3 pi ≠ 8`), so G7 is a different statement |
| `lock_rate_ratio` | the lock written as the rate ratio `a0/c = H_Lam/(2 pi)` |

**Scope, stated in the file's header:** Lean certifies algebra, not physics and not data. The lock
equation is a *postulate*; the KMS period, the 1:1 winding and the choice of `H_Lam` as the target
are inputs, and the numeric comparison to CFG493 lives in `out2.py`.

`OUT2RateLock_MUTATE.lean` (the false twin): **EXIT = 1, 7 errors**, all six false theorems
unprovable.

---

## 9. Defects, disclosed

* **D1 (preregistration error, self-reported).** §4 of `PREREGISTER.md` stated the offset from
  `kappa = 1/2` as "+0.043 dex / 8.5 %". The run gives **0.0356 dex / 7.87 %**: 0.043 dex was the
  lock-vs-*measured* ratio, mis-copied as the lock-vs-*fit* offset. Consequence: the precision a
  2σ test needs is 4.18 %, not the 4.3 % pre-registered. The predicted label
  ("PASS on output, FAIL on recovering 1/2, NOT DISCRIMINATED") is unchanged.
* **D2.** The 0.44σ pull is post-selected over 3 discrete options against CFG493's own pull table
  (pre-registered §6). Not a confirmation.
* **D3.** The lock equation (3) is **postulated**, not derived from the framework. 1 imported
  postulate, 2 discrete choices, 0 continuous parameters.
* **D4.** The mechanism is quantum (KMS periodicity) inside a classical framework. The output is
  `hbar`-free, which is why it is still reportable, but the import is real.
* **D5.** MU1 (`H_0` instead of `H_Lam`) is **not excluded** (1.27σ). The mechanism does not
  uniquely select its own lock target; "the vacuum" is argued, not proven. This is the lane's
  largest residual freedom.
* **D6 (build defect, recorded not hidden).** The **first** build of `OUT2RateLock.lean` had **3
  theorems carrying `sorryAx`** (`lock_kappa_lt_half`, `lock_kappa_gt_two_fifths`,
  `lock_rate_ratio`) from a wrong `Real.sqrt_lt_sqrt` arity, a `ring` after an already-closed
  `field_simp`, and a `positivity` failure. The reported build is the repaired one (exit 0, 0
  errors, no `sorryAx`); the intermediate output is kept in the lane's history and described here
  so "the build that was committed" and "the build that passes" are not conflated.
* **D7.** The *phase-transition* content (§5 item 4) is asserted, not derived; the output `kappa`
  does not depend on it, but prediction (4) does. Weakest part of the lane.
* **D8.** Footing dependence is disclosed, not pooled: the lock output is footing-invariant, the
  pull is not (0.46σ canonical vs 1.47σ alt).

---

## 10. What this does and does not change

* **Does change:** `kappa` is now an **output** of a stated mechanism with no continuous free
  parameter, and the value is `sqrt(2/(3 pi)) = 0.460659`, **not** `1/2`. The `G_lam` flat
  direction is removed by an anchoring of `Q`, not by a new force — which is what the assignment
  asked for and what nine sectors plus three dedicated routes could not do.
* **Does not change:** the register's label. `kappa = 1/2` remains **FITTED**, because this lane's
  output is a *different* number and the data cannot choose between them. If the record keeps
  `1/2`, this mechanism is wrong by 7.87 %; if the lock is right, the record's fits carry a
  −0.036 dex shift in `a0`, which is 0.25σ of their own 0.14–0.17 dex scatter, i.e. invisible there
  and visible only to a 4 % `a0` measurement that does not exist yet.
* **Consistent with:** `CFG493` (`0.4172 ± 0.0946`, "CONSISTENT BUT NOT DISCRIMINATING"),
  `kappa_closure/k01–k05` (the horizon value `0.461`, previously a coefficient with no mechanism),
  `L276` (the `a0(z)` arm is undecided for every law), and `FINAL-19` (which excluded the
  saturation route, 22σ).

`kappa = 1/2 FITTED; not theory closed. Adopts nothing.`
