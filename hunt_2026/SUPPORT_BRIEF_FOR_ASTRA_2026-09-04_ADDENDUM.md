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

## C. The matched disc forward solve you asked for — `hunt_2026/f26_matched_disc_forward_solve.py`

Running at the time of this commit (147 discs, three kernels, each at its own profiled M/L and a₀, ±0.15 dex in a₀;
the validation reproduces the exact exponential disc's QUMOND correction to 0.02 dex on interior points). The
per-kernel disc correction and the paired comparison on QUMOND-corrected residuals follow in the next commit.
