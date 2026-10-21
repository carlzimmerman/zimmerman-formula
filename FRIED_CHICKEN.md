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

---

## Status 2026-10-12 (appended; the rows above are the 08-21 record and are not edited)

Current footings 9.3603e-11 / 1.1312e-10. The live picture (campaign_fresh_gravity/MECHANISM_JOINT_2026-10-12.md §5–6): cold
energy is real, gravitating mass on the one shared metric, arranged inside each bound system by its own baryons through a
nonlocal, history-driven settling (class A). The law and the supply are axioms; κ = ½ is fitted.

| # | row | status now | source |
|---|---|---|---|
| 1 | Rotation curves | ⚠️ unchanged: observed rms 0.100 / 0.101 dex on the CFG4 SPARC harness (not the intrinsic 0.06 target) | CFG663 criteria |
| 3 | Lensing tracks dynamics | ✅ galaxy scale, and now **required**: a response that does not lens is EXCLUDED (Δrms +0.155/+0.158 dex, 2000/2000 KiDS draws). 🔴 cosmic shear: the current settling rules are EXCLUDED on canonical by raw KiDS-1000 ξ± (Δχ² +68.7) | CFG663; CFG596 |
| 6 | GW170817 | ✅ on the shared-metric branch. Lean-certified (zero sorry): any sector that tilts light but not gravitons by the law's own deep tilt delays light ≥ 2.36e6 / 2.60e6 s through the Milky Way alone, from **every** sky direction, either kernel — ≥ 1.3e6 × the 1.7 s bound | CFG665 |
| 8 | Cosmology | background unchanged; 🔴 nonlinear growth on the gravitating field fails at 512³ (PAPER45 v2.2 corrected) | CFG555, CFG596 |
| 10 | Amplitude law | 🔴 OPEN, now specified: the selector must satisfy S1–S9 (reads c and the enclosed baryons nonlocally, deposits real lensing mass, silent at high g, not thermal, two-way energy exchange, frozen in mergers). No microphysics supplies it | MECHANISM_JOINT §6; CFG660, CFG661 |
| new | Substructure | NOT DIAGNOSTIC: J0946's dark solution is EXCLUDED (needs ×13 its light limit at g ≈ 10 a0); its luminous solution is CONSISTENT (law on its light 10^8.8 vs measured 10^8.9). Decider: J0946 satellite light ≳ 7e7 L☉ keeps it, < 5e6 kills it | CFG666 |

Rule 5 still binds: nothing is published as a completed theory while row 10 is open.

---

## Status 2026-10-21 (appended; earlier rows are not edited)

Footings 9.3603e-11 / 1.1312e-10 m s⁻², never pooled. κ = ½ is FITTED (measured 0.417 ± 0.095 canonical, CFG493). Cold energy is
real gravitating mass that is not a particle species. Each row restates a committed LEDGER row or a dated note of
`campaign_fresh_gravity/THEORY_CANONICAL_2026-10-18.md`; `THEORY_CANONICAL_2026-10-21_DRAFT.md` is an audited draft, not adopted.

