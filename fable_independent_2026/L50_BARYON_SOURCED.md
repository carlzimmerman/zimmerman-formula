# L50 — baryon sourcing: does L49's pincer open?

`L50_baryon_sourced.py` + `.out` — **40 checks, 28 PASS, 12 FAIL; every one of the nine controls passes and
most of the FAILs are the finding.** Runs in 2 s. Both a₀ footings (9.3619e-11 canonical, 1.1279e-10 alt) on
every dimensional number.

L49 found a minimum addition — a cold collisionless component in the matter sector, decoupled from the clock
— that satisfies the whole cluster specification, leaves the clock tachyon satisfied identically, touches
neither the Solar System nor the preferred-frame parameters nor BBN, and repairs the CMB and linear growth
exactly. It then failed for **one stated reason**: *the action's MOND scalar is sourced by the total
potential and therefore amplifies the very mass that was added to replace it.* That is a design choice, not
a theorem. This lane changes the source and recomputes everything.

---

## 0. The answer in one line

> **Conservation survives, the galaxy overshoot shrinks by a quarter but does not vanish, the cluster window
> moves up by 80% and now agrees with the galaxy ceiling to 0.1σ — and the intersection is still empty,
> because the CMB window cannot move at all. The gap narrows from a factor 2.82 to 1.72 (canonical) and 3.63
> to 2.06 (alt). The pincer does not open.**

What *does* change is the shape of the problem. Under baryon sourcing, at the measured hydrostatic bias
b = 0.20, **clusters and the CMB become compatible** (0.893 ± 0.158 against 1.000, 0.7σ). The entire
surviving obstruction is galaxies, and it is one number: **f ≤ 0.582 / 0.486**.

---

## 1. Conservation — the first thing that could have killed it, answered first

**B2 PASS. Baryon sourcing does not break the Bianchi identity, and the reason is structural rather than
lucky.**

The threat named in the brief is real only for a source inserted by hand into the *field equation*. Here the
modification is written into the *Lagrangian*, so the action remains a diffeomorphism-invariant functional of
(g, τ, φ, ψ_b, ψ_c); the Einstein equation is untouched (G_μν = 8πG T^total_μν); and ∇_μT^μν(total) = 0
follows from the Bianchi identity exactly as before. What is *not* conserved is the individually coupled
species, ∇_μT^μν(coupled) = −β T ∂^νφ — an exchange term the scalar's own equation cancels identically.
Verified symbolically on FRW with the coupled sector present: the total continuity residual
d(ρ_tot)/dt + 3H(ρ_tot + p_tot) evaluates to **0** on shell.

The lane is therefore not killed at step one.

---

## 2. The modification, at the level of the Lagrangian

**B1 PASS, derived not quoted.** For a static weak field ds² = −(1+2Φ)dt² + (1−2Φ)dx², sympy gives
J^i = ∇^iΦ exactly at first order and ∇_μJ^μ = ∇²Φ. So integrating the deposited action's drag coupling by
parts,

```
2(2 − K_B) J^μ ∂_μφ   =   −2(2 − K_B) φ ∇²Ψ   =   −8πG(2 − K_B) φ ρ_total ,
```

and ρ_total is everything minimally coupled to g. **That identity is L49's diagnosis, and it is a written
choice.** Two replacements were priced.

| | what changes | scalar equation | phantom gravitates? |
|---|---|---|---|
| **V-A** replacement | delete the drag coupling; couple φ to the baryon trace, `−8πG(2−K_B) φ T_b` | ∇·[J′(Y)∇φ] = 4πGρ_b | **NO** — §5 |
| **V-B** compensation | **keep** the drag coupling; add one term coupling φ to the cold sector, `ΔL = +8πG(2−K_B) φ ρ_c` | ∇·[(J′−1)∇φ] = 4πGρ_b | **YES** |

V-A is the RAQUAL/Bekenstein–Milgrom conformal coupling. V-B's coefficient is fixed by one condition — that
it cancel ρ_c out of the scalar's source — and it is the *same* (2 − K_B) that generates MOND.

