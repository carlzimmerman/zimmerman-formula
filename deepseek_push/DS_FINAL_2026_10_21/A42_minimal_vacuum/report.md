# A42 — the minimal vacuum: β = 0, Λ_bare = 3H₀²/c², and what the theory predicts for cosmology

**Lane:** A42_minimal_vacuum · **Date:** 2026-10-21 · **Base:** `THEORY.md` (P1/P3, §3.6, §4),
`A33_master_action/MASTER_ACTION.md` §3.5 and K16, `A18_two_ratios/report.md`.
**Script:** `a42_checks.py` (27/27 PASS, exit 0, 1.2 s) · **Output:** `a42.out` · **Data:** `a42_results.json`.
Six mutations, each exit 1: `MUTATE.md`, `a42_MUTATE_*.out`.

## Claim

**The chain is exact, and it is the last thing that is.** β = 0 does give `H² = Λ_bare c²/3`, and
`Λ_bare = 3H₀²/c²` does give `H = H₀`, `ρ_bare = ρ_crit` and `a₀ = 0.5 c √(Gρ_crit) = 1.1312×10⁻¹⁰ m/s²`
(−0.070 % from the quoted `1.132×10⁻¹⁰`). But the same three lines that produce those numbers also
produce a universe with **no matter in it**: at β = 0 equation (F1) is exactly GR, so
`H₀² = Λ_bare c²/3` and `H₀² = Λ_bare c²/3 + 8πGρ_m/3` cannot both hold. β = 0 is therefore not a
cosmology — it is the **empty de Sitter endpoint**, `Ω_Λ,eff = 1`, with `H(z) = H₀` for every z, no Big
Bang, no CMB.

Put the census in and the algebra chooses the coupling for you:

> **β = (2/3) Ω_m = 0.21087**, with `Λ_bare = 3H₀²/c²` unchanged.

That is the only value of β for which `Λ_bare = ρ_crit` coexists with `Ω_m = 0.3163` at `H = H₀`.
It closes the dark-energy budget **exactly** — the 1.462 excess is not a fine-tuning, it *is* the matter
density, `Λ_bare/Λ_obs = 1/(1−Ω_m) = 1.4626`, and the clock's stress at that β is `ρ_β = −Ω_mρ_crit`
to the last digit. And it changes the expansion history: the `(2+3β)` factor multiplies the matter term,
so the branch is **flat ΛCDM with `Ω_m,eff = Ω_m/(1+Ω_m) = 0.2403`**, i.e. `H(z=1)` is **8.65 % low** and
the comoving distance at z = 1 is **4.81 % long** (+7.15 % at z = 2) against Planck-LCDM at the same
Ω_m. That is measurable many times over, and it is the wrong sign: the branch is excluded at **10.3σ**
in `Ω_m,eff` (and 0.1092 against 0.1431 in `Ω_m h²`, which is worse).

So the payoff in the task's item (4) is real and it is a *falsification*: the framework has **no
cosmological free parameter beyond Ω_m** — β and Λ_bare are both predicted — and the prediction does not
match the sky. §4 enumerates the three ways to keep `a₀ = 1.132×10⁻¹⁰`: two fail on the expansion
history (the clock stress at β = (2/3)Ω_m, and curvature), and the third — a constant **negative** vacuum
energy `−Ω_mρ_crit` — is not in the action. The agent the action does contain is the one that misses.

**Status:** `NO-GO(β=0 as a cosmology)` + `DERIVED(the chain, the Λ–a₀ identity, β = (2/3)Ω_m)` +
`NUMERICAL(the background table and the 8.7 % H(z=1) discrepancy)`.

---

## 1. The chain, exactly

From (F1) of A33/`MASTER_ACTION.md` §3.5, `3(2+3β)H² = 2Λ_bare c² + 4Kρ` (`K = 4πG`; the action's own
units are c = 1, so the `c²` on Λ is the restored one). (F1) is one line from the minisuperspace
Lagrangian `L_bg = −3(2+3β)aȧ²/(4KN) − ΛNa³/(2K) − ρNa³`: varying `N` at `N = 1` gives it directly, and
at β = 0 it reads `6H² = 2Λ + 4Kρ`, i.e. `H² = Λ/3 + 8πGρ/3`. **The `(2+3β)` multiplies the matter term,
not only the Λ term** — that single fact is the whole of §3(c) and §4.

