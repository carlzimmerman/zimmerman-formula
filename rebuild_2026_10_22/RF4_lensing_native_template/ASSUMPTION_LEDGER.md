# RF4_lensing_native_template: ASSUMPTION LEDGER (committed with the criteria)

| input | value or source | class | role |
|---|---|---|---|
| KiDS-1000 shapes, Z_B | source cache (session scratch), DR4.1 gold | RAW + SURVEY-CALIBRATION (no m correction, no n(z), as in SI3) | ΔΣ, a |
| KiDS-bright lenses, photo-z | `lr_lenses.npz`, `KiDS_DR4_brightsample.fits` | RAW, photo-z calibrated on GAMA | lenses, tracers |
| Lens M★ (R0) | catalogue, LePhare/record | LITERATURE-INPUT (assumed IMF, SPS) | baryons, EM1 masses |
| R2 +0.295 dex on red | SI2's choice | LITERATURE-INPUT, an open choice | band edge |
| Cold gas relation | X78/F2 −0.69 lg M★ + 6.63 | LITERATURE-INPUT | baryons |
| Zhang+24 hot gas, 1.84 M★, β 0.43 | X78/GH2, profile to k R_vir | RAW X-ray, past R_vir extrapolated | baryons; k grid |
| B21 stacks + covariance | `brouwer2021_rar` | RAW + survey calibration, B21 cosmology rescaled by F2's factors | G1 |
| GAMA G3C v10, GKV M★ | `cfg519_work`, `gama_dr4_gkv` | RAW redshifts; FoF linking tuned on ΛCDM mocks: ΛCDM-PROCESSED, labelled | G3 hosts, σ_off, satellite fraction row |
| GH1 stacks | `gh1_esd.npz` | RAW | G3 |
| Native background | Ω_m 0.2976, h 0.6856 (`NAT_*`, X73/F2) | FRAMEWORK-NATIVE | R, r_ta, ρ̄_m |
| a₀, κ = ½ | both footings | FRAMEWORK-NATIVE, κ fitted | law, E's floor |
| c_f = 4 | external | LITERATURE-INPUT, EXTERNAL | arm E only |
| η(M_t), ρ₁₀, ρ₁₁, f_c | CE1, X80, RG1 table | FRAMEWORK-NATIVE, zoom ε cut (X81); core shape by hand (X70) | arm N |
| ZN1 shapes | `zn1_shapes.json`, 9 seeds per tag | FRAMEWORK-NATIVE; zoom ICs ledgered there | arm Z |
| EM1's M200 relation | fit with NFW, Bullock c(M) | LITERATURE-INPUT, flagged by SI3's limits | arms N, Z |
| Two-halo T shape | tracer counts around these lenses | RAW | G1, G2 |
| Linear, scale-independent tracer bias | assumption, tested by TS3 only at two tracer cuts | ASSUMPTION | T's use inside 3 Mpc |
| a | shear at 3–15 Mpc, this sample | RAW | T's amplitude |
| Growth factor, σ₈, P(k) | none | not used | RF5 not needed for this template |
| CFG805 T1x template | K1 only; X53 ledger: ΛCDM-inherited ICs | ΛCDM-PROCESSED, labelled | K1 identity; never graded |
| f_sat 0.28 (+0.21, −0.16) | Hadzhiyska+ 2026 HOD table, read in GH11; other sample | LITERATURE-INPUT; its HOD fit runs on an N-body suite, so ΛCDM-PROCESSED, labelled, as a bracket | miscentring |
| σ_off | G3C members, this lane | RAW + FoF (above) | miscentring |
| Gaussian offset form | assumption | ASSUMPTION | miscentring |
| GH10/GH11 kSZ points + covariance | DR2 data release; assumed σ_true 300 km/s, r_fid 0.64 from mocks | RAW + ΛCDM-PROCESSED (r from mocks), labelled | G4 |
| GH9 mass offset | GH9 | RAW comparison | G4 |
| DESI DR1 BGS neighbours | `gh6_bgs.npz` | RAW | kSZ template |
| Fiducial background in GH10's model (0.3085, 0.679) | inherited in `gh10.py`, sets D_A only | ΛCDM-PROCESSED, labelled; effect on D_A below 2 % at z < 0.4, K6 needs it to reproduce the record | G4 |
| Isolation veto, footprint rule | CFG96, F2, CFG903 | STANDARD analysis choice | samples, clones |
| Lensing projection, Newtonian ΔΣ for E, N, Z; AQ for the law | `AQ.delta_sigma`, `nu_simple` | STANDARD-MOND-MACHINERY | all |
