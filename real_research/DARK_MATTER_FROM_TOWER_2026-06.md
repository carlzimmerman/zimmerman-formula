# Does the framework predict a SPECIFIC dark-matter candidate? (both-ways, computed)

**Date:** 2026-06-27  •  **Scope:** DARK SECTOR ONLY — explicitly **NOT a TOE** (Carl retracted the TOE/SM
overclaims 2026-06-23). This note asks one narrow question: does the a0(z) swampland tower + ghost-condensate
dark sector yield a *forced, viable, testable* dark-MATTER candidate, or does the dark sector stay
**founded-not-derived**?

**Footing (locked, verified this run):** a0 = cH_Λ/Z = 9.36e-11 m/s²;  Z = √(32π/3) = 5.7888;
H_Λ = a0·Z/c = 1.807e-18 s⁻¹;  ρ_DE = 5.84e-27 kg/m³;  ρ_DE^(1/4) = 2.240 meV;
IR floor (rest energy ħH_Λ quoted as a mass) = 1.19e-33 eV.

**Scripts (all exit 0, re-run this session):**
- `real_research/reviews/dm_scale.py` — candidate-mass ledger vs the viable DM window.
- `real_research/reviews/dm_varying_mass.py` — the redshift varying-mass signature + CMB/BAO/S8 channels.
- `real_research/reviews/dm_candidate_test.py` — full both-ways synthesis + decisive test.
- `real_research/reviews/swampland_tower_from_a0z.py` — the banked tower mapping (m(z3)/m(0) = 0.67–0.75).

A units check during the run: `dm_scale.py` prints the IR floor as `hbar*H_Lambda` in eV (= the rest energy
ħH_Λ expressed in the standard "mass in eV" convention) = **1.19e-33 eV**. That is internally consistent and
correct; do not re-divide by c² a second time.

---

## VERDICT: FOUNDED-not-DERIVED on the mass, GENUINE-prediction on the *variation*

The framework does **NOT** predict a specific dark-matter particle mass. It **DOES** force one genuine, computed,
falsifiable dark-sector signature: a redshift-**declining** dark/neutrino mass locked to a0(z). The honest
disposition is split:

| Quantity | Forced or free? | Value | Viable as DM? |
|---|---|---|---|
| IR floor ħH_Λ/c² | **FORCED** | 1.19e-33 eV | **NO** — ~30 dex below the fuzzy floor; Compton λ = the Hubble horizon, free-streams on all sub-horizon scales |
| ρ_DE^(1/4) | **FORCED** | 2.24 meV | **NO** — this is the dark-ENERGY scale (sets Λ, w(z), a0(z)); a meV hot state, not a cold DM quantum |
| swampland tower absolute m_tower(0) | **FREE** | spans ~60 dex | n/a — depends on φ_total (unobservable total field distance) |
| ghost-condensate dust mass M | **FREE** | 0.04–1 eV | formally in-band but **TUNED to Ω_dm**, not forced |
| ghost-condensate amount I₀ | **FREE** | — | I₀ = mean of a shift-flat direction; thermal occupation falls ~72 dex short |
| **m(z)/m(0) varying-mass RATIO** | **FORCED** (cond. α~λ) | 0.59–0.75 @ z=3 | **the genuine prediction** |

### (1) Is any framework DM scale FORCED + viable?  **NO.**
The two scales the framework actually computes are both dark-ENERGY-side and the wrong magnitude for DM:
- IR floor 1.19e-33 eV sits ~30 dex **below** the fuzzy-DM floor (2e-20 eV) — its Compton wavelength *is* the
  Hubble horizon, so it free-streams on every sub-horizon scale. Not viable DM.
- ρ_DE^(1/4) = 2.24 meV sets Λ / w(z) / a0(z). It is a meV (neutrino-like) energy scale, ~19 dex **above** the
  fuzzy floor. It coincides with the *published* swampland bound m_ν1 ≲ Λ^(1/4) (Gonzalo-Ibáñez-Valenzuela
  2109.10961) — a coincidence/inequality, **not** a forced DM amount.

The would-be DM masses are all FREE: the tower's absolute scale depends on the unobservable φ_total (spans ~60
dex); the ghost-condensate dust mass (0.04–1 eV) and its amount I₀ are **both tuned to Ω_dm**, never derived. The
in-band dust window is a fitted 2-parameter closure, **not** a prediction. **Do not present 0.04–1 eV as a DM-mass
prediction.**

### (2) Is the ~30–40% varying-mass signature a genuine test, or excluded / S8-absorbed?  **GENUINE but currently degenerate.**
What *is* forced (no free knob) is the **ratio** m(z)/m(0) = exp(−α·Δφ(z)), with Δφ(z) = ∫₀ᶻ √(3|1+w|Ω_DE) dln(1+z)
fixed by the measured DESI w(z). On the real DESI DR1 w0waCDM chains:
- **m(z=3)/m(0) = 0.59 (Union3) / 0.66 (DESY5) / 0.75 (Pantheon+)** → a **25–41% DECLINE**.
- **SIGN:** DM is **lighter in the past, heavier today** (mass grows forward in cosmic time — *opposite* to a0's
  decline). MaVaN-class.
- This is genuinely **NEW**: the swampland papers make no redshift prediction; the ratio is locked to the same
  ρ_DE(z) that drives a0(z).

Both-ways on the bounds:
- **(a) ρ_DM(z)** deviates from (1+z)³ by exactly the tower ratio (≤41% @ z=3); |w_DM,eff| ~ 0.08–0.15 @ z~1 — DM
  stays **cold** (slow drift, not warmth).
