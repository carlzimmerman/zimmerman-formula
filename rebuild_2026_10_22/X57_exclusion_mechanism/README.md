# X57_exclusion_mechanism: what keeps full-strength cold dark energy out of galaxies without heating or converting it?

**Post-result correction, 2026-10-27:** [A1](CORRECTION_A1.md) supersedes the
R4b inference below. M6 is **NOT DECIDABLE on both footings**, including alt.
The corrected two-sigma band-entry bound does not exclude either footing, and
nonnegative density alone does not establish a shear lower bound. General
radial profiles remain unresolved; no physical rescue is demonstrated. M1–M4
retain their independent failing gates. The original results below are retained
as history; [corrected results and provenance](../../closure_program_2026_10_27/gate_fixes/README.md)
are separate artifacts.
The historical forest fraction below is an assumed gas-variance budget, not
a calibrated flux confidence limit. The
[population-versus-forest calculation](../../closure_program_2026_10_27/RESULTS.md)
separates that benchmark from the required galaxy population and its ancestry.

## Historical frozen-run report

Criteria: `FROZEN_CRITERIA.md` + `ASSUMPTION_LEDGER.md` (6cadf4f9b0, committed alone, before any script or number). Two
coordinator instructions were folded in before the freeze: the R4b line is graded for every class, and M5 is reported only.
No amendment. κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s², never pooled. Cold dark energy is a gravitating w ≈ 0
field component, not matter and not a particle. No ΛCDM-derived inputs. Not "theory closed". Nothing here says the data
favour the framework. Every number below is from `x57_exclusion.out` / `x57_exclusion_results.json`.

## Verdict (frozen rule): **UNDECIDED**

- **M1, M2, M3 and M4 are EXCLUDED on both footings, each by its own line.** None of these exclusions depends on R4b.
- **M6 (displacement) is the only graded class not excluded on canonical.** There it is NOT DECIDABLE WITH RECORD DATA. On
  alt it is EXCLUDED BY R4b, and by R4b alone.
- **M5 (object-keyed, nonlocal) is reported only.** The peer's `X58_object_keyed_switch` runs it operationally (frozen
  9964127dfd). Its results were not committed when this README was written, so its numbers are **pending** here.

