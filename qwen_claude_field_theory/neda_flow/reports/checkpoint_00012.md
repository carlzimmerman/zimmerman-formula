# checkpoint 00012

iterations: 12
experiments: 14
failures by gate/stage: {"startup": 2, "architect": 3}
survivors: 2
branch counts: {"novel": 1}
latest survivors: [
 {
  "candidate_id": "SEED-KHRONO",
  "name": "khronometric/Horava + MOND, e^-y self-screened",
  "family": "screened-preferred-frame",
  "status": "CONDITIONAL (NOT viable)",
  "gates": {
   "G3(c_T=1)": "PASS",
   "G6(lensing Psi=Phi boosted)": "PASS",
   "G7(alpha~e^-y)": "PASS-structural",
   "G5(khronon 1<lam_K<=1.10)": "PASS",
   "G4(DOF=3)": "PASS",
   "G8(Lambda_sc as eta->0)": "OPEN-MAKE-OR-BREAK",
   "G9-G12": "OPEN"
  },
  "ref": "theory_discovery/KHRONOMETRIC_MOND_GAUNTLET.md 3ebd8132"
 },
 {
  "candidate_id": "SEED-NONLOCAL",
  "name": "nonlocal DEFW/F+ pure-metric",
  "family": "spatially-nonlocal",
  "status": "OPEN (localization untested)",
  "gates": {
   "MOND/BTFR/spherical-lensing": "PASS",
   "c_T(TT quad)": "PASS",
   "G4-G7": "OPEN"
  },
  "warning": "prior localization found omega^2=(1/2)c^2k^2 extra mode",
  "ref": "mond_compiler_2026/FROZEN_PRIMITIVE.md"
 }
]