Both change the scalar's **source** and nothing else, so both predict the same thing for everything measured
with baryons and light. The whole family is therefore carried as one parameter, ε = the fraction of the cold
component that still sources the scalar:

```
ε = 1  (L49) :  g = g_bar + f·g_halo + a₀ Δ( [g_bar + f·g_halo] / a₀ )
ε = 0  (L50) :  g = g_bar + f·g_halo + a₀ Δ(  g_bar              / a₀ )
```

**B4 PASS:** Δ is strictly increasing, so baryon sourcing gives a strictly smaller kernel term at every
f > 0. The change has the sign the lane needs.

**B3 FAIL, recorded as a cost.** V-B's compensating coefficient is fixed by one condition but *chosen* rather
than forced by a symmetry. Unlike L49 P3's λ ≤ 3.9e-7 it needs no exactness — a mismatch just moves ε
continuously off 0 — which is why the family is carried as ε.

---

## 3. The controls — L49's pincer rebuilt first

Nine controls, all PASS. Without these the lane would be quotation rather than verification.

| control | reproduced here | L49 |
|---|---|---|
| **A1** cluster amount | M_dark/M_bar = **5.73 ± 0.68**, f_bar = **0.149**, both footings | X1 |
| **A2** post-kernel residual | **3.09** / **2.76** M_bar | X6 |
| **A3** SPARC machinery | kernel **0.145 / 0.142** dex at medians **+0.030 / +0.003**; halo alone **0.171** at **−0.026** | X8 |
| **A4** the overshoot at f = 1 | median **−0.259 / −0.283** dex = **1.82× / 1.92×** in acceleration | N1 |
| **A5** the three windows | galaxies **≤ 0.355 / 0.276** (strict 0.185 / 0.120); clusters **0.316 ± 0.100 / 0.261 ± 0.093**; CMB **1.000 ± 0.010** | §4 |
| **A6** empty intersection, CMB binding | galaxies and clusters overlap; the galaxy ceiling is Ω_c h² = 0.0426 / 0.0331, short by **2.8× / 3.6×** | N2/N2a |
| **A7** ε is a deformation | at f = 0 the new machinery is **bit-identical** (< 1e-12 dex) to the old at ε = 0, 0.25, 1 | — |
| **A8** the kernel's cluster share | **2.64 / 2.97** M_bar of the missing 5.73 | — |
| **A9** standard MOND at f = 0 | deep-MOND ratio **1.0050** at g_bar = 1e-4 a₀; excess saturates at exactly **0.6476 a₀** | — |

---

## 4. The three windows, recomputed

|  | ε = 1 (L49) | **ε = 0 (L50)** | moved |
|---|---|---|---|
| **galaxies**, generous (median RAR shift inside 0.11 dex) | f ≤ 0.355 / 0.276 | **f ≤ 0.582 / 0.486** | **+64% / +76%** |
| galaxies, strict (rms not degraded by 0.02 dex) | f ≤ 0.185 / 0.120 | f ≤ 0.375 / 0.270 | +103% / +125% |
| **clusters**, b = 0, self-consistent at 1000 kpc | 0.316 ± 0.100 / 0.261 ± 0.093 | **0.569 ± 0.130 / 0.508 ± 0.133** | **+80% / +94%** |
| clusters, at the allowed b = 0.20 | 0.527 ± 0.134 / 0.455 ± 0.127 | 0.893 ± 0.158 / 0.832 ± 0.159 | +70% / +83% |
| **the CMB** | 1.000 ± 0.010 | **1.000 ± 0.010** | **0%** |
| **gap to the CMB** | 2.82× / 3.63× | **1.72× / 2.06×** | **−39% / −43%** |

- **D3 PASS (control).** The baryon-sourced cluster window agrees with its own closed form,
  f = (post-kernel residual)/(cosmic share) = 3.09/5.4286 = **0.569** and 2.76/5.4286 = **0.508** — because
  with the scalar blind to the cold component the kernel's contribution no longer depends on f.
