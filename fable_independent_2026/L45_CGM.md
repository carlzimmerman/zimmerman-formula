# L45 — undetected baryons at pair separation: L41's last open door, **CLOSED by observation**

`L45_cgm_baryons.py` + `.out` — **18 checks, 8 PASS, 10 FAIL; the FAILs are the finding.** Runs in 7 s.
Both a₀ footings (9.3619e-11 canonical, 1.1279e-10 alt) throughout.

L41 assembled the specification the cluster source must meet, proved it **not self-consistent**, and left
**exactly one door open** — its check B5, the possibility that the galaxy pairs' baryons are *undercounted*.
It wrote that the door "is closed, if at all, by circumgalactic-medium mass budgets … which is a literature
question this lane does not settle and does not claim to."

**This lane settles it.** The door is **CLOSED**, by six independent local measurements, on every reading of
the requirement including L41's own smallest one.

---

## 0. Stated before the computation: there was no outcome here that was a win

If undetected baryons *had* supplied the pair requirement, that would **not** have been a win for this
framework. It would be a free function of host mass and environment — exactly what ΛCDM's galaxy-formation
sector already contains — and L41 said so in its own R11. The result is a **cost either way**. Nothing here
claims data favour this framework over ΛCDM; they do not, and L41's E1 showed ΛCDM's abundance-matching
relation predicts the pair ratio to 0.6σ with nothing fitted.

---

## 1. The controls, first

| control | reproduced here | published | source |
|---|---|---|---|
| **A1** pair ratio | N = **1900**, A_Newton = **5.645 ± 0.136**, M_dark/M_bar = **30.9 ± 1.5** | 30.9 ± 1.6 | L21 S1 |
| **A2** cluster ratio at the pair's own radius | **9.20 ± 1.30** at 132 kpc; gap **3.4× at 11σ** | 9.20 ± 1.30, 3.4×/11σ | L41 A1 |
| **A3** cosmic baryon fraction | Ω_b/Ω_m = **0.1564**, Ω_dm/Ω_b = **5.39**; Ω_b h₇₀ = 0.0457 vs the FRB-measured 0.051 ± 0.006 (**0.9σ**) | Planck 2018 VI; Connor+ 2025 | new here |
| **A4** galaxy-scale baryon deficit | Bregman+ 2022's own accounting reassembles to a hot phase = **33%** of the cosmic share (they quote ~30%) and an implied halo of 1.90e12 M⊙; abundance matching puts the **stars** at **16%** of an L\* halo's share | ~30%; "galaxies retain ~20% in stars" | new here |
| **A5** the pair forward model | A = **1.802 / 1.731** (canonical/alt), implied M/M_K = **8.34** (isolated) and **10.14** (carried) | 1.802 / 1.731; 8.3 and 10.0 | L21 |

A3 and A4 are the brief's required budget-machinery controls: the machinery reproduces a published cosmic
baryon fraction *and* a published galaxy-scale baryon deficit before it is used against the requirement.

---

## 2. THE REQUIREMENT, recomputed from L21's own data

Per **galaxy**, inside the pairs' own median separation **r_p = 132 kpc**, against a K-band stellar mass of
**7.75e10 M⊙** (Υ_K = 0.6, no gas):