| step | statement | residual |
|---|---|---|
| K1 | β = 0, ρ = 0 ⇒ `H² = 2Λ_bare c²/6 = Λ_bare c²/3` | **0** (symbolic) |
| K2 | `Λ_bare = 3H₀²/c²` ⇒ `H² = H₀²` identically | **0** (symbolic) |
| K2b | (F1) from `L_bg` **with** the matter term; GR at β = 0 | **0 / 0** (symbolic) |
| K3 | `ρ_bare ≡ Λ_bare c²/8πG = 3H₀²/8πG = ρ_crit` | ratio `1.000000000000000` |
| K4 | `a₀ = 0.5 c √(Gρ_crit)` | `1.131204×10⁻¹⁰ m/s²` |
| K5 | vs the quoted values | **−0.0704 %** vs `1.132e-10`; **−0.1145 %** vs `1.1325e-10` |
| K6 | `Λ = 32πa₀²/c⁴ ⇔ a₀ = κc√(Gρ_bare)` with κ = ½ | **0** (identity) |
| K7 | `a₀ ∝ κ`; κ = 1 would give `2.2624×10⁻¹⁰` | factor exactly 2 |

The −0.07 % is not a discrepancy in the physics, it is the three-digit rounding of the quoted number:
`H₀ = 67.447 km/s/Mpc` reproduces `1.132×10⁻¹⁰` exactly, and `1.1325×10⁻¹⁰` needs 67.477. At
`H₀ = 67.4` the identity gives 1.1312. K2b closes a gap in A33's K10, which varies `L_bg` at `ρ = 0` and so never tests the coefficient of the
matter term — the coefficient §3(c) turns on. K6 is a **control, not a result**: `Λ = 32πa₀²/c⁴` is the same
statement as κ = ½, so it cannot be evidence for either.

Three numbers that follow and are worth keeping:

- `ρ_bare = ρ_crit = 8.5329×10⁻²⁷ kg/m³`, `Λ_bare = 1.5926×10⁻⁵² m⁻²`;
- `Λ_bare/Λ_obs = 1.4624` against `1/(1−Ω_m) = 1.4626` — agreement **1.5×10⁻⁴**, i.e. the quoted 1.462
  and the census are the same statement;
- `a₀ = 1.1312×10⁻¹⁰` is **+2.53 %** above A9's free SPARC fit `1.1033×10⁻¹⁰`, where the canonical
  footing `9.354×10⁻¹¹` is 15.2 % below it. The galaxy data prefer the bare-vacuum footing, which is why
  the branch in §3 matters.

## 2. The principal-positivity bound — and the fact that β = 0 is a limit point

With `η = γ = K L_*²/2` and `L_* = 24 pc`:

```
2 η a₀²/K  =  L_*² a₀²  =  (a₀ L_*/c²)²  =  (L_*/L_MOND)²  =  8.688×10⁻¹⁹     [a₀ = 1.1312e-10]
                                                              5.948×10⁻¹⁹     [a₀ = 9.36e-11]
```

(K8 verifies the algebra symbolically; the SI conversion is the standard one — in c = 1 units a₀ has
dimension 1/L. A3 K12 quotes `2(L_*a₀/c²)² = 1.19×10⁻¹⁸` on the canonical footing, which reproduces
`2×5.948×10⁻¹⁹` — an independent cross-check of the conversion.)

So the honest answer to "show that β = 0 satisfies the bound" is: **it does, to eighteen digits, and not
strictly.** The bound's right-hand side is `8.69×10⁻¹⁹`, not zero. Two readings, both recorded in K9/K10:

- **as a strict inequality**, β = 0 is below it by `8.69×10⁻¹⁹`; the minimal admissible vacuum is
  `β = 8.69×10⁻¹⁹`, which shifts `Λ_bare` by `1.5β = 1.30×10⁻¹⁸` relative — unobservable at 18 digits;
- **as a condition on the propagating scalar**, the bound has no domain at β = 0: A3's scalar kinetic
  coefficient is `B = K(2+3β)/β`, which diverges as β → 0, i.e. the deformed mode is absent and the
  gravitational sector is **exactly GR**. The admissible set is `{0} ∪ (8.69×10⁻¹⁹, ∞)`.

