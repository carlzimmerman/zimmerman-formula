# CLASH cluster-core residual TARGET (Famaey-Pizzuti-Saltas 2025) on the framework's footing (2026-06-19)

*Topic "clash_target". Pulls the PRECISE FPS CLASH-lensing residual (arXiv:2410.02612, PRD 111 2025),
expresses it as the target profile M_res(<r) any relativistic MOND must supply at a CLASH cluster, and
checks it against the banked eRASS1-Xray cored target. Code: `clash_target_profile.py` (run reproduces
every number). Both ways; quarantine held (a0/Z never asserted derived).*

## HEADLINE (both ways)
The CLASH-lensing residual (FPS 2025) and the eRASS1-Xray residual (banked) are the **SAME cored object
from two INDEPENDENT probes**. At a matched mass (RXJ1347 ~1e15 = the eRASS1-rich bin), CLASH-lensing
**M_res(<420 kpc)=2.37e14 Msun vs eRASS1-Xray 2.30e14 (ratio 1.03)** — they agree to ~3% in the core. Both
are cored (gamma=0), gas-tracking, ~420-430 kpc cutoff, missing/gas ~10, remarkably uniform. The only
gap is the **R500-integrated magnitude: CLASH/eRASS1 ~1.6x** = the known WL(lensing)-vs-HSE(Xray) mass-scale
gap (the banked eta bracket [~1.0 HSE, ~2.33 WL]). It is a **SHARED undershoot of the relativistic-MOND
family** — AeST drops BELOW MOND at low acceleration (same sign, Durakovic-Skordis), and the framework's
dS-Unruh nu is the LOWEST of the three interpolations, so its undershoot is MARGINALLY the WORST, NOT
better than AeST. There is NO framework-distinctive MI cored-profile edge at the CLASH target.

## (a) THE FPS CLASH TARGET (precise, read from the paper)
- 16 CLASH clusters, mostly relaxed, kT=5.9-15.5 keV. Strong+weak-lensing shear + magnification
  (Umetsu+2016). Observable = M_lensGR(r) from (Phi-Psi); residual dM(r)=M_MOND(r)-M_gas-M_*-M_BCG (Eq.13).
- a0 ~= 1e-10 m/s^2 (FPS), simple Q' (Eq.8).
- **CORED**: generic alpha-beta-gamma fit (Eq.15) gives <gamma>=0.015 (geom-mean <1e-3) -> constant-density
  core. **Outer slope steeper than -3.5**, BIC-preferred beta=6.
- **Dark-mass-follows-gas (Eq.17)**: rho_dM = eta*rho_gas*exp(-lambda r/r0), weighted means
  **<log10 eta>=0.93 (eta=8.5, "missing/gas ~10")**, **<r0/lambda>=0.43 Mpc = 430 kpc** exp cutoff.
- **Remarkable UNIFORMITY** of eta and cutoff across all 16 clusters (flat in M_gas and kT, Fig.4).
- FPS note: an a0-RESCALE is NOT equivalent (it would tie dM to TOTAL baryons incl. BCG; data tie dM to
  the GAS alone). [Bears on MI-vs-MG: a depth-of-well a0(r) reading is disfavored by the gas-tracking.]

## (b) THE TARGET PROFILE M_res(<r) [Msun] on the framework's footing
From the FPS Table-I generic cored profile rho_dM=rho_s/(1+r/rs)^beta (g=0, a=1), used DIRECTLY (the
core-integrated M_res is robust to the outer slope to ~15%; beta=6 BIC-preferred shown):

| r [kpc] | A209 (kT=7.3, ~few e14) | RXJ1347 (kT=15.5, ~1e15) |
|---|---|---|
| 140 | 1.25e13 | 2.70e13 |
| 280 | 5.16e13 | 1.18e14 |
| **420 (CORE)** | **9.9e13** | **2.37e14** |
| 700 | 1.83e14 | 4.60e14 |
| 1000 | 2.44e14 | 6.37e14 |
| 1300 | 2.83e14 | 7.57e14 |
| total (r->inf) | 3.74e14 | 1.06e15 |

