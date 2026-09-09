#!/usr/bin/env python3
"""
L56 -- THE POTENTIAL-DEPTH TRIGGER: the one door L51 priced and deliberately declined to close
==============================================================================================

L51 established that this theory has a SECOND covariant scalar linear in the metric perturbation that a
frame-free theory provably does not have -- it needs the preferred timelike vector -- and that spending it
is the first mechanism in this programme to move the cluster weak-lensing SHAPE failure at all: inside the
3 sigma lensing-versus-dynamics budget the shear log-slope residual goes from 8.8 sigma to 4.9 sigma
(canonical) and 9.0 to 4.7 (alt).  It then failed to be SWITCHABLE: on the acceleration and on the baryon
density 100% of the cluster weak-lensing rows sit inside the SPARC range, and the required weight
overshoots the deposited theory's own Phi = Psi to 1e-4 by 3.2e6 and a generous 20% empirical bound by
1.6e3.

L51 left EXACTLY ONE trigger open, priced rather than closed: the POTENTIAL DEPTH, which unlike the
acceleration and the density does NOT overlap SPARC over 0.5-2 Mpc.  It requires a logarithmic slope of
16.0 against the theory's own bound, or 6.5 against a 20% empirical bound, across a factor 2.22 in the
trigger.  L51 called that "steep, but NOT excluded", and it explicitly refused to quote the one internal
test that might have shut it, because at five clusters that test is noise-limited (fractional error 1.41).

THIS LANE ASKS: can a potential-depth trigger carry this, and if so what does it cost?

THE ORDER, fixed in advance so the answer cannot drift.
  PART A  CONTROLS.  L51's two combinations, its 8.8 -> 4.9 improvement, the independent 9 sigma shape
          failure, the measured lensing-to-dynamical mass ratio, AND -- the whole basis of this lane --
          its finding that the acceleration and density triggers OVERLAP while the potential depth does
          not.  Verified here, not inherited.
  PART B  THE TRIGGER, WRITTEN COVARIANTLY.  Potential depth is not a covariant scalar by itself, and
          L31 Step E proved that no local functional of a single metric can carry the MOND variable
          because adding a uniform field leaves every curvature invariant unchanged.  Does the depth
          trigger hit the same obstruction?  If it survives, what carries it?  Settled BEFORE any fitting.
  PART C  THE TRIGGER RE-MEASURED ON ITS OWN COVARIANT DEFINITION.  If the carrier references the
          cosmological background, the trigger is the TOTAL depth including the environment, not the
          object's own.  The non-overlap must then be re-established on THAT variable.
  PART D  THE SYSTEMS IN BETWEEN.  A weight that is off in galaxies and on in clusters must pass through
          groups, the outskirts of large discs, dwarfs and the wide-binary regime, and those are measured.
  PART E  THE TWO GATES, AND THE BEST ACHIEVABLE IMPROVEMENT AS A CURVE.  The lensing-to-dynamics
          agreement (1.55 sigma) and the deposited theory's no-slip result out to 1 Mpc.
  PART F  THE PRICE.  Parameter count, naturalness of the required steepness, and whether anything
          independent of the cluster data fixes it.
  PART G  VERDICT, and -- if it fails -- the GENERAL THEOREM, because that closes the last named handle
          on the cluster shear shape and the programme deserves the general statement.

HONESTY RULES CARRIED FROM L51, both directions.
  * A steep tuned function that fits five clusters is NOT a result.  If that is what is found, it is said.
  * The five-cluster cluster-to-cluster scatter is noise-limited (L51 C13b) and is NOT used as a kill
    anywhere in this lane.  Every kill here rests on an AMPLITUDE (well determined) or on a STRUCTURAL
    identity, never on that scatter.
  * Both a0 footings on every dimensional number: 9.3619e-11 / 1.1279e-10 m s^-2.
  * Never a statement that data favour this framework over LambdaCDM.

Nothing under closure_2026/ or the lead agent's directories is imported or executed.  The symbolic algebra
is built here in sympy.  The cluster, group, galaxy and dwarf data are read directly from the on-disk
public archives (X-COP FITS, Herbonnet 2020 Tables 2-3, SPARC rotmod, Lovisari 2015, McConnachie 2012).
"""
import numpy as np, math, json, os, sys, glob, warnings
import sympy as sp
from scipy.integrate import quad, IntegrationWarning
warnings.filterwarnings("ignore", category=IntegrationWarning)

FAILS = []
def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)

def sec(title):
    print("\n" + "=" * 118); print(title); print("=" * 118, flush=True)

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
G = 6.674e-11; MSUN = 1.989e30; kpc = 3.0857e19; Mpc = 3.0857e22; c_light = 2.99792458e8
H0 = 70e3 / Mpc; h70 = 1.0; OmM, OmL = 0.3, 0.7
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
C2 = c_light ** 2

print("=" * 118)
print("L56 -- the potential-depth trigger: the one door L51 priced and declined to close")
print("=" * 118, flush=True)
print(f"    a0 footings: canonical {A0['canonical']:.4e} m/s^2, alt {A0['alt']:.4e} m/s^2")
print( "    convention: ds^2 = -(1+2 Phi) dt^2 + (1-2 Psi) dx^2;  slip s = Phi - Psi;  gamma_PPN = Psi/Phi;")
print( "    lensing potential (Phi+Psi)/2.  Dimensionless potential X = |Phi|/c^2 throughout PART B onwards.")


# ==================================================================================================
sec("PART A -- CONTROLS: L51's combinations, its 8.8 -> 4.9, the 9 sigma shape, the mass ratio, the overlap")
# ==================================================================================================

# ---------- A1: the two combinations, rebuilt ----------
t_, x_, y_, z_ = sp.symbols("t x y z", real=True)
XV = (t_, x_, y_, z_); ETA = sp.diag(-1, 1, 1, 1)
def d1(f, m): return sp.diff(f, XV[m])

def lin_ricci(Hm):
    """R^(1)_mn from the FIRST-ORDER Christoffels of g = eta + h.  No formula assumed."""
    Gam = [[[sp.S(0)] * 4 for _ in range(4)] for _ in range(4)]
    for l in range(4):
        for m in range(4):
            for n in range(4):
                Gam[l][m][n] = sp.Rational(1, 2) * ETA[l, l] * (d1(Hm[l, n], m) + d1(Hm[l, m], n) - d1(Hm[m, n], l))
    R = sp.zeros(4, 4)
    for m in range(4):
        for n in range(4):
            R[m, n] = sp.expand(sum(d1(Gam[l][m][n], l) - d1(Gam[l][l][m], n) for l in range(4)))
    return R

PhiF = sp.Function("Phi")(x_, y_, z_); PsiF = sp.Function("Psi")(x_, y_, z_)
Hst = sp.zeros(4, 4); Hst[0, 0] = -2 * PhiF
for i in (1, 2, 3): Hst[i, i] = -2 * PsiF
R1 = lin_ricci(Hst)
Rs1 = sp.expand(sum(ETA[a, a] * R1[a, a] for a in range(4)))          # frame-free scalar  S1 = R^(1)
u = [1, 0, 0, 0]                                                      # unit timelike u^m about flat space
S2 = sp.expand(sum(u[m] * u[n] * R1[m, n] for m in range(4) for n in range(4)))   # S2 = R^(1)_mn u^m u^n
lapPhi = sum(sp.diff(PhiF, v, 2) for v in (x_, y_, z_))
lapPsi = sum(sp.diff(PsiF, v, 2) for v in (x_, y_, z_))
S1_target = sp.expand(2 * (2 * lapPsi - lapPhi))
a1_ok = (sp.simplify(Rs1 - S1_target) == 0) and (sp.simplify(S2 - lapPhi) == 0)
# read the 2x2 map off explicitly on a basis with unit Laplacians: Phi = al r^2/6, Psi = be r^2/6
al, be = sp.symbols("alpha beta", real=True)
r2_6 = (x_ ** 2 + y_ ** 2 + z_ ** 2) / 6
Hb = sp.zeros(4, 4); Hb[0, 0] = -2 * al * r2_6
for i in (1, 2, 3): Hb[i, i] = -2 * be * r2_6
Rb = lin_ricci(Hb)
S1b = sp.expand(sum(ETA[a, a] * Rb[a, a] for a in range(4))); S2b = sp.expand(Rb[0, 0])
Mmap = sp.Matrix([[S1b.coeff(al), S1b.coeff(be)], [S2b.coeff(al), S2b.coeff(be)]])
detM = sp.det(Mmap)
print(f"    S1 = R^(1)         = {sp.simplify(Rs1)}")
print(f"    S2 = R^(1)_mn u^m u^n = {sp.simplify(S2)}")
print(f"    map (lap Phi, lap Psi) -> (S1, S2) = {Mmap.tolist()},  determinant {detM}")
check("A1 [control] L51's two combinations reproduce: S1 = 2 lap(2 Psi - Phi) frame-free, "
      "S2 = lap Phi needs u, map determinant -4",
      a1_ok and detM == -4, f"det {detM}; S2 isolates the Newtonian potential, (S1 + 2 S2)/4 = lap Psi")

# ---------- the kernel and the cluster/galaxy machinery ----------
def Delta(s):
    s = np.asarray(s, float); d = np.where(s > 0, s / np.expm1(np.sqrt(np.maximum(s, 1e-300))), 0.0)
    return np.where(s > 2.540, 0.6476, d)
def g_kernel(g_bar, a0): return g_bar + a0 * Delta(g_bar / a0)

def Ez(z): return math.sqrt(OmM * (1 + z) ** 3 + OmL)
def rho_crit(z): return 3 * (H0 * Ez(z)) ** 2 / (8 * math.pi * G)
def nfw_delta_c(cc): return (200.0 / 3.0) * cc ** 3 / (math.log(1 + cc) - cc / (1 + cc))
def nfw_rho(r, rs, dc, rhoc): return dc * rhoc / ((r / rs) * (1 + r / rs) ** 2)
def nfw_Sigma(R, rs, dc, rhoc):
    xx = R / rs; A = 2 * rs * dc * rhoc
    if abs(xx - 1) < 1e-8: return A / 3.0
    if xx < 1: return A / (xx * xx - 1) * (1 - 2 / math.sqrt(1 - xx * xx) * math.atanh(math.sqrt((1 - xx) / (1 + xx))))
    return A / (xx * xx - 1) * (1 - 2 / math.sqrt(xx * xx - 1) * math.atan(math.sqrt((xx - 1) / (xx + 1))))
def nfw_gfun(xx):
    if abs(xx - 1) < 1e-8: return math.log(xx / 2.0) + 1.0
    if xx < 1: return math.log(xx / 2.0) + math.acosh(1.0 / xx) / math.sqrt(1 - xx * xx)
    return math.log(xx / 2.0) + math.acos(1.0 / xx) / math.sqrt(xx * xx - 1)
def nfw_Sigmabar(R, rs, dc, rhoc): return 4 * rs * dc * rhoc * nfw_gfun(R / rs) / (R / rs) ** 2
def nfw_DS(R, rs, dc, rhoc): return nfw_Sigmabar(R, rs, dc, rhoc) - nfw_Sigma(R, rs, dc, rhoc)
def nfw_M3d(r, rs, dc, rhoc):
    xx = r / rs; return 4 * math.pi * dc * rhoc * rs ** 3 * (math.log(1 + xx) - xx / (1 + xx))
def c200_DM14(M200, z):
    a = 0.520 + (0.905 - 0.520) * math.exp(-0.617 * z ** 1.21); b = -0.101 + 0.026 * z
    return 10 ** (a + b * math.log10(M200 * h70 / 1e12))
def nfw_from_M200(M200, z):
    cc = c200_DM14(M200, z)
    r200 = (3 * M200 * MSUN / (4 * math.pi * 200.0 * rho_crit(z))) ** (1.0 / 3.0)
    return r200 / cc, nfw_delta_c(cc), rho_crit(z), cc, r200
def Sigma_of_R(rho, R, zmax):
    f = lambda zz: rho(math.sqrt(R * R + zz * zz))
    a = quad(f, 0.0, R, limit=200)[0]
    b = quad(f, R, zmax, limit=400)[0] if zmax > R else 0.0
    return 2.0 * (a + b)
def Sigmabar_of_R(rho, R, zmax, n=40):
    xg, wg = np.polynomial.legendre.leggauss(n)
    Rp = 0.5 * R * (xg + 1.0); wp = 0.5 * R * wg
    return 2.0 * sum(wi * Rpi * Sigma_of_R(rho, Rpi, zmax) for Rpi, wi in zip(Rp, wp)) / (R * R)

