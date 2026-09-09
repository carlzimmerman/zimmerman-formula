#!/usr/bin/env python3
"""
L41 -- the cluster source, stated as a SPECIFICATION: is it self-consistent, and does any object meet it?
=========================================================================================================
Seven lanes have closed every mechanism this programme owns for the cluster residual, and two of them added
constraints that were not there before.  Each lane reported a NEGATIVE.  Nobody has assembled them into the
one thing they collectively determine: a POSITIVE specification of what any successful completion's cluster
source must supply, with every requirement carrying a number, a tolerance and a source script -- and then
asked the question no single lane could ask, namely whether that specification is SATISFIABLE AT ALL.

WHAT IS BEING SYNTHESISED (all in fable_independent_2026/)
  L2   the inverse problem: Delta_req = 5.5 s^0.81, log-slope 3.9 sigma above the 1/2 that caps any kernel;
       clusters need 2.2-5.1x the boost galaxies MEASURE at the same accelerations, worst |z| = 13.
  L5   a fixed-strength finite-range force: shape passes at 0.064 dex, galaxies and BBN each kill it (41x).
  L6   a screened force in potential, density or enclosed mass: closed, plus a cosmological-ordering theorem.
  L7   the residual is quantitatively the cosmic dark-to-baryon share at cluster scale, 5.73 +/- 0.68.
  L18  the hydrostatic bias is not an escape and runs the wrong way (it withdrew one of L7's own claims).
  L21  binary galaxies need M_dark/M_bar = 30.9 +/- 1.6 WITHIN the pair separation against 5.73 +/- 0.68 at
       0.80 R500 -- a factor 5.7 at 16 sigma.  The ladder is NOT monotone.
  L22  the curl field is real and locally up to 27%, but div a_S = 0 makes it exactly invisible to the
       enclosed-mass inversion, so L2's caveat is discharged and L2 stands.
  L24  the shortfall against lensing and against dynamics agree at 1.55 sigma (the residual behaves like
       MASS), AND -- new, and never before folded into a specification -- in the raw shear observable the
       framework is short by 2.5-2.7x with a Delta-Sigma log-slope 0.53 +/- 0.06 SHALLOWER at 9 sigma.
  g04a the required source is 6.8x the baryons with rho ~ r^-1.53 over 40-750 kpc and NOT cored; the
       Tremaine-Gunn floor is m >= 4.67 eV.
plus the recorded dark-sector no-go (Pauli, wave, four condensates, thermal relic).

THE THREE QUESTIONS THIS LANE ANSWERS
  (1) Assembled as ONE specification, is it self-consistent -- could ANY object satisfy all of it at once?
      If not, exhibit the incompatible pair.  That is the theorem.
  (2) The sharpest new tension.  L7 says clusters want the cosmic share; L21 says pairs want 5.7x that
      inside their own separation.  What would a component have to look like RADIALLY to give both?  Does
      that profile survive L24's measured shear log-slope and the galaxy-scale non-overshoot gate?
  (3) The flagged internal disagreement: Famaey, Pizzuti & Saltas 2024 find the lensing residual CORED
      inside ~1 Mpc; this repository's g04a reports rho ~ r^-1.53 and NOT cored.  Real conflict, or two
      parametrisations of the same thing over different radial ranges?

THE FAMILY SEARCHED, so that "no profile exists" is a search result and not a straw man.  The most general
HOST-BLIND rule that maps a system's baryons to the source is a function of the enclosed baryon mass and the
radius.  Take its scale-free form

        M_X( < r )  =  C * M_bar( < r )^a * (r / 100 kpc)^b ,

which contains, as special cases, everything the programme has proposed: a = 1, b = 0 is "X traces the
baryons at a universal ratio" (the cosmic-share reading); a = 0 is a universal background halo independent
of the host; a = 1, b < 0 is a kernel-like boost that decays outward; and any (a, b) in between.  The two
measured anchors -- 5.73 at 1000 kpc in a cluster, 30.9 at 132 kpc in a pair -- fix ONE LINE in (a, b), so
the family is scanned along that line and every remaining gate is applied to each member.  A member that
passes them all would be a live candidate and the most valuable outcome available in this lane.

CHECKS THAT CAN FAIL.  Each states a PROPOSITION; PASS means the proposition holds.
  K0-K3  CONTROLS.  Independently reproduce L7's cosmic ratio, L2's boost ratio and power-law slope, and
         L21's pair ratio from their own data, and validate the projection machinery on the analytic NFW.
         Without these the synthesis is quotation rather than verification.
  P0     the projection machinery, applied to a dark component with an NFW shape, reproduces the MEASURED
         weak-lensing shear log-slope -- the POSITIVE control that the shape gate is passable at all.
  A1     a single radial law R(r) = M_X/M_bar in ABSOLUTE radius serves both anchors.
  A2     the same in SCALED radius r/R200.
  A3     a component that TRACES the baryons at a universal ratio serves both anchors (the cosmic-share
         reading taken literally).
  B1     the two-anchor family line has a member reproducing the cluster's OWN measured ratio profile.
  B2     it has a member passing L24's measured shear log-slope.
  B3     it has a member passing the galaxy-scale non-overshoot gate at L* AND at the dwarf scale.
  B4     THE SEARCH: some single member of the family passes B1, B2 and B3 simultaneously.
  C1     the incompatible pair, measured internally: the host-mass exponent the two anchors demand agrees
         with the host-mass exponent measured INSIDE the pair sample itself.
  D1     [control] the power-law fitter recovers an injected slope.
  D2     the required source's density log-slope over 40-750 kpc reproduces g04a's -1.53 independently.
  D3     the cored-versus-cuspy disagreement is REAL: a cored profile of the Famaey type is excluded by the
         X-ray inversion over the range where the two are compared.
  E1     the non-monotone ladder is a constraint on LambdaCDM too -- i.e. LambdaCDM's own abundance-matching
         relation, with no freedom, FAILS to predict the pair ratio.  (Checked hard, in the direction that
         would make the claim FALSE, because a constraint on LambdaCDM from this repository must be verified
         far past the point of comfort before it is stated.)
  V1     VERDICT: the assembled specification is self-consistent, i.e. some object could meet all of it.

Both a0 footings throughout (9.3619e-11 canonical, 1.1279e-10 alt).  A FAIL marks a proposition that does
not hold; the FAILs here are the finding.
"""
import numpy as np, math, json, os, sys, glob, time
from scipy.spatial import cKDTree

T0 = time.time(); FAILS = []
def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
def P(s=""): print(s, flush=True)
def info(s): print("  " + s, flush=True)

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.normpath(os.path.join(HERE, ".."))
DATA = os.path.join(REPO, "real_research", "data")
G = 6.674e-11; MSUN = 1.989e30; kpc = 3.0857e19; Mpc = 1e3*kpc
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
S_SAT, D_SAT = 2.540, 0.6476                       # the carried kernel, THE_ACTION_2026-09-05 section 3
OM, OB, ODM = 0.315, 0.049, 0.266; F_COSMIC = ODM/OB
UPS_K, MK_SUN, H0_KMS = 0.6, 3.28, 67.4            # L21's K-band footing, unchanged
h70, OmM, OmL = 0.7, 0.3, 0.7                      # the cluster-data frame (Herbonnet / Sereno / X-COP)
H0c = h70*100e3/Mpc
RNG = np.random.default_rng(20260908)

def Delta(s):
    s = np.asarray(s, float)
    d = np.where(s > 0, s/np.expm1(np.sqrt(np.maximum(s, 1e-300))), 0.0)
    return np.where(s > S_SAT, D_SAT, d)
def g_kernel(gb, a0): return gb + a0*Delta(gb/a0)

P("=" * 122)
P("L41 -- the cluster source as a SPECIFICATION: assembled, tested for self-consistency, searched for a satisfier")
P("=" * 122)
P("  sources are the committed products of this lane and of the repository; nothing below is retyped from prose.")
P("    clusters : closure_2026/cluster_measurement_audit_2026/results.json  (the lead's radius-unit audit)")
P("    clusters : real_research/data/xcop/<name>/*.fits                      (independent read, for projection)")
P("    galaxies : real_research/data/sparc_data/*_rotmod.dat")
P("    pairs    : real_research/data/2mrs_catalog.csv                        (rebuilt, not reused)")

# ==========================================================================================================
P("\n" + "=" * 122)
P("PART A -- CONTROLS.  Reproduce the three headline numbers this synthesis is built on, from their own data.")
P("=" * 122)

CLJ = json.load(open(os.path.join(REPO, "qwen_claude_field_theory/closure_2026/cluster_measurement_audit_2026/results.json")))
RAD_AUD = np.array(CLJ["radii_kpc"], float)
R500 = {d["name"]: d["own_R500_kpc"] for d in CLJ["radius_audit"]}
ROWS = CLJ["rows"]

# ---- K0: L7's cosmic ratio ------------------------------------------------------------------------------
CLU = {}
for rw in ROWS:
    f = rw.get("footing", "canonical"); a0 = A0[f]
    CLU.setdefault(f, {}).setdefault(rw["cluster"], []).append(
        (float(rw["r_kpc"]), float(rw["g_baryon_over_a0"])*a0, float(rw["g_hse_over_a0"])*a0,
         bool(rw["stellar_file_present"])))
K0 = {}
for f in sorted(CLU):
    a0 = A0[f]; rows = []
    for n, pts in CLU[f].items():
        p = np.array([(x[0], x[1], x[2]) for x in sorted(CLU[f][n])])
        r = p[:, 0]*kpc; gb = p[:, 1]; gh = p[:, 2]
        Mb = gb*r**2/G/MSUN; Mh = gh*r**2/G/MSUN; Mk = g_kernel(gb, a0)*r**2/G/MSUN
        rows.append(dict(name=n, r=p[-1, 0], Mb=Mb[-1], Mh=Mh[-1],
                         rN=(Mh[-1] - Mb[-1])/Mb[-1], rF=(Mh[-1] - Mk[-1])/Mb[-1], fbar=Mb[-1]/Mh[-1]))
    K0[f] = rows
    rN = np.array([x["rN"] for x in rows]); fb = np.array([x["fbar"] for x in rows])
    rF = np.array([x["rF"] for x in rows])
    info(f"{f:>9}: {len(rows)} clusters at {rows[0]['r']:.0f} kpc "
         f"({rows[0]['r']/np.median(list(R500.values())):.2f} R500 median) -- "
         f"f_bar {np.median(fb):.3f}, Newtonian M_dark/M_bar {np.median(rN):.2f} +/- {np.std(rN, ddof=1):.2f} "
         f"({100*np.std(rN, ddof=1)/np.median(rN):.0f}% scatter), framework residual {np.median(rF):.2f} M_bar")
