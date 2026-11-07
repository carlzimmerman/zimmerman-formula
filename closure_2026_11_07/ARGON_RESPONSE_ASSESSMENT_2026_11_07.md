# Assessment of the outside solver's answer (2026-11-07, ~16:20)

The owner handed QUESTION_FOR_ARGON_2026_11_07.md to an outside solver and pasted its answer. This file records what
it claims, what the record already says about each claim, and the one lane it earns. Nothing is adopted.
Kappa = 1/2 FITTED; not theory closed.

## 1. What it claims

Q1. A host-independent release speed from the action's own constants: v_k = 2 c (a_geo L*)^(1/3) with
    a_geo = a0/c^2, giving 577.7 km/s (canonical: a0 1.2e-10, L* 21.7 pc) and 571.4 km/s (alt: 1.1e-10, 22.9 pc).
    Mechanism offered: a "critical wavelength" lambda_crit = (L*^2 c^2 / a0)^(1/3) ~ 2.1-2.25 kpc where a stiffness
    dispersion acceleration L*^2 c^2 / lambda^3 equals a0; the kick is "the work a0 does across one such layer",
    (1/2) v_k^2 = c_branch a0 lambda_crit, with c_branch = 2 chosen from the Pi^6 -> Pi^2 branch change.
    Mutations offered: a Pi^4 core gives c_branch = 1 and 408 / 404 km/s (fails galaxy clearing); 1D mixing gives
    1625 km/s (evaporates clusters). Its own caveat: in the action the stiffness acts as L*^2 nabla^2 on P, so the
    natural balance gives lambda ~ L* and v ~ 9 km/s unless a c^2 enters, and the (Q - 1) ~ Phi/c^2 suppression would
    make the kick host-dependent (v_k ~ v_f^(2/3)), which kills it.
Q2. No mechanism outside C1-C4 without a baryonic (atomic) scale; none valid inside the framework.
Q3. F1 is the prime suspect (P independent of A need not oscillate with the photon-baryon fluid; K(Q) = 0 would make
    F2 trivial); F3's lensing masses might be NFW-template-biased by +0.25-0.35 dex in a log potential.

## 2. What the record says

Q1. (a) CK2 (fe224c21ec) already showed, on the certified equations, that no isolated host changes branch
    (rho_ph/rho_DE >= 5e-4 everywhere, 1e8-1e15 Msun, Sigma/X >= 2), that F = F' = 0 at the branch point so a branch
    change carries zero latent energy, and that the only stored stiffness energy tracks the well (0.8-125 km/s). The
    solver's premise that collapse crosses the branch and releases a0 x lambda_crit has no term behind it; the
    solver says so itself in its caveat. (b) The number is a dimensional construction: 2 c (a_geo L*)^(1/3). The
    prefactor is chosen among 3/2, 2 and 12/5 (500, 578, 633 km/s); choosing the one that lands in the window is the
    knob the owner barred on 09-26. (c) L* is a LOWER BOUND from the outer globulars (D10), not a measurement; at
    L* = 90 pc the same formula gives ~930 km/s. The coincidence lives at the bound only. (d) The branch IS crossed in
    dynamical collapse (the D.P = 0 interfaces of AC14-AC22, FS1, FS2: "the clock's s^2 pressure shocks the stream
    front"), so one thing is genuinely testable: whether the certified fold machinery shows a layer of width
    ~(L*^2 c^2/a0)^(1/3) and a post-fold specific energy ~2 a0 lambda_crit, flat across host depth. That is lane AK1.
Q2. Agrees with the record (C1-C4, FA2/FA3, EW1/EW2/EW4). No new door.
Q3. F1: "P does not oscillate with the photon-baryon fluid" is the AC2q clock-clustering question, already a no-go in
    the record (QX3: the clock cannot cluster; QX15: baryons-only FAIL). F3: X-COP's requirement is hydrostatic, not
    an NFW-template lensing fit, so the +0.25-0.35 dex template bias does not touch the gate as graded; the lensing
    cross-check with no LCDM prior is already the record's K5 prediction line. No new door, but the F1 suspicion
    matches the record's own ranking.

## 3. The one lane it earns: AK1 (owner: the FS1/FS2 session, which holds the fold solver)

Question: in the certified planar and 3D fold runs (AC14 grid, FS1 shock-capturing, FS2 viscosity-free), when the
stream crosses D.P = 0 and the clock's s^2 pressure shocks the front, (i) what is the shock-layer width, and does it
scale as (L*^2 c^2 / a0)^(1/3) ~ 2.1 kpc or as L* ~ 22 pc; (ii) what specific kinetic energy does the clock sector
carry after the fold, and does it scale as 2 a0 lambda_crit (v ~ 575 km/s), as the stored stiffness (v ~ 1-100 km/s,
host-tracking), or with the well depth (v ~ v_f^(2/3)); (iii) does the answer move with L* as L*^(1/3) between 22
and 90 pc and stay flat across the M234 / M490 hosts and the AC14 depth grid. Frozen lines: a layer within a factor 2
of lambda_crit AND a post-fold speed within 500-650 km/s on both hosts and both footings = CONFIRMED (then the
derivation is owed as a theorem, not an ansatz); otherwise REFUTED with the measured scaling. MUTATE: a Pi^4 blend
must change the number; L* doubled must move it by 2^(1/3) if the identity holds. KA: FS2's fold times to 0.
Read-only on other lanes; new outputs small; RSS under 1 GB; push via temporary index; one message to "Theory
completion".

## 4. Bottom line for the owner

The solver's number is striking and cheap to test, but as it stands it is a coincidence at a lower bound with a
chosen prefactor, and the action-level check already on the record (CK2) says the action releases nothing at the
branch. AK1 asks the one place where the branch is actually crossed, the certified fold runs, whether the layer and
the energy the solver describes exist. If they do, the solver has found a theorem to prove; if not, Q1 is closed by
the PDE itself and the framework's third postulate stays a postulate.

## Post-result AK1 (a6c9137af9): the identity is not in the fold equations

Frozen label NO VERDICT, because the planted-speed control did not recover (the planar stream slows before the fold,
so a planted 577.6 km/s reads 318 / 309). Every graded row nonetheless reads regime I: post-fold clock speeds of
0.02-0.16 km/s against the 500-650 band, widths linear in L* (doubling gives 2.00, the identity predicts 1.587),
speeds that track the well (d ln V / d ln v_f 1.00 / 0.95; doubling L* leaves V unchanged where the identity predicts
1.260), alpha_L 1.01 / 0.94. Two disclosures matter: the protocol's lambda_crit of 2.09 / 2.25 kpc was a factor-10
slip (it is 22.5 / 24.0 kpc), and the planar reduction is non-relativistic (1 - X/X_bg <= 2.4e-7) with no dynamical
D.P = 0 crossing, so regime III cannot be reached by this machinery at all. The outside solver's number stays a
dimensional construction; nothing in the certified fold equations produces it. Combined with CK2 (no release term,
statics) the kick identity has no home in the action.
