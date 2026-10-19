# CFG837 (lane SHELL): radial-shell tether dynamics and the free fraction F(f_loss)

Criteria: `FROZEN_CRITERIA.md`. Derivation and verdict: `DERIVATION.md` (NO REDUCTION, sign reversed; lane label CONSTRAINT TIGHTENED). Ledger row: CFG837 in
`../LEDGER.md`. Helper script: `cfg837_shell_check.py` (committed in 1eaa5a118). kappa = 1/2 FITTED; not "theory closed".

## Script run (2026-10-18): NOT EXECUTED, pre-run code review only

**The script was not run.** A 1024^3 job (CFG650 engine under the overnight chain, about 39 GB resident, restarted shortly before this review) was live. The
standing no-compute rule applies whenever a 1024^3 run is live: nothing computational runs beside it, not even scripts that take seconds. The script's own guard
(`CFG837_I_CHECKED=1` means "no 1024^3 job is live") could not be set truthfully. So there are **no script numbers**, nothing in `DERIVATION.md` or the ledger row is
confirmed or contradicted, and the frozen verdict stands as committed. The row's status "WRITTEN, NOT RUN, UNTESTED, QUEUED" is unchanged, so the ledger is not edited.

### Code review (read line by line against DERIVATION.md; the script is unchanged from 1eaa5a118)
No bug found that changes any number the script would print. Checked:
- Part A: `x_apo` is the root of (3 - p) x^2 - p x - p = 0 (DERIVATION 3.3). `half_period` is the theta-substitution of dt = r0 dx / v, with
  v^2 = [2(3 - p)/(3 x^3)](x - 1)(x_a - x)(x - x_b): (x - 1)(x_a - x) = hw^2 sin^2(theta) cancels dx = hw sin(theta) dtheta, leaving sqrt(3/(2(3 - p))) x^1.5 / sqrt(x - x_b) (DERIVATION 3.4).
  `eps_sudden` = -(3 - p)/(3 r0) (3.2). The leapfrog uses m^2 = p at r0 = 1. The marginal test uses v^2 = 2(r^2 - 1)/r^3 (3.4). All match.
- Part B: start at the peak equilibrium r = mu/sqrt(p) (mu = 1). Linear mass ramp q: p -> 1 with kick-drift-kick and q evaluated at both half-kicks. Sudden value
  -(3 - p) sqrt(p)/3, adiabatic value -2/3, nu = tau p^(3/4) = tau / r0^(3/2). T_end = pi sqrt2 is the final small-oscillation period (DERIVATION 4.1-4.3). All match.
- Part C: `accel` and `energy` are identical to `../CFG776_frozen_relic/cfg776.py` (whose K2 check passed dE/E <= 1e-3). The rank energy uses the mid-shell mass,
  which differs from the exact discrete coefficient (a^2 + ab + b^2)/3 by dm^2/12 (negligible). The physical edge R0 = 5.364 sqrt(p) gives m(R0) = 5.364 p
  less the core offset.

Caveats for whoever runs it (interpretation, not code bugs; the script was left unchanged so a later run matches the committed version):
1. Default part. Without `CFG837_PART` set, only Part A runs. A full check needs three invocations (A, B, C). The script writes `cfg837_part{A,B,C}.out` and
   `cfg837_part{A,B,C}_results.json` itself. There is no MUTATE mode, and the frozen criteria define none.
2. Part C `u_beyond_1000` is too weak at TEND = 1000. Escaping shells have v_inf of about 0.3-0.95 (hand: v_inf^2 = 2 eps0, e.g. p = 10 at r0 = 17 coreless gives
   eps0 = 7/51, v_inf = 0.52; p = 10 at r0 = 50 gives 0.31, at r0 = 1 with the core 0.94). By t = 1000 most unbound shells have not reached r = 1000. Read the rank-energy count `u(eps>0)`, not `u(r>1000)`.
3. Part C `F_dyn = u / f_loss` is the derivation's U/S only on the physical edge, where M_c = 5.364 p. The core offset makes it about 1.4% high at p = 1.5
   (M_c = 7.93 against 8.05). On the `cfg776_R0_50` edge, M_c = sqrt(p) 49.5 + 0.5 is an arbitrary cut, so F_dyn there is not U/S.
4. Part C at TEND = 1000 on the R0 = 50 edge: the outer shells at p = 1.5 and 2 have not finished one half-swing (3.393 x 50^1.5 = 1200 t0;
   6.106 x 354 = 2160 t0). That snapshot is pre-relaxation for the outer shells.
