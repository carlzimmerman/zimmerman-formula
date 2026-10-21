# CFG955 AMENDMENT A1 (dated 2026-10-21; committed alone, before the MAIN rerun)

**Status.** POST-RESULT for:
- the K and MUTATE stages (K 8/8 PASS; MUTATE 5/5 bite, exit 1 by design);
- the static lines that MAIN attempt 1 printed before it was stopped: the structural sympy checks H0 / L4 / L6 / L7, a1/a2 and L5.

PRE-RESULT for every graded spherical-toy output (a3, L1, the toy energy books). No K-T toy run reached a window, a D value or an
ON-THE-LAW flag in any committed or scratch run. The frozen text of `FROZEN_CRITERIA.md` (903cd8f1d) is not edited. κ = ½ FITTED;
footings never pooled; not theory closed.

## What happened (disclosed in full)

1. **MAIN attempt 1** (2026-10-21) printed K (identical to the K stage), the structural checks, then a1/a2 and L5:
   - **a1 (simple kernel) missed the frozen 1e-6 line:** 1.64e-6 (canonical) and 2.80e-6 (alt). ν_mono passed at 2.87e-7 / 4.84e-7.
   - **L5 returned NOT UNIQUE** for NGC 3198 (second roots C = 0.457–0.534; F(C) flat to |F| ≤ 1e-3 between them and C = 1) and
     for the toy (second root C = 0.087).
2. **The first K-T toy run (IC-L) stalled.** After more than 30 min it had not reached t = 100, against about 3 min for CFG935's
   identical relaxation-off start. I stopped my own process by verified PID (no other process was touched). Its partial log is kept
   as `cfg955_firstrun_stopped_toycollapse.out`.
3. **Diagnosis** (scratch scripts outside the repository; short capped runs; each number printed in the scratch log is quoted in
   the README). The frozen K-T toy develops a **central collapse** starting at t ≈ 12–18:
   - 15% of the dust shells end up inside r < 0.01 by t = 14 (law: 5e-5 of the mass inside 0.05);
   - the global time step falls from ~2e-3 to ~1e-5;
   - t_end = 350 / 650 is then infeasible (well over 10 h per run).

   The collapse:
   - is present at N = 40000 (time step already falling by t = 12);
   - is present with softening 0.1 (56% of the dust inside r < 0.05 by t = 22);
   - is present at the fast probe τ/10;
   - is present with relaxation forbidden inside r = 0.24 (55% inside r < 0.5 by t = 21; law 1.2%);
   - is **absent with relaxation off** (law state kept: 0.0136 inside r < 0.5 at t = 40, law 0.0118).

   So it belongs to the K-T relaxation itself, not to N, the softening, the cadence or the unresolved centre.

## A1.1 (compute; applies to every spherical-toy run in MAIN and in the post-hoc stage)

Each spherical-toy run is capped at **30 min of wall clock**. A capped run is scored on CFG935's windows taken **relative to the
time reached** (W1 = [0.5, 0.75], W2 = [0.75, 1] of t_reached). It is labelled "capped at t = …", and its ON-THE-LAW flag is graded
as frozen. This is CFG935's A5 rule. No other toy setting changes (N = 10000, ε = 0.02, r_min = 1e-3, DTMAX 0.02, CA 0.03, the
bins, the seeds, the ICs, T1 = τ_ff/(2α) with α = 1; the relaxation cadence is 0.05, an implementation choice fixed before the first
run and disclosed).

## A1.2 (the frozen class text applied as written; code correction before the rerun)

The frozen §7 says NO KINETIC PARENT needs, in addition to a FAIL, "a structural statement (H0, L1, L2, L5, L6, L7 or T-EX) that
passes its check [and] shows the failure is generic". MAIN attempt 1's code fell back to NO KINETIC PARENT on any FAIL. That does not
implement the clause, and it is corrected to apply the clause literally, test by test:
- an (a) FAIL is generic iff a3 fails **and** L5 is NOT UNIQUE (the hydrostatic family does not select the law and the dynamics do
  not reach it);
- a (b) FAIL is generic iff b3 fails for every τ candidate (L6, the multi-stream drag);
- an a1-only miss, or any other FAIL, has no listed generic statement.

If every FAIL is generic, the class is NO KINETIC PARENT. If a FAIL has no generic statement, the frozen rule does not classify, and
the output says **"NOT CLASSIFIED BY THE FROZEN RULE"** with the reason. CONDITIONAL and ENGINE HAS A KINETIC PARENT are unchanged.

## A1.3 (post hoc; reported; NO class weight) in `cfg955_posthoc.py`

- **PH1, a1 convergence.** The simple-kernel NGC 3198 check at N = 100001 (frozen), 200001 and 400001 table nodes. If the miss falls
  with N, it is discretisation of the tabulated stationary state; the frozen a1 grade is still reported as FAIL.
- **PH2, the second hydrostatic equilibrium.** Its law deviation on NGC 3198's 43 radii and in the toy, and along the near-degenerate
  family C ∈ [C₂, 1].
- **PH3, the collapse diagnostics** (the six capped runs above), rerun inside the repository's script with 200 s caps, so that every
  number quoted is reproducible.
- **PH4, the thermostatted linear stability (T-BE, stated after seeing the collapse).**
  - In the fluid limit of K-T (τ → 0, p = ρT_J with T_J held by the bath), radial perturbations y = δM obey the Sturm–Liouville
    problem −(y′/(r²ρ))′ − (4πG/(r²T_J)) y = ω² y/(r²ρT_J), with y(r_in) = y(r_e) = 0 (rigid edge; this choice is conservative).
  - For the deep-law SIS phantom (T_J = v_c²/2, ρ = v_c²/(4πGr²)) this is −y″ − 2y/r² = (2ω²/v_c²) y. Its zero-frequency solutions are
    r^((1 ± i√7)/2) (sympy). By Sturm's theorem a negative ω² exists whenever the deep region spans more than e^(2π/√7) ≈ 10.7 in
    radius.
  - Computed: the lowest eigenvalue on the toy and on NGC 3198 (both footings, both kernels), by finite differences.

  This is a candidate explanation of the collapse (a Bonnor–Ebert / Antonov-type instability of a thermostatted SIS). It carries no
  class weight: it is not one of the frozen structural statements.

κ = ½ FITTED; footings never pooled; cold energy (no particle species); not theory closed.
