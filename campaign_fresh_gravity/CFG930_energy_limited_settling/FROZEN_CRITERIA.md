# CFG930 FROZEN CRITERIA: energy-limited settling of primordial cold energy (H-ELS)

- **Block:** CFG930–939 (LEDGER row "CFG930–939 RESERVED", orchestrator chat 2026-10-20). This lane uses CFG930 only.
- **Kind:** HYPOTHESIS TEST with ONE new constant (ε, the feedback coupling) and one new rule (energy-limited settling).
- **Status of this file:** committed ALONE, before any script exists and before any number of this lane is computed.
- **Standing rules:** κ = ½ is FITTED. The footings 9.3603e-11 and 1.1312e-10 m/s² are scored separately and never pooled. The
  extra mass is cold energy, not a dark-matter particle. Verdicts use raw data and framework-native inputs only: no Moster,
  Behroozi, Duffy, HMcode, BAHAMAS, ΛCDM mass function or abundance matching in any verdict. ΛCDM-derived inputs appear only
  in the K tests and the labelled MUTATE-K control. No result here means "theory closed", and nothing here says the data
  favour the framework.

## 1. Record check (done before writing this file)

Targeted greps of LEDGER.md (rows CFG35, CFG42, CFG45, CFG53, CFG59, CFG62, CFG65, CFG71, CFG75, CFG104, CFG112, CFG211,
CFG782, CFG784, CFG804, CFG806, CFG823, CFG834, CFG837, CFG853, CFG874, CFG880, CFG913, CFG915, CFG918, CFG921, CFG922,
CFG925, CFG926; strings "photo-evap", "debris").

- No energy-limited selector on the collapse debris has been tested. The nearest prior tests are listed below; none is
  identical, so the lane proceeds.
  - **CFG59 / CFG62 / CFG75 / CFG104 / CFG112 / CFG211:** one universal debris fraction φ; one-variable two-group splits
    (log M*, edge-to-collapse ratio, support, satellite/central). CFG62 found "0 of 20 splits"; three contiguous mass groups
    with non-monotonic φ (ultra-faints 0.39–0.84, Boötes I + classical dSphs 0.14–0.30, SLUGGS + S0s 0.81–0.96).
    These are steps or constants, not an energy budget.
  - **CFG782:** photo-evaporation unbinding selector: DEAD.
  - **CFG784:** fossil free cold: NOT RUN.
  - **CFG806:** SN energy vs the law's potential, used for GAS retention (f_ret): NOT DERIVED.
  - **CFG834 / CFG837:** constraints on the free (untethered) component and the shell-unbinding threshold, not on settling
    of the collapse debris.
- CFG42's own inputs (Moster+13 collapse masses, Dutton–Macciò concentrations) are ΛCDM machinery. They are used here only
  to reproduce CFG42 (K1) and in the labelled MUTATE-K control.

## 2. Disclosure: this hypothesis is NOT blind

H-ELS was formed by the owner and orchestrator AFTER CFG42–CFG926 had been seen. The grading therefore uses out-of-calibration
classes and sealed predictions. These are the record statements it was built from, quoted from LEDGER.md and the lane READMEs:

