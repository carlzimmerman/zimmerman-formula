# GB1: the all-gates battery. NOTHING PASSES ALL STATIC GATES

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Criteria: FROZEN_CRITERIA.md (e9464bc8ce), committed alone
before any script. Script: gb1.py (one thread, about 2 minutes, under 1 GB). Outputs: gb1.json / gb1.out (main),
gb1_MUTATE.json / gb1_MUTATE.out (Newton twin). A rerun gives a byte-identical gb1.json.

**Label: no candidate passes. None of the six reaches PASS on every static row (G1-G8) on either footing.** G9 (CMB
lensing shape and growth) is NOT EVALUATED in v1, so even a static winner would only have "passed all static gates".

- Every candidate graded fails the Coma UDGs (G5) by at least 3.97 sigma_U.
- Every candidate either fails X-COP (G2), groups (G3) and the dSph classes (G6), or is NO VERDICT on them with a
  bracket reading of FAIL for every admissible value.
- The plain law passes SPARC and the Solar System and fails everything else.

## Known answers (all PASS; nothing was graded until they did)

| KA | canonical | alt | line |
|---|---|---|---|
| KA1 L0 class means vs QX20 (X, E, S, G f*0, G f*1) | +0.467499, +0.209888, +0.027383, +0.358644, +0.195519; max \|d\| 4.3e-7 | +0.434523, +0.188763, -0.000603, +0.320274, +0.158280; 4.5e-7 | 1e-6 |
| KA2 UDG mean vs S1 | +1.120753, \|d\| 0 | +1.077576, 2.2e-16 | 1e-9 |
| KA3 QX21 (footing-free KiDS; dSph 5 classes x 2 footings, medians and CIs replayed) | D +0.158171, sigma_stat 0.040095, D_law +0.000215, sigma_tot 0.0641; max \|d\| 0 | (same) | 1e-9 |
| KA4 L1 ellipticals vs QX26 D_imf | +0.093043, 2.5e-7 | +0.074252, 3.2e-7 | 1e-6 |
| KA5 L2 SPARC prediction vs QX20 V2 | +0.133882260, 0 | +0.113236781, 0 | 1e-9 |
| KA6 dSph x inversion; C6P constants | 0 missing; Mars 0.172844, Hees margin 4.8486e7 | 0 missing; 0.172844, 5.7022e7 | see disclosure 1 |

