# CFG643 FROZEN CRITERIA: "Door 1", baryon -> cold-energy heat exchange Q_c = C a0 v rho_b

Date 2026-10-12. Committed ALONE, before any CFG643 code or script number exists.

Settings: kappa = 1/2 FITTED; footings canonical 9.3603e-11 / alt 1.1312e-10 m/s^2, never pooled, every gate reported per
footing. "Cold energy" throughout; its mass is required. No dark-matter particle species is added: if a gate needs one, the
lane says so plainly and that gate fails the framework's own rule. No LCDM or standard-MOND yardstick enters any verdict.
Not "theory closed".

Pre-freeze disclosure: before writing these criteria the analyst did a mental order-of-magnitude estimate (scaling
C_min ~ (K/M V_f^2)(M_cat/M_b) V_f/(a0 t), and t_b ~ V/(C a0) of tens of Myr at C ~ 1). No script was run and no gate number
below was computed. The universality factor (2) and the gates are the task's own specification, not chosen after seeing data.

## Inputs (all inherited read-only from the record)

- Heating law (posited, not framework-derived): Q_c = C a0 v rho_b per unit volume into the cold energy, -Q_c out of the
  baryons. Source: astra's MECHANISM.md checkpoint (sol61_push/cold_production_2026_10_11/mechanism_2026_10_12), which quotes
  Famaey, Khoury, Penco & Sharma arXiv:1912.07626 eqs 26-28. The paper itself is not re-read here (no downloads); the formula
  is taken from the checkpoint as context.
- a0 = kappa c sqrt(G rho_DE) at the two footings.
- Systems: CFG541's three 1-D systems, rebuilt by importing CFG541's `Model` read-only and rerunning its alpha = 1 settling
  flow: MW-like (M_b 6e10, Hernquist a 2.5 kpc), group-like (CFG540 median), X-COP-scale cluster (1.5e14 point mass; labelled
  as the X-COP proxy). Census f_ret and the turnaround catchment are inherited (CFG541 inputs).
- Target state = CFG541's settled final state (the law's phantom inside the exhaustion edge r_*). Its isotropic Jeans
  kinetic energy K_f (pressure zero at r_ta, as CFG541 `Model.energy`).
