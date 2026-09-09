# L61 — the three permitted branches, and the theorem that follows them there

`L61_permitted_branches.py` + `.out` — **47 checks, 37 PASS, 10 FAIL; every one of the eleven controls
passes and every FAIL is the finding.** Runs in 2.4 s, exit 0. Both a₀ footings (9.3619e-11 canonical,
1.1279e-10 alt) on every dimensional number.

PAPER9 / [L31](L31_FOLIATION_NOGO.md) states its own scope in its own words: the foliation theorem binds
theories with (i) static weak-field MOND, (ii) one metric with matter minimally coupled, (iii) exactly two
propagating gravitational modes, with the locality proviso discharged against the known nonlocal class by
[L39](L39_NONLOCAL_MODES.md)'s lensing lock. What it explicitly does **not** close is written in the paper:

> "three or more propagating modes, two metrics, or a non-minimal matter coupling are all untouched."

Eighteen months of this programme have lived in the fourth corner. This lane searches the other three.

---

## 0. The answer in one line

> **The 'excess spent once' theorem generalises, and that is the result. It is branch-independent — its
> argument uses measured accelerations, Ω_c h², and the theory's own MOND normalisation, and mentions
> neither the mode count nor the metric count nor the matter coupling. Two of the three permitted branches
> are then closed by gates run here (branch 1 at the lensing gate, generically rather than
> construction-specifically; branch 3 at the tensor-speed gate, with the flagged contrary ledger entry
> adjudicated and found already withdrawn by this repository's own sf29). The third — two metrics — stays
> OPEN at the mode-health gate, at exactly the calculation the repository's own record already names, and
> it inherits the theorem whatever that calculation returns.**

---

## 1. Controls, first — eleven of them, all PASS

| control | reproduced here | published |
|---|---|---|
| **A1–A4** the four mode counts | GR **2**, GR+scalar **3**, khronometric **3**, Einstein-aether **5**, from `N = (P − 2F − S)/2` | L39 C1–C3, PAPER9 |
| **A4b** the same formula on two metrics | Hassan–Rosen **7** = 2+5; with the Boulware–Deser mode **8** | the record's own 7-vs-8 fork |
| **A5** PPN α₂ at the exhibited point | **−2.0226e-7**, margin **1.978×** against 4e-7 | −2.02e-7, margin 1.98× |
| **A5b** closure locus + S_eff ceiling | \|K₂\| = **1.92935e6**; S_eff ≤ 1 − 1/σ_max = **0.4355** | 1.9294e6; 0.4355 |
| **A6** SPARC rotation curves, kernel alone | **0.145 / 0.142 dex** at medians **+0.030 / +0.003** | 0.145 / 0.142, +0.030 / +0.003 |
| **A6b** abundance-matched halo alone | **0.171 dex** at median **−0.026** | 0.171, −0.026 |
| **A7** bounded-boost ceiling value | C a₀ = **6.063e-11 / 7.304e-11** m s⁻² | 6.06e-11 / 7.30e-11 |
| **A7b** Saturn phantom mass, bare kernel | **1.40e4× / 1.69e4×** the Pitjev–Pitjeva bound | 1.40e4 / 1.69e4 |
| **A8** conformal null geodesics (symbolic) | `Γ̃^a_bc k^b k^c − Γ^a_bc k^b k^c − 2k^a(k·∂lnΩ) = 0`, all four components | L39 C-c2, L50 E2 |

**One control was attempted and is reported as NOT reproduced, with the reason attributed rather than
hidden.** The gate table's *"99.23% of 2352 points"* for the ceiling's SPARC violation rate is a
Υ-**profiled** number (g03w, with SPARC's own Q<3 / i>30 cuts). At fixed Υ_d = 0.5 and no error bars this
lane counts 73.3% / 79.9% below the ceiling — much higher, exactly as [L11](L11_GALACTIC_LIMIT.md) B3
already recorded (*"my fixed-Υ counts sit ~2.5× higher for BOTH kernels"*). It is printed as a diagnostic
and is **not used as a control**; the ceiling's *value* (A7) is the part reproduced.

Five gate numbers reproduced against the brief's "at least two". Nothing below leans on a number that was
not rebuilt from committed data with independent code.

---

## 2. The decisive structural question, answered first: the theorem generalises

[L55](L55_COMPOSITION_KERNEL.md)'s theorem is scoped to *this action's kernel combined with a ΛCDM-profile
cold abundance*. Its argument, stripped of the action, is that the galaxy anomaly is one number per point
and a component present in the amount the CMB requires already spends it. That argument mentions no mode
count, no metric count and no matter coupling. Restated with hypotheses:

> **THEOREM (excess spent once — branch-independent form).** Let a theory predict, at each point of a
> galaxy, the acceleration felt by a test baryon as `g_pred = g_bar + A_X + A_K`, with `g_bar` the
> Newtonian field of the **observed** baryons, `A_X` the acceleration **transmitted** to that baryon by a
> pressureless component present in the amount the CMB fixes, and `A_K` everything else the modification
> supplies. Assume
> **(H-a)** no cancellation: `A_X ≥ 0` and `A_K ≥ 0` pointwise;
> **(H-b)** MOND normalisation: with `A_X = 0` the theory reproduces the observed relation, so in the deep
> regime `A_K → √(g_bar a₀)`, which *is* the measured anomaly;
> **(H-c)** transmission: `A_X = η·g_halo` with `η > 0`.
> Then `g_pred − g_obs = A_X ≥ 0` **pointwise**: the theory overshoots the measured rotation curve by
> exactly the cold component's transmitted pull.
>
> **The conclusion depends on the number of propagating modes, the number of metrics and the matter
> coupling ONLY through (H-a) and (H-c).** Everything else is arithmetic on measured accelerations.

### 2.1 The inequality, on the data (B1)

At η = 1, with the **weakest** kernel the theory admits (baryon-sourced, ε = 0), the median over the 2059
deep-MOND SPARC points is `g_pred/g_obs = ` **1.692**, a +0.228 dex overshoot. The full table:

| η | ε = 1 rms can/alt | median | ε = 0 rms can/alt | median |
|---|---|---|---|---|
| 0.00 | 0.145 / 0.142 | +0.030 | 0.145 / 0.142 | +0.030 |
| 0.35 | 0.206 / 0.225 | −0.109 | 0.162 / 0.174 | −0.057 |
| 0.58 | 0.259 / 0.280 | −0.170 | 0.197 / 0.210 | −0.110 |
| 1.00 | 0.338 / 0.360 | −0.259 | 0.264 / 0.277 | −0.191 |

### 2.2 The number every branch has to hit (B2, B3)

| ceiling on η, generous criterion (median RAR shift ≤ 0.11 dex) | canonical / alt | published |
|---|---|---|
| ε = 1, kernel reads the total potential | **0.355 / 0.276** | L49: 0.355 / 0.276 |
| ε = 0, kernel reads the baryons only | **0.582 / 0.486** | L50: 0.582 / 0.486 |
| what the CMB requires at recombination | **1.000 ± 0.010** | Planck Ω_c h² = 0.1200 ± 0.0012 |

η and L49/L50's cold fraction *f* enter identically, so this ceiling **is** their window — which makes B2
simultaneously the requirement and a control on it.

> **Any theory in any branch must transmit at most ~58% (canonical) / ~49% (alt) of the CMB-required cold
> component's Newtonian pull at SPARC radii, while transmitting ~100% of it at recombination.**

### 2.3 The only escape, and why it is closed on ORDERING rather than on magnitude

Breaking (H-c) means making baryons blind to the cold component *inside galaxies* while leaving the CMB's
driving intact. Two mechanism families exist and both fail, and they fail on the **direction** of the
required effect, not on how large it has to be — a factor ~1.7 is not extreme.

| family | test | result |
|---|---|---|
| **B4 range** (graviton mass, Yukawa mediator) | a Yukawa force ratio `(1+mr)e^{−mr}` is strictly decreasing | tune it to η(10 kpc) = 0.582 and η(r_s) = **1.34e-7** — the third peak loses its driving; tune it to η(r_s) ≥ 0.90 and η(10 kpc) = **0.999206** — the galaxy is untouched. **It suppresses LONG range and not short; the requirement is the opposite** |
| **B5 density** | ρ at recombination vs ρ in a galaxy where the anomaly is measured | ρ_rec = 3.59e-18 kg m⁻³ vs **7.20e-21** at 10 kpc counting the disc's own midplane baryons — recombination is **498×** denser (52 939× at 30 kpc, halo only). **Wrong ordering** |
| **B6 acceleration** | the acoustic driving `g ~ c²Φ/r_s` vs galactic g | **2.4–24 a₀** (Φ = 1e-5 to 1e-4) against SPARC's median **0.73 / 0.61 a₀** — 0.99 dex, **no clean separation**; and clusters at R500 sit at **0.33–0.58 a₀**, at or *below* galaxies, while requiring **more** transmission |
| **B7 potential** | galaxies vs clusters | clusters are **64×** deeper and require η = 0.569 ± 0.130 (b = 0) to 0.893 ± 0.158 (b = 0.20) — **more**, not less. **Wrong ordering** |

This is L6's cosmological-ordering horn run in the mirror — L6 asked whether a monotone `S(X)` could
*enhance* clusters relative to galaxies; the question here is whether one could *suppress* the cold
component's pull in galaxies relative to recombination — and L6's own horn fires again, at the
recombination epoch L6 never used.

### 2.4 The other half of the trade, reproduced (B8)

Suppressing the **kernel** instead of the halo requires `s ≤ 0.495 / 0.439` at η = 1 (reproducing L50 D8 /
L55 D4), and in the deep regime `s·a₀Δ(g/a₀) = a₀′Δ(g/a₀′)` with `a₀′ = s²a₀` **exactly** (verified to
6.4e-5 in the strict limit), so the surviving term's own MOND transition sits at
**a₀′ ≤ 0.245 a₀ = 2.29e-11 / 2.17e-11 m s⁻²**.

### 2.5 The verdict (B9 PASS), and its scope

**The argument is branch-independent.** Stated as the theorem it is:

> **No relativistic theory that (a) reproduces the observed deep-MOND relation in galaxies with its cold
> component switched off, (b) contains a pressureless component in the amount the CMB requires, and
> (c) transmits that component's Newtonian pull to baryons with an efficiency that is not smaller inside
> galaxies than at recombination, can fit the measured rotation curves. It overshoots by the transmitted
> pull, pointwise. The only hypothesis a branch can attack is (c), and (c) requires a suppression whose
> ordering is short-range-off / long-range-on, or dense-off / dilute-on with recombination denser than a
> galaxy — neither of which any mass term or monotone environmental screening supplies.**

**Scope, stated rather than buried.** The cold component's **galaxy profile** is still an input
(abundance-matched ΛCDM here). A theory that puts the cold component somewhere other than in galaxy halos
escapes — and that is a statement about the dark sector's microphysics, closed separately by this
repository's 2026-09-06/07 dark-sector no-go (Pauli, wave, four condensates, thermal relic), **not** by
this theorem. That is the honest boundary and it is the same one L55 caveat 2 draws.

**What this means for the programme, plainly.** The remaining choice is between a working kernel and a full
cold cosmology in *any* theory of this kind, not only in the deposited one. That is a negative and it is
the most valuable thing in this lane.

---

## 3. A structural observation the search produced: the three branches are not three directions

The permitted branches **overlap**, and the overlap is the whole space:

- **branch 2 ⊂ branch 1 in mode count** (D2): a healthy second metric costs five extra propagating modes,
  so every two-metric theory is also a ≥3-mode theory (7 = 2+5, or 8 with the Boulware–Deser ghost).
- **branch 3 needs a field to build the coupling from.** If that field propagates we are in branch 1; if
  it does not, L31's own Proposition Q applies and there is a preferred frame.

So the permitted space is essentially *"≥ 3 propagating modes"*, and the operative question becomes: **what
does the extra mode buy?** By L39's operator lemma it must buy the second transverse symmetric operator —
the thing that unlocks the lensing equation from the rotation-curve equation. Section 4 shows a
Lorentz-invariant extra mode cannot supply it.

---

## 4. BRANCH 1 — three or more modes, Lorentz invariant. **DEAD at gate 1.**

RAQUAL (Bekenstein–Milgrom 1984) and phase-coupling gravity (Bekenstein 1988), N_grav = 3 and ≥3 in L31's
table. The brief's question is whether their known failures are **generic to the branch** or specific to
those two constructions.

### 4.1 The fork, and why it is exhaustive (C.0)

L39's operator lemma and DC-013's ray lock (both **cited, not re-derived**) between them say a
Lorentz-invariant extra mode cannot unlock lensing by modifying the **metric sector** at any number of
modes. The only remaining lever is the **matter coupling**:

| arm | disposition |
|---|---|
| **(1a)** conformal `g̃ = A(φ)g` | tested here — §4.2 |
| **(1b)** disformal `g̃ = Ag + B ∂φ∂φ` | **this is branch 3**; handed to §6 |
| **(1c)** the field acquires a **timelike gradient vev** (mimetic / DEFW) | a preferred frame — L39 established it; *satisfies* the theorem's conclusion rather than escaping it |
| **(1d)** a vector with a timelike vev (TeVeS, GEA, AeST) | preferred frame, already in L31's table |

(1c) and (1d) are instances of the conclusion, not escapes. (1b) leaves the branch. **Branch 1's own
content is (1a).**

### 4.2 The obstruction, derived and generic (C1–C4)

Derived symbolically from the deep-MOND normalisation alone, with no kernel shape assumed:

```
rho_phi     = X^(3/2) / (12 pi G a0 c^2)            (AQUAL scalar's static energy density)
rho_phantom = sqrt(X) / (4 pi G r)                  (the density that would produce g ~ 1/r)
ratio       = X r / (3 a0 c^2)  =  v_c^4 / (3 a0 r c^2)  =  (v_c^2/c^2) x (g_MOND / 3 a0)
```

> **A conformally coupled Lorentz-invariant scalar's own gravitating stress is smaller than the phantom it
> must mimic by the galaxy's own v²/c².**

On the data: median `ρ_φ/ρ_phantom = ` **1.35e-8 (canonical) / 1.52e-8 (alt)**, max 1.95e-7, over the deep-MOND
SPARC points. **C2 FAIL** — the branch lenses like general relativity on the baryons alone. **C3 FAIL** —
it predicts M_dyn/M_lens of **3.30 / 3.46** (90th percentile 5.64 / 6.09) where the measurement is ~1.

**C4 PASS — the obstruction is kernel-independent.** Three interpolating functions (the deposited
saturating kernel, Milgrom simple, Milgrom standard) give the same suppression to within a factor **1.75**,
all below 1e-5, because the scale is set by v²/c² and not by *f*.

**And the historical record agrees for this reason.** Bekenstein's own RAQUAL → PCG → TeVeS sequence was
driven by exactly this; L39 quotes DEFW 2011 verbatim on TeVeS's unit timelike vector being what "*helps in
obtaining the right amount of light deflection*". **The failure is the branch's, not the constructions'.**

### 4.3 What the extra mode costs

It costs the whole lensing sector and buys nothing, because a Lorentz-invariant scalar cannot supply L39's
second transverse operator: its gradient is spacelike in a static configuration, and a timelike gradient
vev is spontaneous Lorentz violation, which is arm (1c). The branch's other known costs — RAQUAL's
superluminal scalar propagation in the transition region, the reason Bekenstein moved to PCG — are
downstream of a gate already closed and are **cited, not computed here**.

**C5 FAIL. Verdict: DEAD at gate 1 (lensing vs dynamics), generically.**

---

## 5. BRANCH 2 — two metrics. **OPEN at gate 5, and not claimed either way.**

**The record was read first, as the brief requires** (`project_relativistic_mond_closure_2026`):

- the single-metric pincer (DC-013 + DC-019) **explicitly does not cover bimetric**;
- **DC-018**: standard ghost-free dRGT / Hassan–Rosen bigravity's helicity-0 Galileon sector cannot give
  MOND's 1/r. **Reproduced here as a control (D1 PASS):** the spherical flux relation
  `r^(3−n)(π′)^n = GM` gives `π′ ~ r^(1−3/n)`, so integer `n ∈ {1,2,3,4}` gives `r^−2, r^−1/2, r^0, r^1/4`
  and MOND's `r^−1` needs the **non-integer n = 3/2**;
- BIMOND connection interactions carry the Boulware–Deser risk (the lapse *ratio*, rank-1 Hessian);
- **the one open door**: the complete 5-invariant derivative-bimetric basis has a 2-D
  background-independent lapse-velocity-free subspace containing MOND-alive directions off the f(Q) line;
  `T4 − T1` gives a static-NR MOND acceleration `a = −4` **and** a lensing source `b = −8`, both nonzero.
  **Health is recorded as UNDECIDED.**

**This lane does not re-close it and does not claim it.** Its gates, in the brief's order:

| gate | verdict | status |
|---|---|---|
| 1 lensing vs dynamics | NOT CLOSED | the T4−T1 direction has a nonzero lensing source alongside the MOND acceleration; whether the ratio gives Φ = Ψ is the record's own un-run coupled g/ĝ solve |
| 2 Solar System | **NOT RUN** | no Solar-System solve exists for this subspace |
| 3 preferred frame | LIABILITY FLAGGED | the record warns the solve must not inherit the α₃ = −1 liability |
| 4 tensor speed | **NOT RUN** | no c_T computation exists for this subspace |
| **5 mode health** | **THE DECIDING GATE, UNDECIDED** | full covariant Hamiltonian count on the `a ≠ 0` sub-family: healthy elliptic auxiliary (**7**) or Boulware–Deser ghost (**8**)? Named in the record as the decisive un-run calculation |
| 6 cluster mass and shear shape | INHERITED | L41/L49's specification is chassis-independent |
| 7 cosmology | **CLOSED BY §2** | D3 |

**D3 PASS — the theorem follows the second metric.** A second metric offers exactly one new way to attack
(H-c): put the cold component on the second metric so its pull reaches baryons only through the g–f
interaction. In every ghost-free bimetric construction that interaction **is a graviton mass term**, so the
transmitted force carries the Yukawa factor of B4 — Compton wavelength 7.00 kpc to suppress at 10 kpc,
at which η(r_s) = **1.34e-7** and the third acoustic peak loses its driving.

**D4 FAIL / D5 FAIL. Verdict: OPEN — not dead on any gate run here, and not alive, because gates 2, 4 and 5
have never been run on it. §2's theorem applies to it whatever gate 5 returns.**

---

## 6. BRANCH 3 — non-minimal matter coupling. **DEAD at gate 4**, and the adjudication.

### 6.1 The identity, proved for both chassis (E1, E1b, E1c)

A conformal coupling cannot bend light (A8, reproved symbolically here). So the whole content of branch 3
is the **disformal** coupling. For `g̃ = A g + B w⊗w` with `w` a unit vector of `g`, at first order:

| chassis | fractional cone tilt `(c_light − c_grav)/c` | shift in Φ matter feels | shift in Ψ |
|---|---|---|---|
| **spacelike w** (a frame-free scalar's gradient) | **−B/(2A)** | 0 | **−B/(2A)** |
| **timelike w** (a khronon's normal — sf27's chassis) | **−B/(2A)** | **−B/(2A)** | 0 |

- **E1 PASS.** The shift a disformal term makes in the potential matter feels **equals** the fractional tilt
  of the matter light cone relative to the graviton cone, exactly, in **both** chassis.
- **E1b PASS.** `|d(Φ − Ψ)| / |tilt| = 1` in both: **a repair of size X costs a cone tilt of size X, and
  there is no lever ratio to exploit.**
- **E1c PASS.** With B = 0 the tilt and both shifts vanish for every A: the conformal lever is pure gauge
  for light bending.

> **The slip you cancel IS the light-cone tilt you create.** That is LOCAL_NO_GO §3.2's identity
> `(c_GW − c_light)/c = Bφ′²/2 = (Ψ − Φ)`, reproved here from the metric and **extended to the timelike-w
> chassis that the flagged contrary entry uses**.

### 6.2 The gate (E2, E3)

Required tilt = the galaxy's own `v_flat²/c²`: **median 1.30e-7, 90th percentile 6.36e-7** across 155 SPARC
galaxies (footing-independent — it is a measured speed; what the footings change is which points are
deep-MOND, 2059 canonical vs 2133 alt of 2786). LOCAL_NO_GO §3.2 quotes 3.9e-7 for NGC 4993's host and
3.0e-7 for the Milky Way; this lane's Milky-Way-mass end gives 6.4e-7.

GW170817: 40 Mpc of path, ≤1.7 s delay ⇒ path-averaged |tilt| ≤ **4.13e-16**. The tilt would have to be
confined to **3.2e-9** of the path to evade it. sf29's own integration puts β = 0 at the Newtonian ends and
nonzero through the MOND zone — i.e. exactly in the halo the wave crosses on the way out and on the way in.
Two host halos of 20 / 50 / 100 kpc occupy 1.0e-3 / 2.5e-3 / 5.0e-3 of the path:

**E3 FAIL — exceeded by 3.1e5× on the most conservative halo extent and 1.6e6× on the least.** The same
ordering LOCAL_NO_GO §3.2 reports ("2e6 ε over the bound" from the two galaxies' MOND regions; "30–300"
from the intergalactic medium alone, which is its conservative floor).

### 6.3 THE ADJUDICATION — the flagged contrary entry does not stand

L50 E5 flagged, and did not settle: *"LEDGER sf27 reports a disformal+conformal coupling to the khronon's
normal repairing the lensing gate in a different chassis."* The files were read.

- **E4 PASS — there is no live contradiction.** `qwen_claude_field_theory/closure_2026/LEDGER.md` row
  **SF29** reads *"REPAIR KILLED — sf28 C withdrawn"*; row **SF28** reads *"causality WITHDRAWN by SF29"*;
  and `RETRACTIONS.md` records the withdrawal in full. **This repository killed the disformal repair
  itself, before L50 was written.**
- **E5 FAIL — a documentation item, handed back and NOT edited.** The LEDGER's **prose** status paragraph is
  stale relative to its own table: it still reads *"All four bills PAID in sf28 … causality safe with the
  sign **forced** — β > 0 everywhere"*, contradicting rows SF28 and SF29 in the same file. A reader who
  stops at the prose gets the withdrawn claim. **That is almost certainly how the contrary entry came to be
  flagged in the first place.**

**What of sf27 survives:** its **algebra**. The two levers genuinely span the (g_dyn, g_lens) plane and the
repair works **pointwise** — which is E1's identity said the other way round. What sf29 killed is making it
globally consistent.

**E6 PASS — sf29's kill and the GW identity are the same physics.** sf29's cone ratio
`(v_matter/v_photon)² = 1 − β` with β < 0 is superluminal by 2.88e-7 at v_c = 150 km/s, and E1's identity
says that same number is the lensing shift. **There was never a contradiction to adjudicate — only a stale
prose paragraph.**

**E7 PASS — sf29's monotonicity theorem, reproduced on the deposited kernel.** `β′ = −2Δ` with Δ > 0 makes
β strictly monotone, while screening needs β = 0 in **both** Newtonian regimes (the high-acceleration
interior and the external-field-dominated far exterior). The required change between x = 100 and x = 0.01 is
**4.93 v_c²** on the deposited saturating kernel and **9.21 v_c²** on the pure deep-MOND √ kernel, against
sf29's 8.52 v_c² on its own chassis kernel. **The gap is strictly positive and of order the phantom's own
potential; the conclusion is kernel-independent.**

**E8 PASS — §2's theorem follows branch 3 too.** A non-minimal coupling is the one branch where (H-c) is
genuinely live, but the coupling that would do it must be scale- or environment-dependent, and B4–B7 give
four variables with four wrong orderings or no separation.

**E9 FAIL. Verdict: DEAD at gate 4 (tensor speed).** Gate 1 is *passed pointwise* by the disformal lever —
that is sf27's real content and it stands — but the same lever is the cone tilt.

---

## 7. Mutation controls (F1–F3, all PASS)

- **F1**: with B = 0 the cone tilt vanishes **and** the lensing repair vanishes together — neither can be
  had alone. (This is the repo's own `doorA` mutation control, rebuilt.)
- **F2**: switching a₀ → 0 at η = 1 returns the halo-only residual −0.026 dex exactly, against −0.191 with
  the kernel on. The §2 overshoot is caused by the kernel, not by the machinery.
- **F3**: the branch-2 counting formula, applied to general relativity itself (P = 12, F = 4, S = 0),
  returns **2** and not 7. No branch-specific tuning.

---

## 8. Verdicts

| branch | verdict | killing gate |
|---|---|---|
| **1 — three or more modes, Lorentz invariant** | **DEAD** | **gate 1, lensing vs dynamics.** ρ_φ/ρ_phantom = 1.35e-8 / 1.52e-8; the suppression is the galaxy's own v²/c² and is kernel-independent to a factor 1.75. **Generic to the branch, not specific to RAQUAL and PCG.** Its escapes are a timelike gradient vev (= a preferred frame, the theorem's own conclusion) or a disformal coupling (= branch 3) |
| **2 — two metrics** | **OPEN** | **gate 5, mode health — UNDECIDED.** Standard dRGT / Hassan–Rosen is closed by DC-018 (reproduced at D1). The repository's own 2-D ghost-free derivative-bimetric subspace is not closed and is not closed here; the deciding calculation is the covariant Hamiltonian count on the a ≠ 0 sub-family (7 vs 8) plus a coupled g/ĝ lensing solve that must not inherit α₃ = −1. **Whatever it returns, §2's theorem applies (D3)** |
| **3 — non-minimal matter coupling** | **DEAD** | **gate 4, tensor speed.** Conformal cannot bend light (A8). Disformal repairs lensing pointwise, but E1 proves the repaired slip **is** the matter/graviton cone tilt in both chassis; required tilt 1.30e-7 against GW170817's 4.13e-16 path average, exceeded 3.1e5–1.6e6×. Independently killed by sf29's two-boundary-condition theorem (gap 4.93 v_c²) |

**F4 FAIL — no permitted branch is alive on every gate.** **F5 FAIL — a full-gate theory in the permitted
space is NOT demonstrated**, and one branch of three remains genuinely open.

### Three-sentence verdict on whether a full-gate theory exists in the permitted space

**No such theory has been exhibited, and two of the three permitted branches are closed by gates run here:
branch 1 fails the lensing-versus-dynamics gate generically — a conformally coupled Lorentz-invariant
scalar contributes 1.4e-8 of the lensing mass it must supply, suppressed by the galaxy's own v²/c², a
statement that holds for every interpolating function and is the reason Bekenstein's own sequence ended at
TeVeS's unit timelike vector — and branch 3 fails the tensor-speed gate, because the disformal slip repair
IS the matter/graviton cone tilt, exactly, in both the spacelike and the timelike chassis.**

**The third branch, two metrics, is genuinely OPEN and this lane deliberately does not close it: standard
bigravity is already closed by DC-018, but the repository's own 2-D ghost-free derivative-bimetric subspace
has a nonzero lensing source alongside its MOND acceleration and its health is UNDECIDED, waiting on
exactly the covariant Hamiltonian count (7 healthy versus 8 with the Boulware–Deser ghost) that the record
already names as the decisive un-run calculation.**

**But the more important result is negative and it binds all three: the 'excess spent once' argument
generalises, because it uses only measured accelerations, Ω_c h², non-cancellation, and the theory's own
MOND normalisation — so the programme's remaining choice is between a working kernel and a full cold
cosmology in ANY theory of this kind, not just in this one, and even a healthy branch-2 construction would
inherit that choice.**

---

## 9. Caveats, stated rather than buried

1. **The theorem's scope is (H-c) and the cold component's galaxy profile.** The profile is an input
   (abundance-matched ΛCDM, ~0.30 dex of systematic on log M200). A theory that distributes the cold
   component away from galaxy halos escapes the theorem — and is closed separately, by this repository's
   2026-09-06/07 dark-sector no-go, which is **cited, not re-run here**.
2. **The generous of L49's two galaxy criteria is carried throughout**, so no branch is handed a
   manufactured deficit. The strict criterion would tighten every η ceiling by roughly a factor two.
3. **Branch 2 is reported OPEN, and "open" is not "promising".** Three of its seven gates have never been
   run. Nothing here says the subspace is healthy, and nothing here says it is not.
4. **The bounded-boost violation percentage was attempted and not reproduced** (§1). Its *value* is; its
   Υ-profiled SPARC rate is not, and the discrepancy is attributed to Υ profiling on L11's own recorded
   evidence rather than left as an unexplained control failure.
5. **The AQUAL stress ratio is a static, spherical, deep-MOND estimate.** It fixes the *scale* — v²/c² — which
   is what the genericity claim needs; it is not a full relativistic lensing calculation, and the
   load-bearing companion statement (a conformal factor cannot bend light) is exact and symbolic.
6. **The GW170817 bound uses the naive 1.7 s / travel-time ratio.** The published two-sided bound
   (−3e-15 < Δc/c < 7e-16) lands in the same place and does not change the conclusion.
7. **DC-013, DC-018 as a class statement, L39's operator lemma, L6's and L55's closures, and the dark-sector
   no-go are CITED, not re-derived.** Only DC-018's flux scaling is reproduced, because it is one line and
   it calibrates branch 2's first gate.
8. **Nothing here favours this framework over ΛCDM and nothing here constrains ΛCDM.** The cold component and
   its profile are ΛCDM's, imported wholesale; κ remains **fitted** (0.4998 / 0.6023).
9. **One documentation item is handed back, not edited** (E5): the LEDGER's prose status paragraph
   contradicts its own SF28/SF29 rows. It is in `qwen_claude_field_theory/closure_2026/`, which this lane
   does not touch.

---

## 10. Reproduction

```
python3 fable_independent_2026/L61_permitted_branches.py
```

Exit 0, 2.4 s. **47 checks: 37 PASS, 10 FAIL.** Eleven controls (A1–A8) rebuild the four published
mode counts, the two-metric 7-vs-8 fork, five gate numbers from the deposited theory's own gate table, and
the conformal-null-geodesic lemma — each from its own data or from scratch in sympy. Three mutation
controls (F1–F3) check that every kill switches off when its cause is removed. Every control passes.
