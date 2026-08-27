# The Consolidated Relativistic Theory (2026-08-27)
## Constraint-defined MOND MMG + Cassini-safe kernel + CMC a₀-clock

**⚠️ STATUS SUPERSEDED 2026-08-27 (same day): the referee-to-closure audit returned FAILED — gamma_PPN=0 exactly, alpha_1=+4/alpha_3=-1, and Newtonian-order matter non-conservation, all kernel-blind (see closure_2026/REFEREE_REPORT_FINAL.md + RETRACTIONS.md). The 'CONDITIONALLY CLOSED' label below is WITHDRAWN; the surviving certified content is the nonrelativistic core.**

**Original status (superseded): CONDITIONALLY CLOSED (certified on the generic branch) — the strongest object in this
repository. NOT claimed as a certified-viable final theory; the three residual defects are listed in
§5 and are conditions, not footnotes.**

---

## 1. The theory (Hamiltonian, preferred foliation)

ADM variables (N, N^i, γ_ij; π_N, π_i, π^ij), q=(1/6)ln det γ, p=π/√γ.

    H_T = H_GR + H_m + ∫d³x [ λ_N π_N + μ₁ C_M + μ₂ D²q + μ₃ D²p + N^i H_i + λ^i π_i ]

with the scalar (lapse) constraint REPLACED by the exact MOND elliptic constraint:

    C_M = D_i[ c² μ(y) D^i ln N ] − 4πG ρ_m ,   y = (c²/a₀)|D ln N|

**Kernel (consolidated choice):** μ(y) = μ_n(y) = y/(1+yⁿ)^{1/n}, n = 5–10
(constitutive primitive G_n with G_n′(y)/2y = μ_n; script `13_kernel_swap_ellipticity.py`).

**Cosmological sector (PROPOSED prescription, not yet certified):** the k=0 homogeneous modes of
(q,p) left open by the closure are prescribed by the CMC clock K = q(t), with

    a₀(q) = c·q/Z   ⇒   a₀(z) = a₀,₀ H(z)/H₀   on FLRW (q = 3H).

Z ≈ 21 and κ = ½ (a₀ = κc√(Gρ_Λ)) remain FITTED, never derived.

## 2. What is certified (theorem-grade, on the generic branch y>0, k≠0)

All from the committed 12-gate suite (`openai_push/final_closure/`, ALL GATES PASS, re-run
2026-08-27) plus gate 13:

- **Exactly 2 local propagating DOF** — the TT tensor pair; the inhomogeneous scalar pair (q,p) is
  removed by second-class constraints (Dirac det Δ = (L_N K)² ≠ 0; 20−12−4=4 phase-space dims).
- **c_T = c, Q_T > 0** — TT sector is exactly GR; no scalar pole, no ghost/gradient instability.
- **Exact MOND weak-field law** div[μ(y)∇Ψ] = 4πGρ_b with no missing sign/factor; deep-MOND
  g=√(g_N a₀) (BTFR), Newtonian recovery.
- **Multipliers fixed by preservation; no tertiary constraint.**
- **Gate 13 (new):** the chassis is kernel-agnostic — the Dirac/rank/DOF gates use μ only through
  ellipticity (μ>0, d(yμ)/dy>0), which μ_n satisfies exactly. So the Cassini-safe kernel inherits
  the full 2-DOF certificate.

## 3. Why the μ_n kernel (Cassini)

The DHF lesson (committed, re-confirmed on the DW branch 2026-08-27): the solar-system observable is
the EFE quadrupole at the EXTERNAL Milky-Way field y_ext ≈ 1.9, not the huge planetary y. There
1−μ_exp = e^{−1.9} ≈ 0.15 is unscreened ⇒ **μ = 1−e^{−y} FAILS Cassini**; committed route1B (25/25):
**μ₅ at 0.39/0.82 of the Q₂ ceiling, μ₁₀ at 0.08/0.21 — clear on both footings.** Cost, stated
plainly: SPARC RAR rms degrades 0.108 → 0.123/0.127 dex vs the a₀-line. That trade is the content.

## 4. The rejected branch (same session, for the record)

The exact-exponential Deffayet–Woodard nonlocal chassis (`fried_chicken_exact_exponential_v2/`) was
driven through five gates: **DOF B** (canonical count 2+2; the (U,ξ) block [[a,b],[b,0]], det=−b²<0 —
a localization ghost survives the full Dirac analysis; the retarded-IC removal is a boundary
prescription, not a Dirac constraint), **cosmology B** (M = −f+K/a³ is w=0 dust — mimics dark
MATTER; a₀ provably free, a₀²=κ²c²Gρ_DE does NOT derive), **Cassini B** (Z[g] localizes to the
external field; e^{−y_ext} unscreened), **tensor B on FLRW** (2nd-order c_T shift; Minkowski c_T=1
exact), **crossing A** (Z=0 regular incl. transport-M). Salvaged novel results → paper (§6).

## 5. The three honest defects (what "CONDITIONALLY" means)

1. **Preferred foliation** — the lapse is removed by a second-class pair; NOT manifestly 4D
   covariant. It is a Hamiltonian MMG theory (legitimate class per arXiv:2011.00805 / 2302.02090),
   not a covariant local action.
2. **Relativistic matter defect** — ∇_μT^{μν}=0 is not a Bianchi identity here; v~c matter EOM
   acquire a MOND-induced correction (Newtonian-order consistent; relativistic order open).
3. **Excluded branches** — k=0 (prescribed in §1 but preservation under H_T not yet derived) and
   y=0 (Newtonian degenerate limit) need separate treatment.

## 6. Novel results banked this session (paper queue)

1. F(A²) single-invariant carrier NO-GO, adversary-proved on generic backgrounds (sf40/41 + FLRW).
2. Auxiliary-Legendre MOND = genuine 0-DOF second-class carrier, any monotone μ (sf42).
3. DW localization ghost: full canonical 2+2 count (novel vs DW 2026, which has no Hamiltonian
   analysis) + linear retarded-IC Cauchy-data count (sf43/44).
4. DW Z[g] localizes to the external field in the Sun+MW configuration ⇒ Cassini verdict for the
   whole DW class (DW 2026 defers this, their eq. 34).
5. Z=0 cosmology↔MOND crossing regularity incl. transport-M (DW publish no perturbation analysis).
6. DW cosmological branch is w=0 dust with a₀ free — the a₀–ρ_DE relation cannot live on that chassis.
7. This consolidation: kernel-agnostic MMG 2-DOF chassis + μ_n ⇒ the first object here holding
   2-DOF + exact MOND + c_T=c + Cassini-safe simultaneously (conditional on §5).

**One line:** a preferred-foliation Hamiltonian MMG theory with the MOND law as its lapse
constraint, certified 2-DOF on the generic branch, Cassini-safe with μ_n, carrying a₀(z)∝H(z) via
the CMC clock — conditionally closed, with the three §5 defects as the remaining program.