| class | canonical | alt | binding number |
|---|---|---|---|
| M1 sector coupling (cold dark energy feels GR only) | **EXCLUDED BY R3** | **EXCLUDED BY R3** (and R4b) | It still collapses by its own self-gravity. Content inside R_last ≥ 0.541 of the fair share (X22's virial-heated floor; the frozen-cut capture is 0.760), against f_max 0.196 / 0.027: ×2.8 / ×20 over |
| M2 repulsive baryon ↔ cold dark energy Yukawa | **EXCLUDED BY R1∩R3** | **EXCLUDED BY R1∩R3** (and R3b, R4b) | The forest allows β ≤ 0.036–0.064 for λ ≳ 10 kpc. Galaxies need β ≥ 1 + μ = 1.035 / 1.005 (static balance at R_last). Best ratio β_max^R1/β_min^R3 = 0.049 / 0.050 at λ = 13 kpc. Lens environment (1 Mpc): 0.036 |
| M3 repulsion by the law's own phantom (x < 1) | **EXCLUDED BY R1** (and R4) | **EXCLUDED BY R1** (and R4, R4b) | Linear phantom push over cold self-gravity Q = 2.23 / 1.91 (z = 2 / 3; alt 2.46 / 2.11) ≥ 1, so cold dark energy does not grow. Cluster cores sit at x_b(r₀) 0.048–0.073, inside SPARC's 0.025–0.240 |
| M4 wave / coherence scale ν_w | **EXCLUDED BY R3** | **EXCLUDED BY R3** (and R4b) | The forest allows ν_w ≤ 97.3 kpc·km/s. Even counting the full de Broglie length as the exclusion radius, only 32.6 % of SPARC have r_w ≥ R_last (median r_w/R_last 0.52). The median galaxy needs ×1.91 the allowed ν_w |
| M6 displacement (compensated anticorrelated patches) | **NOT DECIDABLE** (R1, CMB, R4b ND) | **EXCLUDED BY R4b** | The CMB is blind at linear order (max \|ΔC_ℓ/C_ℓ\| 7.4e-6, against 2.0 for the uncompensated control). The forest allows F_b ≤ 0.060 / 0.048 of all baryons in depleted patches (z = 3). The record has no measured F_b |
| M5 object-keyed (nonlocal) | reported only | reported only | X58 pending. Action-form analysis below |

So no graded class supplies the exclusion through its own physics, except possibly M6. The frozen rule gives UNDECIDED,
not NO GRADED CLASS VIABLE, only because of M6 on canonical.

## Step 0 (stop rule): 23 / 23 reproduced exactly (K0)

| item | value |
|---|---|
| X22 forest edge | α_NF 0.02991 Mpc/h, λ_hm 0.4167 Mpc/h, M_hm 4.894e9 M☉ |
| X22 galaxy tolerance | f_max 0.1965 / 0.0269; tolerated M_c(<R_last)/M_b median 0.0354 / 0.0049; R_last / V_last medians 11.27 kpc / 99.7 km/s |
| X22 capture | frozen-cut capture median 0.7603; virial-heated content 0.5405; rms linear gravity 3.83e-12 / 5.15e-12 m/s² at z = 2 / 3 |
| X34 | cold dark energy must be on (dust-like) by z_on = 5e4; 2e4 is excluded |
| X54 | ξ ∈ [−0.0035, +0.0011] (DES-SN5YR), [−0.0036, +0.0010] (PP), [−0.0037, +0.0009] (U3); Ω_m 0.2970 (BAO), 0.3039 (BAO + PP) |
| X53 / X55 | Δχ²(H2H − L2H, all radii) +429.57 / +455.55; n_sep 4.55 / 4.26σ |
| X30 via X56's law copy | OUTER meas 0.716 ± 0.141 / 0.656 ± 0.129. The law alone predicts 0.999: Z −2.01 / −2.14 (canonical, h 0.672 / 0.686) and −2.66 / −2.80 (alt). The law alone leaves MID T3 short at Z +4.46 / +4.11 |
| X43 | MID T3 Z +0.30; groups Z +2.05 |
| X40b | cluster g_b(r₀)/a₀ T1–T3 0.048 / 0.055 / 0.073 (canonical) and 0.041 / 0.048 / 0.064 (alt) |
| X47 | VT FAILS AT growth / data; VT-O CONSISTENT (NONLOCAL, mechanism open) |
| X32 | dust-like tracer f_ret 0.80–1.02 |

## Per class (what was computed)

**M1, sector-dependent coupling.** If cold dark energy feels only GR, its linear growth is X22's dust growth (R1 holds by
construction). It still collapses into galaxy-scale halos by its own self-gravity, because the galaxies' Lagrangian
scales are 9.5 × the forest's half-mode mass (X22 A3). Being blind to the law's phantom does not stop that collapse.
Inside R_last it keeps at least 0.541 of the fair share against 0.196 / 0.027 allowed. **Yes, it still collapses.**

**M2, repulsive Yukawa between baryons and cold dark energy.**
- Machinery: X22's two-fluid ODE, with the baryon ↔ cold cross term multiplied by (1 − β_eff),
  β_eff = β/(1 + (a/(k h λ))²), and the forest graded on the gas.
- **Range and strength allowed by R1 (forest):** β_max^R1 = 6.6 at λ = 100 pc; 0.25 at 1 kpc; 0.072 at 10 kpc; 0.039 at
  100 kpc; and 0.0365 for λ ≥ 1 Mpc. At early times every forest scale lies inside λ (physical λ, comoving scales shrink
  into it), so the baryons' fall into cold wells is cut throughout.
- **Required by R3:** β (1 + x)e^{−x} ≥ 1 + μ at x = R_last/λ, i.e. β ≥ 1 + μ = 1.035 / 1.005 even for λ ≫ R_last.
- **The intervals do not intersect at any λ.** The best ratio is 0.049 (canonical) / 0.050 (alt) at λ = 13 kpc. The lens
  environment (1 Mpc) gives 0.036; this is the λ → ∞ asymptote, so the grid edge does not limit it. Assembly against
  the fair-share self-gravity (reported) gives 0.008.
- **Equivalence principle (derived, ledger A9):** the force couples baryons only to cold dark energy. Its local source is
  cold dark energy within λ of Earth, which R3 itself requires to be absent. So EP tests do not bind; no external number
  is used. The class fails before EP matters.
