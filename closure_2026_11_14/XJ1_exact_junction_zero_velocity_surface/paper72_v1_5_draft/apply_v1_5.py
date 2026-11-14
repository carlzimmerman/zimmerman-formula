#!/usr/bin/env python3
"""PAPER72 v1.5 DRAFT (not deposited): anchored edits that fold in XJ1 (the junction), CSD1 (charge delivery), the
Codex correction's audit, FWN2, the blind RRL1R, and CJ1's tenth update (RB1R, RB2R, GAS1).

Revision 2 of this script (2026-11-14): the Codex session's dated local correction is now committed in the paper
source (9935bcc45e) and the owner has said the lead merges after it. The script reads the paper's current TeX and
audit, applies the edits below (each anchor must occur exactly once, or the script stops) and writes
    out/PAPER72_v1_5_DRAFT.tex and out/PAPER72_audit_v1_5.py          (default; a copy, for building and auditing)
or, with --in-place, the paper's own two files under qwen_claude_field_theory/papers_2026/.
  python3 -I -B apply_v1_5.py [--in-place]
Run it once on a source that is still version 1.4 plus the local correction; it stops if the source is already 1.5.
Nothing is deposited. kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import os, re, sys
INPLACE = "--in-place" in sys.argv
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
PDIR = os.path.join(ROOT, "qwen_claude_field_theory", "papers_2026")
TEXP = os.path.join(PDIR, "PAPER72_law_with_cold_dark_energy_counted_once_2026.tex")
AUDP = os.path.join(PDIR, "PAPER72_audit.py")
tex = open(TEXP, encoding="utf-8").read(); aud = open(AUDP, encoding="utf-8").read()
if "Working note (PAPER72), version 1.5" in tex: sys.exit("the source is already version 1.5; nothing applied")

def once(s, a, b, what):
    if s.count(a) != 1: sys.exit(f"anchor not unique ({s.count(a)}): {what}")
    return s.replace(a, b)
def _line(s, test, what):
    lines = s.split("\n"); hit = [i for i, l in enumerate(lines) if test(l)]
    if len(hit) != 1: sys.exit(f"line anchor not unique ({len(hit)}): {what}")
    return lines, hit[0]
def after_line(s, prefix, add, what, contains=False):
    lines, i = _line(s, (lambda l: prefix in l) if contains else (lambda l: l.startswith(prefix)), what)
    lines[i] = lines[i] + add; return "\n".join(lines)
def line_after(s, prefix, new, what):
    lines, i = _line(s, lambda l: l.startswith(prefix), what)
    lines.insert(i + 1, new); return "\n".join(lines)

# ---- labels as graded (xj1b_grade.json, xj1b2_grade.json, with the bracket stage)
FAIL = "FOREST ROW FAILS AT FLUX LEVEL"; HOLD = "FOREST ROW HOLDS AT FLUX LEVEL"
LAB = {"E1": ("NO VERDICT", FAIL), "E2": (FAIL, FAIL), "E3": (FAIL, FAIL), "Ezv": (FAIL, FAIL),
       "E0.5": (HOLD, HOLD), "Ec3": (HOLD, HOLD), "Ec2": (HOLD, HOLD), "E0.75": (HOLD, HOLD)}
BRACKET_SENTENCE = ""    # one or two sentences on the brackets
BRACKET_TUPLES = []      # (TeX fragment, source key, literal)
CJ1_AUDIT = "135 of 135"  # CJ1's audit count at the scorecard update the paper cites
CJ1_AUDIT_LIT = "reads 135 of 135."

ABSTRACT = r"""
Version 1.5 adds the lanes that landed after version 1.4 and corrects three readings of versions 1.3 and 1.4 (Section~11). The crossing speed is an algebraic intersection of two speed relations, not a derived switch: the mass-budget sentence given for it had its inequality reversed. The junction used by every lane that graded the candidate multiplies the law's halo inside the settled radius by a factor that runs from 0.48 to 1.83 on the forest's haloes, so the layout that was graded is the law only where that factor is 1; under it the rotation-curve gate fails on the canonical footing at two and three fold radii, and the galaxy rows called equal to the law are not exactly so. With the law itself inside the settled radius, the forest row FAILS at the level of the transmitted flux at two and three fold radii and at the turnaround surface on both footings: the holds of versions 1.3 and 1.4 belong to a layout whose inside is not the law. Post hoc, the same lane finds that the law placed unscaled inside the second or the third caustic of the clock's own infall, at about 0.6 and 0.5 of the fold radius, holds the forest row on both footings, keeps every rotation curve on the law and passes the lensing gate, with no constant read from data. These are hits found by looking, in one build; no blind build has graded them. They are also drawn profiles and not states the clock is shown to reach: charge conservation at the moving boundary cannot be met by the action's non-advective flux, which is of order one part in a million of the flow, and the clock's own shell flow delivers one to twelve per cent of the charge that the law's halo needs inside the caustic."""

CHANGED = r"""\paragraph{What changed since version 1.4.} Version 1.4 (DOI 10.5281/zenodo.24221457) is unchanged in every sentence that is still true; version 1.5 adds Section~11, corrects Section~9.1 in place where it is marked ``corrected 2026-11-14'', and adds dated additions marked ``Version 1.5'' in Sections~6, 9 and 10. Three readings change. The crossing speed is an algebraic intersection, not a derived transition: the same-radius mass inequality of Section~9.1 was reversed. FZS1's junction rescales the inner cold profile, so the completed form's galaxy rows are not shown to equal the law. And the candidate's forest hold at $f=2$ and 3 is a hold of that rescaled layout, not of the law's. Section~11 folds in XJ1, CSD1, FWN2, RB1R, RB2R, RRL1R and the look-up GAS1, and the audit of the correction itself. Historical lane labels are preserved; no label of an earlier lane changes. The candidate is NOT ADOPTED.

