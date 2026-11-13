# FINAL5 FROZEN CRITERIA — the decisive measurement that closes the amount question

Committed **alone**, before any script, any download and any number. TEST lane, quarantined;
adopts nothing, relabels nothing, registers nothing. Form B = the a0 law with cold dark energy
counted once; kappa = 1/2 FITTED; not theory closed. Footings canonical (a0 9.3603e-11) and
alt (1.1312e-10), never pooled.

---

## 0. What GAS1 left open, and what this lane freezes

GAS1 (HY4-1) showed that the gas that would put Form B's demand inside the cosmic budget is a
**fixed surface density**

    Sigma_gas = a0 / (pi G x_b^2),     x_b^2 = R_b (1 + R_b) = 5.41 x 6.41 = 34.6781

extending from `R_budget = x_b r_M` outward, and that this column is 284-574x every baryon in
the volume, 328-3750x B21's own hot gas, and +8.0 to +16.3 sigma against GO1's measured group gas.

It closed the galaxy leg **as an argument**, not as a measurement: it needed published gas numbers
that do not exist at Mpc radii around isolated galaxies. This lane freezes the observation that
would supply them. It grades **nothing about the theory** — it grades whether the reading's required
column is there.

**The key realisation (stated before any number):** the required column makes `g_bar` a *constant*
at those radii:

    g_bar(R) = G M_bar(<R)/R^2 = G (pi R^2 Sigma_gas)/R^2 = pi G Sigma_gas = a0 / x_b^2 = const

So the prediction is not "extra gas", it is **a flat baryonic acceleration of a0/34.6781 =
2.6993e-12 m/s^2 from ~66 kpc to 2.6 Mpc around every isolated L\* galaxy**. That is a
predicted *observable*, and the thermal SZ (`y`) is linear in exactly the required column:

    y(b) = (sigma_T/(m_e c^2)) kT_e * N_e(b),      N_e(b) = Integral n_e dl = Sigma_proj(b)/(mu_e m_p)

`N_e` is the **electron column**, i.e. the required surface density itself, in cm^-2. No clumping
factor enters, no squared-density bias enters, and (for the sheet) y is **flat in b**. This makes the
stacked tSZ the primary test — not the X-ray surface brightness, which is quadratic in the density
and therefore both clumping-biased and far fainter at 2.6 Mpc.

---

## 1. The target class (frozen, no tuning after the fact)