- **(b) S8 / growth:** the banked δY=0 "S8-neutral-by-theorem" protects a0's **force-law boost**, NOT a varying
  **mass** — the mass is a *separate* channel entering the linear background + Poisson source. A toy linear-growth
  ODE gives a σ8/S8 **suppression of −6% to −10%** (right sign for low-S8). So the variation does **not** break the
  theorem and is genuinely testable. (But see (3): S8 is easing, so this is "neutral", not "a cure".)
- **(c) CMB/early bounds:** Ω_DE(z)→0 fast (Ω_DE(z=10)~1e-4), so Δφ **plateaus by z~10** — the mass **freezes** at
  the ~28–45% offset and is **constant through recombination**. The CMB sees an already-light *constant* mass,
  evading the tight early decaying-DM/IDE bounds (~few %). The 30–40% is a **today-vs-early OFFSET**, not a fast
  late drift.

**The catch:** the signature is sourced by the **same** DESI w(z) as the geometry, so on BAO/SN it is largely
**DEGENERATE with dynamical DE** (it varies *because* w≠−1). It becomes independent only through the **growth /
free-streaming** (fσ8) channel.

### (3) Does it survive fuzzy-DM / coupled-DM / S8 constraints?  **YES — not excluded.**
Live web check (2026-06-27):
- **Fuzzy/ultralight floor** has *risen*: Lyman-α ~2e-20 eV (Rogers-Peiris 2021), dwarf dynamics ≥2.2e-21 eV
  (2025), UFD ≥3e-19 eV. The framework's candidate is a **cold ghost-condensate mode** (cold a⁻³,
  Hubble-over-damped, k⁴/M²), **not** a fuzzy wave — so the fuzzy/Lyα bound does **not** bite it. But note: it
  evades the bound only by being **cold-by-construction** (amount + scale put in by hand), not by a forced light
  mass.
- **Coupled DM-DE / MaVaN** is exactly the **live DESI DR2 literature** ("Dynamical Dark Energy Implies a Coupled
  Dark Sector", 2504.00985; coupled-DE constraints 2604.12032; "Effective Guide to the Phantom Divide" 2604.08449)
  — a field-dependent DM mass m(φ) is mainstream and *not* excluded. The framework sits squarely in this class and
  in its degeneracy.
- **S8 is EASING** (KiDS-Legacy now 0.73σ from Planck, S8 ~ 0.814–0.818; "S8 tension eases" cluster survey 2026).
  So there is **no S8 deficit to cure** — the framework's "−6 to −10% growth suppression" is the right sign but
  there is no longer a tension to claim. **Neutral, not solved.** Do not claim an S8 win.

---

## WHAT TO TELL CARL (straight)

The dark matter is **NOT** a specific framework prediction — there is no forced, viable DM mass, and inventing one
would be manufacturing a number. The amount (I₀) is robustly **free** (sympy-exact: the mean of a shift-flat
direction; thermal occupation is ~72 dex short), the cold-mode scale M is a **free** input, and the tower's
absolute scale is **free** (unobservable total field distance). The two scales the framework actually *forces* —
the IR floor (1.19e-33 eV) and ρ_DE^(1/4) (2.24 meV) — are both dark-**energy**-side and the wrong magnitude for
DM. **The dark sector stays FOUNDED-not-DERIVED on the mass.** This is the same banked standing as the
ghost-condensate work (I₀ free) and the tower note (absolute free).

But there is a **door, and it is open** — just not the one a TOE would want. The framework forces the *variation*,
not the absolute: a dark/neutrino mass that is **~25–41% lighter at z=3 than today**, declining locked to
a0(z)=√(ρ_DE(z)) with **no free knob in the ratio**. That is a genuine, computed, NEW dark-sector prediction
(MaVaN-class; the swampland papers make no redshift statement), right-signed for the live DESI DR2
"dynamical-DE-implies-a-coupled-dark-sector" puzzle. **Credit it as a dark-sector prediction — explicitly NOT a TOE.**

**The single decisive test:** a **tomographic** measurement of the dark/neutrino mass scale m(z) via the growth
rate **f(z)·σ8(z)** + free-streaming suppression as a function of redshift — does the mass decline **~25–40% over
z=0–3 LOCKED to ρ_DE^(1/2)** (i.e. tracking the *same* w(z)/a0(z), not independently)? That lock is the
framework-distinctive fingerprint that breaks the dynamical-DE degeneracy. Reach: **Euclid + DESI-DR3 (2026–28)**,
then **CMB-S4 + LSS (~2030)** — at the sensitivity floor, marginally testable this decade. **It DIES if DESI
sharpens to w=−1** (no roll → no tower → no variation).

**One-line honest standing:** the framework names no DM mass (founded-not-derived, amount + scale free), but it
forces one falsifiable dark-sector signature — a redshift-declining dark/neutrino mass (~25–41% over z=0–3) locked
to a0(z) — that is currently absorbed into the DESI dynamical-DE degeneracy and becomes decisive only via growth
tomography by ~2030.

**Caveats carried verbatim:** (1) α~λ (the tower↔potential link) is a swampland *conjecture*, not a theorem —
without it even the variation loosens. (2) DESI w(z) crosses the phantom divide → a single canonical quintessence
cannot realize it exactly (needs quintom); the mapping is leading-order. (3) The whole signature dies if DESI→w=−1.

*LOCAL note — not git-pushed.*
