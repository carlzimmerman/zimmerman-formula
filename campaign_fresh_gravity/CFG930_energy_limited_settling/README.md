# CFG930: energy-limited settling of primordial cold energy (H-ELS). CONTRADICTED on both footings, at all 36 corners, in every variant

**Bottom line.** The synthesis does not survive on framework-native inputs. The decisive class is the MW ultra-faints:
- **At the primary corner (framework-consistent reading N-A)** the ultra-faints stay at the bare law's +0.325 / +0.304 dex
  (z +3.77 / +3.55).
- **At the most generous corner F* (N-B)**, ε calibrated on the MW classicals settles the ultra-faints completely (offset
  again +0.325 / +0.304). It also leaves unsettled debris in the faint SPARC rotators: −0.344 / −0.362 dex, z −6.4 / −6.5.

Three structural reasons, each checked by its own diagnostic, make the failure robust:
1. **No leftover.** The record's catchment supply (5.364/f_ret, f_ret = 0.10) is only 1–5% of the law's phantom inside
   CFG35's edge for every dwarf, and 35–41% for SPARC. CFG35's leftover f_ex is 0 in all 251 tabulated objects, so there is no debris
   to retain.
2. **No central surplus.** The native primordial cold mass inside each dwarf's aperture is 14–32% of the settled phantom's
   (median Q_ap). Under the identity reading, settling into the phantom RELEASES energy in 100% of objects (ΔU < 0). It needs
   no feedback input at all.
3. **The energy ordering is inverted.** Per unit of debris binding energy, the faintest systems have the most SN energy:
   E_SN/ΔE is about 600 for the ultra-faints, 22 for the classicals and 0.5 for SPARC. So the ultra-faints settle first and
   the rotators never do. This is the reverse of hypothesis item 3.

κ = ½ is FITTED. The footings 9.3603e-11 / 1.1312e-10 are scored separately and never pooled. Verdicts use raw data and
framework-native inputs only; ΛCDM inputs appear only in the K tests and the labelled MUTATE-K check. The extra mass is cold
energy, not a particle. Not "theory closed". Nothing here says the data favour the framework.

| | |
|---|---|
| Kind | HYPOTHESIS TEST: one new constant (ε) and one new rule (energy-limited settling) |
| Block | CFG930–939 (this lane uses CFG930) |
| Criteria | `FROZEN_CRITERIA.md`, **3dec25afe**, committed alone before any script or number |
| Amendment | `AMENDMENT_A1.md`, **ac09dba80**, written before any run (clarifications only; no rule changed) |
| Sealed predictions | `SEALED_PREDICTIONS.md`, sha256 **57b1141e…dc789** (`SEALED_PREDICTIONS_SHA256.txt`), committed in **cbb3b9888**, before this README |
| Not blind | H-ELS was formed after CFG42–CFG926. The criteria quote the record it was built from and disclose the pre-freeze expectations E1–E3. All three were confirmed. |

## The hypothesis and what is new

Cold energy starts as ordinary cold collisionless matter (Ω_c/Ω_b = 5.364, CFG649/CFG654), so every system begins with a
primordial collapse halo. Settling into the law's phantom proceeds only as far as baryonic feedback energy pays for unbinding
the central surplus. The unpaid remainder stays as real bound mass: the "excess family".

**Model** (CFG35/CFG42 sum form with a settled fraction):

    g = g_law + (1 − f_s) G M_deb(<r)/r²,   M_deb = f_ex (1 − f_b) M_NFW,   f_s = clip(ε e_SN M_formed / ΔE, 0, 1)
    ΔE = ∫_0^{r_e} g_law(r) M_deb(<r) dr     (lifting the debris out to CFG35's edge, in the law's potential)

### Posits

| posit | status | value / source |
|---|---|---|
| **energy-limited settling rule f_s = clip(E_avail/ΔE)** | **NEW** | this lane |
| **ε (feedback coupling)** | **NEW, one constant**, calibrated on the MW classical dSphs per footing | primary: no root (any ε ≤ 1 allowed); F*: ε* = 0.052 / 0.112 |
| e_SN = 1e49 erg per M☉ formed | declared | criteria §3.4 |
| M_formed | inherited data | Weisz+14 SFH × E-MILES for 35 matched dwarfs (CFG827 code), else a 13.3-Gyr burst; SPARC M*/m_rem (constant SFR) |
| galaxy law, κ = ½ | inherited, κ FITTED | ν_e (= ν_mono for y ≤ 0.1), exact footings |
| supply 5.364/f_ret, census f_ret | inherited (both flagged ΛCDM-derived in the record) | CFG804/CFG416 fixed point; f_b = 1/(1+5.364) |
| ρ_s = C ρ̄_m(z_coll), with z_coll from NFW97's EPS half-mass condition | declared generic collapse physics; C bracketed {1500, 3000, 6000} | native σ(M) and D(z) from CFG654 cmb tables (σ8 0.8252 reproduced) |
| NFW boundary | declared, bracketed | native r_ta (Δ_ta(0) 11.898) or r_vir (Δ_vir 304) |
| edge r_e = 0.40 r_ta,law | inherited (CFG35) | native background |

