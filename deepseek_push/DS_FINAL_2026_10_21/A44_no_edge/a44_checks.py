"""A44 -- the NO-EDGE tension: is the cold sector's cosmic share truncated at the right radius?

Lane A44.  Reads only files already on disk:
  real_research/data/lensing_rar/brouwer2021_rar/*        (Brouwer+21 KiDS-1000 Fig. 3: 4x15 + 60x60 cov)
  campaign_fresh_gravity/CFG801_settled_edge_vs_kids/     (the +197 / +753 record)
  campaign_fresh_gravity/CFG804_catchment_supply_derived/ (the -0.2 / -1.5 census record)
  deepseek_push/DS_FINAL_2026_10_21/A18_two_ratios/       (N = 5.364/f_ret, u = R_tot/N, P-A18)
  deepseek_push/DS_FINAL_2026_10_21/A29_u_radial/         (u = 0.47 in, 0.99 out; r_sp = 1.3674 r200c)
No network.  Deterministic.  kappa = 1/2 fitted (not theory closed), as in the source lanes.

Models (M_b profiled per stellar-mass bin, one number per bin, identical freedom for every model):
  N0       law phantom, no edge                       (the record's "edgeless law" reference)
  E(N)     law phantom cut at r_e = r_M sqrt(N(N+1)): enclosed cold mass exactly N M_b
  EA(N)    the 5.84 r_M cut with N times the cold mass per baryon   (mass at fixed edge)
  NFW(q)   cold mass q M_b in an NFW halo, c = c_DM14((1+q) M_b)    (same mass, other shape)
  S1(u)    A29 step + the SYSTEM cosmic share inside r_sp, cut at r_sp
  S2(u)    the cosmic-share cut at r_e kept, amplitude x u
  S3(u)    the A29 step on the full law phantom (no renormalisation), cut at the catchment edge
  S4(u)    the A29 step + the CATCHMENT cosmic share inside r_sp, cut at r_sp
  S4b(u)   S4 continued outside r_sp to r_e at the same rest-mass amplitude
  E(53.64) A18's catchment denominator: 5.364/f_ret = 53.64 M_b, no step

Delta Sigma is linear in the density, so every step model is a linear combination of tabulated
cold profiles; the projection is done once per footing.  The NFW projection is a 200-node
Gauss-Legendre quadrature in the variable r = R cosh u, validated against a 3000-point adaptive
integration (cylinder mass at r_max agrees with M_3D to 1.8e-5).

Footings: a0 = 9.3603e-11 (canonical) and 1.1312e-10 m/s^2 (alt), never pooled.
Exit 0 iff every check passes.  A44_MUTATE=<name> breaks one check group (see MUTATE.md).
"""
import json, math, os, sys, time
import numpy as np
from scipy.integrate import quad

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
DATA = os.path.join(REPO, "real_research", "data", "lensing_rar", "brouwer2021_rar")
MUT = os.environ.get("A44_MUTATE", "") or (sys.argv[1] if len(sys.argv) > 1 else "")
T0 = time.time()

OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))

# ------------------------------------------------------------------ constants
GPC = 4.30091e-3          # pc (km/s)^2 / Msun
GMPC = 4.30091e-9         # Mpc (km/s)^2 / Msun
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
SUP = 5.364               # R_cosmic = (1-f_b)/f_b = 5.364327
FB16 = 0.157
FRET_GAL = 0.10           # CFG416 three-segment table, M_ta < 1e12.5
if MUT == "system":
    FRET_GAL = 1.00       # MUTATION: the system denominator, i.e. N = 5.364 (the record's excluded model)
N_CATCH = SUP / FRET_GAL  # 53.64 = A18's N for an MW-like catchment
RHO_CRIT = 1.2607e11      # Msun/Mpc^3 at z = 0, h = 0.674
K_SPLASH = 1.3673815175297723   # A29: r_sp = 0.83 r200m = 1.3674 r200c
RADII = np.array([0.03539, 0.048108, 0.065396, 0.088897, 0.12084, 0.16427, 0.2233, 0.30354,
                  0.41262, 0.5609, 0.76246, 1.0365, 1.4089, 1.9152, 2.6035])
NL = len(RADII)

X = np.logspace(-3, 3, 600)
LMB = np.arange(9.0, 12.001, 0.15)
LX = np.log(X)
GLX, GLW = np.polynomial.legendre.leggauss(200)
VQ = 0.5 * (GLX + 1.0); WQ = 0.5 * GLW

rhoh = lambda s: 1.0 / (2 * math.pi * s * math.sqrt(1 + 4 * s * s))   # law phantom, units M_b/r_M^3
def m_law(s):  return 0.5 * (math.sqrt(1 + 4 * s * s) - 1)            # M_ph(<s)/M_b
def s_edge(N): return math.sqrt(N * (N + 1))                          # r_e/r_M where M_ph = N M_b
def a0_of(foot): return A0[foot] * 3.0857e16 / 1e6                    # (km/s)^2/pc
def rM_of(Mb, foot): return math.sqrt(GMPC * Mb / (a0_of(foot) * 1e6))   # Mpc
def r200_of(M, foot, z=0.0):
    return (3 * M / (4 * math.pi * 200 * RHO_CRIT * (0.315 * (1 + z) ** 3 + 0.685))) ** (1 / 3)
def c_DM14(Mh, z=0.0):
    """Dutton & Maccio 2014 c200 (Planck), verbatim from campaign_fresh_gravity/CFG2_common.py."""
    a = 0.520 + 0.385 * math.exp(-0.617 * max(z, 1e-6) ** 1.21)
    b = -0.101 + 0.026 * z
    return 10 ** (a + b * math.log10(Mh * 0.674 / 1e12))

