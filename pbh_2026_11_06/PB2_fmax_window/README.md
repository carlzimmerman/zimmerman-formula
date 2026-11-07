# PB2: the ceiling f_max(M) on primordial black holes, 1e0 - 1e9 Msun. NO WINDOW AT f_b >= 0.2 outside a 316-630 Msun sliver that is a row-edge artifact; the framework moves the robust ceiling by x0.45 to x1.0 (it loosens dynamics, tightens LVK and accretion); DB1's 1e2-1e7 Msun cluster black holes are CLOSED as 20-50 % of the baryons

Criteria `FROZEN_CRITERIA.md` (06450918d1), committed alone before any script or number. Script `pb2_fmax.py` (about 3 s,
small compute), output `pb2_fmax.out`, everything in `pb2_fmax_results.json`. **Exit 1: KA1 fails at 1e3 Msun** (section
"Checks"). Adopts nothing. kappa = 1/2 FITTED; not theory closed. Footings canonical / alt are reported apart and never pooled.
They differ only through nu, and by at most 5 % here. No particle; the cold sector stays retired. Nothing here says the data
favour the framework, or that PBHs exist.

**Units.** f_b = Omega_PBH / Omega_b. To convert: f_DM-equivalent = f_b / 5.364, and f_m = Omega_PBH / Omega_m = f_b / 6.364.
STD is the literature f_DM limit times 5.364, i.e. the same physical Omega_PBH. FW is that row after the computed framework
modifications (no CDM anywhere; the only real mass is baryons plus PBHs).

## Ceiling table: ROBUST envelope, f_b,max (canonical; alt where it differs), with the dominant row
| M (Msun) | STD | FW | FW/STD | dominant (STD -> FW) | AGGRESSIVE STD -> FW | ROBUST without A1 extrapolation, STD -> FW |
|---|---|---|---|---|---|---|
| 1e0 | 0.101 | 0.0996 | 0.98 | G1 LVK (subsolar edge) | same | same |
| 1e1 | 0.0221 | 0.0177 | 0.80 | G1 LVK | same | same |
| 1e2 | 4.15e-3 | 1.85e-3 | 0.45 | G1 LVK | 2.6e-4 (A3 dressed) -> 8.4e-4 (X1) | same |
| 1e3 | 0.0807 | 0.0800 / 0.0798 | 0.99 | A1 CMB accretion (AHK) | 2.6e-7 (A3) -> 0.080 (A1) | same |
| 1e4 | 3.25e-3 | 3.00e-3 / 2.96e-3 | 0.92 | A1 (extrapolated) | 4.5e-8 (A3) -> 3.0e-3 | 0.019 (D2 Eri II) -> 0.69 (D2) |
| 1e5 | 1.12e-3 | 7.4e-4 / 7.1e-4 | 0.66 | A1 (extrapolated) | 2.9e-8 (A3) -> 7.4e-4 | 0.32 (L3 millilensing) -> 0.32 |
| 1e6 | 3.84e-4 | 3.84e-4 | 1 | A1 (extrapolated) | 2.6e-8 (A3) -> 3.8e-4 | 8.6e-3 (D4 DF) -> 7.8e-3 (D4) |
| 1e7 | 1.32e-4 | 1.32e-4 | 1 | A1 (extrapolated) | 2.3e-8 (A3) -> 1.3e-4 | 5.4e-4 (D4) -> 4.9e-4 (D4) |
| 1e8 | 4.5e-5 | 4.5e-5 | 1 | A1 (extrapolated) | 2.0e-8 (A3) -> 4.5e-5 | 5.4e-4 (D4) -> 3.1e-3 (P2) |
| 1e9 | 1.6e-5 | 1.6e-5 | 1 | A1 (extrapolated) | 1.8e-8 (A3) -> 1.6e-5 | 3.1e-4 (P2) -> 3.1e-4 (P2) |
GAUSSIAN envelope (reported only): G2 PTA closes 1 Msun to 3e-9, and S1 mu closes everything >= 1e5 Msun (Gaussian peaks:
"no interesting cosmological role", 1710.06945). Non-Gaussian formation escapes both; that is stated, not scored.

