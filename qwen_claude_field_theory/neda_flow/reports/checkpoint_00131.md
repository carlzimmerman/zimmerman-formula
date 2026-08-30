# checkpoint 00131

iterations: 131
experiments: 166
failures by gate/stage: {"startup": 2, "architect": 5, "G0": 2, "G8": 1, "G4": 1}
survivors: 6
branch counts: {"constraint-first": 3, "degenerate": 2, "multi-sector": 3, "novel": 3, "spatially-nonlocal": 3}
latest survivors: [
 {
  "candidate_id": "SEED-SCALESPLIT",
  "family": "spatially-nonlocal",
  "name": "scale-split two-auxiliary localized F+ (A=I, M=m^2 diag(0,1))",
  "ref": "closure_2026/scale_split_door/",
  "status": "CLOSED (DC-012): spectral-healthy but UNDER-LENSES (pincer, 0/3 refuted); lensing fix needs a frame = closed khronometric family"
 },
 {
  "candidate_id": "SEED-KHRONO",
  "family": "screened-preferred-frame",
  "gates": {
   "G3(c_T=1)": "PASS",
   "G4(DOF=3)": "PASS",
   "G5(khronon 1<lam_K<=1.10)": "PASS",
   "G6(lensing Psi=Phi boosted)": "PASS",
   "G7(alpha~e^-y)": "PASS-structural",
   "G8(Lambda_sc as eta->0)": "OPEN-MAKE-OR-BREAK",
   "G9-G12": "OPEN"
  },
  "name": "khronometric/Horava + MOND, e^-y self-screened",
  "ref": "theory_discovery/KHRONOMETRIC_MOND_GAUNTLET.md 3ebd8132",
  "status": "CLOSED (KM-X1 + door1 + FM-000004): finite-alpha_inf killed by GW170817+plateau; screened-alpha->0 killed by P7"
 },
 {
  "candidate_id": "SEED-NONLOCAL",
  "family": "spatially-nonlocal",
  "gates": {
   "G4-G7": "OPEN",
   "MOND/BTFR/spherical-lensing": "PASS",
   "c_T(TT quad)": "PASS"
  },
  "name": "nonlocal DEFW/F+ pure-metric",
  "ref": "mond_compiler_2026/FROZEN_PRIMITIVE.md",
  "status": "OPEN (localization untested)",
  "warning": "prior localization found omega^2=(1/2)c^2k^2 extra mode"
 }
]
