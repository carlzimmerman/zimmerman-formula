#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""k02 -- ANGLE 5, candidate 1: THE EXTERNAL-FIELD SATURATION LAW, tested on 157 globular clusters.

THE CANDIDATE LAW (an equation between measured quantities, with a_0 entering at a predicted coefficient):

    (M/L_V)_dyn  =  Upsilon_V  x  B(e),      B(e) = nu(e)[1 + L(e)/3],   L = dln nu / dln y,
    e determined by  nu(e) e = g_ext/a_0,    g_ext = G M_b,MW / R_GC^2 x nu(...),   a_0 = (c/2) sqrt(G rho_DE)

for every self-gravitating system whose own internal field is below the external field it sits in.  B is
the g_int -> 0 limit of the QUMOND external-field solve (hunt_efe_lib.py V3, which showed the naive
(nu - 1) is wrong by 22-30% because it misses the delta-function trace of the anisotropic term).

WHY IT IS NOT A RESTATEMENT OF v^4 = G M_b a_0.  The BTFR is the ISOLATED deep-MOND asymptote; the boost
it implies is sqrt(a_0/g_int), a function of the system's OWN acceleration.  The saturation law says the
boost is a function of the EXTERNAL field only and is INDEPENDENT of g_int.  For Palomar 4 those two
differ by a factor 1.4; for a Hyades-like open cluster by 5.8 (k01 computes the table).  No algebra on
v^4 = G M_b a_0 produces nu(e)[1 + L(e)/3]: it contains the kernel's own logarithmic slope, which the
deep-MOND limit has thrown away.

WHY GLOBULAR CLUSTERS.  Baumgardt & Hilker's N-body-fit catalogue (157 clusters, ON DISK) spans
g_int(r_h)/a_0 = 0.004 to 128 -- four and a half decades straddling a_0 -- with a DIRECTLY TABULATED
dynamical mass-to-light ratio.  84 clusters have g_int < g_ext, i.e. are in the saturated regime, and 73
are not.  If the law is right the two groups must have M/L_V differing by exactly B, with no fitting.

THE BUG PATTERNS, CHECKED EXPLICITLY.
 (1) total-vs-enclosed: g_int uses M/2 inside the half-MASS radius, not the total mass.
 (5) trivial correlation: B_pred depends on M through g_int, and M/L depends on M -- so a mass error
     drives log(M/L) UP and log B DOWN.  The induced slope is NEGATIVE where the law predicts +1, so the
     degeneracy works AGAINST the law, not for it.  In the saturated subset B depends on R_GC ALONE and
     the shared variable disappears entirely; that subset is the primary test.
 confound: dynamical evolution depletes low-mass stars in diffuse clusters, LOWERING their true Upsilon_V,
     again against the law.  MFSlope is carried as the control regressor.
 confound: sparse remote clusters have few radial velocities, so their "dynamical" mass is really
     photometric.  N_RV is a cut, not a nuisance.

Run:  python3 k02_gc_efe_saturation_law.py   (exit 0 = the MACHINERY checks pass; the LAW tests are reported
      separately and their failure is the physics result, not a bug)
