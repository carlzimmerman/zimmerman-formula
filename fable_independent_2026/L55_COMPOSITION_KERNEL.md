# L55 — the composition kernel: can the kernel be suppressed where cold matter dominates?

`L55_composition_kernel.py` + `.out` — **28 checks, 9 PASS, 19 FAIL; every one of the six controls passes and
most of the FAILs are the finding.** Runs in 3 s. Both a₀ footings (9.3619e-11 canonical, 1.1279e-10 alt) on
every dimensional number.

L49 found the minimum addition is a cold collisionless component; it satisfies the whole cluster
specification, leaves the clock tachyon satisfied identically and repairs the CMB and growth exactly, but the
three admissible cold fractions have an empty intersection. L50 re-sourced the MOND scalar on the baryons
alone, moved both windows it was meant to move (galaxies and clusters now agree to 0.1σ), and still failed:
the CMB window cannot move, and the gap only narrowed from 2.82× to 1.72×. Both lanes named the same
remaining move — **suppress the kernel where the cold component dominates** — and L50 computed what it needs:
the kernel's effective strength below about ½ at f = 1.

This lane tests the only way to get that from a field-theory variable rather than by hand: **let the kernel's
argument depend on the baryon fraction f_b = ρ_b/(ρ_b + ρ_c) — a ratio of two species rather than any single
environmental scalar.**

---

## 0. The answer in one line

> **The mechanism is genuinely outside L6's closed class, and it does open the three-way intersection — the
> first time in this sequence that the pincer opens at all. But it opens it by switching the kernel off where
> MOND is needed. At the abundance the CMB fixes, the ΛCDM halo alone already supplies 109% of the observed
> deep-MOND anomaly, so the kernel's share is capped at W ≤ 0.389 on both footings, against 0.888 in the
> deposited theory — and that cap is a bound, not a failed search: eleven suppression functions on two
> different composition variables all collapse onto one number.**

---

## 1. The controls, first — L50's windows and L6's closure, both rebuilt

Six controls, all PASS. Without these the lane would be quotation rather than verification.

| control | reproduced here | published |
|---|---|---|
| **X1** cluster amount + residual | M_dark/M_bar = **5.73 ± 0.68**, f_bar = **0.149**, post-kernel residual **3.09 / 2.76** M_bar | L49 X1/X6, L50 A1/A2 |
| **X2** SPARC machinery | kernel **0.145 / 0.142** dex at medians **+0.030 / +0.003**; abundance-matched halo alone **0.171** at **−0.026** | L49 X8, L50 A3 |
| **X3** L50's windows and gap | galaxies ≤ **0.582 / 0.486**; clusters **0.569 ± 0.130 / 0.508 ± 0.133**; gap **1.72× / 2.06×**; at b = 0.20 clusters want 0.893 ± 0.158 = 0.7σ from the CMB | L50 §4 |
| **X4** L50's sharp form | a uniform suppression to **s ≤ 0.495 / 0.439** is what the galaxy window requires at f = 1 | L50 D8 |
| **X5** L6's overlap horn | acceleration \|z\| = **24.9** at 100% overlap; density **12.8** at 100%; potential **17.7** at 47%; mass **7.9** at 11% | L6 S0–S3 |
| **X6** L6's ordering horn | background **1057×** below cluster outskirts in ρ_b, Φ and g_bar → 0; **E_out = 1.82 / 1.68** = 4× the BBN bound | L6 S4 |

**L6's closure reproduces on its own terms, both horns.** Nothing below leans on a number that was not
rebuilt from the committed data with independent code.

---

## 2. The crux, settled first: is a baryon-fraction kernel outside L6's closed class?

L6 closed S(X) for X a **single** environmental scalar — potential, baryon density, acceleration, enclosed
mass — on two horns. L6's own closing note records that *"a non-monotone S, or S of two variables at once, is
a fitted function rather than a screening mechanism. Neither is claimed closed here."* So the class is
formally untested; three tests decide whether it collapses in practice.

