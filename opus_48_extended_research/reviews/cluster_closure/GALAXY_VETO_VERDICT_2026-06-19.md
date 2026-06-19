# The GALAXY VETO on the two cluster closures — VERDICT (2026-06-19)

*The make-or-break test. For each candidate closure, does it break the galaxy-scale RAR/BTFR where
the framework/MOND is nailed at ~0.13-0.14 dex on 175 SPARC galaxies? Framework sealed: a0=9.36e-11,
dS-Unruh nu g_obs=sqrt(g_bar^2+g_bar*a0), Ups~0.70. Both ways. Quarantine held (a0/Z not derived).
Code: galaxy_veto_test.py, galaxy_veto_bothways.py (run, reproduced).*

## Bottom line
The veto cleanly SEPARATES the two closures — this is the whole point of the veto, and it lands exactly
where 40 years of MOND cluster fixes landed:

| Closure | Galaxy-scale signature | Veto |
|---|---|---|
| **Topic-2: eV collisionless residual on cluster galaxies** (sterile/active nu, or undetected baryons) | Tremaine-Gunn forbids it from packing into a galaxy: m_TG,min ~ 28-174 eV (my calc) / 100s eV-keV (lit). An eV state is phase-space-excluded from galaxies by 4-16 orders in density. Contributes <1% of galaxy baryonic mass, <10 km/s on the outer RC. | **PASSES** |
| **Topic-3: density-a0 MI-dynamic flattening** (a0 ~ sqrt(rho_local)) | Same law on galaxy disks gives a 200-400x median (up to 1.6e4x) a0 boost. RAR scatter blows from ~0.14 dex to ~0.36-0.38 dex (2.6x the floor, +0.23 dex). No fixed smoothing L threads cluster-ON / galaxy-OFF. | **BREAKS** |
| Topic-3b: genuine MI non-adiabatic theta(y) sigma-spread | On a galaxy disk omega_ex/omega_in ~ 0.02-0.10 (deeply adiabatic) -> theta->const -> exactly MOND. Null on the RAR. | **PASSES (null)** |

## (a) Does the topic-2 matter component add mass inside galaxies? NO — verified via Tremaine-Gunn.
The historical eV-neutrino cluster fix (Sanders 2003, Angus+2008/2010, 11 eV sterile or 2 eV active)
survives the galaxy veto for a DEEP reason, not a fudge: the **phase-space (Tremaine-Gunn 1979) bound**.
A thermal/collisionless fermion of mass m can pack a max coarse-grained phase-space density Q_max ~ m^4;
to gravitationally dominate a galaxy core (sigma~10-150 km/s, r_c~0.3-3 kpc) requires m >~ 28-174 eV
(my degenerate-packing calc) — the refined literature bounds are m >~ 0.13-0.18 keV (Pauli, 95%) up to
0.41-0.59 keV (thermal relic). An **eV-scale** residual is below this by 1-4 orders in m, i.e. ~4-16
orders in packable density. It free-streams out of galaxies: on a 10-20 kpc galactic scale the neutrino
halo is <1% of the baryonic mass and adds <10 km/s to the outer rotation curve (Sanders/Angus, verbatim
literature). **So the cluster-fix mass is automatically ABSENT from galaxies — RAR untouched.** This is
precisely why eV-neutrino cluster fixes did NOT die on the galaxy veto (unlike modified-law fixes).
COST (quarantine): it is a SEPARATE mass component, not given by a0=Lambda; it relocates rather than
solves the cluster problem (what is the eV residual?), and DESI Sigma m_nu < 0.072 eV kills the *active*-
neutrino version by ~80x, pushing it to a sterile/dark-baryon residual.

## (b) Does the topic-3 MI-dynamic boost change galaxy rotation curves? YES — fatally, for density-a0.
The density-a0 reading (a0_local = (c/2)sqrt(G rho_local) = a0_FW*sqrt(rho_local/rho_DE)) is the one
zero-parameter mechanism that genuinely FLATTENS the cluster eta(r) deficit (banked: 1.55-7.66 -> 0.75-1.30,
CLUSTER_DENSITY_A0_SHAPE_RECONCILED). Applied to galaxy disks — where rho_disk ~ 1e5-1e6 rho_DE — it
boosts a0 by ~200-400x (median) and ERASES the RAR: scatter 0.14 -> 0.36-0.38 dex, 2.6x the 0.13-dex
floor. **Both-ways control (the #1 rule):** the break is robust across Ups in {0.5,0.6,0.7}, interp in
{dS-Unruh, simple/McGaugh}, a0 in {9.36e-11, 1.2e-10}, and scale-height h in {0.3,0.5,1.0 kpc} — every
footing gives floor ~0.14-0.15 dex and density-a0 ~0.36-0.38 dex. It is NOT a convention artifact. And
no fixed smoothing length L threads both: the cluster core needs the boost ON at ~300-450 kpc (~few-x),
the galaxy needs it OFF (1.0x) at ~0.3-3 kpc; at L~300 kpc a galaxy is diluted to a ~1.7x boost that
STILL shifts the RAR, and shrinking L restores the 1e5-1e6 disk density and the full break. This is the
canonical graveyard: the density-a0 cluster flattening dies on the galaxy veto.

## The MI non-adiabatic sigma-spread is galaxy-safe (passes by being null).
The genuine MI-distinctive cluster observable (the relational sigma-spread, theta a function of
omega_ex/omega_in; GENUINE_MI_CLUSTER_DISTINCTIVE) departs from MOND only when omega_ex ~ omega_in. A
galaxy disk has omega_ex/omega_in ~ 0.02-0.10 (deeply adiabatic) so theta->const and the RAR is exactly
MOND. It supplies no cluster MASS (it is a member-internal kinematic effect, not a closure) but it does
not break galaxies either. Galaxy-veto: passes by being null on disks.

## One line
The galaxy veto SEPARATES the closures the way it always has: a **Tremaine-Gunn-protected eV collisionless
residual** (topic 2) PASSES — it is phase-space-forbidden from galaxies, contributes <1% of disk mass,
RAR untouched — but it is a separate, unforced, not-from-a0=Lambda component that relocates the problem;
the **density-a0 MI flattening** (topic 3), the one zero-parameter cluster cure, BREAKS the veto, blowing
the RAR from 0.14 to ~0.37 dex robustly across every footing with no smoothing scale that threads both —
exactly where 40 years of MOND cluster fixes died. No closure both fixes clusters AND survives galaxies.

## Sources
- Repo: CLUSTER_DENSITY_A0_SHAPE_RECONCILED_2026-06-14.md (density-a0 flattening + SPARC trap);
  GENUINE_MI_CLUSTER_DISTINCTIVE_2026-06-15.md (MI theta(y)); NO_EXTRA_MASS_STEELMAN/CLUSTER_CLOSING_CALC
  (eta~2 needs a 2nd component, eV-nu the conventional patch); FRAMEWORK_A0_RAR_MLFIT / SPARC_RAR_FOOTING
  (0.108-0.147 dex RAR floor); real_research/data/sparc_data/*_rotmod.dat (Lelli+2016, 175 gal/2807 pts).
- Lit: Tremaine & Gunn 1979 PRL 42 407; Boyarsky+2009 / Di Paolo+2018 (arXiv:1704.06644, m>=0.18-0.59 keV);
  Sanders 2003, 2007 (neutrinos as cluster DM, TG protects galaxies); Angus 2009 MNRAS 394 527 (11 eV
  sterile + MOND, "TG sufficiently low not to affect galaxy dynamics"); DESI 2024 (Sigma m_nu<0.072 eV).