- The sign is checked (K2: repulsion lowers baryon clustering, T_b 0.034 at β 1). The MUTATE twin (attractive) gives
  T_b = 3.22.

**M3, repulsion from the law's own field.**
- Sign: outward where x < 1. Object scale: the phantom push beats the fair-share cold self-gravity only beyond
  r* = 5.364 √(G M_b/a₀) = 17.7 / 16.1 kpc for the median SPARC M_b (7.3e9 M☉), i.e. outside the median R_last.
- **(L)** If the law acts on linear baryon perturbations: x_lin = 0.041–0.055 ≪ 1, so the push on cold dark energy is
  1.9–2.5 × its own linear self-gravity. It does not grow, so R1 fails. This is X47's μ-pincer in phantom form.
- **(V)** If the law is off in the linear regime (v3s without khronon charge, X35): x < 1 in both the linear medium and in
  galaxies, so the key is not x. The class becomes object-keyed (M5) and Theorem G applies.
- **Either way, R4 fails:** cluster cores sit at x_b(r₀) 0.04–0.07, inside the SPARC range, so an x-keyed push that empties
  galaxies also empties cluster cores.

**M4, wave / coherence scale.**
- Machinery: the linear term −(ν_w²/4)k_phys⁴ δ_c in X22's ODE. ν_w is a field-energy parameter in m²/s; no particle mass
  is implied.
- Largest forest-allowed value: ν_w,max = 97.3 kpc·km/s (3.0e24 m²/s). This is generous: X22's ODE starts at a = 1e-3 and
  misses the earlier suppression (ledger A3).
- The coherence length r_w = 2πν_w/V **shrinks with mass**. Cores are largest in the smallest objects.
  - It cannot clear the median galaxy: r_w/R_last median 0.52, with 32.6 % of SPARC cleared.
  - It leaves cluster cores untouched: r_w = 0.6 kpc at σ = 1000 km/s, so R4 holds.
- Even a cleared core is not an empty one, so this R3 FAIL is a lower bound.
- The task's guess that the scale "grows with mass" has the wrong sign for this class.

**M6, displacement.**
- Compensated patches with δ_c,in = −0.804 / −0.973 need δ_b,in = +4.31 / +5.22 from the start.
- Positivity: the depleted Lagrangian volume is ≤ 0.188 / 0.161, and at that bound every baryon in the universe sits in
  the patches. Checked by brute force (K5).
- The forest bounds the frozen isocurvature gas variance: F_b ≤ 0.060 / 0.048 (z = 3) and 0.106 / 0.084 (z = 2). This
  uses σ²_ad(R_L = 0.442 Mpc/h, z = 0) = 10.6 on the record's BBKS shape with EM1's σ₈.
- X34's vanilla CLASS with C7's parameters is blind to the compensated mode: 7.4e-6, against 2.0 for the uncompensated
  control. So the CMB cannot decide (ND).
- **Open:** whether every isolated galaxy's Lagrangian region (and, by X55, its environment to ~1 Mpc) fits inside ≤ 5–6 %
  of the cosmic baryons. The record has no F_b.

**R4b, the common line (coordinator).**
- Every graded class keeps the law on cluster baryons and adds non-negative cold mass. Its OUTER prediction is therefore
  ≥ the law's 0.999: Z −2.01 / −2.14 (canonical; one hundredth past the 2.0 line in the h 0.672 cell) and −2.66 / −2.80
  (alt).
- The frozen escape route is a cold dark energy deficit below the cosmic mean around clusters. Its mass bound is
  D = 3.77e12 / 1.17e13 M☉ = 0.323. That exceeds the canonical drop needed (0.284) and is below the alt one (0.344). So R4b
  is **ND on canonical and FAIL on alt**, for every class.
