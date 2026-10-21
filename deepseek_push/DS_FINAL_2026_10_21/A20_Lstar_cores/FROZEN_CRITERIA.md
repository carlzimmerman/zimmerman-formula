# A20 — FROZEN CRITERIA (pre-registration)

Written **before** any data-derived number in this lane was computed, and not edited afterwards.
Script `a20_checks.py` implements exactly these rules. If a rule is violated the script prints FAIL.

Lane: A20. Date: 2026-10-21. Repo: `zimmerman-formula`, `deepseek_push/DS_FINAL_2026_10_21/A20_Lstar_cores/`.

---

## 0. What is being tested

The theory (A16, verified) makes a **one-length** statement: the `Gamma = 2` contact pressure of the cold
sector switches off where its gradient equals gravity,

    R(r) ≡ |(1/rho_c) dp/dr| / g  =  (L*/r)^2 ,      R(L*) = 1 ,        (F1)

for every cusp `rho_c ∝ r^-n` with `1 <= n <= 2` (the ratio is density-free: `n` and `rho_c` cancel).
So every halo carries a pressure-supported **core of size L***, and `L*` is **one number**.

This lane measures whether the data can see that core, and which candidate formula for `L*` survives.

## 1. The no-juggling guard (C1 — the load-bearing criterion)

**C1.** `L*` is **ONE scalar, identical for every galaxy.** No per-galaxy value, no dependence on `V_f`,
`M_b`, `sigma_obs`, morphology, distance or inclination may enter. A candidate that predicts a
*distribution* of `L*` fails C1 **before any data are consulted**, and by an amount measured as
`spread = log10(L*_max/L*_min)` over the sample. C1 requires `spread = 0` exactly.

**C2.** Any candidate formula for `L*` must be built from quantities already in the theory:
`{a0, c, G, H0, Lambda, rho_Lambda, kappa}` — plus, at most, one *medium* property that the theory itself
defines (`sigma_c`, the cold-sector dispersion). A candidate may **not** import a galaxy property
(`V_f`, `M_b`, `r_M`) as an input, because that is per-galaxy freedom wearing a formula's clothes.

**C3.** `L* ∈ [24 pc, 1 kpc]` — the record's window (A11 §15, `sigma_c = sqrt(a0 L*)` at the two ends).
A candidate that places `L*` outside the window for any galaxy in the sample fails C3 for that galaxy;
the failure statistic is the **fraction of the sample outside the window**.

**C4.** The **independent observable** is the velocity dispersion of the cold medium implied by the
candidate, `sigma_c = sqrt(a0 L*)`. It must agree with the measured cold-phase dispersion of nearby
galaxies within a factor **2**. Reference values, fixed before the test:
`sigma_thermal = 8.23 km/s` (`10^4 K`, `mu = 1.22`; AG6D B7 via A11 §15) and the observed cold/warm HI
dispersion range `6-10 km/s` (second-moment maps of nearby spirals and dwarfs). The agreement statistic is
the ratio `sigma_c(implied) / 8.23 km/s`.

**C5.** A single `L*` must not predict a core larger than the best-resolved data allow:
`R_core = (pi/sqrt2) L* = 2.2214 L*  <=  R_turn`, where `R_turn` is the measured radius at which the
total rotation curve's logarithmic slope has fallen to `0.3` (LITTLE THINGS `R0.3`, Oh+2015 Table 2).
Inside a constant-density core `v ∝ r` (slope 1), so a core larger than `R_turn` is excluded by the
measured slope at `R_turn`. Because `L*` is one number, **the single best-resolved galaxy bounds the
whole sample.**

## 2. The candidate formulas, frozen as stated in the record

**Candidate 1** — `L* = sigma_c^2 / a0`  (A11 §15: `24 pc <-> 8.33 km/s`, `1 kpc <-> 53.74 km/s`).
Inverted for the observable: `sigma_c = sqrt(a0 L*)`. No galaxy property enters. One number if `sigma_c`
is one number.

