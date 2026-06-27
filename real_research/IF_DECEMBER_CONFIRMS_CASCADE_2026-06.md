# IF DECEMBER CONFIRMS — Conditional Consequence Cascade

**Status banner (read first, applies to every line below):**

> **CONDITIONAL. This document assumes the two December-window tests confirm. It is NOT a claim
> that they have, will, or are likely to.** Every clause is "**IF** the data confirms, **THEN** ...".
> The data is **not asserted**. Both named tests currently have **null/underpowered or
> non-diagnostic** real-data status (recorded below). This is a contingency *map* — deployable the
> day the data lands — not a present verdict. No IF→IS slide anywhere.

**Framework as subject.** Inertia = a body's nonlocal-in-time response to the de Sitter cosmic-horizon
Unruh bath; that bath carries one clock, the de Sitter rate H_Λ, fixing **a₀ = cH_Λ/Z = 9.36×10⁻¹¹
m/s²**. The framework uses **its own interpolation** g_obs = √(g_bar² + g_bar·a₀) — **never McGaugh's ν**.
It is **modified INERTIA with a horizon-derived a₀**, NOT a MOND variant; reason from its own premises first.

The two December-window gates:
- **(A) Gaia DR4** (2 Dec 2026): dwarf y-contrast — diffuse plunge-orbit dwarfs run hotter at matched
  pericenter+mass. Carriers Crater II (y=3.28), Antlia II (y=2.55) vs adiabatic controls Fornax/Sculptor
  (y<0.3). MG-impossible. DOI 10.5281/zenodo.20949773.
- **(B) DESI DR3** (2026–27): a₀(z) DECLINING ~√ρ_DE, −26% by z=3, opposite-signed to McCulloch-rising
  and Milgrom-flat.

All numbers below were re-derived this session (clean-room scripts) and match the banked corpus
(`reviews/desi_a0z_loop_CLOSED.py`, `DATA_GATE_PREREGISTRATION_2026.md`, `DWARF_ECC_SIGMA_PILOT_2026-06.md`).

---

## 1. IF Gaia DR4 confirms the dwarf y-contrast

**The condition (precise).** A positive carrier-vs-control σ excess at matched pericenter+mass:
the diffuse plunge-orbit carriers (Crater II y=3.28, Antlia II y=2.55) running internally hotter than
adiabatic controls (Fornax/Sculptor y<0.3), surviving an explicit tidal-heating control.

### THEN it ESTABLISHES
1. **Modified INERTIA is real — not modified gravity.** A history-dependent, time-nonlocal inertial
   response is *detected*. This is the framework's core premise getting its **first positive
   confirmation**; until now it only *rode* the MOND-vs-ΛCDM premise it shares with everyone.
2. **The bath-clock time-nonlocality is OBSERVED.** Inertia reads the history-averaged acceleration —
   the single clock 1/H_Λ imprinting on internal dynamics — exactly as Milgrom-1994's no-go (any MI
   must be time-nonlocal) demands.
3. **The discriminating axis is the diffuseness-gated y = ω_ext/ω_internal**, confirmed *per object*
   from DR4 proper motions, not statistically inferred.