The SPARC rms line (L0's fixed-Upsilon rms + 0.010) is 0.1457 canonical and 0.1425 alt.

## Candidate x gate x footing (canonical / alt)

| | G1 SPARC (Z, rms) | G2 X-COP (mean, rms) | G3 groups (pass f*0, f*1 of 20) | G4 ellipticals (mean) | G5 Coma UDGs | G6 dSph (bright M31 / MW classical / LG field, median - anchor [95 % CI]) | G7 KiDS (R, sigma) | G8 Solar System (worst use of bound) |
|---|---|---|---|---|---|---|---|---|
| **L0** plain law | PASS +0.027, 0.136 / PASS -0.001, 0.133 | FAIL +0.468, 0.476 / FAIL +0.435, 0.444 | FAIL 0, 0 / FAIL 0, 0 | FAIL +0.210 / FAIL +0.189 | FAIL +1.121 (+4.28) / FAIL +1.078 (+4.11) | FAIL: +0.199 [+0.079, +0.393] / +0.217 [-0.049, +0.544] / +0.019 [-0.027, +0.164]; alt +0.188 [+0.068, +0.382] / +0.207 / +0.007 | FAIL +0.158 (+2.46) / same | PASS 0.211 / PASS 0.190 |
| **L1** law + IMF | NV (disc/bulge sigma); bracket PASS all (Z +0.024..+0.007, rms <= 0.140) / NV; bracket PASS all | NV (BCG sigma); bracket FAIL all (+0.451..+0.445) / NV; FAIL all (+0.418..+0.412) | NV; bracket FAIL all (0, 1) / NV; FAIL all (0, 1) | PASS +0.093 / PASS +0.074 | FAIL +1.121 (+4.28) / FAIL +1.078 (+4.11) | NV (SPARC anchor needs sigma); bracket FAIL: bright M31 +0.212 [+0.092, +0.406] / alt +0.201 [+0.081, +0.395] | NV (lens sigma); bracket PASS all (R +0.121..+0.080, <= 1.90 sigma) / same | PASS 0.211 / PASS 0.190 |
| **L2** QX20 V2 power law (reference) | FAIL -0.107, 0.169 / FAIL -0.114, 0.172 | FAIL +0.028, 0.126 / FAIL +0.030, 0.126 | FAIL 1, 1 / FAIL 1, 1 | PASS -0.009 / PASS -0.003 | FAIL +1.073 (+4.09) / FAIL +1.040 (+3.97) | FAIL: +0.303 [+0.178, +0.492] / +0.324 / +0.125 [+0.067, +0.264]; alt FAIL similarly | FAIL +0.133 (+2.08) / FAIL +0.135 (+2.11) | FAIL 6.9e5 / FAIL 4.0e5 |
| **F1** exact AQUAL field | FAIL +0.049, 0.150 / FAIL +0.022, 0.1429 (line 0.1425) | FAIL +0.468, 0.476 / FAIL +0.435, 0.444 | FAIL 0, 0 / FAIL 0, 0 | FAIL +0.210 / FAIL +0.189 | FAIL +1.121 / FAIL +1.078 | FAIL: +0.178 [+0.057, +0.371] / +0.196 / -0.003; alt +0.166 [+0.046, +0.360] | FAIL +0.158 (+2.46) / same | PASS 0.211 / PASS 0.190 |
| **F2** formation-epoch a0 memory | NV (z_f); bracket MIXED | NV; bracket FAIL all | NV; FAIL all | NV; FAIL all (+0.189 at best / +0.166) | NV; FAIL all (>= +3.96 sigma) | NV; FAIL all | NV; FAIL all | NV; bracket PASS all |
| **F3** exact field + IMF | NV; bracket FAIL all (rms 0.150-0.153 / 0.143-0.148) | NV; bracket FAIL all | NV; bracket FAIL all | PASS +0.093 / PASS +0.074 | FAIL +1.121 / FAIL +1.078 | NV; bracket FAIL all | NV; bracket PASS all | PASS 0.211 / PASS 0.190 |
| *MUTATE Newton* | FAIL +0.431, 0.514 (both) | FAIL +0.937 | FAIL 0, 0 | FAIL +0.416 | FAIL +2.21 (+8.4) | FAIL: +1.05 / +0.79 / +0.67 | FAIL +0.158 | PASS 0 |

NV = NO VERDICT (a needed feature is not carried by that class; it counts as not passing). The bracket readings are
reported and never replace the graded cell. The X-COP and group stellar sigma brackets are QX26's (250-350, 200-300
km/s).

## Labels

| Candidate | Label |
|---|---|
| L0 plain law | **FAIL** (G2, G3, G4, G5, G6, G7). Passes G1 SPARC and G8 Solar System on both footings |
| L1 law + IMF | **FAIL** (G5); NO VERDICT (G1, G2, G3, G6, G7). On the brackets it would also fail G2, G3 and G6. It is the best of the six: it adds G4 and, on the bracket, G7 |
| L2 QX20 V2 power law | **FAIL** (G1, G2, G3, G5, G6, G7, G8), as expected for a reference fitted on the hot points: it misses the SPARC anchor by -0.11 and the Solar System by a factor of 4e5-7e5 |
| F1 exact AQUAL field | **FAIL** (G1-G7). The action's own field changes nothing on the hot gates (spheres are exact) and moves SPARC the wrong way at fixed Upsilon |
| F2 formation-epoch a0 memory | **NOT GRADABLE** (every row needs z_f, carried by no class). For every admissible a0(z_f)/a0(0) in 0.33-1.21, G2-G7 fail |
| F3 exact field + IMF | **FAIL** (G5); NO VERDICT elsewhere, with bracket FAIL on G1, G2, G3, G6 |
| MUTATE Newton | **FAIL** (G1-G7) on both footings: the battery bites |

**Which candidate passes every static gate: none.**

## What the battery says

1. **The Coma UDGs (G5) are the hardest row.** They sit +1.04 to +1.12 dex above every prediction, 4-4.3 sigma_U. None
   of the six candidates moves them down by more than 0.05 dex. That repeats QX20's finding that every variable leaves
   the UDGs 3-4 sigma low.
