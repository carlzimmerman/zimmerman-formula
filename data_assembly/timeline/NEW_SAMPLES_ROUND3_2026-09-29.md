# Hunt round 3 (data front, 2026-09-29): new samples found

Method: web searches plus arXiv HTML pages read through a summariser, no downloads. Everything is UNVERIFIED beyond the pages read. Four rows appended to `sample_ledger.csv` (now 42 samples).

## Worth attention
**NOEMA3D** (Jolly+2026, arXiv:2604.18503 and arXiv:2604.18504): 10 massive main-sequence galaxies at z = 1.12-1.63, from the PHIBSS extension (8 in GOODS-N, 2 in the Extended Groth Strip; names G4_/GN4_ in paper 1's sample table).
- Resolved CO(4-3)/(3-2) rotation curves, 0.47 arcsec, mean extent 2.74 R_e, one curve per galaxy (Fig. 6, figure only).
- Table 3 (paper 1): Vc at R_e 197-379 km/s, baryonic mass log 10.68-11.52, f_DM(R_e) 0.04-0.55.
- Paper 2: three independent gas masses per galaxy (CO with alpha_CO 4.36, dust, [CI] with alpha 18.7) and resolved dust/CO/[CI] radial profiles (figures only). Stellar masses log 10.45-11.43.
- Why it matters: it is the only public sample found with resolved CO curves, measured CO gas and SED stellar masses together. It is not the KURVS or ALPAKA objects (overlap not stated in the pages read).
- Caveat: the f_DM values say these are baryon-dominated within R_e, so the acceleration at R_e is probably high, not the low-acceleration regime. R_e was not read, so no g was computed. The outer radii (to about 2.7 R_e) are the useful part.
- To use it: read Tables 1 and 3 by code from the arXiv HTML (no download); digitising Fig. 6 needs the source PDF, which needs the owner's go.

## Filled or checked, lower value
- FUDS0 BTFR (arXiv:2608.04371): 74 HI galaxies to z = 0.40 (24 high-quality to z = 0.15), global line widths, no BTFR evolution (slope 3.32, scatter 0.036 dex). Fills the z 0.1-0.4 gap with HI, but line-width based, and the molecular part is a formula, not measured.
- ALPINE z ~ 4.5 multi-tracer (arXiv:2609.03166): three galaxies, six gas tracers compared; a gas-mass systematic test, not a rotation sample.
- Already in the repo, no action: RC100/Genzel+2020, MSA-3D, ALPAKA, MUSE-DARK, KURVS, PHIBSS2.

## Still open
- The KMOS3D x PHIBSS/NOEMA3D overlap (do any NOEMA3D galaxies appear in KMOS3D, RC100 or SINS?) is not checked.