Either way the physics at β = 0 is unchanged, and A33's use of "β > 0" is safe. What is **not** safe is
reading `β > 2ηa₀²/K` as "β may be taken to be zero and then matter added": that is the step §3 tests.

For reference the branch clears the bound by `2.43×10¹⁷`.

## 3. The cosmology of Ω_Λ,eff = 1

`E(z) = H(z)/H₀`, `d_C` in Mpc, age in Gyr, `q₀ = −ä/(aH²)` at z = 0. Radiation is neglected
(0.03 % on the age, <10⁻⁴ on `d_C` at z < 3; K14 reproduces Planck's 13.797 Gyr — computed at H₀ = 67.36 —
to 0.004 Gyr). All rows use H₀ = 67.4 for the distances so the comparison is at fixed H₀.

| model | E(0.5) | E(1) | E(2) | d_C(1) | d_C(2) | age | q₀ |
|---|---|---|---|---|---|---|---|
| **(a) pure de Sitter** (Λ only, β = 0) | 1.0000 | 1.0000 | 1.0000 | 4448.0 | 8895.9 | **∞** | −1.000 |
| **(b) flat, census** (Ω_c 0.2666 + Ω_b 0.0497) | 1.3233 | 1.7928 | 3.0371 | 3398.7 | 5306.4 | 13.780 | −0.5256 |
| **(c) branch** `Λ_bare = ρ_crit`, β = 0.21087 | 1.2533 | 1.6377 | 2.6921 | 3562.1 | 5685.9 | 14.866 | −0.6396 |
| **(d) β = 0 + matter, Λ_bare = ρ_crit** (closed) | 1.1644 | 1.5051 | 2.5872 | 3780.7 | 6049.4 | 15.421 | −0.8418 |
| Planck-LCDM (Ω_m = 0.3153, H₀ = 67.4) | 1.3224 | 1.7908 | 3.0328 | 3400.7 | 5310.8 | 13.793 | −0.5271 |

**(a) The pure de Sitter endpoint.** `H(z) = H₀` exactly, `d_C = (c/H₀)z = 4448.0 z Mpc`, `q₀ = −1`.
There is **no Big Bang**: the age integral is `∫dz/(1+z)/H₀ = ln(1+z)/H₀`, which diverges (K12:
100.2 Gyr at z = 10³, 200.4 Gyr at z = 10⁶). The Hubble time is 14.507 Gyr, 5.2 % above Planck's age,
but the model has no hot early universe, no BBN and no CMB. Against flat ΛCDM with the same census
(row b) the comoving distance is **+30.87 % at z = 1 and +67.65 % at z = 2** — measurable at any
conceivable precision, but the model is excluded by the existence of matter, not by a distance
measurement.

**(b) The census-filled flat case is ΛCDM, identically.** Against Planck-LCDM at the *same* Ω_m the
fractional distance difference is **exactly zero** — it is the same model — so the answer to "is it
measurable" is **no, and not because it is small: there is nothing to measure.** Against Planck's own
`Ω_m = 0.3153` the difference is −0.058 % (z = 1) and −0.083 % (z = 2), two orders of magnitude below
even a Euclid-era distance measurement (0.3 %). And case (b) has a price the task's phrasing hides:
fitting the observed expansion with β = 0 **forces** `Λ_bare = 3H₀²(1−Ω_m)/c² = Λ_obs` (K16,
`1.0888×10⁻⁵²` against `1.0890×10⁻⁵²`), hence `a₀ = 9.354×10⁻¹¹ m/s²` — **17.4 % below** the theory's
own value. **Case (b) is not the theory; it is ΛCDM with the theory's a₀ discarded.**

**(c) The branch that keeps `a₀ = 1.132×10⁻¹⁰` and the census.** β is not free: (F1) at `H = H₀`,
`Λ_bare = 3H₀²/c²`, `ρ = Ω_mρ_crit` has the **single root β = 2Ω_m/3** (K18, symbolic). Its `E(z)` is
flat ΛCDM with `Ω_m,eff = Ω_m/(1+Ω_m) = 0.24029` (K19, residual `8.9×10⁻¹⁶`), because the `(2+3β)`
factor multiplies the matter term: `E² = 2[1+Ω_m(1+z)³]/(2+3β)`. The physical statement behind the
factor is `G_cosmic = 2G/(2+3β) = G/(1+Ω_m) = 0.7597 G_local` — a 24 % difference between the
cosmological and the laboratory Newton coupling, which is the same fact as the shifted `Ω_m`.