**Candidate 2** — `L* = V_f^2 / (k a0)`, with `k = 9` **fixed by the record** (A11 §15: the upper window
end is `V_f^2/(9 a0)` for `V_f = 165.2 km/s`, motivated by `CONDITIONAL(sigma_c <= V_f/3)`). `k` is **not**
fitted here; it is taken at 9 and the result is also reported at `k = 1` (where candidate 2 degenerates to
`L* = r_M`, the MOND radius). `V_f` is measured per galaxy, so candidate 2 predicts a **distribution** of
`L*`.

## 3. Decision rule (frozen)

For each candidate, in this order:

1. **C1 gate.** `spread > 0.3 dex` ⟹ **FAIL C1**, reported as `NO-GO(C1)` regardless of anything else.
2. **C3 test.** Report the fraction outside `[24, 1000] pc`. `> 10 %` ⟹ FAIL C3.
3. **C4 test.** Report `sigma_c/8.23`. Outside `[1/2, 2]` ⟹ FAIL C4.
4. **C5 test.** Report `2.2214 L* / R_turn,min`. `> 1` ⟹ FAIL C5.

A candidate **survives** only if it passes C1, C3, C4 and C5 in the same row (the same `L*` value).
The headline killing number for each failure is the statistic in that row.

**Pre-registered expectation, stated to be falsifiable:** candidate 2 fails C1 and C4; candidate 1
survives only in the lower part of the window (a `sigma_c` near `8.3 km/s`, i.e. `L* ~ 24 pc`), because
`1 kpc <-> 53.7 km/s` is not a *cold* medium. If candidate 1 fails C5 as well, the lane returns
`NO-GO(C5)` for the whole window.

## 4. Measurement conventions, frozen

- **SPARC**: 175 `*_rotmod.dat` curves, distance from the `# Distance = ... Mpc` header. The tabulated
  innermost radius is `r_first`. The **beam floor** is `theta x D` with `theta = 30"` — the typical HI beam
  of the SPARC compilation (labelled `[EXT]`, sensitivity reported at 15" and 60"). The **innermost
  reliable radius** is `r_rel = max(r_first, theta D)`. Both `r_first`-based and `r_rel`-based fractions
  are reported; the `r_rel` one is the conservative/primary one.
- **LITTLE THINGS** (Oh+2015, on disk at `_external_data/little_things_oh2015`): 26 dwarfs, `~6"` beam,
  linear resolution 20-530 pc (per-galaxy beam `= Rmax/(Rmax/HI_beam)` from Table 2). Core bound uses
  `R0.3` from Table 2 (distance-independent, no beam assumption).
- **MIGHTEE-HI DR1 cubes** (`_external_data/hi_profiles_2026_10_18`, `mightee_pipeline_2026_10_19`):
  recorded `beam_arcsec = 75.6"`, `radius = 113.4"`. Their linear resolution at `z ~ 0.03` is `~49 kpc`;
  they are recorded as **unusable for a core bound** and are not used as evidence.
- `L*` grid for the prediction tables: `24, 100, 300, 1000 pc`. Halos: **MW-like** `M_b = 6e10 Msun`,
  Hernquist `a = 1.5 kpc` (`V_f = 165.2 km/s`, `r_M = 9.453 kpc`); **dwarf-like** `M_b = 1e8 Msun`,
  Hernquist `a = 0.7 kpc` (`V_f = 33.4 km/s`, `r_M = 386 pc`). `Upsilon`-free: `M_b` is the only baryonic
  input and it is a *halo* choice, not a fit to the `L*` question.

## 5. What would count as a detection (frozen)

A **detection** of the core requires at least one galaxy with `r_rel < L*`. If `r_rel > L*` for every
galaxy in a sample, that sample returns a **null**, not a bound, and the null must be reported as such
(with the number of galaxies that *could* have seen it).

A **bound** requires `2.2214 L* > R_turn` in at least one well-resolved galaxy (C5).

Both numbers are computed for every candidate and both are reported.

## 6. Post-hoc note on §4 (data description only — no criterion changed)

§4's estimate "linear resolution at `z ~ 0.03` is `~49 kpc`" was written before the cube header was read.
The measurement in `a20_checks.py` (K10) gives `z = 0.047`, `D_L = 216.2 Mpc`, `75.6" -> 79.3 kpc`, i.e.
3302x `L*`. The conclusion of §4 (unusable for a core bound, not used as evidence) is unchanged and the
criterion C1–C5 were not touched.
