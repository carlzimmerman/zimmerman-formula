# CFG90 FROZEN (written 2026-09-29 ~10:55 UTC, before any script existed or ran)

## Question
Can an independent implementation, built only from the README statements of CFG52 and CFG54 and the data tables on disk,
reproduce: (Q1) 242 galaxies with g_bar < a0; (Q2) 16 of them with a flat-vs-a0*E(z) prediction gap above 1 sigma and none
above 2 sigma; (Q3) no clean z >= 1.5 object with g_bar < 0.3 a0 (canonical), one further RC100 object (zC 410041) on the
alt footing; (Q4) pooled z >= 1.5, g_bar < a0 (N = 14): flat +0.135 dex, rival -0.037 dex; (Q5) PHIBSS N = 0 of 51 at the
frozen velocity radius 1.31 r_h. Plus sensitivity: usable-disc count vs g_bar threshold (0.3, 0.5, 1 a0), velocity radius
(1.31 r_h = 2.2 R_d, r_flat, r_peak; native per-survey convention as baseline), a0 footing (9.3603e-11 / 1.1312e-10), and
the number of z >= 1.5 discs with g_bar < a0 that exist at all.

## Files read before freezing (nothing else): CFG52 README, CFG54 README, CFG63 README+FROZEN_QUESTION, data tables
real_research/data/{rc100_nestorshachar2023_table3, msa3d_2026_rotation_curves(+provenance), kmos3d_ubler2017, kross_harrison2017}.csv,
data_assembly/kmos3d_phibss/{phibss13_joined, kmos3d_catalog}.csv (+ its README and TACCONI2013 note, which record data
provenance and choose no radius), prep_2026/jeanneau_refit/{jeanneau26_catalog_cds.csv, DATA.md} (the MUSE-DARK II table),
prep_2026/a0z_crossscale/highz_target_ledger_verified_2026.out (the 23-object lensed/CO ledger, first 3000 bytes).
NOT opened: any CFG52/CFG54 .py, .out, _results.json, feas_per_galaxy.csv. Comparison happens only after my runs.

## Selection rules and modelling choices (as read; every choice not in a README is MINE and declared here)
- Constants: G=6.6743e-11, Msun=1.98841e30 kg, kpc=3.085678e19 m. Flat LCDM Om=0.3138 (README), h=0.6736 (mine: chosen because
  a0 = (1/2) c H0 sqrt(3 OL/8pi) then equals 9.36e-11; control C1 checks this). E(z)=sqrt(Om(1+z)^3+OL). a0 footings 9.3603e-11
  (canonical) and 1.1312e-10 (alt) as numbers given in the campaign READMEs. Angular scale via the same flat cosmology.
- Kernel (mine; README says only "the same nu_mono"): g_obs = g_bar nu(y), y=g_bar/a0, nu(y)=1/(1-exp(-sqrt y)) (Milgrom 1999
  eq. 9 / McGaugh RAR form). Alternative kernel nu=(1+sqrt(1+4/y))/2 reported as a sensitivity, not as the headline.
- Rival: same kernel with a0 -> a0 E(z). Gap_i = |log g_flat - log g_rival|.
- Baryons: exact Freeman exponential disc, R_d = R_e/1.68, of M_bar; g_bar = v_disc^2/R at the velocity radius R_v; v^2 = (2GM/R_d)
  y^2 [I0K0 - I1K1], y=R/2R_d. Point mass GM/R^2 reported as the upper-bound variant.
- Mass: RC100 logMbar; KMOS3D (Ubler) logMbar; MUSE-DARK II logMBar; MSA-3D stars + molecular gas with the Tacconi+2018 (eq. 6)
  main-sequence scaling log(Mmol/M*) = 0.06 - 3.3 (log(1+z)-0.65)^2 - 0.41 (logM* - 10.7) [Delta_MS = 0, no HI] (mine; the README
  says only "with gas"); KROSS stars-only (README flags only MSA as "with gas"; KROSS g_bar is then an upper bound on baryon
  deficiency, i.e. counts are upper limits) with a variant that adds the same Tacconi scaling.
