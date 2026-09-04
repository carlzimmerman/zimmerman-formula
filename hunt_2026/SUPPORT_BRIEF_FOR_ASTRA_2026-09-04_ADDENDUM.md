# Addendum to the support brief, 2026-09-04 (night): what the target is missing, and the matched disc solve

## A. The gate the 13 requirements do not contain

Your §6 plan derives Φ and χ from metric or constrained variables, varies that action, and computes the constraint chain,
toward a static limit that is exactly AQUAL/QUMOND with the chosen kernel at every scale. Three committed numbers say that
static limit is dead before the covariant question is reached:

| the framework's kernel, modified gravity | value | script |
|---|---|---|
| Solar-System EFE quadrupole, QUMOND | 6.2× / 6.8× the Park 2026 ceiling (canonical / alt) | f23 §6 |
| same, exact AQUAL (non-spherical solve) | 7.7× / 8.8×; 7.3× / 8.3× at g_ext − 1σ | f24 |
| modified inertia, lensing | M_dyn/M_lens = 6.4 vs 1.0–1.3 observed, ~20σ | `real_research/reviews/mi_lensing_axis_2026.py` |

None of the 13 requirements is "the theory's own static limit must give |Q₂| < 5.2×10⁻²⁷ s⁻² in the Galactic external
field". Requirement 4 (Cassini/PPN) was checked in the closure program through the kernel's Newtonian tail and the
vector-sector PPN parameters; the EFE quadrupole lives in the transition at r_M(☉) ≈ 0.1 pc and is a property of the
static equation's *shape*, not of its tail. Any completion that reproduces requirement 1 exactly inherits 6–9×.

So the structural statement, which is the closest thing to a lightbulb the numbers allow: **a viable static limit cannot be
scale-free.** It must carry a length ξ below which the phantom response switches off, with 0.1 pc ≪ ξ ≲ 200 pc: the Solar
System and the Gaia wide binaries are then Newtonian, discs and dwarf spheroidals keep the RAR, and lensing keeps the
phantom because the phantom is still a real gravitating response above ξ. Nothing in the framework's own scales supplies a
parsec-scale length (f22 §4a: the Λ lengths are Gpc), so ξ would be a new measurable parameter, like κ.

What the repository has already done with this idea, so you do not repeat it: the localised version (a Helmholtz filter on
the external field, `york_Lclosure_global_2026.py` / `york_Lclosure_dirac_2026.py`, "Theorem 8") was closed as a *local*
closed theory because localising the filter adds a propagating mode. A genuinely non-localisable version, or a medium
with a healing length (condensate/superfluid-type, which supplies ξ = ħ/(m c_s) without a nonlocal kernel), has not been
written; the condensate work that exists (`project_condensate_mu_pincer`) died on the *amount* of phantom between KiDS
galaxy stacks and clusters, not on ξ.

## B. Its one clean test, and its honest status on the ledger — `hunt_2026/f27_newtonian_side_of_the_ledger.py` (3 checks, 2 hypothesis fails)

Predictions of a ξ in that window: Cassini passes; **Gaia DR4 wide binaries give γ_v = 1.00**, the opposite of the
framework's pre-registered 1.16–1.23 (this is the Cassini ↔ wide-binary lock of `cassini_widebinary_lock_2026.py`, read
the other way round); globular clusters (r_h ≈ 20 pc) are Newtonian.

The ledger, with B_Newton = B_MOND + log₁₀ν(y) computed for every row:

- Three of the four outer-halo globulars ARE Newtonian-side: Pal 4 (B_MOND −0.81, B_N −0.11), Pal 14 (−0.87, +0.15),
  NGC 2419 (−0.20, +0.02). Pal 3 is MOND-side (−0.15, +0.72). MOND over-predicts the three by 0.2–0.9 dex.
- But size does **not** order the ledger: DF2 (1.65 kpc, B_N +0.00), the Salpeter early-types, the tidal dwarfs and the
  Milky Way vertical force also sit Newtonian-side at large radii, several of them marginally (M/L choice flips the
  early-types; the tidal dwarfs and K_z are within 0.15 dex of both). "Smaller is Newtonian" has AUC 0.58, p = 0.32.

So this is a Cassini + globular-cluster + DR4 statement, not a ledger pattern, and I am not presenting it as a result.
It is the only structure I can find that passes both arms of the pincer, and DR4 falsifies it cleanly: γ_v = 1.00 keeps
it alive and kills the framework's own pre-registration; γ_v ≈ 1.2 kills it and leaves modified gravity Cassini-dead.

## C. The matched disc forward solve you asked for — `hunt_2026/f26_matched_disc_forward_solve.py` (8 checks, 2 hypothesis fails)

