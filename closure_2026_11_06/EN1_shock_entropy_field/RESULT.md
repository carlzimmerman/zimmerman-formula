# EN1: shock-entropy field in the khronon sector. FAIL; the f table is not passed

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. This is a TEST lane that grades the owner's proposal as stated.
There is no particle. Criteria: FROZEN_CRITERIA.md (eae8892550), committed alone before any script. Script: en1.py
(one thread, about 3 s). Outputs: en1.json / en1.out, and the MUTATE twin's en1_MUTATE.json / en1_MUTATE.out. GB1,
KD1, QX5 and the X-COP temperature files are read only; none of them is edited. A rerun is byte-identical.

**Label: FAIL, all three variants, both footings. G2 X-COP and G3 groups fail. G4 ellipticals, G5 Coma UDGs, G6 dSph
classes and G7 KiDS are NO VERDICT: a proxy is missing. G1 SPARC and G8 Solar System pass. G9 (CMB) is carried as
FAIL: rho_x = 0 before the first shocks. The shock-entropy field does NOT pass the f table.**

**Why it fails, measured.** Across classes the measured adiabat K is ordered the way the need is: discs 0, ellipticals
24-86, groups 300-700, X-COP 200-1500 keV cm^2. Within a host the order reverses:

| | X-COP 0.1 R500 | 0.2 | 0.3 | 0.5 | 0.7 | groups R2500 | groups R500 |
|---|---|---|---|---|---|---|---|
| uniform f needed (median, canonical / alt) | 5.34 / 4.94 | 4.93 / 4.46 | 4.44 / 4.01 | 3.33 / 2.97 | 2.39 / 2.07 | 6.17 / 5.30 | 1.44 / 1.09 |
| measured K (median, keV cm^2) | 205 | 410 | 603 | 982 | 1075 | 311 | 706 |

- The need falls outward by 2.2x in X-COP and by 4.3x in groups. Over the same radii K rises 5x and 2.3x.
- In V-frac, M_x(<r)/M_b(<r) is a mass-weighted average of g(sigma) inside r. So for ANY non-decreasing g, it can only
  rise outward wherever sigma does. This is a post-result reading, not a frozen label.
- It survives the cooling caveat. Between 0.3 and 0.7 R500 the cooling time is long, so K is the shock record, and
  there the need still falls 1.9x while K rises 1.8x.

## The constant, fixed once per footing on X-COP

The mean over GB1's 35 X-COP points of M_x(<r)/M_b(<r) is set equal to KD1's Xcop_f_need (4.1786 canonical, 3.7833
alt). Nothing else is fitted.

| Variant | constant | canonical | alt |
|---|---|---|---|
| V-frac-L, g = sigma/sigma_* | sigma_* (keV cm^2) | 103.2 | 114.0 |
| V-frac-S, g = ln(1 + sigma/sigma_*) | sigma_* (keV cm^2) | 5.230 | 7.845 |
| V-dens-L, rho_x = lambda sigma | lambda (Msun kpc^-3 per keV cm^2) | 278.3 | 252.0 |

## Proxy per class (sigma = K = kT n_e^(-2/3), mu_e 1.155)

