# C6_literal_cassini: does the healthy C4-literal form (γ_F = 0) still pass the Solar System?

## Verdict

- **By the frozen verdict rule: UNDECIDED.** One validation check, C2, is a frozen FAIL. It fails on float rounding,
  not physics (see Checks).
- **Reading: PASSES, by 2.8×10⁷ to 5×10⁹.** All 24 Cassini cells pass at L★ = 24, 50 and 90 pc, on both footings and
  for fields E0–E3. They pass Hees 2014 and Park 2026. The planets and wide binaries are unchanged from D7d.
- **What the numbers show.** Removing the curl stiffness **lowers** Q₂ by 10–19 %. It does not open a quadrupole.
  The hedgehog survives.
- **So a healthy covariant screened theory exists at this level.** C5 found the parent healthy at linear order. This lane
  finds it Solar-System-clean at O(ε) in a uniform Galactic field.
- κ = ½ FITTED. Not "theory closed". Nothing here says the data favour the framework.

Script: `c6_literal_cassini.py`, with solvers in `c6_solver.py`. It reuses D7d's solver read-only.
- **Checks:** 7/8 PASS, exit 1, 23 min.
- **Compute:** 0.90 GB peak RSS, single thread, no downloads.
- **Criteria:** frozen first (1b2ced55a4), plus a post-result AMENDMENT 1.
- **Outputs:** every number below is in `c6_literal_cassini_results.json`. Earlier executions are kept as `*_RUN1.*`
  and `*_RUN2.*`.

## The equations (C1, sympy, residual 0)

The C4-literal static Lagrangian is −|∇Φ|²/2K + P·∇Φ − W(K|P|) − (γ_L/2)(∇·P)² − ρΦ, with γ_L = KL★²/2 and A33's W.
Its Euler–Lagrange equations are:

- (L) ∇²Φ = Kρ + ∇·p;
- (P_L) ∇Φ + (L★²/2)∇(∇·p) = a₀p/(a₀ − |p|).

The only change from D7d is ∇² → ∇∇·. The consequence is exact: **h(p) = ∇χ, with χ = Φ + (L★²/2)∇·p.** With γ_F = 0
the theory is a scalar theory in disguise, and p = ∇χ/(1 + |∇χ|/a₀).

The linear kernel about the Galactic background is χ_k = m/(1 − m + κ²m/2), where m = k̂·J⁻¹·k̂ and
J = diag(1+x_e, 1+x_e, (1+x_e)²). D7d's kernel is k̂·[(κ²/2)I + J − k̂k̂]⁻¹·k̂.

## Results (both footings, E0–E3; Route F, exact to O(GM/L★²u_e) ≤ 1.3e-5, check C8)

| L★ | Q₂ canonical (s⁻²) | Q₂ alt (s⁻²) | Q₂ / Hees 9.0e-27 (max) | Q₂ / Park 5.2e-27 (max) |
|---|---|---|---|---|
| 24 pc | 1.04–1.86e-34 | 0.93–1.58e-34 | 2.1e-8 | 3.6e-8 |
| 50 pc | 1.15–2.05e-35 | 1.03–1.75e-35 | 2.3e-9 | 4.0e-9 |
| 90 pc | 1.96–3.52e-36 | 1.76–3.00e-36 | 3.9e-10 | 6.8e-10 |

- **Ratio to D7d (γ_F = γ_L):** 0.894 / 0.853 / 0.835 / 0.813 for canonical E0–E3, and 0.905–0.838 for alt.
- **Inner planets:** the anomaly is the hedgehog GM/L★², identical to D7d. At 24 pc that is Mars 0.173, Saturn 0.035 and
  Earth 0.028 of their bounds. At 50 pc Mars is 0.040, and at 90 pc it is 0.012.
- **Wide binary (1.5 M☉, 20 kAU):** γ_v − 1 = 8.1e-6 (24 pc), 1.87e-6 (50 pc) and 5.8e-7 (90 pc). That is within 0.1 % of
  D7d. There is no wide-binary boost visible to DR4.
- **R5, the Cassini lower bound (reported only):** Route N on a single grid gives L★_C ≤ 1.78 r_M. That is
  ≤ 0.069 pc (canonical) and ≤ 0.063 pc (alt), at all E. Alt E3 passes at 1.78 r_M here, where D7d's failed.
  - The non-converged band, Λ = 0.1–1 r_M, is the same as in D7d.

## Mechanism (question 3)

