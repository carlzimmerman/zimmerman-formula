# L21 — binary galaxies: the regime between a galaxy and a cluster

`L21_binary_galaxies.py` (16 checks, **7 FAIL**; every control passes). Both footings throughout,
a₀ = 9.3619e-11 (canonical) / 1.1279e-10 (alt) m s⁻².

L7 left the programme with a sharp split: **clusters** need the cosmic dark-to-baryon share (5.73 ± 0.68
against Ω_dm/Ω_b = 5.43, universal to 12%), **galaxies** need the kernel and no such share. Binary galaxies
sit between — deep MOND (g_N/a₀ = 10⁻⁴ to 10⁻¹), no hot gas, no hydrostatic assumption, pure two-body
dynamics, no dark-matter fitting freedom. This lane asks which of the two governs there.

## What already existed, and what this lane adds

This is **not** a new front. The repository already carries it, and the numbers below confirm rather than
replace those:

| existing | what it established |
|---|---|
| `hunt_2026/h48_h69_binary_galaxies.py` | 2087 isolated 2MRS major pairs; framework's best case low by A = 1.74 ± 0.06, ΛCDM at 0.87; **KT2017 is unusable** (its group finder selects on the dv being measured, 48b) |
| `hunt_2026/h48_h69b_relative_isolation.py` | relative isolation (no third galaxy inside F·r_p) does not move it: A = 1.76–1.89 across F = 2…8 while ΛCDM stays at 0.90–1.06 |
| `hunt_2026/h47_dwarf_pairs.py` | 138 isolated ALFALFA dwarf pairs, 4.4 km/s velocities: A = 1.79 ± 0.20 (1.12 ± 0.29 relatively isolated); TiNy Titans is not machine-readable |
| `closure_2026/g02c_two_body_force.py` | independent QUMOND **field solve** of the two-body force, agreeing with Milgrom's analytic result to 1% |
| `hunt_2026/h81_h82_mw_external_fields.py` | the external field **computed** from 2M++: e_N = 0.01240 / 0.01027 |

L21 adds five things: the **carried, saturated kernel** instead of the pure deep-MOND limit; the
**computed** external field with an orientation-averaged anisotropic EFE response instead of a nominal
isotropic 0.02–0.03; the **cosmic-share curve**, which nobody had computed at pair separations; the
**combination** of the kernel with that share; and a pre-registerable forecast on an axis immune to the
stellar M/L.

## The machinery, and its controls

The framework's relative acceleration for a pair, from the carried kernel (`THE_ACTION_2026-09-05` §3,
ν_RAR, Δ(s) = s/(e^√s − 1) saturated at 0.6476 for s > 2.540):

> **a_rel(r) = G M_tot/r² + a₀ Δ(G M_eff /(a₀ r²))**, with
> **M_eff = (2/3)² [(M₁+M₂)^{3/2} − M₁^{3/2} − M₂^{3/2}]² / μ²**, μ = M₁M₂/M_tot.

M_eff is *defined* so the deep-MOND limit is Milgrom's exact two-body force, reused from
`h48_h69`/`g02c` rather than re-derived; the Newtonian limit is exact by construction. For an equal pair
M_eff = 0.610 M_tot and v_rel = 1.05099 (G m a₀)^{1/4}, independent of separation. Where the external
field dominates, the branch is quasi-Newtonian with the orientation-averaged QUMOND response
ν̄ = (ν_∥ + 2ν_⊥)/3 = **7.99** (canonical) / **8.73** (alt) at the computed e_N; the framework's honest
prediction is the smaller of the two branches, the isolated one being its **best case**.

Controls, all passing:

