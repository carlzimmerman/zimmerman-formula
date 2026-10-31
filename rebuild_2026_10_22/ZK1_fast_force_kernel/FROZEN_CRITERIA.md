# ZK1_fast_force_kernel: FROZEN CRITERIA (committed before any comparison with X48's force)

**Question.** Can a compiled kernel replace `x48_zoom.accel` with no change beyond rounding? `x48_force.c` computes the same softened direct sum, plus the same Λ term. On one M4 core under load it does a full N = 57,777 force in about 1.8 s; numpy takes about 160 s. That speed is the only number I've seen. The owner wants the Mac on the most important calculations, and asked for closure today. At numpy's speed ZN1 and X80 take days.

**Standing.** κ = ½ FITTED. No physics changes: same G, softening, η step rule, background, ICs. `x48_zoom.py` is not edited; a wrapper replaces its `accel`. Not theory closed.

## Checks
- **K1, force.** On three real particle sets (10¹³ ng 48, 10¹⁴ ng 64, 10¹² ng 64), compared with `x48_zoom.accel` itself: max over particles of |Δa| / median |a| ≤ 1e-10, and median |Δa|/|a| ≤ 1e-12.
- **K2, engine.** 20 steps from a real snapshot (10¹³ ng 48) with each kernel, same step rule: max |Δx| / max |x| and max |Δv| / max |v| ≤ 1e-9.
- **K3, physics.** Full reruns from the ICs of three finished runs (10¹³ ng 48, seeds 1–3), compared with X48's own snapshots: ICs identical; median over seeds of |Δ ln η_S| and |Δ ln c_nfw| (X77's fit) ≤ 0.05; median over seeds and over radii in [r_conv, r_vir] of |Δ ln M(<r)| ≤ 0.02.
- **MUTATE:** ε × 1.01 in the kernel must fail K1.

## Rules
- A run may switch kernels once K1 and K2 pass.
- **No result from a switched run is graded until K3 passes.** If K3 fails, the switched runs are discarded and the record says why.
- Rounding differences grow chaotically in an N-body run, so particles in a switched run won't match numpy's late in the run. That's why K3 tests profiles and not particles. K3's differences are also a direct measure of the zooms' chaos noise, and are reported as that.
- Every switched run's folder says so.
