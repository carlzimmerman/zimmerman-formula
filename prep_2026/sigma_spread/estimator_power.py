#!/usr/bin/env python3
r"""
OPERATIONAL ESTIMATOR + POWER ANALYSIS for the MI relational sigma-spread, against the
2026 PUBLIC data landscape (post-recon).  LANE R, 2026-07-16.  Exit 0.
=========================================================================================
THE ESTIMATOR (pre-registered form; makes the discriminator operational on real data):
  Per cluster, for each member i with INTERNAL dispersion sigma_i (+- e_i):
    1. residual  d_i = ln sigma_i - <ln sigma | L_i, R_e,i>      (removes Faber-Jackson /
       mass-sigma trend: the "matched internal baryons" control)
    2. matched-radius control: restrict to a shell in projected cluster-centric radius
       (the MOND-transition shell R500-R200, where the signal peaks: rederive script (3))
    3. infall-phase proxy p_i from projected phase space (PPS): p_i = zone tag or
       k_r = (|dv|/sigma_cl)*(R_proj/R200)  [Rhee+2017-class], optionally sharpened by
       morphology/SF tags. Proxy purity DILUTES the observed amplitude: D ~ 0.4 (banked MC).
    4. STATISTIC (a): slope b of d_i on p_i within the shell -> MI: b>0 with amplitude
       Delta_obs = D * f (f = intrinsic spread over the y-window); MG: b == 0 EXACTLY.
       STATISTIC (b): excess-variance -- Var(d | high p) - Var(d | low p) -> MG: 0.
  NULL CALIBRATION: shuffle p_i within the shell (kills any real y-dependence, preserves
  all M-sigma scatter, measurement noise, radial trends) -> empirical null of b.

HOW THE CONFOUNDS ENTER THE NULL (each with its control):
  * INTERLOPERS (non-members in the shell): carry NO y-signal -> pure dilution eps_int
    (also fatten tails). Enter Delta_obs as (1-eps_int); caustic membership on >~200-member
    clusters keeps eps_int ~ 0.05-0.2 in the outer shell.
  * SUBSTRUCTURE: an infalling GROUP shares coherent (R,v) AND its members share formation
    history -> can correlate sigma-residual with PPS position -> the one confound that can
    fake b != 0 in MG. Control: Dressler-Shectman flag + remove correlated groups; shuffle
    null does NOT protect against it (it is a real correlation) -> must be cut, not shuffled.
  * M-SIGMA (Faber-Jackson) SCATTER: intrinsic scatter s_FJ of sigma at fixed (L, R_e) is
    ~uncorrelated with orbit phase -> enters as NOISE floor per member (not bias): dwarfs
    s_FJ ~ 0.05-0.10 dex (12-26%). THIS, not measurement error, dominates once e_i < s_FJ.
  * TIDAL HEATING (CDM channel): same-signed b>0 BUT radially anti-correlated (peaks in
    core) + cumulative + strips -> separable via the radial-trend + undisrupted cuts
    (banked S1-S3). It is a CONFOUND ON THE MI INTERPRETATION, not on the MG=0 falsification
    (MG=0 is falsified by ANY robust b>0 only after the substructure cut; a tidal b>0 in
    the OUTER shell of undisrupted members is CDM-expensive but not impossible -> the
    radial profile of b is the final separator).

POWER: two-bin difference test (low-p vs high-p), per-member noise
  s^2 = (e_i/sigma_i)^2 + s_FJ^2 ; detect Delta_obs = D*(1-eps_int)*f at 3 sigma:
  N_per_bin = 2*(3*s/Delta_obs)^2, N_tot = 2*N_per_bin.  (Slope test on uniform p is
  ~equivalent within ~20%; the two-bin form matches the banked feasibility.py.)

BOTH WAYS: we quantify the DESI-era upgrade exactly where it helps (phase tagging) and
refuse to let it fake an upgrade where it cannot (internal sigma of the diffuse carriers).
"""
import numpy as np

