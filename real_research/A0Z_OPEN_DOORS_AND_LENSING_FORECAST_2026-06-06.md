# Open doors for a₀(z): the one live test (z-binned lensing RAR), and two of my overclaims retracted

*C. Zimmerman, 2026-06-06. "Keep going — any open doors?" Pursued with two adversarial agents (a CMB/novelty
referee, an open-doors scan). Result: one genuinely new conceptual framing that I then had to **correct twice**, and
one genuinely actionable observational door — quantified. Honest throughout; the corrections are the point.*

## 1. "MOND switches on late" — true, but NOT novel and NOT a CMB win (two retractions)

I proposed: since `a₀∝√ρ_DE`, the MOND scale relative to cosmic dynamics tracks `a₀(z)/[cH(z)] ∝ √Ω_DE(z)` — MOND is
full-strength today (Ω_DE=0.69) and ~0 in the matter era, so MOND is a **late-time, dark-energy-era phenomenon**. The
clean statement is **correct** (and is *why* `a₀~cH₀` today — because Ω_DE~1 now). But the agent caught two overclaims:

- **RETRACTED — not a CMB advantage.** I claimed the framework is "CMB-safe in a way constant-`a₀` MOND is not"
  because `a₀→0` at recombination. **Wrong.** At recombination the characteristic acceleration is **g ≈ 20 a₀**
  (Sanders astro-ph/0509532; standard RelMOND number), so constant-`a₀` MOND is *already* deep-Newtonian there
  (MOND boost ~5%). Driving `a₀` smaller takes g/a₀ from ~20 to ~∞ — both Newtonian. The real MOND-CMB problem is the
  **3rd-peak forcing** (a gravitating dark-matter-like component), which is **`a₀`-independent** and inherited
  unchanged. My script's crude sound-horizon estimate (g/a₀~1.8) was the error; the literature value is ~20. *No CMB
  win.*
- **RETRACTED — not novel.** `a₀=√(8πGρ_DE/3)` with exactly this "MOND weakens in the matter era" behaviour **is
  Limbach, Psaltis & Özel 2008** (arXiv:0809.2790) — the same paper I'd cited for the √ρ_DE-vs-cH test. They wrote the
  coupling, derived the sign behaviour (constant for w=−1, declining for w>−1, `a₀/cH` falls into the past), and even
  marginally favoured it over `cH`. **The framework's kernel is their 2008 proposal.** Its only fresh pieces are the
  specific value `c²√(Λ/32π)` (coefficient closed/moot), the DESI-`w₀wₐ` evaluation, and the non-monotonic z≈0.4 bump.

*(Script `a0z_switches_on_late.py` rewritten to state this honestly — the √Ω_DE framing kept as pedagogy + LPO2008
credit, the CMB-advantage and novelty claims removed.)*

## 2. Open-doors scan — exactly one survives

A systematic scan of every observable that could detect a ≤26% change in `a₀` between z=0 and z~3:

| door | verdict | why |
|---|---|---|
| **z-binned weak-lensing RAR** (KiDS/DES/HSC) | **LIVE — the one actionable door** | lensing measures g_obs directly: no inclination/pressure-support/beam-smearing (the systematics that gave kinematics a *spurious* rise). Brouwer+2021 reached deep-MOND with 259k lenses at 0.1<z<0.5 but never binned in z. Public data; unpublished. |
| cluster outskirts vs z | rejected | the cluster scale is `g‡≈17×a₀` (the "cluster problem"); a 26% shift is buried under a 1700% offset of unknown z-dependence |
| structure growth fσ8(z) | rejected | MOND overshoots σ8 by ~2× and is patched with an 11-eV sterile-ν; a 26% `a₀` shift is fully degenerate |
| intermediate-z kinematics (dwarfs/IFS) | rejected — **the trap** | this door is *occupied* and gives the WRONG sign: MUSE-DARK III rises (contaminated, ΛCDM-degenerate). New kinematic surveys will reproduce the same spurious rise. |
| the z≈0.4 bump to few-% | not pre-2028 | DESI-PV is z~0.07; Euclid spectroscopy is 0.9<z<1.8 (skips it); 4MOST/WALLABY too shallow |
| BBN / 21-cm / PTA / GW / dSph-EFE / UDGs | rejected | no clean z-leverage on `a₀` |