- **Reported only (post-result diagnostic, does not change any grade):**
  - A uniform evacuated 3 Mpc sphere's shear at 2 Mpc is only 0.089 of M_hole/(πR²), which would put the escape far
    short on canonical too.
  - Only a class that empties cluster outskirts below the cosmic mean can use the escape at all. M1, M4 and M6 do not
    (M6's outskirts are the cold-enriched side).
  - Read that way, R4b fails for every class on both footings, and M6 would be EXCLUDED BY R4b on canonical as well.
  - The canonical margin of the law-alone line itself is thin (Z −2.01).

## M5 (reported only): which action form could implement an object-level switch?

What the record requires (X47, X56, and X58's rule): below X43's crossover (M ≈ 10^12.09 / 10^12.43 M☉, where η Σ_coll =
a₀/(2πG); `X56_law_floor_structure/x56_x43copy_law_x48.out`) the law acts on baryons and there is no cold halo; above it, cold dark energy is present in collapse halos. The
switch must key on the bound object and be off in the linear universe.

- **Local fields fail.**
  - A local key in x, ρ_b, θ or the tether invariant either acts in the linear universe or never forms. This is the
    μ-pincer: X47's local rule FAILS at growth, and M3 (L) above gives Q 1.9–2.5.
  - CFG944's Theorem G: no local L(θ, u) satisfies the static law, linear growth, ghost freedom and the slip line together.
  - X22 step 3C: x and ρ_b do not separate the cosmic medium from SPARC.
- **Forms that are not excluded, none of them in the record:**
  - **(a) A phase-space key.** The cold component's own velocity dispersion vanishes before shell crossing and is nonzero
    in virialised objects. So it is off in the linear universe without a ghost. CFG944 lists "a medium held up by
    dispersion rather than a tether" as untested. It needs a kinetic (multi-stream) description, which the single-stream
    khronon lacks (X14: caustics generic). On its own it does not separate galaxies from clusters, since both are
    virialised. It also needs the object's Σ compared with a₀/(2πG).
  - **(b) A retarded nonlocal operator** (□⁻¹ of an invariant that is quadratic in perturbations, such as shear or
    vorticity) carrying the object's formation history. It is covariant, but nothing in the record derives it, and its
    ghost status is unknown.
  - **(c) A constraint functional over a bound region.** This is the switch as stated, but it is not a field theory.
- **Status:** an operational rule (X58, numbers pending) without an action. Theorem G and the μ-pincer leave only (a)–(c).

## Shortlist (reported, not graded) and the deciding observation

1. **M6, displacement** (not excluded on canonical by the frozen rule). It survives only if the depleted patches hold
   ≤ 5–6 % of the cosmic baryons (forest) and all of them sit in ≤ 16–19 % of the volume. It also has to pass R4b, which
   the reported reading above says it does not.
2. **M5, an object-keyed switch** (reported only; operational test X58; action forms (a)–(c), none derived).

**One observation that decides between them:** the small-scale Lyman-α forest gas power at z ≈ 4–5.5.
- M6's isocurvature gas excess is frozen, while the adiabatic power grows as D². At the bound allowed at z = 3, its ratio
  to the adiabatic power rises roughly as 1/D² toward higher z, and so must show up as a forest excess at k ≈ 1–10 h/Mpc.
- M5 leaves the cold sector adiabatic: no excess at any z.

## Checks

- **Main run: 7/7 PASS, exit 0.** 18.4 s, peak RSS 0.265 GB (self + CLASS children), one thread.
  - K0: Step 0, 23/23, plus the M2 FAIL onset is monotone.
  - K1: at β = 0 the ODE gives δ_m(z = 0) 0.787089, equal to X22's C2.
  - K2: the M2 sign.
  - K3: the M4 sign. **Disclosed:** at the frozen ν₁ = 0.1 kpc·km/s (≪ ν_w,max) the printed T² is 1.00000 to five
    decimals, so K3 tests only the sign of the term, not its size; the twin's anti-pressure still flips it.
  - K4: sympy Yukawa limits, +4πGβλ²ρ_b locally and −β × Newton at kλ ≫ 1.
  - K5: M6 positivity, closed form against brute force.
  - K6: resources.
- **MUTATE (`X57_MUTATE=1`): exit 1, twin OK.** Exactly K0, K2, K3 and K5 fail, as required; K1, K4 and K6 pass.
  - m1: attractive force, T_b 3.22.
  - m2: anti-pressure.
  - m3: X53 Δχ² + 1.
  - m4: r → 1/5.364.
- CLASS runs went to the system temp directory and were removed after the run. The binary SHA-256 is in the JSON.

## Files

- `x57_exclusion.py`: run with `PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x57_exclusion.py` (twin:
  `X57_MUTATE=1`).
- `x57_exclusion.out`, `x57_exclusion_results.json`: normal run.
- `x57_exclusion_MUTATE.out`, `x57_exclusion_results_MUTATE.json`: twin.
