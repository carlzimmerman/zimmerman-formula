# MaNGA / IFU-side inventory — cluster-member EFE sigma-spread scout

**Lane:** IFU/MaNGA side of the feasibility scout for the cluster-member EFE
sigma-spread "nearest bite" (`prep_2026/cluster_efe_channel/SYNTHESIS.md`).
**Question:** is the diffuse-carrier × cluster-member overlap assemblable from
public MMU-MaNGA now? **This lane holds the likely binding number.**
**Status:** paper feasibility estimate from published catalog metadata — NOT a
real cross-match (no multi-GB MMU download). Arithmetic in `inventory_manga.py`
(exit 0). Honest both ways.

---

## Q1 — Does MMU-manga serve resolved stellar velocity dispersion? YES.

The MMU `scripts/manga` builder serves, per galaxy, **both**:
- DRP `LOGCUBE` datacubes (96×96 spaxel spectra), and
- the **DAP `MAPS` HYB10-MILESHC-MASTARSSP** derived-analysis maps.

The DR17 DAP MAPS file carries the stellar-kinematics extensions
**`STELLAR_SIGMA`** (raw LOS stellar velocity dispersion), `STELLAR_SIGMA_IVAR`,
`STELLAR_SIGMA_MASK`, and **`STELLAR_SIGMACORR`** (quadrature instrumental
correction; use channel 0 in DR17). So the **resolved 2-D stellar sigma map is
served**; `sigma_e` = aperture 2nd moment inside R_e with `STELLAR_SIGMACORR`
quadrature-subtracted. **Kinematics availability is a GO** — this is not the
blocker.

Caveat that matters downstream: the MaNGA instrumental LSF has 1σ ≈ **70 km/s**.
DAP dispersions are "robust down to ~20 km/s" **only at high SNR**; below the LSF
they are correction-dominated and, for faint targets, often upper limits.

## Q2 — MaNGA DR17 sample and the low-sigma (diffuse) carriers

- Total: **10,010** unique galaxies (DR17), nearly flat in log M* over
  ~10^9 – 6×10^11 M⊙, median z ≈ 0.03. Stellar-mass **floor ≈ 10^9** — the
  low-sigma dwarfs that carry the EFE signal are structurally under-represented.
- Mass structure (Sánchez-García+ 2026, arXiv:2605.19426):
  **977** dwarfs (log M* ≤ 9.5), **1,538** intermediate (9.5–10),
  **2,515** total below log M* = 10.
- Dedicated dwarf ancillary **MaNDala** (Cano-Díaz+ 2022): only **136** galaxies
  (M* < 10^9.06), and only **35 are satellites** — mostly centrals/modest
  groups, **not rich clusters**.
- Empirical sigma anchor (Penny+ 2016, MaNGA yr-1 dwarfs, M*=1–5×10^9):
  sigma_e spanned **40–127 km/s** and **5/39 (~13%) were unmeasurable** below the
  floor. So even at ~10^9 M⊙ a large fraction sit **above 70** or are
  unmeasurable; the 20–70 km/s window is essentially the ≤9.5 dwarfs plus the low
  tail of the intermediates.

**Diffuse carriers (sigma 20–70 km/s), all environments:** ~**590** kinematically
in-window → ~**330** after a reliability haircut for the LSF floor. That is the
usable low-sigma IFU population in MaNGA. It is real but modest, and it is a
**field-dominated** population.

## Q3 — SAMI supplement

SAMI cluster sample (Owers+ 2017): **906** galaxies across **8 low-z clusters**
(A85, A119, A168, A2399, A3880, A4038, APMCC0917, EDCC0442; 0.029<z<0.058)
**with membership + cluster-centric radius + peculiar velocity** — i.e.
Rhee-zone-taggable out of the box, and the clusters are rich enough for caustic
a_ext profiles. Mass floor is redshift-dependent (~log M* > 9.5 nearest).
Diffuse cluster members ≈ **160**. **SAMI is NOT in MMU** (separate download,
different pipeline/LSF ~ analogous floor).

---

## The binding overlap (diffuse × cluster-member × caustic-taggable)

| Cut | MMU-MaNGA | +SAMI |
|---|---|---|
| Diffuse, usable sigma 20–70 (all env) | ~330 | — |
| **× rich-cluster member, caustic-able** | **~40** | ~160 (SAMI) |
| **Assemblable stack** | **~40** | **~200** |

Target for a ~2–3σ firewalled exploratory run: **300–500**.

## VERDICT

- **Resolved sigma: SERVED (GO).** MMU-manga delivers the DAP `STELLAR_SIGMA`
  maps needed for `sigma_int`. This lane's kinematics requirement is met.
- **Diffuse × cluster overlap in MMU-MaNGA alone: ~tens (NO-GO).** MaNGA is
  stellar-mass-limited (M* ≳ 10^9) and **field-dominated**; the low-sigma cluster
  dwarfs that carry the signal are both rare and pushed against the 70 km/s LSF
  floor (upper limits, not values). ~40 diffuse tagged members **dies on
  statistics** for a 300–500 target.
- **MaNGA + SAMI stack: ~200 (BORDERLINE / underpowered),** and only by pulling
  SAMI, which is **not** an MMU product — so the "assemble from public MMU now"
  framing fails on this lane.

**What is actually needed:** a MaNGA+SAMI(+MAGPI/Hector) IFU stack with a
homogenized low-sigma calibration, or a dedicated **dwarf-IFU cluster survey**
(deeper than MaNGA's mass floor, sigma reliable well below 70 km/s), ultimately
**ELT-class** IFU to push diffuse cluster dwarfs to the ~20 km/s regime cleanly.
The MMU DESI/legacysurvey side can supply cluster redshifts/membership (other
lane), but it cannot supply the resolved sigma_int — only IFU can, and the IFU
that is in MMU (MaNGA) does not have the diffuse cluster-member numbers.

*Numbers are cited published catalog values; the overlap fractions are
transparent estimates in `inventory_manga.py`, not a cross-match. No physics
claim — data-availability go/no-go only.*

### Sources
- MMU manga builder README + SDSS DR17 DAP MAPS datamodel (STELLAR_SIGMA / STELLAR_SIGMACORR).
- Abdurro'uf+ 2022 (DR17, arXiv:2112.02026): 10,010 galaxies, mass range, LSF ~70 km/s.
- Sánchez-García+ 2026 (arXiv:2605.19426): 977 dwarfs ≤9.5, 1538 intermediate, 2515 <10.
- Cano-Díaz+ 2022 (AJ, 10.3847/1538-3881/ac8549): MaNDala 136 dwarfs, 35 satellites.
- Penny+ 2016 (arXiv:1609.01299): yr-1 dwarfs, sigma_e 40–127, 5/39 unmeasurable, environmental.
- Owers+ 2017 SAMI cluster sample: 906 galaxies, 8 clusters, membership+radius+velocity.