| lane | statement |
|---|---|
| CFG42 | "the debris must switch off where the phantom supplies the mass — a design constraint, not a fix"; the ultra-faints went +0.325 / +0.304 → −0.059 ± 0.143; classicals over-predicted (MW −0.118 / −0.123; M31 LVD −0.107 (−2.67σ)) |
| CFG45 / CFG65 | "a cusp closes the ultra-faints and over-predicts the classical dwarfs, a core removes both" |
| CFG880 | "bright dwarfs want no clump, tiniest UFDs a large one (shape may matter)" |
| CFG828 | across 29 dwarfs Δ anticorrelates with g_bar (ρ = −0.47, p = 0.011; exploratory) |
| CFG921 | within the dwarfs the excess falls with size at fixed g_bar: d = −1.36 ± 0.18 per dex of r12 |
| CFG827 | "the excess is nearly uniform … with no age dependence" (mean E +0.38) |
| CFG918 | a bound envelope cannot absorb the energy a forming core must shed (Sextans B0, Draco and Sextans in G1) |
| CFG922 | the cluster-core excess against the baryon census: "EXCESS STANDS" |
| CFG925 R3 | the framework EFE WORSENS the satellites (no external-field effect is seen) |
| CFG926 R5 | the red-lens excess is plausibly IMF |
| CFG913 | no LOCAL mobility law is feasible in the declared classes |
| CFG823 | faint dSphs need ~50–110% of their WHOLE catchment cold supply (53.6 M_b) inside r1/2 (BUDGET TIGHT at Υ 2) |
| CFG804 | supply N = 1/f_ret(M_ta) from the record's census (f_ret 0.10 at galaxy masses); "the law holds out to where it is used up" |

**Seen in this session before freezing:**
- CFG827's per-dwarf table (Υ_SFH and E_SFH for all 36 Weisz+14 dwarfs, MW classical E values included);
- CFG42's committed numbers;
- the README summaries of CFG823, CFG828, CFG853, CFG874, CFG921 and CFG922;
- CFG922's needed-mass JSON entries;
- the CFG654 native table headers (k range 1e-4–110 h/Mpc; Δ_ta(z) = 5.59 at z = 49 to 11.90 at z = 0).

**Pre-freeze expectations (back-of-envelope, no script, written here so they cannot be claimed as discoveries):**
- **E1.** With the census supply (5.364/f_ret = 53.6 M_b for every dwarf), the law's phantom inside CFG35's edge exceeds the
  whole supply in every dwarf. CFG35's leftover fraction f_ex is then expected to be zero: no debris in the
  framework-consistent reading.
- **E2.** At a fixed cold/baryon ratio, E_avail/ΔE ~ M_formed/(M_c V²) ∝ 1/V². The faintest systems would then be the EASIEST
  to settle, the opposite of H-ELS item 3.
- **E3.** The NFW r⁻¹ cusp is shallower than the deep-MOND phantom's r⁻². The native primordial profile may carry less cold
  mass than the phantom at r_1/2, so there may be no central surplus under the identity reading.

The tests below were designed to check E1–E3, including in the readings most favourable to H-ELS.

## 3. The hypothesis in testable form

H-ELS: before any bound system exists, cold energy is ordinary cold collisionless matter with Ω_c/Ω_b = 5.364 (CFG649/CFG654).
Every system starts with a primordial cold halo (the collapse debris). The law is the settled state. Settling proceeds only
as far as the system's baryonic feedback energy pays for unbinding the central surplus. The unpaid remainder stays as real,
bound, collisionless mass, and that remainder is the excess family.

### 3.1 Model (the CFG35/CFG42 sum form with an energy-limited settled fraction f_s)

    g_HELS(r) = g_law(r) + (1 − f_s) · G · M_deb(<r) / r²
    M_deb(<r) = f_ex · (1 − f_b) · M_NFW(<r)

- g_law: the law of the class's baryons (the reused estimator's kernel; §4).
- f_s = 0 is CFG42's rule; f_s = 1 is the bare law.
- **Form A (primary):** the debris amplitude is scaled by (1 − f_s) at every radius.
- **Form B (variant):** an inside-out core. The debris inside r_c is removed, with r_c defined by ΔE(<r_c) = E_avail, so the
  core grows with f_s.

### 3.2 Input sets