| # | row | status now | source |
|---|---|---|---|
| 1 | Rotation curves | ⚠️ unchanged in kind: raw SPARC weighted rms about the law 0.101 / 0.099 dex with one global M/L (not the intrinsic 0.06 target). No rotating system carries an excess | CFG695; CFG919 |
| 3 | Lensing tracks dynamics | ✅ galaxy scale: lensing = dynamics at test precision, conditional on a well-posed parent; isolated blue lenses at the dwarfs' g_bar sit on the law, A = 1.016 ± 0.086 (read: within ~0.1 dex). ⚠️ cosmic shear: theory-v2 run from framework-native early-universe inputs is CONSISTENT with raw KiDS-1000 on BOTH footings (Δχ² −10.08 NC1x canonical, −9.39 NC2x alt); class ROBUST, size amplitude-driven, so quote the class, not the number; absolute fits mediocre (χ²_min 144.68 / 145.38 for 108 points); DES diagnostic and CONSISTENT for NC2x only; CMB lensing SAFE, CONSISTENT only under post-hoc A1, low power. Always stated with it: the engine that produces the pass has no established physical parent (row 10) | CFG847; CFG829, CFG840; CFG654-A2, CFG654-A3, CFG909, CFG909-NC2x, CFG917 |
| 8 | Cosmology | ⚠️ background from the framework's own BAO ruler: the native r_d (147.07 Mpc) breaks the BAO degeneracy; constant dark energy is not rejected (1.97σ, primary); Ω_k +0.011 ± 0.048; native H0 67.70 [67.09, 68.31]; BAO cannot separate the framework from ΛCDM. a0(z)/a0(0) = 0.91 / 0.94 / 0.91 at z 1 / 1.5 / 2.33 against the rival a0 ∝ H(z) at 1.76 / 2.35 / 3.49: not decidable yet (the decisive kinematic point needs ≈ 0.10 dex at z ≈ 2.5). Nonlinear growth: the zero-knob rule's 512³ failure stands for that rule; theory-v2's native shear pass is row 3, conditional. Still-shared inputs of the native run: Planck ΛCDM-chain column, H0 from θ*, massless ν, f_ret census, M2 cooling inputs, survey nuisances. The owner's damped-wave a0(z) idea is being tested (criteria frozen, no result yet) | CFG689; CFG555; CFG654-A2; CFG956, CFG957 |
| 10 | Amplitude law / mechanism | 🔴 OPEN. As a rest state the law is derived: it is the tethered medium's exact unique static ground state (under the record's assumptions). As dynamics no physical theory on the record supplies it. (a) An always-on tether whose excess is the phantom has no linear self-gravity (theorem D-T), and no local theory gives the law, a¹ growth and no EFE together; exact non-local parenthood of the class-A engine is a NO-GO. (b) Three candidate parents of that engine have been tried: the labelled-domain theory fails mergers and clusters; the source-changing theory is CONDITIONAL on galaxy scale but FAILS clusters; the relaxing-cold-dust kinetic parent is NOT CLASSIFIED by its frozen rule and, post hoc, there is NO KINETIC PARENT (the engine's relocation E8 is not the τ → 0 limit of any locally mass-conserving kinetic theory; the bath-held law profile is Bonnor–Ebert unstable, e-fold 0.21–0.25 Gyr in NGC 3198; no record-derived τ works, the excess is unreachable at any τ and the cluster-core excess survives). What worked there: exact mass and momentum conservation, no RMIN, no EFE, a¹ growth. The current engine's relocation step has no known conservative physics behind it, and the shear passes transfer to no tested parent. (c) The record's settling equation does not conserve energy; no repair that keeps the released energy inside matter brings an infall start onto the law (1-D shell toy), so a repair needs an energy sink outside the matter sector | v2 S2 (AG4), CFG935; CFG941, CFG944, CFG946, CFG947; CFG950, CFG951; CFG953, CFG954; CFG955; CFG932, CFG935 |
| new | Excess family | 🔴 OPEN, unexplained. Every system with an excess is pressure-supported and no rotator has one, but pressure support does not set the amount. Local Group dwarfs (83) +0.37 / +0.33 dex over the law (not an estimator artefact; an EFE would raise it); cluster cores ×1.91 / ×1.75 inside ~1 Mpc, real mass the law does not supply (survives the baryon census and every small reframing); Coma UDGs +0.33 dex (2.4–2.6σ, fragile); red lenses possibly a stellar-IMF effect (conditional on discs staying near Chabrier). Tidal dwarfs and NGC 1052-DF2/DF4 sit at Newton (explained only if they captured no cold energy; label-driven, not out-of-sample). No one-constant selector fits the whole family | CFG919, CFG925; CFG687, CFG922, CFG929; CFG933, CFG948; CFG926; CFG936, CFG939; CFG921, CFG928 |
| new | Gaia DR4 wide binaries (December 2026) | OPEN, waiting on data. The sealed prediction is Newtonian. Kill line restated 2026-10-21: DR4 kills it iff R − 1 ≥ max(0.01, 3σ_R), σ_R from the pairs in R; otherwise UNDECIDED (CONSISTENT unreachable). At the plan's N (~2,100 pairs in R) a full MOND-size boost is caught only ~half the time (44–47%, MOCK); reliable discrimination needs ~7,000 pairs | CFG740; CFG943; OWNER-DECISION-DR4-ALMA-1021 |
| new | ALMA U4_27928 (2026-11-06), GS4_24110 (2026-11-28) | OPEN, waiting on data. The original frozen CFG806-U4 / CFG809 plans govern; the clarifications and addenda were filed before any data; one disc excludes no model. Forecast S/N is low for both, so an upper limit is the likely outcome. Per CFG809 clarification addendum A, GS4 CAN return a ROBUST framework verdict on most branches (15–17 of 20 CI21 values on the six non-FLOOR branches) | CFG571, CFG806-U4, CFG809, CFG942, CFG942-1021, CFG942-ADDENDA-BCD; OWNER-DECISION-ALMA |

Rule 5 still binds: nothing is published as a completed theory while row 10 is open.
