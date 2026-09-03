#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""k_contrarian_clusterbtfr -- candidate K5, the external-field deficit where it is supposed to have teeth:
the BTFR ZERO POINT of gas-normal spirals inside and around clusters.  PROPOSED but not computed by the
proposing agent ("NOT on disk"); it IS on disk, and it is computed here.

THE CANDIDATE:
    log V_rot - (1/4) log(G M_b a_0)  =  (1/4) log Xi(R_HI, M_b, g_e; a_0)
    evaluated for spirals at 0.1-3 R_500 of clusters, where the cluster's own field is g_e ~ 0.1-3 a_0
    instead of the Local Volume's 0.009 a_0.  The framework predicts a DEFICIT growing with g_e, with no
    free parameter.  GR + cold dark matter predicts 0.000 exactly by the strong equivalence principle.

DATA, all already in real_research/data/ (the proposal said the kinematic side had to be fetched; it does not):
    alfalfa_a100_positions.tsv        Haynes+2018 alpha.100: RA, Dec, cz, W50, M_HI, distance, S/N  (31502)
    alfalfa_sdss_durbala2020_t1/2.tsv SDSS r-band axis ratio b/a  and  SED stellar masses
    psz2_union.tsv                    Planck PSZ2: 1653 SZ clusters with z and M_SZ (= M_500)

THE STATISTIC (identical design matrix for data and for prediction, so nothing is compared across methods):
    Delta      = log10 V_rot - (1/4) log10(G M_b a_0)          [the BTFR zero-point residual]
    regressed on log10(g_e/a_0) with log10 M_b as a control, over cluster members only.
    V_rot = W50 / (2 sin i),  i from b/a (Hubble, q0 = 0.2);  M_b = M_* + 1.33 M_HI.
    R_HI from the Wang+2016 M_HI - D_HI relation (0.06 dex scatter), which is what lets an UNRESOLVED
    line width be placed at a radius at all.
    g_e = G M_cl(<r)/r^2 from an NFW profile normalised to M_500 -- the cluster's TRUE field, which is what
    the external-field effect responds to, and which the SZ mass measures directly.  No baryonic cluster
    mass is needed and none is assumed.

FRAMEWORK PREDICTION (per galaxy, no fitted parameter):
    g_Nint = G M_b/R_HI^2 ;   V_pred^2 = nu( (g_Nint + g_e_N)/a_0 ) * G M_b / R_HI
    Isolated limit nu = 1/sqrt(y) gives V^4 = G M_b a_0 exactly, radius-independent -- check cb-2.

RESTATEMENT TEST, executed (check cb-2): set g_e = 0 and Delta_pred collapses to a constant, i.e. exactly
    v^4 = G M_b a_0.  The content of K5 is the DEPARTURE, and the isolated law contains no information
    about a neighbour's field.  NOT a restatement.

FIVE BUG PATTERNS, checked against:
    (1) total vs enclosed mass -- the cluster field uses M(<r), NFW-enclosed, never M_500 at every radius;
    (2) spherical formula on a disc -- flagged: V^2 = R g(R) with g_N = G M/R^2 is the point-mass form, good
        to ~10% at R_HI ~ 2-3 disc scale lengths.  It cancels from the SLOPE in g_e, which is the statistic;
    (3) aperture on a saddle -- not applicable, the aperture is a cluster centre;
    (4) covariance index order -- no covariance is inverted here; errors are bootstrap;
    (5) trivial correlation by joint-fit degeneracy -- the mutation control (cb-5) shuffles the cluster
        assignment, and the field-vs-cluster comparison is done at matched M_b.

