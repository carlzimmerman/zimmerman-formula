# DR4_orbit_count_memory: FROZEN CRITERIA (committed alone, before any script or number)

kappa = 1/2 FITTED, unused here. Cold dark energy is a gravitating field component, no particle. Not theory closed. Nothing here says the data favour the framework. No a0 in the cold sector. One thread, nice 15, seconds, no download.

## Question
An outside text claims a Deser-Woodard non-local box^-1 R memory, "tracked as" N_dyn = (t0 - t_coll)/t_dyn(r), separates z = 3 filaments and z = 0 clusters (N_dyn <= 1) from galaxy discs (N_dyn 30-50), and so evades the Matching Theorem (Zenodo 22261001, `opus_48_extended_research/papers/THE_MATCHING_THEOREM.md`). Is box^-1 R an orbit count? Does either quantity separate the three sites? Is N_dyn a covariant local field?

## Record check (done before this file)
- CFG123 (+ referee CFG153, CFG230 row D09): Deser-Woodard/RR static response is a scoped no-go for the phantom density; DW linear static point mass is a pure G rescaling plus slip; it leaves "f with a branch point at Xbar(t)" untested and says that would postulate the target. CFG70: a memory kernel's time scale doesn't change the static reaction.
- No lane found gates on N_dyn or an orbit count. So the gate is new, its operator is not.

