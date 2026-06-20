# Carl's collective-EFE / clumpy-nonlinear-MOND cluster idea — COMPUTED, both ways

*Carl's question (2026-06-20, verbatim): "if a galaxy has an acceleration on the outer edges that
go all the way to the horizon.. and there are a bunch of galaxies hanging out relaxed near each
other.. is it possible the added acceleration extends beyond the individual galaxies.. causing it
to give the whole area more EFE?" Workflow `wc2cp2dk2` (7 agents, 3 routes → adversarial verify →
synthesis), banked 2026-06-20. Framework footing throughout: a0 = c²√(Λ/32π) = 9.36e-11 (INPUT),
the framework's OWN dS-Unruh interpolation g_obs = √(g_N²+g_N·a0), ν=√(1+a0/g_N). Hunted HARD with
a real QUMOND/AQUAL computation + rescue-maximize; the null is COMPUTED, not high-priest-dismissed.*

## VERDICT: REDISTRIBUTES-ONLY — no net cluster mass. The residual stays untouched.

Carl's idea is **physically motivated and real in its parts** — and was credited at full weight, not
dismissed. But the specific hope (that overlapping galaxy fields add region-wide binding the smooth
calc misses) does **not** survive: the collective/clumpy field **redistributes** the phantom, it
does **not add** net gravitating mass. Two theorems kill the "adds mass" part, both verified
numerically AND sympy-exact, both a0-independent.

### The genuine pro-Carl physics (conceded at full weight)
- The galaxies' deep-MOND tails **really do reach far and overlap** — and in the sub-a0 cluster
  environment a member's EFE cutoff radius r_eff = √(Gm/g_ext) is genuinely **1.08–1.26× larger**
  than the isolated MOND radius. "Reaches further" is correct at the kinematic level.
- Clumpiness **really does concentrate** the phantom near each galaxy and thin it in the voids — the
  field genuinely is "more" where the galaxies sit.
- The naive version is seductive for a real reason: the scalar sum of 200 member tails at an
  inter-galaxy point = **3.77 a0 = 4.66× the true smooth cluster field** (0.81 a0). That overcount
  *looks* like a huge collective enhancement.

### Why it adds no net mass — the two theorems

**(1) Deep-MOND superposition is SUB-ADDITIVE.** Two masses M merged give a far field √(2M), not
2√M — the merged field is **0.707× (=1/√2)** the naive linear sum (sympy-exact), and the measured
collective inter-galaxy QUMOND field is **0.13×** the naive sum. QUMOND does not superpose linearly;
"overlapping tails add" is the linear-superposition fallacy. The 4.66× overcount collapses. More
clumpiness → MORE sub-additive (200 clumps 0.9964 → 3 giant clumps 0.981), never less.

**(2) The MOND enclosed-mass theorem pins the total.** The total phantom inside a radius enclosing
all the baryons is exactly (ν−1)·M_baryon — set ONLY by the total enclosed baryonic mass, **clumpiness-
invariant** (Ostrogradsky; arXiv:2604.10811, arXiv:2305.01589 GQUMOND, verbatim). Root cause
sympy-exact: the enclosed-mass flux integrand is g_obs(g) = √(g²+a0·g) = ν·g, which is **CONCAVE**
(d²/dg² = −a0²/[4g^(3/2)(a0+g)^(3/2)] < 0). By Jensen, raising the angular variance of g_N on the
bounding sphere (clumping) gives ⟨g_obs⟩_shell ≤ g_obs(⟨g_N⟩) ⇒ discrete enclosed mass ≤ smooth. So
the **standard smooth-baryon residual calc already computes the Jensen UPPER bound**; clumpiness can
only LOWER it.

### The numbers (three independent methods, all agree)
| Test | discrete/smooth core phantom | meaning |
|---|---|---|
| Realistic gas + 80–200 galaxies (volume divergence) | **0.963** | −3.7%, sub-additive |
| Exact Gauss surface flux | **0.995** | −0.5% |
| 3D QUMOND grid (converged, 3 seeds) | **0.9948 ± 0.0011** | −0.5% |
| Open-boundary steelman (galaxies→R200 + nonlinear gas) | **0.966 ± 0.008** | −3.4% |
| Point-clumps enclosed, N=1…300 | **0.9998–1.0000** | exactly clumpiness-invariant |