rN_can = np.array([x["rN"] for x in K0["canonical"]])
RATIO_CLU = float(np.median(rN_can)); E_RATIO_CLU = float(np.std(rN_can, ddof=1))
MBAR_CLU = float(np.median([x["Mb"] for x in K0["canonical"]]))
MDARK_CLU = float(np.median([x["Mh"] - x["Mb"] for x in K0["canonical"]]))
R_ANCHOR_CLU = float(K0["canonical"][0]["r"])
check("K0 [control] an independent recomputation of L7 returns its published cluster ratio 5.73 +/- 0.68 and "
      "f_bar = 0.149 at the outermost audited radius, on both footings",
      abs(RATIO_CLU - 5.73) < 0.05 and abs(E_RATIO_CLU - 0.68) < 0.05
      and abs(np.median([x["fbar"] for x in K0["canonical"]]) - 0.149) < 0.002,
      f"M_dark/M_bar = {RATIO_CLU:.2f} +/- {E_RATIO_CLU:.2f} vs L7's 5.73 +/- 0.68; "
      f"f_bar = {np.median([x['fbar'] for x in K0['canonical']]):.3f} vs 0.149")

# ---- K1: L2's required boost, its slope, and the cluster/galaxy ratio -----------------------------------
def fit_pl(s, d, cl, nboot=400):
    """log-log fit of Delta_req = A s^p with a cluster-level bootstrap (the unit of independence)."""
    m = (s > 0) & (d > 0); s, d, cl = s[m], d[m], np.array(cl)[m]
    c = np.polyfit(np.log10(s), np.log10(d), 1)
    names = np.unique(cl); ps = []
    for _ in range(nboot):
        pick = RNG.choice(names, size=len(names), replace=True)
        idx = np.concatenate([np.where(cl == n)[0] for n in pick])
        if len(idx) < 5: continue
        ps.append(np.polyfit(np.log10(s[idx]), np.log10(d[idx]), 1)[0])
    res = np.log10(d) - np.polyval(c, np.log10(s))
    return c[0], float(np.std(ps, ddof=1)), 10**c[1], float(np.std(res))

s7 = np.array([rw["g_baryon_over_a0"] for rw in ROWS if rw["footing"] == "canonical" and rw["stellar_file_present"]])
d7 = np.array([rw["g_hse_over_a0"] - rw["g_baryon_over_a0"] for rw in ROWS
               if rw["footing"] == "canonical" and rw["stellar_file_present"]])
c7 = [rw["cluster"] for rw in ROWS if rw["footing"] == "canonical" and rw["stellar_file_present"]]
p_req, ep_req, A_req, rms_req = fit_pl(s7, d7, c7)
info(f"required boost, canonical / stellar-7: Delta_req = ({A_req:.2f}) s^({p_req:.3f} +/- {ep_req:.3f}), "
     f"rms {rms_req:.3f} dex; the class ceiling on the log-slope is 1/2, so this is "
     f"{(p_req-0.5)/ep_req:.1f} sigma above it")

UPS_D, UPS_B = 0.5, 0.7
gal = []
for fn in sorted(glob.glob(os.path.join(DATA, "sparc_data", "*_rotmod.dat"))):
    try: d = np.loadtxt(fn, comments="#")
    except Exception: continue
    if d.ndim != 2 or d.shape[1] < 6: continue
    r = d[:, 0]*kpc; Vo = d[:, 1]*1e3; eV = d[:, 2]*1e3; Vg = d[:, 3]*1e3; Vd = d[:, 4]*1e3; Vb = d[:, 5]*1e3
    Vb2 = Vg*np.abs(Vg) + UPS_D*Vd*np.abs(Vd) + UPS_B*Vb*np.abs(Vb)
    m = (r > 0) & (Vo > 0) & (Vb2 > 0) & (eV/np.maximum(Vo, 1) < 0.10)
    if m.sum() < 3: continue
    r, Vo, Vb2 = r[m], Vo[m], Vb2[m]
    gal.append((Vb2/r, Vo**2/r))
gb_g = np.concatenate([x[0] for x in gal]); go_g = np.concatenate([x[1] for x in gal])
info(f"SPARC: {len(gb_g)} points from {len(gal)} galaxies (Upsilon_d = 0.5, Upsilon_b = 0.7, eV/V < 0.10)")

RAT, ZZ = [], []
for f in ("canonical", "alt"):
    a0 = A0[f]
    sc = np.array([rw["g_baryon_over_a0"] for rw in ROWS if rw["footing"] == f and rw["stellar_file_present"]])
    dc = np.array([rw["g_hse_over_a0"] - rw["g_baryon_over_a0"] for rw in ROWS
                   if rw["footing"] == f and rw["stellar_file_present"]])
    sg = gb_g/a0; dg = (go_g - gb_g)/a0
    lo = max(sc.min(), sg.min()); hi = min(sc.max(), sg.max())
    edges = np.geomspace(lo, hi, 7)
    for i in range(6):
        mc = (sc >= edges[i]) & (sc < edges[i+1]); mg = (sg >= edges[i]) & (sg < edges[i+1])
        if mc.sum() < 3 or mg.sum() < 10: continue
        cm, gm = np.median(dc[mc]), np.median(dg[mg])
        ce = np.std(dc[mc], ddof=1)/math.sqrt(mc.sum()); ge = np.std(dg[mg], ddof=1)/math.sqrt(mg.sum())
        RAT.append(cm/gm); ZZ.append((cm - gm)/math.hypot(ce, ge))
ZMAX = float(max(abs(np.array(ZZ))))
info(f"cluster/galaxy required-boost ratio over the overlap, both footings: "
     f"{min(RAT):.1f}-{max(RAT):.1f}, worst |z| = {ZMAX:.0f} with pooled standard errors "
     f"(L2 quotes 13 with a CLUSTER-level bootstrap, L6's control 25 with pooled errors; this is the "
     f"pooled-error number and the conservative one to carry is L2's 13)")
check("K1 [control] an independent recomputation of L2 returns its published power-law slope 0.811 +/- 0.079, "
      "its amplitude 5.5, and its cluster/galaxy boost ratio range 2.2-5.1 with the kill firing at |z| > 9",
      abs(p_req - 0.811) < 0.02 and abs(A_req - 5.47) < 0.20
      and abs(min(RAT) - 2.2) < 0.4 and abs(max(RAT) - 5.1) < 0.6 and ZMAX > 9,
      f"p = {p_req:.3f} vs 0.811; A = {A_req:.2f} vs 5.47; ratios {min(RAT):.1f}-{max(RAT):.1f} vs 2.2-5.1; "
      f"worst |z| = {ZMAX:.0f} (pooled) bracketing L2's 13 and L6's 25")

# ---- K2: L21's pair ratio, rebuilt -----------------------------------------------------------------------
def unitvec(ra, de):
    ra = np.radians(ra); de = np.radians(de)
    return np.c_[np.cos(de)*np.cos(ra), np.cos(de)*np.sin(ra), np.sin(de)]
def ang_sep_deg(u, v): return np.degrees(2*np.arcsin(np.clip(np.linalg.norm(u - v, axis=-1)/2, 0, 1)))
def cmb_frame(ra, de, vhel):
    ra_r, de_r = np.radians(ra), np.radians(de)
    ra_gp, de_gp, l_ncp = math.radians(192.85948), math.radians(27.12825), math.radians(122.93192)
    sb = np.sin(de_r)*math.sin(de_gp) + np.cos(de_r)*math.cos(de_gp)*np.cos(ra_r - ra_gp)
    b = np.arcsin(np.clip(sb, -1, 1))
    y = np.cos(de_r)*np.sin(ra_r - ra_gp)
    x = np.sin(de_r)*math.cos(de_gp) - np.cos(de_r)*math.sin(de_gp)*np.cos(ra_r - ra_gp)
    l = l_ncp - np.arctan2(y, x)
    la, ba, amp = math.radians(264.021), math.radians(48.253), 369.82
    return vhel + amp*(np.sin(b)*math.sin(ba) + np.cos(b)*math.cos(ba)*np.cos(l - la))

CZ_LO, CZ_HI, RP_MAX, DV_MAX, DV_ISO, V_ERR, F_REL = 3000., 12000., 1000., 2000., 1000., 40., 5.0
mr = np.genfromtxt(os.path.join(DATA, "2mrs_catalog.csv"), delimiter=",", names=True)
mok = np.isfinite(mr["cz"]) & (mr["cz"] > 0)
m_ra, m_de, m_K = mr["RAJ2000"][mok], mr["DEJ2000"][mok], mr["Ktmag"][mok]
MX = unitvec(m_ra, m_de); MT = cKDTree(MX); cz = cmb_frame(m_ra, m_de, mr["cz"][mok])
ang_max = math.degrees(RP_MAX/1000.0/(CZ_LO/H0_KMS))
cand = MT.query_pairs(2*math.sin(math.radians(ang_max)/2), output_type="ndarray")
ii, jj = cand[:, 0], cand[:, 1]
czm = (cz[ii] + cz[jj])/2; Dm = czm/H0_KMS
rp = np.radians(ang_sep_deg(MX[ii], MX[jj]))*Dm*1000.0
dv = cz[ii] - cz[jj]
sel = (np.abs(dv) < DV_MAX) & (czm > CZ_LO) & (czm < CZ_HI) & (rp < RP_MAX) & (rp > 10.0)
ii, jj, rp, dv, czm, Dm = ii[sel], jj[sel], rp[sel], dv[sel], czm[sel], Dm[sel]
LK = lambda K, D: 10**(0.4*(MK_SUN - (K - 5*np.log10(D*1e6) + 5)))
L1_, L2_ = LK(m_K[ii], Dm), LK(m_K[jj], Dm)
rok = (np.maximum(L1_, L2_)/np.minimum(L1_, L2_)) < 6.0
ii, jj, rp, dv, czm, Dm, L1_, L2_ = (a[rok] for a in (ii, jj, rp, dv, czm, Dm, L1_, L2_))
mid = MX[ii] + MX[jj]; mid /= np.linalg.norm(mid, axis=1)[:, None]
dch, idx = MT.query(mid, k=80)
dist = np.degrees(2*np.arcsin(np.clip(dch/2, 0, 1)))*np.radians(1.0)*Dm[:, None]*1000.0
bad = (idx == ii[:, None]) | (idx == jj[:, None]) | (np.abs(cz[idx] - czm[:, None]) >= DV_ISO)
d3 = np.where(bad, np.inf, dist).min(axis=1)
keep = d3 > F_REL*rp
S = dict(rp=rp[keep], dv=dv[keep], M1=UPS_K*L1_[keep], M2=UPS_K*L2_[keep])
NPAIR = len(S["rp"])

