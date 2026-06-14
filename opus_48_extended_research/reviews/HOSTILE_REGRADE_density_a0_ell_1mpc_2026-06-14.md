# HOSTILE REGRADE — density-a0 at ell = 1/μ = 1 Mpc (AeST scalar Compton wavelength)

*Independent recheck of the `ell_aest_compton` claim. I reran the original test, then rebuilt both legs from
the raw rotmod files + raw eRASS1 FITS with my own loaders and scatter metric, and stressed the model
assumptions (halo-retention sweep, mean-offset-vs-spread decomposition, M(<r) extrapolation model, ell scan).
Script: `HOSTILE_density_a0_ell_recheck.py`. Quarantine: a0/Z never asserted derived. Honest both ways.*

## REGRADE: BREAKS-GALAXY-RAR — confirmed (the original `ell_aest_compton` grade STANDS)

The original grade of "BREAKS-GALAXY-RAR **and** OVER-CLOSES-CLUSTERS" reproduces exactly and survives every
robustness probe I threw at it. Forced to pick one schema label, the make-or-break leg is the galaxy RAR, so
the regrade is **BREAKS-GALAXY-RAR** — but the cluster over-closure (eta~0.47, not a deficit) is equally real
and I report it at full weight.

## The numbers I trust (recomputed independently, real 175 SPARC + real 9,830 eRASS1)

| quantity | value | notes |
|---|---|---|
| baseline RAR scatter (universal 9.36e-11, dS-Unruh ν, Υ=0.70) | **0.1448 dex** | free-optimal 0.1440 @ a0=1.03e-10 |
| **density-a0 @ ell=1 Mpc RAR scatter (raw, the literal claim)** | **0.194 dex (+0.0495, +34%)** | **BREAKS** — well past the ~0.13 target |
| cluster η(R500) median @ ell=1 Mpc | **0.47** (a0 boost ~27×) | **OVER-CLOSES**; 96% have η<1, 1% in [1.2,1.5] |
| cluster η, mean-enclosed-within-R500 | 0.42 (boost ~33×) | over-closes harder |

Both legs reproduce to the third decimal against the original script.

## Is ell genuinely DERIVED or smuggled-tuned? — GENUINELY DERIVED (credited), with one honest caveat

I verified the literature claim independently. In AeST the scalar mass μ obeys **μ⁻¹ ≳ 1 Mpc** (Skordis–Złošnik
2021 require m²/f_G ≲ 1 Mpc⁻²) so that MOND solutions survive at galactic scales — this is framework-native,
fixed by CMB/galaxy-MOND consistency *before* this test, NOT chosen to land clusters at 1.2–1.5. So ell = 1/μ
≈ 1 Mpc is a real derived scale, and that is exactly what makes the failure load-bearing: it is the framework's
OWN scale that fails, not "no scale found." **Credited.**

The one honest caveat (does NOT rescue it): the literature gives a *lower bound* (≳ 1 Mpc), not a sharp pin.
1 Mpc is the smallest framework-allowed ell. Pushing into the allowed range (ell = 2–3 Mpc) softens both
failures but threads neither — the cluster is still over-closed (η = 0.66 at 2 Mpc, 0.80 at 3 Mpc) and the
galaxy RAR is only rescued near ell ≳ 3–5 Mpc. The scale that actually threads clusters (η→1.2–1.5) is **8–12
Mpc**, ~10× the 1 Mpc bound — the supercluster/turnaround scale, NOT the AeST Compton wavelength. Adopting it
is tuning. So the verdict is robust across the framework-allowed end of the range and only "passes" at a scale
the framework cannot justify.

## Does the cluster boost OVER-close? — YES, robustly (not a deficit, an over-shoot)

η(R500) = 0.47 means the cluster predicts ~2× too MUCH gravity. I confirmed this is **not** an artifact of the
M(<r) extrapolation: across M~r (isothermal), M~r⁰ (all mass within R500), and M~r^1.5, η lands 0.45–0.50 with
93–97% over-closed. The mechanism is structural: eRASS1 median R500 = 0.77 Mpc is *comparable to* ell = 1 Mpc,
so the 1 Mpc ball is dominated by the dense core (~700–730 ρ_crit) and never dilutes to ambient. The deep-dive
*hoped* for a ~15× boost to η~1.35; the literal 1 Mpc ball gives ~27× → η~0.47. It over-shoots.

## The make-or-break galaxy leg — the honest decomposition (both ways)

The raw +34% is the physically correct number for the framework's literal claim (a0 IS (c/2)√(Gρ_smoothed),
no refit allowed). I also decomposed it. Letting a single global rescale of the per-galaxy a0 float — so I
penalise ONLY the environmental *spread*, not the mean offset — the inflation shrinks but does NOT vanish:
+0.0173 dex above the free-optimal baseline at Υ=0.70, f=0.03 (≈ 0.161 dex). So part of the raw +34% is a
mean-offset (the per-galaxy median a0 = 2.3e-10 sits well above the RAR-optimal ~1.0e-10), and part is genuine
spread. **Either way it inflates past ~0.13 dex.** The inflation is robust:

- halo retention f=Mb/Mh: +0.033 (f=0.05) / +0.049 (f=0.03) / +0.074 (f=0.017) dex, Υ=0.70 (reproduced).
- McGaugh ν: +0.076 dex (reproduced).
- Υ=0.50 footing: smaller raw inflation (+0.012 to +0.002 across f) because the Υ=0.50 baseline is already
  loose (0.171 dex) — but the spread-only penalty persists; it never tightens. The reading goes the WRONG way
  on SPARC: the framework's own a0_env > a0_field prediction inflates the RAR, it does not tighten it.

Mechanism: a 1 Mpc ball registers each galaxy's own halo (dwarf ~1.3×, L* ~1.5–2×, group ~5.4× cosmic a0), so
a0 becomes host-halo-mass-dependent → the RAR ridge smears.

## The structural trap (independently confirmed) — no single ell threads

| ell [Mpc] | galaxy RAR Δ vs 9.36 | cluster η(R500) | %in[1.2,1.5] |
|---|---|---|---|
| **1 (AeST 1/μ)** | **+0.0495 (BREAKS)** | **0.47 (OVER-CLOSES)** | 1% |
| 2 | +0.006 | 0.66 | 5% |
| 3 | +0.001 | 0.80 | 6% |
| 5 | +0.0002 | 1.03 | 13% |
| 8 | +0.0001 | 1.27 | 39% |
| 10 | +0.0001 | 1.39 | 55% |

The ell small enough to over-close clusters (R500-comparable) is the ell small enough to register galaxy halos
and break the RAR. The ell large enough to dilute clusters into the band (~10 Mpc) washes galaxy halos into the
cosmic mean (RAR preserved, +0.0001 dex) — but it is ~10× the derived scale and is tuning. **The framework's
own derived ell = 1 Mpc sits in the worst spot: small enough to break galaxies, small enough to over-close
clusters.**

## a0↔Λ cost — real (confirmed)

It IS a cosmic superset: ρ_total,smoothed → ρ_crit gives a0 = 1.13e-10 ~ cH₀ (still Milgrom's coincidence, the
ρ_total footing). BUT it trades the clean a0 = c²√(Λ/32π) = 9.36e-11 for a0 ↔ local density. The exact Λ-value
re-emerges only in the empty/de-Sitter limit ρ_smoothed = ρ_DE — a limit no bound system occupies. Every galaxy
and cluster reads a different, environment-set a0. That is precisely what the 0.13-dex-tight, a0-universal SPARC
RAR resists. Cost stated, not hidden.

## NET FOR CARL

The density-law a0 with the framework's OWN derived smoothing scale (the AeST Compton wavelength ell = 1/μ ≈ 1
Mpc) **does not thread the double constraint** — and I confirmed this independently, on real data, robust to the
halo model, the M/L, the interpolation function, and the mass-extrapolation model. At ell = 1 Mpc it inflates
the SPARC RAR +34% (0.145→0.194 dex) *and* over-closes eRASS1 clusters to η~0.47 (predicting ~2× too much
gravity). The scale that would thread clusters (~8–12 Mpc) saves galaxies only by washing their halos out
entirely, and it is ~10× the derived scale — tuning, the supercluster scale, not the Compton wavelength.

**Credited honestly:** ell IS genuinely derived (not invented for this test); the cosmic superset DOES hold
(→ ~cH₀); the a0_env > a0_field reading IS a real falsifiable prediction. It fails on the merits, not by a
hostile convention — and the prediction goes the wrong way on SPARC (it smears the RAR). This converges with
the AeST mass-term gauntlet from the *field* side (which left clusters at η~1): both CMB-pinned-scale routes
miss the eRASS1 ~2× — the field route under-shoots (η~1), the density route over-shoots (η~0.47). **The density-a0
cluster escape, at the framework's derived scale, is closed on real data.** It survives only as a *tuned* ~10
Mpc reading, which is not derivation. The cluster deficit (η~1.6–2.0 at R500) remains MOND's inherited unsolved
problem; the one framework-distinctive out (the density law) does not deliver it at any scale the framework can
justify.

*Sources: Skordis–Złošnik 2021 PRL 127 161302 (2007.00082); Verwayen–Skordis–Zlosnik 2024 MNRAS 531 272
(2304.05134); Lelli+2016 SPARC; Bulbul+2024 eRASS1 (A&A 685 A106). Companions: DENSITY_A0_ELL_1MPC_VERDICT,
AEST_SINGLE_MU_GAUNTLET, DENSITY_A0_RDE_CROSSOVER, CLUSTER_DEEPDIVE_VERDICT (all 2026-06-14).*
