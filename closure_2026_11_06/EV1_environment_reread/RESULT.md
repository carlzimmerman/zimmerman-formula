# EV1: environment, re-read, does NOT carry the step between discs and hot systems

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. No dark-matter particle. Both footings, never pooled.
- Criteria: FROZEN_CRITERIA.md (71bbb66c0d), committed alone before any script.
- Readings: ev1_readings.py -> readings.json (4aa33b53ce), committed before the grader existed.
- Grader: ev1.py -> ev1.json / ev1.out; ev1.py --mutate -> ev1_MUTATE.*. One thread, under 1 GB, seconds.
  A rerun gives a byte-identical ev1.json. Nothing was downloaded.

## Label: NO

No environment key passes the static gates on either footing. Each measure fails at least two rows that have power, and
each of those fails survives the hard check in section 6.

The within-class tests show why. Where environment changes and class does not, the offsets do not follow the
environment:
- SPARC Ursa Major members show no step;
- NGC 720 is isolated and carries the largest elliptical offset;
- KiDS isolated lenses still split.

Where environment and class change together (satellites against LG field dwarfs, Coma UDGs), the switch is
consistent. But that is the class split itself, and the amplitude it needs differs by class: about 1.6x the phantom
for satellites, 4-46x for Coma UDGs, and more than 100x for clusters (no F_env in [1, 100] passes X-COP).

## The keys

Key form, the same for all three measures: g = g_N + F_S (g_law - g_N). F_S = F_env where the switch S = 1, and 1
elsewhere. F_env is fixed on the graded satellites (MW classical + bright M31, 33 systems), so that their median
residual equals the SPARC anchor.