5. Part B at p = 3, sudden: eps0 = 0 exactly, so the printed "unbound" flag there is round-off, not a result. Part B tabulates eps against nu but does not solve
   for nu_c(f_loss). A bracket can be read from the rows.

### What each part would test once run (claims in DERIVATION.md)
| claim | tested by | hand values to compare (DERIVATION, or hand arithmetic here) |
|---|---|---|
| single-shell closed forms; threshold p >= 3, f_loss >= 2/3 (no crossing) | Part A | x_apo 1.1036 / 1.6180 / 2.7321 / 5.8541 at p 1.1 / 1.5 / 2 / 2.5; half-swing 3.393 (p 1.5), 6.106 (p 2); eps0 = -(3 - p)/3; p 3.4 escapes |
| any monotone history: -2/3 <= eps_final <= sudden value; p < 3 never unbound; the critical loss-time ratio nu_c | Part B | adiabatic -0.6667; sudden -0.6124 / 0 / +2.051 / +7.379 at p 1.5 / 3 / 5.6 / 10 |
| shell crossing: unbound mass rises with p; energetic bound; F_E about 1, F_C about 0 | Part C | coreless bound u_max = 1 - (c/R)^(1 - kappa(p)) about 0.19 (p 1.5), 0.55 (p 2), 0.95 (p 3) on the physical edge (approximate: Part C has a core) |
| CFG813 minimum 0.38 / median 0.90; early/late retention ratio 1.5 (CFG811); unbound = free identification | not testable by the script | record-reading or postulate items |

### To run (only after no 1024^3 job is live: the CFG650 engine, `run_650.py` and the overnight chain all gone)
    for P in A B C; do CFG837_I_CHECKED=1 CFG837_PART=$P OMP_NUM_THREADS=1 nice -n 19 python3 cfg837_shell_check.py; done > cfg837_shell_check.out 2>&1
Estimated: Part A seconds, Part B about a minute, Part C about 10 minutes, all under 200 MB.

## Script run (2026-10-18, owner chat): EXECUTED — Parts A, B, C confirm the derivation
Run beside the live 1024³ job on the owner's explicit 2026-10-18 instruction (light lanes allowed, 1 core, nice 19);
`CFG837_I_CHECKED=1` was set under that override (the guard's literal meaning, "no 1024³ job live", did not hold — disclosed).
Script unchanged from 1eaa5a118. Total 4.9 min, < 50 MB. Outputs: `cfg837_part{A,B,C}.out` and `cfg837_part{A,B,C}_results.json` (written by the script).
- **Part A (DERIVATION §3.2–3.4): all PASS.** Apocentres x_apo 1.1036 / 1.6180 / 2.7321 / 5.8541 and half periods
  2.398 / 3.393 / 6.106 / 16.770 at p = 1.1 / 1.5 / 2 / 2.5 match the closed forms to 1e-4; p = 3 is exactly parabolic
  (v² = 2(r² − 1)/r³); p = 3.4 escapes.
- **Part B (§4.2–4.3): confirmed.** Slow loss always ends at the adiabatic ε = −2/3 (bound) for every p; at p = 10
  (f_loss 0.90) sudden loss unbinds (ε +7.38). The critical ramp lies between ν = 2.5 (unbound) and ν = 25 (bound), so
  **ν_c(0.90) ∈ (2.5, 25)** — the bracket §4.3 asked for.
- **Part C (§5, shell crossing): confirms the sign, and is stricter than the bound.** On the physical edge the unbound
  fraction u(ε > 0) is 0.023 / 0.023 / 0.095 / 0.939 / 0.975 at p = 1.5 / 2 / 3 / 5.6 / 10: monotone in p (§5.3's
  "expected, not proven" now shown for these p). Early-type-like losses (f_loss 0.82–0.90) unbind ~94–98%; cluster-like
  losses (f_loss ~0.33–0.36) unbind ~2.3%, ten times below the u_C ≥ 0.23 the record needs and inside §5.2's u_max
  (0.16–0.24). Energy is conserved to ≤ 5e-4. Caveat 2 of the review applied (read u(ε > 0), not u(r > 1000)).
- **Verdict unchanged and now checked numerically: NO REDUCTION — the dynamics unbind more where more baryons were lost
  (early types), while the data need the clusters (which lost less) to carry the larger free fraction.**
