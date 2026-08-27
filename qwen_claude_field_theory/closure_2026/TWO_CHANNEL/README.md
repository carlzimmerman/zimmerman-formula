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

## YCG-v2 (Cotton-squared tensor potential) — tested, same wall

OpenAI's refinement adds V_TT ~ C_ij Δ^{-2} C^ij (Cotton-squared, k³·k⁻⁴·k³ = k²) to supply an
independent tensor gradient. **That is a genuine contribution** — it is a real escape from the CGD
c_T = 0 no-go. But it repairs a sector YCG never broke (YCG retains Einstein's TT term anyway),
and it does not touch the killer.

**The killer, in its cleanest form** (`scripts/ycg_v2_source_check.py`): the MOND divergence
operator D_i[μ D^iΨ] arises from the **q-variation**, and under minimal coupling

    δS_m/δq = (δS_m/δh_ij)(δh_ij/δq) = −2√h T^i_i

because q is the conformal factor of the *spatial* metric (δh_ij/δq = 4h_ij). So the MOND equation
is sourced by the **spatial stress trace T^i_i**, not by ρ_b. Pressureless baryons — the matter
galaxies are made of — have T^i_i ~ ρv²/c² ≈ **5×10⁻⁷ ρ** for the Milky Way. The MOND equation has
essentially no source. This is Horn 2 (MOND inert), reached independently.

**The duality, now proven twice:**

    ρ_b   (energy density)  lives in the LAPSE      variation  δS_m/δN
    T^i_i (stress trace)    lives in the CONFORMAL  variation  δS_m/δq

Put MOND on N → MMG → dynamics but γ_PPN = 0. Put MOND on q → YCG → spatial potential but no
source for galaxies. The two ADM scalar constraints carry *different matter sources*, and MOND
needs the one attached to the potential it cannot live on.

## THE UNIFYING RESULT — HKT closes the menu (results/hkt_theorem.out)

**Hojman–Kučař–Teitelboim (1976):** if H_⊥ (a) closes the Dirac algebra, (b) is ultralocal in
h_ij, (c) is ≤ quadratic in momenta, then H_⊥ **is** GR's, uniquely.

Exact MOND requires a nonlinear μ in the static constraint ⇒ H_⊥ must be deformed ⇒ one of
(a),(b),(c) must break — **and which one breaks determines which observable fails.** All six
architectures tested this session map onto exactly that classification:

| Breaks | Architecture | Fails as | Evidence |
|---|---|---|---|
| (a) closure | MMG: H_⊥ → C_M | γ_PPN=0, α₃=−1 | 8c53d66a |
| (a) closure | MMG_REPAIR_A: S₂′ | γ=1 but α₃=−3, BTFR dies | 2542182b |
| (b) ultralocality | CGD nonlocal Δ⁻¹³R | ³R\|_TT=0 ⇒ c_T=0 | 6f603c50 |
| (b) ultralocality | DW: □_ret⁻¹(R_uu) | ghost 2T+2S; Cassini 10–14σ | DOI 22132648 |
| (c) momentum structure | F(A²) kinetic carrier | khronon propagates (2+1) | sf40/sf41 |
| source routing | YCG: MOND on q | T^i_i ~ 5×10⁻⁷ρ ⇒ inert | 5b7efd3d |
| source routing | CMYG: g̃ = e^{2αq}g | conformal ⇒ no lensing; disformal ⇒ cone split | this run |

**THEOREM.** {exact MOND, minimal coupling, 2 tensor DOF, γ_PPN=1, c_T=1} is **overdetermined**.
GR is HKT's unique (a)+(b)+(c) point; MOND requires leaving it; every exit lands on a *measured*
contradiction. This is not "MOND is impossible" — it is: **no 2-DOF local deformation of H_⊥
delivers MOND with GR's lensing.** The wall is HKT, not any single construction.

**The minimal sacrifice.** Of the four droppable requirements, exactly one has no committed kill:
**drop "2 DOF" → 2+1 with a screened scalar (k-mouflage/Vainshtein).** Then γ_PPN=1 (screened in
the solar system), lensing works (a single conformal source gives Φ=Ψ), c_T=1 (TT untouched), and
μ=1−e^{−y} is retained. Cost: a third propagating DOF. Repo status: *"never tried, ranked #4"*.
Its open gate is whether screening survives the wide-binary/EFE data the Gaia DR4 registration
tests — which makes DR4 the decisive experiment for the surviving class.
