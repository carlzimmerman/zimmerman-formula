# X40_fixed_core_radius — FROZEN CRITERIA (committed alone, before any script or number of this lane)

**Hypothesis FC.** Route E: cold dark energy (w ≈ 0, collisionless at merger speeds, not matter) clumps everywhere,
gravity is Newtonian, and the RAR is emergent. Its halos are Burkert-cored with a **core of fixed physical size r_c**,
the same in every halo. This is the behaviour of a self-interacting field's ground state (a Thomas–Fermi radius set by the
field, independent of the halo's mass). The motivation comes from X38 + X39:
- a fixed surface density (X38) gives r₀ ∝ √M, so the biggest clusters get the widest, flattest cores. That is the wrong
  way round: their MID band comes out ×2 short (Z +4).
- baryonic contraction cannot fix it without breaking SPARC (X39).
- a fixed core length is resolved in galaxies (R ~ kpc) and negligible at 0.3–1 Mpc in clusters.

**One new constant, r_c.** It is calibrated on SPARC only, then the clusters are graded once with no further freedom.
Standing rules: κ = ½ FITTED (it does not enter route E's dynamics here; the footings enter through C* and the X30 grading
cells). Footings never pooled. Raw data, framework-native. No ΛCDM concentration relation. Not "theory closed". Nothing here
may say the data favour the framework.

## 1. SPARC calibration (sets r_c; no cluster input)

- EM1's machinery and committed M200 relation, borrowed (as X38): lg M200 = a + b(lg M_b − 10), with A (11.18, 0.90) and
  B (11.20, 0.90).
- Burkert with r₀ = r_c in every galaxy. ρ₀ is set by M_h(<R200) = M200.
- **r_c = the value minimising the pooled SPARC rms** over a fixed log grid of 0.5–30 kpc (41 points), on background A.
  It is reported with the rms and the median Υ at that point.
- SPARC's grade is EM1's line at r_c on both backgrounds.
- The same r_c serves both footings: the SPARC prediction does not depend on a₀ under route E.

## 2. Clusters (verdict-bearing, one evaluation)

- X30's machinery and keys, executed read-only, as X38/X39.
- Halo: Burkert, r₀ = r_c, normalised to M_h(<r_ta) = 5.364 M_b, zero outside r_ta. Newtonian on M_b + M_h.
- Keys as X38: G-MID-T1..T3, G-MID-b, G-OUT-all, G-OUT-T1..T3, G-OUT-b, G-IN-all, G-OUT-Mall, G-OUT-M1..M3, G-IN-Mall.
  |Z| ≤ 2 in both h cells.

## 3. Verdict (per footing; the class needs both footings to agree)

- **FC PASSES** — the SPARC line passes on both backgrounds AND every cluster key passes.
- **FC PASSES SPARC ONLY** / **CLUSTERS ONLY** / **FAILS** — as X38, with the failing legs listed.

Reported:
- r_c ± the grid points within Δrms = 0.002;
- the cluster grades at those neighbouring r_c (reported only, never adopted);
- the comparison with X38 per key;
- r_c against L★ (21.7 / 22.9 pc), stated, not graded.

Not graded: dwarfs, the forest (a field core of r_c also implies a Jeans-type cutoff, to be checked separately), and
galaxy–galaxy lensing.

## 4. Checks (all must pass; `--mutate` must fail K1)

- **K0:** X38's SD numbers are reproduced by this lane's code with the X38 halo (SPARC rms 0.0795 bg A canonical; cluster
  OUTER all-KT pred 0.697) to 1e-4.
- **K1:** the fixed-r_c Burkert normalisation returns M200 (galaxies) and the fair share (clusters) to 1e-10, and the
  closed-form M(<r) matches the quadrature to 1e-6.
- **K2:** with r_c → 0 (10⁻⁴ kpc), the SPARC halo approaches a cusp: the predicted median Υ falls below X38's. A sanity
  direction check, not a number.
- **K3:** peak RSS < 2 GB; one thread; minutes.
- **MUTATE:** the normalisation uses B(R/r_c) evaluated with +2 arctan; K1 must fail.
