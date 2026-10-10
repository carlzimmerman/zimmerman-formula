# CFG536 FROZEN CRITERIA: CFG534's post-hoc overlap-weighted early - late estimator, frozen unchanged and applied to a DISJOINT held-out sample (stack P minus f30) in the validated stack-P environment

Written 2026-10-09, before any CFG536 script exists and before any held-out shear-based number (Delta d, Delta eps, per-class eps, or
jackknife scatter) has been computed. Committed alone. This file is never edited; departures go in the README, dated.

Standing settings: a0 = kappa c sqrt(G rho_DE), kappa = 1/2 FITTED. Footings 9.3603e-11 (canonical) and 1.1312e-10 (alt), scored
separately and NEVER pooled. Kernel nu_mono = 1/(1 - exp(-sqrt y)). The cold energy's mass is still required (no particle species).
Not "theory closed"; nothing here says the data favour the framework. On-disk data only, nothing downloaded. nice -n 10, <= 4 threads.
No knob is fitted.

## 0. Why
CFG534 (criteria aa8dc312e, results 086f14f74) tested H: at fixed stellar mass, early-type (quenched) lenses carry extra settled cold
energy beyond the law's minimum, Delta eps(early - late) > 0. Its frozen matched estimator gave +0.529 +- 0.324 / +0.485 +- 0.296 (Z 1.6)
on the f30 lenses. AFTER seeing that, a lower-variance "overlap" weighting was added (no verdict weight): +0.777 +- 0.245 / +0.712 +- 0.224
(Z +3.18). Because the weighting was chosen after the f30 data were seen, re-running it on f30 confirms nothing. This lane freezes that
estimator exactly and applies it, unchanged, to lenses that played no part in choosing it.

## 1. Samples
- **Held-out sample HO = stack P AND NOT f30** (`cfg96_isoflags.npz` mask `f30`; stack P = the 181,477 lenses of `lr_lenses.npz`).
  Structural facts checked before writing (lens counts and lensing weights only; no shear read): 124,212 lenses (61,507 early typ 1 /
  62,705 late typ 0); 901 CFG503 (M_gal, z) groups hold both classes (60,534 early / 42,951 late lenses in them); the within-group
  log M* range has median 0.011 dex (90th percentile 0.016), so a group is still a fixed (M*, z) cell. f30 = iso30 of the CFG502 stage
  (exact), so HO and f30 are disjoint and HO + f30 = stack P (control C4).
- **Control sample f30** (57,265 lenses) only for the reproduction controls C1/C2, labelled NOT CONFIRMATORY.
- **Disclosure (before any number):** HO is disjoint from the choice of estimator, but it is NOT blind to the record. The unmatched
  stack-P early/late lensing split (which includes HO lenses) is already known: CFG505 4.40-4.52 sigma on K1, CFG509 3.88 sigma after
  class leakage. What has never been computed is the mass-matched (inside group x bin cells) Delta eps on HO with either CFG534 estimator.

## 2. Environment (validated stack-P environment, CFG529 G1m)
Window W10, measured stack-P leaked-satellite fraction 0.2234 (CFG519 `main.f_IC`), CFG520 part-B scaling (CFG529's `MEAS["P"]`),
constructions **A** (CFG503 sharp boundary) and **B** (CFG504 smooth DK14 transition, primary x_t), exactly as CFG529 validated it
(G1m: A 26.13, p 0.037; B 14.08, p 0.52). Per group: E = CFG529 `evec(GP, c, s, "W10", MEAS["P"][s], ...)`, own (LAW_RTA) =
CFG529 `own_rec(c, "P", foot, "LAW_RTA", s, "W10", MEAS["P"][s])`, both SHMRs (Moster primary, Behroozi).

## 3. The estimator (frozen = CFG534's code path, not re-implemented)
The script exec's `CFG534_history_dependent_settling/cfg534_kids.py` read-only up to (not including) its `SPL = {` line. That defines
CFG534's `wsum`, `match`, `esd_w`, `mstack`, `cp_w`, `gls`, `compare` exactly as committed (and, through CFG531 / CFG529, the data,
groups, patches, Hartlap factor, bands and `fit_eps`). For HO the per-group tables `GT[(c, foot, s)]` in that namespace are replaced by
the stack-P environment tables of section 2; nothing else changes.
- **Primary (verdict) estimator: `compare(HO & early, HO & late, mode="overlap")`**: in each (group, radial bin) cell both classes are
  scaled to W_A W_B / (W_A + W_B); cells lacking either class are dropped; Delta d = d_early - d_late; Delta eps per band = GLS amplitude
  of the matched own stack o on Delta d with the 50-patch jackknife covariance of the LOO Delta d vectors and the Hartlap factor.
- **Statistic:** band K9 (bins 6-14). Z_ver = the SMALLER of the Moster-template and Behroozi-template Z (CFG534's `Zmin`).
  sigma = the Moster-template sigma.
- **Reported (no verdict weight):** CFG534's FROZEN reweighting `compare(..., mode="A")` on HO (class B scaled to class A's cell
  weight); per-band values (K-in, K-mid, K-out); per-class eps.

