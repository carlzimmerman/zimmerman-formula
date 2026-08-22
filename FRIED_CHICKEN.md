# FRIED CHICKEN — the requirements

Carl's standing term for a completed field theory. This file exists so "done" is a fixed,
falsifiable target rather than a moving one, and so that neither of us can quietly redefine it
after the fact. Every row is a pass/fail with a number.

**A row may only be marked PASS when a committed script that exits zero produces the number,
on BOTH footings (a₀ = 9.3619e-11 canonical / 1.1279e-10 alt).**

---

## The ten requirements

| # | Requirement | Threshold | Status |
|---|---|---|---|
| 1 | **Rotation curves** | RAR ≤ 0.06 dex intrinsic on 175 SPARC galaxies, Υ inside the Spitzer prior | ⚠️ 0.108 dex observed at Υ=0.70; 0.127 on the μ₁₀ kernel |
| 2 | **BTFR** | v_c⁴ = GM_b a₀, slope 1/4 | ✅ **exponent DERIVED** (`virialisation_2026.py`); normalisation = κ, still fitted |
| 3 | **Lensing tracks dynamics** | \|(p_r+2p_t)/ρc²\| < 0.049 (KiDS-1000 full covariance) | ✅ 1e-7 for any cold carrier |
| 4 | **Solar system — monopole** | 1-AU anomaly inside per-planet EPM budgets | ✅ 4e-28 × Mars budget on μ₁₀ (`route1B_monotone_escape_2026.py`) |
| 5 | **Solar system — quadrupole** | Cassini Q₂ ≤ 5.2e-27 s⁻² | ✅ 0.08–0.21 × ceiling on μ₁₀ |
| 6 | **GW170817** | \|c_T/c_γ − 1\| < 7e-16 | ✅ **structurally absent** under the frame flip (`frame_flip_2026.py`) |
| 7 | **Theoretical health** | no ghost, no gradient instability, no Cherenkov | ✅ K″ > 0 verified over 45 decades |
| 8 | **Cosmology** | w = −1, Ω_dm = 0.265 to the CMB, CLASS pass intact | ✅ w_DE = −1 to 4.6e-10; charge carries Ω_dm |
| 9 | **No double count** | clustered sector + phantom ≤ RAR tolerance | ✅ absent under the frame flip — one sector, counted once |
| 10 | **THE AMPLITUDE LAW** | ρ = √(GM_b a₀)/(4πGr²) as a **dynamical consequence**, not initial data | 🔴 **OPEN — and the barotropic route to it is now CLOSED** (`collapse_2026.py`) |

---

## What is explicitly NOT required

* **κ = ½ derived.** It is FITTED, measured at 0.529 ± 0.034 with four candidates inside 2σ.
  Deriving it would be a bonus, not a requirement. Requirement 2 is satisfied by the *exponent*.
* **A Theory of Everything.** No path from a₀ to the Standard Model exists in this material;
  the SM-bridge lanes are walled by a number-field obstruction. Carl publicly retracted the TOE
  claims on 2026-06-23 and this file will not reopen them.
* **Clusters.** Historically ~2× short and inherited unchanged by every mechanism. Real, but a
  known open front of the field, not a bar for this framework specifically.

---

## The one remaining question, in one sentence

> **Does the dark sector virialise at the MOND radius?**

Given σ² = GM_b/(2r_M) with r_M = √(GM_b/a₀), the profile, its coefficient and the BTFR all
follow with no freedom left. `virialisation_2026.py` proved the confinement radius is *forced*
to be ∝ r_M by a dimensional theorem with a unique solution — the sector has no galactic length
of its own (c²/a₀ = 31,112 Mpc). What is not proved is that it *settles* there.

**That is requirement 10.** `collapse_2026.py` has now closed the obvious route to it:

> **No barotropic equation of state `c_s² = c_s²(ρ)` can give both a flat rotation curve and
> the BTFR.** Flatness forces the isothermal exponent (`ρ ~ r^(-2/(s+1))` equals `r^-2` only at
> `s = 0`); `s = 0` forces `v_c² = 2σ²` with no reference to `M_b`, hence a *universal* rotation
> speed; the BTFR forbids one. Three statements about the same exponent, mutually incompatible.
> The argument never uses the kernel — only that pressure is a function of density — so no
> ghost-free choice escapes it.

**What that leaves is informative rather than fatal.** The required `σ² ∝ M_b^(1/2)` exactly,
so the sector's temperature must *know the baryonic mass* — and the only available quantity
carrying `M_b` is the baryons themselves. **The dark pressure must couple to the baryonic
field.** Every mechanism tried in this programme made the dark sector respond to *gravity*;
none made its *pressure* respond to the *baryons*. That is where requirement 10 now sits.

---

## Rules that bind both of us

1. A row moves to PASS only with a committed script that exits zero. No verbal upgrades.
2. Both footings, every number.
3. A "fails" claim is verified as rigorously as a "works" claim. Six manufactured deficits have
   already been withdrawn in this programme, and three manufactured wins.
4. Before quoting any magnitude: state *where* the rate-limiting step happens and confirm the
   formula is valid there. That single error accounts for most of the withdrawn results.
5. Nothing is published as a completed theory while row 10 is open.