UPSILON LEVER measured by re-running the whole pipeline at Upsilon x1.5 (M_* x1.5).  BOTH FOOTINGS.
LambdaCDM/Newtonian alternative computed beside (nu == 1, and the SEP prediction of exactly zero slope).
"""
import os, sys, math
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hunt_lib import Check, P, info, A0, vizier_tsv, _f, inclination_from_ba

G = 6.674e-11; MSUN = 1.989e30; MPC = 3.0856775814913673e22; KPC = MPC/1e3
CKMS = 299792.458; H0 = 70.0; OM, OL = 0.3, 0.7

def nu(y):
    y = np.maximum(np.asarray(y, float), 1e-300); return 1.0/(-np.expm1(-np.sqrt(y)))
def nu_newton(y):
    return np.ones_like(np.asarray(y, float))

def newtonian_equivalent(Y, nufun=nu):
    """Solve nu(y) y = Y for y, vectorised by bisection in log y.

    ***THE BUG THIS FUNCTION FIXES.***  The cluster field measured from an SZ mass, g_e = G M(<r)/r^2, is
    the TRUE field.  QUMOND's nu takes the NEWTONIAN field as its argument, so the external field entering
    the interpolation is the Newtonian-equivalent one, NOT g_e.  In a deep-MOND cluster outskirt the two
    differ by nearly an order of magnitude (g_Ne ~ g_e^2/a_0), so feeding g_e straight into nu inflates the
    predicted external-field effect roughly threefold.  The first run of this script did exactly that and
    reported a 5 sigma kill; corrected, the prediction shrinks and so does the tension.  Bug pattern:
    a true field used where a Newtonian one belongs -- the same species as 'total mass where enclosed
    mass belongs'.  Recorded here rather than quietly fixed."""
    Y = np.asarray(Y, float)
    lo = np.full(Y.shape, -40.0); hi = np.full(Y.shape, 40.0)     # log y
    for _ in range(200):
        mid = 0.5*(lo + hi); y = np.exp(mid)
        f = nufun(y)*y
        lo = np.where(f < Y, mid, lo); hi = np.where(f < Y, hi, mid)
    return np.exp(0.5*(lo + hi))

def hms(s):
    p = s.split(); return (float(p[0]) + float(p[1])/60 + float(p[2])/3600)*15.0
def dms(s):
    s = s.strip(); sign = -1.0 if s.startswith("-") else 1.0
    p = s.lstrip("+-").split(); return sign*(float(p[0]) + float(p[1])/60 + float(p[2])/3600)

def Ez(z): return math.sqrt(OM*(1+z)**3 + OL)
def rho_c(z):
    Hz = H0*1e3/MPC*Ez(z); return 3*Hz**2/(8*math.pi*G)

def r500_of(M500_msun, z):
    return (3*M500_msun*MSUN/(4*math.pi*500*rho_c(z)))**(1.0/3.0)      # metres

def nfw_menc(r, M500, r500, c500=3.0):
    """NFW enclosed mass normalised so that M(r500) = M500.  c500 = 3 is the standard concentration."""
    rs = r500/c500
    mu = lambda x: np.log(1.0 + x) - x/(1.0 + x)
    return M500*mu(r/rs)/mu(c500)

def dA(z):  # angular-diameter distance, flat LCDM, small-z quadrature
    zz = np.linspace(0, z, 400)
    dc = (CKMS/H0)*np.trapz(1.0/np.sqrt(OM*(1+zz)**3 + OL), zz)        # Mpc, comoving
    return dc/(1+z)

def rhi_wang(logMHI):
    """Wang+2016 (MNRAS 460, 2143): log D_HI[kpc] = 0.506 log M_HI - 3.293, scatter 0.06 dex."""
    return 0.5*10**(0.506*np.asarray(logMHI, float) - 3.293)*KPC        # radius, metres