## Rules
**R-X (the operator).** Signature (-+++), retarded zero data, X = box^-1 R. Background: X'' + (3 + H'/H) X' = -R/H^2 in ln a, R = 8 pi G (rho_m + 4 rho_DE), start deep in radiation with X = X' = 0. Static well: laplacian(dX) = 8 pi G rho / c^2, so dX = 2 Phi / c^2. Total X = Xbar(t) + 2 Phi(r)/c^2. Evaluated: (a) SPARC galaxies, all r, Phi from Vobs inward, flat V_last out to R200 = V_last/(10 H0), then -V_last^2 beyond; (b) X-COP, Phi from M_FORW to R200 (json), -GM200/R200 beyond; (c) filament, z = 3, delta = 1, 10, 100, uniform sphere radius L = 0.1 and 1 Mpc proper, Phi = -2 pi G delta rhobar L^2. Worldline: a circular orbit over N orbits, dX/dN at fixed t is 0 by symmetry; only Xbar drift remains, X'(ln a) H T, reported.

**R-N (the claim's quantity).** T(r) = 2 pi r / v_c(r), chosen because it's the convention under which the claim's 30-50 can arise; r/v_c multiplies every N by 2 pi and moves all sites alike. t_coll = t(z_f), z_f from the record's native half-mass table, X73 `sigma_coll_table`, bg A: 1e11 1.1365, 1e12 0.9440, 1e13 0.7507, 1e14 0.5615, 1e15 0.3850, linear in lg M, held flat outside. M200: X-COP json; SPARC V_last^3/(10 G H0). Ceiling variant: age t0 for every well, inner-region-older worry stated either way. SPARC: all 175 rotmod files, all points r > 0, Vobs > 0, v_c = Vobs. X-COP: 12 clusters, M_FORW, the record's X-COP grid x = r/R500 in 0.1, 0.2, 0.3, 0.5, 0.7, with 30, 50, 100 kpc and R500, R200 reported only. Cross-check on M_NFW. Filament: delta as above, T = sqrt(3 pi/(G rho_tot)), age t(z = 3) as ceiling. Unbound background: same formula, delta = 0, z = 0, 3, 16.

**Background.** Native: Om 0.2976016, h 0.6856427 (GS1/GC2 in X73); Omega_r h^2 = 4.15e-5 declared; constant rho_DE, flat. Disclosed: this drops the framework's evolving rho_DE detail; X' and ages move at the percent level at most and no line here is that close unless reported otherwise.

## Pass lines (a separator "survives" only as below)
- **L1, X-SEP.** A monotonic function of total X can isolate discs from both filament and cluster only if discs aren't strictly between them. Also needs the disc-cluster gap at z = 0 to exceed the disc population's own spread. Both, or fail.
- **L2, ORBIT.** X is an orbit count only if dX/dN differs between sites by the ratio of their N per unit time. Reported; the line is that site ratio of (X drift per Hubble time) tracks site ratio of N within a factor 2.
- **L3, CLAIM.** At N_c = 1, the one threshold that adds no number: >= 90 % of X-COP grid points have N <= 1 and >= 90 % of SPARC points have N > 1. Both, on z_f and on ceiling.
- **L4, ANY THRESHOLD.** Diagnostic, threshold-free: min over N_c of balanced misclassification, SPARC points vs X-COP grid. <= 0.05 needed on both z_f and ceiling. Passing L4 and not L3 means a threshold that has to be FITTED: not "no new number", so labelled FITTED and doesn't count as surviving.
- **L5, FILAMENT PAIR.** Filament ceiling N at delta = 100 below SPARC's 5th percentile. Reported separately, since that pair can pass while the cluster pair fails.
- **L6, COVARIANCE.** Derive what field equation gives N_dyn; name each added field, vector, and non-analytic function. Single-valued at multistreaming? State it. Not a number; a statement with its reason.

## Labels
- **ARGUMENT FAILS**: L3 fails, or L1 fails and N needs an added field with a fitted threshold. Numbers reported; no gating rule graded.
- **SEPARATOR SURVIVES**: L3 passes on both variants and a stated field carries it. Then and only then a separate commit freezes a gating rule, graded on the record's lines (SPARC rms <= 0.110, Upsilon 0.50-0.80 both backgrounds, tilt <= 0.15, 15 keys |Z| <= 2 on +0.005, X-COP, groups, LITTLE THINGS), after reproducing NR3's EM1-off baseline to |d| <= 1e-6.
L5 passing alone gets the sub-label [FILAMENT PAIR ONLY].

## Checks (failed check: no verdict)
- K1 matter era X' -> -2, |d| <= 1e-3, in a pure matter run.
- K2 Xbar(0) on CFG123's parameters (H0 67.36, Om 0.3153, Or h^2 4.15e-5; solver check only, not a grade) against its U-bar 16.035: |d| <= 2 %; CFG123's is on the RR background, hence not tighter.
- K3 laplacian inverse on an NFW: numerical retarded-static kernel integral against 2 Phi closed form, |d| <= 1e-4.
- K4 age: numeric t(z) against flat matter + DE closed form with radiation off, |d| <= 1e-6.
- K5 N at R200 for a virial sphere equals (t0 - t_f) * 10 H0 / (2 pi), |d| <= 1e-10, SPARC path.
- K6 z_f table re-read from X73's results json, exact. X-COP: M_FORW at json R500 against json M500, median ratio within 0.8-1.25.
- K7 SPARC files read: 175; points count reported. All 12 X-COP read.

## MUTATE (separate output)
MUTATE=1: X-COP v_c divided by 30, and X-COP depth set shallower than filament. L3 must flip to pass on the X-COP side and L1's order must change; if the grader doesn't move, no verdict.

## Disclosed, not blind
Many results known. Before this file I did hand estimates: N about 50-60 at the solar radius, about 20 at 30 kpc in a rich cluster, about 1-2 at R500, and X about 2 Phi/c^2 with discs between filament and cluster. Those shaped my expectation, not these lines; the lines are the claim's own (N_c = 1) plus a threshold-free overlap. z_f is favourable to the claim for clusters, since the half-mass time understates how old a core is.

## Expectation on record, mine
ARGUMENT FAILS. X is a potential plus a clock on the Hubble time; discs sit between filament and cluster; X-COP N well above 1 at all x <= 0.5; L5 likely passes; L4 possibly close to passing outside the cores but the threshold fitted. N_dyn needs a clock scalar plus a flow vector and sqrt(R), and isn't single-valued where streams cross.