```
[PASS] C1  analytic 0.55229/0.81379 exact; vs g02c's independent QUMOND field solve 1.01% and 0.82%
[PASS] C1b v_rel -> 1.05099 (G m a0)^{1/4}: recovered 1.05096
[PASS] C2  at d = 0.01 r_M the saturated residual is 6.5e-5 of the Newtonian force
[PASS] C3  both limits exact; deep-MOND residual falls 100x for 100x in radius (the kernel's own O(sqrt s))
[PASS] C4  independent rebuild of the pair sample: N = 1900 vs 1830, sigma = 201.3 vs 200.7 km/s
[PASS] M1  scrambled partners drive the pair fraction 0.83 -> 0.00
[PASS] M2  a0 x 100 moves log10(A) by +0.477, tracking the forward model's own +0.488
```

## The three curves

σ_los for an L\* pair (M_b = 1.6e11 M_⊙, the sample median), canonical footing, km/s:

| r_p [kpc] | framework isolated | framework carried | Newton baryons | cosmic share pt | cosmic share NFW | kernel + cosmic share | ΛCDM AM |
|---|---|---|---|---|---|---|---|
| 20 | 130.5 | 129.8 | 86.9 | 220.3 | 133.1 | 256.9 | 201.3 |
| 100 | 112.5 | 102.0 | 38.8 | 98.5 | 95.0 | 186.3 | 229.8 |
| 400 | 109.0 | 54.9 | 19.4 | 49.3 | 62.7 | 139.3 | 188.2 |
| 1000 | 108.2 | 34.7 | 12.3 | 31.2 | 42.6 | 88.1 | 146.1 |

The **shapes** are what separate them without trusting the stellar M/L: framework isolated is flat in r_p
(slope −0.010) and ∝ M_b^{1/4}; Newton and the cosmic share are ∝ r^{−1/2} (−0.472) and ∝ M_b^{1/2};
abundance-matched ΛCDM is nearly flat (−0.017) and ∝ M_b^{0.9}.

## Measured, on 1900 isolated 2MRS major pairs

Sample rebuilt independently (relative isolation, no third 2MRS galaxy inside 5 r_p of the midpoint);
median r_p = 132 kpc, median log M_b(pair) = 11.19, σ_los = 201.3 ± 5.3 km/s.
A = (observed)/(parameter-free prediction); A = 1 means the law is right with no free parameter.

| law | A (canonical) | A (alt) | implied M/M_assumed | σ from 1 |
|---|---|---|---|---|
| framework, isolated (**best case**) | 1.802 ± 0.041 | 1.731 | 8.3 | 19.6 |
| framework, carried with the EFE | 2.311 ± 0.053 | 2.219 | 10.0 | 24.9 |
| Newton on baryons | 5.645 ± 0.138 | — | 31.9 | 33.6 |
| **cosmic share, point mass** | **2.222 ± 0.054** | — | 4.9 | 22.4 |
| **cosmic share, NFW** | **2.319 ± 0.053** | — | 7.7 | 25.0 |
| **framework kernel + cosmic share** | **1.141 ± 0.028** | **1.099** | 1.5 | 5.0 |
| ΛCDM abundance-matched | 0.967 ± 0.024 | — | 1.0 | 1.4 |

Separation slope: measured **d log σ/d log r_p = −0.170 ± 0.029**, against −0.010 (framework isolated,
5.6σ), −0.472 (cosmic share, 10.6σ), −0.263 (cosmic share NFW, 3.2σ), −0.224 (kernel + cosmic share,
1.9σ), −0.017 (ΛCDM AM, 5.4σ). **No law wins both axes**: ΛCDM AM wins the amplitude and loses the shape;
kernel + cosmic share wins the shape and is 5σ off in amplitude. The bins with the lever have a fitted
interloper fraction climbing 0.08 → 0.39, so this axis is systematics-limited, not statistics-limited.

## The discriminator, written to be pre-registered

For equal masses on the isolated branch the prediction is parameter-free and separation-independent:
σ_los = (1.05099/√3)(G m a₀)^{1/4} = 0.60679 (G m a₀)^{1/4}, i.e. **107.7 km/s** (canonical) /
**112.9 km/s** (alt) for two 8e10 M_⊙ galaxies at *any* separation beyond ~30 kpc.

