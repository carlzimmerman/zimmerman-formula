# FA3 ideas: nonlocal, history and global actions on top of the a0 law + v3s

Written before any FA3 script or number. Kappa = 1/2 FITTED; not theory closed. Adopts nothing. No particle.
Footings canonical (a0 9.3603e-11, Lstar 21.7 pc) and alt (1.1312e-10, 22.9 pc), never pooled.
Owner's ask for this lane: "new answers to a new action and full theory". That lifts the 11-07 DIRECTION STOP list for
this lane only. FA2 takes local actions; WL1 takes the web-off switch keyed on khronon multi-streaming (cited here,
not graded). EW1 lists Deser-Woodard nonlocal MOND as a literature row (R09, by hand, PROVISIONAL); I1 below is the
record-native, graded form of that memory class.

## What the space has to beat (record numbers)

- Residue after SE2 (joint systematics): X-COP +0.440 / +0.408 dex, groups +0.232 / +0.194, Coma UDGs +1.120 / +1.075.
  Discs f <= 0.33 / 0.19; LG field dwarfs 0.
- The CMB wall: with the law on the linear web the lensing amplitude is r = 74.7 / 89.4 against |r - 1| <= 0.072
  (SV5 iter_1); the web phantom must be F_web <= 0.005 (OQ1/OQ2).
- Keep Cassini / PPN / c_T, galaxy lensing = dynamics, SPARC, and state the causal structure (AC18, SV2: the leaf
  constraint is instantaneous; tau-ordering holds).
- QX20: the step sits at FIXED local M_b, g_N, depth, r/r_M, f_gas. DX1: the needed amount spans ~100x across classes.
  So a key at a point cannot carry it. A property of the whole host, or of its history, is not ruled out by those two
  results. That is the reason for this space.

## Why these are not DX1's D4 (history: DEAD)

DX1 D4 asked whether a disc's formation history could EXPEL or never ACCRETE a captured cold component. Its kills are
about a substance: contraction pulls it in (wrong sign), supernova energy would have to unbind it (5-23 % share,
inverted ordering), and capture at turnaround depends only on Phi. None of the candidates here has a substance. Each
changes how the law's own phantom depends on the source's PAST (I1, I3, I4) or on the WHOLE bound region (I5, I6). No
capture, expulsion or feedback budget enters, so D4's three kills do not apply. Each candidate gets its own kill
instead, stated before any number.

## The eight candidates

Notation: W = (nu(y) - 1) g_N is the law's phantom field (y = |g_N|/a0, simple nu), so g = g_N + W. Every candidate
keeps v3s's static AQUAL sector, its Solar-System screening and its tensor sector unchanged, and changes only how W is
built. Pointwise |W| <= a0 for every y (W/a0 = (nu - 1) y rises from 0 to 1): a law identity used below.

### I1. Causal memory of the phantom (retarded kernel along the khronon flow) -- GRADED

- **Action / equation.** W_eff(x, t) = integral_0^t K(s) W_law(x_L(t - s), t - s) ds, with K >= 0 and support s >= 0.
  x_L is the worldline of the khronon flow n (in the weak field, the matter element). The local form for the
  exponential kernel K = e^{-s/tau}/tau is a first-order transport equation n.grad W_eff = (W_law - W_eff)/tau. That is
  the retarded box^{-1} of Deser-Woodard type, reduced to the khronon's preferred time. It adds one constant, tau.
- **Causal structure.** The memory equation is hyperbolic with characteristics along n, inside the light cone. W_law is
  still the leaf-elliptic AQUAL field, so AC18 / SV2's instantaneous mode is inherited, not repaired.
- **Why not dead.** SV5 iter_3 (class T) switched the Jeans scale on one global clock a0(z). I1 is a per-worldline
  memory of the source, so hosts and the web can in principle carry different histories. WL1 is a multi-stream switch,
  not a memory.
- **Target.** The CMB wall: a web whose source keeps changing has a lagged, smaller phantom, while static hosts have the
  full one.
- **Most likely kill, stated now.** In the linear web the physical |g_N| at a fixed comoving point falls with time
  (g ~ D/a^2), so |W| falls too. The web's past phantom is never smaller than its present one, and any positive kernel
  then gives S_web(t) >= N(t) = integral_0^t K. A host point at the same epoch has past |W| <= a0, so
  S_host(t) <= N(t) a0/|W_host(t)|. Hence **S_web >= (|W_host|/a0) S_host at every epoch, for every kernel.** KiDS
  lenses (z 0.1-0.5) overlap the web's lensing epoch and need S_host ~ 1 (galaxy lensing = dynamics). Their |W|/a0 is
  of order 0.1-0.3, so S_web >= ~0.1 against <= 0.005. Expected label: FAIL (web row), whatever tau or kernel.