# ------------------------------------------------------------------ data
def load_data():
    R, Y, E = [], [], []
    for b in range(1, 5):
        d = np.loadtxt(os.path.join(DATA, f"Fig-3_Lensing-rotation-curves_Massbin-{b}.txt"))
        bis = 1.0 if MUT == "nobias" else d[:, 4]
        R.append(d[:, 0]); Y.append(d[:, 1] / bis); E.append(d[:, 3] / bis)
    c = np.loadtxt(os.path.join(DATA, "Fig-3_Lensing-rotation-curves_Massbins_covmatrix.txt"))
    mins = sorted(set(c[:, 0])); C = np.zeros((4 * NL, 4 * NL))
    for row in c:
        m, n = mins.index(row[0]), mins.index(row[1])
        i = int(np.argmin(abs(RADII - row[2]))); j = int(np.argmin(abs(RADII - row[3])))
        C[m * NL + i, n * NL + j] = row[4] / (1.0 if MUT == "nobias" else row[6])
    return np.array(R), np.array(Y), np.array(E), C

R, Y, ERR, C = load_data()
PRIM = [i for i in range(NL) if RADII[i] <= 0.31]
FULL = list(range(NL))
PRINTMUT = f"   [MUTATE {MUT}]" if MUT else ""

# ------------------------------------------------------------------ projections (cold part only)
def esd_cold(rhofun, smax=None, x=X):
    """Delta Sigma_cold * r_M^2/M_b for density rhofun(s) in units M_b/r_M^3 (no baryon term)."""
    Sig = np.empty_like(x)
    for i, xi in enumerate(x):
        if smax is not None and xi >= smax:
            Sig[i] = 0.0; continue
        tm = math.sqrt(smax ** 2 - xi ** 2) if smax is not None else np.inf
        Sig[i] = 2 * quad(lambda t: rhofun(math.hypot(xi, t)), 0, tm, limit=400)[0]
    integ = 2 * math.pi * x ** 2 * Sig
    Mc = np.concatenate([[math.pi * x[0] ** 2 * Sig[0]],
                         math.pi * x[0] ** 2 * Sig[0]
                         + np.cumsum(0.5 * (integ[1:] + integ[:-1]) * np.diff(np.log(x)))])
    f = Mc / (math.pi * x ** 2) - Sig
    return np.maximum(f, 1e-10 * np.max(f))

def nfw_esd(xs, rs, rho_s, rmax, rM):
    """Delta Sigma_NFW in units M_b/r_M^2, R = xs*rM (Mpc), rs/rmax in Mpc, rho_s in Msun/Mpc^3."""
    r = xs * rM
    ok = r < rmax
    umax = np.where(ok, np.arccosh(np.clip(np.where(ok, rmax / np.where(ok, r, 1.0), 1.0), 1.0, None)), 0.0)
    u = umax[:, None] * VQ[None, :]
    rr = r[:, None] * np.cosh(u)
    integ = rho_s / ((rr / rs) * (1 + rr / rs) ** 2) * (r[:, None] * np.cosh(u)) * umax[:, None]
    Sig = 2.0 * (integ * WQ[None, :]).sum(axis=1)
    Sig = np.where(ok, Sig, 0.0)
    integ2 = 2 * np.pi * xs ** 2 * Sig
    Mc = np.concatenate([[math.pi * xs[0] ** 2 * Sig[0]],
                         math.pi * xs[0] ** 2 * Sig[0]
                         + np.cumsum(0.5 * (integ2[1:] + integ2[:-1]) * np.diff(np.log(xs)))])
    return np.maximum(Mc / (math.pi * xs ** 2) - Sig, 1e-10 * np.max(Mc / (math.pi * xs ** 2) + 1e-30))

def table(builder, foot, xs=X):
    T = np.empty((len(LMB), len(xs)))
    for i, lm in enumerate(LMB):
        T[i] = builder(lm, foot, xs)
    return np.maximum(T, 1e-10 * np.max(T, axis=1, keepdims=True))

def interp2(T, lm, lx):
    """bilinear in log M_b and log x, log f."""
    j = np.clip(np.searchsorted(LX, lx) - 1, 0, len(X) - 2)
    fx = (lx - LX[j]) / (LX[j + 1] - LX[j])
    i = np.clip((lm - LMB[0]) / (LMB[1] - LMB[0]), 0, len(LMB) - 1.000001)
    i0 = int(i); fi = i - i0
    v = ((1 - fi) * ((1 - fx) * np.log(T[i0, j]) + fx * np.log(T[i0, j + 1]))
         + fi * ((1 - fx) * np.log(T[i0 + 1, j]) + fx * np.log(T[i0 + 1, j + 1])))
    return np.exp(v)

# ------------------------------------------------------------------ fitting
GRID = np.arange(9.0, 12.0001, 0.01)
ZK = [10.14, 10.46, 10.70, 10.89]

def model_ss(f, lm, Rb, foot):
    M = 10 ** lm; rM = rM_of(M, foot)
    return M / (rM * 1e6) ** 2 * np.exp(np.interp(np.log(Rb / rM), LX, np.log(f))) + M / (math.pi * (Rb * 1e6) ** 2)

def model_2d(T, lm, Rb, foot):
    M = 10 ** lm; rM = rM_of(M, foot)
    return M / (rM * 1e6) ** 2 * interp2(T, lm, np.log(Rb / rM)) + M / (math.pi * (Rb * 1e6) ** 2)

