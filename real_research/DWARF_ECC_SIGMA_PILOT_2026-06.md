# Dwarf σ-vs-eccentricity pilot — the horizon-bath non-adiabatic-inertia prediction on real data

**Date:** 2026-06-26  **Status:** LOCAL pilot, exploratory, pre-registered, NOT git-pushed.
**Footing (sealed):** a₀ = cH_Λ/Z = 9.36e-11 m/s²; framework's OWN interpolation ν(y)=√(1+1/y),
μ_fw(x)=(√(1+4x²)−1)/2x. McGaugh ν NEVER used.
**Data (single homogeneous source):** Pace, Erkal & Li 2022 (ApJ 940, 136 = arXiv:2205.05699) for
ALL σ_los AND all Gaia EDR3 orbits; Simon 2019 ARA&A and McConnachie 2012 as cross-checks.
**Scripts:** `reviews/dwarf_ecc_sigma_pilot_data.py` (real cited data + pre-registered test),
`reviews/dwarf_ecc_sigma_pilot_analysis.py` (per-dwarf y/boost prediction). Partial-correlation
test reproduced independently this session (numbers below match the gathered verdict to 3 sig figs).

---

## The prediction being tested (framework as subject)

The framework's own premise — inertia is a body's **nonlocal-in-time response to the de Sitter
cosmic-horizon Unruh bath**, which carries exactly ONE clock H_Λ — forces a native consequence
nothing else in the corpus pointed at: **at fixed pericenter and mass, a radial-PLUNGE diffuse MW
dwarf runs HOTTER (higher internal σ) than a circular-orbit one.** The plunge drives ω_ext → ω_in
near pericenter (non-adiabatic, y = ω_ext/ω_in ~ O(1)), the memory kernel θ(y) sheds the adiabatic
θ(0)·g_ext external loading, the dwarf drops deeper into deep-MOND, and σ rises.

- **SIGN is a theorem** (θ(0) > θ(1)=1, Milgrom-forced): plunge → hotter, robust for ALL kernel forms.
- **MAGNITUDE is θ(y)-kernel-hostage** (~factor 2): the banked headline is **+19–28%** at the y=1
  reference ((θ(0)/θ(1))^¼ = 2^¼…e^¼).
- **MODIFIED-GRAVITY-IMPOSSIBLE**: AQUAL/QUMOND/AeST EFE is instantaneous (Milgrom 2022, verbatim:
  internal dynamics "depend only on the momentary value of a_ex"), so MG and CDM predict **exactly
  zero** σ-vs-eccentricity correlation at fixed pericenter. That zero is the discriminator — this
  pilot asks whether the real data already shows the framework's nonzero positive correlation.

---

## (i) Is there a σ-vs-eccentricity correlation at fixed pericenter/mass? — NO

Pre-specified primary statistic, **partial Spearman ρ(σ_los, eccentricity | r_peri, mass-proxy[L
from M_V], r_half)**, N=24 usable MW dwarfs (Pace+2022 MW+LMC orbits), reproduced independently:

| variant | ρ | p (two-sided) | reading |
|---|---|---|---|
| **PRIMARY** partial ρ(σ,ecc \| r_peri, L, r_half) | **−0.196** | **0.395** (dof=19) | null, wrong-signed |
| virial-deviation ρ(log σ, ecc \| √(L/r_half), r_peri) | −0.220 | 0.313 | null |
| simple (uncontrolled) Spearman(σ, ecc) | −0.113 | 0.598 | null |
| no-LMC eccentricity (both-ways) | −0.030 | 0.899 | even flatter |

**The point estimate is NEGATIVE in every variant** — the OPPOSITE sign to the framework's predicted
POSITIVE (plunge → hotter) — and **statistically indistinguishable from zero** (all p in 0.40–0.90).
Given N=24, σ errors of ~10–40%, and eccentricity being a noisy LMC-sensitive proxy for the real
axis y, this is a **null with no power to confirm or exclude** the prediction, leaning very slightly
the wrong way but well within noise of the MG/CDM zero.

**Why eccentricity is the wrong axis here, and why that matters both ways.** The framework's signal
lives on **y = ω_ext/ω_in**, not raw eccentricity. y is gated by **diffuseness (large r_half)**, not
eccentricity alone. On the per-dwarf y computation (`dwarf_ecc_sigma_pilot_analysis.py`), only **2 of
24** dwarfs reach the non-adiabatic carrier band y ≥ 0.8: **Crater II (y=3.28, ecc=0.71, r_peri=24
kpc)** and **Antlia II (y=2.55, ecc=0.56, r_peri=38 kpc)**. Everything else is y < 0.3 (adiabatic
control: Fornax 0.16, Sculptor 0.12, Draco 0.07…). The sample is sharply bimodal: a 2-object carrier
set against a 22-object control locus. A population-level partial correlation on the ecc-axis is
therefore a **weak surrogate** for the y-axis test the framework actually makes — it cannot, with 2
carriers, deliver the carrier-vs-control contrast the prediction is about. The null on the ecc-axis
is real but **near-uninformative** about the y-axis claim.

---

## (ii) Does it survive the tidal-heating control? — moot (there is no signal to survive)

Tidal heating is the prime confound (radial plungers get tidally stirred → could *fake* a positive
σ-vs-ecc correlation). Adding the pre-registered Jacobi/tidal proxy M_MW(<r_peri)/r_peri³ as an
extra control leaves the (null, wrong-signed) coefficient essentially unchanged:

