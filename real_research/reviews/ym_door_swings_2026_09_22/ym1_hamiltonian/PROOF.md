# D-YM1 (Hamiltonian door): an explicit, volume-uniform strong-coupling gap

**Status.** Analytic proof, self-reviewed, then independently reviewed
(see `REVIEW.md`). The external leaves are all standard and openly
available:

- Ueltschi, *Cluster expansions and correlation functions*, Moscow Math.
  J. 4 (2004) 511–522, arXiv:math-ph/0304003v3, **Theorem 1**. This is a
  Kotecký–Preiss criterion for polymers in a general measure space.
- The Dyson expansion for a bounded perturbation of a semibounded
  self-adjoint operator.
- Perron–Frobenius for positivity-improving semigroups (Reed–Simon IV,
  Thms XIII.44–45).
- The Casimir minimum C_F = (N²−1)/(2N), proved in I15 §2.

Every scalar inequality below is evaluated in `verify.py` (60-digit
arithmetic, `results.json`).

**What it closes.** I15 §4 proved a gap for x ≥ X_d, but only by applying
Yarotsky's theorem, whose constants c1 and c2 are existence constants. It
registered "a useful explicit X_d" as open (door D-YM1), with the unlock
condition "lawful access to J. Math. Phys. 45 (2004) 2134, or a cluster
expansion with tracked constants". This file supplies the second option.
Yarotsky's paper is not used.

**What it does not do.** It is a fixed-lattice-spacing, strong-coupling
statement (x ≥ 131–227). It says nothing about the scaling window, the
continuum limit or the Clay problem (door D-YM2; see `../ym2_continuum/`).
No novelty is claimed for the method: space-time cluster expansions of this
kind go back to Ginibre, Kennedy–Tasaki, Borgs–Kotecký–Ueltschi and
Yarotsky. The only new content is that the constants are tracked for this
model.

---

## 1. Model and theorem

Fix d ≥ 2 and N ≥ 2, and let G = SU(N). Let E be a finite set of
positively oriented links of ℤ^d. Let P be a set of elementary plaquettes
whose four links all lie in E; P may be any selection. This covers every
finite open subgraph of I15 §4. The Hilbert space is the unconstrained
tensor product ℋ = ⊗_{l∈E} L²(G, Haar). The Hamiltonian is the I15
Hamiltonian

    H_I15 = (x/2) Σ_l C_l + (b_N/x) Σ_p (1 − T_p),    T_p = Re Tr(U_p)/N,

with 0 ≤ b_N ≤ 2N and x = g² > 0. Divide by x/2:

    H := (2/x) H_I15 = H_0 + λ Σ_p (1 − T_p),   H_0 = Σ_l C_l,   λ = 2 b_N / x².

**Theorem 1.** Put b = C_F/2, G = 7/100, a_1 = 4G²,
c = (C_F − b)/(1+G+G²) and a_2 = cG(1+G). Define

    λ_*(d) := G c e^{−a_1} / (32 (d−1) (1+G)^7)  =  C_F · 6.2137×10⁻⁴/(d−1).

If λ ≤ λ_*(d), the following hold for every finite (E, P):

- E_0(H) is a simple eigenvalue.
- The ground state Ω is strictly positive and gauge invariant.
- spec(H) ∩ (E_0, E_0 + b) = ∅.

Consequently, both on ℋ and on the gauge-invariant subspace,

    gap(H_I15) ≥ (x/2)·(C_F/2) = x C_F/4 ≥ 3x/16.

**Corollary (explicit X_d).** For b_N ≤ 2N we have λ/C_F = 2b_N/(x² C_F)
≤ (32/3)/x². So Theorem 1 applies for all N ≥ 2 whenever x ≥ X_d, with

| | X_2 | X_3 | X_4 |
|---|---|---|---|
| uniform in N (b_N ≤ 2N) | 131.1 | 185.3 | 227.0 |
| SU(2), b = 2 (YM05 normalisation) | 92.7 | 131.1 | 160.5 |
| SU(3), b = 2 | 69.5 | 98.3 | 120.4 |
| SU(3), b = N | 85.1 | 120.4 | 147.4 |