| Class | Proxy | Source |
|---|---|---|
| X-COP (7 clusters x 5 radii) | kT(r): spectroscopic profile, log-interpolated in r/R500. n_e(r): from dM_gas/dr. K 155-1456 keV cm^2 | `_external_data/xcop_thermo_2026_11_02/<name>/spectral_results_<name>.fits`, `<name>_temperature.fits` (sha256 in SOURCES.txt; on disk since 11-02, untracked); `real_research/data/xcop/<name>/<name>_fgas_profile.fits`, `_mstar.fits` |
| Groups (20) | global kT; n_e from the local slope of M_gas between R2500 and R500. K 181-674 (R2500) and 375-1567 (R500) | `real_research/data/lovisari2015_groups.tsv` |
| Ellipticals | K at 10 kpc from kT_o and n_e,10kpc: NGC 720 33, 1407 60, 4125 24, 4261 86, 4472 30, 4649 43 keV cm^2. **NGC 6482 is not in the table**, so G4 is NO VERDICT | `real_research/data/cfg57_gas_sources/fukazawa2006_table4.tsv` |
| SPARC discs | 0: no X-ray-hot gas at the measured radii | GB1 / SPARC |
| Coma UDGs | NO VERDICT. No Coma ICM density (n_e0 or n_e(r)) is on disk; S1 and CFG948 carry only the beta-model shape | needs a Coma n_e profile over 0.5-2 Mpc (owner's yes) |
| dSphs, KiDS lenses | NO VERDICT. There is no host-CGM or lens-halo hot-gas measure on disk | none |
| Solar System | 0 (no shocks inside 10 AU) | C6P via GB1 |

## The f table: predicted / needed, with the cell's GB1 status

| Class | footing | V-frac-L | V-frac-S | V-dens-L |
|---|---|---|---|---|
| SPARC (need <= 0.326 / 0.194) | can / alt | 0 PASS / 0 PASS | 0 PASS / 0 PASS | 0 PASS / 0 PASS |
| X-COP (4.18 / 3.78, by calibration) | can | 4.18, **FAIL** (mean +0.031, rms 0.205) | 4.18, **FAIL** (+0.003, rms 0.107: narrow) | 4.18, **FAIL** (+0.120, rms 0.361) |
| | alt | 3.78, **FAIL** (+0.029, 0.200) | 3.78, **FAIL** (+0.003, 0.110: narrow) | 3.78, **FAIL** (+0.111, 0.345) |
| groups f*0 / f*1 (3.46 / 1.23; alt 2.86 / 0.93) | can | 3.50 / 3.50, **FAIL** 0/20, 1/20 | 4.00 / 4.00, **FAIL** 1/20, 0/20 | 20.6 / 10.3, **FAIL** 0/20, 0/20 |
| | alt | 3.17 / 3.17, **FAIL** 0/20, 1/20 | 3.61 / 3.61, **FAIL** 1/20, 0/20 | 18.6 / 9.3, **FAIL** 0/20, 0/20 |
| ellipticals (0.86 / 0.77) | can | 0.44 on 6, NO VERDICT | 2.20 on 6, NO VERDICT | 0.003 on 6, NO VERDICT |
| | alt | 0.40 on 6, NO VERDICT | 1.85 on 6, NO VERDICT | 0.002 on 6, NO VERDICT |
| dSph bright M31 / MW classical (1.68 / 1.82; alt 1.27 / 1.41) | both | NO VERDICT | NO VERDICT | NO VERDICT |
| Coma UDGs (86 / 78) | both | NO VERDICT | NO VERDICT | NO VERDICT |

- In groups, the median residual is near zero for V-frac-L f*0 (+0.033 / +0.016). The groups still fail point by
  point: every group is under-predicted at R2500 (+0.13 to +0.30) and over-predicted at R500 (-0.07 to -0.27). This
  is the radial reversal in the table above.
- V-dens-L puts 5x the X-COP-calibrated f into groups, and essentially nothing into ellipticals or UDGs. A density
  per volume tracks K r^3 / M_b, not the need.
- Reported, not graded (G4 on the 6 ellipticals with a proxy; line 0.15; plain law +0.232 / +0.210):

  | | canonical | alt | with QX26 IMF (can / alt) |
  |---|---|---|---|
  | V-frac-L | +0.113 | +0.103 | +0.026 / +0.016 |
  | V-frac-S | -0.166 | -0.139 | -0.211 / -0.188 |
  | V-dens-L | +0.231 | +0.209 | +0.117 / +0.097 |

- Reported, not graded (Coma UDGs, sigma needed at the frozen constant for f = 86 / 78):

  | | sigma needed (keV cm^2) | n_e implied at kT 8.6 keV |
  |---|---|---|
  | V-frac-L | 8.9e3 | <= 3.0e-5 cm^-3 |
  | V-dens-L | 1.4e5 | <= 4.8e-7 cm^-3 |
  | V-frac-S | about 1e38 | unreachable for any finite K |

  X-COP's graded K reaches only 1456. A Coma n_e profile would decide V-frac-L. A value above about 3e-5 cm^-3 at
  the UDGs' 0.5-2 Mpc would FAIL it.

## GB1 rows (all three variants share G1, G8 and the NO VERDICT rows)

| Row | canonical | alt |
|---|---|---|
| G1 SPARC | PASS Z +0.0274, rms 0.1357 (line 0.1457) = L0 | PASS -0.0006, 0.1325 (0.1425) |
| G2 X-COP | FAIL (above) | FAIL |
| G3 groups | FAIL (above) | FAIL |
| G4 ellipticals | NO VERDICT (NGC 6482 has no proxy; no bracket) | NO VERDICT |
| G5 Coma UDGs | NO VERDICT (no Coma n_e on disk) | NO VERDICT |
| G6 dSph classes | NO VERDICT (no CGM measure) | NO VERDICT |
| G7 KiDS split | NO VERDICT (no lens-halo hot-gas measure) | NO VERDICT |
| G8 Solar System | PASS: worst planet 0.211, Cassini 2.8e-8 (= L0) | PASS 0.190, 2.0e-8 |
| G9 CMB | FAIL, carried: sigma = 0 before shocks, so this is the QX15 baryons-only control (+1.7e5) | FAIL, carried |

Reported: for V-dens-L, the ambient sigma that would put the ephemeris bound of 1e-10 Msun inside 1 AU is 7.5e11
(canonical) and 8.3e11 (alt) keV cm^2. That is far above any plasma, so it is harmless.

## Known answers and MUTATE

- KA1, constant 0 against gb1.json L0 on G1-G8: max |d| 0, statuses equal, both footings: PASS. The L0 class means
  match QX20's KA dict: 4.3e-7 / 4.5e-7 (line 1e-6): PASS.
- KA2, M_gas rebuilt from the derived density: max relative difference 5.0e-4 (line 1e-2): PASS.
- KA3, proxies: only NGC 6482 is missing; the groups and X-COP are all finite: PASS.
- **MUTATE: sigma replaced by the present temperature kT, constant re-fixed the same way.**
  - It BITES. Every variant FAILS G3 on both footings, and V-dens-L also fails G2.
  - It does NOT separate. No row passes for the main field and fails for the twin.
  - The difference runs the other way (reported; a post-freeze reporting addition). The present-temperature twin
    PASSES X-COP for V-frac-L (rms 0.089 / 0.089) and V-frac-S (0.081 / 0.083), where the shock-entropy field fails.
  - The reason: T(r) is nearly flat (7.3 to 4.7 keV over 0.1-0.7 R500), so it follows the falling need better than
    the rising K.
  - So the battery does tell the two keys apart, and the shock record does worse than the dead host-temperature key.
    The temperature twin still fails groups (1-5 of 20).

## Disclosures

1. **No action, only a field equation.** The source is dissipative (entropy production). The energy rho_x gains
   must come from the khronon / dark-energy sector. That exchange is stated, not modelled.
2. **K is a lower bound on sigma** where the cooling time is shorter than the age: cluster and group cores, and
   elliptical atmospheres. Raising the core sigma cannot fix the radial reversal at 0.3-0.7 R500, where cooling is
   slow.
3. **X-COP temperatures are projected spectroscopic values.** The T_SZ reading beyond the X-ray range gives
   identical graded numbers.
4. **Group K uses the global kT at both radii.** A falling T(r) would lower K at R500 by about 0.7x. K would still
   rise outward (n_e falls faster), so the reversal stands.
5. **Elliptical sigma is uniform at its 10-kpc value.** Each galaxy has one measured point. Fukazawa's distances
   are not rescaled to Humphrey's.
6. **The X-COP calibration fixes the mean f, not the mean residual.** The X-COP mean residual is therefore not
   exactly zero (+0.003 to +0.12).
7. **V-dens with form S is undefined.** It would need two constants. Three variants are graded, not four.
8. **Post-freeze additions, reporting only, no label changed.** The within-host need vs proxy table, the reverse
   MUTATE comparison, and the fix for a `'---'` entry in Fukazawa's kT column (a parsing bug, no number moved).
9. **The data the NO VERDICT rows need, which the owner must approve downloading:**
   - a Coma ICM n_e profile;
   - NGC 6482 hot-gas kT and n_e;
   - host-CGM entropy at the dSph satellites;
   - the KiDS lens-halo hot gas.

   Even if every one of these rows passed, the G2 / G3 failures stand.
10. **Bullet-type offsets are argued, not graded.** rho_x rides on the shocked gas, so in a merger it would follow
    the gas, not the galaxies. QX13 reached the same conclusion by argument.

Kappa = 1/2 FITTED; not theory closed.
