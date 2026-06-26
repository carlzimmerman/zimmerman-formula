# Color-channel lepton-selector (Task C, the cross-fermion wall) — VERDICT: NO natural color-selector; the selector is ELECTRIC CHARGE; wall STANDS

**Date:** 2026-06-25
**Scripts:** `color_channel_selector.py` (sympy/mpmath dps=50), plus a Sumino-grounded
residual check. Primary source confirmed: Sumino arXiv:0812.2103 / 0903.3640.

## The question
Color N_c=3 cancels in Q (a ratio) — corpus-closed. But a *channel-structured* color
weight (color-singlet leptons vs color-triplet quarks entering the family-gauge /
dS-Unruh sum **differently**, not as a cancelling overall N_c) was never tested.
Is there a NATURAL color-channel weight that lands leptons at channel-equipartition
(g=1 ⟺ Koide) while pushing quarks off — or must any such weight be hand-tuned?

## Setup (sympy/mpmath-exact, reproduced)
The S3 1+2 (singlet+doublet) decomposition of the √-mass vector gives the geometric
ratio **g = a_doublet/a_singlet = r_circ/√2**, with **Q = 1/3 + g²/3**. Koide ⟺ **g=1**
(equal per-irrep / per-channel amplitude). Reproduced: leptons g=0.99999 (Q=0.66666),
up g=1.2437 (Q=0.8489), down g=1.0928 (Q=0.7314). A per-CHANNEL weight (singlet by w_S,
doublet by w_D) gives **g_eff = (w_D/w_S)·g_bare** — the only non-trivial color hook,
since an overall color factor cancels (re-proven exact: up g unchanged under ×7.3).

## The decisive no-go — color is doubly blocked
A color-channel selector would have to do TWO things; **both are impossible naturally:**

1. **Keep leptons-only at Koide.** Any color-defined exponent f(N_c) with the cleanest
   forms (N_c−1, (N_c−1)/2, 1−1/N_c, log₂N_c, the fundamental Casimir 4/3) sets
   **f=0 for every color singlet**, so it does nothing to leptons (good) — but it equally
   does nothing to the **colorless NEUTRINO**, predicting it at g=1/Koide too. Neutrino g
   is a free function of m₁ (g=0.87→0.08 as m₁=0→0.05 eV), generically NOT 1. So
   "color-singlet → Koide" is **falsified by the neutrino.** The two colorless sectors
   (charged lepton, neutrino) do not both obey Koide → "colorless" is not the selector.

2. **Split up from down.** Up and down are the **identical color triplet** (N_c=3, fundamental).
   Every color-defined f gives f_up = f_down → predicts g_up = g_down EXACTLY. But
   g_up=1.2437 ≠ g_down=1.0928. Color is structurally blind to the up/down difference;
   that splitting is electroweak/Yukawa.

Any weight that nonetheless reproduces the three measured g's needs **3 independent
w_D/w_S** — the generic-fit trap (fits by construction, predicts nothing).

## What the selector ACTUALLY is — confirmed from Sumino's primary source (both-ways CREDIT)
Sumino's real mechanism (0903.3640, fetched): the family-gauge loop
**δm_i = −(3α_F/8π)[log(μ²/v_i²)+c] m_i** cancels the QED IR-log
**+(3α/4π) Q_em² log(...) m_i**. The QED side carries **Q_em²**. With a charge-blind
family coupling α_F, the residual is **(α_F/2 − α·Q_em²)**:
- |Q_em|=1 (leptons) → residual = 0 (Koide protected) ✓
- up Q_em²=4/9, down Q_em²=1/9 → residuals 0.556α, 0.889α (broken, and DIFFERENTLY) ✓

So the lepton-selector is **electric charge Q_em²**, real and natural, and it splits
up from down (4/9 vs 1/9) — exactly what color CANNOT do. Two further Sumino facts kill
the color route: (a) the cancellation α≈¼α_F is a **TUNING** Sumino himself calls "an
accidental factor (or parameter tuning)," motivated by sin²θ_W≈¼ EW-unification, **not a
symmetry**; (b) **QCD color does not enter the charged-lepton calculation at all.** A
color-enhanced family loop (×N_c=3 for quarks) makes the quark residual LARGER
(2.6α, 2.9α), pushing quarks further from Koide, never to zero without per-quark tuning.

## Verdict (both ways)
- **No manufactured win:** there is NO natural color-channel weight that is
  lepton-selective. Color is doubly blocked (colorless includes the non-Koide neutrino;
  up/down share color). Any color selector is hand-tuned per sector → predicts nothing.
- **No manufactured deficit:** the lepton-selector the task hoped color might supply DOES
  exist and is natural — it is **electric charge Q_em²** (Sumino's QED IR-log), confirmed
  from the primary source. It even splits up from down. But it lives in the **electroweak/
  charge sector + the U(3) conjugate (3,1)/(3̄,−1) assignment**, which the framework's
  geometric/thermal (color-blind, EP-blind) dS-Unruh spine does not carry, and the
  cancellation itself is a tuning, not a derivation.

**The cross-fermion wall STANDS.** Color is not the lepton-selector; electric charge is,
and it sits in Sumino's posited family-gauge dynamics, not on the a₀/Z/κ/dS-Unruh spine.
Quarantine held (2/3, √2, g=1 enter only as the empirical target, never as an input).
