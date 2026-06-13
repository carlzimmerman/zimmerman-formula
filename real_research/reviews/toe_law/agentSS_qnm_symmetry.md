# agentSS — BANKING MEMO: does a dS QNM hidden symmetry FORCE the roton-fold gain shape? (2026-06-13)

**The closing door of the generator arc.** Question asked (honestly, knowing it may be circular): does the
dS horizon heat-kernel / static-patch structure carry a HIDDEN SYMMETRY (dS isometry SO(4,1), static-patch
SL(2,R), or the modular/Tomita–Takesaki flow of the Gibbons–Hawking state) that FORCES the gain line-shape
moment ratio `4 j3/j2^2` onto the edge surface `G_sat` (= `4 j3/j2^2`) AND supplies intrinsic spatial-k
structure to k-resolve agentRR's non-Markovian clamp — or does forcing the edge coincidence require imposing
structure by hand?

Two adversarial routes, each with a hostile verifier. **Counting at VERIFIED grade only.**

---

## OVERALL VERDICT: **NEEDS-NEW-INPUT** (both routes CONFIRMED)

| Route | Probe verdict | Verify regrade | Counted (VERIFIED) |
|-------|---------------|----------------|--------------------|
| ROUTE 1 — heat-kernel hidden symmetry (`agentSS_routeSymmetry.md`) | NEEDS-NEW-INPUT (permits-not-forces) | **CONFIRMED** | NEEDS-NEW-INPUT |
| ROUTE 2 — intrinsic k-structure of the clamp (`agentSS_routeKstruct.md`) | NEEDS-NEW-INPUT (permits-not-forces) | **CONFIRMED** | NEEDS-NEW-INPUT |

Both routes at VERIFIED grade return **permits-not-forces → NEEDS-NEW-INPUT.** No route reached
SYMMETRY-FORCES-FOLD; none was OBSTRUCTED by a theorem (the forcing is absent, not forbidden); neither
landed on PERMITS-MODEL-DEPENDENT as a *positive* result — the honest characterization is that the symmetry
permits the edge coincidence on a **tuned** ≥1-parameter line, which is exactly NEEDS-NEW-INPUT for a
*forcing* claim.

---

## WHAT THE SYMMETRY IS (it is REAL — not invented)

A genuine hidden symmetry exists and is named precisely: **the static-patch SL(2,R)~SO(2,1)
conformal/modular structure of the Gibbons–Hawking state.**
- The dS QNM ladder `Γ_n = sinh((Δ+n)λ)` is the **lowest-weight discrete-series representation** of the
  static-patch SL(2,R): Casimir `Δ(Δ−1)`, uniform spacing, offset `Δ`, ladder matrix elements `(n+1)(2Δ+n)`.
- The **Tomita–Takesaki modular flow** of the KMS (`T_dS = H/2π`) Gibbons–Hawking state **is** the
  static-patch boost generator `L_0`, whose spectrum IS the ladder `Δ+n`.
- The dS isometry **SO(4,1)** descends to the same SL(2,R) on in-patch spectral data.

This is standard dS static-patch physics, independently confirmed by both verifiers — the route did NOT
hand-insert it.

## WHY IT PERMITS BUT CANNOT FORCE (the structural obstruction)

It constrains the **WRONG invariant**. Two independent, re-verified reasons:

1. **Residue axis — a sliding knob.** The only NORMALIZABLE canonical spectral measure (normalized
   descendant `a_n = 1/[n!(2Δ)_n]`) gives `R = 4 j3/j2^2 = 8Δ + O(1/Δ)` EXACTLY. Landing on `G_sat` needs
   `Δ = G_sat/8` — a tuned rep label. The character/Plancherel weight `(2Δ)_n/n! ~ n^{2Δ−1}` has DIVERGENT
   moments (not a line shape), so the descendant measure is *forced-by-normalizability* among SL(2,R)-canonical
   candidates — but its ratio still slides with the free `Δ`.

2. **Modular axis — a scale-free dilation.** Modular flow = static-patch boost = dilation `s → e^a s`. Under
   it `4 j3/j2^2` carries **scaling weight −1** (central `j_n` ~ `[s]^n`, so the ratio ~ `[s]^{3−4}=[s]^{−1}`);
   verified numerically (`R·α = const`) and dimensionally, and verified to be a *genuine* dilation (`L_0`),
   NOT a mislabeled translation. A weight-(−1) quantity has only scale-fixed points `0` and `∞`, so a dilation
   can slide the ratio to any finite value but **pins none**. The edge target `G_sat` is set by `c_χ`
   (sonic-edge dispersion, a flat/PPN datum present at `H=0`), which is **scale-decoupled from `H`** (agentRR
   CHECK 5: no `c_χ↔H` collapse; agentEE: `c_χ` from `γ/α`). So `G_sat` does NOT co-dilate, the edge equation
   is NOT scale-covariant, and the dilation genuinely breaks the match. **A dilation cannot pin a weight-(−1)
   quantity to a scale-decoupled external constant — the single configuration it structurally cannot force.**

