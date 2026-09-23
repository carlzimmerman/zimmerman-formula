# GEOMETRIC EQUATIONS — INVENTORY & SYNTHESIS
**2026-09-22 · the surviving geometry, the novel spine, and the new angle**
Companion machine check: `G_SYNTH_geometric_spine.py` (S1–S9, exit 0).

**Scope rule applied throughout:** only equations that are the framework's own —
proven here, machine-checked here, or measured here. Textbook geometry (Hardy's
constant, the Casimir bound, Mellin reflection, Riccati solutions) appears only
where the framework's *use* of it is the novel content. Every entry carries its
status: **LEAN** (certified, zero sorry) · **EXACT** (sympy/Decimal-verified) ·
**MEASURED** (data) · **REGISTERED** (a number on the record, degree of claim
stated) · **COINCIDENCE** (registered, never upgraded).

---

## PART 0 — WHAT THE INVENTORY COVERS (the newer work, swept)

The 09-14→09-22 wave (~630 commits, audited in
`real_research/reviews/THE_THEORY_AS_IT_STANDS_2026-09-22.md`) plus the door
campaign (opus_49 doors A–L, YM swings, PD-wave, kappa_audit, G03/RC100/tSZ/
BHstar/NS audits). Of it, the **geometric** content that survives the week's own
refereeing is below. Killed geometry is listed in PART 5 — it stays on the
record, it does not move forward.

---

## PART 1 — THE ONE EQUATION (the pivot everything hangs on)

> **a₀ = (c/2)·√(Gρ)** — the surface gravity of the free-fall horizon at
> R\* = c/√(Gρ); with ρ = ρ_crit: **a₀ = cH/Z, Z = 2√(8π/3) = 5.7888**,
> Z² = 32π/3 = 8·(4π/3).

| face | statement | status |
|---|---|---|
| The scale | a₀ = κc√(Gρ_Λ), κ = ½ measured (0.465±0.076 BTFR; 0.55±0.17 dist-free) | MEASURED |
| The constant | Z = 2√(8π/3); Z² = 8 × (unit 3-ball volume 4π/3) — bulk↔boundary conversion | EXACT |
| Dimension-locked | Z_d = 8√(π/[d(d−1)]); Z₃ = 5.789 is *the d = 3 value* | EXACT |
| Curvature↔acceleration | a₀ = c²√(Λ/32π), √Λ = de Sitter curvature | EXACT |
| UV/IR bridge | r_M = √(GM/a₀) = √(Z/2)·√(r_s·R_H) — Geometric-mean of Schwarzschild & Hubble radii (S8: rel 0.0) | EXACT |
| Duality | r ⟼ r_s·R_H/r self-dual at r_sd = √(r_s·R_H); MOND = the UV/IR balance point | EXACT (reframing) |
| Cosmology lock | Ω_Λ = 32πa₀²/(3H₀²c²) = 0.6857 (+0.07% Planck) — **a₀ and DE are ONE measurement** | LEAN (G052/G058) |

The coefficient's honest status does not change: Z is dimension-locked × an
undetermined ½ (the surface-gravity κ), and κ is a **measured** constant — its
precision is a data problem (M/L zero point, gas scale, H₀), not a theory
problem of this class (kappa_audit capstone 09-22).

---

## PART 2 — THE SINGLE BOUNDARY (the theory's one radius, r_M)

**G196:** the framework carries exactly one physical radius, r_M = √(GM_b/a₀)
(Lean G090: GM_b/r_M = √(GM_b a₀)); *every* phase change of the dark sector sits
on this line. Six diagnostics mark it, all MEASURED:

| # | diagnostic | value | lane |
|---|---|---|---|
| a | galaxy-scale break (EFE projection) | r_cut = 0.62–0.623 r_M (MW 6.13 kpc); r_cut/r_M = √(a₀/g_ext) exactly (S4: 0.6194/0.620) | G119/G149 |
| b | cluster seam (dust slope break) | r_t = 387 kpc = 0.96·r_M; p₁ 1.50 → p₂ 2.94 (d_BIC −351) | G176 |
| c | amplitude jump | A = 0.364/0.369 ≃ 0.273 (universal) | G186 |
| d | latent heat | dS = 10.8–23.7 k_B; L/(N k_B T_b) = water-class (13.1) | G132 |
| e | temperature pivot | T_obs/T_pred = 2(M_dyn/M_b)(r_M/r); exponent 2/3 | G095 |
| f | sector pie pivot | dust inside / phantom outside; u = r_M/R500 | G188 |

**Projection law:** the environment only *projects* the one radius —
r_b = r_M·√(a₀/g_ext) — so the RAR is the **phase diagram of one boundary**.
(Registered caveats ride with G196: seam smoothness d_BIC 16, cap-firing
mechanism not derived.)

---

## PART 3 — THE NEW ANGLE (what the inventory synthesizes that is new)