(`verify.py`, `results.json` → `headline`, with values rounded **up** to
one decimal; for example 131.02 → 131.1). These are sufficient thresholds,
not optimal ones. They replace I15's "finite but numerically
unspecified X_d" with numbers.

---

## 2. Elementary facts

**(F1) Link spectrum.** On L²(G), C ≥ 0 and ker C is the constants. On the
orthogonal complement, C ≥ C_F = (N²−1)/(2N) ≥ 3/4 (I15 §2). Let P_l be the
projection of the l-th factor onto the constants, and Q_l = 1 − P_l. For
S ⊂ E, put Π_S = ∏_{l∈S} Q_l ∏_{l∉S} P_l. The Π_S are commuting
orthogonal projections with Σ_S Π_S = 1. They commute with H_0, and

    ‖Π_S e^{−sH_0}‖ ≤ e^{−s C_F |S|}   (s ≥ 0).

**(F2) Plaquette operators.** ‖T_p‖ ≤ 1. For l ∉ p, T_p commutes with P_l
and Q_l. For l ∈ p,

    P_l T_p P_l = 0.

*Proof.* Consider T_p as a function of U_l with the other links fixed. It
is a linear combination of matrix elements of U_l in the fundamental
representation and in the antifundamental representation, since
U_l^{-1} = U_l^† when the link is reversed. By Schur orthogonality, the
Haar integral of every matrix element of a nontrivial irreducible
representation vanishes. So the Haar integral of T_p over U_l is zero, and
P_l M_f P_l = (∫ f dU_l) P_l for a multiplication operator M_f. ∎

**(F3) Perron–Frobenius.** H = −Δ_M + W on the compact connected Riemannian
manifold M = G^E. Here C_l is the Laplace–Beltrami operator of the
bi-invariant metric normalised by tr(t_a t_b) = δ_ab/2, and W is a bounded
multiplication operator.

The heat kernel of M is continuous and strictly positive for t > 0, so
e^{−tH_0} is positivity improving. Because W is bounded, e^{−tH} is
positivity improving as well (Reed–Simon IV, Thm XIII.45). H has compact
resolvent. So E_0 is a simple eigenvalue with an a.e. strictly positive
eigenvector Ω (Thm XIII.44), and in particular ⟨1, Ω⟩ > 0.

Gauge transformations act by measure-preserving diffeomorphisms of M,
which preserve positivity, and they commute with H. So gΩ is again a
positive normalised ground state, and hence gΩ = Ω.

**(F4) Spectral criterion.** Let ψ ⊥ Ω, and suppose
⟨ψ, e^{−t(H−E_0)}ψ⟩ ≤ C_ψ e^{−bt} for all t ≥ 0. Then the spectral measure
of ψ for H − E_0 gives zero mass to [0, b). Otherwise
∫ e^{−tE} dν_ψ ≥ ν_ψ([0, b−ε]) e^{−t(b−ε)} for some ε > 0, which contradicts
the bound as t → ∞. If this holds for every ψ ⊥ Ω, then
spec(H) ∩ (E_0, E_0 + b) = ∅.

---

## 3. Dyson expansion and the event graph

Let V = Σ_p T_p, so H = H_0 + λ|P| − λV. Since ‖V‖ ≤ |P| and
‖e^{−sH_0}‖ ≤ 1, the Dyson series converges absolutely for every t > 0 and
all φ, ψ ∈ ℋ:

    ⟨φ, e^{−t(H_0−λV)} ψ⟩ = Σ_{n≥0} λ^n Σ_{p_1..p_n} ∫_{0<s_1<…<s_n<t}
          ⟨φ, e^{−(t−s_n)H_0} T_{p_n} ⋯ T_{p_1} e^{−s_1 H_0} ψ⟩ ds_1⋯ds_n.   (3.1)

