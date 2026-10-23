# v3 sealed Gaia DR4 Milky Way predictions (lane S3_v3_mw_seals)

- **Sealed object:** `SEALED_V3_MW_DR4.json`, SHA-256 `15b7e6ffb0a340248e111d83a4dd214492f0f2e3b2294e5ff23d6542da3b6160` (`PREDICTIONS_V3_HASH.txt`). Committed before the DR4 release (2026-12-02).
  Never edit either file after the seal; any change goes into a new, dated file. This is NOT CFG553 (the record's old-model set, untouched).
- **Theory:** v3 static limit: AQUAL div[mu(|grad Phi|/a0) grad Phi] = 4 pi G rho_b, mu = x/(1+x); EFE; screening l_g << 1 pc (unscreened); mu_K^2 term not included (batch R6).
- **Inputs:** McMillan 2017 Table 3 (CFG514 transcription), stars x s, gas held; s band 0.89503, 0.94751, 1.00000, 1.05249, 1.10497; e_N (h81, ΛCDM-processed) {'alt': 0.01054, 'canonical': 0.01273}; field toward (l, b) = (268.5, 33.0), γ = 57.0°; R0 = 8.122 kpc; 3-D estimator pointwise ratio (AMENDMENT A3) (validated by C5: True).
- **Rules after DR4:** CFG553 FROZEN_CRITERIA.md s4-s5 adopted verbatim: F = the v3 census band (primary: EFE), R = the NFW census band; P6 scored as a scalar per radius with rival 0; footings and variants never pooled.
- κ = ½ FITTED; footings never pooled; no dark-matter particle; predictions, not results; not theory closed.

## Headline (census s = 1; band = min–max over the five s values)

| quantity | footing | v3 (EFE) | v3 isolated | NFW fitted to Ou+24 |
|---|---|---|---|---|
| V_c(20 kpc), anticentre wedge [km/s] | canonical | 196.0 (190.4–201.3) | 196.1 (190.5–201.3) | 207.2 (207.2–207.3) |
| dlnV/dlnR 15–22 kpc | canonical | -0.126 (-0.136–-0.116) | -0.123 (-0.134–-0.112) | -0.171 (-0.176–-0.163) |
| dlnV/dlnR 15–27.5 kpc | canonical | -0.120 (-0.129–-0.111) | -0.115 (-0.124–-0.104) | -0.174 (-0.182–-0.163) |
| K_z(R0, 1.1)/2πG [M☉ pc⁻²] | canonical | 92.3 (86.5–98.0) | 92.5 (86.7–98.2) | 76.3 (72.7–79.9) |
| Σ(|z| < 1.1) true column [M☉ pc⁻²] | canonical | 92.6 (87.4–97.8) | 92.8 (87.6–98.0) | 74.6 (71.3–77.8) |
| ρ_tot(R0, 0) Oort limit [M☉ pc⁻³] | canonical | 0.166 (0.159–0.172) | 0.166 (0.160–0.173) | 0.116 (0.110–0.122) |
| σ_z(R0≈8, 0), h = 0.30 kpc [km/s] | canonical | 19.8 (19.3–20.3) | 19.8 (19.3–20.4) | 17.3 (16.8–17.7) |
| V_c(60 kpc), anticentre wedge / in-plane [km/s] | canonical | 170.9 (166.0–175.6) | 178.2 (174.0–182.2) | 166.6 (163.6–170.6) |
| mean V_c 30–60 kpc [km/s] | canonical | 178.8 (174.0–183.3) | 182.3 (177.9–186.4) | 178.4 (176.3–181.2) |
| V_c(20 kpc), anticentre wedge [km/s] | alt | 203.2 (197.5–208.6) | 203.3 (197.6–208.6) | 207.2 (207.2–207.3) |
| dlnV/dlnR 15–22 kpc | alt | -0.115 (-0.125–-0.105) | -0.112 (-0.122–-0.101) | -0.171 (-0.176–-0.163) |
| dlnV/dlnR 15–27.5 kpc | alt | -0.110 (-0.118–-0.101) | -0.104 (-0.113–-0.094) | -0.174 (-0.182–-0.163) |
| K_z(R0, 1.1)/2πG [M☉ pc⁻²] | alt | 96.8 (90.9–102.7) | 97.0 (91.2–102.9) | 76.3 (72.7–79.9) |
| Σ(|z| < 1.1) true column [M☉ pc⁻²] | alt | 98.0 (92.6–103.3) | 98.2 (92.9–103.5) | 74.6 (71.3–77.8) |
| ρ_tot(R0, 0) Oort limit [M☉ pc⁻³] | alt | 0.174 (0.168–0.181) | 0.175 (0.169–0.181) | 0.116 (0.110–0.122) |
| σ_z(R0≈8, 0), h = 0.30 kpc [km/s] | alt | 20.3 (19.8–20.8) | 20.3 (19.8–20.8) | 17.3 (16.8–17.7) |
| V_c(60 kpc), anticentre wedge / in-plane [km/s] | alt | 178.4 (173.2–183.2) | 186.2 (181.8–190.3) | 166.6 (163.6–170.6) |
| mean V_c 30–60 kpc [km/s] | alt | 186.4 (181.5–191.0) | 190.1 (185.6–194.4) | 178.4 (176.3–181.2) |

Local 'phantom' density at (R0, 0) (dynamical minus baryonic; what a DR4 Jeans analysis would call dark): canonical 2.22 GeV cm⁻³ midplane, 0.25 shell average; alt 2.55 GeV cm⁻³ midplane, 0.28 shell average; NFW 0.338 GeV cm⁻³.

## P6 (new, v3-specific): azimuthal asymmetry of the in-plane V_c from the external field

A = 2(V_max − V_min)/(V_max + V_min) over galactocentric azimuth φ (φ measured from the Sun→GC direction toward l = 90°; the anticentre side is φ = 180°). Isolated v3 predicts A = 0. Rival: 0.

| R [kpc] | A canonical | A alt | φ(V_max), φ(V_min) canonical [deg] |
|---|---|---|---|
| 15 | 0.018 | 0.019 | 110, 270 |
| 20 | 0.030 | 0.031 | 65, 270 |
| 25 | 0.041 | 0.042 | 65, 270 |
| 30 | 0.052 | 0.054 | 100, 270 |
| 40 | 0.071 | 0.072 | 75, 270 |
| 50 | 0.082 | 0.083 | 90, 265 |
| 60 | 0.082 | 0.082 | 75, 270 |

## P2 rotation curve, census (km/s; anticentre wedge for v3)

| R | v3 can | v3 alt | v3 iso can | v3 iso alt | NFW |
|---|---|---|---|---|---|
| 10 | 213.1 | 218.9 | 213.0 | 218.8 | 230.4 |
| 11 | 211.3 | 217.3 | 211.2 | 217.2 | 227.9 |
| 12 | 209.3 | 215.5 | 209.2 | 215.4 | 225.2 |
| 13 | 207.2 | 213.7 | 207.2 | 213.6 | 222.6 |
| 14 | 205.3 | 211.9 | 205.2 | 211.8 | 220.0 |
| 15 | 203.4 | 210.2 | 203.4 | 210.1 | 217.6 |
| 16 | 201.7 | 208.5 | 201.6 | 208.5 | 215.3 |
| 17 | 200.1 | 207.0 | 200.1 | 207.0 | 213.1 |
| 18 | 198.6 | 205.6 | 198.6 | 205.7 | 211.1 |
| 19 | 197.3 | 204.4 | 197.3 | 204.4 | 209.1 |
| 20 | 196.0 | 203.2 | 196.1 | 203.3 | 207.2 |
| 21 | 194.9 | 202.1 | 195.0 | 202.3 | 205.5 |
| 22 | 193.8 | 201.1 | 194.0 | 201.3 | 203.8 |
| 23 | 192.8 | 200.1 | 193.1 | 200.4 | 202.3 |
| 24 | 191.9 | 199.3 | 192.2 | 199.6 | 200.7 |
| 25 | 191.0 | 198.4 | 191.4 | 198.9 | 199.3 |
| 26 | 190.2 | 197.7 | 190.7 | 198.2 | 197.9 |
| 27 | 189.5 | 196.9 | 190.0 | 197.5 | 196.5 |
| 5 | 209.9 | 213.7 | 209.9 | 213.7 | 231.0 |
| 6 | 213.6 | 217.9 | 213.5 | 217.8 | 234.1 |
| 7 | 215.3 | 220.1 | 215.2 | 220.0 | 235.0 |
| 8 | 215.5 | 220.6 | 215.4 | 220.6 | 234.4 |
| 9 | 214.6 | 220.1 | 214.5 | 220.0 | 232.7 |

## P1 K_z/(2πG) [M☉ pc⁻²], census, v3 (EFE; vertical quantities from the exact γ = 0 solve) / NFW

| R | z 0.5 | z 1.1 | z 2.0 |
|---|---|---|---|
| 10 | 46.4 / 48.9 / 33.4 | 59.5 / 62.7 / 46.8 | 69.2 / 73.1 / 59.9 |
| 11 | 37.1 / 39.2 / 25.9 | 47.9 / 50.6 / 36.8 | 56.7 / 60.0 / 48.1 |
| 12 | 30.1 / 31.9 / 20.4 | 39.0 / 41.3 / 29.3 | 46.9 / 49.8 / 39.1 |
| 13 | 24.8 / 26.3 / 16.3 | 32.1 / 34.1 / 23.6 | 39.1 / 41.6 / 32.2 |
| 14 | 20.7 / 22.1 / 13.3 | 26.8 / 28.5 / 19.4 | 33.0 / 35.2 / 26.8 |
| 15 | 17.5 / 18.6 / 10.9 | 22.6 / 24.1 / 16.0 | 28.0 / 29.9 / 22.5 |
| 16 | 15.0 / 16.0 / 9.1 | 19.2 / 20.6 / 13.4 | 24.1 / 25.8 / 19.1 |
| 5 | 170.7 / 177.1 / 145.6 | 206.9 / 214.7 / 188.5 | 212.7 / 221.3 / 209.1 |
| 6 | 128.9 / 134.2 / 106.0 | 158.0 / 164.6 / 139.2 | 167.1 / 174.4 / 159.4 |
| 7 | 98.2 / 102.6 / 78.1 | 122.0 / 127.6 / 104.2 | 132.5 / 138.7 / 122.9 |
| 8 | 75.5 / 79.2 / 58.1 | 95.1 / 99.7 / 78.9 | 105.8 / 111.2 / 95.7 |
| 9 | 58.7 / 61.8 / 43.7 | 74.7 / 78.6 / 60.3 | 85.2 / 89.7 / 75.2 |
(canonical / alt / NFW)

## Required DR4 precision (CFG553 §4 rule; 3σ)

- alt|Kz_R0_1p1: F 96.8 [90.91, 102.7], R 76.27 [72.71, 79.85] → {'sigma_req_F': 5.6500942817093245, 'sigma_req_R': 4.882175954450029}
- alt|V60: F 178.4 [173.2, 183.2], R 166.6 [163.6, 170.6] → {'sigma_req_F': 2.6115679125046447, 'sigma_req_R': 2.2210142677484157}
- alt|mean_30_60: F 186.4 [181.5, 191], R 178.4 [176.3, 181.2] → {'sigma_req_F': 1.7270793300942369, 'sigma_req_R': 1.0248462292875804}
- alt|slope_15_22: F -0.1152 [-0.1245, -0.1048], R -0.1706 [-0.1761, -0.1634] → {'sigma_req_F': 0.016076212272890314, 'sigma_req_R': 0.015368074700235781}
- alt|slope_15_27p5: F -0.1098 [-0.1178, -0.1009], R -0.1737 [-0.1821, -0.1627] → {'sigma_req_F': 0.01764847093778767, 'sigma_req_R': 0.01863143561335102}
- canonical|Kz_R0_1p1: F 92.25 [86.49, 97.99], R 76.27 [72.71, 79.85] → {'sigma_req_F': 4.133217005758969, 'sigma_req_R': 3.40674203059614}
- canonical|V60: F 170.9 [166, 175.6], R 166.6 [163.6, 170.6] → NOT SEPARABLE
- canonical|mean_30_60: F 178.8 [174, 183.3], R 178.4 [176.3, 181.2] → NOT SEPARABLE
- canonical|slope_15_22: F -0.1265 [-0.1363, -0.1156], R -0.1706 [-0.1761, -0.1634] → {'sigma_req_F': 0.012303689124748737, 'sigma_req_R': 0.011444284708120903}
- canonical|slope_15_27p5: F -0.1201 [-0.1285, -0.1107], R -0.1737 [-0.1821, -0.1627] → {'sigma_req_F': 0.014220462032807116, 'sigma_req_R': 0.015063295815321565}

## Variants (census, EFE γ = 0; envelope only)

- alt|B2_6.0e10: V20 198.2 km/s, slope 15–27.5 -0.124, K_z(R0,1.1)/2πG 94.7, V60 171.9
- alt|B2b_7.3e10: V20 210.6 km/s, slope 15–27.5 -0.133, K_z(R0,1.1)/2πG 109.5, V60 183.4
- alt|B3_short_disc: V20 214.5 km/s, slope 15–27.5 -0.123, K_z(R0,1.1)/2πG 101.2, V60 189.7
- canonical|B2_6.0e10: V20 191.1 km/s, slope 15–27.5 -0.134, K_z(R0,1.1)/2πG 90.1, V60 164.7
- canonical|B2b_7.3e10: V20 203.2 km/s, slope 15–27.5 -0.144, K_z(R0,1.1)/2πG 104.5, V60 175.8
- canonical|B3_short_disc: V20 207.2 km/s, slope 15–27.5 -0.134, K_z(R0,1.1)/2πG 96.9, V60 181.8