**K (CFG42's own; K tests and MUTATE-K only):**
- M_NFW: h48's Dutton–Macciò 200c NFW at Moster+13 halo_mass(Υ_V L_V), clamped at 1e9.
- f_b = CFG35's FB = 0.02237/(0.02237 + 0.1200).
- f_ex = max(0, 1 − M_ph(<r_e)/[(1 − f_b) M_coll]) with CFG35's edge_phantom (x_e = 0.40, ν_mono, CFG7 r_ta_law).

**NATIVE (the verdict):**
- **Catchment:** M_ta solves M_ta = M_b/(f_ret(M_ta) f_b), with f_ret the record's census (CFG416/CFG804 fret_of, verbatim:
  0.10 below log M_ta 12.5, linear to 0.55 at 13.5, +0.30/dex up to 0.90) and f_b = 1/(1 + 5.364). The cold mass is
  M_c = (1 − f_b) M_ta = 5.364 M_b/f_ret.
- **Profile:** NFW with ρ_s = C · ρ̄_m(z_coll). This is the "inner density ∝ the mean density at collapse" rule of
  collisionless collapse (Navarro, Frenk & White 1997). It is declared as generic gravitational physics, with C a declared
  constant: C = 3000 (NFW97, f = 0.01), bracket {1500, 6000}.
  - z_coll comes from NFW97's extended-Press–Schechter half-mass condition:
    erfc{ δ_c (1/D(z_coll) − 1) / sqrt(2[σ²(fM) − σ²(M)]) } = ½, with f = 0.01 and δ_c = 1.686.
  - σ(M) is the native linear σ at z = 0 from CFG654's cfg654_scorer_tables_cmb.npz (Plin_z0, kh, h, Om), top-hat window,
    M = (4π/3) ρ̄_m0 R³.
  - Beyond k = 110 h/Mpc, P(k) is extended with the cold-matter asymptote P ∝ k^(n_s − 4) [ln(1 + 2.34 k/Γ)]², with Γ = Ω_m h
    and n_s = 0.9649 (CFG654 ics table). It is matched to the table at k_max and integrated to 1e5 h/Mpc. The extension is
    declared; it carries the σ of the smallest catchments.
  - D(z) is the native growth from the same table (lnD vs lna), normalised to 1 at z = 0. ρ̄_m0 = Om · 3H0²/(8πG) with the
    table's h.
- **Boundary:** M_NFW(<r_b) = M_ta, where r_b is:
  - **primary:** the native turnaround radius r_ta = [3 M_ta/(4π Δ_ta(0) ρ̄_m0)]^(1/3), with Δ_ta(0) from
    cfg654_delta_ta_cmb.json;
  - **bracket:** r_vir, with mean enclosed density Δ_vir ρ̄_m0. Here Δ_vir = 8 Δ_ta(z_ta)(1 + z_ta)³ and t(z_ta) = t0/2, in
    the native background (Om, Or, OL of the scorer table; spherical collapse with r_vir = r_ta/2 at t_c = 2 t_ta).
- **Edge for f_ex:** r_e = 0.40 r_ta,law, with r_ta,law the radius where the law's untruncated mean enclosed density (point
  mass M_b, class kernel) equals Δ_ta(0) ρ̄_m0 (native background).

### 3.3 Readings (how the primordial cold mass meets the law)

- **N-A (primary, framework-consistent):** f_ex as in CFG35, with the native M_c and edge. The phantom consumes cold energy
  up to the edge, and only a leftover can be debris (E1 expects f_ex = 0).
- **N-B (favourable bracket):** f_ex = 1. The whole primordial cold mass is kept as debris on top of the law. This
  double-counts the cold energy the settled phantom is made of (ρ_c = ρ_ph). It is declared only as the most generous end.
- **R1 (identity variant):**
  M_dark(<r) = min(M_ph(<r), f_s M_c) + (1 − f_s) M_c,NFW(<r), and g = g_N,bar + G M_dark(<r)/r².
  - Settled cold fills the phantom from the inside out. Unsettled cold keeps the primordial profile.
  - This REPLACES the law term.
  - Its energy is ΔU = U_settled − U_prim = ∫ g_law(r) [M_c,NFW(<r) − min(M_ph(<r), M_c)] dr, in the law's potential, out
    to max(r_b, r_sup), where r_sup is the supply edge M_ph(<r_sup) = M_c.

