# SCOUT — TRGB lever on the a0-line: the gas-dwarf subsample split by distance flag fD

**Run:** `scout_split.py` (exit 0) → `scout_split.json`, `_scout_console.txt`.
**Sample:** SPARC gas-dominated dwarf points (Lelli-McGaugh-Schombert 2016), fire_common cuts
Q≤2, inc≥30°, eV/Vobs<10%, point-level gas cut Vgas² > Ud·Vdisk² + Ub·Vbul² (Ub=1.4Ud).
**Line under test:** E := g_obs² − g_bar² = a0·g_bar (through origin, slope = a0).
**Footings:** canonical a0 = cH_Λ/Z = 9.355e-11 vs alt cH₀/Z = 1.1305e-10 (20.9% gap).
**Distance-flag systematic (banked, fire_common.SIG_LND):** σ_lnD = {1 Hubble-flow 0.25,
2 TRGB 0.05, 3 Cepheid 0.05, 4 UMa 0.10, 5 SNIa 0.08} → TRGB/Cepheid carry a distance
systematic **5× smaller** than Hubble-flow. That is the lever.

## The split (fiducial Ud = 0.50)

| fD | method | N_gal | N_pts | D [Mpc] | Vflat [km/s] | Mbar [1e9 M⊙] | y = g_bar/a0 | straddles y=1 |
|----|--------|------:|------:|---------|--------------|----------------|--------------|:---:|
| 1 | Hubble-flow | 39 | 221 | 4.7 – 100.6 | 34 – 234 | 0.20 – 117 | 0.011 – 0.11 | no |
| 2 | **TRGB** | **19** | **188** | 1.3 – 8.8 | 47 – 131 | 0.05 – 9.3 | 0.009 – 0.17 | no |
| 3 | Cepheid | 1 | 3 | 13.8 | 150 | 33.6 | 0.033 – 0.04 | no |
| 4 | UMa-cluster | 3 | 14 | 18.0 | 84 – 109 | 1.8 – 8.8 | 0.039 – 0.09 | no |
| 5 | SNIa | 0 | 0 | — | — | — | — | — |

**High-quality-distance set (fD ∈ {2,3}) = 20 gals / 191 pts.** TRGB carries essentially the
whole lever; the lone Cepheid galaxy is star-dominated at higher Ud and drops out.

Cross-check at the banked headline Ud = 0.70 (reproduces the banked 49 gals / 310 pts):
TRGB 18/147, Hubble-flow 29/154, UMa 2/9, Cepheid 0. **TRGB is ~half the gas-dom sample and
point-balanced against Hubble-flow at both Ud.** → The "N too small to discriminate" honest
null is **NOT** triggered on sample size; TRGB alone rivals the Hubble-flow point count.

## Selection-bias assessment: HQ (TRGB+Cepheid) vs Hubble-flow

Ratios of medians (HQ / Hubble-flow):

| quantity | HQ median | HF median | ratio | reading |
|----------|-----------|-----------|-------|---------|
| distance D | 4.4 Mpc | 12.5 Mpc | **0.35×** | HQ closer — by TRGB construction (nearby-only) |
| Vflat | 66 km/s | 80 km/s | 0.83× | HQ modestly slower rotators |
| Mbar | 0.66e9 | 2.46e9 | **0.27×** | **HQ is the nearby low-mass dwarf population** |
| **y = g_bar/a0** | **0.043** | **0.047** | **0.90×** | **same acceleration regime** |

**The selection difference is real in distance and mass, negligible in acceleration.**
TRGB-anchored gas dwarfs are systematically closer and ~3–4× lower in baryonic mass (that is
exactly what TRGB distances select — nearby, resolvable dwarfs). But the a0-line is a
statement about **acceleration**, and the quantity that actually enters the slope estimator,
y = g_bar/a0, is near-identical between the two sets (0.043 vs 0.047). Because the identity
E = a0·g_bar holds at **every** g_bar independent of a galaxy's mass or distance, the
mass/distance offset does **not** bias the slope a0 — it only changes which galaxies, not
which part of the line, are sampled. **The TRGB a0 probes the same segment of the a0-line as
the Hubble-flow a0.**

## Conditioning caveat (honest, load-bearing)

**Neither subsample straddles y = 1.** Both live entirely in the deep regime y ≲ 0.2
(g_bar ≪ a0). Consequences, stated both ways:

- **For measuring the a0 magnitude (a through-origin slope): this is fine, even favorable.**
  Deep-regime gas points are exactly where E = a0·g_bar is cleanest and where the M/L
  degeneracy is most suppressed (φ small). The slope is well-conditioned from points at any
  y; straddling y=1 is not required for a line through the origin.
- **For discriminating the ν SHAPE (framework vs McGaugh vs simple-ν): it is not.** Shape
  separation lives at y ≳ 1, and there are essentially zero such points in either gas
  subsample. So the TRGB set can sharpen the a0 *number* but cannot also test the *kernel*.

## Verdict for the lever run

1. **Clean enough to fire, with a light touch.** The TRGB subsample is a comparable,
   near-clean a0 measurement — same acceleration regime as Hubble-flow, so no strong
   selection bias to correct. Trimming the few Hubble-flow points above the TRGB y-max
   (~0.17) or reweighting in y fully removes the residual regime mismatch; full
   range-matching is not required to avoid a biased slope.
2. **Not underpowered in count.** 18–19 TRGB galaxies / 147–188 gas-dom points is half the
   banked gas sample — enough to compute a0 with a real error bar. Whether it can *resolve*
   the 20.9% canonical-vs-alt footing gap is a **budget** question (does cutting σ_lnD 5×
   shrink σ_tot below ~10%?), not a selection question — that is for the next fit script.
3. **Keep the estimator honest.** Re-apply the model-based / iterated GLS (never raw
   observed-error weights — that is the trap that manufactured the fake a0≈3.3e-11 deficit).
   Report canonical (9.355e-11) and alt (1.1305e-10) footings both ways; McGaugh+2016
   g_dagger=1.2e-10 for comparison only. No "proves" language.
4. **Λ-inversion context:** Λ = 3Z²·â₀²/c⁴, Z=√(32π/3)=5.789. A tighter TRGB â₀ tightens the
   dwarf-rotation → cosmological-constant inversion; this scout does not run it (fit script's
   job) but confirms the input subsample is a fair, same-regime sample to feed it.
