# DOOR G — X_d CLUSTER ATTEMPT: re-deriving Yarotsky's c1, c2 by tracking the cluster expansion (2026-09-22)

**Mandate:** the I15 many-plaquette rung reduces the volume-uniform strong-coupling window to
`x >= X_d = max(1, sqrt(2 A_d/c1), sqrt(2 c2 A_d))`, `A_d = (32/3)·d(d-1)/2`, with c1, c2 the
constants of Yarotsky's Theorem 1 (arXiv:math-ph/0411042v1 pp. 2-4). Door E established that c1, c2
are existence constants in every accessible layer and that the alleged source of their values
(J. Math. Phys. 45 (2004) 2134-2152, DOI 10.1063/1.1705718, ref. [23] of the arXiv paper) is
inaccessible. Door G is the mandated **re-derivation attempt**: actually track the cluster
expansion of arXiv:math-ph/0411042v1 Section 2 (Lemma 1 -> eq. (14) -> resolvent series (15) ->
spectral estimate (4)-(5)) with explicit constants, for the specific gauge model.

**Verdict (deliverable level 2, with level-1-shaped conditional data and one genuine partial bound):**
the tracking attempt **reduces c1, c2 to ONE unknown constant M** — the constant of the *dressed*
(doubly-exponentiated) cluster remainder — with every other ingredient (sector lemma, cluster counts,
budget sums, the expansion structure, the bridge arithmetic) made explicit and machine-verified,
**and proves that no crude norm-bound route can reach eq. (14)**: the sign-less far-field family sum
`sum_{r>=1} (2r+1)^d eps^{-r}` diverges for every `eps in (0,1)`.  The precise inequality whose
constant this attempt cannot make explicit is stated in Section 6 (hypothesis (D) with sub-inequality
(D-core)).  Conditional on (D), explicit numbers fall out: Section 7.  Nothing in Sections 7 is
claimed as proven.  The only fully proven *new* quantitative statements of this door: Sections 3-4
(lemmas), Section 5 (negative result), Section 8 (volume-dependent explicit gap bound).

---

## 1. The model and the dictionary (from PROOF.md §4, verbatim structure)

- Sites = positively oriented links of the d-dimensional cubic lattice; `H_x = L^2(SU(N), Haar)`.
- Free part per site: `h_x = C_x / C_F` (`C_F = (N^2-1)/(2N) >= 3/4`), gap exactly 1, unique zero vector
  `Omega_x = constant 1` (PROOF.md §2).  The bridge groups the d outgoing links into `H_z`; the
  shift-invariant single-link version is equivalent for the range analysis (S = {0,e_1,...,e_d},
  `|S| = d+1` sites, perturbation range `Lambda_0 = S`).
- Perturbation: `phi_z = -[2 b_N/(x^2 C_F)] sum_{i<j} T_(z,ij)`, `T_p = Re Tr(U_p)/N`, `||T_p|| <= 1`,
  `eta := sup_z ||phi_z|| <= 2 b_N m/(x^2 C_F) <= A_d / x^2`, `m = d(d-1)/2`, `A_d = (32/3) m`,
  using `b_N/C_F <= 16/3`.
- Bridge: for `x >= X_d = max(1, sqrt(2 A_d/c1), sqrt(2 c2 A_d))` one has `eta <= c1/2 < c1` and
  `c2 eta <= 1/2`; Yarotsky Th.1 (5) gives normalized gap `>= 1 - c2 eta >= 1/2`; rescaling by
  `x C_F/2` gives `gap >= x C_F/4 >= 3x/16`.
- Target of this door: **explicit, provable c1, c2** (or the exact blocking inequality).

