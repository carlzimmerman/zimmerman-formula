# Hostile regrade — Sweep 5 (falsifiable corners + exhaustion verdict), 2026-06-15

*Opus 4.8 [1m]. Re-ran SWEEP5_exhaustion_grid.py myself (reproduces every banked number to the digit), and
web-VERIFIED the load-bearing Mistele squeeze against the PRIMARY sources (arXiv:2301.03499 Mistele-McGaugh-
Hossenfelder 2023; arXiv:2304.05134 Verwayen-Skordis-Boehm 2024), extracting the actual m²/f_G and μ numbers from
the PDFs rather than taking the memos on faith. Both ways. Quarantine held (a0/Z never asserted derived).*

## What reproduces (CONFIRMED, full weight)

- **Grid reproduces exactly.** framework a0 = 9.3614e-11; SPARC 175 loaded; eRASS1 N=9830, z_med=0.30.
  Front-2 RAR: dS-Unruh min 0.1029 dex @(1.2e-10, U=0.65), 52/84 (62%) viable; FW@U0.5:0.1447, U0.7:0.1083.
  Front-7 cluster median η(R500): dS-Unruh 2.37/2.33/2.21/2.07 across a0=[9.1,9.36,10.5,12.0]e-11. All banked.
- **Cluster η is a0/IF-ROBUST at ~2** — across the ENTIRE galactic box η stays 1.9–2.4; the galactic knobs
  (a0, Υ, ν) NEVER drive η→1. CONFIRMED: cluster closure cannot come from the galactic sub-box. Credit.
- **The box factorizes** into galactic {a0=Λ, Υ, ν} (fronts 1–6,8,9) and cosmological {μ, I0, cs²} (front 7 + CMB),
  sharing no parameter. The exhaustion question = do they intersect. Correctly posed. Credit.

## TWO corrections to the sweep's framing (both ways)

### CORRECTION 1 — the Mistele squeeze is a PILE-UP at m²/f_G≈1 Mpc⁻², NOT two DISJOINT intervals.
The sweep's `fine_tuning` field says: *"no single m²/f_G satisfies both galaxy-WL and clusters … the viable
mu-interval for clusters is DISJOINT from the galaxy-WL interval."* The PRIMARY source does **not** support
"disjoint." Verbatim from Mistele 2023 (arXiv:2301.03499, eq. 10 context):
> "Skordis & Złosnik (2021) require m²/f_G ≲ 1 Mpc⁻². … this does not guarantee MOND-like behavior for weak
> lensing which probes radii up to ∼1 Mpc. One might therefore want to choose an even smaller m²/f_G. **But this
> is not easily possible. Indeed, galaxy clusters require more acceleration than MOND** … m²/f_G **cannot be much
> smaller than 1 Mpc⁻²** and we assume **m²/f_G ∼ (1 Mpc)⁻²**."

And Verwayen-Skordis 2024 (arXiv:2304.05134): "in practice **μ⁻¹ ≳ 1 Mpc**"; galaxy WL (~200 kpc) "gives an
estimate that **μ⁻¹ ≳ 1 Mpc**"; fiducial **μ = 1 Mpc⁻¹**.

So BOTH sides converge on m²/f_G ≈ 1 Mpc⁻² (μ⁻¹ ≈ 1 Mpc): galaxies want it *smaller* (MOND extends further),
clusters forbid it from being *much smaller*. The result is a **narrow pile-up band right at 1 Mpc⁻²**, with a
*residual* mild WL tension because even at 1 Mpc⁻² AeST deviates slightly from MOND at ~1 Mpc — NOT two
non-overlapping intervals with an empty gap. The earlier SWEEP4 memo got this right ("narrow ~4× window,
non-empty"); the SWEEP5 `fine_tuning` prose overstated it to "DISJOINT." **The squeeze is real and tight, but
the cluster μ is NOT in a galaxy-WL-FORBIDDEN zone — it is at the EDGE of the galaxy-WL-allowed zone, where a
residual tension exists but no hard exclusion.** Net effect on the verdict: the cosmological intersection is
TIGHT/edge-tensioned, not strictly EMPTY for the mass-term. This is a SOFTENING of the sweep's pessimism — both
ways: still a genuine squeeze (no manufactured room), but not the harder "disjoint/empty" the sweep wrote.

### CORRECTION 2 — at the Λ-tied a0, the framework's OWN dS-Unruh IF needs Υ≳0.6, not "57% of [0.4,0.7]".
The sweep's "57% of [0.40,0.70] viable" counts viable CELLS across the a0 BAND. At the *single* Λ-tied
a0=9.36e-11 under the framework's *own* dS-Unruh ν, my run gives scatter vs Υ: 0.40→0.191, 0.50→0.145,
0.55→0.128, 0.60→0.117, 0.65→0.110, 0.70→0.108. So at threshold 0.13 dex only Υ∈{0.55,0.60,0.65,0.70} pass
(4/7), and it is **one-sided: Υ≳0.55–0.60**, not a symmetric 57% slab. (simple-mu/McGaugh are more forgiving,
5–6/7.) Threshold sensitivity: 3/7 at 0.12, 4/7 at 0.13–0.14 for dS-Unruh. **Both ways:** this is NOT fine-tuned
— the required Υ≳0.6 is *exactly* the framework's stated footing (Υ≈0.70, the Spitzer 3.6µm population-synthesis
value), so the one-number a0=Λ lands viable at the independently-motivated Υ. But it is honest to state the
dependence as "the framework's own IF requires the upper half of the Υ prior," not "57% of the prior works." The
broad-region claim survives; its precise shape is one-sided and IF-dependent.