For each of 147 SPARC discs and each kernel: the baryonic field at the kernel's own profiled M/L (f25), inverted to a
sech² thick disc with f18's analytic Hankel inversion, solved in QUMOND with the kernel's ν on the same Hankel grid at
the profiled a₀ and ±0.15 dex, and the disc correction T(R) = log₁₀[g_QUMOND/g_algebraic] applied to the algebraic
prediction on the data before the paired comparison. Validation: the chain reproduces an exact exponential disc's
correction to 0.02 dex on interior points (0.04 at the outermost, extrapolated point). Inversion residual median 0.073
dex, 87 of 147 under 0.10; the comparison is read on the full sample and on that subset. Catalogue distance and
inclination for every kernel (paired); no external field. Descriptive MSE, no sigma.

| | median T (dex) | g_bar/a₀ 0.03–0.1 | 0.1–0.3 | 0.3–1 | 1–3 | 3–30 |
|---|---|---|---|---|---|---|
| ν_RAR | −0.025 | −0.040 | −0.027 | −0.023 | −0.019 | −0.007 |
| μ_exp | −0.023 | −0.040 | −0.027 | −0.023 | −0.013 | −0.001 |
| μ₁₀ | −0.023 | −0.044 | −0.031 | −0.030 | −0.002 | 0.000 |

1. **The disc geometry cannot separate exp from RAR.** Their corrections agree to 0.002 dex (median) against a kernel
   difference of up to 0.073 dex. After correction the paired MSE difference is a coin flip on the full sample
   (interval [−0.00111, +0.00102] dex², exp worse in 49%) and leans exp on the well-inverted subset (worse in 19%,
   interval still containing zero). Undecided stays undecided.
2. **The disc geometry weakens, but does not remove, the μ₁₀ rejection.** μ₁₀'s correction vanishes above a₀ where
   the RAR's is −0.02 dex, so the forward solve moves μ₁₀ toward the data at high acceleration: worse than ν_RAR in
   94.6% of resamples (full) and 90.2% (subset), against 99.9% algebraically. On the forward solve μ₁₀ is
   *disfavoured*, not rejected; the rejection rests on the algebraic comparison (f25, f28). This is the one place
   the forward solve changed a verdict's strength, and you were right to ask for it.
3. **The QUMOND correction makes the framework's kernel fit WORSE** (RMS 0.2015 → 0.2031 dex, ΔMSE +0.00064), leaves
   μ_exp unchanged, and improves μ₁₀. SPARC discs follow the spherical algebraic relation better than the QUMOND disc
   solution of the same kernel. That is f18's curl-sign finding on the full sample: the data do not want the
   modified-gravity disc field. It is a second, independent reason the static limit cannot be "one μ in AQUAL/QUMOND"
   — and it is the side of the fork that has no field-sourced quadrupole either.

Scope left open, as you named it: per-galaxy distance and inclination marginalisation, the external field, and the
AQUAL (rather than QUMOND) disc operator. None of these can plausibly move a 0.002-dex kernel-independence.

## D. The one-argument pincer, closed on the μ_n family — `hunt_2026/f28_one_argument_pincer.py` (4/4)

Both axes with the same machinery: the committed DHF quadrupole integral at the solar-circle field (both footings), and
the paired-galaxy comparison with a₀ and a global disc M/L profiled per kernel.

| kernel | Q₂/ceiling canonical | alt | Cassini | SPARC RMS (dex) | worse than ν_RAR in | galaxy verdict |
|---|---|---|---|---|---|---|
| ν_RAR | 6.23 | 6.83 | fail | 0.2015 | — | reference |
| μ₁ | 6.06 | 6.60 | fail | 0.2016 | 72% | tolerated |
| μ₂ | 2.81 | 3.69 | fail | 0.2042 | 98.8% | disfavoured |
| μ₃ | 1.24 | 1.96 | fail | 0.2059 | 99.8% | rejected |
| μ₄ | 0.59 | 1.10 | safe (canonical) | 0.2070 | 100% | rejected |
| μ₅ | 0.31 | 0.66 | safe | 0.2076 | 100% | rejected |
| μ₇ | 0.13 | 0.31 | safe | 0.2083 | 100% | rejected |
| μ₁₀ | 0.06 | 0.17 | safe | 0.2087 | 100% | rejected |

No member is both Cassini-safe and galaxy-tolerated. The boundary is sharp on both sides: the softest Cassini-safe
member (n = 4) loses on every paired resample; the sharpest galaxy-tolerated member (n = 1) is 6× over the ceiling.
Exact AQUAL only widens the Cassini side (f24: +8–30%). Scope: the μ_n family is the sharpness axis DHF identify as
the only lever on Q₂; it is not every one-argument law, and the statement is on that family.

Read with RESUME_HERE's own line — which field carries the halo cannot move Q₂ — this is the closure of the
one-argument class: no static law μ(g/a₀), carried by any field, passes both the Solar System and the galaxy data.
The second argument is not another acceleration (u02); it is a length.
