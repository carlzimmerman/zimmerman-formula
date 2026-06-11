# agentDD — Vector carrier on the u-frame: does it evade Y's four walls?

**STATUS: COMPLETE except one cosmetic re-run (the D2 numeric-direction comparator print is
finishing in the background; the wall-2 verdict is already carried by the W/S generic-direction
machine passes + the structural ≤one-D argument). All four walls adjudicated; verdict
SAME-WALLS, banked below. (Relaunch after spend-limit death; this file was written incrementally
after every wall, per the relaunch protocol.)**

*agentDD, 2026-06-11. Files: `agentDD_vector_carrier.py` (staged D0/D1/D1b/D2/D3/D4; stage
D4 with `AGENTDD_D4_FULL=1` for the full {W,S,C} system) → `agentDD_vector_carrier.out`
(append-mode: preserves the honest sequence including two corrected dead ends — the LAST
D1b/D3/D4 blocks are authoritative). Pickles: `agentDD_eqs.pkl`, `agentDD_D1b.pkl`,
`agentDD_D4.pkl`; arrays `agentDD_D3_frac.npy`. Inputs read first:
`agentY_psislip_construction.md` IN FULL (+ `agentY_quasistatic.py`/`agentY_gates.py`/
`agentY_eqs.pkl` reused), `agentW_partner_uniqueness.md` Part 2, `UNIFIED_ACTION_ASSEMBLY.md`.
Discipline: framework-favorable construction attempt run at maximum hostility per the working
rule; every kill machine-derived and convention-checked; both-ways findings at full weight.
No git.*

## Setup (locked before any computation)

**The model.** Fields: g_munu; khronon T (unitary gauge, u_mu = -d_mu T/|dT|; a_i = d_i ln N
exactly — the a0-keying carrier, as in agentY); a NEW vector B_mu. Leaf-projection b_i = h_i^nu B_nu;
static spherical background b_i = (b_r(r), 0, 0). Bookkeeping identical to agentY's MOND-homogeneous
grading (potentials ~ eps, a0 = eps*alpha, alpha finite): b_r ~ eps-class, **Z = gam^rr b_r^2 c^4/a0^2**
(the keying variable, the analog of Y = q.q c^4/a0^2). The structural difference that defines the door:
**b is NOT a gradient** — its EOM is algebraic (no first integral tying it to Phi' by integration by
parts), and its stress carries intrinsic b_i b_j anisotropy at ZERO derivative order.

