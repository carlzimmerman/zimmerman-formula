# Owner decision, 2026-11-07 evening: accept the corrected-kernel labels as standing

Owner's words, in the orchestrator session: "Accept, ship v1.3".

Scope. The CMB-lensing Limber integrator used since lane QX3 (`limber_ratio`) omitted the lensing potential's k^-4.
The error was found by CK4 (ea06286d99), confirmed from the code by the Field equations session, and confirmed by an
independent rebuild with no shared code (GL2, d0c3692fc6: restored shape within 7e-4 of CLASS; dropped, 0.045-33.9).
The affected labels were re-read with the kernel corrected by GL1 (4699adbbd7, sector side), GL3 (e3be44f619, web
line) and GL4 (e14bb102a5, QX15 cells); with the error re-inserted every recorded number reproduces (KA0, max |d| 0).

Decision. The corrected values become the standing labels for every row GL1, GL3 and GL4 report as MOVES; rows they
report as HOLDS keep their labels with the corrected numbers noted. In PAPER70 the twenty-one rows marked "re-stated
pending owner" read "re-stated (owner 2026-11-07)". The original frozen RESULT files are not edited; the erratum
section keeps old and corrected values side by side. No label outside the GL1/GL3/GL4 lists changes.

Moves accepted (both footings): QX3 iter3 FAIL -> member found (beta 0.8, mu0 1259); QX7 iter_3 no window -> G2'
window 31/31; QX10 iter_1 NO VERDICT -> PASS C1-C4; CE2 GL gate PASS -> NO VERDICT (overall FAIL holds); SV5 iter_1 W2
PASS -> FAIL (class W no-go holds); SV5 T0.2 late Jeans tolerated below z 2.0 / 1.5 / 0.75; SV5 iter_3 H-native FAIL ->
WINDOW-CONDITIONAL (H-flat no-go holds); QX28 G6b FAIL -> PASS (G6 holds via G6a); FA2 C2 L_max 0.3 -> 1.0 Mpc (label
holds); QX15 C3 TENSION -> PASS. Holds with corrected numbers: QX3 iter2 (gap x500 -> x7.9), QX7 iter_4 (clusters
0/857), KD1 G9a / SE1 arm (a) (wall 1 holds on the BBN side), CK4 GL, SV5 W1 and every web row (x18-39 over 1.072),
OQ1/OQ2, EW2, WL1 (kernel-free), QX27, QX29, QX31, LD1 (kernel-free), QX15 C1/C2/C4/P1.

Consequence. None of the accepted moves opens a door: the kernel-free cluster, group and KiDS rows stand, wall 1
holds, every web row still fails. The record's conclusions (DEDUCTION sections 7-10) are unchanged. With this
decision no row in the record is marked pending. Adopts nothing beyond the labels named. Kappa = 1/2 FITTED; not
theory closed.
