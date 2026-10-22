# A81 — VERDICT

**The final joint fit, every parameter profiled, is one consistent parameter set — and the theory's
remaining freedom is two numbers, not four.**

```
kappa_P3 = 0.378081 +- 0.025764 (stat) +- 0.118038 (syst) = 0.378081 +- 0.120817
             (kappa_DE = 0.456915)
a0       = 8.553737e-11 m/s^2        B = 1.199647 +- 0.03813        u = 0.442872 +- 0.02293
T        = 5.5059 for 2 shared parameters (p = 0.0637, 1.85 sigma), 90.3% of it the IMF prior
T_data   = 0.5333 (0.30 sigma)       T_prior = 4.9725
Delta-chi2(thermal - kappa=1/2) = +1.824508 -> 1.3507 sigma, LR 2.4899 : 1
```

1. **The three data channels agree at 0.30σ.** SPARC (−0.62σ), clusters (+0.36σ) and the SLACS ridge
   (+1.92σ) are consistent; the whole tension is the IMF normalisation at `+2.04 sigma`, with
   `B = 1.199647` outside Treu's 95% upper bound `1.1767`. That is A71's 1.97σ, sharpened by 0.07σ.

2. **The thermal point `κ_DE = Z/4π = 0.460659` is free**: the fit sits `-0.12 sigma` from it and pays
   `0.015199` in χ² to be there. **`κ_DE = ½` costs `Δχ² = 1.824508` (`1.3507 sigma`, LR `2.4899 : 1`)**
   with B and u refit at both points — A74's `1.863869` reproduced to 2.1%. Neither point is excluded,
   and the old `κ_P3 = ½` target (`1.1312e-10`) is `4.56 sigma` away and is a different theory.

3. **The lensing channel is κ-blind in its data** — `0.2113` over the whole band with B profiled, and
   A71's `6.3517` is an unprofiled-B artefact (`0.3985` when B is actually profiled). The `9.1069` that
   looks like a κ preference is the IMF prior through `B_req(κ)`; adding SLACS moves κ by `+0.00660`
   (`0.26 sigma`) and tightens σ(κ) by 0.16%. The σ_ap channel moves B by at most `+0.49%` and κ by
   `-0.00040`: it breaks nothing and confirms nothing.

4. **The ledger: nine symbols, 2 forced (`K`, `α`), 1 postulate (`a0`), 1 atomic-conditional (`σ_c`),
   2 BBN-bounded (`β`, `Λ_bare`), 3 free (`γ`, `η`, `L*`) — and 2 genuinely free parameters.** The three
   free symbols are one scale (`|dlnγ| = 2|dlnL*|`, `|dlnσ_c| = 0.5|dlnL*|`, rank 2 of 5, nullity 1),
   so the count is **η plus one P-sector scale**. Adopting the atomic `σ_c` would reduce it to 1; A76's
   finding that no measured `σ_c` exists on disk is exactly the refusal of that adoption. The two
   known tensions are in the ledger itself: **`L*` has no measured `σ_c` (A76)** and **`η/γ` has no
   matching principle (A77)**.

5. **All seven cross-lane identities hold**: `κ_DE = Z/4π` (residual `0.0e+00`), `a0 = cH_Λ/2π`
   (`8.742e-04` / `2.165e-04`), `I(y_t) = 8π/κ²` → `y_t = 77.876356` (`1.6e-13`, inside `[60, 140]`),
   `L* = σ_c²/a0` → `25.42031 pc` (`0.0e+00`), `β = (2/3)Ω_Λ(r_Λ − 1)` (`< 1e-9`),
   `ΔN_eff = -11.1738 β/(1+1.5β)` → `-0.30026`, and A80/A85 on `B(n=4)` (`1.22799` vs `1.22688`,
   `0.09%`, `0.01 sigma`). No identity fails. The largest residual is the BRIEF's Λ/H0 rounding
   (`Ω_Λ = 0.684996` implied against `0.6847` used), not a contradiction between lanes.

**One sentence.** The theory survives every channel at 1.85σ with a 2σ IMF normalisation, cannot
distinguish `a0 = cH_Λ/2π` from `κ = ½` at better than 1.35σ, and its parameter count is genuinely two
— one P-sector scale it cannot measure and one inertia it cannot derive.

*27/27 checks PASS, exit 0, cold start; 10 mutations, every one exit 1, 22/27 checks killed
(`MUTATE.md`); every number in `report.md` verified against `a81.out`
(`verify_report_numbers.py`, 505 tokens, 0 missing). Nothing committed.*
