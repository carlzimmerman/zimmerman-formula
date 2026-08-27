# MMG_REPAIR_A — S2' = D^2(q + ln N): partial repair, then a MOND-lapse no-go
Verdict: **REPAIRED_PARTIAL → FAILED.** Independently computed (workflow wf_5ca09aa1), not relayed.

## What S2' fixes (PASS)
- **Lensing / gamma_PPN (39/39, commit d296d440):** S2'=0 makes u=q+lnN harmonic; bounded+harmonic
  => u=const=gauge => q=-lnN exactly => gamma_ij=N^{-2}delta_ij => **Phi=Psi at ALL accelerations,
  gamma_PPN=1**, kernel- and footing-blind. The factor-of-two lensing kill of the baseline is gone.
  C_M untouched => Psi is exact AQUAL. Cassini gamma PASS (0.91 sigma).
- **alpha_1: +4 -> 0 (PASS)**, alpha_2 = 0.
- **Dirac rank SURVIVES:** new entry E={pi_N,S2'}=-D^2(1/N) => Pfaffian = L_N K - E c_M, still
  second-class generic (rank 4, k!=0). => the "lensing restoration => scalar restoration" duality
  is **REFUTED**: restoring Phi does NOT reintroduce the scalar. 2-DOF count holds.

## What kills it — TWO independent obstructions in the untouched C_M sector
1. **alpha_3 = -3 (FAIL, 26/26, gateA_fork_ppn):** the Phi_1 coefficient in g_00 is fixed = 1 by
   C_M's instantaneous elliptic response, vs GR's 4; S2' does not touch it. Forcing gamma=1 makes
   the mismatch WORSE: baseline -1 -> **-3** = 7.5e19x the 4e-20 pulsar bound. (OpenAI's -3 CONFIRMED
   by independent run; the audit's -1 value refuted.) Also zeta_2=-1-xi (pulsar Pdot ~5e4x).
2. **Deep-MOND law DESTROYED (FAIL, commit bc0b416e) — new, OpenAI did not have this:** q=-lnN
   revives R^(3)=4 D^2 Psi/c^2, flipping the phantom source: r_4 = +(c^2/4piG)D.[(1-mu)D Psi]
   = +c^2 rho_phantom (was -). Matter conservation is repaired at 1 AU but the deep-MOND floor
   becomes **repulsive (+a0/2)**: v^4=GMa0 / BTFR KILLED.

## Structural lesson (the theorem)
S2' cleanly separates the two sectors: the METRIC constraint sets lensing (repairable => gamma=1),
the MOND LAPSE constraint C_M sets the momentum/PPN sector AND the phantom-source sign (NOT
repairable by any metric-sector edit). **Restoring Phi=Psi does not restore the MOND momentum
sector, and same q=-lnN tie that gives gamma=1 flips the deep-MOND source repulsive.** First fatal
condition under ordered gates: alpha_3=-3. Candidate B (C_M-as-secondary) is the only remaining
named fork; it must alter C_M itself — the sector proven here to carry every surviving kill.
Evidence: openai_push/repair_fork/{gateD_dirac_fork,gate_L_lensing_S2prime}, gateA_fork_ppn,
openai_push/final_closure/gate_fork_S2prime_matter_mondlaw. All exit 0.