| reading | M_b,true / M_K | M_b,true [M⊙] | **undetected** [M⊙] |
|---|---|---|---|
| Newton on baryons alone (no kernel, no dark) | 31.86 | 2.47e12 | **2.39e12** |
| **the framework's carried kernel, ISOLATED branch (its best case)** | **8.34** | **6.46e11** | **5.68e11** |
| the framework's carried kernel with the computed external field | 10.14 | 7.86e11 | 7.08e11 |
| baryons **plus** a cosmic-share dark component (L41's own B5 reading) | 4.96 | 3.84e11 | 3.06e11 |

**The operative number is the framework's own best case: 5.68e11 M⊙ of undetected baryons inside 132 kpc of
an L\* galaxy — 7.3 stellar masses of invisible gas** (6.3 on the alt footing; the Newtonian and
cosmic-share readings are footing-free because a₀ cancels). L41's B5 quoted 4.96×; that is reproduced, and
the framework's own 8.34× is larger and is the one that matters.

**The profile freedom is priced and it does not help.** Every gram inside r_p projects inside r_p, so the
**mean column over the disc of radius r_p is fixed by the mass alone**, at any profile:

```
<N_H> = 9.22e20 cm^-2 ,   <DM> = 354 pc cm^-3 ,   <n_e>(<r_p) = 2.01e-3 cm^-3
```

At b → 0 the whole family ρ ∝ r^−α spans only a **factor 3**: the uniform sphere gives 1.5× the mean, and
the least detectable configuration there is — a thin shell at r_p — gives exactly 0.5×.

---

## 3. THE THREE-WAY CONFRONTATION

### (a) Is the required mass inside the total baryon budget? — **C1 PASS, but at the ceiling**

Abundance matching at M\* = 7.75e10 gives M200 = 5.63e12 M⊙ (R200 = 376 kpc); its **entire** cosmic baryon
allotment is 8.81e11 M⊙. The requirement is **73% of the whole allotment**, all of it inside **0.35 R200**
and none of it anywhere else in the halo. On a conservative halo mass (2.5e12) it is **165%** — more than
the halo owns. Framework-agnostically: gathering 6.46e11 M⊙ of baryons needs a comoving Lagrangian sphere of
**2.92 Mpc swept to 100% efficiency**, against the 3.23 Mpc the halo's own mass corresponds to.

**This arm passes and is reported as passing.** The galaxy plausibly *has* that many baryons somewhere. The
kill is that they are not *there*.

### (b) Is it consistent with the observed radial distribution? — **C2, C6, C8 FAIL**

| measurement | as published | scaled to 132 kpc |
|---|---|---|
| Werk+ 2014 COS-Halos cool phase, **its own fitted n_H(r)** | > 6.5e10 within R_vir | 5.56e10 |
| Bregman+ 2018 X-ray hot halo, **its own ρ ∝ r^−1.5** | 5.0e9 within 50 kpc | 2.15e10 |
| Bregman+ 2022 thermal SZ (density-linear) | 9.8 ± 2.8e10 within 250 kpc | 3.77e10 |
| **sum of the detected phases** | | **7.71e10** |
| **REQUIRED** | | **5.68e11** |

**C2 FAIL: 7.4× over at the same radius**, and **3.5× over** against the most generous possible reading —
the *full* SZ mass at 250 kpc plus the *full* COS-Halos cool mass within R_vir (1.63e11 M⊙), at twice the
radius. That is 17σ on the SZ statistical error alone. Three independent probes — UV absorption, X-ray
emission and the thermal SZ — agree on the amount and none leaves room.

**C6 FAIL, the one place the density is weighed dynamically.** Salem+ 2015 measure the Milky Way's halo from
the ram-pressure stripping of the LMC's disc: n = 1.10e-4 ± 4.4e-5 cm⁻³ at 48.2 kpc. The requirement, in its
shallowest and most favourable configuration, gives **2.01e-3 cm⁻³ there — 18×**. *Stated against interest:*
this single arm **is** evadable by a hollow configuration; but the hollow limit is the thin shell, which C3
and C5 then catch at 1.5× and 12×, and which C4 catches worst of all because a shell *maximises* ∫n²dV.

**C8 FAIL, and it is the framework's own kernel that fires it.** The Milky Way is the one galaxy whose
enclosed mass at ~100 kpc is measured directly.

```
framework kernel on the DETECTED baryons (6.0e10)  ->  M(<100 kpc) = 6.65e11 (canonical) / 7.27e11 (alt)
the same kernel with the escape's 1.58e11 added     ->              1.32e12          / 1.44e12
measured (Deason+ 2021, halo stars)                 ->              6.07e11 +/- 1.24e11
```

With the **detected** baryons the kernel lands at **0.5σ**. With the escape's baryons it over-predicts by
**2.2× at 5.8σ, on both footings**. (The 0.5σ is a genuine success of the *kernel* and is recorded as one —
but it is **not** a discriminant, because a ΛCDM halo fits the same number by construction.)

*Priced against interest:* L21's M0 found the framework's deficit **grows** with host mass (A = 1.59 in the
lowest mass bin against 1.80 for the sample), and the Milky Way sits at the low-mass end, so the fair
requirement there is **5.36×** rather than 8.34×. That gives 9.41e10 M⊙ and a predicted M(<100 kpc) of
1.10e12 — **1.8× measured at 3.9σ**. Weaker, still a fail; the check carries the sample value and this is the
honest floor.

### (c) Is it excluded by non-detection? — **C3, C4, C5 FAIL; C7 PASS**

| channel | required | measured | over by |
|---|---|---|---|
| **dispersion measure** at the FRB's own b = 29 kpc | 519 pc cm⁻³ (uniform); **182 for the family minimum** | 50–120 (Prochaska+ 2019, FRB 181112 through a *more massive* galaxy at a *smaller* impact parameter) | **4.3× (1.5× at the family minimum)** |
| **X-ray emission** (∫n²dV) | — | Bregman+ 2018 / eROSITA stacks | **697× at matched shape; 167× even granting the minimum-emission uniform configuration** |
| **absorption column** | ⟨N_H⟩ = 9.22e20 cm⁻² (profile-free) | 4.0e19 cm⁻² (Werk+ 2014, mean log N_H = 19.6, *after* a ×100 ionisation correction) | **23×** |
| **global FRB baryon partition** | 0.42 ± 0.08 of all cosmic baryons inside 132 kpc of a galaxy | 0.41 ± 0.10 (FLIMFLAM DR1) / 0.24 ± 0.10 (Connor+ 2025) | **+0.1σ / +1.3σ — PASSES** |

The mean density 2.01e-3 cm⁻³ also sits **exactly at** Prochaska+ 2019's own ceiling n_e < 2e-3 cm⁻³ for hot
virialised halo gas, which any centrally concentrated profile then exceeds.

**C7 is reported as a PASS.** The global partition is a real tension but not a kill — the two published FRB
analyses disagree with each other by more than the effect. The kill is C2–C6, which are local and much
sharper.

### Which phase could it be?

| phase | channel | requirement exceeds by |
|---|---|---|
| hot, T ~ 10^6.3 K (virial) | X-ray emission (n²) | 167× |
| warm-hot, 10⁵–10⁶ K | dispersion measure + O VI/O VII | 4.3× |
| cool photoionised, 10⁴ K | Lyman-α + metal columns | 23× |
| cold neutral atomic | every sightline would be a DLA | 4.6× the 2e20 cm⁻² threshold |
| **cold molecular clumps** | **none of the above directly** | **not excluded by these channels** |
| compact objects (MACHOs) | microlensing (EROS-2, Tisserand+ 2007) | < 8% of a halo |

**The one surviving phase is cold, dense, neutral molecular gas with a tiny volume filling factor** — and
Prochaska+ 2019's same sightline bounds exactly that at f_V < 1e-4. It is closed independently by **D1**,
which is blind to phase and counts only mass.

### Sensitivity: does the verdict depend on which reading is used? — **No**

| reading | M_b/M_K | M_hid [M⊙] | /CGM(132) | /CGM(generous) | ⟨DM⟩ | ⟨N_H⟩/obs | EM floor |
|---|---|---|---|---|---|---|---|
| Newton on baryons alone | 31.86 | 2.39e12 | 31.0× | 14.7× | 1491 | 97× | 2950× |
| framework kernel, carried with the EFE | 10.14 | 7.08e11 | 9.2× | 4.3× | 442 | 29× | 259× |
| framework kernel, isolated (best case) | 8.34 | 5.68e11 | 7.4× | 3.5× | 354 | 23× | 167× |
| baryons + cosmic-share halo (L41's B5) | 4.96 | 3.06e11 | 4.0× | 1.9× | 191 | 12× | 48× |

**Every reading fails every local arm**, including L41's own cosmic-share reading, which is the smallest of
the four. And the systematics run the *right* way for the escape and are priced: taking L21's own
deepest-isolation amplitude A = 1.51 lowers the requirement to **4.5× the K-band mass (2.70e11 M⊙)**, which
is still **4× the measured CGM at 132 kpc** and 169 pc cm⁻³ in mean dispersion measure against 50–120.

---

## 4. THE CONSEQUENCES — can one distribution serve all four? **No. D4 FAIL, 1 of 4.**

### D1 clusters — **FAIL, and this is the structural kill**

The rule is host-blind by construction, so it must also apply to the galaxies *in* clusters, where the
baryon fraction is measured. X-COP publishes both M_gas and M_star:

| cluster | M_gas | M_star | M_HSE | f_bar | f_bar with the rule | / cosmic |
|---|---|---|---|---|---|---|
| A1795 | 5.51e13 | 3.78e12 | 3.78e14 | 0.156 | 0.229 | 1.46 |
| A2029 | 8.06e13 | 6.12e12 | 6.21e14 | 0.140 | 0.212 | 1.35 |
| A2142 | 9.06e13 | 6.00e12 | 6.35e14 | 0.152 | 0.221 | 1.42 |
| A2319 | 9.16e13 | 5.35e12 | 6.44e14 | 0.151 | 0.212 | 1.35 |
| A644 | 5.93e13 | 4.28e12 | 4.95e14 | 0.128 | 0.192 | 1.23 |
| A85 | 6.47e13 | 2.37e12 | 4.50e14 | 0.149 | 0.188 | 1.20 |
| ZW1215 | 5.73e13 | 3.55e12 | 5.27e14 | 0.115 | 0.165 | 1.05 |

The median cluster baryon fraction runs **0.149 → 0.212 = 1.35× cosmic**, in **7 of 7** clusters. A cluster
cannot hold more baryons per unit mass than the universe does. **And the framework's own reading makes it
worse**: its kernel says the true gravitating mass is *below* M_HSE, which raises f_bar further.

The only repair is to make the rule **environment-dependent** — gas retained in the field, stripped and
already-counted in clusters — which is a **second** free function on top of the first.

### D2 rotation curves — **PASS, for shallow profiles only**

Tolerance recomputed from the RAR's own 0.11 dex scatter: 0.408 M_b inside 10 kpc at L\*, 0.589 at a dwarf.
Scanning ρ ∝ r^−α truncated at r_p (with the dwarf truncation scaled as M\*^(1/3), the choice generous to
the escape), the admissible window is **α ∈ [0.00, 1.00]**; α ≥ 1.25 fails at the dwarf. **This arm does not
close the door** — L41 already found that, and it is reproduced here.

### D3 lensing shape — **FAIL: the escape does not touch it**

The escape's added component is (F−1)·M_star(r), and over 0.5–2 Mpc it moves the cluster baryon
enclosed-mass log-slope by only **−0.109** (+1.256 → +1.147). The amount that *would* matter is precisely
the amount D1 excludes. L24's 9σ shear-slope failure (framework −0.309 vs measured −0.851 ± 0.040), R3's 3-D
shape and R4 are left **exactly where L41 found them**.

### D4 — the joint test

```
[FAIL] pairs           -- supplies 30.9 M_bar inside 132 kpc     needs 5.7e11 Msun; measured CGM there 7.7e10
[FAIL] clusters        -- keeps f_bar at or below cosmic         f_bar 0.149 -> 0.212 = 1.35x cosmic
[pass] rotation curves -- under 0.41 M_b inside 10 kpc           passable for alpha <= 1.00
[FAIL] lensing shape   -- reaches -0.851 +/- 0.040               untouched at -0.309, 9 sigma short
```

**The two arms that decide fail in OPPOSITE directions**: the pairs need more gas than is observed, and the
clusters cannot absorb any. No single distribution reconciles them.

---

## 5. Verbatim PASS/FAIL

```
[PASS] A1 [CONTROL] an independent rebuild of the 2MRS pair sample reproduces L21's Newtonian amplitude 5.645 and its dark-to-baryon ratio 30.9 +/- 1.6 inside the pair separation
[PASS] A2 [CONTROL] this lane reproduces L41's fixed-radius cluster value 9.20 +/- 1.30 at 132 kpc and its 3.4x/11 sigma gap against the pairs, from the same cluster data
[PASS] A3 [CONTROL] this lane's baryon-budget machinery reproduces a published cosmic baryon fraction: Planck's Omega_b/Omega_m = 0.156 and Omega_dm/Omega_b = 5.4, and agrees with the FRB-measured Omega_b
[PASS] A4 [CONTROL] this lane's baryon-budget machinery reproduces a published galaxy-scale baryon deficit: Bregman+ 2022's ~30% hot-halo share of the cosmic budget and abundance matching's ~20% stellar share
[PASS] A5 [CONTROL] the forward model reproduces L21's published framework amplitudes 1.802 (canonical) / 1.731 (alt) and its implied mass factors 8.3 (isolated) and 10.0 (carried)
[PASS] C1 (a) the required mass is inside the system's total baryon budget -- the galaxy has that many baryons to hide
[FAIL] C2 (b) the required mass is consistent with the observed radial distribution: that much CGM is measured at ~130 kpc
[FAIL] C3 (c-i) the implied dispersion measure is consistent with the FRB constraints on foreground galaxy halos and on the Milky Way's own halo
[FAIL] C4 (c-ii) the implied X-ray emission is consistent with the measured hot halos of L* galaxies
[FAIL] C5 (c-iii) the implied absorption column is consistent with the measured circumgalactic hydrogen column at these radii
[FAIL] C6 (b/c) the implied in-situ gas density agrees with the one place it is measured directly, the Milky Way's halo at ~50 kpc
[PASS] C7 (c-v) the global baryon partition measured by fast radio bursts allows this much mass inside 132 kpc of galaxies
[FAIL] C8 (b) the required baryons are compatible with the Milky Way's directly measured enclosed mass at 100 kpc, run through the framework's own kernel
[FAIL] D1 the same host-blind rule, applied to the clusters' own measured stellar mass, keeps the cluster baryon fraction at or below the cosmic value
[PASS] D2 some member of the profile family puts little enough inside 10 kpc to leave the rotation-curve fit intact at BOTH L* and dwarf scale
[FAIL] D3 the escape repairs, or even moves, L24's 9 sigma cluster lensing-shape failure
[FAIL] D4 [THE JOINT TEST] a single undetected-baryon distribution serves the pairs, the clusters, the rotation curves and the lensing shape at once
[FAIL] E1 [VERDICT] the undetected-baryon escape survives the observational confrontation, i.e. L41's last door remains OPEN
```

---

## 6. What this does and does not say

1. **This is a cost for the framework and not a result in its favour.** Had the escape survived, that would
   *also* have been a cost — ΛCDM's galaxy-formation sector imported wholesale, exactly as L41 wrote.
2. **Nothing here constrains ΛCDM.** ΛCDM does not need the escape: its missing baryons are **ejected** to
   large radii and to the IGM by feedback — which is what the FRB partition, the SZ profile and the eROSITA
   extrapolation to ~3 R_vir all measure. The framework needs them **bound and inside 132 kpc**, and that is
   the specific thing the data exclude.
3. **The framework's kernel passes the Milky Way's M(<100 kpc) on the detected baryons at 0.5σ.** Real, and
   recorded as such — but not a discriminant.
4. **Systematics are priced and run toward the escape.** L21's amplitudes are upper limits; even its
   deepest-isolation A = 1.51 leaves the requirement 4× the measured CGM.
5. **The observation that would reopen this**, if anyone wants to: a **stacked FRB dispersion-measure excess
   behind isolated L\* galaxies at 100–150 kpc, at the ~10 pc cm⁻³ level**. Current samples do not reach it.
   That, not a theoretical argument, is what would move this verdict.

---

## 7. Three-sentence verdict

**The door is CLOSED by observation.** The framework's own carried kernel needs **5.68e11 M⊙ of undetected
baryons inside 132 kpc of an L\* galaxy — 7.3 stellar masses of invisible gas** — and while that is
formally inside the halo's cosmic allotment (73%, C1 PASS), it is **7.4× the summed measured circumgalactic
medium at the same radius**, **23× the COS-Halos hydrogen column** (a mean column fixed by the mass alone,
so no profile evades it), **4.3× the FRB-measured foreground-halo dispersion measure**, **18× the
ram-pressure-weighed Milky Way halo density at 48 kpc**, **167×** the X-ray emission measure even in its
minimum-emission configuration, and it makes the framework's own kernel over-predict the Milky Way's
directly measured M(<100 kpc) by **2.2× at 5.8σ on both footings** (1.8× at 3.9σ on the low-mass amplitude
that is fairer to the Milky Way) — while every smaller reading of the requirement, including L41's own,
fails every one of those arms too.

**No single distribution serves all four constraints (D4, 1 of 4):** the pairs need more gas than is
observed and the clusters cannot absorb any — applying the same host-blind rule to X-COP's own measured
stellar mass drives the cluster baryon fraction to **1.35× cosmic in 7 of 7 clusters** — the rotation-curve
gate is passable only by shallow profiles, and the escape leaves L24's 9σ cluster lensing-shape failure
**untouched**, moving the enclosed-mass slope by 0.109 where the amount that would matter is exactly the
amount the cluster baryon fraction forbids.

**This is a cost for the framework and not a win, and it constrains ΛCDM not at all** — ΛCDM's missing
baryons are ejected to the IGM, which is where the FRB partition, the SZ profile and the eROSITA
extrapolation find them, whereas the framework requires them bound at 100 kpc, which is the one thing the
data exclude; the single surviving loophole is cold molecular clumps with a filling factor below 1e-4, and
that is closed independently by the cluster baryon fraction, which is blind to phase and counts only mass.

---

*Sources searched and read for this lane (not recalled): Planck 2018 VI (Aghanim+ 2020); Werk+ 2014 ApJ 792,
8; Tumlinson, Peeples & Werk 2017 ARA&A 55, 389; Bregman+ 2018 ApJ 862, 3; Bregman+ 2022 ApJ 928, 14;
Salem+ 2015 ApJ 815, 77; Prochaska+ 2019 Science 366, 231; Prochaska & Zheng 2019 MNRAS 485, 648; Khrykin+
2024 ApJ 973, 151 (FLIMFLAM DR1); Connor+ 2025 Nature Astronomy (DSA-110); Deason+ 2021 MNRAS 501, 5964;
Tisserand+ 2007 A&A 469, 387 (EROS-2); Zhang+ 2024 A&A (eRASS:4 hot CGM stacking); Moster, Naab & White 2013.*

*Handed back, not edited here:* L41 §2.4's B5 entry can be marked settled — the door it left open is closed,
and the requirement it priced at 4.96× is the *smallest* of four readings, all of which fail. FINDINGS' L41
entry and HANDOFF_CONTRACT are owned by other lanes and were not touched.
