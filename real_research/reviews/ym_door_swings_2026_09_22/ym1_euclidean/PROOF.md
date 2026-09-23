# D-YM1 (Euclidean companion): an explicit Dobrushin mass gap for Wilson SU(N)

**Status.** Elementary proof, self-reviewed and independently reviewed
(`../ym1_hamiltonian/REVIEW.md` covers both doors). It relies on three
external leaves:

- Dobrushin's uniqueness theorem together with Föllmer's covariance
  estimate (H. Föllmer, J. Funct. Anal. 46 (1982) 387; H.-O. Georgii,
  *Gibbs Measures and Phase Transitions*, ch. 8);
- the positive transfer matrix of Wilson lattice gauge theory (M. Lüscher,
  Commun. Math. Phys. 54 (1977) 283; K. Osterwalder and E. Seiler, Ann.
  Phys. 110 (1978) 440);
- Jentzsch/Perron–Frobenius for strictly positive kernels.

`verify.py` checks every numerical ingredient (exit 0, `ALL CHECKS PASSED`).

**No novelty.** Strong-coupling mass gaps for lattice gauge theory are
classical (Osterwalder–Seiler 1978). An explicit, volume-uniform threshold
already exists in the literature. Shen, Zhu and Zhu, Commun. Math. Phys.
400 (2023) 805, arXiv:2204.12737, prove a strictly positive mass gap for
|β_SZZ| < 1/(16(D−1)), where β_SZZ is the coefficient in the action
Nβ Re Tr U_p. In the Wilson normalisation used here this reads
β_W < N²/(16(D−1)), which for SU(3) in D = 4 is 0.1875.

SZZ's rate is not explicit. Their Corollary 1.6 says only that "c_N
depends on K_S, N and d". Remark 4.12 gives c_N ∼ K_S/(d(g)(…)) with
d(g) = N²−1, so the rate degrades with N, and the statement is covariance
decay for cylinder functions. This file adds a one-page, self-contained
route in which the rate, which is N-uniform, is also explicit.

It also refines the register. `opus_49_doorE/REPORT.md` lane (b) states
that no explicit, quantitative, volume-uniform strong-coupling gap theorem
exists for SU(N). SZZ 2023, which that report cites, does have an explicit
threshold for a strictly positive mass gap. What is missing is an explicit
rate, and this file supplies one.

## Theorem

Let D ≥ 2 be the spacetime dimension. Let Λ be a periodic box with every
side ≥ 3, with time extent L_t and a spatial box Λ_s, and consider the
Wilson measure

    dμ(U) ∝ exp(β Σ_p T_p(U)) ∏_l dU_l,     T_p = Re Tr(U_p)/N,

which is the standard β_W, since β_W Σ(1 − T_p) generates the same
measure. Put

    α(β) := 6(D−1) tanh β.

If 0 < β and α < 1, the following holds for every spatial box and
every N ≥ 2. (β > 0 is needed for the transfer matrix to be positive.) The
transfer matrix 𝕋 on the gauge-invariant Hilbert space L²_inv(SU(N)^{E_s})
has a simple top eigenvalue λ_0, and

    m := ln(λ_0/λ_1) ≥ −ln α(β) > 0.

The threshold is 0 < β < artanh(1/(6(D−1))):

| D | 2 | 3 | 4 |
|---|---|---|---|
| β_max (all N) | 0.1682 | 0.0835 | 0.0556 |
| SZZ 2023, SU(3) | 0.5625 | 0.2813 | 0.1875 |

For example, in D = 4 the gap bound is m ≥ 1.71 at β = 0.01 and
m ≥ 1.02 at β = 0.02.

## Proof

1. **TV lemma.** Let ν be a probability measure and p_i ∝ e^{h_i} (i = 1, 2)
   densities with osc(h_1 − h_2) ≤ δ. Then TV(p_1, p_2) ≤ tanh(δ/4).
   Writing g = h_2 − h_1 ∈ [a, a + δ], TV = E_{p_1}(e^g/E e^g − 1)_+, and
   the maximum over laws of g is attained on two-point laws. There it
   equals q(1−q)u/(1+qu) with u = e^δ − 1, whose maximum is
   (e^{δ/2} − 1)/(e^{δ/2} + 1). `verify.py` checks this against brute force.
