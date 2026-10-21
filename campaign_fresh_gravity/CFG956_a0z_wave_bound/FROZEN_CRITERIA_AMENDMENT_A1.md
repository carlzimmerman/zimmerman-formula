# CFG956 AMENDMENT A1 (2026-10-21): added after criteria, before results

Base criteria 707cdf4cb4. This amendment holds two owner additions and one owner clarification. They arrived through the coordinator
after the base criteria were committed, and before any script was written or any number computed in this lane (K, MUTATE or main).
It is committed alone. Everything in the base criteria not changed here stands.

## A1.1 Attribution
The oscillating-a0(z) hypothesis, including its damped form, is the owner's idea (2026-10-21).
This sentence goes into the README and the figure caption as written.

## A1.2 The owner's damped-wave family (new stage DAMPED; verdict weight as for branches S and C)
- **Picture:** the wave was larger early and shrinks over time, and today we are on the way DOWN from a recent peak.
- **Form:**
  a0(z)/a0(0) = A(z) · [1 + ε0 (1+z)^β sin(2π ln(1+z)/P + φ)] / [1 + ε0 sin φ],
  so ρ_DE(z)/ρ_crit,100 = W · A(z)² · [1 + ε0 (1+z)^β sin(2π ln(1+z)/P + φ)]².
  - The amplitude ε(z) = ε0 (1+z)^β grows with z for β > 0, so it decays with time.
  - W is profiled, as in base §3, so a0(0) stays at the footing value.
  - Branches S and C are exactly as in base §3. Branch N is not run for this family.
- **a0 ≥ 0 cap:** ε0 ∈ [0, ε0_cap(β)], with ε0_cap = (1 + 2.5)^(−β).
  - The cap keeps a0 ≥ 0 at every phase over the whole z range the likelihood evaluates (z ≤ 2.5).
  - For β = 0 it is 1, the base rule.
  - If Δχ²_prof(ε0_cap) < 3.84, the class is NO BOUND BELOW THE CAP.
- **Phase constraint, "on the way down now":**
  - "On the way down" means d a0/dt < 0 today, i.e. d a0/dz > 0 at z = 0, for the wave factor.
  - The condition is g'(0) ≥ 0, with g(z) = 1 + ε0 (1+z)^β sin(θ(z) + φ) and θ = 2π ln(1+z)/P.
  - That is β sin φ + (2π/P) cos φ ≥ 0. It is a constraint on φ alone: φ ∈ [−δ, π − δ] with δ = atan2(2π/P, β).
  - φ is profiled inside that interval (least-squares bounds).
  - The total slope d(a0/a0(0))/dz at z = 0, including A'(0) in branch S, is reported at each bound.
  - In branch S, A'(0) > 0 already, from the CFG689 node segment between z 0 and 0.4.
- **Declared grid:**
  - β ∈ {0, 0.5, 1, 2}, with the base P grid (19 periods).
  - ε0 evaluation grid = ε0_cap × {the base ε grid}.
  - 8 φ starts, spread evenly inside the allowed half-circle, each warm-started from the previous ε0 as in base §4.
  - The statistic, ε0_95 rule, DISJOINT flag, Δχ²_0 and its classes are as in base §4. Δχ²_0 still has 2 dof: ε0, plus φ on a
    half-circle.
- **Reported for each (β, P), per branch:**
  - ε0_95;
  - the largest allowed amplitude ε0_95 (1+z)^β at z = 0.5, 1, 2.33, 3 and 5.
    - z = 3 and 5 lie above every datum, so the expansion data do not constrain them. The README says so.
    - An amplitude above 1 there would mean a0 < 0 at the troughs. It is printed as the formula value and flagged; the physical cap
      is 1.
- **High-z prediction window (reported):** the allowed damped waves at their bound (ε0_95, every allowed φ) give a range of
  a0(z)/a0(0) at z = 3, 3.5, 4, 4.5 and 5, clipped at 0.
  - With A(z > 2.33) = A(2.33) in branch S and 1 in branch C.
  - This prediction holds only within the family. The bound comes from z ≤ 2.33, and the z 3–5 values follow only if the same
    (β, P, φ) form holds there.
- **MUT-D (frozen pass rule; written to the _MUTATE outputs):**
  - Mock: the base-§7 mock construction, but with a damped wave injected: β = 1, P = 0.5, ε0 = 0.1, φ = π/2 (which satisfies the
    phase constraint: β sin φ + (2π/P) cos φ = 1 > 0).
  - Fit: branch S, β = 1, P = 0.5, with the phase constraint.
  - PASS if Δχ²_prof(0) ≥ 3.84, ε0 = 0.1 lies inside the 95% interval, and |ε̂0 − 0.1| ≤ 0.01.
- **Compute:** stage DAMPED is a separate run (mode DAMPED → cfg956_DAMPED.{out,json}), one process after MAIN, with its own 4 h wall
  cap. The rule for exceeding it is as in base §9.

## A1.3 Two further items (reported only)
- **Does CFG689's own best fit prefer a0 rising or falling toward today?** With nodes linear in z, d a0/dz at z = 0 has the sign of
  w(0.4) − w(0).
  - Primary: the profile Δχ² of the tied fit, w(0.4) = w(0), with every other CFG689 primary parameter free (1 dof). The σ is
    √Δχ², signed by the best fit's sign.
  - Also reported: the posterior fraction with w(0.4) > w(0), from this lane's K4 chains; and the same for the z ≈ 0.7 node,
    w(0.7) vs w(0), which is the longer-baseline "down from a recent peak" reading.
- **For comparison only:** the record's DESI DR2 CPL (w0–wa) products.
  - Source: `sonnet55_push/puzzle_32pi/p13c_desi_dr2_chains_a0z.csv`, the record's chain quantiles of a0(z)/a0(0), with
    p13c_desi_dr2_chains_a0z.py and .out for any w0/wa printed there.
  - They are read for the sign of dρ_DE/dt today, i.e. whether a0(z)/a0(0) at the lowest tabulated z > 0 is above or below 1, per
    fit.
  - No external fit is imported. If the record holds no w0/wa values, that part is written "not in record".
  - These are not framework-native inputs and carry no weight.

## A1.4 Owner clarification: how the sketch is presented
- The owner's blue sketch was only a rough illustration. It is NOT the hypothesis.
- The hypothesis is the general family: the plain wave (base §3) and the damped wave (A1.2).
- Base §5 is still computed (its Δχ², its class number and its H(0.5) shift). It is labelled "illustrative sketch", in its own
  section after the main results, and is never headlined. No headline of the form "the sketch is excluded".
- The README leads with the allowed region:
  - ε_max vs P (and vs β for the damped family);
  - the largest allowed amplitudes by redshift;
  - the high-z prediction window.
- Scope: expansion bound only. Physical models and the other observables (growth, CMB, high-z galaxies) belong to lane CFG957 and are
  not done here. The base §6 galaxy-side check stays as written (reported only), kept short.

## A1.5 Figure
One figure, extended to:
- the ε_max vs P curves (base §3 branches; the footings are identical by construction, and labelled so);
- ε0_95 vs P per β (damped, branches S and C);
- a panel (d)-style a0(z)/a0(footing, today) panel, with the largest allowed wave envelope, the high-z prediction window, the
  "no expansion bound above z ≈ 2.5" region, and the illustrative sketch drawn faint and labelled as such.

The caption carries the A1.1 sentence.
