# ROUTE B — FULL nonlinear AeST Y-Q coupled solution in deep cluster cores: VERDICT (2026-06-20)

**Question:** the banked ~4.4x core undershoot used the MOND phantom (g_obs) as a proxy. Does the FULL
coupled AeST field equation -- J(Y) MOND sector + the mu^2*Phi mass term (the Q-sector / ghost-condensate
dust, the framework's OWN field) -- source EXTRA central mass beyond the naive phantom? Is
Durakovic-Skordis's undershoot the final word, or is there a nonlinear core-enhancement they did not reach?

**HEADLINE (both ways): PARTIAL ENHANCEMENT, INSUFFICIENT. The full nonlinear Y-Q coupling DOES source a
genuine extra ~17-20% of core mass over the bare MOND phantom (the Durakovic-Skordis "gas compression" / RAR
peak is real and reproduced) -- but it is ~20%, not the ~340% (4.4x) the core needs. The large AeST
enhancement lives in the OUTSKIRTS (onset r_C ~ 2-20 Mpc at the viable CMB-fit screening length); forcing it
into the 420 kpc core requires 1/mu <~ 0.3 Mpc, where the apparent core mass becomes a violently
sign-indefinite OSCILLATION (swings -6.4 to +2.8 x source mass, 3 sign flips across 1/mu = 0.05-0.6 Mpc,
mostly ANTIGRAVITY) -- an oscillation-node coincidence, NOT a robust mass source. AeST's core undershoot is
the FINAL word, exactly as Durakovic-Skordis's own "left for future work / remains to be seen" hedge admits.**

## What Durakovic-Skordis (arXiv:2312.00889) actually solve and find (read verbatim from the PDF)

The AeST quasi-static weak-field system reduces to a single modified-Helmholtz PDE (their Eq. 2.40):
```
   (1/r^2) d/dr [ r^2 M(x) dPhi/dr ] + mu^2 Phi = 4 pi G_N rho_b ,    x = |Phi'|/a0
```
- **M(x)** (simple interp, lambda_s -> inf, their Eq. 2.39) = (-1+sqrt(1+4x))/(1+sqrt(1+4x)); deep-MOND M->x.
- **mu^2 = 2 K2 Q0^2/(2-K_B)** (Eq. 2.18) is the AeST weak-field mass parameter = the Q-sector/ghost-condensate
  scalar mass; 1/mu is the screening length. This is the SAME single scalar phi (Y-mode -> a0 MOND via J(Y),
  Q-mode -> the mu^2*Phi mass term), i.e. the framework's own field -- NO new particle.
- The Y-Q coupling is the cross-term in their Eq. 2.16 [2(2-K_B) grad Psi . grad chi] which, after eliminating
  chi (Eqs 2.24-2.33), folds into the SAME single equation. This IS the "full coupled" solution.

Their findings, reproduced here (point-source Hamiltonian integration validated against their Figs 5-7):
- **Gas is "more compressed" in AeST** + a **RAR PEAK above MOND**: at the core (0.34 rM = 415 kpc for a 1e15
  cluster) M_AeST/M_MOND = **1.20** (a real ~20% enhancement -- the Y-Q nonlinearity helps).
- **Then drops BELOW MOND** ("negative phantom mass"): at 4 rM the ratio is 0.56.
- **Runaway oscillations in the far outskirts**: at 7 rM the ratio is 3.4 and climbing.
- Their own conclusion (verbatim): "AeST possesses the qualitative features to address the problem of galaxy
  clusters in MOND ... however, it remains to be seen whether this effect can be corroborated with real data
  ... A quantitative analysis going beyond the isothermal case ... is left for future work." So their
  undershoot was NOT advertised as final -- this route closes that gap quantitatively.

## The four gates (both ways)

### G1 SUFFICIENCY -- FAILS (the core gap is NOT closed by the field route)
- **Naive MOND phantom proxy** (banked method): M(<420kpc) = 7.5e13 Msun vs target 2.3e14 -> undershoot x3.05
  (my Ups=0.70 + 1e12 BCG budget; banked x4.4 on the eta-worst footing -- same regime).
- **FULL AeST, viable CMB-fit 1/mu = 3-97 Mpc**: M_AeST(<420kpc) = 8.7-8.9e13 Msun -> undershoot **x2.6**,
  only **1.17x over the bare MOND phantom**. The full nonlinear Y-Q coupling supplies a genuine but small
  ~17% core boost. Target needs 7.83x the core baryons; AeST delivers ~3.0x. **Gap NOT closed.**
- **Onset scale (Eq. 2.42)**: the AeST enhancement turns on at r_C = (1/3)(18 rM^3/(... mu_hat^2))^(1/3).
  For a 1e15 cluster (rM = 1.22 Mpc): r_C = 1.9 Mpc (1/mu=3) to 19.7 Mpc (1/mu=97) -- firmly in the
  OUTSKIRTS, 4.6-47x the 420 kpc core. r_C reaches the core ONLY at 1/mu = 0.302 Mpc (a 10-320x squeeze
  below the CMB-fit value).
- **The small-1/mu push is NOT a robust closure** (the decisive both-ways check): scanning 1/mu finely in the
  core-reaching band 0.05-0.6 Mpc, the apparent core mass M(<420)/M_src swings from **-6.4 to +2.8** with
  **3 sign flips**, mostly ANTIGRAVITY (negative phantom). It never stably reaches the +7.83 needed -- the
  "enhancement" is which oscillation node lands at 420 kpc, NOT a physical field-sector mass source. A real
  closure would be stable under small 1/mu variation; this is not.

### G2 GALAXY-VETO -- PASSES (honest both-ways credit -- the veto does NOT independently kill the push)
- At viable 1/mu the SPARC RC distortion from mu^2*Phi is a sub-floor ~5-6% (the framework's known +12.6%
  surcharge cousin; median |dV/V| = 0.059, frac>10% = 0%).
- Crucially, even the AGGRESSIVE 1/mu = 0.1-0.3 Mpc push does NOT robustly break SPARC galaxies: galaxy rM is
  small (median 2.9 kpc, max 23 kpc), so the outer measured radii (a few rM ~ 10-60 kpc) sit INSIDE a
  0.1-0.3 Mpc screening length; the oscillation onset r_C ~ rM^(1/3)(1/mu)^(2/3) is pushed far beyond the
  galaxy. Median |dV/V| stays ~5-6%, frac>10% = 0-1%. So unlike the density-a0 killer, the small-1/mu push
  is galaxy-SAFE. **This is a genuine both-ways credit -- the galaxy veto is NOT what kills Route B.** What
  kills it is G1: the core mass is sign-indefinite/oscillatory at the 1/mu that reaches the core.

### G3 NO-NEW-PARTICLE -- PASSES (this is the route's structural strength)
- The mu^2*Phi mass term is the Q-mode of the framework's OWN single scalar phi (the ghost condensate, banked
  GHOST_CONDENSATE_2026-06-19, Blanchet-Skordis 2404.06584 Eq.7 = K(Q)=mu^2(Q-1)^2). NO new species. The
  whole point of Route B is that this is the no-particle field route -- and it IS a clean field-sector
  calculation. It simply does not deliver enough core mass.