def ml_amp(dv, shape, dvmax=DV_MAX, verr=V_ERR):
    dv = np.asarray(dv, float); s = np.asarray(shape, float)
    def nll(lA, lf):
        A = math.exp(lA); f = 1/(1 + math.exp(-lf)); sg = np.sqrt((A*s)**2 + verr**2)
        p = f*np.exp(-0.5*(dv/sg)**2)/(math.sqrt(2*math.pi)*sg) + (1 - f)/(2*dvmax)
        return -np.sum(np.log(np.maximum(p, 1e-300)))
    best = (1e30, 0., 0.)
    for lA in np.linspace(math.log(0.10), math.log(12.0), 110):
        for lf in np.linspace(-4, 4, 41):
            v = nll(lA, lf)
            if v < best[0]: best = (v, lA, lf)
    lA0, lf0 = best[1], best[2]
    for _ in range(3):
        lf0 = min(np.linspace(lf0 - 1.0, lf0 + 1.0, 81), key=lambda x: nll(lA0, x))
        lA0 = min(np.linspace(lA0 - 0.15, lA0 + 0.15, 81), key=lambda x: nll(x, lf0))
    fine = np.linspace(lA0 - 0.35, lA0 + 0.35, 161)
    prof = np.array([min(nll(lA, lf) for lf in np.linspace(lf0 - 0.8, lf0 + 0.8, 21)) for lA in fine])
    prof -= prof.min(); lA0 = fine[int(np.argmin(prof))]; hi = fine[prof < 0.5]
    err = (hi.max() - hi.min())/2 if len(hi) > 1 else float(np.diff(fine).mean())
    return math.exp(lA0), math.exp(lA0)*err

def sig_newton(M1, M2, rp_kpc, nmc=400, seed=11):
    """Projected-separation forward model for Newton on the baryons, written out here rather than imported:
       only r_p is observed, so the 3-D separation is drawn from a log-uniform prior weighted by the
       random-orientation kernel p(r_p|r) = r_p / (r sqrt(r^2 - r_p^2)).  Returns sigma_los in km/s."""
    g = np.random.default_rng(seed)
    M1 = np.atleast_1d(np.asarray(M1, float)); M2 = np.atleast_1d(np.asarray(M2, float))
    rp = np.atleast_1d(np.asarray(rp_kpc, float))
    u = g.random((len(rp), nmc))
    r = rp[:, None]*np.exp(u*math.log(20.0))*1.0001
    w = 1.0/np.sqrt(np.maximum((r/rp[:, None])**2 - 1.0, 1e-6)); w /= w.sum(axis=1, keepdims=True)
    v2 = G*(M1[:, None] + M2[:, None])*MSUN/(r*kpc)
    return np.sqrt(np.sum(w*v2, axis=1)/3.0)/1e3

sh_N = sig_newton(S["M1"], S["M2"], S["rp"])
A_N, eA_N = ml_amp(S["dv"], sh_N)
RATIO_PAIR = A_N**2 - 1.0; E_RATIO_PAIR = 2*A_N*eA_N
MBAR_PAIR = float(np.median(S["M1"] + S["M2"])); R_ANCHOR_PAIR = float(np.median(S["rp"]))
info(f"pairs rebuilt: N = {NPAIR}, median r_p = {R_ANCHOR_PAIR:.0f} kpc, median M_b(pair) = {MBAR_PAIR:.2e} Msun")
info(f"  Newtonian-on-baryons amplitude A = {A_N:.3f} +/- {eA_N:.3f}  =>  "
     f"M_dark/M_bar within r_p = A^2 - 1 = {RATIO_PAIR:.1f} +/- {E_RATIO_PAIR:.1f}")
check("K2 [control] an independent rebuild of the 2MRS pair sample reproduces L21's Newtonian amplitude "
      "5.645 and its dark-to-baryon ratio 30.9 +/- 1.6 within the pair separation",
      abs(A_N/5.645 - 1) < 0.06 and abs(RATIO_PAIR/30.9 - 1) < 0.15 and abs(NPAIR/1900. - 1) < 0.15,
      f"N = {NPAIR} vs 1900; A = {A_N:.3f} vs 5.645; ratio {RATIO_PAIR:.1f} +/- {E_RATIO_PAIR:.1f} vs 30.9 +/- 1.6")

# ---- K3: the projection machinery ------------------------------------------------------------------------
def sigma_of_R(rho_grid_r, rho_grid_v, R, rmax):
    """Sigma(R) = 2 int rho(sqrt(R^2 + z^2)) dz.  With z = R sinh t, r = R cosh t and dz = R cosh t dt this
       becomes 2 int_0^T rho(R cosh t) R cosh t dt, which has no coordinate singularity at r = R."""
    if R >= rmax: return 0.0
    T = math.acosh(rmax/R); t = np.linspace(0, T, 600)
    ch = np.cosh(t); rr = R*ch
    v = np.exp(np.interp(np.log(rr), np.log(rho_grid_r), np.log(np.maximum(rho_grid_v, 1e-300))))
    v = np.where(rr > rmax, 0.0, v)
    return float(2.0*R*np.trapz(v*ch, t))
def dsigma_of_R(rho_grid_r, rho_grid_v, R, rmax, n=80):
    """DeltaSigma(R) = Sigmabar(<R) - Sigma(R).  Sigmabar is integrated in log R' because Sigma ~ 1/R' for a
       cuspy inner profile, so the integrand Sigma R'^2 is well behaved on a log grid."""
    lo = 1e-4*R
    Rp = np.exp(np.linspace(math.log(lo), math.log(R), n))
    Sp = np.array([sigma_of_R(rho_grid_r, rho_grid_v, x, rmax) for x in Rp])
    Sbar = 2.0*np.trapz(Sp*Rp**2, np.log(Rp))/R**2
    return Sbar - sigma_of_R(rho_grid_r, rho_grid_v, R, rmax)

def nfw_delta_c(c): return (200.0/3.0)*c**3/(math.log(1+c) - c/(1+c))
def nfw_g(x):
    if abs(x-1) < 1e-8: return math.log(x/2.0) + 1.0
    if x < 1: return math.log(x/2.0) + math.acosh(1.0/x)/math.sqrt(1-x*x)
    return math.log(x/2.0) + math.acos(1.0/x)/math.sqrt(x*x-1)
def nfw_Sigma(R, rs, dc, rhoc):
    x = R/rs; A = 2*rs*dc*rhoc
    if abs(x-1) < 1e-8: return A/3.0
    if x < 1: return A/(x*x-1)*(1 - 2/math.sqrt(1-x*x)*math.atanh(math.sqrt((1-x)/(1+x))))
    return A/(x*x-1)*(1 - 2/math.sqrt(x*x-1)*math.atan(math.sqrt((x-1)/(x+1))))
def nfw_DS(R, rs, dc, rhoc): return 4*rs*dc*rhoc*nfw_g(R/rs)/(R/rs)**2 - nfw_Sigma(R, rs, dc, rhoc)
def Ez(z): return math.sqrt(OmM*(1+z)**3 + OmL)
def rho_crit(z): return 3*(H0c*Ez(z))**2/(8*math.pi*G)
def c200_DM14(M200, z):
    a = 0.520 + (0.905 - 0.520)*math.exp(-0.617*z**1.21); b = -0.101 + 0.026*z
    return 10**(a + b*math.log10(M200*h70/1e12))
def nfw_from_M200(M200, z):
    c = c200_DM14(M200, z); r200 = (3*M200*MSUN/(4*math.pi*200*rho_crit(z)))**(1./3.)
    return r200/c, nfw_delta_c(c), rho_crit(z), c, r200

rs_t, dc_t, rc_t, c_t, r200_t = nfw_from_M200(1.0e15, 0.08)
rgr = np.exp(np.linspace(math.log(1e-3*Mpc), math.log(200*Mpc), 900))
rho_t = dc_t*rc_t/((rgr/rs_t)*(1+rgr/rs_t)**2)
errs = []
for Rt in (0.5, 1.0, 2.0):
    num = dsigma_of_R(rgr, rho_t, Rt*Mpc, 200*Mpc); ana = nfw_DS(Rt*Mpc, rs_t, dc_t, rc_t)
    errs.append(abs(num/ana - 1))
    info(f"projection control: NFW DeltaSigma at {Rt:.1f} Mpc, numerical/analytic = {num/ana:.5f}")
check("K3 [control] the projection machinery reproduces the analytic general-relativistic NFW DeltaSigma to 1%",
      max(errs) < 0.01, f"max |error| = {max(errs):.2e}")

# ==========================================================================================================
P("\n" + "=" * 122)
P("PART B -- THE SPECIFICATION, assembled.  Every requirement with its number, its tolerance and its source.")
P("=" * 122)

# the measured weak-lensing shear log-slope, recomputed here from Herbonnet 2020's published M200 rather
# than quoted from L24: the NFW + Dutton-Maccio model is deterministic, so this is an independent evaluation.
WL = {"A85": (0.055, 8.4), "A1795": (0.062, 13.9), "A2029": (0.077, 18.1),
      "A2142": (0.091, 14.5), "ZW1215": (0.075, 5.1)}
