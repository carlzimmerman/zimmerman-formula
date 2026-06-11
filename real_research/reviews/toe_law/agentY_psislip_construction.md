# agentY — [SLOT-Y] the explicit lens-only slip Lagrangian: built, audited, and **machine-OBSTRUCTED** — the scalar u-DHOST class cannot carry (μ,Σ) = (1,ν); the four walls mapped, the surviving architecture banked

*agentY, 2026-06-11. Files: `agentY_quasistatic.py` → `.out` (the sympy quasi-static derivation: the
field equations, the slip formula, the lens-only conditions and their complete branch analysis, the
tensor-sector and FRW theorems; equations pickled to `agentY_eqs.pkl` for reuse) and `agentY_gates.py`
→ `.out` (banked-number gate, the calibration trackability check, the decisive pollution numbers, the
architecture theorems and gate arithmetic). Inputs read first: `agentW_partner_uniqueness.md` Part 2
(the unique class + four named gates), `agentU_khronon_m22.md` (the shared u-frame, PPN corners),
`UNIFIED_ACTION_ASSEMBLY.md` ([SLOT-Y] + the five interface conditions), `../lensing_rar/`
`agentZ_second_variable.md` (the dial is TYPE-IRREDUCIBLE, morphology-tracking). Conventions locked to
the bank and gated in-run before any new use (`agentY_gates.py` SG0: the 61.2/19.4/6.2 slip targets,
Cassini y = 1.1×10¹², the ×1.3×10⁷ margin, the four ν shapes verbatim from
`agentW_partner_uniqueness.py` L59–62, both a₀ footings). This was a framework-favorable construction
attempt, so the discipline was inverted per the working rule: maximum hostility — and the hostility
won. Every "it fails" claim below is machine-derived, was checked against convention/bookkeeping
artifacts (three such artifacts were caught and killed in-run — see the bug log), and the failure is
robust. No git.*

---

## VERDICT UP FRONT: **OBSTRUCTED** — with the obstruction mapped, not just declared

**The scalar realization of agentW's unique surviving class does not exist.** A lens-only,
MOND-amplitude static slip — matter feels Φ_N(baryons) only, photons feel the ν(g_bar/a₀)-keyed
phantom — cannot be carried by any scalar sector built on the assembly's u-frame at quasi-static
order, under the interface conditions (one frame, one scale a₀, zero matter-felt stress). Four
independent walls close every routing, each machine-derived (§4):

