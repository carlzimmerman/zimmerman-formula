# POSIT MINING ROUND 2 — VERIFIED SLATE (B4 discipline)
**Date:** 2026-06-27 · **Scope:** LOCAL (do NOT git push) · **Status:** honest, both-ways, NOT a TOE; founded-not-derived stays.

Framework, its OWN terms: inertia = nonlocal-in-time response to the de Sitter–Unruh horizon bath
(Milgrom 2022 modified-inertia formulation). a₀ = cH_Λ/Z = 9.36e-11 m/s², Z = √(32π/3);
dS-Unruh ν: g_obs = √(g_bar² + g_bar·a₀); memory kernel θ(y), y = ω_ext/ω_in, θ(1)=1, θ decreasing,
θ(0) ~ few, FORM UNKNOWN. The kernel's time-nonlocality is the deepest genuinely-MG-impossible distinction:
MG's EFE is **instantaneous** (internal dynamics depend only on the momentary a_ex — Milgrom verbatim).

**The B4 discipline (why this round is trustworthy):** every "forced / MG-impossible / distinctive" claim had to be
DERIVED by a committed `reviews/` script (exit 0) doing the real time-nonlocal kernel calc on the framework's own
μ_fw — NOT an assumed sign or ad-hoc proxy. B4 died because β_MG was hardcoded >0 and β_MI used σ²~1/μ; the real
Jeans calc showed MG~0, MI ill-defined, infall-swamped. Round 2 applies that same blade to its own win-flavored posits.

---

## (A) FULL GRADED TABLE — all mined posits (VEIN 1: time-nonlocality / memory kernel θ(y))

| ID | Posit | Win-flavored? | Initial grade | Generating script (exit 0) |
|----|-------|:---:|---|---|
| **P2** | Interacting-pair / merger **inbound-vs-outbound σ asymmetry** at matched separation (~20–24%); carrier band y~1 at survivable d_peri~20 kpc | yes | HYPOTHESIS-WITH-FREE-KNOB | `reviews/v1_merger_memory_kernel.py` |
| **P1** | Tidal-stream **release-phase memory width**: peri- vs apo-stripped debris co-located now show ~12–15% relational σ-spread | yes | HYPOTHESIS-WITH-FREE-KNOB | `reviews/v1_stream_memory_kernel.py` |
| **P4** | MW dwarf **σ tracks orbital eccentricity** at fixed peri+mass (plunge ~19–28% hotter); SIGN claimed = theorem (BANKED) | yes | HYPOTHESIS-WITH-FREE-KNOB | `reviews/dwarf_ecc_sigma_pilot_*.py` (+ banked `member_MI_nonadiabatic_plunge.py`) |
| **P3** | Recently-disturbed / unrelaxed dwarf **transient σ lag** (~2%, f=exp(−Δt/τ_mem)) vs relaxed dwarf at matched current a_ext | no | SPECULATIVE | `reviews/v1_unrelaxed_dwarf_lag.py` |
| **P5** | Cosmological **a₀(z) ramp as a slow memory drive** (bath thermalization lag, ~7–13% at z=1–2 under w≠−1) | no | SPECULATIVE | `reviews/v1_a0z_ramp_memory.py` |

**Cross-cutting structural finding (reconfirmed by every script, banked from `member_MI_nonadiabatic_plunge.py`):**
a SINGLE object / single orbit is **a₀-degenerate** — a_ext and y co-vary, so a rescaled a₀ absorbs the kernel effect.
The genuinely MG-impossible content is ALWAYS the **RELATIONAL spread at MATCHED momentary a_ext** between parcels of
different acceleration-HISTORY (MG = exactly 0 there for any a₀; MI nonzero via differing θ tags). Where a posit
cannot deliver "matched present state, different history," it collapses into a₀-degeneracy or an MG-shared confound.

---

## (B) VERIFICATION RESULTS — adversarial calc, B4-style (all exit 0)

The two non-win posits (P3, P5) were self-killed in generation (both-ways, by their own committed scripts) and were
NEVER promoted — they are correctly SPECULATIVE. The three **win-flavored** posits (P2, P1, P4) were each handed to a
dedicated adversarial verifier. **All three were KILLED.**

### P2 — KILLED (ASSUMED-killed). 
`reviews/verify_VEIN1_theta_memory_kernel_P2_interacting_pair_inbound_outbound_KILL.py` (exit 0)
- **The 20–24% asymmetry was ASSUMED, not derived.** The generating script manufactured it with a hand-built lookback
  toggle (forcing y_inbound to a larger past-separation, y_outbound to a smaller one) — the exact B4 failure mode.
