# IMPLEMENTATION A (SHOOTING): the full nonlinear AeST mass-term BVP vs the cluster deficit eta~2.15

*Opus 4.8, 2026-06-14. Companion script + log:
`cluster_aest_shooting_solver.py`, `cluster_aest_shooting_output.txt`. Grade:
**FALSIFIED-AS-CLOSURE.** The mass-term route, done RIGHT (full nonlinear ODE,
physical Phi(inf)->0 BC, one CMB-pinned mu, realistic baryons), gives a robust
DEFICIT eta(R500)~0.33-0.46 at cluster masses -- it is NOT a first-principles cure
for the eRASS1 eta~2.15. Quarantine held: a0/Z never asserted derived; mu flagged
free.*

## The angle that makes this decisive (vs the prior partial)

The prior route (`cluster_aest_massterm_derivation.py`) integrated a **vacuum point
mass outward** with the **natural inner BC** P=G_N M and an explicit free boundary
shift chi_inf (= per-cluster tuning), stopping at 6 Mpc. This implementation builds
the **full nonlinear scalar BVP** and imposes the **physical asymptotic BC by
shooting**, with **realistic baryons** -- and finds the prior "natural-BC deficit"
is the *correct, well-posed, r_max-independent* answer, now with no free constant
left to slide.

## The equations (exact, Durakovic-Skordis 2024 JCAP 04 040 / arXiv:2312.00889)

- Modified Helmholtz (their 2.40): `(1/r^2) d/dr[r^2 M(x) Phi'] + mu^2 Phi = 4 pi G_N rho_b(r)`
- Interpolation (their 2.9): `M(x) = (sqrt(1+4x)-1)/(sqrt(1+4x)+1)`, `x=|Phi'|/a0` (M->1 Newton, M->x deep MOND)
- Mass scale (their 2.18): `mu^2 = 2 K2 Q0^2/(2-K_B)`, `1/mu >~ 1 Mpc` CMB/cosmo-pinned
- Solved in `(Phi, F)`, `F=r^2 M(x) Phi'`: `dPhi/dr=u(F,r)`, `dF/dr=r^2(4 pi G_N rho_b - mu^2 Phi)`.
  The flux inversion is **closed-form** (no root solve): `|u|=a0(sqrt(f)+f)`, `f=|F|/(a0 r^2)`
  (derived + round-trip-verified to 1e-10 in the script).

## Method

- **Full nonlinearity** -- the exact M(x); NO `(mu R)^2` expansion (which the prior route
  showed breaks at mu*R500~1.7). `(mu R500)^2` runs 0.42 -> 1.96 across the sample: the
  expansion is invalid, the full ODE is mandatory.
- **Physical BC = envelope minimization.** The KEY numerical finding: with a **real**
  mass (mu^2>0) the homogeneous outer solutions are **oscillatory with a 1/r envelope**
  (Helmholtz sin(mu r)/r, cos(mu r)/r), NOT decaying Yukawa. So "Phi=0 at one node r_max"
  is **ill-posed** -- it sets only the oscillation PHASE, and eta(R500) then SWINGS
  0.42-1.10 as r_max walks 15->40 Mpc (verified). The well-posed Phi(inf)->0 is the
  solution whose **irreducible outer oscillation amplitude is MINIMIZED** (the particular
  solution sourced by the localized baryons; the homogeneous oscillation driven to its
  floor). Minimizing `E(Phi_c)=max_{r in [0.5,0.95]r_max}|r Phi(r)|` over the shooting
  parameter Phi_c gives an **r_max-INDEPENDENT** eta(R500) (0.437/0.448/0.464/0.496 at
  r_max=20/25/30/40 Mpc -- stable to ~6%). chi_inf is NOT a knob: Phi_c is fixed by this
  condition. Integration to **r_max=30 Mpc** (well past 20 Mpc), DOP853, rtol 1e-10.
- **One CMB-pinned 1/mu = 1 Mpc** (Skordis-Zlosnik 2021 / Verwayen+2024: m^2/f_G <~ 1
  Mpc^-2 => 1/mu >~ 1 Mpc), held **identically** for clusters AND the galaxy check. NOT
  retuned.
- **Realistic baryons**: beta-model hot gas (beta=2/3, rc=0.18 R500) + Hernquist BCG;
  f_gas500 rising 0.09->0.15 with mass (eRASS-like), f_star500=0.012. M500 =
  {1,3,5,10}e14 Msun, R500 from 500 rho_crit(z=0.3) = 0.65-1.40 Mpc.

## Results (all computed; see the log)

