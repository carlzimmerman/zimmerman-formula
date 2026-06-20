# CLUSTER-CORE STACK — best-case no-new-particle coverage (key "stack") — 2026-06-20

**Workflow:** `cluster-stack`. Stacks the INDEPENDENT no-new-particle pieces from the framework MI phantom
toward the rich-cluster CORE target, no double-counting, both shape scenarios, both banked normalizations, on
the framework footing a0=9.36e-11. Real eRASS1 (Bulbul+2024, erass1cl_primary_v3.2.fits) + WebFetch of the
three cited papers. Script: `stack_no_new_particle_core.py` (run reproduces every number).

## HEADLINE (both ways)
**In the GALAXY-tracking best case, ZERO new particles cover ~76% of the rich cluster core (realistic
geometry), ~85% at the absolute banked ceiling — a SUBSTANTIAL partial closure, NOT a true closure. In the
GAS-tracking case the best is ~50%. The residual gap that stays is ~20-32% of the bare core gap (~3e13 Msun,
galaxy-tracking) to ~50-68% (gas-tracking). So: better than "still ~50%", short of a clean ~80-90%
near-closure — and which it is hinges entirely on ONE contested observable (core-residual shape).**

## INPUTS (banked, ROUTEA primary normalization)
- CORE TARGET M_res(<420 kpc) = **1.357e14 Msun** (~10x gas; lensing=X-ray ratio 1.03).
- Framework MI phantom = **3.508e13 Msun** (~1.4x gas) = 25.9% of target.
- Bare CORE GAP = **1.006e14 Msun**, undershoot x3.87.
- (Carried both ways: the CLASH/eRASS1 eta-worst anchor target 2.30e14 / phantom 4.00e13 / gap 1.90e14 / x5.75
  — gives systematically LOWER coverage because the target is bigger; reported alongside.)

## THE STACK (each piece at honest best-case, no double-count)
| Piece | Mass in core | % of target | Source |
|---|---|---|---|
| Framework MI phantom (start) | 3.508e13 | 25.9% | banked (= AeST MG to machine precision) |
| (i) Route B full-AeST Y-Q field boost (+20% on phantom) | 7.0e12 | 5.2% | Durakovic-Skordis 2312.00889 (reproduced) |
| (ii) IGIMF stellar remnants in core (GALAXY-track, max-gen 8x) | 5.4e13 | 39.7% | Zhang-Zonoozi-Kroupa 2602.06082 |
| (iii) Missing warm-hot baryons (optimistic ceiling) | 7.3e12 | 5.4% | ROUTEA (FLAG: mostly >R500) |
| **TOTAL (galaxy-tracking best)** | **1.033e14** | **76.2%** | residual 32% of gap |

GAS-tracking best (same pieces, IGIMF shape-suppressed ~3x): TOTAL 6.74e13 = **49.7%**, residual 68% of gap.

## CRUCIAL HONESTY (enforced)
1. **No IGIMF double-count.** Route A's "2x heavier BCG" (+1.2%) is the SAME top-heavy IMF as Route D's
   remnants — it is DROPPED, subsumed into the single IGIMF EXTRA mass (boost-1)*M_star_canon (stars+remnants).
   The IGIMF mass is counted ONCE.
2. **Gas- and galaxy-tracking are MUTUALLY EXCLUSIVE** shape readings (FPS vs Bullet) — never summed; reported
   as two scenarios.