| check | result |
|---|---|
| **B1** does f_b collapse into a function of one L6 variable? | **FAIL (it does not).** At the same acceleration, potential, baryon density or enclosed baryon mass the two populations sit at **different** f_b, separated by \|z\| up to **60**. f_b carries information about a second species that none of L6's variables contains |
| **B2** does the cosmological-ordering horn fire? | **FAIL (it does not).** Cluster outskirts f_b = **0.1486**; the homogeneous background is **0.1556** — a ratio of **1.05**. In every L6 variable the background is orders of magnitude beyond cluster outskirts; in f_b it is indistinguishable from them. This is L7's measured f_bar = 0.149 vs cosmic 0.156 read as a statement about the screening variable: the chain galaxy → cluster → cosmos **terminates** in f_b |
| **B3** can the BBN horn bite? | **FAIL (it cannot).** s ≤ 1 is a *suppression*, the opposite sign to L6's enhancement; and the kernel is an **additive a₀-scale term**, not a rescaling of G — its fractional size at BBN-era accelerations is **6.1e-5**, so switching it off entirely changes G_eff by 1 part in 2e4 |
| **B4 [THE CRUX]** is it inside L6's class? | **FAIL — it is NOT inside it**, on three independent grounds |

**Being outside a closed class is not evidence that it works.** The mechanism therefore has to be tested on
its own, which is §3–§5.

---

## 3. The function — and the two horns

**C1, the thing the brief flagged as most likely to kill it, checked before any window was recomputed.**
2059 of 2786 SPARC points (74%) are deep-MOND (g_bar < a₀). At the cold abundance the CMB fixes, those points
sit at:

- **f_b = 0.255** on the **enclosed-mass** reading (the one that sets the rotation curve) — 89% of them below
  one half, i.e. **cold-dominated**. **The suppression switches on exactly where the kernel is supposed to
  work.** C1 FAIL.
- **f_b = 0.800** on the **local-midplane** reading — a thin disc is locally baryon-dominated even where the
  *enclosed* mass is not. **C4 PASS:** the local reading rescues the disc across h_z = 0.15–1.0 kpc (median
  f_b 0.89 → 0.55).

These are the two horns and they answer the question oppositely. Both are carried.

**C2 FAIL.** L6's own overlap machinery run in the new variable: at the same enclosed f_b, clusters and
galaxies require kernel strengths differing at **\|z\| = 20.7** over 100% overlap (local reading: 9.8). L6's
overlap horn does fire in the new variable, for the same reason it fired in the old ones.

**C3 FAIL.** There is no threshold to be sharp about: **58%** of the deep-MOND galaxy points fall inside the
cluster f_b range, so any monotone s that switches off at cluster outskirts switches off at those galaxy
points too.

---

## 4. The windows — and the pincer opens

| variant | galaxies (can / alt) | clusters b = 0 | clusters b = 0.20 | CMB |
|---|---|---|---|---|
| **H1** enclosed f_b, s = f_b³ | **1.372 / 1.362** | 1.054 ± 0.126 | 1.365 ± 0.157 | 1.000 |
| H1′ enclosed, f\* = 0.5, n = 8 | 1.286 / 1.273 | 1.055 ± 0.125 | 1.365 ± 0.157 | 1.000 |
| H2 local f_b, s = f_b³ | 1.001 / 0.931 | 1.054 ± 0.126 | 1.365 ± 0.157 | 1.000 |
| **H2′** local f_b, s = f_b⁴ | **1.073 / 1.018** | 1.055 ± 0.125 | 1.365 ± 0.157 | 1.000 |
| L50 control (no suppression) | 0.582 / 0.486 | 0.569 ± 0.130 | 0.893 ± 0.158 | 1.000 |

- **D1 PASS.** The galaxy ceiling moves on **both** readings and by a large margin — the first move in the
  L49–L50–L55 sequence that lifts it past f = 1.