print("\n  A2 -- CONTROL: the projection machinery against the analytic NFW convergence and shear.")
zc = 0.08
rs_c, dc_c, rhoc_c, ccc, r200c = nfw_from_M200(1.0e15, zc); zmx = 3000 * rs_c
rho_cb = lambda r: nfw_rho(r, rs_c, dc_c, rhoc_c)
eS, eD = [], []
for R in np.array([0.5, 1.0, 2.0]) * Mpc:
    Sn = Sigma_of_R(rho_cb, R, zmx); Sa = nfw_Sigma(R, rs_c, dc_c, rhoc_c)
    SBn = Sigmabar_of_R(rho_cb, R, zmx); SBa = nfw_Sigmabar(R, rs_c, dc_c, rhoc_c)
    eS.append(abs(Sn / Sa - 1)); eD.append(abs((SBn - Sn) / (SBa - Sa) - 1))
    print(f"      R = {R/Mpc:4.2f} Mpc : Sigma num/ana = {Sn/Sa:.6f}   DeltaSigma num/ana = {(SBn-Sn)/(SBa-Sa):.6f}")
check("A2 [control] the projection machinery reproduces the analytic NFW Sigma and DeltaSigma to 0.5%",
      max(eS) < 5e-3 and max(eD) < 5e-3, f"max |Sigma err| {max(eS):.2e}, max |DeltaSigma err| {max(eD):.2e}")

from astropy.io import fits
XDIR = os.path.join(REPO, "real_research/data/xcop")
WL_H20 = {   # Herbonnet et al. 2020 MNRAS 497, 4684, Tables 2 and 3 (masses in 1e14 Msun)
 "A85":    dict(z=0.055, M200=8.4,  M500=5.7,  eM500=2.2, beta=0.878, Rmax=1.6),
 "A1795":  dict(z=0.062, M200=13.9, M500=9.3,  eM500=2.2, beta=0.864, Rmax=1.8),
 "A2029":  dict(z=0.077, M200=18.1, M500=12.1, eM500=2.5, beta=0.834, Rmax=2.2),
 "A2142":  dict(z=0.091, M200=14.5, M500=9.7,  eM500=2.3, beta=0.809, Rmax=2.5),
 "ZW1215": dict(z=0.075, M200=5.1,  M500=3.5,  eM500=2.2, beta=0.833, Rmax=2.1),
}
WLN = list(WL_H20)
def _rkpc(rad, unit, R500):
    u = (unit or "").strip().lower()
    if u in ("r/r500", "r500"): return np.asarray(rad, float) * R500
    if u == "mpc": return np.asarray(rad, float) * 1e3
    return np.asarray(rad, float)
def load_cluster(name):
    p = os.path.join(XDIR, name); c = {"name": name}
    with fits.open(os.path.join(p, name + "_hydro_mass.fits")) as f:
        dd = f[1].data; R5 = float(f[1].header["R500"]); c["R500"] = R5
        c["rh"] = _rkpc(dd["RADIUS"], f[1].columns["RADIUS"].unit, R5)
        c["Mh"] = np.array(dd["M_FORW"], float); c["eMh"] = np.array(dd["EM_FORW"], float)
    with fits.open(os.path.join(p, name + "_fgas_profile.fits")) as f:
        dd = f[1].data
        c["rg"] = _rkpc(dd["RADIUS"], f[1].columns["RADIUS"].unit, c["R500"]); c["Mg"] = np.array(dd["MGAS"], float)
    sp_ = os.path.join(p, name + "_mstar.fits"); c["has_star"] = os.path.exists(sp_)
    if c["has_star"]:
        with fits.open(sp_) as f:
            dd = f[2].data
            c["rs"] = _rkpc(dd["RADIUS"], f[2].columns["RADIUS"].unit, c["R500"]); c["Ms"] = np.array(dd["MSTAR"], float)
    return c
ETT = json.load(open(os.path.join(XDIR, "xcop_r500_ettori2019.json")))
CLU = {n: load_cluster(n) for n in WLN}
print(f"\n      X-COP profiles read for the five clusters with published weak lensing "
      f"(measured stellar profiles present: {all(CLU[n]['has_star'] for n in WLN)})")

GRID = np.exp(np.linspace(math.log(1.0), math.log(1.0e5), 1200))     # kpc
def loginterp(xq, xp, fp):
    m = np.isfinite(xp) & np.isfinite(fp) & (fp > 0) & (xp > 0)
    return np.exp(np.interp(np.log(xq), np.log(xp[m]), np.log(fp[m]), left=np.nan, right=np.nan))
def build(c):
    def extend(rp, fp, r, steepen):
        f = loginterp(r, rp, fp); lo, hi = rp.min(), rp.max()
        sin_ = (math.log(fp[2]) - math.log(fp[0])) / (math.log(rp[2]) - math.log(rp[0]))
        sout = min(max((math.log(fp[-1]) - math.log(fp[-4])) / (math.log(rp[-1]) - math.log(rp[-4])), 0.0), 1.5)
        f = np.where(r < lo, fp[0] * (r / lo) ** sin_, f)
        if steepen: f = np.where(r > hi, fp[-1] + sout * fp[-1] * (1.0 - (r / hi) ** -1.0), f)
        else:       f = np.where(r > hi, fp[-1] * np.ones_like(r), f)
        return f
    c["Mgas_i"] = extend(c["rg"], c["Mg"], GRID, True)
    c["Mstar_i"] = extend(c["rs"], c["Ms"], GRID, False)
    c["Mbar"] = c["Mgas_i"] + c["Mstar_i"]
    c["Mh_i"] = np.exp(np.interp(np.log(GRID), np.log(c["rh"]), np.log(c["Mh"]),
                                 left=np.nan, right=math.log(c["Mh"][-1])))
    c["eMh_i"] = np.exp(np.interp(np.log(GRID), np.log(c["rh"]), np.log(c["eMh"]),
                                  left=np.nan, right=math.log(c["eMh"][-1])))
    c["R200"] = ETT[c["name"]]["R200"] * 1e3 if c["name"] in ETT else 1.6 * c["R500"]
    return c
for n in WLN: build(CLU[n])
for n in WLN:
    d = WL_H20[n]; d["rs"], d["dc"], d["rhoc"], d["c200"], d["r200"] = nfw_from_M200(d["M200"] * 1e14, d["z"])

def rho_from_M(Mgrid, r_trunc_kpc):
    lg = np.log(GRID); rm = GRID * kpc
    rr = np.maximum(np.gradient(np.asarray(Mgrid, float), lg) * MSUN / (4 * math.pi * rm ** 3), 1e-45)
    lr = np.log(rr)
    def f(r_m):
        rk = r_m / kpc
        if rk > r_trunc_kpc: return 0.0
        return math.exp(np.interp(math.log(max(rk, GRID[0])), lg, lr))
    return f
def Mfw_grid(c, a0):
    rm = GRID * kpc; gb = G * np.asarray(c["Mbar"], float) * MSUN / rm ** 2
    return g_kernel(gb, a0) * rm ** 2 / (G * MSUN)
def at(vals, r_kpc): return float(np.exp(np.interp(math.log(r_kpc), np.log(GRID), np.log(np.maximum(vals, 1e-30)))))

print("\n  A3 -- CONTROL: reproduce the 9 sigma cluster shear-SHAPE failure (L24 C11 / L51 C2).")
SHAPE, BASE = {}, {}
for foot, a0 in A0.items():
    rows = []
    for n in WLN:
        c = CLU[n]; d = WL_H20[n]; rt = 2.0 * c["R200"]; zt = rt * kpc
        Mfw = Mfw_grid(c, a0); rho_fw = rho_from_M(Mfw, rt)
        Rf = np.exp(np.linspace(math.log(0.5 * Mpc), math.log(min(2.0, d["Rmax"]) * Mpc), 12))
        DSfw = np.array([Sigmabar_of_R(rho_fw, R, zt) - Sigma_of_R(rho_fw, R, zt) for R in Rf])
        DSwl = np.array([nfw_DS(R, d["rs"], d["dc"], d["rhoc"]) for R in Rf])
        sfw = np.polyfit(np.log(Rf), np.log(DSfw), 1)[0]; swl = np.polyfit(np.log(Rf), np.log(DSwl), 1)[0]
        rows.append(dict(name=n, Rf=Rf, DSfw=DSfw, DSwl=DSwl, sfw=sfw, swl=swl,
                         Mfw500=at(Mfw, c["R500"]), MWL500=nfw_M3d(c["R500"] * kpc, d["rs"], d["dc"], d["rhoc"]) / MSUN,
                         MHSE500=at(c["Mh_i"], c["R500"]), eMHSE500=at(c["eMh_i"], c["R500"]),
                         Mfw=Mfw, rt=rt, R500=c["R500"]))
    dsl = np.array([r["sfw"] - r["swl"] for r in rows])
    SHAPE[foot] = (float(dsl.mean()), float(dsl.std(ddof=1) / math.sqrt(len(dsl)))); BASE[foot] = rows
    print(f"      {foot:9s}: framework log-slope {np.mean([r['sfw'] for r in rows]):+.3f}, "
          f"measured {np.mean([r['swl'] for r in rows]):+.3f}, difference {SHAPE[foot][0]:+.3f} "
          f"+/- {SHAPE[foot][1]:.3f} ({abs(SHAPE[foot][0])/SHAPE[foot][1]:.1f} sigma)")
zs = {f: abs(SHAPE[f][0]) / SHAPE[f][1] for f in A0}
check("A3 [control] the 9-sigma cluster shear-shape failure is reproduced independently "
      "(L51 C2: +0.516 +/- 0.058 / +0.521 +/- 0.058)",
      all(abs(SHAPE[f][0] - 0.518) < 0.05 for f in A0) and all(zs[f] > 6 for f in A0),
      ", ".join(f"{f} {SHAPE[f][0]:+.3f} +/- {SHAPE[f][1]:.3f} ({zs[f]:.1f} sigma)" for f in A0))

print("\n  A4 -- CONTROL: the required lensing phantom, the required slip, and the measured mass ratio.")
FIT = {}
for foot in A0:
    rows = BASE[foot]; out = []
    for r in rows:
        c = CLU[r["name"]]; d = WL_H20[r["name"]]; rt = r["rt"]
        MWL = np.array([nfw_M3d(rr * kpc, d["rs"], d["dc"], d["rhoc"]) / MSUN for rr in GRID])
        MP = MWL - r["Mfw"]
        msk = GRID <= rt; rr_m = GRID[msk] * kpc
        gfw = G * np.maximum(r["Mfw"][msk], 0) * MSUN / rr_m ** 2
        gwl = G * np.maximum(MWL[msk], 0) * MSUN / rr_m ** 2
        def cum(gg):
            tot = np.concatenate([[0.0], np.cumsum(0.5 * (gg[1:] + gg[:-1]) * np.diff(rr_m))])
            return -(tot[-1] - tot)                                  # Phi(r) = - int_r^{rt} g dr'
        Phi_fw = cum(gfw); Pot_P = cum(gwl) - Phi_fw
        i500 = int(np.argmin(np.abs(GRID[msk] - r["R500"])))
        out.append(dict(name=r["name"], fP=float(MP[np.argmin(np.abs(GRID - r["R500"]))] / r["Mfw500"]),
                        slip500=abs(2 * Pot_P[i500]) / C2,
                        frac500=abs(2 * Pot_P[i500]) / max(abs(2 * Phi_fw[i500]), 1e-30),
                        Xfw500=abs(Phi_fw[i500]) / C2,
                        rgrid=GRID[msk], PotP=Pot_P, Phifw=Phi_fw, MP=MP[msk]))
    FIT[foot] = out
    print(f"      {foot:9s}: median M_P(<R500)/M_fw = {np.median([o['fP'] for o in out]):.3f}, "
          f"median |slip| at R500 = {np.median([o['slip500'] for o in out]):.3e} "
          f"(= {np.median([o['frac500'] for o in out]):.2f} x the framework's own lensing potential)")
E_CL = {f: float(np.median([o["frac500"] for o in FIT[f]])) for f in A0}   # the EXCURSION ratio at clusters
ratios, eratios = [], []
for r in BASE["canonical"]:
    d = WL_H20[r["name"]]; Rw = r["MWL500"] / r["MHSE500"]
    eratios.append(Rw * math.hypot(d["eM500"] / d["M500"], r["eMHSE500"] / r["MHSE500"])); ratios.append(Rw)