**Model-specific facts used below (all proven; the first three are in PROOF.md and re-verified here):**
1. `h_x | H_x' >= 1` (gap exactly 1), `H_x' := H_x ⊖ Omega_x`.
2. **Vacuum expectation vanishes**: `<Omega, T_p Omega> = 0` for every plaquette, because
   `E[Tr(U_p)] = Tr(E[U_1...U_4])` and `U_1...U_4` is Haar-distributed (convolution of Haar with
   itself), and `int Tr(g) d mu(g) = 0` for N>=2 (defining rep nontrivial).  Hence
   `<Omega, phi_x Omega> = 0` — the first-order (Wick) renormalization of the perturbation
   **vanishes identically** for this model.  (Numerically sanity-checked; see verify.py.) This
   removes the usual `E_Lambda = <Omega,Phi Omega> + ...` extensive leading term; the remaining
   energy piece is `O(eta * eps * C(d,eps))`-small per site and never blocks the estimates below.
3. `||T_p|| <= 1`; `||phi_x|| <= eta`.
4. `d_I` = minimal length (number of nearest-neighbor edges, auxiliary lattice vertices allowed)
   of a connected graph with vertex set containing I;  `d_{J;I}` = minimal length of a connected
   graph containing J whose vertex set meets I.  (Paper's convention; the lemmas below use only
   monotonicity in J and `d_{J;I} >= dist(J,I)`, which hold for any reasonable reading.)

---

## 2. The source chain to be tracked (arXiv:math-ph/0411042v1, Section 2)

1. Eq. (7): `H_Lambda ⊖ Omega_{Lambda,0} = ⊕_{∅≠I⊂Λ} H'_I ⊗ Omega_{Lambda\I,0}`.
2. Creation operators `û_I v = <v, Omega_{I,0}> u_I` with `û_I û_J = 0` for `I∩J ≠ ∅`.
3. Ground-state ansatz `Omegã_Lambda = exp(Sigma_K v̂_K) Omega_{Lambda,0}`,
   `<Omegã,Omega> = 1`; **Lemma 1** (paper, eq. (8)): for every eps>0, if `eta` is small:
   `max_x Sigma_{I∋x} ||H_{I,0}v_I|| eps^{-(d_I+1)} <= 1`  (so `||v_K|| <= eps^{d_K+1}`).
   *Proof idea only in the arXiv text ("contraction"); the map lives in [23].*
4. Renormalized Hamiltonian (11)-(13): `H̃_Lambda = H̃_{Lambda,0} + Φ̃_Lambda`,
   `Φ̃_Lambda û_I Omegã = Sigma_J ((F_Lambda v_I)_J)̂ Omegã`,
   `(F_Lambda v_I)_J = P_{Lambda,J} exp(-Sigma v̂_K) [Phi_Lambda, v̂_I] exp(Sigma v̂_K) Omega_{Lambda,0}`.
5. **Eq. (14)** (the heart): `Sigma_{J⊂Λ} ||(F_Lambda v_I)_J|| eps^{-(d_{J;I}+1)}
   <= c sup_x ||phi_x||^{|I|} ||v_I||` — "expanding into a commutator series and using Lemma 1,
   one finds (14)".  The constant c: **not tracked anywhere in the arXiv text**; full details
   deferred to [23] (paywalled).
6. `|||·|||`-norm; `|||Φ̃ v||| <= c eta |||H̃_0 v|||`; resolvent series (15) converges for z outside
   `{|z-a| <= c2 eta a}`; Theorem 1 (4)-(5) with `gap >= 1 - c2 eta`.

**The reduction claim of this door**: everything downstream (step 6) is explicit once eq. (14)-type
estimates hold with a constant M (Section 4, Proposition R).  Everything upstream splits into
(a) **provable-with-explicit-constants parts** (Sections 3-4: the sector lemma, the counting lemmas,
the budget sums), and (b) **one unproved link (D)** (Section 6): the *dressed* remainder bound
`Sigma_J eps^{-(d_{J;I}+1)} ||P_J e^{-A}[phi_x,v̂_I]e^{A} Omega|| <= M eta ||v_I||` for the SPECIFIC
model.  The negative result of Section 5 shows (b) is not a formality: its crude (sign-less) analog
diverges, so (D) must use the alternating structure (the `e^{-A}·e^{A}` cancellation), whose
quantitative form this session cannot make explicit.  **That is the first blocking inequality.**

