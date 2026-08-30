# checkpoint 00100

iterations: 100
experiments: 128
failures by gate/stage: {"startup": 2, "architect": 5, "G0": 2, "G8": 1}
survivors: 6
branch counts: {"constraint-first": 3, "novel": 3, "multi-sector": 1, "degenerate": 2, "spatially-nonlocal": 2}
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
  "candidate_id": "FM-000027",
  "family": "spatially-nonlocal",
  "gates_machine_passed": [
   "G0",
   "G1",
   "G2",
   "G3"
  ],
  "iter": 94,
  "name": "Scale-Split Dual-Operator Nonlocal F+ (SSDNF+)",
  "status": "SURVIVOR_PENDING_AUDIT",
  "ts": 1788105996.209087
 },
 {
  "candidate_id": "FM-000029",
  "family": "constraint-first",
  "gates_machine_passed": [
   "G0",
   "G1",
   "G2",
   "G3"
  ],
  "iter": 95,
  "name": "Dual-Operator Constraint-First MOND (DOC-MOND)",
  "status": "SURVIVOR_PENDING_AUDIT",
  "ts": 1788106149.164403
 }
]