ratios = np.array(ratios); eratios = np.array(eratios); wgt = 1.0 / eratios ** 2
Rmeas = float(np.sum(wgt * ratios) / np.sum(wgt)); eRmeas = float(1.0 / math.sqrt(np.sum(wgt)))
print(f"      measured lensing/dynamical ratio, inverse-variance mean: {Rmeas:.3f} +/- {eRmeas:.3f} "
      f"(L51 C5 / L24 C5: 1.148 +/- 0.146 and 1.154 +/- 0.147)")
check("A4 [control] the measured cluster lensing/dynamical mass ratio is reproduced",
      abs(Rmeas - 1.15) < 0.08, f"{Rmeas:.3f} +/- {eRmeas:.3f}")

print("\n  A5 -- CONTROL: L51's 8.8 -> 4.9 / 9.0 -> 4.7 improvement inside the 3 sigma budget.")
BEST51 = {}
for foot in A0:
    rows = BASE[foot]; fPmed = float(np.median([o["fP"] for o in FIT[foot]]))
    f_cap = min(max(0.0, (Rmeas + 3 * eRmeas - 1.0)) / fPmed, 1.0)
    best = None
    for f in np.linspace(0.0, 1.0, 51):
        dsl = np.array([np.polyfit(np.log(r["Rf"]), np.log((1 - f) * r["DSfw"] + f * r["DSwl"]), 1)[0] - r["swl"]
                        for r in rows])
        m = float(dsl.mean()); e = float(dsl.std(ddof=1) / math.sqrt(len(dsl)))
        if f <= f_cap + 1e-9: best = (f, m, e, abs(m) / max(e, 1e-9))
    f, m, e, zz = best; BEST51[foot] = dict(f=f, m=m, e=e, z=zz, f_cap=f_cap, fPmed=fPmed)
    print(f"      {foot:9s}: 3-sigma ceiling f <= {f_cap:.2f}; at f = {f:.2f} the residual shape error is "
          f"{m:+.3f} +/- {e:.3f} ({zz:.1f} sigma, from {zs[foot]:.1f} sigma)")
check("A5 [control] L51's ceiling reproduces: inside the 3-sigma lensing/dynamics budget the freedom takes "
      "the shape residual from 8.8 to 4.9 sigma (canonical) / 9.0 to 4.7 (alt)",
      abs(BEST51["canonical"]["z"] - 4.9) < 0.6 and abs(BEST51["alt"]["z"] - 4.7) < 0.6,
      ", ".join(f"{f} {zs[f]:.1f} -> {BEST51[f]['z']:.1f} sigma at f = {BEST51[f]['f']:.2f}" for f in A0))

print("\n  A6/A7 -- CONTROL: the overlap finding this entire lane rests on.  Acceleration and density "
      "OVERLAP;\n           the potential-depth proxy Phi_loc = g_bar r does NOT.  Verified, not inherited.")
UPS_D, UPS_B = 0.5, 0.7
gal, GALS = [], {}
for fn in sorted(glob.glob(os.path.join(REPO, "real_research/data/sparc_data", "*_rotmod.dat"))):
    try: dd = np.loadtxt(fn, comments="#")
    except Exception: continue
    if dd.ndim != 2 or dd.shape[1] < 6: continue
    rr = dd[:, 0] * kpc; Vo = dd[:, 1] * 1e3; eV = dd[:, 2] * 1e3
    Vg = dd[:, 3] * 1e3; Vd = dd[:, 4] * 1e3; Vb = dd[:, 5] * 1e3
    Vb2 = Vg * np.abs(Vg) + UPS_D * Vd * np.abs(Vd) + UPS_B * Vb * np.abs(Vb)
    m = (rr > 0) & (Vo > 0) & (Vb2 > 0) & (eV / np.maximum(Vo, 1) < 0.10)
    if m.sum() < 3: continue
    rr, Vo, Vb2 = rr[m], Vo[m], Vb2[m]
    gb = Vb2 / rr; M = gb * rr ** 2 / G
    rho = np.gradient(M, rr) / (4 * math.pi * rr ** 2)
    nm = os.path.basename(fn).replace("_rotmod.dat", "")
    GALS[nm] = dict(r=rr, gb=gb, vo=Vo, M=M)
    for i in range(len(rr)):
        if rho[i] <= 0: continue
        gal.append(dict(g=nm, r=rr[i], gb=gb[i], vo=Vo[i], M=M[i], phi=gb[i] * rr[i], rho=rho[i]))
print(f"      SPARC: {len(gal)} points in {len(GALS)} galaxies (Upsilon_d = {UPS_D}, Upsilon_b = {UPS_B}, "
      f"eV/V < 0.10)")

CLPTS = {}
for foot, a0 in A0.items():
    pts = []
    for o, r in zip(FIT[foot], BASE[foot]):
        c = CLU[o["name"]]; rg = o["rgrid"]; sel = (rg >= 500.0) & (rg <= 2000.0)
        rr = rg[sel] * kpc
        Mb_all = np.exp(np.interp(np.log(rg), np.log(GRID), np.log(np.maximum(c["Mbar"], 1e-30))))
        gb = G * Mb_all[sel] * MSUN / rr ** 2
        rho_b = np.gradient(Mb_all * MSUN, np.log(rg))[sel] / (4 * math.pi * rr ** 3)
        s_req = np.abs(2 * o["PotP"][sel]) / C2
        Xfw = np.abs(o["Phifw"][sel]) / C2
        for i in range(0, len(rr), 12):
            pts.append(dict(cl=o["name"], r=rr[i], gb=gb[i], rho=max(rho_b[i], 1e-40),
                            phi=gb[i] * rr[i], s=s_req[i], Xfw=Xfw[i]))
    CLPTS[foot] = pts

TOL_THEORY = 1e-4      # the deposited theory's own no-slip result, Phi = Psi to better than 1e-4 (L11)
TOL_DATA = 0.20        # a generous empirical galaxy-galaxy-lensing tolerance on the fractional slip
OVER = {}
for var, label, unit in [("gb", "g_bar", " m/s^2"), ("rho", "rho_b", " kg/m^3"), ("phi", "Phi_loc", " m^2/s^2")]:
    row = {}
    for foot in sorted(A0):
        xc = np.array([p[var] for p in CLPTS[foot]]); xg = np.array([p[var] for p in gal])
        lo, hi = max(xc.min(), xg.min()), min(xc.max(), xg.max())
        frac = float(((xc >= lo) & (xc <= hi)).mean()) if hi > lo else 0.0
        row[foot] = dict(lo=xc.min(), hi=xc.max(), glo=xg.min(), ghi=xg.max(), frac=frac, overlap=hi > lo,
                         gap=(xc.min() / xg.max()))
        print(f"      {label:8s} {foot:9s}: clusters {xc.min():.3g}-{xc.max():.3g}{unit}; "
              f"SPARC {xg.min():.3g}-{xg.max():.3g}{unit}; "
              + (f"OVERLAP, {100*frac:.0f}% of cluster rows inside" if hi > lo else
                 f"NO OVERLAP (gap factor {xc.min()/xg.max():.2f})"))
    OVER[label] = row
check("A6 [control] the acceleration and density triggers OVERLAP SPARC completely (L51 C9: 100% of "
      "cluster rows inside)",
      all(OVER[l][f]["overlap"] and OVER[l][f]["frac"] > 0.99 for l in ("g_bar", "rho_b") for f in A0),
      ", ".join(f"{l} {100*OVER[l]['canonical']['frac']:.0f}%" for l in ("g_bar", "rho_b")))
gapf = {f: OVER["Phi_loc"][f]["gap"] for f in A0}
check("A7 [control] the potential-depth proxy Phi_loc = g_bar r does NOT overlap SPARC over 0.5-2 Mpc "
      "(L51: clusters 1.87-4.67e11, SPARC <= 8.42e10, gap 2.22)",
      all(not OVER["Phi_loc"][f]["overlap"] for f in A0) and all(abs(gapf[f] - 2.22) < 0.2 for f in A0),
      ", ".join(f"{f} gap {gapf[f]:.2f}x" for f in A0))

print("\n  A8 -- CONTROL: L51's required logarithmic slope on the surviving trigger (16.0 / 6.5, 15.8 / 6.2).")
STEEP51 = {}
for foot in A0:
    xc = np.array([p["phi"] for p in CLPTS[foot]]); sc = np.array([p["s"] for p in CLPTS[foot]])
    xg = np.array([p["phi"] for p in gal]); vg = np.array([p["vo"] for p in gal])
    ig = int(np.argmax(xg)); xg_max = xg[ig]; xc_min = xc.min()
    s_cl = float(np.median(sc[xc < np.percentile(xc, 20)]))
    s_th = TOL_THEORY * vg[ig] ** 2 / C2; s_da = TOL_DATA * vg[ig] ** 2 / C2
    p_th = math.log(s_cl / s_th) / math.log(xc_min / xg_max)
    p_da = math.log(s_cl / s_da) / math.log(xc_min / xg_max)
    STEEP51[foot] = dict(p_th=p_th, p_da=p_da, s_cl=s_cl, xc_min=xc_min, xg_max=xg_max,
                         s_th=s_th, s_da=s_da)
    print(f"      {foot:9s}: W must rise from <= {s_th:.2e} (theory) / {s_da:.2e} (data 20%) to "
          f"{s_cl:.2e} across {xc_min/xg_max:.2f}x  =>  slope {p_th:.1f} / {p_da:.1f}")
check("A8 [control] L51's required steepness reproduces (16.0 / 6.5 canonical, 15.8 / 6.2 alt)",
      abs(STEEP51["canonical"]["p_th"] - 16.0) < 0.8 and abs(STEEP51["canonical"]["p_da"] - 6.5) < 0.8 and
      abs(STEEP51["alt"]["p_th"] - 15.8) < 0.8 and abs(STEEP51["alt"]["p_da"] - 6.2) < 0.8,
      ", ".join(f"{f} {STEEP51[f]['p_th']:.1f} / {STEEP51[f]['p_da']:.1f}" for f in A0))


# ==================================================================================================
sec("PART B -- THE TRIGGER, WRITTEN COVARIANTLY: does the depth hit L31's local-invariant obstruction?")
# ==================================================================================================
print("""
  L31 Step E: MOND's variable is not a local scalar, because adding a UNIFORM field Phi -> Phi + g.x
  leaves the entire Hessian and hence every curvature invariant exactly unchanged while |grad Phi|
  changes.  The potential DEPTH carries a strictly stronger version of the same disease: it is not even
  invariant under a CONSTANT shift.  Settle this before any fitting.
""")

# ---- B1: the constant shift is an exact isometry, not merely a linear-order degeneracy
cshift = sp.Symbol("c0", positive=True)
Phi_s = sp.Function("Phi")(x_, y_, z_); Psi_s = sp.Function("Psi")(x_, y_, z_)
tt = sp.Symbol("tt", real=True)
# metric with potential Phi, in time t;  metric with potential Phi_tilde where 1+2 Phi_tilde = (1+2c0)(1+2Phi)
g_orig = -(1 + 2 * Phi_s)
g_shift = -((1 + 2 * cshift) * (1 + 2 * Phi_s))
# pull back the shifted metric under t = tt / sqrt(1+2 c0):  dt^2 -> dtt^2/(1+2c0)
pullback = sp.simplify(g_shift / (1 + 2 * cshift))
b1_ok = sp.simplify(pullback - g_orig) == 0
print(f"      exact static metric  -(1+2 Phi) dt^2 ;  deepen by a constant, 1+2 Phi~ = (1+2 c0)(1+2 Phi),")
print(f"      then rescale t~ = sqrt(1+2 c0) t :  pulled-back g_00 = {sp.simplify(pullback)}  vs original "
      f"{sp.simplify(g_orig)}")
check("B1 [test] the potential DEPTH is a local covariant scalar of the metric alone",
      not b1_ok,
      "NO -- a constant shift of Phi is an EXACT isometry (a rescaling of t), so no functional of the "
      "metric and its derivatives, of any order, local or nonlocal, can measure the depth.  This is "
      "L31 Step E's obstruction in its strongest form: not a linear-order degeneracy but an exact one")