### 3.4 Energy

- **E_avail** = ε · e_SN · M_formed, with e_SN = 1e49 erg per M☉ formed (declared).
- **M_formed:**
  - **The 36 Weisz+14 dwarfs of CFG827:** M_formed = L_V / Σ_i Δm_i ℓ(t_i), with ℓ = M(*+remn)/(M/L_V), using CFG827's SSP
    reader and SFH bins exec'd read-only. [M/H] = −1.31 is primary; −1.71 and −0.71 are reported.
  - **Every other dwarf:** a 13.3-Gyr single burst at [M/H] −1.31 (primary). The variant uses the median M_formed/L_V of
    CFG827's 36.
  - **Names** are matched case- and space-insensitively, with CFG827's NAMEMAP and "And"/"Andromeda" aliases. Unmatched
    objects use the burst rule; the match list is printed.
  - **SPARC:** M_formed = M*/m_rem, with m_rem = M(*+remn) of a constant SFR over 0–13.3 Gyr at [M/H] 0.00 (same table and
    integrator).
  - **Clusters:** the median BCG stellar mass from CFG922's A1 census (bcg_med; bracket bcg_sup), divided by the 13.3-Gyr
    m_rem at [M/H] 0.00, PLUS an AGN term in {0, 3e62 erg}. 3e62 erg is a declared upper end: the largest cavity outbursts
    are ~1e62 erg, and ~1% of the rest-mass energy of a 1e10 M☉ black hole is 2e62 erg.
- **ΔE (sum form)** is the energy to lift the debris inside r_e out to r_e in the law's potential:
  ΔE = ∫_0^{r_e} [Φ(r_e) − Φ(r)] dM_deb = ∫_0^{r_e} g_law(r) M_deb(<r) dr, with η = 1 (circular orbits in a flat-curve
  potential change only Φ). Debris beyond r_e is not counted.
  - Variant: Φ includes the debris' own gravity.