- **D4 PASS.** The cluster window moves, and *upward* — clusters need **more** cold matter when the kernel
  stops amplifying it. That is the correct direction and it moves them toward the CMB.
- **D6 PASS.** Galaxies and clusters remain mutually admissible, and the agreement is sharper than L49's: the
  ceiling 0.582 against the requirement 0.569 ± 0.130, a difference of **0.1σ**. (On the strict galaxy
  criterion, and at b = 0.20, this overlap closes — both stated.)
- **D10 FAIL — and it reframes the problem.** At the allowed b = 0.20 the cluster requirement is
  **0.893 ± 0.158 / 0.832 ± 0.159**, i.e. **0.7σ / 1.1σ from the CMB's f = 1.000**. Under baryon sourcing
  **clusters and the CMB are compatible**, and the entire surviving obstruction is galaxies.
- **D5 FAIL — the galaxy overshoot does not vanish.** At f = 1 the median residual falls from −0.259 to
  **−0.191** dex (canonical) and −0.283 to **−0.208** (alt): an overshoot of **1.55× / 1.61×** rather than
  1.82× / 1.92×. **Baryon sourcing removes 26% / 27% of the overshoot in dex; 74% survives.** L49's diagnosis
  is correct but it is the *smaller* half of the effect.
- **D7 FAIL — the intersection is still empty.** Galaxies ≤ 0.582 / 0.486, clusters 0.569 ± 0.130 /
  0.508 ± 0.133, CMB 1.000 ± 0.010.

### 4.1 The obstruction stated sharply — and it is source-independent

**D9 FAIL.** Ask the question the other way: at f = 1, what fraction *s* of the kernel may survive before
galaxies break?

> **s ≤ 0.495 (canonical) / 0.439 (alt)** — the action's MOND kernel must be suppressed by a factor
> **2.0× / 2.3×** where galaxies are measured.

Re-sourcing the scalar cannot do that. Even at ε = 0 — the most re-sourcing can achieve — the galaxy ceiling
is 0.582. What re-sourcing removes is the *halo-driven* part of the kernel; the *baryon-driven* part is the
MOND anomaly itself, and it is what the theory exists to produce.

---

## 5. A new risk the lane creates, and it does not fire

The deposited theory cures its clock tachyon by Q₀ = 0, and **C1 PASS** reproduces L49 P1 independently: the
clock's induced gradient-mass coefficient is exactly K₂Q̄²/a², vanishing identically at Q̄ = 0.

**C2 PASS.** On an exactly homogeneous slice J^μ = 0 and Y = 0, so the deposited action has **no homogeneous
source** for φ and Q̄ = 0 is an exact solution — that is *why* the cure works. **Any direct matter coupling
supplies one.** Solving d/dt[a³K′(Q̄)] = −8πG(2−K_B)ρ_s a³ gives a³Q̄ = Ct, i.e. Q̄ ≠ 0 is forced, and by C1
the clock tachyon is revived.

**C4 PASS — and the reason is a clean cancellation.** In matter domination Q̄ = −H f_s (2−K_B)/|K₂| with
f_s = ρ_s/ρ_total, so Ω_K = f_s²(2−K_B)²/(6|K₂|); **on the closure locus c₂|K₂| = (2−K_B)² both |K₂| and
(2−K_B) cancel**, leaving

```
Ω_K = f_s² c₂/6 ,        rate/H = f_s √(c₂/2c₁₄) = f_s √(σ/2)
```

with c₁₄ gone entirely. The programme's own criterion (rate ≤ H at every a) is then **f_s ≤ √(2/σ)**:

| variant | source | f_s | rate/H | margin |
|---|---|---|---|---|
| V-A | baryons | Ω_b/Ω_m = 0.1556 | **0.143** | 7.0× |
| V-B | the cold component | Ω_c/Ω_m = 0.8444 | **0.774** | **1.29×** |

The bound is √(2/σ) = **1.091** at σ\* and **1.063** at the top of the clock window σ < 1.7716 — both above 1,
and f_s ≤ 1 always, so the gate is **structurally safe for any source**. It is nonetheless a real cost: the
deposited theory satisfies it *identically*, V-B satisfies it at 1.29×.