"""

DECIDE = r"""\item Version 1.5, for the junction (Section~11): a blind build of the law placed unscaled inside the second and the third caustic, with its own caustic computation, graded on the forest at flux level and on where rotation curves end; a second, independently written build of the exact junction; the rows not re-graded for it (the resolved discs at $z\approx2$, groups, the matter-power and lensing-amplitude rows, the Milky Way's enclosed-mass profile and the dwarfs); and, for the junction to be more than a drawn profile, a flow of the action that delivers the charge: a tracked system solved with the field equations across a transition of finite width, with the conserved current's interface condition met."""

EDGE = r""" Version 1.5: this window is for FZS1's rescaled junction. With the law itself inside the settled radius the lensing gate passes at every radius run, from 0.5 to 3 fold radii, so it sets no lower edge, and the forest at flux level allows no more than about one fold radius (Section~11.2)."""

LEAVES10 = r""" Version 1.5: the hold at $f=2$ and 3 belongs to FZS1's rescaled junction; with the law itself inside the settled radius both radii FAIL the forest at flux level on both footings (Section~11.2)."""

COUNTS = r""" Version 1.5: the table gives the counts after CJ1's tenth update (Section~11.5): row 15, X-COP's two-sided amount, is placed DEPENDS ON AN UNTESTED ASSUMPTION and no longer FAILS."""

ROW15 = r""" Version 1.5: X-COP's two-sided amount is no longer among them (row 15, Section~11.5)."""

D = {"E1": ("3.938 (0.263)", "5.366 (0.390)"), "E2": ("16.37 (0.79)", "25.73 (1.96)"), "E3": ("42.76 (1.86)", "78.36 (4.47)"),
     "Ezv": ("25.06 (1.12)", "42.08 (2.86)"), "E0.5": ("0.583 (0.050)", "0.794 (0.059)"), "Ec3": ("0.512 (0.049)", "0.691 (0.052)"),
     "Ec2": ("1.213 (0.095)", "1.648 (0.133)"), "E0.75": ("1.909 (0.138)", "2.584 (0.209)")}
def row(name, key):
    c, a = LAB[key]
    return name + " & " + D[key][0] + "; " + c + " & " + D[key][1] + "; " + a + r"\\"

SECTION = r"""\section{Version 1.5: the junction of rule 6, the law itself inside the settled radius, and what charge conservation asks}
The lanes in this section landed on 2026-11-14, after version 1.4 was deposited (DOI 10.5281/zenodo.24221457). Each froze its criteria in a commit before any graded number; frozen readings come first and post hoc readings are labelled. This section withdraws readings of versions 1.3 and 1.4. It changes no lane's label.

\subsection{What the junction of versions 1.3 and 1.4 does}
Rule 6 says that the law's layout holds inside the settled radius. Every lane that graded it (FZS1, SRH1, JNT2, JNT2R, FRZ4 to FRZ6R, FWN1, FWN1R, FWN2 and WLJ1) built the inside with FZS1's junction: the law's cold halo multiplied by $s=C_R(R_{\rm set})/C_B(R_{\rm set})$, the reference's enclosed cold mass over the law's at the settled radius. Rule 4 gives the law's halo from the baryons with no free amplitude, so a halo of $s$ times the law's is the law only where $s=1$. XJ1 measured how far from 1 it is.
\begin{itemize}
\item On the forest's haloes ($f$ 1 to 3, $z$ 2.2 to 4.4) $s$ runs from 0.48 to 1.83. Today, for $\log M_b$ 8 to 10.45 on canonical, it is 0.47 to 0.93 at $f=1.25$, 0.57 to 0.78 at $f=2$ and 0.69 to 0.72 at $f=3$.
\item \textbf{Rotation curves under that junction} (post hoc, XJ1's amendment A2: PD1's statistic on 175 SPARC galaxies with one $s$ per galaxy from the lens chain; the known answer $s=1$ reproduces PD1's stored numbers). The median galaxy keeps 0.59 to 0.75 of the law's halo. PD1's gate reads PASS/PASS at $f=1.25$ (rms 0.0646/0.0640 against lines of 0.0660/0.0658), FAIL/PASS at $f=2$ (0.0682/0.0654) and FAIL/FAIL at $f=3$, where the massive spirals miss their own line on both footings; the law itself reads 0.0560/0.0558. Where the gate passes, the fitted median mass-to-light ratio has risen from 0.58/0.52 to between 0.75 and 0.87.
\end{itemize}
So the placement EQUALS THE LAW for the completed form's galaxy rows (Section~9.2) is exact only where $s=1$: it was made from membership below the crossing speed alone. No row is relabelled here.

\subsection{The law itself inside: the forest row FAILS where the rescaled junction held}
XJ1's exact junction keeps the law's layout, unscaled, inside $R_{\rm set}$ and gives the rest of the system's cold component the reference's shape outside it, multiplied by one factor so that the mass inside the turnaround radius is unchanged. The cold component is still counted once and the boundary $v^*(z)$ is unchanged. The cases below were frozen before any number and graded at flux level in FWN1R's build (4 seeds in every bin; gate $\Delta\chi^2\le4$; D is the 12-bin flux $\Delta\chi^2$).
{\small
\begin{longtable}{@{}p{3.4cm}p{6.0cm}p{6.0cm}@{}}\toprule
Settled radius & canonical: D (SE); label & alt: D (SE); label\\\midrule\endhead
""" + "\n".join([row(r"$R_{\rm fold}$", "E1"), row(r"$2\,R_{\rm fold}$", "E2"), row(r"$3\,R_{\rm fold}$", "E3"), row("zero-velocity surface", "Ezv")]) + r"""\bottomrule
\end{longtable}}
\begin{itemize}
\item \textbf{The lane's frozen word on both footings: THE HOLD DOES NOT SURVIVE THE EXACT JUNCTION.} In the same boxes FZS1's junction reads 0.024/0.029 at $f=2$ (FRZ6R) and 0.572/0.691 at $f=3$ (FWN1R); the exact junction is 671/878 and 75/113 times higher. So the forest holds at $f=2$ and 3 of Sections~9.3 and 10 belong to a layout whose inside is not the law.
\item \textbf{A settled radius with no free constant, as frozen.} The zero-velocity surface is FLD1's turnaround radius of the clock's shells, 2.3 to 3.5 fold radii at the forest's redshifts; it FAILS on both footings. The fold radius itself is not resolved on canonical and FAILS on alt.
\item \textbf{Checks.} The control, FZS1's junction at $f=5$, equals FWN1R's stored parts in all 96 files and still fails (8.834/10.897). Every known answer passes and every twin bites; one known answer needed a round-off tolerance (amendment A1, committed before any box number). Both graders were re-run from the committed parts into a separate folder with identical output; the boxes were not re-run.
\item \textbf{The estimate was wrong.} The criteria's hand estimate put D at 0.02 to 0.5 at the fold radius, 0.1 to 3 at twice it, 2 to 20 at three times it and 0.5 to 10 at the zero-velocity surface. Every one came out 5 to 30 times higher.
\item \textbf{Where the gate is crossed (reported).} Interpolating between the radii that were run, D reaches 4 at $f=1.01$ on canonical and 0.89 on alt.
\end{itemize}

\subsection{Post hoc: radii inside the fold, and the clock's own caustics}
After the matter-level numbers of the frozen cases were read, and before any flux-level number, XJ1 added four cases by dated amendments (A3, A5): the exact junction at 0.5 and 0.75 fold radii, and at the second and third caustic of the clock's infall. The caustics come from FLD1's shell computation with a count of passages through the centre added, whose 24 runs reproduce FLD1's stored series exactly: the $k$-th caustic is the largest radius reached by shells that have passed the centre at least $k$ times. The fold radius is the first. The second is at 0.68 of the fold radius today and 0.60 to 0.65 at $z$ 2.2 to 4.4; the third at 0.535 and 0.47 to 0.51; the ratios are the same within 0.01 for $\log M_b$ 9.4 to 12. No constant multiplies them.
{\small
\begin{longtable}{@{}p{3.4cm}p{6.0cm}p{6.0cm}@{}}\toprule
Settled radius & canonical: D (SE); label & alt: D (SE); label\\\midrule\endhead
""" + "\n".join([row(r"$0.5\,R_{\rm fold}$", "E0.5"), row("third caustic", "Ec3"), row("second caustic", "Ec2"), row(r"$0.75\,R_{\rm fold}$", "E0.75")]) + r"""\bottomrule
\end{longtable}}
The lane's words on both footings are A WINDOW IS LEFT: f in [0.5, 0.75], and HOLDS WITH NO FREE CONSTANT for the second caustic and for the third. BRACKETS_GO_HERE
\begin{itemize}
\item \textbf{Rotation curves.} No SPARC galaxy's last measured point lies beyond the third caustic (the largest ratio is 0.77; 0.60 for the second), so with the exact junction at either caustic every curve is the law's own and PD1's numbers carry over unchanged. The $z\approx2$ discs below the crossing speed also stay inside (0.391 of the fold radius at most, against a third caustic at 0.446 or more), so the coverage line of Section~9.2 still fails through the discs above the crossing speed only.
\item \textbf{Lensing.} With the exact junction the KiDS early-type gate passes on both footings at every radius run, from 0.5 to 3 fold radii and at both caustics, where FZS1's junction fails it at $f=1$; a blind build found earlier that this gate cannot see the settled radius.
\item \textbf{The Milky Way beyond 100\,kpc} (post hoc reading with PLT1's pulls reproduced): the third caustic sits at 99\,kpc and the medians of the pulls are unchanged, $+1.40$/$+1.47$ for the field stars against $+1.39$/$+1.57$ for the law at every radius.
\item \textbf{At matter level}, the record's older gate with no gas physics, the third caustic reads 2.87/6.37 and the second 8.15/19.04 against the line of 4: the third passes on canonical only and the second fails on both.
\end{itemize}
\textbf{What counts against these holds.} They are post hoc. The search went from the frozen zero-velocity surface, which fails, to two radii inside the fold and then to the caustics, so a hold of the second or third caustic is a hit found by looking, from a family of two. The integer is not fixed: the fold is not resolved or fails, the second and third both hold, and today's rotation curves also allow the fourth caustic, at 0.448 of the fold radius, and are cut at the fifth by one galaxy (post hoc, amendment A6; the forest was not run there). A hold means the layout departs little enough from the reference at $z$ 2.2 to 4.4; it is not evidence for the law inside. Neither the junction nor the caustics are derived from the action: behind the fold FLD1's shell equation is not exact and the action gives no answer (Section~7). The gas inputs are provisional and the grid only marginally resolves the smoothing scale, as in Section~10.1. One build graded these cases. A second, independently written build of the exact junction at 0.5 and 2 fold radii, and a blind lane grading the two caustics with its own caustic computation (XJ1R), were running when this version was written and are not in it. The blind lane's light stage, built without sight of XJ1's numbers, gives the same caustic ratios, finds no galaxy beyond either caustic (the largest ratios 0.602 and 0.767) and reads the same matter-level numbers, 8.146/19.037 and 2.872/6.368; its forest run had not started.

\subsection{What charge conservation asks of any such junction}
A layout that passes profile gates is a drawn profile until the clock's conserved charge is shown to reach it. A note by a Codex session, re-derived by an independent audit and by CSD1, gives the condition: with no reservoir of charge on the surface, a conserved current obeys $[J^r]-\dot R\,[J^t]=0$ across an interface $r=R(t)$, and in the weak-field reduction of Section~7 this is $N_{\rm out}(v_{\rm out}-\dot R)=N_{\rm in}(v_{\rm in}-\dot R)$, with $N$ the charge density. Integrated in time, an interior that stands still must hold exactly the charge the flow has carried through its boundary.
\begin{itemize}
\item \textbf{The action's other channel is negligible.} The non-advective term of the action's current is 3e-7 to 5e-7 of the advective flux for a Milky-Way-mass system at 100\,kpc (the audit), and 1.8e-6 to 4.7e-6 outside the caustics in CSD1's evaluation, where it supplies 4.8e-7 to 1.3e-6 of the flux that is missing. A thinner transition does not change its main part, which depends on the potential and its first derivative. The note's sentence that full polarization transport could change the conclusion below is wrong in the weak field.
\item \textbf{The sign.} Over 7,110 snapshots of XJ1's two caustic layouts (today and the twelve forest redshifts, both footings) the law's density just inside the caustic is below the density just outside in 3,706 and above it in 3,373. In the first group an interior that stands still while its boundary grows would need the outer flow to move outward.
\item \textbf{The amount (CSD1).} With the clock's own shell flow from an isolated seed, the record's own infall, the charge inside the third caustic is 0.0086 to 0.068 of what the law's halo needs there, for $\log M_b$ 8 to 11.5 at $z$ 0, 2.2, 3.0 and 4.4; the label is SHORT AT CAUSTIC 2 / SHORT AT CAUSTIC 3 on both footings. Seeding the patch with the cosmological share does not help: tuned to turn around 59.3 times the baryon mass with the law off, the same patch turns around 2.0 times with the law on and delivers 0.017 to 0.121. In that shell equation the clock's own excess does not bind itself; only the baryons pull it in. With the halo model's reference layout taken as the delivered charge the ratio is 0.49 to 1.67, under at low mass and over at high mass (it crosses 1 at $\log M_b$ 10.09/10.42 today); the reference is not a flow, so this shows what a delivery would have to supply, not that one exists.
\item \textbf{The standing state exists.} The static balance of that shell equation is the law exactly (CSD1's first known answer). What is missing is the transport into it.
\end{itemize}
So the caustic layouts of Section~11.3 cannot be assembled by the clock's own flow with a standing interior: the flow brings one to twelve per cent of the charge, and the action has no other channel in the weak field. This is the open joint of Section~7 in numbers. It changes no profile gate. CSD1 has two amendments; the second is post hoc and concerns how one known answer treats empty cells, with the same numbers either way. The audit checked six of the note's eight example rows, and the note's own ``independent review'' is by the same session that wrote it.

\subsection{Further lanes since version 1.4}
\textbf{FWN2} (not blind) ran the split with FZS1's junction at $f=4$ in both forest builds and at $f=3.5$ and 4.5 in FWN1R's build. As a read across, $f=4$ is NOT RESOLVED on both footings: FWN1's build reads 4.34/5.37 and cannot tell; FWN1R's build reads 3.18/3.71, a hold on canonical, FRAGILE, and NO VERDICT on alt. In FWN1R's build the split holds at $f=3.5$ (1.50/1.78) and fails at $f=4.5$ (5.62/6.62), every label FRAGILE to the gas smoothing scale and $\gamma$. These are numbers for the rescaled junction of Section~11.1.

\textbf{RRL1R}, the blind re-grade of RRL1, gives the same label in all four framework cases, MEASURED SLOPE MAKES A PASSING BIN FAIL [40-55 COLD], robust only on the rotation-curve stellar mass on alt. DESI's NFW halo gets the same label: the row is shared by every smooth model.

\textbf{RB1R, RB2R, GAS1 and CJ1's tenth update.} RB1R, a blind re-grade of the X-COP amount, reads AMOUNT CONSISTENT ON BOTH SIDES on both footings. On the owner's decision of 2026-11-14 CJ1 re-sourced row 15, X-COP's two-sided amount, to form B's own numbers: the FAIL it had quoted is a reading with half the share kept out of the core, which is not form B. Its word for the completed form changes from FAILS to DEPENDS ON AN UNTESTED ASSUMPTION, and the counts of Section~9.2 are CJ1's after that update. RB2R, a blind re-grade of the hosted low rows, reads LOW ROWS COUNT AGAINST B on both footings, so row 36 stays a fail of form B. GAS1, a look-up whose numbers stay PROVISIONAL, finds that half the gas smoothing scale, the bracket behind several FRAGILE flags, is mostly outside the measurements, while $\gamma$ 1.2 and 1.6 are inside them.

\subsection{Every lane folded into version 1.5}
Labels canonical/alt as each file states them; ``both'' means the same label on both footings.
{\footnotesize
\begin{longtable}{@{}p{1.6cm}p{3.8cm}p{5.6cm}p{4.7cm}@{}}\toprule
Lane & Question & Label as frozen & Post hoc / re-grade\\\midrule\endhead
XJ1 & the law unscaled inside the settled radius, at flux level & THE HOLD DOES NOT SURVIVE THE EXACT JUNCTION (both); the zero-velocity surface FAILS (both); the fold radius NOT RESOLVED / FAILS & A3, A5 post hoc: A WINDOW IS LEFT: f in [0.5, 0.75] (both); HOLDS WITH NO FREE CONSTANT for the second and the third caustic (both); hits, not blind\\
CSD1 & does the clock's flow deliver the law's charge inside the caustic & isolated seed: SHORT AT CAUSTIC 2 / SHORT AT CAUSTIC 3 (both); reference as the supply: DEPENDS ON MASS (both) & A2 post hoc (a known answer's empty cells); the cosmological seed SHORT (both)\\
FWN2 & the split at $f=3.5$, 4 and 4.5, at flux level & $f=4$ NOT RESOLVED (both) & not blind; rescaled junction\\
RRL1R & RRL1, blind & MEASURED SLOPE MAKES A PASSING BIN FAIL [40-55 COLD] (all four framework cases) & confirms RRL1's label and its fragility\\
RB1R & the X-COP amount, blind & AMOUNT CONSISTENT ON BOTH SIDES (both) & row 15 re-sourced on the owner's decision\\
RB2R & the hosted low rows, blind & LOW ROWS COUNT AGAINST B (both) & not blind to which rows to expect\\
CJ1, updated & the scorecard after these lanes & an assembly; grades nothing; NOT ADOPTED & audit CJ1AUDIT_GOES_HERE\\\bottomrule
\end{longtable}}

\subsection{Where this leaves the form}
Version 1.5 changes no label of an earlier lane. It withdraws three readings of versions 1.3 and 1.4: that the crossing speed follows from the rules, that the completed form's galaxy rows equal the law, and that the candidate's forest hold at $f=2$ and 3 is a hold of the law's layout. The last two are true of a junction that rescales the law's halo, and of that junction only. With the law itself inside, the settled radius cannot exceed about one fold radius, so the constant $f$ that version 1.4 bounded between 1.25 and about 4 has no window there. What is left is a post hoc candidate with no constant read from data: the law inside the second or the third caustic of the clock, which in one build holds the forest row, keeps the rotation curves and passes the lensing gate on both footings. It is a hit found by looking, no blind build has graded it, and it is a drawn profile: the clock's own flow delivers one to twelve per cent of the charge it needs and the action has no other channel in the weak field. Form B's failing rows stay, with X-COP's two-sided amount moved from a fail to a row that depends on an untested assumption. The joint is a rule and not an equation, neither the junction nor the caustic follows from the action, and $\kappa$ and 5.41 are fitted. The candidate is NOT ADOPTED. The theory is not closed.

"""

ESTIMATE = r""" Version 1.5: (xxiii) XJ1's hand estimate, frozen before any number, gave the exact junction at the fold radius a 75\,\% chance of holding the forest and favoured the zero-velocity surface as a settled radius with no free constant; every frozen case came out 5 to 30 times above its estimated range, the fold is not resolved or fails, and the surface fails. (xxiv) The lead estimated the action's non-advective flux at about one part in a million of the flow before it was computed; the audit and CSD1 find 3e-7 to 5e-6."""

METHOD = r"""Version 1.5's lanes: XJ1, XJ1R, CSD1, FWN2, RRL1R, RB1R, RB2R and the look-up GAS1 are under \texttt{closure\_2026\_11\_14/}; the Codex session's correction, its enclosed-mass audit and its junction and transport notes are under \texttt{codex\_mass\_budget\_2026\_11\_14/}, with the lead's audit note, and the independent audit of them is \texttt{reviews/codex\_mass\_budget\_audit\_2026\_11\_14/}. None is registered and none relabels an earlier lane. Post hoc items are marked in their lanes: XJ1's amendments A2 (rotation curves under FZS1's junction), A3 (0.5 and 0.75 fold radii), A4 (the second build's cases), A5 (the caustics) and A6 (how far the integer can go), each written after earlier reported numbers of that lane were read and committed before the numbers it governs; XJ1's A1 is a round-off tolerance; CSD1's A2. The headers of XJ1's criteria and of its first amendment carry clock times that were guesses and are wrong; the commit times are the record, and the lane's result says so. XJ1's first forest pass was stopped for 48 minutes when free disk and swap ran short, and six of its twelve bins were read while it was stopped; its result records that no criterion, case or amendment was written after that look. The Codex folder was committed after its audit with home-directory paths replaced in ten files; its run logs and large regenerable files are not in the repository.

"""

# ---- apply to the TeX
tex = once(tex, "% PAPER72 v1.4 (2026-11-14; v1.3 2026-11-13,", "% PAPER72 v1.5 DRAFT (2026-11-14, not deposited; v1.4 2026-11-14, deposited 2026-11-14 UTC; v1.3 2026-11-13,", "comment line")
tex = once(tex, "version 1.4, 2026-11-14 (v1.3: DOI 10.5281/zenodo.24212016;", "version 1.5, 2026-11-14 (v1.4: DOI 10.5281/zenodo.24221457; v1.3: DOI 10.5281/zenodo.24212016;", "version line")
tex = once(tex, "No hit is added.\nWe list what is open", "No hit is added.\n" + ABSTRACT.strip("\n") + "\nWe list what is open", "abstract")
m = re.findall(r"\\paragraph\{Local correction, 2026-11-14 \(not deposited\)\.\}[^\n]*\n\n", tex)
if len(m) != 1: sys.exit(f"local-correction paragraph not unique ({len(m)})")
tex = tex.replace(m[0], CHANGED)
tex = line_after(tex, r"\item Version 1.4, for $f$ and the weak-lensing amplitude (Section~10):", DECIDE, "what would decide it")
tex = after_line(tex, r"\textbf{$f$, edge by edge.}", EDGE, "f, edge by edge")
tex = after_line(tex, "Version 1.4 changes no label of an earlier lane and adds no hit.", LEAVES10, "Section 10.4")
tex = once(tex, "FAILS & 5 & 5\\\\", "FAILS & 4 & 4\\\\", "counts table, FAILS")
tex = once(tex, "DEPENDS ON AN UNTESTED ASSUMPTION & 4 & 4\\\\", "DEPENDS ON AN UNTESTED ASSUMPTION & 5 & 5\\\\", "counts table, DEPENDS")
tex = after_line(tex, "CJ1's scorecard grades nothing new:", COUNTS, "counts sentence")
tex = after_line(tex, "untouched by rule 6, form B's fails on X-COP's two-sided amount", ROW15, "row 15 in the fails list", contains=True)
sec = SECTION.replace(" BRACKETS_GO_HERE", (" " + BRACKET_SENTENCE) if BRACKET_SENTENCE else "").replace("CJ1AUDIT_GOES_HERE", CJ1_AUDIT)
tex = once(tex, r"\section{Our own estimates}", sec + r"\section{Our own estimates}", "Section 11")
tex = after_line(tex, "Recorded before the numbers that tested them.", ESTIMATE, "estimates")
tex = once(tex, "\n\\end{document}", "\n" + METHOD + "\\end{document}", "method")

# ---- the audit: the version 1.5 block
T = []
def t(frag, path, lit): T.append((frag, path, lit))
t("version 1.5, 2026-11-14 (v1.4: DOI 10.5281/zenodo.24221457", "P72z", '"version": "1.4", "doi": "10.5281/zenodo.24221457"')
t("after version 1.4 was deposited (DOI 10.5281/zenodo.24221457)", "P72z", '"deposition_id": 24221457')
t("by a factor that runs from 0.48 to 1.83 on the forest's haloes", "XJC", "s over the forest halo grid runs from 0.48 to 1.83")
t("$s$ runs from 0.48 to 1.83", "XJC", "s over the forest halo grid runs from 0.48 to 1.83")
t("it is 0.47 to 0.93 at $f=1.25$, 0.57 to 0.78 at $f=2$ and 0.69 to 0.72 at $f=3$", "XJR", "s = 0.47 to 0.93 at f 1.25, 0.57 to 0.78 at f 2, 0.69 to 0.72 at f 3")
t("The median galaxy keeps 0.59 to 0.75 of the law's halo", "XJA3", "the median galaxy keeps 0.59 to 0.75 of the law's halo")
t("PASS/PASS at $f=1.25$ (rms 0.0646/0.0640 against lines of 0.0660/0.0658)", "XJR", "| 1.25 R_fold | PASS, rms 0.0646 | PASS, rms 0.0640 | 0.75 / 0.68 | 0.79 / 0.75 |")
t("PASS/PASS at $f=1.25$ (rms 0.0646/0.0640 against lines of 0.0660/0.0658)", "XJR", "rms at most 0.0660 / 0.0658 for all galaxies")
t("FAIL/PASS at $f=2$ (0.0682/0.0654)", "XJR", "| 2 R_fold | FAIL, rms 0.0682 | PASS, rms 0.0654 | 0.62 / 0.59 | 0.85 / 0.78 |")
t("FAIL/FAIL at $f=3$, where the massive spirals miss their own line on both footings", "XJR", "| 3 R_fold | FAIL, rms 0.0691, massive 0.0480 | FAIL, massive 0.0469 | 0.70 / 0.70 | 0.80 / 0.75 |")
t("the law itself reads 0.0560/0.0558", "XJR", "the law itself reads 0.0560 / 0.0558")
t("has risen from 0.58/0.52 to between 0.75 and 0.87", "XJA3", "with the fitted median mass-to-light ratio rising from 0.58 / 0.52 to 0.75 to 0.87")
for key, nm in (("E1", "E1 (frozen) | R_fold, the first caustic"), ("E2", "E2 (frozen) | 2 R_fold"), ("E3", "E3 (frozen) | 3 R_fold"),
                ("Ezv", "Ezv (frozen) | zero-velocity surface, 2.3 to 3.5 R_fold"), ("E0.5", "E0.5 (A3) | 0.5 R_fold"),
                ("Ec3", "Ec3 (A5) | third caustic, 0.47 to 0.51 R_fold at z 2.2 to 4.4"), ("Ec2", "Ec2 (A5) | second caustic, 0.60 to 0.65 R_fold"),
                ("E0.75", "E0.75 (A3) | 0.75 R_fold")):
    frag = D[key][0] + "; " + LAB[key][0] + " & " + D[key][1] + "; " + LAB[key][1]
    t(frag, "XJR", "| " + nm + " | " + D[key][0] + " |"); t(frag, "XJR", "| " + D[key][1] + " |")
t("THE HOLD DOES NOT SURVIVE THE EXACT JUNCTION", "XJR", "| **Q1, the junction (frozen)** | THE HOLD DOES NOT SURVIVE THE EXACT JUNCTION | THE HOLD DOES NOT SURVIVE THE EXACT JUNCTION |")
J23 = "FZS1's junction reads 0.024/0.029 at $f=2$ (FRZ6R) and 0.572/0.691 at $f=3$ (FWN1R); the exact junction is 671/878 and 75/113 times higher"
t(J23, "XJR", "where the record's junction reads 0.024 / 0.029 (FRZ6R's J2), a factor 671 / 878")
t(J23, "XJR", "where the record's reads 0.572 / 0.691 (FWN1R's J3), a factor 75 / 113")
t("2.3 to 3.5 fold radii at the forest's redshifts; it FAILS on both footings", "XJR", "| **Q2, the zero-velocity surface (frozen)** | FAILS (the zero-velocity surface) | FAILS (the zero-velocity surface) |")
t("The fold radius itself is not resolved on canonical and FAILS on alt", "XJR", "| **Q2, the fold radius (frozen)** | NOT RESOLVED (the fold radius): NO VERDICT | FAILS (the fold radius) |")
t("equals FWN1R's stored parts in all 96 files and still fails (8.834/10.897)", "XJR", "| J5 (control, the record's junction) | 5 R_fold | 8.834 (0.333) | fails, as FWN1R stored it | 10.897 (0.564) | fails, as FWN1R stored it |")
t("Both graders were re-run from the committed parts into a separate folder with identical output", "XJR", "every number and label is identical (0 differences in each grade file)")
t("put D at 0.02 to 0.5 at the fold radius, 0.1 to 3 at twice it, 2 to 20 at three times it and 0.5 to 10 at the zero-velocity surface", "XJC", "E1 0.02 to 0.5; E2 0.1 to 3; E3 2 to 20; Ezv 0.5 to 10.")
t("Every one came out 5 to 30 times higher", "XJR", "The estimate was wrong by a factor 5 to 30 at every frozen radius")
t("D reaches 4 at $f=1.01$ on canonical and 0.89 on alt", "XJR", "at f = 1.01 canonical (0.96 to 1.08 for D + 2 SE and D - 2 SE) and at f = 0.89 alt (0.84 to 0.95)")
t("whose 24 runs reproduce FLD1's stored series exactly", "XJR", "all 24 runs reproduce FLD1's stored series exactly")
t("The second is at 0.68 of the fold radius today and 0.60 to 0.65 at $z$ 2.2 to 4.4; the third at 0.535 and 0.47 to 0.51", "XJR", "The second caustic is at 0.68 R_fold today and 0.60 to 0.65 at z 2.2 to 4.4; the third at 0.535 today and 0.47 to 0.51")
t("A WINDOW IS LEFT: f in [0.5, 0.75]", "XJR", "| **Q3, the window under the exact junction (A3, post hoc)** | A WINDOW IS LEFT: f in [0.5, 0.75] | A WINDOW IS LEFT: f in [0.5, 0.75] |")
Q4 = "HOLDS WITH NO FREE CONSTANT for the second caustic and for the third"
t(Q4, "XJR", "| **Q4, the third caustic (A5, post hoc)** | HOLDS WITH NO FREE CONSTANT (the third caustic) | HOLDS WITH NO FREE CONSTANT (the third caustic) |")
t(Q4, "XJR", "| **Q4, the second caustic (A5, post hoc)** | HOLDS WITH NO FREE CONSTANT (the second caustic) | HOLDS WITH NO FREE CONSTANT (the second caustic) |")
t("(the largest ratio is 0.77; 0.60 for the second)", "XJR", "(largest ratio 0.77, UGC00128; 0.81 at mass-to-light 0.3, UGC09133), the second (0.60)")
t("(0.391 of the fold radius at most, against a third caustic at 0.446 or more)", "XJR", "is 0.391 on both footings; the smallest third-caustic ratio over z 0 to 2.7 is 0.446")
t("where FZS1's junction fails it at $f=1$", "XJR", "The record's junction fails this gate at f = 1 (+2.003 / +2.037)")
MW = r"the third caustic sits at 99\,kpc and the medians of the pulls are unchanged, $+1.40$/$+1.47$ for the field stars against $+1.39$/$+1.57$ for the law at every radius"
t(MW, "XJR", "exact junction at the third caustic +1.40 / +0.75 and +1.47 / +0.86")
t(MW, "XJR", "the law at every radius +1.39 / +0.85 (canonical) and +1.57 / +1.18")
ML = "the third caustic reads 2.87/6.37 and the second 8.15/19.04 against the line of 4"
t(ML, "XJR", "| Ec3 | 2.87 PASS | 6.37 FAIL |"); t(ML, "XJR", "| Ec2 | 8.15 FAIL | 19.04 FAIL |")
t("a hit found by looking, from a family of two", "XJR", "found by looking, from a family of two")
A6 = "today's rotation curves also allow the fourth caustic, at 0.448 of the fold radius, and are cut at the fifth by one galaxy"
t(A6, "XJR", "The fourth caustic is at 0.448 R_fold today and the fifth at 0.389")
t(A6, "XJR", "no galaxy's last measured point lies beyond the fourth caustic (largest ratio 0.916, UGC00128); one lies beyond the fifth (UGC00128, 1.055)")
BL = "finds no galaxy beyond either caustic (the largest ratios 0.602 and 0.767) and reads the same matter-level numbers, 8.146/19.037 and 2.872/6.368"
t(BL, "XRrc", "k 2, Y 0.5: 0 of 175 beyond R_2(0); worst UGC00128 0.602"); t(BL, "XRrc", "k 3, Y 0.5: 0 of 175 beyond R_3(0); worst UGC00128 0.767")
t(BL, "XRc0c", "chain SEc2: D_rec 8.14627"); t(BL, "XRc0c", "chain SEc3: D_rec 2.87212")
t(BL, "XRc0a", "chain SEc2: D_rec 19.0369"); t(BL, "XRc0a", "chain SEc3: D_rec 6.36842")
# 11.4
t(r"$[J^r]-\dot R\,[J^t]=0$", "CXJ", "[J^r] - Rdot [J^t] = 0.")
t(r"$N_{\rm out}(v_{\rm out}-\dot R)=N_{\rm in}(v_{\rm in}-\dot R)$", "CXJ", "N_out(v_out-Rdot) = N_in(v_in-Rdot).")
NA = "is 3e-7 to 5e-7 of the advective flux for a Milky-Way-mass system at 100\\,kpc (the audit), and 1.8e-6 to 4.7e-6 outside the caustics in CSD1's evaluation, where it supplies 4.8e-7 to 1.3e-6 of the flux that is missing"
t(NA, "CXN", "3e-7 to 5e-7 for a Milky-Way-mass system at 100 kpc")
t(NA, "CSD", "eps = |c lambda P| / |N v| is 1.8e-6 to 4.7e-6 outside")
t(NA, "CSD", "the channel supplies 4.8e-7 to 1.3e-6 of it")
t("The note's sentence that full polarization transport could change the conclusion below is wrong in the weak field", "CXN", '**WRONG in the weak field:** the sentence "Full polarization transport can change that conclusion"')
SG = "the law's density just inside the caustic is below the density just outside in 3,706 and above it in 3,373"
t("Over 7,110 snapshots of XJ1's two caustic layouts", "REV", "The recount gives 7,110 rows, 27 with zero outer density, 3,706 with ratio < 0.999, 3,373 with ratio > 1.001 and 4 near-equal.")
t(SG, "REV", "3,706 with ratio < 0.999, 3,373 with ratio > 1.001")
AM = "the charge inside the third caustic is 0.0086 to 0.068 of what the law's halo needs there"
t(AM, "CSD", "| 8 | 0.0171 | 0.0114 | 0.0107 | 0.0095 | 0.0155 | 0.0103 | 0.0097 | 0.0086 |")
t(AM, "CSD", "| 11.5 | 0.0681 | 0.0473 | 0.0443 | 0.0432 | 0.0616 | 0.0423 | 0.0390 | 0.0379 |")
t("the label is SHORT AT CAUSTIC 2 / SHORT AT CAUSTIC 3 on both footings", "CSD", "| **SHORT AT CAUSTIC 2 / SHORT AT CAUSTIC 3** (also k = 1 and 0.5 R_fold) | **SHORT AT CAUSTIC 2 / SHORT AT CAUSTIC 3** (same) |")
SC = "the same patch turns around 2.0 times with the law on and delivers 0.017 to 0.121"
t(SC, "CSD", "the same seeded patch turns around 2.0 M_b, not 59.3")
t(SC, "CSD", "| 9 (D_3) | 0.0443 | 0.0273 | 0.0240 | 0.0195 | 0.0402 | 0.0246 | 0.0216 | 0.0173 |")
t(SC, "CSD", "| 11.5 | 0.1208 | 0.0764 | 0.0691 | 0.0634 | 0.1093 | 0.0695 | 0.0624 | 0.0565 |")
t("tuned to turn around 59.3 times the baryon mass with the law off", "CSD", "law-off confirm 59.32 M_b turned around against 59.49")
SR = "the ratio is 0.49 to 1.67, under at low mass and over at high mass (it crosses 1 at $\\log M_b$ 10.09/10.42 today)"
t(SR, "CSD", "from 0.49 to 1.67 of it, under at low"); t(SR, "CSD", "k = 3 crossing at log M_b 10.09 at z 0"); t(SR, "CSD", "k = 3 crossing at 10.42")
t("The static balance of that shell equation is the law exactly", "CSD", "So the static balance of FLD1's equation is the law")
t("The audit checked six of the note's eight example rows", "CXN", "Six of eight rows were checked and match to the last digit with the halo code's G")
t("is by the same session that wrote it", "CXN", 'The "independent" reviewer is a subagent of the same session, so it is not independent of that session')
# 11.5
t("FWN1's build reads 4.34/5.37 and cannot tell", "FW2", "D is 4.34 / 5.37 (canonical / alt)")
t("FWN1R's build reads 3.18/3.71", "FW2", "D is 3.18 / 3.71.")
t("the split holds at $f=3.5$ (1.50/1.78) and fails at $f=4.5$ (5.62/6.62)", "FW2", "f = 3.5 reads 1.50 / 1.78 and holds with room. f = 4.5 reads 5.62 / 6.62 and fails with room.")
t("$f=4$ is NOT RESOLVED on both footings", "FW2", "| alt | NO VERDICT (unresolved at 12 seeds: D 5.37, SE 1.33) | NO VERDICT, FRAGILE (lam_x0.5; gam_1.6; tau_x0.9) | **f = 4 NOT RESOLVED** |")
t("MEASURED SLOPE MAKES A PASSING BIN FAIL [40-55 COLD], robust only on the rotation-curve stellar mass on alt", "RRR", "| framework line, rotation-curve stellar mass | alt | **MEASURED SLOPE MAKES A PASSING BIN FAIL [40-55 COLD]** | robust: every bracket gives the same head word (bin lists vary) |")
t("DESI's NFW halo gets the same label", "RRR", "| H (DESI NFW), reported | - | MEASURED SLOPE MAKES A PASSING BIN FAIL [40-55 COLD] | fragile: other model -> FAIL REMOVED |")
t("reads AMOUNT CONSISTENT ON BOTH SIDES on both footings", "CJS", 'the blind RB1R "AMOUNT CONSISTENT ON BOTH SIDES" on both footings')
t("the FAIL it had quoted is a reading with half the share kept out of the core, which is not form B", "CJS", 'PD1 "FAIL +0.16" is its reading with half the share kept out of the core, which is not form B')
t("Its word for the completed form changes from FAILS to DEPENDS ON AN UNTESTED ASSUMPTION", "CJS", "its word changes from FAILS to DEPENDS ON AN UNTESTED ASSUMPTION, on the owner's decision of 2026-11-14")
t("reads LOW ROWS COUNT AGAINST B on both footings", "CJS", 'the blind RB2R "LOW ROWS COUNT AGAINST B" on both footings')
t("is mostly outside the measurements, while $\\gamma$ 1.2 and 1.6 are inside them", "CJS", "is mostly outside the measurements; gamma 1.2 and 1.6 are inside them")
t("no longer FAILS", "CJS", "The counts move by one (FAILS 4, DEPENDS ON AN UNTESTED ASSUMPTION 5)")
t("an assembly; grades nothing; NOT ADOPTED & audit " + CJ1_AUDIT, "CJS", CJ1_AUDIT_LIT)
# estimates and method
t(r"gave the exact junction at the fold radius a 75\,\% chance of holding the forest", "XJC", "Labels: E1 HOLDS 75 %")
t("The headers of XJ1's criteria and of its first amendment carry clock times that were guesses and are wrong; the commit times are the record", "XJR", "both were guesses and are wrong.")
t("six of its twelve bins were read while it was stopped; its result records that no criterion, case or amendment was written after that look", "XJR", "No criterion, case, gate or amendment was written or changed after that look")
t("with home-directory paths replaced in ten files", "CXN", "Home-directory paths were replaced by")
for b in BRACKET_TUPLES: t(*b)
BLOCK = '''# ---------------- version 1.5: XJ1 (the junction), CSD1, the Codex correction's audit, FWN2, RRL1R, CJ1's tenth update ----------------
XJR = D14 + "XJ1_exact_junction_zero_velocity_surface/RESULT.md"; XJC = D14 + "XJ1_exact_junction_zero_velocity_surface/FROZEN_CRITERIA.md"
XJA3 = D14 + "XJ1_exact_junction_zero_velocity_surface/AMENDMENT_A3.md"
XRrc = D14 + "XJ1R_blind_caustic_junction/xj1r_rc.out"; XRc0c = D14 + "XJ1R_blind_caustic_junction/xj1r_c0_canonical.out"; XRc0a = D14 + "XJ1R_blind_caustic_junction/xj1r_c0_alt.out"
CSD = D14 + "CSD1_charge_delivery_at_the_caustic/RESULT.md"
CXJ = "codex_mass_budget_2026_11_14/latest_review/JUNCTION_THEOREM.md"; CXN = "codex_mass_budget_2026_11_14/AUDIT_NOTE_2026_11_14.md"
REV = "reviews/codex_mass_budget_audit_2026_11_14/README.md"
FW2 = D14 + "FWN2_forest_flux_split_f4/RESULT.md"; RRR = D14 + "RRL1R_blind_halo_slope_regrade/RESULT_BLIND.md"
L += [
__TUPLES__
]
'''
VARS = {k: k for k in ("P72z", "XJR", "XJC", "XJA3", "XRrc", "XRc0c", "XRc0a", "CSD", "CXJ", "CXN", "REV", "FW2", "RRR", "CJS")}
rows = [f" ({frag!r}, {VARS[p]}, {l!r})," for frag, p, l in T]
aud = once(aud, '# (fragment in the TeX, JSON file, key path, format, the number as the TeX prints it)\nJ = [', BLOCK.replace("__TUPLES__", "\n".join(rows)) + '# (fragment in the TeX, JSON file, key path, format, the number as the TeX prints it)\nJ = [', "audit block")
aud = aud.replace("version 1.4, 2026-11-14 (v1.3: DOI 10.5281/zenodo.24212016", "version 1.5, 2026-11-14 (v1.4: DOI 10.5281/zenodo.24221457; v1.3: DOI 10.5281/zenodo.24212016")
aud = once(aud, '("version line", "Working note (PAPER72), version 1.4" in TEX)', '("version line", "Working note (PAPER72), version 1.5" in TEX)', "audit version rule")
aud = once(aud, '("FAILS & 5 & 5", CJS, "FAILS 5;")', '("FAILS & 4 & 4", CJS, "FAILS 4;")', "audit counts, FAILS")
aud = once(aud, '("DEPENDS ON AN UNTESTED ASSUMPTION & 4 & 4", CJS, "DEPENDS ON AN UNTESTED ASSUMPTION 4;")', '("DEPENDS ON AN UNTESTED ASSUMPTION & 5 & 5", CJS, "DEPENDS ON AN UNTESTED ASSUMPTION 5;")', "audit counts, DEPENDS")
if INPLACE:
    open(TEXP, "w", encoding="utf-8").write(tex); open(AUDP, "w", encoding="utf-8").write(aud)
    print(f"wrote IN PLACE: the paper's TeX ({len(tex.splitlines())} lines) and audit ({len(T)} new checks)")
else:
    # the copy reads out/'s TeX and finds the repository root from git, not from its own depth
    aud = once(aud, 'HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))',
               'HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = subprocess.run(["git", "-C", HERE, "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()', "audit root")
    aud = once(aud, 'TEX = open(os.path.join(HERE, "PAPER72_law_with_cold_dark_energy_counted_once_2026.tex"), encoding="utf-8").read()',
               'TEX = open(os.path.join(HERE, "PAPER72_v1_5_DRAFT.tex"), encoding="utf-8").read()', "audit tex path")
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    open(os.path.join(HERE, "out", "PAPER72_v1_5_DRAFT.tex"), "w", encoding="utf-8").write(tex)
    open(os.path.join(HERE, "out", "PAPER72_audit_v1_5.py"), "w", encoding="utf-8").write(aud)
    print(f"wrote out/PAPER72_v1_5_DRAFT.tex ({len(tex.splitlines())} lines) and out/PAPER72_audit_v1_5.py ({len(T)} new checks)")
print("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