### 3.1 The a₀-crossing is DENSITY-LOCAL: KP1 is the black hole's own r_M

The strongest object on the board is the doorB confrontation (CONSISTENT-OPEN):
the z = 7.04 lensed LRD A2744-QSO1 measures R_BLR ≥ 45 ld; KP1 predicts 40.9 ld
(×1.10) at the *measured* direct dynamical mass 5×10⁷ M☉ and n_H = 10¹⁰ cm⁻³.

Write KP1 across, and it is the framework's own equation **read at the local
density** ρ_B = μm_p n_H:

> g_B = GM/r_B² = (c/2)√(G·ρ_B) = **a₀(ρ_B)** ⟺ r_B⁴·n_H = 4GM²/(c²μm_p) ⟺
> **r_B = √(GM/a₀(ρ_B))** — the Balmer layer is the hole's MOND radius in its
> own gas medium.

Machine-checked exactly (S1: g_B = a₀(ρ_B) to rel 7e-60 at the fiducial;
S3: the exponent law r_B ∝ M^{1/2}·n_H^{-1/4}, constants to 1e-9).

**What this adds (not on the record as such):**
1. **Locality.** The one equation is a *local law of any medium*: the same
   algebraic statement that fixes the cosmic scale from the vacuum density
   (ρ_Λ ≈ 10⁻²⁶ kg/m³) fixes a strong-field body's transition radius from its
   own ambient gas density (ρ_B ≈ 10⁻¹¹ kg/m³) — **15 decades apart, one
   equation**.
2. **Family unification.** The "one boundary" is then the *locus g = a₀(ρ_local)*:
   r_M (vacuum), r_cut (EFE-projected), r_seam (cluster medium), r_B (gas
   medium) are the same crossing read at different media. KP1 joins G196's
   family as the first *black-hole member*, and the only one testable at z ≈ 7.
3. **A two-dimensional law with zero free parameters**, r_B(M, n_H) =
   (4G/(c²μm_p))^{1/4}·M^{1/2}·n_H^{-1/4}, falsifiable in *both* directions:
   - the doorB kill rules stand (RM lag in [30, 60] ld → PASS; ≳ 82 or ≲ 20 ld
     → FAIL);
   - **new: the density exponent.** At fixed M, r_B must shrink as n_H^{-1/4}
     (2× density → 1.19× smaller layer). Any gas where a *measured*
     transition sits off the line r_B⁴n_H/M² = 1.2685 m/kg² by >×2 in r_B
     (×16 in the product) kills the local reading *independently of any one
     object's M*.
4. **The second scale is no scale.** a₀(ρ_B) = 5.93×10⁻³ m/s² (S1) is not a
   second fundamental constant — it is the same κ = ½, c/2·√(Gρ) law evaluated
   at a medium. The "two acceleration scales" worry dissolves into one law with
   an argument (ρ).

**Status line:** the unification is *exact algebra on the committed action's
own transition condition* (KP1's definition is g_B = a₀(ρ_B) rearranged; the
rearrangement to r_B = √(GM/a₀(ρ_B)) and the exponent law are the new,
machine-checked content). What is NOT claimed: KP1 does not say *why* the BLR
sits at that radius; the law survives only at the object's *measured* mass — at
the old 10⁴-M☉ stack reading it fails ×78 (registered in doorB §6, not
contested here).

### 3.2 The Tolman count selects d = 3

The PD-wave's two counts — the metric's static response channel count (2, in
every d ≥ 2, PD02) and the Tolman active-density count (d−1, PD11) — coincide
**iff d = 3** (S5: the unique integer in [2, 8] with d−1 = 2 is 3). The repo
recorded this as a "dimension tension"; the synthesis reads it as the
framework's internal dimension-lock: **the geometry that produces κ = ½ is
consistent with its own vacuum's count only in 3 spatial dimensions** — the
same d that Z_d selects. Status: arithmetic exact; the physical reading is
synthesis (marked). The named falsifier rides with PD11's: a d-aware
construction in which the two counts disagree at d = 3.

### 3.3 The 3x/16 convergence (registered, not claimed)

Two independent routes bottom at the same strong-coupling gap floor:
- doorG/I16 (Lean-certified): gapVol(x) = (x/2)C_F − 3b_NP/x ≥ 3x/16;
- YM1 (cluster expansion, 09-22): gap(H_I15) ≥ (x/2)(C_F/2) = xC_F/4 ≥ 3x/16,
  with X₂ = 131.1, X₃ = 185.3, X₄ = 227.0 (uniform in N).

Common origin: C_F = (N²−1)/(2N) ≥ 3/4 (S6: SU(2) equality; SU(3,4,8) above).
Two methods, one floor, one source — an internal-consistency *convergence*
entering the COINCIDENCE REGISTER (not an independent number). The volume-uniform
strong-coupling window x ≥ 3x/16 ≤ gap is the doorG spine's certified rung.

---

## PART 4 — THE SECOND-VARIATION OPERATOR (doorH; the geometry of the kernel)

