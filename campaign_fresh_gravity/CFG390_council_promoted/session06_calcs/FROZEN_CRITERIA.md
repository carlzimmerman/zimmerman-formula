# Session 6 calcs, FROZEN before any script exists

κ = ½ fitted; both footings. No DM particle; the cold mass is still required. On-disk data only.

## P. Satellite-plane members vs non-members
If the Milky Way's plane of satellites (VPOS) formed from tidal debris, its members are tidal dwarfs. Under the settling model, tidal dwarfs have a target but no catchment, so they should be Newtonian (CFG7 leans that way for young TDGs). Then plane members should sit far BELOW non-members in σ relative to the law.
- Objects: LVD MW resolved systems (31 UFDs, AUDIT_UFD cut; plus the 12 classicals of Session 4, LMC/SMC excluded) with full phase space. Offset = log(σ_obs/σ_law) with AUDIT_UFD's isolated estimator, Υ_V = 2.
- Orbital pole: L = r × v (astropy Galactocentric defaults), 300 MC draws over the quoted distance/pm/vlos errors (seed 41). VPOS normal (l, b) = (169.3°, −2.8°) (Pawlowski, Pflamm-Altenburg & Kroupa 2012, as recalled; declared). Galactocentric direction (cos b cos l, cos b sin l, sin b).
- Member: ≥ 50% of draws with the pole within 30° of ±normal (in-plane orbit, either sense). Co-orbiting-only membership reported.
- Δ = median offset(members) − median offset(non-members), computed within each population (UFDs; classicals) and pooled after subtracting each population's own median. Bootstrap over objects (2000, seed 43).
- **TDG-ORIGIN SUPPORTED** if pooled Δ < −0.2 dex at > 3σ. **DISFAVOURED** if Δ − 2σ_Δ > −0.2 (members are not Newtonian-poor by the needed amount). **NON-DISCRIMINATING** otherwise. The full law boost is ≈ +0.3 to +1 dex for these systems, so −0.2 is a conservative threshold.
- MUTATE: replace member offsets by the Newtonian expectation (offset − log ν^½). Must return SUPPORTED; exit 1 when it does.

## F. Fossil a₀ by Hubble type in SPARC
a₀ tracks ρ_DE (DESI-like: about +6% at z ≈ 0.5 and about −13% at z ≈ 2). If the settling rate is slow, a disc keeps the target of its settling epoch. Early types settled earlier, so their deep-regime residuals sit lower: early − late ≈ ½ log(0.87/1.06) ≈ −0.04 dex. With fast settling the difference is 0.
- Data: CFG4_common.load_sparc(), Q ≤ 2. Points with log g_bar < −10.5 **and** gas-dominated (V_gas² ≥ 0.7 V_bar² at Υ_disk 0.5, Υ_bul 0.7), so Υ barely matters. Residual vs ν_mono, both footings. Per-galaxy weighted mean residual (galaxies with ≥ 3 such points).
- Early: T ≤ 5; late: T ≥ 8 (declared; T 6–7 excluded). Δ = median(early) − median(late), bootstrap over galaxies (2000, seed 47).
- **NON-DISCRIMINATING** if σ_Δ > 0.02 (−0.04 cannot be seen at 2σ). Otherwise **SLOW-SETTLING HINT** if Δ < −0.02 at > 2σ, **FAST/NO FOSSIL** if Δ > −0.02 at > 2σ, else inconclusive.
- MUTATE: add −0.04 dex to every early-type residual; Δ must drop by 0.04 ± 0.005; exit 1 when it does.