(A209 total 3.74e14 vs FPS Table-II dM=2.88e14, RXJ1347 1.06e15 vs 7.71e14 — the ~1.3x offset is integrate-
to-inf vs FPS's truncation at the turnaround r0; expected direction/size, so the reconstruction is faithful.)
Framework footing surcharge for a0=9.36e-11 + dS-Unruh nu vs FPS a0=1e-10 + simple: a few-to-~13% magnitude
shift (the same one banked for eRASS1), does NOT change the cored shape or the order of M_res.

## (c) CLASH-lensing vs eRASS1-Xray — DO THEY AGREE? YES (matched mass)
| region | eRASS1 Xray (banked, rich 1e15) | CLASH RXJ1347 (b6, ~1e15) | ratio |
|---|---|---|---|
| M_res(<140 kpc) | 5.4e13 | 2.7e13 | 0.50 |
| **M_res(<420 kpc CORE)** | **2.30e14** | **2.37e14** | **1.03** |
| M_res(<700 kpc) | 3.7e14 | 4.6e14 | 1.24 |
| M_res(<1400 kpc=R500) | 4.8e14 | 7.9e14 | 1.64 |

- Core scale: eRASS1 ~420 kpc vs CLASH cutoff 430 kpc / rs(b6) 0.72-0.81 Mpc -> MATCH
- Missing/gas: eRASS1 6-10 vs CLASH eta~8.5 -> MATCH. Shape: both cored + sharp outer slope -> MATCH.
- Uniformity: eRASS1 eta(R500)=2.33 (intrinsic 0.04 dex) vs CLASH "remarkably uniform" -> MATCH.
- The R500 ~1.6x offset = WL-vs-HSE mass-scale gap [Li+2024 ~110%] = the banked eta(R500) bracket. The two
  probes measure the SAME cored residual at the core; they diverge at R500 by exactly the known systematic.

## (d) BOTH WAYS — is there an MI edge? NO (shared undershoot), at full weight
- The framework (MI / dS-Unruh) and AeST (MG / phantom source) share the deep-MOND lensing phantom: all
  three interpolations (dS-Unruh, AeST totally-screened Eq.2.9, FPS simple) -> the SAME g_obs=sqrt(gN*a0)
  asymptote; they differ only ~6-18% in the transition (gN/a0~0.02-0.04 at cluster cores).
- AeST does NOT do better: Durakovic-Skordis show the AeST RAR has a transient PEAK above MOND, then DROPS
  BELOW MOND at low accel ("as if negative mass density") — same-signed undershoot at deep-MOND cores.
- The framework's dS-Unruh nu is the LOWEST interpolation of the three -> for a given lensing it needs the
  MOST extra mass -> its cored undershoot is MARGINALLY the WORST, NOT an edge. No framework-distinctive MI
  cored-profile difference at the CLASH target.
- Consistent with the banked CLUSTER_RESIDUAL_CLOSURE: the MI-dynamic route supplies NEGLIGIBLE mean residual;
  the only framework-distinctive cluster product is the non-adiabatic relational sigma-SPREAD (a TEST, not a
  closure, and not a lensing observable). The CLASH cored residual is a shared MOND-family target.

## ONE LINE
FPS's CLASH-lensing cored residual = eRASS1's X-ray cored residual (same shape, ~420-430 kpc cutoff,
missing/gas~10, uniform, ~2.3e14 Msun inside ~420 kpc at matched M500~1e15, ratio 1.03); it is a SHARED
relativistic-MOND undershoot, on which the framework's MI has no edge over AeST's MG (if anything its lower
nu makes it marginally worse). Quarantine held; no manufactured MI edge, no reflexive dismissal.
