# KDE1 frozen criteria: the clock made into the dark-energy field (2026-11-10)

TEST lane, quarantined. Adopts nothing, relabels nothing, registers nothing. Footings canonical (a0 9.3603e-11 m/s^2)
and alt (1.1312e-10 m/s^2) are never pooled. The cold component is cold dark energy; no particle claim. Not a LCDM lane.
Committed alone, before any script or graded number.

## The candidate, as briefed

Units c = 1, K = 4 pi G, symbols as in QX17 (`closure_2026_11_06/QX17_covariant_field_equations/RESULT.md`).

    S = Int sqrt(-g) { R/(4K) + (1/2) Q^2 - V(tau) + P^m A_m - W(K|P| ; a0(tau)) - gamma_L F(Pi) + lambda n^m P_m } + S_m

    a0(tau) = kappa sqrt(G V(tau)),  W(p; a0) = (a0^2/K)[-p/a0 - ln(1 - p/a0)],  F(Pi) = [max(Pi, 0)]^2 / 2,
    gamma_L = K Lstar^2 / 2,  Pi = D_m P^m.

That is action (A) with the dust term L_K(Q) and the constant Lambda replaced by a canonical kinetic term and a
potential for the clock, and a0 tied to V. "The record's stiffness term" is read as QX17's F (reading K). The owner's
11-07 Pi^6 blend (b = rho_DE) is reading B; it changes F only near Pi = 0 and is treated in R2, not in R1.

## Order

Step R (the record) first, as the brief requires. Items 1 to 7 of the brief are graded only if step R does not end
the lane. If step R ends it, items 1 to 7 are answered in RESULT.md from the record (quoted, with lane and commit), or
marked "not in the record", and nothing new is graded for them.

## Hand expectation, stated before any script

The record search (done before this file, by reading) found `action_search_2026_11_05/AC2_single_clock/ACTION.md`
("one canonical scalar supplies dark energy and the preferred clock"; a0^2 = xi G V(phi)), its switched form AC2s
(AC6: "stiffness off where D.P < 0") and the repaired AC2q (AC7). I expect R1 to find KDE1 identical to AC2s with
xi = kappa^2. I also expect AC2's own FRW closed form to say the clock is not stiff on sub-Hubble scales (its phase
speed goes to zero at Lstar = 0), against the brief's premise.

## R1 (graded): is KDE1 the record's AC2s?

Two Lagrangian densities, built by two separate routes in one script (no shared helper for A or Pi):

- **KDE1**, from the brief through QX17's closed forms: Q = sqrt(-g^{ab} d_a tau d_b tau), n_a = -d_a tau / Q,
  P.A = -P^a d_a ln Q, Pi = div P + P^a d_a ln Q with div P from d ln sqrt(-g), switched F as above.
- **AC2s**, from AC2's ACTION.md and AC6's switch, through Christoffel symbols: X = -(1/2) g^{ab} d_a phi d_b phi,
  n_a = -d_a phi / sqrt(2X), A_a = n^b nabla_b n_a, D.P = h^{ac} nabla_a P_c, p = K sqrt(P.P),
  a0^2 = xi G V(phi) with xi = kappa^2, gamma = K Lstar^2/2, stiffness -(gamma/2)(D.P)^2 where D.P >= 0 and 0 where
  D.P < 0, multiplier lambda_P n.P. The GR term is checked once symbolically (Mpl^2/2 = 1/(4K) for Mpl^2 = 1/(8 pi G)).

Configurations: random polynomial fields in 2+1 (metric, clock, P = h.V so that n.P = 0 holds in a neighbourhood,
lambda), as in QX17, 2 points per configuration, a fixed list of seeds, with a polynomial V(tau) > 0 on the sampled
range and P small enough that K|P| < a0. At least 8 points on the Pi > 0 branch and 8 on Pi < 0; the script raises
the number of seeds (fixed rule: seeds 1, 2, 3, ... in order) until both counts are met, and reports how many it used.
mpmath, 40 digits. Run once per footing: V is scaled by (a0_footing / a0_canonical)^2 so the two runs carry a0 values
in the footings' ratio (the identity is algebraic; this only keeps the footings separate).

- **IDENTICAL**: relative difference of the two densities <= 1e-30 at every point, both branches, both footings.
- **DIFFERENT**: above 1e-6 at any point. Anything between is UNDECIDED.

## R2 (quoted, not graded): what the record holds on AC2, AC2s, AC2q

For each of the brief's items 1 to 7, the record's verdict on AC2 / AC2s / AC2q with its lane, quoted from the lane's
README or RESULT and from `closure_2026_11_05/CLOSURE.md` section 3 and `closure_2026_11_06/CLOSURE_FINAL.md`. Not
re-run. Reading B (Pi^6 blend near Pi = 0) is placed against AC7's control M-b and AC21 in words only.

## Known answers (each must pass, or the label is NO VERDICT)