def chi2(f, L, idx, foot, two=False):
    yv = np.concatenate([Y[b] for b in range(4)])
    mv = np.concatenate([(model_2d if two else model_ss)(f, L[b], R[b], foot) for b in range(4)])
    sel = np.concatenate([np.array(idx) + NL * b for b in range(4)])
    r = (yv - mv)[sel]
    if not np.all(np.isfinite(r)):
        return float("inf")
    with np.errstate(all="ignore"):
        return float(r @ np.linalg.solve(C[np.ix_(sel, sel)], r))

def fit(f, idx, foot, two=False):
    L = list(ZK)
    for _ in range(3):
        for b in range(4):
            L[b] = float(min(GRID, key=lambda g: chi2(f, L[:b] + [g] + L[b + 1:], idx, foot, two)))
    return L, chi2(f, L, idx, foot, two)

def score(tag, f, foot, two=False):
    Lp, cp = fit(f, PRIM, foot, two); La, ca = fit(f, FULL, foot, two)
    d = dict(tag=tag, chi2_prim=cp, chi2_all=ca, logMb_prim=Lp, logMb_all=La,
             n_prim=4 * len(PRIM), n_all=4 * len(FULL), two_d=two)
    P(f"    {tag:42s} chi2_prim {cp:8.2f}  chi2_all {ca:9.2f}   logMb_prim {['%.2f' % v for v in Lp]}")
    return d

# ================================================================== run
P("=" * 122)
P("A44 -- the NO-EDGE tension: the cosmic-share cold halo, KiDS-1000 isolated lensing, and the A29 step" + PRINTMUT)
P("=" * 122)
P(f"data: 4 stellar-mass bins x 15 radii {RADII[0]:.4f}-{RADII[-1]:.4f} Mpc, 60x60 covariance, "
  f"primary {len(PRIM)} radii/bins (R <= 0.31 Mpc)")

RES = dict(lane="A44", generated=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), mutate=MUT or None,
           constants=dict(a0=A0, SUP=SUP, f_ret_gal=FRET_GAL, N_catch=N_CATCH, k_splash=K_SPLASH,
                          rho_crit=RHO_CRIT, G_Mpc=GMPC, data=DATA),
           footings={})
CK = []
def ck(cid, what, measured, ok):
    CK.append(dict(id=cid, what=what, measured=str(measured), pass_=bool(ok)))
    P(f"  [{cid}] {'PASS' if ok else 'FAIL'}  {what}: {measured}")

tot = sum(len(np.loadtxt(os.path.join(DATA, f"Fig-3_Lensing-rotation-curves_Massbin-{b}.txt"))) for b in range(1, 5))
sym = float(np.max(np.abs(C - C.T)) / np.max(np.abs(C)))
P("\n-- data integrity --")
ck("K1", "4x15 rows, 60x60 covariance symmetric, diagonal = quoted error^2 (bin 1)",
   f"{tot} rows, asym {sym:.1e}, diag/err^2 max dev {np.max(abs(np.diag(C)[:NL]/ERR[0]**2-1)):.2e}",
   tot == 60 and sym < 1e-12 and np.max(abs(np.diag(C)[:NL] / ERR[0] ** 2 - 1)) < 2e-3)
ck("K1b", "primary radii <= 0.31 Mpc (the record's clean range)", f"n = {len(PRIM)}, R_max = {RADII[PRIM[-1]]:.4f}",
   len(PRIM) == 8)

