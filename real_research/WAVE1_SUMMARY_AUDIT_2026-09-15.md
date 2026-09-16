# AUDIT — WAVE 1 (2026-09-15)

Adversarial pass over the 2026-09-15 "wave 1" batch (G070–G092, H033–H035,
GRAVITY_EVERYWHERE, LAW_VERIFIED, KEPLER_GRADE_10) run BEFORE the batch's
uncommitted lanes were committed. Both footings throughout
(canonical a0 = 9.3619e-11, alt 1.1279e-10).

Method note: every item below is either (a) reproduced by running the artifact
in this repo, or (b) a quote of one committed artifact against another. Nothing
here is asserted from memory.

---

## WORK ORDER — what another agent should pick up

Each item is a concrete edit or a concrete run. Nothing here needs new physics;
it is all bringing three summary documents back to what their own gates say.

**W1. `deepseek_push/GRAVITY_EVERYWHERE.md` §1.3 — add the circularity label.**
The line `Omega_Lambda = 32 pi a0^2/(3 H0^2 c^2) = 0.6857 (+0.07% of Planck
0.6847)` must carry the L258 A1/A2 finding inline: a0 is built from Planck
inputs, so the +0.07% is two roundings, not a prediction. Copy the wording
G079 already uses. Same section: mark `a0 = Lambda^2/(2 M_Pl)` as NOTATION
(L260), not a derivation. Do NOT touch §4's open list — it is correct.

**W2. `hy4_push/KEPLER_GRADE_10.md` — rewrite the subtitle and add priority
citations.** The subtitle "made by no other framework" is true for P8 and P9
only. Suggested replacement: "Quantitative and falsifiable; two of ten (P8, P9)
are distinctive to this framework, and P9 is untested." Then, per prediction:
cite Milgrom 2009 at P1 (the surface-density prediction Donato+2009 measured);
mark P2/P3/P4 as DEFINITIONAL consequences of r_M := sqrt(G M_b/a0) rather than
as predictions; cite the deep-MOND BTFR at P6; state at P7 that mu_2 is
data-selected; state at P10 that c_T = c and no-hair are shared with GR and
LCDM. At P5, keep the distinction from Milgrom's isothermal 4/9 but say
plainly that the coefficient is the FITTED kappa = 1/2 (k01-k03: provably
underivable by the candidate action to date). P11 needs no change.

**W3. `deepseek_push/LAW_VERIFIED.md` — fix the lensing row and the count.**
Change "KiDS/Brouwer + DES-Y3 data vector" to what G073 actually used
(KiDS-1000 Brouwer+2021, cross-checked against the repo's own KiDS-DR4
re-stack — the SAME survey). Then re-count: with the lensing lane on one
survey, "8 independent instruments" needs restating. Also: the closing
paragraph's "never-before-tested observables" list should drop the universal
surface density (Milgrom 2009 / Donato 2009) and keep the ones that are
actually new (the dSph floor at this coefficient, the funnel, the GC boundary).

**W4. `deepseek_push/G081_equilibrium_stability.py` — two numerical bugs.**
(a) `fixed_well_probe_Omega1_2` returns NaN; the contrast probe never runs.
(b) The second zero mode (xi = r^2) integrates to residual 2.0 against the
lane's own 1e-4 budget on (0, r_break]; re-run on a grid that resolves it, or
state why it cannot be. Until both are fixed, the marginal-stability conclusion
in the JSON's `formation` field is not established and the gate stays OPEN.
This is the gate GRAVITY_EVERYWHERE.md §4 item 2 names as deciding whether the
equipartition temperature is dynamics or ansatz — it is the highest-value
unfinished item in the batch.

**W5. `glm53_push/G062_mw_test.py` — broken instrument, fix or retire.**
Thread a0 through the alt arm (`curves["canonical"] == curves["alt"]` is
currently exactly True); find the MSUN/KPC conversion dropped in the
enclosed-mass and disc-force paths (V0d ratio 9.0e19, V0c ratio 9.7e19); then
re-derive V0b, whose 3.2% miss against the closed form may be real or may be
the same slip. Until then G072 is the MW instrument and G062 is not a verdict.

**W6. One a0 for the whole tree.** The registered canonical footing is
9.3619e-11. KEPLER_GRADE_10 uses 9.3624e-11; G062 computes 9.362307e-11 beside
an `a0_registered` of 9.3619e-11. Harmless to every verdict, worth unifying.

**W7. An open question, not an edit.** KEPLER_GRADE_10 P9 predicts the phantom
share falls to 1.6% by z = 3. G080 measures the BTFR z-trend as DEAD FLAT
(weighted slope -0.032 +/- 0.077 dex/z). Does the P9 mechanism leave G080's
flat trend intact, or does a falling phantom share move the zero point too?
Not checked here. If they conflict, one of them is wrong.

---

## A. WHAT VERIFIES (checked, not asserted)