## Results (`cfg930.out`, `cfg930_results.json`)

**Uniform error recipe:** the source lane's statistical error ⊕ a Υ floor (Υ ×½ to ×2). z = statistic/total.
- |z| < 2: CONSISTENT
- 2 ≤ |z| < 3: TENSION
- |z| ≥ 3: CONTRADICTED

### Primary corner: N-A, C 3000, r_ta, census supply, Form A

f_ex = 0 everywhere, so the model IS the bare law. The calibrator has no root (offset +0.027 / +0.007 at every ε), so all 42
grid values of ε ≤ 1 are allowed and none helps.

| class | canonical stat (z) | label | alt stat (z) | label |
|---|---|---|---|---|
| U: MW ultra-faints (31 + 9 limits, KM median, dex in σ) | +0.325 (+3.77) | **CONTRADICTED** | +0.304 (+3.55) | **CONTRADICTED** |
| C: MW classicals (calibrator, 14) | +0.027 (+0.32) | CONSISTENT | +0.007 (+0.09) | CONSISTENT |
| M: M31 Collins+13 (14) / LVD (34) | +0.064 (+0.78) / +0.044 (+0.60) | CONSISTENT | +0.045 (+0.55) / +0.031 (+0.42) | CONSISTENT |
| I: isolated LG dwarfs (11, mean D, dex in g) | +0.194 (+1.27) | CONSISTENT* | +0.155 (+1.02) | CONSISTENT* |
| S: SPARC, 147 galaxies (median of galaxy medians, dex in g) | +0.011 (+0.07) | CONSISTENT | −0.015 (−0.11) | CONSISTENT |
| S3: SPARC, faintest M* tercile | +0.019 (+0.26) | CONSISTENT | −0.018 (−0.24) | CONSISTENT |
| X: eRASS1 median cluster | no debris (0 vs needed window 1.76–3.11e13 M☉) | **CONTRADICTED** | same | **CONTRADICTED** |

\* Under CFG874's own error (bootstrap only, no Υ floor) the isolated class is +0.194 ± 0.077 (2.5 se), i.e. TENSION. The
uniform recipe adds a Υ floor of 0.133. Either way the overall is set by the ultra-faints.

**Overall (primary): CONTRADICTED on both footings.**

### Favourable corner F*: N-B (all primordial cold kept as debris on top of the law), C 6000, r_vir, supply ×2

| class | canonical (ε* 0.0523) | alt (ε* 0.1124) |
|---|---|---|
| U | +0.325 (+3.77) **CONTRADICTED**: f_s = 1 (fully settled) | +0.304 (+3.55) **CONTRADICTED** |
| C (calibrator) | 0.000 | 0.000 |
| M Collins / LVD | +0.014 / +0.023, CONSISTENT | +0.009 / +0.022, CONSISTENT |
| I | +0.132 (+0.68), CONSISTENT | +0.126 (+0.72), CONSISTENT |
| S | −0.304 (−3.18) **CONTRADICTED** | −0.317 (−3.28) **CONTRADICTED** |
| S3 | −0.344 (−6.44) **CONTRADICTED** | −0.362 (−6.45) **CONTRADICTED** |
| X | over-predicted (projected debris 0.95–1.10e14 vs ≤ 3.1e13) **CONTRADICTED** | same |

Even at ε = 0, F* moves the ultra-faints only to +0.262 / +0.248 (z +3.1 / +2.9; `cfg930_MUTATE_eps0.out`). The most generous
native debris does not close them before any settling.

### All 36 corners, both footings (`corners` in the JSON)

- **N-A (12 corners):** every corner equals the bare law. U is CONTRADICTED; all other galaxy classes are CONSISTENT.
- **N-B (12):** U is CONTRADICTED at every corner, fully settled at ε* = 0.011–0.11 (all physical). S3 is CONTRADICTED at
  8 / 9 corners (canonical / alt), TENSION at 3 / 3, and CONSISTENT at 1 / 0. S is TENSION or CONTRADICTED at 4 corners. The cluster class is CONTRADICTED at 9 corners (over-predicted)
  and UNDERDETERMINED at the 3 r_ta × census corners.
- **R1 (identity reading, 12):** U is CONTRADICTED; all others are CONSISTENT.
- **Final label CONTRADICTED at 36 / 36: ROBUST.**

