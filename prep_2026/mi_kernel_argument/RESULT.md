# Feeding the DERIVED kernel argument into the MI growth ODE — sigma8 + bulk flow vs Qin 2021

**Date:** 2026-07-17. **Script (exit 0, both a₀ footings):** `growth_derived.py` (reuses the banked
`mi_linear_cosmology/{mi_growth,mi_spectra}.py` ODE, BBKS transfer, Planck normalization, and
Qin-2021 bulk-flow integral). **Upstream:** `DERIVATION.md` / `kernel_argument.py` (the derived,
not posited, prescription); baseline `mi_linear_cosmology/RESULT.md`.

## What is different from the banked run

The banked `mi_growth.py` ran three **posited** floors (`SC`, `floor_a0`, `floor_cH`). This run
drives the **same** ODE with the **derived** prescription: the RAR-producing **first-moment** closure
is BARE for the cosmological element too, and the horizon floor lives only in the **dS–Unruh pole**
(`X_pole = Z² + (|a|/a₀)²`, accel floor `cH_Λ = Z·a₀ = 5.789 a₀`, footing-independent in a₀-units).
The pole couples **only when the mode is slow vs the horizon memory rate** (`ω=H(z) ~ H_horizon`), and
that frequency selection is the theory's **FREE gap-A closure** (PULLBACK PB-D4/PB-P1). The derivation
names **two** forks; this run implements both **self-consistently with the frequency gate**, which the
banked posited `floor_cH` did not:

- **FORK 1 — constant H_Λ floor** (`cH_Λ = Z·a₀`, constant). `ω=H(z) ~ H_Λ` only near z=0, so the
  pole coupling (and the floor) **turns on near z=0 and the mode is BARE at high z**. Implemented as a
  frequency gate `w(z)=1/(1+(r/r_gate)²)`, `r=H(z)/H_Λ`, `r_gate` swept across the free gap (1.5–10).
- **FORK 2 — rising cH·E(z) floor** (horizon rate tracks the instantaneous H(z)). Then `ω=H(z) ~
  H_horizon=H(z)` at **every** epoch → **always** couples to the pole, but the floor value **rises into
  the past** as `c·H(z)=c·H₀·E(z)`.

Endpoints `BARE` (no floor) and `FLOOR_const_allz` (= banked `floor_cH`, floor at ALL z) bracket the two.

## Numbers (canonical a₀=9.36e-11 | alt a₀=1.13e-10; Planck σ₈=0.811; Qin V35=380±25, V100=410±80)

| case (derived reading) | σ₈ (×Planck) can/alt | f₀ | V(35) ×Qin | V(100) ×Qin | verdict |
|---|---|---|---|---|---|
| **BARE** first-moment (RAR-consistent) | 6.90/8.00 (8.5–9.9×) | 1.03 | 5508/6469 (14–17×) | 3337/3919 (8–10×) | **DEAD** overshoot |
| **FORK 1** const floor, **freq-GATED** (r_gate=3) | 4.84/5.56 (6.0–6.9×) | 0.70 | 2654/3068 (7–8×) | 1608/1859 (4–5×) | **DEAD** overshoot |
| — FORK 1 across free gap r_gate=1.5→10 | 5.89→3.09 (7.3→3.8×) | — | 3831→1409 | — | **DEAD** for the whole free range |
| **FORK 2** rising cH·E(z), always-on | 0.83/0.83 (1.02×) | 0.54 | 350/354 (0.9×) | 212/214 (0.5×) | **VIABLE but = ΛCDM (MI OFF)** |
| _FLOOR_const_allz (posited, NOT freq-faithful)_ | 1.02/1.02 (1.26×) | 0.55 | 440 (1.16×) | 266 (0.65×) | _the banked "cure"_ |

Both footings agree (spread ≤15%; alt slightly worse on BARE, identical on the floored cases).

## Verdict — DEAD on one derived fork, ΛCDM-degenerate on the other; the attractive middle is NOT derived

Feeding the **derived** prescription (not the posited floors) into the growth ODE **removes the
appealing banked result** (σ₈≈1.02 *with* bulk flows lifted above ΛCDM toward Qin's high flows).
That result required `floor_cH` = the constant `cH_Λ` floor **applied at every z**, which the
derivation's own frequency argument (DERIVATION §4) says is **not** what the constant-H_Λ fork gives:
a constant floor only bites near z=0. Applied self-consistently with the frequency gate, the two
derived forks split cleanly and **neither lands in the attractive middle**:

- **FORK 1 (constant floor, frequency-gated) is DEAD.** Because most linear growth accumulates at
  z ≳ 0.5 where the growing mode is fast (`H(z) ≫ H_Λ`) and therefore **bare**, the gated floor only
  slows the last e-fold. σ₈ stays **3.8–7.3× Planck** across the *entire* free r_gate gap (bulk flows
  4–8× Qin). The runaway is a high-z effect the late-time floor cannot undo — the classic
  MOND-structure overshoot (Nusser 2002), essentially intact.
- **FORK 2 (rising cH·E(z), always-on) is VIABLE but MI-OFF.** Coupling to the pole at every epoch with
  a floor that rises into the past drives ν_eff→1 at all z, i.e. growth collapses onto ΛCDM:
  **σ₈=0.83, V(35)=350, V(100)=212 — indistinguishable from ΛCDM (333/202)** and **NOT** elevated
  toward Qin's high bulk flows. It survives only by switching MI off cosmologically at all epochs — no
  distinctive MI signal, no Qin enhancement.

**Straight, both footings:** under the DERIVED (frequency-selected) prescription the MI cosmological
verdict is **not a live win**. The two self-consistent derived forks land at **OVERSHOOT-DEAD**
(constant floor, gated) or **ΛCDM-DEGENERATE / MI-OFF** (rising floor); the banked "σ₈≈1 + flows toward
Qin" middle is an artifact of the **posited** constant-floor-at-all-z, which the frequency argument
does not support. The overall picture remains **bracketed and not-forced** — the frequency closure is
the theory's genuinely FREE gap-A degree of freedom (PULLBACK PB-D4/PB-P1 pin nothing), so **no fork is
derived to be *the* answer** — but the specific derived readings do **not** deliver a viable-and-distinctive
cosmology: it is dead (overshoot) or degenerate (no MI signal). The **galactic deep-MOND RAR is
preserved in every case** (the floor is never applied to the fast bound orbits; DERIVATION §3), so this
is not a manufactured save and not a manufactured kill.

**Open (unchanged):** the covariant MI perturbation theory on FLRW must *compute* — not posit — whether
the growing mode's secular acceleration couples to the pole (floored) or the first moment (bare), and
must resolve the constant-H_Λ vs rising-H(z) floor fork; both are needed to collapse the bracket.

*Reproduce:* `cd .../mi_kernel_argument && python3 growth_derived.py` (exit 0). Both a₀ footings.
No "proves"/closed/TOE claim. Credits: Nusser 2002 (astro-ph/0109016); Skordis–Złośnik 2021
(PRL 127:161302); Qin 2021 (CF4TF/W09 bulk flows).