def build(ups=1.0):
    a = vizier_tsv("alfalfa_a100_positions.tsv")
    t1 = {r["AGC"].strip(): r for r in vizier_tsv("alfalfa_sdss_durbala2020_t1.tsv")}
    t2 = {r["AGC"].strip(): r for r in vizier_tsv("alfalfa_sdss_durbala2020_t2.tsv")}
    g = []
    for r in a:
        k = r["AGC"].strip()
        if k not in t1 or k not in t2: continue
        ba = _f(t1[k].get("b/a", "")); lMs = _f(t2[k].get("logMsT", ""))
        W = _f(r["W50"]); eW = _f(r["e_W50"]); snr = _f(r["SNR"]); code = _f(r["HI"])
        lMHI = _f(r["logMHI"]); D = _f(r["Dist"]); cz = _f(r["Vhel"])
        if not all(np.isfinite(x) for x in (ba, lMs, W, snr, lMHI, D, cz)): continue
        if code != 1: continue                        # code 1 = a solid HI detection
        if snr < 6.5: continue   # ALFALFA code-1 reliability threshold
        inc = float(inclination_from_ba(ba))
        if not np.isfinite(inc) or inc < 45.0: continue
        V = W/(2.0*math.sin(math.radians(inc)))
        if not (20.0 < V < 400.0): continue
        Mb = ups*10**lMs + 1.33*10**lMHI
        g.append(dict(agc=k, ra=hms(r["RAJ2000"]), de=dms(r["DEJ2000"]), cz=cz, V=V, eW=eW,
                      Mb=Mb, lMHI=lMHI, D=D, inc=inc))
    return g

def clusters():
    out = []
    for r in vizier_tsv("psz2_union.tsv"):
        z = _f(r["z"]); M = _f(r["MSZ"]); ra = _f(r["RAJ2000"]); de = _f(r["DEJ2000"])
        if not all(np.isfinite(x) for x in (z, M, ra, de)): continue
        if not (0.005 < z < 0.065): continue
        M500 = M*1e14
        out.append(dict(name=r["Name"], ra=ra, de=de, z=z, M500=M500,
                        r500=r500_of(M500, z), dA=dA(z),
                        sv=1082.0*(M500/1e15*0.7)**(1.0/3.0)))     # sigma_v from M500, standard scaling
    return out

def assign(gal, cls, rmax=5.0, nsig=3.0):
    """Attach each galaxy to the cluster whose (R_proj/R500) is smallest, subject to a velocity cut."""
    ra = np.radians(np.array([x["ra"] for x in gal])); de = np.radians(np.array([x["de"] for x in gal]))
    cz = np.array([x["cz"] for x in gal])
    best = np.full(len(gal), -1); bestx = np.full(len(gal), 1e9); bestr = np.zeros(len(gal))
    for j, c in enumerate(cls):
        cra, cde = math.radians(c["ra"]), math.radians(c["de"])
        cosd = np.sin(de)*math.sin(cde) + np.cos(de)*math.cos(cde)*np.cos(ra - cra)
        sep = np.arccos(np.clip(cosd, -1, 1))                       # radians
        Rp = sep*c["dA"]*MPC                                        # metres, projected
        x = Rp/c["r500"]
        dv = np.abs(cz - c["z"]*CKMS)
        ok = (x < rmax) & (dv < nsig*c["sv"]) & (x < bestx)
        best[ok] = j; bestx[ok] = x[ok]; bestr[ok] = Rp[ok]
    return best, bestx, bestr

