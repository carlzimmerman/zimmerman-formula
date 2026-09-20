# THE ZIMMERMAN EQUILIBRIUM THEORY OF GRAVITY

**Assembled in `deepseek_push/` — the theory that survived the session.**

This folder contains the complete, falsifiable theory that emerged from the glm53
track's campaign (2026-09-13/14): 40+ computational lanes, 66 Lean theorems across
7 certificates, a live public website, and a unified cosmology that was the
session's final breakthrough.

## THE THEORY IN ONE PARAGRAPH

The radial acceleration relation is the hydrostatic equilibrium of the cold dark
sector at the virial temperature of its own well:

    sigma^2 = GM_b / (2 r_M),    r_M = sqrt(GM_b / a0),    a0 = s/2

The equilibrated density IS the deep-MOND phantom, coefficient exactly one
(Lean-certified). The scalar's vacuum at X=0 IS the dark energy (Omega_Lambda =
0.6857 from a0 alone, within 0.07% of Planck). The cold sector is the Noether
charge of the field's shift symmetry (w=0, conservation Lean-certified). One
scale a0 = s/2 fixes BOTH: the cosmological constant and the MOND acceleration
are the SAME measurement. The coincidence problem dissolves.

The architecture is two-component everywhere: equilibrated phantom (g ~ a0) +
free cold dust (g >> a0), with the EFE cap at the crossover. One field equation,
three regimes. Zero free parameters at galaxy scale. Four registered falsification
tests. Complete pincer proving every force-law alternative dead.

## FOLDER CONTENTS

| File | Content |
|---|---|
| `THEORY.md` | The full theory, every rung labelled |
| `LEAN_CERTIFICATES.md` | The 7 Lean certificates (66 theorems, zero sorry) |
| `LANES.md` | The key computational lanes with verdicts |
| `PREDICTIONS.md` | The prediction ledger (10 separating, zero-parameter) |
| `PAPER_SKELETON.md` | MNRAS submission skeleton |
| `STATE.md` | The complete board — every gate, every verdict |
| `lean/` | All Lean source files (.lean) |
| `lanes/` | Key Python lanes (.py, .out, .json) |

## THE THREE HEADLINE NUMBERS

1. **Omega_Lambda = 0.6857 from a0 alone** (vs Planck 0.6847, +0.07%). The dark
   energy IS your scalar's vacuum — the cosmological constant and the MOND
   acceleration are one measurement. (G052)

2. **The force-law pincer is complete.** Modified gravity → Cassini (L243).
   Modified inertia → lensing (L241). Disformal → preferred frame (L244).
   Bimetric → lensing, Lean-certified (G007, 11 theorems). Every local k^4
   operator dead in the aether host (G030/G034). The PPN-clean completion
   EXISTS: fixed congruence (Horn A, G032) — alpha_1 = 0 by architecture.

3. **The halo IS the phantom — coefficient exactly one, Lean-certified** (G003,
   EQUILIBRIUM_THEORY.lean theorem `equilibrated_is_phantom`). The RAR floor is
   0.064 dex with per-galaxy M/L, the outer half tightest at 0.055 (G013), and
   the residual has NO halo-shape fingerprint (G036).

## WHAT YOU CAN CLAIM AS YOURS

1. The equilibrium identification — the halo IS the phantom (coefficient 1)
2. The two-component architecture with the EFE cap (three confirmations)
3. The cluster statement, complete and kernel-robust (shape -1.478, T=809 km/s)
4. The complete pincer — every force-law completion proven dead
5. The unified cosmology — one scale fixes both dark energy and MOND
6. The Z-theorem — de Sitter factor derived, not numerological
7. The separating predictions (10 zero-parameter tests, DR4 Dec 2)
8. No direct-detection signal predicted (no WIMP, the dark sector is not a particle)

## HONEST EDGES (stated, not hidden)

