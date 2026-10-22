# E2_field_equation — which field equation does the action give, and does it matter?

## Verdict: CRISP FINDING

The framework's own action gives **AQUAL with μ(x) = x/(1+x)**, not QUMOND. So D2, D7b and D7c used a
standard-MOND equation that is not the framework's. Recomputed with the action's equation:

- **Cassini Q₂ fails harder.** The canonical law is **2.44–4.59×** the Hees 2σ line on the canonical footing and **2.85–5.19×**
  on the alt footing, for every y_t row. With QUMOND it was 1.69–3.70× and 1.90–4.03×. AQUAL/QUMOND = **1.23–1.49**,
  depending on the external field.
- **γ_v at 20 kAU moves down by 0.007–0.011.** At the PREREG primary field, γ_v goes from 1.175 to **1.167** (canonical)
  and from 1.210 to **1.199** (alt). At the PREREG alt field it goes from 1.151 to 1.145 and from 1.182 to 1.173.
  The frozen line was 0.005, so the verdict is "γ_v CHANGES". The shift is inside A24's claimed ≤ 0.019.
- **D7c's family no-go survives, and gets stronger.** Under AQUAL, no family member passes Q₂ at all four fields on
  both footings. The Q₂-only passer n = 8 now fails (alt E3, 1.04×). The β near-miss also fails its canonical E0
  cell (1.01–1.12×). The least-tense SPARC passer is now β = 5, worst cell **1.41×** (it was 1.19–1.23× under QUMOND).
- **D7d is consistent.** Its (L)/(P) at L★ = 0 are the same AQUAL equation. Our AQUAL value at its K4 inputs is
  3.843e-26, which matches BN11's 3.8e-26 to 1.1 %.

Script `e2_field_equation.py` (solvers `aqual_axi.py`, `aqual_fft.py`) runs in about 8 minutes, single thread.
**10/10 checks PASS**, exit 0. Criteria were frozen first (commit 021ee82abb). `--mutate` swaps AQUAL for QUMOND, the
hidden-ingredient error itself. K3 then FAILS (0.74 of BN11), giving 9/10. Every number below is in
`e2_field_equation_results.json`. κ = ½ is FITTED. Footings are never pooled. The theory is not closed.

## Part 1: the derivation (K1a, K1b, K1c)

PAPER49's Lagrangian at γ = 0 is L = −|∇Φ − KP|²/2K − ρΦ − W_rem(u). Varying it gives two equations.

- From Φ: ∇·(∇Φ − KP) = Kρ.
- From P: ∇Φ − KP = R(u) P̂, with R = K dW_rem/du = u²/(a₀ − u). This is algebraic, and it makes P parallel to ∇Φ.

Solving the P equation gives u = a₀g/(a₀+g), with g = |∇Φ|. Then ∇Φ − KP = μ(g/a₀)∇Φ with μ = x/(1+x). Putting this into
the Φ equation gives

  **∇·[μ(|∇Φ|/a₀) ∇Φ] = 4πGρ.**

That is AQUAL. sympy verifies each step exactly. A non-symmetric 3-D test field gives a residual of 6e-15.

The A33/DSF-21 form reduces to the same equation in the static weak field. That form is −|∇Φ|²/2K + P·∇Φ − W_full − ρΦ,
and it differs from PAPER49's Lagrangian by exactly 0. D7d's (P) at L★ = 0 also matches.

Why this is not QUMOND:
- The action forces ∇Φ to be curl-free.
- It does not force h = μ∇Φ to be curl-free. QUMOND's assumption is that h equals g_N.
- On the AQUAL solution (canonical, E2), the divergence-free part of h is **22 %** of the anomalous field at r_M (K1c).

## Validation

- **K2:** Route A in QUMOND mode reproduces D7b's Route M to 0.7 % (all 8 cells, same sign).
- **K3:** Route A in AQUAL mode gives BN11 to 1.1 %. QUMOND at the same inputs is 0.742 of BN11 (D7b had 0.737).
- **K4:** in the isolated limit, AQUAL equals the algebraic law to 1e-4.
- **K5:** grid convergence is 0.28 %, and the iteration converges to 6e-10.
- **K6:** the 3-D FFT linear AQUAL EFE matches B_par = 1/μ_e and B_perp = 1/(μ_e√(1+L₀)) to 0.26 %.
- **K7:** the 3-D and axisymmetric AQUAL solvers agree to 1.9 % on a single mass in an external field.
- **K8:** 3-D QUMOND reproduces D2's 1.1897 (we get 1.1887). AQUAL changes by 0.0015 between the two grids.

