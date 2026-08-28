# FC-8R CLOSURE REQUIREMENTS

```
====================================================================
   NO PASS WITHOUT DERIVATION FROM THE FC-8R FIELD EQUATIONS.
====================================================================
```

- A statement inherited from ordinary AeST is **NOT** an FC-8R PASS.
- A numerical scan is **NOT** a theorem unless the scanned equations are printed.
- A tuned parameter point is **NOT** viable until every required inequality is checked.
- An assumed relation `Φ=Ψ` is **NOT** acceptable.
- An assumed 7-DOF count is **NOT** acceptable.

Every gate returns exactly one of:

```
PASS   — the quantity is explicitly produced by the FC-8R field equations and meets the requirement.
FAIL   — the equations produce a value that violates the requirement (report it; first FAIL terminates the branch).
OPEN   — the quantity cannot yet be derived from the frozen action here (state precisely what is missing).
```

---

## FROZEN-CANDIDATE RULE

The purpose of this directory is not to improve the theory indefinitely. **FC-8R is frozen.**

**Allowed:** correcting algebraic mistakes; fixing dimensions/sign conventions; deriving omitted field
equations; evaluating existing parameters; proving existing claims; producing explicit counterexamples.

**Not allowed:** introducing a new field; changing the matter coupling; changing μ_10; replacing the
potential-only lock; re-introducing α/ζ; adding PPN counterterms; changing the number of propagating
fields; selecting boundary conditions solely to remove a pathology.

If a required gate fails, report **FAIL**. If a gate cannot be evaluated from the frozen action, report
**OPEN**. **Never convert OPEN into PASS.** Preserve every correction and failed branch in `RESULTS.md`.

---

## The gates

### G0 — Symbolic audit (`fc8_symbolic_audit.py`)  [runnable now]
Prove `μ_10(y)=y+O(y¹¹)`, `J_10(x)=x³/3+O(x¹³)`, and `δ²S_MOND^R=0` on `Y=0, χ=χ₀`. **Fail the script if a
quadratic `χ̇²`, tensor, or scalar kinetic term appears** from the MOND sector. Verify the exact-elimination
validity (`V(χ)>0` global) and that `𝒜(χ)=κ²GV` carries no `χ̇`/`∇χ`.

### G1 — Full nonlinear Dirac rank (`dirac_fc8.py`)  [attack FIRST]
Full 3+1 decomposition of FC-8R. Do **not** count DOF from field names. Construct: all canonical momenta;
all primary constraints; total Hamiltonian; preservation equations; all secondary/tertiary constraints;
the complete Poisson-bracket matrix; its rank on the generic branch — **explicitly including `π_χ`**. Then
`N_phys=(N_phase−2N_first−N_second)/2`. Repeat on branches: (a) generic; (b) `a₀→0` / `V→0` boundary;
(c) `Y→0`; (d) homogeneous FLRW; (e) static spherical. First failure terminates that branch. Target
`N_phys=7`; **7 is a target, not a theorem** until the matrix rank is printed.

### G2 — PPN (`ppn_fc8.py`)
**DERIVE** the FC-8R 1PN metric directly from the FC-8R action; map into the PPN gauge; extract
`γ, β, α₁, α₂, α₃, ξ, ζ₁, ζ₂, ζ₃, ζ₄`. **Do not import Einstein-aether PPN formulas unless the FC-8R→EA
parameter map is derived explicitly.** Search the healthy parameter space only after deriving the map. For
every surviving point report `K_B, λ_s, 𝒦₂, μ, V₀, m_χ, α₁, α₂, β−1, γ−1, c_T²−1`, all scalar/vector
kinetic eigenvalues, all propagation speeds. (Context: GW170817 bounds EA `c₁₃~10⁻¹⁵`, 1802.04303; 2026
strong-field pulsar preferred-frame bounds — treat non-parametrically.)

### G3 — Weak field / slip (`weak_field_fc8.py`)
Expand `Φ,Ψ,φ,A_0,A_i,χ` consistently and **compute `Φ−Ψ`**. Three outputs only: **PASS** `Φ−Ψ=0` from the
traceless field equation; **PARTIAL** `Φ−Ψ` nonzero but bounded by an explicit expression; **FAIL** an
unavoidable O(1) slip. No "AeST normally has Φ=Ψ, therefore PASS."

### G4 — Nonlinear spherical + IR (`spherical_fc8.py`)
For `ds²=−e^{2Φ(r)}dt²+e^{2Λ(r)}dr²+r²dΩ²`, solve simultaneously `Φ,Λ,A_t,A_r,φ,χ`. Test whether the
physical acceleration satisfies `g_N=g²/(g^{10}+a₀^{10})^{1/10}` and whether `Φ=Ψ` comes out of the
**solution** (not the ansatz). Compute the IR crossover `r_C~(r_M μ^{−2})^{1/3}` and report `r_C/r_galaxy`
(do not merely "take μ small"); the oscillatory-onset-beyond-virial condition ⇒ `μ⁻¹≳Mpc` is a falsifiable
constraint, not an assumption.

### G5 — FLRW perturbations / growth (`flrw_fc8.py`)
At `χ=χ₀, a₀²=κ²GV₀` derive the full quadratic scalar system. Require `K_i>0` and `c_i²≥0` for **every
propagating mode**, and check the **nondynamical** mode separately (AeST has a nonpropagating mode whose
Hamiltonian sign depends on wavelength, transition at `k_*`; do not report only propagating dispersion
relations). Also answer the cosmological question: does the solution remain potential-dominated enough
(`χ̇²≪V`) that `a₀(z)` behaves acceptably?

---

## Boiled down

> Freeze FC-8R. Do not invent anything else. Derive the full Hamiltonian, PPN, weak-field, nonlinear
> spherical, and FLRW equations from the frozen action. Run symbolic/numerical falsification gates. First
> failure terminates the branch. Report PASS only when the quantity is explicitly produced by the
> equations; OPEN when it cannot be derived. Do not inherit PASS from AeST. Do not import EA PPN formulas
> without deriving the map. Preserve every correction and failed branch in the audit log.
