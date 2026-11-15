#!/usr/bin/env python3
"""Apply the version 1.7 edits to PAPER72's TeX source and to its audit script, in place.

Version 1.7 folds in what happened after version 1.6 was deposited (DOI 10.5281/zenodo.24246863), all of it on
2026-11-15: the owner's adoption of the bounded closure statement (BCS1) and his go to deposit it here; the Gaia DR4
pre-data record, deposited as a record of its own (DR4REC1, DOI 10.5281/zenodo.24248715); the owner decisions of the
day on Gaia DR4; the check of the sealed wide-binary prediction under the adopted stiffness (CQB1); the wiring of the
release-day path (DP8); and the scorecard's update of that morning. It folds in no new graded data row.

Every edit is anchored on an exact string of the version 1.6 source; if an anchor is missing or not unique nothing is
written. The script refuses to run on a source that is already version 1.7. It computes no number: every number in
the inserted text is quoted from a committed file, and the audit entries added here check each one.

Run from anywhere inside the repository:  python3 apply_v1_7.py
kappa = 1/2 FITTED; not theory closed. Adopts nothing.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
PAP = os.path.join(ROOT, "qwen_claude_field_theory", "papers_2026")
TEXP = os.path.join(PAP, "PAPER72_law_with_cold_dark_energy_counted_once_2026.tex")
AUDP = os.path.join(PAP, "PAPER72_audit.py")
tex = open(TEXP, encoding="utf-8").read()
aud = open(AUDP, encoding="utf-8").read()
if "Working note (PAPER72), version 1.7" in tex:
    sys.exit("source is already version 1.7; nothing done")


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
tex = once(tex, "% PAPER72 v1.6 (2026-11-15; v1.5 2026-11-14, deposited 2026-11-14 UTC;",
           "% PAPER72 v1.7 (2026-11-15; v1.6 2026-11-15, deposited 2026-11-15 UTC; v1.5 2026-11-14, deposited 2026-11-14 UTC;", "comment line")
tex = once(tex, "Working note (PAPER72), version 1.6, 2026-11-15 (v1.5: DOI 10.5281/zenodo.24231666;",
           "Working note (PAPER72), version 1.7, 2026-11-15 (v1.6: DOI 10.5281/zenodo.24246863; v1.5: DOI 10.5281/zenodo.24231666;", "version line")

# the "what changed" paragraph for 1.6 takes the place of the one for 1.5, which moves below the abstract
lines = tex.split("\n")
i15 = [i for i, l in enumerate(lines) if l.startswith(r"\paragraph{What changed since version 1.5.}")]
i14 = [i for i, l in enumerate(lines) if l.startswith(r"\paragraph{What changed since version 1.4.}")]
if len(i15) != 1 or len(i14) != 1 or i15[0] > i14[0]:
    sys.exit("ANCHOR (what-changed paragraphs) not as expected; nothing written")
old15 = lines[i15[0]]
CHANGED = r"""\paragraph{What changed since version 1.6.} Version 1.6 (DOI 10.5281/zenodo.24246863) is unchanged in every sentence that is still true; version 1.7 adds Section~13 and dated additions marked ``Version 1.7'' in Sections~6 and 12 and in the estimates. It adds no graded data row and changes no label, no scorecard word and no count. Four things happened on 2026-11-15, after version 1.6 was deposited. The owner adopted a bounded closure statement as the record's closure statement, a statement of where the form stands and not a pass, and it is deposited with this version. What is registered for Gaia DR4 wide binaries, the rule that will score it and the tools that will run on release day were deposited as a record of their own, made before the data (DOI 10.5281/zenodo.24248715). A check made before the data finds the sealed wide-binary prediction unchanged under the stiffness that was adopted after it was sealed. And the owner's decisions of that day were wired into the release-day path and checked on DR3. The candidate is NOT ADOPTED."""
lines[i15[0]] = CHANGED
lines[i14[0]:i14[0]] = [old15, ""]
tex = "\n".join(lines)

ABSTRACT = r"""Version 1.7 adds no graded data row (Section~13). It deposits the closure statement that the owner adopted on 2026-11-15, which says where the form stands and is not a pass, and it records what is registered for Gaia DR4 wide binaries before the data. The adopted action predicts screened, Newtonian binaries that the frozen pipeline cannot tell from Newton's own, so the release listed for 2026-12-02 can count against the form and cannot confirm it. The registered files are deposited as a record of their own (DOI 10.5281/zenodo.24248715). A check made before the data finds the sealed prediction unchanged under the stiffness adopted after it was sealed.
"""
tex = once(tex, "the outer cluster shear and the four low dwarf rows.\nWe list what is open,",
           "the outer cluster shear and the four low dwarf rows.\n" + ABSTRACT + "We list what is open,", "abstract")

tex = after(tex, r"\item Gaia DR4 (2026-12-02), scored as pre-registered.",
            " Version 1.7: the pre-registration, the decisions that fix its scoring and the release-day tools are deposited as a record made before the data (DOI 10.5281/zenodo.24248715; Section~13.2).", "Section 6 Gaia item")
tex = after(tex, "placing them on the scorecard is its lead's and the owner's step.",
            " Version 1.7: the scorecard has since recorded them, with no word for the completed form and no count changed (Section~13.5).", "12.7 scorecard")

SEC13 = r"""\section{Version 1.7: the closure statement, and the Gaia DR4 record made before the data}
Everything in this section is of 2026-11-15, after version 1.6 was deposited (DOI 10.5281/zenodo.24246863). None of it is a graded data row, and none of it changes a lane's label, a scorecard word or a count.

