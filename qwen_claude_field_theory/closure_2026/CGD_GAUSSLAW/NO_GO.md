# CGD/Gauss-Law No-Go Theorem (2026-08-27)

**Theorem (CGD-CANONICAL).** Under the hypotheses of the CGD specification —
(i) E_i local in the ADM canonical variables (h_ij, π^ij) and the intrinsic Ricci ³R_ij, at at
most two spatial derivatives; (ii) no additional propagating scalar or vector degree of freedom;
(iii) matter minimally coupled to the metric g_μν only — the equation

    D_i E^i = 4πG ρ_b

has no solution.

**Proof.** By the ADM canonical decomposition of a minimally-coupled matter action, matter enters
the gravitational Hamiltonian only through T_{00} (in H_⊥) and T_{0i} (in H_i). Any constraint of
the theory that is sourced by matter under minimal coupling is therefore a linear combination of
{H_⊥, H_i, and their spatial derivatives}.

Enumerate the local 1-tensors on the spatial slice at ≤ 2 spatial derivatives built from
(h_ij, π^ij, ³R_ij):

    E1 = D_i K,                    E2 = D^j(π_ij/√h),         E3 = D_i ³R,
    E4 = D^j ³R_ij = ½ D_i ³R,     E5 = D^j(π_ij/√h − α h_ij K),   E6 = D^j(³R_ij − ⅓ h_ij ³R) = ⅙ D_i ³R.

Contracted Bianchi in 3D collapses E4, E6 into E3, leaving three independent divergences:

    D_i E1^i = D² K                 (zero on any CMC slice; else K contaminates H_⊥),
    D_i E2^i = −½ D^i T_{0i}        (momentum-flux source; vanishes for static matter),
    D_i E3^i = 16πG D² ρ_b + D² (K_ij K^ij − K²)   (via H_⊥; Laplacian of density, wrong order).

None equals 4πG ρ_b. □

**Bounded scope.** The theorem does *not* rule out:
- Higher-derivative E_i (≥ 3 spatial derivatives): a new Ostrogradski-degeneracy certification;
- Enlargement of the phase space by an auxiliary field with its own second-class constraint:
  this is the auxiliary-Legendre / MMG route, whose lapse-constraint incarnation was
  independently audited to FAILED (γ_PPN = 0, α_3 = −1, Newtonian-order matter non-conservation);
- Nonminimal matter coupling: explicitly forbidden by the CGD specification.

**Nonlocal localization.** The natural local completion of the required object,
E_i = −D_i ∇^{−2} ³R, uses an inverse Laplacian; the resulting theory is the Deffayet–Woodard
nonlocal class, itself published as a no-go (external-field Cassini quadrupole Q_2 ≈ 2×10^{−26}
s^{−2} versus 5.2×10^{−27} ceiling, 10–14σ; PAPER1 §4.2, DOI 10.5281/zenodo.22132648).

**The emerging structural picture (this session, four independent proofs):**

1. **F(A²) no-go** (sf40/sf41): MOND nonlinearity in a kinetic Hessian ⇒ scalar propagates.
2. **MMG audit** (2026-08-27, commit 8c53d66a): deleting H_⊥ to get 2 DOF ⇒ γ_PPN=0, α_3=−1,
   matter non-conservation.
3. **MMG_REPAIR_A** (commit 2542182b): S_2'=D²(q+ln N) repairs γ_PPN=1 and keeps 2 DOF, but
   C_M still gives α_3 = −3 and flips the deep-MOND source sign (BTFR killed).
4. **CGD no-go** (this document): matter-density source cannot be the divergence of a local
   1-tensor built from ADM phase space at ≤ 2 derivatives.

Together: any local, minimally-coupled, 2-DOF MOND theory must edit the Hamiltonian sector
(⇒ MMG's failure chain), the tensor sector (⇒ c_T ≠ 1 on FLRW, cf. DW), or add higher-derivative
structure (⇒ new Ostrogradski program). These are the honestly-remaining doors.

## Second, independent no-go (2026-08-27) — the natural nonlocal completion also fails

An independent one-shot run (OpenAI) took the natural nonlocal escape of the theorem above
and found a *different* fatal condition, cleanly. The candidate

    E_i = (c²/4) D_i Δ_h^{−1} ³R

has the desired weak-field scalar behavior — around a Newtonian metric ³R^{(1)} ≈ (4/c²)∇²Ψ, so
E_i^{(1)} ≈ ∇_i Ψ, and the CGD equation formally reduces to the target MOND Poisson. But on a
transverse-traceless perturbation h_ij = δ_ij + γ_ij^{TT},

    ³R^{(1)}|_TT = 0 identically  (verified: `scripts/verify_tt_kills_R.py`, exit 0)

because the linearized 3-Ricci scalar collapses to −∂_i∂_j γ^{ij} + ∇² γ^i_i, both terms zero
for TT modes. Hence E_i^{(1)}|_TT = 0, the CGD constitutive potential J(Y=E²) contributes
nothing at O(γ²) to the tensor sector, and the tensor dispersion loses its k² gradient term:

    ω² = 0   (instead of ω² = c² k²)  ⇒  c_T² = 0  or ill-defined.

**This kills the nonlocal completion** — the very escape my local no-go left open. So:

- Local low-derivative CGD (my no-go): fails because no local 1-tensor divergence equals ρ_b.
- Natural nonlocal completion (OpenAI's no-go): fails because ³R^(1)|_TT = 0 kills c_T.

The two obstructions are complementary and cover the CGD architecture's realistic options. The
remaining escapes each carry a specific price (see README §"CANNOT BE REPAIRED").

## The next-move suggestion (from the OpenAI run, banked, not attempted here)

The failure is precise: *one scalar/longitudinal constitutive invariant cannot simultaneously
carry MOND and the tensor gradient.* A genuinely two-channel gravitational constitutive theory
would need to decompose the phase space as

    H = H_TT + H_MOND

with H_TT supplying the ordinary c_T² k² tensor propagation, and H_MOND acting only on a
constrained longitudinal sector to produce D_i D^i = 4πG ρ_b. Making the tensor channel
invisible to the MOND Gauss constraint without introducing a scalar DOF is the hard part; this
is a distinct architecture and belongs to a separate certification program.