**C5 PASS.** V-B makes the cold mass φ-dependent, so Ω_c could drift. The cosmological amplitude is
φ ~ f_c(2−K_B)/|K₂| = 7.9e-7, giving a fractional drift of **7.1e-7** — five orders below Planck's 1% on
Ω_c h². **The CMB window is unchanged by the modification.**

---

## 6. The price

### 6.1 Lensing — where the two variants part company

**E2 FAIL for V-A: a conformally baryon-coupled MOND scalar does not lens.** Two independent statements,
both computed:

1. *The phantom does not gravitate.* With the drag coupling deleted, the MOND sector contributes to the
   Einstein equation only its own gradient energy. The ratio of that to the phantom density it must mimic is
   |∇φ|²r/(2a₀c²) = **1.6e-7** at 10 kpc in a galaxy and **1.6e-5** at 1 Mpc in a cluster.
2. *A conformal coupling cannot bend light — derived, not asserted.* For a generic static isotropic metric
   diag(−N², B², B², B²) with arbitrary N(x), B(x), and an arbitrary conformal factor A(x), the Christoffel
   difference contracted on a g-null k satisfies D^μk^ν − D^νk^μ = 0 for **all sixteen** index pairs. Null
   geodesics are unchanged.

**E3 FAIL.** The cold component dilutes the failure but does not remove it. At f = 0.569, V-A predicts
M_dyn/M_lens = **1.65** in clusters (down from the un-completed kernel's 1/f_bar ≈ 6.4) and **1.65** at the
median SPARC radius. In L24 C8's own statistic that is 2.2σ — *not* a kill on its own, since L24's error is
five-cluster weak-lensing noise. The load-bearing statement is structural: V-A predicts a definite inequality
where the deposited theory predicts an identity (Φ = Ψ, M_dyn/M_lens = 1 exactly).

**E4 PASS for V-B.** This is why V-B is the variant to carry: the drag coupling is retained, so the phantom
enters the Einstein equation exactly as before, and baryons *and photons* remain minimally coupled to the
single metric g. Φ = Ψ, M_dyn/M_lens = 1 and γ_PPN = 1 are untouched; only the scalar's source changes.

**E5 FAIL — the standard repair for V-A is already closed here.** Repairing a conformally coupled scalar's
lensing needs a disformal piece (this is why TeVeS carries a vector), and `LOCAL_NO_GO_AND_FORK_PAPER` §3.2's
identity ties the cancelled slip to a light-cone tilt: (c_GW − c_light)/c = Bφ′²/2 = (Ψ − Φ). GW170817's
intergalactic path alone exceeds the bound by 30–300×, and the programme's own I2 requirement (one physical
metric, no disformal matter metric) forbids it by construction. **A contrary record is flagged rather than
resolved:** LEDGER sf27 reports a disformal+conformal coupling to the khronon's normal *repairing* the
lensing gate in a different chassis. The two are not the same construction; this lane does not adjudicate
them, and V-B needs neither.

**On the literature question the brief asked.** TeVeS and AeST both couple *universally*: TeVeS through a
disformal physical metric that all matter sees, AeST through the aether's acceleration J^μ. The stated reason
is the one E2 derives — a universal coupling buys the equivalence principle and lensing at the same time,
and a conformal coupling to a *subset* of matter buys neither.

### 6.2 The equivalence principle

**E1 PASS, with the cost named.** In both variants baryons feel the kernel and the cold component does not:
at f = 0.582 the median fractional difference across SPARC is **η = 0.39** — an O(1) violation *between
sectors*. Two things it is not:

- It is **not** a violation within the Standard Model *in V-B*: baryons stay minimally coupled to g, so there
  is no composition dependence and MICROSCOPE/Eötvös are untouched. In **V-A** it is: the conformal coupling
  is to the trace T_b, and electromagnetic binding energy is traceless — one more reason to carry V-B.