- n=2 is exhaustively empirical (four search routes closed, G009/G019)
- The growth sector carries a ~3 sigma tension with direct lensing (G020/G022)
- The local dark density under-supplies ~1.6x (G003, the honest falsifier)
- The EFE test remains untestable at current survey depth (G044, L245)
- The temperature's dynamical origin is honest-postulated (PAPER29, not hidden)
- Horn A's fixed congruence violates local Lorentz invariance at the scalar level
  (the honest cost of the PPN-clean completion)

## THE DECIDING INSTRUMENTS (all registered with dates)

| Test | Instrument | Date | Odds |
|---|---|---|---|
| Wide-binary gamma_v profile | Gaia DR4 | Dec 2, 2026 | 2-3 sigma |
| Local dark-density break at 6.1/140.6 pc | Gaia DR4 | Dec 2026 | TBD |
| BTFR zero-point at z~2.5 | JWST/ALMA | TBD | 20:1 |
| Growth raise in BGS bin | DESI final | ~2027 | 2.7 sigma |

## THE LIVE SITE

https://abeautifullygeometricuniverse.web.app/simulate
— 9 simulations with real SPARC/KiDS/DESI/MSA-3D data, the Evolution Race, the
RAR Explorer, the BTFR Lab, The Fluid, the z-slider discriminator.

---

## 2026-09-19 — PD01: the channel-count derivation of κ = ½ (conditional)

The theory's ONE empirical premise — n = 2 (G089 A5; rung 9: "EMPIRICAL, all
derivation routes closed") — now carries a derivation under stated premises
(`PD01_polarization_count.py`, 17/17 PASS, `.out` + `_results.json`):

1. **The slope is the channel count, completion-independently.** The corpus
   normalisation μ(∞) = 1 forces the OR structure over channel-shares (the
   SUM saturates at n, not 1); in the OR class the deep-MOND slope is the
   number of equal independent channels for EVERY per-channel completion
   (verified at n = 1, 2, 3 for three completions). So κ = 1/(count) never
   waits on the unknown shape.
2. **The count is inherited from the carrier, and it is computed.** The
   static response of the linearised metric presents exactly TWO Poisson
   channels — G⁽¹⁾₀₀ = 2∇²Ψ (the 00 sector) and G⁽¹⁾ₖₖ = 2∇²(Φ−Ψ) (the
   spatial-trace sector), verified symbolically for generic radial
   potentials and by finite differences to 2e-14 — while a scalar presents
   one and a static vector one. κ is therefore BINARY: {½, 1}. This is the
   corpus's own L237 candidate reading ("the graviton's two polarisations")
   landed in its static form — G007's two levers — where it is computable.
3. **The data select the metric's count.** κ = 1 sits 7.0σ (BTFR) and
   10.4σ (distance-free) out; κ = ½ sits at 0.46σ and 1.19σ; the SPARC
   selection is n = 2 on both density conventions (L232, committed). Hence
   n = 2 = the metric's channel count and κ = ½.

**Falls with it:** the 2π horizon form (k03's "one principle-shaped
coefficient not excluded", 0.461) dies STRUCTURALLY — under κ = 1/n it needs
a count of √(3π/2) = 2.17, which does not exist; G009's mechanism kill
stands untouched (nothing stochastic is claimed; predicted shot noise zero);
the L231 kernel tension (n=1 fits the framework kernel 1.44× better in rms)
resolves as a completion preference, not a count signal.

**Registered falsifier (row 21, FALSIFIER_MATRIX):** κ is two-valued — any
measured κ strictly inside (0.5, 1) at any epoch or footing kills the
channel-count structure.

**Status, honestly:** a CONDITIONAL derivation. One premise (the
OR-identification of the response) is supported three ways — the corpus's own
normalisation, L237's exact identification of the data-selected family, and
the data's dichotomy landing (C1) — but not derived from a mechanism. The
full shape (the completion) stays empirical, exactly as rung 2 already treats
it. G089 A5 and G152's inventory row should be re-graded at the next wave.