**Variants** (primary and F*): Form B (inside-out core), debris self-gravity in Φ, the ν_simple kernel, the CFG827-median
M_formed/L for non-SFH objects, and [M/H] −1.71 / −0.71.
- Every variant is CONTRADICTED on both footings.
- The only class flip is F* Form B: S CONTRADICTED → TENSION (−0.279 / −0.282). S3 stays CONTRADICTED (z −5.7 / −5.8).

## Why it fails: diagnostics (no class weight; numbers canonical / alt)

| | finding |
|---|---|
| f_ex (E1) | 0 in 251 / 251 tabulated objects. M_c/M_ph(<r_e) medians: ultra-faints 0.014 / 0.012, classicals 0.051 / 0.044, M31 0.047–0.051, isolated 0.046, SPARC 0.41 / 0.35 |
| D4 central surplus (E3) | Q_ap = M_cNFW(<r_ap)/M_ph(<r_ap), medians: U 0.15 / 0.14, C 0.32 / 0.29, M31 0.28–0.30, I 0.26 / 0.24. Q > 1 only for M 32 (11.4 / 5.6), a compact elliptical with a small phantom |
| D1 energy direction | identity reading: ΔU = U_settled − U_primordial < 0 for **100%** of objects in every class (median −2e43 J for ultra-faints, −3e46 J for dSphs, −3e51 J for SPARC). Settling into the phantom releases energy and needs none. Read with CFG918, the forming core must SHED energy, so feedback works against it |
| D5 identity-reading bound | the largest excess R1 can give at any f_s: ultra-faints gain +0.018 dex in σ (median; max +0.035), KM +0.304 vs law +0.325. Classicals +0.001; isolated +0.110 vs law +0.194 |
| D2 who is starved (E2) | N-B, at that corner's ε*: Spearman ρ(f_s, M_b) = −0.6 to −0.9 in every class with spread. E_SN/ΔE medians: U 644 / 575, C 22 / 20, M31 LVD 24 / 22, isolated 42 / 38, SPARC 0.50 / 0.45. The faintest settle completely, the rotators hardly at all |
| D3 what it would take | under N-B at ε = 0, the ultra-faints close only with the supply ×6460 / ×5790 (f_ret ≈ 1.6e-5, far outside the census). Calibrating ε on the classicals then needs ε* = 25 / 31 (UNPHYSICAL, > 100% of SN energy). The ultra-faints return to +0.325 and SPARC goes to −0.77 (z −10). No supply level rescues it |

**ΛCDM-input capability check (MUTATE-K, no verdict weight).** With CFG42's own Moster+13 / Dutton–Macciò inputs, the
calibrator has a root (the selector can act), but at ε* = 1.13 / 1.39. That is more than 100% of the SN energy (UNPHYSICAL).
At that ε the ultra-faint closure is lost: +0.284 / +0.283, against −0.059 with no settling. Even with abundance-matching
masses, one energy coupling cannot keep the ultra-faints closed while removing CFG42's classical over-prediction, because
ΔE in the law's potential scales the same way.

## Controls

| control | result |
|---|---|
| K1a | CFG42 exec'd read-only reproduces its committed H1/H2/H4 numbers exactly (max \|d\| 0); H4 n 110, nfex 0 |
| K1b / K7b | this lane's H-ELS path with CFG42 inputs: f_s = 0 equals CFG42's rule and f_s = 1 its law (5.6e-17) |
| K2 | CFG827's Υ_SFH (3 metallicities) and E_SFH for all 36 dwarfs (max \|d\| 0) |
| K3 | CFG874's isolated E = +0.1944 ± 0.0767 / +0.1553 ± 0.0765, exec'd and by this lane's bootstrap replay (exact); its K1 identity (0) |
| K4 | CFG828 SPARC median +0.0309 recomputed (2696 points, \|d\| 0); CFG828 ρ(Δ, g_bar) −0.467 (N 29); CFG921 F0 +0.856, F10 −1.356; CFG823 median q 0.303; CFG922 U need 2.431e13; CFG804 N(10.5) = 10 |
| K5 | σ8 0.82521 vs CFG654 NATIVE_CMB 0.82522; Δ_ta(0) 11.8977; D(0) = 1; P(k) extension continuous, slope −2.754 vs table −2.776 |
| K6 | NFW mass 9e-15; z_coll root 4e-16; ΔE vs quadrature 8.5e-8; projected mass vs double integral 0; potential 5e-8 |
| K7a | f_s = 1 equals the bare law at every object (0) |
| M0 (ε = 0, K inputs) | **BITES:** reproduces CFG42's classical over-prediction exactly (MW −0.118 / −0.123; LVD −0.107 / −0.109; z −1.78 / −2.67) |
| M∞ (ε → ∞) | K inputs reproduce CFG42's law numbers (0). Native N-A / N-B equal the bare law (0). R1 equals the supply-capped law (A1-6; the cap binds for Boötes III only, Mph/Mc 1.10) |
| MK | selector can act (root on both footings); ε* > 1 (above) |