- **Baryon profile in Φ:** a Plummer sphere with 3D half-mass radius
  - (4/3) R_h for dwarfs (the estimator's aperture, where half the baryons are enclosed);
  - 1.68 R_disk for SPARC;
  - R500 for the median cluster.
- **f_s** = clip(E_avail/ΔE, 0, 1). If ΔE ≤ 0 (possible only in R1), f_s = 1: settling is downhill and not energy-limited.

## 4. Classes, estimators and statistics (reused read-only; per footing)

Main runs use the exact footings 9.3603e-11 / 1.1312e-10. The K tests use each source lane's own constants (CFG42 uses
hunt_lib's 9.36e-11 / 1.13e-10).

**Kernel:** the exponential ν_e of every reused dwarf/SPARC estimator, which agrees with ν_mono to 3e-9 for y ≤ 0.1 (CFG64).
Variant: ν_simple, which is g_N = g²/(g + a0) as stated for the law.

**Uniform error recipe:** the source lane's statistical error ⊕ a Υ floor. The floor is half the shift of the class statistic
between Υ × ½ and Υ × 2 (CFG42's Υ_V 1–4 around 2; SPARC Υ_disk 0.25–1.0 and Υ_bulge scaled alike). Υ propagates into M_b
and M_c, not into M_formed. The source lane's own error is reported beside it.

| class | sample and statistic | role |
|---|---|---|
| U: MW ultra-faints | FG001/CFG42: 31 resolved + 9 upper limits; Kaplan–Meier median of log10(σ_obs/σ_pred) at (4/3) r_h with half the baryons; bootstrap 1000 (seed 42) | graded |
| C: MW classical dSphs | FG001/CFG42: 14, with CFG18 infall gas; median; 1.2533 rms/√n | **CALIBRATOR** |
| M: M31 dSphs | Collins+13 (14) and LVD (34), as CFG42 (infall gas); each graded; class = the worse | graded |
| I: isolated LG dwarfs | CFG874's 11 (≥ 300 kpc from MW and M31), Υ_V 2, HI inside r12 by CFG874's disc rule; mean of D = log10(3σ²/r12 / g_pred); bootstrap se (4000, seed 874) | graded |
| S: SPARC, all | CFG828's cuts (Q ≤ 2, i ≥ 30°, eV/V < 0.10), Υ_d 0.5, Υ_b 0.7; per galaxy, the median over points of log10(g_obs/g_pred); class = median over galaxies; 1.2533 rms/√n | graded |
| S3: SPARC, faintest tercile | the same, for the lowest third in M* = 0.5 L[3.6] among galaxies passing the cuts | graded |
| X: eRASS1 cluster cores | median-cluster comparison (§4.1) | graded, not galaxy-scale |

- For SPARC, the debris is added spherically: g_deb(R) = G M_deb(<R)/R² at each point. M_b = 0.5 L[3.6] + 1.33 M_HI from the
  master table.
- For the satellites and isolated dwarfs, M_b is the estimator's own baryons (stars at Υ_V 2, plus gas as the source lane
  counts it), and M_c is built from it. For the isolated dwarfs the catchment uses all HI (1.33 M_HI), while the estimator uses
  CFG874's gas inside r12.

**Class rule** (each class, each footing, z = statistic/error):
- |z| < 2: **CONSISTENT**;
- 2 ≤ |z| < 3: **TENSION**;
- |z| ≥ 3: **CONTRADICTED**.

### 4.1 Cluster class (crude; declared)

- **Median cluster:** M_b = 1.2 × median MGAS500 of CFG687's 318 eRASS1 clusters (cfg687_percluster.npz), bracket ×1.0 to
  ×2.0, with R500 = their median.
- **Prediction:** the H-ELS residual debris projected inside R = 0.5 Mpc (truncated-NFW cylinder mass, numerical).
- **Target:** CFG922's U-solution needed mass (needed_masses → U, canonical / alt). The acceptance window is
  [λ_Z2 · M_gas,cyl, 2 · needed − λ_Z2 · M_gas,cyl], with M_gas,cyl = needed/λ and λ_Z2 from CFG922's Z2 entry.
- **Grade:**
  - CONSISTENT (MID only; OUTER not computed) if the primary corner lies in the window;
  - CONTRADICTED if every corner of {M_b bracket} × {AGN 0, 3e62} × {bcg_med, bcg_sup} lies outside on the same side;
  - otherwise UNDERDETERMINED.
- The shape of CFG922's needed extra differs from an NFW, so this is an amplitude check only.

## 5. Calibration (ONE constant, ONE class)

- **Calibrator:** ε, per footing, on class C (MW classical dSphs). ε* is the root of [C's median offset = 0] on [0, ∞). The
  offset is non-decreasing in ε, so the root is found by bisection in log ε on [1e-8, 1e4].
- **Physical domain:** ε ≤ 1, since an SN-energy-limited rule cannot use more than the SN energy. A root ε* > 1 makes the
  overall **UNPHYSICAL**.
- **No root** (the offset has the same sign at ε = 0 and ε = ∞):
  - define the allowed set A = {ε ∈ [0, 1]: |z_C| < 2} on the grid {0} ∪ logspace(−4, 0, 41);
  - if A is empty, the overall is **CALIBRATION IMPOSSIBLE**;
  - otherwise each graded class takes its best label over A, and the joint test requires ONE common grid ε ∈ A at which
    every galaxy-scale class is CONSISTENT.
- With a root, everything is graded at ε* (the A-set result is reported beside it).

## 6. Overall rule, corners, variants

**Primary corner:** N-A, C = 3000, r_b = r_ta, census supply, Form A, the law's potential, ν_e, burst M_formed for non-SFH
objects, [M/H] −1.31.

**Overall (per footing):**
- **SURVIVES:** the calibration exists with ε* ≤ 1 (or A is non-empty), AND every galaxy-scale graded class (U, M, I, S, S3)
  is CONSISTENT at one ε.
- **CONTRADICTED:** any galaxy-scale graded class is CONTRADICTED at ε* (or, without a root, at every ε in A); or the overall
  is UNPHYSICAL / CALIBRATION IMPOSSIBLE.
- Otherwise: **NOT SURVIVING (TENSION)**.

**Final:** SURVIVES only if it SURVIVES on both footings; CONTRADICTED if either footing is CONTRADICTED; otherwise NOT
SURVIVING (TENSION).

**Corners** (Form A, law potential, ν_e; each fully re-calibrated):
{N-A, N-B, R1} × C {1500, 3000, 6000} × r_b {r_ta, r_vir} × supply {census, ×2} = 36 per footing.
- "Supply ×2" doubles M_ta and M_c: f_ret halved at every mass.
- The final label is **ROBUST** if it is identical at all 36 corners. Otherwise the count and the differing corners are
  reported, and the primary-corner label stands as the verdict.
- **Favourable corner F*:** (N-B, C 6000, r_vir, supply ×2).

**Variants** (at the primary corner and at F*; reported; a variant that flips a class marks that class FRAGILE):
- Form B;
- Φ including the debris' self-gravity;
- the ν_simple kernel;
- the CFG827-median M_formed/L_V for non-SFH objects;
- [M/H] −1.71 / −0.71.

## 7. Diagnostics (no class weight)

- **D1:** the R1 energy direction. The median ΔU per class, and the fraction with ΔU < 0 (settling releases energy), primary
  corner.
- **D2:** who is starved. Spearman ρ(f_s, M_b) per class at ε* (or at the A-set midpoint), primary corner and F*.
- **D3:** what it would take. A multiplier N_x on the native supply (M_ta, M_c) at ε = 0 under N-B (C 3000, r_ta) that zeroes
  the U offset, found by bisection on [1, 1e5]. Then, at that N_x, C's calibration ε* and the other classes. N_x is NOT
  framework-native (it is abundance-matching territory) and cannot change the verdict.
- **D4:** central surplus. Q_ap = M_c,NFW(<r_ap)/M_ph(<r_ap) at each dwarf's aperture (native, primary C and r_b): median,
  range, and the fraction with Q_ap > 1.
- **D5:** the R1 maximum excess over all f_s ∈ [0, 1] (no energy rule) for U, C and I. This is the most generous bound of the
  identity reading.

## 8. Controls

**K tests** (`CFG930_MODE=K`; outputs cfg930_K.out, cfg930_results_K.json):
- **K1:** CFG42's committed H1/H2/H4 numbers are reproduced by exec'ing its code read-only to 1e-9, AND by this lane's
  H-ELS code path with K inputs at f_s = 0 to 1e-9:
  - UF km/tot/z for law and rule, both footings;
  - CL med/tot/z for cls, col, m31;
  - H4 n = 110, nfex = 0.
- **K2:** CFG827's Υ_SFH and E_SFH for all 36 dwarfs, to 1e-12.
- **K3:** CFG874's primary isolated E and se_E on both footings, and the K1 identity, to 1e-12.
- **K4:** source facts recomputed or read from committed JSON:
  - CFG828's SPARC overall median (+0.031, recomputed with this lane's SPARC loader, to 1e-9) and its exploratory
    ρ(Δ, g_bar) over 29 dwarfs (−0.47, recomputed from cfg828_results.json rows);
  - CFG921's F0 and F10 (read);
  - CFG823's median q (read);
  - CFG922's needed masses and λ_Z2 (read);
  - CFG804's census (N = 10 at log M_b 10.5).
- **K5:** native tables.
  - σ8 from this lane's integrator on Plin_z0 equals CFG654's stored native σ8 (cfg654_ics_results.json, the entry matching
    the cmb tables) within 2e-3.
  - Δ_ta(0) = 11.8977.
  - D(z = 0) = 1.
  - The extended P(k) is continuous at k_max (ratio 1 to 1e-12), and its local slope there is within 0.1 of the table's.
- **K6:** numerics.
  - NFW enclosed mass vs quadrature (1e-8).
  - The z_coll root residual (< 1e-8).
  - ΔE vs an independent quadrature (1e-6).
  - Projected NFW mass vs a numerical double integral (1e-4).
  - The Plummer + ν law potential vs direct integration (1e-6).
- **K7:** limits. f_s = 1 equals the bare law in every class (1e-12), and f_s = 0 with K inputs equals CFG42's rule (1e-9).

**MUTATE** (separate outputs, cfg930_MUTATE_<tag>.out and cfg930_results_MUTATE_<tag>.json):
- **M0** (`eps0`): K inputs, ε = 0 forced through the H-ELS path. It must reproduce CFG42's classical over-prediction (MW cls
  median −0.118 / −0.123, LVD −0.107 / −0.109, to 1e-9). It BITES if both are over-predicted (z < −1.5). The native ε = 0 values
  are reported beside it.
