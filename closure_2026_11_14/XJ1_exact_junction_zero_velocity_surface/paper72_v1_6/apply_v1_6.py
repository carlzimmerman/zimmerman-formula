#!/usr/bin/env python3
"""Apply the version 1.6 edits to PAPER72's TeX source and to its audit script, in place.

Version 1.6 folds in what landed after version 1.5 was deposited (DOI 10.5281/zenodo.24231666): the blind lane XJ1R,
XJ1's second build, BJ1's flux-level run, WLJ2, GAS2, ABS1, DBL1, and the lanes behind CJ1's scorecard updates twelve
to sixteen (EUC17R, EUC18, EUC20, EUC20R, EUC21, EUC21R, OTA1, RRL2, RRL3R, WLG1, WLG1R), with the scorecard's new counts.

Every edit is anchored on an exact string of the version 1.5 source; if an anchor is missing or not unique nothing is
written. The script refuses to run on a source that is already version 1.6. It computes no number: every number in
the inserted text is quoted from a committed lane file, and the audit entries added here check each one.

Run from anywhere inside the repository:  python3 apply_v1_6.py
kappa = 1/2 FITTED; not theory closed. Adopts nothing.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
PAP = os.path.join(ROOT, "qwen_claude_field_theory", "papers_2026")
TEXP = os.path.join(PAP, "PAPER72_law_with_cold_dark_energy_counted_once_2026.tex")
AUDP = os.path.join(PAP, "PAPER72_audit.py")
tex = open(TEXP, encoding="utf-8").read()
aud = open(AUDP, encoding="utf-8").read()
if "Working note (PAPER72), version 1.6" in tex:
    sys.exit("source is already version 1.6; nothing done")


def once(text, anchor, new, what):
    n = text.count(anchor)
    if n != 1:
        sys.exit(f"ANCHOR ({what}) found {n} times; nothing written")
    return text.replace(anchor, new)


def after(text, anchor, add, what):
    return once(text, anchor, anchor + add, what)


def before(text, anchor, add, what):
    return once(text, anchor, add + anchor, what)


# ------------------------------------------------------------------ TeX
tex = once(tex, "% PAPER72 v1.5 (2026-11-14; v1.4 2026-11-14, deposited 2026-11-14 UTC;",
           "% PAPER72 v1.6 (2026-11-15; v1.5 2026-11-14, deposited 2026-11-14 UTC; v1.4 2026-11-14, deposited 2026-11-14 UTC;", "comment line")
tex = once(tex, "Working note (PAPER72), version 1.5, 2026-11-14 (v1.4: DOI 10.5281/zenodo.24221457;",
           "Working note (PAPER72), version 1.6, 2026-11-15 (v1.5: DOI 10.5281/zenodo.24231666; v1.4: DOI 10.5281/zenodo.24221457;", "version line")

# the "what changed" paragraph for 1.5 takes the place of the one for 1.4, which moves below the abstract
lines = tex.split("\n")
i14 = [i for i, l in enumerate(lines) if l.startswith(r"\paragraph{What changed since version 1.4.}")]
i13 = [i for i, l in enumerate(lines) if l.startswith(r"\paragraph{What changed since version 1.3.}")]
if len(i14) != 1 or len(i13) != 1 or i14[0] > i13[0]:
    sys.exit("ANCHOR (what-changed paragraphs) not as expected; nothing written")
old14 = lines[i14[0]]
CHANGED = r"""\paragraph{What changed since version 1.5.} Version 1.5 (DOI 10.5281/zenodo.24231666) is unchanged in every sentence that is still true; version 1.6 adds Section~12 and dated additions marked ``Version 1.6'' in Sections~6, 9 and 11. Four results landed after it. A blind build confirms, as labels on both footings, the two post hoc holds of Section~11.3: the law placed unscaled inside the second or the third caustic holds the forest row, FRAGILE in that build to half the gas smoothing scale. A second, independently written build reproduces the junction finding of Section~11.2. The layout that conserves charge by construction FAILS the forest row at flux level on both footings. And with the law unscaled inside, the weak-lensing-amplitude row reads a fail, with the tension slightly worse, as for the adopted form. The counts of Section~9.2 are CJ1's after its sixteenth update: on the owner's decisions rows 35 and 28 moved from FAILS to NO POWER and to DEPENDS ON AN UNTESTED ASSUMPTION, and neither is a pass. Historical lane labels are preserved; no label of an earlier lane changes. The candidate is NOT ADOPTED."""
lines[i14[0]] = CHANGED
lines[i13[0]:i13[0]] = [old14, ""]
tex = "\n".join(lines)

ABSTRACT = r"""Version 1.6 adds the lanes that landed after version 1.5 (Section~12). A blind build, with its own caustic computation and its own junction code and without sight of the first lane's numbers, grades the law placed unscaled inside the second and the third caustic: both hold the forest row at flux level on both footings (1.55/1.66 and 0.76/1.14 against the line of 4), and no rotation curve reaches beyond either. It is the first hit of the candidate sixth rule that a blind build has confirmed as a label. In that build both holds are FRAGILE to half the gas smoothing scale, a value that lies outside the measurements at two of the three redshifts checked and that neither build resolves. A second build of the exact junction agrees with the first at half a fold radius on both footings and at two fold radii on alt; on canonical at two fold radii it agrees in size and cannot resolve the word. The confirmation changes none of what counts against these holds: the caustic was chosen by looking, the layout is a drawn profile that the clock's own flow does not assemble, and the layout that conserves charge by construction now FAILS the forest row at flux level on both footings (12.7/14.8 against 4, with no bracket under the line). Read with the law unscaled inside, the matter-power row holds on canonical and is not resolved on alt, and the weak-lensing-amplitude row fails at every radius graded, the tension made slightly worse and not relieved. A check of the forest gate itself finds that its reference model does not fit the DESI points in absolute terms, so a label that is not a hold and sits near the line depends on a step no lane had tested; the holds and the clear fails do not. On the owner's decisions two rows of form B no longer read as fails: the ultra-faint dwarfs and M31's bright dwarfs have no power under the blind systematics budget, and the Milky Way's halo stars at 40 to 55\,kpc depend on the anisotropy convention, each reading backed by a blind build. Neither is a pass. Two rows still fail: the outer cluster shear and the four low dwarf rows.
"""
tex = once(tex, "its flux-level run had not been made.\nWe list what is open,",
           "its flux-level run had not been made.\n" + ABSTRACT + "We list what is open,", "abstract")

ITEM6 = r"""
\item Version 1.6, for the caustic junction (Section~12): a forest model that sets the gas smoothing scale and resolves half of it, since the two builds that hold disagree only there; the gate's reference model fitted to the data in absolute terms, or a gate that does not need that step (ABS1); a flow of the action that delivers the law's charge inside the caustic, or a proof that none does; the rows not yet re-graded for the unscaled junction (the resolved discs at $z\approx2$, groups, the Milky Way's enclosed-mass profile and the dwarfs); and, for row 25, the owner's decision on its word under that junction."""
tex = after(tex, "with the conserved current's interface condition met.", ITEM6, "Section 6 item")

tex = after(tex, "is placed DEPENDS ON AN UNTESTED ASSUMPTION and no longer FAILS.",
            " Version 1.6: the table gives the counts after CJ1's sixteenth update (Section~12.6): rows 35 and 28 are placed NO POWER and DEPENDS ON AN UNTESTED ASSUMPTION and no longer FAILS, each on the owner's decision of 2026-11-14.", "9.2 intro")
tex = once(tex, "\nNO POWER & 7 & 7\\\\", "\nNO POWER & 8 & 8\\\\", "count NO POWER")
tex = once(tex, "\nFAILS & 4 & 4\\\\", "\nFAILS & 2 & 2\\\\", "count FAILS")
tex = once(tex, "\nDEPENDS ON AN UNTESTED ASSUMPTION & 5 & 5\\\\", "\nDEPENDS ON AN UNTESTED ASSUMPTION & 6 & 6\\\\", "count DEPENDS")
tex = after(tex, "Version 1.5: X-COP's two-sided amount is no longer among them (row 15, Section~11.5).",
            " Version 1.6: the halo stars, and the ultra-faints with M31's bright dwarfs, are no longer among them either (rows 28 and 35, Section~12.6); the outer cluster shear and DF2, DF4, NGC\\,147 and IC\\,1613 remain.", "9.2 fails bullet")
tex = after(tex, "CJ1 keeps row 22's word by the rule it already used in row 11 and marks it unconfirmed.",
            " Version 1.6: this still holds for the completed form of this section, whose junction rescales the law's halo. The blind XJ1R confirms as labels two holds of a different layout, the law unscaled inside a caustic (Section~12.1).", "9.2 no confirmed hit")
tex = after(tex, "its forest run had not started.", " Version 1.6: both have landed (Sections~12.1 and 12.2).", "11.3 running")
tex = after(tex, "so its three words are NOT RESOLVED on both footings.",
            " Version 1.6: the run has been made and FAILS on both footings (Section~12.3).", "11.4 BJ1 bullet")
tex = after(tex, "BJ1 keeps the first two and is far over the forest gate at matter level, its flux-level run pending.",
            " Version 1.6: at flux level it FAILS on both footings (Section~12.3).", "11.4 triangle")
tex = after(tex, "while $\\gamma$ 1.2 and 1.6 are inside them.",
            " Version 1.6: GAS2 has since read those tables from the papers' pages by eye (Section~12.5).", "11.5 GAS1")
tex = once(tex, "and the counts of Section~9.2 are CJ1's after that update.",
           "and the counts of Section~9.2 were, at version 1.5, CJ1's after that update.", "11.5 counts")
tex = after(tex, "no word for the completed form and no count changed.",
            " Version 1.6: three later updates changed two words and the counts (Section~12.6).", "11.5 later updates")

SEC12 = r"""\section{Version 1.6: the blind build of the caustic junction, a second build, charge conservation at flux level, and the rows since version 1.5}
The lanes in this section landed on 2026-11-14, after version 1.5 was deposited (DOI 10.5281/zenodo.24231666). Each froze its criteria in a commit before any graded number; frozen readings come first and post hoc readings are labelled. This section changes no lane's label.

\subsection{The blind build: the law inside the second and the third caustic holds the forest row, FRAGILE}
XJ1R was built from a brief that states the candidate of Section~11.3, its definitions and its gates, and holds no result of XJ1. Its builder, a separate session barred from XJ1's folder, from the scorecard and from this paper, froze its own criteria, wrote its own shell computation and passage count for the caustics and its own exact junction in FWN1's forest build (12 seeds at $z$ 2.2, one seed at five other redshifts), and committed its grader before any forest part existed. When the run ended the lead, who is not blind, ran that grader unchanged.
{\small
\begin{longtable}{@{}p{3.4cm}p{6.0cm}p{6.0cm}@{}}\toprule
Settled radius & canonical: D (SE); label & alt: D (SE); label\\\midrule\endhead
second caustic & 1.553 (0.708); FOREST ROW HOLDS AT FLUX LEVEL, FRAGILE & 1.660 (0.852); FOREST ROW HOLDS AT FLUX LEVEL, FRAGILE\\
third caustic & 0.760 (0.389); FOREST ROW HOLDS AT FLUX LEVEL, FRAGILE & 1.141 (0.595); FOREST ROW HOLDS AT FLUX LEVEL, FRAGILE\\
control: FZS1's junction at $5\,R_{\rm fold}$ & 8.085 (2.414); above the gate & 9.448 (2.790); above the gate\\\bottomrule
\end{longtable}}
\begin{itemize}
\item \textbf{The lane's words on both footings: CAUSTIC 2 HOLDS, BLIND, FRAGILE (lam\_x0.5) and CAUSTIC 3 HOLDS, BLIND, FRAGILE (lam\_x0.5).} With twice the seed error added the numbers are 2.970/3.363 and 1.537/2.331, under the line of 4. XJ1's build read 1.213/1.648 and 0.512/0.691 (Section~11.3). So both post hoc holds are confirmed as labels by a blind build on both footings: the first hit of the candidate sixth rule that a blind build has confirmed as a label.
\item \textbf{Rotation curves.} No SPARC galaxy's last measured point lies beyond either caustic, at a mass-to-light ratio of 0.5, 0.3 or 0.8; the largest ratios are 0.602 and 0.767, as in XJ1.
\item \textbf{Checks.} The control equals FWN1's stored value and stays above the gate. Every known answer passes and both twins bite: with the change doubled the cases read 3.03/4.08 and 3.27/3.51 times higher. The blind build's matter-level numbers, 8.147/19.038 and 2.872/6.369, agree with XJ1's (8.15/19.04 and 2.87/6.37).
\item \textbf{Where the two builds differ.} With half the gas smoothing scale the blind build reads 46.5/60.4 and 33.9/47.5, far over the line, where XJ1's build read 3.955/4.385 and 1.63/2.12. Every other frozen bracket stays under the line in the blind build (the largest are 3.46/3.36 and 1.58/1.57, at $\gamma$ 1.6), and over the measured range of the smoothing scale the cases run from 0.82 to 0.10 / 1.93 to 0.88 and from 0.43 to 0.09 / 1.06 to 0.49. Neither build's grid resolves half the smoothing scale, and GAS2 (Section~12.5) places it inside twice the measurement error at $z$ 2.2 only. The flag stays; what it turns on is a scale that no build here can test.
\item \textbf{What the confirmation does not change.} The statement was found by looking, from a family of two caustics, after other radii had failed. A blind build shows that the layout is not excluded by the forest in a second build; it does not make the choice of caustic less post hoc. A hold means that the layout departs little enough from the reference at $z$ 2.2 to 4.4. It is not evidence for the law inside, and it does not separate the framework from a cold reference. The layout is still a drawn profile (Sections~11.4 and 12.3).
\item \textbf{The builder's disclosures.} It read the control's ``must still fail'' as D above 4, where FWN1's own label for that case is NO VERDICT; it recomputed the control at two seeds for field identity and graded it from FWN1's parts; one test part ran as a fourth heavy process for two minutes; and it saw one commit subject of this paper in the commit list, which carried no number of the caustic cases.
\end{itemize}

\subsection{The second build of the exact junction}
Build A is a second, independently written implementation of the exact junction, in FWN1's forest build, for two of XJ1's cases (its amendment A4). The lead graded it with the builder's committed grader.
{\small
\begin{longtable}{@{}p{2.0cm}p{3.7cm}p{3.7cm}p{3.0cm}p{3.0cm}@{}}\toprule
Settled radius & build A, canonical & build A, alt & first build, canonical & first build, alt\\\midrule\endhead
$0.5\,R_{\rm fold}$ & 0.780 (0.409); HOLDS, FRAGILE & 1.246 (0.670); HOLDS, FRAGILE & 0.583 (0.050); HOLDS & 0.794 (0.059); HOLDS\\
$2\,R_{\rm fold}$ & 16.45 (7.02); NO VERDICT & 22.84 (7.75); FAILS & 16.37 (0.79); FAILS, FRAGILE & 25.73 (1.96); FAILS\\\bottomrule
\end{longtable}}
Read across, reported and not a label: at half a fold radius HOLDS IN BOTH BUILDS on both footings; at two fold radii NOT RESOLVED on canonical and FAILS IN BOTH BUILDS on alt. On canonical at two fold radii the builds agree in size (16.45 and 16.37) and differ in word, because build A's seed error at 12 seeds is nine times the first build's. In build A the hold at half a fold radius is FRAGILE to half the gas smoothing scale (29.9/74.7 there, against 2.04/2.63 in the first build), the same disagreement as in Section~12.1. In build A the exact junction at two fold radii is 84 times FZS1's junction on canonical. Its matter-level numbers, 3.428/7.649 and 134.81/326.91, equal the first build's to four figures. Every known answer of build A passes and both twins bite. So the finding of Section~11.2, that the forest hold at $f=2$ does not survive the law placed unscaled inside, is reproduced by an independent implementation on alt, and in size on canonical. Build A did not run the caustic cases.

\subsection{Charge conserved by construction: FAILS THE FOREST at flux level}
BJ1's flux-level run, which version 1.5 did not have, was made in FWN1R's build (4 seeds in every bin, then the brackets) and graded with the grader committed before the run.
{\small
\begin{longtable}{@{}p{3.4cm}p{6.0cm}p{6.0cm}@{}}\toprule
Capture surface & canonical: D (SE); label & alt: D (SE); label\\\midrule\endhead
first caustic & 12.763 (0.881); FOREST ROW FAILS AT FLUX LEVEL & 14.893 (2.26); FOREST ROW FAILS AT FLUX LEVEL\\
second caustic & 12.725 (0.884); FOREST ROW FAILS AT FLUX LEVEL & 14.829 (2.25); FOREST ROW FAILS AT FLUX LEVEL\\
third caustic & 12.718 (0.886); FOREST ROW FAILS AT FLUX LEVEL & 14.802 (2.25); FOREST ROW FAILS AT FLUX LEVEL\\\bottomrule
\end{longtable}}
\begin{itemize}
\item \textbf{The lane's words on both footings: FAILS THE FOREST (caustic 1), FAILS THE FOREST (caustic 2) and FAILS THE FOREST (caustic 3).} Rotation curves and the lensing gate pass in all six cells, as in Section~11.4, so the forest's is the only failing word.
\item \textbf{No label is FRAGILE.} No frozen bracket brings a case under the line: the lowest, at twice the gas smoothing scale, is 4.28 to 4.29 on canonical and 7.76 to 7.77 on alt, and over the measured range of that scale the cases run from 9.5 to 5.0 and from 12.4 to 8.6.
\item \textbf{The number does not depend on the caustic.} It comes from the heavier haloes, where the law's region grows to the equal-charge radius beyond every caustic.
\item \textbf{Checks.} Every known answer passes and both twins bite; the grader reproduces byte for byte into a separate folder.
\item \textbf{Under the other scale of Section~12.5} (our arithmetic with ABS1's range of factors, not a lane's number) the three cases would read 7.0 to 9.7 on canonical and 8.1 to 11.3 on alt, still over the line.
\end{itemize}
So the reading at the end of Section~11.4 now stands at flux level in this build. No layout graded here meets all three of: the law unscaled out to the last point of every rotation curve, charge conserved at the junction with the reference as the supply, and the forest. The caustic layouts keep the first and the third, now in two builds, one of them blind, and move charge by fiat. BJ1 keeps the first two and fails the third on both footings. That reading is the lead's, not a lane's label. BJ1 is one build and not blind, its gas inputs are provisional, and its delivered charge is the halo model's reference, not a flow of the action.

\subsection{Rows 24 and 25 with the law unscaled inside}
WLJ2 (not blind; no amendment) read every gate that WLJ1 ran for the matter-power and the weak-lensing-amplitude rows with XJ1's exact junction, at the third and the second caustic and at 0.5, 0.75 and 1 fold radii.
\begin{itemize}
\item \textbf{Row 25, the weak-lensing amplitude.} The lane's tension word is that the exact junction WORSENS it, on both footings; by WLJ1's gate rule the row reads ROW FAILS WITH THE EXACT JUNCTION on both footings, as the adopted form does. For the reference, raw KiDS sits 5.409/5.408 of its widths below the pinned amplitude. The exact junction moves it a further 0.04 to 0.35 / 0.10 to 0.54 widths, and the Legacy gap 0.05 to 0.38 / 0.13 to 0.73 widths; on alt the raw-KiDS statistic is reported and not used, because its twin does not bite there. At one fold radius the worsening is marginal: canonical rests on one statistic at $+0.043$ against a floor of 0.02 that the lane itself chose. One failing gate is KL1's DES row, which is above two widths for the pure reference too ($+2.16$/$+2.11$), a fail the layout does not create. Under the rescaled junction that gate had no verdict because its doubled-layout twin did not bite; here the twin bites. So the exact junction brings no relief and a small worsening, not a new tension.
\item \textbf{Row 24, matter power.} ROW HOLDS WITH THE EXACT JUNCTION on canonical, with the raw-KiDS statistic between 0.19 and 2.13 against its line at 4. On alt the word is NOT RESOLVED: the third caustic reaches 4.85, a tension, and the other radii hold. No hold differs from the adopted form's word, so nothing here is a hit.
\item \textbf{A surprise.} At the caustics the layout is not equal to the reference: its matter power at $k$ 3 reads 1.070/1.126 where the adopted form's reads 1.051/1.088. The lane's hand estimate had the direction and the order wrong.
\item \textbf{Limits.} These gates read $z=0$, where the baryon mass above $10^{12}\,M_\odot$ is extrapolated; those are the groups that carry the signal. The long stages, 8 h 56 min of compute, were not repeated by that lane's lead.
\item \textbf{The scorecard's words are unchanged.} Rows 24 and 25 keep PASSES TRIVIALLY and NO POWER, which were placed for the rescaled junction. Under the exact junction row 25 would be placed FAILS; that change is the owner's decision and has not been made.
\end{itemize}

\subsection{The forest gate's own inputs}
\textbf{GAS2} read GAS1's tables from the papers' pages by eye: 151 of 151 table entries are confirmed and no placement level changes. One of GAS1's two readings of the smoothing-scale convention is void, since it rested on a misread factor. Under the reading that is left, half the gas smoothing scale (39.5 comoving kpc), the bracket behind most FRAGILE flags, is inside twice the measurement error at $z$ 2.2 only and outside the measurements at $z$ 3.0 and 4.4.

\textbf{ABS1} (not blind) tested a step that no lane had checked. The gate multiplies the DESI data by the model's fractional change in flux power, which assumes that the gate's reference model fits those data. It does not: the lane's fit word is DOES NOT FIT on both footings, with a $\chi^2$ of 13,859 on 714 points, and 5,802 on 690 degrees of freedom with an amplitude and a tilt fitted in every redshift bin. The model's flux power is 25 to 40\,\% too low at $z$ 2.2 and 15 to 25\,\% too low at $z$ 2.4, the two bins that carry most of every forest number in the record. Its gate word is GATE MOVES: with the reference's own power in place of the data, every D falls to 0.55 to 0.76 of its stored value. Holds stay holds and fails far from the line stay fails; a label that is not a hold and sits below about 7 depends on the choice. The lane tests the gate's model, a 20\,Mpc/$h$ box with fixed gas parameters, and not the framework; it relabels nothing and cannot say which scale is right. For the cases of Sections~11 and 12 (our arithmetic, not a lane's): the caustic holds stay holds; the fold radius's 3.94/5.37 of Section~11.2 would read 2.2 to 3.0 / 3.0 to 4.1, so its two words are among those that depend on the choice; and BJ1's fail does not (Section~12.3).

\textbf{DBL1}, a look-up, asked whether the public data table is unblinded, since its file carries a blinding keyword. It reads UNBLINDED: ESTABLISHED, by the documented meaning of the keyword and the identity of the release. It did not find a sentence in a primary source saying that the released table is unblinded, and its sources were read through a fetch tool and are PROVISIONAL.

\subsection{The scorecard after its sixteenth update}
Since version 1.5 CJ1's scorecard has been updated a fourteenth, a fifteenth and a sixteenth time and by two notes; its own audit reads 182 of 182. Two words for the completed form changed, each from FAILS, each on the owner's decision of 2026-11-14, and neither into a pass. The counts in Section~9.2 are the scorecard's after these changes: FAILS 2, NO POWER 8 and DEPENDS ON AN UNTESTED ASSUMPTION 6 on both footings.
\begin{itemize}
\item \textbf{Row 35, the Milky Way's ultra-faints and M31's bright dwarfs: from FAILS to NO POWER.} RB2's FAILS HIGH uses measurement scatter only. The blind DSB1 (Section~7) stops at a known answer as frozen and has no label; under its amendment no graded class fails on either footing (the ultra-faints read $+0.572$ $[-0.043,+1.173]$ / $+0.542$ $[-0.087,+1.127]$) and no class could detect an offset of 0.30 dex (the smallest detectable is 0.59 to 1.23 dex). DG1's own budget agrees. The medians stay high, so this is not a pass, and the ultra-faints fail again if the nine upper-limit rows are fixed at their limits or dropped.
\item \textbf{Row 28, the Milky Way's halo stars with the measured star-count slope: from FAILS to DEPENDS ON AN UNTESTED ASSUMPTION.} The row now has two blind-checked readings that differ only in the anisotropy convention. With one constant anisotropy the 40 to 55\,kpc bin fails (RRL1 and the blind RRL1R, Section~11.5). With the anisotropy measured in each bin it does not: RRL2 found this post hoc, its own frozen words carrying no weight because its mutations did not bite, and the blind RRL3R froze that reading as its primary. As frozen RRL3R reads NO VERDICT (KNOWN ANSWER) for every case, stopped by one planted mock; under its amendment A1 it reads ROW PASSES UNDER THE MEASURED CONVENTION, FRAGILE in three of five cases and NO VERDICT (SLOPE), FRAGILE in the other two, and it reproduces RRL2's post hoc numbers. The gate has power there: a planted 20 per cent cold bin at 40 to 55\,kpc is caught in 18 of 20 seeds. Every case is FRAGILE: with one constant anisotropy, or with the RR Lyrae score cut at 0.6, the bin is cold again in four of five cases. The framework and DESI's NFW halo move together in every convention, so the row separates nothing between them. Not a pass.
\item \textbf{What still fails.} Row 20, the outer cluster shear, and row 36, DF2, DF4, NGC\,147 and IC\,1613. OTA1 (not blind) regraded row 20 with the cold share counted once on the baryons out to turnaround: STILL FAILS on both footings. The failing statistic falls from $+4.41$/$+4.07$ to $+3.64$/$+3.31$, about a third of the way to its line at 2.
\item \textbf{The Euclid lens rows (39 to 41), words unchanged.} EUC17 found that the catalogue's stellar mass is the model's mass inside the modelling circle, which the earlier lanes had spread over an infinite body. The rows were re-read at that mass; EUC17, EUC20 and EUC21 are each followed by a blind build that gives the same labels (EUC17R, EUC20R, EUC21R), and EUC18 has none. With every source at infinity the share of lenses above the ceiling's margin falls from 15.6\,\%/13.9\,\% to 6.0\,\%/5.0\,\%, a hit and not a pass. The gate on certified source redshifts reads $+0.192$/$+0.174$: NO VERDICT, with the centre between its lines. With drawn source redshifts the population still breaks the ceiling (EUC18: CEILING BROKEN on both footings, FRAGILE on alt). The wide-lens break stays at 1.7 arcsec and wider and goes in the bin below it. At that mass 108/22 lenses sit above the crossing speed, with no step at the boundary (NO SWITCH, FRAGILE on both footings). The missing mass as cored hot gas stays excluded, and only a cusp is left (EUC21). The mass definition rests on the catalogue paper's text and on one lens's maps.
\item \textbf{The wide lenses as groups (row 40, word unchanged).} WLG1 counted the group baryons around the 316 wide lenses, the member stars plus one stacked hot-gas value given to every lens. It reads WIDE LENSES ARE FAST GROUPS: ROW 40 PASSES, FRAGILE on canonical and GROUPS TOO SLOW: ROW 40 FAILS, FRAGILE on alt: the group speed over the crossing speed is 1.093 $[1.061,1.125]$ / 0.904 $[0.878,0.931]$, and 0.634/0.524 with no gas. The blind WLG1R reads NOT EVALUABLE, BLIND on both footings, on a coverage check that the frozen text lets one read in two ways; every graded number agrees. So the blind build confirms the arithmetic and the fragility, not the label, and the canonical word is a hit in one build.
\end{itemize}

\subsection{Lanes of the same day that are not on the scorecard}
Four further lanes landed on 2026-11-14 in another session. They test the law or form B on newly published data, they are not on CJ1's scorecard, and this version's lead has not re-run or checked them; they are in the public repository under \texttt{closure\_2026\_11\_14/} and not in this version's supplement. Their words are quoted so that nothing known is left out. CLR1, form B on 106 HIFLUGCS clusters: STILL FAILS [non-cool-core clusters, 0.1-0.5 R500: over-predicts] FRAGILE on both footings, on one shape cell ($-0.137$ dex, interval $[-0.182,-0.089]$), while at $R_{500}$ form B closes the residual in all three classes. SQM1, the total mass inside 5/$h$ kpc in Euclid's first quick release, from the stars under the law: NOT EVALUABLE as frozen, and under its amendment STILL FAILS [beta\_z HIGH] FRAGILE on both footings, the law's redshift trend being $-0.17$ against a measured $-0.33\pm0.05$. MDZ1, the law's $a_0(z)$ against a published measurement that rises with redshift: NO VERDICT on both footings in all four cases; as published the rise excludes the law, and the lane's frozen brackets span both words. MWM1, the Milky Way line against DESI's enclosed mass at 20 to 80\,kpc: NO VERDICT on both footings for its primary case, FRAGILE on canonical. None bears on the candidate sixth rule; placing them on the scorecard is its lead's and the owner's step.

\subsection{Every lane folded into version 1.6}
Labels canonical/alt as each file states them; ``both'' means the same label on both footings.
{\footnotesize
\begin{longtable}{@{}p{1.6cm}p{3.8cm}p{5.6cm}p{4.7cm}@{}}\toprule
Lane & Question & Label as frozen & Post hoc / re-grade\\\midrule\endhead
XJ1R & XJ1's two caustic cases, blind & CAUSTIC 2 HOLDS, BLIND, FRAGILE (lam\_x0.5) (both); CAUSTIC 3 HOLDS, BLIND, FRAGILE (lam\_x0.5) (both) & confirms XJ1's two holds as labels; graded by the lead with the builder's grader\\
XJ1, second build & the exact junction at 0.5 and 2 fold radii, written independently & 0.5: HOLDS, FRAGILE (both); 2: NO VERDICT / FAILS & read across: HOLDS IN BOTH BUILDS (both); NOT RESOLVED / FAILS IN BOTH BUILDS\\
BJ1, flux level & the layout that moves no charge & FAILS THE FOREST for every caustic (both) & no FRAGILE flag; rotation curves and lensing pass\\
WLJ2 & rows 24 and 25 with the law unscaled inside & row 25: ROW FAILS WITH THE EXACT JUNCTION (both); row 24: ROW HOLDS WITH THE EXACT JUNCTION / NOT RESOLVED & not blind; no amendment\\
ABS1 & does the gate's reference fit the data in absolute terms & DOES NOT FIT (both); GATE MOVES (both) & not blind; tests the gate's model\\
GAS2 & GAS1's tables, read by eye & a check, no label: 151 of 151 entries confirmed & one of GAS1's two readings is void\\
DBL1 & the data table's blinding keyword & UNBLINDED: ESTABLISHED & a look-up; sources PROVISIONAL\\
RRL2 & row 28 under one convention & NO VERDICT, FRAGILE (census case, both); two mutations did not bite & post hoc: the cold bin passes with the measured anisotropy\\
RRL3R & row 28 with the measured anisotropy, blind & NO VERDICT (KNOWN ANSWER) for every case (both) & A1: ROW PASSES UNDER THE MEASURED CONVENTION, FRAGILE in three of five cases\\
OTA1 & row 20 with the share counted to turnaround & STILL FAILS / STILL FAILS & not blind\\
WLG1 & group baryons around the wide lenses & WIDE LENSES ARE FAST GROUPS: ROW 40 PASSES, FRAGILE / GROUPS TOO SLOW: ROW 40 FAILS, FRAGILE & a hit on canonical in one build\\
WLG1R & WLG1, blind & NOT EVALUABLE, BLIND (both) & confirms the arithmetic and the fragility, not the label\\
EUC17R & EUC17, blind & CEILING HOLDS (the sample with every source at infinity) & the same labels as EUC17\\
EUC18 & the population gate at the in-mask mass & gate NO VERDICT / NO VERDICT; statistic CEILING BROKEN / CEILING BROKEN & FRAGILE on alt\\
EUC20, EUC20R & the wide-lens bins and the switch test at the in-mask mass; blind & 1.3 to 1.7 arcsec bin NO VERDICT / NO VERDICT; NO SWITCH, FRAGILE / NO SWITCH, FRAGILE & the blind build reads the same\\
EUC21, EUC21R & the hot-gas lane at the in-mask mass; blind & ONLY A CUSP IS LEFT / ONLY A CUSP IS LEFT & the blind build reads the same two words\\
CJ1, updated & the scorecard after these lanes & an assembly; grades nothing; NOT ADOPTED & audit 182 of 182\\\bottomrule
\end{longtable}}

\subsection{Where this leaves the form}
Version 1.6 changes no label of an earlier lane. The post hoc candidate of version 1.5, the law unscaled inside the second or the third caustic of the clock, is now a hit that a blind build has confirmed as a label on both footings, and a second build reproduces the junction finding behind it. It is still FRAGILE, in the blind build, to a gas smoothing scale that neither build resolves; the caustic was still chosen by looking; and it is still a drawn profile. The clock's own flow delivers one to twelve per cent of the charge it needs, and the one layout graded here that conserves charge with the law out to every rotation curve FAILS the forest row at flux level on both footings. Read with that junction the weak-lensing tension is slightly worse, not relieved, and row 25 would read a fail. The forest gate on which every hold of Sections~9 to 12 rests uses a reference model that does not fit the data in absolute terms; the holds and the clear fails do not depend on that step, and the labels near the line do. Form B's failing rows are now two, the outer cluster shear and the four low dwarf rows; two former fails read NO POWER and DEPENDS ON AN UNTESTED ASSUMPTION on the owner's decisions, each backed by a blind build, and neither is a pass. The joint is a rule and not an equation, neither the junction nor the caustic follows from the action, and $\kappa$ and 5.41 are fitted. The candidate is NOT ADOPTED. The theory is not closed.

"""
tex = before(tex, "\\section{Our own estimates}", SEC12, "Section 12")

EST = r""" Version 1.6: (xxvi) From the matter-level size the lead told the owner to expect BJ1's flux-level number near a fifth of its matter-level one; it came out a twentieth. BJ1's frozen guess of the word, FAILS THE FOREST for every caustic on both footings, held. (xxvii) XJ1R's hand estimate, frozen blind, put D at 0.05 to 1.5 for the second caustic and 0.02 to 1 for the third, and gave a rotation curve a 35 and a 55 per cent chance of being cut; three of the four numbers came out just above their ranges and no curve is cut. (xxviii) WLJ2's hand estimate put the matter power at the caustics between the split's and the full law's; it came out above the full law's. Its guess that the row-25 tension would worsen held."""
tex = after(tex, "(xxv) BJ1's criteria guessed that very few haloes at the forest's redshifts would be short of charge; about half of the halo grid is.", EST, "estimates")

METHOD = r"""Version 1.6's lanes: the forest run and result of XJ1R, XJ1's second build, BJ1's flux-level run, WLJ2, ABS1, GAS2, DBL1, RRL2, RRL3R, OTA1, WLG1, WLG1R, EUC18, EUC20, EUC20R, EUC21 and EUC21R are under \texttt{closure\_2026\_11\_14/} and EUC17R is under \texttt{closure\_2026\_11\_13/}; CJ1's scorecard and its audit were updated for them, and a copy of the scorecard as it stood when version 1.5 was deposited is kept beside the script that wrote this version's edits. None is registered and none relabels an earlier lane. Post hoc items are marked in their lanes: RRL3R's amendment A1, written after one known answer stopped its frozen run and before any gate number, on which every reading of that lane other than NO VERDICT rests; RRL2's reading with the full-sky slope; the word changes of CJ1's fifteenth and sixteenth updates, which are the owner's decisions; and the arithmetic with ABS1's factors in Sections~12.3 and 12.5, which is ours. XJ1R was graded by a lead who is not blind, with the blind builder's committed grader run unchanged. The lanes of Section~12.7 are quoted from their result files and were not checked. XJ1R, ABS1, WLJ2, RRL3R (with RRL2), OTA1, WLG1 (with WLG1R), EUC17R, EUC18, EUC20 (with EUC20R) and EUC21 (with EUC21R) each carry a Lean file for the algebra they use, written after the lanes landed on the owner's standing instruction: the control junction against the exact one and the exclusivity of the forest labels and of the lane words (XJ1R); the gate statistic's exact scaling when the data are replaced by a constant multiple, with the bound when the factor varies between bins, and the closed-form best amplitude (ABS1); the tension words' exclusivity and the doubled-layout twin (WLJ2); the dependence of the line-of-sight Jeans prediction on the anisotropy, the star-count law at its break and the agreement of the two builds' forms of it (RRL3R); the rescaling that brings the cold share to its full amount at turnaround, with its continuity (OTA1); the cube-root scaling of the group speed with baryon mass and the pooled coverage fraction lying between the two class fractions (WLG1); the direction of the in-mask-mass correction and its twins (EUC17R); the Einstein mass's dependence on the source distance and the exclusivity of the population gate's words (EUC18); that the share above the margin cannot rise under the correction and that a lens above the crossing speed stays above it (EUC20); and the law's monotonicity with the bracket on the hydrostatic integrand, which shows that the needed gas pressure does not scale exactly with the missing mass (EUC21). Each compiles against the repository's Mathlib build with no error, and each has a twin of false variants in which every theorem fails to compile. They certify algebra, not physics, and no number or label; the look-ups GAS2 and DBL1 have no algebra to certify. XJ1R's 40 forest part files, the second build's and BJ1's flux-level part files are in the supplement.

"""
tex = before(tex, "\\end{document}", METHOD, "Method")

# ------------------------------------------------------------------ audit
aud = once(aud, '("version 1.5, 2026-11-14 (v1.4: DOI 10.5281/zenodo.24221457; v1.3: DOI 10.5281/zenodo.24212016; v1.2: DOI 10.5281/zenodo.24182757", P +',
           '("v1.4: DOI 10.5281/zenodo.24221457; v1.3: DOI 10.5281/zenodo.24212016; v1.2: DOI 10.5281/zenodo.24182757", P +', "audit version line 1")
aud = once(aud, '("version 1.5, 2026-11-14 (v1.4: DOI 10.5281/zenodo.24221457; v1.3: DOI 10.5281/zenodo.24212016", P72z,',
           '("v1.4: DOI 10.5281/zenodo.24221457; v1.3: DOI 10.5281/zenodo.24212016", P72z,', "audit version line 2")
aud = once(aud, "('version 1.5, 2026-11-14 (v1.4: DOI 10.5281/zenodo.24221457', P72z,",
           "('v1.4: DOI 10.5281/zenodo.24221457', P72z,", "audit version line 3")
aud = once(aud, '("NO POWER & 7 & 7", CJS, "NO POWER 7;")', '("NO POWER & 8 & 8", CJS, "NO POWER 8;")', "audit count 1")
aud = once(aud, '("FAILS & 4 & 4", CJS, "FAILS 4;")', '("FAILS & 2 & 2", CJS, "FAILS 2;")', "audit count 2")
aud = once(aud, '("DEPENDS ON AN UNTESTED ASSUMPTION & 5 & 5", CJS, "DEPENDS ON AN UNTESTED ASSUMPTION 5;")',
           '("DEPENDS ON AN UNTESTED ASSUMPTION & 6 & 6", CJS, "DEPENDS ON AN UNTESTED ASSUMPTION 6;")', "audit count 3")
aud = once(aud, '("fragile and shared by every smooth model (RRL1)", CJS, "On data, fragile, and shared by every smooth model',
           '("fragile and shared by every smooth model (RRL1)", CJS15, "On data, fragile, and shared by every smooth model', "audit historic 1")
aud = once(aud, 'row 24 is now placed PASSES TRIVIALLY and row 25 NO POWER.", CJS, "at f 1.25, 2 and 3 | no | PASSES TRIVIALLY | no |")',
           'row 24 is now placed PASSES TRIVIALLY and row 25 NO POWER.", CJS15, "at f 1.25, 2 and 3 | no | PASSES TRIVIALLY | no |")', "audit historic 2")
aud = after(aud, 'CJS14 = "codex_mass_budget_2026_11_14/before_correction/CJ1_SCORECARD_at_PAPER72_v1_4.md"\n',
            '# The scorecard as it stood when version 1.5 was deposited (commit 1f4546aa80), for quotations that describe earlier versions.\n'
            'CJS15 = "closure_2026_11_14/XJ1_exact_junction_zero_velocity_surface/paper72_v1_6/CJ1_SCORECARD_at_PAPER72_v1_5.md"\n', "audit CJS15")
aud = once(aud, '("version line", "Working note (PAPER72), version 1.5" in TEX)', '("version line", "Working note (PAPER72), version 1.6" in TEX)', "audit rule")

BLOCK = open(os.path.join(HERE, "audit_block_v1_6.py.txt"), encoding="utf-8").read()
aud = before(aud, "J = [\n", BLOCK, "audit block")
ARITH = '''A += [
 ("the three cases would read 7.0 to 9.7 on canonical and 8.1 to 11.3 on alt", f"{12.718 * 0.55:.1f} to {12.763 * 0.76:.1f}; {14.802 * 0.55:.1f} to {14.893 * 0.76:.1f}", "7.0 to 9.7; 8.1 to 11.3"),
 ("would read 2.2 to 3.0 / 3.0 to 4.1", f"{3.938 * 0.55:.1f} to {3.938 * 0.76:.1f} / {5.366 * 0.55:.1f} to {5.366 * 0.76:.1f}", "2.2 to 3.0 / 3.0 to 4.1"),
]
'''
aud = before(aud, "NOTES = [\n", ARITH, "audit arithmetic")

open(TEXP, "w", encoding="utf-8").write(tex)
open(AUDP, "w", encoding="utf-8").write(aud)
print("applied: TeX and audit are now version 1.6")
print("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
