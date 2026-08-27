# TWO_CHANNEL — H_TT + H_MOND architectures (2026-08-27)

**STATUS: FAIL — but with the sharpest structural result of the program: the MMG/YCG duality.**

## The crispy result: the ADM two-potential duality theorem

In ADM, the Newtonian force and the spatial/lensing potential are set by **two different
constraints**:
- the **lapse** N (g_00) → geodesics → galaxy rotation curves;
- the **conformal factor** ψ (h_ij) → spatial curvature → the lensing half of γ_PPN.

GR ties them (γ_PPN = 1) *precisely through the Hamiltonian constraint*. Both two-channel
architectures must sacrifice that constraint to get 2 DOF — and each then gets exactly one
potential right:

| Architecture | Modifies | Gets | Loses |
|---|---|---|---|
| **MMG** (audited 8c53d66a) | lapse constraint C_M | MOND dynamics ✓ | γ_PPN = 0 (no spatial potential) |
| **YCG** (this run) | conformal/York constraint | spatial potential, c_T=1 ✓ | **no MOND dynamics** — rotation curves stay Newtonian |

**They are exact mirror images.** Neither can have both.

## YCG specifics (scripts/ycg_lapse_vs_conformal.py)

YCG genuinely escapes two prior no-gos: only ONE potential (no Horn-1 double counting, unlike the
Aug-22 York/CMC construction), and the TT sector is untouched so c_T = 1 (unlike CGD). Real wins.

But MOND written on the conformal constraint reaches the lapse only as an effective density
ρ_eff = J/(8πGc²) ~ g³/(a₀c²), which is (i) 1/c²-suppressed (post-Newtonian, not Newtonian order)
and (ii) scales as 1/r³ instead of the required phantom 1/r². Ratio to the needed phantom density:
**ρ_eff/ρ_ph = GM/(3c²r) ≈ 2×10⁻⁷** at the solar radius. Rotation curves stay Newtonian.

## The trilemma (scripts/two_channel_trilemma.py)

Under minimal coupling, matter enters via δS_m/δN, and N sits in the TT sector, the MOND sector,
or both — giving exactly three horns: G_eff = 2G (York gate E), MOND inert (D_iD^i = 0), or the
MMG chassis (audited FAILED). No fourth route.

## Where this leaves the program — five independent structural obstructions

1. **F(A²)** (sf40/41) — nonlinearity in a kinetic Hessian ⇒ a scalar propagates
2. **MMG audit** (8c53d66a) — deleting H_⊥ ⇒ γ_PPN=0, α₃=−1, matter non-conservation
3. **MMG_REPAIR_A** (2542182b) — restoring γ_PPN=1 ⇒ α₃=−3, deep-MOND source sign flips
4. **CGD dual no-go** (6f603c50) — local matter-source failure + nonlocal c_T = 0
5. **Two-channel trilemma + MMG/YCG duality** (this) — one constraint gives one potential

**The emerging general statement:** any local, minimally-coupled, 2-tensor-DOF theory whose
weak-field limit is exact MOND must either delete H_⊥ (⇒ MMG failures), modify the tensor Hessian
(⇒ propagating scalar), or use nonlocal projections (⇒ tensor-sector damage). The Hamiltonian
constraint is what welds dynamics to lensing, and every 2-DOF route so far has had to break it.

**Untouched by all five:** the a₀(z) ∝ H(z) clock and the a₀ = κc√(Gρ_Λ) coefficient — these are
measurement-side predictions independent of the relativistic completion, and the Gaia DR4
registration tests them directly.
