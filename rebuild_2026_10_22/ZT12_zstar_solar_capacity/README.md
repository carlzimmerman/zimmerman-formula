# ZT12: R1's cap on the Sun's hedgehog cannot break Solar-System screening. Z-T12 PASS; the cap only lowers the anomaly, by ~10³ at the planets (exact pointwise mechanism derived)

Criteria and ledger **c4b23a2970** (committed before any number). Script `zt12_solar_capacity.py` (seconds, 0.11 GB). `--mutate`
(cap applied to p, a non-local cap) fails KM3 as it should (exit 1). κ = ½ FITTED. Footings never pooled. No dark-matter
particle. Not "theory closed". Nothing here says the data favour the framework.

## The mechanism (M1–M4, all checks PASS)

1. **The held dust's self-gravity cancels exactly (M1).** In C6's screened static Lagrangian, put the Φ equation (Φ′ = g_N + p)
   back in. The local terms become −(g+p)²/2K + p(g+p)/K − p²/2K = −g²/2K: every p-term cancels (sympy residual 0). What
   survives is local in the held density D = ∇·p: **E[D] = (1/K) ∫ [(γ_L/2) D² + Φ_N D] dV** (Green reciprocity for ∫ρΦ_D). Numerically,
   the Hessian of the *unsimplified* functional on a 240-shell grid is diagonal, γ_L w/K, with off-diagonal terms ≤ 7e-6
   (finite-difference roundoff).
2. **Free solution (M2).** γ_L D + Φ_N = μ gives D = 2GM/(L★² r) + const, which is C6's hedgehog, held density M/(2πL★² r)
   and anomaly GM/L★² (residual 0).
3. **The obstacle is pointwise (M3).** E is local and strictly convex in D, so R1's cap 0 ≤ D ≤ Kρ_d gives exactly
   **D_Z★ = min(D_v3s, Kρ_d)**. Inside r_nl = M☉/(2πL★²ρ_d) the Sun sits in a uniform ball of held dust. Outside it the
   hedgehog is untouched. A bounded L-BFGS-B minimisation of the full functional reproduces the clamp to 8.6e-12, with the
   exterior unchanged to 2.1e-13.
4. **The cap can only lower the anomaly (M4).** p_Z★ = (4π/3)Gρ_d r for r ≤ r_nl, and (GM/L★²)(1 − r_nl²/3r²) outside. Both match
   quadrature to 4e-16, and p_Z★ ≤ p_v3s at every radius. At a planet inside r_nl the anomaly is (2/3)(r/r_nl) of v3s's.

## Numbers (worst over L★ 24 / 50 / 90 pc and both footings; ratio to the bound)

| bracket (cap the Sun's hedgehog sees) | r_nl | worst planet (Mars or Saturn) | Cassini Q₂ / Park |
|---|---|---|---|
| B0: none (stars own no dust, R2) | — | 0 | 3.6e-8 (C6's value) |
| B1: local held density 0.059 / 0.068 M☉ pc⁻³ | 60–970 AU | **2.6e-4** | 7.4e-4 |
| B2: 10 × local | 6–97 AU | 2.6e-3 | 7.4e-3 |
| v3s (no cap; C6 reproduced to 2e-5) | ∞ | 0.173 (Mars, 24 pc) | 3.6e-8 |

The Q₂ row is a conservative bound: C6's value + 4πGρ_cap, the most a uniform saturated ball of any shape can add. Reported
alongside: the Milky Way's own held density as a uniform ball gives ≤ 2.6e-4 of the bounds (≤ 2.6e-3 at 10×), and the
gravitational wake from the Sun's 230 km/s motion gives ≤ 5e-6. Both are common to v3s and Z★.

**Verdict: PASS** (worst 7.4e-4 in B1; 7.4e-3 even in B2).

## Reading

- The worry was that capping the hedgehog would unscreen the Sun. The opposite happens. Screening is the stiffness term
  (γ_L/2)D², and the cap only removes held dust. The held density is the only thing the anomaly is made of, so removing some of
  it lowers the anomaly.
- So Z★'s Solar System is *cleaner* than v3s's. The tightest v3s cell (Mars at L★ = 24 pc, 17 % of its bound) drops to
  2e-4 under B1. In B0, Z★'s own reading for stars, the planets see no hedgehog at all.
- Z-T3's qualifier still applies: the saturated set is well-posed only for ρ_d > 0. The local held density is > 0, so the
  zero-dust edge does not arise here.
- Scope: screened (linear) order, spherical, a static Sun. The MW field enters only through C6's Q₂. Transporting the moving
  Sun's charge (X15's open point) is not solved.

## Implementation note (before commit, after the first numbers)

Three fixes were made to the numerical self-checks only. The physical table and the verdict were identical in every run.
(1) E_full is evaluated as a difference from D = 0, term by term and unsimplified. The D-independent g_N² energy is
10⁷ × the stiffness term on this grid and cancelled catastrophically. (2) The bounded minimiser runs in preconditioned
variables z = √(γ_L w/K) D with the unsimplified analytic gradient, because unscaled L-BFGS-B stalled. (3) KM4 compares the
closed forms with quadrature of the clamped D, as the criteria state, rather than with the grid solution, which carries a
1e-3 discretisation error.
