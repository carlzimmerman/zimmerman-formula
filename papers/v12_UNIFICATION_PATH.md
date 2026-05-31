# A Path to Unification from Scaling-MOND Geometry

**v12 · Draft, 2026-05-31 · companion to `reviews/unification_path_gates.py`**

You asked for a path to a unified theory *from scaling-MOND geometry*. There is one — but it
only works after one honest reframe, and it lives or dies on one near-term experiment. This
document is the gated roadmap: four stages, each with a concrete deliverable and a pass/fail
criterion, written so the program survives on evidence rather than faith.

---

## 0. The reframe: which "geometry"?

The framework has used "geometry" two ways, and only one survives this session's audit:

- **Dead:** Z² = 32π/3 as the *compactification volume* that *derives the constants*. The
  constants are search artifacts (FDR), the value isn't a spectral invariant (six failed
  routes), and the matching cosmic topology is **excluded** (42° CMB ghosts absent,
  `matched_circle_ghost_location.py`; axis falsified by the repo's own code,
  `topology_chirality_audit.md`).
- **Live:** the **de Sitter horizon** geometry, in the *emergent/entropic-gravity* sense
  (Jacobson 1995; Padmanabhan; Verlinde 2011/2016; Milgrom's 1999 vacuum-MOND). Gravity and
  inertia *emerge* from horizon thermodynamics, and the **finite** cosmic horizon adds a MOND
  acceleration scale a₀ ~ cH(z). **Scaling MOND, a₀(z) = cH(z)/Z, is the signature that this
  emergence is physical** — and it's the one piece of the framework that is derived, distinctive,
  and falsifiable.

So: *the geometry worth unifying around is the cosmic horizon, not the compactification number.*
With that reframe, the path is real.

## 1. The organizing principle

> Gravity + inertia emerge from horizon thermodynamics (entropic gravity); the finite de Sitter
> horizon contributes a low-acceleration correction of scale a₀ ~ cH(z); the Standard Model is
> the matter content of the compactification. The whole sits in one action.

This is a member of a *real, live* research family (Jacobson derived Einstein's equations from
horizon entropy; Verlinde derives a₀ ~ cH₀; Milgrom derives MOND as a de Sitter vacuum effect).
The framework's specific contribution is the *scaling* a₀(z) = cH(z)/Z plus the *matter sector*
(the E₆ orbifold) bolted on. The unified action is written in `v12_SCALING_MOND_ACTION.md`.

## 2. The four gates

### Gate 1 — Falsification (near-term, decisive): the z>10 BTFR test
a₀(z)=a₀(0)E(z) makes deep-MOND v_flat = (G M a₀(z))¹ᐟ⁴ **larger** at high z by E(z)¹ᐟ⁴ — a
**factor 2.2–2.4 at z=12–14** versus constant-a₀, far above the ~25% mass-uncertainty band.
- **Pass/fail:** JWST/ALMA rotation speeds + dispersions at z>10. JADES-GS-z14 (ALMA,
  FWHM≈136 km/s) already sits with the *evolving* value (~121) and disfavors constant (~50).
- **STATUS: PASS-so-far.** If z>10 rotations come in at the constant-a₀ value, **the program is
  dead** and there is no unified theory to build. *Everything below is contingent on this gate.*
  (`jwst_rotation_predictions.py`)

### Gate 2 — Cosmological consistency: re-fit the CMB with *scaling* a₀(z)
Skordis–Złośnik RelMOND fits the CMB with **constant** a₀. Here a₀ is **~2×10⁴ × larger** at
recombination — but a₀/cH = 1/Z stays *constant* at every epoch, so the MOND effect is a fixed
fraction of horizon dynamics (arguably *more* natural than constant-a₀).
- **Pass/fail:** modify an SZ/`hi_class`-type Boltzmann code with a₀(z)=cH(z)/Z; demand the
  TT/EE peaks + lensing stay within Planck error.
- **STATUS: OPEN — the single most important *theory* calculation.** Computable with existing
  tools; not done; not faked. This is where the cosmology lives or dies at recombination.

### Gate 3 — Derivation fork: where does the O(1) come from?
a₀ ~ cH is derived; the divisor is the open piece. The de Sitter **temperature** gives **2π**
(a₀=cH/2π, 8% low); the framework's **2√(8π/3)** is geometric (exact). Both sit inside a₀'s
20% systematic, so **data cannot yet separate them**.
- **(a)** *Derive* 2√(8π/3) from horizon + compactification volume (the "coupling = √(volume
  modulus)" conjecture). High payoff, likely very hard — the horizon alone gives 2π.
- **(b)** *Accept* a₀ = cH/2π (clean, free, within systematics) and **drop the geometric-Z
  claim.** ← the honest default. It costs the "Z links to particle physics" dream and keeps a
  clean emergent-gravity MOND.
- **STATUS: FORK.** Most likely resolution: (b).

### Gate 4 — Unification: SM (orbifold) + gravity/MOND (horizon) in one action
- **What is genuinely unified:** gravity + the *dark sector* (MOND scale) from **one principle**
  (horizon thermodynamics). That is a real unification of gravity + inertia + dark phenomenology.
- **What is *attached*, not derived:** the SM, as the matter content of the compactification.
  The constants stay inputs/moduli.
- **The deep open link:** does the *same* compactification that yields the SM also fix the
  horizon coupling Z? That is the geometric pin of Gate 3(a).
- **STATUS: OPEN.** Best honest case = **one consistent action** (coexistence), **not** "the SM
  derived from geometry." That distinction is the whole ballgame — and the honest line.

## 3. What kind of unified theory this honestly is

**It is** a member of the emergent/entropic-gravity family, with the SM attached as matter via
the orbifold, and **a₀(z)=cH(z)/Z as a falsifiable signature** — live, ambitious, near-term-
testable physics. **It is not** a theory that derives the constants from Z² (that's the dead
numerology) and **not** a cosmic-topology claim (excluded). The honest ceiling is a *unification
of the gravitational/dark sector under horizon thermodynamics, with the SM as its matter* — not
a theory of everything. That is still a large, legitimate prize.

## 4. Order of operations (cheap/decisive first)

1. **Gate 1** — collect z>10 BTFR data. If it fails, stop. *(months–years; data is coming)*
2. **Gate 2** — run the scaling-a₀ CMB Boltzmann fit. *(a real, doable calculation)*
3. **Gate 3** — accept a₀=cH/2π, or attempt the horizon-volume derivation.
4. **Gate 4** — write the SM↔horizon coupling, *if* 1–3 survive.

**The program is only as alive as Gate 1.** That dependency is not a weakness — it is exactly
what makes this science where the numerology was not. The single highest-value next action is
Gate 2 (the CMB re-fit): it is the most important thing you can *compute today*, and it would
either turn scaling MOND into a serious cosmology or break it at recombination.

---

*Reproducibility: `reviews/unification_path_gates.py`, `reviews/scaling_mond_action.py`,
`reviews/horizon_a0_derivation.py`, `reviews/desitter_factor_audit.py`,
`reviews/jwst_rotation_predictions.py`. Papers: `v12_SCALING_MOND_ACTION.md`,
`v12_RADION_MOND_BRIDGE.md`, `v12_E6_GUT_CONSTRUCTION.md`. Lineage: Jacobson 1995;
Padmanabhan 2010; Verlinde 2011, 2016; Milgrom 1999; Skordis–Złośnik 2021.*
