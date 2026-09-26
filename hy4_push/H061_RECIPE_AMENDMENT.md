# H061 RECIPE AMENDMENT — 2026-09-26 (RETRACTED IN PART)

> **STATUS CHANGE.** The first version of this file announced a derivation of
> `kappa = 1/2`. **That announcement is withdrawn.** It was wrong twice over:
> it was not new, and it could not have worked. What survives is narrower and
> methodological. The retraction is recorded first because it is the load-bearing
> content of this file.

---

## 0. RETRACTION — the kappa derivation is withdrawn

**What was claimed:** that `kappa = 1/n` with `n = nPol(D) = D(D−3)/2 = 2` at `D = 4`
promotes `kappa = 1/2` from FITTED to DERIVED, and that the recipe's frozen
numbers should be amended accordingly.

**Why it is withdrawn — two independent reasons:**

1. **It is already in the record.** `README.md:66` records the same content from
   `[L230](../../fable_independent_2026/L230_one_number.py)` and
   `[L231](../../fable_independent_2026/L231_the_curve.py)`: *"κ = 1/c where c is
   the function's deep-MOND slope"* and *"μ_n(Y) = 1 − (1+Y)^{−n} has slope exactly
   n … with 1 − μ_n = (1 − μ₁)^n"*. `H017_results.out` states it verbatim:
   *"This is a DERIVATION of the value of n from the dimensionality of spacetime."*
   H061 rediscovered L230 + L231 + H017 and presented them as new.

2. **It is provably impossible in this class.** `README.md:126` — *"κ no-go / zero-mode
   theorem — this class of actions cannot derive the a₀–Λ coefficient; the MOND
   primitive enters the field equations only through its derivative."* `README.md:66`
   sharpened it: the result holds *"regardless of field content or whether Λ appears
   explicitly"*. **κ = 1/n is a normalisation statement, and the normalisation is
   precisely the zero mode the no-go is about.** Relating two empirically fixed
   numbers does not derive either.

**Also withdrawn:** the proposed new frozen ingredient I6's stronger form ("kappa is
derived"). The weaker form — *the kinetic function is not a free function, because
f′ = μ₂ and μ₂ is a member of the counted family* — stands, because it is an
identity, not a normalisation.

**Action taken:** the header of `lean/H061_where_dark_energy_is.lean` has been
corrected in place. The Python lane's gates are unaffected; only their narration was.

---

## 1. What survives — one new, load-bearing warning

**NEW INGREDIENT (I7 — measurement rule).**
The mode count is a **linear coefficient**, not an exponent:

```
mu_n(Y)  is linear at the origin  =>  d ln mu_n / d ln Y  ->  1  for EVERY n
```

Therefore **any log–log fit through the deep-MOND regime is structurally blind to
the mode count.** It returns ≈1 no matter what the theory says.

This is not armchair: **this lane's C2 gate FAILED on its first pass for exactly
this reason.** The gate asked `d ln μ_n / d ln Y → n`; the run returned 1. The fix
was to test the ordinary derivative `μ_n'(0) = n` (certified: `mu_eq_Y_mul_sum`,
`sum_range_ones_eq_card`, `mu_coeff_n1/n2/n3`).

**Why it matters for the recipe:** any future gate that infers the exponent from a
log–log slope is a null measurement wearing a result's clothes. Test the ordinary
derivative.

## 2. Cassini — the banner's dichotomy needs its first horn cut

The `FRIED_CHICKEN.md` banner claims: *no independent dark density ⟹ modified
gravity ⟹ dies on the arm-level Cassini quadrupole (4.8–8.9× the ceiling, proved
carrier-independent).*

**That first horn is unsound against this repo's own committed lanes:**

- `route1B_monotone_escape_2026.py:237` (check 2.2) **PASSES** μ₅ / μ₁₀ / μ₂₀ —
  published monotone interpolation functions **clear** the Cassini quadrupole.
  The verdict says it outright (`:362-366`): *"a monotone, published interpolation
  function (μ_n, n ≥ 5) clears the Cassini quadrupole … What Cassini kills is
  **Carl's interpolation function** … not Carl's a₀."*
- The specific factor is **unsupported**: `cassini_prefactor_check_2026.py:141` —
  *"the SPECIFIC FACTOR 4.8x-8.9x is unsupported by the calibration it claims."*
  Matched-η anchors give **3.17×–6.17×**.
- **"carrier-independent" is kernel-blindness, not theory-independence.** ξ,
  c₁₄/K_B/J_Y and any static-potential→PPN mapping are **not used** in the Q₂
  number at all.

**So the forced choice is not forced.** The escape is **kernel choice**, not a
particle. That vindicates Carl's instinct while correcting his target: he does not
need to reject the corridor, he needs to change the kernel inside it.

## 3. Reminder — the standing record, unchanged

From `README.md:126` and `README.md:60,62`: **κ = ½ remains fitted, not derived.**
κ = 0.551 ± 0.043 (distance-free), combined 0.529 ± 0.034. Four candidate
coefficients sit inside 2σ. The value of Λ itself is **OPEN (owed by everyone)**.

**Do not amend the recipe's frozen numbers on kappa.**

## 4. Next obligation (corrected)

The kappa question is closed as *empirical* and there is a theorem saying the
action class cannot do better. So the next load-bearing calculation is **not**
"derive kappa." It is the one the L374 result already blocked:

> The carrier does not pass through itself (L374: multi-streaming / shell crossing
> fails, energy drift ≤ 1.2e-6, reproduced under 2× grid and dt÷2 to 2e-5). And
> Requirement 10's one non-EOS route — violent relaxation — **was run and falsified**,
> contrary to `FRIED_CHICKEN.md:104-106`.

So: **the amplitude law has no route left**, and the "formation question is unrun"
caveat should be removed from the register. That is a stronger and more honest
statement than the current register makes.

---

*Filed in `hy4_push` per the per-model separation convention. Corrects, and does not
delete, the earlier version of this file.*
