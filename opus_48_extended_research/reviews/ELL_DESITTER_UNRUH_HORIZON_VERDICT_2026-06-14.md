# Deriving ell from de Sitter-Unruh horizon physics, and testing the density-law a0 on SPARC + eRASS1 — VERDICT (2026-06-14)

**Grade: LEAVES-CLUSTER-DEFICIT (the derived ell is COSMOLOGICAL, Gpc, not the few-Mpc the cluster boost needs).**
Code: `ell_desitter_unruh_horizon.py` · Data: real 175 SPARC `*_rotmod.dat` (Lelli+2016) + real eRASS1 `erass1cl_primary_v3.2.fits` (Bulbul+2024, N=9830 clean, WL-calibrated).

## The task
The deep-dive (`CLUSTER_DEEPDIVE_VERDICT_2026-06-14.md`) found the one distinctive framework escape from the cluster
deficit is the density law `a0 = (c/2)√(G ρ_total,smoothed-over-ell)` — but it rides on an UNDERIVED smoothing scale
ell. Derive ell from first principles (the de Sitter-Unruh modified-inertia physics), then test whether ONE ell threads
**both** the galaxy RAR (must stay ~0.13 dex) and the cluster eta (must fall to ~1.2-1.5, not over-close eta<1).

## The derivation of ell (framework-native, not tuned)
The dS-Unruh inertia: `T_eff = (ħ/2πckB)√(a²+(cH_local)²)`. The "cH_local" is the LOCAL de Sitter/horizon
acceleration; in a region of density ρ_total the local-Friedmann rate is `H_local² = (8πG/3)ρ_total`, giving
`a0 = (c/2)√(G ρ_total)`. The natural coarse-graining scale of this bath is the **local apparent-horizon radius**

> **ell = r_AH = c / H_local = c / √((8πG/3) ρ_total)**, solved SELF-CONSISTENTLY (ρ_total = ρ_DE + ⟨ρ_matter⟩_ell).

This is **genuinely DERIVED** (the radius of the local causal/coherence horizon that sets the Unruh bath), not tuned.
The MOND radius `r_M = √(GM/a0)` was tested as the alternative ell.

## What the derived ell comes out to — the fatal scale mismatch
- At cosmic density (ρ~ρ_crit): **r_AH ~ c/H0 ~ 5400 Mpc** = the Hubble radius (Gpc, COSMOLOGICAL).
- r_AH only shrinks to ~1 Mpc when ρ ~ 2×10⁷ ρ_crit — far above any cluster's ~500-ρ_crit R500 mean.
- At the full R500 mean density (500 ρ_crit), r_AH = **199 Mpc** ≫ R500 (0.77 Mpc). The horizon NEVER shrinks to
  the cluster scale.

So r_AH is **~100-1000× too big everywhere** and never at the few-Mpc smoothing scale the cluster boost needs.

## (1) GALAXY RAR — real 175 SPARC (PASSES, trivially, because the scale is huge)
Per-point self-consistent density-a0 on the real curves (Υ=0.70 framework footing; Υ=0.50 cross-checked):
- The horizon ball (Gpc) washes EVERY galaxy's matter to ~ρ_DE → **a0_eff = a0(ρ_DE) = 9.36e-11 to 4 figures at
  every point** (a0_eff/a0_DE range [1.0000, 1.0000]).
- **RAR scatter under density-a0 = 0.1471 dex (Υ=0.70) / 0.1537 dex (Υ=0.50) — IDENTICAL to the const-a0(ρ_DE)
  baseline, inflation +0.0000 dex.** Galaxies SURVIVE — but only because the scale is so large the density law
  collapses back to a uniform a0.

## (2) CLUSTERS — real eRASS1 N=9830 (FAILS — no local boost)
- Baseline const a0(ρ_DE): **eta(R500) = 2.149** [IQR 1.99-2.54].
- Self-consistent horizon density-a0: ell converges to **3427 Mpc**, the loop lands at ρ_total ≈ ρ_DE+ρ_crit (the
  cosmic mean), giving a UNIFORM **1.57× boost → a0 = 1.47e-10** (essentially the 1.13e-10 ρ_total footing) and
  **eta = 1.752** [IQR 1.62-2.07]. That is just the ρ_total-vs-ρ_DE footing shift — it applies to galaxies too — NOT
  a cluster-specific boost, and nowhere near 1.2-1.5.