- It is **not** inconsistent with the ΛCDM halos used throughout. In V-B the cold component feels only the
  Newtonian field of ρ_b + ρ_c, which is exactly the gravity under which abundance-matched NFW halos are
  built — *more* self-consistent than under total sourcing, where the halo would itself have been
  MOND-boosted.

### 6.3 Preferred-frame parameters and the Solar System

**E6 PASS.** V-B changes nothing in the aether/scalar sector (the added term couples φ to a component absent
from the Solar System), so α₁ = −4c₁₄ = **−4.00e-6** and α₂ = (c₁₄/2)(1/σ − 1) = **−2.02e-7** stand. V-A
*deletes* the drag coupling and with it the MOND piece of `LOCAL_NO_GO` §3.3's α₁ = −4c₁₄ − 4(2−K_B)/(J_Y+1)
— a genuine gain, and moot given E3.

**E7 PASS.** A smooth cold halo at f = 0.569 puts **2.48e-15 M⊙** inside Saturn's orbit against
Pitjev–Pitjeva's 6.7e-11, a margin of **26 967×**.

---

## 7. The exhibited point, run against the gates

**The point: variant V-B, f = 0.569 of the abundance-matched ΛCDM halo**, on the deposited theory's own
exhibited parameters (K_B = 0.2, c₁₄ = 1e-6, σ = 1.679312732, c₂ = 1.6793e-6, |K₂| = 1.9294e6 on the closure
locus, ξ and p unchanged).

**F1 PASS — 11 of 13 gates**, including both gates the lane put at risk:

| gate | verdict |
|---|---|
| Cassini / sunward / ξ | PASS (aether-scalar sector untouched) |
| Saturn phantom mass | PASS, margin 26 967× |
| α₁, α₂, α₃, γ | PASS, literally unchanged |
| c_T = c (GW170817) | PASS (c₁₃ = 0; no disformal matter metric) |
| mode count and health | PASS |
| **clock tachyon** | **PASS, at 1.29× rather than identically** |
| **lensing == dynamics** | **PASS, structurally (V-B)** |
| BBN | PASS, ΔN_eff = 0 |
| rotation curves | PASS at this f (median −0.107 / −0.128 dex, rms 0.195 / 0.208) |
| cluster amount | PASS at this f (0.0σ / 0.5σ) |
| **conservation / Bianchi** | **PASS, verified symbolically** |
| CMB cold-matter density | **FAIL** — Ω_c h² = 0.0683 against 0.1200 ± 0.0012, short by 1.76× |
| linear growth / σ₈ | **FAIL** by the same factor |

**F3 PASS.** The point is a strict improvement on L49's: f = 0.569 against 0.316, a factor 1.80, with the CMB
deficit falling from 2.8× to 1.76× and no gate lost.

---

## 8. What closes it — the theorem

**V6 FAIL.** Two statements, and neither is a number that could be argued down.

**(i) The CMB window cannot move.** It is a statement about the pressureless *gravitating* density at
recombination. On the closure locus the MOND sector contributes **exactly zero** to linear growth
(S_eff = 1 − (2−K_B)²/(c₂|K₂|) = 0), so changing which matter sources a field that contributes nothing
changes nothing. C5 confirms the only channel by which the modification could have touched it — a
coupling-induced drift in Ω_c — is 7e-7.

**(ii) The galaxy window cannot reach f = 1.** At that abundance the ΛCDM halo *alone* already reproduces
SPARC at **0.171 dex with median −0.026**, so any further acceleration is an overshoot. The kernel adds
a₀Δ(g_bar/a₀), which in the deep-MOND regime **is** the observed anomaly. Re-sourcing removes only the
halo-driven part — 26% of the overshoot in dex — and the remaining 74% is the theory's own reason for
existing.

The only remaining move is to suppress the kernel itself where the cold component dominates, to
**s ≤ 0.495 / 0.439** at f = 1. That is L49's option **(b)** — a screening function of the total density —
and it is a different lane, already constrained by L6's cosmological-ordering theorem.

---

## 9. Three-sentence verdict

