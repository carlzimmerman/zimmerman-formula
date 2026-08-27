# CGD_GAUSSLAW — Constrained Gravitational Displacement / Gauss-Law MOND
## Full closure attempt, 2026-08-27

**Objective.** Construct MOND from a nonlinear constitutive law on a *canonical gravitational
displacement* E_i built from ADM phase space, with the matter-density source arising via a genuine
gravitational Gauss constraint D_i D^i = 4πG ρ_b — under minimal matter coupling and with no
additional propagating scalar or vector mode.

**Status: FAIL** — structural no-go under the specification's own rules. Details in `NO_GO.md`;
enumeration script `scripts/cgd_candidate_enumeration.py` (exit 0, results/cgd_enumeration.out);
independent adversarial verification via workflow (see `results/`).

## The obstruction, in one line

The matter-density source in ADM lives in the Hamiltonian constraint H_⊥ (a scalar). The
divergence of any local 1-tensor built from (h_ij, π^ij, ³R_ij) at ≤2 derivatives cannot be that
scalar; it can only be either identically zero (in CMC), proportional to D^i T_{0i} (a momentum
source — zero for static matter), or proportional to D² ρ_b (Laplacian of density, wrong
derivative order). Hence the required D_i D^i = 4πG ρ_b has no local 2-derivative solution under
minimal coupling.



## Second, independent obstruction — the natural nonlocal completion also fails

(Verified this session, `scripts/verify_tt_kills_R.py`.) The natural nonlocal completion of the
required object, E_i = (c²/4) D_i Δ_h^{−1} ³R, has the correct weak-field scalar behaviour
(E_i^{(1)} ≈ ∇_i Ψ) but ³R^{(1)}|_TT = 0 identically, so the constitutive potential J(Y=E²)
contributes NOTHING to the tensor sector — c_T² = 0 (or ill-defined). Two complementary no-gos
now cover both the local (matter-source failure) and the natural nonlocal (tensor-sector failure)
CGD candidates. Details in NO_GO.md §"Second, independent no-go".

## Gate table (spec §29)

| Gate | Requirement                            | Result | Evidence |
|------|----------------------------------------|--------|----------|
| G1   | Fundamental gravitational E_i exists   | PARTIAL | E1..E6 catalogued; all fail G4 |
| G2   | No independent scalar/vector mode      | (n/a — no candidate reaches this test) | |
| G3   | Canonical displacement exists          | PARTIAL | J(Y) constitutive is known-realizable |
| G4   | Genuine gravitational Gauss constraint | **FAIL** | scripts/cgd_candidate_enumeration.py PART 2-3 |
| G5   | Minimal matter coupling                | THEOREM | scripts/cgd_candidate_enumeration.py PART 0 |
| G6   | First degeneracy condition             | — | not reached |
| G7   | Second degeneracy condition            | — | not reached |
| G8   | Exactly 2 nonlinear DOF                | — | not reached |
| G9   | Exact μ=1−e^{−y}                       | KNOWN | prior committed work (J(Y)) |
| G10  | Newtonian limit                        | — | not reached |
| G11  | Deep-MOND limit                        | — | not reached |
| G12  | c_T=1                                  | **FAIL** (nonlocal completion) | scripts/verify_tt_kills_R.py: ³R^(1)&#124;_TT = 0 |
| G13  | Stability/causality                    | — | not reached |
| G14  | Cosmology                              | — | not reached |
| G15  | Linear perturbations                   | — | not reached |
| G16  | Lensing                                | — | not reached |
| G17  | PPN                                    | — | not reached |

FIRST FAILED GATE: **G4 (genuine gravitational Gauss constraint under minimal coupling)**.

==================================================
FINAL STATUS
==================================================

STATUS: FAIL

FIRST FAILED GATE: G4 — no local low-derivative canonical E_i has D_i E^i = 4πG ρ_b under
minimal matter coupling.

EXACT OBSTRUCTION: The ADM matter-density source T_{00} = ρ_b enters gravity only through the
Hamiltonian constraint H_⊥ = (K_ij K^ij − K² − ³R)/16πG + ρ_b ≈ 0, which is a SCALAR density.
The divergence of any local 1-tensor E_i built from (h, π, ³R) at ≤ 2 spatial derivatives is
either (a) identically zero on CMC slices (E1 = D_i K case), (b) proportional to D^i T_{0i} (E2,
E5: momentum-flux source, zero for static matter), or (c) proportional to D² ρ_b (E3, E4, E6 via
Bianchi collapse: Laplacian of density, one order too many). None equals 4πG ρ_b.

MATHEMATICAL LOCATION: `scripts/cgd_candidate_enumeration.py` PART 0 (matter-entry theorem) and
PART 2 (per-candidate divergence structure). Every candidate is derived by the standard ADM
Poisson-bracket algebra and contracted second Bianchi identity in 3D; nothing is asserted.

WHY IT CANNOT BE REPAIRED WITHOUT CHANGING THE ARCHITECTURE: The three admissible escapes
(higher-derivative E_i; enlarged phase space; nonminimal coupling) each violate one of the
specification's own non-negotiable rules:
- Higher-derivative E_i requires a new Ostrogradski-degeneracy certification program (Rule 10);
- Enlarged phase space smuggles a scalar/vector or reduces to the MMG architecture (Rule 3, 5;
  MMG already proven FAILED — γ_PPN=0, α_3=−1, matter non-conservation, commit 8c53d66a);
- Nonminimal coupling is forbidden outright (Rule D / §6 tail).

Localizing the object needed by the theorem forces a nonlocal inverse-Laplacian structure
(E_i = −D_i ∇^{−2} ³R), which is the Deffayet–Woodard nonlocal class — already published as a
no-go (Cassini 10–14σ; DOI 10.5281/zenodo.22132648).

The CGD/Gauss-law route as specified today is structurally EMPTY.