---

## 3. Proven Lemma A (sector/weight monotonicity) — the local core of (14)

For one hex `x+S` (|S| = d+1), one vector `v in H_Lambda`, and the decomposition of `w := phi_x v`
into the excited-sector projections inside the hex: `w = Sigma_{A ⊆ x+S} P_A w` (disjoint sectors `A`
of the hex; `Sigma_A P_A = id` on the hex factor).  Let `J_A := A ⊔ ((I ∪ U) \ (x+S))` for a source set
I and created-support U.  Then, since `J_∅ ⊆ J_A` implies `d_{J_A;I} >= d_{J_∅;I}`:

```
Sigma_{A⊆x+S} eps^{-(d_{J_A;I}+1)} ||P_A w||
    <= eps^{-(d_{J_∅;I}+1)} · 2^{|S|} · ||w||
    <= eps^{-(d_{J_∅;I}+1)} · 2^{|S|} · eta · ||v|| .
```

*Proof.* `d_{·;I}` is monotone in its first argument; `||P_A w|| <= ||w||` for each of the `2^{|S|}`
sectors (subadditivity + orthogonality give `||w|| <= Σ_A||P_A w|| <= 2^{|S|/2}||w||`; we use the
looser `2^{|S|}`); `||phi_x|| <= eta`.  (All steps elementary; the `2^{|S|} = 2^{d+1}` sector factor
is absorbed in the compounded constants q of Section 7.)

**Consequence**: *each single application of one `phi_x` to a product vector contributes exactly one
`eta` and one weight `eps^{-(d_{(I∪U)\S_x;I}+1)}`, with no further sector-count factor.*  (The 2^{|S|}
sector factors DO enter later in the crossed terms, Section 6; they are absorbed in the compounded
constant q of Section 7.)

---

## 4. Proven counting lemmas (all constants explicit; machine-verified, verify.py S1-S2)

**(B1) Cluster count (walk bound).** The number of connected subsets of `Z^d` of size n containing a
fixed site is at most `(2d)^{2(n-1)}`.
*Proof.* Each such set has a spanning tree; the depth-first traversal is a walk of length 2(n-1)
starting at the fixed site whose set of visited vertices contains the set; map set to the (canonical)
walk — injective; # nearest-neighbor walks of length L from a fixed site is `(2d)^L`.
[Degree-2d lattice, so each step has ~2d choices.]
*Machine check:* exact brute-force counts (box `[-3,3]^d`, d=2: n<=8; d=3: n<=4) and an independent
growth-recursion count both satisfy the bound; counts displayed in verify.py output (e.g. d=2:
1,4,18,76,311,1216,...).

**(B2) Shell count.** # sites at `ℓ^∞`-distance r from a fixed site `<= (2r+1)^d`.

**(B3) Budget sums.** With `B(d,eps) := Sigma_{m>=1} (2d)^{2(m-1)} eps^{m+1} = eps^2/(1-4 d^2 eps)`
(geometric series, verified against 2000-term partial sums; convergence iff `eps < 1/(4d^2)`), and
`C_2(d,eps) := [Sigma_{m>=0} (2d)^{2m} eps^{2m+2}]^{1/2} = eps (1 - 4 d^2 eps^2)^{-1/2}`:
- `Sigma_{K∋x} ||v_K|| <= B(d,eps)`  for admissible collections (Lemma-1-type `||v_K|| <= eps^{d_K+1}`);
- `||A|| <= C_2(d,eps)` where `A := Sigma_K v̂_K` (operator norm on the tensor space).
*Proof of the operator-norm line:* `v̂_K` has operator norm `||v_K||` and acts only on the sector
coefficient `< ·, Omega_{K,0}>`; for unit w, `||Aw|| <= (Sigma_K ||v_K||^2)^{1/2} (Sigma_K |<w,Omega_{K,0}>|^2)^{1/2}
<= C_2(d,eps)`; the sector coefficients form a sub-unitary family.  (Cauchy-Schwarz + `||w||=1`.)
Machine-verified values: d=2,3,4 with `eps = 1/(8d^2)`: B = 1.95e-3, 3.86e-4, 1.22e-4; `(2d)^2 eps = 1/2 < 1`.