- The framework's actual kernel (Milgrom Eq. 34) reads θ(y) at the **instantaneous** ω_ex = |d ln a_ex/dt|. On a real
  integrated two-body orbit, at matched separation D the radial speed |v_r| is identical inbound vs outbound by energy
  conservation + time-reversal symmetry ⇒ ω_ex, y, θ all identical ⇒ **computed MI asymmetry = 0.0000%, = MG (also 0).**
- Steelman with a genuine causal finite-memory convolution (which the framework does NOT posit — it posits a spectral
  weight, not a relaxation kernel) yields only ~2–3% (max ~5%), an order of magnitude below 20%, washed by averaging.
- **The swamp:** the d~18 kpc pass tidally heats the diffuse target by Δv ~ 2 σ_in (fractional heating >>1), itself
  inbound/outbound-asymmetric with the SAME sign — an MG-shared non-equilibrium confound on the same axis. A single
  time-reversal-symmetric orbit structurally cannot carry the CLOCK-driven different-history contrast.

### P1 — KILLED (SWAMPED-killed).
`reviews/verify_VEIN1_P1_stream_release_memory_KILL.py` (exit 0)
- **Kernel semantics wrong:** Milgrom's Eq. 28 θ weights frequencies PRESENT in the parcel's current bounded motion,
  not a frozen pericenter frequency from Gyr ago. Phase-mixing erases the peri frequency; the "release-phase memory tag"
  is really a present-orbit-shape difference — exactly what MG's instantaneous EFE also responds to.