| Measure (switch S = 1 when ...) | F_env canonical / alt | Readings (canonical; alt identical in S) |
|---|---|---|
| M1 external field: x_e >= QX24's x_c (0.0447 / 0.0406), noclu | 1.639 / 1.589 | SPARC 0/175, ellipticals 0/7, satellites 26/33, LG field 0/13, Coma 9/9, Sun 1 (x_e 2.2); X-COP and groups None |
| M2 host membership | 1.690 / 1.637 | SPARC 28 UMa (26 in GB1's sample), ellipticals 2/7 (Virgo pair), satellites 33/33, LG field 0, Coma 9/9, Sun 1; X-COP, groups and KiDS 0 |
| M3 hot atmosphere, own or host's | 1.639 / 1.589 | X-COP, groups and ellipticals 1; satellites 30/33 (d_host <= 300 kpc); LG field 0; Coma 9/9; Sun 1; SPARC 0; KiDS None |

M1 and M3 give the same F_env. The median satellite is the same switched-on system in both, so the calibration lands
on the same root (calib_check in ev1.json).

## Measure x gate x footing (canonical / alt)

| Row | M1 external field | M2 membership | M3 hot atmosphere |
|---|---|---|---|
| G1 SPARC (Z, rms; line 0.1457 / 0.1425) | PASS +0.027, 0.136 / PASS -0.001, 0.133 | PASS +0.012, 0.144 / **FAIL** -0.016, 0.1438 (fragile, 0.0013 over) | PASS +0.027, 0.136 / PASS -0.001, 0.133 |
| G2 X-COP (mean, rms) | NV, bracket FAIL all (S=1: +0.315 / +0.288) | FAIL +0.468 / +0.435 | FAIL +0.315, 0.330 / +0.288, 0.304 |
| G3 groups (pass f*0, f*1 of 20) | NV, bracket FAIL all (S=1: 0, 3 / 1, 3) | FAIL 0, 0 / 0, 0 | FAIL 0, 3 / 1, 3 |
| G4 ellipticals (mean; line 0.15) | FAIL +0.210 / +0.189 | FAIL +0.185 / +0.164 | PASS +0.123 / +0.103 |
| G5 Coma UDGs | FAIL +0.920 (+3.51 sigma_U) / +0.889 (+3.39) | FAIL +0.908 (+3.46) / +0.876 (+3.34) | FAIL +0.920 (+3.51) / +0.889 (+3.39) |
| G6 dSph (bright M31 / MW classical / LG field, minus anchor) | PASS +0.000 / +0.028 / +0.019; alt +0.000 / +0.029 / +0.007 | PASS +0.000 / +0.032 / +0.035; alt PASS | PASS +0.000 / +0.028 / +0.019; alt PASS |
| G7 KiDS isolated split (R, line 2 sigma) | FAIL +0.158 (2.46 sigma) / same | FAIL +0.158 (2.46 sigma) / same | NV; bracket MIXED (early own halo on: R -0.040 / -0.029, PASS; otherwise 2.46 sigma) |
| G8 Solar System (worst use) | PASS 0.347 / 0.302 | PASS 0.357 / 0.311 | PASS 0.347 / 0.302 |
| W1 SPARC UMa vs field | key predicts 0: not tested | P +0.142 / +0.138 vs d -0.024 +- 0.064: NO VERDICT (2.6 sigma off) | key predicts 0: not tested |
| **Key label** | **FAIL (G4, G5, G7); NV (G2, G3)** | **FAIL (G1 alt, G2, G3, G4, G5, G7)** | **FAIL (G2, G3, G5); NV (G7)** |

G9 (CMB lensing, growth) is NOT EVALUATED, as in GB1.

The G6 satellite cells pass by construction, because F_env is calibrated on them. G6 tests only the LG field cell and the
split between MW classical and bright M31.

## Known answers and controls (all PASS)

- KA1: GB1's L0 rows, recomputed through gb1.py's own loaders and gates, match gb1.json to max |d| 0 on both footings.
- KA2: QX24's Delta_s (+0.199267 / +0.187893) and x_c (0.044695 / 0.040560) match to 0. The seven ellipticals' x_e,
  recomputed with the estimator on both readings, also match to 0 relative.
- KA3: every key at F_env = 1 reproduces L0 exactly on its gradable rows.
- MUTATE (switches inverted, calibrated F_env kept): every key FAILS G1 and G6 on both footings, so the battery bites.
  For example, M2 inverted gives SPARC Z -0.092 / -0.116 and bright M31 +0.318 [+0.198, +0.512].

## Switch reading, row by row (independent of amplitude)

| Contrast | What a switch needs | Observed | Verdict |
|---|---|---|---|
| **W1: SPARC Ursa Major (26) vs field SPARC (119)**, the test with power | Members raised by about +0.14 (M2) | d = -0.024 +- 0.064 (bootstrap 0.023; UMa distance error 0.060 dominates). Key-free: **NO STEP** | Against membership. UMa is a spiral group with no X-ray gas (no MCXC entry), so M1 and M3 do not switch it on and are not tested |
| G6: satellites vs LG field dwarfs | Satellites raised, field dwarfs on the law | Bright M31 +0.20 above the field (GB1 L0); the field cell sits at +0.02 under every key | Consistent with the switch, but this is the class split itself |
| G4: NGC 720 (most isolated, x_e 2e-4) vs the Virgo pair | Isolated on the law | NGC 720 residual +0.51 / +0.48 under M1 and M2 (switch off), +0.39 / +0.37 under M3. NGC 4472 +0.27 / NGC 4649 +0.41 (M1) | Against M1 and M2. M3 switches NGC 720 on only because it has its own hot halo |
| G7: KiDS isolated early vs late | No split if isolation switches off | +0.158 +- 0.064 (2.46 sigma, below 3) | Weakly against M1 and M2; M3 is compatible only on the reading that early-type lenses have their own hot halos |
| W3: field UDG AGC 114905 vs Coma UDGs | Field UDG on the law | AGC 114905 sits below the law, x_e about 1e-3 a0 (QX14); a switch that turns on can never lower it | Coma is switched on under every key but needs F 4-46, against 1.6. AGC 114905 stays unexplained (QX4/QX14) |

Taken together:
- External field (M1) and membership (M2) fail the within-class tests where they have power.
- Hot atmosphere (M3) is the one reading whose on/off pattern follows the hot/disc split. That is because it marks
  dispersion-supported, X-ray-bright systems: it is close to a class label and to the dead host-temperature key.
- Even M3 fails clusters, groups and the Coma UDGs on amplitude. One switch with one amplitude cannot carry the step.

## Section 6: the FAILs, checked as hard as a PASS

| FAIL | At F_env = 1 (plain law) / bracket | Could any F_env in [1, 100] pass it (others' S kept)? | maxclu (M1) | Robust? |
|---|---|---|---|---|
| G2 X-COP, G3 groups (all keys) | +0.468 / +0.435; groups 0 of 20 | no, for every key | still NV, bracket FAIL | yes |
| G4 ellipticals M1 | +0.210 | no (all 7 switched off) | Virgo pair switches on, mean +0.187 / +0.165, still FAIL | yes |
| G4 ellipticals M2 | +0.210 | yes at F >= 3.2 / 2.2, which is 1.9x / 1.3x the satellite amplitude | n/a | yes at the frozen amplitude |
| G5 Coma UDGs (all keys) | +1.121 / +1.078 | yes, only at F 4.6-46 / 3.8-38 | same | yes: the switch is on, the amplitude is 3-30x short |
| G7 KiDS (M1, M2) | +0.158, 2.46 sigma | no (isolated lenses are off) | same | a consistency-line fail (2 sigma), not a 3 sigma detection |
| G1 SPARC M2 alt | rms 0.1438 vs 0.1425 | yes at F <= 1.47 | n/a | **fragile** (canonical passes); M2 fails 5 other rows anyway |

The M1 maxclu reading (reported, recalibrated by the same rule: F_env 1.640 / 1.590) switches on 6 SPARC points and
the Virgo pair. Its row statuses match the graded noclu reading exactly. QX24's T2 fragility does not carry into GB1:
on G4 the Virgo pair moves the class mean by only 0.02.

## What it would have meant physically if the answer were yes

- **M1 (external field):** the phantom would be amplified, not screened, by an ambient field. That is the opposite sign
  to the standard EFE, and it would have needed a non-local coupling to the host's potential gradient.
- **M2 (membership):** a host-bound process, such as tidal heating or a host-supplied component, captured by bound
  orbits only.
- **M3 (hot atmosphere):** the extra gravity would be tied to immersion in hot, pressure-supported gas. It would point
  to a coupling to the hot baryons (their pressure or temperature) rather than to environment as such.

Neither answer is given here. EV1 shows that none of the three readings carries the step with one amplitude, and that
the within-class environment contrasts (UMa, NGC 720, KiDS isolated) go against M1 and M2.

## Disclosed

1. Known before the freeze, as stated in the criteria: QX24's per-elliptical numbers, GB1's L0 table, Virgo membership of
   NGC 4472 and NGC 4649, SPARC below x_c on noclu, and KiDS isolation. SPARC UMa offsets were unseen.
2. MCXC self-exclusion was implemented as "an entry centred within 50 kpc is the system's own". NGC 1407 sits 0.00 Mpc
   from RXCJ0340.1-1835 and NGC 6482 0.01 Mpc from RXC J1751.7+2304. This puts the frozen rule into code; it is not a
   new rule.
3. Literature facts, not read from files: the MW and M31 coronae (M3 satellites, Sun); UMa having no X-ray
   intragroup gas (an inference from its absence in MCXC); four elliptical positions inherited from QX24.
4. W1's 0.060 dex UMa distance error is the full sensitivity. g_bar does not depend on D and g_obs scales as 1/D, so the
   offset shifts by -log10(D'/D) in every regime. "Conservative" in the criteria was a misnomer; the number is the
   correct one. On the bootstrap alone (0.023), M2's prediction would sit 7 sigma off. That reading is reported, not
   graded.
5. M3 is close to a class label (X-ray selection marks hot systems), and SPARC discs' own coronae are set to 0 because no
   per-galaxy catalogue is on disk. The reported Vflat >= 200 km/s bracket is stored in readings.json but was not
   graded.

Kappa = 1/2 FITTED; not theory closed.
