# DOOR A — does the REAL cosmic non-equilibrium supply the active MOND kernel? CLOSES, but for a NEW reason; concedes the prior band-separation argument (2026-06-26)

*Pushes the one genuinely-open input behind the active-kernel sign theorem: the closure rested on "dS supplies no
sustained drive + the active frenesy term is band-separated (super-horizon IR vs ω_orbit≈295 H₀)." DOOR A stress-tests
that against the REAL non-equilibrium universe (arrow of time, structure formation, non-stationary H(t)). Both ways:
a genuine crack in the prior reasoning is stated at full weight; the door's net status is reported honestly. sympy/mpmath
verified (`/tmp/doorA_*.py`); cosmological-dissipation primaries fetched.*

---

## VERDICT: CLOSES — but the prior "band-separated" half of the argument is WRONG and is hereby corrected. The wall is the SIGN (passivity of the in-band power), not the band.

DOOR A produces a genuine advance: it **defeats the band-separation argument** the banked closure leaned on. Structure
formation / virialization has real spectral power **AT ω_orbit** (the dynamical time IS the orbital time — they coincide
by virialization, `w_dyn/w_orb ≈ 0.48`). So "the active term is super-horizon IR, band-separated by ~295×" is **false for
the realizable in-band non-equilibrium**. That is a real correction to the prior verdict's reasoning — credited at full
weight.

**But the door still closes**, on a stronger and more honest reason: the cosmic non-equilibrium **decomposes** such that
the two requirements for an active MOND kernel are carried by **different, non-overlapping** features —

- **(R1) power AT ω_orbit** is supplied ONLY by structure formation / virialization, which is **PASSIVE-signed** (dynamical
  friction + violent relaxation = drag; the collisionless Tremaine–Hénon–Lynden-Bell H-theorem fixes coarse-grained
  `dS/dt ≥ 0`, irreversible mixing ⇒ `ρ≥0` in band ⇒ `δm = 2∫ρ/ω² > 0` ⇒ inertia RAISED ⇒ **anti-MOND**);
- **(R2) the active (gain, `ρ<0`) sign** could come ONLY from the frenetic/NESS drive, whose realizable sources (cosmic
  expansion, accretion/infall) live at **w ~ H₀**, ~110–280× **BELOW** the band, and are not coherently phase-correlated
  with an individual probe's orbit.

The active MOND kernel needs the **product** R1·R2. R1 is passive; R2 is out of band. **They never coincide.**

---

## What DOOR A genuinely cracks (full credit, corrects the bank)

The banked `ACTIVE_KERNEL_SIGNTHEOREM` and `NONEQUILIBRIUM_PASSIVITY_ESCAPE` both rested partly on band-separation:
*"particle production is a super-horizon (IR, ω≲H) phenomenon, band-separated from a sub-horizon orbital probe."* That is
correct for dS particle production — but the REAL universe's dominant non-equilibrium at galactic scales is **structure
formation**, and:

- Orbital frequency at the MOND scale: `w_orb ≈ 2.4e-16 rad/s`, `w_orb/H₀ ≈ 110` (at a=a0, ≈ 284 — matches the banked ~295).
- Galactic dynamical/virialization frequency: `w_dyn ≈ 1.16e-16 rad/s`, `w_dyn/w_orb ≈ 0.48`. **Same band.**
- This is not a coincidence: virialization sets `t_dyn ~ T_orb`. Structure formation is a **dissipative, entropy-producing,
  time-asymmetric** process (the real arrow of time, DOOR A's premise) operating **at the probe's own frequency**.

**⟹ The "band-separated" leg of the prior closure is RETRACTED.** A skeptic was right that the global super-horizon
argument doesn't cover the local galactic non-equilibrium.

## Why the door closes anyway (the SIGN wall, three independent inputs)

1. **In-band power is passive-signed (the THLB H-theorem).** Structure formation couples to an orbiting probe as
   **dynamical friction** (Chandrasekhar drag — energy removed, opposes motion) and **violent relaxation** (Lynden-Bell
   phase mixing). The collisionless-Boltzmann H-theorem (Tremaine–Hénon–Lynden-Bell 1986): any convex H decreases under
   coarse-grained mixing ⇒ `dS/dt ≥ 0` irreversibly ⇒ the in-band response is a **positive dissipator** (`ρ≥0`) ⇒
   `δm > 0` ⇒ anti-MOND. Numerically: an in-band relaxing kernel gives `δm = +9.5e16 > 0`; the MOND sign appears ONLY if
   a `ρ<0` band is **inserted by hand** (`δm = −6.6e16`).
2. **The non-stationarity (broken FDT) drive is itself out of band.** H(t) evolves on `1/H₀ ≈ 14 Gyr`; the FDT-breaking
   parametric drive sits at `w ~ Hdot/H ~ H₀`, adiabatic w.r.t. the orbit by `H₀/w_orb ≈ 0.009` (~110×). The dissipation
   (commutator) kernel of a healthy field is **state-independent** ⇒ its sign stays locked positive even out of
   equilibrium (banked Candidate-1 result, re-confirmed). FDT failure lets the **noise** grow, not the dissipation sign flip.
3. **Cosmological particle-creation dissipation is positive (fetched primaries).** The expanding-universe influence
   functional gives the expansion a **dissipative (damping) + noise** structure with positive entropy production
   (gr-qc/9403054: "dissipative term … noise term related to fluctuations of particle creation"); oscillating-condensate
   dissipation in FLRW is **decay** (energy loss, friction), requiring `ω>>H` and giving positive damping (2202.08218,
   abstract: condensate decay via the imaginary part of the retarded self-energy). No cosmological gain branch.

## The honest both-ways caveat (where a skeptic could still push)

- **GAP (real, conceded):** the THLB H-theorem governs the WHOLE system's coarse-grained entropy, which is **necessary but
  not sufficient** to fix a single probe's response `ρ≥0` (a refrigerator lowers a subsystem's entropy while raising the
  total). The patch: the inertia kernel is the probe's retarded self-energy; a relaxing bath with **no sustained in-band
  population inversion and no in-phase external power** cannot do net positive work on the probe over a cycle (2nd-kind
  perpetual motion). The galactic NESS **is** driven (accretion), but the drive is **out of band** — so at `ω_orbit` the
  probe sees an effectively undriven, relaxing, **passive** sub-bath. This patch is robust physics but is a **physical-input
  judgment** ("the realizable in-band drive is relaxational, not a coherent gain medium"), not a closed-form theorem — the
  same character as the banked caveat ("dS supplies no sustained drive"). A genuinely-active, in-band, phase-coherent
  galactic pumping mechanism would reopen it; none is known and the H-theorem argues against its existence.
- **NET:** the door's status is unchanged from "closed," but the **reason is upgraded and corrected**: band-separation was
  the wrong wall (DOOR A defeats it); **passivity of the in-band power** is the right wall. The active kernel is still
  un-sourceable from the realizable cosmos; the MOND sign must be **postulated**. Quarantine held; nothing flips on the
  empirical fronts (s^TX, a0(z)).

## One line

DOOR A **defeats the prior "band-separated super-horizon" argument** (structure formation / virialization has genuine
spectral power AT ω_orbit — `t_dyn ~ T_orb` by virialization, `w_dyn/w_orb ≈ 0.48` — a real crack, fully credited and a
correction to the bank), **but the door still closes** because the cosmic non-equilibrium **decomposes** so the two
requirements never coincide: the only IN-BAND power (structure formation) is **passive-signed** (dynamical friction +
violent relaxation; THLB H-theorem ⇒ `δm = 2∫ρ/ω² > 0`, anti-MOND; cosmological particle-creation dissipation is positive,
fetched gr-qc/9403054 + 2202.08218), while the only potentially-ACTIVE feature (the frenetic/NESS drive — expansion,
accretion) lives at `w ~ H₀`, ~110–280× BELOW the band; R1 (in-band) and R2 (active sign) are carried by non-overlapping
features and the MOND kernel needs their product — so the active MOND kernel remains **un-sourceable from the realizable
non-equilibrium universe**, the SIGN (passivity) is the wall, not the band, and the one honest gap (whole-system H-theorem
≠ subsystem `ρ≥0`) is patched by the no-in-band-coherent-drive physical input — a robust physics judgment, not a closed
theorem, exactly mirroring the banked caveat.

**Scripts (absolute):** `/tmp/doorA_spectra.py` (orbital band vs cosmic non-eq spectra; the in-band crack),
`/tmp/doorA_sign.py` (active-vs-passive sign of in-band sources; non-stationarity out of band),
`/tmp/doorA_loophole.py` (local-NESS frenesy loophole; THLB H-theorem positivity),
`/tmp/doorA_final.py` (R1/R2 decomposition table + numerical δm sign seal).
**Primaries fetched:** gr-qc/9403054 (FD relation for semiclassical cosmology — dissipative+noise, +entropy production),
arXiv:2202.08218 (FLRW condensate dissipation = decay/friction, ω>>H), 1305.0229 (dS = FDT/KMS passive bath).
**Builds on / corrects:** `real_research/ACTIVE_KERNEL_SIGNTHEOREM_2026-06.md`,
`reviews/NONEQUILIBRIUM_PASSIVITY_ESCAPE_2026-06-15.md`, `real_research/COVARIANT_MI_COMPLETION_2026-06.md`.