1. **First-derivative operators cannot slip.** Every operator built from first u-frame derivatives —
   J(Y), S(Y)a·q, K(Y)a², F(Y)(a·q)², and the leaf-braiding w(Y)□_hχ — has its spatial-metric
   variation one order beyond leading: the rr-constraint forces Ψ′ = Φ′ exactly. (The "static scalar
   gradients have anisotropic stress" intuition from GR is potential-suppressed: a canonical scalar
   halo's slip is O(ε) ~ 10⁻⁷ of the phantom, not MOND-sized — machine lemma, §4.1.)
2. **Second-derivative bilinears break in-halo c_T.** Operators quadratic in second derivatives (the
   genuine quartic/DHOST slip generators, (Dq)², q·Dq·Dq·q, GLPV-F4-type, and likewise (∇a)²
   khronon-only variants) couple (∂h_TT)² on a SPACELIKE-gradient background at the amplitude of
   their slip. The published c_T = 1 classifications protect only timelike (cosmological)
   backgrounds; in halos these operators shift the tensor cone at O(slip) ~ 10–100 vs the GW170817
   10⁻¹⁵ bound through the MW halo: dead by ~15 orders (§4.2).
3. **The c_T-safe mixed quartics route the amplitude into the wrong channel.** The one c_T-safe slip
   generator family — the mixed u-DHOST cross-quartics C(Y)(a·q)(P_T·Dq)/a₀² (single D-factor:
   h-linear only) — CAN carry exactly ν(y) in the ij-channel (the calibration is closed-form for all
   four banked ν shapes, `agentY_gates.py` SGA). But at that amplitude the same operators feed the
   Hamiltonian constraint at **(a₀r/c²)⁻¹ ≈ 10⁷ × the phantom** (machine-measured: δg/g_bar =
   3×10⁷–1.6×10⁸ across y = 0.3–0.01, P-independent across two decades of kinetic stiffness —
   `agentY_gates.py` SGB). Root cause, confirmed analytically: a potential-amplitude scalar's
   anisotropic-stress channel is its weakest channel; phantom-sized ij-stress forces the operator's
   Lagrangian ~(a₀r/c²)⁻¹ above the local EH scale. Against the double-counting theorem's 8.7–21.6σ
   kill of ~0.2-dex matter-channel pollution, this is dead by seven orders.
4. **The exact-μ=1 conditions admit only trivial slip.** Demanding Δ_Φ ≡ 0 for all profiles, the
   complete branch analysis of the lens-only conditions in the minimal basis collapses every solution
   to slip/Φ′ ∈ {0, κ (const), −1}: no y-tracking slip coexists with an exactly clean matter channel.
   The one apparent exception (J = Y/4, where all conditions vanish identically) is the **singular
   surface** of the field equations, not a solution — the C-free system there is inconsistent
   (0 = 8πGρ̄, machine-verified), and the conditions' vanishing was 0×∞ (§4.4; caught by the gate).

The amplitude-keying is what kills it: interface condition 2 (one scale — a₀) forces the slip scalar
to potential-scale gradients q ~ a₀-class, and a potential-scale field has no channel routing that
delivers phantom-scale anisotropy without wrecking either the tensor cone (wall 2), the matter
channel (walls 3–4), or the slip itself (wall 1). **The kill is NOT ghosts** — the place the tasking
flagged as the likeliest death — the foliation makes every operator time-derivative-free in unitary
gauge and the Ostrogradsky question never arises (§5.4). The class dies in the channel-routing.

**What this does to agentW's class:** the unique surviving partner structure narrows further. The
metric-level Ψ-channel slip sector, if it exists, is **not a scalar on the u-frame**: the remaining
candidates are (i) intrinsically anisotropic carriers (a vector/spin-2 partner field whose stress is
not built from a single gradient), (ii) nonlocal/history-dependent operators (the matter sector's own
M22 nonlocality echoed in the lensing sector — outside quasi-static scalar scope by construction),
(iii) the exact-in-C analysis at the singular surface (logged, low prior), (iv) the K/F/S-dressed
extended bases (machinery banked; the channel-routing argument is operator-generic and gives them a
low prior, but they are not machine-closed — stated honestly). Each inherits, for free, the
architecture theorems of §5 (c_T ≡ 1, α_M ≡ 0, FRW quietness, the geometric morphology dial).

---

## 0. The spec (restated sharply) and what was actually attempted

The assembly's S_slip slot: a c_T-preserving DHOST-class sector coupled to the SAME u^μ as the matter
sector, producing in the quasi-static limit

> **matter:** ∇²Φ = 4πG ρ_b  (μ = 1; stars feel Newton-of-baryons only — the MI sector owns dynamics)
> **photons:** ∇²Ψ = 4πG ρ_b + ∇·[2(ν(g_bar/a₀)−1) **g**_bar]  (Σ = ν; slip η = Ψ′/Φ′ = 2ν−1
> = 61.2/19.4/6.2 at g_bar = 10⁻¹³/10⁻¹²/10⁻¹¹, McGaugh ν, framework a₀ — re-gated in-run)

under the five interface conditions (one frame, one scale, zero matter-felt partner stress at the
8.7–21.6σ double-counting bar, the agentZ morphology dial, photons/gravitons on shared cones).

**Fields:** g_μν; the khronon T (u_μ = −∂_μT/√(−∂T·∂T), agentU, canonical kinetic corner); a slip
scalar χ. **u-frame objects:** q_μ = h_μ^ν∂_νχ (leaf-tangential gradient; h = g + uu),
Y = q·q c⁴/a₀² (the dimensionless keying variable), a_μ = u^ν∇_νu_μ (khronon acceleration; in
unitary gauge a_i = ∂_i ln N exactly — in static weak field a_i = ∂_iΦ: the local field, which is
what makes a₀-keying architectural). **The operator basis explored** (everything available at
phantom order to a scalar on the foliation):

> S_slip = (c⁴/8πG) ∫√−g [ −(a₀²/c⁴)J(Y) + σS(Y)a·q + K(Y)a·a + F(Y)(a·q)²c⁴/a₀²
>          + a₀w(Y)□_hχ/c² + C₁(Y)a^μq^νD_νq_μ c⁴/a₀² + C₂(Y)(a·q)(D·q)c⁴/a₀²
>          + C₃(Y)(a·q)(q^μq^νD_μq_ν)c⁸/a₀⁴ ]

(D = leaf covariant derivative; □_h = leaf Laplacian). Covariantly the C-operators are
(∇∇T)(∇∇χ)-cross quartics with first-derivative dressings — genuinely DHOST-class bi-scalar
operators, degenerate BY THE FOLIATION. The two C-combinations that matter assemble into the
transverse-divergence form **C(Y)(a^μq_μ)(P_T^{νρ}D_νq_ρ)**, P_T = h − qq/|q|²: the slip is sourced
by the bending of the χ field lines (§5.3).

## 1. The c_T = 1 DHOST classification, pinned — and why the published class was never going to do it

- **Quadratic DHOST** (Langlois–Noui 1510.06930; reviews 1811.06271, 1906.03020): L = f₀ + f₁□φ +
  f₂R + ΣAᵢLᵢ (L₁ = φ_{μν}φ^{μν}, L₂ = (□φ)², L₃ = □φφ^μφ_{μν}φ^ν, L₄ = φ^μφ_{μν}φ^{νρ}φ_ρ,
  L₅ = (φ^μφ_{μν}φ^ν)²); viable = class Ia. **GW170817:** c_T = 1 ⟹ A₁ = A₂ = 0 with degeneracy
  fixing A₄ = (1/8f₂)[48f₂ₓ² − 8(f₂−Xf₂ₓ)A₃ − X²A₃²], A₅ = (A₃/2f₂)(4f₂ₓ + XA₃) — the
  1710.05901 (Ezquiaga–Zumalacárregui) / 1711.07403 (Langlois–Saito–Yamauchi–Noui) surviving class,
  {f₀, f₁, f₂, A₃} free. [Quoted in the X = φ_μφ^μ convention of the Langlois review.]
- **The second-generation kill:** GW decay into the scalar (Creminelli–Lewandowski–Tambalo–Vernizzi
  1809.03484; nonlinear 1910.14035) forces |α_H| ≲ 10⁻¹⁰ on the cosmological background — the
  cosmological-clock DHOST slip is dead as a large-slip engine. Any candidate must be cosmologically
  quiet and halo-keyed. The u-frame construction achieves this automatically (§5.2).
- **The structural mismatch with the lensing-RAR job, pinned:** the surviving class's quasi-static
  slip (Crisostomi–Koyama 1711.06661; Dima–Vernizzi 1712.04731; Kobayashi 1901.07183) is partial
  Vainshtein breaking INSIDE matter — Φ′, Ψ′ corrections keyed to M′(r), M″(r), GR restored exactly
  outside the source. The Brouwer signal lives at 0.03–3 Mpc where M′ ≈ M″ ≈ 0. **No published
  member, as parametrized, produces halo-scale slip** — consistent with agentW §2.4's empty
  literature. The construction had to (and did) move the keying into the u-frame: a_i = ∂_iΦ supplies
  g_bar locally, the χ-profile supplies the a₀-normalized argument Y.
- **A result of this memo sharpens the classification picture:** the c_T = 1 statements above are
  TIMELIKE-background statements. On the spacelike-gradient (halo) backgrounds this application
  needs, the degeneracy-forced A₄, A₅ couple (∂h_TT)² through the q-contractions and shift the local
  tensor cone at the operator amplitude (machine check of the TT-quadratic content, §4.2). The
  published "surviving" quartics are GW170817-dead **in halos** at MOND-slip amplitudes — a boundary
  with reach beyond this program (any "DHOST slip at galactic scales" proposal hits it).

## 2. The two theorems that survive everything (machine-proved, [SA]/[SB] of the .out)

1. **c_T = 1 and α_M = 0 identically, all backgrounds, halo interiors included.** Every operator in
   the basis is leaf-tangential with at most one D-factor: h_ij enters algebraically (machine: no
   derivative of h appears in S_slip on a TT-perturbed background). The tensor kinetic term is
   exactly M_P²/2: the GW-speed gate and the GW-friction gate pass by architecture, not by tuning —
   stronger than any published DHOST tuning, which holds only on FRW. Current standard-siren
   constraints (σ(α_M) ~ O(0.1–1), Lagos+-class and GWTC-3-era dark-siren fits — pinned
   approximately, from-memory values flagged) are trivially satisfied; the class predicts exactly 0.
2. **FRW quietness.** The comoving khronon has a_μ = 0 (machine-computed): the χ-source is off
   cosmologically; with J(0) = 0 the sector carries zero stress on FRW — no dark-energy
   contribution beyond Λ, no cosmological scalar bath for gravitons to decay into (the 1809.03484
   evasion), α_H-equivalent ≡ 0 on FRW. The sector wakes only where a_μ ≠ 0: in halos, keyed to the
   local field. (The Boltzmann-level audit of perturbative wakes remains the assembly's named
   post-construction calculation; nothing here changes that.)

These are now permanent fixtures for [SLOT-Y]: any successor carrier built leaf-tangentially on the
u-frame inherits both.

## 3. The derivation (what the machine actually did — `agentY_quasistatic.py`)

Static spherical quasi-statics in the MOND-homogeneous bookkeeping (potentials ~ ε; a₀ = εα with α
finite — the standard Bekenstein–Milgrom grading in which every slip operator enters the action at
one order, with the C-quartics' per-channel tiering adjudicated numerically where the formal grading
cannot encode the αr-finite MOND relation):

- **Metric:** ds² = −(1+2εΦ)dt² + (1+2εL)dr² + (1+2εM)r²dΩ² — TWO spatial functions, varied
  independently, isotropic gauge (L = M = −Ψ) imposed only in the equations. (Gauge-fixing in the
  action loses the rr-vs-tangential traceless equation — exactly the slip channel; the first pass
  made precisely this error, caught because it contradicted the GR anisotropic-stress limit. Bug
  log, item i.)
- **GR gate:** slip off ⟹ lapΨ = 4πGρ̄ (N-equation), Φ′ = Ψ′ (rr-constraint), Φ = Ψ (tangential):
  exact. Canonical-scalar gate: a J = Y/2 scalar's Δ_Φ and Δ_Ψ vanish at leading order (its real
  GR slip is O(ε) of the phantom): exact.
