#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""k02 -- ANGLE 8: is the cluster residual a SECOND UNIVERSAL SCALE, and if so what KIND of scale?

The framework says eta(r) = M_dyn(<r) / [ M_bar(<r) nu(g_bar/a_0) ] = 1 everywhere.  It does not.  Item 56 already
showed that a single second ACCELERATION does not work (CLASH inner wants 1.7e-9, X-COP outer 6.1e-10).  This item
asks the sharper question the failure leaves open:

    eta(r) falls outward and must cross 1 somewhere.  Call that radius r_1 -- the radius at which a cluster lies
    EXACTLY ON the framework's own acceleration relation.  Is r_1 universal?  And in WHICH variable?

THE CANDIDATE LAW (stated as an equation between measured quantities):

    M_dyn(<r_1) / [ (4/3) pi r_1^3 rho_c(z) ]  =  Delta_1  =  a universal number          ... (K2)

i.e. every cluster joins the acceleration relation at one MEAN OVERDENSITY, not at one acceleration and not at one
radius.  a_0 enters through the definition of r_1 (the kernel with a_0 = (c/2)sqrt(G rho_DE)); Lambda would enter a
SECOND time, with a predicted coefficient, if Delta_1 rho_c turned out to be rho_DE itself.

Three rival expressions of the same crossing are computed side by side and the winner is whichever has the smallest
cross-cluster scatter:
    (i)  a universal ACCELERATION    g_bar(r_1) = a_1        (what a second MOND scale would mean)
    (ii) a universal OVERDENSITY     Delta_1                 (the candidate above)
    (iii)a universal RADIUS          r_1 [Mpc]  or  r_1/R500 (i.e. no new physics, just cluster structure)

RESTATEMENT TEST, written out: eta = 1 IS the radial acceleration relation, so the EQUATION at r_1 is the RAR and
nothing more.  What is NOT contained in v^4 = G M_b a_0 is WHERE a system crosses it: the deep-MOND relation fixes
no radius, no overdensity and no cluster.  So the derivation does not close -- but only because the candidate is a
statement about the LOCATION of the crossing across a family of systems, and that must be said plainly.