**eta(R500) = g_AeST/g_MOND, single CMB-pinned mu=1/(1 Mpc), physical BC, no tuning:**

| M500 [Msun] | R500 [Mpc] | g_bar/a0 | (mu R500)^2 | **eta(R500)** |
|---|---|---|---|---|
| 1e14 | 0.650 | 0.036 | 0.42 | **0.847** |
| 3e14 | 0.938 | 0.066 | 0.88 | **0.634** |
| 5e14 | 1.112 | 0.086 | 1.24 | **0.464** |
| 1e15 | 1.401 | 0.123 | 1.96 | **0.327** |

- **d eta / d log10(M500) = -0.53** -- eta FALLS steeply with mass. eRASS1 is flat-to-
  slightly-falling (slope ~ -0.03) around **eta~2.15**. The model has the wrong *sign of
  the offset* (deficit not excess) and far too steep a mass trend.
- **Radial shape (5e14): peak-then-dip, never reaching the target.** eta rises to ~0.90
  at ~0.5 R500, DIPS to 0.46 at R500, then a weak secondary bump to **1.07 at r~1.8
  R500** (the "helpful" peak the literature names -- barely above MOND, at the WRONG
  radius), then drops again. This matches Durakovic-Skordis "a peak followed by a deficit
  (negative phantom mass)" exactly -- and it never approaches 2.15 anywhere.
- **Peak radius grows with mass** (1.59->2.21 Mpc for 1e14->1e15) but **slower than
  sqrt(M500)** (r_peak/sqrt(M/5e14) DROPS 3.56->1.56), so it cannot be parked at each
  R500 without per-cluster tuning.
- **Galaxy-safety at the SAME mu: PASSES.** SPARC-like disk (Mbar=6e10 Msun): AeST/MOND
  deviation over 10-30 kpc is **0.19% max** -- galaxies stay MOND-pure. The mass term is
  genuinely OFF in galaxies and ON at clusters with one mu.

**Both ways -- what would 2.15 cost?** Scanning 1/mu (one mu per row, never retuned),
eta(R500) at 5e14 peaks at only **~0.92** (1/mu=0.5 Mpc) and then FALLS again as mu grows
(1/mu=0.35,0.25 -> 0.46, 0.41 -- the oscillatory regime), while the galaxy deviation at
25 kpc climbs past ~1% by 1/mu~0.25. **No single mu delivers eta~2.15 at R500 while
keeping galaxies MOND-pure** -- the boost simply never reaches 2.15, and what little
boost there is requires mu where galaxies start to break. The galaxy<->cluster scale
tension (Mistele+2023) is reproduced directly here, end to end.

## Verdict: FALSIFIED-AS-CLOSURE

Done on its own terms, fully nonlinear, with the physical (well-posed, r_max-independent)
boundary condition and realistic baryons, the AeST scalar mass term gives a **robust
DEFICIT eta(R500) ~ 0.33-0.46** at cluster masses (a weak excess only at r~1.8 R500, the
wrong radius; only the lightest 1e14 group nears unity, at 0.85). It does **NOT** produce
the eRASS1 eta~2.15 from first principles, the mass trend has the wrong sign and is far
too steep, and **no single CMB-pinned mu** reaches 2.15 without breaking galaxies. The
prior route's eta=2.15 came only from a per-cluster boundary shift chi_inf -- and once the
physical BC removes that freedom, the boost is gone. The mass term is a **genuine
intrinsic AeST mechanism at the right scale** (galaxies provably untouched, 0.19%), but as
a cluster cure it is **falsified as a closure**: bank it as a *prediction of a deficit*,
not a fix. The eRASS1 cluster problem remains MOND's shared, unsolved liability.

Both ways, honestly: this is a clean fail for the mass-term-as-cluster-cure hypothesis, not
a manufactured one and not a manufactured win. The numbers are robust (r_max-independent,
galaxy-safe, closed-form-verified integrator).

**Quarantine:** a0/Z never asserted derived; mu flagged as a free AeST constant, CMB-pinned,
held identical for galaxies and clusters.

Sources: Durakovic & Skordis 2024 JCAP 04 040 (arXiv:2312.00889); Verwayen, Skordis &
Zlosnik 2024 MNRAS 531 272 (arXiv:2304.05134); Skordis & Zlosnik 2021 PRL 127 161302;
Mistele, McGaugh, Schombert 2023 A&A 676 A100 (arXiv:2301.03499). eRASS1 target banked in
`real_research/FRAMEWORK_EMPIRICAL_STANDING.md` (eta_median 2.15, geomean 2.36).