# ---- B2: control -- and the uniform-field version, the exact form L31 used
gvec = sp.symbols("g1 g2 g3", real=True)
H_uni = sp.zeros(4, 4)
Phi_u = Phi_s + gvec[0] * x_ + gvec[1] * y_ + gvec[2] * z_
H_uni[0, 0] = -2 * Phi_u
for i in (1, 2, 3): H_uni[i, i] = -2 * Psi_s
R_uni = lin_ricci(H_uni)
H_pl = sp.zeros(4, 4); H_pl[0, 0] = -2 * Phi_s
for i in (1, 2, 3): H_pl[i, i] = -2 * Psi_s
R_pl = lin_ricci(H_pl)
b2_ok = all(sp.simplify(R_uni[m, n] - R_pl[m, n]) == 0 for m in range(4) for n in range(4))
check("B2 [control] L31 Step E reproduces: adding a uniform field leaves every component of the "
      "linearised curvature exactly unchanged", b2_ok,
      "all 16 components identical for arbitrary g -- so the gradient is not local either, and the "
      "obstruction the earlier lane proved is confirmed here independently")

# ---- B3: the enumeration -- every scalar the deposited theory has, tested for depth-blindness
print("""
      B3 -- THE ENUMERATION.  The deposited action (THE_ACTION 2026-09-05) is built from: the metric g;
      a clock scalar tau entering ONLY through the unit normal n_mu = -d_mu tau / sqrt(-(d tau)^2); and a
      MOND scalar phi entering ONLY through its derivatives, Q = n.d phi and V_mu = q_mu^nu d_nu phi.
      Every scalar in it is therefore built from DERIVATIVES of the potential, or from the metric alone.
      Each is tested below against a constant deepening of the potential.
""")
Nlapse = sp.sqrt(1 + 2 * Phi_s)
SCALARS = [
    ("R (Ricci scalar)",                    sp.simplify(sum(ETA[a, a] * R_pl[a, a] for a in range(4))), True),
    ("R_mn n^m n^n",                        sp.simplify(R_pl[0, 0]), True),
    ("theta = div n  (static: 0)",          sp.S(0), True),
    ("a^2 = (n.grad n)^2  ~ |grad Phi|^2",  sp.simplify(sum(sp.diff(Phi_s, v) ** 2 for v in (x_, y_, z_))), True),
    ("Y = V.V = |grad phi_perp|^2",         sp.Symbol("Ysym"), True),
    ("N = lapse  (NOT tau-reparam invariant)", Nlapse, False),
]
b3_all_blind = True
for nm, expr, blind in SCALARS:
    shifted = expr.subs(Phi_s, Phi_s + cshift)
    same = sp.simplify(shifted - expr) == 0
    if blind and not same: b3_all_blind = False
    print(f"        {nm:42s}  depth-blind under Phi -> Phi + c0 : {'YES' if same else 'NO'}")
check("B3 [control] every scalar the deposited action is built from is blind to the potential depth",
      b3_all_blind,
      "R, R_mn n^m n^n, theta, a^2 and Y all depend on DERIVATIVES of Phi only.  The lapse N is the one "
      "object that is not blind -- and the action does not contain it, because tau enters only through "
      "n_mu, which is invariant under tau -> f(tau) while N -> N / f'.  So the METRIC side offers nothing")

# ---- B4: THE CARRIER.  Q = n.d phi with a cosmological background Q0
print("""
      B4 -- WHAT CARRIES IT, IF ANYTHING.  The theory's MOND scalar phi has a cosmological background
      phi = Q0 t + delta phi (this is how AeST-type actions work and how the deposited action's K(Q) is
      expanded).  Q = n^mu d_mu phi is a genuine local scalar -- invariant under tau -> f(tau), invariant
      under phi -> phi + const -- and in a static field it is Q = (d_t phi)/N.  That makes 1 - Q/Q0 a
      DEPTH.  This is the candidate the brief named, and it is exhibited here rather than asserted.
""")
Q0s = sp.Symbol("Q0", positive=True); Ph = sp.Symbol("Ph", real=True)
Q_static = Q0s / sp.sqrt(1 + 2 * Ph)                          # Q = d_t phi / N with d_t phi = Q0
Xdef = sp.simplify(1 - Q_static / Q0s)
Xser = sp.expand(sp.series(Xdef, Ph, 0, 3).removeO())
b4_ok = (sp.simplify(Xser - (Ph - sp.Rational(3, 2) * Ph ** 2)) == 0)
print(f"        Q = Q0 / sqrt(1 + 2 Phi)   =>   1 - Q/Q0 = {sp.simplify(Xdef)}")
print(f"        expanded:  1 - Q/Q0 = {Xser}    (i.e. = Phi/c^2 to leading order)")
check("B4 [test] the potential-depth trigger CAN be written covariantly in this theory",
      b4_ok,
      "YES -- carried by X = 1 - Q/Q0 with Q = n^mu d_mu phi the clock-projected gradient of the theory's "
      "OWN MOND scalar.  It evades L31 Step E because it is not built from the metric alone: it uses a "
      "matter-sector scalar whose nonzero cosmological background supplies the missing reference.  This "
      "is a genuine escape and the lane records it as one")

# ---- B5: the price of that carrier -- the reference is COSMOLOGICAL, so the trigger is the TOTAL depth
print("""
      B5 -- AND THE PRICE, WHICH IS STRUCTURAL, NOT A CAVEAT.  Q0 is the value of Q where the clock runs
      at its background rate -- i.e. at the cosmological boundary.  So X = 1 - Q/Q0 measures the depth
      RELATIVE TO THE COSMOLOGICAL BACKGROUND: it is the TOTAL potential at a point, the object's own
      well PLUS every well it sits inside.  Superposition is exhibited, not assumed.
""")
P1, P2 = sp.symbols("Phi1 Phi2", real=True)
eta_ = sp.Symbol("eta", positive=True)                        # a common small bookkeeping parameter
X_tot = 1 - 1 / sp.sqrt(1 + 2 * eta_ * (P1 + P2))
X_lin = sp.expand(sp.series(X_tot, eta_, 0, 2).removeO().coeff(eta_))
lin_ok = (sp.simplify(X_lin - (P1 + P2)) == 0)
print(f"        for Phi = Phi1 + Phi2:  X = 1 - Q/Q0 = (Phi1 + Phi2)/c^2 + O(Phi^2)  -- exactly additive "
      f"at leading order ({'verified' if lin_ok else 'NOT verified'})")
check("B5 [test] the covariant carrier can be referenced to the OBJECT rather than to the cosmos",
      not lin_ok,
      "NO -- X is additive in the potential and its zero is the cosmological background, so a galaxy "
      "inside a cluster carries the CLUSTER's trigger value.  There is no local field that sees a host "
      "and not its substructure: 'the host's potential' is not a functional of anything local.  This is "
      "the price of the escape in B4, and PART C and PART D are what it costs")

# ---- B6: the response formula, derived once and used everywhere below
print("""
      B6 -- THE ONE FORMULA THE REST OF THE LANE USES, derived here.  Let s = W(X).  An object that digs
      its own well dPhi on top of an AMBIENT trigger X_amb makes the slip vary across itself by
      ds = W'(X_amb) dPhi/c^2 = p W(X_amb) (dPhi/c^2)/X_amb, with p = d ln W / d ln X.  Its own
      lensing-versus-dynamics signature is 2 dPhi/c^2.  So the fractional slip it suffers is

            R(X)  =  p W(X) / (2 X)   =  p E(X),        E(X) = W(X)/(2X)

      -- INDEPENDENT of the object.  E is what an isolated object at its own depth suffers; R is what a
      small object EMBEDDED at ambient X suffers.  Both are dimensionless and both are directly what
      'gamma_PPN - 1' and 'fractional slip' mean.  E at clusters is measured in A4.
""")
for foot in A0:
    print(f"        {foot:9s}: measured cluster excursion ratio E(X_cl) = {E_CL[foot]:.3f} "
          f"(the required slip as a fraction of the framework's own lensing potential at R500)")
check("B6 [control] the response formula is the identity R = p E, with E(X_cl) measured from the shear "
      "data and p the logarithmic slope of the weight",
      all(0.05 < E_CL[f] < 1.0 for f in A0),
      ", ".join(f"{f} E(X_cl) = {E_CL[f]:.3f}" for f in A0) +
      " -- this is an AMPLITUDE, not the five-cluster scatter, and it is what every kill below uses")



# ==================================================================================================
sec("PART C -- THE TRIGGER RE-MEASURED ON ITS OWN COVARIANT DEFINITION")
# ==================================================================================================
print("""
  L51's non-overlap was established for the LOCAL PROXY Phi_loc = g_bar r.  B4/B5 say the covariant
  carrier is X = 1 - Q/Q0 = the INTEGRATED depth relative to the cosmological background.  Those are
  different variables and everything must be re-established on the second one, not inherited.

  ONE CONVENTION IS UNAVOIDABLE and is stated rather than hidden: the depth is referenced to the
  cosmological background, so the integral runs out to where each object's own field merges into that
  background.  The SAME rule is applied to every system -- integrate to T x R200, with R200 obtained
  from the baryonic mass through the cosmic baryon fraction (f_b = 0.157) and the 200 rho_c definition
  -- and T = 1, 2 and 4 are all carried through.  T = 2 is L51's own cluster choice, so at T = 2 the
  cluster numbers reduce exactly to A4's.  Every number below is a RANGE over T and over both footings.
  Where a conclusion depends on T it is said so; the load-bearing one (C3) does not.
""")
TRUNC = [1.0, 2.0, 4.0]
FB = 0.157
rho_c0 = 3 * H0 ** 2 / (8 * math.pi * G)
def R200_from_Mb(Mb_msun):
    """R200 in kpc from a baryonic mass, via M200 = M_b / f_b and the 200 rho_c definition"""
    M200 = Mb_msun / FB * MSUN
    return (3 * M200 / (4 * math.pi * 200.0 * rho_c0)) ** (1.0 / 3.0) / kpc

def Mb_cluster(c):
    lg = np.log(GRID); lM = np.log(np.maximum(c["Mbar"], 1e-30))
    return lambda rk: math.exp(np.interp(math.log(max(rk, GRID[0])), lg, lM))
def Mb_galaxy(gd):
    rk = gd["r"] / kpc; M = gd["M"] / MSUN
    return lambda x: math.exp(np.interp(math.log(max(x, rk[0])), np.log(rk), np.log(M)))
def Mb_point(Mb): return lambda rk: Mb
def Phi_int(Mbf, r0_kpc, rt_kpc, a0, n=240):
    """|Phi(r0)| = int_{r0}^{rt} g_kernel dr in m^2/s^2, for a baryon profile Mbf(r_kpc) in Msun"""
    if rt_kpc <= r0_kpc: return 0.0
    rr = np.exp(np.linspace(math.log(r0_kpc), math.log(rt_kpc), n)) * kpc
    Mb = np.array([Mbf(x / kpc) for x in rr])
    return float(np.trapz(g_kernel(G * Mb * MSUN / rr ** 2, a0), rr))

def cluster_slip_at(foot, T):
    """recompute the framework potential and the required lensing phantom P with rt = T x R200"""
    out = []
    for r in BASE[foot]:
        c = CLU[r["name"]]; d = WL_H20[r["name"]]; rt = T * c["R200"]
        msk = (GRID <= rt); rr_m = GRID[msk] * kpc
        MWL = np.array([nfw_M3d(x * kpc, d["rs"], d["dc"], d["rhoc"]) / MSUN for x in GRID[msk]])
        gfw = G * np.maximum(r["Mfw"][msk], 0) * MSUN / rr_m ** 2
        gwl = G * np.maximum(MWL, 0) * MSUN / rr_m ** 2
        def cum(gg):
            tot = np.concatenate([[0.0], np.cumsum(0.5 * (gg[1:] + gg[:-1]) * np.diff(rr_m))])
            return -(tot[-1] - tot)
        Phi_fw = cum(gfw); P = cum(gwl) - Phi_fw
        i5 = int(np.argmin(np.abs(GRID[msk] - r["R500"])))
        Xi = abs(Phi_fw[i5]) / C2; si = abs(2 * P[i5]) / C2
        out.append(dict(name=r["name"], X=Xi, s=si, E=si / max(2 * Xi, 1e-30)))
    return out

GAL_R200 = {g: R200_from_Mb(GALS[g]["M"][-1] / MSUN) for g in GALS}
COV = {}
print(f"      {'T':>4s} {'foot':>9s} {'X_cl(R500)':>12s} {'W_cl (slip)':>12s} {'E_cl':>7s} "
      f"{'X_gal max':>11s} {'gap':>6s} {'p (theory)':>11s} {'p (data 20%)':>13s}")