- **The χ first integral** (regularity at r = 0): σΦ′·(S + 2YS′) = 2J′(Y)χ′ — the AQUAL-form source
  relation; with S ≡ 1: **χ′ = σΦ′/2J′**: the χ-gradient tracks the local baryonic field, the
  a₀-keying is exact and architectural.
- **The slip, algebraically:** the rr-constraint carries it —
  > **Ψ′ − Φ′ = −(4πG/r)·[C-sector T_rr content]|on-shell**
  with the C = 0 part identically zero (wall 1) and the C-linear part finite and ν-trackable. For
  the minimal routing (c10 = 0, J″ = 0): slip/Φ′ = 2Y(c20 + Yc20′), closed-form matchable to any
  2(ν−1) (machine: exact to 10⁻¹⁵ across y = 10⁻³–10, all four banked shapes — `gates` SGA).
- **The lens-only condition:** Δ_Φ ≡ Δ_Ψ − (1/r²)(r²(Ψ′−Φ′))′ = 0 for ALL profiles, collected in the
  independent on-shell data (ρ̄′, ρ̄, geometric): three coefficient-classes of conditions on the
  operator functions. Their complete branch analysis is §4.4's wall.
- **Solved perturbatively in the C-amplitude** (the system is bilinear in second derivatives once the
  quartics are on), with the perturbative validity itself then machine-tested — and failed at matched
  amplitude (wall 3): the honest sequence is part of the result.