for foot in ("canonical", "alt"):
    a0 = a0_of(foot)
    P("\n" + "=" * 122)
    P(f"FOOTING {foot}: a0 = {A0[foot]:.4e} m/s^2 = {a0:.4f} (km/s)^2/pc")
    P("=" * 122)
    F = dict(footing=foot, a0_m_s2=A0[foot])

    P("\n-- N0: the edgeless law (the record's reference) --")
    FN = esd_cold(rhoh, None)
    n0 = score("N0 edgeless law", FN, foot)
    F["N0"] = n0; C0p, C0a = n0["chi2_prim"], n0["chi2_all"]
    if foot == "canonical":
        ck("K2", "no-edge reference chi2_prim (CFG801: 83.86)", f"{C0p:.2f}", abs(C0p - 83.8596) < 0.1)
    else:
        ck("K2b", "alt no-edge chi2_prim (CFG801 alt: 79.7)", f"{C0p:.2f}", abs(C0p - 79.7) < 0.3)

    P("\n-- E(5.364): the cosmic share cut at r_e = 5.8426 r_M (the model the record excludes) --")
    FE = esd_cold(rhoh, s_edge(SUP))
    e1 = score("E(N=5.364) system cosmic share", FE, foot)
    e1["dchi2_prim"] = e1["chi2_prim"] - C0p; e1["dchi2_all"] = e1["chi2_all"] - C0a
    e1["edge_rM"] = s_edge(SUP); e1["M_c_over_Mb"] = SUP
    F["E1"] = e1
    P(f"      dchi2 vs no-edge: prim {e1['dchi2_prim']:+.2f}   all {e1['dchi2_all']:+.2f};  "
      f"M_c(<r_e)/M_b = m_law(5.8426) = {m_law(s_edge(SUP)):.6f}")
    if foot == "canonical":
        ck("K3", "CFG801 reproduction: +197.1 (primary) and +753.0 (all radii)",
           f"{e1['dchi2_prim']:+.1f} / {e1['dchi2_all']:+.1f}",
           abs(e1["dchi2_prim"] - 197.1) < 0.5 and abs(e1["dchi2_all"] - 753.0) < 1.0)
    else:
        ck("K3b", "CFG801 alt reproduction: +234 (primary), +813 (all)",
           f"{e1['dchi2_prim']:+.1f} / {e1['dchi2_all']:+.1f}",
           abs(e1["dchi2_prim"] - 234.0) < 1.5 and abs(e1["dchi2_all"] - 813.0) < 2.0)

    P("\n-- E(N): the same function and the same amplitude, only the cutoff moves --")
    ESC = {}
    for N in [5.364, 6, 8, 10, 12, 16, 20, 24, 32, 43.8, 53.64, 65.7, 100]:
        r = score(f"E(N={N:6.2f}) edge {s_edge(N):6.2f} r_M", esd_cold(rhoh, s_edge(N)), foot)
        r["dchi2_prim"] = r["chi2_prim"] - C0p; r["dchi2_all"] = r["chi2_all"] - C0a
        r["edge_rM"] = s_edge(N); r["M_c_over_Mb"] = N
        ESC[f"{N:g}"] = r
    F["Escan"] = ESC
    # the edge radius required at dchi2 = 4 (primary), interpolated on the scan
    Ns = np.array([ESC[k]["M_c_over_Mb"] for k in ESC]); ds = np.array([ESC[k]["dchi2_prim"] for k in ESC])
    o = np.argsort(Ns); Ns, ds = Ns[o], ds[o]
    Nreq = None
    for i in range(len(Ns) - 1):
        if (ds[i] - 4) * (ds[i + 1] - 4) <= 0:
            Nreq = float(Ns[i] + (4 - ds[i]) * (Ns[i + 1] - Ns[i]) / (ds[i + 1] - ds[i])); break
    F["N_required_primary"] = Nreq
    P(f"      edge required for dchi2 <= 4: N = {Nreq:.1f} M_b, r_e = {s_edge(Nreq):.1f} r_M"
      if Nreq is not None else "      edge required for dchi2 <= 4: beyond the scan")

    P("\n-- edge, not slope: the same 3D function inside r_e, a 10x heavier halo outside --")
    FC = esd_cold(rhoh, s_edge(N_CATCH))
    M3num = 4 * math.pi * quad(lambda ss: ss * ss * rhoh(ss), 0, s_edge(SUP), limit=400)[0]
    Dmax = max(abs(math.exp(np.interp(math.log(xx), LX, np.log(FE)) - np.interp(math.log(xx), LX, np.log(FC))) - 1)
               for xx in [1.0, 2.0, 3.0, 4.0, 4.5, 5.0])
    ck("K5" if foot == "canonical" else "K5b",
       "law profile integrates to 5.364 M_b at r_e; the 5.364 and 53.64 M_b halos share the 3D density inside it "
       "(projected dSigma differs only by the LOS column of the outer mass)",
       f"4pi Int s^2 rho ds = {M3num:.6f} (m_law {m_law(s_edge(SUP)):.6f}); dSigma max dev {Dmax*100:.1f}%",
       abs(M3num - SUP) < 1e-4 and Dmax < 0.10)

    P("\n-- EA(N): N times the cold mass per baryon, the edge kept at 5.84 r_M --")
    EA = {}
    for N in [6, 10]:
        r = score(f"EA(N={N}) mass x{N}, edge 5.84 r_M", N * FE, foot)
        r["dchi2_prim"] = r["chi2_prim"] - C0p; EA[str(N)] = r
    r_same = score("EA(5.94) mass 31.9 M_b, edge 5.84 r_M", 5.94 * FE, foot)
    r_same["dchi2_prim"] = r_same["chi2_prim"] - C0p
    F["EA"] = EA; F["EA_same_mass"] = r_same
    if foot == "canonical":
        ck("K5c", "at the SAME cold mass (31.9 M_b) the edge decides: 5.84 r_M vs 32.5 r_M",
           f"dchi2 {r_same['dchi2_prim']:+.1f} vs {ESC['32']['dchi2_prim']:+.1f}",
           r_same["dchi2_prim"] > 300 and ESC["32"]["dchi2_prim"] < 40)

    P("\n-- NFW(q): the same cold mass in an NFW halo, concentration from the halo mass --")
    def nfw_builder(q, cfix=None):
        def b(lm, ft, xs):
            Mb = 10 ** lm; rM = rM_of(Mb, ft); M200 = q * Mb
            cc = cfix if cfix is not None else c_DM14((1 + q) * Mb)
            r200 = r200_of(M200, ft); rs = r200 / cc
            rho_s = M200 / (4 * math.pi * rs ** 3 * (math.log1p(cc) - cc / (1 + cc)))
            # dimensionless: rs and r_max in units of r_M, rho_s in units of M_b/r_M^3
            return nfw_esd(xs, rs / rM, rho_s * rM ** 3 / Mb, 5 * r200 / rM, 1.0)
        return b
    TNF = table(nfw_builder(SUP), foot)
    nf = score("NFW M200=5.364 M_b, c=c_DM14(M200)", TNF, foot, two=True)
    nf["dchi2_prim"] = nf["chi2_prim"] - C0p; nf["dchi2_all"] = nf["chi2_all"] - C0a
    nf["c200"] = [c_DM14((1 + SUP) * 10 ** lm) for lm in n0["logMb_prim"]]
    F["NFW"] = nf
    NFV = {}
    for cfix in [4.5, 10.0, 20.0]:
        T = table(nfw_builder(SUP, cfix), foot)
        r = score(f"NFW c={cfix:4.1f} (M200=5.364 M_b)", T, foot, two=True)
        r["dchi2_prim"] = r["chi2_prim"] - C0p; NFV[str(cfix)] = r
        if cfix == 10.0:
            F["NFW_c10"] = r
    F["NFW_c"] = NFV
    P(f"      c200 = {['%.2f' % v for v in nf['c200']]}")
    if foot == "canonical":
        ck("K6", "an NFW at the same mass is still excluded: dchi2 > +100 (it is less bad than the 5.84 r_M cut, "
           "which is why shape and edge must be scored separately)",
           f"NFW {nf['dchi2_prim']:+.1f} vs E1 {e1['dchi2_prim']:+.1f}", nf["dchi2_prim"] > 100)

    P("\n-- geometry: the A29 splashback radius against the cosmic-share edge --")
    GEO = []
    for b, lm in enumerate(n0["logMb_prim"]):
        Mb = 10 ** lm; rM = rM_of(Mb, foot)
        rsp = K_SPLASH * r200_of((1 + SUP) * Mb, foot)
        GEO.append(dict(bin=b + 1, logMb=lm, M_b=Mb, r_M_kpc=rM * 1e3, r_e_kpc=s_edge(SUP) * rM * 1e3,
                        r_sp_kpc=rsp * 1e3, r_sp_over_r_e=rsp / (s_edge(SUP) * rM),
                        s_sp=rsp / rM, Mph_rsp_over_Mb=m_law(rsp / rM),
                        Mph_rsp_over_cosmic=m_law(rsp / rM) / SUP,
                        u_in_pred_fret010=m_law(rsp / rM) / N_CATCH))
    F["geometry"] = GEO
    P("      bin  logM_b  r_M[kpc]  r_e[kpc]  r_sp[kpc]  r_sp/r_e  M_ph(r_sp)/5.364M_b  M_ph(r_sp)/53.64M_b")
    for g in GEO:
        P(f"       {g['bin']}   {g['logMb']:5.2f}  {g['r_M_kpc']:7.1f}  {g['r_e_kpc']:7.1f}   "
          f"{g['r_sp_kpc']:7.1f}   {g['r_sp_over_r_e']:6.2f}   {g['Mph_rsp_over_cosmic']:10.2f}   "
          f"{g['u_in_pred_fret010']:12.3f}")
    # A29 stack: r_sp = 1.4137 Mpc, r200c = 1.0323 Mpc -> M200 = 3.48e14.  Two M_b routes:
    #  (a) A18's cluster anchor M_b = 1.4e14 (the value A18 uses for its cluster algebra);
    #  (b) self-consistent M_b = M200/6.364 = 5.47e13.  r_sp/r_e < 1 on both.
    rsp_cl = 1.4137386182260803; r200_cl = 1.0322909901299508
    M200_cl = 4 * math.pi / 3 * 200 * RHO_CRIT * r200_cl ** 3
    cl = {}
    for lab, Mb in (("A18_anchor", 1.4e14), ("selfconsistent", M200_cl / (1 + SUP))):
        rM = rM_of(Mb, foot)
        cl[lab] = dict(M_b=Mb, r_M_Mpc=rM, r_e_Mpc=s_edge(SUP) * rM, r_sp_over_r_e=rsp_cl / (s_edge(SUP) * rM),
                       s_sp=rsp_cl / rM, Mph_rsp_over_cosmic=m_law(rsp_cl / rM) / SUP)
    F["cluster_geometry"] = dict(r_sp_Mpc=rsp_cl, r200c_Mpc=r200_cl, M200_cl=M200_cl, routes=cl,
                                 r_sp_over_r_e=cl["A18_anchor"]["r_sp_over_r_e"],
                                 Mph_rsp_over_cosmic=cl["A18_anchor"]["Mph_rsp_over_cosmic"])
    P(f"      A29 cluster stack: r_sp {rsp_cl:.3f} Mpc, r200c {r200_cl:.3f} Mpc -> M200 {M200_cl:.2e}")
    for lab in ("A18_anchor", "selfconsistent"):
        c = cl[lab]
        P(f"        M_b {lab:14s} {c['M_b']:.2e}: r_M {c['r_M_Mpc']:.3f} Mpc, r_e {c['r_e_Mpc']:.3f} Mpc, "
          f"r_sp/r_e {c['r_sp_over_r_e']:.2f}, M_ph(r_sp)/5.364M_b {c['Mph_rsp_over_cosmic']:.2f}")
    # crossover r_sp = r_e, on M200 = 6.364 M_b
    lo, hi = 12.0, 15.0
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        Mb = 10 ** mid
        if K_SPLASH * r200_of((1 + SUP) * Mb, foot) / (s_edge(SUP) * rM_of(Mb, foot)) > 1:
            lo = mid
        else:
            hi = mid
    F["crossover_logMb"] = 0.5 * (lo + hi)
    P(f"      r_sp = r_e at M_b = {10**(0.5*(lo+hi)):.2e} (M200 = {(1+SUP)*10**(0.5*(lo+hi)):.2e}); "
      f"below it r_sp > r_e and the step cannot sit at the edge")
    if foot == "canonical":
        ck("K7", "at all four KiDS masses r_sp > 3 r_e (the step is outside the cosmic-share edge)",
           f"r_sp/r_e {min(g['r_sp_over_r_e'] for g in GEO):.2f}-{max(g['r_sp_over_r_e'] for g in GEO):.2f}",
           min(g["r_sp_over_r_e"] for g in GEO) > 3.0)
        ck("K7b", "at r_sp the law phantom has spent 3.5-4.8x the cosmic share",
           f"{min(g['Mph_rsp_over_cosmic'] for g in GEO):.2f}-{max(g['Mph_rsp_over_cosmic'] for g in GEO):.2f}",
           min(g["Mph_rsp_over_cosmic"] for g in GEO) > 3.0)
        ck("K7c", "the step can sit inside the edge only above M_b = 1e14 (M200 = 1e15)",
           f"crossover logM_b = {F['crossover_logMb']:.2f}", F["crossover_logMb"] > 14.0)

    P("\n-- S: the A29 step, u_in inside r_sp and u = 1 outside --")
    def s_sp(lm, ft, q=SUP):
        return K_SPLASH * r200_of((1 + q) * 10 ** lm, ft) / rM_of(10 ** lm, ft)
    Tss = table(lambda lm, ft, xs: (SUP / m_law(s_sp(lm, ft))) * esd_cold(rhoh, s_sp(lm, ft), x=xs), foot)
    Tss_raw = table(lambda lm, ft, xs: esd_cold(rhoh, s_sp(lm, ft), x=xs), foot)
    Tsc = table(lambda lm, ft, xs: esd_cold(rhoh, s_edge(N_CATCH), x=xs), foot)
    STEP = {}
    for u in [0.3348, 0.4116, 0.4716]:
        r = score(f"S1 step + SYSTEM share inside r_sp, u={u:.3f}", u * Tss, foot, two=True)
        r["dchi2_prim"] = r["chi2_prim"] - C0p; r["dchi2_all"] = r["chi2_all"] - C0a; r["u_in"] = u
        STEP[f"s1_{u:.3f}"] = r
    u0 = 0.4716
    r = score("S2 truncation at r_e kept, amplitude x u", u0 * FE, foot)
    r["dchi2_prim"] = r["chi2_prim"] - C0p; STEP["s2"] = r
    # census supply per row
    def fret_of(lM):
        if lM < 12.5: f = 0.10
        elif lM < 13.5: f = 0.10 + 0.45 * (lM - 12.5)
        else: f = min(0.55 + 0.30 * (lM - 13.5), 0.90)
        return min(f, 1.0)
    def N_of(logMb):
        f = 0.10
        for _ in range(200):
            fn = fret_of(logMb - math.log10(f * FB16))
            if abs(fn - f) < 1e-12: break
            f = 0.5 * (f + fn)
        return 1 / f, 1 / f * SUP          # (1/f_ret, cold mass in M_b)
    Mrow = np.array([N_of(lm)[1] for lm in LMB])[:, None]      # cold mass at the catchment edge, in M_b
    S4cut = u0 * (Mrow / SUP) * Tss                             # u x A x rho_law, A = (5.364/f_ret)/m_law(s_sp)
    r = score("S4 step + CATCHMENT share in r_sp, cut r_sp", S4cut, foot, two=True)
    r["dchi2_prim"] = r["chi2_prim"] - C0p; r["dchi2_all"] = r["chi2_all"] - C0a
    STEP["s4_cut"] = r
    F["step"] = STEP
    US = [0.2, 0.3, 0.3348, 0.4116, 0.4716, 0.6, 0.7, 0.8, 0.9, 0.95, 1.0]
    UCHI = {}
    for u in US:
        ue = 1.0 if MUT == "nostep" else u          # MUTATION: the step is switched off
        r = score(f"S3 u-step on the full phantom, u={u:.4f}", Tsc - (1 - ue) * Tss_raw, foot, two=True)
        r["dchi2_prim"] = r["chi2_prim"] - C0p; r["dchi2_all"] = r["chi2_all"] - C0a
        UCHI[f"{u:g}"] = r
    F["u_scan"] = UCHI
    ds = np.array([UCHI[f"{u:g}"]["dchi2_prim"] for u in US]); ureq = None
    for i in range(len(US) - 1):
        if (ds[i] - 4) * (ds[i + 1] - 4) <= 0:
            ureq = float(US[i] + (4 - ds[i]) * (US[i + 1] - US[i]) / (ds[i + 1] - ds[i])); break
    F["u_required"] = ureq
    sig_step = math.sqrt(max(UCHI["0.4716"]["chi2_prim"] - UCHI["1"]["chi2_prim"], 0.0))
    F["u_step_significance_sigma"] = sig_step
    P(f"      u required by the primary range (dchi2 = 4): {ureq};  the u = 0.4716 step is "
      f"{sig_step:.1f} sigma from u = 1")
    if foot == "canonical":
        ck("K8", "the A29 step at u = 0.4716 on the full phantom is excluded (primary)",
           f"dchi2 {UCHI['0.4716']['dchi2_prim']:+.1f}", UCHI["0.4716"]["dchi2_prim"] > 9)
        ck("K8b", "u required by the data >= 0.8 (A29 measures 0.47)", f"u_req = {ureq}",
           ureq is not None and ureq >= 0.8)
        ck("K8c", "S1 (step + system share) is WORSE than the truncation it was meant to repair",
           f"S1 {STEP['s1_0.472']['dchi2_prim']:+.1f} vs E1 {e1['dchi2_prim']:+.1f}",
           STEP["s1_0.472"]["dchi2_prim"] > e1["dchi2_prim"])
        ck("K8d", "S4 (step + catchment share) repairs most of E1: dchi2 falls by > 150",
           f"S4 {STEP['s4_cut']['dchi2_prim']:+.1f} vs E1 {e1['dchi2_prim']:+.1f}",
           (e1["dchi2_prim"] - STEP["s4_cut"]["dchi2_prim"]) > 150)

    P("\n-- E(53.64): the cosmic share with A18's catchment denominator, 5.364/f_ret --")
    ec = score("E(N=53.64) catchment cosmic share", FC, foot)
    ec["dchi2_prim"] = ec["chi2_prim"] - C0p; ec["dchi2_all"] = ec["chi2_all"] - C0a
    ec["M_c_over_Mb"] = N_CATCH
    F["E_catch"] = ec
    if foot == "canonical":
        ck("K9", "the catchment-denominator cosmic share fits where the system-denominator one fails",
           f"dchi2_prim {ec['dchi2_prim']:+.1f} vs E1 {e1['dchi2_prim']:+.1f}",
           abs(ec["dchi2_prim"]) < 5 and e1["dchi2_prim"] > 100)

    P("\n-- CFG804 reproduction: the census N = 1/f_ret model as implemented in the record --")
    NGRID = np.round(np.concatenate([[1.0], np.arange(2.0, 10.01, 0.25)]), 2)
    FD = {}
    def f_for(N):
        Nn = float(NGRID[np.argmin(abs(NGRID - N))])
        if Nn not in FD:
            FD[Nn] = esd_cold(rhoh, math.sqrt(((2 * SUP * Nn + 1) ** 2 - 1) / 4))
        return FD[Nn]
    T804 = np.empty((len(LMB), len(X)))
    for i, lm in enumerate(LMB):
        T804[i] = f_for(N_of(lm)[0])
    d804 = score("CFG804 census N = 1/f_ret", np.maximum(T804, 1e-10 * np.max(T804, axis=1, keepdims=True)),
                 foot, two=True)
    d804["dchi2_prim"] = d804["chi2_prim"] - C0p; d804["dchi2_all"] = d804["chi2_all"] - C0a
    d804["N_per_bin"] = [N_of(lm)[0] for lm in d804["logMb_prim"]]
    d804["edge_rM_per_bin"] = [math.sqrt(((2 * SUP * N_of(lm)[0] + 1) ** 2 - 1) / 4) for lm in d804["logMb_prim"]]
    F["CFG804"] = d804
    if foot == "canonical":
        ck("K10", "CFG804 reproduction: -0.2 (primary), +148.7 (all radii)",
           f"{d804['dchi2_prim']:+.1f} / {d804['dchi2_all']:+.1f}",
           abs(d804["dchi2_prim"] + 0.2) < 1.5 and abs(d804["dchi2_all"] - 148.7) < 5.0)
    else:
        ck("K10b", "CFG804 alt reproduction: -1.5 (primary), +172.2 (all)",
           f"{d804['dchi2_prim']:+.1f} / {d804['dchi2_all']:+.1f}",
           abs(d804["dchi2_prim"] + 1.5) < 1.5 and abs(d804["dchi2_all"] - 172.2) < 6.0)
    P(f"      N per bin {['%.2f' % v for v in d804['N_per_bin']]}, edge "
      f"{['%.1f' % v for v in d804['edge_rM_per_bin']]} r_M, cold mass "
      f"{['%.1f' % (v*SUP) for v in d804['N_per_bin']]} M_b")

    P("\n-- Delta Sigma(R), bins 1 and 4 (M_b = the no-edge best fit; h70 Msun/pc^2) --")
    T1 = u0 * Tss; T3 = Tsc - (1 - u0) * Tss_raw; T4 = S4cut
    idx = [4, 5, 6, 7, 8, 9, 10, 11]
    DTAB = {}
    for b in range(4):
        lm = n0["logMb_prim"][b]; Mb = 10 ** lm; rM = rM_of(Mb, foot)
        rows = []
        for i in idx:
            rr = RADII[i]; lx = math.log(rr / rM); pre = Mb / (rM * 1e6) ** 2
            bary = Mb / (math.pi * (rr * 1e6) ** 2)
            rows.append(dict(R=float(rr), data=float(Y[b][i]), err=float(ERR[b][i]),
                             E1=float(pre * math.exp(np.interp(lx, LX, np.log(FE))) + bary),
                             NFW=float(pre * interp2(TNF, lm, lx) + bary),
                             N0=float(pre * math.exp(np.interp(lx, LX, np.log(FN))) + bary),
                             S1=float(pre * interp2(T1, lm, lx) + bary),
                             S3=float(pre * interp2(T3, lm, lx) + bary),
                             S4=float(pre * interp2(T4, lm, lx) + bary),
                             E_catch=float(pre * math.exp(np.interp(lx, LX, np.log(FC))) + bary)))
        DTAB[f"bin{b+1}"] = dict(logMb=lm, r_M_kpc=rM * 1e3, r_e_kpc=s_edge(SUP) * rM * 1e3,
                                 r_sp_kpc=GEO[b]["r_sp_kpc"], rows=rows)
    F["dSigma"] = DTAB
    for b in [0, 3]:
        k = f"bin{b+1}"
        P(f"    {k} (logM_b {DTAB[k]['logMb']:.2f}, r_M {DTAB[k]['r_M_kpc']:.1f} kpc, "
          f"r_e {DTAB[k]['r_e_kpc']:.1f} kpc, r_sp {DTAB[k]['r_sp_kpc']:.1f} kpc):")
        P("      R[Mpc]  data+-err    E1(5.364)  NFW(5.364)  N0(noedge)  S1(step)   S3(u=.47)  S4(step+cat) E(53.6)")
        for r in DTAB[k]["rows"]:
            P(f"      {r['R']:6.4f} {r['data']:6.2f}+-{r['err']:4.2f}  {r['E1']:9.3f}  {r['NFW']:10.3f}  "
              f"{r['N0']:10.3f}  {r['S1']:9.3f}  {r['S3']:9.3f}  {r['S4']:11.3f} {r['E_catch']:9.3f}")

    P("\n-- the number that decides: cold mass required inside 0.31 Mpc --")
    REQ = []
    for b in range(4):
        lm = n0["logMb_prim"][b]; Mb = 10 ** lm; rM = rM_of(Mb, foot)
        s = RADII[PRIM[-1]] / rM
        mc = m_law(s) * Mb
        REQ.append(dict(bin=b + 1, logMb=lm, M_c_Msun=mc, over_cosmic=mc / (SUP * Mb), s=float(s)))
    F["required"] = REQ
    for r in REQ:
        P(f"    bin {r['bin']}: s = 0.3035/r_M = {r['s']:5.1f}, M_c(<0.31 Mpc) = {r['M_c_Msun']:.2e} Msun "
          f"= {r['over_cosmic']:5.2f} x 5.364 M_b")
    if foot == "canonical":
        ck("K11", "the cold mass required inside 0.31 Mpc is > 3x the cosmic share in >= 3 of 4 bins",
           f"{['%.2f' % r['over_cosmic'] for r in REQ]}", sum(r["over_cosmic"] > 3 for r in REQ) >= 3)
        ck("K11b", "the edge required by the data (dchi2 <= 4) is > 2x the cosmic-share edge 5.84 r_M",
           (f"N = {Nreq:.1f} M_b ({Nreq/SUP:.2f} x cosmic), r_e = {s_edge(Nreq):.1f} r_M"
            if Nreq is not None else "beyond the scan"),
           Nreq is not None and Nreq / SUP > 2.0)

    P("\n-- local log-slope d ln(Delta Sigma)/d ln R, 0.1208 -> 0.30354 Mpc --")
    SL = []
    for b in range(4):
        lm = n0["logMb_prim"][b]; Mb = 10 ** lm; rM = rM_of(Mb, foot)
        i0, i1 = 4, 7
        g = math.log(Y[b][i1] / Y[b][i0]) / math.log(RADII[i1] / RADII[i0])
        lx0, lx1 = math.log(RADII[i0] / rM), math.log(RADII[i1] / rM)
        gl = (np.interp(lx1, LX, np.log(FN)) - np.interp(lx0, LX, np.log(FN))) / (lx1 - lx0)
        gn = (np.interp(lx1, LX, np.log(TNF[b])) - np.interp(lx0, LX, np.log(TNF[b]))) / (lx1 - lx0)
        gc = (np.interp(lx1, LX, np.log(FC)) - np.interp(lx0, LX, np.log(FC))) / (lx1 - lx0)
        SL.append(dict(bin=b + 1, data=g, law=float(gl), nfw=float(gn), catch=float(gc)))
        P(f"    bin {b+1}: data {g:+.2f}   law phantom {gl:+.2f}   NFW(5.364) {gn:+.2f}   E(53.6) {gc:+.2f}")
    F["slopes"] = SL

    RES["footings"][foot] = F