**A1. The Lean certificates compile, for real.** Recompiled from a clean
`lake env lean` against the repo's own Mathlib
(`fable_independent_2026/lean_2026`, leanprover/lean4 v4.34.0-rc2):

    deepseek_push/lean/G090_equivalence.lean    -> exit 0
    deepseek_push/lean/G083_surface_density.lean -> exit 0

`#print axioms` on all ten theorems returns
`[propext, Classical.choice, Quot.sound]` — **no `sorryAx`**. The commit
messages for 74de498c9 and 6036c69a5 are accurate as written. (Two linter
warnings in G090 at line 60: an unreachable/unused `ring`. Cosmetic.)

**A2. The commit messages carry their own FAILs.** G070 (V2 FAIL, UFD slope),
G073 (V2 FAIL on the point estimate), G075 (V1/V2 FAIL, 6/11), G080 (V2 FAIL)
all put the failure in the subject line rather than the footnotes. That is the
standing working rule being followed.

**A3. G079 is the most honest document in the batch.** It states in print that
the free dust is ~99% of Omega_dm and "functionally CDM — THE THEORY'S HONEST
OVERLAP WITH LCDM", and it explicitly EXCLUDES the one-constant closure:
"Omega_Lambda from a0: circular — L258 A1/A2". See A4.

---

## B. THE FINDINGS

**B1. GRAVITY_EVERYWHERE.md §1.3 presents a number its own sibling gate calls
circular.** §1.3 prints

    Omega_Lambda = 32 pi a0^2/(3 H0^2 c^2) = 0.6857  (+0.07% of Planck 0.6847)

with no caveat. `grep -i circular deepseek_push/GRAVITY_EVERYWHERE.md` returns
nothing. Meanwhile `deepseek_push/G079_cosmic_budget.out` says of the same
quantity: "EXCLUDED on the committed record: the one-constant 'closure'
(Omega_Lambda from a0: circular — L258 A1/A2, G03C)". PAPER29 v2/v3 carry the
same finding as §8: a0 is built from Planck inputs, so the +0.07% is two
roundings, not a prediction. **The §1.3 presentation must not be cited.**
Same section: `a0 = Lambda^2/(2 M_Pl)` is NOTATION (L260) — a definition
equalling itself — not a derivation.

**B2. KEPLER_GRADE_10.md's subtitle is false for most of its own list.**
The subtitle is "Quantitative, falsifiable, and made by no other framework".
Against that bar:

| # | Claim | Status |
|---|---|---|
| P1 | Sigma_ph = a0/(pi G) | **Not novel.** This is the standard MOND central-surface-density result (Milgrom 2009); the document cites Donato+2009's measurement of it without citing the MOND prediction it was made against. Neither KEPLER_GRADE_10, LAW_VERIFIED nor GRAVITY_EVERYWHERE contains the string "Milgrom". |
| P2 | g(r_M) = a0 exactly | **Definitional.** r_M := sqrt(G M_b/a0) is the radius at which g = a0. It cannot come out otherwise. |
| P3 | M_ph(r_M)/M_b = 1.000000 | **Definitional**, given the linear law plus P2's definition. This is L260's "definitions equalling themselves" category. |
| P4 | r_M = sqrt(G M_b/a0) | **A definition**, tabulated. |
| P6 | BTFR A = 1/(G a0) | **Not novel** — the canonical deep-MOND BTFR zero point. |
| P7 | the RAR shape from mu_2 | mu_2 is the DATA-SELECTED kernel (it is ~nu_RAR); the shape is fitted, not predicted. 0.150 dex is AT the SPARC benchmark scatter, which is also where MOND sits. |
| P10 | c_T = c, no BH hair | Shared with GR, LCDM and most healthy scalar-tensor theories. Not discriminating. |
| P5 | sigma/v_c = 1/sqrt(2) | **Partly distinctive** — Milgrom's MOND isothermal sphere gives sigma^4 = (4/9) G M a0, this gives (1/4). But the coefficient is kappa = 1/2, which is FITTED and provably underivable by the candidate action (kappa_closure k01–k03). It is a fitted coefficient, not a prediction. |
| P8 | r_cap = (a0/g_ext) r_M | **Genuinely distinctive** (the L242 EFE break-radius law). This is the real one. |
| P9 | RAR weakens with z | **Distinctive but NOT ESTABLISHED** — the document says so itself. Flagged for an internal-consistency check: if the phantom share falls to 1.6% by z=3, does that leave G080's measured DEAD-FLAT BTFR z-trend intact? Unresolved here. |

P11 (the 22% a0 gap) is carried honestly and is the document's best page.

**Correct subtitle: two of ten are distinctive to this framework (P8, P9), and
P9 is untested.** The rest are deep-MOND results, definitions, or GR.

