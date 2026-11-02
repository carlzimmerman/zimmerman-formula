# BF3_all_gates_first: FROZEN CRITERIA (committed alone, before any BF3 script or number)

Owner's standing go for search lanes, 2026-11-02. **Question:** in a dimension-pruned grammar over forced constants, does ANY closed form H pass discs, clusters, galaxy lensing, groups and stars-only systems together?

**Not blind.** Read before this: BF1's criteria and script, BF2's README, criteria, amendment, `bf2_common.py`, `bf2_scan.py`, `bf2_supp*.py`, RQ3's `acceptance.py` and `tolerances.json`, CRG1's `crg1_lens.py`, `crg1_groups.py`, `crg1_sparc.py`, the law's RQ3 row values. The failures that motivate these gates were seen; BF2's forms and their numbers are known. No BF3 number exists yet. The gates below were chosen knowing how P3, P7, P8 and the law fail. A description at best: no action, no field equation, no fitted float. kappa = 1/2 FITTED. Footings canonical 9.3603e-11 and alt 1.1312e-10 reported apart, never pooled. No LCDM input is added here; **disclosed inheritance:** A30's two-halo template in CRG1 and RQ3 carries fixed background numbers (h 0.6736, 0.02237 + 0.1200) and a P_grav file. I don't change the row, its amplitude b >= 0 is free per bin, and for anything reaching the end I report chi^2 with b = 0 as well. No cold component, no particle; the cold sector stays retired and nothing here reinstates it. Not theory closed. Nothing here says the data favour the framework. PAPER67, ledger, outside summary untouched. BF1, BF2, BK2, SR3 jobs and files untouched; read-only use of their files and of RQ3, CRG1.

## Search space
Leaves per row, from baryons only: y = g_b/a0, ell = r a0/c^2, f = gas share of enclosed baryons clipped to [0, 1]. Constants 1, 2, 1/2, pi. Unary sqrt, log1p, inv1p, square. Binary + - * /. No other float. Closure as BF1: level 2 pool by value dedupe, ranked by nodes then lexical. Evaluation points for the dedupe are this lane's own rows.

Wrappers as BF1, with law(g, a) = g/2 + sqrt(g^2/4 + a g): W1 law(g_b, a0 H); W2 law(g_b H, a0); W3 law(g_b, a0) H.

Families:
- **A, protected by construction:** H = 1 + f T. T is every pool member and every a op b on pool pairs. Any H smooth at f = 0 with H(0) = 1 has this form.
- **B, BF1's own grammar filtered:** H = a op b on pool pairs, keeping H(f=0) = 1 numerically (gate 0).
- **C:** BF1's L4 hits as a frozen snapshot of `chunks/real_L4/hits.jsonl` at scan time, line count and SHA-256 recorded, gate 0 applied.
- **E, extended, wall budget:** Family A with the pool extended by level 3 members, ranked by nodes, cap 80,000, canonical only, jobs in rank order, stopped at 3 hours of wall time; coverage reported as found. A cap is a real limit.
Families A, B, C run on both footings, each searched on its own. Family E canonical only.

## Stage 1, gates, in this order, all lines set now
AND is order free, so **execution** may run X-COP first to save compute: the survivor set is unchanged. The funnel in the order below is measured on a deterministic 0.1 % sample of chunks where every gate runs, S included.

**Gate 0, stars-only.** |H(f=0) - 1| <= 1e-12 at y from 1e-5 to 1e7, ell 1e-12, 1e-6, 1e-2. At f = 0, then, Saturn reads the law exactly. **The law itself fails unscreened Cassini (PAPER58, RQ3 C1), so this gate is "the law's standing", not a pass of Cassini.** The Sun is gas physically and f = 0 is a labelling choice; f = 1 at Saturn is reported for anything that reaches the end.

**Gate L, galaxy lensing, RQ3's A30 path with two tiers.** Chi^2 of the KiDS stack, four mass bins, 60 points, two-halo amplitude b >= 0 per bin, covariance plus a systematic C_sys = s^2 Y Y^T on the data vector Y, s = 0.125, fully correlated. s is the quadrature of 0.05 dex in amplitude from 0.10 dex of stellar-mass systematic, same 0.10 dex as RQ3's groups row, with amplitude ~ M^(1/2) in the low-acceleration regime, and about 2 % each for shear calibration and redshift. **These three inputs are PROVISIONAL, mine, from memory of the literature, not measured here.** Gas in the lens model is not varied; its scaling x 0.5 and x 0.25 is reported beside for forms reaching the end. Lines, dof 56 as RQ3, |Z| <= 2:
- **L-abs:** chi^2_sys <= 56 + 2 sqrt(112) = 77.2.
- **L-law:** chi^2_sys <= the law's chi^2_sys on the same footing + 21.2. Separate label, because the law may fail L-abs.
RQ3's cov-only chi^2 is reported beside.

**Gate G, groups, RQ3's B1 path,** 63 groups, mean offset, stat plus 0.10 dex mass systematic, |Z| <= 2. lM there is baryonic. No gas on file, so f is assumed: **must pass at f = 0.3 and at f = 0.6.** f = 0.85 reported, not gated: the dispersions weigh radii near Re, where I expect enclosed gas share below the outer value, an assumption of mine. f = 0 would pass trivially and isn't used.

