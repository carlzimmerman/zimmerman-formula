# checkpoint 33000

iterations: 33000
experiments: 66402
failures by gate/stage: {"startup": 6, "architect": 5, "G0": 75, "G8": 1, "G4": 1, "G6": 6}
survivors: 9
branch counts: {"aleatoric": 99, "constraint-first": 3, "degenerate": 2, "multi-sector": 3, "novel": 3, "spatially-nonlocal": 3}
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
  "candidate_id": "DOOR-MBMMG2",
  "family": "single-metric constraint-first (slip-repaired)",
  "name": "MB-MMG-2: slip-constrained MMG (D^2 s=0, s=(Phi-Psi)/c^2; C_M kept)",
  "gates": {
   "Gate1_rank": "PLAUSIBLE-PASS (Pf=Lc-k^2 b, rank-4 generic, N_grav=2)",
   "Gate2_slip": "PASS (gamma 0->1)",
   "Gate3_MOND": "PASS",
   "alpha_1": "repaired 4->0",
   "alpha_3": "FAIL -3 O(1), pulsar 7.5e19x"
  },
  "ref": "closure_2026/bimetric_secondfield/mb_mmg2_gate1_and_pincer.py",
  "status": "PRICED-DOWN (DC-019): fixes slip+alpha_1, plausibly 2-DOF, but alpha_3=O(1) survives (C_M elliptic/instantaneous). Not viable single-metric; folds into the pincer's HORN 2.",
  "warning": "slip repair is real but alpha_3 excludes it; do not freeze as viable"
 }
]
