# L68 — dipolar dark matter: the last named member of the last open hatch, and the one that passes lensing

`L68_dipolar_dm.py` + `.out` — **20 checks, 17 PASS, 3 FAIL; every one of the six controls passes and every FAIL is
the finding.** Runs in 0.1 s, exit 0. Both a₀ footings (9.3619e-11 canonical, 1.1279e-10 alt) on every dimensional
number; the Blanchet & Le Tiec (2009, Phys. Rev. D **80**, 023524) model is used through its stated Newtonian-limit
equations, with the internal potential fixed by requiring MOND and then read back.

[L61](L61_PERMITTED_BRANCHES.md) proved, branch-independently, that a theory which reproduces deep-MOND with its cold
component off **(a)**, carries a pressureless component in the CMB's amount **(b)**, and transmits its pull to baryons
no less efficiently in galaxies than at recombination **(c)**, overshoots the rotation curves pointwise. Its one hatch
is **(a)**: MOND *emergent from* the dark sector. [L67](L67_EMERGENT_MOND.md) ran the hatch for **superfluid** dark
matter: the hatch is real (the phonon force vanishes with the condensate off; the anomaly is spent once), **but it
died at the lensing gate** — phonons do not bend light, so the class predicts M_dyn/M_lens ≈ 5–7 where the measured
ratio is 1.02. L67 recorded **dipolar dark matter as in the class and untested**. This lane runs it.

---

## 0. The answer in one line

> **Dipolar dark matter escapes hypothesis (a) exactly as the superfluid does, and it does the thing the superfluid
> could not: because its MOND phantom is the polarisation charge −∇·Π, which is REAL GRAVITATING MASS (it sources T₀₀
> with only a v²/c² anisotropic stress), it PASSES the lensing gate — M_dyn/M_lens = 1.00 against the measured 1.02,
> where the superfluid gave 5.6–6.5. This is a genuine structural difference and it is the most that any emergent-MOND
> theory in this programme has achieved. But it dies in the internal sector: reproducing MOND forces the polarisation
> to sit at near-perfect anti-screening (effective permittivity ε → 0), which makes the monopole's effective
> self-gravity G_eff = G/ε diverge, so the smooth monopole that "spends the anomaly once" is a fine-tuned unstable
> equilibrium — if it stays smooth the state is unstable, if it clusters L61's overshoot (1.69) fires. The
> emergent-MOND hatch is now closed on both its named members: the superfluid at lensing, the dipolar medium in its
> internal sector.**

---

## 1. Controls — six, all PASS

| control | reproduced here | source |
|---|---|---|
| **A1** mode counts | GR **2**, GR+scalar **3**, khronometric **3**, Einstein-aether **5** | L31/L39/L61 |
| **A2** L61's overshoot | median g_pred/g_obs = **1.692** at η = 1, 2059 deep points | L61 B1: 1.692 |
| **A3** L61's ceilings | **0.355/0.276** (total-sourced), **0.582/0.486** (baryon-sourced) | L49/L50/L61 B2 |
| **A4** KiDS lensing RAR | overlap max \|dev from ν_RAR(1.2e-10)\| **0.09/0.06 dex**; across the four mass bins at 30–300 kpc universal to **0.033 dex** | Brouwer et al. 2021 |
| **A5** L67's superfluid lensing numbers | measured M_dyn/M_lens **1.02**; superfluid predicts **5.64–6.46** at the overlap | L67 E1b: 5.17–6.65 |
| **A6** Blanchet–Le Tiec's μ-function from their action | W(Π) = 2πG Π² + (4πG)²Π³/3a₀ ⇒ g = g_b + √(a₀g_b): **μ → x** deep, **μ → 1** Newtonian | Blanchet & Le Tiec 2009 |

**A6, the model-specific control, DERIVED before use.** The dipolar medium's Newtonian-limit equations (Blanchet & Le
Tiec 2009; Famaey & McGaugh 2012 §7.2) are Poisson `∇·g = −4πG(ρ_b + σ − ∇·Π)` and internal equilibrium `w(Π) = g`
with `w = dW/dΠ`. Writing `y = 4πG Π` (an acceleration), weak clustering makes σ cancel Λ on the background and drop
out of galaxy gradients, so `g = g_b + y` and the medium sits near **perfect anti-screening** `y ≈ g`. Requiring the
deep-MOND √-law fixes `W(Π) = 2πG Π² + (4πG)²Π³/(3a₀)`, whence `g = g_b + √(a₀ g_b)` — Milgrom's law with a
"simple-ν"-type interpolation, `μ → x` deep and `μ → 1` Newtonian, both limits verified symbolically. The a₀–Λ tie the
model shares with the framework is `a₀ = √Ω_Λ H₀ c/(2π) = 1.19e-10 = 1.27 a₀` — a₀ ∝ √Λ ∝ H(z), the framework's own
surviving prediction, not a new liability.

