# Z6 predeclaration (written before any Z6 script was run)

Claim under referee (lane X3, script x04, README Part B): the record's action requirement
"kappa = 1/2 <=> M1 = (4/3) t_Lambda, M1 = (2/3) c/a0" is IDENTICAL, for a sharp retarded 1/r (Sciama)
kernel with weight r dr on [0, T = R_c/c], to R_c = c^2/a0 = 2 R*; "the record's memory kernel IS
Sciama's kernel if its cutoff is the Rindler distance of a0".

What I read before predeclaring (disclosed): X3's README and x04; the record's paper
opus_48_extended_research/papers/RAPIDITY_GAP_MI_ACTION.md (v6); real_research/reviews/
mi_a0_from_one_line_2026.py, mi_N_count_and_kappa_iff_2026.py, mi_local_source_for_K_2026.py,
mi_kernel_localisation_2026.py, mi_wightman_first_moment_2026.py, mi_rapidity_kernel_solved_2026.py
(headers). Hand expectations (NOT results): K is a worldline memory kernel in PROPER-TIME lag s acting
on the rapidity gap, free normalisation N = M0 = int K ds (>= 2.1e6), M1 = int s K ds; Sciama's kernel at
R_c = 2 R* has strength I = 2 pi G rho R_c^2/c^2 = 8 pi, not 1; the record's short-memory condition
lambda*Omega <~ 0.1 is violated by T = c/a0 by ~3e3 in the Milky Way.

Objects computed (each by a committed sympy/mpmath script with controls):
 O1 the record's kernel: support, normalisation, M0, M1, closed form and limits, the (2/3) renormalisation.
 O2 moments and the cutoff map R_c(shape, M0) for: sharp r dr, uniform, exponential, Yukawa/gamma-2.
 O3 structure: Sciama force = linear retarded response of a; expansion M0 a - M1 adot + ...; record's
    Theta = int K theta with theta ~ |a| s/c (nonlinear, magnitude); relation between the two; step responses.
 O4 regimes: long/short memory for a T = c/a0 kernel, Mercury/Earth/Milky Way, the record's own mu_2 and
    Delta bound; Sciama-strength versus required strength.

Verdict rule (fixed now):
 TRUE            = (i) the arithmetic M1 = (2/3)T holds AND (ii) the kernel-level map record-K <-> Sciama weight
                   is canonical (independent of shape/lag convention) AND (iii) the strength M0 equals Sciama's
                   physical strength at that cutoff AND (iv) the record's regime constraints are met.
 TRUE ONLY FOR THE MOMENT = (i) holds but at least one of (ii)-(iv) fails.
 FALSE           = (i) itself fails (mis-computed moment).
Any check whose failure would flip the verdict is written as an assertion or a control that must trip.
No person's name appears in any file. No record file is edited; nothing is committed.
