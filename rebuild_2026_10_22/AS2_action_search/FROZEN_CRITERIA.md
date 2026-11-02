# AS2_action_search: FROZEN CRITERIA (committed alone, before any script or number)

Id: the brief named this lane AS1. `AS1_outer_slope` holds that id, so this is AS2 under the brief's next-free rule.

Question: inside a stated finite grammar, is there a covariant action for g_N = g^2/(g + a0), a0 = kappa c sqrt(G rho_DE), that passes the gates below?

**Method, plainly.** This is enumeration against analytic gates. An action has no data table to regress on, so nothing here is fitted to data and nothing here is a data test. A row passing all gates is a candidate only: it needs a hand derivation, outside review and data grading. An empty result holds for this grammar only and is not a no-go theorem.

kappa = 1/2 FITTED. Footings canonical 9.3603e-11 and alt 1.1312e-10 m/s^2, both reported, never pooled. No dark matter particle. The cold component is cold dark energy. The cold sector stays retired: no result here reinstates it, only the owner can. Published work credited: AeST (Skordis and Zlosnik), Khronon (Blanchet and Skordis), BIMOND and QUMOND (Milgrom), TeVeS (Bekenstein), Einstein-aether (Jacobson and Mattingly). Not theory closed. Nothing here says the data favour the framework.

## Not blind
Read before freezing: UX1 README, criteria, ux1_gates.py, ux1_q2.py and its output; THEORY_V3_DRAFT; V3S verdict lines 1-60; BOLTZ1 README; REQUIREMENTS_LIST; STANDING 284-300; heads of C1, C4, H1, M1 READMEs.
Hand expectation written now, from that reading: Kh + P + gamma_L (v3) fails G6 at the mu_K cap; twisting aether with gamma_L fails G7; aether or scalar carriers whose Newtonian part has an order-unity a^2 coefficient (AeST) may fail G5 near the recorded alpha_1 = -2(K_B+2); conformal and disformal couplings fail G2. One untested corner I expect to be the closest row: a khronon plus a separate scalar carrying the law with gamma_L on the scalar's spatial Laplacian. C1 dismissed that form because it is not AQUAL off symmetry, but the law's spherical limit does not require AQUAL off symmetry. This expectation doesn't change a label.

## Grammar (frozen)
**Field content, at most two beyond the metric.**
S scalar; SX scalar + auxiliary scalar; Ae unit timelike vector, twisting; Kh unit timelike hypersurface-orthogonal vector (khronon); SAe; SKh; KhP khronon + auxiliary spatial covector; AeP twisting aether + auxiliary spatial covector; BM second metric; BMS second metric + scalar; M mimetic scalar. Excluded and stated: second metric + vector, three-field content, higher-rank tensors, f(R)-type and cubic or higher Horndeski operators (no such invariant was listed).

