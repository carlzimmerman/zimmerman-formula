# SC1_self_coupled_core_law — FROZEN CRITERIA (committed alone, before any script or graded number)

Written 2026-10-25 at the owner's request: "Grade the self-coupled core law next: frozen criteria first, fix q at a candidate
(1/3), check SPARC with Sigma varying as sigma^q, then X30's cluster cells." κ = ½ FITTED. Footings canonical / alt,
scored separately, never pooled. Cold dark energy (w ≈ 0, clumping, a gravitating field component; not matter, never a
particle). Nothing here says the data favour the framework or ΛCDM. Not "theory closed".

## 0. Hypothesis SC

LN1's T7 (Lean, 667db25771) derives, from an isothermal core plus a self-interaction rate × age = 1 with σ/m ∝ v^(−n), the
core law Σ₀ ∝ σ^q t^(−1/2), q = (1+n)/2. T8 gives a certified window. `window_eval` puts q = 1/3 (n = −1/3) at the top of
the open range for a cluster requirement of about 3×.

**SC (primary):** X38's route-E Burkert halos, unchanged except for the core surface density, which becomes per-system:

  Σ_i = Σ_a0 · (σ_i / σ_ref)^(1/3),  Σ_a0 = a₀/(2πG),  σ_ref = median σ over the SPARC galaxies used.

- The anchor σ_ref keeps the median SPARC galaxy at X38's Σ_a0. It is the coupling normalisation K, fixed by a₀ at galaxy
  scale, not fitted to any residual.
- q = 1/3 is fixed. There is no q scan.
- No age term in the primary.

**Dispersions (X19's V2 convention, fixed now):**
- SPARC: σ = V_obs(last point)/√2.
- Clusters with a KT: σ = √(kT/(0.6 m_p)) (X30's `SIG_KT` formula).
- Clusters without a KT: the median σ_KT of their MGAS500 tercile (`T3M`), the same fill rule X39 used for BCGs.

## 1. Grading (unchanged machinery)

- **SPARC:** X38's `sparc()` with Σ replaced per galaxy. EM1 backgrounds A and B, EM1's `line` (rms ≤ 0.110 and
  0.50 ≤ median Υ ≤ 0.80).
- **Clusters:** X38's 15 cells (`grade_clusters` logic): MID T1–T3 and slope, OUTER all / T1–T3 / slope, OUTER M-all /
  M1–M3, INNER all and M-all. Both h (0.672, 0.686); a cell passes if |Z| ≤ 2 at both.

| class (per footing; the lane verdict needs both footings to agree, else UNDECIDED) | rule |
|---|---|
| SC PASSES | the SPARC line passes for both backgrounds and every cluster cell passes |
| SC PASSES SPARC, IMPROVES CLUSTERS | SPARC passes; no cell that passes in X38 fails; summed |Z| of X38's failing cells falls by ≥ 50% |
| SC PASSES SPARC ONLY | SPARC passes, otherwise |
| SC FAILS SPARC | the SPARC line fails for either background |

Reported only (never graded, never used to pick q):
- age variant: cluster Σ × (0.5)^(−1/2), clusters about half the galaxies' age;
- brackets q = 1/4 and q = 1/2;
- σ_ref, the per-tercile median Σ/Σ_a0, and each cell's change from X38.

## 2. Checks

- **K0** q = 0 reproduces X38: SPARC rms and median Υ for both backgrounds (to 1e-9) and every cluster cell prediction
  (to 1e-6), both footings.
- **K1** The median σ_KT over the KT clusters equals 517.1 km/s ± 0.5 (DH1/X26's number).
- **K2** Peak RSS < 2 GB, one thread.
- **MUTATE=1** (separate outputs): every system gets σ = σ_ref, so Σ = Σ_a0 everywhere. The predictions must reproduce X38
  exactly. MUTATE exits 1 if they do, 0 if not.

## 3. Disclosed before freezing

- **Hand estimate.** With σ_ref ≈ 100 km/s and σ_KT ≈ 400–900, clusters get Σ ≈ 1.6–2.1 Σ_a0 (2.3–3.0 with the age
  variant). X40b (C) said 3–5× is needed, so SC is expected to improve the cluster cells but may not pass them.
- **SPARC risk.** SPARC σ spans about 20–200 km/s, so Σ varies by ×0.6–1.3 around Σ_a0. Whether X38's line survives that
  is the test.
- **Dwarfs.** CD1's cap would move with Σ: at σ ≈ 10 km/s, Σ ≈ 0.46 Σ_a0. The dwarfs' median need was S ≈ 0.5 of the
  Σ_a0 cap, so this is a known tension. It is graded in a later lane, not here (stated now).
- **Physics.** n = −1/3 is a cross-section that rises weakly with velocity, which is unusual among published
  self-interacting models.