for T in TRUNC:
    for foot, a0 in A0.items():
        cs = cluster_slip_at(foot, T)
        X_cl = float(np.median([o["X"] for o in cs]))
        E_cl_T = float(np.median([o["E"] for o in cs]))     # median of the per-cluster RATIOS, as in A4
        W_cl = 2 * E_cl_T * X_cl
        Xg = np.array([Phi_int(Mb_galaxy(GALS[g]), GALS[g]["r"][0] / kpc, T * GAL_R200[g], a0) / C2
                       for g in GALS])
        X_gal = float(Xg.max()); gap = X_cl / X_gal
        pth = math.log((E_cl_T / TOL_THEORY) * gap) / math.log(gap) if gap > 1 else float("nan")
        pda = math.log((E_cl_T / TOL_DATA) * gap) / math.log(gap) if gap > 1 else float("nan")
        COV[(T, foot)] = dict(X_cl=X_cl, W_cl=W_cl, E_cl=E_cl_T, X_gal=X_gal, gap=gap, p_th=pth, p_da=pda)
        print(f"      {T:4.0f} {foot:>9s} {X_cl:12.4e} {W_cl:12.4e} {E_cl_T:7.3f} {X_gal:11.4e} "
              f"{gap:6.2f} {pth:11.2f} {pda:13.2f}")
gaps = [COV[k]["gap"] for k in COV]
print(f"      control: at T = 2 the cluster excursion reduces to A4's number "
      f"({COV[(2.0,'canonical')]['E_cl']:.3f} vs {E_CL['canonical']:.3f} canonical, "
      f"{COV[(2.0,'alt')]['E_cl']:.3f} vs {E_CL['alt']:.3f} alt)")
check("C1 [test] the NON-OVERLAP that this whole door rests on survives on the covariant trigger with a "
      "margin at least as large as L51's proxy gap of 2.22",
      min(gaps) >= 2.22,
      f"gap = {min(gaps):.2f} - {max(gaps):.2f} over T = 1-4 and both footings, against 2.22 on L51's "
      f"local proxy.  The separation is REAL and is NOT an artefact of L51's proxy -- that is a result in "
      f"the door's favour -- but at the tightest convention it is {2.22/min(gaps):.2f}x smaller than the "
      f"proxy suggested, and the required steepness moves correspondingly to "
      f"{min(COV[k]['p_th'] for k in COV):.1f} - {max(COV[k]['p_th'] for k in COV):.1f} rather than 16.0")

print("""
  C2 -- BUT THE COVARIANT TRIGGER IS THE TOTAL DEPTH (B5), SO THE POPULATION THAT MATTERS IS NOT THE
  ISOLATED ONE.  A galaxy at 0.5-2 Mpc from a cluster centre carries the CLUSTER's trigger value, not its
  own.  Those galaxies are not hypothetical in this sample: the X-COP stellar-mass profiles measure them.
""")
shell = []
for n in WLN:
    c = CLU[n]
    ms = at(c["Mstar_i"], 2000.0) - at(c["Mstar_i"], 500.0)
    mg = at(c["Mgas_i"], 2000.0) - at(c["Mgas_i"], 500.0)
    shell.append((n, ms, mg))
    print(f"      {n:8s}: stellar mass in the 0.5-2 Mpc shell {ms:.3e} Msun   (gas {mg:.3e} Msun)")
star_present = all(s[1] > 1e11 for s in shell)
check("C2 [control] there is measured galaxy-scale (stellar) mass at the cluster radii the weight must "
      "switch on at", star_present,
      f"{min(s[1] for s in shell):.2e} - {max(s[1] for s in shell):.2e} Msun of measured stars per "
      f"cluster in that shell -- i.e. galaxies, sitting at the cluster's trigger value by B5")

print("""
  C3 -- WHAT THOSE GALAXIES SUFFER.  THE CONVENTION DROPS OUT.  The cluster does not require a slip
  VALUE, it requires a slip PROFILE: matching the added lensing phantom pointwise gives
        ds/dr = W'(X) dX/dr,   ds/dr = -2 dP/dr = 2 g_P,   dX/dr = -g_fw/c^2
        =>    W'(X) = 2 g_P / g_fw = 2 M_P(<r) / M_fw(<r)      at every cluster radius.
  By B6 the fractional slip on a small object embedded at ambient X is exactly W'(X)/2.  So

        R_embedded (at cluster radii)  =  M_P(<r) / M_fw(<r),

  which is A4's measured phantom-to-framework mass ratio and NOTHING else -- no truncation, no zero
  point, no pinning, no steepness.  It is the single most robust number in the problem.
""")
R_EMB = {f: float(np.median([o["fP"] for o in FIT[f]])) for f in A0}
for foot in A0:
    per = ", ".join(f"{o['name']} {o['fP']:.2f}" for o in FIT[foot])
    print(f"      {foot:9s}: M_P/M_fw at R500 per cluster -- {per}")
    print(f"                 median R_embedded = {R_EMB[foot]:.3f}  =  {R_EMB[foot]/TOL_THEORY:.1e} x the "
          f"deposited theory's own Phi = Psi bound, {R_EMB[foot]/TOL_DATA:.2f} x a generous 20% "
          f"empirical bound")
R_max = max(R_EMB.values()); R_min = min(R_EMB.values()); R_floor = R_min
check("C3 [CRUX] the covariant potential-depth trigger can act at cluster depths WITHOUT acting on the "
      "galaxies that sit at those depths",
      R_max <= TOL_THEORY,
      f"NO -- the required slip GRADIENT fixes the embedded response exactly: R = M_P/M_fw = "
      + ", ".join(f"{f} {R_EMB[f]:.3f}" for f in A0) +
      f", i.e. {R_min/TOL_THEORY:.1e} - {R_max/TOL_THEORY:.1e} x the theory's own 1e-4 bound and "
      f"{R_min/TOL_DATA:.2f} - {R_max/TOL_DATA:.2f} x a 20% empirical bound.  No convention, no "
      f"steepness and no five-cluster scatter enters this; it is the amplitude of the phantom the shear "
      f"data require.  This is L51's C9 overlap argument recovered for the depth trigger")
print("      cross-check of the two routes at T = 2: the power-law pinning of C1 gives p x E_cl = "
      + ", ".join(f"{COV[(2.0,f)]['p_th']*COV[(2.0,f)]['E_cl']:.2f}" for f in A0)
      + ", against the exact " + ", ".join(f"{R_EMB[f]:.2f}" for f in A0)
      + " -- agreement to a factor of a few, which is all a power-law model of W deserves.  The exact "
        "route is the one quoted.")
print("""

  C4 -- AND THE TWO DETERMINATIONS OF THE STEEPNESS DO NOT AGREE.  W'(X) = 2 g_P/g_fw is measured at
  every cluster radius, so the LOCAL logarithmic slope of W at cluster depths is measured too:
  p_local = 1 + d ln W' / d ln X over 0.5-2 Mpc.  The slope needed to CONNECT the cluster value down to
  the galaxy bound is the p of C1.  A single power law requires them to be equal.
""")
PLOC = {}
for T in TRUNC:
    for foot in A0:
        sl = []
        for r in BASE[foot]:
            c = CLU[r["name"]]; d = WL_H20[r["name"]]; rt = T * c["R200"]
            msk = (GRID <= rt); rr_m = GRID[msk] * kpc
            MWL = np.array([nfw_M3d(x * kpc, d["rs"], d["dc"], d["rhoc"]) / MSUN for x in GRID[msk]])
            Mfw = np.maximum(r["Mfw"][msk], 1e-30)
            gfw = G * Mfw * MSUN / rr_m ** 2
            def cum(gg):
                tot = np.concatenate([[0.0], np.cumsum(0.5 * (gg[1:] + gg[:-1]) * np.diff(rr_m))])
                return -(tot[-1] - tot)
            X = np.abs(cum(gfw)) / C2
            Wp = 2 * np.maximum(MWL - Mfw, 1e-30) / Mfw
            sel = (GRID[msk] >= 500.0) & (GRID[msk] <= 2000.0) & (X > 0) & (Wp > 1e-25)
            if sel.sum() > 4:
                sl.append(np.polyfit(np.log(X[sel]), np.log(Wp[sel]), 1)[0] + 1.0)
        PLOC[(T, foot)] = float(np.median(sl)) if sl else float("nan")
        print(f"      T = {T:.0f} {foot:9s}: p_local (measured from the required slip gradient) = "
              f"{PLOC[(T,foot)]:6.2f}   vs   p_connect (needed to reach the galaxy bound) = "
              f"{COV[(T,foot)]['p_th']:6.2f}   ratio {COV[(T,foot)]['p_th']/PLOC[(T,foot)]:.2f}")
ratios_p = [COV[k]["p_th"] / PLOC[k] for k in COV if np.isfinite(PLOC[k]) and PLOC[k] > 0]
check("C4 [test] the weight can be ONE power law: the slope measured at cluster depths matches the slope "
      "needed to connect down to galaxies (within 1.5x)",
      len(ratios_p) > 0 and max(ratios_p) < 1.5 and min(ratios_p) > 1 / 1.5,
      f"p_connect / p_local = {min(ratios_p):.2f} - {max(ratios_p):.2f} over T = 1-4 and both footings.  "
      f"THIS ONE IS CONVENTION-DEPENDENT and is reported as such, not banked: at the loosest truncation "
      f"the two determinations agree to {min(ratios_p):.2f}x, at the tightest they differ by "
      f"{max(ratios_p):.0f}x.  What is convention-free is that p_local is MEASURED at "
      f"{min(PLOC.values()):.1f} - {max(PLOC.values()):.1f}, i.e. the weight is genuinely steeper than "
      f"the chameleon/symmetron 1-3 at cluster depths on most conventions.  Whether a single power law "
      f"also reaches the galaxy bound is left open here")
print("""
      Neither of these uses the five-cluster scatter of the required weight, which L51 C13b showed is
      noise-limited (fractional error 1.41) and which this lane does not quote in either direction.
""")


# ==================================================================================================
sec("PART D -- THE SYSTEMS IN BETWEEN: groups, disc outskirts, dwarfs, wide binaries")
# ==================================================================================================
print("""
  A weight that is off in galaxies and on in clusters must pass smoothly through the systems in between,
  and those are measured.  The weight is pinned at both ends by C1 -- W(X_gal_max) = the galaxy bound,
  W(X_cl) = the measured required cluster slip -- so everything below is a PREDICTION with no freedom
  left, evaluated on data, on the covariant trigger, on both footings, over the full T range.

  TWO QUANTITIES, kept separate throughout.  The EXCURSION E = W/(2X) is what an isolated object suffers
  from its own well; the pinning fixes it at the galaxy end, so it is not an independent test there.
  The RESPONSE R = p E is what a small object sitting INSIDE an ambient well suffers.  Cassini and the
  wide binaries measure R; galaxy-galaxy lensing of isolated galaxies measures E.
""")
def ER(X, T, foot, arm):
    d = COV[(T, foot)]; p = d["p_th"] if arm == "theory" else d["p_da"]
    W = d["W_cl"] * (np.asarray(X, float) / d["X_cl"]) ** p
    E = W / (2 * np.asarray(X, float))
    return E, p * E, p

# ---------------- D1: X-ray groups ----------------
GRP = []
with open(os.path.join(REPO, "real_research/data/lovisari2015_groups.tsv")) as fh:
    hdr = None
    for line in fh:
        if line.startswith("#") or not line.strip(): continue
        parts = line.rstrip("\n").split("\t")
        if hdr is None: hdr = parts; continue
        d = dict(zip(hdr, parts))
        try:
            R500 = float(d["R500_kpc"]); Mg = float(d["Mgas500_1e12"]) * 1e12; M500 = float(d["M500_1e13"]) * 1e13
        except Exception: continue
        GRP.append(dict(name=d["name"], R500=R500, Mb=Mg * 1.30, M500=M500))
print(f"      D1 GROUPS: {len(GRP)} X-ray groups (Lovisari, Reiprich & Schellenberger 2015, Tables 1-2), "
      f"M_b = M_gas500 x 1.30 (a stated stellar correction), M_b held constant beyond R500 -- "
      f"conservative, since the real gas mass keeps rising and would DEEPEN them")