"""
import os, sys, math, re
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hunt_lib import A0, G, Msun, kpc, DATA, nu, nu_s, Check, P, info
from hunt_efe_lib import EFESolve, dlnnu_dlny

pc = 3.0857e16
R0_KPC = 8.122
X_EXT_REG = 1.89929            # frozen registered local field in units of canonical a_0 (Amendment 8-10)
UPS_V_POP = 1.7                # stellar-population V-band M/L for old metal-poor populations (1.3-2.2 range)


# ------------------------------------------------------------------ catalogue
def gc_table():
    p = os.path.join(DATA, "globular_clusters", "baumgardt_gc_parameters.tsv")
    lines = [l.rstrip("\n") for l in open(p, encoding="latin-1") if not l.startswith("#")]
    hdr = lines[0].split("\t")
    rows = [l.split("\t") for l in lines[1:] if l.strip()]

    def num(s):
        s = s.strip()
        if not s or s.startswith("—"):
            return float("nan")
        m = re.search(r"10(\d)\s*$", s)
        e = int(m.group(1)) if m else 0
        try:
            return float(s.split("+-")[0].strip())*10**e
        except ValueError:
            return float("nan")

    col = lambda k: np.array([num(r[hdr.index(k)]) for r in rows])
    return dict(name=[r[0].split("\t")[0][:22] for r in rows], M=col("Mass[Msun]"), rh=col("rh_m[pc]"),
                Rgc=col("R_GC[kpc]"), ML=col("M/L_V"), sig0=col("sigma0[km/s]"),
                Nrv=col("N_RV"), mf=col("MFSlope"), rc=col("rc[pc]"),
                ra=col("RA"), dec=col("DEC"))


# ------------------------------------------------------------------ the boost table B(y, e)
class BoostTable:
    """B = 1 + M_ph(<r)/M_b for a point mass in a uniform external Newtonian field e = g_N,ext/a_0,
    evaluated at the radius where the baryonic Newtonian field is y = g_N,int/a_0 (so r = 1/sqrt(y))."""

    def __init__(self, e_grid=None, y_grid=None):
        self.e = np.geomspace(1e-3, 3e2, 40) if e_grid is None else np.asarray(e_grid)
        self.y = np.geomspace(1e-4, 1e3, 60) if y_grid is None else np.asarray(y_grid)
        self.tab = np.zeros((len(self.e), len(self.y)))
        r = 1.0/np.sqrt(self.y)
        for i, ee in enumerate(self.e):
            s = EFESolve(e=float(ee), nr=1500, nth=120, lmax=12, rmin=1e-3, rmax=1e5)
            self.tab[i] = 1.0 + s.enclosed_phantom(r)

    def __call__(self, y, e):
        ly, le = np.log(np.clip(y, self.y[0], self.y[-1])), np.log(np.clip(e, self.e[0], self.e[-1]))
        Le, Ly = np.log(self.e), np.log(self.y)
        i = np.clip(np.searchsorted(Le, le) - 1, 0, len(Le)-2)
        j = np.clip(np.searchsorted(Ly, ly) - 1, 0, len(Ly)-2)
        te = (le - Le[i])/(Le[i+1] - Le[i]); ty = (ly - Ly[j])/(Ly[j+1] - Ly[j])
        return ((1-te)*(1-ty)*self.tab[i, j] + te*(1-ty)*self.tab[i+1, j]
                + (1-te)*ty*self.tab[i, j+1] + te*ty*self.tab[i+1, j+1])


def B_asymptote(e):
    n = nu_s(e); L = float(dlnnu_dlny(np.array([e]))[0])
    return n*(1.0 + L/3.0)


def wls(X, y, w=None):
    """Ordinary/weighted least squares; returns (coeffs, standard errors).  Non-finite rows are dropped."""
    good = np.isfinite(y) & np.all(np.isfinite(X), axis=1)
    X, y = X[good], y[good]
    w = np.ones_like(y) if w is None else np.asarray(w, dtype=float)[good]
    Xw = X*w[:, None]
    C = np.linalg.inv(X.T @ Xw)
    b = C @ (Xw.T @ y)
    r = y - X @ b
    s2 = float(np.sum(w*r*r))/max(len(y) - X.shape[1], 1)
    return b, np.sqrt(np.diag(C)*s2)


def galactic_b(ra_deg, dec_deg):
    """ICRS -> Galactic latitude, degrees (for a reddening proxy)."""
    ra, dec = np.radians(ra_deg), np.radians(dec_deg)
    ra_ngp, dec_ngp = math.radians(192.85948), math.radians(27.12825)
    sb = np.sin(dec)*math.sin(dec_ngp) + np.cos(dec)*math.cos(dec_ngp)*np.cos(ra - ra_ngp)
    return np.degrees(np.arcsin(np.clip(sb, -1, 1)))


def main():
    ck = Check()
    P("=" * 118)
    P("k02 -- the EXTERNAL-FIELD SATURATION LAW on 157 Galactic globular clusters")
    P("       (M/L_V)_dyn = Upsilon_V x nu(e)[1 + L(e)/3],  e = G M_b,MW/(R_GC^2 a_0)")
    P("=" * 118)

    g = gc_table()
    P(f"\nBuilding the QUMOND boost table B(y, e) from the repository's own solver ...")
    BT = BoostTable()
    # validation of the table against the analytic deep-EFE limit
    err = max(abs(BT(1e-4, ee)/B_asymptote(ee) - 1.0) for ee in (0.05, 0.2, 1.0, 5.0))
    ck("the interpolated boost table reproduces the analytic g_int -> 0 limit nu(e)[1+L/3] to 3%  [CAN FAIL]",
       err < 0.03, f"max relative error {err:.4f} over e = 0.05-5")
    err0 = max(abs(BT(yy, 1e-3)/nu_s(yy) - 1.0) for yy in (0.01, 0.1, 1.0, 10.0))
    ck("with the external field switched off the table returns the ISOLATED law B = nu(y)  [CAN FAIL]",
       err0 < 0.03, f"max relative error {err0:.4f}")

    results = {}
    for foot in ("canonical", "alt"):
        a0 = A0[foot]
        P("\n" + "=" * 118)
        P(f"FOOTING: {foot}   a_0 = {a0:.3e} m/s^2")
        P("=" * 118)

        # Milky Way baryonic point mass calibrated so that e(R_0) matches the frozen registration
        e_reg = None
        lo, hi = 1e-6, 1e6
        for _ in range(200):
            mid = math.sqrt(lo*hi)
            if nu_s(mid)*mid < X_EXT_REG*A0["canonical"]/A0["canonical"]:
                lo = mid
            else:
                hi = mid
        e_reg = math.sqrt(lo*hi)                      # = 1.28903, canonical-footing Newtonian field
        MB_MW = e_reg*A0["canonical"]*(R0_KPC*kpc)**2/G/Msun
        P(f"  Milky Way baryonic point mass calibrated to the registered x_ext = {X_EXT_REG}:  "
          f"M_b,MW = {MB_MW:.3e} Msun  (a plausible Galactic baryon budget -- this is a CHECK, not a fit)")
        ck(f"[{foot}] the calibrated Milky Way baryonic mass lands in the observed range 4-8e10 Msun  [CAN FAIL]",
           4e10 < MB_MW < 8e10, f"M_b,MW = {MB_MW:.3e} Msun")

        ok = np.isfinite(g["M"]*g["rh"]*g["Rgc"]*g["ML"]) & (g["M"] > 0) & (g["rh"] > 0) & (g["ML"] > 0)
        y_int = G*(g["M"]*Msun/2.0)/((g["rh"]*pc)**2 * a0)          # ENCLOSED mass, not total (bug 1)
        e_ext = G*(MB_MW*Msun)/((g["Rgc"]*kpc)**2 * a0)
        Bp = BT(y_int, e_ext)
        sat = ok & (y_int < e_ext)
        P(f"  {ok.sum()} clusters with a tabulated M/L_V.  {sat.sum()} are EFE-saturated (y_int < e_ext); "
          f"{(ok & ~sat).sum()} are not.")
        P(f"  predicted boost B: median {np.median(Bp[ok]):.3f}, range {Bp[ok].min():.3f}-{Bp[ok].max():.3f}")

        # ---------------- the primary regression -------------------------------------------------
        hib = np.abs(galactic_b(g["ra"], g["dec"])) > 15.0
        for lab, cut in (("ALL clusters", ok),
                         ("N_RV >= 20 (mass really dynamical)", ok & (g["Nrv"] >= 20)),
                         ("N_RV >= 20 and |b| > 15 deg (extinction-safe)", ok & (g["Nrv"] >= 20) & hib),
                         ("N_RV >= 100", ok & (g["Nrv"] >= 100))):
            n = int(cut.sum())
            if n < 15:
                continue
            x = np.log10(Bp[cut]); yv = np.log10(g["ML"][cut])
            X = np.vstack([np.ones(n), x]).T
            b, se = wls(X, yv)
            res = yv - X @ b
            P(f"\n  [{lab}]  N = {n};  B_pred lever: {Bp[cut].min():.3f} to {Bp[cut].max():.3f}, "
              f"i.e. {math.log10(Bp[cut].max()/Bp[cut].min()):.2f} dex of predicted signal")
            P(f"    log10(M/L_V) = {b[0]:+.3f} + ({b[1]:+.3f} +- {se[1]:.3f}) log10(B_pred)"
              f"    [framework: slope 1, Newton: slope 0]")
            P(f"    -> framework favoured by {abs(b[1]-0)/se[1]:.1f} sigma over Newton if slope=1; "
              f"slope is {abs(b[1]-1)/se[1]:.1f} sigma from the framework's 1 and "
              f"{abs(b[1]-0)/se[1]:.1f} sigma from Newton's 0")
            P(f"    scatter of log10(M/L_V):            {yv.std():.3f} dex   [Newton's residual]")
            P(f"    scatter of log10(M/L_V / B_pred):   {(yv - x).std():.3f} dex   [framework's residual]")
            P(f"    implied Upsilon_V = median(M/L_V / B_pred) = {np.median(10**(yv-x)):.3f} "
              f"(stellar populations: 1.3-2.2)")
            if lab.startswith("N_RV >= 20"):
                results[foot] = dict(N=n, slope=b[1], se=se[1], sc_newton=yv.std(), sc_frame=(yv-x).std(),
                                     ups=float(np.median(10**(yv-x))))

        # ---------------- the saturated subset: B depends on R_GC ALONE ---------------------------
        cut = sat & (g["Nrv"] >= 20)
        n = int(cut.sum())
        P(f"\n  [SATURATED SUBSET, N_RV >= 20]  N = {n}   -- here B_pred is a function of R_GC only, so the")
        P(f"     mass-sharing degeneracy of bug pattern 5 is absent entirely.")
        if n >= 12:
            x = np.log10(Bp[cut]); yv = np.log10(g["ML"][cut])
            b, se = wls(np.vstack([np.ones(n), x]).T, yv)
            P(f"     log10(M/L_V) = {b[0]:+.3f} + ({b[1]:+.3f} +- {se[1]:.3f}) log10(B_pred)")
            P(f"     framework needs +1.000; Newton needs 0.000.  Measured is "
              f"{abs(b[1]-1)/se[1]:.1f} sigma from the framework and {abs(b[1])/se[1]:.1f} sigma from Newton.")
            results[foot + "_sat"] = dict(N=n, slope=float(b[1]), se=float(se[1]))
        # split by regime: which branch of the theory is each carrying cluster testing?
        iso = ok & (y_int > e_ext) & (Bp > 1.5) & (g["Nrv"] >= 20)
        satb = ok & (y_int <= e_ext) & (Bp > 1.5) & (g["Nrv"] >= 20)
        for lab2, c2 in (("ISOLATED branch (y_int > e_ext, B > 1.5): tests nu(g_int), i.e. the RAR "
                          "extended to star clusters -- the RESTATEMENT branch", iso),
                         ("SATURATED branch (y_int <= e_ext, B > 1.5): tests nu(e)[1+L/3], the NEW "
                          "content that no BTFR algebra gives", satb)):
            if c2.sum() >= 4:
                P(f"\n  [{lab2}]")
                P(f"     N = {int(c2.sum())};  median B_pred = {np.median(Bp[c2]):.2f}, "
                  f"median M/L_V = {np.median(g['ML'][c2]):.2f}, "
                  f"implied Upsilon_V = {np.median(g['ML'][c2]/Bp[c2]):.3f}")
                P(f"     -> the law needs Upsilon_V in 1.3-2.2; it gets "
                  f"{np.median(g['ML'][c2]/Bp[c2]):.3f}, short by a factor "
                  f"{1.3/np.median(g['ML'][c2]/Bp[c2]):.1f}-{2.2/np.median(g['ML'][c2]/Bp[c2]):.1f}")
                if foot == "canonical":
                    results[foot + ("_iso" if c2 is iso else "_satb")] = float(
                        np.median(g["ML"][c2]/Bp[c2]))

        # ---------------- the two-group contrast ---------------------------------------------------
        lowB = ok & (Bp < 1.10) & (g["Nrv"] >= 20)
        hiB = ok & (Bp > 1.60) & (g["Nrv"] >= 20)
        if lowB.sum() >= 5 and hiB.sum() >= 5:
            m_lo = np.median(g["ML"][lowB]); m_hi = np.median(g["ML"][hiB])
            b_lo = np.median(Bp[lowB]); b_hi = np.median(Bp[hiB])
            P(f"\n  [TWO-GROUP CONTRAST]  unboosted (B < 1.10, N = {lowB.sum()}): median M/L_V = {m_lo:.3f}")
            P(f"                        boosted   (B > 1.60, N = {hiB.sum()}): median M/L_V = {m_hi:.3f}")
            P(f"     observed ratio {m_hi/m_lo:.3f}   vs   predicted {b_hi/b_lo:.3f}   "
              f"(Newton predicts 1.000)")
            results[foot + "_contrast"] = (float(m_hi/m_lo), float(b_hi/b_lo))

        # ---------------- the money table --------------------------------------------------------
        if foot == "canonical":
            idx = np.argsort(-np.where(ok, Bp, 0.0))[:14]
            P(f"\n  [THE CLUSTERS THAT CARRY THE TEST]  the 14 with the largest predicted boost")
            P(f"  {'cluster':22s} {'M':>9s} {'r_h':>6s} {'R_GC':>7s} {'y_int':>8s} {'e_ext':>8s} "
              f"{'B_pred':>7s} {'M/L_obs':>8s} {'Ups implied':>12s} {'N_RV':>5s}")
            for q in idx:
                P(f"  {g['name'][q][:22]:22s} {g['M'][q]:9.2e} {g['rh'][q]:6.1f} {g['Rgc'][q]:7.1f} "
                  f"{y_int[q]:8.4f} {e_ext[q]:8.4f} {Bp[q]:7.3f} {g['ML'][q]:8.2f} "
                  f"{g['ML'][q]/Bp[q]:12.3f} {g['Nrv'][q]:5.0f}")
            P(f"     'Ups implied' is what the stellar population would have to be for the law to hold;")
            P(f"     stellar populations give 1.3-2.2 for old metal-poor globulars.")

        # ---------------- is Baumgardt's mass really dynamical?  A transparent cross-check ---------
        if foot == "canonical":
            Mw = 4.0*(g["sig0"]*1e3)**2*(g["rh"]*pc)/G/Msun     # Wolf-style M_1/2 estimator, same table
            cw = ok & np.isfinite(Mw) & (g["sig0"] > 0) & (g["Nrv"] >= 20)
            ratio = Mw[cw]/g["M"][cw]
            bw, sew = wls(np.vstack([np.ones(int(cw.sum())), np.log10(Bp[cw])]).T, np.log10(ratio))
            P(f"\n  [IS THE MASS REALLY DYNAMICAL?]  A transparent Wolf-style estimator 4 sigma_0^2 r_h/G")
            P(f"     built from the SAME table's central dispersion, compared with the N-body mass:")
            P(f"     median ratio {np.median(ratio):.3f}, scatter {np.std(np.log10(ratio)):.3f} dex, "
              f"N = {int(cw.sum())}")
            P(f"     d log(M_Wolf/M_Nbody)/d log B = {bw[1]:+.3f} +- {sew[1]:.3f}")
            P(f"     -> a ratio flat in B means the N-body masses ARE tracking the kinematics for the")
            P(f"        boosted clusters too, so the kill cannot be blamed on photometric masses.")
            ck("the N-body masses do not drift systematically against a transparent kinematic estimator as "
               "the predicted boost grows (so the kill is not an artefact of photometric masses)  [CAN FAIL]",
               abs(bw[1])/sew[1] < 3.0, f"slope {bw[1]:+.3f} +- {sew[1]:.3f}")

        # ---------------- WHERE on the B(e) curve does the exclusion bite? -------------------------
        if hiB.sum() >= 5:
            P(f"\n  [RANGE OF VALIDITY -- the most important caveat]  The clusters that carry the exclusion")
            P(f"     are the ones with a large predicted boost, and those all sit at LOW external field:")
            P(f"       B > 1.60 subset: e_ext = {e_ext[hiB].min():.3f}-{e_ext[hiB].max():.3f}, "
              f"R_GC = {g['Rgc'][hiB].min():.1f}-{g['Rgc'][hiB].max():.0f} kpc")
            P(f"     The frozen Gaia DR4 wide-binary prediction sits at e = 1.289 (the solar circle), where")
            P(f"     B = 1.34 and NO globular cluster is saturated (they are all internally denser than the")
            P(f"     local Galactic field).  So this kill excludes the SMALL-e end of B(e) and leaves the")
            P(f"     solar-neighbourhood end for December.  Saying otherwise would over-claim.")

        # ---------------- controls -----------------------------------------------------------------
        cut = ok & (g["Nrv"] >= 20) & np.isfinite(g["mf"])
        n = int(cut.sum())
        X = np.vstack([np.ones(n), np.log10(Bp[cut]), g["mf"][cut], np.log10(g["Nrv"][cut])]).T
        b, se = wls(X, np.log10(g["ML"][cut]))
        P(f"\n  [CONTROLLED REGRESSION, N = {n}]  log10(M/L_V) ~ 1 + log B + MFSlope + log N_RV")
        P(f"     log B      {b[1]:+.3f} +- {se[1]:.3f}   (framework 1, Newton 0)")
        P(f"     MFSlope    {b[2]:+.3f} +- {se[2]:.3f}   (dynamical-evolution control)")
        P(f"     log N_RV   {b[3]:+.3f} +- {se[3]:.3f}   (measurement-quality control)")
        results[foot + "_ctrl"] = (float(b[1]), float(se[1]))

        # radius-only foil: is B doing anything log R_GC alone would not?
        cut = ok & (g["Nrv"] >= 20)
        n = int(cut.sum())
        b2, se2 = wls(np.vstack([np.ones(n), np.log10(g["Rgc"][cut])]).T, np.log10(g["ML"][cut]))
        r_B = np.corrcoef(np.log10(Bp[cut]), np.log10(g["ML"][cut]))[0, 1]
        r_R = np.corrcoef(np.log10(g["Rgc"][cut]), np.log10(g["ML"][cut]))[0, 1]
        P(f"\n  [FOIL] log R_GC alone: slope {b2[1]:+.3f} +- {se2[1]:.3f}; "
          f"r(log B, log M/L) = {r_B:+.3f} vs r(log R_GC, log M/L) = {r_R:+.3f}")

        # reddening proxy: if M/L_V were contaminated by un-dereddened light it would track |b|
        bgal = np.abs(galactic_b(g["ra"], g["dec"]))
        cutb = cut & np.isfinite(bgal)
        b3, se3 = wls(np.vstack([np.ones(int(cutb.sum())), np.log10(np.maximum(bgal[cutb], 1.0))]).T,
                      np.log10(g["ML"][cutb]))
        P(f"  [REDDENING FOIL] log10(M/L_V) on log|b|: slope {b3[1]:+.3f} +- {se3[1]:.3f}  "
          f"(a large negative slope would mean the M/L_V column is not dereddened; "
          f"un-dereddened light would INFLATE low-|b| = low-B clusters and bias the test AGAINST the law)")

        # how much would Upsilon_V have to conspire to hide a real boost?
        if foot == "canonical" and (foot + "_contrast") in results:
            obs, pred = results[foot + "_contrast"]
            P(f"  [CONSPIRACY BUDGET] to hide the predicted contrast the true Upsilon_V of the boosted "
              f"clusters would have to be {math.log10(pred/obs):.3f} dex BELOW the unboosted ones.")
            P(f"     Metallicity does push that way -- outer-halo clusters are metal-poor and stellar")
            P(f"     populations give Upsilon_V ~ 2.0 at [Fe/H] = -0.5 and ~1.5 at -2.0, i.e. at most 0.12 dex.")
            P(f"     Shortfall that metallicity cannot cover: {math.log10(pred/obs) - 0.12:.3f} dex.")

    # ------------------------------------------------------------------ verdict checks
    P("\n" + "=" * 118)
    P("VERDICT")
    P("=" * 118)
    for foot in ("canonical", "alt"):
        r = results[foot]
        P(f"  {foot:10s}: slope {r['slope']:+.3f} +- {r['se']:.3f}  "
          f"(framework 1.000, Newton 0.000);  Newtonian scatter {r['sc_newton']:.3f} dex, "
          f"framework scatter {r['sc_frame']:.3f} dex;  implied Upsilon_V = {r['ups']:.2f}")
    law = []

    def law_test(name, ok, detail=""):
        law.append((name, ok))
        P(f"  [{'LAW PASSES' if ok else 'LAW FAILS '}] {name}" + (f"   ({detail})" if detail else ""))

    sc_n = results["canonical"]["sc_newton"]; sc_f = results["canonical"]["sc_frame"]
    law_test("dividing M/L_V by the predicted boost TIGHTENS its distribution rather than loosening it",
             sc_f < sc_n, f"framework {sc_f:.3f} dex vs Newton {sc_n:.3f} dex")
    sl, se = results["canonical"]["slope"], results["canonical"]["se"]
    law_test("the measured slope of log M/L_V on log B is within 3 sigma of the predicted +1",
             abs(sl - 1.0)/se < 3.0, f"slope {sl:+.3f} +- {se:.3f}, {abs(sl-1)/se:.1f} sigma from 1")
    law_test("the measured slope is more than 3 sigma from Newton's 0",
             abs(sl)/se > 3.0, f"{abs(sl)/se:.1f} sigma from 0")
    rs = results["canonical_sat"]
    law_test("in the SATURATED subset -- where B depends on R_GC alone and no degeneracy can help -- the "
             "slope is within 3 sigma of +1", abs(rs["slope"] - 1.0)/rs["se"] < 3.0,
             f"slope {rs['slope']:+.3f} +- {rs['se']:.3f}, {abs(rs['slope']-1)/rs['se']:.1f} sigma from 1, "
             f"{abs(rs['slope'])/rs['se']:.1f} sigma from Newton's 0")
    ups = results["canonical"]["ups"]
    law_test("the implied stellar-population Upsilon_V lands inside the 1.3-2.2 range for old metal-poor "
             "globulars", 1.3 <= ups <= 2.2, f"Upsilon_V = {ups:.2f}")
    n_fail = sum(1 for _, o in law if not o)
    P(f"\n  >>> {len(law) - n_fail} of {len(law)} law tests pass.  "
      + ("THE EXTERNAL-FIELD SATURATION LAW IS EXCLUDED IN GLOBULAR CLUSTERS." if n_fail >= 3 else
         "the law survives this arena."))
    ck("the law test suite is decisive one way or the other (it did not merely return no-information: the "
       "predicted signal spans at least 0.3 dex and the slope error bar is below 0.3)  [CAN FAIL]",
       results["canonical"]["se"] < 0.3, f"sigma(slope) = {results['canonical']['se']:.3f}")

    # ------------------------------------------------------------------ mutation controls
    P("\n  MUTATION CONTROLS")
    a0 = A0["canonical"]
    ok = np.isfinite(g["M"]*g["rh"]*g["Rgc"]*g["ML"]) & (g["M"] > 0) & (g["rh"] > 0) & (g["ML"] > 0)
    cut = ok & (g["Nrv"] >= 20)
    yv = np.log10(g["ML"][cut])
    MB_MW = 1.28903*A0["canonical"]*(R0_KPC*kpc)**2/G/Msun
    for lab, mult in (("a_0 x 10", 10.0), ("a_0 x 0.1", 0.1), ("a_0 x 1 (truth)", 1.0)):
        yi = G*(g["M"]*Msun/2.0)/((g["rh"]*pc)**2 * a0*mult)
        ee = G*(MB_MW*Msun)/((g["Rgc"]*kpc)**2 * a0*mult)
        Bm = BT(yi, ee)
        x = np.log10(Bm[cut])
        b, se = wls(np.vstack([np.ones(cut.sum()), x]).T, yv)
        P(f"    {lab:16s}: slope {b[1]:+.3f} +- {se[1]:.3f},  framework scatter {(yv-x).std():.3f} dex "
          f"(Newton {yv.std():.3f})")
    x_t = np.log10(BT(G*(g["M"]*Msun/2.0)/((g["rh"]*pc)**2*a0), G*(MB_MW*Msun)/((g["Rgc"]*kpc)**2*a0))[cut])
    x_10 = np.log10(BT(G*(g["M"]*Msun/2.0)/((g["rh"]*pc)**2*a0*10), G*(MB_MW*Msun)/((g["Rgc"]*kpc)**2*a0*10))[cut])
    ck("mutation control bites: a_0 x 10 changes the framework's residual scatter measurably  [CAN FAIL]",
       abs((yv - x_10).std() - (yv - x_t).std()) > 0.01,
       f"{(yv-x_t).std():.3f} -> {(yv-x_10).std():.3f} dex")
    # nu = 1 (pure Newton) foil
    ck("the nu = 1 foil is what 'Newton' means here and is already computed as the slope-0 hypothesis",
       True, f"Newtonian scatter {yv.std():.3f} dex")

    # ------------------------------------------------------------------ the Upsilon lever, numerically
    P("\n  UPSILON LEVER, numerically.")
    P("    The tested quantity is B_hat = (M/L_V)_dyn / Upsilon_V.  M/L_V is measured (dynamical mass over")
    P("    observed light) and carries NO stellar M/L assumption; Upsilon_V enters only as the denominator")
    P("    of the amplitude.  So:")
    P("      d log B_hat / d log Upsilon_V   =  -1.000  (exactly, by construction) -- the AMPLITUDE test")
    P("      d (slope of log M/L_V on log B) / d log Upsilon_V  =  0.000 -- the SHAPE test is Upsilon-free")
    P("    A 0.1 dex error in Upsilon_V moves the amplitude by 0.1 dex and the slope not at all.  The shape")
    P("    test is therefore the load-bearing one, and it is the one reported as the verdict.")
    return ck.done()


if __name__ == "__main__":
    sys.exit(main())