P("\n" + "=" * 122)
P("SUMMARY -- canonical footing (alt in a44_results.json; the two are never pooled)")
P("=" * 122)
F = RES["footings"]["canonical"]
P(f"  N0   edgeless law                                  chi2_prim {F['N0']['chi2_prim']:8.2f}   dchi2     ----")
P(f"  E1   system cosmic share, edge 5.84 r_M            chi2_prim {F['E1']['chi2_prim']:8.2f}   dchi2 {F['E1']['dchi2_prim']:+8.1f}")
P(f"  NFW  same mass, c = c_DM14                         chi2_prim {F['NFW']['chi2_prim']:8.2f}   dchi2 {F['NFW']['dchi2_prim']:+8.1f}")
P(f"  S1   step + system share inside r_sp (u=.472)      chi2_prim {F['step']['s1_0.472']['chi2_prim']:8.2f}   dchi2 {F['step']['s1_0.472']['dchi2_prim']:+8.1f}")
P(f"  S2   system share kept, amplitude x u              chi2_prim {F['step']['s2']['chi2_prim']:8.2f}   dchi2 {F['step']['s2']['dchi2_prim']:+8.1f}")
P(f"  S3   step on the full phantom (u=.472)             chi2_prim {F['u_scan']['0.4716']['chi2_prim']:8.2f}   dchi2 {F['u_scan']['0.4716']['dchi2_prim']:+8.1f}")
P(f"  S4   step + catchment share inside r_sp (u=.472)   chi2_prim {F['step']['s4_cut']['chi2_prim']:8.2f}   dchi2 {F['step']['s4_cut']['dchi2_prim']:+8.1f}")
P(f"  E    catchment cosmic share 53.64 M_b              chi2_prim {F['E_catch']['chi2_prim']:8.2f}   dchi2 {F['E_catch']['dchi2_prim']:+8.1f}")
P(f"  C804 census N = 1/f_ret                            chi2_prim {F['CFG804']['chi2_prim']:8.2f}   dchi2 {F['CFG804']['dchi2_prim']:+8.1f}")
P(f"  edge required (dchi2 <= 4): N = {F['N_required_primary']:.1f} M_b, r_e = "
  f"{s_edge(F['N_required_primary']):.1f} r_M" if F["N_required_primary"] is not None
  else "  edge required (dchi2 <= 4): beyond the scan")
