# Y-WAVE_BRIEF — successor wave spawned by the conductor tick of 2026-09-25 (evening)
Conductor-run (delegate_task absent, per Q/R/S/T/U/V/W/X precedent). 0->3 lanes on
3 distinct OPEN doors. House rules 1-10 (LOOP_CONDUCTOR.md) bind every lane:
append-only, no fabrication, honest FAILs preserved verbatim, no lane touches
another lane's files, no leaf commits, raw data untracked, kills pre-registered
BELOW before any run. Lane exit != 0 is a legal honest-FAIL signal; the conductor
verifies, never re-tunes.

## Context (surviving numbers, file refs)
- V03 died at the decision-tree confusion counter (KeyError 'central',
  V03_trio.py:623) AFTER the science cells: C6 doorB CONSISTENT-OPEN REPRODUCED
  (R = 1.9971+-0.0032 -> reading 1.8151+-0.0030, z = -0.91 vs record 1.8178);
  pre-registered falsifiers/classes in V03_PRE.txt stand unchanged.
- V04 died at the analytic-connection section (sympy complex, line 241) with the
  factorized N=1 route reading 2.4-4.7x MC (z = -1165..-3197). Sections (1)/(1c)
  completed and are banked (E[D^m] m=1..8 at q=0/3; volume q=0 E[D]=0.337868,
  P(N=1)=0.241484).
- Mechanism found during spawn prep (honest disclosure; lanes must MACHINE-VERIFY,
  not assume): J02 updates direc (newu) BEFORE the next step's escape draw, so the
  N=1 step-2 budget is the direction-coupled wall distance
  wall2(s,mu) = -s*mu + sqrt(1 - s^2 (1-mu^2))  (central, q=0);
  instrumented evidence: emp step-2 survival 0.42631 vs mean e^{-wall2} 0.42706;
  corr(mu1, wall2) = -0.766; probe route-D values P(N=1)=0.270246 vs MC 0.2706,
  E[D 1_N1]=0.096876 vs MC 0.096947, E[D^2 1_N1]=0.071575 vs MC 0.071614.

## Lanes (prefix_name owns its files; no collisions; U05/V02 lanes untouched)
### V03b_trio_fix  (door: the ignorance-trio decision tree, V03 successor)
Goal: fix-forward V03's crash (append the KILL-B/UNDET-B rows + robust confusion
counter + output renamed V03b_trio_results.json + partial tree dump), rerun the
FULL locked protocol. Falsifiers: V03_PRE.txt verbatim (KILL-B / VOID-R / VOID-U /
MIRROR / CROSS / HIERARCHY / TRIO-AGREE classes locked before any number).
Kills: any registered check failing -> recorded verbatim, exit per script; the
decision-tree confusion table is the deliverable either way.
### V04b_routeD  (door: the N=1-sector analytic connection, central q=0)
Goal: certify route D (see mechanism above) E[D^m 1_{N=1}], m=1..8, central,
tau0=1, q=0. Kills: K1 route-P(N=1) within 3 SE of MC (V04 recorded
0.270045+-0.000140); K2 every m within 3 SE of MC n=2e6 (24-block jackknife) ->
sector law CLOSED; any miss -> route-D FAIL recorded, exit 1; K3 GL600^2 primary,
GL1200^2 witness |delta| < 1e-12 rel, mpmath 30-dps spot at m=1,2 within 1e-9;
K4 q!=0 legs out of scope (recorded open, not attempted). V04's factorized route
is REFUTED by K2's own evidence table (kept verbatim in the JSON).
### U06_routeD_volume  (door: the same law on the volume source; U03/Kellerer seam)
Goal: volume-source route D: E[D^m 1_{N=1}], m=1..3, q=0, tau0=1, via the 5D
(ρ, c, s, mu, phi) Gauss-Legendre route with chord geometry (given chord half-
length b, source uniform on c in [-b, b]; wall2 from x = (rho,0,c+s),
pd = x.newu = rho*sqrt(1-mu^2)*cos(phi) + (c+s)*mu,
wall2 = -pd + sqrt(pd^2 + 1 - rho^2 - (c+s)^2)).
Kills: K1 route-P(N=1) within 3 SE of MC P(N=1) (V04 recorded 0.241484, n=3e6);
K2 m=1..3 within 3 SE of MC n=2e6 (24-block jackknife); K3 resolution witness
(N=56 grid) rel delta < 3e-3 on every reported moment; any miss -> honest FAIL,
exit 1.

## Deliverables per lane
(prefix).py / (prefix).out (captured, exit line) / (prefix).json (numbers + kills
fired) / short md section appended by the CONDUCTOR at the next tick's register
update. No lane commits. Raw data stays untracked.
