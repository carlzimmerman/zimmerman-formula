# DW1_dwarf_core_flattening — RESULT: no stated mechanism flattens the core law below ~20 km/s (M1, M2 ruled out; M3 FAILS)

Frozen criteria 279b4aa47c (committed alone). Amendment A1 (`AMENDMENT_A1.md`): reporting code only, no graded line
changed; the canonical graded numbers are identical to the first run. κ = ½ FITTED; footings never pooled; cold dark
energy, not matter; nothing here says the data favour the framework or ΛCDM; not "theory closed".

**Question (owner).** Can OS1's core law Σ = Σ_a0 (σ/σ_ref)^q_f (q_f = 0.892 / 0.748, calibrated on SPARC, passing 14/15
cluster cells) flatten below ~20 km/s for a stated physical reason, rescuing the dwarfs without touching SPARC or clusters?

## Result (`dw1_dwarf_flattening.out`)

| mechanism | test | canonical | alt |
|---|---|---|---|
| **M1** rate saturation (short mean free path) | needs Knudsen number Kn < 1 at dwarf σ | Kn = 1158 (5 km/s) … 653 (1000 km/s) | Kn = 2048 … 539 | → **RULED OUT**: Kn ≫ 1 everywhere |
| **M2** gravothermal collapse | the core law sets Γt = 1 at every core | system-independent | same | → **RULED OUT** within this law (structural) |
| **M3** σ = the halo's own V_max/√2 (self-consistent) | fraction z ≥ 2, median S | 0.640, 5.14 | 0.404, 2.29 | → **M3 FAILS** on both footings |

Checks 5/5:
- K0: the stellar-σ rule reproduces OS1 exactly.
- K1: m₁ = max Bk/x = 0.8606192.
- K2: the σ_h solve is self-consistent.

MUTATE (σ_h = σ_ref, so Σ = Σ_a0) reproduces CD1 exactly (0.011; 0.532 / 0.439), exit 1.

**Why M3 fails.** Using the halo's own dispersion raises the dwarfs' σ only about 2× (median σ_h 14 / 12 km/s against
σ★ ≈ 7). The cores still sit at Σ ≈ (14/70.5)^0.89 ≈ 0.24 Σ_a0. The ultra-faints are worst (median S ≈ 10 / 4), then
the MW classicals (7 / 3.5). Only the four large, diffuse systems pass easily (Antlia II, Crater II, Sagittarius,
S ≤ 0.4). They are the ones the law itself over-predicts.

**Where M1 lands, a closed form worth keeping.** The Knudsen number at the anchor is
Kn_ref = (4/(3√π)) · (2 a₀ t) / σ_ref. Here 2a₀t ≈ 0.27 c (canonical): the coupling fixed by a₀ at galaxy scale is
weak enough that scattering is long-mean-free-path in every system from dwarfs to clusters. So a self-coupled cold sector
anchored this way can never reach the fluid regime.

## What it means

The dwarfs and the galaxy–cluster law are now cleanly separated:
- **One law, one SPARC-fixed constant:** Σ ∝ σ^0.75–0.89 links galaxies and clusters (OS1).
- **Below σ ≈ 20 km/s:** dwarfs need 2–10× more central pull than that law allows. Neither saturation (M1), collapse
  (M2), nor a consistent halo σ (M3) supplies it.

The dwarf excess needs physics that acts only at small scales, which is where the record has always placed it (X24's
~4 km/s floor, X28's r^−0.8, DF1's Γ ≈ 0.88). A new core condition, e.g. one that also lets cores collapse, would be a
different law and needs its own lane.