# ---------------------------------------------------------------- signal (from rederive_mi_spread.py, exit 0)
F_BAND = {"floor 6% (kernel low, y<=1.5)": 0.06,
          "fiducial 10% (rational)":       0.10,
          "kernel high 13%":               0.13}
DILUTION = 0.40          # banked PPS-proxy purity MC (feasibility.py); both-ways: 0.3/0.6 scanned below
EPS_INT  = 0.10          # interloper fraction in the caustic-cleaned outer shell

# ---------------------------------------------------------------- per-member noise scenarios
# (e_meas fractional on sigma~10-20 km/s carriers; s_FJ intrinsic at fixed L,R_e)
SCEN = [
    # label,                                e_meas_frac, s_FJ
    ("2026 published UDG/dSph (LEWIS/KCWI, 20-40%)", 0.30, 0.15),
    ("deep MUSE/KCWI campaign (~3 km/s on 15)",      0.20, 0.15),
    ("ELT resolved-star (~1.5 km/s on 15)",          0.10, 0.15),
    ("ELT + tight FJ control (s_FJ=0.08)",           0.10, 0.08),
    ("measurement-only idealization (banked)",       0.10, 0.00),
]

def N3sigma(f, e_frac, s_fj, D=DILUTION, eps=EPS_INT, nsig=3.0):
    delta = D*(1.0-eps)*f
    s = np.hypot(e_frac, s_fj)
    npb = 2.0*(nsig*s/delta)**2
    return int(np.ceil(2*npb))

print("="*100)
print(" POWER: N_total (matched outer-shell, infall-tagged, undisrupted diffuse members) for 3 sigma vs MG=0")
print("="*100)
print(f"  Delta_obs = D(1-eps)*f, D={DILUTION}, eps_int={EPS_INT}; noise = quadrature(e_meas, s_FJ)\n")
hdr = f"  {'scenario':48s} | " + " | ".join(f"{k.split()[0]:>9s} f={v:.0%}" for k, v in F_BAND.items())
print(hdr); print("  " + "-"*96)
for lab, e, sfj in SCEN:
    row = " | ".join(f"{N3sigma(f, e, sfj):>15d}" for f in F_BAND.values())
    print(f"  {lab:48s} | {row}")
n_fid_elt = N3sigma(0.10, 0.10, 0.15)
n_fid_ideal = N3sigma(0.10, 0.10, 0.0)
n_best = N3sigma(0.13, 0.10, 0.08)
n13_ideal = N3sigma(0.13, 0.10, 0.0)
n13_ideal0 = N3sigma(0.13, 0.10, 0.0, eps=0.0)
print(f"""
  READ (both ways):
   * The banked 'N~100-180 vs MG at ELT precision' is recovered ONLY in the measurement-only
     idealization at the upper kernel band (f=13%: N~{n13_ideal}; drop eps_int too -> N~{n13_ideal0}).
     The fiducial f=10% idealization is N~{n_fid_ideal}. Adding the honest Faber-Jackson intrinsic-
     scatter floor s_FJ~0.15 raises the fiducial ELT requirement to N~{n_fid_elt}; the best realistic
     corner (f=13%, tight FJ control) is N~{n_best}. So the banked N was OPTIMISTIC by ~x2-5:
     the intrinsic M-sigma scatter, not instrument error, is the binding noise once ELT exists.
   * Proxy dilution fork: D=0.3 -> N x {N3sigma(0.10,0.10,0.15,D=0.3)/max(n_fid_elt,1):.1f}; D=0.6 (DESI-era caustic+PPS tagging on
     >200-member clusters) -> N x {N3sigma(0.10,0.10,0.15,D=0.6)/max(n_fid_elt,1):.2f} relative to fiducial.""")

