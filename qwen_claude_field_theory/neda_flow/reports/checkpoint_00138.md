# checkpoint 00138

iterations: 138
experiments: 239
failures by gate/stage: {"startup": 4, "architect": 5, "G0": 12, "G8": 1, "G4": 1, "G6": 3}
survivors: 8
branch counts: {"aleatoric": 18, "constraint-first": 3, "degenerate": 2, "multi-sector": 3, "novel": 3, "spatially-nonlocal": 3}
latest survivors: [
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
  "candidate_id": "FM-000076",
  "family": "aleatoric",
  "gates_machine_passed": [
   "G0",
   "G1",
   "G2",
   "G3"
  ],
  "iter": 137,
  "name": "ALEATORIC-137006",
  "status": "SURVIVOR_PENDING_AUDIT",
  "ts": 1788114659.189933
 },
 {
  "candidate_id": "FM-000082",
  "family": "aleatoric",
  "gates_machine_passed": [
   "G0",
   "G1",
   "G2",
   "G3"
  ],
  "iter": 138,
  "name": "ALEATORIC-138004",
  "status": "SURVIVOR_PENDING_AUDIT",
  "ts": 1788114727.2722769
 }
]