In each of the n+1 intervals, insert 1 = Σ_S Π_S next to the heat factor.
A **configuration** ω consists of events (p_k, s_k), k = 1..n, together
with Q-sets S_0, …, S_n, where S_k is the Q-set on (s_k, s_{k+1}),
s_0 = 0 and s_{n+1} = t. By (F2), a term vanishes unless

- S_k Δ S_{k−1} ⊂ p_k, because T_{p_k} commutes with P_l and Q_l for l ∉ p_k;
- p_k ⊂ S_{k−1} ∪ S_k, which is admissibility: no link of p_k is P both
  just before and just after the event.

The value of ω is
λ^n ⟨φ, Π_{S_n}e^{−(t−s_n)H_0}T_{p_n}Π_{S_{n−1}}⋯T_{p_1}Π_{S_0}e^{−s_1H_0}ψ⟩.

**Event graph 𝔊(ω).** Its vertices are the events plus two boundary
vertices ∂_0 (time 0) and ∂_t (time t). The *touch times* of a link l are
0, t, and the times of events whose plaquette contains l. Between two
consecutive touch times the P/Q state of l is constant. Each such interval
on which l is Q is an **edge** of 𝔊 joining the two touch vertices; its
length is the interval length.

Write ℓ(ω) = Σ(edge lengths) = ∫_0^t |S(s)| ds. An event has at most 8
edge-ends (one "before" and one "after" per link of its plaquette). By
admissibility it has at least one on each of its 4 links.

---

## 4. Polymers and factorisation

A **(bulk) polymer** γ consists of m ≥ 1 events (q_i, r_i), with times in
(0, t), and an admissible post-event P/Q label for each event and each of
its 4 links. The labels are subject to two conditions:

- every link is P before the first event touching it and after the last;
- the event graph of γ (edges = its own Q-intervals) is connected.

Define:

- supp γ ⊂ E × ℝ, the union of the closed segments {l} × [u, v] over the
  edges of γ;
- m(γ), the number of events;
- ℓ(γ), the total edge length;
- ext(γ) = max r_i − min r_i, the time extent.

Since the edges of a connected graph cover [min r_i, max r_i], and every
covered instant has at least one Q-link,

    ext(γ) ≤ ℓ(γ).                                                        (4.1)

The **weight** of γ is w(γ) = λ^m ⟨1, X_γ 1⟩. Here 1 is the constant
function (all links P), and X_γ is the time-ordered product of the
T_{q_i} with the heat factors and projections Π_{S^γ}, where S^γ is γ's
own Q-set. By (F1) and ‖T‖ ≤ 1,

    |w(γ)| ≤ λ^m e^{−C_F ℓ(γ)}.                                           (4.2)