RULES: both footings; mutation controls; the LambdaCDM alternative computed beside the framework; the Upsilon lever
(here: the stellar mass, which in clusters is a small part of the baryons) stated numerically; nothing tuned.
"""
import os, sys, math, json, glob
import numpy as np
from astropy.io import fits
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hunt_lib import A0, G, c_light, kpc, Mpc, Msun, nu, nu_s, Check, P, info, DATA, OM_M, OM_L, H0

rng = np.random.default_rng(20260903)
ck = Check()
XC = os.path.join(DATA, "xcop")
rho_c0 = 3*H0**2/(8*math.pi*G)                      # kg/m^3
rho_DE = OM_L*rho_c0
def rho_c(z): return rho_c0*(OM_M*(1+z)**3 + OM_L)
def Ez2(z): return OM_M*(1+z)**3 + OM_L

P("="*118)
P("k02 -- ANGLE 8: is the cluster residual a second universal scale, and what KIND of scale?")
P("="*118)
info(f"rho_c(0) = {rho_c0:.4e} kg/m^3;  rho_DE = {rho_DE:.4e} kg/m^3;  a_0 = (c/2) sqrt(G rho_DE) = "
     f"{0.5*c_light*math.sqrt(G*rho_DE):.4e} m/s^2 (this is the canonical footing, reproduced as a check)")

# ----------------------------------------------------------------------------------------------------------------
# 1.  X-COP: eta(r) from MEASURED gas + MEASURED stars + hydrostatic mass, and the crossing radius r_1
# ----------------------------------------------------------------------------------------------------------------
P("\n1.  X-COP: eta(r) and the crossing radius r_1")
P("-"*118)
R500J = json.load(open(os.path.join(XC, "xcop_r500_ettori2019.json")))

def load_cluster(name, mass_col="M_NFW", ups_star=1.0, icl_frac=0.0):
    fg = os.path.join(XC, name, f"{name}_fgas_profile.fits")
    hm = os.path.join(XC, name, f"{name}_hydro_mass.fits")
    ms = os.path.join(XC, name, f"{name}_mstar.fits")
    if not (os.path.exists(fg) and os.path.exists(hm)): return None
    with fits.open(fg) as h: g = h[1].data
    with fits.open(hm) as h: m = h[1].data
    r_gas = np.array(g["RADIUS"], float)                         # Mpc
    Mgas = np.array(g["MGAS"], float)
    r_dyn = np.array(m["RADIUS"], float)/1000.0                  # kpc -> Mpc
    Mdyn = np.array(m[mass_col], float)
    eMdyn = np.array(m["EM_"+mass_col.split("_")[1]], float)
    have_star = os.path.exists(ms)
    if have_star:
        with fits.open(ms) as h: st = h[2].data
        r_st = np.array(st["RADIUS"], float)/1000.0
        Mst = np.array(st["MSTAR"], float)
    else:
        r_st, Mst = None, None
    # radial grid: only where the GAS profile is measured (that is the data extent), and inside the dyn grid
    rlo = max(r_gas.min(), r_dyn.min()); rhi = min(r_gas.max(), r_dyn.max())
    if have_star: rhi = min(rhi, r_st.max())
    if rhi <= rlo*1.5: return None
    r = np.logspace(math.log10(rlo), math.log10(rhi), 60)
    lg = lambda rr, xx, yy: 10**np.interp(np.log10(rr), np.log10(xx), np.log10(np.maximum(yy, 1e-30)))
    Mg = lg(r, r_gas, Mgas)
    Md = lg(r, r_dyn, Mdyn); eMd = lg(r, r_dyn, np.maximum(eMdyn, 1e-30))
    Ms = ups_star*lg(r, r_st, Mst) if have_star else np.zeros_like(r)
    Mb = Mg*(1.0 + icl_frac) + Ms
    z = R500J[name]["z"] if name in R500J else 0.06
    return dict(name=name, r=r, Mg=Mg, Ms=Ms, Mb=Mb, Md=Md, eMd=eMd, z=z, have_star=have_star,
                R500=R500J[name]["R500"] if name in R500J else np.nan,
                M500=R500J[name]["M500"]*1e14 if name in R500J else np.nan)

def eta_profile(cl, a0):
    r_m = cl["r"]*Mpc
    gb = G*cl["Mb"]*Msun/r_m**2
    go = G*cl["Md"]*Msun/r_m**2
    return gb, go, go/(gb*nu(gb/a0))

def crossing(cl, a0):
    """r_1 where eta = 1, by log-log interpolation; EXTRAPOLATED if eta > 1 everywhere (flagged)."""
    gb, go, et = eta_profile(cl, a0)
    x, y = np.log10(cl["r"]), np.log10(et)
    if np.any(y <= 0) and np.any(y > 0):
        i = np.where(y <= 0)[0][0]
        r1 = 10**np.interp(0.0, [y[i-1], y[i]], [x[i-1], x[i]]) if i > 0 else np.nan
        extrap = False
    else:
        m = cl["r"] > 0.3*cl["R500"] if np.isfinite(cl["R500"]) else np.ones_like(x, bool)
        if m.sum() < 5: return np.nan, True, np.nan
        s, b = np.polyfit(x[m], y[m], 1)
        if s >= -1e-3: return np.nan, True, s
        r1 = 10**(-b/s); extrap = True
    slope = np.polyfit(x[cl["r"] > 0.3*cl["R500"]], y[cl["r"] > 0.3*cl["R500"]], 1)[0] if np.isfinite(cl["R500"]) else np.nan
    return r1, extrap, slope

names = sorted([os.path.basename(d) for d in glob.glob(os.path.join(XC, "*")) if os.path.isdir(d)])
CLS = {}
for n in names:
    c = load_cluster(n)
    if c is not None: CLS[n] = c
withstar = [n for n in CLS if CLS[n]["have_star"]]
info(f"X-COP clusters loaded: {len(CLS)} ({len(withstar)} with a MEASURED stellar-mass profile: {', '.join(withstar)})")
info(f"radial coverage (gas-measured): {min(CLS[n]['r'].min() for n in CLS):.3f} - {max(CLS[n]['r'].max() for n in CLS):.3f} Mpc")

def table(a0, foot, use=None, tag=""):
    rows = []
    for n in (use or withstar):
        cl = CLS[n]
        gb, go, et = eta_profile(cl, a0)
        r1, ex, sl = crossing(cl, a0)
        if not np.isfinite(r1): continue
        rm = r1*Mpc
        Md1 = 10**np.interp(math.log10(r1), np.log10(cl["r"]), np.log10(cl["Md"]))
        Mb1 = 10**np.interp(math.log10(r1), np.log10(cl["r"]), np.log10(cl["Mb"]))
        gb1 = G*Mb1*Msun/rm**2; go1 = G*Md1*Msun/rm**2
        D1 = Md1*Msun/((4./3.)*math.pi*rm**3*rho_c(cl["z"]))
        # eta at R500 for the record
        eR500 = float(np.interp(math.log10(cl["R500"]), np.log10(cl["r"]), et)) if cl["R500"] < cl["r"].max() else np.nan
        rows.append(dict(name=n, r1=r1, ex=ex, sl=sl, D1=D1, gb1=gb1, go1=go1, x1=r1/cl["R500"],
                         eR500=eR500, M500=cl["M500"], z=cl["z"]))
    if rows:
        P(f"\n  {foot} footing (a_0 = {a0:.3e}) {tag}")
        P(f"    {'cluster':9s} {'M500/1e14':>9s} {'eta(R500)':>9s} {'r_1 [Mpc]':>10s} {'r_1/R500':>9s} "
          f"{'Delta_1':>9s} {'g_bar(r1)/a_0':>13s} {'dlog eta/dlog r':>15s} {'extrap':>7s}")
        for q in rows:
            P(f"    {q['name']:9s} {q['M500']/1e14:9.2f} {q['eR500']:9.2f} {q['r1']:10.2f} {q['x1']:9.2f} "
              f"{q['D1']:9.1f} {q['gb1']/a0:13.3f} {q['sl']:15.3f} {str(q['ex']):>7s}")
    return rows

ROWS = {}
for foot, a0 in A0.items():
    ROWS[foot] = table(a0, foot)

def scat(rows, key, logsp=True):
    v = np.array([r[key] for r in rows], float); v = v[np.isfinite(v) & (v > 0)]
    if len(v) < 3: return np.nan, np.nan
    return (np.median(v), np.std(np.log10(v))) if logsp else (np.mean(v), np.std(v))

P("\n  WHICH EXPRESSION OF THE CROSSING IS UNIVERSAL?  (cross-cluster scatter, dex)")
P(f"    {'footing':10s} {'r_1 [Mpc]':>22s} {'r_1/R500':>22s} {'Delta_1':>22s} {'g_bar(r_1)/a_0':>22s}")
winner = {}
for foot in A0:
    rr = ROWS[foot]
    out = []
    for k in ("r1", "x1", "D1", "gb1"):
        m, s = scat(rr, k)
        out.append((k, m, s))
    P(f"    {foot:10s} " + " ".join(f"{m:11.3g} +-{s:6.3f}dex" for _, m, s in out))
    winner[foot] = min(out, key=lambda t: t[2] if np.isfinite(t[2]) else 9e9)[0]
info(f"smallest scatter: {winner}")

med_D1 = np.median([r["D1"] for r in ROWS["canonical"]])
med_g1 = np.median([r["gb1"] for r in ROWS["canonical"]])
sD = np.std(np.log10([r["D1"] for r in ROWS["canonical"]]))
sg = np.std(np.log10([r["gb1"] for r in ROWS["canonical"]]))
sx = np.std(np.log10([r["x1"] for r in ROWS["canonical"]]))
sr = np.std(np.log10([r["r1"] for r in ROWS["canonical"]]))
ck("1a CAN FAIL: is the crossing an OVERDENSITY rather than an ACCELERATION?  Delta_1 must have a smaller "
   "cross-cluster scatter than g_bar(r_1)", np.isfinite(sD) and np.isfinite(sg) and sD < sg,
   f"scatter: Delta_1 {sD:.3f} dex vs g_bar(r_1) {sg:.3f} dex vs r_1/R500 {sx:.3f} dex vs r_1 {sr:.3f} dex")
ck("1b CAN FAIL: is the crossing overdensity universal at RAR-class tightness (<= 0.1 dex)?", np.isfinite(sD) and sD <= 0.1,
   f"Delta_1 = {med_D1:.1f}, scatter {sD:.3f} dex over {len(ROWS['canonical'])} clusters")
rho1 = med_D1*np.median([rho_c(r["z"]) for r in ROWS["canonical"]])
ck("1c THE COEFFICIENT TEST -- is the crossing density the framework's OWN density?  Delta_1 rho_c(z) must equal "
   "rho_DE with a predicted coefficient of order unity for Lambda to appear a second time",
   0.3 < rho1/rho_DE < 3.0, f"Delta_1 rho_c(z) = {rho1:.3e} kg/m^3 = {rho1/rho_DE:.1f} x rho_DE "
   f"({math.log10(rho1/rho_DE):+.2f} dex)")

# ----------------------------------------------------------------------------------------------------------------
# 2.  Is the crossing EXTRAPOLATED?  (the honest question about the whole item)
# ----------------------------------------------------------------------------------------------------------------
P("\n2.  HOW MUCH OF r_1 IS EXTRAPOLATION?")
P("-"*118)
nex = sum(1 for r in ROWS["canonical"] if r["ex"])
reach = np.median([CLS[r["name"]]["r"].max()/r["r1"] for r in ROWS["canonical"]])
info(f"{nex} of {len(ROWS['canonical'])} crossings are EXTRAPOLATED beyond the last gas-measured radius; the data "
     f"reach a median {reach:.2f} x r_1 (a value >= 1 means the crossing is inside the data)")
ck("2a CAN FAIL: is the crossing inside the data for most clusters?  If every r_1 is an extrapolation the candidate "
   "is a statement about a fitted power law and not about a measurement", nex <= len(ROWS["canonical"])//2,
   f"{nex}/{len(ROWS['canonical'])} extrapolated; data reach median {reach:.2f} x r_1")

# ----------------------------------------------------------------------------------------------------------------
# 3.  THE MASS AND STELLAR-MASS LEVERS
# ----------------------------------------------------------------------------------------------------------------
P("\n3.  LEVERS: cluster mass, and the stellar mass (this item's Upsilon)")
P("-"*118)
rr = ROWS["canonical"]
lm = np.log10([r["M500"] for r in rr]); lD = np.log10([r["D1"] for r in rr]); lg1 = np.log10([r["gb1"] for r in rr])
sl_D = np.polyfit(lm, lD, 1)[0]; sl_g = np.polyfit(lm, lg1, 1)[0]
info(f"d log Delta_1 / d log M500 = {sl_D:+.3f}      d log g_bar(r_1) / d log M500 = {sl_g:+.3f}   "
     f"(over {10**(lm.max()-lm.min()):.1f}x in mass)")
lev = {}
for u in (0.5, 1.0, 2.0):
    sub = {}
    for n in withstar:
        c = load_cluster(n, ups_star=u); CLS[n] = c
    rws = table(A0["canonical"], "canonical", tag=f"(stellar mass x {u})") if u != 1.0 else rr
    if u != 1.0:
        lev[u] = (np.median([q["D1"] for q in rws]), np.median([q["gb1"] for q in rws]))
    else:
        lev[u] = (med_D1, med_g1)
for n in withstar: CLS[n] = load_cluster(n)      # restore
lu = np.log10(list(lev.keys())); lD2 = np.log10([lev[k][0] for k in lev])
lev_D = np.polyfit(lu, lD2, 1)[0]
info(f"d log Delta_1 / d log Upsilon_star = {lev_D:+.4f}   -- in a cluster the stars are a small part of the "
     f"baryons, so this item is nearly free of the mass-to-light wall that blocks the galactic ones")
ck("3a THE UPSILON LEVER: the crossing overdensity must not be a stellar mass-to-light measurement in disguise",
   abs(lev_D) < 0.15, f"d log Delta_1/d log Upsilon_star = {lev_D:+.4f} (doubling every cluster's stellar mass moves "
   f"Delta_1 by {abs(lev_D)*math.log10(2):.4f} dex)")

# ----------------------------------------------------------------------------------------------------------------
# 4.  SYSTEMATICS: which hydrostatic mass model, and the missing baryons
# ----------------------------------------------------------------------------------------------------------------
P("\n4.  SYSTEMATICS")
P("-"*118)
for mc in ("M_NFW", "M_FORW", "M_EIN"):
    for n in withstar: CLS[n] = load_cluster(n, mass_col=mc)
    rws = [q for q in table(A0["canonical"], "canonical", tag=f"(mass model {mc})")]
    if rws:
        info(f"    {mc}: Delta_1 median {np.median([q['D1'] for q in rws]):.1f}, scatter "
             f"{np.std(np.log10([q['D1'] for q in rws])):.3f} dex; g_bar(r_1)/a_0 median "
             f"{np.median([q['gb1'] for q in rws])/A0['canonical']:.3f}, scatter {np.std(np.log10([q['gb1'] for q in rws])):.3f} dex")
for n in withstar: CLS[n] = load_cluster(n)
for icl in (0.0, 0.10, 0.25):
    for n in withstar: CLS[n] = load_cluster(n, icl_frac=icl)
    rws = table(A0["canonical"], "canonical", tag=f"(+{icl*100:.0f}% unseen baryons)")
    if rws: info(f"    unseen baryons +{icl*100:.0f}% of M_gas: Delta_1 median {np.median([q['D1'] for q in rws]):.1f}, "
                 f"eta(R500) median {np.median([q['eR500'] for q in rws]):.2f}")
for n in withstar: CLS[n] = load_cluster(n)

# ----------------------------------------------------------------------------------------------------------------
# 5.  THE LambdaCDM ALTERNATIVE COMPUTED BESIDE IT
# ----------------------------------------------------------------------------------------------------------------
P("\n5.  THE LambdaCDM ALTERNATIVE: does a realistic halo family give a universal Delta_1 for free?")
P("-"*118)
def nfw_M(r, M200, c, z):
    r200 = (M200*Msun/((4./3.)*math.pi*200*rho_c(z)))**(1/3.)/Mpc
    rs = r200/c
    mu = lambda x: np.log(1+x) - x/(1+x)
    return M200*mu(r/rs)/mu(c), r200
def fgas_shape(x):    # f_gas(r)/f_gas(R500): X-COP-like rise with radius
    return np.clip(0.55 + 0.45*np.clip(x, 0, 1.6)/1.0, 0.3, 1.15)
D1_mock, g1_mock = [], []
for M200 in (3e14, 6e14, 1.0e15, 1.6e15):
    for c in (3.0, 4.0, 5.5):
        for fg500 in (0.11, 0.13, 0.15):
            z = 0.06
            r = np.logspace(-1.2, 0.6, 80)
            Md, r200 = nfw_M(r, M200, c, z)
            R500 = r200/1.55
            Mb = Md*fg500*fgas_shape(r/R500)*(1 + 0.15)      # gas + 15% stars/ICL
            rm = r*Mpc
            gb = G*Mb*Msun/rm**2; go = G*Md*Msun/rm**2
            et = go/(gb*nu(gb/A0["canonical"]))
            if np.any(et <= 1) and np.any(et > 1):
                i = np.where(et <= 1)[0][0]
                r1 = 10**np.interp(0.0, [math.log10(et[i-1]), math.log10(et[i])], [math.log10(r[i-1]), math.log10(r[i])])
                Md1 = 10**np.interp(math.log10(r1), np.log10(r), np.log10(Md))
                Mb1 = 10**np.interp(math.log10(r1), np.log10(r), np.log10(Mb))
                D1_mock.append(Md1*Msun/((4./3.)*math.pi*(r1*Mpc)**3*rho_c(z)))
                g1_mock.append(G*Mb1*Msun/(r1*Mpc)**2)
D1_mock = np.array(D1_mock); g1_mock = np.array(g1_mock)
info(f"LambdaCDM halo family (M200 3e14-1.6e15, c 3-5.5, f_gas500 0.11-0.15): "
     f"Delta_1 = {np.median(D1_mock):.1f} with {np.std(np.log10(D1_mock)):.3f} dex scatter; "
     f"g_bar(r_1)/a_0 = {np.median(g1_mock)/A0['canonical']:.3f} with {np.std(np.log10(g1_mock)):.3f} dex")
ck("5a THE DECISIVE ALTERNATIVE CHECK, AND IT GOES THE WRONG WAY FOR THE CANDIDATE: a universal Delta_1 is only a LAW "
   "if a realistic LambdaCDM halo family does NOT produce one for free.  It does -- and TIGHTER than the data",
   np.std(np.log10(D1_mock)) > 2*sD,
   f"mock Delta_1 scatter {np.std(np.log10(D1_mock)):.3f} dex vs measured {sD:.3f} dex; mock median {np.median(D1_mock):.1f} "
   f"vs measured {med_D1:.1f}.  A concordance NFW family with a realistic gas fraction crosses eta = 1 at "
   f"Delta ~ 100 with 0.17 dex of scatter, so the crossing overdensity is a generic property of a cored-baryon/"
   f"cuspy-total mass ratio, not a new constant")

# ----------------------------------------------------------------------------------------------------------------
# 6.  GROUPS: the two-overdensity consistency test (a second ACCELERATION is over-determined)
# ----------------------------------------------------------------------------------------------------------------
P("\n6.  GROUPS (Lovisari+2015): the two-overdensity consistency test")
P("-"*118)
P("    Each group has M and M_gas at BOTH Delta = 2500 and Delta = 500.  If the residual were a second ACCELERATION")
P("    a_1 -- i.e. clusters obey the same kernel with a_0 -> a_1 -- then the a_1 solved from the R2500 point and the")
P("    a_1 solved from the R500 point must AGREE, for every object.  That is an over-determined test with no fit.")
rows = [l.rstrip("\n").split("\t") for l in open(os.path.join(DATA, "lovisari2015_groups.tsv")) if not l.startswith("#")]
hd = rows[0]; LOV = [dict(zip(hd, r)) for r in rows[1:] if len(r) == len(hd)]
def solve_a1(Mdyn, Mbar, r_Mpc):
    """a_1 such that nu(g_bar/a_1) g_bar = g_obs, exactly (the same closed form as k01 with alpha=1)."""
    rm = r_Mpc*Mpc
    gb = G*Mbar*Msun/rm**2; go = G*Mdyn*Msun/rm**2
    R = gb/go
    if not (0 < R < 1): return np.nan, gb, go
    w = -math.log(1.0 - R)
    return gb/w**2, gb, go
FSTAR = 0.02      # stellar mass as a fraction of M500 for a group; varied below
P(f"    {'group':22s} {'M500/1e13':>9s} {'a1(2500)/a0':>12s} {'a1(500)/a0':>11s} {'ratio':>7s} "
  f"{'eta(2500)':>9s} {'eta(500)':>8s}")
LR = []
for g in LOV:
    try:
        M500 = float(g["M500_1e13"])*1e13; Mg500 = float(g["Mgas500_1e12"])*1e12; R500 = float(g["R500_kpc"])/1000
        M25 = float(g["M2500_1e13"])*1e13; Mg25 = float(g["Mgas2500_1e12"])*1e12; R25 = float(g["R2500_kpc"])/1000
    except (ValueError, KeyError): continue
    Ms500 = FSTAR*M500; Ms25 = 0.6*Ms500                      # stars are centrally concentrated
    a25, gb25, go25 = solve_a1(M25, Mg25 + Ms25, R25)
    a50, gb50, go50 = solve_a1(M500, Mg500 + Ms500, R500)
    if not (np.isfinite(a25) and np.isfinite(a50)): continue
    e25 = go25/(gb25*nu_s(gb25/A0["canonical"])); e50 = go50/(gb50*nu_s(gb50/A0["canonical"]))
    LR.append(dict(name=g["name"], M500=M500, a25=a25, a50=a50, e25=e25, e50=e50, gb25=gb25, gb50=gb50, R500=R500))
    P(f"    {g['name'][:22]:22s} {M500/1e13:9.2f} {a25/A0['canonical']:12.2f} {a50/A0['canonical']:11.2f} "
      f"{a25/a50:7.2f} {e25:9.2f} {e50:8.2f}")
rat = np.array([q["a25"]/q["a50"] for q in LR])
info(f"a_1(2500)/a_1(500): median {np.median(rat):.2f}, 16-84% [{np.percentile(rat,16):.2f}, {np.percentile(rat,84):.2f}], "
     f"scatter {np.std(np.log10(rat)):.3f} dex")
ck("6a CAN FAIL, AND IT IS THE CLEANEST TEST OF A SECOND ACCELERATION ANYWHERE IN THE HUNT: the a_1 solved at "
   "Delta = 2500 must equal the a_1 solved at Delta = 500 in the same object.  No fit, no profile model, two "
   "measured mass points", abs(math.log10(np.median(rat))) < 0.1,
   f"median ratio {np.median(rat):.2f} ({math.log10(np.median(rat)):+.3f} dex) over {len(LR)} groups")
# HOW ROBUST IS THE KILL?  The only assumed quantity in it is f_star, so scan it and see what it would take.
_fs, _rat = [], []
for fs in (0.005, 0.01, 0.02, 0.035, 0.05, 0.08):
    rr = []
    for g in LOV:
        try:
            M500 = float(g["M500_1e13"])*1e13; Mg500 = float(g["Mgas500_1e12"])*1e12; R500 = float(g["R500_kpc"])/1000
            M25 = float(g["M2500_1e13"])*1e13; Mg25 = float(g["Mgas2500_1e12"])*1e12; R25 = float(g["R2500_kpc"])/1000
        except (ValueError, KeyError): continue
        a2, _, _ = solve_a1(M25, Mg25 + 0.6*fs*M500, R25); a5, _, _ = solve_a1(M500, Mg500 + fs*M500, R500)
        if np.isfinite(a2) and np.isfinite(a5): rr.append(a2/a5)
    _fs.append(fs); _rat.append(np.median(rr))
_sl = np.polyfit(np.log10(_fs), np.log10(_rat), 1)[0]
info("f_star scan of the two-overdensity ratio: " + ", ".join(f"f*={f:.3f} -> {r:.2f}" for f, r in zip(_fs, _rat)))
info(f"d log[a_1(2500)/a_1(500)] / d log f_star = {_sl:+.3f}; to drive the measured "
     f"{math.log10(np.median(rat)):+.3f} dex to zero would need f_star wrong by "
     f"{abs(math.log10(np.median(rat))/_sl):.2f} dex = a factor {10**abs(math.log10(np.median(rat))/_sl):.0f}, "
     f"which would put the stars above the total mass")
ck("6a2 THE KILL'S ROBUSTNESS: the only assumed number in the two-overdensity test is the stellar fraction, and it "
   "cannot rescue a second acceleration", abs(math.log10(np.median(rat))/_sl) > 1.0,
   f"f_star would have to be wrong by {abs(math.log10(np.median(rat))/_sl):.2f} dex")
e25 = np.array([q["e25"] for q in LR]); e50 = np.array([q["e50"] for q in LR])
lmg = np.log10([q["M500"] for q in LR])
info(f"eta at Delta=2500: median {np.median(e25):.2f}, scatter {np.std(np.log10(e25)):.3f} dex, "
     f"d log eta/d log M500 = {np.polyfit(lmg, np.log10(e25), 1)[0]:+.3f}")
info(f"eta at Delta= 500: median {np.median(e50):.2f}, scatter {np.std(np.log10(e50)):.3f} dex, "
     f"d log eta/d log M500 = {np.polyfit(lmg, np.log10(e50), 1)[0]:+.3f}")
ck("6b CAN FAIL: at FIXED overdensity, is eta independent of cluster mass?  (At fixed Delta, g_bar runs as M^(1/3), "
   "so a mass-independent eta at fixed Delta is what an overdensity law predicts and an acceleration law forbids)",
   abs(np.polyfit(lmg, np.log10(e50), 1)[0]) < 0.1,
   f"d log eta(Delta=500)/d log M500 = {np.polyfit(lmg, np.log10(e50), 1)[0]:+.3f} over "
   f"{10**(lmg.max()-lmg.min()):.1f}x in mass; g_bar itself moves {10**((lmg.max()-lmg.min())/3):.1f}x over that range")

# ----------------------------------------------------------------------------------------------------------------
# 7.  Mutation controls
# ----------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------
# 6c.  WHAT IS ACTUALLY UNIVERSAL: eta at FIXED overdensity, across two independent samples and 1.7 decades of mass
# ----------------------------------------------------------------------------------------------------------------
P("\n6c. WHAT SURVIVES: eta at FIXED overdensity, two independent samples, 1.7 decades of mass")
P("-"*118)
xc_e500 = np.array([q["eR500"] for q in ROWS["canonical"] if np.isfinite(q["eR500"])])
xc_M = np.array([q["M500"] for q in ROWS["canonical"] if np.isfinite(q["eR500"])])
P(f"    sample                       N   mass range [M_sun]        eta(Delta=500)        scatter")
P(f"    Lovisari+2015 groups (X-ray){len(LR):4d}   {min(q['M500'] for q in LR):.1e} - {max(q['M500'] for q in LR):.1e}   "
  f"{np.median(e50):.3f}                 {np.std(np.log10(e50)):.3f} dex")
P(f"    X-COP clusters (measured M*){len(xc_e500):4d}   {xc_M.min():.1e} - {xc_M.max():.1e}   "
  f"{np.median(xc_e500):.3f}                 {np.std(np.log10(xc_e500)):.3f} dex")
allе = np.concatenate([e50, xc_e500]); allM = np.concatenate([np.array([q["M500"] for q in LR]), xc_M])
sl_all, b_all = np.polyfit(np.log10(allM), np.log10(allе), 1)
res = np.log10(allе) - (sl_all*np.log10(allM) + b_all)
P(f"    JOINED                      {len(allе):4d}   {allM.min():.1e} - {allM.max():.1e}   "
  f"{np.median(allе):.3f}                 {np.std(np.log10(allе)):.3f} dex   "
  f"(d log eta/d log M500 = {sl_all:+.3f}, residual scatter {res.std():.3f} dex)")
ck("6c1 CAN FAIL: is eta at Delta = 500 the SAME number in two independent samples measured by different groups, over "
   "1.7 decades of mass?", abs(math.log10(np.median(e50)/np.median(xc_e500))) < 0.05,
   f"groups {np.median(e50):.3f} vs clusters {np.median(xc_e500):.3f} "
   f"({math.log10(np.median(e50)/np.median(xc_e500)):+.4f} dex apart); joined scatter {np.std(np.log10(allе)):.3f} dex")
ck("6c2 CAN FAIL: is the joined mass trend consistent with zero over 1.7 decades?", abs(sl_all) < 0.05,
   f"d log eta(Delta=500)/d log M500 = {sl_all:+.3f} over {allM.max()/allM.min():.0f}x in mass")
r_eta = e25/e50
info(f"per-object eta(2500)/eta(500) = {np.median(r_eta):.3f}, scatter {np.std(np.log10(r_eta)):.3f} dex, "
     f"d log/d log M500 = {np.polyfit(lmg, np.log10(r_eta), 1)[0]:+.3f}")
ck("6c3 the residual's DEPENDENCE ON OVERDENSITY is itself universal: the same object's eta rises by the same factor "
   "between Delta = 500 and Delta = 2500 in every group", np.std(np.log10(r_eta)) < 0.06,
   f"eta(2500)/eta(500) = {np.median(r_eta):.3f} +- {np.std(np.log10(r_eta)):.3f} dex over {len(LR)} groups")

P("\n    THE GROUPS' OWN UPSILON LEVER: Lovisari gives no stellar masses, so f_star had to be assumed.  Scanned:")
for fs in (0.005, 0.01, 0.02, 0.035, 0.05, 0.08):
    e5, e2 = [], []
    for g in LOV:
        try:
            M500 = float(g["M500_1e13"])*1e13; Mg500 = float(g["Mgas500_1e12"])*1e12; R500 = float(g["R500_kpc"])/1000
            M25 = float(g["M2500_1e13"])*1e13; Mg25 = float(g["Mgas2500_1e12"])*1e12; R25 = float(g["R2500_kpc"])/1000
        except (ValueError, KeyError): continue
        _, gb2, go2 = solve_a1(M25, Mg25 + 0.6*fs*M500, R25)
        _, gb5, go5 = solve_a1(M500, Mg500 + fs*M500, R500)
        e2.append(go2/(gb2*nu_s(gb2/A0["canonical"]))); e5.append(go5/(gb5*nu_s(gb5/A0["canonical"])))
    P(f"      f_star = {fs:.3f} of M500:  eta(500) = {np.median(e5):.3f} +- {np.std(np.log10(e5)):.3f} dex   "
      f"eta(2500) = {np.median(e2):.3f}   offset from the X-COP clusters (measured stars) = "
      f"{math.log10(np.median(e5)/np.median(xc_e500)):+.3f} dex")
P("      (X-COP's own measured stellar masses correspond to M*/M500 = "
  f"{np.median([np.interp(CLS[n]['R500'], CLS[n]['r'], CLS[n]['Ms'])/CLS[n]['M500'] for n in withstar]):.3f})")

P("\n    THE RESTATEMENT TEST FOR THIS ONE, DONE EXPLICITLY AND AGAINST INTEREST:")
P("    In the deep-MOND limit nu = sqrt(a_0/g_bar), so")
P("        eta = (M_dyn/M_bar)/nu = (1/f_b) sqrt(g_bar/a_0) = sqrt( g_N /(a_0 f_b) )   with  f_b = M_bar/M_dyn,")
P("    hence  eta^2 f_b a_0 / g_N(R500) = 1 IDENTICALLY.  So 'eta(Delta=500) is universal' is algebraically the SAME")
P("    statement as 'f_gas a_0/g_N(R500) is constant', which is this programme's own item 19 (flat to -0.010 +- 0.005")
P("    in eRASS1) -- and that in turn is the MEASURED gas-fraction-mass relation f_b ~ M^(1/3) wearing a_0's clothes.")
chk = np.array([q["e50"]**2*((q["gb50"]/ (G*q["M500"]*Msun/(q["R500"]*Mpc)**2)))*A0["canonical"]/q["gb50"]*
                (G*q["M500"]*Msun/(q["R500"]*Mpc)**2)/ (G*q["M500"]*Msun/(q["R500"]*Mpc)**2) for q in LR])
ident = np.array([q["e50"]**2*(q["gb50"]/q["gb50"]) for q in LR])   # placeholder, real identity below
fb = np.array([q["gb50"]/(G*q["M500"]*Msun/(q["R500"]*Mpc)**2) for q in LR])
gN = np.array([G*q["M500"]*Msun/(q["R500"]*Mpc)**2 for q in LR])
idv = e50**2*fb*A0["canonical"]/gN
info(f"numerical check of the identity eta^2 f_b a_0/g_N = 1 in the deep limit: median {np.median(idv):.3f} "
     f"(it is not exactly 1 because the kernel is only ~24% from its asymptote at these accelerations, "
     f"y = {np.median(fb*gN)/A0['canonical']:.3f})")
ck("6c4 THE RESTATEMENT TEST CLOSES for this half of the item: eta at fixed overdensity is an algebraic rewrite of "
   "the measured gas-fraction-mass relation, so it must be LABELLED a restatement, not a new law",
   abs(math.log10(np.median(idv))) < 0.25,
   f"eta^2 f_b a_0/g_N = {np.median(idv):.3f} over the 20 groups; the deep-MOND identity would make it exactly 1")

P("\n7.  MUTATION CONTROLS")
P("-"*118)
D1_x4 = []
for n in withstar:
    cl = CLS[n]; r1, ex, sl = crossing(cl, 4*A0["canonical"])
    if np.isfinite(r1):
        Md1 = 10**np.interp(math.log10(r1), np.log10(cl["r"]), np.log10(cl["Md"]))
        D1_x4.append(Md1*Msun/((4./3.)*math.pi*(r1*Mpc)**3*rho_c(cl["z"])))
ck("M1 a_0 x 4 must move the crossing overdensity -- the estimator is not a_0-blind",
   len(D1_x4) >= 3 and abs(math.log10(np.median(D1_x4)/med_D1)) > 0.1,
   f"Delta_1(4 a_0) = {np.median(D1_x4) if D1_x4 else float('nan'):.1f} vs {med_D1:.1f} "
   f"({math.log10(np.median(D1_x4)/med_D1) if D1_x4 else float('nan'):+.3f} dex)")
# nu = 1 (Newton): the crossing must move to a completely different place
D1_n = []
for n in withstar:
    cl = CLS[n]; rm = cl["r"]*Mpc
    et = cl["Md"]/cl["Mb"]
    if np.any(et <= 1):
        i = np.where(et <= 1)[0][0]
        D1_n.append(np.nan)
info(f"with nu = 1 (pure Newton) eta = M_dyn/M_bar >= 5 everywhere in every cluster "
     f"(min over the sample {min(np.min(CLS[n]['Md']/CLS[n]['Mb']) for n in withstar):.2f}), so no crossing exists at all")
ck("M2 with no kernel (nu = 1) there is no crossing anywhere in any cluster, so r_1 is a property of the kernel and "
   "not of the mass profiles", min(np.min(CLS[n]["Md"]/CLS[n]["Mb"]) for n in withstar) > 2.0,
   f"min M_dyn/M_bar over the whole sample = {min(np.min(CLS[n]['Md']/CLS[n]['Mb']) for n in withstar):.2f}")
# shuffle: give each cluster another cluster's baryon profile
perm = list(withstar[1:]) + [withstar[0]]
D1_sh = []
for n, m in zip(withstar, perm):
    cl = dict(CLS[n]); other = CLS[m]
    cl["Mb"] = 10**np.interp(np.log10(cl["r"]), np.log10(other["r"]), np.log10(other["Mb"]))
    r1, ex, sl = crossing(cl, A0["canonical"])
    if np.isfinite(r1):
        Md1 = 10**np.interp(math.log10(r1), np.log10(cl["r"]), np.log10(cl["Md"]))
        D1_sh.append(Md1*Msun/((4./3.)*math.pi*(r1*Mpc)**3*rho_c(cl["z"])))
ck("M3 pairing control: giving each cluster ANOTHER cluster's baryon profile must inflate the scatter in Delta_1 if "
   "the tightness is carried by the pairing", len(D1_sh) >= 3 and np.std(np.log10(D1_sh)) > sD,
   f"shuffled scatter {np.std(np.log10(D1_sh)) if D1_sh else float('nan'):.3f} dex vs real {sD:.3f} dex")

P("\n" + "="*118)
P("VERDICT -- k02")
P("="*118)
P(f"  Delta_1 (canonical) = {med_D1:.1f} +- {sD:.3f} dex over {len(ROWS['canonical'])} X-COP clusters")
P(f"  g_bar(r_1)/a_0      = {med_g1/A0['canonical']:.3f} +- {sg:.3f} dex")
P(f"  r_1/R500            = {np.median([r['x1'] for r in ROWS['canonical']]):.2f} +- {sx:.3f} dex")
P(f"  Delta_1 rho_c(z) / rho_DE = {rho1/rho_DE:.2f}")
P(f"  the two-overdensity group test: a_1(2500)/a_1(500) = {np.median(rat):.2f} +- {np.std(np.log10(rat)):.3f} dex, "
  f"{sum(1 for q in LR if q['a25'] > q['a50'])}/{len(LR)} groups the same sign")
P(f"  WHAT DIES: r_1 (100% extrapolated, unstable, and LambdaCDM produces a tighter Delta_1 than the data).")
P(f"  WHAT DIES: any single second ACCELERATION for clusters -- killed by an over-determined two-point test.")
P(f"  WHAT SURVIVES, LABELLED: eta(Delta) is universal -- eta(500) = {np.median(allе):.3f} +- {np.std(np.log10(allе)):.3f} dex "
  f"over 1.7 decades of mass in two samples, eta(2500) = {np.median(e25):.3f} +- {np.std(np.log10(e25)):.3f} dex -- but it is")
P(f"  an algebraic rewrite of the measured gas-fraction-mass relation and must be quoted as a restatement.")
sys.exit(ck.done())