---

## 2. Hypothesis (a) fails — dipolar DM is in the class (C1)

The MOND enhancement on baryons is the phantom field of the polarisation charge: `g − g_b = 4πG Π = A_K`, and
`Π = σ|ξ|` exists only where the medium exists. Symbolically `A_K(σ = 0) = 0` — **no medium, no dipole moment, no
polarisation charge, no phantom.** **C1 PASS: hypothesis (a) fails, exactly as the brief conjectured; MOND is emergent
from the medium.** Unlike the superfluid's phonon (a force carrying negligible mass), here A_K is sourced by a MASS
density −∇·Π — and that mass is what the lensing gate tests, and it is why this member could differ.

---

## 3. Spent once (D1, D2) — the phantom IS the anomaly

The phantom `y = 4πG Π = g − g_b` equals the MOND anomaly by construction, so the polarisation supplies **~100%** of
the anomaly (median phantom/anomaly = **1.098**), not the superfluid's ≤ 7%. The double-counting risk is therefore not
a diffuse condensate — it is the **monopole σ**, a pressureless component at the CMB's Ω_c h². 

- **D1 PASS.** With the monopole smooth (weak clustering) the polarisation alone reproduces the rotation curves to MOND
  accuracy (median g_dyn/g_obs = **1.070**, +0.029 dex — a MOND fit); if the CMB-abundance monopole clustered like CDM
  it would overshoot at **1.837** (L61 B1's 1.692). **So "spent once" holds only under weak clustering.**
- **D2.** L61 B5's ordering applies directly: the monopole must be smooth in galaxies yet present and pressureless at
  recombination (ρ ≈ 2.9e-18 kg m⁻³, ~1e9× today's mean) — **denser then than in a galaxy, the wrong ordering for a
  density-triggered "stay smooth" rule.** The medium's equation of state must supply the smoothing (§6).

This is L67 caveat 3's "(H-c) without a mechanism," now attached to a specific medium and made a computation.

---

## 4. The gates

| gate | verdict | the number |
|---|---|---|
| **1 lensing vs dynamics** | **PASS — the structural difference** | E1a: stress `W/(ρ_pol c²) = ½ v²/c²` (symbolic; median slip \|Φ−Ψ\|/Φ = **4.0e-8**). E1b: M_dyn/M_lens = **1.000** against measured **1.02/1.02** (superfluid **5.6–6.5**), because the phantom −∇·Π = −σ∇·ξ is a compression of the massive medium — ordinary mass, so it sources Φ and Ψ equally. E1c: on the KiDS mass bins the phantom's lensing tracks the universal measured RAR to **0.033 dex** (the phantom **is** the RAR anomaly), where the superfluid was 0.29–0.58 dex low/spread |
| **2 Solar System** | **MARGINAL / not passed cleanly** | it HAS a computable high-acceleration limit (μ → 1), unlike the superfluid's EFT wall; bare anomaly √(a₀g_N) at Saturn is **1.8–2.0e7×** the Pitjev–Pitjeva bound, but the Galactic external field (a_ext = 1.29 a₀) quenches it to a residual quadrupole ~a₀²/g_N of **1.6–2.3e-2×** the bound — standard MOND's own tension; a sharper μ passes |
| **3 preferred frame** | **CARRIED** | the medium's rest frame u^μ; the dipole ξ^μ propagates, so the frame propagates — L61 arm (1c), realised by matter (E7) |
| **4 tensor speed** | **PASS** | one metric, matter minimally coupled ⇒ c_T = c exactly; the model modifies the SOURCE, not the propagation of gravity (E3) |
| **5 internal-sector health** | **UNSTABLE — the kill** | §6 |
| **6 clusters** | **CONTINGENT** | the phantom at a cluster's g_bar ≈ 0.4 a₀ boosts by **2.6×** against the 5.7–11 needed, a factor 3–6 short; clusters can be fit only by letting the monopole cluster **in clusters but not galaxies** — the weak-clustering hypothesis with the opposite sign, unmechanised (E4) |
| **ladder (L21)** | shape reproduced, amplitude contingent | pair boost ν = **9.7** > cluster boost **2.6**: the non-monotonicity follows from ν(a_N/a₀) as in any MOND; the pair amplitude (30.9) needs the clustered monopole too (E5) |
| **Gaia arms** | **above Arm A** | §5 |

### 4.1 The lensing pass, stated precisely

The one emergent-MOND mechanism whose anomaly carries its own gravitating mass is gravitational polarisation. The
phantom `−∇·Π = −σ∇·ξ` is a compression of the massive medium, so it is ordinary non-relativistic mass: it sources T₀₀
fully, and its only pressure is the internal potential `W ~ y²/8πG`, which is `½ v²/c²` of the phantom rest-energy
density (median 4.0e-8 on SPARC). Hence Φ = Ψ up to v²/c² and **M_dyn/M_lens = 1 + O(v²/c²) = 1.00**. The contrast with
the superfluid is exact: there the anomaly was a *force* with no mass, so M_lens missed it entirely and the *same*
v²/c² was the whole (tiny) lensing signal, giving M_dyn/M_lens = 5–7; here the anomaly *is* mass, so v²/c² is a
correction to a ratio of 1. **The lane does not die at lensing** — a genuine structural difference from L67.

---

## 5. The registered Gaia arms (E6)

Dipolar DM reproduces standard MOND with ν(y) = 1 + 1/√y, so it predicts a wide-binary anomaly through the
external-field effect. Standard QUMOND sky-average at the registered a_N,ext = 1.289 a₀:
`γ_v = √(ν(y_ext)(1 + ⅓ d ln ν/d ln y)) = ` **1.317** (footing-independent in a₀ units).

**E6 FAIL — the class's γ_v falls inside neither registered arm.** γ_v = 1.317 sits **3.2–4.8σ** above Arm A's upper
edges (1.1814/1.2267) and above the 1.23 no-verdict edge, **11σ** above Newton — like the superfluid's 1.27–1.34, a
consequence of the slow simple-ν transition. **A DR4 wide-binary result inside Arm A (1.16–1.23) or Newtonian is
evidence against the dipolar phantom; DR4 cannot confirm it.** This is the point-field EFE asymptote (Amendment-9
status), like the superfluid's.

---

## 6. The internal sector — mode count and the load-bearing instability (PART G, G1)

**Mode count.** Beyond GR's 2 tensor modes the medium adds a pressureless fluid (the monopole σ: 0 new *propagating*
gravitational modes, it is dust) and a dynamical dipole vector ξ^i (≤ 3 components, one constraint in the covariant
theory). Total field content **2 (tensor) + 3 (dipole) = up to 5**, of which the longitudinal dipole is load-bearing.
The isolated dipole oscillator is stable (W″ = 4πG + 2(4πG)²Π/a₀ > 0); the pathology is in the coupled system.

**The instability (G1 PASS — the finding).** MOND requires the medium to sit near **perfect anti-screening**, `y ≈ g`,
so the residual g_b is small. The medium's effective gravitational permittivity for its own density perturbations is
`ε = dg_b/dg = 1 − 4πG/W″(Π) = (2g/a₀)/(1 + 2g/a₀)`, which → 0 deep in MOND:

| g | ε | G_eff/G = 1/ε |
|---|---|---|
| 0.01 a₀ | 0.020 | **51** |
| 0.1 a₀ | 0.167 | 6.0 |
| 1.0 a₀ | 0.667 | 1.5 |

So the monopole's effective Newton constant diverges as the system goes deeper into MOND, and its collapse time is
shorter than standard free-fall by **√ε = 0.41** at 0.1 a₀. **The MOND-tuned medium is MORE Jeans-unstable exactly
where it must stay smooth.** "Weak clustering" is not a stable state but a fine-tuned unstable equilibrium — a
polarisation requiring an unstable configuration is not a theory.

### The pincer, stated as the theorem it is

> **Dipolar dark matter escapes L61 by making the phantom real gravitating mass, so it PASSES lensing (§4.1) — but the
> SAME construction that makes the polarisation nearly cancel the field (perfect anti-screening, needed for MOND)
> makes the monopole's self-gravity diverge, so the smooth monopole that "spends the anomaly once" (D1) cannot be
> maintained. If the monopole stays smooth the state is unstable; if it clusters, L61's overshoot (1.69) fires. The
> lensing pass is real and structural; the death is in the internal sector, not at lensing.**

---

## 7. Verdicts

**F1 FAIL** — dipolar DM escapes (a) [C1], PASSES the lensing gate [E1] (the structural difference), and passes tensor
speed [E3], but dies in the internal sector [G1]; Solar System marginal [E2], clusters and "spent once" contingent
[E4/D1]. **F2 FAIL — dipolar dark matter, the last named member of the last open hatch, is NOT ALIVE through every
gate: DEAD at the internal-sector-health gate, NOT at lensing.** The emergent-MOND hatch is now closed on both its
named members — the superfluid at lensing, the dipolar medium in its internal sector.

### Three-sentence verdict

**Dipolar dark matter escapes L61's hypothesis (a) exactly as the superfluid does — its MOND force is the phantom of
the polarisation charge and vanishes with the medium off — and it does something the superfluid could not: because
that phantom is real gravitating mass (the polarisation −∇·Π sources T₀₀ with only a v²/c² anisotropic stress), it
PASSES the lensing gate that killed the superfluid, M_dyn/M_lens = 1.00 against the measured 1.02 where the superfluid
gave 5.6–6.5.**

**But it dies in the internal sector: reproducing MOND requires the polarisation to sit at near-perfect anti-screening
(ε → 0), which makes the monopole's effective self-gravity diverge, so the smooth monopole that "spends the anomaly
once" is a fine-tuned unstable equilibrium — if it stays smooth the state is unstable, if it clusters L61's overshoot
(1.69) fires.**

**Its distinctive Gaia number γ_v = 1.32 sits above the registered Arm A band (1.16–1.23), like the superfluid's
1.27–1.34, so a DR4 wide-binary result inside Arm A or Newtonian would count against it and DR4 cannot confirm it;
nothing here favours any framework over ΛCDM, κ = ½ remains fitted, and a₀ ∝ √Λ ∝ H(z) — which the model shares — is
the framework's own surviving prediction.**

---

## 8. Caveats, stated rather than buried

1. **The model is used through its Newtonian-limit equations, with W(Π) fixed by requiring MOND and read back.** The
   deep-MOND cubic W(Π) = 2πG Π² + (4πG)²Π³/3a₀ reproduces Blanchet & Le Tiec's μ-function (A6); the higher-order
   interpolation that sharpens the Solar-System transition is not modelled, and E2's verdict is stated as
   transition-region-dependent, exactly as for standard MOND.
2. **The lensing pass is a stress-tensor estimate, not a full relativistic lensing solve.** It fixes the *scale* of
   the slip — ½ v²/c² — which is what the genericity claim needs; the load-bearing companion statement (the phantom is
   a compression of the massive medium, so it is ordinary T₀₀ mass) is exact.
3. **The internal-sector instability is the Newtonian coupled-system mechanism** (ε → 0 ⇒ G_eff → ∞), self-consistent
   with the W(Π) derived here and faithful to why Blanchet & Le Tiec invoke "weak clustering" in the first place. The
   full covariant ghost/gradient analysis of the dipole kinetic sector is more involved and is not claimed here; the
   gravitational instability of the *required configuration* is what is computed, and it is decisive on its own.
4. **The equation of state was checked, not assumed.** The recorded superfluid cosmological closure
   (`superfluid_route_gates_2026`) is **not reused** — dipolar DM's background is w ≈ 0 monopole + w = −1 internal
   potential (CDM + Λ), a *different* EoS; the tension is instead the density-ordering of D2 and the instability of G1,
   both derived here.
5. **Clusters and the ladder amplitude are contingent, not computed fits** — they require the monopole to cluster
   differentially (in clusters, not galaxies) with no scale supplied, the same unmechanised (H-c) as D1/D2.
6. **The Gaia number is the point-field EFE asymptote** (Amendment-9 status), footing-independent in a₀ units; a full
   nonlinear solve would move it at the ~0.05 level and it stays above Arm A.
7. **Nothing here favours any framework over ΛCDM and nothing here constrains ΛCDM.** The monopole abundance is
   ΛCDM's, imported wholesale; κ = ½ remains **fitted**; a₀ ∝ H(z) — which this model shares as a₀ ∝ √Λ — remains the
   framework's surviving distinctive prediction, untouched by this lane.

---

## 9. Reproduction

```
python3 fable_independent_2026/L68_dipolar_dm.py
```

Exit 0, 0.1 s. **20 checks: 17 PASS, 3 FAIL** (E6, F1, F2 — the findings). Six controls rebuild the four mode counts,
L61's overshoot and both ceilings, the KiDS lensing pipeline, L67's superfluid lensing numbers, and Blanchet & Le
Tiec's μ-function from their stated action — each from committed data or from scratch in sympy. Nothing under
`closure_2026/` or the lead's directories is imported or executed.