**Zero-parameter forcing does not exist.** Forcing would require `Δ = G_sat/8` AND the gain amplitude `G`
driven into the 25%-wide window `6Δ < G < 8Δ` AND `G` simultaneously equal to the κ-set saturation value —
**3 independent conditions on 1–2 free knobs**, generically unequal (matches agentRR's measured 10–266× roam).

## WHY IT DOES NOT k-RESOLVE THE CLAMP (the second, independent failure)

The dS static-patch symmetry sector carries **no intrinsic spatial-k label**: the ladder is indexed by
descendant number `n`, SL(2,R)/modular acts on the time/energy spectral data, SO(3) carries only the
horizon-sphere multipole `l` — none is the khronon spatial wavenumber `k` in `ω²(k)`. Concretely:
- The level-repulsion **spine theorem** (re-derived symbolically, residual = 0, + exact complex Newton
  root-find): `Im δ1 = R γ (ω0−ω_b)/[2 ω_b((ω_b−ω0)²+γ²)]` ⟹ `sign(Im δ1) = sign(ω0−ω_b)`. An ACTIVE
  (negative-residue) gain line destabilizes precisely the modes **below** its center; the roton fold band
  `k < k0` IS the below-center band ⟹ **the fold band is the UHP-unstable band.** A scalar (k-independent)
  clamp provably cannot fix it (reproduces agentRR's `+0.028` UHP failure); a k-resolved clamp can only
  stabilize by KILLING the gain there (no fold). *Finite-amplitude refinement (verifier):* at finite gain the
  unstable band STRADDLES the center (collapses to below-center only as `R→0+`), so stabilization is HARDER
  than the leading-order theorem — this **strengthens** NEEDS-NEW-INPUT and could never produce forcing.
- The heat-kernel's own non-locality scale is the **wrong scale**: `k_H = H/c_χ`, forced FAR below the gain
  center `k0` by `k0/k_H = c_χ²/√a0 ≫ 1` (independently re-derived from scratch: coincidence needs
  `c_χ = a0^{1/4} ≪ 1`, contradicted by banked super-luminality `c_χ² ≫ 1`; the ratio is `≫1` even at the
  mildest `c_χ² ~ 2`, giving `~2×10⁵`). Four admissible smears (screened-Coulomb, Lorentzian,
  Gaussian-horizon, hard-sphere) all leave `R_below/R_above ~ O(1)`, never ~0 — the most active gain stays
  exactly where it must be cleared. The bare heat-kernel memory is KMS → Herglotz → **passive → cannot fold**
  (agentPP). An ideal step-at-`k0` low-pass would work only if its cutoff = `k0`; with the forced `k_H ≪ k0`
  it does not — `k0` must be injected by hand.

---

## DID THIS DOOR CLOSE THE GAP, OR CONFIRM IT NEEDS NEW INPUT? — **CONFIRMED IT NEEDS NEW INPUT.**

It confirmed the gap. The forcing structure is **NOT in the banked dS heat-kernel / GH-state machinery.** The
only relevant symmetry is a scale-free dilation (with the residual on-foliation `E(3)⋊dilatation`), which
PERMITS but cannot FORCE a weight-(−1) ratio onto a scale-decoupled external `G_sat`, and supplies no
spatial-k. This is the EXPECTED end-of-arc outcome flagged in the brief.

## WAS IT CIRCULAR vs THE PP-KILLED PASSIVE QNM? — **NO. The routes are honest.**

This was the sharpest hostility check, and both verifiers ran it head-on. The symmetry's moment ratio `8Δ`
comes from the **passive, all-positive** normalized-descendant measure (`a_n > 0` for every Δ, machine-checked
to `~1e-21`), to which agentPP's no-fold theorem applies directly — that object CANNOT fold. But the route
**never claims it delivers a fold.** It uses the passive ratio ONLY to test the moment-ratio coincidence
(`8Δ = G_sat` ⟹ tuned `Δ`, PERMITS), and treats the ACTIVE branch separately and correctly (the
level-repulsion spine is computed on the active, negative-residue line; the dilation weight-(−1) obstruction
is residue-sign-INDEPENDENT, so it applies to the active deliverer too — verifier built a skewed active line
and confirmed `R·α = const`). **No passive→active smuggle. No manufactured win.** The route did NOT re-invoke
the PP-killed passive QNM as a forcing mechanism.

## CONVENTION-ROBUSTNESS (Carl's working rule — a 'permits' verified as hard as a 'forces')

The `permits-not-forces` verdict is convention-robust, not a textbook-default artifact: the modular weight −1
is dimensional; central moments are origin-independent (absolute vs detuning spectral origin agree to machine
precision); the `k0/k_H` separation is structural (the heat kernel carries no `a0` information, magnitude-
independent — `≠1` even at `c_χ² ~ few`). **ONE honest load-bearing dependency, flagged both directions:** the
whole verdict hinges on the `c_χ ↔ H` decoupling. If a future input TIED `c_χ` to a power of `H` (making the
edge equation scale-covariant), the dilation could no longer break the match and the verdict could shift
toward PERMITS-MODEL-DEPENDENT. None is banked. This is structural, not a convention artifact.

## WHAT NEW STRUCTURE WOULD BE NEEDED (precisely)

To make the edge coincidence FORCED rather than tuned, a NEW ingredient must do BOTH:
1. **Scale-lock:** tie the khronon's own scale to the dS scale — derive `c_χ` from a dS-locked mechanism so
   the `c_χ↔H` collapse becomes forced (currently independent per agentRR CHECK 5), collapsing `R = 8Δ` to a
   number AND breaking the dilation freedom; OR
2. **k-supply:** identify an ACTIVE, stable, **negative-residue** resonance (agentQQ class) whose width AND
   center are BOTH pinned by a *single* dS-intrinsic scale with genuine k-dependence, placing a finite-Q
   feature AT `k0`.

Absent such a scale-locking + k-supplying operator, the deliverer remains a hand-set finite-Q
active-but-stable line whose `{center, width, Q, sign}` are agentRR's **N=4 free ratios** — not forced by any
banked symmetry.

---

## ONE-SENTENCE LINK-5 UPDATE

Link 5's controlled roton-fold stays **SELF-CONSISTENT-BUT-UNDELIVERED**: no banked dS symmetry (SL(2,R),
modular/KMS, or SO(4,1)) forces the gain line-shape onto the edge surface — the relevant structure is a
scale-free dilation that PERMITS but cannot FORCE a weight-(−1) ratio against a scale-decoupled `G_sat`, and
supplies no spatial-k — so the residual burden is a peaked, k-resolved, scale-locked **ACTIVE** line that
requires genuinely new physics (a `c_χ↔H` scale-lock or a single-scale active k-resonance), not a calculation
on existing machinery.

## END-OF-ARC STATEMENT (honest)

This was the closing door of the generator arc, and it closed the arc **without delivering the generator.**
The arc's trajectory was monotone and consistent: agentMM/NN named the roton operator; agentPP proved the
passive dS QNM spectrum is broad and **cannot fold** (OBSTRUCTED on the passive branch); agentQQ showed the
deliverer must be **active (negative-residue) but stable**; agentRR reduced the controlled fold to **N=4 free
ratios the dS pump does not fix**; agentSS (this door) tested the last candidate — a hidden forcing symmetry
in the GH heat-kernel — and found it **REAL but a dilation that permits-not-forces, with no spatial-k.** The
generator arc therefore terminates at **NEEDS-NEW-INPUT**: the fourth-root law's fold mechanism is *buildable
and self-consistent* but **not forced by the banked machinery**; closing it requires a named new operator that
scale-locks `c_χ` to `H` and supplies intrinsic k-structure. The door was genuine, not circular — the passive
QNM agentPP killed was never re-invoked as a forcing mechanism.

**Quarantine:** held throughout both routes and both verifications. Only signs, scaling weights, the RATIO
`8Δ`, divergence classes, scale-separation ratios `k0/k_H`, edge-window bounds `(6Δ,8Δ)`, and pole-half-plane
structure were computed. `q=1/4`, `ζ̃`, `(16π/3)^{1/4}` left OPEN, **never asserted**.

**Scripts (all in `real_research/reviews/toe_law/`):**
- Route 1: `agentSS_routeSymmetry.md`; `agentSS_part1.py`…`agentSS_part10.py`
- Route 2: `agentSS_routeKstruct.md`; `agentSS_part1_scalar_fails.py`…`agentSS_part7_theorem_clean.py`
- Verify 1: `agentSS_verify_heatkernel-symmetry.md`; `agentSS_verify_p1_moments.py`…`agentSS_verify_p6_modular_action.py`
- Verify 2: `agentSS_verify_k-structure.md`