**Fixes before any number** (disclosed): one keyword clash in the object class (an attribute named like the method's self
argument) stopped the first K launch with a TypeError before it produced any number. It was renamed. Nothing else changed
between the A1 commit and the runs.

## Sealed predictions (sha256 57b1141ebf61ef30e6e4be851ef4962278496796e640923761da8776398dc789)

- **S1 (tidal dwarfs):** zero excess, the same as the bare law.
- **S2 (gas-rich rotators with M* < 1e6 vs gas-poor dSphs at the same g_bar):**
  - Primary: zero for both.
  - F*: rotators +0.02 to +0.31 dex in g (more gas means more excess); dSphs 0 (fully settled).
- **S3 (classical-dSph ranking):**
  - Primary: no ranking (zero excess).
  - F*: predicted ρ(excess, M_formed) = **+0.565 / +0.739** (more stars formed, MORE excess).
  - The non-blind check on CFG827's eight MW classicals gives **ρ = −0.714**: the observed ranking has the sign the original
    premise wanted, and the native model predicts the opposite. No weight, because these values were seen before sealing.
- These are predictions of a CONTRADICTED hypothesis. They are recorded so it cannot be re-fitted later.

## What is established

- On framework-native inputs (census supply, native collapse epoch, native growth), primordial collapse debris cannot be the
  excess family under any reading tested (N-A, N-B, R1), any C, boundary or supply ×2, either form, either kernel, either
  footing.
- The census supply is too small to leave any debris beyond the law's phantom (f_ex = 0). The native NFW cusp sits BELOW the
  settled phantom at every dwarf aperture except M 32. Settling into the phantom releases energy.
- An SN-energy budget scaled to the law's potential settles the faintest systems first. That is the opposite of what the
  excess family needs (CFG828: excess anticorrelates with g_bar; CFG880: tinies want the most). It would leave real debris in
  gas-rich rotators, which SPARC excludes (S3 z −6.4).
- The record's design constraint from CFG42 ("the debris must switch off where the phantom supplies the mass") is NOT met by
  an energy budget. Native debris is either absent (N-A) or switches off in the wrong systems (N-B).

## What is NOT established

- **No energy-limited mechanism is excluded for a different supply.** D3 shows the supply would have to be ~6000× the census
  (f_ret ~ 1e-5, abundance-matching territory), and even then ε* > 20. That route is not open on framework-native terms.
- **No new inputs were measured.** The census f_ret, 5.364 (both flagged ΛCDM-derived in the record), NFW97's collapse
  calibration C (from collisionless N-body; bracketed ×/÷2) and the cold-matter P(k) asymptote beyond 110 h/Mpc are all
  inherited or declared.
- **Satellite halos are not tidally stripped here.** Stripping would remove debris and deepen the ultra-faint failure.
- **The SPARC debris is added spherically.** The cluster class is a crude median-cluster amplitude check (OUTER not computed).
- **The ΛCDM-input MK result carries no weight.**
- **The excess family is still unexplained.** This lane removes one candidate mechanism. It does not say which mechanism, if
  any, works.

## Reproduce

One core, `nice -n 10`, ≤ 0.41 GB, nothing downloaded. CFG42, CFG827 and CFG874 code is exec'd read-only (writes refused);
other lanes' JSON files are only read.

- `CFG930_MODE=K OMP_NUM_THREADS=1 nice -n 10 python3 cfg930.py` → `cfg930_K.out`, `cfg930_results_K.json` (exit 0, 5 s)
- `CFG930_MODE=MUTATE_eps0 …` → `cfg930_MUTATE_eps0.out`, `cfg930_results_MUTATE_eps0.json` (exit 0 = bites)
- `CFG930_MODE=MUTATE_epsinf …` → `cfg930_MUTATE_epsinf.out`, `cfg930_results_MUTATE_epsinf.json` (exit 0)
- `CFG930_MODE=MUTATE_K …` → `cfg930_MUTATE_K.out`, `cfg930_results_MUTATE_K.json` (exit 0 = selector can act)
- `OMP_NUM_THREADS=1 nice -n 10 python3 cfg930.py` → `cfg930.out`, `cfg930_results.json`, `SEALED_PREDICTIONS.md` + hash
  (110 s, exit 0)

κ = ½ is FITTED. The footings are never pooled. No dark-matter species. Not "theory closed".
