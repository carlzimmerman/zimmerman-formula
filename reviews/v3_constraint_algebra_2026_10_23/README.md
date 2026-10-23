# v3 constraint algebra, 2026-10-23 — RESULT

Owner's request (2026-10-23). Criteria `FROZEN_CRITERIA.md` committed `e86f83df5e` before any script; AMENDMENT A1
(`48804b096a`, post-result) records run 1 (6/9) and three check-code defects, fixed with no threshold changed.
κ = ½ FITTED. Footings canonical / alt never pooled (a₀ enters only the V2 sweep). No dark-matter particle. No data.
Not theory closed.

## Verdict: v3's constraint algebra CLOSES, uniformly — 3 DOF; H4's ill-posedness is dynamical, not algebraic

1. **The Dirac chain stops at the secondaries (V1, exact reduced scalar sector, sympy).** v3 in unitary gauge (τ = t,
   Q = 1/N; H4 L33): primaries π_N, π_i, π_P (η = 0); secondaries C_N = δH_T/δN, H_i, φ_P = δH_T/δP (the P equation). The
   multipliers λ_N, λ_P are fixed by the (N, P) Hessian A, so **no tertiary**. π_i, H_i are first class; π_N, π_P, C_N, φ_P
   are second class: **(26 − 12 − 8)/2 = 3 DOF** (2 tensor + the khronon scalar).

   | background | rank (k = 0.7, 1.3, 3) | first-class rows | det A | scalar DOF/mode |
   |---|---|---|---|---|
   | B1 Minkowski, μ_K = 0 | 4, 4, 4 | π_s, H_x | −k² | 1 |
   | B2 Minkowski, μ_K = 0.3 | 4, 4, 4 | π_s, H_x | −(1.027k² + 0.09) | 1 |
   | B3 FRW point with BS dust (N₀ = 0.9) | 4, 4, 4 | π_s, H_x | −(93k² + 10)/90 | 1 |
   | B4 sheared momentum + BS dust | 4, 4, 4 | π_s, H_x | −(93k² + 10)/90 | 1 |

2. **Uniform on every background, in closed form (V2, frozen coefficients, exact W).**
   `det A = K⁴N₀³ det M (1 + ½L★²q) · S`, with q = kᵀM⁻¹k, κ = 1 + γ_Lρ_P, g₀ = a₀x P̂₀ and
   `K S = −μ_K²/N₀³ − [κ²q + g₀ᵀM⁻¹g₀ + ½L★² Σ_{i<j} m_i m_j (g₀ᵢk_j − g₀ⱼk_i)²] / (N₀(1 + ½L★²q))`.
   Every term in the bracket is ≥ 0, so **det A < 0 everywhere except on the locus {μ_K = 0, x = 0, and k = 0 or
   γ_Lρ_P = −1}**. sympy confirms the Hessian, the Schur identity and the determinant lemma (residual 0). The sweep
   (x 1e-3–1e9, γ_Lρ₀ −0.9 to 0.1, three k directions, kL★ 1e-3–1e8, μ_K 0 and 1/(100 kpc), L★ at the floors, 24 and
   90 pc, both footings) gives det A < 0 at **476,280 / 476,280** points. The closed form agrees with a 50-digit mpmath
   inverse to 3e-39.
3. **No moving-P half mode in v3.** At η = 0 there is no π_P, so DSF-21's moving-P background (Codex's witness)
   does not exist. The other "moving" directions (expansion, shear, BS dust) leave A unchanged, since A does not depend
   on the gravitational momentum. The DSF-21 obstructions (β ≠ 0 non-closure; the π_P half mode,
   `reviews/codex_arrival_audit_2026_10_23/`) are both absent.
4. **J(Y) and the P sector give the same lapse operator (V3).** For J_x, J′(Y) = −1/M_T and J′ + 2YJ″ = −1/M_L
   exactly on W's domain u < a₀. So the P-sector Schur complement's principal symbol is BS's J(Y) lapse Hessian,
   (1/(KN₀))[J′k² + 2J″(g·k)²]. The result therefore covers v3 written with BS's K(Q) and J(Y).
5. **H4's ρ_τ < 0 regions are 12 decades from the locus (V4).** Over all 320 H4 region values (both footings, f0/f3,
   base/fine), the largest |ρ_τ| is 7.99e-23 kg/m³ (LMC–MW, alt). That gives γ_L|ρ| = 1.7e-13 to 2.9e-12 for L★ from the
   floors to 90 pc, against the degeneracy at γ_Lρ_P = −1. **v3's constraint rank does not change there.** H4's
   instability, ω² = ρ_τ(k²/χ − K), is the reduced dynamics of a well-defined scalar. No constraint-bookkeeping repair
   exists: a cure has to change that scalar's dynamics (H4 traces the unbounded rate to γ_L).
6. **MUTATE (clock term deleted, V5 as frozen).** On Minkowski at μ_K = 0 the rank drops 4 → 2: π_N and C_N become
   first class, the lapse is gauge again and there are 0 scalar DOF (GR's count). At μ_K > 0 (B2–B4) the rank stays 4,
   because K(Q)'s lapse mass alone keeps N non-gauge. So **at μ_K = 0 the khronon's constraint structure comes from
   the clock term**, which is C4's Legendre coupling P·A.

Reported, no threshold set: **near-degeneracy at high acceleration.** For kL★ ≲ 1 + x and μ_K = 0,
|S| ≈ κ²k²/(K(1+x)²). At x = 1e9 (Solar-System accelerations) |KS|/k² ~ 1e-18, the sweep minimum. The lapse operator
is non-degenerate but weak there. This is the P-side image of BS's J′ → 0 at large Y, and it bears on the
strong-coupling scale P3 estimated (loop factor ≤ 1.3e-3). That estimate is not re-examined here.

## Checks

| run | result |
|---|---|
| run 1 (`v3_dirac_RUN1.*`) | 6/9 — V1 ×4, V2 locus and V4 PASS; V2(i), V2(ii) and V3 FAIL on check-code defects (AMENDMENT A1) |
| run 2 (`v3_dirac.out`, `v3_dirac_results.json`) | **9/9 PASS** |
| MUTATE (`v3_dirac_MUTATE.out`) | 8/9, exit 1: B1 rank 2, 0 scalar DOF (V5 PASS-as-required); B2–B4 rank 4 |

Single thread, nice 15, 37 s, while the 384³ L1 job ran.

## What this does not do

- It does not test the sign or health of the reduced scalar Hamiltonian (H4's question, unchanged), the vector and
  tensor sectors, matter beyond BS dust, BS25's DBI K (Q7), or the strong-coupling scale.
- V2 is a frozen-coefficient (WKB) symbol. Invertibility of A as a global operator on an inhomogeneous or compact
  background is not proven. V1's exact brackets are at homogeneous points only.
- v4 (AeST + γ_L) is a different action, and its DOF count stays OPEN (C1).