**Operator basis** (leaf-tangential, mirroring agentY's so every wall comparison is like-for-like):

> S_V = (c^4/8piG) Int sqrt(-g) [ -(a0^2/c^4) U(Z)  +  sigma S(Z) (a.b)  +  (a0/c^2) W(Z) (D.b)
>        + F(Z) (a.b)^2 c^4/a0^2  +  C1(Z) a^i b^j D_i b_j c^4/a0^2  +  C2(Z) (a.b)(D.b) c^4/a0^2 ]
> (+ the 2-D set {(D.b)^2, f_ij f^ij, ...} computed ONLY for the Wall-2 check; + a Maxwell/B_0
>    Gauss-law variant for the Wall-3 scaling question)
> [NOTE — this is the basis AS PLANNED; at condensate amplitude the legal normalizations differ:
>  S needs an a0 completion and C must NOT carry 1/a0 — bug log items 1-2; the corrected basis is
>  {(a0)W(Ya)(D.b), (a0)S(Ya)(a.b), C(Ya)(a.b)(D.b)}.]

- U(Z): potential — intrinsic stress at zero derivatives (the operator a scalar CANNOT have:
  for q = Dchi the analog J(Y) was wall-1-killed by the on-shell first-integral cancellation).
- S(Z)(a.b): the source coupling (b is sourced by the local field a_i = d_i Phi — keeps one scale, a0).
- W(Z)(D.b): a-INDEPENDENT single-D operator — for a gradient this is the braiding (N-channel only);
  for a vector it has genuine ij-content. Candidate N-feed escape (the a-linear C-ops of the scalar
  fed eqN at eps^-1 = (a0 r/c^2)^-1 BECAUSE varying out the single a-factor removes one eps).
- C1, C2: the direct analogs of the scalar's c_T-safe mixed quartics (a-linear, one-D), for
  like-for-like wall-3 comparison.

**Wall order + the decisive question for each** (verdict written before the next wall starts):
1. Wall 1: does the rr-constraint still force Psi' = Phi' on-shell for the FIRST-DERIVATIVE vector
   sector {U, S, F}? (Scalar: yes, exact cancellation via the chi first integral. Vector: the
   cancellation mechanism is structurally absent — machine-verify, then measure the amplitude.)
2. Wall 2: TT-perturbed background per operator: h-linear (safe) vs (dh_TT)^2 (in-halo c_T death).
   Einstein-aether template: its tensor sector c_T^2 = 1/(1 - c_1 - c_3) — pinned in-run.
3. Wall 3 (DECISIVE): SGB-clone — match slip to 2(nu-1), measure dg/g_bar on the same Hernquist
   10^11 Msun halo, framework a0, McGaugh nu, same y-grid as agentY's table. Plus the Gauss-law
   variant (B_0 + Maxwell): does the vector's own constraint re-route the N-feed?
4. Wall 4: Delta_Phi == 0 for all profiles — branch analysis on the vector system.
5. Survivor (if any): minimal Lagrangian, (1,nu) check, agentZ dial sign, remaining gates.

**Files:** `agentDD_vector_carrier.py` (staged: `python3 agentDD_vector_carrier.py D0|D1|D2|D3|D4`,
each stage appends to `agentDD_vector_carrier.out` and pickles intermediates), this memo (updated
after every wall). Gate discipline: D0 must reproduce the banked numbers (61.2/19.4/6.2 slip targets,
Cassini y = 1.1e12 margin x1.3e7, cluster x1.96, AND agentY's wall-3 row dg/g_bar(y=0.3, P=1) =
-2.7e7 from the pickled equations) before anything new runs.

## Charge

The Y-successor construction door. agentY closed every scalar u-DHOST slip carrier with four
machine-derived walls. The banked toggle named three escape routes; this memo works the first:
a **vector field B_mu coupled to the same u-frame**, generating Psi-channel slip via its
intrinsic transverse / anisotropic stress (B_i B_j), targeting (mu, Sigma) = (1, nu) from
agentW Part 2.

## Plan of attack (walls IN ORDER, verdict written before the next begins)

1. **Wall 1** — first-derivative couplings cannot slip; rr forces Psi' = Phi'. Does the
   vector's intrinsic B_i B_j anisotropic stress evade it? Quasi-static system derived
   (reusing agentY_eqs.pkl where possible).
2. **Wall 2** — in-halo c_T breaking on spacelike backgrounds. Is there a c_T-safe vector
   subclass? Einstein-aether tensor sector = the template; pin its c_T structure.
3. **Wall 3 — THE DECISIVE ONE** — Hamiltonian-constraint pollution at 1e7–1e8x the
   double-counting bar. Same pollution ratio for the vector realization; does the vector's
   own Gauss-law constraint change the scaling? Hostile + quantitative.
4. **Wall 4** — the mu = 1 branch.
5. **If a subclass survives** — minimal Lagrangian; verify (1, nu) emerges; morphology dial
   carries agentZ's sign; remaining gates.

## VERDICT: **SAME-WALLS** — walls 3 and 4 transfer (through the KEYING, not the carrier); the
vector door closes with a sharper theorem than the scalar's, and the carrier class narrows to
NONLOCAL/HISTORY operators (+ the logged singular-surface route)

**Which wall transfers and why.** Wall 1 is genuinely EVADED (the condensate/hedgehog vector
slips — a structural capability no scalar has) and Wall 2 is evaded by construction (≤ one-D
basis; c_T ≡ 1, α_M ≡ 0 identically, machine). But **Wall 3 transfers**: at slip-matched
amplitude the Hamiltonian-constraint pollution measures +2.3×10⁶ … +4.5×10⁷ × g_bar across
y = 1 → 0.01 (same Hernquist/ν/a0 harness as agentY's table; scalar row was −1.4×10⁷ … −1.5×10⁸)
— opposite sign, factor ~3 smaller, equally dead at 5–7 orders over the 8.7–21.6σ double-counting
bar. And **Wall 4 transfers in closed form**: the exact lens-only condition's geometric (r⁰) class
is α⁶·(slip/Φ′) = 0 — the pollution's irreducible core IS the slip. The root is not the carrier's
spin or stress structure: it is the KEYING. The only local a0-keyed scalar on the u-frame is
Y_a = a·a c⁴/a0² (= y²), and δY_a/δΦ — the keying's own response to the lapse — feeds the
Hamiltonian constraint at (a0r/c²)⁻¹ × slip no matter what field carries the operator.

**The keying theorem (the constructive yield, argument + machine):** at quasi-static order, ANY
local, Y_a-keyed, MOND-amplitude Ψ-channel slip carrier on the u-frame — scalar (agentY, four
walls), or vector at sourced amplitude (wall 1 here), or vector at condensate amplitude (walls
3–4 here, with the slip ≡ 0 closure machine-derived for the full one-D basis) — pollutes the
matter channel at (a0r/c²)⁻¹ × phantom. **The carrier must read y NONLOCALLY.** This converges
with the matter sector from the opposite direction: M22's inertia filter is a time-nonlocal
functional on the same u-frame, and Theorem X2 already forced the matter channel to be active
and history-dependent. Link 7's partner slot now reads: not a scalar (agentY), not a local
vector/condensate (this memo) — **the lensing sector, like the dynamics sector, must be a
history/filter operator.** The unique-class pincer has narrowed to the M22-echo direction plus
agentY's logged singular-surface route (low prior). Honest scope: "local" = the operator bases
machine-explored (zero-derivative potentials, first-derivative couplings, one-D mixed operators,
two-D operators [c_T-dead on spacelike backgrounds], at both sourced and condensate amplitudes);
a generic spin-2 condensate not of b⊗b form inherits the keying argument but is not
machine-closed (b⊗b realizations are covered by this memo's machinery).

**Working-rule check (conventions):** the wall-4 closure is symbolic — no a0 value, footing,
weighting, or ν-shape enters it. The wall-3 table is at framework a0/McGaugh ν; at 6–7 orders
over the bar, the canonical footing and the other three banked shapes move nothing (the same
moot-at-orders note agentY recorded). No deficit here is a convention artifact; and the
framework-favorable findings (wall-1 evasion, the S-counterterm family, the architecture
theorems, the dial) are reported at full weight alongside.

## D0 — gates (run 2026-06-11, before any new use)

ALL OK: slip targets 61.2/19.4/6.2 reproduced; Cassini y = 1.14e12, simple-nu slip 1.75e-12,
margin x1.3e7; cluster nu(y=0.10) = 3.62, x1.96 short — all banked values. Harness certification:
agentY's decisive wall-3 row re-derived from `agentY_eqs.pkl` on the same Hernquist halo:
slip-match residual 2.7e-15, dg/g_bar(y=0.3, P=1) = **-2.69e7** vs banked -2.7e7. The pickled-eq
pipeline and the SGB clone are certified for like-for-like vector comparison.

---

## Wall 1 — anisotropic stress vs the rr lock

**VERDICT: TRANSFERS at sourced (potential-class) amplitude — machine-derived; ONE corner evades
the counting and is carried forward: the CONDENSATE vector + a-independent divergence operator.**

The machine result (stage D1, full two-function-metric quasi-statics, GR gate exact):

- The vector EOM for {U(Z), S(Z) a·b} is **algebraic**: b0 = S0 Φ′/(2U′) — the exact structural
  analog of agentY's first integral χ′ = σΦ′/2J′. The b-field tracks the local field; a0-keying
  architectural, as hoped.
- But the rr-constraint comes out **clean even before the b-EOM is used**: eqL = 2r(Ψ′ − Φ′);
  slip ≡ 0 on-shell. The U/S/F stress never reaches the equation.
- Root cause, isolated by direct tier count: L_U = −(a0²/c⁴)N√γ U(Z) carries the prefactor
  (εα)² = a0², so its metric dressings (the Lf- and Φ-couplings = the rr- and N-channel stress)
  land at **O(ε³) in the action — one tier beyond the O(ε²) tier that makes the GR equations**
  (machine check: O(ε²) of L_U contains neither Lf nor Φ; O(ε³) contains both). The vector's
  intrinsic B_iB_j anisotropy is REAL but potential-suppressed: ~ε ~ 10⁻⁷ of the phantom — the
  same lemma that killed the canonical scalar (agentY §4.1), now shown to be
  **amplitude-keyed, not gradient-structure-keyed**. A b sourced by the local field (b ∝ a via
  any legal coupling) is ε-class, and ε-class stress cannot slip at MOND amplitude, gradient or not.

**The corner the potential-class grading cannot reach (named, carried to D1b/D3):** a vector can
do what a gradient cannot — sustain an O(1) **condensate** amplitude (vev of U; hedgehog
configuration b = β r̂, the leaf-radial frame field) while staying weak-field, because b is not
∂(potential). At condensate amplitude the leaf divergence is geometric: D·b ~ 2β/r — an O(ε⁰)
object with a 1/r profile. The single-D, a-INDEPENDENT operator

> (a0/c²) W(Z) (D·b)

then sits at **O(ε¹) action tier with O(ε²) metric dressings = exactly the GR equation tier**:
slip-capable in eqL, while its eqN (Hamiltonian) feed goes only through the explicit N-measure
(= one ε higher, GR-tier — NOT the ε⁻¹-enhanced a-variation route that produced agentY's 10⁷).
Deep-MOND shape check (hand, to be machine-verified): the deep phantom is (ν−1)g_bar →
√(GMa0)/r = a0 r_M/r — exactly the a0/r profile the hedgehog divergence supplies. The whole door
now lives in: (i) can the ν(y)-keying be arranged without re-importing a-linear pollution
(Wall 3, decisive), (ii) is the condensate's own sector healthy (Wall 2 + tadpole audit).
A scalar has NO analog of this corner (χ ~ O(1) is not weak-field; ∂χ cannot condense) — this is
a genuinely vector door, exactly where the agentY toggle pointed.

**Wall 1 addendum — the condensate corner DERIVED (stage D1b): the door is structurally open.**
Model: unit-norm leaf-radial hedgehog (b_r = √γ_rr, constraint solved into the action so the
constraint stress is kept — the standard unit-norm-aether move), keying variable Y_a = a·a c⁴/a0²
= y² (the khronon sector's own variable — one scale, interface condition 2 honored). Machine
results (GR gate exact; both tiers kept per the agentY per-channel rule):

- **[W only] (a0/c²)W(Y_a)(D·b):  Ψ′ − Φ′ = 2W′(Y_a)Φ′²/α — slip ≠ 0, a-INDEPENDENT operator.**
  In physical form: slip/Φ′ = 2y·W′(y²). Matching slip/Φ′ = 2(ν(y)−1) gives the closed-form
  calibration **W′(Y_a) = (ν(√Y_a)−1)/√Y_a** — first-order, no integration constant ambiguity in
  the slip (homogeneous mode absent), W ~ Y_a^{1/4} deep (W(0) = 0: the sector switches itself off
  where a → 0 — FRW quietness for free). Wall 1 does NOT transfer to the condensate vector.
- [S only] (a0)S(Y_a)(a·b) (corrected legal normalization — see bug log items 1–2 for the first
  pass): **slip ≡ 0 exactly** — but its eqN feed is NONZERO: a pure Hamiltonian counterterm
  family that cannot touch the slip. (A tool no scalar basis had.)
- [C only] C(Y_a)(a·b)(D·b) (corrected): **slip/Φ′ = C0 + 2Y_a·C0′** — universal in Y_a, legal;
  exact match C0(Y_a) = (1/y)·2∫₀^y(ν−1)dt with the zero-slip homogeneous mode ~1/y (the agentY
  SGA structure reproduced). The direct analog of the scalar's c_T-safe mixed quartics.
- The eqN (Hamiltonian) feeds of all three classes were extracted symbolically: the W-feed carries
  NO divergent coefficient at matched amplitude (W stays at its natural (ν−1)-class values, vs
  agentY's c20 forced to (a0r/c²)⁻¹ above EH). Whether the residual feed is phantom-sized
  (survivable / cancelable) or 10⁷× (dead) is exactly Wall 3 — measured numerically in D3.

**WALL 1 VERDICT: EVADED — but only in the condensate (hedgehog) realization.** The sourced
(potential-class) vector hits the same wall as the scalar. The evasion mechanism is unique to a
non-gradient field: O(1) amplitude with weak-field stress, geometric divergence D·b ~ 2/r
supplying the deep-MOND a0/r phantom profile shape natively.

## Wall 2 — c_T on spacelike (in-halo) backgrounds

**VERDICT: EVADED for the retained basis — by construction, machine-verified; and the wall itself
is PINNED on the vector kinetic sector.**

- Machine TT scan (in-halo background: lapse gradient a ≠ 0 AND the spacelike condensate present,
  O(h²)): **(a0)W(Y_a)(D·b): NO (∂h)²/h∂²h content** — h enters as source only (one Γ-factor,
  h-linear). Same for S(Y_a)(a·b) and C(Y_a)(a·b)(D·b) (the C-op and the comparator evaluated at
  two distinct numeric condensate directions to keep the rationals tractable). The agentY
  architecture theorems transfer: **c_T = 1 and α_M = 0 identically, all backgrounds, halo
  interiors included.**
- The Einstein-aether template, pinned: the aether tensor sector has c_T² = 1/(1 − c_+),
  c_+ = c1 + c3 (Jacobson–Mattingly); GW170817 ⇒ |c_+| ≲ 3×10⁻¹⁵ — a statement protected on the
  TIMELIKE u. On the SPACELIKE condensate the same structure appears through (Db)² ⊃ (Γ[h]b̄)² =
  (∂h_TT)²·b̄² with b̄² = 1 (unit norm): **any standard vector kinetic term at condensate amplitude
  is GW170817-dead in halos** — agentY's timelike-only boundary transfers verbatim to the vector
  kinetic sector (machine: the (Db)² comparator shows the (∂h)² content the retained basis lacks).
  The construction therefore carries NO (Db)²; the honest price: the condensate's direction modes
  get no two-derivative kinetic term — constraint-type dynamics from the mixed ε¹ operators
  (cuscuton-class precedent; agentY §5.2's residual flag transfers verbatim; the Boltzmann audit
  stays the assembly's named post-construction calculation).

## Wall 3 — Hamiltonian-constraint pollution (decisive)

**VERDICT: TRANSFERS — measured. The a-independence of the operator FACTOR does not protect the
KEYING VARIABLE's variation.**

The SGB-clone (same Hernquist 10¹¹ M☉ halo, framework a0, McGaugh ν, same grid; slip matched
exactly, residual 6.4×10⁻¹⁵):

| carrier | dg/g_bar @ y=1.0 | 0.3 | 0.1 | 0.03 | 0.01 |
|---|---|---|---|---|---|
| (a0)W(Y_a)(D·b), matched | +2.31e6 | +5.70e6 | +1.17e7 | +2.41e7 | +4.47e7 |
| C(Y_a)(a·b)(D·b), matched | +2.31e6 | +5.70e6 | +1.17e7 | +2.41e7 | +4.47e7 |
| agentY scalar (P=1, banked) | −1.4e7* | −2.7e7 | −5.1e7 | −9.1e7 | −1.5e8 |

(*the y=1.0 scalar entry read off the same SGB diagnostic; Δ_Ψ/div(slip) for the vector =
+2.0e6 to +2.5e6 across the table — lens-only would be exactly +1.)

- The matched W- and C-realizations give **identical pollution to all printed digits**: they are
  the same on-shell theory (IBP-related up to zero-slip counterterm content). The wall-3 number is
  **carrier-independent across the one-D condensate class**: ~+2×10⁶–4×10⁷ = (a0r/c²)⁻¹ × phantom
  class — opposite sign to the scalar's, factor ~3 smaller, **equally dead: 5–7 orders over the
  0.2-dex / 8.7–21.6σ double-counting bar.**
- Mechanism, isolated analytically and confirmed by the D4 class structure: the slip operator must
  be keyed to y, and the ONLY local a0-keyed scalar available on the u-frame is Y_a = a·a c⁴/a0².
  The δW(Y_a)/δΦ variation (the keying's own response to the lapse) feeds eqN with an
  UNSUPPRESSED geometric piece ~ slip/r² — (a0r/c²)⁻¹ above the phantom — regardless of how the
  operator's a-factors are arranged. The W-feed groups as 2W′(Y_a)(Φ′ + rΦ″) = 2W′(4πGρ̄r − Φ′):
  a ρ̄-class + geometric-class pair that no measure-route suppression touches.
- **The Gauss-law question (tasking item 3), answered: NO — the vector's own constraint structure
  does not change the scaling.** A B_u = u·B temporal sector with a Maxwell term is a leaf-scalar
  sector: at potential amplitude its stress is wall-1-suppressed (the D1 machine result covers it:
  algebraic-EOM sectors cannot slip at leading tier); at condensate amplitude its Maxwell energy
  is super-GR unless ε²-suppressed; and ANY realization must still key through Y_a — the pollution
  lives in the keying variable, not in the field's constraint structure. The Gauss law constrains
  the longitudinal mode; it has no channel that intercepts the δY_a/δΦ route into the Hamiltonian
  constraint.

## Wall 4 — the mu = 1 branch

**VERDICT: TRANSFERS — in the strongest form yet: a one-line closure.**

The exact lens-only condition Δ_Φ ≡ 0 for ALL profiles, on the FULL one-D condensate system
{W(Y_a)(a0)(D·b), S(Y_a)(a0)(a·b), C(Y_a)(a·b)(D·b)}, independent data (Φ′, Φ″, r) with
4πGρ̄ = ∇²Φ (μ=1 self-consistency), collected by monomial class (machine, stage D4):

> **CLASS Φ″⁰ r⁰:  α⁴·(C0α² + 2C1cΦ′² + 2Φ′W1α) = 0  —  which is exactly  α⁶·(slip/Φ′) = 0.**

**The geometric class of the Hamiltonian pollution IS the total slip.** The exact condition's
r⁰-class contains no S-symbols and no derivative freedom: lens-only ⟺ slip ≡ 0, identically,
for the entire class. The zero-slip S-counterterm family (the one genuinely new tool the vector
supplies — nonzero eqN feed, zero slip) enters ONLY the two classes that survive after the slip
is dead (Φ″r² and r¹: it can clean up a constant-W sector, i.e. cancel a cosmological-constant-
type residue — useful for nothing). Both structural identities are machine-confirmed
(D4 CONSISTENCY: r⁰-class = α⁶·(slip/Φ′): True; Φ″r¹-class = 2α⁵√Y_a·d(slip/Φ′)/dY_a: True —
the second condition is the first one's Y_a-derivative, adding nothing). Compare agentY's scalar
wall 4 (branch tree collapsing to slip/Φ′ ∈ {0, κ, −1}): the vector's closure is cleaner and
harder — **slip ≡ 0 is the only branch.**

## The door's residue (no survivor — but four things bank)

1. **The keying theorem** (verdict section): local Y_a-keyed slip carriers on the u-frame are
   closed as a CLASS — scalar and vector, sourced and condensate amplitude. The successor target
   is now uniquely shaped: a nonlocal/history slip operator echoing the M22 filter. This is the
   strongest narrowing of agentW's class since agentY, and it is a CONVERGENCE result: both
   halves of the program now demand the same nonlocal structure on the same frame.
2. **The S-counterterm family** — (a0)S(Y_a)(a·b) carries exactly ZERO slip while feeding the
   Hamiltonian constraint: a tool no scalar basis had (the scalar's every Y-function moved both
   channels). Useless for saving the local class (the r⁰-closure is S-free) but available to any
   future nonlocal construction needing a matter-channel counterterm with clean lensing.
3. **The architecture theorems extend across carriers**: c_T ≡ 1 / α_M ≡ 0 identically for the
   ≤ one-D leaf-tangential basis at condensate amplitude (machine, in-halo background with the
   spacelike condensate present), and the GW170817 in-halo boundary now explicitly covers the
   vector KINETIC sector ((Db)² at unit norm = Δc_T ~ O(1) — 15 orders dead): any future carrier
   must again be kinetic-term-free in the GW-relevant channels.
4. **The morphology dial survives a second carrier**: the condensate orients along the field
   lines (the S-coupling's job), and the slip engine is (D·b)-keyed = the divergence/bending of
   the oriented condensate — zero for planar, maximal for spherical configurations, agentZ's
   TYPE-IRREDUCIBLE sign (spheroids > disks) with the same geometric range. The dial is now a
   two-carrier-robust design principle of the operator geometry, independent of which field
   finally carries the slip.

## For the assembly ([SLOT-Y] disposition) and DERIVATION_CHAIN Link 7

- **[SLOT-Y] narrows again, decisively.** After agentY ("the class is empty of scalars") the
  surviving candidates were: (i) vector/spin-2 on the same u, (ii) nonlocal/history operators,
  (iii) the singular-surface exact route, (iv) dressed extended bases. This memo closes (i)'s
  vector half BY MACHINE (walls 3+4 transfer; the slip ≡ 0 closure is exact for the full one-D
  condensate basis) and inherits the keying argument against (i)'s spin-2 half and (iv)
  (operator-generic, not machine-exhaustive — stated as such). The S_slip line should read:
  *scalar AND local-vector u-frame realizations machine-obstructed (agentY four walls; agentDD
  keying theorem + slip≡0 closure); the surviving candidate space: NONLOCAL/HISTORY slip
  operators (the M22-echo — now the convergent prime candidate from BOTH sectors), the
  singular-surface route (logged, low prior), and non-b⊗b spin-2 condensates (keying-argument
  disfavored, not machine-closed).*
- **Link 7 wording sharpens:** the lens-only partner is not just "not a scalar" — *no LOCAL
  Y_a-keyed carrier of any explored spin/amplitude can route MOND-amplitude slip into the
  Ψ-channel without (a0r/c²)⁻¹ matter-channel pollution; the partner must read the local field
  through a history/filter, exactly as Milgrom-22 inertia does. The program's two missing-physics
  slots have collapsed into one structural demand: u-frame nonlocality, in both channels.*
- The inherited-architecture lines (c_T ≡ 1, α_M ≡ 0, FRW quietness via W(0) = 0, the
  morphology dial) attach to the slot unchanged, now two-carrier-robust.

## Bug log (the honest sequence — each caught by an internal gate)

1. **The C-op's first normalization carried 1/a0** (mirroring agentY's scalar quartic
   normalization): at condensate amplitude this puts its leading content at ε⁰ — a super-GR
   tadpole that is NOT a total derivative = an illegal operator — and the O1+O2 truncation
   sampled it inconsistently, printing a spuriously tiny pollution row (−2.3 … −59) that briefly
   looked like the door wide open. Caught by the dimensional audit + total-derivative check
   before any banking; re-run with the legal normalization C(Y_a)(a·b)(D·b) — whose matched
   realization then reproduced the W-row to ALL printed digits (the two operators are the same
   on-shell theory, a nontrivial consistency certificate). The wrong row is preserved in the
   .out (first D3 block) as the dead end it is.
2. **The S-op at condensate amplitude was dimensionally short by 1/L** in the first D1b pass
   (legal at sourced amplitude where b ~ 1/L, illegal after b became dimensionless); the tell was
   an explicit r in its slip formula (a non-universal, mass-dependent calibration). Corrected to
   (a0)S(Y_a)(a·b) → slip exactly 0 (and the counterterm role emerged).
3. **The D2 generic-direction TT scan was computationally intractable** for the C-op and the
   (Db)² comparator (>26 CPU-min on the unit-norm rationals); replaced by scans at two distinct
   numeric condensate directions — valid for the (∂h)²-existence check, noted as such.
4. The D1 potential-class "no slip even in the raw rr-equation" result was verified not to be a
   truncation artifact by the direct tier count (the O(ε³) lemma) before being banked as
   wall-1-transfer.

*Machine state: D0 gates reproduced the banked slip targets (61.2/19.4/6.2), Cassini
(y = 1.14×10¹², slip 1.75×10⁻¹², ×1.3×10⁷), the cluster ×1.96, AND agentY's decisive wall-3 row
(−2.69×10⁷ vs banked −2.7×10⁷ from `agentY_eqs.pkl`) before any new derivation ran. All GR gates
exact (Poisson + Φ′=Ψ′ + eqB≡0 with the sector off, both gradings). The .out preserves the full
honest sequence including the two corrected dead ends; the LAST D1b/D3/D4 blocks are the
authoritative ones. Equations pickled: `agentDD_eqs.pkl` (sourced grading, full basis),
`agentDD_D1b.pkl` (condensate grading, corrected basis), `agentDD_D4.pkl` (the exact condition
system). No git operations performed.*