3. **Route B's boost is on the bare phantom** (+20% of P), not +20% of the target — added as (mult-1)*phantom.
4. **Warm-hot baryons are >R500** (AGN-expelled; can't lower core g_bar) — carried only as a thin optimistic
   ceiling, not load-bearing; the headline holds without it (~71% galaxy-track without warm-hot).
5. **a0 surcharge applied:** framework 9.36e-11 vs Kroupa 1.2e-10 makes the deep-MOND target x1.282 harder;
   the IGIMF reach is divided by this. (So Kroupa's 88%-at-R200 is OPTIMISTIC for the framework.)
6. **IGIMF arm sits inside the banked skeptic ceiling** (skeptic_shape_bothways.py: 40-65% of the shortfall):
   our realistic-geometry galaxy arm = 54% of the bare gap; absolute ceiling 65% -> total 85%.

## BEST-CASE bracket (galaxy-tracking, ROUTEA)
- realistic enclosed-fraction geometry (f_use=0.49, IGIMF=54% of gap): **76%** coverage, residual 32% of gap.
- absolute banked ceiling (IGIMF=65% of gap): **85%** coverage, residual 21% of gap — but this double-leans on
  the two weakest pieces (IGIMF at its ceiling AND the >R500 warm-hot baryons).
- Honest headline: **~76-80%** (defensible), **85% absolute ceiling**.

## VERDICT (both ways)
- **CREDIT at full weight:** with the contested shape going galaxy-tracking (Bullet/Famaey 2605.10022, residual
  "centred on the galaxies", "mostly collisionless"), the framework's OWN field (Route B +20%) PLUS real
  stellar remnants (IGIMF, no new species) PLUS the MI phantom cover ~3/4 of the rich core at ZERO new
  particles. That is materially better than the banked "shared open gap, no no-particle help" and better than a
  flat ~50%.
- **CONCEDE at full weight:** it is NOT a closure. (a) The galaxy-tracking shape is CONTESTED — FPS read the
  same residual gas-tracking (2410.02612, missing-to-gas ~10, exp cutoff), which suppresses remnants to ~50%
  total. (b) Even the galaxy-tracking best leaves ~20-32% of the bare gap (~3e13 Msun) uncovered. (c) The 85%
  ceiling leans on the >R500 warm-hot baryons and IGIMF at its absolute max. (d) On the harder CLASH/eRASS1
  eta-worst anchor the same stack covers only ~50%. The cluster core stays a shared relativistic-MOND open
  soft-spot, now quantified as ~half-to-three-quarters closeable with no new particles depending on one datum.
- **The decisive handle is OBSERVATIONAL, not a calculation:** a resolved, deprojected total-to-baryon profile
  of one rich relaxed core (CLASH + XRISM) settling gas- vs galaxy-tracking. Galaxy-tracking -> ~76-85%
  no-particle; gas-tracking -> ~50% and the core stays the irreducible gap.

Quarantine held: a0/Z/kappa/I0 never asserted derived. No manufactured closure (the residual is conceded at
full weight, the gas-tracking arm and the a0 surcharge are kept), no reflexive dismissal (the galaxy-tracking
~76% is credited at full weight).

## FILES
- `opus_48_extended_research/reviews/cluster_stack/stack_no_new_particle_core.py` — the stack (run reproduces all numbers)
- `opus_48_extended_research/reviews/cluster_stack/CLUSTER_STACK_NO_NEW_PARTICLE_2026-06-20.md` — this verdict

## SOURCES
- Zhang-Zonoozi-Kroupa 2026, arXiv:2602.06082 (PRD 113, 043027) — IGIMF stellar remnants; baryons = 88%(+5+2/-4-1)
  of MOND M_dyn at R200, 46 clusters z<0.1, top-heavy IMF -> NS+stellar-BH remnants dominate the boost.
- Famaey-Pizzuti-Saltas 2024, arXiv:2410.02612 (PRD 111, 123042) — CLASH core target; residual GAS-tracking,
  missing-to-gas ~10, exp cutoff ~430 kpc.
- Famaey 2026, arXiv:2605.10022 — Bullet residual GALAXY-tracking ("centred on the galaxies", mostly
  collisionless), total-to-baryon ~8-9 within 300 kpc, residual 3.4e14 Msun projected (the contested shape).
- Durakovic-Skordis 2023, arXiv:2312.00889 (JCAP 04(2024)040) — AeST cluster isothermal spheres; the +17-20%
  core Y-Q field boost (banked Route B).
- eRASS1: Bulbul+2024, real_research/data/erass1cl_primary_v3.2.fits (on disk).