## 3. Lensing-RAR forecast — it sharpens the Verlinde kill, but can't see the bump

Forecast (`a0z_lensing_forecast.py`), per-bin `a₀` precision = statistical (√N from Brouwer's 259k @ 8%) ⊕
circumgalactic-gas systematic floor. Signal across the lensing window z=0.15→0.45: **framework +1.9% (the bump),
flat 0%, Verlinde +18.8%.**

| scenario | per-bin σ(a₀) | Verlinde signal | framework bump |
|---|---|---|---|
| Brouwer KiDS now (259k, 2 bins, gas 5%) | 12% | 1.1σ | 0.1σ (below floor) |
| DES+HSC+KiDS (~1.5M, 3 bins, gas 5%) | 8% | 1.7σ (hint) | 0.2σ (below floor) |
| LSST/Euclid (~10M, 4 bins, gas 3%) | 4% | **3.4σ (DETECT)** | 0.3σ (below floor) |

So the lensing door **cleanly tests the rising rivals** (Verlinde reaches 3σ at LSST — a cleaner Verlinde test than
the contaminated kinematics) but **cannot see the framework's +2% bump** in the z<0.5 window with any near-term data:
the bump sits below the gas-mass systematic floor (~3–5%) even at LSST precision.

## 4. The honest bottom line — what we actually need

**The framework's distinctive signal is below the floor of every available and near-term probe**, for a structural
reason: it is **too small where clean data exist** (the +2% bump at z<0.5, accessible to lensing but under the gas
floor) and **the clean data don't exist where it is large** (the −25% decline at z≥2, accessible only to deep-MOND
kinematics, of which there is *no* example — every confirmed z≥2 disk is high-acceleration). "Safe but untested" is
therefore **not a temporary state** — it persists until one of:

- **(a)** a sub-3%, gas-controlled lensing RAR at z~0.3–0.5 (LSST/Euclid + improved circumgalactic-gas modeling), or
- **(b)** a clean deep-MOND (g≪a₀) rotation curve at z≳2 (a future ELT/JWST target that does not yet exist).

**Actionable now (the one new result reachable from public data):** z-bin the existing lensing RAR (Brouwer pipeline
or Mistele-McGaugh 2024 exact deprojection, arXiv:2310.15248) across z=0.15/0.30/0.45 — it will **sharpen the
exclusion of the rising rivals** (Verlinde/QI), the framework's one robust empirical win, with a clean method that
the kinematic tests lacked. It will *not* confirm the framework (the bump is too small), but it removes the last
refuge of the rising-`a₀` competitors using data immune to the systematics that have muddied every kinematic test.

**Net:** the open doors are now fully mapped. The framework is a falsifiable hypothesis (Limbach-Psaltis-Özel 2008's
`a₀∝√ρ_DE`, evaluated with DESI's evolving DE) whose distinctive prediction is real but **sub-floor for a decade**
absent new instruments; its rising rivals are excludable now and more cleanly via lensing; and its theoretical
realization remains blocked (singular-surface ghost). The science is honest, bounded, and — on the prediction that
matters — waiting on data that do not yet exist.

**Sources:** Limbach/Psaltis/Özel 2008 [0809.2790]; Sanders, MOND & Cosmology [astro-ph/0509532]; Brouwer+2021 KiDS
lensing RAR [2106.11677]; Mistele & McGaugh 2024 deprojection [2310.15248]; MUSE-DARK III [2604.22613];
Tian+2020 cluster RAR [2001.08340]; AeST CMB [2007.00082].