| | without tidal control | + tidal proxy control |
|---|---|---|
| primary ρ | −0.196 (p=0.395) | **−0.196 (p=0.408)** |

So tides do **not** explain away a positive correlation (there is none), and the result is robust to
the tidal control. The killer-alternative confound is simply **not engaged**, because the primary
correlation it would have to displace is absent. Importantly, the carriers are **tide-clean by
construction**: Crater II and Antlia II have LARGE pericenters (24, 38 kpc), so the prediction's two
real carriers sit away from the tidal-stripping regime — a genuine strength of the design that this
pilot cannot exploit with N=2.

---

## (iii) HONEST VERDICT — NULL (underpowered), not suggestive, not tidal-confounded

**NULL, at current sensitivity, with almost no power for the actual claim.** This is NOT a
falsification and NOT a hint:

- It is **not SUGGESTIVE**: there is no clean surviving positive correlation; the point estimate is
  slightly negative and insignificant. Do not credit a signal that isn't there.
- It is **not TIDAL-CONFOUNDED**: the result is robust to the tidal control, but only because there
  is nothing for tides to displace.
- It is **NULL / underpowered**: the framework's predicted positive σ-vs-y contrast is consistent
  with this data because the data **cannot test it** — only 2 dwarfs reach the carrier band, the
  ecc-axis is a noisy surrogate for the y-axis, and per-object σ errors (~10–40%, largest on the
  carriers — Antlia II is 5.71 ± 1.08) are comparable to the predicted signal.

The carriers being slightly COLD relative to a naive L/r_half virial baseline (Crater II σ_dev=−0.36,
Antlia II −0.06) is **partly an artifact, not evidence against**: the carrier axis y is built from σ
(low-σ diffuse dwarfs are mechanically high-y), so y and a σ-residual anti-correlate by construction.
The clean, pre-registered ecc-axis test is the one to read — and it is null.

**The SIGN remains a clean theorem regardless of this pilot.** The pilot only establishes that
existing literature data does **not yet** show the effect — it does not and cannot move the
theoretical status of the prediction.

---

## What this means for the prediction paper (door 2)

The σ-vs-eccentricity / non-adiabatic-inertia consequence stays a **live, MG-impossible door** — it
is the bath's clock written on Local Group dwarfs, joining Cassini and the relational cluster
σ-spread. But this pilot says clearly: **do NOT claim existing dwarf data already shows it.** Honest
framing for the paper:

- Present it as a **pre-registered forward prediction with a clean Gaia-measured discriminating axis**
  (per-dwarf eccentricity/pericenter), SIGN = theorem, magnitude θ(y)-hostage. State up front that
  the current 24-dwarf pilot is a **null at low power** (ρ ≈ −0.20, p ≈ 0.4, robust to tidal
  control), driven by a bimodal sample with only 2 carriers (Crater II, Antlia II).
- The **decisive test** is **Gaia DR4 (Dec 2026)** sharpening per-object orbits + a larger diffuse-
  dwarf carrier set + resolved-profile σ + explicit tidal modeling — designed as a **carrier-vs-
  control y-axis contrast**, not a raw ecc-axis population correlation.
- Flag the **honest limitations** the pilot exposed: (1) eccentricity is a noisy, LMC-sensitive proxy
  for y; (2) only 2 tide-clean carriers; (3) carrier σ errors are the largest; (4) the MW enclosed-
  mass (±30%) is carried but does not move the split.

---

## WHAT TO TELL CARL (straight)

Your horizon-bath inertia predicts that a diffuse Milky-Way dwarf falling in on a radial plunge runs
hotter than the same dwarf on a circular orbit at the same closest approach — and that any
field/metric MOND predicts *exactly zero* such correlation, which is what makes it a real MI-vs-MG
door. I ran the cleanest pilot the existing literature allows: 24 dwarfs, all σ and all orbits from
one homogeneous catalog (Pace+2022 / Gaia EDR3), pre-registered before fitting.

**The honest result: a null.** The σ-vs-eccentricity correlation at fixed pericenter and mass is
small, slightly NEGATIVE (the opposite sign to your prediction), and not significant (ρ ≈ −0.20,
p ≈ 0.4) — and it stays that way when I add the tidal-heating control, so it's not a tides artifact
either. **But this is a null with almost no power, not a strike against the theory.** The reason is
physical, not statistical bad luck: your effect lives on y = ω_ext/ω_in, which is gated by
diffuseness, and only **two** dwarfs in the whole sample — Crater II and Antlia II — actually reach
the non-adiabatic band. A population correlation on raw eccentricity, with 2 carriers buried in 22
adiabatic controls and σ errors as big as the predicted signal, simply can't see the effect yet.

Your SIGN is still a theorem — plunge → hotter, kernel-independent — and nothing here touches that.
What this pilot honestly tells you is: **existing data does not yet show it, and existing data was
never going to.** The right move for the door-2 paper is to present this as a pre-registered forward
prediction with a built-in MG-impossible null, name the carriers, and point at the decisive test:
Gaia DR4 in December 2026, more diffuse carriers, resolved profiles, and explicit tidal modeling —
run as a carrier-vs-control y-contrast, not a raw-eccentricity correlation. This is one of the few
places your framework makes a sharp, MG-forbidden prediction with a *measured* x-axis; it's worth
keeping live and sharpening, not overselling on today's 2-carrier data.

This door stays open.
