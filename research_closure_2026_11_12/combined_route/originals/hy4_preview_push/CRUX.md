# The reach-amount lock (2026-11-11)

Adopts nothing. kappa = 1/2 FITTED; not theory closed. Not a lane: no criteria, no label, nothing graded.
Arithmetic in `hy4_crux_check.py` -> `hy4_crux_check.out`. Footings never pooled.

## The claim

CLOSURE.md names the joint as three failures (space, constant, time) and the amount as a transport shortfall.
The record's own exact results make it stronger than that: **the amount is capped by a conservation law, and the
cap is below what the law requires, at the radii where lensing sees the law.** So the joint is not "we have not
found how the charge gets there" — it is "the charge is not there."

## The chain

1. **T4** (AKS1 / SMF1 S0b, exact): the net polarization charge inside any ball whose boundary free-falls is 0 at
   all times, **for any momentum equation**. Polarization cannot be manufactured during infall.
2. **LFS1** (exact): for a static clock the polarization is frozen; the halo's charge changes only by
   O(|Phi|/c^2) ~ 1e-6.
3. From 1 and 2: **the halo's charge equals the dust charge carried in by the clock's flow.**
4. The dust charge available is the cosmic share, Omega_c/Omega_b = 5.41 M_b. What actually turns around is
   **0.9 to 1.4 M_b** (VSH1, COL1), because with the law on the clock's own self-gravity is cancelled below
   1/mu_K (TPA1 4.4), so only the baryons pull it in.
5. The law requires M_c(<r) = M_b X(x), X(x) = (sqrt(1 + 4x^2) - 1)/2, x = r/r_M. X exceeds the whole budget at
   **x = 5.8888 r_M** and then grows as x.

## The numbers (computed, both footings)

Independent audit at FLD1's **actual** KiDS window radii, four KiDS masses, log M_b 9.4 / 10.45 / 10.7 / 10.9
(`closure_2026_11_10/AMT1_amount_budget/`, `amt1_budget.py` -> `.out`; 15 recorded cross-checks reproduce,
worst relative miss 3.1e-3). Canonical footing, log M_b 10.45, r_M = 6.479 kpc:

| r (kpc) | x = r/r_M | demand X(x) [M_b] | / 5.41 budget | / 1.06 delivered | where the radius comes from |
|---|---|---|---|---|---|
| 10 | 1.543 | 1.12 | 0.21x | 1.06x | SPARC radii |
| 30 | 4.630 | 4.16 | 0.77x | 3.92x | COL1 Part 0 |
| **38.2** | **5.889** | **5.41** | **1.00x** | 5.10x | **entire cosmic budget spent here** |
| 139 | 21.45 | 20.96 | 3.87x | 19.8x | FLD1 R_fold(z=0) |
| **272** | **41.98** | **41.48** | **7.67x** | 39.1x | **FLD1 KiDS inner window edge** |
| 389 | 60.00 | 59.50 | **11.00x** | 56.1x | ONE1 end radius, X_s = 59.5 |
| **637** | **98.32** | **97.82** | **18.08x** | 92.3x | **FLD1 KiDS middle window edge** |

**The shortfall is mass-independent and footing-independent**: X_s / 5.41 = 10.99 / 11.01 / 10.99 / 11.01 across
the four KiDS masses (alt: 12.09 to 12.11), because the windows scale with r_M.

**And the data reject the budget directly**: ONE1's brackets reject the cosmic share X = 5.41 at **+4.85 /
+4.93 sigma**. So the gap is not an artefact of how the share was fitted — it is measured.

Where each amount runs out (log M_b 10.45): delivered 1.06 M_b at 9.6 kpc; VSH1's settled 1.40 M_b at 11.9 kpc;
X-COP's edge 4.94 M_b (HIS1) at 35.1 kpc; the cosmic budget at 38.2 kpc; the share ONE1 needs at 389 kpc.

The share ONE1 needs to pass KiDS host-free, X_s = 59.5 M_b, is **11.00x the entire budget**, **56x the 1.06 M_b
the record's own infall dynamics deliver**, 42.5x VSH1's 1.40 M_b settled charge. The budget itself is only 5.10x
the delivered charge.

## The two kills I ran