| item | value | source |
|---|---|---|
| Parent catalogue | KiDS-1000 / KiDS-DR4 bright lenses, `real_research/data/lensing_rar/lr_lenses.npz` | **on disk** |
| Candidates | 181,477 lenses, 1000 deg^2, z < 0.5 | **on disk** (GAS1 KA6) |
| Isolation cut | KO1 "host-free": no neighbour with `Delta = 0.3` dex more stellar mass inside a line-of-sight window `W = 230` Mpc (comoving), KO1's plain float tie rule; veto radius `F R_h`, `R_h = min(3 Mpc, sqrt(G Mgal/1e-15))` | **on disk** (GAS1 FROZEN §3; CFG96 `_kids_split_isolation`) |
| Veto F (primary) | **1.6** R_h | on disk (GAS1; ONE1's graded radius) |
| Expected P1 count | **17,335 lenses** (23 % of candidates) | on disk (GAS1 KA6) |
| Brackets on F | 1.0, 1.3, 1.6 | on disk (KO1 E7) |
| z distribution (catalogue) | 5/25/50/75/95 pct = 0.161 / 0.245 / 0.308 / 0.367 / 0.432 | **computed here** |
| log10 Mgal (catalogue) | 5/25/50/75/95 pct = 9.82 / 10.37 / 10.67 / 10.86 / 11.00 | **computed here** |
| Representative stack baryon mass | `<M_b> = 8.42e10 Msun` -> `r_M = 11.20 kpc` -> `R_budget = 65.9 kpc` | on disk (GAS1 §2 table) |

**Why this class.** The column requirement `(a0/G) R^2 / x_b^2` depends on **R alone** — it does
not care what the galaxy is. Three consequences drive the choice:
1. **Isolation is the whole point.** Any neighbour, group or filament contributes its *own* gas at
   Mpc radii; the test is whether an L\* galaxy in isolation carries a cluster's gas column. The
   host-free cut (0.3 dex, 230 Mpc, 1.6 R_h) is the strictest such cut the record has already
   run and reproduced (GAS1 KA6: 40,667 / 25,708 / 17,335 at F = 1.0 / 1.3 / 1.6).
2. **L\*, not dwarfs or clusters.** GAS1 §8: at cluster scale the required column is *within a factor
   ~1* of what X-COP measures (0.37-1.26), so clusters cannot decide it. Dwarfs sit at radii
   where R_budget is small but their gas is not measured either. L\* is where the requirement is
   already 11x the entire cosmic budget while the *total* halo mass is independently known
   (M200 ~ 1e12), so the prediction is *impossible*, not merely implausible.
3. **The sample already exists, with weights and mocks.** GO1's Part A pipeline
   (`closure_2026_11_10/GO1_group_outskirts/go1_measure.py`, `go1.py`) already stacks KiDS shear
   **and** the ACT y map with randoms, jackknife errors, a gNFW beam correction, two CIB treatments
   and three nulls. This measurement is GO1 with the sample swapped from 102 eRASS1 groups to
   17,335 KiDS isolated lenses. Nothing new has to be written to run it.

## 2. The instrument (named, with provenance)

**Primary — ACT DR6.02 needlet-ILC Compton-y map (LAMBDA), already on disk.**
- `<home>/new_physics/_external_data/act_dr6_nilc/strip_ComptonY.f32be` (829,785,600 B)
- `strip_ComptonY_deproj_cib_1.0_10.7.f32be` (the same strip, CIB-deprojected)
- `header_ComptonY.fits`, `header_ComptonY_deproj_cib_1.0_10.7.fits`, `strip_geometry.txt`
- Grid 43200 x 10320 CAR, CDELT = 0.0083333 deg = **0.5 arcmin/pix**; strip = rows 3239-8040,
  i.e. **Dec -36 deg to +4 deg** — this is the KiDS-S footprint, so the lens catalogue and the map
  overlap by construction.
- **Beam 1.6 arcmin Gaussian** — from `FETCH_LOG.md`. Cite Coulton et al. 2024 (PRD 109, 063530).
- **Noise: not from memory.** It is taken from GO1's own measured stacked y error
  (`go1.json`, `primary/full/sig_at/x/Gy`): sigma(M_gas^y) = 6.9e12 Msun for the shell
  1 -> 2.83 R500 with N = 102. This lane rescales that error to the KiDS geometry and N;
  the implied per-beam sigma_y is reported for comparison with the published ACT value.

**Secondary — eROSITA / eRASS1 DR1 (SRG).** Not downloaded; the 50-tile plan for GO1's own
groups is priced at 0.73 GB in `GO1/DATA_PLAN.md`, with 80-210 s of exposure per group — too
shallow for one system at 3-5 R500. For a 17,000-lens stack the limiting factor is
large-scale soft-foreground structure, not exposure; X-ray therefore grades **shape and
normalization of n_e**, while the SZ grades **column**.

**Tertiary — X-ray absorption (O VII 21.60 A / O VIII 18.97 A) and FRB dispersion measure.**
Both are linear in column like the SZ but need either a bright background source or a
well-localised FRB behind an isolated L\* halo; listed as the confirmatory path, not graded here
(no O VII survey or FRB DM catalogue for isolated L\* hosts is on disk).

**In what follows, every number is either (a) computed here from files on disk, (b) quoted from a
file in this repo with the file named, or (c) explicitly flagged `[memory]`.**

---

## 3. The statistics (frozen)

Two footings, never pooled. Both statistics are evaluated on the primary lens set P1.

### S1 — PRIMARY: the column amplitude
    f_col  ==  M_gas,meas(< R_ref) / M_gas,req(< R_ref),      R_ref = 1 Mpc
    M_gas,req(<R) = (a0/G) R^2 / x_b^2  -  M_star = pi R^2 Sigma_gas - M_star

Obtained by deprojecting the stacked, beam-corrected ACT DR6 Compton-y profile (GO1 Part A,
`onion_A`) with the frozen temperature model, and quoting the 1 Mpc enclosed value.
The 1 Mpc reference radius is chosen because it is interior to the last KiDS bin, exterior to
R200 (so the 2-halo term is measurable but not dominant), and resolved by the 1.6' beam at the
lens median redshift.

### S2 — SECONDARY: the shape index
    gamma, from a power-law fit  S_X  ~  b^(-gamma)   over 0.3 - 2.6 Mpc
(equivalently the outer logarithmic density slope `p`, with gamma = 2p - 1 and y ~ b^(1-p)).
The sheet predicts **gamma = 1.00 exactly** and a **flat y plateau**; any normally-shaped hot
halo gives p ~ 1.5-2, i.e. gamma ~ 2-3 and y falling as b^(-0.5) to b^(-1).

### S3 — TERTIARY, reported not graded
    n_e(R) and EM(b) from the eRASS1 stack, against the group-scale measurement quoted in
    GO1/DATA_PLAN.md from Bulbul+2026 (arXiv:2607.27804): n_e = (4.8 +- 1.3)e-5 cm^-3 at
    0.7-2 R500 and (5.5 +- 2.0)e-6 cm^-3 at 2-4 R500 (R500 = 0.66 Mpc).

---

## 4. The pre-registered decision rule (THE numbers, fixed now)

### Primary, per footing
| outcome | condition |
|---|---|
| **KILL** the missing-baryon reading on the galaxy leg | `f_col <= 0.10` **and** the upper 99.7 % bound on `f_col` is `<= 0.10` (i.e. >= 3 sigma) |
| **KEEP** the reading (it survives to the next test) | `f_col >= 0.50` **and** the lower 99.7 % bound on `f_col` is `>= 0.50` |
| **NO VERDICT** | anything else, or any bracket/null below fails (§5) |

**Why 0.10 (kill).** GAS1's two routes differ by footing and by up to 30x in required mass: the
law-driven route (L1) needs `pi R^2 Sigma_gas`; the footing-free data-driven route (L3) needs only
`M_3D,obs/6.41 - M_b`. Evaluated on the record's own KiDS bins, L3/L1 = **0.02 to 0.11**. So 0.10 is
precisely the level below which **even the cheapest escape route in the record fails** — the gas on
disk cannot supply the L3 requirement, let alone L1. It is footing-independent to within 25 %.

**Why 0.50 (keep).** CRUX.md's pre-registered consequence is the exact mirror image: "if GAS1 finds
that the gas on disk can supply less than half of the 11.0x, then form B's halo is not the cold
charge." Supplying at least half keeps the reading inside the record's own survival condition.

### Secondary (shape), per footing
| outcome | condition |
|---|---|
| **KILL** (independent of normalization) | `gamma >= 1.5` at >= 3 sigma, i.e. the outer column falls faster than `b^(-0.25)` and cannot sustain the required flat column to 2.6 Mpc |
| **KEEP** | `gamma <= 1.25` at >= 3 sigma AND `f_col >= 0.50` |
| **NO VERDICT** | otherwise |

A KILL on S2 is strictly stronger than a KILL on S1: it says the required column is not there
*regardless of the temperature model*.

### Label
One label per footing. If the labels differ, both are printed and the difference is named.

---

## 5. Brackets that must all pass before any outcome is reported

If **any** of the following fails, the lane reports `NO VERDICT` for that footing, whatever f_col says.

| # | bracket | requirement |
|---|---|---|
| B1 | CIB / dust | `ComptonY` and `ComptonY_deproj_cib_1.0_10.7` must give the same label |
| B2 | beam | with and without GO1's gNFW beam correction must agree within 25 % at 1 Mpc |
| B3 | environment / 2-halo | the label must be the same in z = 0.05-0.20 and z = 0.20-0.43 |
| B4 | sample purity | the label must be the same at veto F = 1.0, 1.3, 1.6 R_h |
| B5 | nulls | GO1's N1 cross-shear and N2 random-minus-random must both pass |
| B6 | mocks | GO1's 200-mock bias test (KA2b) must satisfy \|bias\| <= 0.3 sd |
| B7 | temperature model | the label must be the same for kT = 0.1, 0.2 and 0.5 keV |

---

## 6. Known answers (must PASS) and mutations (must BITE)

**Known answers — computed, not quoted:**
- KA1: `Sigma_gas` reproduces GAS1's 6.1627 (canonical) and 7.4477 (alt) Msun/pc^2 to 1e-4 relative.
- KA2: the implied `g_bar = pi G Sigma_gas` equals `a0/x_b^2` to 1e-12 relative, both footings.
- KA3: the enclosed requirement `pi R^2 Sigma_gas - M_b` reproduces GAS1's 3.234e13 / 5.716e13 /
  1.000e14 / 1.326e14 Msun (canonical) at 1.29 / 1.72 / 2.27 / 2.62 Mpc to 2e-3 relative.
- KA4: the local density equals `Sigma_gas/(2R)` (Abel-consistent with M ~ R^2) to machine precision.
- KA5: emission measure reduces to the analytic `arccosh(R_out/b)/b` form to 1e-6 relative.
- KA6: the SZ y plateau is invariant to R_out when expressed as an electron column.

**Mutations — each must change the prediction by the stated factor:**
- M1: a0 -> 10 a0 raises Sigma_gas and M_gas,req by exactly 10.000.
- M2: a normally-shaped halo (rho ~ R^-2, normalized to the same local n_e at 1 Mpc) must
  under-supply the enclosed mass at 2 and 2.6 Mpc by the computed factors and over-supply at
  0.3 Mpc.
- M3: clumping C = 3 raises the X-ray S_X by exactly 3 and leaves y unchanged.
- M4: removing the 17,335-lens stack (N = 102, group geometry) must reproduce GO1's measured
  y-gas error within a factor of 2 after rescaling.

---

## 7. What this lane may not do

- It may not change the lens set, veto radius, window, or `R_ref` after seeing any number.
- It may not download eRASS1 event files (owner's decision; `DATA_PLAN.md` is a plan, not a fetch).
- It may not pool the footings, or quote a footing-mixed Sigma.
- It may not adopt, relabel or register anything. Form B's labels stand as they are.

kappa = 1/2 FITTED; not theory closed.