## 4. Power forecast (stated before scoring; weights and model tables only, no shear)
Shape-noise Fisher scaling of the K9 own-template information, Sum_k o_k^2 / var_k with the matched cell weights (CFG503 LAW_RTA full
Moster tables), gives sigma_HO / sigma_f30 = 0.690 (overlap) and 0.679 (frozen), both footings. Scaled from the f30 values:
- **overlap: expected sigma_HO ~ 0.169 (canonical) / 0.155 (alt);** frozen: ~ 0.220 / 0.201.
- Caveat: the same shape-noise model predicts frozen/overlap = 1.70 on f30, while the jackknife gave 1.32, so the jackknife sigma is not
  purely shape-noise; HO lenses are less isolated (more companion / large-scale-structure noise). Declared range for the overlap
  sigma_HO: 0.17-0.24 (canonical). If H's effect were the f30 overlap value (+0.78), the expected Z_HO is ~3.2-4.6; if it were the f30
  frozen value (+0.53), ~2.2-3.1. Not diagnostic (sigma > 0.30) is not expected.

## 5. Verdict (per footing; applied in this order)
1. **NOT DIAGNOSTIC** if sigma(Delta eps K9, overlap, HO) > 0.30 in either construction, or if MU1 (section 7) fails.
2. **CONFIRMED** if Delta eps(K9) > 0 with Z_ver >= 3 in BOTH constructions AND MU1 passes (shuffles kill it).
3. **CONSISTENT** if 2 <= Z_ver < 3 in both constructions (same sign, > 0), or Z_ver >= 3 in one and >= 2 in the other.
4. **NOT CONFIRMED** otherwise (Z_ver < 2 in either construction, or Delta eps <= 0).
Headline: if the footings differ, FOOTING-DEPENDENT with both labels. **Label "LEAKAGE-LIMITED"** is attached to the verdict of a
footing if the leakage bias estimate L2 (section 6) is >= 0.5 x Delta eps_HO (Moster, K9) in either construction.

## 6. Companion / leakage mix (reported; the L2 qualifier above is the only verdict effect)
Within a matched cell the environment term E is colour-blind and cancels exactly in Delta d. So any class difference in leaked
satellites goes straight into Delta eps, with a positive sign if early types are more often leaked satellites (CFG509: early types have
1.53x the excess companions at matched M*, z; f_leak 0.168 vs 0.113 on stack P). HO is less isolated than f30 (stack P 0.2234 vs f30
0.1686 overall), so the bias may be larger on HO than on f30.
- **L1 (measured, per class):** CFG519's satellite flag S_IC from `_external_data/cfg519_work/cfg519_state.npz` (matched, in-overlap
  lenses), reweighted with CFG519's 48 (log M*, z, typ) cells (direct cells with >= 20 matched lenses only; the weight share defined is
  reported) to the lensing weight wl = Sum_k WW of each target: f30-early, f30-late, HO-early, HO-late, f30, HO. 12-region jackknife
  (CFG519 regions). Delta f = f_early - f_late per sample. Control C6: f30 overall (both classes, CFG519's cell scheme incl. fallback)
  reproduces CFG519's `main.f30` 0.16863 to 1e-6.
- **L2 (bias estimate):** Delta eps_leak = Delta f_HO x [GLS amplitude on o (K9, the HO overlap covariance) of D], where D is the
  matched (overlap-weighted) stack of the per-group derivative of the model with respect to the leaked fraction:
  [E(f = 1) - E(f = 0)] + [own(f = 1) - own(f = 0)] in the W10 environment, per construction and footing (Moster). Same for f30 with
  the W30 environment and Delta f_f30 (reported). Reported (no weight): the leakage-adjusted Z = (Delta eps_HO - Delta eps_leak)/sigma.
- The CFG509 class-leakage values are quoted beside L1 as an independent (counts-based, halo-model-converted) cross-check.

## 7. MUTATE (CFG536_MUTATE=1 -> *_MUTATE.*)
- **MU1 (the kill):** early/late labels permuted inside each CFG503 group within HO, 50 seeded shuffles (seeds 5360-5409); overlap
  estimator. PASS iff |mean Z(K9, Moster)| < 1 in all four cells (A/B x footing). The shuffle SD of Z and the seed-5360 value are reported.
- **MU2 (method):** mock d_early = d_late,matched + 0.3 o on HO (CFG534's MU2 path, overlap mode): Delta eps = 0.300 in every band to 1e-6.

## 8. Controls (load-bearing; exit 1 if any fails)
- **C1 (NOT CONFIRMATORY):** the overlap estimator on f30 (f30 environment, CFG534's own GT) reproduces CFG534's committed
  `postfreeze_overlap.1a_type` K9 eps, sigma and Z (Moster) and Zmin in all four cells to 1e-6.
- **C2:** the frozen mode on f30 reproduces CFG534's `compare.1a_type` K9 the same way (1e-6).
- **C3:** on HO the matched classes share identical stacked model vectors (1e-10 relative; both modes, all bands, both SHMRs).
- **C4:** HO and f30 are disjoint and their union is stack P.
- **C5:** the stack-P environment as built reproduces CFG529's G1m LCDM chi2 (A and B) from its committed JSON within 0.01.
- **C6:** see section 6.

## Disclosures policy
Numbers in the README come from the results JSON. Any change after the first run is dated and disclosed. kappa = 1/2 is fitted; the cold
energy's mass is still required; not "theory closed".
