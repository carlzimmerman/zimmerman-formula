# WM1 AMENDMENT A2: gate 0, SEEDING (committed alone, before any gate-0 number)

Criteria 6e40130dfa, A1 5cba17a249. Adopts nothing. kappa = 1/2 FITTED; not theory closed. Footings never pooled.

**Disclosure of timing.** WM1's RESULT (d45cfa36da) has already landed as FAIL / FAIL, first failing gate 2 groups. The orchestrator
asked for this gate after that result, relaying the outside source's round-16 numbers to CHECK, not adopt. No gate-0 quantity has
been computed. A2 changes the label's order only: gate 0 is graded first, and if it fails, the label becomes "FAIL at seeding".
The earlier gates and their numbers stand unchanged.

## Gate 0: can the construction seed galaxy-scale structure?

**Initial conditions from CLASS, not from a growing-mode guess.** Each species' Newtonian-gauge-free density transfer
(synchronous gauge; the gauge term is negligible for k >= 0.05 h/Mpc at z 1000) is taken from CLASS at z 1000 and z 950. The
derivative d delta / d ln a comes from the finite difference. So the baryons start Silk-damped and drag-released, and the relic
starts with its own free-streaming cut.
- delta_b, delta_chi at z 1000; d/d ln a from z 1000 -> 950.
- The two-fluid ODE of FROZEN section 2 then runs from z 1000 to z 0. Graded with the law on (nu from the cold reference power,
  A1); Newton (nu = 1) beside.
- Free streaming after z 1000 is not in the ODE (pressureless component). This is disclosed; KA-S1 below bounds it.

**Reported:** the baryon and total-matter power relative to the cold reference (CLASS, omega_cdm), P_X / P_ref, at k 0.5, 1, 2,
5 h/Mpc and z 3 and z 0, law on and Newton.

**Graded line (halo formation).** The cumulative number density of collapsed halos n(> M) at M = 1e10, 1e11, 1e12 Msun and z 2 and
z 0 is computed by Press-Schechter on the model's linear total-matter power, delta_c 1.686.
- The **graded filter is the sharp-k filter** with c 2.5 (Benson et al. 2013; Schneider et al. 2013). This is the standard for
  truncated spectra: a top-hat filter manufactures spurious small halos below the cut. The top-hat reading is reported beside.
- The baryon-power reading (n from P_b) is reported.
- **Gate 0 PASS iff n(> M) >= 0.5 x the cold reference's n(> M)** at every M in {1e10, 1e11} and z in {2, 0}. The cold reference
  with Newtonian growth is the spectrum the record's abundance matching (Moster 2013, used by SS1's AM bracket) maps onto the
  observed stellar mass function. The 0.5 is a disclosed line, not a record line.
- **FAIL** otherwise: the label is then "FAIL at seeding", with the numbers. Overproduction is reported, not graded here; it is
  bounded by gates 8 and CS.
- 1e12 is reported only.
- Disclosed approximation: linear power with delta_c 1.686 under the law. The law also speeds nonlinear collapse, so this reading
  is generous to formation.

**Known answers.**
- **KA-S1:** Newton (nu = 1) from the CLASS IC reproduces CLASS's own warm total-matter power at z 0 within 5 % at k <= 1 h/Mpc,
  and within 25 % at k 2 h/Mpc. That bounds the effect of post-z 1000 free streaming.
- **KA-S2:** Newton with the cold reference IC reproduces CLASS cold within 2 % at k 0.5-5 h/Mpc, z 0.
- **KA-S3:** the reference n(> M) is identical under both filters at M >= 1e12 within a factor 1.5. This is a filter sanity check,
  reported.

**Relics.**
- Graded: the frozen W (188.7 eV, M_hm 4.97e12).
- Reported bracket: the outside source's relic, m 107.5 eV (the middle of its 105-110).
- MUTATE MW1 / MW2 are rerun through gate 0 (reported).

## Source numbers checked (reported, never adopted)

- M_hm(m) by the source's formula 1.19e10 (m / keV)^-3.33 against this lane's Viel half-mode, at 105, 107.5, 110 and 188.7 eV.
- k_hm at 107.5 eV, from CLASS.
- The source's capture f = [1 + (M_hm / (2 M_tot))^0.8]^-1.5, at its own M_hm and at W's, for:
  - lenses at M* 10^10.5, 11, 11.3, 11.5 (M_tot = 6.41 M_b, with M_b = M* as the source states);
  - groups at M500 2.1e13, 4.5e13, 1.4e14 (raw f; its "phase-space core" is not modelled).
- Primary CMB |Delta C_l / C_l| (TT) at l < 800 and at l 2500, and C_L^phiphi warm / cold at L 100, 300, 1000 for the 107.5 eV relic
  (CLASS). Also with the law (WM1's S_B at L 100 and 300; L 1000 only if the record's Limber grid reaches it, otherwise stated).

## Nonlinear response

The lane's machinery is linear plus SS5's 1D sheet code (another lane, not run here). The RESULT states what the linear system
can and cannot say about mode coupling. It does not claim a nonlinear number.

Files: wm1_seed.py -> parts/seed_<footing>.json, wm1_seed.out. Small outputs only.