| discrimination | N for 3σ, v_err = 40 km/s | N for 3σ, v_err = 10 km/s |
|---|---|---|
| framework vs cosmic share (point) | 384 | 122 |
| framework vs cosmic share (NFW) | 192 | 93 |
| framework vs Newton on baryons | 11 | 8 |
| framework vs ΛCDM abundance-matched | 23 | 24 |
| framework vs framework + cosmic share | 34 | 38 |
| cosmic share vs ΛCDM abundance-matched | 22 | 15 |

On the **shape** axis, which is immune to Υ_K and to the gas fraction: the framework's isolated branch and
the cosmic share differ by 0.462 in slope, so **N = 65 pairs** suffices at this data quality. Both numbers
are far below the 1900 pairs already in hand — **statistics are not the limitation, isolation depth is.**

## The scale question — the four results worth carrying forward

**1. The cosmic share is a cluster-scale statement, not a universal one.** A Newtonian reading of the pair
data requires **M_dark/M_bar = 30.9 ± 1.6 within the pair separation**, against 5.73 ± 0.68 at 0.80 R500
and the cosmic 5.43 — a factor 5.7, 16σ. The ladder is not monotone in scale and there is no "the cosmic
share turns on above some radius". At pair separations galaxies are baryon-poor relative to cosmic, which
is why abundance-matched halos (34× the baryons, not 6.4×) land at A = 0.97 and the cosmic share does not.

**2. A cosmic-share halo alone does NOT rescue the framework's regime — it does worse than the kernel.**
A = 2.22 (point) / 2.32 (NFW) against the framework's own 1.80. This is against the naive expectation and
is stated as such.

**3. The kernel and the cosmic share TOGETHER very nearly work, and neither piece does alone.**
A = 1.141 ± 0.028 (canonical) / 1.099 (alt), against 1.80 for the kernel alone and 2.22 for the share
alone, and its separation slope is the closest of any law to the measured one (1.9σ). It is still 5σ from
1, so it is not a fit — but it is the sharpest quantitative statement this regime produces: **the amount
the framework is short at pair separations is, to about 10% in velocity, the amount the cluster residual
is.** The same number appears in two regimes four decades apart in mass.

**4. Where the external field dominates, the framework's EFE and the cosmic dark share are the same law.**
Beyond ~200 kpc both are quasi-Newtonian with a constant boost — ν̄(e_N) = 7.99 against 1 + 5.43 = 6.43 —
identical in shape at every separation and every mass, differing by **11.5% in velocity**, below the
stellar-M/L systematic. This is a structural degeneracy, not a coincidence of this sample, and it means the
EFE branch cannot be tested against a cosmic-share halo at large separation by kinematics alone. The two
curves **cross at r_p ≈ 70 kpc** (g_N = 0.049 a₀); the maximum divergence over an observable 30–1000 kpc
is 0.546 dex in velocity at 1000 kpc, and it is the **isolated** branch that produces it.

## Two further findings, both against interest

**The framework's deficit grows with mass** (M0 FAIL): A(framework) climbs 1.59 ± 0.08 → 2.10 ± 0.10 across
0.56 dex in M_b, 3.9σ, while abundance-matched ΛCDM moves the other way (1.23 → 0.83). A kernel with no
scale in it forbids this. It is `h48_h69`'s 69d (σ ∝ M^{1/2} rather than M^{1/4}) seen as a trend in the
residual, and it is the axis a deeper sample should attack first.

**The galaxy-side objection to a dark component bites on shape and mass scale, not on amount** (S6 FAIL).
Computed here directly from the carried kernel and the RAR's 0.11 dex scatter rather than reused: the
tolerance on extra mass inside 10 kpc is 0.41 M_b at L\* and 0.59 M_b at a dwarf. An NFW halo carrying the
cosmic share puts 0.34 M_b inside 10 kpc at L\* — **admissible** — but 1.90 M_b at 2e9 M_⊙ — **excluded by
3.2×**. So L1/g04k's exclusion is of a *concentrated* component (cold infall delivers 0.92–1.45 M_b inside
10 kpc, 2.7× more concentrated than NFW at L\*) and of dwarfs, not of the cosmic amount as such. Any
mechanism that wants to supply the cluster residual must produce an NFW-or-shallower profile and must
switch off below ~10^10 M_⊙.