**Proposition R (the reduction; unconditional).** Grant the dressed-remainder bound (D) of Section 6
with constant M.  Then, with
`L := M·(1+2B(d,eps))·exp(2B(d,eps)(1+B(d,eps)))`,
the pair
`c1 := 1/(2L)`,   `c2 := 4L`
satisfies the bridge contract: for `x >= X_d = max(1, sqrt(2A_d/c1), sqrt(2c2 A_d))` one has
`eta <= A_d/x^2 <= c1/2` and `c2·eta <= 1/2`; hence by PROOF.md §4 the normalized gap is `>= 1/2`
and the physical gap `>= 3x/16`.  (Elementary algebra; machine-checked at the computed X_d in
verify.py S5.  The contraction condition `L·eta < 1` holds automatically for `eta <= c1/2 = 1/(4L)`.)

---

## 5. Proven NEGATIVE RESULT: the crude (sign-less) route to (14) diverges

The natural first attempt: bound `Sigma_J eps^{-(d_{J;I}+1)} ||(F_Lambda v_I)_J||` by the triangle
inequality + Lemma-1-type norm bounds + Lemma A.  The far-field is governed by single-site clusters
`K = {y}` of the ground-state cloud, `||v_K|| <= eps^{d_K+1} = eps`.  For `|y| = r` large:

```
weight of the y-term  <=  eps^{d_K+1} · eps^{-(d_{J;I}+1)}  =  eps · eps^{-(r+1)} = eps^{-r}
summed over the shell:  (2r+1)^d · eps^{-r}  per shell.
```

**Theorem (blocking divergence).** `Sigma_{r>=1} (2r+1)^d eps^{-r} = +∞` for every `eps in (0,1)`.
*Proof.* Each term `(2r+1)^d eps^{-r} >= eps^{-r} -> +∞` (since `eps^{-1} > 1`).
Machine-checked: verify.py S3 prints partial sums through r=59 for d=2,3,4 at several eps values
(e.g. d=2, eps=1/8: partial = 9.3e92 and still growing; d=4, eps=1/(64·16)=9.8e-4: partial = 8.1e185).

**Consequence (precise).** Eq. (14) of the arXiv paper **cannot** be derived from Lemma-1-type
norm bounds + Lemma A + the counting lemmas alone, *no matter how small eps is taken*.  The
`e^{-A} [φ_x, v̂_I] e^{A}` factor (the dressed, alternating expansion; A = the ground-state creation
field) must supply the far-field cancellation.  Equivalently: *the a priori information content of
Lemma 1 (`||v_K|| <= eps^{d_K+1}`, no distance structure relative to I) is provably insufficient*;
the quantitative form of the cancellation is exactly the content that the arXiv text defers to [23]
("expanding this expression into a commutator series and using Lemma 1, one finds that (14)").

Also note (counting obstruction, independent of the alternation): even a *generic* vector w with
`||w|| <= C` cannot satisfy
`Sigma_J eps^{-(d_{J;I}+1)} ||P_J w|| <= C'` via counting, because
`#{J ⊆ Λ : d_{J;I} <= m} >= 2^m` (all subsets of a segment of m sites adjacent to I) — the unweighted
projection sum would have to be split across `>= 2^m` terms with weights `>= eps^{-m}`.  Decay must
come per-J from the *structure of w*, not from counts: this is the "cluster-count reason" in its
exact form.

---