- **M∞** (`epsinf`): ε → ∞ (f_s = 1) for both input sets. It must give the bare law in every class (1e-12 vs the law path).
- **MK** (`K`): the full H-ELS calibration and grading with CFG42's ΛCDM inputs. This is a capability check that the selector
  can act: C must have a root. It is labelled "ΛCDM inputs, not a verdict", and its classes carry no weight.

## 9. Sealed predictions (frozen form here; numbers written by the main run into SEALED_PREDICTIONS.md, hashed and committed before any data for them is read; this lane reads none)

- **S1 (tidal dwarf galaxies):** a tidal dwarf has no primordial halo, so H-ELS predicts zero excess at every ε. A TDG sample
  (gas counted, the same estimator) must sit on the law. A mean excess > 2 se contradicts H-ELS. (The bare law predicts the
  same; S1 separates H-ELS from any "uniform dwarf excess" reading, not from the bare law.)
- **S2 (faint gas-rich rotating dwarfs, M* < 1e6):** H-ELS's excess at ε* (frozen model; gas counted in M_b and M_c; M_formed
  = M*/m_rem for a constant SFH at [M/H] −1.31), compared with a gas-poor dSph at the same g_bar.
  - The main run writes the predicted ratio and sign over a declared grid (M* 1e5, 3e5, 1e6; M_gas/M* 1, 3, 10;
    g_bar 1e-12.5 to 1e-11.5).
  - Under N-A both are zero (bare law).