**Invariants.** Law carrier I, exactly one per candidate: X, Y, a^2 (aether acceleration), F_ti^2, K_JS (nabla A nabla A), Y_B (Milgrom's C-tensor scalar), P^2, or the difference gradient, as content allows. Fixed quadratic add-ons from a coefficient list: Einstein-Hilbert (always), K_B F^2 with K_B in {0, 1/2}, Maxwell-twist F_ij^2, a.V and a.P cross terms with coefficient in {0, 1, 2} of the form that includes AeST's 2:1 ratio, Y with coefficient in {0, 1, 2}, quadratic P^2 with coefficient in {0, 1}, background clock Q0 in {0, 1}. Stiffness option in {none, (D.P)^2, (D.V)^2, (D.a)^2, (box phi)^2}, each costing the one scale L. Matter: minimal on g, conformal, TeVeS disformal, scalar disformal. Cold term option: none; K(Q) on the existing field (costs scale mu); separate P(X) (costs a field slot); mimetic constraint; twin dust on the second metric.

**Free function.** The carrier function f(y), y = sqrt(I)/a0, is drawn from a bottom-up expression grammar: leaves {y, u = y^2, 1, 2, 1/2}; unary {neg, inv, sqrt, log(1+.), log(1-.), exp}; binary {+, -, *, /}; at most 9 nodes; distinct by value and first two derivatives on a fixed y grid to 1e-9; hard cap 1,000,000 distinct expressions, smaller sizes first. If the cap binds I state at which size. An overall coefficient from {+-1/4, +-1/2, +-1, +-2, +-4} is enumerated. No fitted number enters. Dust abundance and Q0's value are integration constants and are named as such.

**Constants.** Beyond a0, at most ONE stated extra scale per candidate, L or mu.
- **Tier A (the frozen cap):** at most two fields, at most one extra scale. Only Tier A rows can be survivors.
- **Tier B (reported only):** exactly one cap relaxed, one extra field for a separate dust, or a second scale. It exists so that v3 itself (L and mu) and UX1's K8 are visible. A Tier B row can't be labelled a survivor.

The script prints the size of the space before any gate runs.

## Gates, cheapest first
Each is a reduction of the candidate's own field equations on a stated background, or carries [REC] and the lane where the engine can't reach it. Every G1 survivor is graded on every later gate, so a near miss shows what it fails and by how much; the sequential counts are read off that matrix.
- **G1 static law.** Spherical static weak-field stationarity of the reduced action, baryons as the only source. Pass: max relative residual in g_N <= 1e-8 for g/a0 in [0.01, 100] where the carrier reaches, coverage of that whole range; numeric pass then confirmed by a sympy zero residual. A stiffness or mass term may leave the law at scales past its stated scale; that is stated.
- **G2 tensor speed and gamma.** c_T = 1 against the matter cone, |c_T - 1| <= 1e-15; gamma = 1 in the matter frame, |gamma - 1| <= 2.3e-5 at every x on the grid. [Bounds from memory, PROVISIONAL.]
- **G3 health.** Plane-wave second variation on a frozen background: Minkowski, FRW's sub-horizon limit (u = 0, Q = Q0) and static (x = 0.01, 1, 100; k parallel and perpendicular to the field). Leading WKB order only; lower-order terms such as Jeans terms aren't seen, and this is stated. FAIL: a complex or negative omega^2 mode, a negative-residue mode, or omega^4 (higher time derivative). ND: degenerate determinant or zero-speed mode whose sign the frozen analysis can't fix. PASS: otherwise. ND is never PASS. BIMOND's recorded ND may stay ND.
- **G4 Cassini Q2.** On the static equation form the candidate actually has (AQUAL, two-field or QUMOND), both footings, four external fields E0-E3, against the Hees line 9e-27 s^-2. Solver read from UX1 (ux1_q2.py), AQUAL known answer against E2 within 2 %. Screened forms carry [REC C6].
- **G4p planets.** Not in the brief's list; added because UX1 found the tail, not Q2, is what sinks an unscreened law. The a0 tail against M1's and C6's ephemeris bounds, both footings. Reported as its own column and counted.
- **G5 preferred frame.** alpha_1 from the vector sector and alpha_2 from the scalar sector of the same second variation with a moving source, evaluated at the candidate's coefficients at the Sun (x at 1 AU), both footings. Bounds |alpha_1| <= 4e-5, |alpha_2| <= 2e-9 [memory, PROVISIONAL]. Known answers: Einstein-aether's Foster-Jacobson formulas must come out at random coefficient points.
- **G6 dust and growth.** A dust-like term in the FRW equation of the metric matter sees, with delta growing as a at k -> 0, on the candidate's stated cold option; state what supplies it. Growth at the mu_K cap carries [REC M1, F3, Q6, X4] for K(Q) on the law's own field. Also reported, not gating, per the brief: does it double count in galaxies (X22 capture 0.76 against tolerance 0.20 / 0.03, X57). Only a separate dust is a result, with nothing reinstated.
- **G7 well-posedness.** Where the vector twists: an omega^2 ~ k^4 mode has nonreal roots on tilted slices (I1, UX1's T-C test rerun) unless there is a global time function. Pass: second order in the principal part, or untwisted foliation.

## Known answers, required before the real run
Script stops before grading if any fails.
- KA1 grammar rediscovers v3's J_x (the K(Q)-free khronon carrier) and AeST's capped J (C1) as exact G1 passes in the right templates.
- KA2 the engine gives GR's two tensor modes and no other mode, and the static GR limit.
- KA3 Einstein-aether spin-2, spin-1, spin-0 speeds and alpha_1, alpha_2 at random points against the published formulas [memory, PROVISIONAL].
- KA4 recorded failures come out: v3 G6 (cap), v3 or AeST unscreened G4 and G4p (E2, M1), AeST with gamma_L G7 (I1), AeST G5 near alpha_1 = -2(K_B + 2) (STANDING), BIMOND K1's Q2 pass and planets fail (UX1), conformal coupling G2, QUMOND parent indefinite (UX1 J1).
- KA5 a planted healthy mock passes all gates, with its reduced equations injected: a pipeline check only, not an action.
- MUTATE twin `AS2_MUTATE=1` writes separate outputs and must fail: flips the Einstein-Hilbert sign in the engine and the carrier's coupling sign.

## Labels
- **SURVIVOR CANDIDATE:** a Tier A row passes all gates and a separate, independently written reduction agrees. Still a candidate only.
- **EMPTY FOR THIS GRAMMAR:** no Tier A row passes. The closest rows are named with the gate each fails and by how much.
- A gate with ND on an otherwise clean row gives **CONDITIONAL ROW**, not a pass.
- If the independent reduction disagrees with the engine, the row is labelled ENGINE DISAGREES and isn't a survivor; both numbers are published.

## Compute and discipline
One thread, nice 19, under 4 GB, checkpoints, SIGTERM stops cleanly and a rerun resumes. BF1, UX7, AF1 and AR1 are not touched. Output `.out` and `.json` carry no timing, so a rerun must be byte-identical. Every failed check is reported. No download, deposit, push or edit outside this lane. Reads of UX1 are read only.
