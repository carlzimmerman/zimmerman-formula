# ROUTE A — POTENTIAL-DEPTH (|Φ|/c²)-keyed cluster boost — verdict 2026-06-20

**Workflow:** `cluster_doors3` Route A. The natural complement to the FAILED density-keying:
key a galaxy-safe cluster boost on potential DEPTH |Φ|/c² (clusters out-rank galaxies in
exactly this), not density (the density-a0 floor broke galaxies because galaxies are
*denser* than clusters). Real A2029 (relaxed, XRISM-clean) + RXJ1347 total/baryonic
potentials; real 175-SPARC RAR veto; Cassini/compact-object veto. Quarantine held
(a0=9.36e-11 input, never asserted derived). Both ways.

## HEADLINE (both ways)
**Route A is the BEST no-particle cluster door found in the whole hunt — it uniquely PASSES
G1 (sufficiency), G2 (galaxy-veto), and G4 (Cassini) — but FAILS G3 (no-new-particle) on
naturalness. It does NOT close the door, but it materially CORRECTS the prior over-harsh
dismissal.**

| Gate | Verdict | Number |
|---|---|---|
| **G1 SUFFICIENCY** | **PASS** | A \|Φ_bar\|-keyed boost closes the gas-tracking A2029 core: coverage ~100–121% across 20–500 kpc, right magnitude AND ~flat shape |
| **G2 GALAXY-VETO** | **PASS** | SPARC RAR 0.1409 → 0.1408–0.1423 dex (floor-level); early-types ~1–2.5% at their measured RAR points |
| **G3 NO-NEW-PARTICLE** | **FAIL** | needs a \|Φ\|/c²-linear a0 coupling of size **amp~1.5×10⁵** — ~10⁵× a natural O(1) relativistic coefficient; no framework field carries it |
| **G4 CASSINI/solar** | **PASS** | Sun's \|Φ\|/c² at the planets ~1×10⁻⁹ → a0_eff/a0 = 1.0001 at Saturn; deep Sun/NS Φ is at g>>>a0 (boost ~10⁻¹⁹ moot) |

## THE LOAD-BEARING FIX that revived G1 (corrects the prior dismissal)
The prior `solution_hunt/galaxy_veto_potential_route.py` keyed on **|Φ|/c² ≈ Vbar²/c²**
(the LOCAL circular speed squared) and found only a ~5x core/disk contrast → "breaks the
veto (linear) or hand-tuned step (steep), and wrong shape." That used the WRONG quantity.
The gravitational potential **DEPTH** is the *integral* |Φ(r)|/c² = (1/c²)∫_r^∞ g dr′
(deepest at the center, far larger than the local v²). On the true integrated **baryonic**
depth:
- cluster-core (A2029 @200 kpc) |Φ_bar|/c² = **2.92×10⁻⁵**; deepest SPARC disk = **4.8×10⁻⁶**
  → **6× contrast** (non-circular, baryons-only; was 16× on total Φ — the circular footing).
- A p=1 |Φ_bar|-linear law (amp~1.5×10⁵) **closes the relaxed core** — coverage 105%/100%/121%
  at 20/200/500 kpc — because on A2029 the required boost B_req≈1.6–1.9 is **nearly flat**
  (slope −0.03) and |Φ| is nearly flat in the core (slope −0.07). So the "wrong radial shape"
  objection does **not** hold on the relaxed/XRISM-clean cluster.
- This is the **first** no-particle term in the entire cluster hunt that genuinely reaches the
  ~30–49% residual at a0=9.36e-11 with a galaxy- and Cassini-safe term.

## Why G3 kills it (the honest concession)
- A |Φ|/c² correction is a post-Newtonian / relativistic term; the **natural** coefficient is
  O(1): a0_eff = a0(1 + O(1)·|Φ|/c²) → at the core gives a boost of **+0.003%**, useless.
  The core needs a0_eff/a0 ≈ 3.4 → the coupling must be **~8×10⁴–1.5×10⁵**, five orders above
  natural. That is a new dimensionless number put in by hand.
- **No framework field carries it.** dS-Unruh modified inertia sets a0 from the *cosmological*
  (cH_Λ)² floor — T_eff ~ cH (the de Sitter horizon), **blind to the local potential by
  construction**; AeST has no |Φ|-linear a0 term (which is exactly *why* MI ≡ AeST-MG to
  machine precision in the core). Keying a0 on local |Φ| with amp~10⁵ is a NEW coupling, not
  own-field, not known-physics. Quarantine forbids asserting a mechanism that forces it.
- The p≥2 steep forms close the SPARC veto more comfortably (max boost 1.02–1.12x) but only by
  becoming a near-**step-function** in |Φ| tuned to the core value (amp 5×10⁹–1.8×10¹⁴) — a
  hand-placed threshold, not a coupling. Re-confirms the prior "steep = tuned step" finding.

## Both-ways corrections logged this pass
1. **Prior dismissal was too harsh (credit to Route A):** the v²/c² proxy under-stated the
   contrast (5x → true 6x baryonic / 16x total) and used merger-inflated targets; on relaxed
   A2029 the law DOES close the core with ~right shape. G1 genuinely PASSES — corrected.
2. **Self-caught artifact (against Route A's favor was over-stated, then corrected back):** an
   intermediate check flagged a 52–72% RAR shift for early-type CENTERS (a0_eff/a0~2.4–3.2).
   That was an artifact of pinning |Φ| at the deep center while scanning g across the band. At
   the radius where ETGs are actually *measured* on the RAR (g~a0, r~10–19 kpc) |Φ_bar|/c² is
   only ~3–7×10⁻⁷ → a0_eff/a0~1.05–1.10 → real shift ~1–2.5% (within floor). G2 PASSES for ETGs
   too — the deep center is g>>a0 (boost moot), the g~a0 band is shallow-Φ. Caught both ways.

## STANDING (unchanged at the top level; Route A door characterized)
The ~30–49% gas-tracking cluster-core residual stays the **shared relativistic-MOND open gap**.
Route A is the strongest no-particle attempt — magnitude, shape, galaxy-veto and Cassini all
clear — and dies only on G3 (no framework field forces a local-|Φ|-keyed a0 with amp~10⁵). It
does NOT relocate to a new particle (it's a gravity-sector modification), so it's a *cleaner*
near-miss than the sterile-ν patch. The honest residual-closure status: **PARTIAL** — Route A
would close it IF a field that forces a |Φ|-keyed a0 with amp~10⁵ were exhibited; none is, and
the framework's own dS-Unruh + AeST fields provably do not. No manufactured cure (G3 conceded
straight), no reflexive dismissal (G1/G2/G4 credited at full weight; the prior harsh read
corrected).

**Scripts:** `cluster_doors3/routeA_potential_depth_keyed.py` (true integrated depth, contrast,
SPARC veto, Cassini), `routeA_followup_shape_cassini_dwarf.py` (full-profile shape, deep-galaxy,
Cassini detail), `routeA_circularity_and_baryonic_phi.py` (the non-circular baryonic-Φ footing),
`routeA_G3_naturalness_and_final.py` (the G3 naturalness kill + final verdict).
