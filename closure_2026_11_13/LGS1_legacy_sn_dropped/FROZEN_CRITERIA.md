# LGS1 — re-read the Dovekie supernova lanes with the legacy low-redshift supernovae dropped (FROZEN, before any number)

2026-11-13. Owner: "Yes, re-run". A re-read of committed lanes. It adopts nothing and edits no ledger.

## Why
Nájera, Banik and Desmond (arXiv:2610.23657) report that the 197 legacy low-redshift supernovae in the DES-SN5YR Dovekie
Hubble diagram (z 0.025–0.087, IDSURVEY other than 10) sit about +0.065 mag off the DES sample extrapolated to low
redshift, and that including them moves their H0 from 76.25 ± 2.87 to 67.98 ± 0.69 km/s/Mpc. The lanes here that read
the Dovekie file (CFG684, CFG689, X54, RF5) keep every supernova with z > 0, legacy included.
Nothing in this lane depends on that paper's numbers. It asks one question of our own lanes:
**do their results change when the legacy supernovae are dropped?**

## Data and samples
The Dovekie Hubble diagram and STAT+SYS inverse covariance already on disk (`_external_data/cfg684_inputs/des5/`, as CFG684).
File counts checked before any fit: 1,820 supernovae; 1,623 with IDSURVEY 10 (DES, z 0.0733–1.1442); 197 legacy.
- `full`: all 1,820. The committed lanes' own selection. Harness check only.
- `des_only`: IDSURVEY 10 only (1,623). **The primary sample.**
- `rand197`: legacy kept, 197 randomly chosen DES supernovae dropped (numpy default_rng, seed 20261113). Size control,
  CFG684 only.
A dropped supernova is removed from the covariance (invert the inverse covariance, take the sub-block, invert), as the
lanes' loaders already do. No cut on MUERR (the lanes apply none). The absolute magnitude stays profiled.

## Method
`lgs1_run.py` executes each lane's committed source with three exact text substitutions: the selection mask, the output
paths (into this folder) and, for CFG684, the list of combinations (the two that contain DES5). Nothing else changes:
same BAO, chronometers, grids, seeds and step counts. `lgs1_collect.py` applies the rules below. Both are committed with
this file, before any `des_only` number exists.

## Part A — CFG684 (BAO+DES5 and BAO+DES5+CC; no CMB)
- **Harness check:** `full` must reproduce the committed `cfg684_results.json` (Δχ²_max, flat-a0 Ω_m mean and sd, tracking
  and rival bands at z* 1.0, 1.5, 2.33) to 1e-6 in both combinations. If not: Part A is NOT EVALUABLE.
- **A1 (CFG684's own rule):** DEGENERACY BROKEN if Δχ²_max over Ω_m 0.24–0.36 is ≥ 4; else NOT BROKEN.
- **A2 (CFG684's own rule, applied to the legacy cut):** ROBUST if the flat-a0 Ω_m of `des_only` agrees with `full` within
  1σ combined (sd added in quadrature); else LEGACY-DEPENDENT. The two samples are nested, so the combined sd is generous;
  the nested-sample sd, sqrt|sd²(des_only) − sd²(full)|, is printed as context and carries no label.
- **A3 (CFG684's README statement that DES5 lifts the tracking floor):** FLOOR HOLDS if the lower edge of the tracking
  band √X(2.33) of `des_only` is above 0; else FLOOR LOST. The values at z* 1.5 and 2.33 are reported.
- **Control:** the same three labels for `rand197`. If `des_only` changes a label and `rand197` does not, the change comes
  from the legacy set and not from the loss of 197 objects.

## Part B — CFG689 modes D5 (curvature free) and TD5F (flat, with the acoustic angle), frozen 60,000 steps, same seeds
- **Harness check:** `full` must reproduce the committed tracking √X quantiles at z* 1.0, 1.2, 1.5, 2.33 to 0.005.
  If a `full` run is not made (run time), `des_only` is compared with the committed file directly and the result says so.
- **B1 per z*:** STABLE if the `des_only` median of tracking √X lies inside the committed 68% band and the committed median
  lies inside the `des_only` 68% band; else SHIFTED.
- **B2:** CLASS UNCHANGED if the script's own P1 class and P0 class are the same as committed; else CLASS CHANGED.
- The script's own chain check (K4) must be ok, or the mode is NOT EVALUABLE. P2 (Δχ² of free nodes against constant w)
  and e_3σ are reported, no label.
- A mode that exits on its busy-machine guard (exit 75) is NOT RUN and reruns later.

## Not in this lane
X54 and RF5 are not re-run, and stay open. X54 needs its patched Boltzmann build (no longer in the temporary folder it
was built in) and a CMB profile, and it belongs to the cold sector retired on 2026-11-01. RF5 runs patched Boltzmann
builds against the CMB for about 2.5 h of wall time. X54 took its tracking band from CFG689 TD5F (0.68–1.04 at z 2.33),
so Part B's TD5F row says whether that input would move. A w0–wa fit is not made here.

## What the result may and may not say
A re-read. ROBUST / STABLE means the committed numbers do not lean on the legacy supernovae. LEGACY-DEPENDENT / SHIFTED
means they do, and the affected lanes then carry that as a stated dependence; it does not by itself say which sample is
right. Nothing here measures H0 or a0, and nothing here grades the framework.

kappa = 1/2 FITTED; not theory closed.