## The regraded exhaustion verdict (both ways, after the two corrections)

- **GALACTIC (sub-box A): NON-EMPTY, BROAD, NATURAL — CONFIRMED.** a0=Λ=9.36e-11 sits inside the data band
  [9.1e-11,1.2e-10] at ≤2% RAR penalty; fronts 1–6,8,9 share it; the one nuisance Υ at the framework's own IF
  must be ≳0.6 (its measured value). One-number prediction in a wide band = the OPPOSITE of fine-tuning. CREDIT.
- **COSMOLOGICAL (sub-box B): the CMB fits at +1 measured I0≈Ω_c h² (natural, ΛCDM-like); the cluster CURE is
  TIGHT-but-not-strictly-disjoint.** The unified-scalar +1 hope genuinely FAILS by the computed cs²=(Q−Q0)/Q∝a⁻³
  scale-blindness (CONFIRMED, that physics is sound and credited). The cluster boost is the separate μ, and the
  Mistele squeeze is REAL — but it is a pile-up at μ⁻¹≈1 Mpc with residual WL tension, not an empty disjoint gap.
  Cost is **+2 (I0 + μ)**, and even at +2 the μ²Φ cure is undelivered (non-monotone, per-cluster). CONCEDE the +2
  and the undelivered cure; SOFTEN "empty/disjoint" to "tight/edge-tensioned."
- **NET:** the verdict stays **(b)-leaning-(a-galactic)**: jointly viable & natural GALACTICALLY (+0, one number),
  viable only at +2 COSMOLOGICALLY, with the cluster front SOFT/MOND-shared/systematic-limited [η~1.0–2.33]. No
  referee-proof kill survives; the galactic corner is genuinely NOT fine-tuned; the cosmological economy claim
  ("two dark sectors, one number") holds ONLY at z=0 galaxies. The two sweep overstatements (disjoint μ-interval;
  symmetric 57% Υ) are corrected DOWNWARD in severity — both ways, the framework comes out slightly BETTER than
  the sweep wrote (tight not empty; one-sided-Υ-at-its-measured-value not a fine slab), while the +2 cost and the
  galactic-only economy are conceded at full weight.

## Falsifiable corners (unchanged, confirmed)
Fastest-shrinking = **wide binaries (Gaia DR4, late 2026)** — the framework's own sharp-IF cap γ~1.08–1.14 straddles
Chae's pro-MOND and the Banik/Pittordis Newtonian null; a Newtonian-leaning DR4 is a SERIOUS blow to the a0(z)
premise. Sharp prediction = **a0(z)∝√ρ_DE declining** (−7.3% in V by z=3, distinctive by SIGN), DESI-gated, 2030s ELT.
Cluster μ-corner = density-a0 member-kinematics σ↑ vs EFE σ↓, ~2027–28. NO manufactured corner; NO dismissal.

*Sources web-verified this session: Mistele-McGaugh-Hossenfelder 2023 A&A 676 A100 (arXiv:2301.03499, eq.10 +
m²/f_G≲1 Mpc⁻² Skordis-Złosnik requirement, extracted from PDF); Verwayen-Skordis-Boehm 2024 MNRAS 531 272
(arXiv:2304.05134, μ⁻¹≳1 Mpc, fiducial μ=1 Mpc⁻¹, extracted from PDF); Durakovic-Skordis 2024 JCAP 04 040
(μ²Φ non-monotone, banked). Grid: opus_48_extended_research/reviews/SWEEP5_exhaustion_grid.py.*