### I2. Memory of the law's argument (the law is evaluated on the past maximum or mean of y) -- NOT GRADED, dead in advance

- nu(y_bar) with y_bar = max or mean of y along the worldline. In the early web, y grows with z (SV5 prints y_med 0.5-0.6
  at z 50, and g ~ 1/a beyond), so y_bar >> 1 at the CMB. That would switch the law off on the web.
- **Kill.** Every baryon element of a galaxy was in that same early web. Its y_bar is set at z >= 50, so nu(y_bar) ~ 1
  inside SPARC discs too, and the law is off where it is measured. A finite memory window brings back I1's problem.
  DEAD.

### I3. Formation-epoch a0 memory with z_f built from the record (GB1 F2 rebuilt) -- GRADED (owner's ask)

- **Equation.** The phantom freezes at assembly: g = g_law(g_N; a0(z_f)), a0(z) = kappa c sqrt(G rho_DE(z)) from CFG689
  (GB1's RZ_TAB; envelope top 1.21; SV5 iter_3's native bump 1.12 at z 0.7).
- **z_f from the record's own numbers (no LCDM input).** Pressureless spherical collapse: the system's present mean
  dynamical density inside the graded radius, rho_bar = 3 v^2 / (4 pi G r^2) from GB1's features, equals 18 pi^2 times
  the footing background matter density at z_f. The background is QX3 iter3's framework-native corner (the one SV5
  uses). 18 pi^2 is the Newtonian top-hat number, not an LCDM fit; turnaround (5.55) is reported as the bracket.
- **Why not dead.** GB1 F2 was NO VERDICT only for lack of z_f. Here z_f is built.
- **Kill, stated now.** GB1: the offset is monotone in a0(z_f)/a0(0) <= 1.21. In deep MOND it moves at most
  0.5 log10 1.21 = 0.041 dex, against X-COP's +0.44. Expected label: FAIL (G2-G7, web), with any z_f.

### I4. Conserved phantom charge (hysteresis + merger additivity) -- GRADED