**B3. LAW_VERIFIED.md mislabels the lensing lane's data.** The scoreboard row
reads "KiDS/Brouwer + **DES-Y3 data vector**", supporting the headline
"8 independent instruments". G073's own output says the opposite:
"NO public DES Y3 or HSC galaxy-galaxy lensing RAR exists" — the cross-check
was the repo's own KiDS-DR4 re-stack, i.e. **the same survey**, which G073
labels honestly ("same survey, NOT DES/HSC") and LAW_VERIFIED does not.

**B4. LAW_VERIFIED.md cited a budget that was not yet in the tree — since
partly resolved, in the right direction.** The closing paragraph's
">= 90% of Omega_dm, the honest budget" came from G079, which at the time of
commit 25117c3ee was untracked. The version of G079 audited that afternoon was
6/9 with a closure ratio of 0.31-0.51 against a required [0.8, 1.2] (G5 FAIL).
G079 was then re-run and committed (04bc65bd7) at **9/9**, closure ratio
0.79-0.95 — now in band, and the dust share (98.7-99.2%) is unchanged and
solid. The residual caveat is real and is G079's own: `cluster_budget` still
carries `"UNVERIFIED": true`, because the mass function is computed here from
literature FORMULAS (EH98 transfer + Tinker+08), not from published abundance
MEASUREMENTS. The 0.79-0.95 is a pipeline agreeing with the pipeline it was
built from. G079 says exactly this; summaries quoting it should too.

**B5. Two Milky Way lanes in this repo disagree and both are in the tree.**
G072 reports 5/5 PASS. G062 (glm53_push, committed here explicitly labelled)
reports 6/21 with hard unit slips: enclosed mass at 30 kpc off by a factor
9.0e19, the disc/sphere force ratio printed as 9.7e19, curve values ~1e12 in
a field labelled km/s, and — decisively — `curves["canonical"] ==
curves["alt"]` is **True**, i.e. the alt-footing arm never switched a0.
**G062 is a broken instrument, not an honest FAIL. Do not cite it.**

**B6. G081's stability conclusion outruns its own checks.** The JSON's
`formation` field states "THE CAPPED ISOTHERMAL PHANTOM IS A CRITICAL
(marginally stable) EQUILIBRIUM ... no exponentially growing mode". The two
checks that would establish it both FAIL on the script's own budgets: V2's
second zero mode has grid residual 2.0 against a declared budget of 1e-4, and
V3's cap-BC subfamilies carry ODE residuals 7.6e-1 and 1.0. The contrast probe
returns `fixed_well_probe_Omega1_2: NaN` — an outright bug. The analytic
identity (xi = r u => u'' = (w/sigma)^2 u) is exact and the eta = 1/2 landing
is exact; the NUMERICAL confirmation is not there yet.
**The G081 relaxation/stability gate stays OPEN** — which is, correctly, how
GRAVITY_EVERYWHERE.md §4 item 2 still lists it.

**B7. a0 drifts in the fourth digit across the batch.** The registered
canonical footing is 9.3619e-11. KEPLER_GRADE_10 uses 9.3624e-11; G062's
constants block computes 9.362307e-11 against a `a0_registered` of 9.3619e-11.
~0.005% — harmless to every verdict, but it means "the certified a0" is not one
number in the tree.

---

## C. WHAT THIS DOES AND DOES NOT CHANGE

Unchanged: the empirical lanes (G070–G078, G080, G092) and their verdicts,
including their FAILs. The Lean certificates. The open list in
GRAVITY_EVERYWHERE.md §4, which is accurate.

Changed: the three SUMMARY documents (GRAVITY_EVERYWHERE §1.3,
LAW_VERIFIED's table + closing paragraph, KEPLER_GRADE_10's subtitle) overstate
novelty and closure relative to the gates they summarise. The gates are more
honest than the summaries built on them. That is the failure mode this
programme has hit before (L258, H029) and it recurred here.

The batch's real content, stated at the bar the programme holds itself to:
a zero-parameter deep-MOND-equivalent mass law, tested on eight datasets at
0.03–0.22 dex, with its domain boundaries (GC crossing, UFD faint end, cluster
amplitude) located and published as failures; two genuinely distinctive
predictions (P8 the EFE break radius, P9 the z-weakening, untested); a fitted
kappa = 1/2; a cluster amplitude that is an input; a relaxation gate that is
open; and a cosmological "closure" that is circular and must be retired from
every summary that still carries it.

*No claim in this file is new physics. Every one is a comparison between two
artifacts already in this repository, or a compile run recorded in §A1.*

---

## D. AUDIT CONDITIONS

This audit was run while the deepseek autoloop was live and committing to the
same branch; G079, G086 and G092 landed mid-audit. G079's numbers in §B4 are
quoted from the COMMITTED version (04bc65bd7, 9/9), with the superseded
afternoon draft noted. G085, G087 and Q007 appeared after this pass and are
NOT audited here.