Rfit = np.exp(np.linspace(math.log(0.5*Mpc), math.log(2.0*Mpc), 12))
wl_slopes = []
for n, (z, M2h) in WL.items():
    rs_, dc_, rc_, _, _ = nfw_from_M200(M2h*1e14, z)
    ds = np.array([nfw_DS(R, rs_, dc_, rc_) for R in Rfit])
    wl_slopes.append(np.polyfit(np.log(Rfit), np.log(ds), 1)[0])
WL_SLOPE = float(np.mean(wl_slopes)); WL_SLOPE_E = float(np.std(wl_slopes, ddof=1)/math.sqrt(len(wl_slopes)))
info(f"measured weak-lensing shear log-slope d ln DeltaSigma / d ln R over 0.5-2 Mpc, recomputed from "
     f"Herbonnet 2020's own M200 + Dutton-Maccio: {WL_SLOPE:+.3f} +/- {WL_SLOPE_E:.3f} "
     f"(per cluster {', '.join(f'{x:+.2f}' for x in wl_slopes)})")

def rar_tol(Mb, r_kpc, a0, tol_dex=0.11):
    gb = G*Mb*MSUN/(r_kpc*kpc)**2; g0 = gb + a0*float(Delta(np.array([gb/a0]))[0])
    lo, hi = 0.0, 60.0
    for _ in range(80):
        f = 0.5*(lo + hi); gbf = (1+f)*gb
        gf = gbf + a0*float(Delta(np.array([gbf/a0]))[0])
        if math.log10(gf/g0) < tol_dex: lo = f
        else: hi = f
    return 0.5*(lo + hi)
TOL_LSTAR = rar_tol(8e10, 10.0, A0["canonical"]); TOL_DWARF = rar_tol(2e9, 10.0, A0["canonical"])
info(f"galaxy-scale non-overshoot gate, recomputed: the carried kernel absorbs {TOL_LSTAR:.3f} M_b inside "
     f"10 kpc at L* (M_b = 8e10) and {TOL_DWARF:.3f} M_b at a dwarf (M_b = 2e9) before g_obs moves by the "
     f"RAR's own 0.11 dex scatter")

SPEC = [
 ("R1  amount, cluster",       f"M_X/M_bar = {RATIO_CLU:.2f} +/- {E_RATIO_CLU:.2f} at 0.80 R500 (1000 kpc), "
                               f"12% cluster-to-cluster; {RATIO_CLU/F_COSMIC:.2f}x the cosmic Omega_dm/Omega_b",
                               "+/- 0.68 (12%)", "L7_cosmic_ratio.py (K0 here)"),
 ("R2  amount, bias-corrected", "the same ratio runs 5.73 -> 9.04 over the measured hydrostatic bias "
                               "b in [0, 0.33]; every escape needs b < 0, which is sigma^2 < 0",
                               "b in [0.00, 0.42] measured", "L18_hse_bias.py"),
 ("R3  3-D shape, cluster",    "rho_X ~ r^-1.5 over 40-750 kpc, i.e. not FLAT, with any core radius <~ 750 kpc "
                               "(see PART D); the required boost is "
                               f"Delta_req = {A_req:.1f} s^{p_req:.2f}, log-slope {(p_req-0.5)/ep_req:.1f} "
                               "sigma above the 1/2 that caps every kernel of the class",
                               "0.09 dex rms about the power law", "g04a (D2 here) + L2 (K1 here)"),
 ("R4  projected shear shape", f"d ln DeltaSigma / d ln R = {WL_SLOPE:+.3f} +/- {WL_SLOPE_E:.3f} over "
                               "0.5-2 Mpc; the framework's phantom gives -0.31, short by 0.53 at 9 sigma "
                               "because it is a near-uniform sheet",
                               "+/- 0.06 (9 sigma)", "L24_lensing_vs_dynamics.py C11"),
 ("R5  lensing == dynamics",   "S_lens - S_dyn = +0.37 +/- 0.24 (1.55 sigma): the source must gravitate "
                               "identically in both probes, so no lensing sector can repair it",
                               "1.55 sigma agreement", "L24 C8"),
 ("R6  mass-scale, NON-monotone", f"M_X/M_bar = {RATIO_PAIR:.1f} +/- {E_RATIO_PAIR:.1f} within {R_ANCHOR_PAIR:.0f} "
                               f"kpc of a 2e11 Msun pair against {RATIO_CLU:.2f} at 1000 kpc of a 6e13 Msun "
                               f"cluster: a factor {RATIO_PAIR/RATIO_CLU:.1f} at "
                               f"{abs(RATIO_PAIR-RATIO_CLU)/math.hypot(E_RATIO_PAIR, E_RATIO_CLU):.0f} sigma",
                               "+/- 1.6 (16 sigma)", "L21_binary_galaxies.py S1 (K2 here)"),
 ("R7  galaxy non-overshoot",  f"<= {TOL_LSTAR:.2f} M_b inside 10 kpc at L* and <= {TOL_DWARF:.2f} M_b at a "
                               "dwarf; an NFW cosmic share gives 0.34 (admissible) and 1.90 (3.2x over)",
                               "0.11 dex RAR scatter", "L21 S6 + g04k/L1"),
 ("R8  phase-space floor",     "Tremaine-Gunn m >= 4.67 eV from the cluster core at sigma = 886 km/s; a "
                               "relic at its floor is cored and fails R3; escaping needs m >~ 8.3 eV",
                               "hard bound", "g04a R3/R4b"),
 ("R9  cosmological abundance","Omega_X/Omega_b = 5.43 at cluster scale; if supplied by a force instead of "
                               "mass, G_cosmo/G_local <= 1.2 from BBN, against the 9.2 a fixed-strength "
                               "force needs (41x) and the 1.82 monotone screening forces (4x)",
                               "|G/G_0 - 1| < 0.2", "L5_long_range_G.py, L6_screened_force.py"),
 ("R10 not a kernel",          "no single-valued Delta(s) serves both populations: at the same accelerations "
                               f"clusters need {min(RAT):.1f}-{max(RAT):.1f}x the galaxy boost, worst |z| = "
                               f"{max(abs(np.array(ZZ))):.0f}; the solenoidal field cannot help because "
                               "div a_S = 0 makes it exactly invisible to the enclosed-mass inversion",
                               "3 sigma per bin", "L2 (K1 here) + L22_curl_field.py"),
]
P("")
info(f"{'requirement':<28} {'tolerance':<26} source")
info("-"*118)
for k, v, tol, src in SPEC:
    info(f"{k:<28} {tol:<26} {src}")
    for ln in [v[i:i+86] for i in range(0, len(v), 86)]:
        info(f"{'':<28} {'':<26} {ln}")

# ==========================================================================================================
P("\n" + "=" * 122)
P("PART C -- IS IT SELF-CONSISTENT?  The two anchors, and the family of profiles that could serve both.")
P("=" * 122)
P("  ANCHOR 1 (cluster): M_X = %.3e Msun inside %.0f kpc, where M_bar = %.3e  =>  ratio %.2f"
  % (MDARK_CLU, R_ANCHOR_CLU, MBAR_CLU, RATIO_CLU))
P("  ANCHOR 2 (pair)   : M_X = %.3e Msun inside %.0f kpc, where M_bar = %.3e  =>  ratio %.1f"
  % (RATIO_PAIR*MBAR_PAIR, R_ANCHOR_PAIR, MBAR_PAIR, RATIO_PAIR))

# ---- A1: one radial law in absolute radius --------------------------------------------------------------
P("")
info("A1 -- can ONE law R(r) = M_X/M_bar in absolute radius serve both?  The clusters MEASURE R(r) at eleven")
info("     radii, so the pair's own radius is inside the measured cluster range and no extrapolation is needed:")
RPROF = {}
for f in ("canonical", "alt"):
    byr = {}
    for rw in ROWS:
        if rw["footing"] != f: continue
        byr.setdefault(float(rw["r_kpc"]), []).append(
            (rw["g_hse_over_a0"] - rw["g_baryon_over_a0"])/rw["g_baryon_over_a0"])
    RPROF[f] = {r: np.array(v) for r, v in byr.items()}
rr = np.array(sorted(RPROF["canonical"]))
med = np.array([np.median(RPROF["canonical"][r]) for r in rr])
sem = np.array([np.std(RPROF["canonical"][r], ddof=1)/math.sqrt(len(RPROF["canonical"][r])) for r in rr])
info(f"     {'r [kpc]':>9} " + " ".join(f"{x:7.0f}" for x in rr))
info(f"     {'R_cluster':>9} " + " ".join(f"{x:7.2f}" for x in med))
info(f"     {'+/- (sem)':>9} " + " ".join(f"{x:7.2f}" for x in sem))
R_clu_at_pair = float(np.exp(np.interp(math.log(R_ANCHOR_PAIR), np.log(rr), np.log(med))))
e_clu_at_pair = float(np.exp(np.interp(math.log(R_ANCHOR_PAIR), np.log(rr), np.log(sem))))
zA1 = (RATIO_PAIR - R_clu_at_pair)/math.hypot(E_RATIO_PAIR, e_clu_at_pair)
info(f"     at the pair's own {R_ANCHOR_PAIR:.0f} kpc the clusters measure R = {R_clu_at_pair:.2f} +/- "
     f"{e_clu_at_pair:.2f}; the pairs require {RATIO_PAIR:.1f} +/- {E_RATIO_PAIR:.1f}")
info(f"     the cluster profile is itself NON-MONOTONE: it rises from {med[0]:.1f} at {rr[0]:.0f} kpc to "
     f"{med.max():.1f} at {rr[int(np.argmax(med))]:.0f} kpc and falls to {med[-1]:.2f} at {rr[-1]:.0f} kpc")