**Labels (FW ROBUST, primary).**
- **X = 1: CLOSED everywhere.**
- **X = 0.2 (DB1's amount):** CLOSED at every decade. Open only for log M in [2.5, 2.8] (316-630 Msun; STD [2.5, 2.7]).
  That sliver is an **edge artifact**: the LVK row's compiled curve ends at 300 Msun, AHK is still rising there, and the
  Segue 1 / Stegmann UFD bounds (f < 0.04 above ~10 Msun, review text) are not in the frozen row list. I do not read it as a window.
- **X = 1e-2:** OPEN at 1e0 to 10^1.2 and at 10^2.4 to 10^3.4; CLOSED elsewhere.
- **X = 1e-4:** OPEN up to 10^7.25; CLOSED at 1e8 and 1e9.
- No label is FRAGILE under the frozen brackets, except alt at X = 1e-4, M = 1e5, which flips at z_ref = 300.

## What the framework changes, row by row (factor FW/STD at the stated masses)
| row | change | factor | why (computed) |
|---|---|---|---|
| D1 wide binaries | LOOSENS | x3.7-4.4 | no CDM halo. PBHs at f_b sit in PB3's spheroid (r_vir 80.8 kpc for 6e10 Msun), rho_NFW / rho_fw1 = 11.4 at 8 kpc, against 5.364. The law binds the binary harder: nu(e_MW) = 1.31 / 1.37, impulse ~Newtonian. |
| D2 Eri II | LOOSENS | x36 | no CDM in the UFD: rho_DM / (eta rho_*) = 194 at eta = 3 (M_dyn 1.24e7) |
| D3 disk heating | LOOSENS | x2.1 (1e9) to x1e4 (low M) | the same density ratio, plus the incredulity of a 6e10 host |
| D4 dynamical friction | ~UNCHANGED at 1e5-1e7 (x0.9-1.05); LOOSENS below; at >= 1e8 it is NO BOUND (fewer than 1 per MW) | | rho_NFW / rho_fw1 = 4.6 at 2 kpc; medium factor sqrt(rho_dyn / (nu rho_real)) = 1.05 / 1.06 |
| L1 LMC microlensing | LOOSENS | x3.6-5.8 | tau_NFW / tau_fw1 = 13 |
| L2 quasar microlensing (C) | LOOSENS | x2.2 | MW 8 kpc proxy |
| X1 X-ray/radio (C) | TIGHTENS | x0.47 | the inner kpc: rho_NFW / rho_fw1 = 2.53 < 5.364 (the SIS spheroid is cuspier than NFW) |
| A1 accretion, naked | TIGHTENS slightly | x0.99 (1e3), x0.92 (1e4), x0.66 / 0.63 (1e5), x1 at >= 1e6 (Eddington cap) | law baryon dressing at z = 600, e = 0.026: E = 1.005, 1.04, 1.23; 2.35-99 at 1e6-1e9, where the cap applies (mdot_N >= 1) |
| A3 CDM-dressed accretion (C) | REMOVED | 1e-7-level ceilings disappear | no CDM halo to dress the PBH. This is the largest framework effect on the AGGRESSIVE envelope (x3e3 to x1e5 looser, 1e2-1e9). |
| G1 LVK | TIGHTENS | x0.98 (1), x0.80 (10), x0.45 (100) | sigma_eq torque from CDM fluctuations is gone (baryons Silk-damped), so primordial binaries are more eccentric and the rate is higher |
| P1 Ly-alpha | LOOSENS | x1.5 (100), x10 (1e3), x64 (1e4) | Newtonian growth without CDM, in the standard H(z). NEWTONIAN-GROWTH CONDITIONAL: the law's own growth is PB1's |
| L3, L4, P2, G2, S1 | UNCHANGED | exactly 1 | cosmological / photon-baryon physics, Omega_PBH-proportional at the standard background |

## Checks
- **KA1 FAILS at 1e3.** The STD robust envelope gives f_DM 0.0151 (AHK) against the recalled reference 1e-3 (x15). At 1e1 it gives
  4.13e-3 against 3e-3 (PASS; page-read "1e-3 to 1e-2" for LVK, 2002.10771 text). At 1e5 it gives 2.09e-4 against 1e-4 (PASS,
  but only through A1's extrapolated anchor).
  - Verified as hard as a pass: no ROBUST row on the list is stronger at 1e3. The review figures' envelope at 1e3 is the
    CDM-dressed CMB curve (contested, 4.8e-8 here). The frozen recalled reference (1e-3) matches neither. The fail is in the
    recalled reference, and KA1 is NOT INDEPENDENT anyway: the rows come from the same compilations the reviews use.
  - Rows missing from the frozen list that would bite near 1e2-1e3: Segue 1 (Koushiappas & Loeb) and Stegmann+ UFDs.
- KA2: no literature CMB-Poisson value located. P2 is derived only: f_DM < 5.7e4 / M.
- KA3 PASS.
- MUTATE PASS on both footings: the M1 planted bound bites; M2 mods-off gives |FW - STD| = 0 exactly; M3 (normalised halo)
  gives relative difference 0.

## Sources and status (every value PROVISIONAL)
- Page-read text of the PBHbounds compilation files (github bradkav/PBHbounds), tracing to:
  - A1: AHK 1612.05644 Fig. 14. Its last anchor (1e10, 1e-6) is the compiler's extrapolation; it drives the ROBUST envelope
    above 3651 Msun.
  - A3: Serpico+ 2002.10771 Fig. 6, spherical with DM halo. The criteria named the disk-dressed curve; only this one was located.
  - X1: Manshanden+ 1812.07967.
  - D1: 1406.5169.
  - D2: Brandt 1605.03665.
  - L1: EROS astro-ph/0607207.
  - L2: 2203.04777.
  - L4: 2204.06001. It gives no bound >= 0.53 Msun.
  - G1: 1805.09034 + 1904.08976.
  - G2: 1910.12239.
  - P1: Murgia 1903.10509 (f M < 60 Msun, abstract page-read).
- Page-read from the Carr+2021 review text (2002.12778):
  - D3 Eq. 78, D4 Eq. 79.
  - L3 Eq. 69. Its extraction is partly garbled; branches read as (M/2e4)^-2, 0.06, (M/4e8)^2.
- Recalled, unverified: P2's beta_iso = 0.04 (Planck 2018), and the MW/Eri II inputs.
- A2 (disk, naked) NOT LOCATED as a curve: only "f = 1 excluded above ~2 Msun" (1707.04206 abstract).

## Disclosures
1. **Transcription fix after the first run.** G1's anchors began at 1.004 Msun, so the 1 Msun grid point had no LVK bound
   (first-run FW ROBUST read 2.17, from L1, and X = 1 was OPEN FRAGILE). The file's own subsolar anchors 0.667 and 0.803 Msun
   were added. 1 Msun now reads 0.0996 (G1), CLOSED at X = 0.2. No other change was made after numbers were seen.
2. **Above 3651 Msun the ROBUST envelope rests on A1's compiler extrapolation.**
   - Without it: 1e4 FW 0.69 (Eri II) and 1e5 FW 0.32 (millilensing) would be OPEN at 0.2, but only in FW (STD 0.019 at 1e4).
   - Naked accretion bounds keep tightening until Eddington (2002.10771), and even a flat continuation at AHK's last value
     (f_DM 9.7e-4, f_b 5.2e-3) closes 1e4-1e5 at 0.2.
   - So the 1e4-1e5 window is not open under any accretion continuation, but that rests on a curve nobody published above 3.7e3.
     Settling it needs the real naked curve at 1e4-1e6.
3. **A_BG.** The standard H(z) is used. A baryon-only background makes H_std/H_bo = 2.11, 1.88, 1.70 at z = 300, 600, 1000,
   which would tighten every accretion row by about that much. The v_bc in a CDM-free universe is not computed.
4. **Incredulity.** The frozen rule (N < 1, so NO BOUND) and the max(f, M/M_host) alternative give the same ROBUST envelope here.
5. The D4 alternative reading (spheroid-star medium, factor 1/sqrt(nu) about 0.97) is reported in the json only.
6. **FW-RAR (reported only, PB3's):** f_b <= 0.86 keeps the MW's outer g within 0.05 dex. It is mass independent.

## For PB1 / PB3 / PB4
- At the DB1 / PB3 amounts (f_b >= 0.2), every decade 1e0-1e9 is CLOSED, on both footings and in both STD and FW.
- Seeds at f_b ~ 1e-4 are allowed up to ~1e7 Msun. At 1e8-1e9 the ceiling is ~1e-5 to 5e-5 (accretion, extrapolated), or
  3e-3 / 3e-4 (P2) without the extrapolation.
- The framework's main effects:
  - It removes the CDM-dressed accretion bounds. The AGGRESSIVE envelope rises from ~1e-8 to the naked level.
  - It loosens every halo-density dynamical bound by 2-40x.
  - It tightens LVK by up to 2.2x.