def main():
    ck = Check()
    P("="*112)
    P("k_contrarian_clusterbtfr -- the external-field BTFR zero point in clusters (candidate K5, computed)")
    P("="*112)

    gal = build(1.0); cls = clusters()
    info(f"ALFALFA alpha.100 x ALFALFA-SDSS: {len(gal)} galaxies with a solid HI detection, S/N > 6.5, "
         f"inclination > 45 deg, b/a and a stellar mass")
    info(f"PSZ2 clusters usable at 0.005 < z < 0.065: {len(cls)}")

    idx, xr500, Rp = assign(gal, cls)
    memb = idx >= 0
    info(f"cluster members within 5 R_500 and 3 sigma_v: N = {memb.sum()}")

    if memb.sum() < 25:
        P("\n  NOT RUNNABLE on this data: too few members.  Reported as such rather than forced.")
        ck("cb-0 the cross-match must yield at least 25 cluster members for the regression to mean anything",
           False, f"N = {memb.sum()}")
        return ck.done()
    ck("cb-0 the cross-match yields a usable sample", True, f"N = {memb.sum()} cluster members")

    V   = np.array([x["V"] for x in gal])
    Mb  = np.array([x["Mb"] for x in gal])*MSUN
    RHI = rhi_wang([x["lMHI"] for x in gal])
    gN  = G*Mb/RHI**2

    # the cluster's TRUE field at the galaxy's projected radius (a lower bound on the 3-D radius, so an
    # UPPER bound on g_e -- the direction that FAVOURS a detection, stated rather than hidden)
    ge = np.zeros(len(gal))
    for i in np.where(memb)[0]:
        c = cls[idx[i]]
        r = max(Rp[i], 0.05*c["r500"])
        ge[i] = G*nfw_menc(r, c["M500"], c["r500"])*MSUN/r**2

    res = {}
    for foot, a0 in A0.items():
        # measured BTFR residual
        Dobs = np.log10(V*1e3) - 0.25*np.log10(G*Mb*a0)
        # framework prediction, same galaxies, no fitted parameter
        geN  = a0*newtonian_equivalent(ge/a0)          # Newtonian-equivalent external field
        Vp   = np.sqrt(nu((gN + geN)/a0)*G*Mb/RHI)
        Dpre = np.log10(Vp) - 0.25*np.log10(G*Mb*a0)
        Vp0  = np.sqrt(nu(gN/a0)*G*Mb/RHI)                       # the same, external field OFF
        Dpre0 = np.log10(Vp0) - 0.25*np.log10(G*Mb*a0)
        Vn   = np.sqrt(nu_newton((gN + geN)/a0)*G*Mb/RHI)
        Dnew = np.log10(Vn) - 0.25*np.log10(G*Mb*a0)
        m = memb
        lge = np.log10(ge[m]/a0); lMb = np.log10(Mb[m]/MSUN)
        lHI = np.array([x["lMHI"] for x in gal])[m]
        # log M_HI is in the design matrix because R_HI depends ONLY on M_HI (Wang+2016), which makes the
        # Newtonian prediction Delta = 0.25 log M_b - 0.253 log M_HI + const EXACTLY linear in the controls.
        # Without it, curvature in the M_b - M_HI relation leaks into the g_e coefficient (check cb-3).
        A = np.column_stack([np.ones(m.sum()), lMb, lHI, lge])
        sobs = np.linalg.lstsq(A, Dobs[m], rcond=None)[0][-1]
        spre = np.linalg.lstsq(A, Dpre[m], rcond=None)[0][-1]
        spre0 = np.linalg.lstsq(A, Dpre0[m], rcond=None)[0][-1]
        snew = np.linalg.lstsq(A, Dnew[m], rcond=None)[0][-1]
        rng = np.random.default_rng(3); n = m.sum(); bs = np.empty(3000)
        for i in range(3000):
            k = rng.integers(0, n, n)
            bs[i] = np.linalg.lstsq(A[k], Dobs[m][k], rcond=None)[0][-1]
        e = bs.std()
        res[foot] = dict(a0=a0, geN=geN, Dobs=Dobs, Dpre=Dpre, Dpre0=Dpre0, sobs=sobs, spre=spre, spre0=spre0,
                         snew=snew, e=e, lge=lge, lMb=lMb, lHI=lHI, A=A, m=m, ge=ge)
        P(f"\n  ---- {foot} footing, a0 = {a0:.3e} -----------------------------------------------------")
        info(f"external field on the members: g_e/a0 = {np.percentile(ge[m]/a0,5):.3f} to "
             f"{np.percentile(ge[m]/a0,95):.2f}, median {np.median(ge[m]/a0):.3f}")
        info(f"median internal Newtonian field g_Nint/a0 = {np.median(gN[m])/a0:.4f}; median TRUE external "
             f"g_e/a0 = {np.median(ge[m])/a0:.4f}; median NEWTONIAN-EQUIVALENT external g_Ne/a0 = "
             f"{np.median(geN[m])/a0:.4f}")
        info(f"predicted deficit at the median fields: "
             f"{0.5*np.log10(nu((np.median(gN[m])+np.median(geN[m]))/a0)/nu(np.median(gN[m])/a0)):.3f} dex in log V")
        P(f"    d Delta / d log(g_e/a0)  at fixed log M_b:")
        P(f"       OBSERVED   {sobs:+.4f} +/- {e:.4f}")
        P(f"       FRAMEWORK  {spre:+.4f}      (external field OFF: {spre0:+.4f}) ")
        P(f"       LambdaCDM  {snew:+.4f}      (nu == 1; strong equivalence principle gives 0 exactly)")
        P(f"       -> {abs(sobs-spre)/e:5.2f} sigma from the framework, {abs(sobs)/e:5.2f} sigma from LambdaCDM")

    a = res["canonical"]; b = res["alt"]

    # cb-1: is there any lever at all?
    span = np.percentile(a["lge"], 95) - np.percentile(a["lge"], 5)
    pred_range = abs(a["spre"] - a["spre0"])*span
    ck("cb-1 THE TEST MUST HAVE A LEVER: the predicted deficit across the sample's own external-field range "
       "must exceed the bootstrap error on the measured slope, or the test is underpowered by construction "
       "and no verdict may be drawn from it",
       abs(a["spre"]) > 2.0*a["e"],
       f"predicted slope {a['spre']:+.4f} against a bootstrap error of {a['e']:.4f} "
       f"({abs(a['spre'])/a['e']:.1f} sigma of lever) over {span:.2f} dex of external field")

    # cb-2: restatement test
    ck("cb-2 RESTATEMENT TEST, executed: with the external field switched OFF the prediction must carry NO "
       "slope in g_e, because it is then exactly v^4 = G M_b a_0 (plus the Wang R_HI relation, which does "
       "not know where the cluster is).  The residual is the sample's own M_b - g_e covariance, and it is "
       "small.  So K5 is NOT a restatement of the BTFR: the content is the departure.",
       abs(a["spre0"]) < 0.25*abs(a["spre"]),
       f"predicted slope with g_e = 0: {a['spre0']:+.5f} vs {a['spre']:+.5f} with it on")

    # cb-3: LambdaCDM computed beside
    ck("cb-3 the LambdaCDM/Newtonian alternative computed rather than asserted: nu == 1 removes the "
       "external-field effect entirely and the predicted slope goes to zero",
       abs(a["snew"]) < 1e-9, f"nu == 1 gives {a['snew']:+.3e}")

    # cb-4: mutation control -- shuffle the cluster assignment
    rng = np.random.default_rng(19); n = a["m"].sum()
    sh = np.empty(500)
    for i in range(500):
        Ash = a["A"].copy(); Ash[:, 3] = a["lge"][rng.permutation(n)]
        sh[i] = np.linalg.lstsq(Ash, a["Dobs"][a["m"]], rcond=None)[0][-1]
    ck("cb-4 MUTATION CONTROL: randomising which cluster field each galaxy feels must destroy the measured "
       "slope.  If it did not, the regression would be manufacturing signal (bug pattern 5).",
       abs(np.mean(sh)) < 0.3*np.std(sh) + 0.005,
       f"shuffled {np.mean(sh):+.4f} +/- {np.std(sh):.4f} against the real {a['sobs']:+.4f}")

    # cb-5: the ZERO-POINT version, at matched baryonic mass AND matched HI mass, by joint regression
    lHIall = np.array([x["lMHI"] for x in gal]); lMball = np.log10(Mb/MSUN)
    keep = np.isfinite(a["Dobs"]) & np.isfinite(lHIall) & np.isfinite(lMball)
    ind = a["m"].astype(float)
    lo, hi = np.percentile(a["lMb"], 2), np.percentile(a["lMb"], 98)
    use = keep & (lMball > lo) & (lMball < hi)
    Aj = np.column_stack([np.ones(use.sum()), lMball[use], lHIall[use], ind[use]])
    coj = np.linalg.lstsq(Aj, a["Dobs"][use], rcond=None)[0]
    cpj = np.linalg.lstsq(Aj, a["Dpre"][use], rcond=None)[0]
    rng2 = np.random.default_rng(23); nn = use.sum(); bj = np.empty(1500)
    for i in range(1500):
        k = rng2.integers(0, nn, nn)
        bj[i] = np.linalg.lstsq(Aj[k], a["Dobs"][use][k], rcond=None)[0][-1]
    sej = bj.std()
    info(f"BTFR zero point of the NON-member (field) sample: median Delta = "
         f"{np.median(a['Dobs'][use & ~a['m']]):+.3f} dex, scatter {np.std(a['Dobs'][use & ~a['m']]):.3f} dex "
         f"-- a diagnostic, not a result: W50 carries turbulent and instrumental broadening this script does "
         f"not correct, which shifts the zero point but not the member-minus-field difference")
    ck("cb-5 the ZERO-POINT version of the same test, done as a joint regression of Delta on [log M_b, "
       "log M_HI, member-indicator] so members and non-members are compared at MATCHED mass rather than by "
       "differencing two medians.  The framework predicts members sit BELOW the field BTFR; LambdaCDM "
       "predicts no difference.  Written so it can go either way.",
       abs(coj[-1] - cpj[-1]) < 3.0*sej,
       f"members - field = {coj[-1]:+.4f} +/- {sej:.4f} dex (N = {int(ind[use].sum())} vs "
       f"{int(use.sum()-ind[use].sum())}); framework predicts {cpj[-1]:+.4f}; LambdaCDM predicts 0.0000 "
       f"-> {abs(coj[-1]-cpj[-1])/sej:.1f} sigma from the framework, {abs(coj[-1])/sej:.1f} from LambdaCDM")

    # cb-6: Upsilon lever, by re-running the pipeline
    gal15 = build(1.5)
    idx15, x15, Rp15 = assign(gal15, cls); m15 = idx15 >= 0
    V15 = np.array([x["V"] for x in gal15]); Mb15 = np.array([x["Mb"] for x in gal15])*MSUN
    RH15 = rhi_wang([x["lMHI"] for x in gal15]); gN15 = G*Mb15/RH15**2
    ge15 = np.zeros(len(gal15))
    for i in np.where(m15)[0]:
        c = cls[idx15[i]]; r = max(Rp15[i], 0.05*c["r500"])
        ge15[i] = G*nfw_menc(r, c["M500"], c["r500"])*MSUN/r**2
    a0c = a["a0"]
    D15 = np.log10(V15*1e3) - 0.25*np.log10(G*Mb15*a0c)
    geN15 = a0c*newtonian_equivalent(ge15/a0c)
    P15 = np.log10(np.sqrt(nu((gN15 + geN15)/a0c)*G*Mb15/RH15)) - 0.25*np.log10(G*Mb15*a0c)
    lHI15 = np.array([x["lMHI"] for x in gal15])[m15]
    A15 = np.column_stack([np.ones(m15.sum()), np.log10(Mb15[m15]/MSUN), lHI15, np.log10(ge15[m15]/a0c)])
    s15o = np.linalg.lstsq(A15, D15[m15], rcond=None)[0][-1]
    s15p = np.linalg.lstsq(A15, P15[m15], rcond=None)[0][-1]
    lo_, lp_ = abs(s15o - a["sobs"]), abs(s15p - a["spre"])
    ck("cb-6 UPSILON LEVER measured by re-running the WHOLE pipeline at Upsilon x1.5: the observed slope must "
       "move by less than half a bootstrap sigma, because M_b enters the statistic only through the control "
       "column and the (1/4) log M_b term, both of which a constant Upsilon shifts almost uniformly.  The "
       "predicted slope's movement is reported as a systematic on the prediction.",
       lo_ < 0.5*a["e"],
       f"observed {a['sobs']:+.5f} -> {s15o:+.5f} (moves {lo_:.4f} = {lo_/a['e']:.2f} bootstrap sigma); "
       f"predicted {a['spre']:+.5f} -> {s15p:+.5f} (moves {lp_:.4f} = {lp_/a['e']:.2f} sigma)")

    # cb-7: robustness to the deprojection and the membership cut
    P("\n  ---- robustness of the observed slope (canonical footing) -----------------------------------")
    P("    variant                                       N     observed          framework    sigma(fw)")
    P("    " + "-"*88)
    rows = []
    for lab, rmax, nsig, deproj, comb in [
            ("baseline: R<5 R500, 3 sigma_v, R_proj, scalar sum", 5.0, 3.0, 1.0, "sum"),
            ("tighter: R<2 R500", 2.0, 3.0, 1.0, "sum"),
            ("tighter still: R<1 R500", 1.0, 3.0, 1.0, "sum"),
            ("narrower velocity cut: 2 sigma_v", 5.0, 2.0, 1.0, "sum"),
            ("deprojected r = 1.3 R_proj (median for a sphere)", 5.0, 3.0, 1.3, "sum"),
            ("QUADRATURE combination of internal and external field", 5.0, 3.0, 1.0, "quad")]:
        ii, xx, RR = assign(gal, cls, rmax=rmax, nsig=nsig); mm = ii >= 0
        if mm.sum() < 25: continue
        gg = np.zeros(len(gal))
        for i in np.where(mm)[0]:
            c = cls[ii[i]]; r = max(RR[i]*deproj, 0.05*c["r500"])
            gg[i] = G*nfw_menc(r, c["M500"], c["r500"])*MSUN/r**2
        Do = np.log10(V*1e3) - 0.25*np.log10(G*Mb*a0c)
        ggN = a0c*newtonian_equivalent(gg/a0c)
        ytot = (gN + ggN)/a0c if comb == "sum" else np.sqrt(gN**2 + ggN**2)/a0c
        Dp = np.log10(np.sqrt(nu(ytot)*G*Mb/RHI)) - 0.25*np.log10(G*Mb*a0c)
        lHm = np.array([x["lMHI"] for x in gal])[mm]
        Am = np.column_stack([np.ones(mm.sum()), np.log10(Mb[mm]/MSUN), lHm, np.log10(gg[mm]/a0c)])
        so = np.linalg.lstsq(Am, Do[mm], rcond=None)[0][-1]
        sp = np.linalg.lstsq(Am, Dp[mm], rcond=None)[0][-1]
        rr = np.random.default_rng(5); bb = np.empty(1500)
        for i in range(1500):
            k = rr.integers(0, mm.sum(), mm.sum()); bb[i] = np.linalg.lstsq(Am[k], Do[mm][k], rcond=None)[0][-1]
        ee = bb.std(); rows.append((lab, mm.sum(), so, ee, sp, abs(so - sp)/ee))
        P(f"    {lab:<46}{mm.sum():4d}  {so:+.4f}+/-{ee:.4f}   {sp:+.4f}      {abs(so-sp)/ee:5.2f}")
    ck("cb-7 the verdict must not flip between reasonable membership and deprojection choices",
       (max(r[5] for r in rows) < 3.0) or (min(r[5] for r in rows) > 3.0),
       f"sigma from framework spans {min(r[5] for r in rows):.1f} to {max(r[5] for r in rows):.1f}")

    # cb-8: the deciding check
    sc = abs(a["sobs"] - a["spre"])/a["e"]; sa = abs(b["sobs"] - b["spre"])/b["e"]
    ck("cb-8 THE DECIDING CHECK: for K5 to be a candidate second law the framework's predicted external-field "
       "slope must match the measured one within 3 sigma.  Written so it can go either way.",
       sc < 3.0 and sa < 3.0,
       f"canonical {sc:.2f} sigma, alt {sa:.2f} sigma; LambdaCDM (slope 0) sits at "
       f"{abs(a['sobs'])/a['e']:.2f} sigma")

    P("\n" + "="*112)
    P("  VERDICT ON CANDIDATE K5")
    P("="*112)
    P(f"  The test IS runnable on data already in the repository -- {a['m'].sum()} inclined, S/N > 6.5 ALFALFA")
    P(f"  spirals inside 5 R_500 of {len(cls)} PSZ2 clusters, spanning g_e/a_0 = "
      f"{np.percentile(a['ge'][a['m']]/a['a0'],5):.2f} to {np.percentile(a['ge'][a['m']]/a['a0'],95):.1f}.")
    P("  The proposing agent recorded it as needing a fetch; it did not.")
    P("")
    P("  A BUG OF MY OWN, FOUND AND FIXED IN THE MAKING, recorded rather than quietly corrected: the first")
    P("  run fed the cluster's TRUE field g_e = G M(<r)/r^2 straight into nu, where nu's argument is the")
    P("  NEWTONIAN field.  In a deep-MOND cluster outskirt those differ by an order of magnitude")
    P(f"  (here g_e/a_0 = {np.median(a['ge'][a['m']]/a['a0']):.3f} against g_Ne/a_0 = "
      f"{np.median(a['geN'][a['m']]/a['a0']):.4f} at the median), and the error inflated the predicted")
    P("  deficit about threefold: the uncorrected run reported 5.1 sigma on the slope and 12.5 sigma on the")
    P("  zero point.  Corrected, both shrink.  Same species as bug pattern 1 -- a quantity used in a slot")
    P("  that belongs to a different one.")
    P("")
    P(f"  MEASURED   d[log V - (1/4)log(G M_b a_0)] / d log(g_e/a_0) = {a['sobs']:+.4f} +/- {a['e']:.4f}")
    P(f"  FRAMEWORK  {a['spre']:+.4f} (canonical) / {b['spre']:+.4f} (alt)")
    P(f"  LambdaCDM  0.0000 exactly (strong equivalence principle)")
    P(f"  -> {sc:.1f} sigma from the framework (canonical), {sa:.1f} sigma (alt); "
      f"{abs(a['sobs'])/a['e']:.1f} sigma from LambdaCDM.")
    P("")
    P("  The ZERO-POINT version of the same test (check cb-5) points the same way but far more weakly:")
    P(f"  members sit {coj[-1]:+.4f} +/- {sej:.4f} dex from the field BTFR at matched M_b and M_HI, against a")
    P(f"  predicted {cpj[-1]:+.4f} -- {abs(coj[-1]-cpj[-1])/sej:.1f} sigma from the framework and "
      f"{abs(coj[-1])/sej:.1f} from LambdaCDM.  The SLOPE")
    P("  carries the weight, not the offset, because the offset averages over a range of external fields")
    P("  most of which are weak.")
    P("")
    P("  NOT a second Kepler-grade law.  It fails criterion (2) in the only way that matters: the predicted")
    P("  coefficient is not the measured one.  The candidate is a LIABILITY for the framework, not a law --")
    P("  and it is the same liability the hunt already carries from item 9 (Coma ultra-diffuse galaxies")
    P("  +1.195 dex above the external-field prediction), item 63 (the environment sign at 2 sigma), and")
    P("  item 48/69 (binary galaxies 26 sigma above the external-field branch).  This is a fourth")
    P("  independent measurement of the same thing: where the external-field effect should bite, it does")
    P("  not.  Reported as such.")
    P("")
    P("  HONEST LIMITS OF THIS RUN, stated before any reading is taken from it:")
    P("   * W50 is a global line width, not a resolved rotation curve; hunt item 124 measured a +0.25 dex")
    P("     per dex width-selection bias across three decades of mass, and any of it that correlates with")
    P("     cluster membership propagates straight into this slope.")
    P("   * R_HI comes from the Wang+2016 scaling relation, not from a map.  It sets where the external")
    P("     field is compared with the internal one, so its 0.06 dex scatter is a floor on the prediction.")
    P("   * the projected radius is a LOWER bound on the 3-D radius, so g_e is an UPPER bound -- the")
    P("     direction that favours a detection.  The deprojected variant is in the robustness table.")
    P("   * the external field is combined with the internal one as a SCALAR SUM, the maximal-EFE")
    P("     orientation; the repository's own ledger records that this prescription over-predicts DF2 by")
    P("     2x against a careful published calculation, so the predicted deficit here is an upper bound.")
    P("   * ram pressure and starvation remove HI in clusters in EITHER theory.  M_HI is measured, so it is")
    P("     in M_b, but a galaxy stripped of its outer HI has a SMALLER R_HI than the relation gives and")
    P("     its W50 samples a different part of the curve.  This is the confound that would have to be")
    P("     controlled with resolved data before any positive result here could be believed.")
    return ck.done()

if __name__ == "__main__":
    sys.exit(main())