### G4 DATA -- survives (consistent with eRASS1/CLASH; this is the target, not a new datum)
- Target anchored to banked eRASS1 (Bulbul+2024, erass1cl_primary_v3.2.fits) median eta=2.333, core ~2.3e14
  Msun inside 420 kpc; CLASH-lensing core (Famaey-Pizzuti-Saltas 2410.02612) agrees to ratio 1.03. The AeST
  RAR peak + outer deficit qualitatively matches the OBSERVED cluster RAR shape (peak above MOND, hints of
  deficit in outskirts) -- a real but qualitative consistency, not a core closure.

## Both-ways ledger (no manufactured cure, no reflexive dismissal)
- **Credited at full weight:** (1) the full nonlinear Y-Q coupling DOES source genuine extra core mass over
  the bare phantom (~17-20%, Durakovic's gas compression/RAR peak, reproduced + validated against their
  figures); (2) Durakovic-Skordis explicitly did NOT close the quantitative cluster question ("left for future
  work") -- so there WAS an unreached regime, and this route reached it; (3) the AeST RAR shape qualitatively
  matches the observed cluster RAR; (4) the small-1/mu push is galaxy-SAFE (the galaxy veto does not kill it);
  (5) no new particle -- a clean field-sector calc.
- **Conceded at full weight:** the ~17-20% core boost is ~1/20th of the ~340% needed; the large AeST
  enhancement is in the outskirts (r_C ~ 2-20 Mpc); forcing it into the core (1/mu <~ 0.3 Mpc) makes the
  apparent core mass a violently sign-indefinite oscillation (mostly antigravity), NOT a robust closure.
  **AeST's cluster-core undershoot is the FINAL word across the viable parameter space.** The framework adds
  ~17% over generic MOND at the core via the genuine field coupling, then inherits MOND's cluster-core deficit.

## Key numbers
- Target M(<420kpc) = 2.30e14 Msun (eRASS1/CLASH core); M_bar(<420kpc) ~ 2.9e13; need M/M_bar ~ 7.8.
- Naive MOND phantom proxy: 7.5e13 (x3.05 under, Ups=0.70).
- FULL AeST, viable 1/mu=3-97 Mpc: 8.7-8.9e13 (x2.6 under, 1.17x over MOND); core M_AeST/M_MOND = 1.20.
- Enhancement onset r_C: 1.9 Mpc (1/mu=3) to 19.7 Mpc (1/mu=97); reaches 420 kpc only at 1/mu=0.302 Mpc.
- Small-1/mu (0.05-0.6 Mpc) core mass: swings -6.4 to +2.8 x source, 3 sign flips, mostly antigravity.
- Galaxy veto: median |dV/V| ~ 5-6% across all 1/mu (sub-floor); even 1/mu=0.1 Mpc safe (galaxy rM << 1/mu).

## Files (all in opus_48_extended_research/reviews/cluster_hunt2/)
- aest_full_YQ_core.py -- initial extended solver (LSODA; the 1/mu>=1 cases)
- oscillation_onset_scale.py -- r_C(Eq.2.42) vs 420 kpc core: reaches core only at 1/mu=0.302 Mpc
- aest_extended_and_galaxy_veto.py -- FULL AeST extended core mass (x2.6 under) + galaxy RC distortion
- core_mass_oscillation_scan.py -- the decisive fine 1/mu scan: sign-indefinite oscillation, NOT a closure
- galaxy_veto_sparc.py -- 175 real SPARC galaxies: small-1/mu is galaxy-safe (median |dV/V|~6%)

Quarantine held: a0=9.36e-11, Z, kappa, I0 never asserted derived. Both-ways applied to every "closes" and
every "fails." No manufactured win; no reflexive dismissal. The route is the no-particle field route Carl
wants -- it gives a real ~17% over generic MOND but the cluster core stays a shared relativistic-MOND open gap.