## Verbatim PASS/FAIL

```
[PASS] C1  [CONTROL] the two-body machinery reproduces the programme's verified deep-MOND two-body force
[PASS] C1b [CONTROL] the bridge's deep-MOND limit is Milgrom's own
[PASS] C2  [CONTROL] at small separation, where the acceleration is high, the prediction reduces to Newtonian
[PASS] C3  [CONTROL] the bridge is exact in BOTH limits for equal, 10:1 and dwarf pairs on both footings
[PASS] C4  [CONTROL] this lane's independent rebuild of the pair sample reproduces the repository's published one
[FAIL] M0  the framework's deficit is INDEPENDENT of the pair's baryonic mass
[PASS] M1  [mutation control] scrambling partners drives the fitted PAIR fraction to the floor
[PASS] M2  [mutation control] the amplitude responds to a0 as v ~ a0^{1/4} demands
[PASS] D1  the framework's and the cosmic-share predictions are distinguishable at all, and by how much
[FAIL] S0  [structure] the framework's EFE prediction is observationally DISTINCT from a cosmic-share halo
[FAIL] S1  the dark-to-baryon ratio the pair data require is the SAME cosmic share the clusters require
[FAIL] S2  a cosmic-share halo reproduces the pair kinematics
[FAIL] S3  the framework's carried kernel reproduces the pair kinematics on its own
[FAIL] S4  the framework's kernel PLUS the cluster-scale cosmic share reproduces the pair kinematics
[PASS] S5  existing published data ALREADY discriminate the three curves at 3 sigma
[FAIL] S6  a cosmic-share component with an NFW shape is admissible inside galaxies on the RAR gate
```

## Systematics that bound everything above

1. **Isolation depth is the leading one and it is not closed.** 2MRS at the sample's median distance sees
   only M_b > 3.6e10 M_⊙, so "isolated" means "no companion above ~23% of the pair's own mass". `h48_h69`
   measured the amplitude falling 1.99 → 1.51 as the isolation reaches four times further down the
   luminosity function. **Every amplitude here is an upper limit on the real one.** A pair sample isolated
   against a catalogue two magnitudes deeper would settle it; nothing else will.
2. **The cross-scale tension is unresolved.** ALFALFA dwarf pairs give A = 1.12 ± 0.29 relatively isolated
   where these major pairs give 1.80 ± 0.04 — 2.3σ apart, and consistent with the mass trend in M0.
3. Circular relative orbits are assumed, which is **generous to the framework** (eccentric orbits at the
   same energy spend more time near apocentre at lower speed).
4. Υ_K = 0.6, no gas in M_b. Closing the framework's amplitude gap needs Υ ≈ 7, outside any stellar
   population. The shape axis is immune to this and is why the forecast headlines it.
5. Pairs beyond ~500 kpc may not be bound; the interloper term removes chance projections, not physically
   associated unbound pairs.

## Standing after L21

Binary galaxies sit on the **failing** side, but not in the way the cluster result predicted. The kernel is
short by a factor 1.73–1.80 in velocity there (8–10× in mass), its deficit grows with mass rather than
staying flat, and its honest external-field branch is short by 2.2–2.3×. A cosmic-share halo — the exact
quantity clusters demand — is short by more still, 2.22–2.32×, so the cluster answer does not simply
extend downward. What does land near 1 with no fitted parameter is the **combination**: kernel plus cosmic
share, A = 1.10–1.14. Read against L7 that is a real and testable structural hint, and read against S0 it
comes with a warning — in the external-field regime this programme's EFE and ΛCDM's dark share are the
same law to 12% in velocity, so the discriminating power lives entirely on the **isolated** branch, at
r_p ≳ 300 kpc, in samples isolated far deeper than 2MRS can manage.