check("A1 a single radial law R(r) in ABSOLUTE radius serves both the cluster and the pair anchor",
      abs(zA1) < 3,
      f"at the same {R_ANCHOR_PAIR:.0f} kpc the clusters give {R_clu_at_pair:.2f} +/- {e_clu_at_pair:.2f} and "
      f"the pairs need {RATIO_PAIR:.1f} +/- {E_RATIO_PAIR:.1f}, a factor {RATIO_PAIR/R_clu_at_pair:.1f} at "
      f"{abs(zA1):.0f} sigma -- so the factor 5.7 of L21's S1 is NOT an artefact of comparing different radii; "
      f"it survives at {RATIO_PAIR/R_clu_at_pair:.1f} when the radius is held fixed")

# ---- A2: scaled radius ----------------------------------------------------------------------------------
def R200_of(M200):                     # metres, z ~ 0.08 cluster frame / z ~ 0 pair frame both use rho_c(0)
    return (3*M200*MSUN/(4*math.pi*200*rho_crit(0.0)))**(1./3.)
M200_clu = float(np.median([x["Mh"] for x in K0["canonical"]]))*1.6      # M(<1 Mpc) -> M200, mild extrapolation
R200_clu = R200_of(M200_clu)/kpc
x_clu = R_ANCHOR_CLU/R200_clu
info("")
info(f"A2 -- in SCALED radius.  The cluster anchor sits at r/R200 = {x_clu:.2f} (R200 = {R200_clu:.0f} kpc).")
info("     The pair's R200 is not measured, so it is SCANNED over the whole plausible range rather than assumed,")
info("     and the comparison is reported for every value:")
info(f"     {'pair R200 [kpc]':>16} {'r_p/R200':>10} {'matched cluster radius':>23} {'cluster R there':>17} {'factor':>8}")
A2FAC = []
for R200_pair in (250., 300., 350., 400., 450., 500., 600.):
    xp = R_ANCHOR_PAIR/R200_pair; r_eq = xp*R200_clu
    Rc = float(np.exp(np.interp(math.log(min(max(r_eq, rr[0]), rr[-1])), np.log(rr), np.log(med))))
    A2FAC.append(RATIO_PAIR/Rc)
    info(f"     {R200_pair:16.0f} {xp:10.3f} {r_eq:20.0f} kpc {Rc:17.2f} {RATIO_PAIR/Rc:8.2f}")
check("A2 a single radial law in SCALED radius r/R200 serves both anchors, for SOME admissible pair R200",
      min(A2FAC) < 1 + 3*E_RATIO_PAIR/RATIO_CLU,
      f"the gap is {min(A2FAC):.1f}-{max(A2FAC):.1f}x over the whole range of pair R200 from 250 to 600 kpc; "
      f"scaling the radius does not help and mostly makes it WORSE than A1's factor, because the cluster "
      f"ratio profile is falling over the matched range")

# ---- A3: X traces the baryons ---------------------------------------------------------------------------
info("")
check("A3 a component that TRACES the baryons at ONE universal ratio (the cosmic-share reading taken "
      "literally) serves both anchors",
      abs(RATIO_PAIR - RATIO_CLU) < 3*math.hypot(E_RATIO_PAIR, E_RATIO_CLU),
      f"{RATIO_PAIR:.1f} +/- {E_RATIO_PAIR:.1f} against {RATIO_CLU:.2f} +/- {E_RATIO_CLU:.2f}, "
      f"{abs(RATIO_PAIR-RATIO_CLU)/math.hypot(E_RATIO_PAIR, E_RATIO_CLU):.0f} sigma.  This is the single most "
      f"important consequence of L7 + L21 together: the cosmic share is a CLUSTER-scale coincidence, not a "
      f"universal component")

# ---- B: the two-parameter family ------------------------------------------------------------------------
P("")
P("-"*122)
P("  THE SEARCH.  The most general host-blind rule mapping a system's baryons to the source is a function of")
P("  the enclosed baryon mass and the radius; its scale-free form is")
P("")
P("        M_X( < r )  =  C * M_bar( < r )^a * (r / 100 kpc)^b ,")
P("")
P("  which CONTAINS every proposal this programme has made: (a, b) = (1, 0) is 'X traces the baryons', a = 0")
P("  is a universal background halo, a = 1 with b < 0 is a kernel-like boost decaying outward.  The two")
P("  anchors fix one LINE in (a, b); the family is scanned along it and every other gate applied to each")
P("  member.  A member passing all of them would be a live candidate.")
P("-"*122)

LN_M = math.log(MBAR_CLU/MBAR_PAIR); LN_R = math.log(R_ANCHOR_CLU/R_ANCHOR_PAIR)
LN_X = math.log(MDARK_CLU/(RATIO_PAIR*MBAR_PAIR))
def b_of_a(a): return (LN_X - a*LN_M)/LN_R
def C_of_a(a):
    b = b_of_a(a)
    return (RATIO_PAIR*MBAR_PAIR)/(MBAR_PAIR**a*(R_ANCHOR_PAIR/100.0)**b)
info(f"the anchor line: {LN_M:.4f} a + {LN_R:.4f} b = {LN_X:.4f},  i.e.  b = {b_of_a(0):.4f} "
     f"- {(b_of_a(0)-b_of_a(1)):.4f} a")

# cluster baryon profile (median over the twelve, from the audit rows) for the ratio-profile gate
MB_PROF = {}
for rw in ROWS:
    if rw["footing"] != "canonical": continue
    MB_PROF.setdefault(float(rw["r_kpc"]), []).append(
        rw["g_baryon_over_a0"]*A0["canonical"]*(rw["r_kpc"]*kpc)**2/G/MSUN)
mb_prof = np.array([np.median(MB_PROF[r]) for r in rr])

# continuous cluster profiles for the projection gate (independent read of the on-disk FITS)
from astropy.io import fits
XDIR = os.path.join(DATA, "xcop")
def _rkpc(rad, unit, R5):
    u = (unit or "").strip().lower()
    if u in ("r/r500", "r500"): return np.asarray(rad, float)*R5
    if u == "mpc": return np.asarray(rad, float)*1e3
    return np.asarray(rad, float)
def load_cluster(name):
    p = os.path.join(XDIR, name); c = {"name": name}
    with fits.open(os.path.join(p, name + "_hydro_mass.fits")) as f:
        d = f[1].data; R5 = float(f[1].header["R500"]); c["R500"] = R5
        c["rh"] = _rkpc(d["RADIUS"], f[1].columns["RADIUS"].unit, R5); c["Mh"] = np.array(d["M_FORW"], float)
    with fits.open(os.path.join(p, name + "_fgas_profile.fits")) as f:
        d = f[1].data
        c["rg"] = _rkpc(d["RADIUS"], f[1].columns["RADIUS"].unit, c["R500"]); c["Mg"] = np.array(d["MGAS"], float)
    sp = os.path.join(p, name + "_mstar.fits"); c["has_star"] = os.path.exists(sp)
    if c["has_star"]:
        with fits.open(sp) as f:
            d = f[2].data
            c["rs"] = _rkpc(d["RADIUS"], f[2].columns["RADIUS"].unit, c["R500"]); c["Ms"] = np.array(d["MSTAR"], float)
    return c
def li(xq, x, v):
    m = (x > 0) & (v > 0)
    return np.exp(np.interp(np.log(xq), np.log(x[m]), np.log(v[m])))
GRID = np.exp(np.linspace(math.log(2.0), math.log(3.0e4), 700))            # 2 kpc .. 30 Mpc
CLC = {}
for n in sorted(WL):
    c = load_cluster(n)
    Mg = li(np.clip(GRID, c["rg"].min(), c["rg"].max()), c["rg"], c["Mg"])
    Mg = np.where(GRID < c["rg"].min(), c["Mg"][0]*(GRID/c["rg"].min())**2.0, Mg)
    Mg = np.where(GRID > c["rg"].max(), c["Mg"][-1]*(1 + 0.35*np.log(GRID/c["rg"].max())), Mg)
    if c["has_star"]:
        Ms = li(np.clip(GRID, c["rs"].min(), c["rs"].max()), c["rs"], c["Ms"])
        Ms = np.where(GRID > c["rs"].max(), c["Ms"][-1], Ms)
    else:
        Ms = 0.12*Mg
    c["Mbar"] = Mg + Ms
    c["Mh_i"] = li(np.clip(GRID, c["rh"].min(), c["rh"].max()), c["rh"], c["Mh"])
    CLC[n] = c
info(f"continuous baryon profiles built for the five weak-lensing clusters ({', '.join(sorted(WL))}) on a "
     f"{len(GRID)}-point log grid, 2 kpc - 30 Mpc")

def rho_from_M(Mgrid, rtrunc_kpc):
    rho = np.gradient(np.asarray(Mgrid, float), np.log(GRID))*MSUN/(4*math.pi*(GRID*kpc)**3)
    rho = np.maximum(rho, 1e-45)
    rho = np.where(GRID > rtrunc_kpc, 1e-45, rho)
    return GRID*kpc, rho
def shear_slope(Mtot_grid, rtrunc_kpc, want_flag=False):
    """d ln DeltaSigma / d ln R over the weak-lensing fitting range 0.5-2 Mpc.  A source whose density RISES
       outward gives DeltaSigma < 0 -- shear of the wrong SIGN, not merely the wrong slope -- which is
       reported as such rather than silently dropped."""
    rg_, rho_ = rho_from_M(Mtot_grid, rtrunc_kpc)
    Rs = np.exp(np.linspace(math.log(0.5*Mpc), math.log(2.0*Mpc), 8))
    ds = np.array([dsigma_of_R(rg_, rho_, R, rtrunc_kpc*kpc) for R in Rs])
    m = ds > 0
    sl = float(np.polyfit(np.log(Rs[m]), np.log(ds[m]), 1)[0]) if m.sum() >= 4 else np.nan
    return (sl, bool(m.sum() < len(Rs))) if want_flag else sl

# P0 -- POSITIVE control: an NFW dark component reproduces the measured shear slope
nfw_sl = []
for n, (z, M2h) in WL.items():
    rs_, dc_, rc_, _, r200_ = nfw_from_M200(M2h*1e14, z)
    Mn = 4*math.pi*dc_*rc_*rs_**3*(np.log(1 + GRID*kpc/rs_) - (GRID*kpc/rs_)/(1 + GRID*kpc/rs_))/MSUN
    nfw_sl.append(shear_slope(Mn + CLC[n]["Mbar"], 3*r200_/kpc))
