# G2_preinfall_retention: FAILS on native inputs. It closes only through a ΛCDM-processed input (Moster SHMR + NFW), and even then it overshoots 8 satellites

**Verdict (both footings, never pooled).**
1. **FAILS on native inputs.** PAPER36's rule moves the satellites' offset from the screened prediction by about 0 at the
   primary native cell.
   - Primary (chemistry-floor collapse mass, top-hat profile, z_coll = 10): **+0.92 ± 0.14 dex** canonical (+0.89 ± 0.15
     alt), against E3's +0.88 on the same 36 systems.
   - Present-baryon collapse mass (f_ret = 1): **+0.98 ± 0.12** (+0.94 ± 0.13 alt), against +0.88.
   - The offset gets slightly worse, not better. The suggestion's own ζ criterion sends three systems to Newton: Boötes III
     and Crater II (stripped inside r12 at pericentre in the host law field) and Andromeda XVII.
2. **Why: the phantom eats the supply.** By PAPER36's own T5, the retained cold energy first pays the law's phantom inside
   the tidal edge (r_t ≈ 0.5 kpc). Only the leftover sits as collapse debris.
   - With present baryons, f_ex = 0 in the median system, so the rule reduces to the screened prediction.
   - With the chemistry floor, the debris inside r12 is about 9e2 M☉, against a need of 4.9e5 M☉.
3. **The native bracket spans −0.55 to +0.99 dex.** Only one corner closes or passes zero: the nominal-yield chemistry
   floor (L_min ≈ 190) with the most concentrated native profile (r^{3/4}). There it overshoots 15–19 systems at > 2σ.
   - So the rule predicts nothing until the collapse mass and the collapse profile are measured.
   - The record has no native value for either (E6 D1: the catchment is set by the initial patch and infall).
4. **RESTS ON A NON-NATIVE INPUT.** PAPER36's own route is Moster+13 SHMR, extrapolated to M* ≈ 1e3–1e6, plus
   Dutton–Macciò NFW.
   - That route closes the median: −0.07 ± 0.10 canonical, −0.08 ± 0.10 alt.
   - It overshoots **8** systems at > 2σ, against the frozen breakage line of 5.
   - That route is the ΛCDM subhalo mass, put in by hand.
5. **Breakage.**
   - **TDGs pass.** ζ = 0 follows from how they formed. Data: +0.08 ± 0.10 dex vs Newton.
   - **DF2/DF4 are NOT given ζ = 0 by the criterion.** With baryons plus the law, the tidal radius at the projected
     distance is 11 / 22 kpc, while r12 is 2.7 / 2.1 kpc. Being stripped would need a pericentre ≤ 24 / 21 kpc (17–34 kpc
     for a host mass ×0.5–3). Stellar ages are 8.3 / 10.7 Gyr. Under ζ = 1 the rule gives σ ≈ 20 / 19 km/s, against
     8.5 / 6.3 observed (+5σ). So ζ = 0 for DF2/DF4 stays a label, as in CFG936.
   - **UFDs pass.** No overshoot in the primary cells. The compact UFDs (Segue 1, Willman 1, Carina III) are unchanged at
     +2.1 to +2.5 dex.
   - **Isolated field dwarfs pass** (ζ = 1, reported): −0.00 ± 0.09 (f_ret 1) and −0.06 ± 0.09 (census).

κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s², never pooled. Cold energy, no particle. Not "theory closed". Nothing
here says the data favour the framework.

## Commits and files
- `FROZEN_CRITERIA.md` + `ASSUMPTION_LEDGER.md`: 92716d0148, committed alone first.
- A1 (pre-result, K2 tolerance): b3fbb9ed9d. A2 (post-hoc disclosures): in the result commit.
- Script `g2_preinfall_retention.py` → `.out`, `_results.json`, `g2_per_system.csv` (primary cells, per system).
- `--mutate` (M_coll → 0) → `*_MUTATE.*`.
- Runtime: one thread, nice 15, about 30 s, 185 MB RSS. Nothing downloaded. E3/E6/CFG936 were read only.

## 1. The rule, from PAPER36's own equation
PAPER36 eq. 1 (CFG35): M_dark(<r) = M_ph(<r) + f_ex (1 − f_b) M_NFW(<r; M_coll), with
f_ex = max(0, 1 − M_ph,edge / [(1 − f_b) M_coll]).

For a satellite (ζ = 1), take the edge to be the tidal radius:
- **retained cold** inside r_t = (1 − f_b) M_coll m(r_t; z_coll);
- the debris inside r12 = f_ex (1 − f_b) M_coll m(r12; z_coll), added to E3's screened (M*/2) B_scr.

M_coll is a **history input**. PAPER36 itself says it "must be measured" and takes it from weak lensing or the Moster SHMR.
The profile is NFW with ΛCDM concentrations. As a function of baryon mass, M_coll = M_b / (f_b f_ret). f_ret has no native
value. z_coll enters through r_vir ∝ M^{1/3}/(1 + z_coll).