**Baryon sourcing is a legitimate action-level modification and it survives the test that could have killed
it outright:** conservation and the Bianchi identity are untouched, because the change is made in the
Lagrangian and diffeomorphism invariance then guarantees ∇_μT^μν(total) = 0 with only the individually
coupled species exchanging energy with the scalar; and in the variant that keeps the drag coupling (V-B) it
also keeps lensing = dynamics, the preferred-frame parameters, c_T = c and the mode count — at the cost of
one chosen coefficient, an O(1) equivalence-principle violation confined to the dark sector, and a
clock-tachyon margin that falls from *identical* to 1.29×.

**It moves both of the windows it was supposed to move** — the galaxy ceiling rises from f ≤ 0.355 / 0.276 to
0.582 / 0.486 and the cluster requirement from 0.316 ± 0.100 / 0.261 ± 0.093 to 0.569 ± 0.130 /
0.508 ± 0.133, so galaxies and clusters now agree to 0.1σ at f ≈ 0.57, and at the measured hydrostatic bias
clusters reach 0.893 ± 0.158, compatible with the CMB at 0.7σ — **but the CMB window does not move at all,
and the intersection stays empty**, with the gap narrowed from 2.82× to 1.72× (canonical) and 3.63× to 2.06×
(alt).

**What closes it is a theorem, not a number:** the CMB window cannot move because on the closure locus the
MOND sector contributes exactly zero to linear growth, and the galaxy window cannot reach f = 1 because at
that abundance the ΛCDM halo alone already reproduces SPARC to 0.171 dex, leaving no room for the kernel
evaluated on the baryons — which is 74% of the overshoot, is the MOND anomaly itself, and is the one thing
re-sourcing cannot touch.

---

## 10. Caveats, stated rather than buried

1. **Nothing here favours this framework over ΛCDM and nothing here constrains ΛCDM.** The cold component and
   its abundance-matched profile are ΛCDM's, imported wholesale; the stellar-to-halo-mass relation remains a
   free function of host mass (L49 M5).
2. **f_gal is the generous of two criteria**, carried so the candidate is not handed a manufactured deficit.
   The strict criterion gives 0.375 / 0.270, on which even the galaxy–cluster overlap closes. The full table
   at nine values of f is printed in the `.out` so a reader can pick another; no choice in the printed range
   reaches f = 1.
3. **Abundance matching carries ~0.30 dex of systematic** on log M200. It moves f_gal and the cluster
   requirement together and cannot close a gap of 1.7×.
4. **V-B's compensating coefficient is fixed by one condition but chosen, not forced by a symmetry.** Whether
   the *same* coefficient also exactly cancels the MOND force on the cold component is a weak-field question
   this lane does not settle. It affects no number here — every window is computed from what baryons and
   light feel — and would only alter the cold component's own equilibrium profile, for which the ΛCDM library
   is already assumed.
5. **The induced-condensate calculation is matter-domination scaling on a flat FRW background**, calibrated
   against g03w's published rate through the same formula L49 X5 uses. It fixes the structure
   (rate/H = f_s√(σ/2), with c₁₄ and |K₂| cancelling on the closure locus); it is not a full
   cosmological-perturbation calculation.
6. **E3's cluster significance for V-A rests on five-cluster weak-lensing noise and is not a kill on its
   own.** The load-bearing statement there is structural: a conformal coupling cannot bend light.
7. **R2's hydrostatic bias cuts both ways.** D10's compatibility of clusters with the CMB holds at b = 0.20;
   at b = 0 clusters want 0.569 and at b = 0.33 more still. The bias is not resolved here, and D10 is stated
   as a reframing of the problem, not as a result about clusters.

---

## 11. Reproduction

```
python3 fable_independent_2026/L50_baryon_sourced.py
```

Exit 0, 2 s. 40 checks: 28 PASS, 12 FAIL. Nine controls (A1–A9) rebuild L49's cluster amount, its post-kernel
residual, its three parameter-free SPARC numbers, its three windows, its empty intersection and its −0.259 dex
overshoot from the same data with independent code, and check that at zero cold fraction the new machinery is
bit-identical to the old and returns the standard deep-MOND law. Every control passes.