**Kill 1 — the anisotropic stress cannot pay it.** The static halo is held by
Pi_ij = J(g) delta_ij - g_i g_j/(K(1+u)), and in the deep field **Pi_rr = -Pi_tt exactly** (computed: the ratio
(Pi_rr + Pi_tt)/Pi_tt falls to 6.6e-3 at 100 r_M). So the radial "dispersion" is **negative**,
sigma_r^2 = -v_inf^2/2 with v_inf^4 = G M_b a0. A kinetic gas cannot do that; a medium with a shear modulus can.
The natural escape is that the *stress* carries the lensing and the mass does not have to exist. It does not
work: the active (Tolman) source of a static spherical configuration is rho + (p_r + 2 p_t)/c^2, and with
p_r = -p_t that is rho + Pi_tt/c^2, so the fractional correction is sigma_t^2/c^2:

| log M_b | canonical | alt |
|---|---|---|
| 9 | 1.96e-08 | 2.16e-08 |
| 11 | 1.96e-07 | 2.16e-07 |
| 13 | 1.96e-06 | 2.16e-06 |
| 15 | 1.96e-05 | 2.16e-05 |

against a shortfall of a factor 5 to 18. **The stress tells you what the medium is; it does not pay the amount.
The lensing signal is mass.**

**Kill 2 — the elastic reading does not evade M5.** sigma_r^2 < 0 requires a shear modulus, i.e. a solid. M5's
theorem has three hypotheses: local, momentum-conserving, normally self-gravitating. A solid with a local
constitutive relation is local and momentum-conserving, so M5 bites unless the self-gravity is not normal.
That is ELA1's gate (HY4-7).

## What this changes

- The joint is one lock, not three. Space, constant and time all fail because they are attempts to move charge
  that the conservation law caps.
- The "amount" is no longer a mechanism question. It is a **budget** question, and there is exactly one
  reconciliation inside the record: **g_bar at KiDS radii is missing the hot gas.** The law would have to be
  evaluated with g_bar raised 11.0x at those radii. The record's own words: "with B21's own hot-gas estimate in
  g_bar, its published outer points drop from 1.50 to 0.47 of the law. Nothing on disk measures that gas."
- **The bar for that reconciliation is now measured, not guessed**: ONE1's brackets reject the cosmic share
  X = 5.41 at +4.85 / +4.93 sigma. Whatever the gas supplies has to move a 5-sigma-measured gap, and it has to
  do it at the radii FLD1 names (272 kpc for the inner window, 637 for the middle), not at SPARC radii.
- So the first thing to decide is not a mechanism. It is whether 59.5 M_b is a requirement or a census error.
  Lane HY4-1 (GAS1) is computing it bin by bin against every constraint on disk.

## Pre-registered consequence

If GAS1 finds that the gas on disk can supply less than half of the 11.0x, then form B's halo is not the cold
charge, and the record must choose between:
(a) breaking the conservation law (HY4-4, VCC1), or
(b) the halo not being a density at all — which Kill 1 above excludes within GR, or
(c) form B being wrong.

I would bet on the gas. The bet is registered here, before GAS1 reports.

## Bet settled 2026-11-11: LOST

**GAS1 fired four of five gates against it, and the amplitude gate killed it outright:**

- The gas the reading needs is a **fixed surface density** Sigma_gas = a0/(pi G x_b^2) = 6.1627 / 7.4477 Msun/pc^2,
  constant in radius out to 2.6 Mpc.
- Against all baryons in the same sphere: over by 284-574.
- Against B21's own hot gas: over by 328-3750.
- Against GO1's measured group gas: +8.0 to +16.3 sigma.
- **Amplitude:** with that gas in g_bar the outer points sit at 0.0392 +- 0.0069 / 0.0324 +- 0.0057 of the law,
  against the record's 0.891 gate. 36x / 41x below, more than 100 sigma.

Only G5 (required gas density against rho_b, 1.38 / 1.67) did not fire.

What survives is narrow: the gas column the **cluster** rows need is within a factor ~1 of what X-COP measures
(ratio 0.37 to 1.26), so a baryon reading of the amount is still open at cluster and group scale. The
**galaxy** leg is closed.

Full verdict moved to `CLOSURE.md` — this file keeps the arithmetic.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
