# CAPSTONE: local MOND lensing REQUIRES an unremovable preferred frame (2026-08-29)
# 108,000-candidate exhaustive covariant local search. Compiler commit 9c52966f.

## What was searched
65-operator covariant local basis (ADM geometric + aux scalar chi + vector A_mu + STF tensor + 8-param
matter frame map), 108,000 candidates (100k main + 8k corrected re-run), 9 sampling families incl. 3
targeted root-finding families. Anti-hiding discipline: mu(y) must be an OUTPUT of eliminating an algebraic
carrier, never an input (the compiler REPORTS mu, it is not handed 1-e^-y). Full mortality table + reached-
gate profile + physics-vs-solver split in mc_report.out. Self-test 5/5, validation 19/19.

## Result: ZERO survivors. Last gate standing = Gate-PPN (preferred-frame vacuum).
The near-misses are not scatter -- they are ONE family. 61 candidates cleared MOND+SLIP+ghost; 46 are
LITERALLY IDENTICAL:  L = -chi(grad phi)^2/2 + chi^3/3 + lam(A^2+1) - F^2/4,  matter on
  g~ = e^{2 M1 phi}[ g_mn + (M3 + M5 phi) A_m A_n ].
The tuned ratio M5/M1 = 4.000000 (min 3.9997, max 4.0002), matching the exact symbolic prediction
M5 = 4 M1 - 2 M1 M3 to < 9e-9. **THIS IS BEKENSTEIN'S DISFORMAL RELATION.** The screen was NOT given it --
it FOUND it by root-finding the zero of the frame-slip. The unique local lensing fix is Bekenstein/TeVeS.

## THE THEOREM (exhaustively searched, this is the capstone):
Every lensing-fixing candidate has a PREFERRED-FRAME VACUUM (boost-breaking |A_0| != 0; ZERO of 59 are
boost-invariant; all die at Gate-PPN). And the preferred frame is NOT REMOVABLE: switching off the operator
that pins A_0 collapses the lensing fix (56/60 lose the Newtonian limit, 3 fall back to slip=2, 0 survive).
The cancellation is proportional to A_0^2 => **the preferred frame IS the lensing mechanism, not a
decoration.** => within the LOCAL, <=2-derivative, covariant, single-metric basis:
  { correct MOND lensing }  ==>  { unremovable preferred-frame carrier }.
This is the exhaustively-searched form of the lensing<->preferred-frame PINCER the whole session found.

## SCOPE / honest caveats
- EXCLUDED (documented, no silent caps): NONLOCALITY (k^-2 kernels) -- the DEFW/F+ escape, a SEPARATE
  programme (the response-space arm + FROZEN_PRIMITIVE.md cover it); >2 derivatives; torsion; parity-odd;
  free functions of the carrier; 2nd copies of an irrep.
- 17,551 of 76,027 chain-entrants were SOLVER non-convergence (undecided, NOT refuted); the 58,476 physics
  kills are decisive and the near-miss family is fully characterised.

## THE ESCAPE (converges with the khronometric finding -- see ../theory_discovery/):
The pincer says you CANNOT remove the preferred frame. The escape is NOT to remove it but to SCREEN its
observable effect: make the preferred-frame COUPLING equal the MOND deviation (1-mu)=e^-y, so alpha_1,alpha_2
~ e^-y self-screen (beaten by ~30000 orders at Solar-System y). That is the khronometric/Horava + MOND
survivor (3 DOF), whose full health is under test (KHRONOMETRIC_MOND_GAUNTLET). Bekenstein's frame is
UNSCREENED (constant disformal) => dies at Gate-PPN; the khronometric MOND-coupled frame is SCREENED => the
one surviving direction.