## 6. THE FIRST BLOCKING INEQUALITY (deliverable): hypothesis (D)

**Statement (D) — dressed remainder bound (unproved in this attempt).**
There exist `M = M(d,eps) < ∞` and an admissible `eps = eps(d) in (0, 1/(4d^2))` such that **for the
specific gauge model** (`phi_x` = group of m plaquette trace terms at the hex `x+S`; `||phi_x|| <= eta`;
ground-state cloud admissible in the Lemma-1 sense) and for every source `I`, every `v_I in H'_I`:

```
(D)   Sigma_{J⊂Λ} eps^{-(d_{J;I}+1)} ||P_{Λ,J} ( e^{-A} [phi_x, v̂_I] e^{A} Ω_{Λ,0} )||
        <=  M · eta · ||v_I|| ,
      A := Sigma_K v̂_K  (the ground-state creation field).
```

Why this is where the attempt stops — the exact sub-inequality whose constant I cannot make explicit:

**(D-core).** Expanding `e^{-A} B e^A = Sigma_{n>=0} (-1)^n/n! (ad_A)^n B`, `B := [phi_x, v̂_I]`, the
remainder bound needs, for the far shells, a quantitative statement of the *alternating* family sums:

```
(D-core)   For each shell r >= 1 of J at distance r from I:
   Sigma_{J: shell r} eps^{-(d_{J;I}+1)} ||P_J ( e^{-A} B e^A - B ) Omega||
        <=  (2r+1)^d · eps^{-r} · rho^r · eta · ||v_I|| · q_0 ,
```