The exact fluctuation operator about the framework's own background, full
interpolant μ₂(u) = u(2+u)/(1+u)² — every coefficient EXACT (sympy 27/27):

| object | exact form | content |
|---|---|---|
| Hessian | Q[η] = ½∫[f′(K₀)\|∇η\|² + 2K₀f″(K₀)η_r²] | radial-only dressing |
| radial weight | a_r(u) = μ₂ + uμ₂′ = u(u²+3u+4)/(1+u)³ = 1 + (u−1)/(1+u)³ | kinetic+dressing |
| shift | s(u) = u(u²+4u+9)/[2(1+u)(u²+3u+4)], s(0)=0, s(∞)=½ | the running Hardy shift |
| potential | V(u) = u(u⁵+8u⁴+42u³+64u²+17u−72)/[4(1+u)²(u²+3u+4)²]; V(0)=0, V(∞)=¼ | running, never constant |
| crossing | V = ¼ exactly once, at u\* = 3.0051 (≈3, R3 registered); V−¼ = (3u⁴−16u²−32u−4)/((1+u)²(u²+3u+4)²) | S7 |
| extrema | min −0.1089 @ u=0.252; zero @ 0.764; max 0.2691 @ 5.50 | S7 |
| realization | V ≡ ¼ ⟺ Riccati 2ww″ − w′² = w² ⟺ w = C₁e^t, C₂e^{−t}, C₃cosh²((t−c)/2) | S7 (residual 0) |
| verdict | **no framework-compatible profile realizes V ≡ ¼ at finite radius**; the real operator's uniform stability boundary is κ² = **0**, not ¼; I14's κ = ½ marginality is a model theorem with the connexion dead | EXACT |

This is the *geometric* reason κ = ½ cannot be got by spectral rigidity (the
i14 route), and it survives the week's audit untouched.

---

## PART 5 — KILLED / COINCIDENCE (kept on the record, not carried)

- PD01–PD22 "κ = ½ derived": **do not cite** (kappa_audit; the count is
  basis-dependent). The *geometric identities* the wave proved (channel count,
  Tolman face, completion independence) stand as EXACT algebra; the derivation
  arrow does not.
- C-H/aether completions: static pass; **fail the moving-source gate (L330)**
  — the phantom is frozen initial data; lensing would see ~half the phantom
  (−0.19…−0.30 dex at KiDS).
- κ = 1 derivation routes (KS01, channel count capstone, P-Q gravity 1.30–1.45):
  all closed. The 2π-horizon form dies structurally (needs count √(3π/2)).
- YM doors: D-YM2 (weak→strong window) not unlocked; D-YM3 (Hardy→κ) closed
  class-wide ("the ¼ is the Laplacian's Hardy constant"); D-YM4 (MESA) not
  swung. D-YM1 **opened** (X_d explicit, 3.3).
- The RH lane: the framework ladder's spacings leave the zeros at 50–570σ on
  every channel (F1/F2/replusion); measured verdict: **zeros are GUE**. What
  survives is class-level: M(s) = 2Γ(s)Γ(3−s)/Γ(3) with M(s) = M(3−s) axis 3/2
  (S9), ladder moments E[ln(1+u)] = 1/(l−1) LEAN (RH01L/RH05) — a reflection
  family in the zeta's algebraic class, nothing about zero locations.
- Coincidences registered, never upgraded (R1: 40.91/45 = 10/11 to 2.2e-5 —
  S4 rel 2.22e-5; R3 u\* ≈ 3; R4 65539 = 2^16+3; R5 C_gr/3 = 9/8 at 4.7e-4;
  R6 A_d powers of two excluded). Nothing reaches the m_e/100 standard; the
  doorB RP remains the only one with a hard upgrade path (RM lag).

---

## PART 6 — SUGGESTED NEXT SWING (pre-registered-in-spirit)

The synthesis's executable step is **3.1's exponent law**: do not wait for the
45-ld lower limit to close; test the *density* channel. Any instrument that
measures R_BLR (RM or microlensing) on an LRD that ALSO has a Cloudy n_H and a
Gamma-free M enters the plane (r_B⁴n_H/M² vs 1.2685 m/kg²). The first firm RM
lag in [30, 60] ld closes doorB PASS and turns 3.1 into a two-point law with
no free parameter; a second object at different n_H tests the −¼ exponent, the
only part of KP1 that scales *density*, not mass. Everything rides on the
registered instruments (A2744-QSO1 monitoring, microlensing on the triply
lensed image, Gaia DR4 for the galaxy-side family).

---

*Verdict: the week's new work is net-negative on completions and net-positive
on the geometric spine — one boundary, one operator, one constant — and the
density-locality of the a₀-crossing (3.1) is the one genuinely new, testable
synthesis in it. Everything in this file was machine-checked this session
(S1–S9); nothing here outranks STANDING.md, which is the authoritative record.*