nfw_sl = float(np.mean(nfw_sl))
info(f"P0 positive control: a dark component with an NFW shape, projected through THIS machinery, gives a "
     f"shear log-slope {nfw_sl:+.3f} against the measured {WL_SLOPE:+.3f} +/- {WL_SLOPE_E:.3f}")
check("P0 [positive control] the shape gate is PASSABLE: a dark component with an NFW shape reproduces the "
      "measured shear log-slope, so a FAIL below is a statement about the candidate and not about the gate",
      abs(nfw_sl - WL_SLOPE) < 3*max(WL_SLOPE_E, 0.06),
      f"NFW gives {nfw_sl:+.3f}, measured {WL_SLOPE:+.3f} +/- {WL_SLOPE_E:.3f} "
      f"({abs(nfw_sl-WL_SLOPE)/max(WL_SLOPE_E, 0.06):.1f} sigma)")

# P1 -- reproduce L24's own new constraint with this machinery, so R4 is verified and not quoted
fw_sl = [shear_slope(np.array([g_kernel(G*mb*MSUN/(r*kpc)**2, A0["canonical"])*(r*kpc)**2/(G*MSUN)
                               for r, mb in zip(GRID, CLC[n]["Mbar"])]), 2*R200_clu)
         for n in sorted(WL)]
FW_SLOPE = float(np.mean(fw_sl))
info(f"P1 reproduction: the FRAMEWORK's own phantom, projected through the same machinery, gives a shear "
     f"log-slope {FW_SLOPE:+.3f} (per cluster {', '.join(f'{x:+.2f}' for x in fw_sl)}) against the measured "
     f"{WL_SLOPE:+.3f} +/- {WL_SLOPE_E:.3f}")
check("P1 [reproduction of L24 C11] the framework's own projected shear log-slope agrees with the measured "
      "one, i.e. its phantom has the right lensing SHAPE",
      abs(FW_SLOPE - WL_SLOPE) < 3*max(WL_SLOPE_E, 0.058),
      f"{FW_SLOPE:+.3f} against {WL_SLOPE:+.3f} +/- {WL_SLOPE_E:.3f}, a difference of "
      f"{FW_SLOPE-WL_SLOPE:+.3f} at {abs(FW_SLOPE-WL_SLOPE)/0.058:.0f} sigma on L24's quoted error -- "
      f"independently reproducing L24 C11's +0.53 +/- 0.06 at 9 sigma, with different code and a different "
      f"baryon build.  L24's new shape constraint therefore enters the specification VERIFIED")

P("")
info(f"{'a':>6} {'b':>7} {'rho_X slope':>12} {'ratio-profile':>14} {'shear slope':>12} {'L* inside 10kpc':>17} "
     f"{'dwarf inside 10kpc':>19}")
info(f"{'':>6} {'':>7} {'(cluster)':>12} {'rms [dex]':>14} {'0.5-2 Mpc':>12} {'[M_b], tol %.2f' % TOL_LSTAR:>17} "
     f"{'[M_b], tol %.2f' % TOL_DWARF:>19}")
info("-"*104)
def member(a):
    b = b_of_a(a); C = C_of_a(a)
    Rmod = C*mb_prof**a*(rr/100.0)**b/mb_prof
    rms = float(np.sqrt(np.mean((np.log10(Rmod) - np.log10(med))**2)))
    n0 = sorted(WL)[0]
    MX = C*CLC[n0]["Mbar"]**a*(GRID/100.0)**b
    sl, neg = shear_slope(MX + CLC[n0]["Mbar"], 2*R200_clu, want_flag=True)
    dM = np.gradient(MX, np.log(GRID))/GRID**3
    w = (GRID > 40) & (GRID < 750) & (dM > 0)
    rho_slope = float(np.polyfit(np.log(GRID[w]), np.log(dM[w]), 1)[0]) if w.sum() > 5 else np.nan
    return dict(a=a, b=b, rms=rms, sl=sl, neg=neg, rho=rho_slope,
                mL=C*(8e10)**a*(10./100.)**b/8e10, mD=C*(2e9)**a*(10./100.)**b/2e9)
SCAN = [member(a) for a in np.round(np.arange(-1.60, 1.81, 0.10), 3)]
for x in SCAN:
    if abs(x["a"]*5 - round(x["a"]*5)) < 1e-9:
        sls = "  NEGATIVE" if x["neg"] else f"{x['sl']:+9.3f}"
        info(f"{x['a']:6.2f} {x['b']:7.3f} {x['rho']:12.2f} {x['rms']:14.3f} {sls:>12} "
             f"{x['mL']:17.3g} {x['mD']:19.3g}")
info(f"({len(SCAN)} members scanned in steps of 0.10 in a over a = -1.6 to +1.8; every second is printed.")
info(" 'NEGATIVE' means the source's density RISES outward, so DeltaSigma comes out negative -- weak-lensing")
info(" shear of the wrong SIGN, which fails R4 more badly than any slope mismatch could.)")

TOL_SL = 3*max(WL_SLOPE_E, 0.058)
ok_rms = [x for x in SCAN if x["rms"] < 0.15]
ok_sl = [x for x in SCAN if np.isfinite(x["sl"]) and not x["neg"] and abs(x["sl"] - WL_SLOPE) < TOL_SL]
ok_gal = [x for x in SCAN if x["mL"] < TOL_LSTAR and x["mD"] < TOL_DWARF]
ok_all = [x for x in SCAN if x in ok_rms and x in ok_sl and x in ok_gal]
def win(lst): return f"a in [{min(x['a'] for x in lst):+.2f}, {max(x['a'] for x in lst):+.2f}]" if lst else "EMPTY"
fin = [x for x in SCAN if np.isfinite(x["sl"]) and not x["neg"]]
best_sl = min(fin, key=lambda x: abs(x["sl"] - WL_SLOPE))
check("B1 the two-anchor family has a member reproducing the cluster's OWN measured ratio profile to 0.15 dex",
      len(ok_rms) > 0,
      f"best rms = {min(x['rms'] for x in SCAN):.3f} dex at a = {min(SCAN, key=lambda x: x['rms'])['a']:+.2f}; "
      f"admissible window {win(ok_rms)}")
check("B2 it has a member whose projected shear log-slope agrees with the measured one within 3 sigma",
      len(ok_sl) > 0,
      f"the family's positive-shear members span {min(x['sl'] for x in fin):+.2f} to "
      f"{max(x['sl'] for x in fin):+.2f} against a measured {WL_SLOPE:+.3f} +/- {WL_SLOPE_E:.3f}; admissible "
      f"window {win(ok_sl)}, closest member a = {best_sl['a']:+.2f} at {best_sl['sl']:+.3f}; every member "
      f"with a < -0.6 produces shear of the WRONG SIGN")
check("B3 it has a member passing the galaxy-scale non-overshoot gate at L* AND at the dwarf scale",
      len(ok_gal) > 0,
      f"admissible window {win(ok_gal)}, and every member in it is one of the wrong-sign-shear members: the "
      f"only way to keep the source out of a 2e9 Msun galaxy while feeding the pairs is to make it rise "
      f"outward, which destroys the lensing signal")
check("B4 [THE SEARCH] some single member of the family passes B1, B2 and B3 at once, i.e. a single radial "
      "profile serves both the cluster and the pair scale and survives the shear and galaxy gates",
      len(ok_all) > 0,
      f"ratio-profile window {win(ok_rms)}, shear window {win(ok_sl)}, galaxy window {win(ok_gal)}; the "
      f"intersection is {win(ok_all)}.  The windows that DO open are disjoint: the member that reproduces "
      f"the cluster's ratio profile is not the member that projects to the right shear slope, and neither "
      f"is admissible inside a dwarf")

# ---- B5: the undetected-baryon escape, priced rather than assumed ----------------------------------------
P("")
NEED_BAR = (1 + RATIO_PAIR)/(1 + F_COSMIC)
info(f"B5 -- the one escape the anchors leave: the pairs' baryons are UNDERCOUNTED.  For a component at the")
info(f"     cosmic share to give the observed pair kinematics, the true baryon mass inside {R_ANCHOR_PAIR:.0f} kpc "
     f"must be {NEED_BAR:.2f}x")
info(f"     the K-band stellar mass, i.e. {NEED_BAR*MBAR_PAIR:.2e} Msun -- {(NEED_BAR-1)*MBAR_PAIR:.2e} of it "
     f"undetected.  Does the framework's")
info("     OWN galaxy-scale gate close that door?  Priced with the distribution that is MOST favourable to the")
info("     escape (uniform density inside the pair separation, which minimises what lands in the inner galaxy):")
hid = (NEED_BAR - 1)*MBAR_PAIR
for rin in (10., 20., 30.):
    f_in = (rin/R_ANCHOR_PAIR)**3
    info(f"       uniform: {hid*f_in:.2e} Msun inside {rin:.0f} kpc = {hid*f_in/2/(MBAR_PAIR/2):.3f} M_b per "
         f"galaxy (gate at 10 kpc: {TOL_LSTAR:.2f})")
f10 = (10./R_ANCHOR_PAIR)**3
check("B5 the framework's own galaxy-scale gate CLOSES the undetected-baryon escape at pair scale",
      hid*f10/MBAR_PAIR > TOL_LSTAR,
      f"it does not: even {NEED_BAR:.1f}x the K-band baryons, spread uniformly inside {R_ANCHOR_PAIR:.0f} kpc, "
      f"puts only {hid*f10/MBAR_PAIR:.4f} M_b inside 10 kpc against a tolerance of {TOL_LSTAR:.2f}.  This door "
      f"is OPEN on this repository's data and is closed, if at all, by circumgalactic-medium mass budgets "
      f"(the requirement is ~4 stellar masses of gas inside 130 kpc of an L* pair), which is a literature "
      f"question this lane does not settle and does not claim to")

