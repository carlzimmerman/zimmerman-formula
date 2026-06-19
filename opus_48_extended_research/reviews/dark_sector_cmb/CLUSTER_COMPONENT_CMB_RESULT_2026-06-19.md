# Does the cluster-closure's galaxy-safe component ALSO do the CMB? (2026-06-19, topic "cluster_component_cmb")

Code: `cluster_component_cmb.py` (run clean). Two bounds on the SAME particle-mass axis; quarantine held (a0/Z/kappa never asserted derived); both-ways applied to every "works"/"tension".

## The two bounds (real literature)
- **BOUND A — Tremaine-Gunn phase-space floor** (AFD-2010 Eq.14 norm, reproduced from `cluster_closure/tremaine_gunn_matter_route.py`): cluster-FILL floor **m > ~4.3 eV**; galaxy-SAFETY (dSph) floor **m < ~390 eV** (eV reading is phase-space-EXCLUDED from dwarfs => galaxy-safe). The eV cluster-fix lives in the window **[4, 390] eV** (cluster-ON, galaxy-OFF).
- **BOUND B — free-streaming / small-scale-power floor** (Bode-Ostriker-Turok; Bond-Szalay HDM; Viel/Abazajian thermal<->sterile): an eV fermion's late-time FS scale is ~tens-of-Mpc (11 eV -> ~109 Mpc z=0); Lyman-alpha thermal-relic WDM floor **m_WDM > ~3.5-5.7 keV** (conservative ~5 keV) == DW-sterile **~38 keV**, or a **~7 keV resonant** (Shi-Fuller, colder) sterile.

## The crux: GAP, not overlap (no single mass threads all three)
On the SAME mass axis the cluster phase-space-galaxy-safety floor (eV) and the CMB/small-scale-coldness floor (keV) are **separated by ~13x (thermal) to ~98x (DW)** — opposite ends.

| | eV reading (Angus 11 eV) | keV reading (~7 keV resonant / ~38 keV DW) |
|---|---|---|
| cluster TG pack (>4 eV) | YES | YES |
| galaxy-safe via TG phase space (dSph <390 eV) | **YES** (excluded from dwarfs) | **NO** (m>>390 eV; TG no longer excludes it from galaxies) |
| CMB acoustic peaks | OK (Angus 2009 fits 1st-3rd; Omega_nu(11eV)~0.25~Omega_cdm) | YES (cold, clusters like CDM) |
| small-scale P(k) / Lyman-alpha (>~5 keV thermal) | **NO** (FS over-erases P(k); +KATRIN/DESI Sum m_nu<0.072 eV/N_eff kill thermalized eV) | **YES** (clears Lyman-a) |

## Verdict (both ways)
- **`one_component_works = "tension"`** (a single species cannot satisfy phase-space-galaxy-safety AND CMB/Lyman-alpha coldness simultaneously).
- The Omega~0.25 ~ Omega_DM,LCDM coincidence is **NOT a unification**. It is real that *the abundance* lines up — but abundance lining up is not the same species threading both *kinematic* constraints.
- **Both-ways correction (not manufactured):** the eV reading does **NOT** fail the acoustic third peak — Angus 2009 explicitly fits the first three peaks with a single 11-eV sterile (its density ~Omega_cdm, clusters at the large acoustic scales). The eV reading dies on **Lyman-alpha small-scale power + lab bounds**, not on the third peak. Stating "11 eV can't do the third peak" would be the over-strong (wrong-direction) claim.
- **The honest reading:** to do the CMB the framework needs ~LCDM-amount of *cold/warm* (keV) dark matter; at keV the galaxy-safety is no longer phase-space — it must come from abundance/warmth like LCDM's sub-dominant WDM. So the framework REPLACES galaxy-scale DM with MOND but **still needs ~LCDM-amount of (galaxy-coexisting, keV-warm) DM for clusters+CMB** — i.e. nuLCDM-like, the dark sector RELOCATED not eliminated — OR two distinct components (an eV-cluster species + a cold-CMB species). "No dark matter" is forfeited at clusters AND the CMB. This is the framework's biggest uncleared cosmological cost, stated plainly.

Sources: Tremaine-Gunn 1979 PRL 42 407; Angus-Famaey-Diaferio 2010 MNRAS 402 395 (arXiv:0906.3322) Eq.14; Angus 2009 MNRAS 394 527; Bode-Ostriker-Turok 2001 ApJ 556 93; Bond-Szalay 1983; Viel 2005 PRD 71 063534 + Abazajian 2006 (thermal<->sterile); Viel 2013 / Irsic 2017 / 2024 high-res Lyman-a (m_WDM>~3.5-5.7 keV); Abazajian 2014 PRL 112 161303 (resonant 7 keV colder); Planck 2018 (Omega_cdm h^2=0.120); DESI 2024 Sum m_nu<0.072 eV; KATRIN 2025 (259-day sterile search). Repo: CLUSTER_RESIDUAL_CLOSURE_2026-06-19.md, SKORDIS_CMB_CLUSTER_DEEPDIVE_LEDGER_2026-06-15.md.
