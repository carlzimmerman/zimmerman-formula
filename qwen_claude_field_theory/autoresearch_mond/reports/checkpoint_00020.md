# checkpoint 00020

iterations: 20
experiments: 29
failures by gate/stage: {"startup": 2, "architect": 4, "G0": 1, "G8": 1}
survivors: 5
branch counts: {"constraint-first": 1, "novel": 2}
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
  "candidate_id": "FM-000001",
  "family": "spatially-nonlocal",
  "gates_machine_passed": [
   "G0",
   "G1",
   "G2",
   "G3"
  ],
  "iter": 0,
  "name": "Nonlocal-Kinetic Screened-Frame Decoupling",
  "status": "SURVIVOR_PENDING_AUDIT",
  "ts": 1788088682.2414348
 },
 {
  "candidate_id": "FM-000004",
  "family": "spatially-nonlocal",
  "gates_machine_passed": [
   "G0",
   "G1",
   "G2",
   "G3"
  ],
  "iter": 0,
  "name": "Spatially Nonlocal F+ Screened Preferred-Frame with Decoupled Propagator",
  "status": "SURVIVOR_PENDING_AUDIT",
  "ts": 1788088682.242074
 }
]