## 4. THE FOUR WALLS (the obstruction map, with the machine evidence for each)

### 4.1 Wall 1 — first-derivative operators cannot slip
For the full first-derivative family {J, S·a·q, K·a², F·(a·q)², w·□_hχ} (and the reducible
B(Y)q·Dq·q ≡ braiding + S-class), the spatial-metric variations sit at one order beyond leading:
machine result, Δ_Φ ≡ Δ_Ψ on-shell — the rr-constraint reads Φ′ = Ψ′ exactly. A first-derivative
u-coupled scalar sector is MODIFIED GRAVITY (both channels carry whatever phantom the N-equation
acquires): the Blanchet–Marsat/Cassini-killed class, never lens-only. Corollary worth banking: the
(μ,Σ)-cosmology intuition "any anisotropic scalar stress gives slip" does not transfer to
MOND-amplitude statics — the canonical scalar's slip is real but potential-suppressed (10⁻⁷ of the
phantom; the global-monopole analogy fails at amplitude, exactly where agentW's branch-(i) causality
wall said real stress dies).

### 4.2 Wall 2 — second-derivative bilinears break in-halo c_T
Any operator with two D-factors carrying free metric contractions — X(Y)D_μq_νD^μq^ν,
X(Y)(q·Dq)²-type, GLPV-F4 ε-tensor quartics, and the khronon-only (∇a)² variants — contributes
(Γ[h])² ⊃ (∂h_TT)² on a spacelike-q̄ background, with coefficient ~ (operator amplitude)×(q̂,k̂
projections). At slip-matched amplitudes this is an in-halo Δc_T of O(10–100) where the GW170817
path crosses the MW circumgalactic field (g ~ 10⁻¹²–10⁻¹³, ν−1 ~ 10–30) vs |Δc|/c ≲ 10⁻¹⁵: dead by
~15 orders. The timelike-background protection of the published c_T = 1 class (q-contractions vanish
on TT for q ∝ δ⁰) is structurally unavailable to a static halo profile. The single-D mixed quartics
(the C-ops) are the unique c_T-safe slip generators — which is why wall 3 is where the class makes
its last stand.