Two polymers are **compatible** if their supports are disjoint. Set
ζ(γ, γ') = −1 if they are incompatible and 0 otherwise. Note that
ζ(γ, γ) = −1.

**Lemma 4.1 (factorisation).** Consider configurations ω with
S_0 = S_n = ∅ (vacuum at both ends). The connected components of 𝔊(ω) are
pairwise compatible polymers, and value(ω) = ∏ w(components). Conversely,
every finite family of pairwise compatible polymers arises from exactly one
such ω. This holds outside a null set of coinciding times.

*Proof.* **Values.** Write each P_l = |1_l⟩⟨1_l|. Along the time axis of
link l, every instant at which l is P cuts the tensor network formed by the
operator product with a rank-one factor. After all cuts, the network is a
disjoint union of pieces. Each piece is one component of 𝔊(ω): its events
(T-tensors) together with its Q-edges (factors Q_l e^{−sC_l}). On P-stretches
the heat factor acts trivially, since C_l 1_l = 0.

The contraction of a disconnected network is the product of the
contractions of its pieces. The contraction of a piece is exactly
⟨1, X_γ 1⟩, because in X_γ every link outside γ's Q-edges is P.

**Bijection.** Components of 𝔊(ω) have disjoint supports up to coinciding
touch times, which form a null set. Conversely, overlay a compatible
family. If a Q-edge of γ' on link l covered an event time of γ on a
plaquette containing l, then (l, r) would lie in both supports, since event
points are endpoints of γ's edges by admissibility. So each event of γ sees
exactly γ's labels on its links, all other polymers being P there. The
components of the overlay are therefore the given polymers.

**Measures.** The Lebesgue–Poisson measure of the event set of ω factorises
over its components, which accounts for the 1/n! of unordered families. ∎

Consequently, with dμ(γ) = w(γ) dμ_0(γ), where μ_0 counts plaquettes and
labels and uses Lebesgue measure on the ordered event times,

    Z_t := ⟨1, e^{−t(H_0−λV)} 1⟩
         = Σ_{n≥0} (1/n!) ∫ dμ(γ_1)⋯dμ(γ_n) ∏_{i<j} (1 + ζ(γ_i, γ_j)).     (4.3)

This is exactly Ueltschi's form (1). Note that Z_t > 0 by (F3).

---

## 5. Tree bounds

Fix numbers c > 0 and a_1 ≥ 0. Set

    κ := 2(d−1) · 16 · λ e^{a_1} / c,   K* := 6^6/7^7 = 0.056653,

and assume κ ≤ K*. Let G be the smallest root in [0, 1/6] of

    G = κ(1+G)^7.

The root exists and is unique because u ↦ u/(1+u)^7 increases on [0, 1/6]
to its maximum K*. It is also the limit of the monotone iteration
G_{j+1} = κ(1+G_j)^7 started from G_0 = 0.

The weights below are |w(γ)| e^{a_1 m(γ) + (C_F − c) ℓ(γ)}. By (4.2) they
are at most λ^m e^{a_1 m} e^{−c ℓ(γ)}.

**Lemma 5.1 (event density).** For a plaquette p and a time r, the density
at (p, r) of polymers having an event there satisfies

    ∫ dμ_0(γ) |w| e^{a_1 m + (C_F−c)ℓ} #{events of γ at p with time in I} ≤ R |I|,
    R := 16 λ e^{a_1} (1+G)^8.

**Lemma 5.2 (covering density).** For a link l and a time s,

    A := ∫ dμ_0(γ) |w| e^{a_1 m + (C_F−c)ℓ} #{edges of γ on l containing s} ≤ G².

*Proof of both.* Each (link, before/after) slot of an event carries at
most one graph edge, since exactly one Q-interval of that link ends, or
begins, at that event. So the event graph has maximum degree 8. Fix a
spanning tree of γ's event graph. Only the tree
edges are kept in the bound e^{−cℓ} ≤ ∏_{tree edges} e^{−c|e|}, since the
others contribute factors ≤ 1. The labels contribute at most 2⁴ = 16 per
event: a link that is P before the event is forced to Q after it, so only
links that are Q before have two choices.

γ is determined by its events and labels, and the tree is extra structure,
so the sum over γ is bounded by a sum over rooted, slot-labelled trees. The
slots of a node are its (link, before/after) pairs: 8 for the root and 7
for any other node, one slot being used by the edge to its parent.

A slot (l, after) of a node at time r either is empty or carries a child.
The child is an event on one of the ≤ 2(d−1) plaquettes containing l, at
time r' > r, reached by an edge of weight e^{−c(r'−r)}, and its own parent
slot is (l, before). Slot (l, before) is handled symmetrically with r' < r.
Integrating over r' gives 1/c per edge. Let F be the total weight of a
non-root subtree, including its node factor 16λe^{a_1}. Then F is bounded
by the fixed point of

    F = 16 λ e^{a_1} (1 + 2(d−1)F/c)^7,  i.e.  G := 2(d−1)F/c = κ(1+G)^7.

