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

## The gates (FC-FINAL: constant a₀, fields g,A,φ — no σ)

### Gate 0 — Symbolic audit (`fc8_symbolic_audit.py`)  [runnable now]
Prove `μ_10(y)=y+O(y¹¹)`, `J_10(x)=x³/3+O(x¹³)`, `𝓕_M=a₀²J₁₀=O(Y^{3/2})` ⇒ **δ²S_MOND=0** on `Y=0`, plus
the MOND law / BTFR / Solar-System suppression. **Fail the script if a quadratic MOND kinetic (tensor or
scalar) term appears** on the vacuum.

### Gate A — Hamiltonian rank (`dirac_fc8.py`)  [attack FIRST]
Take the known AeST 3+1 system and replace **only** `𝓕(Y,Q)→𝓕_Q^★(Q)+a₀²J₁₀(√Y/a₀)`. Recompute all
momenta, primary/secondary/tertiary constraints, the complete Poisson-bracket matrix, and its rank on
the regular branch. Do **not** count DOF from field names. `N_phys=(N_phase−2N_first−N_second)/2`. Repeat
on branches: (a) generic Y≠0; (b) `Y→0`; (c) homogeneous FLRW; (d) static spherical. Target **N_phys=6**
(the established AeST count, IF the modified `𝓕` preserves the 4-first/4-second-class degeneracy). First
failure terminates that branch; 6 is a target until the rank is printed.

### Gate B — Tensor (`ppn_fc8.py`/dedicated)
Derive the TT quadratic action of FC-FINAL; require `Q_T>0` and `c_T²=1` (AeST designed for `c_GW=c_EM`,
PRL 127.161302 — but re-derive with the modified `𝓕`, do not inherit).

### Gate C — PPN (`ppn_fc8.py`)
**DERIVE** the FC-FINAL 1PN metric from the action; map to PPN gauge; extract `γ, β, α₁, α₂, α₃`. **No
imported Einstein-aether formula unless the FC-FINAL→EA field-redefinition/parameter map is demonstrated.**
Require `|α₁|<10⁻⁴`, `|α₂|<10⁻⁷` (Living Rev. Relativity 27:5). Per surviving point report
`K_B, 𝒦₂, μ, a₀, α₁, α₂, β−1, γ−1, c_T²−1`, all kinetic eigenvalues, all speeds.

### Gate D — Full spherical incl. `m_×` (`spherical_fc8.py`)
For `ds²=−e^{2Φ(r)}dt²+e^{2Λ(r)}dr²+r²dΩ²`, solve the full quasistatic `Φ,Λ,A_t,A_r,φ` **without assuming
the vector vanishes** (the `m_×` scale, PRD 110.024062). Test whether `g_N=g²/(g^{10}+a₀^{10})^{1/10}`
comes from the **solution** (with metric/aether backreaction), not the ansatz.

### Gate E — Lensing (`weak_field_fc8.py`)
Compute `Φ−Ψ` from the nonlinear field equations. Three outputs only: **PASS** `Φ−Ψ=0` from the traceless
equation; **PARTIAL** nonzero but explicitly bounded; **FAIL** unavoidable O(1) slip. No "AeST normally has
Φ=Ψ, therefore PASS."

### Gate F — Infrared (`spherical_fc8.py`)
Compute `r_C~(r_M μ^{−2})^{1/3}` and require `r_C ≫ r_{gal,test}` (oscillatory onset beyond the tested
galactic domain ⇒ `μ⁻¹≳Mpc`, a falsifiable constraint — not "take μ small").

### Gate G — Cosmology (`flrw_fc8.py`)
Use `𝓕_Q^★(Q)` to reproduce the established AeST cosmological behavior (CMB + matter power at linear
scales for suitable K(Q)); do **not** make a₀ responsible for dark energy. Derive the full quadratic
FLRW system; require `K_i>0`, `c_i²≥0` for every propagating mode, and check the **nondynamical** mode
separately (AeST low-k mode, sign flips at `k_*`, 2109.13287 — do not report only propagating dispersions).

---

## Boiled down

> Freeze FC-8R. Do not invent anything else. Derive the full Hamiltonian, PPN, weak-field, nonlinear
> spherical, and FLRW equations from the frozen action. Run symbolic/numerical falsification gates. First
> failure terminates the branch. Report PASS only when the quantity is explicitly produced by the
> equations; OPEN when it cannot be derived. Do not inherit PASS from AeST. Do not import EA PPN formulas
> without deriving the map. Preserve every correction and failed branch in the audit log.
