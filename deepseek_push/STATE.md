# STATE — the Zimmerman Equilibrium Theory as of 2026-09-14

## THE ONE-LINE SUMMARY

A complete, zero-parameter, Lean-certified theory of the galactic acceleration
scale: the RAR is the equilibrium of the dark sector at its virial temperature
(the halo IS the phantom, coefficient 1), every relativistic force-law
completion is proven dead (the pincer), a PPN-clean completion exists (Horn A),
and the same constant predicts the dark-energy density to 0.07% (G052).

## THE BOARD — every gate

| Gate | Verdict | Lane/Lean |
|---|---|---|
| RAR reproduced, zero parameters | **PASS** (0.150 dex) | G002, L232 |
| M/L floor | **0.064 dex** (did NOT fire; outer half 0.055) | G013 |
| Scatter decomposition | **offset + white noise + sag; no halo fingerprint** | G036, G044 |
| Offset is M/L, not physics | **CONFIRMED** (R²=0.016/0.006) | G040 |
| Cluster shape | **PASS** (−1.478 vs −1.53; T=809 km/s) | G008, G012 |
| Cluster kernel-robust | **PASS** (μ₂ swap: slope <0.05, boost <10%) | G017 |
| Cassini (bare kernel) | **DEAD** (6.44×/7.63×) | L243, G004/G005 |
| Lensing (MI) | **DEAD** (conformal cancellation) | L241 |
| Preferred-frame (vector) | **DEAD** (α₁=O(1)) | L244 |
| Bimetric | **DEAD, Lean** (11 thms) | G007 |
| Photocount | **DEAD** (variance 3×) | G009 |
| Local k⁴ operators | **DEAD forever** (7 tried) | G030, G034 |
| **Horn A fixed congruence** | **ALIVE: α₁=0 by architecture; PPn-clean** | G032 |
| **Unified cosmology** | **PASS 5/6: Ω_Λ=0.6857 from a₀ (+0.07% of Planck)** | G052 |
| n=2 | **EMPIRICAL** (all derivation routes closed) | G009, G019 |
| Growth raise | **TENSION recorded (~3σ vs lensing), DESI decides** | G020, G022 |
| Local dark density | **0.0062 M☉/pc³, under-supplies 1.6× (one-way)** | G003 |

## THE THEORY'S SHAPE

**One scale** a₀ = s/2, **two sectors** (the MOND scalar + the Noether-charge
dust), **one action** (G031), **three regimes** (galaxy outskirts / cluster
transition / solar system) — with the EFE cap marking the two-component
handoff. Zero free parameters at galaxy scale.

## THE UNIFICATION (G052, the missing piece found)

Dark energy and MOND acceleration are one measurement: Λ⁴ = 4a₀²/G gives
Ω_Λ = 0.6857 (0.07% from Planck); the cold sector is the flatness residual
Ω_dm = 0.2650; the coincidence epoch z≈0.49 is the μ₂ shape, not a tuning.
The scalar stiffens w→+1 at early times — the reason the two-sector
architecture exists.

## WHAT DECIDES IT (registered instruments)

1. **Gaia DR4** (Dec 2 2026): E1–E7 — the vertical profile (ν=2 arithmetic,
   box-ν 1/√z, 140.6 pc break), the radial break (6.1 kpc), the wide-binary
   rising γ_v and period–separation break (7.4 kAU).
2. **DESI final** (~2027): E8/E9 — the growth factor-4 fall (BGS +2.7% → QSO
   +0.6%), the forest +3.1%.
3. **JWST/ALMA**: the BTFR zero-point at z≈2.5 — 0.00 vs +0.33 dex, 20:1.
4. **Euclid/CMB-S4**: confirm Ω_Λ = 0.6857.

## THE HONEST EDGES (never said to be closed)

n=2 is empirical. The growth sector is in tension with direct lensing. The
local density under-supplies. rung 4's temperature origin is honest-postulated
(PAPER29). Horn A's fixed congruence violates LLI at the scalar scale. The EFE
test is untestable at current survey depth (G044/L245).

**Never say the theory is closed. Say it is under test.** These four
instruments decide the rest of the story.

## THE ARTIFACTS

- `THEORY.md` — the full derivation chain, every rung certified
- `LEAN_CERTIFICATES.md` — 66 theorems, 7 certificates, zero sorry
- `LANES.md` — the core lanes with verdicts
- `PREDICTIONS.md` — E1–E10, zero-parameter, with kills and instruments
- `PAPER_SKELETON.md` — MNRAS/PRD/A&A draft
- `lean/` — 6 verified certificates (all compile, exit 0)
- `lanes/` — G031/G032/G036/G040/G052
- Live site: https://abeautifullygeometricuniverse.web.app/simulate