This holds by induction on depth: the depth-j truncations increase to the
smallest root. The root with 8 free slots gives R. For Lemma 5.2, choose
the spanning tree to contain the covering edge (u, v), with u at time r < s
and v at time r' > s. Both endpoints then carry 7 free slots, and

    A ≤ [2(d−1)·16λe^{a_1}(1+G)^7]² ∫_{r<s}∫_{r'>s} e^{−c(r'−r)} = (2(d−1)F/c)² = G². ∎

---

## 6. The Kotecký–Preiss condition

Let b ≥ 0 be the decay rate we are after, let a_2 ≥ 0, and put
c := C_F − a_2 − b > 0. Define

    a(γ) := a_1 m(γ) + a_2 ℓ(γ),     μ_b := e^{b·ext} μ.

**Lemma 6.1 (contacts).** Let X be a polymer, or a boundary component as in
§7 (a set of events and Q-edges, some of which may start at time 0 or end
at time t). Then

    ∫ d|μ_b|(γ') |ζ(X, γ')| e^{a(γ')} ≤ 2(d−1) R ℓ(X) + G² · #edges(X),

where R and G are those of §5 with this c.

*Proof.* By (4.1), |w| e^{a + b·ext} ≤ |w| e^{a_1 m + (a_2+b) ℓ}, and
a_2 + b = C_F − c, which is the weight of §5.

Suppose γ' ≁ X. Then some link l carries an edge [u, v] of X and an edge
[u', v'] of γ' that intersect. There are two cases:

- u' ∈ [u, v]. The edges of bulk polymers start at events, so u' is the
  time of an event of γ' on a plaquette containing l, and it lies in
  [u, v].
- u' < u ≤ v'. Then γ' has an edge on l containing the time u.

So 1[γ' ≁ X] is at most the sum over edges [u, v] of X of the numbers of
such events plus the numbers of such edges. Integrating with Lemmas 5.1 and
5.2 bounds each edge's contribution by 2(d−1) R (v − u) + G², which gives
the claim. ∎

For a bulk polymer, #edges ≤ 4m, since each edge has an "after" end at an
event and each event has 4 "after" slots. Therefore the **Kotecký–Preiss
condition** for μ_b,

    ∫ d|μ_b|(γ') |ζ(γ, γ')| e^{a(γ')} ≤ a(γ)   for all γ,                (6.1)

holds as soon as

    a_2 ≥ 2(d−1) R   and   a_1 ≥ 4 G².                                    (6.2)

**Parameter choice.** Take b = C_F/2, G = 7/100, a_1 = 4G²,
c = (C_F − b)/(1+G+G²) and a_2 = cG(1+G). Then c = C_F − a_2 − b.

Choose λ = λ_*(d) as in Theorem 1. Then κ = G/(1+G)^7 ≤ K*, and G is the
smallest root. Moreover 2(d−1)R = κ c (1+G)^8 = c G (1+G) = a_2, so (6.2)
holds with equality in the first condition. `verify.py` checks every one
of these identities in 60-digit arithmetic.

For λ < λ_*(d), κ decreases and so does its root, while a_1 and a_2 are
kept fixed, so (6.2) continues to hold.

**Consequences (Ueltschi 2004, Theorem 1).** Theorem 1 has two
hypotheses besides (3), and both hold here. First, |1 + ζ| ≤ 1, since
ζ ∈ {0, −1}. Second, ∫ d|μ_b| e^{a} < ∞, which holds in finite volume at
finite t by the tree bounds. Since |μ| ≤ |μ_b|, condition (6.1) also
holds for μ and for any restriction of μ.

The bound behind all three consequences below is the following. By
symmetry of ϕ, and by Theorem 1's (4) applied to μ_b (whose ϕ contains
1/n!, with n = 1 giving 1),

    Σ_n ∫ d|μ_b|^n |ϕ(A_1..A_n)| Σ_i |ζ(X, A_i)|
        = Σ_n n ∫ d|μ_b|(A_1)|ζ(X, A_1)| ∫ d|μ_b|^{n−1} |ϕ(A_1..A_n)|
        ≤ ∫ d|μ_b|(A_1) |ζ(X, A_1)| e^{a(A_1)} =: K(X).                    (6.3)

This is Ueltschi's (5), with a set X in place of a polymer. Theorem 1 then gives
absolutely convergent cluster expansions of log Z_t and of log Z_t[X] for
every set X. Here Z_t[X] is the partition function (4.3) restricted to
polymers compatible with X, and the cluster sums use Ueltschi's function ϕ.
Theorem 1's bound (4), applied to μ_b and combined with Lemma 6.1, yields
three consequences.

**(C1)** |log Z_t − log Z_t[X]| ≤ K(X), where

    K(X) := ∫ d|μ_b| |ζ(X, ·)| e^{a} ≤ a_2 ℓ(X) + G² #edges(X).

**(C2)** Suppose X lies in times [0, s_X] and Y in times [s_Y, t]. Clusters
meeting both have time extents whose union covers [s_X, s_Y], since
incompatible polymers have intersecting time extents. Hence
Σ ext ≥ (s_Y − s_X)_+, and

    |log ζ_t(X∪Y) − log ζ_t(X) − log ζ_t(Y)| ≤ e^{−b(s_Y−s_X)_+} K(X),

where ζ_t(X) := Z_t[X]/Z_t. The left side is exactly the sum over clusters
containing a polymer ≁ X and a polymer ≁ Y, by inclusion–exclusion on the
indicator "some polymer ≁ ·".

**(C3)** For X in times [0, s_X] and t < t',

    |log ζ_{t'}(X) − log ζ_t(X)| ≤ e^{−b(t−s_X)} K(X).

The difference consists of the clusters of the (0, t') system that meet X
and leave (0, t).

---

## 7. From the cluster expansion to the gap

Take arbitrary φ, ψ ∈ ℋ and expand ⟨φ, e^{−t(H_0−λV)}ψ⟩ by (3.1), now
allowing S_0 and S_n to be arbitrary. The vector ψ enters only through
(⊗_{l∉S_0}⟨1_l|) Π_{S_0} ψ, a tensor on the legs in S_0. All of these legs
are edges at ∂_0, and similarly for φ at ∂_t. So cutting at P-instants
leaves:

- bulk polymers;
- either one component Γ_{0t} containing both ∂_0 and ∂_t, or two
  components Γ_0 ∋ ∂_0 and Γ_t ∋ ∂_t.

Here Γ_0 = {∂_0} if S_0 = ∅. As in Lemma 4.1, the value factorises:

    ⟨φ, e^{−t(H_0−λV)}ψ⟩ = Σ_{Γ_0 ~ Γ_t} v(Γ_0) v(Γ_t) Z_t[Γ_0∪Γ_t] + Σ_{Γ_{0t}} v(Γ_{0t}) Z_t[Γ_{0t}],   (7.1)

where v(Γ_0) = λ^m ⟨1, X_{Γ_0} ψ⟩ and so on. By (F1),

    |v(Γ_0)| ≤ λ^m ‖Π_{S_0}ψ‖ e^{−C_F ℓ(Γ_0)},

and similarly for the others. Γ_0 is connected through ∂_0, so its edges
cover [0, s_0], where s_0 is its last time. Hence
ext(Γ_0) := s_0 ≤ ℓ(Γ_0). Likewise ext(Γ_t) := t − s_t ≤ ℓ(Γ_t) and
ext(Γ_{0t}) = t ≤ ℓ(Γ_{0t}).

**Boundary sums.** Put

- c_B := C_F − b − 3a_2 > 0;
- κ_B := 32(d−1) λ e^{3a_1}/c_B, and require κ_B < K*;
- G_B := the smallest root of G_B = κ_B(1+G_B)^7.

Using (C1), #edges(Γ_0) ≤ 4m + |S_0| and the tree bound of §5, rooted at
∂_0 with one slot per link of S_0:

    B(ψ) := Σ∫_{Γ_0} |v(Γ_0)| e^{b·ext(Γ_0) + 3K(Γ_0)}
          ≤ Σ_{S_0⊂E} ‖Π_{S_0}ψ‖ (e^{3G²}(1+G_B))^{|S_0|} ≤ 2^{|E|} (e^{3G²}(1+G_B))^{|E|} ‖ψ‖,   (7.2)

uniformly in t. The corresponding sum for Γ_{0t}, weighted by e^{b·ext + K}, is bounded
uniformly in t. Take the spanning tree from ∂_0; it contains ∂_t. Along
the tree path from ∂_0 to ∂_t, each event node chooses one of its 7 free
slots to continue the path, carries the other 6 as ordinary subtrees, and
reaches its path-child with the usual edge weight. Relative to an
unmarked subtree, each path step therefore costs

    7 κ (1+G)^6 = 7 G/(1+G)

per step. This is < 1 exactly when G < 1/6, i.e. when κ < K*. The
Γ_{0t} term carries only e^{b·ext + K}, so the KP value κ = 0.769 K*
already suffices. The overbound e^{3K}, with κ_B = 0.941 K* and
G_B = 0.1124, also works, and gives a ratio of 0.707.

∂_t has a pinned time, so its incoming edge replaces one factor 1/c by
e^{−c(t−r_k)} ≤ 1. The final edge into
∂_t has weight ≤ 1. ∂_t's other slots contribute (1+G_B) each, and φ
contributes ‖Π_{S_n}φ‖ ≤ ‖φ‖ summed over at most 2^{|E|} sets S_n.

Summing the geometric series over path lengths gives a bound
C_Λ(φ, ψ)/(1 − 0.707), independent of t.

For the certified parameters, κ_B = 0.941 K* (`verify.py`). All these
constants depend on the volume. Only the rate b does not, and only the rate
enters (F4).

**The estimate.** Write R_t(φ, ψ) := ⟨φ, e^{−t(H_0−λV)}ψ⟩ / Z_t,
L_t(ψ) := Σ_{Γ_0} v(Γ_0) ζ_t(Γ_0) and L'_t(φ) := Σ_{Γ_t} v(Γ_t) ζ_t(Γ_t).
Dividing (7.1) by Z_t,

    R_t = L_t L'_t − Σ_{Γ_0 ≁ Γ_t} vvζζ + Σ_{Γ_0 ~ Γ_t} vvζζ (e^{D} − 1) + Σ_{Γ_{0t}} vζ,

with D := log ζ(Γ_0∪Γ_t) − log ζ(Γ_0) − log ζ(Γ_t). Each correction is
O(e^{−bt}):

- **Incompatible pairs.** Here s_0 ≥ s_t, so
  1 ≤ e^{−bt} e^{b·ext(Γ_0) + b·ext(Γ_t)}. With |ζ| ≤ e^{K}, the term is
  bounded by e^{−bt} B(ψ) B(φ).
- **Compatible pairs.** By (C2), |e^D − 1| ≤ |D| e^{|D|} ≤
  e^{−b(s_t−s_0)_+} K(Γ_0) e^{K(Γ_0)}, and
  e^{−b(s_t−s_0)_+} ≤ e^{−bt} e^{b·ext(Γ_0)+b·ext(Γ_t)}. Since K ≤ e^{K},
  the term is bounded by e^{−bt} B(ψ) B(φ).
- **Connecting components.** ext(Γ_{0t}) = t, which gives e^{−bt} times the
  uniformly bounded Γ_{0t} sum.

By (C3), the same bookkeeping shows that L_t(ψ) is Cauchy with rate e^{−bt}:
components Γ_0 that reach beyond t have ext ≥ t. The same holds for L'_t(φ),
because time reflection maps it to the conjugate of L_t(φ), all factors
being self-adjoint. So

    R_t(ψ, ψ) = L(ψ) L'(ψ) + O(e^{−bt}).                                   (7.3)

**Conclusion.** Let N_t := ⟨1, e^{−t(H−E_0)} 1⟩ ∈ (0, 1]. Then
⟨ψ, e^{−t(H−E_0)}ψ⟩ = N_t R_t(ψ, ψ), because e^{−tH} = e^{−λ|P|t} e^{−t(H_0−λV)}.

As t → ∞, the left side tends to |⟨Ω, ψ⟩|², and N_t tends to
|⟨1, Ω⟩|² > 0 by (F3). By (7.3), therefore,
L(ψ)L'(ψ) = |⟨Ω, ψ⟩|² / |⟨1, Ω⟩|².

For ψ ⊥ Ω this vanishes, so

    ⟨ψ, e^{−t(H−E_0)}ψ⟩ ≤ R_t(ψ, ψ) = O(e^{−bt}).

By (F4), spec(H) ∩ (E_0, E_0 + b) = ∅. The gauge-invariant subspace
contains Ω (F3) and is invariant under H, so its gap is at least that of
ℋ. With b = C_F/2 and H_I15 = (x/2)H, this proves Theorem 1. ∎

---

## 8. What changed in the register

- **I15 §4** (existence of X_d, value unknown) is now superseded by explicit
  values. X_3 = 185.3 suffices uniformly in N ≥ 2 and b_N ≤ 2N, with gap
  ≥ 3x/16. The YM05 normalisation (b = 2) gives X_3 = 131.1 for SU(2) and
  98.3 for SU(3).
- **Door D-YM1** is closed by the second unlock route: a cluster
  expansion with tracked constants for this model. Yarotsky's 2004 J. Math.
  Phys. paper is no longer needed. There is still no arXiv copy of it
  (checked 2026-09-22).
- **Still open**, and not touched here:
  - the "x ≥ 2 many-plaquette window" (this proof needs x ≳ 100);
  - the infinite-volume GNS statement with explicit constants. Only the
    finite-volume, volume-uniform statement is proved here, and I15's
    Yarotsky-based infinite-volume statement keeps its non-explicit
    threshold;
  - every continuum question.
- **Scale check.** At x ≥ 131 the proven bound gives an inverse gap of at
  most 16/(3·131.02) ≈ 0.041 lattice spacings. This window is deep in the lattice regime and carries no
  continuum information (see `../ym2_continuum/`).

## 9. Files

- `verify.py` evaluates the scalar conditions (6.2) and the boundary
  condition κ_B < K*, checks the lattice combinatorics and the tree
  constant K*, and prints the X_d table. Exit 0 and `ALL CHECKS PASSED`.
- `results.json` and `run_stdout.txt` hold that run. Only the
  `headline` block, with G = 7/100 and κ_B = 0.941 K*, is certified. The
  grid-optimum rows sit on κ_B ≈ K*, where the Γ_{0t} step needs strict
  inequality, so they are reference only and are not to be quoted.
- `REVIEW.md` holds the independent adversarial review and its resolution.


---

**Addendum 2026-09-23 (append-only).** A parallel, independent swing of the same door,
`real_research/ym1_bdl_extension_2026/` (lane L326, Lean I19, refereed in-repo), follows a different
route. It carries Bravyi–DiVincenzo–Loss (CMP 284 (2008) 481, arXiv:0707.1894), a tracked-constant
Kirkwood–Thomas proof, to Kogut–Susskind SU(N). It gets the sharper thresholds **X₂ ≈ 42.3, X₃ ≈ 59.9,
X₄ ≈ 73.3**, with the same gap form ≥ 3x/16, uniform in N and in finite volume. **Those are the repo's
best explicit thresholds.** This file remains an independent confirmation by a different method, a
space-time polymer expansion on Ueltschi 2004. Its constants are weaker (131/185/227), and it shares none
of its combinatorics with L326. Two independent routes to the same statement is the point of keeping it.
