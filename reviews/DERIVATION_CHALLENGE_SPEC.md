# The Derivation Challenge: what would actually pull 32π/3 out of the orbifold

**For:** whoever attempts the computation (another agent, or Carl).
**Status:** this is the ONE well-posed mechanism whose success would convert
Z² = 32π/3 from a *definition* into a *derivation*. Everything else has been ruled out.

---

## Goal (one sentence)

Compute, with **zero tunable continuous parameters**, a radion effective potential
V(L) for the spacetime M₄ × T³/Z₂ whose global minimum sits at the compactification
circumference

    L = Z² ℓ_P = (32π/3) ℓ_P ,   i.e.   x_min ≡ ⟨L⟩/ℓ_P = 32π/3 = 33.5103…

so that 32π/3 comes **out** of the dynamics instead of being put **in**.

---

## Why this is THE mechanism (and not something else)

It was established (see `reviews/forty_invariants_test.py`, `eta_local_bruning_seeley.py`,
`radion_stabilization_test.py`) that:

1. **32π/3 is a length/volume**, not a scale-free invariant. Concretely it is the
   compactification circumference in Planck units: L = 2πR = Z²ℓ_P (the radius is
   R = 16/3 ℓ_P). The π in it is the KK circumference 2π, not a spectral quantity.
2. **Scale-free invariants of the flat orbifold cannot equal it.** Eta = 0; Euler = 4;
   index/signature/torsion/Chern–Simons/Dedekind are rational; the lattice-zeta
   transcendentals (Epstein, Madelung, packing density, …) compute to other numbers.
   40 candidates tested, 0 hits except the definition itself.
3. **The only way a *length* is not simply "chosen" is if it is *dynamically selected*** —
   i.e. the radion (the modulus field whose VEV is the size of the extra dimensions) is
   stabilized at that length by a potential V(L).

So the entire "is Z² derived?" question reduces to exactly one computation:
**is there a parameter-free V(L) with its global minimum at L = 32π/3 ℓ_P?**

---

## The exact object to compute

The one-loop (Casimir / Coleman–Weinberg) radion effective potential:

    V(L) = Λ_bulk·Vol(L)  +  (1/2) Σ_fields (±1) Tr log( −∂² + M_n²(L) ) │_regularized
                           +  V_gravity(L)

- **Sum over all fields** on M₄ × T³/Z₂: SM gauge bosons, the three fermion families,
  the Higgs, and the graviton. Sign +1 for bosons, −1 for fermions.
- **M_n(L) = |n| / L** are the Kaluza–Klein masses, where the momentum vector n runs over
  the T³ lattice **projected by the Z₂ (inversion) action**, using the correct
  **Pin⁻ / spin structure** and the orbifold parities at the **8 fixed points**.
- **Regularize** with the Epstein zeta function of that Z₂-projected lattice,
  E_Λ(s) = Σ′ |n|^{−2s}, analytically continued. For massless fields this collapses to
  V(L) = C/L⁴ with C a number fixed entirely by the field content.
- **V_gravity(L)** = the higher-dimensional Einstein–Hilbert term + the radion kinetic
  term. This is what introduces ℓ_P and makes x = L/ℓ_P a pure number to be predicted.

This is standard, exactly computable physics (Epstein/heat-kernel regularization on a
torus orbifold). No new mathematics is required to *set it up*.

---

## Inputs you ARE allowed (all discrete)

- the field content — *counted* bosonic vs fermionic degrees of freedom, not chosen
- the spin / Pin⁻ structure and Z₂ parities — discrete topological data
- the number of fixed points = 8 — topological
- any flux quanta N — integers

## Inputs that are FORBIDDEN (these = inserting the answer)

- any bulk scalar mass m, brane tension, or coupling **adjusted to move the minimum**
- any overall normalization chosen "to match 137" or "to match 32π/3"
- selecting which of several formulas to keep

---

## Success / failure criteria (sharp, unfakeable)

- **SUCCESS** ⇔ x_min = 32π/3 = 33.5103 (circumference) — equivalently radius 16/3 —
  with **every input discrete/counted**, AND the result is **stable**: vary any
  continuous quantity in the calculation and x_min must not move. If the field content
  is truly fixed there is nothing to tune, so x_min is simply a number the theory spits
  out. If that number is 32π/3, the derivation is real. (Then I eat the "dumb.")

- **FAIL — runaway:** net Casimir coefficient C ≠ 0 ⇒ V ∝ 1/L⁴ monotonic ⇒ no minimum
  (the extra dimensions decompactify or collapse). This is the *default* outcome and
  must be overcome.

- **FAIL — wrong value:** a genuine minimum exists but x_min ≠ 32π/3. (Useful: we'd then
  know the real stabilized size.)

- **FAIL — needs tuning:** a minimum at 32π/3 exists only for some hand-set continuous
  parameter ⇒ it's a fit. (Test: vary that parameter; if x_min tracks it, it's not derived.)

---

## What you need to know going in (the honest part)

1. **A finite-L minimum generically requires the leading 1/L⁴ term to (nearly) cancel** —
   i.e. the net 4D vacuum energy ≈ 0. That cancellation *is the cosmological-constant
   problem*, unsolved for 40 years. If the boson−fermion content of T³/Z₂ makes C vanish
   **naturally** (by the orbifold projection / a hidden supersymmetry), that alone is a
   major result, independent of the value of the minimum.

2. **The target factorizes as 32/3 = 8 × (4/3).** The **8** can come honestly from the
   8 fixed points / 8 twisted sectors. The **4π/3** is a phase-space / Epstein geometric
   factor. The precise, narrow thing to prove is that these *discrete* pieces assemble to
   32π/3 with nothing fitted. That is the whole ballgame.

3. **Prior odds are low.** String theory's moduli stabilization does not generically land
   on clean transcendentals; stabilized values are usually tuned. But this is the *right,
   well-posed, checkable* problem, and a clean answer either way is worth having.

---

## If Casimir self-stabilization fails, the backups (in order)

- **Flux compactification:** integer flux N through the cycles of T³/Z₂; V(L) from flux
  energy (∝ N²/Vol) balanced by curvature/tension. N is quantized (allowed). The
  geometric volume factors carry explicit π's, so a π-multiple minimum is *possible* —
  the test is whether the rational part **32/3** drops out of N and the fixed-point
  count with no tuning.
- **Goldberger–Wise:** a bulk scalar with boundary VEVs. Warning: this needs a continuous
  mass m and VEV ratio, so it will almost certainly land in the "needs tuning" bucket
  unless m and the VEVs are themselves fixed by discrete data.

---

## One-paragraph brief for the next agent

Do not fit anything. Build the one-loop radion potential V(L) for M₄ × T³/Z₂ using only
the counted Standard-Model + graviton field content, the Z₂-projected KK spectrum with the
correct Pin⁻/spin structure, the 8 fixed points, and (if used) integer fluxes — no tuned
masses, tensions, or couplings. Regularize with the Epstein zeta of the projected lattice.
Find the global minimum x_min = ⟨L⟩/ℓ_P. Report it. If x_min = 32π/3 = 33.51 with nothing
tuned and it survives varying every continuous input, the Z² framework has a genuine,
parameter-free derivation of its master constant. If V(L) runs away (no minimum), or the
minimum is elsewhere, or it only hits 32π/3 under tuning — it does not, and 32π/3 stands
as the Friedmann/geometric definition 8 × (4π/3).