# ---------------------------------------------------------------- the 2026 sigma-side wall
print("="*100)
print(" THE 2026 WALL: who can MEASURE internal sigma of the carriers?")
print("="*100)
c = 2.998e5
for lab, R in [("DESI blue (R=2000)", 2000.), ("DESI red/NIR (R=5500)", 5500.),
               ("SDSS (R~2000)", 2000.), ("MUSE (R~3000 @ 7000A)", 3000.), ("ELT-HARMONI (R~18000)", 18000.)]:
    sig_i = c/(2.355*R)
    print(f"   {lab:24s}: instrumental sigma floor ~ {sig_i:5.1f} km/s  vs carriers at 8-20 km/s "
          f"{'-> BELOW FLOOR (cannot measure)' if sig_i > 20 else '-> marginal/OK'}")
print("""   => DESI (DR1 public; DR2 NOT public as of 2026-07-16, verified 401) measures member
      REDSHIFTS (v_los to ~10-30 km/s -- excellent for PPS infall tagging) and internal sigma
      ONLY for sigma >~ 60-100 km/s members. Those members are ADIABATIC-DEAD by the same MI
      physics (y <~ 0.3, a_in >~ 0.5 a0): predicted spread ~0.1-0.7% (rederive script (4)).""")

# can the DESI/SDSS-measurable dE population carry the test instead? (quantified kill)
f_dE = 0.007                      # predicted spread for the dE class (rederive (4), fiducial)
N_dE = N3sigma(f_dE, 0.06, 0.12)  # 6% sigma errors (SDSS-quality), tight FJ 0.12
print(f"   dE route quantified: f~{f_dE:.1%}, best SDSS-quality errors -> N_3sigma ~ {N_dE:,}")
print(f"   vs ~959 members with sigma in Sohn+2017 A2029-class catalogs -> shortfall x{N_dE/959:,.0f}.")
print("   => The ensemble-sigma route through bright members is DEAD; no firewall bypass exists.")

# ---------------------------------------------------------------- available vs needed (the gap)
print("="*100)
print(" 2026 AVAILABLE vs NEEDED (the honest gap)")
print("="*100)
avail_udg_sigma = 38          # Gannon+2024 living catalog rows (touched: data/gannon2024_udg_living.csv)
avail_cluster_udg = 24        # of those in cluster/group environments w/ usable stellar or GC sigma (census_verify.py)
print(f"""   Carriers with ANY internal sigma today: {avail_udg_sigma} UDGs total (Gannon+2024 living catalog,
   downloaded + counted in census_verify.py), of which ~{avail_cluster_udg} are in cluster/group environments;
   per-object errors 16-45%. LEWIS Hydra-I adds ~6-12 'constrained' as papers land.
     NEEDED (3 sigma vs MG=0): ~{N3sigma(0.13,0.10,0.08)}-{N3sigma(0.10,0.10,0.15)} infall-tagged, outer-shell, undisrupted carriers
       with <~10% sigma errors  ->  GAP: x15-60 in N *at a precision tier that does not exist yet*.
     With TODAY'S 20-40% errors the same test needs N~{N3sigma(0.10,0.30,0.15)} -> gap x{N3sigma(0.10,0.30,0.15)//avail_cluster_udg}.
   VERDICT: STILL UNDERPOWERED in 2026 -- and the DESI DR1/DR2 wave does not change the binding
   constraint (it upgrades the free side: membership + phase tagging for thousands of clusters).
   Any firing on today's ~24 objects is EXPLORATORY/FIREWALLED (cannot support or kill).""")

# consistency assertions (exit-0 contract)
assert 100 <= n13_ideal0 <= 180, f"banked 100-180 corner not recovered: {n13_ideal0}"
assert N3sigma(0.10, 0.10, 0.15) > 400, "honest FJ floor must dominate ELT stats"
assert N_dE > 100_000, "dE route must be quantifiably dead"
print("\n EXIT 0 = estimator specified; power grid + gap quantified; banked 100-180 recovered as the")
print(" upper-band/no-interloper idealized corner (N~%d); honest requirement N~270-900." % n13_ideal0)
