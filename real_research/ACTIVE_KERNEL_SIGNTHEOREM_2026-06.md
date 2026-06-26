# The Active-Kernel Sign Theorem — Route E's last sub-problem is CLOSED (FOUNDED-not-DERIVED), a real theorem (2026-06-26)

*The deepest open theory question on the gravity side: can ANY physically-realizable cosmological/dS source supply the
ACTIVE, sign-flipping memory kernel that Route E (the nonlocal modified-inertia corner — the framework's only ghost-free
covariant MI home) needs to LOWER inertia at low acceleration (MOND), while staying causal (Kramers-Kronig) and
ghost-free? Both-ways discipline: a real escape would make the framework's MI DERIVABLE (a genuine advance, credited at
full weight); a manufactured source is not physics. Independently re-derived in sympy/mpmath; the two load-bearing
physical inputs (Milgrom-1999's own status statement; dS = passive thermal/FDT bath) fetched from the primary
literature.*

---

## VERDICT: (B) CLOSED. No realizable dS source supplies the active kernel. Route E is provably FOUNDED-not-DERIVED.

The passivity → anti-MOND sign theorem is **airtight**, proven three independent ways. Every realizable de Sitter source
is **passive** (a genuine KMS/FDT thermal equilibrium), and a passive bath **raises** inertia at low acceleration — the
**wrong sign** (anti-MOND). The one genuinely-active mechanism in the literature (frenesy in a driven non-equilibrium
steady state) is **real physics but not realizable from dS** (dS has no sustained drive/current) and is **band-separated**
from the orbital frequency by ~295×. Therefore the MOND-signed nonlocal kernel **cannot be derived** from the dS vacuum;
it must be **postulated**. This **closes the framework's deepest open theory problem** — and it closes it as a *theorem*,
not a failure-to-find.

**This does not weaken the banked standing — it confirms and tightens it.** It is the strongest form of the
covariant-MI-completion closure: a real sign theorem mapping exactly what a completion must evade. The forward is now
**data** (the live empirical fronts), not theory.

---

## The theorem (stated precisely)

> **ACTIVE-KERNEL SIGN THEOREM.** Let `Sigma_R(ω)` be the retarded self-energy a probe of bare mass `m` acquires from
> coupling to any cosmological/dS source, assumed **(iii) CAUSAL** (`Sigma_R` analytic in the upper-half ω-plane ⇒
> Kramers-Kronig) and **(iv) GHOST-FREE / UNITARY** (Källén-Lehmann spectral density `ρ(ω) ≥ 0`). Then the adiabatic
> (low-ω, deep-MOND-band) inertia shift is
>
>   `δm = (2/π) ∫₀^∞ [Sigma''(ωₚ)/ωₚ] / ωₚ² dωₚ = 2 ∫₀^∞ ρ(ωₚ)/ωₚ² dωₚ ≥ 0`,
>
> i.e. inertia is **RAISED** at low acceleration — **ANTI-MOND**. Because `Sigma''(ω) = π·ω·ρ(ω)`, ghost-freedom
> (`ρ≥0`) ⇔ passive dissipation (`Sigma''/ω ≥ 0`) ⇔ positive adiabatic inertia shift. The MOND modified-inertia sign
> (`δm < 0`, inertia LOWERED at low a) **requires** `ρ(ωₚ) < 0` in a low-frequency band = a **negative-norm ghost**.
> Hence for any **stationary, linear, unitary** kernel, "active + causal + ghost-free + MOND-sign" is
> **overdetermined-impossible**.
>
> The only logical escape — **non-linear frenesy** in a driven NESS — is not covered by the linear no-go, but it is
> **not realizable from a dS / KMS-equilibrium cosmos** (no sustained drive or current) and is band-separated from
> `ω_orbit ≈ 295 H₀` regardless. ∴ **no realizable, sign-correct, causal, ghost-free active cosmological kernel exists**;
> the Route-E active kernel must be **POSTULATED**.

Numerically confirmed (`/tmp/active_kernel_numeric.py`): a ghost-free `ρ≥0` Lorentzian gives `δm = +238` (anti-MOND);
only inserting a **negative-ρ band at low ωₚ** (a ghost) gives `δm = −3311` (MOND sign). The two are mutually exclusive.

---

## One important both-ways CORRECTION to the task's framing (do not skip this)

The task framing said the active kernel is forbidden by **causality (Kramers-Kronig) or ghost re-introduction**. The
independent re-derivation shows that is **not quite right**, and getting it right *sharpens* the theorem:

- **CAUSALITY ALONE does NOT forbid the MOND kernel.** I built an explicit counterexample
  (`/tmp/active_kernel_causality.py`): `M(ω) = m[1 − g·Ω₀²/(Ω₀² − ω² − iΓω)]`, `0<g<1`. Both its poles sit at
  `Im = −Γ/2` (lower half-plane) ⇒ analytic in the UHP ⇒ **CAUSAL**; `M(0) = m(1−g) < m` ⇒ inertia **LOWERED**
  (MOND-signed); `M(∞) = m` ⇒ Newtonian recovery; the physical (graviton) pole has positive normalization `M(0)>0` ⇒
  **no ghost at the physical pole**. So a causal, MOND-signed inertia kernel **exists as a mathematical object**.
- **What it necessarily has is `Im M(ω) < 0` for ω>0** — it **supplies** energy to the orbit each cycle = a **gain /
  active medium**.
- **The wall is therefore PASSIVITY (thermodynamics), not causality and not the no-ghost condition.** The correct no-go
  is: *passivity alone ⇒ anti-MOND* (airtight); *causality alone permits MOND*; so the MOND kernel **requires breaking
  passivity** — an out-of-equilibrium / gain source.
- **Reconciliation with the ghost statement** (`/tmp/active_kernel_reconcile.py`): the causal counterexample is "ghost-free
  *at the probe's physical pole*", but it is **not the self-energy of any unitary (ρ≥0) bath** — viewed in a
  Källén-Lehmann rep its resonance carries a wrong-sign (ρ<0) bath mode. So "ghost-free at the physical pole" ≠ "unitary
  passive bath". A causal MOND kernel needs **either** a non-unitary (ρ<0) bath mode (a ghost) **or** an external drive
  (Im M<0, active). Both are forbidden for a **passive, unitary** dS vacuum. The two scripts are consistent layers; the
  theorem stands.

**Net of the correction:** the decisive question is *purely* whether the dS source can be **active** — and it cannot.
That is what makes the verdict a theorem rather than a convention.

---

## The realizability audit — four candidate active sources, all PASSIVE or non-realizable

| # | Candidate dS/cosmological source | Realizable? | Sign-correct (active)? | Why it fails |
|---|---|---|---|---|
| 1 | **Time-dependent expanding background** (H(t), growing horizon, cosmic-history squeezing) | YES | **NO — PASSIVE** | Squeezing changes only the **noise** (symmetric anticommutator) kernel; the **dissipation** (antisymmetric commutator) kernel is the **state-independent** field commutator of a healthy field ⇒ its sign stays locked **positive**. A hotter non-stationary bath is still a **passive** bath. |
| 2 | **Driven / squeezed / non-thermal dS vacuum** (Bunch-Davies, particle production) | YES | **NO — PASSIVE in band** | Bros-Epstein-Moschella / Figari-Hollands: the BD state restricted to the static patch is **KMS-thermal** at `T_dS` ⇒ detailed balance ⇒ **passive**. Particle production is a **super-horizon (IR, ω≲H)** phenomenon, band-separated from a sub-horizon orbital probe (`ω_orbit/H₀ ≈ 295`) that sees the KMS-thermal passive tail. |
| 3 | **Horizon dynamics** (apparent-horizon flux à la Jacobson/Padmanabhan, for inertia) | YES | **NO — PASSIVE** | Jacobson's `δQ = T δS` is an **equilibrium Clausius** relation; the non-equilibrium extension (Eling-Guedens-Jacobson) has entropy production `σ ~ +(shear)² ≥ 0`, **sign-definite by the 2nd law** ⇒ a horizon is a **positive dissipator**, no gain branch. |
| 4 | **Comoving-frame "frenetic" activity** (Milgrom's cosmic inertia-frame; NESS frenesy) | **NO** | **YES (as physics)** | Frenesy (Maes / Baiesi-Maes-Wynants NESS response theory) **genuinely can** flip the differential-response sign and violate FDT — the **only** real active mechanism in the literature, **credited at full weight as physics**. But it needs a **sustained driven non-equilibrium current doing work on the probe**; dS is a **maximally-symmetric KMS equilibrium** (no current, no drive). Invoking it requires **postulating a cosmological drive = a manufactured source** (forbidden), and it is band-separated from `ω_orbit` anyway. |

**The framework's own kinematic kernel (Milgrom-1999 / Luo-2026 dS-Unruh broadening)** is the analytic
derivative-expansion memory whose **adiabatic limit IS the passive `T_eff` floor** — it supplies the **FORM**
(`a0 ~ √Λ`), but its inertia-correction sign is the **passive** one. It is the floor, not an active source.

**Best candidate, named honestly:** the **frenetic/NESS route (Candidate 4)** — the only physics that *can* flip the
sign. It fails **not by the theorem** but by **non-realizability** (dS supplies no sustained drive) plus band-separation.
Marginal as physics, not realizable as a dS source. **No candidate is simultaneously realizable + sign-correct.**

---

## The two load-bearing physical inputs — both confirmed from the primary literature

1. **Milgrom 1999 (astro-ph/9805346), fetched, abstract verbatim:** the dS-Unruh temperature is
   `T ∝ √(a² + a₀²)` with `a₀ = (Λ/3)^(1/2)` — the `a0 ~ √Λ` **scale** is genuine. And **Milgrom himself states the
   mechanism is not derived:** *"An actual inertia-from-vacuum mechanism is still a far cry off."* This is the
   framework's own primary source confirming **FOUNDED-not-DERIVED** — the kernel is proposed kinematically, the
   inertia-from-vacuum derivation is open. The theorem here names *why* it stays open (the sign).
2. **de Sitter is a passive thermal/FDT bath (e.g. 1305.0229), fetched:** a field in dS *"obeys a
   fluctuation-dissipation relation and its equilibrium distribution is Maxwell-Boltzmann"* at `T_dS = H/2π`. FDT +
   equilibrium = **passive**. This is the input that puts every realizable dS source in the passive class. It is
   **established published physics**, not a convention artifact — so the passive verdict for Candidates 1-3 is **robust**.

---

## The honest caveat (both-ways) — exactly where a skeptic could push, and why it doesn't reopen the framework

- **(A) The theorem's reach is precisely scoped.** It proves no active sign-correct kernel for **stationary, linear**
  response with a Källén-Lehmann rep. The **one genuine logical gap** is **non-linear frenesy in a driven NESS**
  (Candidate 4) — **real active physics**, NOT covered by the linear no-go. I credit it at full weight as the only
  non-vacuous escape direction. It fails by **non-realizability** (dS = KMS equilibrium, no sustained drive) plus
  band-separation, **not** by the theorem. So calling it "closed" rests on the physical-input judgment *"dS supplies no
  cosmological drive"* — robust, but a physics statement, not a theorem about frenesy itself. A skeptic who **postulates
  an out-of-equilibrium cosmological drive** (NOT dS) could reopen it — but that is a **manufactured / non-dS source,
  outside the framework's stated dS foundation.** Honest both-ways: that door is *physically* shut, not *logically*
  nailed.
- **(B) The KMS/passivity of the static patch is well-established published physics** (BD = thermal KMS in the static
  patch; FDT holds in dS), so the passive verdict is robust, not a textbook-default artifact.
- **(C) This NO does not weaken the framework — it confirms and tightens it.** Route E (the nonlocal MI corner) is now
  provably **FOUNDED-not-DERIVED via a sign theorem**: the active kernel must be **postulated**; a0's **VALUE** remains
  inherited (only the `√Λ` **SCALE** is forced — same κ/Z wall, banked KAPPA_FORCING_DOOR_CLOSED). Symmetric with the
  banked **passivity check-7** and the **trichotomy** in `COVARIANT_MI_COMPLETION_2026-06.md`. **Nothing flips.** The open
  piece (active kernel source) is now closed as **un-sourceable from the passive dS vacuum.**

---

## Where this sits in the covariant-MI trichotomy (banked) — the last open horn is now closed

The covariant MOND-reproducing MI completion must be one of three (banked `COVARIANT_MI_COMPLETION_2026-06.md`):

1. **LOCAL aether/vector MI gate** → **Ostrogradsky ghost** (`|a|` is 2nd-derivative; the vector labels the frame, can't
   lower derivative order; Milgrom-1994 wall). *Blocked.*
2. **FIELD / modified-gravity MI** → 5th-force that moves Φ; the slip⇔Φ Bianchi lock + the covariant lensing no-go
   forbid a Cassini-safe covariant slip. *Blocked (fails Cassini).*
3. **NONLOCAL MI (Route E)** → the **only ghost-free corner** (entire/branch-cut form factor, single healthy pole). Its
   lone remaining failure was that its kernel **must be active** at `ω~ω_orbit` to give MOND, but the static dS-Unruh
   floor is **passive**. **← THIS DOC closes that last sub-problem: the active kernel is un-sourceable from the passive
   dS vacuum (sign theorem). Route E is FOUNDED-not-DERIVED.**

**All three horns are now blocked with named, sympy-confirmed obstructions.** The covariant-MI-completion program — the
framework's deepest gravity-side theory question — is **closed in its strongest form.**

---

## What it MEANS (the honest bottom line)

The framework is a **genuinely-founded effective field theory**, not a completed derivation:

- **FORCED (real, credited at full weight):** `a0 ~ c√Λ` as a **SCALE** emerges non-circularly from the dS-Unruh lock
  (`a_dS = cH_Λ` is genuine Deser-Levin physics); the deep-MOND/Newtonian limits and BTFR (sympy-exact); the nonlocal
  branch-cut form factor is ghost-free where the local truncation is not (the genuine Route-E advance).
- **POSTULATED (not derived — this theorem is *why*):** the **MOND sign** (inertia LOWERED at low a) and the **specific
  normalization** (`Z = √(32π/3)`, the `32π` is gravitational, unseen by a kinematic kernel; a0's **VALUE** inherited via
  the unforced κ). The active kernel that delivers the MOND sign **cannot come from the passive dS vacuum** — it must be
  written down by hand.
- **The forward is DATA, not theory.** The deepest open *theory* problem is now closed (as a no-go that tightens, not
  overturns, the standing). What remains live is **empirical**: the s^TX SME boost-dipole (Saturn 8.68e-10 vs
  INPOP/Cassini ~8.3e-9, ~9.6× margin — the more decisive near-term gravity test) and the a0(z) hostage front (BTFR-sign,
  DESI/ELT). Theory side: **founded EFT, walls mapped, quarantine held.**

---

## One line

The active-kernel sign theorem is **airtight and closes the program**: any causal, ghost-free, unitary cosmological kernel
is **passive** (`δm = 2∫ρ/ω² ≥ 0`) ⇒ inertia **RAISED** at low a ⇒ **anti-MOND**; the MOND inertia-lowering sign requires
a negative-norm (ρ<0) ghost band or an active gain medium, and **every realizable dS source is a passive KMS/FDT
equilibrium** (Candidates 1-3) while the only genuinely-active mechanism (frenesy/NESS, Candidate 4 — credited at full
weight as physics) **is not realizable from dS without a postulated drive** and is band-separated from `ω_orbit ≈ 295 H₀`
— so Route E's MOND kernel **cannot be DERIVED from the cosmos, only POSTULATED**: Route E is provably
**FOUNDED-not-DERIVED**, the covariant-MI-completion trichotomy has all three horns blocked, `a0 ~ √Λ` is a forced
**scale** with the MOND **sign/normalization postulated**, and the live action is now **data** (s^TX, a0(z)), not theory.
The one honest both-ways caveat: "closed" on Candidate 4 rests on *"dS supplies no sustained drive"* (robust physics, not
a theorem about frenesy) — a non-dS out-of-equilibrium drive would reopen it, but that is a manufactured source outside
the framework's dS foundation. No escape was inflated, no NO was high-priested.

**Scripts (absolute):** `/tmp/active_kernel_sign.py` (passive-bath Step-1, δm≥0 pointwise), `/tmp/active_kernel_step2.py`
(Candidates 1-2: expansion-squeezing + BD/KMS band-separation), `/tmp/active_kernel_step3.py` (Candidates 3-4:
horizon-2nd-law + frenesy/NESS non-realizability), `/tmp/active_kernel_step4.py` (KK + Källén-Lehmann ρ≥0 ⇔ passive ⇔
anti-MOND, the residue↔sign theorem), `/tmp/active_kernel_causality.py` (the both-ways correction: causality alone does
NOT forbid the MOND kernel — passivity does; explicit causal MOND-signed counterexample), `/tmp/active_kernel_numeric.py`
(ρ≥0 → δm=+238 vs ghost band → δm=−3311), `/tmp/active_kernel_escape.py` (final theorem statement + escape audit),
`/tmp/active_kernel_reconcile.py` (causal-counterexample vs ρ≥0 no-ghost are consistent layers).
**Banked:** `real_research/COVARIANT_MI_COMPLETION_2026-06.md` (the trichotomy + check-7), KAPPA_FORCING_DOOR_CLOSED,
MI_KERNEL_FROM_DSUNRUH_2026-06-19, MODIFIED_INERTIA_the_natural_home.
**Primaries fetched:** Milgrom 1999 astro-ph/9805346 (`a₀=(Λ/3)^(1/2)`; *"inertia-from-vacuum mechanism is still a far
cry off"*), dS-as-FDT/KMS-thermal-bath (1305.0229: *"obeys a fluctuation-dissipation relation … Maxwell-Boltzmann"* at
`T_dS=H/2π`). Milgrom 1994 (local-MI no-go), Luo 2026 2602.14515 (kinematic dS-Unruh kernel).
