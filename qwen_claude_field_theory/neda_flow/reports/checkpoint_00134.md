# checkpoint 00134

iterations: 134
experiments: 187
failures by gate/stage: {"startup": 2, "architect": 5, "G0": 2, "G8": 1, "G4": 1, "G6": 1}
survivors: 7
branch counts: {"constraint-first": 3, "degenerate": 2, "multi-sector": 3, "novel": 3, "spatially-nonlocal": 3, "aleatoric": 3}
latest survivors: [
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
 },
 {
  "candidate_id": "FM-000060",
  "family": "aleatoric",
  "gates_machine_passed": [
   "G0",
   "G1",
   "G2",
   "G3"
  ],
  "iter": 134,
  "name": "ALEATORIC-134002",
  "status": "SURVIVOR_PENDING_AUDIT",
  "ts": 1788113600.504687
 }
]