- Control V0: K_f/M_cat and dW/M_cat recomputed must equal cfg541_results.json to relative 1e-6 (else the lane stops).
- v (speed in the heating law): primary v = V_f/sqrt(2) (astra's choice); variant v = V_f.
- System age t_age: primary 10 Gyr for all three; variant (declared) MW 12, group 8, cluster 5 Gyr.
- Baryon kinetic reservoir: primary K_b = (1/2) M_b V_f^2 (astra's t_b); variant CFG541's 0.75 M_b V_f^2.

## Transport laws (stated, with origin)

- T0 FRAMEWORK-NATIVE: the cold energy is collisionless; phase mixing is reversible; there is no irreversible heat flux
  (CFG541/542, astra's relaxation-rate check: self-collision time 135x the crossing time at 10 kpc). A = 0.
- T1 FKPS CLOSURE (ASSUMED, not framework): ideal-gas behaviour with relaxation on a Jeans/dynamical time. Energy leaves at
  L_T1 = integral over r_in..r_* of (3/2) rho_c sigma^2 (sigma/r) 4 pi r^2 dr (sigma = isotropic Jeans dispersion of the
  target). A_T1 = G L_T1 / V_f^5. Inner cutoff = CFG541's r_in; the sensitivity to r_in (x10) is reported.
- T2 COLLISIONAL (context): relaxation at the cold self-collision rate rho_c S sigma_rel with astra's benchmark S = 0.3 cm^2/g,
  L_T2 = integral (3/2) rho_c sigma^2 * min(rho_c S sqrt(16/pi) sigma, sigma/r) dV. A_T2 = G L_T2 / V_f^5. Introduces S (a
  particle self-cross-section); reported for the slope/universality test only.
- Heating integral B = integral v rho_b dV / (M_b V_f). With primary v this is 1/sqrt(2) exactly.
- Balance L_heat = L_transport gives V^4 = (B C / A) G M_b a0; the law's own normalisation needs C_BTFR = A / B.

## Gates and pass rules (each per footing)

G1 ENERGY SUPPLY.
- G1a (IC-C benchmark, as tasked): required import E_imp = K_f - K_IC, with K_IC = (3/2)(0.05 V_f)^2 M_cat (the IC-C
  sigma = 0.05 V_f benchmark; K_IC/M_cat = 0.00375 V_f^2). Supply S = C a0 M_b v t_age. C_min = E_imp/(a0 M_b v t_age).
  PASS iff max(C_min)/min(C_min) <= 2 across MW, group, cluster (primary v and t_age). Variants reported, do not change the
  label unless every variant agrees (then noted).
- Cross-check: collective_energy_lower RESULT import fractions (MW 0.497, cluster 0.638 M V_f^2) give C_min within 25% of
  the CFG541-based value (declared consistency, not a gate).
- G1b (framework-native formation, the record's own path): CFG541 infall from rest at turnaround requires a SINK
  E_sink = dW - K_f > 0. Heating (Q_c >= 0 by construction of the law) adds energy. PASS iff E_sink <= 0 in every system
  (i.e. the native path needs import). Otherwise G1b FAILS BY SIGN: heating cannot supply what the native path needs.

G2 BTFR NORMALISATION.
- Compute C_BTFR = A/B under T0, T1, T2.
- T0: A = 0 -> no balance exists -> G2-native FAILS (no steady state; heat accumulates linearly in time).
- T1/T2: PASS iff (i) C_BTFR within a factor 2 across the three systems AND (ii) C_BTFR within a factor 2 of the G1a C_min of
  every system (one C does both jobs). A T1 pass is labelled "PASS ONLY UNDER THE ASSUMED FKPS CLOSURE".

G3 BARYON BUDGET.
- t_b = K_b / (C a0 M_b v) (= V_f/(sqrt(2) C a0) for primary). PASS iff t_b >= t_age in every system, at C = C_min (G1a)
  and separately at C = C_BTFR(T1). Note: at C = C_min this is equivalent to E_imp <= K_b (C-independent).
- Replenishment variant (declared ceiling on framework-supplied energy): every catchment baryon, M_cat/5.364, donates a full
  V_f^2. PASS iff E_imp <= (M_cat/5.364) V_f^2 in every system.

G4 MICROPHYSICS.
- Required cold-baryon cross-section (closure: energy per collision ~ m_c v^2, w ~ v; O(1) factors flagged):
  sigma_cb/m_b = C a0 / (rho_c v^2). Evaluate at C_min with the target rho_c, v = sigma(r), at MW 8 and 30 kpc and cluster
  100 and 500 kpc.
- G4(i) EXISTENCE (analytic): PASS iff a fixed-coupling interaction gives sigma proportional to 1/(n_c v^2). The v^-2 is
  allowed (s-wave unitarity saturation sigma = 4 pi hbar^2/(mu v)^2); a 1/n_c factor needs a density-dependent mediator
  (astra's trial screened scalar: negative compressibility). Any route also needs a non-gravitational baryon vertex absent
  from the present action, i.e. a particle with a free cross-section -> FAILS the framework's no-new-species rule.
- G4(ii) CONTEXT (labelled, different channel: Sagunski+ limit is on cold SELF-interaction): report sigma_cb/m_b in clusters
  against 0.35 cm^2/g, and the unitarity ceiling on the cold particle mass m_c <= sqrt(4 pi hbar^2 rho_c / (C m_b a0)).

G5 CONSISTENCY.
- G5a CFG541 S(i): if the heat is retained (T0), the final cold K = K_f (from infall) + E_sink + heat. PASS iff
  log10(K/K_f) <= 0.1 dex (CFG541's own rule) for the native path with heat at C_min. (Baryon heating is a different SOURCE
  from settling, but adds to the same cold kinetic energy.)
- G5b CFG623 (Bullet allows alpha ~ 0): momentum exchange accompanying Q_c gives drag deceleration on the cold energy
  a_d = C a0 rho_b/rho_c (sigma proportional to 1/w^2 at the merger speed; variant sigma fixed at the thermal v: a_d scaled by
  (w/v)^2). Offset dx = (1/2) a_d t^2 over t = 0.2 Gyr (CFG623 window starts at 0.1 Gyr after pericentre), rho_b/rho_c in
  [0.1, 1] (declared bracket, context). PASS iff dx <= 24.9 kpc (CFG623's T_L) for C = C_min at the cluster.
- G5c CFG596 (clumping excess): analytic. Heating can move settled mass only by pushing it off the law's profile (candidate B
  places settled mass by the deficit). Label: REDUCES CLUMPING ONLY BY BREAKING THE LAW, or NEUTRAL. Not a numeric gate.

MUTATE (CFG643_MUTATE=1, separate outputs):
- M1 C -> 0: supply exactly 0, IC-C import unmet (delivered/required = 0): reproduces astra's bound. Must hold.
- M2 C x 2: supply ratio 2 to relative 1e-12. Must hold.
- M3 sign of Q reversed (export): G1b's sign verdict must flip for the sign test (tooth on the sign logic).

## Verdict rule

- OPEN DOOR: G1a, G2 (under a framework-native or at least T1 transport), G3, G4(i) pass with one C that is O(1)-natural or
  derivable.
- KNOB: no gate fails cleanly, but C must differ by system beyond a factor 2 or be tuned.
- CLOSED: any of G1b, G3, G4(i) fails cleanly on both footings (the fail must be verified as hard as a pass: control V0,
  variants, MUTATE).

Run: OMP_NUM_THREADS=1 nice -n 10 python3 cfg643.py (single process, < 300 MB, no PM, no downloads). The running 1024^3 job
and the cfg625 driver are not touched.