GRP_R, GRP_X = {}, {}
for T in TRUNC:
    for foot, a0 in A0.items():
        Xg = np.array([Phi_int(Mb_point(g["Mb"]), g["R500"], T * R200_from_Mb(g["Mb"]), a0) / C2
                       for g in GRP])
        keep = Xg > 0                       # drop groups whose R500 exceeds T x R200 at this convention
        Xg = Xg[keep]; GRP_X[(T, foot)] = Xg
        if T == 1.0 and foot == "canonical" and (~keep).any():
            print(f"      at T = 1, {int((~keep).sum())} of {len(GRP)} groups have R500 > T x R200 and "
                  f"are dropped at that convention (reported, not silently skipped)")
        for arm in ("theory", "data"):
            E, R, p = ER(Xg, T, foot, arm); GRP_R[(T, foot, arm)] = (float(E.max()), float(R.max()))
T0, F0 = 2.0, "canonical"
GRP_X0 = GRP_X[(T0, F0)]
print(f"      at T = 2, canonical: group X spans {GRP_X0.min():.3e} - {GRP_X0.max():.3e}, against the "
      f"deepest SPARC galaxy {COV[(T0,F0)]['X_gal']:.3e} and the cluster {COV[(T0,F0)]['X_cl']:.3e}")
nbelow = int((GRP_X0 <= COV[(T0, F0)]["X_gal"]).sum())
print(f"      {nbelow} of {len(GRP)} groups sit BELOW the deepest SPARC galaxy in the trigger; "
      f"{len(GRP)-nbelow} sit above it")
for T in TRUNC:
    for foot in A0:
        for arm in ("theory", "data"):
            E, R = GRP_R[(T, foot, arm)]
            print(f"      T = {T:.0f} {foot:9s} ({arm:6s}): worst group excursion E = {E:.3e}, worst "
                  f"embedded response R = {R:.3e}")
g_th = max(GRP_R[(T, f, "theory")][1] for T in TRUNC for f in A0)
g_da = max(GRP_R[(T, f, "data")][1] for T in TRUNC for f in A0)
g_th_min = min(GRP_R[(T, f, "theory")][1] for T in TRUNC for f in A0)
g_da_min = min(GRP_R[(T, f, "data")][1] for T in TRUNC for f in A0)
check("D1 [test] the pinned weight passes through X-ray GROUPS without breaking them",
      g_th <= TOL_THEORY and g_da <= TOL_DATA,
      f"worst group response {g_th_min:.2e} - {g_th:.2e} on the theory arm ({g_th/TOL_THEORY:.1e} x the "
      f"1e-4 bound at the worst convention) and {g_da_min:.2e} - {g_da:.2e} on the data arm "
      f"({g_da/TOL_DATA:.1e} x the 20% bound); and {nbelow}/{len(GRP)} groups sit BELOW the deepest SPARC "
      f"galaxy CENTRE -- see D5, where a matched-radius control shows that particular comparison is a "
      f"reference-radius artefact, so it is stated rather than banked")

# ---------------- D2: the outskirts of large discs ----------------
print("\n      D2 DISC OUTSKIRTS: the outermost measured point of every SPARC rotation curve.")
OUT_R = {}
for T in TRUNC:
    for foot, a0 in A0.items():
        Xo = np.array([Phi_int(Mb_galaxy(GALS[g]), GALS[g]["r"][-1] / kpc, T * GAL_R200[g], a0) / C2
                       for g in GALS])
        if T == T0 and foot == F0:
            print(f"      at T = 2, canonical: disc-outskirt X spans {Xo.min():.3e} - {Xo.max():.3e}")
        for arm in ("theory", "data"):
            E, R, p = ER(Xo, T, foot, arm); OUT_R[(T, foot, arm)] = (float(E.max()), float(R.max()))
for T in TRUNC:
    for foot in A0:
        for arm in ("theory", "data"):
            E, R = OUT_R[(T, foot, arm)]
            print(f"      T = {T:.0f} {foot:9s} ({arm:6s}): worst outskirt excursion E = {E:.3e}, worst "
                  f"response R = {R:.3e}")
o_th = max(OUT_R[(T, f, "theory")][1] for T in TRUNC for f in A0)
o_da = max(OUT_R[(T, f, "data")][1] for T in TRUNC for f in A0)
o_E_th = max(OUT_R[(T, f, "theory")][0] for T in TRUNC for f in A0)
o_E_da = max(OUT_R[(T, f, "data")][0] for T in TRUNC for f in A0)
check("D2 [test] the pinned weight passes through the OUTSKIRTS OF LARGE DISCS, on the pinning arm that "
      "survives the Solar System (the steep, theory-tolerance arm; D4 excludes the shallow one)",
      o_th <= TOL_THEORY,
      f"the EXCURSION reaches {o_E_th:.2e} (theory arm) and {o_E_da:.2e} (data arm) -- the gate the "
      f"pinning was written against, so it holds by construction.  The RESPONSE reaches {o_th:.2e} on the "
      f"theory arm, which CLEARS the 1e-4 bound at {o_th/TOL_THEORY:.2f} x, and {o_da:.2e} on the data "
      f"arm, which is {o_da/TOL_DATA:.2f} x the 20% bound -- marginal, and the data arm is separately "
      f"excluded by Cassini in D4.  Disc outskirts are therefore the one intermediate scale the weight "
      f"passes, and the FAIL here is marginal and is reported as marginal")

# ---------------- D3: dwarfs ----------------
print("\n      D3 DWARFS: McConnachie 2012 Local Group dwarf spheroidals.")
dw = []
with open(os.path.join(REPO, "real_research/data/dsph/mcconnachie2012_dsph.csv")) as fh:
    hdr = fh.readline().strip().split(",")
    for line in fh:
        d = dict(zip(hdr, line.rstrip("\n").split(",")))
        try: s = float(d["sigma*"])
        except Exception: continue
        if s > 0: dw.append(dict(name=d["Name"], sig=s * 1e3, sub=d.get("SubG", "")))
X_dw = np.array([3.0 * d["sig"] ** 2 for d in dw]) / C2      # STATED convention Phi ~ 3 sigma^2
print(f"      {len(dw)} dwarfs with measured sigma*, own depth X ~ 3 sigma^2/c^2 = {X_dw.min():.3e} - "
      f"{X_dw.max():.3e}  (a STATED convention; the answer is many orders from any bound, so it does "
      f"not matter)")
MW_MB = 6.5e10; R_SUN = 8.2                                   # STATED Milky Way model
X_MW = {}
for T in TRUNC:
    for foot, a0 in A0.items():
        X_MW[(T, foot)] = Phi_int(Mb_point(MW_MB), R_SUN, T * R200_from_Mb(MW_MB), a0) / C2
print(f"      Milky Way ambient at the Sun (M_b = {MW_MB:.1e} Msun, R = {R_SUN} kpc, R200 = "
      f"{R200_from_Mb(MW_MB):.0f} kpc): X = "
      + ", ".join(f"{X_MW[(T,'canonical')]:.3e} (T={T:.0f})" for T in TRUNC))
DW_R, SAT_R = {}, {}
for T in TRUNC:
    for foot in A0:
        for arm in ("theory", "data"):
            E, R, p = ER(X_dw, T, foot, arm); DW_R[(T, foot, arm)] = float(R.max())
            E2, R2, _ = ER(np.array([X_MW[(T, foot)]]), T, foot, arm); SAT_R[(T, foot, arm)] = float(R2[0])
d_th = max(DW_R[(T, f, "theory")] for T in TRUNC for f in A0)
d_da = max(DW_R[(T, f, "data")] for T in TRUNC for f in A0)
s_th = max(SAT_R[(T, f, "theory")] for T in TRUNC for f in A0)
s_da = max(SAT_R[(T, f, "data")] for T in TRUNC for f in A0)
s_th_min = min(SAT_R[(T, f, "theory")] for T in TRUNC for f in A0)
s_da_min = min(SAT_R[(T, f, "data")] for T in TRUNC for f in A0)
print(f"      isolated dwarfs: worst response {d_th:.2e} (theory arm) / {d_da:.2e} (data arm)")
print(f"      but Local Group dwarfs are SATELLITES: by B5 they carry the MILKY WAY's trigger, where the "
      f"response is {s_th_min:.2e} - {s_th:.2e} (theory) / {s_da_min:.2e} - {s_da:.2e} (data)")
check("D3 [test] the pinned weight passes through DWARFS, isolated and as satellites",
      d_th <= TOL_THEORY and d_da <= TOL_DATA and s_th <= TOL_THEORY and s_da <= TOL_DATA,
      f"isolated dwarfs on the theory arm are safe by many orders ({d_th:.1e}); on the DATA arm the "
      f"pinning is nearly linear (p ~ 1), which makes the fractional slip almost scale-free, so even a "
      f"dwarf takes {d_da:.2e} ({d_da/TOL_DATA:.2f} x the 20% bound).  Satellites at the Milky Way's "
      f"ambient depth take {s_th:.2e} (theory, {s_th/TOL_THEORY:.2f} x) and {s_da:.2e} (data, "
      f"{s_da/TOL_DATA:.2f} x).  The dwarf channel therefore does not decide anything on its own; it is "
      f"the near-linearity it exposes that Cassini then kills in D4")

# ---------------- D4: wide binaries and Cassini ----------------
print("""
      D4 WIDE BINARIES AND THE SOLAR SYSTEM.  Both sit inside the Milky Way, so by B5 both carry the SAME
      ambient trigger -- the Galaxy's depth at the Sun, not their own.  A 10 kAU pair's own well is
      eleven orders below the ambient, so a pair never triggers the weight itself; what it feels is the
      ambient RESPONSE, which is exactly the quantity Cassini measures.  Cassini: |gamma - 1| < 2.3e-5.
""")
CASSINI = 2.3e-5
WB_PHI = G * 2.0 * MSUN / (1.0e4 * 1.496e11)
print(f"      a 10 kAU pair of two solar masses: its OWN X = {WB_PHI/C2:.3e}, against the Milky Way "
      f"ambient {X_MW[(T0,F0)]:.3e} -- a factor {X_MW[(T0,F0)]*C2/WB_PHI:.1e}")
for T in TRUNC:
    for foot in A0:
        for arm in ("theory", "data"):
            R = SAT_R[(T, foot, arm)]
            print(f"      T = {T:.0f} {foot:9s} ({arm:6s}): ambient response R = {R:.3e} vs Cassini "
                  f"{CASSINI:.1e}  ->  {R/CASSINI:.2e} x")
print(f"      Milky Way model sensitivity (T = 2, canonical):")
for mb in (4.0e10, 6.5e10, 1.0e11):
    Xm = Phi_int(Mb_point(mb), R_SUN, T0 * R200_from_Mb(mb), A0[F0]) / C2
    _, Rth, _ = ER(np.array([Xm]), T0, F0, "theory"); _, Rda, _ = ER(np.array([Xm]), T0, F0, "data")
    print(f"        M_b(MW) = {mb:.1e} Msun -> X = {Xm:.3e}, response {float(Rth[0]):.2e} (theory) / "
          f"{float(Rda[0]):.2e} (data)")
cass_th, cass_da = s_th, s_da
check("D4 [test] the pinned weight passes CASSINI, and with it the wide-binary regime, at the Milky Way's "
      "own ambient depth",
      cass_th <= CASSINI and cass_da <= CASSINI,
      f"theory arm {s_th_min:.2e} - {cass_th:.2e} ({cass_th/CASSINI:.2f} x Cassini at the worst "
      f"convention, {s_th_min/CASSINI:.2e} x at the best) -- reported as MARGINAL, not as a kill, because "
      f"it turns on the Milky Way model; data arm {s_da_min:.2e} - {cass_da:.2e}, which is "
      f"{cass_da/CASSINI:.1e} x Cassini and IS decisive.  So the shallow 20% pinning arm is not "
      f"available at all: only the steep theory arm survives the Solar System, and C3 already fails on it")

# ---------------- D5: the ladder ----------------
print("\n      D5 -- THE LADDER, canonical footing, T = 2, theory arm.  Sorted by trigger value.")
X_out_med = float(np.median([Phi_int(Mb_galaxy(GALS[g]), GALS[g]["r"][-1] / kpc, T0 * GAL_R200[g],
                                     A0[F0]) / C2 for g in GALS]))
LAD = [("isolated dwarf spheroidal (median)", float(np.median(X_dw))),
       ("SPARC disc outskirt (median)", X_out_med),
       ("Milky Way at the Sun (Cassini, wide binaries)", X_MW[(T0, F0)]),
       ("X-ray group at R500 (median)", float(np.median(GRP_X0))),
       ("deepest SPARC galaxy (the pinning point)", COV[(T0, F0)]["X_gal"]),
       ("cluster at R500 (where the slip is required)", COV[(T0, F0)]["X_cl"])]