## Numbers

**R1. Q₂ (s⁻²), AQUAL, y_t = none, fields E0–E3.**
- Canonical: 2.200e-26, 3.127e-26, 3.557e-26, 4.097e-26.
- Alt: 2.565e-26, 3.492e-26, 3.996e-26, 4.632e-26.
- The y_t band moves Q₂ by under 0.7 %, as D7b found.
- Anchoring each cell to D7b's quadrature (AQUAL/QUMOND ratio × Route M) gives the same verdict in every cell.

**R2. γ_v.** Orientation-averaged; Δ is AQUAL minus QUMOND on the same grid:

| footing | g_ext | QUMOND (D2) | AQUAL | Δ |
|---|---|---|---|---|
| canonical | 1.778e-10 | 1.1751 | 1.1667 | −0.0084 |
| alt | 1.778e-10 | 1.2095 | 1.1986 | −0.0109 |
| canonical | 2.078e-10 | 1.1514 | 1.1448 | −0.0066 |
| alt | 2.078e-10 | 1.1817 | 1.1730 | −0.0087 |

AQUAL is lower at every orientation. The registered Arm A band is 1.1614–1.1814 (canonical) and 1.1917–1.2267 (alt).
It was built with QUMOND-type machinery, and the AQUAL values sit near its lower edge.

**R3. Family.** SPARC verdicts are D7c's, unchanged.

| member | SPARC | worst AQUAL Q₂ cell |
|---|---|---|
| n = 2 | PASS | 3.59× |
| standard μ | PASS | 2.32× |
| β = 1.25 | PASS | 2.81× |
| β = 2 | PASS | 1.57× |
| β = 2.5 | PASS | 1.47× |
| β = 3 | PASS | 1.44× |
| β = 4 | PASS | 1.42× |
| β = 5 | PASS | 1.41× |
| β = 6 | PASS | 1.42× |
| n = 8 | fail | 1.04× (alt E3) |

The β members now fail canonical E0 as well (1.01–1.12×). AQUAL ≥ QUMOND in every cell computed (ratio 1.03–1.49).

## Input ledger

| input | class | source |
|---|---|---|
| Field equation (AQUAL, μ = x/(1+x)) | FRAMEWORK-NATIVE | derived here from PAPER49 / A33 |
| QUMOND in D2/D7b/D7c | STANDARD-MOND-MACHINERY | replaced here; the sensitivity is R1–R3 |
| GM_⊙ | RAW | IAU |
| E0: g_N,e = 6.913e-11 | FRAMEWORK-NATIVE | A60 |
| E1–E3: total g_e | SURVEY-CALIBRATION (kinematic) | record band, via D7b |
| PREREG g_ext 1.778 / 2.078e-10 | SURVEY-CALIBRATION (R₀, v_c) | PREREG §1.1, via D2 |
| Hees 2014 and Park 2026 Q₂ bounds | RAW (ephemeris fit) | BOUNDS.md, via D7b |
| BN11 3.8e-26 | external AQUAL benchmark | validation only, not in a verdict |
| SPARC verdicts | RAW + SURVEY-CALIBRATION (SPS Υ prior) | D7c / AG4b, unchanged |

## What this does not show

- The external field is uniform and static, and the Sun is a point mass. There is no ephemeris refit.
- The binary is D2's single 1+1 M☉ circular case, not the registered population or estimator.
- The cold sector's own density is neglected.
- SPARC is not refitted with AQUAL. Its fits are algebraic, so thin-disc AQUAL corrections are not computed.
- Nothing about L★ > 0. D7d owns the screened case, and its L★ → 0 target is the R1 table above.
- Memory: the 3-D jobs run in child processes. Peak RSS is 1.18 GB in the parent and 1.09 GB in a child, run
  sequentially. The first run, all in one process, peaked at 2.2 GB. Its numbers are identical.

## Record notes

- `deepseek_push/DS_FINAL_2026_10_21/A24_wide_binaries/report.md` says "the law *is* AQUAL" (lines 16 and 37) but computes
  with QUMOND (line 62).
  - Its ≤ 0.019 bound holds: the actual shift is −0.011.
  - The sign it does not state: AQUAL is lower.
- D7c README, "What this does not show": "AQUAL would raise Q₂ by about 1/0.74".
  - That holds for the canonical law (1.23–1.49).
  - It does not hold for the β members (1.03–1.22).
  - The no-go conclusion is unaffected.
