# FRIED CHICKEN — the requirements

> ## ⚠️ WHAT THIS FRAMEWORK IS, LABELLED HONESTLY
>
> In the frame-flip configuration that clears nine of these ten rows, **ρ_halo is an
> independent, self-gravitating mass density** with its own equation of motion, sourcing the
> metric through T_μν and carrying Ω_dm = 0.265 to the CMB. **That is a dark sector.**
>
> `dark_sector_honesty_2026.py` tested the alternative and it fails: the `g_b, ∇g_b`
> construction **cannot** arise from a local covariant action whose field equations contain no
> independent dark density. It requires `Φ''`, its Ostrogradsky Hessian is `6u₁³/u₂⁴` — nonzero
> everywhere on the support, hence **non-degenerate** — and the Euler–Lagrange equation comes
> out **fourth order** with a ghost. It is not polynomial in `Φ''` and cannot be arranged into
> the Galileon/Horndeski/DHOST degenerate class.
>
> **Honest label: a dispersion-supported dark sector.** Not modified gravity. Not
> dark-matter-free.
>
> **The dichotomy is clean and the framework must pick a horn.** No independent dark density
> ⟹ modified gravity ⟹ dies on the arm-level Cassini quadrupole (4.8–8.9× the ceiling, proved
> carrier-independent). Survives Cassini ⟹ has an independent dark density ⟹ is a dark sector.
>
> **What survives intact:** a₀ = κc√(Gρ_Λ), both published papers (neither claims to be
> dark-matter-free), and the corpus's standing slogan **"no dark-matter *particle*"** — the
> carrier is a field, and a field is not a WIMP. That distinction is untouched.
>
> **Do not say from now on:** that this framework is dark-matter-free, that it has no dark
> matter in galaxies, or that the halo is "phantom" in the frame-flip picture. Phantom language
> belongs to the modified-gravity horn only, where there is no independent density to be
> phantom about.

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
| 6 | **GW170817** | \|c_T/c_γ − 1\| < 7e-16 | ✅ **structurally absent** under the frame flip — but see the banner: that is bought by being a dark sector |
| 7 | **Theoretical health** | no ghost, no gradient instability, no Cherenkov | ✅ K″ > 0 verified over 45 decades |
| 8 | **Cosmology** | w = −1, Ω_dm = 0.265 to the CMB, CLASS pass intact | ✅ w_DE = −1 to 4.6e-10; charge carries Ω_dm |
| 9 | **No double count** | clustered sector + phantom ≤ RAR tolerance | ✅ absent under the frame flip — one sector, counted once |
| 10 | **THE AMPLITUDE LAW** | ρ = √(GM_b a₀)/(4πGr²) as a **dynamical consequence**, not initial data | 🔴 **OPEN — every route avoiding an inserted global scale has now failed** (`collapse_2026.py`, `baryon_coupled_pressure_2026.py`, `local_selection_2026.py`) |

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

**And the baryon-coupled repair has now been tested too, and the no-go is class-wide.** The
unique local length built from the baryonic field is `g_b/|∇g_b| = r/2`, giving
`c_s² = a₀ g_b/|∇g_b|` — which at `r_M` equals `√(GM_b a₀)/2` **exactly, coefficient and all.**
The right temperature really *is* a₀ times the radius where `g_b = a₀`. But used as a *law*
rather than a boundary condition it fails: the hydrostatic balance's two sides differ by exactly
one power of `r` for every density exponent. And solving for the sound-speed profile that
supports a flat curve returns `c_s² = C₁r² + v_c²/2`, whose **unique bounded branch is a
constant**.

> **The amplitude law cannot arise from any local equation of state** — not barotropic
> `c_s²(ρ)`, not baryon-coupled `c_s²(g_b)`, not any `c_s²(r)` whatever. Flatness demands a
> *uniform* temperature, and no position-dependent law supplies one.

**So requirement 10 is a formation question, not an equation-of-state question.** The
temperature must be uniform with its value set globally — a₀ times the radius where the
baryonic field equals a₀ — which says the sector thermalised in the region `g_b > a₀` and kept
that virial temperature. That is collapse history: multi-streaming, caustics, violent
relaxation. **It is the one route this programme flagged twice as unrun and never ran**, both
attempts having errored out.

### The obstruction, stated cleanly rather than rescued

`local_selection_2026.py` ran the test properly: derive the general hydrostatic system first,
pin the hypotheses, then ask whether a **local covariant** rule can select the temperature
**without inserting M_b, r_M or the BTFR**.

**Hypotheses, now exact.** Asymptotic flatness + self-gravity dominance + **boundedness of
c_s²** force `c_s² = v_c²/2`. The general solution is `c_s² = 2πGC + C₁r²`; drop boundedness
and the `r²` mode survives, drop flatness and nothing is forced. Three hypotheses, no more.

**A genuine local invariant exists**, and this was not obvious:
`g_b³/|∇g_b|² = GM_b/4` **exactly and r-independently**, so
`σ² = √(a₀ g_b³)/|∇g_b| = √(GM_b a₀)/2` — the right temperature, coefficient and all, from
local field data with no global integral. Exact for a point mass *and* for Hernquist.

**And it fails the extended-baryon test.** That r-independence is a property of the
`g_b ~ 1/(r+a)²` family, not a general fact. For an **exponential disk** the invariant varies
by **1.41×** across 0.5–3 r_M; Plummer varies by 1.19×. There is no single local value for a
theory to select. It lands within 13% of target *at r_M* — but "at r_M" is exactly the global
input the test forbids.

> **No-go: the amplitude law is not derivable from a local equation of state, from a local
> baryon-coupled pressure, or from a local covariant selection rule on realistic baryons.
> Every route that avoids inserting a global scale has failed; every route that succeeds has
> inserted one.**

This supersedes the optimism of `caustics_2026.py`, which rescued the law by *assuming* collapse
halts at r_M — an inserted global scale, not a mechanism.

---

## Rules that bind both of us

1. A row moves to PASS only with a committed script that exits zero. No verbal upgrades.
2. Both footings, every number.
3. A "fails" claim is verified as rigorously as a "works" claim. Six manufactured deficits have
   already been withdrawn in this programme, and three manufactured wins.
4. Before quoting any magnitude: state *where* the rate-limiting step happens and confirm the
   formula is valid there. That single error accounts for most of the withdrawn results.
5. Nothing is published as a completed theory while row 10 is open.