- **KA1.** Replace (1/2)Q^2 - V(tau) in the KDE1 density by mu^2 (Q-1)^2/(2K) - Lambda/(2K) and hold a0 constant: the
  result equals action (A) as written in QX17 RESULT.md section 0, coded separately, at the R1 points, relative
  difference <= 1e-30. (Equal densities have equal Euler-Lagrange equations, so QX17's certified K1-K5 then apply.)
- **KA2.** The static limit gives the law: (a) sympy, exact: max_P [P.A - W(K|P|; a0)] = (a0^2/K)[u - ln(1 + u)],
  u = |A|/a0, with a0 = kappa sqrt(G V) symbolic; (b) Lean: `balance_iff_lawS` restated in KDE1.lean (mu(x) = x/(1+x):
  mu(g/a0) g = g_N iff g^2 = g_N (g + a0)), compiles.
- **KA3.** Law off (P = 0, lambda = 0): the tau Euler-Lagrange expression of sqrt(-g)[(1/2)Q^2 - V(tau)], taken by
  sympy differentiation on 3 random configurations in 2+1, equals -sqrt(-g)(box tau - V'(tau)) up to the overall sign
  fixed once, relative difference <= 1e-30; on flat FRW the reduction gives tau'' + 3 H tau' + V'(tau) = 0 (exact).

## MUTATE (separate outputs; each must bite)

Each twin replaces one piece of the AC2s side and reruns R1. Bites = relative difference >= 1e-6 on at least one point.

- **M1** unswitched stiffness (AC2 as written, -(gamma/2)(D.P)^2 everywhere). Also reported: agreement on Pi > 0.
- **M2** AC2q's switch, -(gamma/2){[max(D.P + 2X, 0)]^2 - (2X)^2}.
- **M3** a0^2 = kappa^2 G (X + V) (a0 tied to the clock's whole energy density) instead of kappa^2 G V.
- **M4** action (A)'s terms (dust mu^2 (Q-1)^2/(2K), Lambda, constant a0) in place of X - V(phi) and a0(phi).

A twin that does not bite is disclosed; then R1 has no power and the label is NO VERDICT.

## D1 (reported, no label): AC2's clock frequency in framework-native numbers

Re-derive, by sympy, the k -> infinity limit of AC2's FRW dispersion from AC2's quadratic action
S2 = Mpl^2 Int a^3 {[eps + cY k^2/H^2] zeta'^2 - eps k^2 zeta^2}, cY = 1/(1 + Lstar^2 k^2/2):
omega^2 -> eps H^2 (1 + Lstar^2 k^2/2), and eps H^2 = K phidot^2. With phidot^2 = (1+w) rho_DE and
rho_DE = a0^2/(kappa^2 c^2 G) (framework-native, as AC6 and AC10): Omega^2 = K s^2 = 4 pi (1+w) a0^2/(kappa^2 c^2).
Report, both footings, 1+w in {0.1, 1, 2} (2 is the maximum for V >= 0): 1/Omega in Gyr; the clock's phase speed
Omega/k in km/s at r = 1/k = 10 kpc, 300 kpc, 1 Mpc and 2 Mpc (a cluster scale), with the Lstar factor at
Lstar 21.7 / 22.9 pc; and Omega tau_f at COL1's first-fold times 0.063 and 0.154 Gyr (AC10's planar fold criterion is
Omega tau_f <= 1 for a clock-only stream; spherical is not shown by it). These numbers grade nothing.

## Lean

`KDE1.lean`: (i) `balance_iff_lawS` restated (KA2b); (ii) omega^2 = E x^2/(E + x^2) < E for E, x > 0 (the clock's
frequency at Lstar = 0 never exceeds sqrt(K s^2), at any k); (iii) its phase speed squared E/(E + x^2) < eta once
x^2 > E/eta; (iv) K s^2 = 4 pi (1+w) a0^2/kappa^2 when a0^2 = kappa^2 G rho_DE, s^2 = (1+w) rho_DE, K = 4 pi G (c = 1);
(v) the largest D1 case, Omega^2 tau_f^2 = 8 pi (a0 tau_f/(kappa c))^2 at alt, 1+w = 2, tau_f = 0.154 Gyr, is below
(1/50)^2, written with rational upper bounds on the inputs. Twin `KDE1_MUTATE.lean` states each one falsely; every
false statement must fail to compile. Build: `cd <repo>/fable_independent_2026/lean_2026 && lake env lean <file>`.

## Labels, per footing

CONSISTENT, AND THE LAW IS ON WHERE OBSERVED (list what is not solved) / FAILS (first failing item and by how much) /
NOT WELL-DEFINED / ALREADY IN THE RECORD AS (name) / NO VERDICT.

- **ALREADY IN THE RECORD AS AC2s** if R1 is IDENTICAL on both footings, KA1-KA3 pass and M1-M4 bite. The lane then
  stops; RESULT.md quotes the record's verdicts (R2) and grades nothing else.
- If R1 is DIFFERENT, the lane continues: items 1 to 7 get their own lines in an amendment, committed alone before any
  number for them.
- NO VERDICT if a known answer fails, a MUTATE twin does not bite, or R1 is UNDECIDED.

## Limits

One thread, under about 1.5 GB. No downloads. Expected runtime minutes. No home paths in any file.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