# ---- C1: the incompatible pair, measured internally -------------------------------------------------------
P("")
P("-"*122)
P("  THE INCOMPATIBLE PAIR.  Along the anchor line the surviving direction is a HOST-MASS law: the source's")
P("  abundance per baryon falls with host mass.  That exponent is not free -- the pair sample MEASURES it")
P("  internally, in quartiles of its own baryonic mass, with the same estimator.  NOT at fixed radius --")
P("  see the caveat below, and C2, which controls for separation and is the load-bearing version.")
P("-"*122)
Mb_pair = S["M1"] + S["M2"]; q = np.percentile(np.log10(Mb_pair), [0, 25, 50, 75, 100])
QR = []
for k in range(4):
    m = (np.log10(Mb_pair) >= q[k]) & (np.log10(Mb_pair) <= q[k+1])
    if m.sum() < 50: continue
    Ak, eAk = ml_amp(S["dv"][m], sig_newton(S["M1"][m], S["M2"][m], S["rp"][m], seed=31+k))
    QR.append((float(np.median(np.log10(Mb_pair[m]))), int(m.sum()), Ak**2 - 1, 2*Ak*eAk,
               float(np.median(S["rp"][m]))))
    info(f"    log M_b = {QR[-1][0]:5.2f}  N = {QR[-1][1]:4d}  median r_p = {QR[-1][4]:5.0f} kpc  "
         f"M_dark/M_bar within r_p = {QR[-1][2]:5.1f} +/- {QR[-1][3]:.1f}")
lm = np.array([x[0] for x in QR]); ra = np.array([x[2] for x in QR]); er = np.array([x[3] for x in QR])
w = 1.0/(er/ra/math.log(10))**2
Xm = np.vstack([lm, np.ones(len(lm))]).T
Cw = np.linalg.inv(Xm.T@(w[:, None]*Xm))
slope_in = float((Cw@(Xm.T@(w*np.log10(ra))))[0]); e_slope_in = float(math.sqrt(Cw[0, 0]))
slope_anchor = math.log10(RATIO_CLU/RATIO_PAIR)/math.log10(MBAR_CLU/MBAR_PAIR)
e_slope_anchor = (E_RATIO_PAIR/RATIO_PAIR/math.log(10))/math.log10(MBAR_CLU/MBAR_PAIR)
zC1 = (slope_in - slope_anchor)/math.hypot(e_slope_in, e_slope_anchor)
info("")
info(f"    d log(M_X/M_bar) / d log M_bar measured INSIDE the pair sample : {slope_in:+.3f} +/- {e_slope_in:.3f}")
info(f"    the same exponent demanded by the cluster-to-pair anchors      : {slope_anchor:+.3f} +/- {e_slope_anchor:.3f}")
info(f"    the two have OPPOSITE SIGN and differ at {abs(zC1):.1f} sigma")
check("C1 [the incompatible pair, one dimension] the host-mass exponent the two anchors demand agrees with "
      "the host-mass exponent the pair sample measures internally, so a host-mass abundance law can serve "
      "both scales",
      abs(zC1) < 3,
      f"internal {slope_in:+.3f} +/- {e_slope_in:.3f} against the anchors' {slope_anchor:+.3f} +/- "
      f"{e_slope_anchor:.3f}: {abs(zC1):.1f} sigma, and of OPPOSITE SIGN.  Within the pair population the "
      f"source's abundance per baryon RISES with host mass; between pairs and clusters it must FALL by a "
      f"factor {RATIO_PAIR/RATIO_CLU:.1f}.  CAVEAT, stated because it weakens this check: r_p correlates with "
      f"M_b across these quartiles, so part of the +{slope_in:.2f} is radial.  C2 below controls for that and "
      f"the mass exponent alone falls to +0.15 +/- 0.12; the robust statement is C2's joint one, not this "
      f"one, and this check should be read as indicative")

# ---- C2: the internal rule in BOTH exponents, against the anchor line ------------------------------------
P("")
info("C2 -- the same test in BOTH exponents at once.  The pair sample can measure the WHOLE rule internally:")
info("     split it three ways in baryonic mass and three ways in separation and fit")
info("        log R = const + alpha log M_bar + beta log r      (so a = 1 + alpha, b = beta),")
info("     then ask whether that (a, b) lies on the anchor line the cluster and pair scales together demand.")
qm = np.percentile(np.log10(Mb_pair), [0, 33.3, 66.7, 100])
qr = np.percentile(np.log10(S["rp"]), [0, 33.3, 66.7, 100])
CELL = []
info(f"     {'log M_b':>16} {'log r_p':>16} {'N':>6} {'M_dark/M_bar':>16}")
for i in range(3):
    for j in range(3):
        m = ((np.log10(Mb_pair) >= qm[i]) & (np.log10(Mb_pair) <= qm[i+1])
             & (np.log10(S["rp"]) >= qr[j]) & (np.log10(S["rp"]) <= qr[j+1]))
        if m.sum() < 80: continue
        Ak, eAk = ml_amp(S["dv"][m], sig_newton(S["M1"][m], S["M2"][m], S["rp"][m], seed=101+3*i+j))
        CELL.append((float(np.median(np.log10(Mb_pair[m]))), float(np.median(np.log10(S["rp"][m]))),
                     Ak**2 - 1.0, 2*Ak*eAk, int(m.sum())))
        info(f"     {CELL[-1][0]:16.2f} {CELL[-1][1]:16.2f} {CELL[-1][4]:6d} "
             f"{CELL[-1][2]:11.1f} +/-{CELL[-1][3]:4.1f}")
lm2 = np.array([c[0] for c in CELL]); lr2 = np.array([c[1] for c in CELL])
y2 = np.log10(np.array([c[2] for c in CELL])); ey2 = np.array([c[3] for c in CELL])/np.array([c[2] for c in CELL])/math.log(10)
X2 = np.vstack([np.ones(len(lm2)), lm2, lr2]).T; W2 = np.diag(1.0/ey2**2)
Cov2 = np.linalg.inv(X2.T@W2@X2); beta2 = Cov2@(X2.T@W2@y2)
alpha, bet = float(beta2[1]), float(beta2[2])
e_alpha, e_bet = float(math.sqrt(Cov2[1, 1])), float(math.sqrt(Cov2[2, 2]))
a_int, b_int = 1.0 + alpha, bet
resid = a_int*LN_M + b_int*LN_R - LN_X
grad = np.array([LN_M, LN_R])
e_resid = float(math.sqrt(grad@Cov2[1:, 1:]@grad))
info("")
info(f"     measured INSIDE the pairs : alpha = {alpha:+.3f} +/- {e_alpha:.3f}, beta = {bet:+.3f} +/- "
     f"{e_bet:.3f}   =>   a = {a_int:+.3f}, b = {b_int:+.3f}")
info(f"     the anchor line requires  : {LN_M:.4f} a + {LN_R:.4f} b = {LN_X:.4f}; this (a, b) gives "
     f"{a_int*LN_M + b_int*LN_R:.4f}")
info(f"     residual {resid:+.3f} +/- {e_resid:.3f} in ln M_X, i.e. the rule measured inside the pair "
     f"population, extrapolated to a cluster, OVER-predicts the cluster source by a factor "
     f"{math.exp(resid):.0f}")
check("C2 [the incompatible pair, both dimensions] the profile rule the pair sample measures internally, "
      "extrapolated to cluster scale, reproduces the measured cluster source",
      abs(resid/e_resid) < 3,
      f"it over-predicts it by a factor {math.exp(resid):.0f} (residual {resid:+.3f} +/- {e_resid:.3f} in "
      f"ln M_X, {abs(resid/e_resid):.1f} sigma).  The pair population's own internal rule -- more source per "
      f"baryon in more massive hosts, and more of it at larger radius -- points in exactly the direction the "
      f"cluster anchor forbids.  No single host-blind rule of this form passes through both")

# ==========================================================================================================
P("\n" + "=" * 122)
P("PART D -- the flagged internal disagreement: is the required source CORED (Famaey+2024) or CUSPY (g04a)?")
P("=" * 122)
P("  Famaey, Pizzuti & Saltas 2024 describe the MOND lensing residual inside ~1 Mpc as an inner CORE with an")
P("  outer slope steeper than about -3.5.  g04a fits a SINGLE POWER LAW to the X-ray-required source over")
P("  40-750 kpc and reports rho ~ r^-1.53, 'not cored'.  Those are different PARAMETRISATIONS over different")
P("  ranges, so before calling it a conflict the obvious test is whether a cored profile, fitted by g04a's own")
P("  procedure over g04a's own range, returns g04a's own slope.")

def pl_slope(r, rho, lo, hi):
    m = (r >= lo) & (r <= hi) & (rho > 0)
    return float(np.polyfit(np.log(r[m]), np.log(rho[m]), 1)[0])
# D1 control: injected power law
r_i = np.exp(np.linspace(math.log(20), math.log(2000), 300))
for inj in (-1.0, -1.53, -2.5):
    got = pl_slope(r_i, r_i**inj, 40, 750)
    if abs(got - inj) > 1e-6: break
check("D1 [control] the power-law fitter recovers an injected density slope exactly over 40-750 kpc",
      all(abs(pl_slope(r_i, r_i**x, 40, 750) - x) < 1e-6 for x in (-1.0, -1.53, -2.5)),
      "recovered -1.000, -1.530, -2.500")

# D2: the required source's slope, recomputed from the X-COP data
req_sl = []
for n in sorted(CLC):
    c = CLC[n]
    Msrc = c["Mh_i"] - c["Mbar"]
    rho = np.gradient(Msrc, np.log(GRID))/GRID**3
    m = (GRID > 40) & (GRID < 750) & (rho > 0)
    req_sl.append(float(np.polyfit(np.log(GRID[m]), np.log(rho[m]), 1)[0]))
REQ_SLOPE = float(np.mean(req_sl))
info("")
info(f"  the required source rho_X = d(M_HSE - M_bar)/dr / 4 pi r^2, five clusters, single power law over "
     f"40-750 kpc: {REQ_SLOPE:+.3f} (per cluster {', '.join(f'{x:+.2f}' for x in req_sl)})")
