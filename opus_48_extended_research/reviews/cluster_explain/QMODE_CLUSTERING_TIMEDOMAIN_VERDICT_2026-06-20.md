# Cluster residual: Q-mode dust clustering (centerpiece) + time-domain/formation MI — verdict 2026-06-20

*Script: `cluster_explain/qmode_clustering_and_timedomain_MI.py` (numpy + sympy, runs clean).
Framework footing: a0=9.36e-11 (INPUT, quarantine held), dS-Unruh g_obs=sqrt(g_bar^2+g_bar*a0).
Both-ways: galaxy-RAR veto is the hard wall; no manufactured close, no reflexive dismissal.*

## HEADLINE
**Both routes FAIL to close the cluster core, and they fail for the SAME deep reason the banked
work found — but this run makes the failure mechanism CRISP and quantitative, and it credits the
real partials honestly.** The Q-mode dust CAN supply the core mass arithmetically (it is ~1.4x the
needed core residual if it clusters like CDM), but the clustering that closes clusters is
*indistinguishable from CDM* and therefore clusters in galaxy disks too, breaking the RAR. There
is NO scale knob (Jeans window is EMPTY and BACKWARDS-ordered; Bridge-1: a0 absent from growth).
The time-domain MI gives a *smaller* mean mass than quasi-static (wrong direction), and the
formation-epoch a0(z) lever is wrong-signed (higher early a0 imprints LESS phantom mass).

## ROUTE 1 (CENTERPIECE) — Q-mode dust clustering: CLOSES ARITHMETICALLY, KILLED BY THE VETO
1. **Generative credit (the dust DOES supply the mass):** a CDM-like dust of the cosmic amount
   puts **3.28e14 Msun inside 420 kpc** of a 1e15 cluster vs the **2.3e14 Msun** core residual needed
   — **ratio 1.43**. So the centerpiece's premise is RIGHT: the framework's cold Q-mode, clustering
   like CDM, more than covers the core. This is exactly how AeST is designed (MOND galaxies + a
   CDM-like gravity-mode dark sector).
2. **The Jeans scale-selection has NO window, and it is ordered BACKWARDS.** To be smooth in a galaxy
   (lambda_J >= 30 kpc) needs cs >= **135 km/s**; to be clumpy in a cluster (lambda_J <= 400 kpc)
   needs cs <= **57 km/s**. EMPTY (135 > 57). And the ordering is adverse: galaxy cores are ~1000x
   DENSER than cluster cores, so the Jeans length is SHORTER in galaxies — a single cs cannot turn the
   dust ON in clusters and OFF in galaxies. (AeST's Q-mode is in fact cs^2->0 sub-horizon — that is
   WHY it fits the CMB third peak like CDM, banked dark_sector_cmb — so it clusters at ALL scales down
   to a tiny Jeans length: maximally galaxy-UNsafe.)
3. **Galaxy veto, direct (the kill):** inject the CDM-like dust on a fiducial SPARC disk. The pure law
   sits at -0.119 dex (on the RAR). Adding the dust at the level it would sit inside an optical disk:
   **30% -> +0.019 dex, 60% -> +0.124 dex, 100% -> +0.233 dex**, PLUS halo/disk-ratio scatter
   galaxy-to-galaxy. The RAR is 0.11-0.14 dex tight. A dust clustered enough to matter in clusters
   re-introduces exactly the cuspy-halo scatter MOND was built to avoid.
4. **Framework's own no-go (why no knob exists):** Bridge-1 (banked) proves a0 is ABSENT from linear
   perturbations, so Q-mode growth knows nothing about a0 — it grows by pure gravitational instability,
   identically to CDM. The amplitude I0 is a single FREE number; fixed at ~Omega_dm for the CMB, it is
   then fixed everywhere. It clusters in galaxies too. **=> CDM relocated, not eliminated** (consistent
   with the banked DARK_SECTOR_CMB verdict).

**Route 1 verdict:** the centerpiece closes the cluster ONLY by being CDM, and CDM fails the galaxy
veto. The "stays smooth in galaxies / clumps in clusters" hope has no realization: no Jeans scale, no
a0-gate, single free I0. This is a real, generatively-explored CLOSE of the idea — the residual is NOT
the field "doing its job" galaxy-safely; it is CDM by another name.

## ROUTE 2 — time-domain / formation-epoch MI: WRONG-SIGNED, SMALL
- **(2a) Multi-frequency MI (honest Milgrom-2022 rms-argument):** cycle-averaged mu uses the rms
  acceleration (>= mean), so mu_MI >= mu_QS and the effective-mass boost 1/mu_MI <= 1/mu_QS. Across
  gbar/a0 in {0.037, 0.44} and ecc in {0, 0.5, 0.9}, **boost(MI/QS) <= 1.000** (e.g. 0.24 at ecc=0.9).
  The non-quasi-static MI gives LESS mean mass, not more. (The banked Jensen-17x apocenter singularity
  reproduced as VOID.)
- **(2b) Formation-epoch a0(z):** the w=-1/declining branch gives **a0(z)=CONST** (no effect). The
  rising branch gives a0(z=2)/a0 ~ **3.0**, but since deep-MOND M_eff ~ sigma^4/(G a0), a HIGHER
  formation a0 IMPRINTS a SMALLER frozen phantom mass (factor 0.33 at z=2) — the **WRONG sign** for a
  mass SURPLUS. And clusters re-virialize to today's a0 (not frozen relics). Banked +2.5% at z=0.296
  stands; <= +10-25% at z=2, sign-ambiguous, z-reach-limited.
- **(2c) sympy pin:** d ln M_eff / d ln a0 = **-1** exactly; deep-MOND scale invariance fixes
  M*G*a0 = eta*sigma^4 with eta=O(1) SHARED by MI and MG. Time-domain MI cannot manufacture mean mass
  beyond this. **MI == MG on the cluster mean mass.**

## BOTH-WAYS / QUARANTINE
- **Credits (full weight):** Route 1's dust arithmetically supplies the core (1.43x) — the AeST-design
  premise is correct; the framework HAS a cold, CMB-required, Omega_dm-worth dark sector.
- **Concessions (full weight):** that dust is CDM (galaxy veto +0.12 to +0.23 dex), no scale/a0 knob
  makes it cluster-selective; time-domain MI is wrong-signed/small; formation a0(z) is wrong-signed.
- a0/Z/kappa/I0 never asserted derived (a0 INPUT, I0 FREE). No new fundamental particle invoked.
- Consistent with banked CLUSTER_RESIDUAL_CLOSURE / CLUSTER_CLOSURE_HUNT2 / DARK_SECTOR_CMB: the
  cluster core stays a **MOND-family-SHARED open gap** — neither a kill nor a closure; the framework's
  own field route (AeST Y-Q force ~17-20%) plus IGIMF remnants remain the live no-particle partials,
  and the dust-as-CDM is the honest cold dark sector the CMB+clusters require (relocated DM).