- Native velocity radius (mine, from each table's own convention): RC100 R_e; MSA-3D R_e,disk; KMOS3D and KROSS 2.2 R_d =
  1.31 R_e; MUSE-DARK II 2.0 R_e (logV2.0); PHIBSS 1.31 r_h (CFG54 README, frozen). KMOS3D rows carry no radius: R_e from the
  KMOS3D catalogue RHALF (arcsec) matched on (z within 0.002, logM* within 0.02); rows failing the match (d>1 unit) are
  dropped and counted. Duplicates within the KMOS3D csv are kept as the README counts 135 rows.
- sigma_V/V: 10% unless a table carries one (MSA-3D eVrot; MUSE posterior std of logV). Mass floor 0.20 dex in g_bar (README).
  Per-object sigma_i (log g_obs) = sqrt( (2 sigV/V/ln10)^2 + (s_i*0.2)^2 ), s_i = dlog g_obs/dlog g_bar of the flat law at
  the object. "Above k sigma" means Gap_i/sigma_i > k. (README says typical sigma 0.13-0.16: consistency check C6.)
- Pooled z>=1.5 & g_bar<a0: Delta_law = mean(log g_obs,meas - log g_law). sigma_pool = sqrt( (1/N^2) sum sigV_i^2(log) + (mean s_i * 0.2)^2 )
  (correlated 0.2 dex mass calibration; README: +1.0 sigma and -0.3 sigma). g_obs,meas = V^2/R_v.
- "Clean" object (Q3): passes internal consistency: where the table carries f_DM (RC100, MSA-3D), the baryonic g implied by
  (1 - f_DM) g_obs agrees with the disc g_bar within 0.5 dex. Raw count (no cleaning) is also reported.
- PHIBSS (CFG54 rules as read): rows with vrot, radius, z_co; exclude co_upper_limit==1 (6) and fgas_inconsistent_in_source==1 (3);
  r_h = rh_opt_kpc, falling back to rh_co_kpc if opt is missing (mine); M_bar = M* + Mmol; R_d = r_h/1.68; R_v = 1.31 r_h.
  Variant: rh_opt only. Post-hoc radius sweep 1.31/2/3/4 r_h reported for comparison with the README's sensitivity line.
- 242: sum of the five survey counts with g_bar<a0 at native radii (RC100+MSA+KMOS3D+KROSS+MUSE) plus the ledger's point-valued
  "PUB" rows below a0 (the 23-object lensed/CO ledger's only listed g_bar/a0 point values are 1.55, 0.95, 3.64: one qualifies);
  this reading of the ledger is a guess and is reported separately as "5-survey" and "+ledger". No de-duplication in the
  headline (the README's z>=1.5 N=14 = 9+3+2 sums the sets); overlap RC100-KMOS3D counted as a diagnostic.

## Pass lines
P1 counts exactly: 242 (or 241/242 by the ledger reading, stated), 16 above 1 sigma, 0 above 2 sigma; per-set g_bar<a0 and <0.3a0
   counts (26/4, 19/4, 16/5, 106/15, 74/43) and z>=1.5 (9,3,2,0,0). P2 Q3 as stated (canonical: 0 clean; alt: +zC 410041).
P3 pooled offsets within +-0.0005 of +0.135 and -0.037 with N=14. P4 PHIBSS 0 of 51, min g_bar/a0 within 0.01 of 1.10.
Any miss is reported as a difference with a cause; failing to reproduce is a valid outcome and is not tuned away.
Controls (a failed control is a failure of the run, exit 1):
 C1 a0 closed form vs stated a0 (0.5%) and alt = can/sqrt(OL) (0.3%); C2 E(z) closed form values (z=0:1; z=1: sqrt(8*0.3138+0.6862)... recomputed
 independently by (1+z)^3 expansion and numerical H(z) integration of the Friedmann eq.); C3 Freeman disc vs direct numerical ring-sum
 potential (rel <1e-3 at R/R_d = 0.5..6), and large-R limit -> GM/R^2, and peak at 2.15 R_d; C4 kernel round trip g_bar->g_obs->g_bar (1e-9) and
 deep/Newtonian limits; C5 disc g_bar vs (1-f_DM) g_obs on RC100 (README: -0.01 dex; pass: median within +-0.03 dex);
 C6 median sigma_i in 0.10-0.20 dex (README 0.13-0.16); C7 selection mock: flat law true, 0.2 dex g_bar noise, selection on noisy
 g_bar<a0: bias must be 0 within 3 MC-sigma when the noise is 0, and positive when it is 0.2 dex (README: +0.03..+0.11);
 C8 KMOS3D/RHALF match quality (>=95% within 1 unit) and RC100 z/mass reproduce.
MUTATE=1: a0 -> 2 a0 (both footings, kernel and rival). Stated direction: every g_bar<thr count is >= the main count and the
total g_bar<a0 count is strictly larger; and the "counts equal main" comparison must FAIL, giving exit 1. A MUTATE that leaves
the counts unchanged would be a failure of the control.

## Sensitivity grid (all reported, none chosen): threshold {0.3,0.5,1} a0 x radius {native, 1.31 r_h, r_peak(Freeman 2.15 R_d),
r_peak,tot (max of flat-law total curve if interior else r_flat), r_flat (first R with |dlnV/dlnR|<0.05 on the flat-law total
curve, search 0.5-20 R_d)} x footing {canonical, alt} x {all z, z>=1.5} x survey. Plus the list of z>=1.5, g_bar<a0 discs.
Exit codes: 0 = all controls pass; 1 = a control fails (main) / the MUTATE direction test passes and equality fails (MUTATE).
Programme rules: no claim that data favour the framework; kappa=1/2 fitted; nothing here says the theory is closed.