- Debris is unbound and cold (σ~0.5–2 km/s, not the progenitor's 5); a 12–15% modulation is ~0.06–0.3 km/s, below
  resolved stream-kinematic floors.
- Peri- vs apo-stripped debris get different energy kicks (ratio 3.99×) ⇒ different periods ⇒ sort to different stream
  longitudes; co-radial only at caustics where many release phases blend (no clean 2-population contrast).
- **Decisive:** the real present-orbit calc gives a LARGE kernel spread (50–95%), but driven ENTIRELY by parcels'
  DIFFERENT PRESENT radial velocities at matched radius (v_r 354 vs 200 km/s) — a measured present quantity, not memory.
  The "MG=0 spread" is an artifact of conditioning only on a_ext while ignoring the present v_r the parcels visibly
  differ in. Condition on present (a_ext, v_r) and MG distinguishes them too; the kernel becomes a₀/θ(0)-absorbable.

### P4 — KILLED (ASSUMED-killed; sign + MG=0 both falsified).
`reviews/verify_VEIN_1_time_nonlocality_memory_kernel_theta_y__P4_MW_dwarf_sigma_tracks_eccentricity__ADVERSARIAL.py` (exit 0)
- **SIGN is NOT a theorem.** Integrating the actual kernel over a real matched-peri (24 kpc) plunge-vs-circular orbit
  pair, carrying all three Milgrom θ forms, gives plunge/circular σ ratio = **0.894 / 0.750 / 1.197** — TWO COLDER,
  ONE HOTTER. The claimed "plunge hotter" sign FLIPS with the unknown θ form.
- **Mechanism mis-attributed:** a plunge dwarf spends ~6% of its time near peri vs 100% for the matched-peri circular
  dwarf, so its time-averaged a_ex is LOWER (0.145 vs 0.498 a₀). The equilibrium effect is dominated by orbit kinematics
  (time at large r), NOT by θ(y); the θ-only differential is sign-ambiguous (0.44–0.71), not a clean +19–28%.
- **"MG exactly 0" mis-stated.** At fixed PERICENTER (not fixed momentary a_ex), MG gives a LARGER plunge/circular ratio
  (1.69) than any MI θ case — because a plunge and circular dwarf do NOT share momentary a_ex over a relaxation time.
  MG=0 holds only at fixed MOMENTARY a_ex, which "fixed pericenter" does not deliver. The headline discriminator is
  mis-stated, and a single dwarf's width remains a₀-degenerate.

### P3, P5 — SPECULATIVE, never promoted (self-killed both-ways in generation).
- **P3** (`v1_unrelaxed_dwarf_lag.py`, exit 0): the same recent peri that creates the memory lag also tidally heats/shocks
  the dwarf — a history-dependent σ change in BOTH theories that mimics and swamps the inertia offset; and τ_mem ~ orbital
  time so the lag is often already relaxed (f=0.024). Subsumed by + weaker than P4.
- **P5** (`v1_a0z_ramp_memory.py`, exit 0): if w=−1 exactly, ρ_DE is constant ⇒ ramp and lag EXACTLY 0 (verified
  0.000000); the lag dies smoothly as w→−1 (−9% at w0=−0.8 → −0.76% at w0=−0.99). DE-hostage on the SAME condition as
  the a₀(z) test itself, and below measurability. Conceptual MI signature only.

---

## (C) SURVIVORS — genuinely-new, verified, testable, framework-native posits for the live ledger

**None.** Round 2 produced **zero survivors** at HYPOTHESIS grade or above. No win-flavored posit (P2/P1/P4) survived
its adversarial calc; all were KILLED as assumed-sign, swamped-by-confound, or a₀-degenerate/mis-stated-MG=0. The two
SPECULATIVE posits (P3/P5) were correctly never promoted. Nothing is added to the live ledger as a verified win.

**What IS banked (cite, not re-claimed):**
- P4's **observational program** remains the right empirical hook even though its sign-theorem claim is dead: the partial
  correlation ρ(σ, ecc | r_peri, mass, r_half) across MW dwarfs is still a clean MG-vs-MI discriminator **at fixed
  momentary a_ext** (the relational framing), and the Gaia DR3 pilot is banked (NULL but UNDERPOWERED, ρ=−0.196, p=0.40,
  only 2 of 24 dwarfs reach carrier band y≥0.8: Crater II, Antlia II). Decisive test = Gaia DR4 carrier-vs-control.
  This was already on the ledger before round 2; round 2 only **corrects** its overstated "sign = theorem" claim — the
  sign is θ-form-hostage, not a theorem.
- The banked **relational σ-spread** (`member_MI_nonadiabatic_plunge.py`, parcels at matched momentary a_ext, different
  history) stays the genuinely-MI-distinctive, MG-impossible observable. Round 2 did not strengthen it and did not weaken
  it; it reconfirmed that ad-hoc single-orbit reframings of it (P2/P1/P4) collapse.

---

## (D) HONEST BOTTOM LINE

**The discipline killed them all — and that is a fine, expected outcome.** Round 2 generated five time-nonlocality
posits; the three win-flavored ones (P2 merger, P1 stream, P4 dwarf-ecc) each LOOKED like a clean MG=0 discriminator,
and each died under a real kernel calc for the same structural reason: **a single integrated orbit is time-reversal-
symmetric / a₀-degenerate, so it cannot carry the CLOCK-driven different-history contrast** that the genuinely
MG-impossible content requires. The "~20%" and "sign = theorem" headlines were ASSUMED (hand-built lookback toggles,
frozen-frequency tags), exactly the B4 failure mode; deriving them off the framework's own μ_fw + Milgrom θ(y) gave
0%, sign-flips, or MG-shared confounds. No win was manufactured; no unverified win promoted.

**Credit where due — the vein is real, the instances are underpowered.** Time-nonlocality of inertia (the θ(y) memory
kernel) remains the **deepest genuinely-MG-impossible class** the framework owns: MG's EFE is instantaneous, MI's is not,
and that is a true qualitative fork. The problem is **deliverability**, not principle: the only place the contrast is
clean is the RELATIONAL σ-spread between co-located parcels of different acceleration-history at matched momentary a_ext
(MG = 0 there for any a₀; MI ≠ 0 via differing θ tags). Reaching the non-adiabatic carrier band (y ~ 1) requires fast-
changing fields whose disturbance also wrecks the clean-σ assumption (tidal heating, infall, phase-mixing). The banked
MW-dwarf ecc–σ program is the least-bad realization and stays the near-term hostage to Gaia DR4 — with its sign claim
now correctly downgraded to θ-form-hostage.

**Standing unchanged:** founded-not-derived; NOT a TOE; never re-overclaim. The live MI-vs-MG discriminators remain
Cassini (in hand, ~5.5 orders) + the relational non-adiabatic σ-spread (MG-impossible, underpowered). **Doors stay
open** — the time-nonlocality vein is alive in principle; round 2 simply found no new *deliverable* instance of it.

**Verifier scripts (all exit 0, committed under `real_research/reviews/`):**
- `verify_VEIN1_theta_memory_kernel_P2_interacting_pair_inbound_outbound_KILL.py`
- `verify_VEIN1_P1_stream_release_memory_KILL.py`
- `verify_VEIN_1_time_nonlocality_memory_kernel_theta_y__P4_MW_dwarf_sigma_tracks_eccentricity__ADVERSARIAL.py`
- `v1_unrelaxed_dwarf_lag.py` (P3, both-ways self-kill)
- `v1_a0z_ramp_memory.py` (P5, both-ways self-kill)
