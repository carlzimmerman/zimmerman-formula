# The Dwarf-Spheroidal σ-Spread Door — Both-Ways Verdict (2026-07-07)

**Framework:** de Sitter–Unruh **modified inertia**. a₀ = cH_Λ/Z = 9.36×10⁻¹¹ m/s², Z = √(32π/3),
RAR ν(y) = √(1+1/y), boost = 1/μ_fw. Validated non-local kernel θ_fw(y) = √2/(1+(√2−1)y²)
(forced single-pole core), 2-pole bracket θ = 2/(1+y²), θ(1)=1, θ≡1 = the local/MG limit.
A_eff = a_internal + θ(y)·a_external, y = ω_ext/ω_in.

**Scripts (exit 0, no git commit):**
- `real_research/reviews/dwarf_sigma_mi_kernel.py` — original (headline **RETRACTED**, see below)
- `real_research/reviews/dwarf_sigma_mi_reconcile.py` — adversarial reconciliation
- `real_research/reviews/dwarf_sigma_mi_final.py` — **the corrected computation of record**

---

## Bottom line

The paper's headline (DOI 20947913 sec. 6.3; DSUNRUH_MI_THEORY_2026 sec. 7 pred. 3) —
**"a diffuse dwarf runs +12–30% HOTTER in σ than a circular dwarf of the same mass and pericenter,
MG-impossible"** — is **RETRACTED**. It is manufactured by a **fake (θ-stripped) MG baseline**, the same
class of error that killed the sibling wide-binary door.

But the door does **not** die like the wide binary. σ is a genuine second moment and **is** kernel-sensitive
(not DC-protected). What survives, after all three adversarial verifiers are reconciled, is a **real but
weaker, τ_mem-conditional** door with a **corrected, stable observable**:

> **σ HYSTERESIS at fixed current galactocentric radius r.** MG (even carrying the framework's own
> instantaneous θ(y) external-field law) gives σ = single-valued f(r): inbound and outbound σ are equal at
> the same r. MI's memory makes σ(r) **double-valued** — a recently post-pericenter dwarf stays hotter than
> an inbound one at the same r. That inbound–outbound scatter is MG-impossible and **immune to
> mass-to-light** rescaling.

**Classification: partial-needs-work.** Kernel-live, MG-impossible in principle, but quantitatively
hostage to a time-domain memory time τ_mem that the frequency-domain θ(y) does **not** force.

---

## The three adversarial findings, reconciled (each re-run and confirmed)

| # | Objection | Re-run result | Correction |
|---|-----------|---------------|------------|
| C1 | **Fake MG baseline** (dc-protection lens): the script fed MG the **bare** a_ext, θ stripped. The framework's own AeST/ghost-condensate realization carries the **same instantaneous θ(y)·a_ext**. | Confirmed. Honest θ-MG phase-spread = 27% (not 65%); MG-impossible gap collapses **−43.5 pp → −5.5 pp**. | Give MG the instantaneous-θ EFE. θ as a pointwise loading rescale is SHARED; only **memory** is MI-distinctive. |
| C2 | **Truncated memory window**: the integral ran only [0, t_obs] with no inbound history, inflating the phase-0.05 V-KS shift. | Confirmed. Full periodic history: phase-0.05 θ-only shift **71% → 32%**; deeper phases barely move. | Full periodic history (8 tail periods). |
| C3 | **Broken orbit clock** (V-ART): linspace-in-r + dr/v_r blows up at peri/apo (v_r→0), giving nonsense periods (Antlia 8764 Gyr, Sculptor 3991 Gyr) and NaN hysteresis. | Confirmed. Eccentric-anomaly substitution r = a(1−e cosE) → dt/dE = a·e·sinE/v_r vanishes at both ends. All four dwarfs now give sensible P_half ≈ 1.3–2.9 Gyr. | Proper clock. |
| C4 | **Sign-flipping "memory-diff (pp)"**: a difference of two spread statistics whose sign flips between carriers (Crater −56, Antlia +5.6) from phase-grid under-sampling. | Confirmed unstable. | Replaced by **fixed-r hysteresis** (single-signed, M/L-immune). |

---

## Non-negotiable validations (final script)

**V-RAR — PASS.** Kernel reduces to framework RAR: max rel.err(boost vs ν) = 3.6×10⁻¹²; θ_fw(1)=θ_2pole(1)=1.

**V-KS — SURVIVES (kernel-sensitive, NOT DC-protected).** This is the decisive contrast with the dead
wide-binary door (a DC-protected orbit-MEAN, signal identically 0). σ is a genuine second moment and the
kernel touches it:
- θ-only shift at matched phase + matched full-periodic memory: **+32% near pericenter** (corrected from
  the truncation-inflated 71%), falling to ~0 at apocenter.
- OBS-B (true DF velocity variance σ² over the stellar distribution function): θ genuinely shifts σ² at
  pericenter (fw −3.7%, 2-pole −7.4%). Not DC-protected.

