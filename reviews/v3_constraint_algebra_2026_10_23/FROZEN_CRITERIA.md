# v3 constraint algebra, 2026-10-23 — FROZEN CRITERIA (before any script or number)

Owner's request: "run the v3 constraint-algebra audit (β = η = 0, P auxiliary, BS K(Q) and J(Y)): frozen criteria first,
then the Dirac chain, rank on static and moving backgrounds, the det A degeneracy locus vs H4's ρ_τ < 0, and mutate."
Follows `reviews/codex_arrival_audit_2026_10_23/` (DSF-21 / A33, η > 0), reusing its sympy machinery. κ = ½ FITTED.
Footings canonical a₀ = 9.36e-11, alt 1.13e-10 m/s², never pooled (a₀ enters only V2's sweep through x and L★ floors).
No dark-matter particle. Not "theory closed". Nothing here uses data. One thread, nice 15, small jobs (a 384³ L1 job is live).

## 0. The action (read before freezing; not blind)

v3 = H4 FROZEN_CRITERIA line 33 / C4: `L/√−g = R/(4K) + P^μA_μ − W(K|P|) − (γ_L/2)(D·P)² + μ_K²(Q−1)²/(2K)`, K = 4πG,
W′(u) = u a₀/(K(a₀ − u)), γ_L = K L★²/2, n^μP_μ = 0, plus Λ. J(Y) is **represented by the P sector** (C4 K3: A33's P sector
at γ = η = 0 is the Legendre dual of J_x; including J(Y) as well would double-count). Unitary gauge τ = t: Q = 1/N,
A_i = ∂_i ln N, P^μA_μ = P^i∂_i ln N (C4 K6), D·P the spatial divergence (H4 A2), β = 0, η = 0 (no Ṗ). Hamiltonian:

    H_T = ∫ { N[(√h/4K)(2Λ − ³R) + (4K/√h)(π_ijπ^ij − ½π²) + √h D·P + √h W + (γ_L/2)√h (D·P)²]
              − √h μ_K²(1 − N)²/(2K N) + N^i H_i },     π_P ≈ 0 (primary, η = 0).

Hand expectation, stated so it cannot steer: N enters non-linearly (K(Q)) and P is auxiliary, so the chain is
primaries π_N, π_i, π_P → secondaries C_N = δH_T/δN, H_i, φ_P = δH_T/δP → **no tertiary** when the (N, P) Hessian A of
H_T is invertible; π_i, H_i first class, the other 8 second class, DOF (26 − 12 − 8)/2 = 3. With frozen coefficients
A = [[a, c†], [c, B]], a = −μ_K²/(K N₀³), c = (1 + γ_Lρ₀) i k + g₀ (ρ₀ = D·P₀, g₀ = W′K P̂₀), B = N₀(K M + γ_L k kᵀ),
M = M_L P̂P̂ + M_T(1 − P̂P̂), M_T = 1 + x, M_L = (1 + x)²; Schur S = a − (1+γ_Lρ₀)² kᵀB⁻¹k − g₀ᵀB⁻¹g₀ ≤ 0, so
det A = det B · S < 0 except on the locus {μ_K = 0, P₀ = 0, (k = 0 or γ_Lρ₀ = −1)}. I expect H4's ρ_τ < 0 regions to sit
nowhere near that locus (γ_L|ρ| ~ 1e-12), i.e. H4's ill-posedness is a dynamical instability of the one scalar, not a
change of constraint rank.

## 1. Checks (`v3_dirac.py`, sympy + numpy; `--mutate` deletes the clock term)

- **V1 (Dirac chain, exact reduced scalar sector k ∥ x, A7 machinery).** Fields a, b, P_x, N, N^x and momenta; ³R exact
  for diag(1+a, 1+b, 1+b); W to the order fixing second derivatives at P = 0. Constraints {π_N, π_s, Π, C_N, H_x, φ_P}.
  Backgrounds: **B1** Minkowski, μ_K = 0; **B2** Minkowski, μ_K = 0.3; **B3** FRW-like expanding point with BS dust
  (N₀ = 0.9, i.e. Q̄ = 1.11; π^ij = qδ^ij, q from C_N = 0; Λ = 0.5, μ_K = 0.3); **B4** anisotropic (sheared) momentum
  π^xx = q₁ ≠ π^yy = q₂ = 0.4, q₁ from C_N = 0, same dust. k ∈ {0.7, 1.3, 3}; K = 1, γ_L = 0.3. Report det of the multiplier
  matrix A (symbol). **PASS iff** at every background and k: every constraint vanishes at the background, the complex
  rank of the 6×6 Fourier bracket matrix is 4, its identically vanishing rows are exactly {π_s, H_x}, det A ≠ 0 (no
  tertiary) ⇒ 1 scalar DOF per mode (3 in total with the 2 tensor modes). Any rank change ⇒ reported as a
  background-dependent count (FAIL of the expectation, a finding either way).
- **V2 (frozen-coefficient 3D symbol of A, exact W).** (i) sympy: the Hessian of the frozen-coefficient second-order
  density equals the form in §0 and S equals the Schur identity, residual 0. (ii) Sweep: x ∈ logspace(−3, 9, 49);
  γ_Lρ₀ ∈ {−0.9, −0.1, −1e-12, 0, 1e-12, 0.1}; angle(k, P̂₀) ∈ {0, π/4, π/2}; kL★ ∈ logspace(−3, 8, 45);
  μ_K ∈ {0, 1/(100 kpc)}; L★ ∈ {floor 21.7 / 22.9 pc, 24, 90 pc}; both footings (a₀ sets g₀ = a₀x). **PASS iff** det A < 0
  at every sweep point. Reported: min over the sweep of |S| / (lower bound a + (1+γ_Lρ₀)² kᵀB⁻¹k + g₀ᵀB⁻¹g₀), which
  must be 1 to 1e-9, and how small |S| gets relative to K⁻¹k² (the near-degeneracy at large x, reported, no threshold).
- **V3 (J(Y) control, γ_L = 0).** The principal symbol of S equals the lapse Hessian of the J(Y) form,
  (1/(K N₀))[J′k² + 2J″(g·k)²], for J_x = Λ − 2a₀²[y − ln(1+y)], y = √Y/a₀ (residual 0). This is the
  "BS K(Q) and J(Y)" check: the two representations give the same lapse operator.
- **V4 (vs H4's ρ_τ < 0).** From H4's committed `h4_v3_saddle_stability_results.json`, every region's
  max_abs_rho_excl_null and median_abs_rho (f0 and f3, base and fine, both footings) → γ_L|ρ| = 2πG L★²|ρ|/c² at every
  L★ above. **PASS iff** max ≤ 1e-6. Reading: PASS ⇒ "H4's ill-posed regions are ≥ 6 decades from the only degeneracy
  locus; v3's constraint rank is uniform there, so H4's ill-posedness is the reduced scalar's dynamics, not the algebra".
- **V5 (MUTATE, clock term deleted).** Expected: B1 rank 2 (π_N and C_N become first class: lapse gauge again, 0 scalar
  DOF), B2–B4 rank 4 (K(Q)'s lapse mass alone keeps N non-gauge). PASS-as-required iff the B1 rank differs from 4;
  everything else reported.

Not tested: vector/tensor sectors, k ⊥ x on the reduced sector (V2 covers arbitrary k directions, frozen coefficients
only), the sign/health of the reduced scalar Hamiltonian (that is H4's question), matter fields beyond BS dust, the
DBI K (Q7), and anything non-perturbative beyond the frozen-coefficient symbol.