### 4.3 Wall 3 — the channel-routing wall (the decisive numbers)
With c20(Y) matched so the ij-channel slip is exactly 2(ν−1)(y) — machine check 10⁻¹⁵ — the same
operators feed the Hamiltonian constraint at:

| P = J′ | δg/g_bar @ y=0.3 | @ y=0.1 | @ y=0.03 | @ y=0.01 |
|---|---|---|---|---|
| 1 | −2.7×10⁷ | −5.1×10⁷ | −9.1×10⁷ | −1.5×10⁸ |
| 5 | −3.1×10⁷ | −5.7×10⁷ | −9.8×10⁷ | −1.6×10⁸ |
| 25 | −3.1×10⁷ | −5.8×10⁷ | −9.9×10⁷ | −1.6×10⁸ |
| 125 | −3.2×10⁷ | −5.8×10⁷ | −9.9×10⁷ | −1.6×10⁸ |

(Hernquist 10¹¹ M☉, framework a₀, McGaugh ν; `agentY_gates.py` SGB.) P-independent across two
decades: no kinetic-stiffness escape. Scale = (a₀r/c²)⁻¹ × phantom, confirmed analytically: at
matched amplitude the C-Lagrangian density is ~(a₀r/c²)⁻¹ above the local EH scale — the
perturbative construction's own breakdown, measured. Against the matter-channel bar (agentW: 0.2 dex
coherent = 8.7–21.6σ), the pollution is ~10⁷-fold over. No SPARC weighting, footing, or Υ-convention
is implicated — this is an internal consistency catastrophe, not a fit tension (working-rule check:
moot at seven orders, run at framework a₀; the canonical footing moves nothing).

### 4.4 Wall 4 — the exact-μ branch graveyard
Demanding Δ_Φ = 0 identically (the strongest reading of interface condition 3), the conditions'
complete branch tree in the minimal basis:
- ρ̄′-class ⟹ J″ = 0 (no MOND keying) OR branch 1: c30Y = −(c10+c20) OR branch 2:
  (c10−c20)Y + c30Y² = 2.
- Branch 1 ∘ ρ̄²-class ⟹ c10 = −c20 (⟹ slip/Φ′ = const — cannot track ν) or c20 = −1/Y (⟹
  slip = −Φ′: Ψ′ = 0, lensing killed).
- Branch 2 ∘ {r¹, r⁰, ρ̄²}-classes ⟹ (hand-factored from the machine conditions, then
  machine-checked) J′ ∝ Y^{−1/2} and c20 = −1/Y forced jointly ⟹ slip = −Φ′ again.
- The would-be exception J′ + 2YJ″ = 1/4 (J = Y/4 + A√Y), where every condition carries the factor
  (4J′+8YJ″−1) and vanishes identically: **the singular surface.** The C-free system there is
  inconsistent with matter (machine: eqN|C=0, J=Y/4 on the branch = −r²ρ̄ ≠ 0); the conditions'
  vanishing was 0×∞. Recorded as a dead end caught by the gate (bug log, item iii) — with the honest
  note that an exact-in-C treatment AT the surface (where the quartics would resolve the degeneracy
  nonperturbatively) is unexplored: a named open route, low prior.

## 5. What survives the obstruction (banked for the successor carrier)