**Gate S, SPARC, FG1's free-Upsilon statistic through CRG1's arithmetic.** rms <= 0.110, median Upsilon in 0.50-0.80. f recomputed at each Upsilon. Tilt, gas-rich tercile rms and rms over the law's 0.054 reported, not gated. BF2 showed this line is generous: stated beside any pass.

**Gate X, X-COP all 7, rows x = 0.1-0.7, RQ3's B23 path.** |mean log10(M_HSE/M_model)| / sqrt(stat^2 + 0.12^2) <= 2, where stat is the scatter of cluster means over sqrt 7 and 0.12 dex is RQ3's hydrostatic term, and scatter of rows about their own mean <= 0.10. **X-strict**, BF1's line, |mean| <= 0.05 and rms <= 0.10, counted beside as a tighter tier.

Cheap paths may stand in for L and G as a prefilter: linear maps on coarse nodes with b unconstrained (a lower bound), and tolerance slack checked in K. Precut before any near-miss bookkeeping: H finite, positive on X-COP, |mean| <= 0.30, scatter <= 0.15. Every Stage 1 pass and every reported near miss is re-graded on RQ3's exact path. Only exact numbers are reported as gate values.

## Stage 2, holdouts, on survivors
Through RQ3's `acceptance.py` read-only, via BF2's loader pattern, lines unmoved, |Z| <= 2: 15 keys (at least 14 pass, as BF2's label), A23a TDG, A9 LITTLE THINGS, A10 IC 1613, A15, A16 Milky Way at assumed f 0.05 and 0.15 as BF2 (no gas on file; reported beside), A18 DiskMass. Ranked by largest gate score, nodes, lexical; at most 6 forms. If there are no survivors, the 4 best near misses by the score below go through, labelled near misses.

**Bullet, B28 and UX6's local reading:** reported. **Expected kill, stated now: any local present-gas form, since UX6, MG1 and BF2 show the boost follows gas share so the peak sits on the gas.** It doesn't count against the search's Stage 1 verdict and it is said in the verdict line.

## Near misses
Score of a form on a set of gates: the largest of |Z|/2 or value/line across them. For each combination of L-abs, L-law, G, S, X, the single best form, labelled NEAR MISS with the gates it fails named. Combinations with X use the forms past the precut, top 300 per cheap combination carried to S, so **S combinations are best of that shortlist, a limit**. Combinations without X come from the 0.1 % sample. Law reported on the same table.

## Labels
- **JOINT FORM, ABSOLUTE:** gate 0, L-abs, G, S, X on both footings.
- **JOINT FORM, LAW'S LENSING:** same with L-law. Says it's as good as the law on lensing, not that lensing passes.
- **Footing-only** variants are said as such.
- **HOLDS HOLDOUTS:** a joint form passing Stage 2. Still not a theory: a second implementation, an action and CMB are owed. The Bullet goes beside it.
- **NO JOINT FORM** within this grammar and these caps: nothing past Stage 1. This says nothing beyond the grammar.

## Controls and look-elsewhere
Same tolerances, control arms with X-COP rows' H leaves (y, ell, f, jointly) permuted across all 35 rows while g_b and M_HSE stay. Arm C1 seed 20261102 on all of families A, B canonical; C2, C3 seeds 1, 2 on 10 % of jobs, frozen by job index. Counts of expressions tried, per-stage passes, joint passes, per arm, in the README. If real joint hits exist and aren't above C1 by a factor of 3 per expression tried, **"NOT ABOVE CONTROL" goes in the title.** Scramble limit: it only breaks X-COP's link; lensing, groups, SPARC stay real, and a form could still be fit by the mean.

## Checks, verify a fail as hard as a win
K1 known answer: H = 1 reproduces RQ3 results for the law: A30 chi^2 154.149 cov-only, B1, A1 0.054, A2 0.52, B23 +0.467, each within 1e-3 absolute on this lane's exact path. K2 BF2's P3, P7 cov-only A30 885, 846 and X-COP on the exact path within rounding. K3 cheap paths against exact on the law, P3, P7 and 50 frozen random pool forms: printed. Cheap L is a lower bound within 3 %, cheap G within 0.01 dex; if not, slack widens, printed, never narrowed. K4 planted: a mock with every target generated from a known H inside Family A, all gates at their lines, must return that form as a joint form with chi^2 near zero. K5 precut loses nothing: on the 0.1 % sample, no expression passing all exact gates fails the precut.
**MUTATE twin, must fail, separate outputs:** H x 1.5 in the evaluator (K1, K2 break) and gate lines at 1e-6 on the planted mock (nothing recovered). Exit 1. **Rerun byte-identical** on a frozen subset of jobs, same results shards.

## Expectation, mine, on record
Stage 1 JOINT FORM, ABSOLUTE on a footing: 3 %. On both: 2 %. LAW'S LENSING on both: 8 %. Law passes L-abs under the added systematic: 25 %. Family A reaches X and S jointly on both: 60 %, much of it through a term in ell. If a joint form appears, holds all holdouts: 10 %. Bullet is DEAD on local f for anything reaching the end: 90 %. Real above control by 3 if anything hits: 50 %.

## Compute
nice 19, at most 4 workers, private memory under 1 GB per process where possible, SIGTERM checkpoints, rerun resumes. Lane directory only; commit by explicit path; no push.