- **Rule.** A bound region carries a phantom charge Q (deep-MOND far field g = Q/r; the law's Q = sqrt(G a0 M_b)).
  Q never decreases when baryons leave (ratchet), and it adds over merging bound progenitors: Q = max(Q_law,
  Q_1 + Q_2). It has no free constant. Effective charge mass M_Q = mu N_eff M_b, where mu = M_b,max / M_b (mass loss)
  and N_eff = (sum sqrt m_i)^2 / sum m_i (mergers). Then g = g_law(g_N; m a0) with m = M_Q/M_b, a per-system charge
  whose phantom scales as sqrt(m) in deep MOND. (Corrected before freezing: an earlier draft wrote
  g_N + g_law(m g_N) - m g_N, which caps the phantom at a0.)
  - Field form: Q is a per-bound-region integration constant, like the khronon's Bernoulli constant q_B (AC15 S1b), but
    in the phantom's normalisation. It needs a new conserved current; no field equation is written yet.
- **Why not dead.** It is not a function of present local variables (QX20) or of a captured substance (D4, the four
  walls). Smooth isolated systems (field dwarfs, quiet discs) sit on the law by construction. Clusters and groups
  (built by mergers) and Coma UDGs (stripped dwarfs) are the systems with the most violent histories.
- **Target.** The residue: X-COP and groups via N_eff, Coma UDGs via mu.
- **Most likely kills, stated now.**
  1. The linear web is unbound, so I4 leaves it on the law: web r = 74.7 / 89.4, FAIL (web row).
  2. mu and N_eff are carried by no class, so G1-G7 are NO VERDICT. The UDG bracket is decidable from the record: in
     deep MOND the offset is 0.5 log10 mu, so G5 needs mu >= ~16, a progenitor gas fraction >= ~0.94 (if all gas was
     stripped and the stars kept). SPARC's own gas fractions at UDG stellar masses set the bracket.
  3. Recursion: Q adds over every generation of progenitors, so N_eff is unbounded for hierarchical assembly. A disc
     built from many small lumps would leave the BTFR. Only an assembly history could grade that.

### I5. Host-inherited global multiplier (phantom amplitude set by the largest bound region containing the point) -- NOT GRADED, dead in advance

- F = F(Q_host or binding energy of the outermost bound region). It is nonlocal in space.
- **Kill.** The Coma UDGs and the X-COP clusters share host class (Coma, M500 ~ 6e14, is an X-COP-class cluster). In
  deep MOND the offset is ~log10 F, so they need F ~ 2.8 (X-COP) and ~12.6 (UDGs) at the same key value. SPARC Ursa
  Major (a bound spiral group) shows NO STEP (EV1: -0.024 +- 0.064). A smooth cluster-scale component cannot reach the
  UDGs either: Coma's mean density at ~0.5 Mpc is ~300x below a UDG's needed dynamical density. DEAD.

### I6. Field-built global invariant (virial-like or shape functional of the static field) -- NOT GRADED, dead in advance

- F = F(I[rho_b]), e.g. integral |grad Phi_ph|^2 / integral |grad Phi_N|^2, or a quadrupole or flattening measure.
- **Kill.** Any static functional of rho_b that separates discs from hot systems separates by shape. The LG field
  dwarfs are pressure-supported spheroids at 0 (SE2 control; GB1 G6). X-COP and the Coma UDGs (both near-spherical)
  need F 20x apart. Inside AQUAL, SV1's Lean shell-mean bound already caps geometry at the law. DEAD.

### I7. Hybrid: gravity part + modified-inertia part (ordered and random orbits treated differently) -- NOT GRADED, kill checked first

- Inertia modified for dispersion-supported orbits only, gravity = the law.
- **Kill (checked first, as asked).** The step is seen in LENSING:
  - KiDS early-minus-late, a lensing-only measurement: +0.158 +- 0.064 (QX21);
  - the record's second cluster mass method is >= hydrostatic (QX21 T3);
  - pure MI is excluded by lensing at 21 sigma (RETRACTIONS.md).
  An inertial boost changes dynamics, not lensing. So it cannot carry a step that lensing sees, and cluster lensing
  needs the extra mass to gravitate. DEAD.

### I8. Khronon fold-count / multi-stream history as an AMPLITUDE -- NOT GRADED, cite WL1

- F = F(N_folds), the number of khronon caustics crossed. WL1 owns the switch reading (law off on single-stream web).
- **Kill for the amplitude reading.** In the static weak field every khronon quantity is a functional of Phi (DX1 §0).
  Fold count accrues per dynamical time, so the inner parts of discs (short t_dyn, many orbits) outrank clusters
  (few crossing times since collapse). That inverts the needed ordering, as in D4. DEAD as an amplitude.

## Adversarial review (subagent, before freezing; folded in)

- **I1.** No escape survives.
  - An expansion-keyed relaxation rate Gamma(theta) breaks the inequality, but its end state is a local switch on
    khronon expansion. That is WL1's door (WL1 stage 2), not graded here.
  - A signed derivative kernel W + c tau dW/dt would need tau to track H(2 - f) across the lensing window, and rotating
    discs (Omega/H ~ 1e2-1e3) wreck SPARC.
  - The bound should use the inner KiDS points (largest |W|/a0). Adopted in the criteria.
- **I3.** The 0.041 dex cap is robust. RZ_TAB lies below 1 for z 1-2.33, so a built z_f near 1-3 makes the offset
  negative.
- **I4.** The draft formula capped the phantom at a0. It is corrected to the charge form g_law(g_N; m a0). Data kills
  for that form:
  - SPARC BTFR tightness bounds N_eff scatter;
  - member-count N_eff would overshoot;
  - literature, provisional: stripped LG satellites (Crater II, Antlia II) sit cold, where a ratchet predicts them hot.
- **Two more ideas (not graded).**
  - (I9) A Gauss-law boundary condition on the bound region's turnaround surface. It keeps the far field at
    sqrt(G a0 M_b), so it can only move mass inward, and SV1's shell-mean bound caps that.
  - (I10) A light-crossing 4-volume coarse-grained source. The web keeps its g_N, so the CMB wall stands, and cluster
    g_N is diluted, which flips X-COP's sign.

## Top 3 for frozen grading

I1 (the only memory class aimed at the CMB wall), I3 (owner's explicit ask, z_f built), and I4 (the only history
class aimed at the residue). I2 and I5-I8 carry their kill above and are not graded.

Kappa = 1/2 FITTED; not theory closed.
