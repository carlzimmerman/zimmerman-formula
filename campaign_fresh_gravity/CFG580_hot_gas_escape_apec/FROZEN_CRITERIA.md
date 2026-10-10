# CFG580 FROZEN CRITERIA — can hidden hot gas supply the KiDS early-type shortfall? (APEC emissivities vs eROSITA)

(owner chat 10-09, "yes do the hot gas test"; AtomDB download approved by the owner). Committed alone before any
emissivity is computed.

Requirement (CFG531 README, template row): KiDS K-in needs extra baryons ≈ 0.8 M* (canonical) / 0.55 M* (alt)
inside ≈ 100 kpc. SLUGGS needs ×17–268 its measured gas (CFG528) — already closed by measurement, not re-tested.
Bound (KIDS_HOT_GAS_ESCAPE_NOTE_2026-09-29; Zhang et al. 2025, A&A 693, A197, Table 3): eRASS:4 quiescent stack,
log M* 10.5–11.0 (median 10.8), L(0.5–2 keV, < R500c ≈ 200 kpc) = (1.1 ± 0.4) × 10^40 erg/s; 2σ upper bound
1.9 × 10^40 erg/s. (Values as recorded in the note; read from the arXiv HTML on 09-29.)

Prediction: gas mass f·M*, M* = 10^10.8 M☉ (variants 10^10.7, 10^10.9), f = 0.8 and 0.55.
 Geometry PRIMARY: uniform-density sphere of radius 100 kpc (the minimum-luminosity configuration for a fixed mass
 inside 100 kpc, since L ∝ ∫ρ² dV). VARIANT: β-model (β = 0.5, r_c = 10 kpc) truncated at 100 kpc.
 Emissivity: pyatomdb CIE (APEC, AtomDB v3.1.3, official CfA release), rest-frame 0.5–2 keV band, per n_e n_H;
 abundances = pyatomdb default; Z ∈ {0.1, 0.3, 1.0} Z☉; kT grid 0.08–0.30 keV.
 ρ_gas = 1.4 m_p n_H; n_e from the APEC ionisation balance (≈ 1.2 n_H).
Verdict:
 ESCAPE CLOSED iff L_pred > 1.9 × 10^40 erg/s for EVERY Z ∈ {0.1, 0.3, 1} at EVERY kT in the hydrostatic range
  [0.10, 0.13] keV (CFG note estimate), for BOTH f = 0.8 and f = 0.55, in the PRIMARY geometry.
 ESCAPE OPEN otherwise: report the (Z, kT) region where the required gas would hide.
 Reported: the full kT grid; M* variants; β-model; the gas fraction that would just reach the bound.
Controls: C1 Z → 0 band emissivity within 30% of an analytic thermal bremsstrahlung estimate (Gaunt 1.2) at
 kT = 0.3 keV; C2 the band-integrated APEC emissivity rises with Z at fixed kT (metals add lines).
MUTATE (CFG580_MUTATE=1): gas mass × 0.01 must give ESCAPE OPEN.
Disclosed: radius/selection mismatch (stacks are SDSS centrals split by star formation, KiDS split by colour;
 stacks integrate within R500c); single-temperature CIE gas; κ fitted; cold energy's mass required; not theory closed.