**V-MG — genuine MG-impossibility, but only in the memory-lag.** An honest MG dwarf carrying the same
instantaneous θ(y)·a_ext still gives σ = single-valued f(r) → **exactly 0** inbound–outbound hysteresis.
MI's memory makes σ(r) double-valued → nonzero hysteresis. This is a real, M/L-immune MG-impossibility.
It is **not** the paper's "+12–30% hotter at fixed pericenter" (which MG reproduces via its own phase-varying
a_ext), and **not** a tautology (MG is given its best shot, instantaneous θ-EFE, and still can't do it).

**V-ART — hysteresis magnitude stable** under resolution (nE 3000/6000/12000 → 19.5/17.6/17.3%). Reported
against measured orbits. *Caveat:* the absolute half-period has not fully converged in the eccentric-anomaly
clock (4.67→1.98 Gyr across nE) because r=a(1−e cosE) is a Keplerian approximation to the power-law halo
orbit; the **door magnitude** (hysteresis %) is what is stable and load-bearing, not the absolute clock.

---

## Exact predicted σ-hysteresis per dwarf (measured orbits, Pace+2022 MW+LMC)

Peak inbound-vs-outbound σ hysteresis at fixed r, forced √2 core vs 2-pole bracket, τ_mem = 0.45 Gyr:

| Dwarf | Type | y_max | **fw (√2)** | 2-pole | **\|fw−2pole\|** | θ-specific? |
|-------|------|-------|------|--------|-----------|-------------|
| **Crater II** | carrier | 3.38 | **17.6%** | 7.0% | **10.6 pp** | STRONG θ-signal |
| **Antlia II** | carrier | 2.50 | **13.2%** | 3.6% | **9.6 pp** | STRONG θ-signal |
| Fornax | control | 0.16 | 13.4% | 14.0% | 0.6 pp | kinematic (θ-blind) |
| Sculptor | control | 0.12 | 17.4% | 18.2% | 0.8 pp | kinematic (θ-blind) |

**Key honest finding (the clean discriminant).** The *raw* hysteresis magnitude is **NOT** a clean
carrier/control diagnostic — controls show comparable (~13–17%) hysteresis because most of it is the
**a_ext-swing memory**, present in *any* memory model even where θ≈const. The genuinely θ-specific signature
is the **fw-vs-2-pole spread**: large for carriers (|fw−2pole| ≈ 10 pp, θ genuinely reweights the y>1
harmonics) and ~0 for controls (θ acts as a constant at y≪1). **Crater II is the prime carrier** (deep
pericenter 24 kpc, y_max = 3.38, a_ext swings 0.071→0.572 a₀).

---

## The biggest caveat (the door's soft spot)

The MG-impossible content is **memory-lag**, whose magnitude is **hostage to τ_mem** — and τ_mem is a
**time-domain** memory time that the framework's **frequency-domain** θ(y) does **not** force:

| τ_mem (Gyr) | τ/P_half | Crater II peak hysteresis |
|-------------|----------|---------------------------|
| 0.05 | 0.02 | 5.6% |
| 0.25 | 0.09 | 16.6% |
| 0.45 | 0.16 | **17.6%** |
| 0.90 | 0.31 | 15.0% |
| 2.00 | 0.69 | 9.8% |

The signal peaks at τ_mem ~ 0.2–0.5 P_half and **dies as τ_mem→0** (no memory) or τ_mem≫P (fully mixed).
A critic can legitimately argue the paper has not shown the dS bath forces **any** nonzero memory time. The
door is real and MG-impossible in principle, but **quantitatively undetermined until τ_mem is derived, not
postulated.** This is the honest analogue of the a₀(z) "hostage" caveat.

---

## The data test — from underpowered null to decisive ≥3σ

**Current status (why it's underpowered).**
- **Crater II:** ~60–120 member stars (Caldwell+2017, Ji+2021), σ ≈ 2.7 km/s with ~±0.3–0.5 km/s
  uncertainty. Too few stars, and — critically — no clean inbound/outbound branch resolution: the pilot
  correlation of σ-residual vs a sigma-embedding non-adiabaticity proxy is ρ = −0.196, p = 0.40, a
  **wrong-signed, underpowered NULL**.
- **Antlia II:** ~150 members (Torrealba+2019, Ji+2021), σ ≈ 5.7 km/s. Larger but shallower pericenter →
  weaker θ-signal.
- The observable was mis-specified: predicting σ from y (which **embeds σ**) makes carriers cold by
  construction. The correct predictor is a **σ-free** non-adiabaticity measure (a_ext history +
  time-since-pericenter, θ-memory-weighted).

**What makes it decisive.**
1. **Gaia DR4 proper motions** (Dec 2026) to nail each dwarf's orbit AND resolve the **inbound vs outbound
   branch** (sign of the current radial velocity relative to the fitted orbit) — this is what turns "phase
   spread" into the clean fixed-r hysteresis pair.
2. **High-precision diffuse spectroscopy:** **N ≳ 200 members** per dwarf at **per-star velocity precision
   ≲ 0.3 km/s**, giving σ to ≲ 0.2–0.3 km/s (≲ 4–5% on a 5–6 km/s dwarf). At that precision a 10–17% fixed-r
   hysteresis is a ≥3σ effect.
3. **Dwarf selection:** target the **deep-pericenter diffuse carriers** where y_max > 1 (Crater II, Antlia II
   are the two in hand; extend to a sample of ~15–20 recently-post-pericenter diffuse dwarfs from the LSST/DESI
   census). The **fw-vs-2-pole spread** is the model-independent-of-magnitude discriminant — measure whether
   carriers separate from controls in the θ-specific channel, not the raw magnitude.
4. **The control:** classical dense dwarfs (Fornax, Sculptor, y_max ≪ 1) should show hysteresis that is
   **the same for fw and 2-pole** (kinematic only). Carriers should show fw ≫ 2-pole. That carrier/control
   split in |fw−2pole| is the signature that is genuinely the kernel, not orbital kinematics.

**Decisive test, one line:** Gaia DR4-dated inbound/outbound branches on ~15–20 deep-pericenter diffuse
carriers + N ≳ 200 stars each at ≲ 0.3 km/s precision, testing whether σ is double-valued at fixed r (MG:
single-valued, 0) and whether the carrier hysteresis is θ-model-sensitive (|fw−2pole| ~ 10 pp) while controls
are not — with the honest prior that the whole magnitude scales with an unforced τ_mem.
