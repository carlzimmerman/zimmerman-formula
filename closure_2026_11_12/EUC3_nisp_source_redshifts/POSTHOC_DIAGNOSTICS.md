# EUC3 POST HOC DIAGNOSTICS (disclosed; no repair, no new word)

2026-11-12. Written after the first pass of the frozen run (sample S, the truth lenses and the grade-X null; outputs
`euc3_interim.*`, commit 5a5d3feeca) and before the complete run. Committed with `euc3_posthoc.py` before that script
has produced any output. The frozen criteria (bf72d787a8) are not edited.

## What was seen

- Instrument checks K1–K5 pass. 37 % of S and 36 % of X are evaluable.
- **H2 fails at both tiers.** T5: 12 grade-X systems pass the rule against a limit of 2.9 (1.28 % of evaluable X; S:
  35 systems, 1.53 %). T8: 7 against 1.8. By the frozen ladder the search is NOT EVALUABLE.
- H4 passes with 0 of 3 recovered. EUCL-DR1-L015763: the lens object's rank-0 solution is z = 2.1144 (probability
  1.000, the line taken as [O III]); the Hα reading of the same line is at rank 1, z = 1.3768, against DESI's 1.3657.
  L012826 and L014688 have no object in the wide-survey MER table.
- The void reading printed for sample P (N = 18): median b +0.251 [+0.079, +0.421] canonical, +0.236 [+0.063, +0.403]
  alt. These numbers were seen. They are not used.
- Several grade-X hits show Hα with [S II]: real emission-line galaxies above their photo-z interval, not noise.

## Why diagnostics and not an amendment

The frozen word stands. The task forbids loosening the rule to make a sample, and nothing seen suggests a tightening
that the catalogue could support: the null hits are bright (S/N up to 21) and several have two lines. What is owed is
a check that the failure is real and not a product of how the null was built. H2 can fail wrongly in one way: grade-X
systems are a different population (fainter, more often star-forming, slightly higher photo-z), so they may carry more
objects that are themselves in the window with a low photo-z.

## What `euc3_posthoc.py` computes (all labelled POST HOC; none can produce a verdict)

On the complete run's per-system table (`euc3_systems.csv`; S and all grade A/B against X):

1. The S and X rates with the Hα S/N threshold at 5, 8, 12 and 20, everything else as frozen.
2. The T5 rates split by: top of the deflector interval z_up below / above 0.60; lens-object H flux above / below S's
   median; hit on the lens object / on a neighbour; hits with a second line only.
3. X reweighted to S's joint distribution in (H-flux tercile × z_up tercile): the matched null rate and the H2 limit it
   implies.
4. The excess rate S − X and all A/B − X with a 95 % interval (normal approximation), and the number of real sources
   in P that interval allows.
5. The margin z_s − z_up of the hits, S against X.
6. EUCL-DR1-L015763 only: b at its rank-1 redshift, beside EUC2's value at the DESI redshift. One lens, not a rule.

κ = ½ FITTED. No outcome favours the framework.
