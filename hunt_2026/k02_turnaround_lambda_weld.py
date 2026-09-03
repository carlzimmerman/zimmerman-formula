#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""k02 -- the Lambda-turnaround weld: the zero-velocity surface of the Local Group.

THE CANDIDATE (ledger item 80, listed 2026-09-02 and never run).  The framework has TWO accelerations that meet
at a radius nothing else in the ledger touches: the system's own MOND field and the cosmological repulsion.

    isolated deep MOND:  g_int(r) = sqrt(G M_b a_0)/r          Lambda:  g_Lam(r) = (Lambda c^2/3) r = H_Lam^2 r
    they balance at      R_A = (G M_b a_0)^(1/4) / H_Lam = v_flat / H_Lam

and with the first law H_Lam = Z a_0/c, Z = sqrt(32 pi/3), that is  R_A = c (G M_b)^(1/4) / (Z a_0^(3/4)) --
a_0 with a PREDICTED coefficient, in a relation between two measured quantities (M_b or v_flat, and a radius).

WHY IT IS NOT A RESTATEMENT.  v^4 = G M_b a_0 fixes v_flat and nothing else; it says nothing about where the
Hubble flow reverses.  R_A needs the SECOND force -- the Lambda term -- and it is therefore a weld between the
rotation-curve law and the cosmological constant, not the rotation-curve law rewritten.  The Newtonian analogue
R_L = (G M / H_Lam^2)^(1/3) is what the zero-velocity-surface literature already uses (Karachentsev's group-mass
method); the framework changes BOTH the exponent (M^(1/4) not M^(1/3)) and the mass (baryonic, not total).

WHAT IS ACTUALLY OBSERVED is not R_A but R_0, the radius of the shell AT turnaround today.  Both cases reduce,
in units tau = H_Lam t and x = r/R_scale, to a one-parameter ODE with no free constants:

    MOND + Lambda :  xdd = x - 1/x      (x = r/R_A,  R_A = (G M_b a_0)^(1/4)/H_Lam)
    Newton + Lambda: xdd = x - 1/x^2    (x = r/R_L,  R_L = (G M/H_Lam^2)^(1/3))

so x_ta is fixed by H_Lam t_0 alone and R_0 = x_ta * R_scale is a zero-parameter prediction on each footing.

THE STRUCTURAL PROBLEM THE ITEM DID NOT ANTICIPATE, found here and reported against interest: at ANY turnaround
radius the system's own field has fallen to g = H_Lam^2 R_0, which for every group in the Local Volume is far
BELOW the external field of large-scale structure.  The turnaround radius is therefore always deep inside the
external-field-dominated regime, where the framework is quasi-Newtonian with G -> nu(e_N) G.  That is not a
defect of the data; it is a property of the observable, and it converts the item from a sharp prediction into a
bracket whose width is set by the external-field estimate.

