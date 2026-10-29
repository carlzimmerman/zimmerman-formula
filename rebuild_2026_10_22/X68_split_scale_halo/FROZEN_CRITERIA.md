# X68_split_scale_halo: FROZEN CRITERIA (committed alone, before any script or graded number)

**Source.** The external model's T1 (relayed by the owner, 10-29): decouple the inner core radius from an outer infall
scale, so cluster halos are not forced onto a Burkert r⁻³ tail just outside a small core. The owner said "keep pushing on
your own". **Motivation in the record:** X43 under-predicts heavy-cluster outskirts (G-OUT-M3 Z +2.41; CFG406
heavy-cluster outer excess). IB1 / X48 find inner cores too dense.

**Standing:**
- κ = ½ FITTED. Footings never pooled.
- Route E, Newtonian; cold dark energy is not matter.
- Not "theory closed". Nothing here may say the data favour the framework.
- c_f = 4 stays EXTERNAL (X43's disclosure), and the label carries it.

## Hypothesis SS (split scale)

Everything is X43 (00bc1a7950) except the halo shape:

ρ(r) = Σ_core r_s² / ((r + r_c)(r² + r_s²))

- **Inner core:** Σ_core = ρ₀ r_c = max(a₀/(2πG), η Σ_coll(M)) is X43's rule, unchanged (η = 14.83).
- **Outer scale:** r_s = max(r_c, r_f / c_f). Here r_f is X43's own formation radius of the half-mass object,
  (3(M/2)/(4π Δ ρ_m(z_f)))^(1/3) with Δ = 18π² on background A, and c_f = 4.
  - This is the infall scale X43 already uses. No new constant.
  - r_s is never inside the core. When r_s = r_c the profile is exactly X43's Burkert.
- **Normalization:** r_c is solved so the halo's mass inside X43's outer radius (R200 for SPARC and groups, r_ta for
  clusters) equals X43's mass. If no root exists on (0, r_f/c_f], that halo FALLS BACK to X43's Burkert, and it is
  counted.
- **Rejected:** the proposal's own r_s = (Σ_core/Σ_M) r_c is not used, because it makes the outer halo depend on a₀.

**Enclosed mass (closed form):** with x = r/r_c and S = r_s/r_c,

M(r) = 4π Σ r_c² S²/(S²+1) [ln(1+x) + (S²/2) ln(1+x²/S²) − S arctan(x/S)].

## Checks (all must pass, else UNDECIDED, exit 1)

- **K0:** with the split forced off (r_s = r_c), X68 reproduces X43's committed results on both footings to 1e-6:
  - SPARC rms on both backgrounds;
  - groups Z;
  - every cluster key's pred.
- **K1:** the closed-form M(r) matches quadrature to 1e-6 at S = 1, 3, 10. At S = 1 it equals X43's π Σ r₀² B(x).
- **K2:** a solved r_c returns the target mass to 1e-8.
- **K3:** peak RSS < 2 GB.

## Verdict (per footing; the class needs both to agree)

- **SS PASSES:** SPARC line on both backgrounds AND all 15 cluster keys |Z| ≤ 2 in both h cells AND groups CONSISTENT.
- **SS FAILS:** <systems / keys with sign>.
- **SS UNDECIDED:** more than 25 % of cluster cells fall back.

**Reported, not graded:**
- the distribution of S = r_s/r_c (SPARC, groups, clusters) and the number of fallbacks;
- every key's Z against X43's (better / worse);
- the proposal's own r_s = (Σ_core/Σ_M) r_c variant, run once on canonical only.

MUTATE: r_s = max(r_c, 2 r_f/c_f), with separate outputs. It must change at least one cluster pred by more than 0.01,
otherwise the harness is insensitive.