1. **The architecture theorems** (§2): c_T ≡ 1 and α_M ≡ 0 identically; FRW quietness/graviton-decay
   evasion. Any leaf-tangential carrier inherits them.
2. **The degeneracy mechanism:** hypersurface orthogonality makes every operator time-derivative-free
   in unitary gauge (Y = γ^{ij}D_iχD_jχ exactly; a_i = ∂_i ln N exactly): no Ostrogradsky sector
   exists to kill. The χ-field is elliptic on the leaves (cuscuton-class; consistent causality on the
   preferred foliation). **The gate-(d) prediction "this is where it most plausibly dies" is
   answered: it does not die there.** Residual flags for any revival: elliptic-mode strong coupling
   in voids (the matched coefficients diverge ~Y^{−5/4} as Y → 0 — the standard deep-MOND coefficient
   divergence, same class as QUMOND's ν(z)); the constraint-reduced gradient analysis on halo
   backgrounds was rendered moot by the obstruction and was not completed.
3. **The geometric morphology dial** — the one genuinely new constructive insight: the c_T-safe slip
   generators assemble into (a^μq_μ)(P_T^{νρ}D_νq_ρ): the slip is keyed to the TRANSVERSE divergence
   (bending) of the field lines — zero for planar configurations, maximal for spherical. Any
   geometry-keyed slip carrier therefore has a built-in morphology-tracking amplitude at fixed g_bar,
   with the agentZ sign (spheroids > disks; the +0.194 dex TYPE-IRREDUCIBLE split needs ×1.56 — the
   geometric range [0, full] covers it). This is the first structural candidate for [SLOT-Z]'s
   "morphology-tracking, not {M*, z, density}" dial that lives in the OPERATOR, not in an external
   field — it survives as a design principle even though this scalar implementation died.
4. **The pipeline:** the full symbolic machinery (two-function-metric quasi-statics, on-shell
   reduction, condition extraction, branch analysis) and the numeric residual/pollution harness, with
   the equations pickled (`agentY_eqs.pkl`). The K/F/S-dressed extended-basis runs are one toggle away
   (`AGENTY_KEEP_K=1`; the K-extension's quadratic branch was started and timed out at the condition
   stage — logged, not closed).

## 6. Gates scorecard (the tasking's four, answered in-model)

| gate | result |
|---|---|
| (a) solar slip auto-pass in-model | For any ν-matched member the Cassini slip is the banked number by construction (1.75×10⁻¹², ×1.3×10⁷ margin, simple-ν; exp-tail dead-dead; SG0 gate reproduced both). Matter channel of an exact-μ member: exactly clean. **Moot at the class level — the class died upstream — but the calibration property is verified.** |
| (b) GW friction α_M | **0 identically** (machine theorem, all backgrounds incl. halos); current siren bounds σ(α_M) ~ O(0.1–1) trivially passed. The in-halo c_T wall (§4.2) is the sharp new GW statement: it executes the quartic sector. |
| (c) clusters ×1.97 + the agentZ dial | ν-keyed slip re-fails clusters at ×1.96 (in-model arithmetic: y(1 Mpc, 7×10¹³ M☉) = 0.10, ν = 3.62 vs ~7.1 needed — the banked ×1.97 reproduced). The dial: structurally PRESENT in the operator geometry (§5.3), right sign, sufficient range — the one [SLOT-Z]-positive finding; quantitative disk-vs-spheroid contrast = the named non-spherical computation for whatever carrier succeeds. |
| (d) ghosts/degeneracy under the u-coupling | **SURVIVES — trivially.** No time derivatives exist in unitary gauge; the u-coupling IS the degeneracy mechanism, not its threat. The class dies at channel-routing (§4.3), not ghosts. |

## 7. For the assembly ([SLOT-Y] disposition) and DERIVATION_CHAIN Link 7

- **[SLOT-Y] does not close with a scalar.** The assembly's S_slip line should read: *scalar
  u-DHOST realizations machine-obstructed (agentY, four walls); the surviving candidate space:
  intrinsically anisotropic carriers (vector/spin-2 partner on the same u), nonlocal/history
  operators (the M22-echo direction), the singular-surface exact-in-C route, and the extended
  dressed bases (low priors, named).* The c_T/α_M/FRW theorems and the geometric-dial principle
  attach to the slot as inherited architecture.
- **Link 7 wording sharpens once more:** agentW's "the lens-only slip carrier is the unique
  remaining class, with its gates named and its literature empty" gains: *its scalar sector is now
  closed constructively — the first nontrivial exclusion INSIDE the unique class. The class is not
  empty of structure (the architecture theorems and the geometric dial are positive results); it is
  empty of scalars.*
- **Both ways, full weight:** this is a hostile-side result obtained while trying to BUILD the
  framework's missing half, with the framework-favorable readings (trackability of all four ν
  shapes, the morphology dial, the exact-μ branch structure) reported at equal strength. The
  obstruction does NOT touch the matter sector (agentU/agentM), the double-counting theorem, or the
  40.5σ wall — it tightens the specification of what must carry the lensing, exactly as the
  tasking's OBSTRUCTED verdict option anticipated ("a boundary narrowing W's class further").