2. **Clusters, groups and the dSph step survive every correction graded.** On the IMF bracket X-COP keeps +0.445 /
   +0.412 and the groups pass 0-1 of 20. In the dSphs, bright M31 stays +0.20 above the SPARC anchor with its CI
   excluding zero, while the LG field dwarfs sit at zero. No feature-only candidate here separates those two dwarf
   classes.
3. **The IMF relation is the one correction that helps.** It brings the ellipticals inside G7's line (+0.093 /
   +0.074) and, on QX26's sigma bracket, the KiDS split inside 2 sigma (R +0.08 to +0.12). It cannot be graded as
   PASS on SPARC, KiDS or the hot classes, because no stellar sigma is carried there.
4. **The action's exact field (F1) is no help.** It is exact in spherical symmetry, so the hot classes are untouched.
   At fixed Upsilon it shifts SPARC's residuals by about +0.02 and raises their rms by 0.014 / 0.010.
   - Canonical: the fail is broad. Dropping the 11 points with T <= -0.2 still leaves rms 0.146.
   - Alt: the fail is marginal (0.1429 against 0.1425). Dropping those 11 points gives 0.139, under the line.
   - QX8's U-refit grader passes the same field, because U refits upward by about 0.02. This row is a fixed-Upsilon
     statement only. F1 fails six other rows on both footings either way.
5. **The history door (F2) is shut by sign and size, not only by missing data.** a0(z) from CFG689 lies at or below
   a0(0) at its central values. Even the 68 % envelope's top, 1.21, moves an offset by at most about +0.04 dex. The
   offset rises monotonically with a0(z_f)/a0(0), so a per-system choice of z_f cannot do better than the uniform
   maximum, and the maximum already fails G2-G7.

## Disclosed

1. **KA6 tolerance slip (post-freeze reading).** The criteria asked for C6P's constants to match the quoted
   0.1728 and 4.85e7 / 5.70e7 "to 1e-4 relative". The quoted values are rounded to 3-4 digits, so the JSON values
   differ from them by 2.5e-4 (Mars) and 3e-4 / 4e-4 (Hees). As frozen the check fails on rounding. The script reports
   both readings and passes on "equal to the quoted rounding". This was a mis-stated tolerance, not a loader fault, and
   no grade depends on it: G8 uses the JSON's own values.
2. **G6 bracket fill.** For L1/F3 the dSphs carry sigma, and the NO VERDICT comes only through the SPARC anchor. The
   bracket uses a single bulge sigma (150, the middle of the frozen SPARC bracket), a code choice not written in the
   criteria. Across the full SPARC bracket the anchor moves by at most 0.017. Bright M31's lower CI end sits +0.09
   above the anchor, so the reading holds at every bracket value.
3. **Conventions, as frozen.**
   - UDG predictions apply the isolated algebraic Delta at the internal x, on top of a base that already includes
     the action with Coma's EFE.
   - F1's T_geom = 0 for KiDS. The criteria justify it by "R_med >= 0.1 Mpc", which is a factual slip: CFG61's K1
     R_med runs from 0.044 to 0.29 Mpc. At 44 kpc and beyond (about 10 or more disc scale lengths) the monopole
     dominates. QX8's outermost SPARC points carry T of about -0.01, so a late-lens T of that size would give
     D_cand of about +0.01, against R = +0.158. The record has no solved lens-scale field.
   - L2's Solar-System multiplier converts Delta with the algebraic law. F2 treats its multiplier as acting on the
     hedgehog too, which is conservative.
4. **G7 power.** At fixed g_bar, any candidate that depends only on g_N gives D_cand = 0; Newton shows this. The KiDS
   row can reward only candidates whose features differ between early and late lenses. For L0 it reads FAIL at
   2.46 sigma against the 2 sigma consistency line (QX21's NO STEP line). QX21's own NO VERDICT answered a different
   question (is there a step at >= 3 sigma), and nothing here contradicts it.
5. **dSph LG field promoted to graded**, as written in the criteria. QX21 had it as reported only.
6. **Hot-system offsets are hydrostatic upper or lower bounds, as in QX20 and QX18.** Elliptical hot gas is not
   modelled, so those offsets are upper bounds.

Kappa = 1/2 FITTED; not theory closed.
