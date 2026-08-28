# FC Scorecard — Architecture C: Laplacian-auxiliary MMG + mu_10

**Verdict: STRUCTURALLY-DEAD as a complete theory.**
C fixes the k=0 (cosmology/background) gate genuinely, but the fix is *orthogonal*
to the k≠0 second-class structure that carries B's kills. C **inherits, unrepaired**,
B's γ_PPN = 0 lensing failure (~20σ on M24 KiDS; 43,479σ on Cassini γ) and
α_3 = −1 (2.5e19× the pulsar bound). Per Carl's rule — *"Do NOT declare C viable
if it inherits an unrepaired ~20σ lensing fail"* — C is not viable.

Failure class: **CONSTRAINT-ARCHITECTURE** (deleting H_perp for the 2-DOF count),
not KERNEL. mu_10 is invisible to every failure below (S_2 contains no μ, no a₀).

---

## What C actually is

C = the constraint-first MMG chassis (openai_push/final_closure/, 12-gate + Gate-13
certified) with its two auxiliary constraints written as **Laplacian multipliers**:

    S_4 = π_N,   S_1 = C_M = D_i[c² μ(y) D^i lnN] − 4πG ρ_m,
    S_2 = D² q,  S_3 = D² p,        q = (1/6) ln det γ ≈ −Φ/c²,   p = π/√γ.

There is **no Hamiltonian constraint H_perp**: C_M replaces the static lapse
equation; nothing replaces H_perp's curvature-sourcing role. The "Laplacian
completion" is exactly the choice S_2, S_3 ∝ D² — designed so that the multiplier
`D²λ` annihilates the k=0 homogeneous mode and the background decouples.

## The claim, tested and proved

**The D² completion fixes k=0 but has zero support on the k≠0 Φ-sourcing equation.**
Certificate: `fc_C_laplacian_orthogonality_certificate.py` (self-contained sympy,
exit 0, re-run this session). The operator D² is a Fourier multiplier m(k) = −k²:

| Sector | multiplier m(k) | consequence | status |
|---|---|---|---|
| **k = 0** (background) | m(0) = 0 | S_2, S_3 vanish identically; C_M divergence vanishes; only π_N survives → Dirac restart regenerates the **Friedmann** constraint (first-class), 0 zero-mode DOF, external CMC clock a₀(z)=a₀,₀H(z)/H₀ | **PASS** (sf54, commit fc2e28f1) |
| **k ≠ 0** (inhomog.) | m(k) = −k² ≠ 0 | S_2 = −k²q(k) = 0 forces **q(k) = 0 ⇒ Φ = 0** at all accelerations, all kernels | **FAIL** (γ_PPN=0) |

The two live on **disjoint Fourier supports**: `supp{m=0} = {k=0}` (the win),
`supp{m≠0} = {k≠0}` (the kill), intersection empty. The multiplier's contribution
to the q-EOM is `−k²λ(k)`, which is 0 at k=0 and lies entirely in the image of D²;
to fake the deleted Poisson monopole source S₀ it would need λ ∼ −S₀/k² → singular
at k=0. **The Laplacian multiplier can never supply the deleted H_perp source.**
Fixing the background is therefore mathematically orthogonal to repairing Φ.

## Inherited kills (unrepaired, kernel-blind)

- **γ_PPN = 0 (lensing):** q(k)=0 ⇒ Φ=0 ⇒ light sees Ψ only, α_MMG/α_equal-slip = 1/2
  pointwise. M24 KiDS lensing RAR Δχ² = +403…+498 over 15 bins (~20–22σ); Cassini
  γ−1 = −1 is 43,479σ; clusters η(R500) 1.72–2.08 doubles to 3.44–4.16.
  Source: `gate_lensing_weakfield_derivation.py` (DERIVED–FAIL, exit 0 this session).
  **mu_10-blind:** S_2 = D²q carries no μ, no a₀ — Part D ratio = 0.5000 in all 6
  (kernel × footing) cells.
- **α_3 = −1 (preferred-frame / non-conservation):** from the elliptic (instantaneous)
  C_M lapse response in the g_00 sector — coefficient 1 vs GR's 4. 2.5e19× the pulsar
  bound. **Independent of the D² multiplier** (∂α_3/∂λ = 0, certificate S5): the k=0
  completion cannot reach the g_00 kinetic-energy coupling. Also α_1 = +4 (4e4× bound).
  Source: `scripts/ppn_mmg_gate_2026.py` (α_1=+4, α_3=−1, γ=0, β=1, kernel-indep <1e-19).

## Gate table

| Gate | Status | Basis | Failure class | Evidence |
|---|---|---|---|---|
| k=0 / cosmology (Friedmann, CMC a₀(z)) | **PASS** | DERIVATION | NONE | sf54_mmg_k0_zero_mode_sector_2026.py exit 0 (commit fc2e28f1) |
| Laplacian ⊥ to k≠0 Φ-sector | **PASS** (proof of orthogonality) | THEOREM | — | fc_C_laplacian_orthogonality_certificate.py exit 0 |
| k≠0 lensing / γ_PPN | **FAIL** | DERIVATION | CONSTRAINT-ARCHITECTURE | gate_lensing_weakfield_derivation.py (Δχ² +403..+498, Cassini 43,479σ) |
| α_3 (preferred-frame) | **FAIL** | DERIVATION | CONSTRAINT-ARCHITECTURE | ppn_mmg_gate_2026.py (α_3=−1, 2.5e19× bound) |
| c_T = 1 | **OPEN** | EXTERNAL-INPUT / not computed | (uncomputed for C) | see warning below |
| 2-DOF certificate ({D²q, H_i} first-class) | **PARTIAL** | referee-flagged UNVERIFIED | — | REFEREE_REPORT_FINAL.md |

## External c_T warning (recorded, NOT independently verified here)

**EXTERNAL-INPUT (orchestrator brief):** the 2026 Laplacian-MMG *viable* subclass is
reported to have **c_T > 1** (superluminal tensor speed). This is passed in from the
task, not derived or reproduced in this repo, and no in-repo citation was located.
It is therefore recorded as **OPEN** for C: c_T = 1 must be independently enforced
and certified before any Laplacian-MMG variant that survived the other gates could be
called viable. It does not change C's verdict — C is already dead on γ_PPN and α_3 —
but it is a second, independent liability the completion must clear.

## Bottom line

The single feature that makes the Laplacian completion decouple the background
(`D²` annihilates k=0) is the same feature that leaves it powerless on k≠0: the
multiplier vanishes exactly where the cosmology fix lives and is fully active — as a
q=0 lock — everywhere the lensing/PPN physics lives. C repairs the cosmology gate and
**nothing else**. The kills are inherited whole from B, kernel-blind, and rooted in
the deleted H_perp — a CONSTRAINT-ARCHITECTURE obstruction, not a kernel choice.

**Decisive open (if anyone wants to resurrect this family):** does the named
within-family repair S_2′ = D²(q + lnN) — which sets Φ = +Ψ and restores γ_PPN = 1
without touching C_M — also fix α_3 = −1? As named it does **not** (α_3 comes from
C_M, in the g_0i/Φ_1 sector S_2′ never touches), and it requires re-running Gates
3/6/7/8 for the new Dirac bracket {π_N, S_2′} = −D²(·/N) ≠ 0. That is a *new*
certification program, not C.

## Files written (this session, uncommitted — orchestrator commits)

- `fried_chicken_final/fc_C_laplacian_orthogonality_certificate.py` (sympy, exit 0)
- `fried_chicken_final/FC_C_scorecard.md` (this file)