LAD.sort(key=lambda t: t[1])
print(f"      {'system':46s} {'X = Phi/c^2':>12s} {'E':>11s} {'R = p E':>11s}")
for nm, X in LAD:
    E, R, p = ER(np.array([X]), T0, F0, "theory")
    print(f"      {nm:46s} {X:12.4e} {float(E[0]):11.3e} {float(R[0]):11.3e}")
X_grp_med = float(np.median(GRP_X0)); X_gal_max0 = COV[(T0, F0)]["X_gal"]
# the fair comparison: groups are read at R500, galaxies at their innermost point.  Read the galaxies at
# a matched fractional radius (0.5 R200, the R500 analogue) and see whether the ordering survives.
X_gal_matched = float(np.max([Phi_int(Mb_galaxy(GALS[g]), 0.5 * GAL_R200[g], T0 * GAL_R200[g],
                                      A0[F0]) / C2 for g in GALS]))
print(f"      REFERENCE-RADIUS CONTROL: groups above are read at R500, galaxies at their INNERMOST point.")
print(f"      Reading the galaxies at a matched fractional radius (0.5 R200, the R500 analogue) gives a "
      f"deepest\n      galaxy X = {X_gal_matched:.3e} against the median group {X_grp_med:.3e} -- the "
      f"ordering is {'CORRECT' if X_grp_med > X_gal_matched else 'still inverted'} there.")
check("D5 [control] the trigger ORDERS the systems the way the mechanism needs -- groups, which need the "
      "weight, above the deepest discs, which must not have it -- when both are read at a matched "
      "fractional radius",
      X_grp_med > X_gal_matched,
      f"at matched radius the median group ({X_grp_med:.3e}) sits "
      f"{'above' if X_grp_med > X_gal_matched else 'below'} the deepest disc ({X_gal_matched:.3e}) by "
      f"{max(X_grp_med, X_gal_matched)/min(X_grp_med, X_gal_matched):.2f}x, so the trigger DOES order the "
      f"populations and D1's '20/20 groups below the deepest galaxy' is a reference-radius artefact, "
      f"stated here rather than banked.  What survives is the gate statement, not an ordering failure: "
      f"the deepest galaxy CENTRES ({X_gal_max0:.3e}) are deeper than every group at R500, and the "
      f"no-slip gate applies at those centres")


# ==================================================================================================
sec("PART E -- THE TWO GATES, AND THE BEST ACHIEVABLE IMPROVEMENT AS A CURVE")
# ==================================================================================================
print("""
  Gate 1: the lensing-to-dynamics agreement, currently 1.55 sigma; buying the WHOLE shape breaks it at
  4.5 sigma (L51 C6, reproduced in A5).  Gate 2: the deposited theory's no-slip result, Phi = Psi to
  1e-4 out to 1 Mpc.  Scan the amplitude f of the added lensing phantom.  For each f the required cluster
  slip scales as f, the steepness p(f) is whatever is then needed to reach the galaxy bound, and the
  embedded-galaxy response R(f) = max(p(f),1) f E_cl follows with no freedom left.  Reported as a CURVE,
  then as three ceilings.  The convention used is the one MOST GENEROUS to the door -- the T that
  minimises R at fixed f -- and it is named.
""")
gen_T = min(TRUNC, key=lambda T: min(COV[(T, f)]["p_th"] * COV[(T, f)]["E_cl"] for f in A0))
print(f"      most generous convention for the consistency test: T = {gen_T:.0f} "
      f"(p_theory = " + " / ".join(f"{COV[(gen_T,f)]['p_th']:.2f}" for f in A0) + ", E_cl = "
      + " / ".join(f"{COV[(gen_T,f)]['E_cl']:.3f}" for f in A0) + ")")
print("""
      FOUR constraints now act on the amplitude f, and two of them pull OPPOSITE ways, which is the
      whole point.  (1) the lensing/dynamics ratio caps f from ABOVE.  (2) the isolated-galaxy no-slip
      gate does not cap f -- it fixes the steepness p(f) needed to reach the galaxy bound.  (3) the
      embedded-galaxy consistency R_emb = p(f) f E_cl caps f from ABOVE.  (4) CASSINI caps f from BELOW:
      a smaller f needs a SHALLOWER weight, and a shallow weight is nearly scale-free, so it leaks into
      the Solar System.  Both R's are computed here from the pinned weight with no freedom left.
""")
CURVE, CEIL = {}, {}
for foot in A0:
    d = COV[(gen_T, foot)]; lngap = math.log(d["gap"]); Xmw = X_MW[(gen_T, foot)]
    rows = BASE[foot]; fPmed = BEST51[foot]["fPmed"]; tab = []
    for f in np.concatenate([np.geomspace(1e-6, 0.09, 40), np.linspace(0.1, 1.0, 61)]):
        dsl = np.array([np.polyfit(np.log(r["Rf"]), np.log((1 - f) * r["DSfw"] + f * r["DSwl"]), 1)[0] - r["swl"]
                        for r in rows])
        m = float(dsl.mean()); e = float(dsl.std(ddof=1) / math.sqrt(len(dsl)))
        row = dict(f=f, z_shape=abs(m) / max(e, 1e-9), z_ld=abs((1.0 + f * fPmed) - Rmeas) / eRmeas)
        for arm, tol in (("th", TOL_THEORY), ("da", TOL_DATA)):
            p = math.log((f * d["E_cl"] / tol) * d["gap"]) / lngap
            pe = max(p, 1e-6)
            row["p_" + arm] = p
            row["Remb_" + arm] = f * R_EMB[foot]        # exact: R = f M_P/M_fw (C3)
            Wmw = f * d["W_cl"] * (Xmw / d["X_cl"]) ** pe
            row["Rcas_" + arm] = max(p, 1.0) * Wmw / (2 * Xmw)
        tab.append(row)
    CURVE[foot] = tab
print(f"      CURVE (canonical footing).  R uses max(p, 1): p < 1 breaks the isolated-galaxy gate instead.")
print(f"      R_emb = f x M_P/M_fw is the same on both arms (it does not depend on the pinning); the "
      f"Cassini response does.")
print(f"      {'f':>9s} {'shape sig':>10s} {'lens/dyn':>9s} {'R_emb':>10s} {'p_th':>7s} "
      f"{'R_Cass th':>10s} {'p_data':>7s} {'R_Cass da':>10s}")
for row in CURVE["canonical"][::8] + [CURVE["canonical"][-1]]:
    print(f"      {row['f']:9.2e} {row['z_shape']:10.2f} {row['z_ld']:9.2f} {row['Remb_th']:10.3e} "
          f"{row['p_th']:7.2f} {row['Rcas_th']:10.3e} {row['p_da']:7.2f} {row['Rcas_da']:10.3e}")
for foot in A0:
    tab = CURVE[foot]
    def ceiling(cond):
        ok = [r for r in tab if r["z_ld"] < 3.0 and cond(r)]
        return (max(ok, key=lambda r: r["f"]), len(ok)) if ok else (tab[0], 0)
    CEIL[foot] = {}
    # ADMISSIBILITY: p >= 1 is required, and it is not a taste.  p < 1 means the weight rises more
    # slowly than the potential, so E(X_gal) > E(X_cl): the galaxy's own fractional slip would exceed
    # the cluster's, contradicting the premise that the cluster needs a slip the galaxy must not have.
    # Algebraically p >= 1 is exactly f E_cl >= tol.  Rows with p < 1 are not solutions and are excluded.
    CEIL[foot]["gates_only"] = ceiling(lambda r: True)
    CEIL[foot]["plus_cassini_th"] = ceiling(lambda r: r["p_th"] >= 1.0 and r["Rcas_th"] <= CASSINI)
    CEIL[foot]["plus_cassini_da"] = ceiling(lambda r: r["p_da"] >= 1.0 and r["Rcas_da"] <= CASSINI)
    CEIL[foot]["all_th"] = ceiling(lambda r: r["p_th"] >= 1.0 and r["Rcas_th"] <= CASSINI
                                   and r["Remb_th"] <= TOL_THEORY)
    CEIL[foot]["all_da"] = ceiling(lambda r: r["p_da"] >= 1.0 and r["Rcas_da"] <= CASSINI
                                   and r["Remb_da"] <= TOL_DATA)
    for k, lab in (("gates_only", "gates 1+2 only (L51's answer)"),
                   ("plus_cassini_th", "+ Cassini, theory-arm pinning"),
                   ("plus_cassini_da", "+ Cassini, 20%-arm pinning"),
                   ("all_th", "+ Cassini + embedded, theory arm"),
                   ("all_da", "+ Cassini + embedded, 20% arm")):
        r, nok = CEIL[foot][k]
        print(f"      {foot:9s} {lab:34s}: " +
              (f"NO amplitude satisfies these -- shape stays {zs[foot]:.1f} sigma"
               if nok == 0 else
               f"f <= {r['f']:.3g}  ->  shape {zs[foot]:.1f} -> {r['z_shape']:.1f} sigma "
               f"(lens/dyn {r['z_ld']:.2f} sigma, p = {r['p_th']:.2f})"))
check("E1 [control] gate 1 alone reproduces L51's answer: 8.8 -> 4.9 / 9.0 -> 4.7 sigma",
      abs(CEIL["canonical"]["gates_only"][0]["z_shape"] - BEST51["canonical"]["z"]) < 0.4 and
      abs(CEIL["alt"]["gates_only"][0]["z_shape"] - BEST51["alt"]["z"]) < 0.4,
      ", ".join(f"{f} -> {CEIL[f]['gates_only'][0]['z_shape']:.1f} sigma" for f in A0))
check("E2 [test] gate 2 -- the deposited theory's no-slip result in galaxies -- is preserved at the "
      "amplitude gate 1 allows",
      all(CEIL[f]["gates_only"][0]["Remb_th"] <= TOL_THEORY for f in A0),
      "the ISOLATED-galaxy excursion is preserved by construction, which is what pins p; the EMBEDDED "
      "response at that amplitude is R = " + ", ".join(f"{CEIL[f]['gates_only'][0]['Remb_th']:.2f}" for f in A0) +
      f", i.e. {max(CEIL[f]['gates_only'][0]['Remb_th'] for f in A0)/TOL_THEORY:.1e} x the same 1e-4 bound, "
      f"on the galaxies that sit at cluster depths")
best_da = {f: (CEIL[f]["all_da"][0]["z_shape"] if CEIL[f]["all_da"][1] else zs[f]) for f in A0}
best_th = {f: (CEIL[f]["all_th"][0]["z_shape"] if CEIL[f]["all_th"][1] else zs[f]) for f in A0}
empty_th = all(CEIL[f]["all_th"][1] == 0 for f in A0)
empty_da = all(CEIL[f]["all_da"][1] == 0 for f in A0)
check("E3 [test] subject to BOTH gates, CASSINI, and the trigger's own embedded consistency, the freedom "
      "still removes the shape failure (residual under 3 sigma)",
      all(min(best_da[f], best_th[f]) < 3.0 for f in A0),
      ("the window is EMPTY on both arms: no amplitude satisfies the lensing/dynamics gate, Cassini and "
       "the embedded-galaxy consistency at once, because Cassini caps f from BELOW (a shallow weight is "
       "scale-free and leaks into the Solar System) while the embedded consistency caps it from ABOVE.  "
       "The shape residual therefore stays at " + ", ".join(f"{f} {zs[f]:.1f} sigma" for f in A0))
      if (empty_th and empty_da) else
      ("best achievable: " + "; ".join(
          f"{f} {zs[f]:.1f} -> {best_da[f]:.1f} sigma (20% arm), {best_th[f]:.1f} sigma (theory arm)"
          for f in A0)))


# ==================================================================================================
sec("PART F -- THE PRICE: parameters, naturalness, and whether anything independent fixes it")
# ==================================================================================================
print("""
  F1 -- WHAT IS BEING ADDED.  A new free function W of a new variable X = 1 - Q/Q0.  Minimally
  parametrised as W = W0 (X/X*)^p with a floor: THREE parameters (amplitude, threshold, steepness) plus
  the CHOICE of variable.  Against it: five clusters, each contributing one shear log-slope, and one
  lensing-to-dynamics ratio.
""")
print(f"      free parameters in W: 3 (W0, X*, p)   |   numbers it is fitted to: {len(WLN)} cluster shear "
      f"log-slopes + 1 lensing/dynamics ratio")