### THEN it FALSIFIES (by theorem) the entire modified-GRAVITY class at this front
Every metric/field MOND — AQUAL, QUMOND, AeST (the framework's *own* only covariant home) — has an
**instantaneous** external-field effect (Milgrom 2022, verbatim: internal dynamics "depend only on the
momentary value of a_ex"), so they predict **exactly zero** σ-vs-history correlation at fixed pericenter
**for any a₀**. ΛCDM likewise predicts zero (a circular and a radial subhalo at matched radius have
identical internal dynamics modulo tidal history — the *controlled confound*, not the signal). A
nonzero positive correlation is **required by the framework and impossible for all of them.** This
joins the Cassini bound as a clean MI-vs-MG discriminator.

**Both-ways (recorded in the preregistration):** the KILL side is also live. A hard null — or a
*negative* correlation surviving the tidal control — at DR4 precision counts **against** the framework's
MI content.

### THEN it PINS θ(y) — the program's single open free function
The measured boost B inverts off the framework's own deep-MOND scaling σ ~ θ_eff^(1/4) at the y=1
reference (θ(1)=1, Milgrom-normalized):

> **θ(0) = (1 + B)⁴**   (clean-room, reproduced this session)

| measured boost B | θ(0) = (1+B)⁴ | reading |
|---|---|---|
| +15% | **1.75** | shallower than every Milgrom example kernel; weak-memory |
| +19% | **2.01** | the rational 2/(1+y²) edge |
| +22% | **2.22** | inside the banked [2, e] window |
| +28% | **2.68** | the e^(1−y) edge; strong-memory |
| >+32% | **>3.0** | steeper than e^(1−y) |

The two carriers at **different y** (3.28, 2.55) sample θ at two points, so the Crater−minus−Antlia gap
additionally constrains the kernel **shape**/decay-rate q = 1/ln(θ₀). (Caveat: carrier-vs-control
magnitudes for y>1 use θ extrapolated *below* 1, so shape is looser than the robust θ(0) amplitude pin.)

### THEN the next-prediction (one kernel → correlated downstream)
Because it is **one kernel across all observables**, pinning θ(0) collapses the cluster member σ-spread
from its banked factor-~2 band to a **single number**. Adopting the pinned exp-family θ(y)=θ(0)^(1−|y|),
cluster infall reach y~0.5 gives σ_plunge/σ_circ = θ(0)^(1/8):

| dwarf boost B | θ(0) | predicted cluster member σ-spread |
|---|---|---|
| +15% | 1.75 | +7.2% |
| +19% | 2.01 | +9.1% |
| +22% | 2.22 | +10.5% |
| +28% | 2.68 | +13.1% |

This **reproduces the banked 6–13% band as a cross-check**, now as a *correlated* prediction off one
measured number — testable on resolved diffuse/UDG cluster-member kinematics. Second over-determining
test: measuring Crater II and Antlia II **separately** must yield Crater > Antlia with a gap set by the
**same q** — a falsifiable consistency check beyond the single amplitude. (The LG MW–M31 timing-orbit
memory boost is likewise pinned, scaling as (ln θ₀)². **s^TX SME dipole and a₀(z) do NOT ride θ(y) and
are NOT sharpened** — stated, not oversold.)

### HONEST current status (NO IF→IS slide)
The pre-registered pilot — 24 real MW dwarfs (Pace/Erkal/Li 2022, Gaia EDR3) — is an explicit **NULL at
near-zero power**: primary partial Spearman ρ(σ, ecc | r_peri, mass, r_half) = **−0.196, p = 0.395**,
slightly the *wrong* sign, robust to a tidal control. Only **2 of 24** dwarfs reach the carrier band; the
carrier per-object σ errors (~10–40%, largest on the carriers) are at or above the signal. **Existing
data cannot test this yet.** This is a null with almost no power — not a hint, not a strike.

---

## 2. IF DESI DR3 confirms a₀(z) declining

**The condition (precise).** DESI DR3 confirms (i) evolving dark energy AND (ii) the DECLINING sign of
a₀(z) tracking √ρ_DE — i.e. a confirmed decline at z≥2. All numbers below are from
`reviews/desi_a0z_loop_CLOSED.py` (DESI DR2 DESY5 CPL w0=−0.752, wa=−0.86) and an independent recompute
this session; they match exactly.

### THEN it ESTABLISHES
1. **a₀ tracks the dark-ENERGY density specifically** — the surface-gravity-of-ρ_DE reading
   a₀ = (c/2)√(G ρ_DE) = c²√(Λ/32π), **NOT** a₀ = cH(z)/Z with ρ_total. This resolves the long-standing
   ρ_DE-vs-ρ_total fork (the 9.36 vs 11.3 ×10⁻¹¹ / √Ω_Λ≈1.21 gap) **in favor of the √ρ_DE branch**:
   the two forms agree at z=0 but diverge in the past (ρ_total rises as matter (1+z)³; ρ_DE *declines*
   in the phantom past). **A measured decline can only come from the ρ_DE branch.**
2. **The horizon origin of a₀ gains direct support** — a₀ follows the instantaneous dark-energy/vacuum
   scale, the same Λ that sets the horizon temperature, exactly as the dS-Unruh MI premise requires.
3. **a₀(z) is promoted** from a passive consistency check into a genuine galaxy-scale **probe of
   dark-energy evolution** — the same formula DESI tests with BAO, read through galaxy dynamics.

Footing locked: a₀(0)=9.36×10⁻¹¹, framework's own interpolation, never McGaugh ν; **a₀(0) stays a
multiplicative INPUT in every ratio — DESI fixes the SHAPE, not the anchor** (quarantine intact).

### THEN it FALSIFIES three rivals (recomputed this session)
At a confirmed z≥2 decline:
1. **McCulloch Quantized Inertia** (a₀ ~ 2c²/Θ, Θ = Hubble horizon → a₀ ~ cH(z) **rising**): predicts
   a₀(z)/a₀(0) = +32% (z=0.5), +79% (z=1), +203% (z=2), +357% (z=3) — **opposite sign**. A confirmed
   z≥2 decline **excludes QI outright.** Cleanest kill: QI and the framework *share* the dS/Unruh-horizon
   motivation but split on horizon CHOICE (Hubble/ρ_total vs de Sitter/ρ_DE) — the z≥2 sign is the
   decisive discriminator between the two readings.
2. **Milgrom-vacuum / a₀ ~ √Λ with Λ a true constant**: predicts **flat 1.000** at all z. Falsified by
   any confirmed evolution. (NB: this is the framework's *own* w=−1 limit — so confirming evolution
   distinguishes the framework's dynamical-DE branch from the static-Λ reading it reduces to if DESI's
   signal evaporates.)
3. **Constant-a₀ standard MOND**: also flat 1.000 — falsified by confirmed evolution.

**Both-ways caveat (honest):** the rising rivals are *already* disfavored on current clean data
(Δχ² = +17 and +38 vs framework; Milgrom 2017 and McGaugh 2024 independently exclude rising a₀~cH₀).
DESI z≥2 confirmation would **clinch** an exclusion that already leans — not create it from scratch.
And **MUSE-DARK III (Ciocan+2026)'s RISING slope is NOT a counter-falsification**: it is intermediate-z
(z<1.4), high-acceleration (g≳a₀, where V⁴/GM_bar overestimates a₀), and ΛCDM-assembly-degenerate
(Mayer+2023 ~+32% apparent drift) — apparent, not fundamental.

### THEN the new consequences (all conditional, all reproduced this session)
- **(a) Phantom-divide BUMP** — the next sharp target. Phantom crossing w(z)=−1 sits at **z_c = 0.405**
  (DESY5); ρ_DE peaks 1.127× there, so a₀(z) rises to a **non-monotonic peak of +6.15% at z=0.405**, then
  declines. This rise-then-fall locked at the *measured* w=−1 crossing is unique-in-SHAPE: flat MOND
  (0%), QI (monotone rising), and ΛCDM (flat fundamental a₀) **cannot** produce it. In the ratio,
  κ/c/Z/interpolation all cancel → **shape is parameter-free given DESI's w(z)**, a₀(0) only multiplicative.
- **(b) High-z deep-MOND BTFR SIGN** — the genuine OUTPUT test (vs DESI→a₀(z) being partly a consistency
  check on the ρ_DE INPUT). dlogV = ¼ dlog a₀, so at z=3 the framework predicts V_flat **−0.033 dex
  (−7.3%) BELOW** the local BTFR zero-point — while constant-MOND/QI sit at/above it. The **sign** of the
  z≥2 deep-MOND BTFR offset (below local) is the framework-distinctive output discriminator.
- **(c) Observable magnitudes:** bump +6.15% a₀ → +1.50% V_flat, +3.03% RAR g_obs. z=3: −26.3% a₀ →
  −7.34% V, −13.8% g.

This **constrains the fork to ρ_DE** (kills cH(z)/Z packaging as fundamental). It does **NOT** pin θ(y) —
that is §1's job. a₀(z) probes the **amplitude law** a₀(ρ_DE), not the interpolation **shape**.

### THEN the preregistered prediction set (declining branch)
1. a₀(z)/a₀(0) declines monotonically past the bump: **1.059 (z=0.5), 1.009 (z=1), 0.862 (z=2),
   0.737 (z=3)** for DESY5; robust across all four DESI DR2 SN combos (z=3 spans **0.63–0.78, ALL <1,
   ALL declining**).
2. Non-monotonic **+6.15% bump peaked at z_c=0.405** (the w=−1 crossing); sign(+) and low-z location
   (z~0.30–0.44) robust across DR1/DR2 combos.
3. z=3 deep-MOND BTFR offset = **−0.033 dex (−7.3% V)** below local zero-point.

### HONEST current status (NO IF→IS slide)
a₀(z) is **non-diagnostic now** and **dissolves if w→−1** (DESI's signal could evaporate; the framework
then reduces to its own static-Λ flat limit). The bump is **below-floor for direct galaxy kinematics**:
+1.50% in V vs a ~3–15% BTFR systematic floor (~2–10× below), and the ΛCDM assembly drift (~+32% at
z=0.4, Mayer+2023) is ~5× larger and same-signed at the bump. The clean target is the **z≥2 sign**, not
the bump amplitude. a₀(z) is **hostage to w(z).**

---

## 3. The JOINT upgraded standing (IF BOTH confirm)

| Front | Before (today) | IF Gaia DR4 confirms | IF DESI DR3 confirms | IF BOTH |
|---|---|---|---|---|
| MI premise (time-nonlocality) | rides shared MOND premise | **directly detected** | — | **detected** |
| MI-vs-MG discriminator | Cassini only (in hand) | **+ dwarf y-contrast** | — | two independent MI-vs-MG discriminators |
| a₀ origin (horizon/ρ_DE) | posited, fork open | — | **ρ_DE branch selected; horizon origin supported** | a₀ both *time-nonlocal* (DR4) AND *ρ_DE-tracking* (DESI) |
| θ(y) kernel | free function, factor-~2 | **pinned: θ(0)=(1+B)⁴** | — | **pinned** + correlated cluster prediction |
| Rivals killed | rising-a₀ leaning out | metric/field-MOND + ΛCDM (this front) | QI, Milgrom-flat, const-MOND | the framework stands ~alone among MI/MG/CDM on these two fronts |

**The joint upgrade in one line:** the framework's two *independent* distinctive claims — inertia is
**time-nonlocal** (DR4) and a₀ tracks **ρ_DE specifically** (DESI) — would each get a first positive
confirmation, on orthogonal physics (local dwarf kinematics vs cosmological DE evolution), with the DR4
boost **pinning the single free function θ(y)** that then makes a **correlated, falsifiable cluster
prediction**. That is a coherent, distinctive, multi-front MI theory — not a fit.

### Next-gen prediction set (deployable post-confirmation)
- θ(0)=(1+B)⁴ → cluster member σ-spread = θ(0)^(1/8) at y~0.5 (resolved UDG/diffuse cluster members).
- Crater II > Antlia II σ-ordering with gap set by the same q (over-determining consistency test).
- z=3 deep-MOND BTFR offset −0.033 dex below local (high-z disc kinematics, ELT era).
- Phantom-divide +6.15% a₀ bump at z_c=0.405 (precision RAR/BTFR campaigns; below floor today).
- LG MW–M31 timing-orbit memory boost, pinned by (ln θ₀)².

### Follow-up papers (each is "IF X then Y", not a claim)
1. *"θ(y) pinned: the inertia memory kernel from the Gaia DR4 dwarf y-contrast"* — inversion +
   correlated cluster prediction.
2. *"a₀ tracks dark energy: the DESI DR3 declining-a₀(z) confrontation"* — fork resolution + QI/flat-MOND
   exclusion + phantom bump.
3. *"Two-front modified-inertia: joint time-nonlocality and ρ_DE-tracking"* — the joint standing, with the
   honest walls (§4) stated up front.

---

## 4. HONEST LIMITS that hold EVEN IF BOTH confirm

These are **not** dissolved by confirmation. State them up front, every time:

1. **The SM stays WALLED → NOT a TOE.** Confirmation tests the *gravitational/inertial* sector. The
   framework still **derives no Standard Model**: the FDR wall holds, there is **no forced Yukawa
   kernel** (the cosmology trick does not transfer — gravity forces √(8π/3); the Yukawa sector has no
   forced kernel), m_p/m_e is not derivable, and the one real particle lead (Koide Q=2/3) the framework
   only **re-labels**. It remains a **one-parameter effective theory at a frontier**, not a theory of
   everything.
2. **Z stays a POSIT → one-parameter.** a₀ = cH_Λ/Z = 9.36×10⁻¹¹ is a **forced SCALE with a FREE O(1)**.
   The dwarf y-contrast tests the **time-nonlocality** (the MI premise); the a₀(z) shape tests the
   **amplitude law** a₀(ρ_DE) — **neither pins the NORMALIZATION value**, which stays
   convention-degenerate (7.5×10⁻¹¹..1.8×10⁻¹⁰ across interpolation × M/L) and **non-diagnostic**. The
   κ-forcing door is *provably* closed; a₀'s value is not derived. (The SPARC RAR a₀ is
   convention-COMPATIBLE and non-diagnostic both ways — never a manufactured deficit *or* win, and never
   via McGaugh's ν.)
3. **The θ(0) inversion's SHAPE leg is extrapolation-sensitive.** Milgrom fixes only θ(1)=1
   (decreasing, θ(0)~few); θ below 1 (for y>1) is unverified in form. The **robust pin is θ(0) from the
   amplitude**; the q/shape is **looser**. θ(y) becomes *pinnable*, **not derived**.
4. **Tidal heating is a real confound** that must be explicitly modeled. The carriers are tide-clean by
   large pericenter (24/38 kpc) by construction, but the population test demands explicit tidal control.
5. **Confirmation selects MI over MG/CDM, not the framework UNIQUELY.** A positive y-contrast picks MI at
   the *premise* level; other preferred-frame/MI completions also predict a positive contrast. The
   framework is then the *most economical* such completion (one parameter, horizon-derived a₀), not the
   *only* one.
6. **a₀(z) is hostage to w(z).** If DESI's evolving-DE signal evaporates (w→−1), the distinctive a₀(z)
   front dissolves and the framework reduces to its own static-Λ flat limit — indistinguishable there
   from constant-a₀ MOND on this axis.

**Doors remain open (never "no doors"):** θ(y) is now *pinnable but not derived*; the covariant MI
completion's exact 3-horn trichotomy stays blocked (MOND sign + Z postulated); the a₀(z) decline is the
separate distinctive front and is w(z)-hostage; the SM bridge induces but derives nothing. The forward
program is **data**, not re-opening closed theory doors.

---

## One-line summary
**IF** December delivers both — the Gaia DR4 dwarf y-contrast (MI real + metric-MOND/ΛCDM killed at this
front + θ(0)=(1+B)⁴ pinned) and the DESI DR3 declining a₀(z) (a₀~ρ_DE selected + QI/Milgrom-flat/const-MOND
killed) — **THEN** the framework gets its first two independent positive confirmations on orthogonal
physics and its single free function pinned; **EVEN THEN** the SM stays walled (not a TOE) and Z stays a
posit (one-parameter). **None of this is asserted — it is the map of what would follow, deployable the
day the data lands.**