with `q_0 = q_0(d, eps)` a compounded constant (walk-bound counts, sector factors) and the crucial
per-shell decay factor `rho < eps`, so the r-series is geometric with ratio `< 1/2`.  **Not proved
here, and not a formality**:
(i) every route through the triangle inequality + norm bounds + Section 4 lemmas provably diverges
(Section 5);
(ii) *tuning eps does not help*: even the most favourable norm-level input `||A|| <= C_2(d,eps) ~= eps`
turns the natural candidate decay into `(2||A||(2d)^2/eps)^r ~ (8 d^2)^r >= 1` — the margin is
**eps-independent** at the crudest level.  Obtaining `rho < eps` is exactly the "dressed cancellation":
the alternating signs in `e^{-A} · e^{A}` with the fixed-point ground-state cloud `{v_K}` (Lemma 1's
vector is NOT a generic admissible collection — it solves the fixed-point equation whose coefficients
carry the decay).  The quantitative consequence is content of [23] (the arXiv text: "expanding this
expression into a commutator series and using Lemma 1, one finds (14)", with no estimate displayed);
this session cannot supply it;
(iii) secondary datum: even the RHS form of (14) is ambiguous in the arXiv text
(`c sup||phi||^{|I|} ||v_I||` — the |I| exponent cannot be checked without [23]); the doorG reduction
uses the LHS-with-weights form (D), which is what the resolvent step (15) needs.

If and when (D) is proven with constant M, Proposition R + the counting machinery deliver explicit
c1, c2, X_d mechanically.  **Until then, no constant in Section 7 is claimed.**

---

## 7. Conditional numbers (what (D) + the lemmas WOULD give; clearly NOT proven)

With the natural compounded counting constant `q(d,eps) = 2^{d+4}·e·B(d,eps)·(1+B(d,eps))^2·d` and
`eps(d)` chosen so that `q/eps = 1/2` (then `M <= rou(d) := Sigma_{r>=1} (2r+1)^d 2^{-r}`), verify.py S4-S5
computes:

| d | eps(d)      | B(d,eps)   | rou(d) | cond. c1    | cond. c2    | **cond. X_d** |
|---|-------------|------------|--------|-------------|-------------|---------------|
| 2 | 1.40e-3     | 2.02e-6    | 33     | 1.52e-2     | 132         | **~53.1**     |
| 3 | 4.71e-4     | 2.26e-7    | 293    | 1.71e-3     | 1172        | **~274**      |
| 4 | 1.78e-4     | 3.19e-8    | 3393   | 1.47e-4     | 13572       | **~1318**     |

Both bridge conditions re-verified at `x = X_d` (eta <= c1/2 and c2·eta <= 1/2; verify.py S5 prints
the checks).  These numbers are the honest *shape of the answer if (D) holds with natural constants*:
explicit, monotonically degrading with d, and numerically stable.  They are **conditional on an
unproved inequality**; the task's humility rule binds: no X_d here is asserted as a theorem.

---

## 8. A proven partial bound (volume-dependent, fully explicit)

On any finite open subgraph with P plaquettes, in the physical (gauge-invariant) sector:
- `E_1(H_Λ) >= E_1(H_E) - ||H_B|| = (x/2) C_F - 2 b_N P/x`  (Weyl; `H_E = (x/2)ΣC`,
  `0 <= 1 - T_p <= 2`;  the physical sector respects the bound since `E_1^phys >= E_1^full`),
- `E_0(H_Λ) <= <1, H_Λ 1> = (b_N/x) Σ_p (1 - <1,T_p1>) = (b_N/x) P`  (trial vector 1; `<1,T_p1>=0`,
  Section 1 fact 2),
- therefore  **`gap(H_Λ) >= (x/2) C_F - 3 b_N P(Λ)/x`**,
- and `gap >= 3x/16` whenever  `x^2 >= 3 b_N P(Λ)/(C_F/2 - 3/16)`,
  i.e. (using `C_F >= 3/4`) whenever `x >= 4 sqrt(b_N P(Λ))`.

(Elementary; constants exact; volume-dependent — it does NOT bound a uniform X_d, but it is a fully
explicit strong-coupling window for each finite volume, the strongest volume-dependent statement of
this type on record in this repo, and it is proven.)

---

## 9. What this door changed for the bridge

- **Upgrade from door E**: the obstruction is no longer merely "c1, c2 live in a paywalled paper".
  This door proves: (i) the expansion **reduces** c1, c2 to a single parameter (D); (ii) every
  ingredient except (D) is explicitly trackable (Sections 3-4, with machine-verified constants);
  (iii) the crude route to (D)/(14) is **provably closed** (divergent far-field series, Section 5) —
  so the honest statement is now: *the quantitative constants of the alternating dressed cluster
  expansion (the content of [23]) are the exact missing quantity*; (iv) conditional numbers X_2 ~ 53,
  X_3 ~ 274, X_4 ~ 1318 exist and are recorded as conditional (Section 7).
- **Rescue lanes unchanged**: prove (D) (research-level cluster-expansion lemma, 10-20 pages of
  estimates, tractable by the standard Malyshev-Kirkwood machinery with the counting lemmas of
  Section 4 as input), or the separate all-hands route (OS-type explicit strong-coupling expansion;
  door E §4 documents none exists in the literature).
- **No theorem in PROOF.md is changed**: I15 stands audited: gap exists uniformly in N and volume for
  `x >= X_d`, X_d finite but numerically unevaluated; this door records the exact boundary of what is
  provable from the accessible record plus this session's work.

## 10. Files

- `opus_49_doorG/Xd_CLUSTER_ATTEMPT.md` — this report.
- `opus_49_doorG/verify.py` — runnable verification: S1 exact cluster counts vs walk bound; S2 budget
  sums (closed form vs partial sum); S3 the divergent far-field partial sums (the negative result);
  S4-S5 the conditional (D)-based tables with the bridge-condition re-checks; S6 doorE arithmetic
  re-verification (`A_d` exact; consolidation identity).  Run: `python3 verify.py` ->
  "ALL PROVEN CHECKS PASSED".  (The conditional sections print their hypothesis labelling inline.)
- Commit `opus_49d doorG X_d CLUSTER ATTEMPT` — new folder only.