Against Planck-LCDM at the same Ω_m: `H(z=1)` **−8.65 %**, `H(z=2)` **−11.36 %**; `d_C(1)`
**+4.81 %**, `d_C(2)` **+7.15 %**; age +7.9 %; `q₀ = −0.6396` against −0.5256. In the parameter that
the shape actually determines, `Ω_m,eff = 0.2403` against `0.3153 ± 0.0073`, i.e. **10.3σ**; in
`Ω_m h²`, 0.1092 against 0.1431 ± 0.0011. **Measurable, and excluded.**

**(d) β = 0 with matter kept.** Then `Λ_bare = ρ_crit` plus `Ω_mρ_crit` is `1.3163` of critical density,
i.e. `Ω_k = −Ω_m = −0.3163` (K21); the model is closed and `H₀,implied = 77.33 km/s/Mpc`, or
equivalently flat with `a₀ = 1.298×10⁻¹⁰` (+14.6 %, and +17.6 % above A9's fit). Distances are
**+11.24 % / +14.00 %** long at z = 1, 2, the age is 15.421 Gyr, `q₀ = −0.8418`. Planck+BAO give
`Ω_k = 0.0007 ± 0.0019`, so this is excluded at **167σ** (K22). **This is the case the task's item (3b)
describes if "Λ_bare = ρ_crit" is taken literally together with the census.**

## 4. The budget: where the 1.462 goes, and whether the numbers close

`ρ_bare = 8.5329×10⁻²⁷ kg/m³ = ρ_crit`, `ρ_DE = 0.6837 ρ_crit = 5.8339×10⁻²⁷`,
`ρ_bare − ρ_DE = 2.6989×10⁻²⁷ kg/m³ = Ω_mρ_crit` **exactly**. So:

> `Λ_bare` is not "1.462× too large". It is `ρ_DE + ρ_m`: the ratio is `1/Ω_DE = 1.4626`, and the
> excess over the observed DE, `(ρ_bare − ρ_DE)/ρ_crit`, is `Ω_m = 0.3163` exactly.

At β = 0 **nothing cancels it**: `ρ_β = −9βH²/4K = 0`. The three ways to close the budget, and their
prices, are all computed (`ρ_DE` here means the *constant* `0.6837ρ_crit`):

| # | agent | required value | `ρ_DE = 0.6837ρ_crit` at z = 0 | `ρ_DE` constant at all z | price |
|---|---|---|---|---|---|
| 1 | **clock stress**, β = (2/3)Ω_m | `ρ_β = −Ω_mρ_crit = −2.6989×10⁻²⁷` | **exact** (K23, residual 10⁻¹⁴) | no — `ρ_β ∝ H²` | `Ω_m,eff = 0.2403`, 10.3σ (case c) |
| 2 | constant **negative** vacuum `ρ_x` | `ρ_x = −Ω_mρ_crit`, `ρ_x/ρ_bare = −0.3163` | exact | **exact** (K25, `|dE| < 2×10⁻¹⁵`) | a new constant equal to minus today's matter density; **not in the action**; negative |
| 3 | curvature | `Ω_k = −Ω_m = −0.3163` | exact | no — `Ω_k ∝ (1+z)²` | 167σ (case d) |

The task's suggested resolution — "the observed DE is the cold sector's own vacuum energy" — is **#2 with
the sign flipped, and it does not work with a positive cold vacuum**: adding `ρ_DE` on top of
`ρ_bare = ρ_crit` gives `H₀ = 87.5 km/s/Mpc`, a 30 % error. The cold sector of this action is a
collisionless Vlasov medium whose stress is dust (`p_c = ρ_cσ_c²`, `σ_c = 8.33 km/s`); it has **no vacuum
energy term** — `L_cold` contains no constant — so #2 is not "the cold sector's vacuum", it is a new
parameter with a negative sign and a magnitude tuned to `−ρ_m,0`.

**What does close, exactly, is #1 at β = (2/3)Ω_m** — and that is the punchline of A33 read backwards:
with `ρ = 0`, matching `Λ_obs` gives `β = −0.2109`; with `ρ = ρ_m`, matching `ρ_crit` gives
`β = +0.2109`. The two footings are `β = ∓(2/3)Ω_m`: same magnitude, opposite sign, and the sign is the
entire difference between "ΛCDM with a₀ = 9.35×10⁻¹¹" and "the theory's own a₀ with a 24 % wrong matter
fraction".

## 5. Status

| item | status |
|---|---|
| the chain β = 0 ⇒ H = H₀, ρ_bare = ρ_crit, a₀ = 1.1312×10⁻¹⁰ | **DERIVED** (K1–K5; exact, −0.07 % is rounding) |
| Λ = 32πa₀²/c⁴ identity | **DERIVED, and it is an identity** (K6, control: cannot be evidence) |
| β = 0 vs `β > 2ηa₀²/K` | **DERIVED + a caveat**: satisfies it to 8.69×10⁻¹⁹, not strictly; β = 0 is the GR limit point (K8–K10) |
| β = 0 as a cosmology | **NO-GO**: it forces `Ω_m = 0` (an empty de Sitter universe with no Big Bang) |
| `Λ_bare = ρ_crit` + census ⇒ β = (2/3)Ω_m | **DERIVED** (K18, unique root) |
| that branch vs Planck-LCDM at the same Ω_m | **NUMERICAL, excluded**: +4.81 %/+7.15 % in `d_C`, −8.65 % in `H(1)`, 10.3σ in `Ω_m,eff` (K19–K20) |
| no cosmological free parameter beyond Ω_m | **DERIVED, and it is the falsification**: β and Λ_bare are predicted, and the prediction misses |
| the 1.462 excess | **DERIVED**: `1/(1−Ω_m)`, exactly `ρ_m/ρ_crit`; cancelled only by the clock stress at β = (2/3)Ω_m (or by a new negative constant) |

## 6. Checks (`a42_checks.py`, 27/27 PASS, exit 0, 1.2 s)

| id | proves | measured | threshold |
|---|---|---|---|
| K1 | β = 0 ⇒ `H² = Λc²/3` (symbolic) | 0 | 0 |
| K2 | `Λ_bare = 3H₀²/c²` ⇒ `H = H₀` (symbolic) | 0 | 0 |
| K2b | (F1) from minisuperspace **including ρ** (A33 K10 tests only ρ = 0) | resid 0 / 0 | 0 |
| K3 | `ρ_bare/ρ_crit` | 1.000000000000000 | 1 ± 1e−14 |
| K4 | `a₀ = 0.5c√(Gρ_crit)` | 1.131204e−10 | \|dev\| < 0.2 % |
| K5 | vs 1.132e−10 / 1.1325e−10 | −0.0704 % / −0.1145 % | \|dev\| < 0.2 % |
| K6 | `Λ = 32πa₀²/c⁴` identity | 0 | 0 |
| K7 | `a₀ ∝ κ`, κ = 1 ⇒ ×2 | 2.000000 | 2 |
| K8 | `2ηa₀²/K = (a₀L_*/c²)²` | `L_*²a₀²` | exact |
| K9 | β = 0 vs the bound | gap 8.688e−19 | < 1e−18 |
| K10 | strict positivity excludes β = 0 | violation 8.688e−19 | 0 < v < 1e−17 |
| K11 | branch clears the bound | 2.43e+17 × | > 1e16 |
| K12 | dS: `E ≡ 1`, `d_C = (c/H₀)z`, no finite age | t(10⁶) = 200.4 Gyr | diverges |
| K13 | flat census matches the closed form | age 13.7802 both | 1e−9 |
| K14 | integrator vs Planck's age | 13.8007 vs 13.797 | < 0.05 Gyr |
| K15 | dS vs ΛCDM at the same census, z = 1, 2 | +30.87 %, +67.65 % | > 1 % |
| K16 | case (b) forces `Λ_obs`, `a₀ = 9.354e−11` | 1.0888e−52 | Λ_obs ± 0.2 % |
| K17 | case (b) vs Planck's Ω_m | −0.058 %, −0.083 % | < 0.3 % |
| K18 | branch β = 2Ω_m/3 (symbolic, unique, used) | 0.210867 | exact |
| K19 | branch `E²` = ΛCDM(`Ω_m/(1+Ω_m)`) | 8.9e−16 | < 1e−13 |
| K20 | branch vs ΛCDM(same Ω_m) | +4.81 %/+7.15 %, −8.65 %/−11.36 %, 10.3σ | > 1 %, > 5σ |
| K21 | β = 0 + matter ⇒ `Ω_k = −Ω_m` | −0.3163, H₀→77.33 | exact |
| K22 | that curvature vs Planck+BAO | 167σ | > 50σ |
| K23 | `ρ_β` identity; closure at the branch | `ρ_β/ρ_crit = −0.316300`, ratio 1.000000000000 | 0 / 1 |
| K24 | 1.462 = 1/Ω_DE; excess = Ω_m | 1.46242 vs 1.46263 | 1e−3 |
| K25 | the only β = 0 closure is `ρ_x = −Ω_mρ_crit` | −2.699e−27 kg/m³, \|dE\| 1.8e−15 | < 1e−12 |
| K26 | one cosmological input | β = 2Ω_m/3 from one root | single root |

Mutations (`--mutate`), each exit 1: `beta0` (K11, K18, K19, K20, K23 — the lane's own premise, taken
literally), `kappa1` (K4, K5, K7, K9), `h0_73` (K4, K5, K9, K16, K24), `no_c2` (K3, K4, K5, K9–K11),
`lam_obs` (K3, K4, K5, K23, K24), `theta_gr` (K19, K20 — the naive "put the census in and set
Ω_Λ = 1−Ω_m" reading). Recorded in `MUTATE.md`.

## 7. What this does not do

1. **No perturbations.** Everything here is the background. The 10.3σ is the `Ω_m,eff` channel of the
   expansion history; a real Planck+BAO+SNe likelihood on the branch is not run, and the cold sector's
   growth (`σ₈`, `f σ₈`) is not computed. The `Ω_m h²` comparison (0.1092 vs 0.1431) says the true
   exclusion is stronger, not weaker.
2. **The bound's coefficient is quoted, not re-derived.** `β > 2ηa₀²/K` is A4 D7 / A22 K9 / round-2 §4;
   this lane evaluates it, identifies that β = 0 is a limit point, and checks the algebraic identity
   `2ηa₀²/K = (a₀L_*/c²)²`. It does not re-derive the factor 2.
3. **`G_cosmic = G_local/(1+Ω_m)` is a consequence, not a check.** I state it because it is the same
   fact as `Ω_m,eff = Ω_m/(1+Ω_m)`; whether BBN tolerates a 24 % lower cosmological G is not computed
   here (it would make the branch worse, not better).
4. **The cold sector is dust.** `p_c = ρ_cσ_c²` with `σ_c = 8.33 km/s` (w ≈ 7.7×10⁻¹⁰). A cold sector
   with a vacuum term is not in `L_cold`; adding one is a new parameter, and §4 shows the sign it would
   need.
5. **κ is untouched.** The whole chain starts from κ = ½ and `a₀ = 1.132×10⁻¹⁰`; A15/A33 leave κ
   underived, and this lane does not change that. It does sharpen the cost: the galaxy data prefer
   `a₀ ≈ 1.10×10⁻¹⁰` (A9), the expansion history prefers `9.35×10⁻¹¹`, and the two are 18 % apart (A9's 17.9 %).
6. **H₀ = 67.4 throughout** (A33/A18); 67.36 appears only in K14's Planck age check. The `h0_73`
   mutation shows the a₀ chain is an 8.2 % effect at H₀ = 73 — i.e. the "1.132e-10" is an H₀ statement
   as much as a theory statement.

## 8. Next

1. **Run the branch through the real likelihood.** `Ω_m,eff = 0.2403` is the weakest statement of the
   mismatch; a Planck+BAO+SNe chain would settle it in one afternoon and should be the lane that replaces
   this one if the branch is to be defended.
2. **Ask what would make `β = (2/3)Ω_m` not apply.** The branch assumes the cold sector is dust and that
   `Λ_bare` is the only vacuum. A cold-sector vacuum term is the only escape in the action's vocabulary,
   and it must be negative and equal to `−ρ_m,0`.
3. **BBN with `G_cosmic = 0.7597 G_local`** is the sharpest independent channel on the branch — sharper
   than the distance test, and it is not in this record.
