# CMB2: what in the action, other than clustering dust, can act on the photon-baryon fluid before recombination? FROZEN CRITERIA (committed alone, before any script or number)

Owner, tonight: "WTF is going on with the CMB ... launch subagents to find out". This lane is registered as CMB2 in
CLOSURE_REGISTER (e21513a8b2) and assigned to the Field equations session. Adopts nothing. Kappa = 1/2 FITTED; not
theory closed. Both footings (canonical a0 9.3603e-11, alt 1.1312e-10 m/s^2), never pooled. No LCDM input: the
background is the footing background (B2) of F1A. A clean NO is a result.

## Equations used
- v3s with the adopted blend: QX17's field equations with Pi_+ -> F'(Pi) and Pi F'(Pi) h_mn in T (QX17D, 6b16322464).
- AC2q: QX17A's equations.
- Matter (photons, baryons, neutrinos) couples minimally to g_mn, as S_m in both actions.

## Degrees of freedom (one subagent each)
- **D1 khronon / clock perturbation, with the dust part removed.** Derive the linear Newtonian-gauge equation for the
  khronon perturbation at z ~ 1100 on the B2 background:
  - v3s: tau with K(Q). The dust IS K(Q), so D1 grades the khronon at the largest amount galaxies allow
    (f <= 0.33 / 0.19, KD1), plus everything in the khronon sector that is not the dust's density.
  - AC2q: the clock phi.
  Report its contribution to the Weyl potential, Psi_W(D1) / Psi_W(dust at R 5.41), at k 0.01, 0.03, 0.1, 0.3 Mpc^-1.
  KA: F1A G4 (Q <= 3.4e-11 for the clock; the dust case gives Q = 1.000).
- **D2 P sector.** Count its propagating modes on the FRW background: the Dirac / ADM constraint count for P.A - W(K|P|)
  - gamma_L F(Pi) + lambda n.P, from QX17B's 3+1 form. If a mode exists, derive its sound speed. If none exists (P is a
  leaf constraint), derive the constrained response, i.e. the phantom density sourced by the photon-baryon potential,
  and grade it as D4.
- **D3 preferred frame in the photon-baryon physics.** From the matter equations nabla_m T^mn_mat = 0 with minimal
  coupling, decide whether Q, n_m or P enter:
  - Thomson coupling;
  - the photon-baryon sound speed c_s;
  - the sound horizon r_s, other than through the background H(z) (already in B2) and the metric potentials (D1, D2, D4).
  sympy: show the matter equations contain no khronon field.
- **D4 the a0 law at z ~ 1100.** Model the law's phantom response to the acoustic potential with a0(z) = x a0, for
  x in {1, 3, 10, 30, 100}. Take the linear-theory acoustic potential at k 0.01-0.3 Mpc^-1 and z 1100 on B2, with its
  physical gradient g_ac.
  - Report g_ac / a0(z).
  - Report the phantom's share of the Weyl potential, (nu(g/a0) - 1) at the acoustic gradient.
  - Report its time behaviour. It is "still" if it does not oscillate with the photon-baryon fluid; it "follows" if it is
    phase-locked to the acoustic source, because it is sourced by the oscillating fluid's own potential.
  - Report the sign of its effect on the ratio of the third to the second peak, in the A2 / A3 driving picture:
    - a still potential deepens the odd (compression) peaks;
    - a potential that follows the source rescales G for the fluid.

## Pre-screen (graded per DoF, both footings)
A DoF can stand in for the cold component on the peaks only if, at some k in 0.03-0.3 Mpc^-1, it supplies a **still**
Weyl potential of at least 0.5 of the dust's (R 5.41) with the action's own free parameters inside their allowed
ranges:
- mu_K up to the BBN bound 8.89e6 Mpc^-1;
- Lstar from 21.7 / 22.9 pc up to 90 pc (X27);
- the blend's b = rho_DE (fixed);
- a0(z) factor x up to 100.
It must also not put more than f 0.33 / 0.19 into galaxies (KD1's capture rule). The galaxy check is read from the
record, not recomputed.

## Labels
- **CANDIDATE**: a DoF passes the pre-screen on both footings AND a peak-ratio fit on PR4 + ACT DR6 survives, run in
  coordination with EV1's CMB1 likelihood, no shared code otherwise, with the CMB1 line as frozen there.
- **NO (DoF named)**: every DoF fails the pre-screen, each with its equation and its number.
- **NO VERDICT**: a control fails.

## Controls
- **KA-dust:** the planted dust at R 5.41 on B2 reproduces F1A G4's baryon contrasts, -26.8 at k 0.05 and -108.1 at
  k 0.3, within 5 %, and passes the pre-screen. This is also the power check.
- **MUTATE-phase:** a planted source equal in amplitude to the dust's but phase-locked to the photon-baryon density must
  read "follows" and fail the pre-screen.
- **MUTATE-gravity (D3):** add a coupling of n^m to the baryon velocity by hand. The sympy check must then find the
  khronon in the matter equations.

The subagents write scripts only inside this lane's directory. The Field equations session grades, commits and pushes.