## Pin table

| id | role |
|---|---|
| 1510.06930 | Langlois–Noui — quadratic DHOST classification (the degeneracy frame) |
| 1811.06271 / 1906.03020 | Langlois review / Kobayashi review — class Ia, c_T=1 conditions, A₄/A₅ formulas as quoted |
| 1710.05901 / 1711.07403 | Ezquiaga–Zumalacárregui / Langlois–Saito–Yamauchi–Noui — post-GW170817 survivors |
| 1809.03484 / 1910.14035 | Creminelli+ — graviton decay into the scalar: |α_H| ≲ 10⁻¹⁰ (the cosmological-slip kill; evaded here by FRW quietness) |
| 1711.06661 / 1712.04731 | Crisostomi–Koyama / Dima–Vernizzi — quasi-static DHOST: in-matter Vainshtein breaking, GR outside (the structural mismatch pinned in §1) |
| 1602.05961 §6 | Khoury's u^μ template — the architecture ported (frame-projected scalar sector), its force decoupled; the port is what this memo built and closed |
| 1107.5264 | Blanchet–Marsat khronon-MOND — wall 1's modified-gravity endpoint (the class any first-derivative routing collapses to) |
| 1710.05834 / 1710.06168 | GW170817 speed bound / differential Shapiro — the in-halo c_T wall's bound; the photon-sector exclusions inherited from agentW |
| cuscuton (Afshordi+) | the elliptic-scalar health precedent for the foliation sector |
| repo | `agentW_partner_uniqueness.md` (the class + gates), `agentU_khronon_m22.md` (frame, corners), `UNIFIED_ACTION_ASSEMBLY.md` (interface conditions), `agentZ_second_variable.md` (the dial spec), `agentW_partner_uniqueness.py` L56–62 (ν shapes, a₀ footings — gated in SG0) |

*Machine state: SG0 reproduced the banked slip targets (61.2/19.4/6.2), the Cassini conjunction
(y = 1.14×10¹², slip 1.75×10⁻¹², margin ×1.3×10⁷) and the cluster ×1.96 against agentW's banked
numbers before any new use. Bug log (the honest sequence — each caught by an internal gate):
(i) the first quasi-static pass gauge-fixed the spatial metric to one function IN THE ACTION,
spuriously killing the slip channel (Δ_Φ ≡ Δ_Ψ exactly); caught against the GR
anisotropic-scalar limit and fixed with the two-function metric. (ii) the radial-divergence
computation double-counted ρ̄′ (chain-rule symbol + Derivative object); caught on inspection of the
remainder class, fixed, conditions re-derived. (iii) the J = Y/4 "solution" — a complete, elegant,
closed-form model (canonical kinetic term, χ = 2Φ exactly, closed-form calibration) — was
machine-verified to satisfy all lens-only conditions identically, and then killed by its own
consistency gate: it is the singular surface of the field equations (eqN|C=0 = −r²ρ̄ ≠ 0); the
conditions' vanishing was 0×∞. It is recorded in the .out as the dead end it is. (iv) the
perturbative-in-C solve was then invalidated AT MATCHED AMPLITUDE by the measured 10⁷ pollution —
which is not a bug but the obstruction itself: the construction's failure mode is the finding.
(v) one stale claim from the first pass ("first-derivative operators cannot slip" was initially
derived inside the buggy gauge-fixing) was re-derived legitimately in the corrected metric before
being used as wall 1. The K-extended run (`AGENTY_KEEP_K=1`) produces the quadratic-branch
expressions and timed out at the condition stage: logged as open, not closed. No git operations
performed.*