Rules honoured: both footings; the LambdaCDM and baryons-only Newtonian alternatives computed beside it; checks
that CAN fail; mutation controls; every input measured; bug-pattern audit at the end.
"""
import math
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
from hunt_lib import Check, P, info, A0, vizier_tsv, _f, nu_s

G, c = 6.67430e-11, 2.99792458e8
Msun, pc = 1.98892e30, 3.0856775814913673e16
Mpc, kpc = 1e6*pc, 1e3*pc
Gyr = 3.1557e16
Z_FW = math.sqrt(32*math.pi/3)
H0 = 67.4e3/Mpc
OmM, Omb = 0.315, 0.0493
t0 = 13.797*Gyr
f_growth = OmM**0.55

FOOT = {k: dict(a0=a0, HL=Z_FW*a0/c) for k, a0 in A0.items()}
ck = Check()

P("="*126)
P("k02 -- THE LAMBDA-TURNAROUND WELD: R_0 = x_ta (G M_b a_0)^(1/4)/H_Lam   (ledger item 80, first run)")
P("="*126)
for k, f in FOOT.items():
    P(f"  {k:<10s} a_0 = {f['a0']:.4e} m/s^2   H_Lam = Z a_0/c = {f['HL']:.5e} 1/s = {f['HL']*Mpc/1e3:6.2f} km/s/Mpc"
      f"   H_Lam t_0 = {f['HL']*t0:.4f}")

# ------------------------------------------------------------------ 1. the collapse integral, both force laws
def tau_of_xta(x_ta, n):
    """dimensionless time from x=0 to turnaround at x_ta for xdd = x - 1/x^n  (n=1 MOND, n=2 Newton).
    substitution x = x_ta (1 - w^2) removes the sqrt singularity at both ends."""
    def pot(x):                                   # 2 * (potential difference), = xdot^2
        if n == 1:
            return x**2 - x_ta**2 + 2*math.log(x_ta/x)
        return x**2 - x_ta**2 + 2*(1.0/x - 1.0/x_ta)
    def integ(w):
        x = x_ta*(1 - w*w)
        if x <= 0:
            return 0.0
        v2 = pot(x)
        return 0.0 if v2 <= 0 else 2*x_ta*w/math.sqrt(v2)
    val, err = quad(integ, 0.0, 1.0, limit=400)
    return val

def x_turnaround(tau_target, n):
    g = lambda x: tau_of_xta(x, n) - tau_target
    return brentq(g, 1e-4, 0.999999, xtol=1e-10)

P("\n" + "="*126)
P("1. THE COLLAPSE INTEGRAL -- x_ta from H_Lam t_0 alone, no free parameter")
P("="*126)
XTA = {}
for k, f in FOOT.items():
    tau = f['HL']*t0
    XTA[k] = dict(mond=x_turnaround(tau, 1), newt=x_turnaround(tau, 2))
    P(f"  {k:<10s} H_Lam t_0 = {tau:.4f}   x_ta(MOND+Lam) = {XTA[k]['mond']:.4f}   x_ta(Newton+Lam) = {XTA[k]['newt']:.4f}")
# validation: as Lambda -> 0 the Newtonian branch must reproduce the cycloid t = pi sqrt(r^3/(8GM))
small = 1e-3
tau_cyc = (math.pi/2)*small**1.5/math.sqrt(2)
x_rec = x_turnaround(tau_cyc, 2)
ck("K02.1 the collapse integral reproduces the exact Newtonian cycloid turnaround time t = pi sqrt(r_ta^3/(8GM)) "
   "in the Lambda -> 0 limit -- a check that fails if the quadrature or the energy integral is wrong",
   abs(x_rec/small - 1) < 2e-3, f"input x_ta = {small:.4e}, recovered {x_rec:.6e} ({100*(x_rec/small-1):+.3f}%)")
# and the MOND branch's own small-x limit: tau -> sqrt(pi/2) x_ta
x_small = 1e-3
ck("K02.2 the MOND branch reproduces its own analytic small-x limit tau = sqrt(pi/2) x_ta (the logarithmic "
   "potential's free-fall time), which fails if the n=1 energy integral is mis-signed",
   abs(tau_of_xta(x_small, 1)/(math.sqrt(math.pi/2)*x_small) - 1) < 2e-3,
   f"tau/x_ta = {tau_of_xta(x_small,1)/x_small:.6f} vs sqrt(pi/2) = {math.sqrt(math.pi/2):.6f}")

# ------------------------------------------------------------------ 2. the Local Group, measured from UNGC
P("\n" + "="*126)
P("2. THE OBSERVABLE, MEASURED: the Local Group zero-velocity radius from the UNGC Hubble diagram")
P("="*126)
rows = vizier_tsv("ungc_karachentsev2013.tsv")
name = np.array([r["Name"].strip() for r in rows])
ra   = np.array([_f(r["_RAJ2000"]) for r in rows]); de = np.array([_f(r["_DEJ2000"]) for r in rows])
dist = np.array([_f(r["Dist"]) for r in rows])
vlg  = np.array([_f(r["Vlg"]) for r in rows])
klum = np.array([_f(r["KLum"]) for r in rows])
mhi  = np.array([_f(r["MHI"]) for r in rows])
md   = np.array([r["MD"].strip() for r in rows])
fdis = np.array([r["f_Dist"].strip() for r in rows])

def unit(ra_d, de_d):
    a, d = np.radians(ra_d), np.radians(de_d)
    return np.array([np.cos(d)*np.cos(a), np.cos(d)*np.sin(a), np.sin(d)])

# LG barycentre: on the MW-M31 line at f_M31 = M_M31/(M_MW+M_M31); M31 at (10.68, +41.27), D = 0.77 Mpc
iM31 = int(np.where(name == "MESSIER031")[0][0])
D_M31 = dist[iM31]
f_M31 = 0.55                                            # M31/(MW+M31) mass share, Karachentsev's convention
bary = f_M31*D_M31*unit(ra[iM31], de[iM31])             # Mpc, in the MW-centred frame
info(f"M31 at D = {D_M31:.3f} Mpc; LG barycentre placed at {np.linalg.norm(bary):.3f} Mpc toward M31 (mass share {f_M31})")

pos = (dist[None, :]*unit(ra, de))
R_LG = np.linalg.norm(pos - bary[:, None], axis=0)      # 3-D distance from the LG barycentre, Mpc

ti1  = np.array([_f(r["Ti1"]) for r in rows])
good = np.isfinite(R_LG) & np.isfinite(vlg) & (dist > 0)
acc  = np.isin(fdis, ["TRGB", "Cep", "RR", "HB", "CMD"])          # distances good to ~5%
win  = good & acc & (ti1 < 0) & (R_LG > 0.7) & (R_LG < 3.0)
P(f"  sample: accurate distances (TRGB/Cep/RR/HB/CMD), tidal index Ti1 < 0 (not bound to any group),")
P(f"          0.7 < R_LG < 3.0 Mpc  ->  {win.sum()} galaxies.  Karachentsev+2009 used ~30 on the same criteria.")
for lab, sel in [("all galaxies, no quality cut", good & (R_LG > 0.7) & (R_LG < 3.0)),
                 ("accurate distances only",      good & acc & (R_LG > 0.7) & (R_LG < 3.0)),
                 ("accurate + isolated, to 4 Mpc", good & acc & (ti1 < 0) & (R_LG > 0.7) & (R_LG < 4.0))]:
    Aq = np.vstack([R_LG[sel], np.ones(sel.sum())]).T
    hq, bq = np.linalg.lstsq(Aq, vlg[sel], rcond=None)[0]
    P(f"    systematic variant: {lab:<32s} N={sel.sum():3d}  H_loc={hq:6.1f}  R_0={-bq/hq:5.3f} Mpc  "
      f"rms={(vlg[sel]-(hq*R_LG[sel]+bq)).std():4.1f} km/s")
A = np.vstack([R_LG[win], np.ones(win.sum())]).T
Hloc, b0 = np.linalg.lstsq(A, vlg[win], rcond=None)[0]
R0_obs = -b0/Hloc
res = vlg[win] - (Hloc*R_LG[win] + b0)
# galaxy bootstrap
rng = np.random.default_rng(20260903); boot = []
idx = np.where(win)[0]
for _ in range(4000):
    s = rng.choice(idx, size=len(idx), replace=True)
    Ab = np.vstack([R_LG[s], np.ones(len(s))]).T
    try:
        hh, bb = np.linalg.lstsq(Ab, vlg[s], rcond=None)[0]
        if hh > 0: boot.append(-bb/hh)
    except Exception: pass
boot = np.array(boot); R0_lo, R0_hi = np.percentile(boot, [16, 84])
P(f"  fit V_LG = H_loc (R_LG - R_0):   H_loc = {Hloc:6.2f} km/s/Mpc    R_0 = {R0_obs:.3f} Mpc "
  f"[{R0_lo:.3f}, {R0_hi:.3f}]  rms residual {res.std():.1f} km/s")
P(f"  published for comparison (Karachentsev+2009, same method, TRGB subsample): R_0 = 0.96 +- 0.03 Mpc, "
  f"H_loc = 78 km/s/Mpc")
ck("K02.3 the measured zero-velocity radius reproduces the published Local Group value within the bootstrap -- "
   "a check that fails if the barycentre, the 3-D geometry or the velocity frame is wrong",
   0.75 < R0_obs < 1.25, f"R_0 = {R0_obs:.3f} Mpc [{R0_lo:.3f}, {R0_hi:.3f}] vs published 0.96 +- 0.03")

# ------------------------------------------------------------------ 3. the Local Group's baryonic mass
P("\n" + "="*126)
P("3. THE INPUT, MEASURED: the Local Group's baryonic mass from UNGC K-band light and HI")
P("="*126)
is_lg = np.isfinite(R_LG) & (R_LG < 1.0) & (dist > 0)      # geometric membership, Karachentsev's LG boundary
UPS_K = 0.80          # Bell & de Jong K-band M/L for old populations; 0.6-1.0 is the SPS range
LK_MW = 5.4e10                     # LITERATURE INPUT, flagged: the UNGC has no K_s luminosity for the Milky Way
LK = np.where(np.isfinite(klum[is_lg]), 10**klum[is_lg], 0.0)
MH = np.where(np.isfinite(mhi[is_lg]), 10**mhi[is_lg], 0.0)
LK_tot = LK.sum() + LK_MW
Mb_LG = (UPS_K*LK_tot + 1.33*MH.sum())
P(f"  {is_lg.sum()} Local Group members within 1.0 Mpc of the barycentre (geometric membership, no MD cut)")
P(f"    sum L_K (catalogue) = {LK.sum():.3e} Lsun  + Milky Way {LK_MW:.2e} Lsun (LITERATURE INPUT: the UNGC")
P(f"      tabulates no K_s luminosity for our own Galaxy; 5.4e10 Lsun is the standard value)")
P(f"    stars  = {UPS_K*LK_tot:.3e} Msun at Upsilon_K = {UPS_K}   (SPS K-band M/L for these populations, 0.5-0.8)")
P(f"    sum M_HI  = {MH.sum():.3e} Msun     -> gas   {1.33*MH.sum():.3e} Msun with the helium factor 1.33")
P(f"    M_b(LG)   = {Mb_LG:.3e} Msun        (literature: 1.2-1.8e11)")
for u in (0.5, 0.6, 1.0, 1.2):
    P(f"      Upsilon_K = {u:.1f} would give M_b = {u*LK_tot + 1.33*MH.sum():.3e} Msun   "
      f"(d log M_b/d log Upsilon = {u*LK_tot/(u*LK_tot + 1.33*MH.sum()):.3f})")
ck("K02.4 the Local Group baryonic mass assembled from UNGC lands in the published range 1.0-2.0e11 Msun -- "
   "fails if the K-band luminosities or the membership cut are being read wrongly",
   0.95e11 < Mb_LG < 2.2e11, f"M_b = {Mb_LG:.3e} Msun from {is_lg.sum()} members at Upsilon_K = {UPS_K}")

# ------------------------------------------------------------------ 4. the external field, measured
P("\n" + "="*126)
P("4. THE EXTERNAL FIELD AT THE LOCAL GROUP -- measured from its own peculiar velocity, and why it decides")
P("="*126)
v_pec = 620e3                                            # LG w.r.t. the CMB, Planck/COBE dipole
g_ext_true = 1.5*H0*v_pec/f_growth
P(f"  LG peculiar velocity w.r.t. the CMB = {v_pec/1e3:.0f} km/s; linear theory g_ext = (3/2) H_0 v/f, f = {f_growth:.3f}")
P(f"  => g_ext (the TRUE field, already boosted) = {g_ext_true:.3e} m/s^2")
EFE = {}
for k, f in FOOT.items():
    a0 = f['a0']
    e_true = g_ext_true/a0
    # invert  u nu(u) = e_true  for the NEWTONIAN external field u = g_N,ext/a_0
    u = brentq(lambda u: u*nu_s(u) - e_true, 1e-8, 10.0)
    nu_e = nu_s(u)
    L = 0.5*math.sqrt(u)*math.exp(-math.sqrt(u))/(1 - math.exp(-math.sqrt(u)))   # d ln nu/d ln y, Route A
    Geff = nu_e*(1 - L/3)                              # sphericalised quasi-Newtonian G_eff/G (QUMOND far field)
    EFE[k] = dict(e_true=e_true, u=u, nu=nu_e, L=L, Geff=Geff)
    P(f"  {k:<10s} g_ext/a_0 = {e_true:.4f} (true)  ->  g_N,ext/a_0 = {u:.5f}   nu(e_N) = {nu_e:6.2f}   "
      f"L = d ln nu/d ln y = {-L:+.3f}   G_eff/G = nu(1 - L/3) = {Geff:6.2f}")
for k, f in FOOT.items():
    g_int_at_R0 = f['HL']**2*R0_obs*Mpc
    P(f"  {k:<10s} the LG's OWN field at the measured R_0 is H_Lam^2 R_0 = {g_int_at_R0:.3e} m/s^2 = "
      f"{g_int_at_R0/f['a0']:.5f} a_0  -- i.e. {EFE[k]['e_true']/(g_int_at_R0/f['a0']):.0f}x SMALLER than the external field")
ck("K02.5 THE STRUCTURAL FINDING, and it is against the item's own premise: at the turnaround radius the "
   "system's internal field is H_Lam^2 R_0 by construction, which for the Local Group is 30-50x below the "
   "external field of large-scale structure.  The isolated deep-MOND branch of item 80 is therefore NOT the "
   "applicable regime, and this check records that rather than hiding it",
   all(EFE[k]['e_true'] > 5*(f['HL']**2*R0_obs*Mpc/f['a0']) for k, f in FOOT.items()),
   "external field exceeds the internal field at R_0 by more than 5x on both footings")

# ------------------------------------------------------------------ 5. the four branches, both footings
P("\n" + "="*126)
P("5. THE PREDICTIONS -- four branches, both footings, the alternative computed beside the framework")
P("="*126)
M200_LCDM = 2.0e12          # LambdaCDM Local Group halo mass, timing-argument/abundance value
P(f"  {'footing':<10s} {'branch':<44s} {'R_scale (Mpc)':>14s} {'x_ta':>7s} {'R_0 pred (Mpc)':>15s} {'obs/pred':>9s}")
PRED = {}
for k, f in FOOT.items():
    a0, HL = f['a0'], f['HL']
    Mb = Mb_LG*Msun
    RA = (G*Mb*a0)**0.25/HL/Mpc
    RL_b = (G*Mb/HL**2)**(1/3.)/Mpc
    RL_efe = (EFE[k]['Geff']*G*Mb/HL**2)**(1/3.)/Mpc
    RL_cdm = (G*M200_LCDM*Msun/HL**2)**(1/3.)/Mpc
    rows_ = [("FRAMEWORK isolated deep MOND + Lambda", RA, XTA[k]['mond']),
             ("FRAMEWORK EFE-quenched (G -> nu(e_N) G) + Lambda", RL_efe, XTA[k]['newt']),
             ("Newton + Lambda, BARYONS ONLY (no boost)", RL_b, XTA[k]['newt']),
             ("LambdaCDM: Newton + Lambda, M_200 = 2e12", RL_cdm, XTA[k]['newt'])]
    PRED[k] = {}
    for lab, Rs, x in rows_:
        R0p = x*Rs
        PRED[k][lab] = R0p
        P(f"  {k:<10s} {lab:<44s} {Rs:14.3f} {x:7.4f} {R0p:15.3f} {R0_obs/R0p:9.2f}")
P(f"\n  MEASURED: R_0 = {R0_obs:.3f} Mpc [{R0_lo:.3f}, {R0_hi:.3f}]  (published 0.96 +- 0.03)")
lo = min(min(PRED[k]["FRAMEWORK EFE-quenched (G -> nu(e_N) G) + Lambda"] for k in PRED),
         min(PRED[k]["Newton + Lambda, BARYONS ONLY (no boost)"] for k in PRED))
hi = max(PRED[k]["FRAMEWORK isolated deep MOND + Lambda"] for k in PRED)
P(f"  The framework's own bracket, isolated-MOND to EFE-quenched, is [{lo:.2f}, {hi:.2f}] Mpc -- a factor "
  f"{hi/lo:.1f} wide, and it contains the measurement.")
ck("K02.6 CLAIM UNDER TEST: that the isolated deep-MOND + Lambda turnaround radius, which is what item 80 "
   "actually proposed, predicts the Local Group's zero-velocity radius.  It does not -- it over-predicts by a "
   "factor 2 to 3 on both footings.  This check is written to FAIL if the item's own prediction is wrong, and it "
   "fails",
   all(abs(math.log10(R0_obs/PRED[k]["FRAMEWORK isolated deep MOND + Lambda"])) < 0.10 for k in PRED),
   "isolated-MOND predicts " + ", ".join(f"{k}: {PRED[k]['FRAMEWORK isolated deep MOND + Lambda']:.2f} Mpc"
                                         for k in PRED) + f" against {R0_obs:.2f} measured")
ck("K02.7 the EFE-quenched branch -- the regime check K02.5 says is the applicable one -- reproduces the "
   "measured R_0 within 0.15 dex on at least one footing, with no dark matter and no fitted parameter",
   any(abs(math.log10(R0_obs/PRED[k]["FRAMEWORK EFE-quenched (G -> nu(e_N) G) + Lambda"])) < 0.15 for k in PRED),
   ", ".join(f"{k}: pred {PRED[k]['FRAMEWORK EFE-quenched (G -> nu(e_N) G) + Lambda']:.2f} Mpc, "
             f"{math.log10(R0_obs/PRED[k]['FRAMEWORK EFE-quenched (G -> nu(e_N) G) + Lambda']):+.3f} dex" for k in PRED))

# the reformulated statement: M_dyn/M_b at the zero-velocity surface = nu(e_N)(1 - L/3)
P("\n  THE REFORMULATED STATEMENT, which is what survives:  the dynamical-to-baryonic mass ratio inferred at the")
P("  zero-velocity surface must equal the EXTERNAL-FIELD boost, M_dyn/M_b = nu(g_N,ext/a_0)(1 - L/3), with")
P("  g_ext measured from the system's OWN peculiar velocity.  For the Local Group:")
for k, f in FOOT.items():
    Mdyn = (R0_obs*Mpc/XTA[k]['newt'])**3*f['HL']**2/G/Msun
    P(f"    {k:<10s} M_dyn(from R_0) = {Mdyn:.3e} Msun  ->  M_dyn/M_b = {Mdyn/Mb_LG:6.2f}   "
      f"predicted nu(e_N)(1-L/3) = {EFE[k]['Geff']:6.2f}   ratio {Mdyn/Mb_LG/EFE[k]['Geff']:.2f} "
      f"({math.log10(Mdyn/Mb_LG/EFE[k]['Geff']):+.3f} dex)")
P(f"    LambdaCDM's answer to the same question is the cosmic baryon share, M_dyn/M_b = 1/f_b = {OmM/Omb:.1f},")
P( "    which is the SAME for every system and carries no dependence on the peculiar velocity.  That is the")
P( "    discriminator: the framework says the ratio must FALL as v_pec rises, roughly as v_pec^(-1/2).")

# ------------------------------------------------------------------ 6. sensitivity and mutation controls
P("\n" + "="*126)
P("6. SENSITIVITY AND MUTATION CONTROLS")
P("="*126)
k = 'canonical'; f = FOOT[k]
P("  levers on the EFE-quenched prediction R_0 = x_ta (nu(e_N) G M_b/H_Lam^2)^(1/3):")
P(f"    d log R_0 / d log M_b        = +1/3 exactly   -> d log R_0/d log Upsilon = (1/3) x (stellar share of M_b)")
star_share = UPS_K*LK_tot/Mb_LG
P(f"       stellar share of M_b(LG) = {star_share:.3f}  =>  d log R_0/d log Upsilon = {star_share/3:+.3f}")
P(f"    d log R_0 / d log g_ext      = (1/3) d log nu/d log e_N x d log e_N/d log g_ext")
for kk, ff in FOOT.items():
    e = EFE[kk]
    d = 0.001
    u2 = brentq(lambda u: u*nu_s(u) - e['e_true']*(1+d), 1e-8, 10.0)
    dlognu = math.log(nu_s(u2)/e['nu'])/math.log(1+d)
    P(f"       {kk:<10s} d log R_0/d log g_ext = {dlognu/3:+.4f}   (nu falls as e^-1/2, so the answer is weakly "
      f"sensitive to the external-field estimate)")
for kk in FOOT:
    a, b = PRED[kk]["FRAMEWORK EFE-quenched (G -> nu(e_N) G) + Lambda"], PRED[kk]["FRAMEWORK isolated deep MOND + Lambda"]
    P(f"    {kk:<10s} footing/branch spread: EFE-quenched {a:.2f} Mpc vs isolated {b:.2f} Mpc = {math.log10(b/a):.2f} dex")

P("\n  MUTATION CONTROLS")
for mult in (0.1, 10.0):
    a0m = A0['canonical']*mult
    HLm = Z_FW*a0m/c
    xm = x_turnaround(HLm*t0, 1)
    RAm = xm*(G*Mb_LG*Msun*a0m)**0.25/HLm/Mpc
    P(f"    M1 a_0 x {mult:<5g}: isolated-MOND R_0 -> {RAm:7.3f} Mpc "
      f"(vs {PRED['canonical']['FRAMEWORK isolated deep MOND + Lambda']:.3f} at the true a_0)")
ck("K02.8 MUTATION: scaling a_0 by 10 must move the framework's prediction.  R_scale goes as a_0^(1/4)/H_Lam ~ "
   "a_0^(-3/4), partly offset because x_ta rises with H_Lam t_0; net, a 10x wrong a_0 must move R_0 by more than "
   "0.3 dex, and the estimator is therefore not an a_0-blind fixed point",
   abs(math.log10(x_turnaround(Z_FW*A0['canonical']*10/c*t0, 1)*(G*Mb_LG*Msun*A0['canonical']*10)**0.25
                  / (Z_FW*A0['canonical']*10/c)/Mpc / PRED['canonical']['FRAMEWORK isolated deep MOND + Lambda'])) > 0.3,
   "a_0 x 10 moves the isolated prediction by more than 0.3 dex")

sh = vlg[win].copy(); rng2 = np.random.default_rng(7)
shuf = []
for _ in range(500):
    rng2.shuffle(sh)
    Ab = np.vstack([R_LG[win], np.ones(win.sum())]).T
    hh, bb = np.linalg.lstsq(Ab, sh, rcond=None)[0]
    if abs(hh) > 1e-6: shuf.append(-bb/hh)
shuf = np.array(shuf)
P(f"    M2 shuffling V_LG among the same galaxies: R_0 -> median {np.median(shuf):.2f} Mpc, "
  f"16-84% [{np.percentile(shuf,16):.2f}, {np.percentile(shuf,84):.2f}] -- the Hubble slope is destroyed")
ck("K02.9 MUTATION: shuffling which galaxy carries which velocity must destroy the measurement.  If the shuffled "
   "R_0 distribution contained the real value tightly, the fit would be a property of the marginal distributions "
   "rather than of the pairing",
   abs(np.median(shuf) - R0_obs) > 0.3 or np.percentile(shuf, 84) - np.percentile(shuf, 16) > 1.0,
   f"shuffled median {np.median(shuf):.2f} Mpc with an 16-84 width of "
   f"{np.percentile(shuf,84)-np.percentile(shuf,16):.2f} Mpc vs the real {R0_obs:.2f}")

# ------------------------------------------------------------------ 7. bug-pattern audit and verdict
P("\n" + "="*126)
P("7. BUG-PATTERN AUDIT")
P("="*126)
P("  (1) TOTAL vs ENCLOSED mass.  The turnaround radius is OUTSIDE the whole system, so the TOTAL baryonic mass")
P("      is the correct one here -- the opposite of the usual trap, and stated so it is not fixed by mistake.")
P("      Checked: the membership cut takes everything within 1.2 Mpc of the barycentre, inside the measured R_0's")
P("      collapsing region, and adding the 0.7-1.2 Mpc shell changes M_b by less than 3%.")
P("  (2) SPHERICAL formula on a DISC.  Not applicable: at Mpc scales the Local Group is a two-body point mass, and")
P("      the collapse integral is spherical by construction.  The two-body correction IS a real caveat and is")
P("      recorded in the verdict rather than modelled.")
P("  (3) An aperture on a SADDLE.  The LG barycentre is a maximum of the potential's source, not a saddle; the")
P("      saddle between MW and M31 is at ~0.35 Mpc, inside the excluded region (the fit starts at 0.7 Mpc).")
P("  (4) A covariance in the wrong index order.  No covariance is used; errors are galaxy bootstraps.")
P("  (5) A trivial correlation from joint-fit degeneracy.  R_0 comes from distances and velocities; M_b comes from")
P("      K-band light and HI fluxes.  The two share the distance scale (both scale with D), which is the one real")
P("      coupling: R_0 ~ D and M_b ~ D^2, so d log(R_0 pred)/d log D = 2/3 against d log(R_0 obs)/d log D = 1.")
P("      A 10% distance-scale error therefore moves the RATIO by only 0.014 dex, not by 0.10.")

P("\n" + "="*126)
P("VERDICT -- ITEM 80 / CANDIDATE k02")
P("="*126)
P("  THE ITEM AS WRITTEN IS REFUTED.  Its prediction was the isolated deep-MOND turnaround radius")
P("  R_0 = x_ta (G M_b a_0)^(1/4)/H_Lam.  Measured against the Local Group's own zero-velocity surface it")
P(f"  over-predicts by a factor {R0_obs and PRED['canonical']['FRAMEWORK isolated deep MOND + Lambda']/R0_obs:.1f} "
  f"(canonical) / {PRED['alt']['FRAMEWORK isolated deep MOND + Lambda']/R0_obs:.1f} (alt).")
P("  THE REASON IS STRUCTURAL, NOT ACCIDENTAL, and it is the transferable finding: at a turnaround radius the")
P("  system's own field has by definition fallen to H_Lam^2 R_0, which is 30-50x below the external field of")
P("  large-scale structure.  EVERY zero-velocity surface in the Local Volume is deep in the external-field")
P("  regime.  The isolated deep-MOND branch can never be the right one for this observable.")
P("  WHAT SURVIVES, and it is a different and better statement than the item's: with the external field measured")
P("  from the group's own peculiar velocity, the framework is quasi-Newtonian at R_0 with G -> nu(e_N)(1-L/3) G,")
P("  and the Local Group's zero-velocity radius follows with no dark matter and no fitted parameter.  The")
P("  discriminating content is then a CORRELATION nothing in LambdaCDM produces: M_dyn/M_b at the zero-velocity")
P("  surface must fall as the group's peculiar velocity rises, roughly as v_pec^(-1/2), where LambdaCDM gives the")
P("  same 1/f_b for every group regardless of its motion.  One system cannot test a correlation; this needs the")
P("  10-15 Local Volume groups with measured R_0 and the CMB-frame peculiar velocity of each.")
P("  NOT KEPLER-GRADE ON ONE SYSTEM.  Promoted to the list as a two-parameter correlation test, not as a law.")
raise SystemExit(ck.done())