## 2. Premises, checked plainly
- **"Conserved, so kept" is total-mass conservation, not enclosed-mass conservation.** PAPER36 does not invoke Liouville
  or ∇T = 0. Its argument is that feedback pushes gas, not a pressureless fluid.
  - Under tides, mass beyond r_t is lost.
  - Pericentre shocks heat the inner orbits.
  - Phase mixing can only lower the coarse-grained density.
  - So ζ = 1 is an **upper bound** on retention. A shortfall at ζ = 1, as here, is a hard failure. A closure at ζ = 1 would
    only have been an upper bound.
- **The framework's own settling does not produce PAPER36's debris.**
  - CFG939: the S2 + S3 medium stays tethered through shell crossing. A free leftover population that the law does not use
    is not a regime of the medium (NOT DERIVABLE).
  - CFG888: in the S3 action, extra cold energy has no self-gravity, and the tether pushes it outward.
  - CFG889: with orbits, the gate does not retain a clump.
  - In covariant v3, clustering BS dust double-counts against the law (CFG946; THEORY_V3_DRAFT line 44).
  - So the debris term is a **POSITED RULE** in every formulation on record.
- **ΛCDM inputs in PAPER36.** All of these are ΛCDM-PROCESSED:
  - Ω_c h² = 0.12 "fitted as in ΛCDM";
  - "inherits ΛCDM's collapse statistics";
  - Moster+13 abundance matching;
  - Mandelbaum+16 halo-model masses;
  - Dutton–Macciò NFW;
  - f_b.
  - It was calibrated on log M* 10.3–11.5 and never tested below about 10.

## 3. Numbers (median log10 M_dyn/M_pred; from `g2_preinfall_retention_results.json` → `cells`)

| cell | canonical | alt | overshoot > 2σ (can.) | class |
|---|---|---|---|---|
| E3 screened (reproduced) | +0.883 ± 0.125 | +0.846 ± 0.130 | — | baseline |
| FREE (f_ret 1), TH, z 10 | +0.979 ± 0.123 | +0.941 ± 0.130 | 0 | native |
| CHEM-cons, TH, z 10 (primary) | +0.921 ± 0.137 | +0.889 ± 0.145 | 0 | native, conditional |
| CHEM-cons, B85, z 10 | +0.406 ± 0.134 | +0.388 ± 0.131 | 1 | native, conditional |
| CHEM-nom, TH, z 15 | +0.681 ± 0.129 | +0.668 ± 0.134 | 0 | native, conditional |
| CHEM-nom, B85, z 6 / 10 / 15 | −0.28 / −0.43 / −0.55 | −0.25 / −0.42 / −0.53 | 15 / 18 / 19 | native, conditional |
| CENSUS (f_ret 0.10), any profile | +0.89 … +1.00 | +0.87 … +0.98 | ≤ 1 | ΛCDM-processed |
| SHMR (Moster), NFW (PAPER36's own) | **−0.07 ± 0.10** | **−0.08 ± 0.10** | **8** | ΛCDM-processed |
| SHMR, B85 | −1.59 … −1.87 | −1.56 … −1.87 | 34–35 | ΛCDM-processed |

**Infall epochs.**
- Source: the 45 MW satellites with LVD proper motions, integrated in the host law field (MW baryons 6e10, no EFE).
- Median z_inf = 3.0 with R_ta0 = 0.83 Mpc and 4.0 with 1.10 Mpc. Willman 1 (9.7) and Segue 1 (6.5) are the earliest.
- M31 satellites are bracketed (apocentre d to 2d, pericentre 0.3d).
- The infall bracket moves the primary offset by ≤ 0.03 dex. Infall sets only ζ, and ζ = 1 for 40–42 of 45.

## 4. Checks: 4/6 PASS (exit 1)
- K1 PASS: E3 reproduced from raw LVD, N 45/46, +0.883/+0.846.
- K3 PASS: rule limits (M_coll → 0 gives the screened prediction; ζ = 0 gives Newton).
- K4 PASS: orbit roots to 2e-15. The Galactocentric distance matches LVD.
- K6 PASS.
- **K2 FAIL** (max 18 %, Andromeda XXII) and **K5 FAIL** (3.8 % median). Both come from independent MC versus E3's; this
  is disclosed in A2 and was not re-tuned.
- **MUTATE did not break K6 as frozen.** The ζ = 0 assignment alone moves O by +0.11. The mutate run does return the
  no-debris answer.

## What this does not show
- No per-system collapse mass or collapse profile. The native bracket is wide, and only measured values could decide it.
- The pericentres use a point-mass MW. The M31 orbits are brackets.
- DF2/DF4 3D distances and orbits are unknown, so the projected-distance r_t is a lower bound only at the present epoch.
- The isolated field dwarfs (B4) use stars only in g_bar (CFG873: gas-sensitive).
- **Most valuable next step:** none for this rule. Its only working input is ΛCDM's subhalo mass. A native rule for the
  satellites needs a derived binding mechanism (E3/E6), not a retention fraction.