ureq_txt = f"{F['u_required']:.2f}" if F["u_required"] is not None else "none (dchi2 never reaches 4)"
P(f"  u required {ureq_txt} (A29: 0.47);  r_sp/r_e: galaxies "
  f"{min(g['r_sp_over_r_e'] for g in F['geometry']):.2f}-{max(g['r_sp_over_r_e'] for g in F['geometry']):.2f}, "
  f"cluster {F['cluster_geometry']['r_sp_over_r_e']:.2f}-"
  f"{F['cluster_geometry']['routes']['selfconsistent']['r_sp_over_r_e']:.2f}")

npass = sum(c["pass_"] for c in CK)
P(f"\n  {npass}/{len(CK)} checks pass.  runtime {time.time()-T0:.1f} s.")
RES["checks"] = CK; RES["n_pass"] = npass; RES["n_total"] = len(CK); RES["runtime_s"] = time.time() - T0

SFX = ("_MUTATE_" + MUT) if MUT else ""
with open(os.path.join(HERE, f"a44{SFX}.out"), "w") as fh:
    fh.write("\n".join(OUT) + "\n")
with open(os.path.join(HERE, f"a44_results{SFX}.json"), "w") as fh:
    json.dump(RES, fh, indent=1, default=float)
sys.exit(0 if npass == len(CK) else 1)