- 0% of clusters over-closed (because there is no real boost).

## The honest both-ways findings (these matter)
1. **The derived horizon ell genuinely fails from the inertia side, exactly as the task's worry anticipated.** The
   dS-Unruh horizon is cosmological (Gpc). Galaxies are safe *precisely because* the scale is huge — and that same
   hugeness kills the cluster boost. You cannot have it both ways with one density-dependent horizon.
2. **A fixed TUNED ell CAN thread both — but it is ~6-10 Mpc, not ~1-2 Mpc.** Scanning fixed ell on real eRASS1 with a
   realistic isothermal cluster (M(<r)~r inside turnaround): ell=1.5 Mpc gives eta=0.56 with 92% of clusters
   OVER-closed (eta<1); the eta~1.2-1.5 window needs **ell ~ 6-10 Mpc** (eta=1.16 at 6 Mpc, 1.47 at 10 Mpc). Galaxies
   stay tight (≤0.001 dex inflation) at every ell ≳ 1 Mpc. **This corrects the deep-dive's "~15× boost → eta 1.2-1.5
   at Mpc-ambient" as OPTIMISTIC** — that was a top-hat estimate; an isothermal cluster concentrates mass, so a 1-2 Mpc
   ball over-boosts and over-closes. The viable tuned scale is even further (6-10 Mpc) from any galaxy/cluster physical
   size, making the "where does this scale come from" problem worse, not better.
3. **The MOND-radius alternative ell = r_M is DEAD.** r_M tracks the SYSTEM (~12 kpc galaxy, ~0.55 Mpc cluster), so it
   smooths each galaxy over its OWN disk (ρ~1e-21 ~ 1e5 ρ_DE) → a0 ~300× too big → destroys the RAR; and it over-closes
   clusters (eta=0.32, 99.7% over-closed). This IS the local/clumpy reading the deep-dive already proved dead.

## Verdict (both ways)
**LEAVES-CLUSTER-DEFICIT.** ell IS derived from the framework's own dS-Unruh inertia (the local apparent-horizon
radius) — but it derives to the WRONG VALUE: cosmological (Gpc), not the few-Mpc a local cluster boost requires. The
density-law a0 therefore does NOT thread both from first principles: it preserves the galaxy RAR (0.147 dex, untouched)
only by being so large-scale that it reduces to a uniform a0, which leaves the cluster eta at ~1.75 (the footing shift,
not a cure). A fixed ~6-10 Mpc ell WOULD thread both, and that scale exists — but it is a TUNED INPUT the dS-Unruh
horizon does not supply, and the MOND-radius derivation gives the dead clumpy reading. **The density-a0 cluster escape
stays SCALE-IS-COSMOLOGICAL: real, falsifiable, but riding on an ell that no framework-native derivation delivers.**

## The honest cost (stated as the task required)
The density reading is a **superset**: `a0 = (c/2)√(G ρ_total)` reduces to ~a0_Lambda cosmically (cosmic ρ_total =
ρ_crit gives a0 = 1.13e-10, still ~cH0, still Milgrom's coincidence; ρ_DE alone is the floor giving 9.36e-11). So it
preserves the a0~cH cosmic coincidence and does NOT cost the a0↔Lambda identity at the background level. BUT making it a
LOCAL law (the only way to help clusters) trades the clean a0↔Λ identity for an a0↔local-density coupling that needs a
smoothing scale — and that scale, derived from the horizon, is cosmological and gives no local boost. So the superset
property is preserved cosmically but is empirically inert for clusters: it buys nothing the uniform a0 didn't already
give, unless ell is tuned.

*No high-priest dismissal (the density law genuinely preserves galaxies, the superset/coincidence is credited, the
~6-10 Mpc tuned scale that works is reported as real). No manufactured win (the derived horizon ell is honestly the
wrong size; the deep-dive's optimistic "1-2 Mpc → 1.2-1.5" is corrected to "over-closes; need 6-10 Mpc"). Quarantine
held: a0/Z posited never asserted derived; ell shown derived-but-cosmological.*