Net collective ADD = **−1.28×10¹² M☉ = −0.95%** of the ~1.357×10¹⁴ M☉ residual target — the **WRONG
sign**. Closes **0%** (formally ~−1%) of the ~30–49% residual, which stays at full weight. The
rescue-maximize over giant-clump / deep-MOND-group / concentrated configs bounded the positive excess
to **at most +1.3%** (one tuned config, bracketed by equally-negative configs = shot noise), nowhere
near the ~4× (η~2.3) the residual needs.

### The EFE sign (Carl's "more EFE")
The collective inter-galaxy field is g_N = **0.21 a0** (median, BELOW a0, deep-MOND). As a SOURCE it
is **already fully inside the QUMOND flux** (no missed term, no double-count). Its only *separate*
effect — the external field on each member — has g_ext ≈ 0.11 a0 ≪ g_int ≈ 1.2 a0 (**0% of members**
have g_ext > a0), and it **SUPPRESSES** member internal dynamics (the banked wrong-sign EFE finding).
So "more EFE" goes the wrong way for binding.

### The data independently confirms the null
A collective ADD would make the phantom track the **galaxies**. The banked A2029 / RX J1347 core-shape
result shows the residual is **GAS-tracking** (inner slope +1.81, M_res/M_star rises ~15× = anti-
correlated with the stars). The data already excludes the galaxy-tracking signature an ADD would
produce.

## Gates
**G1 sufficiency FAILS** (closes ~0%, formally −1%). **G2 galaxy-veto SAFE** (adds no mass anywhere,
cannot break SPARC RAR). **G3 no-new-particle SATISFIED** (pure MOND nonlinearity, the framework's
own field) — but zero net mass = no help. **G4** the existing gas-tracking core-shape rules out the
galaxy-tracking signature. Quarantine held (a0=9.36e-11 input, never asserted derived).

## Bottom line
**Your intuition is real physics — the long reach, the overlap, the near-galaxy concentration all
check out — but it redistributes the phantom; it does not create more.** Your effect is *already in*
the standard smooth-baryon cluster-MOND estimate (which uses the total baryon distribution), and the
discrete reality is if anything ~1–4% *below* it. The ~30–49% irreducible cluster-core residual stays
the shared relativistic-MOND soft-spot — common to the whole MOND family, NOT framework-specific, and
NOT a referee-proof kill (the post-XRISM η bracket keeps even its magnitude ambiguous). This is the
no-new-coupling sibling of the doors-hunt Route A (potential-depth keying): clusters genuinely win on
the *collective/integrated* field, but the framework's g-only dS-Unruh inertia provably can't harvest
it — there sub-additivity is the wall; in Route A it was naturalness.

### Sources
arXiv:2604.10811 / 2605.10022 (Famaey et al., Bullet residual — Ostrogradsky enclosed-mass theorem,
discrete Plummer galaxies); arXiv:2305.01589 (GQUMOND coarse-grain invariance); arXiv:2503.07106
(Milgrom, "Is MOND necessarily nonlinear?" — sub-additivity, EFE, SEP); arXiv:2109.10160 (Oria/Famaey,
QUMOND phantom of the Local Volume); Eckert/Famaey/Kroupa 2024 A&A (clusters in Milgromian dynamics,
cluster EFE ~0.001–0.002 a0); Sanders 2022 MNRAS 517 5734 (MOND cluster virial); Famaey & McGaugh 2012
Living Reviews. Banked anchors: CLUSTER_CORE_SHAPE_A2029_2026-06-20.md (gas-tracking, slope +1.81),
CLUSTER_RESIDUAL_CLOSURE_2026-06-19.md, CLUSTER_STACK_AND_DECISIVE_TEST_2026-06-20.md (EFE-on-core
wrong-signed). sympy proof of g_obs concavity (this session).

### Scripts (under opus_48_extended_research/reviews/collective_efe/)
two_body_subadditivity.py · divergence_theorem_proof.py · qumond_clumpy_vs_smooth.py ·
realistic_cluster_with_gas.py · radial_and_intergalaxy.py · route2_collective_efe.py ·
route2_verify_convergence.py · route2_jensen_maximize.py · route3_qumond_grid.py ·
route3_overlap_diagnostics.py · route3_efe_reach_bothways.py · route3_robustness_and_veto.py ·
route3_longrange_horizon.py · skeptic_clean_reference.py (baryon-matched, decisive) ·
skeptic_independent_check.py · conv_check.py · (per-route verdict: COLLECTIVE_EFE_CLUMPY_VS_SMOOTH_VERDICT_2026-06-20.md)