- **D2 PASS — the pincer opens.** On H1, H1′ and H2′ the ceiling clears f = 1 on both footings, clusters need
  **1.054 ± 0.126** at b = 0 (**0.4σ** from the CMB's 1.000), and the CMB fixes 1.000 ± 0.010. **This is a
  genuine positive and is reported before it is priced.**

### 4.1 What it costs — and the trade-off is a bound, not a search

**D3 FAIL — the whole question.** The ΛCDM halo at the CMB's own abundance already supplies **109%** of the
observed deep-MOND anomaly on its own, so the kernel's remaining room is whatever the tolerance allows:

| term | share W of the observed deep-MOND anomaly |
|---|---|
| the kernel, deposited theory at f = 0 | **0.888** (the kernel *is* the anomaly) |
| the ΛCDM halo alone at f = 1 | **1.090** |
| the kernel, H1 enclosed horn at f = 1 | **0.016 / 0.019** |
| the kernel, H2′ local horn at f = 1 | **0.344** |

**D4 FAIL — and this is the general form.** A uniform suppression, so the result cannot depend on which
variable is screened:

| s | f_max canonical | f_max alt | W | rms at f = 1 |
|---|---|---|---|---|
| 1.000 | 0.582 | 0.486 | 0.888 | 0.264 |
| 0.600 | 0.910 | 0.847 | 0.533 | 0.220 |
| **0.439** | **1.041** | **0.999** | **0.390** | 0.204 |
| 0.300 | 1.155 | 1.126 | 0.266 | 0.191 |
| 0.000 | 1.411 | 1.411 | 0.000 | 0.171 |

> **f = 1 admissible on both footings requires s_eff ≤ 0.438, at which W ≤ 0.389.**

And **eleven genuine functions of f_b, on both readings, land on that same uniform curve at their own median
deep-MOND strength to within 0.122 in f_max and 0.056 in W.** The galaxy data see exactly **one** number —
the kernel's effective strength where the anomaly is — and every choice of variable is only a different way
of setting it. This generalises L50 D8 from a uniform suppression to **any function of any variable**,
environmental or compositional.

**D5 FAIL — what survives is not the theory's kernel.** In the deep-MOND limit Δ(x) → √x, so
s·a₀Δ(g/a₀) = a₀′Δ(g/a₀′) with **a₀′ = s²a₀ exactly** (verified to 1e-2 in the strict limit; only roughly on
the data, 29–132%, because SPARC is not yet asymptotic — both reported). So the surviving term's own MOND
transition sits at **a₀′ ≤ 0.192 a₀**, a factor **5.2** below where the observed relation turns over. For it
to still set that scale the action would need **κ = 2.60** rather than the fitted 0.4998. What happens
instead is D7: the BTFR zero point is the halo's, so **the framework's a₀ is no longer measured by galaxy
dynamics and κ loses the 0.465 ± 0.076 BTFR anchor it is quoted from.** κ is fitted rather than derived, so
this is not a falsification — it is the loss of the coincidence that motivated the tie.

**D6 FAIL, and it cuts the other way — stated because the generous criterion is doing real work.** At f = 1
the halo *alone* gives 0.171 dex against the kernel's 0.145, so **no kernel treatment whatever meets L49's
strict criterion at f = 1.** That is a statement about the ΛCDM halo library's scatter, not about this
mechanism, and it means the strict criterion cannot test it. The generous criterion is carried throughout,
exactly as L49 and L50 carry it.

**D7 FAIL — the three distinctive galaxy-scale statements, at H2′:**

- deep-MOND BTFR zero point **+0.196 → +0.410 dex**, now set by the halo rather than by V⁴ = G M_b a₀;
- **36%** of SPARC points have the halo term alone above the bounded-boost ceiling C a₀ = 6.06e-11 m s⁻², so
  the falsifier the programme calls the one ΛCDM structurally cannot make is a statement about an
  unobservable (L49 N3, unchanged);
- the kernel is above half strength at **41%** of deep-MOND points.

### 4.2 The gates, and the new one this mechanism creates

**D8 FAIL, 13 of 14.** Everything the deposited theory passes still passes at the exhibited point (H2′,
s = f_b⁴, f = 1) — Cassini, the Saturn phantom mass (margin 17 603×), α₁ = −4.00e-6 and α₂ = −2.02e-7,
c_T = c, mode count, the clock tachyon (Q̄ = 0 remains an exact solution because Y = 0 on a homogeneous
slice), lensing = dynamics, BBN, rotation curves, the cluster amount at 0.4σ — **including the two gates L49
and L50 fail outright, the CMB cold-matter density and linear growth.** Conservation also passes:
diffeomorphism invariance does not care how many matter scalars J reads, so L50 B2's argument carries.

**D9 FAIL — the gate this mechanism creates, and it is the largest unpaid bill.** If the kernel's strength
reads ρ_c, then δS/δρ_c contains (∂s/∂ρ_c)J(Y): **the cold component acquires its own fifth force.** For
s = f_b^p, ∂ln s/∂ln ρ_c = −p(1 − f_b), which at p = 4 is −2.0 at f_b = 0.5, and the kernel supplies W = 0.34
there, so the extra acceleration is of order **0.7 of the anomaly itself — O(1), not a correction.** Every
halo profile used in this lane (Moster abundance matching, Dutton–Macciò concentrations, NFW) is built for
dust in Newtonian gravity, so **under this action the halo library is not self-consistent** and every window
would have to be recomputed with a re-equilibrated halo. This is an order-of-magnitude estimate, not a solved
profile, and it is the reason the D2 opening should not be read as a working theory.

---

## 5. The price

**E1 FAIL — worse in kind than L50's, though not in laboratory magnitude.** The violation is now twofold:
(a) baryons feel the kernel and the cold component does not (L50's, inherited); (b) **new here — the force on
a baryon depends on how much other-species matter is nearby**, so the field a test particle feels is not a
functional of the metric and the scalar alone. Magnitude η = 0.137 at f = 1. Neither is a laboratory or
Solar-System effect: baryons and photons stay minimally coupled to the single metric g, so γ_PPN, Eötvös and
MICROSCOPE are untouched, and there is 3.8e-15 M⊙ of cold matter inside Saturn's orbit against 6.7e-11
(17 603× margin). **The cost is structural, not empirical.**

**E2 FAIL — one new free function, and the number it must hit is set by astrophysics.** s(f_b) carries a
scale and a sharpness, neither predicted by the action, and no symmetry selects it. Worse: D4 fixes
s_eff ≤ 0.438, and on the local reading at fixed p = 4 that number runs from **0.62 at h_z = 0.15 kpc to 0.09
at h_z = 1.0 kpc** — a factor 7.1. **The mechanism's success is controlled by disc scale height, about which
the action says nothing.**

**E3 FAIL, with the fairest statement of what survives.** The kernel contributes more than 10% of the total
acceleration at 93.4% of SPARC points in the deposited theory, at **65.1%** on the local horn at f = 1 — so it
is not switched off — but D5 and D7 show that what survives is a term whose own MOND scale is five times too
small and whose distinctive predictions are the halo's. On the **enclosed** horn it is switched off entirely:
above half strength at **0%** of deep-MOND points, W = 0.016.

---

## 6. The theorem

**V1 FAIL, V2 FAIL.**

> The observed galaxy-scale anomaly is **one number per point**, g_obs − g_bar. At the cold abundance the CMB
> fixes, the abundance-matched ΛCDM halo alone already supplies **109%** of it and reproduces SPARC at 0.171
> dex with median −0.026. Whatever the MOND kernel adds at that abundance is therefore an overshoot, and the
> galaxy window can be reached only by suppressing the kernel to **s_eff ≤ 0.438** where the anomaly is
> measured. **That bound is a statement about the data and the halo, not about the kernel's functional
> form** — D4 verifies that eleven suppression functions keyed to two different composition variables all
> reduce to the same one number as far as the galaxy data are concerned. It is therefore invariant under
> every remaining move: re-sourcing the scalar (L50), screening on an environmental scalar (L6), or keying
> the kernel to the species composition (this lane). Each is only a different way of choosing s_eff.

> **Hence, quantitatively:** at Ω_c h² = 0.1200 the kernel may supply at most **W = 0.39** of the observed
> deep-MOND galaxy anomaly, against 0.89 in the theory without a cold component; and since a partial
> suppression is exactly degenerate with a smaller a₀ in the deep limit, the surviving term's own MOND
> transition sits at ≤ 0.19 a₀ while the turnover, the BTFR zero point and the bounded-boost ceiling are all
> the halo's. **A full cold abundance and a MOND kernel doing the galaxy work are alternatives, not
> complements** — not because the pincer stays shut, but because they are two explanations of the *same*
> measured excess, and the excess can only be spent once. The theory can have the CMB, the clusters and the
> growth of structure, at which point its kernel is at most a third-strength correction whose own MOND scale
> is five times too small and none of whose distinctive predictions survives as a test; or it can have the
> galaxy phenomenology at f = 0, at which point S_eff = 0 exactly and it fails the CMB and linear growth
> outright.

---

## 7. Three-sentence verdict

**The mechanism is genuinely new and the pincer genuinely opens:** a kernel keyed to the baryon fraction is
outside L6's closed class on three independent grounds — f_b is not a single-valued function of any of L6's
four variables (|z| up to 60), the cosmological-ordering horn does not fire because clusters retain
essentially the cosmic baryon fraction so the background sits *at* cluster outskirts in f_b rather than
beyond them (1.05), and the sign is a suppression of an additive a₀-scale term to which BBN is blind
(6.1e-5) — and on both readings of f_b the galaxy ceiling clears f = 1, with clusters at 1.054 ± 0.126 (0.4σ
from the CMB) and thirteen of fourteen gates still passing, including the two that L49 and L50 fail outright.

**It opens by deleting what it was meant to protect:** the ΛCDM halo at the CMB's abundance already supplies
109% of the observed deep-MOND anomaly, so the kernel's share is capped at W ≤ 0.389 on both footings against
0.888 in the deposited theory, the BTFR zero point and the bounded-boost ceiling become the halo's, the
surviving term's own MOND transition sits at ≤ 0.19 a₀, the cold component acquires an O(1) fifth force that
invalidates the very halo library every number here uses, and the one quantity the mechanism must hit is set
by disc scale height rather than by the action.

**The theorem is that this is a bound and not a failed search:** eleven suppression functions on two
composition variables all collapse onto a single number — the kernel's effective strength where the anomaly
is measured — so f = 1 forces it below 0.438 and MOND doing the work requires it near 1, which means that
within this action a full cold abundance and a working MOND kernel are alternatives rather than complements,
because they are two explanations of one measured excess.

---

## 8. Caveats, stated rather than buried

1. **Nothing here favours this framework over ΛCDM and nothing here constrains ΛCDM.** The cold component,
   its abundance-matched profile and its stellar-to-halo-mass relation are ΛCDM's, imported wholesale, and a
   per-galaxy NFW with two free parameters reaches 0.061 dex where the kernel reaches 0.145 (L28 / L49 W1).
2. **This is not a closure of MOND-like theories in general.** It closes the combination of *this* action's
   kernel with a full cold abundance whose galaxy profile is ΛCDM's. A theory whose cold component is
   distributed differently — less in galaxies, more elsewhere — is not covered, though L49's specification
   and the 2026-09-06/07 dark-sector no-go between them close every mechanism so far proposed for making one.
3. **The generous of L49's two galaxy criteria is carried throughout**, so the candidate is not handed a
   manufactured deficit. D6 shows the strict criterion cannot be used here at all: at f = 1 the halo alone
   already misses it, independently of any kernel.
4. **The local-midplane f_b** uses SBdisk/SBbul photometry for stars and a thin-disc inversion of V_gas for
   gas, at a fixed scale height. C4 varies h_z over 0.15–1.00 kpc and E2 shows s_eff swings by a factor 7
   across that range, so the local horn's success is h_z-controlled and is reported as such.
5. **Abundance matching carries ~0.30 dex of systematic** on log M200. It moves the galaxy ceiling and the
   cluster requirement together and does not touch the theorem, which is about the halo *already* supplying
   the anomaly at f = 1.
6. **D9's fifth force is an order-of-magnitude estimate**, not a solved profile. It is the mechanism's
   largest unpaid bill and it is flagged, not resolved.
7. **Cluster windows** use the enclosed baryon fraction inside the same 1000 kpc aperture as L50, at b = 0
   and b = 0.20. The hydrostatic bias is not resolved here.
8. **The kernel, its saturation constant and the closure locus are the deposited theory's**, unchanged;
   nothing here re-fits them, and κ remains **fitted** (0.4998 / 0.6023).

---

## 9. Reproduction

```
python3 fable_independent_2026/L55_composition_kernel.py
```

Exit 0, 3 s. 28 checks: 9 PASS, 19 FAIL. Six controls (X1–X6) rebuild L49/L50's cluster amount and
post-kernel residual, their three parameter-free SPARC numbers, L50's two windows and its 1.72× / 2.06× gap,
L50 D8's s ≤ 0.495 / 0.439, and both horns of L6's closure — the four overlap kills and the cosmological
ordering — each from its own committed data with independent code. Every control passes.