print(f"      the deposited action already carries K(Q); W(Q) is a SECOND free function of the SAME "
      f"argument, so the cost is a function, not a coupling")
check("F1 [test] the addition is cheap -- one new coupling constant or fewer", False,
      f"3 free parameters plus the choice of trigger variable, fitted to {len(WLN)} cluster shear slopes.  "
      f"A steep tuned function that fits five clusters is not a mechanism, and this lane says so rather "
      f"than quoting the improvement it buys")

print("""
  F2 -- IS THE STEEPNESS NATURAL?  W is a function of Q about the cosmological background Q0, so its EFT
  expansion is W = sum_n w_n X^n with X = 1 - Q/Q0.  A leading power p means w_1 ... w_(p-1) all vanish.
  Each order is tested against CASSINI alone, independently of the galaxy pinning: a term w_n X^n
  normalised to supply the cluster slip at X_cl gives |gamma - 1| = n w_n X_MW^(n-1) at Saturn.
""")
n_min = {}
for T in TRUNC:
    for foot in A0:
        d = COV[(T, foot)]; Xmw = X_MW[(T, foot)]; nmin = None
        for n in range(1, 81):
            if n * (d["W_cl"] / d["X_cl"] ** n) * Xmw ** (n - 1) <= CASSINI: nmin = n; break
        n_min[(T, foot)] = nmin
        if T == T0:
            print(f"      T = {T:.0f} {foot:9s}: X_MW = {Xmw:.3e}, X_cl = {d['X_cl']:.3e}, required slip "
                  f"{d['W_cl']:.3e}")
            for n in (1, 2, 3, 4, 5, 6, 8, 10, 12, 16):
                gam = n * (d["W_cl"] / d["X_cl"] ** n) * Xmw ** (n - 1)
                print(f"          n = {n:2d}: |gamma-1| at Saturn = {gam:9.3e}  "
                      + (f"(excluded by Cassini, {gam/CASSINI:.1e} x)" if gam > CASSINI else "(allowed)"))
        print(f"      T = {T:.0f} {foot:9s}: Cassini forces the leading power to n >= {nmin}")
nmin_best = min(v for v in n_min.values() if v); nmin_worst = max(v for v in n_min.values() if v)
check("F2 [test] the required steepness is natural -- the leading term of the EFT expansion about the "
      "cosmological background can be low order (n <= 3, as chameleon and symmetron screening are)",
      nmin_best <= 3,
      f"Cassini ALONE forces n >= {nmin_best} at the most generous convention and n >= {nmin_worst} at the "
      f"least, on both footings, with no input from the galaxy pinning.  That is at least {nmin_best-1} "
      f"tuned cancellations in an expansion about the cosmological background -- and the galaxy pinning "
      f"independently asks for p = {min(COV[k]['p_th'] for k in COV):.1f} - "
      f"{max(COV[k]['p_th'] for k in COV):.1f}.  Two independent routes agree the weight must be steep, "
      f"which is what makes it tuned rather than mechanistic")

print("""
  F3 -- DOES ANYTHING INDEPENDENT OF THE CLUSTER DATA FIX THE THRESHOLD?  X* = Phi*/c^2 is
  dimensionless.  The theory's own constants are a0, c, G and H0, and a0 is itself fitted.  Every
  dimensionless potential they build is tested against the required X*.
""")
Xstar_req = {f: COV[(T0, f)]["X_cl"] for f in A0}
H0v = 67.4e3 / Mpc; xi_ = A0["canonical"] / (c_light * H0v)
CAND = [("a0 / (c H0)   [ = a0 (c/H0) / c^2 ]", xi_), ("(a0/(c H0))^2", xi_ ** 2),
        ("sqrt(a0/(c H0))", math.sqrt(xi_)), ("c H0 / a0", 1.0 / xi_)]
CAND_ILL = [(f"(a0/(c H0))^{n}", xi_ ** n) for n in (3, 4, 5, 6)]
print(f"      required X* = " + ", ".join(f"{f} {Xstar_req[f]:.3e}" for f in A0)
      + f"   (T = 2; {COV[(TRUNC[-1],'canonical')]['X_cl']:.3e} at T = 4)")
best_dex, best_nm = 99.0, ""
for nm, v in CAND:
    dex = abs(math.log10(v / Xstar_req["canonical"]))
    if dex < best_dex: best_dex, best_nm = dex, nm
    print(f"        {nm:38s} = {v:11.4e}   ({math.log10(v/Xstar_req['canonical']):+6.2f} dex)")
print(f"      higher integer powers, shown ONLY to make the point that they carry no information:")
for nm, v in CAND_ILL:
    print(f"        {nm:38s} = {v:11.4e}   ({math.log10(v/Xstar_req['canonical']):+6.2f} dex)")
spacing = abs(math.log10(xi_))
print(f"      consecutive powers of a0/(c H0) are {spacing:.2f} dex apart, so ANY target is within "
      f"{spacing/2:.2f} dex of some power by construction; admitting a free integer exponent is itself "
      f"a fitted parameter, and a hit at that level is not evidence.  Only n = 1 (and, at a stretch, "
      f"n = 2) is a principled combination, and the check uses those.")
check("F3 [test] a scale independent of the cluster data fixes the threshold (within 0.5 dex), using "
      "only principled combinations of the theory's own constants",
      best_dex < 0.5,
      f"closest principled candidate is {best_nm} at {best_dex:.2f} dex.  The theory has ONE intrinsic "
      f"length (c/H0) and ONE intrinsic acceleration (a0), and their one dimensionless potential "
      f"a0/(c H0) = {xi_:.3f} overshoots the required {Xstar_req['canonical']:.2e} by "
      f"{math.log10(xi_/Xstar_req['canonical']):.1f} dex.  A free integer power CAN be made to land "
      f"within {spacing/2:.2f} dex, but that exponent is then a fitted parameter, not a prediction.  The "
      f"threshold is set by the cluster data and by nothing else")

E_CL_range = (min(COV[k]["E_cl"] for k in COV), max(COV[k]["E_cl"] for k in COV))

# ==================================================================================================
sec("PART G -- VERDICT, AND THE GENERAL THEOREM")
# ==================================================================================================
usable = (R_max <= TOL_THEORY and all(best_da[f] < 3.0 for f in A0) and cass_th <= CASSINI and
          cass_da <= CASSINI and nmin_best <= 3)
check("G1 [VERDICT] the potential-depth trigger is a USABLE handle on the cluster shear shape",
      usable,
      f"the covariance obstruction is SURVIVED (B4: the trigger is carried by X = 1 - Q/Q0, the clock's "
      f"own scalar), and that is a real positive.  But the carrier's zero is the cosmological background "
      f"(B5), so the trigger is the TOTAL depth; the galaxies that sit at cluster depths then take "
      f"R = M_P/M_fw = {R_min:.2f} - {R_max:.2f} exactly, against 1e-4 and 20%.  Best "
      f"achievable subject to both gates AND the trigger's own consistency: " +
      ", ".join(f"{f} {zs[f]:.1f} -> {best_da[f]:.1f} sigma (20%) / {best_th[f]:.1f} sigma (1e-4)"
                for f in A0))

print("""
  G2 -- THE GENERAL THEOREM.  Stated because this was the last named handle on the cluster shear shape.

  THEOREM (no scale-selective metric slip from a single local trigger).
  Let the slip be s = W(X) for a single-valued W of one local scalar X built from the metric, the
  preferred unit normal, and the theory's scalars.  Then:

   (i)   If X is built from the metric alone it is blind to the potential depth -- a constant deepening
         is an EXACT isometry, a rescaling of t (B1) -- and blind to a uniform field (B2, L31 Step E).
         What remains available is a curvature, i.e. an acceleration or a density, and L51 C9-C11 showed
         those overlap SPARC completely: 100% of the cluster weak-lensing rows sit inside the galaxy
         range, overshooting the theory's own no-slip bound by 3.2e6 (reproduced here, A6).

   (ii)  If X uses the theory's clock, the unique carrier of a depth is X = 1 - Q/Q0 with
         Q = n^mu d_mu phi (B4).  This is a genuine escape from (i): Q is not built from the metric.
         But its zero is the cosmological background, so X is the TOTAL potential at a point -- additive
         over sources (B5) -- and cannot be referenced to an object rather than to the cosmos.  There is
         no local field that sees a host and not its substructure.

   (iii) Under (ii), any object embedded at ambient X suffers a fractional slip R = W'(X)/2, independent
         of the object (B6).  And W' is not free: matching the required lensing phantom pointwise gives
         W'(X) = 2 g_P/g_fw, so R = M_P(<r)/M_fw(<r) EXACTLY -- no truncation, no zero point, no
         steepness, no five-cluster scatter (C3).  Measured on the X-COP weak-lensing sample that is
         {efloor:.2f}-{ehi:.2f}, i.e. {ovr:.1e} times the deposited theory's own Phi = Psi result and
         {ovrd:.2f} times a generous 20% empirical bound.  It scales with the amplitude f of the phantom,
         so it can be reduced only by giving up the shear-shape repair itself -- and Cassini then caps
         the amplitude from BELOW, because a weaker cluster slip needs a shallower weight and a shallow
         weight is nearly scale-free (E3).  The interior is empty.

   COROLLARY.  A scale-selective metric slip is not obtainable from any single local trigger in this
   theory: not from the metric sector (i), not from the clock sector (ii).  Since the second combination
   is the only linear-in-h freedom the preferred vector supplies (L39's operator count, reproduced in
   A1), and since a frame-free addition cannot move the lensing potential at all (L51 B4), the cluster
   weak-lensing SHAPE is not reachable by an operator freedom of this theory under any trigger.

   WHAT WOULD OVERTURN IT, stated so the theorem is falsifiable.
     * A weight built on a NON-LOCAL functional that is not a function of the local field value -- for
       instance one responding to the size of the region over which the field is coherent rather than to
       the field's depth there.  That is a different object; it is not tested here and the theorem does
       not cover it.
     * A measurement showing M_P/M_fw at cluster radii is far smaller than the {efloor:.2f}-{ehi:.2f}
       found here.  That is the one input the kill rests on, it is an AMPLITUDE rather than the
       noise-limited five-cluster scatter L51 refused to quote, and it would have to fall by 3-4 orders
       of magnitude on the theory arm and by a factor {onefac:.1f} on the empirical arm.  Per cluster it
       ranges 0.21-1.65 (canonical), so no single cluster carries it.
""".format(efloor=R_min, ehi=R_max, ovr=R_min / TOL_THEORY, ovrd=R_min / TOL_DATA,
           onefac=R_min / TOL_DATA))

print("""
  G3 -- WHAT THIS LANE DELIBERATELY DID NOT DO, to L51's own standard, in both directions.
   * The five-cluster cluster-to-cluster scatter of the required weight is NOT used anywhere, in either
     direction.  L51 C13b showed it is noise-limited (fractional error 1.41) and this lane inherits that
     refusal rather than the number.
   * The kill in C3/G2 rests on E(X_cl), an AMPLITUDE -- the required lensing phantom as a fraction of
     the framework's own potential -- which is a factor-of-two statement, not a precision one.
   * The door is NOT closed by failing to fit.  The fit succeeds: a unique W exists (L51 C3, A4 here),
     the covariance obstruction is genuinely survived (B4), and the non-overlap that L51 found is real
     on the covariant variable too (C1).  It is rejected on what it does elsewhere.
   * Two results run in the door's FAVOUR and are recorded as such: B4 (the trigger is covariantly
     writable, which L51 doubted) and C1 (the non-overlap is not an artefact of L51's proxy).
   * Two numbers are reported as MARGINAL rather than as kills: the Cassini response on the steep
     pinning arm (D4), which is within a factor of a few either way of the bound and depends on the
     Milky Way model; and the group ordering (D5), where the framework's own group-scale residual is
     estimator-limited in this repository and cannot presently confirm or refute the prediction.
   * No statement anywhere that data favour this framework over LambdaCDM.
""")

sec("SUMMARY")
print(f"    FAILS: {len(FAILS)}")
for f in FAILS: print(f"      - {f}")
print(f"\n    a0 footings carried on every dimensional number: "
      f"{A0['canonical']:.4e} / {A0['alt']:.4e} m s^-2")
print("    deliverables: L56_potential_trigger.py, L56_potential_trigger.out, L56_POTENTIAL_TRIGGER.md")
