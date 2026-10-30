# GH9_cigale_chen_mass_offset: FROZEN CRITERIA (committed alone, before any Wisconsin mass value is read)

**Question.** GH8's class, BELOW ROUTE E'S NEED (A(1.8) 0.26 ± 0.19), is limited by the stellar-mass scale: its lenses have DESI CIGALE masses, while the
gas normalisation M_hot = 1.84 M★ is Zhang+24's, on SDSS DR7 masses from Chen+12. **How far is CIGALE from that scale, and does GH8's class survive the correction?**

## Data

- **New, owner OK:** `wisconsin_pca_bc03-26.fits.gz` from SDSS (data.sdss.org/sas/dr12/sdss/spectro/redux/galaxy/v1_1/, 142,540,520 B), the Chen+12 PCA method with BC03. The whole file is
  fetched because it cannot be cut on the server. Nothing else is fetched.
- **On disk:** GH7 lenses, GH8 velocities and apertures, DESI CIGALE and BGS, GAMA GKV G09.
- **Proxy caveat, fixed in advance:** this table uses Chen's method, but it may not be the exact table Zhang used. The result is an offset to that method, not a proven offset to Zhang's numbers.

## Match

- Wisconsin rows with finite MSTELLAR_MEDIAN and WARNING == 0, positive errors; if a row is duplicated, the first after sorting by SPECOBJID.
- Matched to DESI BGS + CIGALE (GH7's quality cuts, same catalogue) within 1.5″ and |Δz| < 0.001.
- **Primary overlap:** 0.1 ≤ z ≤ 0.19 and GH7's mass range after correction (log M★,CIGALE 10.6–11.0), no central cut.
- Both masses are WMAP7-footed as supplied, so no h term enters Δ. **IMF:** the data model says Kroupa for Wisconsin and the CIGALE log says Chabrier. The PRIMARY Δ is raw.

## Offset

Δ = log M★,CIGALE − log M★,Wisconsin. Measured **at fixed CIGALE mass**, because CIGALE is what assigned GH8's model: Δ_j = median Δ in each of GH7's four lm cells (10.6–11.0, width 0.1).
Errors: 200 bootstrap resamples. Also reported: scatter (MAD), passive vs star-forming (log sSFR −11), north vs south, and the fraction of pairs in the overlap vs the DESI parent at the same mass.

**Redshift trend.**
- Slope dΔ/dz within 0.05–0.19 at the same CIGALE mass.
- **Bridge (on disk):** log M★,CIGALE − log M★,GKV vs z in G09 over 0.1–0.5, since GKV is one mass system across z. Reported as the shape of the trend, not as an offset to Zhang.

## Propagation

Rebuild GH7's model per (z, lm) cell at log M★ − Δ_j, with R_vir and M_hot both following the new mass, by the identical code, for k = 1, 1.8, 3. Re-run GH8's ALL stack with the same seed, lenses, velocities, R and weights.
No map, velocity or selection changes. **Lens selection is not redone:** the lenses stay the ones GH8 graded.

## Verdict (frozen, GH8's rule, A(1.8) + 2 max(σ_shuffle, σ_jack) < 1, at all three R)

Graded at three offsets:
- **D1** PRIMARY: Δ_j.
- **D2** IMF: Δ_j + the published-style constant log(M_Kroupa/M_Chabrier) = 0.04 dex, sign fixed so that both are on one IMF: Δ becomes Δ_j + 0.04, because Kroupa masses run higher than Chabrier.
- **D3** z-extended: Δ_j + the bridge's change in the CIGALE−GKV median between the overlap's and the lenses' median z (or the in-overlap slope if the bridge fails K5).

Classes:
- **SURVIVES MASS SCALE:** BELOW at D1, D2, D3.
- **REMOVED BY MASS SCALE:** BELOW fails at D1.
- **PARTLY LIMITED:** BELOW holds at D1 but fails at D2 or D3.

Reported: the break-even Δ, and A(1), A(3) at D1. The normalisation lock from GH8 stands: if A(1) is also below 1 by more than 2σ, the wording is "below Zhang-normalised gas at every extent".

**Interpretation lock.** Survival addresses only the mass scale. GH8's marginal control, inherited β, K2 failure and non-blind status all remain. REMOVED means GH8's result becomes INCONCLUSIVE, not that gas was found. Neither class says the law wins or that gas is excluded.

## Checks

- **K1:** matched pairs: median |Δz| < 2e-4 and the median separation < 0.5″.
- **K2:** Δ = 0 through the rebuilt model reproduces GH8's A(1.8) within 1e-3 (the model rebuild itself reproduces `gh7_cap.npz` within 1e-6 relative).
- **K3:** injecting +0.2 dex into Wisconsin masses shifts every Δ_j by −0.2 within 1e-6.
- **K4:** at least 2000 pairs per lm cell, else the cell uses the all-cell median and this is reported.
- **K5:** the bridge has at least 500 pairs in every 0.1 wide z bin to 0.4.
- **MUTATE:** Wisconsin masses shuffled among pairs: the MAD widens by at least 1.5× (the pairing carries signal), and v → −v flips T̂ exactly.

**Scope.** κ = ½ FITTED; c_f EXTERNAL; cold dark energy is a gravitating field component, never a particle; not theory closed; nothing here says the data favour the framework. One thread, nice 15, RSS < 6 GB (X48 zooms are running; stop if machine memory runs short).
