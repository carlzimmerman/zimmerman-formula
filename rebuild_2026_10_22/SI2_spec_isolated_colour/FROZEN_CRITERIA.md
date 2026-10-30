# SI2_spec_isolated_colour: FROZEN CRITERIA (committed alone, before any script or number from this split)

**Question.** BL1 found, on KiDS's photometric isolation, that blue lenses need no halo-mass shift in amplitude and red lenses need +0.32 dex, and that S2's red stellar-mass ladder removes most of the red gap for both models. SI1 found route E short at 120–750 kpc on spectroscopically isolated S1, law ahead by Δχ² +8.7, and that lead shrinks with M★. So split the spectroscopic samples by colour and apply the same ladder to both models. Does the record's lensing tension survive on clean lenses, when both theories get the same baryons?

**Data.** SI1's stack (P2's script, its measurement rebuilt in scratch). Lens colour u − r from KiDS-bright LePhare `MAG_ABS_u − MAG_ABS_r`, matched exactly as P2 matches masses. Red is u − r > 2.0, S2's central split. Lenses keep P2's selection unchanged. The hole term stays the sample's full iso-random stack (I3 or I1), because its veto does not depend on the lens's colour. This is a stated approximation; its size is the raw L − R variant, reported.

**Stellar-mass ladder, the same for both models.** R0: catalogue M★. R2: red lenses and red neighbours +0.295 dex (S2's +0.123 from CFG667 and +0.172 from CFG926's IMF relation), blue unchanged. Galaxies with no LePhare match (proxy mass) are unshifted. As in S2, cold and hot gas stay tied to the catalogue M★. Route E's M200 moves with M★ through EM1's relation; the law's baryons move with M★.

**Models.** L(a) and H exactly as SI1 (commit ed3c0f8bb1): FC1's rule, EM1's relation, halo to r_ta, neighbours by the same model.

## Frozen outputs (each footing and each of S3, S1 separately; never pooled)
SI1's statistic: Δχ² = χ²(H) − χ²(L(a)), D, the classes NOT POWERED / LAW PREFERRED / ROUTE E PREFERRED / NEITHER, plus χ² and p for each model.

1. **Blue lenses, R0.** The population SPARC samples, with no mass correction.
2. **Red lenses, R0 and R2.**
3. **All lenses, R2.**

**Combined reading (frozen).** It uses line 3 on both samples, canonical.
- **LENSING TENSION GONE ON CLEAN LENSES:** on S1 and S3, neither is LAW PREFERRED, and H has p ≥ 0.05 on both.
- **TENSION REMAINS:** LAW PREFERRED on S1 or S3 with H's p < 0.05 there.
- **MIXED:** anything else.

## Reported
- A_in, A_O1, A_O2 by colour for H and L.
- Raw L − R variant.
- u − r 2.5 split counts only.

## Checks (any failure makes the combined reading NOT DECIDED)
- **K1:** colour reconstruction: LePhare match count equals P2's `valid`, and the red fraction printed for S1 and S3.
- **K2:** at R0 with no split, the run reproduces SI1's committed χ²(H), χ²(L) on S3 and S1, both footings, |d| ≤ 1e-9.
- **K3:** blue and red weighted parts sum to the full model stack at R0 within 1e-9, per bin (S3).
- **MUTATE:** swap the red and blue labels. Line 2's χ²(H) at R2 must change.

## What this cannot show
- The red stellar-mass scale is an open choice (CFG667 §3). R2 is taken from the record, not derived here, and a pass under R2 is conditional on it.
- Colour is a proxy. M★ estimator differences between SPARC and KiDS are not measured here.
- It does not measure leakage in KiDS's photometric isolation.
- S3 is small: its class may stay NOT POWERED.

κ = ½ FITTED. Footings never pooled. Cold dark energy is a gravitating field component, never a particle. Not theory closed. Nothing here says the data favour the framework.