2. **Influence of one link on another.** The conditional law of U_l is
   ∝ exp(β Σ_{p∋l} T_p). In a periodic box with sides ≥ 3, two distinct
   links lie in at most one common plaquette (checked by enumeration). So
   changing a link l' ≠ l changes a single term β T_p = (β/N) Re Tr(U_l S)
   through its staple S ∈ SU(N). Since |(1/N) Re Tr(UA)| ≤ 1, the change
   has oscillation ≤ 4β in U_l. By step 1, the Dobrushin coefficient is
   C_{ll'} ≤ tanh β. Exactly 6(D−1) links share a plaquette with l (checked
   by enumeration). Hence sup_l Σ_{l'} C_{ll'} ≤ α.
3. **Covariance decay.** If α < 1, Föllmer's estimate gives
   |Cov(f, g)| ≤ ¼ Σ_{i,j} δ_i(f) D_{ij} δ_j(g), with D = Σ_n C^n, where
   δ_i(f) = sup{|f(ω) − f(η)| : ω = η off i}. Using the symmetric majorant
   (tanh β) × adjacency for C avoids any row/column ambiguity. The
   entries of C^n vanish below graph distance n, and the row sums of C^n
   are ≤ α^n. So D_{ij} ≤ α^{dist(i,j)}/(1−α).
4. **Distance between time slices.** Links sharing a plaquette differ by at
   most 1 in time coordinate, where temporal links sit at half-integer
   times. So a spatial link at time 0 and one at time t are at graph
   distance ≥ min(t, L_t − t) (checked by breadth-first search). For
   gauge-invariant functions F, G of the spatial links at times 0 and t,
   this gives
   |⟨F_0 G_t⟩ − ⟨F⟩⟨G⟩| ≤ 4|E_s|² ‖F‖_∞ ‖G‖_∞ α^{min(t, L_t−t)}/(1−α).
5. **Transfer matrix.** Integrating every temporal link, with no gauge
   fixing, gives Z = Tr(𝕋^{L_t}), where 𝕋 = e^{βS_s/2} K_0 P_G e^{βS_s/2}.
   The per-site temporal-link integral is exactly P_G, so Polyakov loops
   are included automatically. Here K_0 is convolution by the
   positive-definite class function e^{β Re Tr g/N}, whose character
   coefficients are positive, and P_G is the gauge projection. So 𝕋 is
   positive and trace class, with a strictly positive continuous kernel on
   L²_inv. By Jentzsch, λ_0 is simple and Ω > 0 (Lüscher 1977;
   Osterwalder–Seiler 1978). Moreover
   ⟨F_0 G_t⟩ = Tr(𝕋^{L_t−t} F 𝕋^t G)/Tr 𝕋^{L_t}.
6. **Limit and spectral argument.** Let L_t → ∞ at fixed Λ_s. For real F,
   step 4 gives Σ_{k≥1} (λ_k/λ_0)^t |⟨k, FΩ⟩|² ≤ C_F α^t for all t. Every
   term is nonnegative, so λ_k/λ_0 ≤ α whenever ⟨k, FΩ⟩ ≠ 0. For a real
   gauge-invariant eigenvector k, take F = k·1{|k| ≤ M}. Then
   ⟨k, FΩ⟩ = ∫ k² 1{|k|≤M} Ω > 0 for large M. Hence λ_1/λ_0 ≤ α. ∎

The spatial volume enters only the prefactor C_F, never the rate. The
threshold is independent of N in this normalisation.

**Exact cross-check (D = 2, SU(2)).** Here the gap on a spatial circle of
L links is m = L ln(I_1(β)/I_2(β)), from the character expansion,
recomputed by quadrature in `verify.py`. It exceeds −ln α at every tested
(β, L).

## Where this sits

This is the same kind of statement as the Hamiltonian door: a fixed
lattice spacing and strong coupling. At β_W = 0.01 (D = 4) the bound gives
a correlation length of at most 0.58 lattice spacings, and the rigorous
windows end at β_W ≈ 0.06–0.19. The SU(3) scaling window starts near
β_W ≈ 5.7, 30–100 times larger, and the continuum limit is β_W → ∞.
Neither statement touches the continuum limit (`../ym2_continuum/`).
