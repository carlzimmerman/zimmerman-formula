# BU1_bullet_cross_section — RESULT: PASSES BOUNDS (both footings), C1 PASS; dwarfs SANE

Frozen criteria bcdb19e9e7 (committed alone; no amendment). κ = ½ FITTED. Footings computed and graded separately, never
pooled. Cold dark energy, not matter; s is its self-coupling rate per unit mass density. Nothing here says the data
favour the framework or ΛCDM. Not "theory closed". Analytic, one thread; nothing downloaded.

**Question.** OS1's core law fixes the cold dark energy's self-interaction with no free number left. Is the implied
cross-section per mass s(v) compatible with merging-cluster bounds, and is it sane at dwarf speeds?

**Derivation.**
- n = 2q_f − 1 = 0.784 (canonical) / 0.496 (alt), from LN2.
- s·v = K σ^(1−n), with K = 9σ_ref^(1+n)/(4πG t Σ_a0²) (LN1 T7 at the SC1 anchor) and v = (4/√π)σ.
- So s(v) = K (√π/4)^(1−n) v^(−n).
- At the anchor (v_ref = 159 km/s), s = 0.155 / 0.106 cm²/g.

## Result (`bu1_cross_section.out`)

| s in cm²/g at v (km/s) | 10 | 50 | 200 | 1000 | 1900 | 3000 | 4700 |
|---|---|---|---|---|---|---|---|
| canonical (n = 0.784) | 1.35 | 0.383 | 0.129 | 0.0366 | 0.0221 | 0.0155 | 0.0109 |
| alt (n = 0.496) | 0.417 | 0.188 | 0.094 | 0.0425 | 0.0309 | 0.0246 | 0.0197 |

| bound (eval speed) | status of the bound value | canonical margin | alt margin |
|---|---|---|---|
| B1 Bullet, Randall+2008, < 1.25 (3000) | **PROVISIONAL** (from memory; not in REFERENCES.bib) | ×81 below | ×51 below |
| B2 Harvey+2015, < 0.47 (1000) | record (CFG1 A09d, contested) | ×13 | ×11 |
| B3 record's CFG725 merger model, ≤ 0.708 (3000) | record (its inputs PROVISIONAL) | ×46 | ×29 |
| C1 Sagunski+2021 cluster cores, < 0.35 (1900) | record, WebFetch ⇒ PROVISIONAL | ×16 → **C1 PASS** | ×11 → **C1 PASS** |
| C2 Andrade+2022, ≲ 0.13 (1900) | memory, PROVISIONAL, reported only | ×5.9 | ×4.2 |
| C3 Peter+2013 halo shapes, ≲ 1 (1900) | memory, PROVISIONAL, reported only | ×45 | ×32 |

**Lane class: PASSES BOUNDS on both footings (C1 PASS).**

Checks 3/3:
- K0: n = 0.784 / 0.496, as in LN2.
- K1: the Knudsen number rebuilt from s reproduces LN2's closed form (870.0 / 1051.4) and DW1's Kn at 5 and 1000 km/s
  exactly.
- K2: ρ₀ s v t = 1 at σ_ref.

**MUTATE** (n → −n, s rising with v; `_MUTATE` outputs):
- canonical moves to **EXCLUDED** (s(3000) = 1.54 > 1.25; C1 FAIL);
- alt stays PASSES BOUNDS but fails C1 (0.36 > 0.35);
- verdict UNDECIDED, exit 1.

So the pass is driven by the derived falling exponent. The anchor value alone does not give it.

## Dwarfs and gravothermal collapse

- At dwarf speeds, s(10 km/s) = 1.35 / 0.42 cm²/g and s(50) = 0.38 / 0.19 cm²/g. This is an ordinary size for
  self-coupled halo models, far below the ~100 cm²/g scale (PROVISIONAL) where dwarf-halo collapse becomes generic.
  **SANE** on both footings.
- **Collapse time.** Use the collapse-time form t_c ≈ (150/C)/(s ρ_s r_s √(4πGρ_s)), C = 0.75 (PROVISIONAL), with the
  core standing in for the scale radius. Combined with the core law, this gives a closed form:
  **t_c / t = (150/C) · v/(3σ) = 150.5 for every system**, independent of σ, K and n. No halo of any mass is
  gravothermally collapsed within a Hubble time.
- **How this interacts with DW1's Γt = 1.** Γt = 1 is the core-*formation* condition, and the law imposes it. It fixes
  ρ₀ for a given s, so it cannot by itself tell whether a halo has collapsed. The t_c/t ratio is the separate statement.
  It shows that the premise "cores are cored, not collapsed" is self-consistent with a margin of ~150.

  But it inherits the construction: since every core has exactly one scattering per Hubble time, collapse is ruled out
  structurally at every scale. The same applies to DW1 M2. So collapse cannot be what deepens the dwarfs.

  In the MUTATE run n is decoupled from q, so Γt ≠ 1 away from σ_ref. t_c/t then varies (2.4–9500) but stays > 1.

## What it means

- The self-coupling that OS1 fixed on SPARC falls as v^(−0.5 to −0.8). It is about 0.1–0.15 cm²/g at galaxy speeds and
  0.01–0.03 cm²/g at merger speeds.
- That is one to two orders of magnitude under every merging-cluster bound in the record and in memory, including
  cluster-core limits. **The Bullet Cluster is not a threat to this law's self-interaction.**
- The weak coupling is consistent with DW1's Kn ≫ 1: the mean free path is λ = v t, the distance travelled in a Hubble
  time.
- Read against the dwarf failure (OS1, DW1): s at 50 km/s is 0.19–0.38 cm²/g, about 5–10× below the Kaplinghat+2016
  core fit (~2 cm²/g, PROVISIONAL, comparison only). The law's dwarf cores come out too shallow, and collapse cannot
  rescue them. The dwarf blank stays where the record has it.

**Caveats (ledger L4–L9).**
- The power law is extrapolated from SPARC's σ range to 4700 km/s.
- The constant-s bounds are applied at one speed each, with no momentum-transfer weighting.
- The cold dark energy is assumed to be the whole merging halo.
- Several bound values are PROVISIONAL (memory or WebFetch). B1 (Randall+2008) is not in `citations/REFERENCES.bib`.
  The margins (≥ ×11) are large compared with these uncertainties.

Run: `python3 bu1_cross_section.py` (exit 0); `MUTATE=1 python3 bu1_cross_section.py` (exit 1, as frozen).