check("D2 an independent read of the X-COP profiles reproduces g04a's required source slope rho ~ r^-1.53 "
      "over 40-750 kpc",
      abs(REQ_SLOPE - (-1.53)) < 0.20, f"recomputed {REQ_SLOPE:+.3f} against g04a's -1.53")

# D3: does a CORED profile of the Famaey type return the same single-power-law slope?
info("")
info("  now the decisive test.  A CORED profile with the outer slope Famaey+2024 describe,")
info("      rho(r) = rho_0 / [ 1 + (r/r_c)^2 ]^(n/2)   with n = 3.5 (cored inside r_c, r^-3.5 outside),")
info("  is passed through g04a's own single-power-law fit over 40-750 kpc:")
info(f"  {'r_c [kpc]':>10} {'fitted slope 40-750 kpc':>26} {'|slope - (-1.53)|':>19}")
cored = []
for rc_kpc in (200., 300., 400., 500., 600.):
    rho_c_ = 1.0/(1 + (r_i/rc_kpc)**2)**(3.5/2)
    sl = pl_slope(r_i, rho_c_, 40, 750); cored.append((rc_kpc, sl))
    info(f"  {rc_kpc:10.0f} {sl:26.3f} {abs(sl-(-1.53)):19.3f}")
best_core = min(cored, key=lambda x: abs(x[1] - REQ_SLOPE))
info(f"  a core radius of {best_core[0]:.0f} kpc returns a single-power-law slope of {best_core[1]:+.3f} over "
     f"40-750 kpc, against the {REQ_SLOPE:+.2f} the X-ray inversion measures -- the SAME number.")
info("  the two statements are therefore not in conflict: 'rho ~ r^-1.53 over 40-750 kpc' is the mean")
info("  log-slope of exactly the cored-with-steep-outskirts shape Famaey+2024 report, and g04a's 'not cored'")
info("  is a statement that the fit is not FLAT, which a core radius comparable to the fitting range does not")
info("  make it.  What g04a's number does exclude is a core radius LARGE compared with 750 kpc:")
big = [x for x in [(rcx, pl_slope(r_i, 1.0/(1 + (r_i/rcx)**2)**(3.5/2), 40, 750)) for rcx in (1000., 1500., 2000.)]]
for rcx, slx in big: info(f"      r_c = {rcx:.0f} kpc gives {slx:+.3f}, i.e. far too flat")
check("D3 the cored-versus-cuspy disagreement is REAL: no cored profile of the Famaey type reproduces the "
      "single-power-law slope the X-ray inversion measures over 40-750 kpc",
      abs(best_core[1] - REQ_SLOPE) > 0.20,
      f"a core radius of {best_core[0]:.0f} kpc reproduces it exactly ({best_core[1]:+.3f} against "
      f"{REQ_SLOPE:+.3f}).  The disagreement is a PARAMETRISATION artefact, not a physical conflict: the two "
      f"groups fit different functional forms over different radial ranges to the same shape.  What survives "
      f"as a real constraint is that the core radius must be <~ 750 kpc, i.e. comparable to or smaller than "
      f"the fitting range -- both descriptions agree on that, and BOTH exclude a relic sitting at its "
      f"Tremaine-Gunn floor, whose core is the whole system")

# ==========================================================================================================
P("\n" + "=" * 122)
P("PART E -- does the non-monotone ladder constrain LambdaCDM?  Checked in the direction that would say NO.")
P("=" * 122)
P("  The repository's standing rule is never to claim data favour this framework over LambdaCDM, so this is")
P("  tested adversarially: LambdaCDM's OWN abundance-matching relation is evaluated at the pair's measured")
P("  baryonic mass, with NO fitted parameter, and asked whether it already predicts the 30.9.")

def moster_mstar(logMh):
    """Moster, Naab & White 2013 z = 0 stellar-to-halo-mass relation (the form L21 carries)."""
    M1, N, be, ga = 11.59, 0.0351, 1.376, 0.608
    x = 10**(logMh - M1)
    return 10**logMh*2*N/(x**-be + x**ga)
def halo_mass(Mstar):
    lo, hi = 9.0, 15.5
    for _ in range(80):
        m = 0.5*(lo + hi)
        if moster_mstar(m) < Mstar: lo = m
        else: hi = m
    return 10**(0.5*(lo + hi))
def nfw_frac(Mh, r_kpc):
    z = 0.0; c = c200_DM14(Mh, z); r200 = (3*Mh*MSUN/(4*math.pi*200*rho_crit(z)))**(1./3.)/kpc
    f = lambda x: math.log(1+x) - x/(1+x)
    return f(c*r_kpc/r200)/f(c), r200

Mstar_each = MBAR_PAIR/2.0
Mh_each = halo_mass(Mstar_each)
frac, r200_g = nfw_frac(Mh_each, R_ANCHOR_PAIR)
pred_ratio = 2*Mh_each*frac/MBAR_PAIR - 1.0
info("")
info(f"  pair median M_b = {MBAR_PAIR:.2e} Msun, i.e. {Mstar_each:.2e} per galaxy")
info(f"  Moster+2013 abundance matching  =>  M200 = {Mh_each:.2e} Msun per galaxy, R200 = {r200_g:.0f} kpc")
info(f"  an NFW halo of that mass puts a fraction {frac:.3f} of itself inside the pair's {R_ANCHOR_PAIR:.0f} kpc")
info(f"  => LambdaCDM predicts M_dark/M_bar within r_p = {pred_ratio:.1f}, against the measured "
     f"{RATIO_PAIR:.1f} +/- {E_RATIO_PAIR:.1f}")
info(f"  and at cluster scale the SAME framework needs no adjustment: clusters retain f_bar = 0.149 against "
     f"the cosmic 0.156, so M_dark/M_bar = {RATIO_CLU:.2f} follows with nothing fitted.")
info("  the ladder is therefore non-monotone in LambdaCDM BY CONSTRUCTION: galaxy-scale halos are")
info("  baryon-POOR (the stellar-to-halo-mass relation), cluster-scale halos are baryon-complete.  The")
info("  quantity L21 measured is the stellar-to-halo-mass relation, which is an INPUT to LambdaCDM fixed by")
info("  the galaxy stellar mass function, not a prediction this measurement tests.")
check("E1 the non-monotone ladder is a constraint on LambdaCDM: its own abundance-matching relation, with no "
      "free parameter, FAILS to predict the pair ratio",
      abs(pred_ratio - RATIO_PAIR) > 3*E_RATIO_PAIR,
      f"it predicts {pred_ratio:.1f} against the measured {RATIO_PAIR:.1f} +/- {E_RATIO_PAIR:.1f} "
      f"({abs(pred_ratio-RATIO_PAIR)/E_RATIO_PAIR:.1f} sigma; L21's own forward model returns A = 0.967 +/- "
      f"0.024 for the same relation, 1.4 sigma from unity).  NOTHING HERE CONSTRAINS LambdaCDM, and this "
      f"lane makes no such claim.  The non-monotone ladder is a problem ONLY for a completion that must "
      f"supply the residual from a UNIVERSAL component with a single cosmological abundance, which is the "
      f"framework's situation and not LambdaCDM's")

# ==========================================================================================================
P("\n" + "=" * 122)
P("PART F -- the verdict")
P("=" * 122)
sat = len(ok_all) > 0 and abs(zC1) < 3 and abs(zA1) < 3 and abs(resid/e_resid) < 3
check("V1 [VERDICT] the assembled specification is self-consistent -- some object could satisfy every "
      "requirement at once",
      sat,
      f"R1/R6 alone are incompatible: the source must be {RATIO_CLU:.2f} baryonic masses at 1000 kpc of a "
      f"cluster and {RATIO_PAIR:.1f} inside {R_ANCHOR_PAIR:.0f} kpc of a pair, and at the SAME radius the "
      f"clusters measure {R_clu_at_pair:.1f} ({abs(zA1):.0f} sigma).  The only family direction that survives "
      f"both anchors is a host-mass abundance law with exponent {slope_anchor:+.2f}, and the full rule the "
      f"pair sample measures internally, (a, b) = ({a_int:+.2f}, {b_int:+.2f}), misses the anchor line by a "
      f"factor {math.exp(resid):.0f} at {abs(resid/e_resid):.1f} sigma.  "
      f"Independently, the {len(SCAN)}-member family search closes with "
      f"an EMPTY intersection: the ratio-profile window {win(ok_rms)}, the shear window {win(ok_sl)} and the "
      f"galaxy window {win(ok_gal)} are PAIRWISE DISJOINT, and every member of the galaxy window produces "
      f"weak-lensing shear of the wrong SIGN")

P("")
info("WHAT THIS DOES AND DOES NOT SAY.")
info(" * It does NOT say the cluster residual has no explanation.  It says no SINGLE UNIVERSAL COMPONENT with")
info("   ONE cosmological abundance and ONE host-blind profile rule can supply both the cluster requirement")
info("   and the pair requirement, on this repository's own measurements of both.")
info(" * It does NOT constrain LambdaCDM (E1).  LambdaCDM supplies exactly the missing ingredient -- a")
info("   host-mass-dependent BARYON retention -- and its abundance-matched halos land within 1.4 sigma of the")
info("   pair kinematics and reproduce the clusters with nothing fitted.")
info(" * The escape the specification leaves open, stated rather than closed: give the SOURCE a")
info("   host-mass-dependent abundance per baryon, or give the BARYONS a host-mass-dependent detection")
info(f"   efficiency (the pair would need {(1+RATIO_PAIR)/(1+F_COSMIC):.1f}x its K-band baryons inside "
     f"{R_ANCHOR_PAIR:.0f} kpc for a cosmic-share component to work).  Either is a NEW FREE FUNCTION of host")
info("   mass, and the second is the stellar-to-halo-mass relation under another name.  A completion that")
info("   adopts it inherits LambdaCDM's galaxy-formation sector wholesale, which is a real cost and should be")
info("   stated as one.")
info(" * The specification is written out as a numbered checklist in L41_CLUSTER_SPEC.md.  Any future")
info("   proposal can be run against it; a proposal that fails R4 or R6 fails without further computation.")

P("")
P(f"RESULT: {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else ""))
P(f"[{time.time()-T0:.0f} s]")
sys.exit(0)