- **The potential sees only ∇·p.** At large κ, both kernels are 2/κ² + O(κ⁻⁴). The 2/κ² term is the isotropic hedgehog
  GM/L★², and it has no quadrupole.
- **Anisotropy enters only at 1/κ⁴, as −4a(c)/κ⁴.**
  - D7d: a = k̂Jk̂ − 1, the arithmetic mean.
  - γ_F = 0: a = 1/m − 1, the harmonic mean, which is smaller.
  - The P₂ coefficients are 1.68 vs 2.00 (canonical E0) and 4.55 vs 6.24 (canonical E3). Hence Q₂ is lower by 10–19 %.
- **The transverse part of δp is not free.** Without curl stiffness, the transverse δp near the Sun is large:
  |δp_T/δp_L| reaches 0.39–0.69, against ≤ 1e-5 in D7d. But (P_L) forces h(p) = ∇χ, so δp = M∇δχ.
  - The transverse part is slaved algebraically to the same scalar χ, through the response tensor M = J⁻¹. It is not a
    free mode.
  - Φ is sourced only by ∇·p, i.e. by k̂·δp in Fourier space. The transverse part never enters Φ. Its only effect is
    through m in the kernel, which is the 10–19 % shift above.
- **Nonlinearity cannot change this.** δp/u_e ≤ 1.3e-5 at 24 pc (C8).

## Checks (7/8)

| check | result | |
|---|---|---|
| C1 | PASS | sympy: (L), (P_L), h = ∇χ, and the closed-form kernel; all residuals 0. |
| C2 | **FAIL (frozen)** | r_F = 1 vs D7d's chi: 3e-15. κ = 0 vs linear AQUAL: 3e-15. Closed form vs general: 4e-15. But x_e = 0, r_F = 0 vs r_F = 1 is **3.8e-11** against < 1e-12. |
| C3 | PASS | This lane's build at r_F = 1 is bit-identical to D7d's build (max \|ΔA\| = 0). |
| C4 | PASS | L★ = 0 AQUAL: BN11 3.829e-26 (ratio 1.008). E2 canonical E0–E3: 2.183 / 3.104 / 3.531 / 4.066e-26, within 0.8 %. |
| C5 | PASS | Route N (γ_F = 0, nonlinear, Richardson) vs Route F at Λ = 30 and 100 r_M, E0 and E3: max \|N/F − 1\| = 1.7e-3. |
| C6 | PASS (weak) | Ratio Λ = 0.01 / Λ = 0 is 1 − 1.1e-4, but the Λ = 0.01 solve is **not converged** (residual 2.3). |
| C7 | PASS | Quadrature 4e-10; tail coefficient 1.8e-5. |
| C8 | PASS | Linear validity 1.3e-5. |

- **Why C2 fails.** The failure is rounding in (κ²/2 + 1) − 1 inside the general 2×2 kernel at x_e = 0, κ = 0.01. The
  identity itself is exact (C1).
- **C6 is weak.** D7d's K7 at Λ = 0.01 was also unconverged (residual 150, `d7d_screened_q2_results.json` K7.conv).
- **Mutation.** `--mutate` drops the 2q_r/r term of Route N's divergence. It breaks C5: max |N/F − 1| = 7e6, with
  the sign flipped. The result is 6/8, exit 1, and the outputs are in `*_MUTATE.*`.
- **Compute disclosure.**
  - The MUTATE run peaked at **1.04 GB** RSS, just over the 1 GB budget.
  - Execution 1 peaked at 1.80 GB and execution 2 at 1.62 GB. Execution 2's peak came from the R5 continuation scan
    running in one process.
  - No 1024³ job was running at any time. Nothing was killed.
  - The final run isolates every Route N solve in its own process and peaks at 0.90 GB.

## Found in the record

- D7d's K7(a) passed on an unconverged Λ = 0.01 r_M solve (residual 150), so the continuity of the AQUAL limit below
  r_M is shown by neither D7d nor this lane. The physical window, L★ ≫ r_M, is unaffected.
- C4's README said the Sun's hedgehog has F = 0, "so the monopole is unaffected". That is confirmed (R2, R3). The
  quadrupole **is** affected, by −10 to −19 %, and the sign of the change is favourable.

## What this does not show

- It is O(ε) and static, in a uniform Galactic field. There is no ephemeris refit and no planetary self-fields. η = 0
  exactly (C5's condition), so P is non-dynamical.
- The band Λ = 0.03–1 r_M is unsolved. L★_C is an upper bound.
- There is no strong-field (NS) or nonlinear well-posedness statement. Those are C5's open items.