\subsection{The record's closure statement}
On 2026-11-15 the owner adopted a bounded closure statement (BCS1) as the record's closure statement. His decision adopts it as a statement of where the theory stands, not a pass and not a derivation, and it adopts no rule: rule 6 stays a candidate. The statement is an assembly. It computes nothing and relabels nothing, and every quotation in it is checked against the committed file it names; its audit reads 249 of 249. Its closing paragraph reads:

\begin{quote}
``The record closes, bounded, on this. The law with $a_0=\tfrac12\,c\sqrt{G\rho_{\rm DE}}$ describes today's rotating galaxies and the Solar System from their baryons with one fitted constant. A cold dark energy component at 5.41 times the baryons, fitted to the CMB and counted once, carries the linear cosmology by construction and gives the richest clusters' amount at its ceiling. As adopted the form fails the Lyman-alpha forest, the outer cluster shear and four low dwarfs, and its weak-lensing amplitude is in tension with raw KiDS (excluded at 3 sigma as frozen). A sixth rule removes the forest fail only as a drawn profile that the clock's own flow does not supply. Both constants are fitted, the hot branch and the joint are rules and not solutions, and no registered prediction has come true. Gaia DR4 on 2026-12-02 can kill it and cannot confirm it.''
\end{quote}

``Bounded'' has the meaning the statement gives it: the record can say what the form is, which of its numbers are fitted, where it was tested and holds, where it fails, what it is silent on and which frozen lines would kill it. It cannot say that the form is derived or that it passes. The statement is in this version's supplement with its audit and both owner decisions, on the owner's go of the same day: ``Yes, include it''.

\subsection{Gaia DR4: what is registered and how it will be scored}
Gaia DR4 wide binaries are the next dated test, and the one that can kill the form. What the record registered for it, the rule that will score it and the tools that will run on release day are deposited as a record of their own, made before any DR4 data exist (DOI 10.5281/zenodo.24248715): a cover note and an archive of 1,002 files, with the pre-registration of 2026-07-16 and its 22 amendments, every owner decision, the sealed prediction and the release-day lanes. This section summarises it; the record is the source.
\begin{itemize}
\item \textbf{The prediction} is the seal CQ2 of 2026-11-04 for the adopted action: wide binaries are screened and Newtonian, with a radial boost of at most $4.45\times10^{-5}$ on the canonical footing and $4.01\times10^{-5}$ on the alternative footing, at 30 kAU. Pushed through the frozen pipeline the fitted value is identical to Newton's in every realisation, and the seal labels the prediction NOT SEPARABLE from Newton on both footings.
\item \textbf{What the release can decide.} In the registry map's words: ``A Newtonian sky is survival for the adopted theory, never confirmation.'' A value three standard errors or more above Newton, and not three or more below the bare law's anchor, excludes the adopted action's screening. A Newton-side reading is worded ``v3s survives'', never ``confirmed''.
\item \textbf{Power.} The forecast for DR4 under the frozen cuts is about 8,000 pairs (7,025 to 8,618), not 30,000. At that size the map puts the chance that a Newtonian sky reads decisive against the bare law at about 0.80 if the systematic error is at its floor of 0.020, and at 0.12 to 0.40 if it is the 0.0375 measured on DR3. Otherwise the reading is UNDECIDED.
\item \textbf{The decisions of 2026-11-15.} Form B's headline score on Gaia DR4 wide binaries is the reading fixed on 2026-11-05: the fork rows with the $R$ statistic beside them. To a sheet of the gaps the registry map had left open, the owner answered ``Accept all recommended''. Each footing has its own verdict line; the $R$ label quoted is the $R$ lane's own, which is the reading under which a kill is harder; no Milky Way row is scored for form B or for the adopted action; and the systematic error uses the seed-mean entry the owner filed on 2026-11-08.
\item \textbf{One rule is still owed.} The decision states no fallback for the systematic error if the seed-mean sweep cannot run on release day: none was put to the owner. In that case the release-day script stops and never computes the error with the single-seed entry. A dated decision before the data is owed.
\end{itemize}

\subsection{The sealed prediction under the adopted stiffness}
CQ2 was sealed with the raw stiffness. On 2026-11-07 the record adopted a smooth blend in its place, and no wide-binary run had been made with it. CQB1 froze its criteria and made the check before the data. Its labels are MARGIN HOLDS, UNCHANGED on both footings. The blend equals the raw stiffness, with its first two derivatives, wherever the switch variable is at least the dark-energy density; over the region the seal's solution occupies the lane finds the ratio at least $6.38\times10^4$ on canonical and $4.90\times10^4$ on alt, and $3.00\times10^4$ and $2.34\times10^4$ after its allowance for an independent estimate of the Galactic phantom density. So the equations the seal solved are the same equations under the blend, and its numbers stand as printed.
\begin{itemize}
\item \textbf{Checks.} The lane reproduces the seal's own numbers first, from a byte-identical copy of its script. All four of its mutations bite; the lead re-ran the lane's script and the four mutations.
\item \textbf{What the mutations show.} The blend is not harmless inside its own layer: with the region placed there by a mutation, the worst boost at 30 kAU rises by a factor of 1.8 to 3.4 above the seal. The result holds because binaries are nowhere near that layer.
\item \textbf{Limits.} The lane checks only where the seal's solution sits relative to the blend layer. It does not re-test the seal's own model. The Galactic phantom values are one disc model's, and the independent estimate agrees with them to a factor of about 2. The lane was run from a brief that carried the lead's guess, so it is not blind.
\end{itemize}

\subsection{The release-day path}
DP8 wired the decisions of 2026-11-15 into the release-day script and its runbook and checked them on DR3 only, with nothing fetched. The seed-mean entry of the systematic error, the fallback for binaries without a neighbour cone, the three rungs of the systematic error and the separation-resolved statistic of Amendment 14(c) are each WIRED; the rest is runbook text. On the release-day path the error term with the seed-mean entry equals the earlier lane's reference in 77 of 77 numbers, the script's own check reads all 30 pinned files in order, and the scorer's self-test reads 20/20. No frozen file was edited. The sweep's network path on DR4 cannot be tested before the release.

\subsection{The scorecard since version 1.6}
CJ1's scorecard was updated once more, on 2026-11-15, by the session that ran the four lanes of Section~12.7: rows 15, 16, 26, 31 and 39 now record MWM1, SQM1, MDZ1 and CLR1. No word for the completed form and no count changed, and the scorecard's audit reads 189 of 189. Three of those readings count against the form, and this version's lead has not re-run them. MDZ1's label is NO VERDICT, and its file says: ``As published, the rise excludes the law on both footings.'' CLR1 reads STILL FAILS [non-cool-core clusters, 0.1-0.5 R500: over-predicts] FRAGILE. SQM1, under its amendment, reads STILL FAILS [beta\_z HIGH] FRAGILE. Changing row 26's word after MDZ1 is the owner's decision and has not been made. Row 38, Gaia DR4, keeps its word and its note: ``Can kill the adopted theory, cannot confirm it.'' CQB1, DP8 and the decisions above are not on the scorecard; placing them is its lead's step.

\subsection{Every item folded into version 1.7}
{\footnotesize
\begin{longtable}{@{}p{2.2cm}p{5.2cm}p{4.6cm}p{3.7cm}@{}}\toprule
Item & What it is & Label or state & Notes\\\midrule\endhead
BCS1 & the bounded closure statement & ADOPTED by the owner as a statement; audit 249 of 249 & an assembly; adopts no rule; not a pass\\
DR4REC1 & the Gaia DR4 pre-data record & deposited, DOI 10.5281/zenodo.24248715 & a time stamp, not a result; its archive is in that record\\
DR4DS1 & the sheet of the gaps the registry map left open & answered by the owner: ``Accept all recommended'' & a draft that decides nothing by itself\\
CQB1 & the seal CQ2 under the adopted blend & MARGIN HOLDS, UNCHANGED (both) & not blind; the lead's guess was graded right\\
DP8 & the decisions wired into the release-day path & the four code items WIRED; checked on DR3 only & one fallback rule still owed\\\bottomrule
\end{longtable}}

\subsection{Where this leaves the form}
Version 1.7 changes no label, no scorecard word and no count. The form's failing rows are still two, the outer cluster shear and the four low dwarf rows, and the readings of Section~13.5 now stand beside them. The closure statement says what the record can say without another lane, and it is bounded: both constants are fitted, the hot branch and the joint are rules, and no registered prediction has come true. Gaia DR4 is the next dated test. Its prediction, its scoring rule and its tools are frozen and deposited; the sealed prediction is unchanged under the adopted stiffness; and the release can count against the form and cannot confirm it. The candidate is NOT ADOPTED. The theory is not closed.

"""
tex = before(tex, "\\section{Our own estimates}", SEC13, "Section 13")

EST = r""" Version 1.7: (xxix) Before CQB1 froze its criteria the lead guessed that around a wide binary the switch variable is $10^4$ to $10^5$ times the dark-energy density, so that the blend equals the raw stiffness there. The lane graded the guess right: the minimum is $6.4\times10^4$ and $4.9\times10^4$."""
tex = after(tex, "Its guess that the row-25 tension would worsen held.", EST, "estimates")

METHOD = r"""Version 1.7's items: the closure statement BCS1 with its audit, the two owner decisions on it, CQB1, the decision sheet DR4DS1, and the cover note, audit and manifest of the Gaia DR4 record DR4REC1 are under \texttt{closure\_2026\_11\_15/}; the two owner decisions of 2026-11-15 on Gaia DR4 are under \texttt{prep\_2026/gaia\_dr4\_prep/}; DP8 is under \texttt{dr4\_push\_2026\_11\_05/}; and the seal CQ2 that CQB1 checks is under \texttt{cq\_lanes\_2026\_11\_04/}. The archive of DR4REC1 is in that record (DOI 10.5281/zenodo.24248715) and is not copied into this version's supplement. None of these is registered as a new prediction and none relabels an earlier lane. CQB1 carries a Lean file for the algebra it and the seal use (CQB1, 19 theorems): the blend's equality with the raw stiffness above the dark-energy density, the density's closed form, the margin statements and the seal's bound on the velocity boost. The scoring rows with the map's edges and the $R$ rule, and the seed-mean error term, carry theirs in the Gaia DR4 record (DP3, 18 theorems; DP7, 10 theorems). Each compiles against the repository's Mathlib build with no error, and each has a twin of false variants in which every theorem fails to compile. They certify algebra, not physics, and no number or label. BCS1 and DR4DS1 are assemblies and DP8 wires code paths; they have no algebra to certify. CQB1 and DP8 were each run by a separate session from a written brief; CQB1's brief carried the lead's guess, so that lane is not blind, and the lead re-ran its script. DP8's DR4 network path cannot be tested before the release. The script that wrote this version's edits is kept beside its audit entries.

"""
tex = before(tex, "\\end{document}", METHOD, "Method")

# ------------------------------------------------------------------ audit
aud = once(aud, '("version 1.6, 2026-11-15 (v1.5: DOI 10.5281/zenodo.24231666", P72z,',
           '("v1.5: DOI 10.5281/zenodo.24231666", P72z,', "audit version line")
aud = once(aud, '("version line", "Working note (PAPER72), version 1.6" in TEX)', '("version line", "Working note (PAPER72), version 1.7" in TEX)', "audit rule")

BLOCK = open(os.path.join(HERE, "audit_block_v1_7.py.txt"), encoding="utf-8").read()
aud = before(aud, "J = [\n", BLOCK, "audit block")
ARITH = '''def _v7_theorems(path):
    return str(len(re.findall(r"^\\s*(?:theorem|lemma)\\s", open(os.path.join(ROOT, path), encoding="utf-8").read(), flags=re.M)))
A += [
 ("(CQB1, 19 theorems)", _v7_theorems("closure_2026_11_15/CQB1_cq2_under_blend/CQB1.lean"), "19"),
 ("(DP3, 18 theorems; DP7, 10 theorems)", _v7_theorems("dr4_push_2026_11_05/DP3_release_day/DP3.lean"), "18"),
 ("DP7, 10 theorems)", _v7_theorems("dr4_push_2026_11_05/DP7_seed_mean_check/DP7.lean"), "10"),
]
'''
aud = before(aud, "NOTES = [\n", ARITH, "audit arithmetic")

open(TEXP, "w", encoding="utf-8").write(tex)
open(AUDP, "w", encoding="utf-8").write(aud)
print("applied: TeX and audit are now version 1.7")
print("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
