# CFG430 FROZEN CRITERIA: does the LMP coexistence field h_c land on y = g_b/a0 = 1 from the operator itself?

Committed before any script was run.

**Door.** CFG478 showed a first-order switch is legal. CFG481 built the exact LMP/Kac operator: a 1-D lattice core with occupancy capped at 4, plus a Kac attraction. The operator has a coexistence field h_c < 0. CFG480 measured a two-mode density ratio of 6.25 in the N256 PM run. The question here is whether h_c maps to g_b = a0 (y = 1) with no new constant.

**What the operator contains.** Its inputs are β, a, U, J and the cap n_max = 4 (inherited from the LMP / #228 construction). None of a0, G, ρ_Λ, c or κ appears. Its outputs are pure numbers. Any route from h_c to y therefore needs a dictionary h ↔ y. The test asks whether a dictionary fixed by the framework's own equations puts h_c at y = 1, and whether that holds across the core parameters.

**Identities worked out while drafting (stated now, checked numerically in the script).** In CFG481's conventions:
- the field argument X enters the weights as e^{βXn};
- the coexistence functional is F_h(X) = Q(X) − (X − h)²/(2βa);
- the dimensionless Kac coupling is K = β³a.

The core Hamiltonian is particle-hole symmetric up to a linear field: n → 4 − n maps it to itself at X_s = (3U + 8J)/2. This gives:
- (I1) the exact coexistence field h_c = X_s − 2β²a, so βh_c = β(3U + 8J)/2 − 2K;
- (I2) the band opens (the onset, which is CFG481's own "phantom switch temperature") at K χ(X_s) = 1, where χ is the per-site occupancy susceptibility of the core chain;
- (I3) for U = J = 0, χ = Var(uniform 0..n_max) = n_max(n_max + 2)/12, so βh_c(onset) = −6/(n_max + 2). For n_max = 4 this is exactly −1.

The script must reproduce I1 against CFG481's own `scan_band` at its reference point: β = 0.56, a = 4, U = 0, J = 0.02, h_c = −2.429, tolerance 1e-3.

**Dictionaries (frozen).** All use the raw gauge, with occupancy counted from n = 0, as in CFG481 and in a Bose occupation number.
- **D1, the kernel-Bose reading (primary, framework-fixed).** ν(y) = 1/(1 − e^{−√y}) = Σ_k e^{−k√y} is one Bose mode with fugacity e^{−√y}. Identify the fugacity e^{βh} with e^{−√y}. Then y_c = (βh_c)².
- **D2, log-fugacity (generic, zero-coefficient).** e^{βh} = y. Then y_c = e^{βh_c}.
- **Gauge-shifted versions (informational, not evidence).** Measuring h from the particle-hole point gives h̃_c ≡ 0 by construction. D2 on h̃ then returns y = 1 for every core and every value of a0. This is a tautology: a0 enters only as the unit of y. It is declared inadmissible in advance.

**Points on the coexistence line.** The operator alone does not choose β.
- **P_on (primary, operator-intrinsic):** the onset (I2). No data input is used.
- **P_480 (secondary):** the β at which γ = ρ_l/ρ_g = 6.25, CFG481's match to CFG480. This point is fitted to the PM run, so it is a constant by construction. It is reported, and it cannot by itself produce a PASS.

**Core grid.** U ∈ {0, 0.1}, J ∈ {0, 0.02, 0.05}, a ∈ {2, 4, 8}, giving 18 settings with n_max = 4. A sensitivity to n_max ∈ {3, 5} at U = J = 0 is reported. The cap is inherited, so it is not graded.

**Window.** |log10 y_c| ≤ 0.1, i.e. y_c in [0.794, 1.259].

**Checks.**
- **C0 (identities):** I1 matches CFG481's scan_band (|Δh_c| ≤ 1e-3). The numerical Maxwell root at three grid settings matches I1 (≤ 1e-3). If C0 fails, the lane is INVALID.
- **C1 (D1 at P_on, pure cap):** U = J = 0, all three a values, inside the window.
- **C2 (D1 at P_on, full grid):** all 18 settings inside the window.
- **C3 (D1 and D2 at P_480):** reported. Inside the window or not, this point carries a fitted constant.
- **C4 (D2 at P_on, full grid):** a generic alternative. If C4 passes while D1 fails, the result is convention-dependent.
- **C5 (PM cross-check, informational, can downgrade):**
  - Recompute s_ph and s_c at z = 0 on two 256³ snapshots with the CFG424 engine functions (imported read-only): cfg424 RES TA MIXA FLAT alt seed360, and cfg410 RES Rc3 MIXA FLAT canonical.
  - Report the median y over cells where the engine's own switch variable r = (s_ph − s_c)/s_c satisfies |r| < 0.05, that is, where the simulated switch actually fires.
  - Report the same over ON cells only (f > 0.5).
  - If the PM boundary median y lies outside [0.5, 2] (0.3 dex), the PM switch does not fire at y = 1. Any operator mapping to y = 1 then does not describe the simulated switch, and a PASS is downgraded to CONDITIONAL.

**Verdict.**
- **PASS (h_c → y = 1 from the operator):** C0, C1 and C2 pass, and C5 is consistent.
- **CONDITIONAL, pure-cap only:** C0 and C1 pass but C2 fails, so y = 1 only for U = J = 0 with n_max = 4 under the D1 reading. Also CONDITIONAL: a PASS downgraded by C5. Either way, the stated restrictions are named.
- **FAIL, needs a constant:** C1 fails. In that case no framework-fixed dictionary puts the operator's own switch point at y = 1, and any mapping requires choosing a constant (a unit for h, a β, or a fitted γ).
- If C4 passes while C1 fails, the result is labelled "convention-dependent". It is still a FAIL for "from the operator itself", because choosing D2 over the framework-fixed D1 is a choice.

**MUTATE (must flip; both directions run, separate output).**
- **M1:** the computed βh_c is replaced by a planted −1.000 at every grid setting and both points. The harness must return C1 and C2 PASS (y_c ≡ 1).
- **M2:** the planted value is −2.000. The harness must return C1 FAIL (y_c = 4).

If either flip does not occur, the harness is broken and the lane is INVALID.

**Compute.** The operator part is analytic plus 5×5 transfer matrices and runs in seconds. C5 is two deposits and a few 256³ FFTs, run under nice -n 15 with ≤ 4 threads, well under 30 minutes. No downloads.