- **S3 (ranking):** the sign and size of Spearman ρ(excess, M_formed) among classical dSphs under H-ELS at ε*.
  - CFG827's E values for its 36 dwarfs were seen in this session, so S3 is sealed for dSphs and data NOT in CFG827 (new SFHs
    or kinematics).
  - A check on the seen CFG827 values is reported as non-blind, with no weight.
- **Hash:** sha256 of SEALED_PREDICTIONS.md in SEALED_PREDICTIONS_SHA256.txt, committed before the README. The faint-rotator
  lane CFG931 (another session) is NOT read by this lane.

## 10. Compute, outputs, amendments

- **Compute:** one core (OMP_NUM_THREADS=1, nice -n 10), each process < 1 GB, one process at a time, nothing downloaded,
  no other lane's files written (writes refused in exec'd code).
- **Script:** cfg930.py, with CFG930_MODE = K | MUTATE_eps0 | MUTATE_epsinf | MUTATE_K | MAIN (default). Main outputs are
  cfg930.out and cfg930_results.json.
- **Amendments:** any change after this commit is a dated, labelled amendment (AMENDMENT_A<n>.md). It states whether it was
  made before or after the K, MUTATE or main run. No class rule changes after a main-run number is seen.

κ = ½ is FITTED. The footings are never pooled. No dark-matter species. Not "theory closed".
