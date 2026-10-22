import os, sys, math, glob, json, time
import numpy as np
from scipy.optimize import brentq, minimize, minimize_scalar
from scipy.special import gammainc
from scipy.interpolate import CubicSpline

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
G_N = 6.67430e-11; C_L = 2.99792458e8; MSUN = 1.98847e30
PC = 3.0856775814913673e16; KPC = 1e3 * PC; MPC = 1e6 * PC
ARCSEC = math.pi / (180.0 * 3600.0)
H0_KMS = 67.4; H0_SI = H0_KMS * 1e3 / MPC; OMEGA_L = 0.6847
SQ_8PI3 = math.sqrt(8.0 * math.pi / 3.0); A0_PER_KAPPA = C_L * H0_SI / SQ_8PI3

SPARC_FILES = sorted(glob.glob(os.path.join(REPO, "real_research", "data", "sparc_data", "*_rotmod.dat")))
GAL = []
for f in SPARC_FILES:
    a = np.loadtxt(f, comments="#")
    if a.ndim != 2 or len(a) < 5: continue
    GAL.append(dict(r=a[:,0]*KPC, V=a[:,1], eV=a[:,2], Vg=a[:,3], Vd=a[:,4], Vb=a[:,5]))
NG = len(GAL)
UG = np.geomspace(0.05, 2.5, 240)

def chi2_sparc(a0, gals=None):
    gals = GAL if gals is None else gals
    tot = 0.0
    for g in gals:
        s2 = g["eV"]**2 + (0.05*g["V"])**2
        Vb2 = (g["Vg"]**2)[None,:] + UG[:,None]*(g["Vd"]**2 + g["Vb"]**2)[None,:]
        gN = Vb2*1e6/g["r"][None,:]
        Vp = np.sqrt(0.5*gN*(1.0+np.sqrt(1.0+4.0*a0/np.maximum(gN,1e-30)))*g["r"][None,:])/1e3
        c = np.sum((g["V"][None,:]-Vp)**2/s2[None,:], axis=1)
        tot += float(c.min())
    return tot

t0 = time.time()
r_sp = minimize_scalar(lambda a: chi2_sparc(a), bounds=(5e-11, 2.5e-10), method="bounded", options=dict(xatol=1e-16))
A0_SP = float(r_sp.x); CHI2_SP = float(r_sp.fun)
print("SPARC fit a0=%.6e chi2=%.3f  %.2fs" % (A0_SP, CHI2_SP, time.time()-t0))

t0 = time.time()
rng = np.random.default_rng(20261021)
boot = np.empty(200)
for k in range(200):
    idx = rng.integers(0, NG, NG)
    gg = [GAL[i] for i in idx]
    boot[k] = minimize_scalar(lambda a: chi2_sparc(a, gg), bounds=(5e-11, 2.5e-10),
                              method="bounded", options=dict(xatol=1e-16)).x
print("bootstrap %.2fs  frac=%.9f" % (time.time()-t0, boot.std(ddof=1)/np.median(boot)))

# ---- SLACS
DATA_SLACS = os.path.join(REPO, "real_research", "data", "slacs_auger2009_lenses.tsv")
_lines = [l.rstrip("\n") for l in open(DATA_SLACS, encoding="latin-1")]
_hi = [i for i,l in enumerate(_lines) if l.startswith("recno")][0]
_hdr = _lines[_hi].split("\t"); _col = {c:i for i,c in enumerate(_hdr)}
_raw = [l.split("\t") for l in _lines[_hi+3:] if l.strip() and not l.startswith("#")]
def _f(v):
    try: return float(v.strip())
    except Exception: return float("nan")
LENS = []
for r in _raw:
    if len(r) < len(_hdr): continue
    d = dict(name=r[_col["SDSS"]].strip(), zl=_f(r[_col["zlens"]]), zs=_f(r[_col["zsrc"]]),
             sig=_f(r[_col["sigma"]]), RE=_f(r[_col["RE"]]), lME=_f(r[_col["Mass"]]),
             Fc=_f(r[_col["Fc"]]), Fs=_f(r[_col["Fs"]]), ReV=_f(r[_col["Re(V)"]]))
    if all(np.isfinite([d["zl"],d["zs"],d["RE"],d["lME"],d["Fs"],d["Fc"]])) and d["RE"] > 0:
        LENS.append(d)
NL = len(LENS)
print("lenses", NL)

OM_SL, OL_SL, H0_SL = 0.3, 0.7, 70.0e3/MPC
_zg = np.linspace(0.0, 6.0, 8001)
_Eg = np.sqrt(OM_SL*(1.0+_zg)**3 + OL_SL)
_ig = np.concatenate([[0.0], np.cumsum(0.5*(1.0/_Eg[1:]+1.0/_Eg[:-1])*np.diff(_zg))])
def DC(z): return (C_L/H0_SL)*float(np.interp(z, _zg, _ig))
def DA(z): return DC(z)/(1.0+z)
def DAls(z1,z2): return (DC(z2)-DC(z1))/(1.0+z2)
def SICR(zl,zs): return C_L*C_L*DA(zs)/(4.0*math.pi*G_N*DA(zl)*DAls(zl,zs))

B4 = 7.669249934
def M2D_star(R, Re, n=4.0):
    b = B4 if n == 4.0 else 2.0*n-1.0/3.0+4.0/(405.0*n)+46.0/(25515.0*n*n)
    return gammainc(2.0*n, b*(np.asarray(R)/Re)**(1.0/n))
def M3D_star(r, Re, n=4.0):
    b = B4 if n == 4.0 else 2.0*n-1.0/3.0+4.0/(405.0*n)+46.0/(25515.0*n*n)
    nu = n*(3.0-(1.0-0.6097/n+0.05463/(n*n)))
    return gammainc(nu, b*(np.asarray(r)/Re)**(1.0/n))
GLX, GLW = np.polynomial.legendre.leggauss(400)
GLX = 0.5*(GLX+1.0); GLW = 0.5*GLW
def M2D_from_g(R, M3Df, a0, rmax=1.0e6*KPC):
    if R >= rmax: return 0.0
    U = math.acosh(max(rmax/R, 1.0+1e-9))
    u = GLX*U; r = R*np.cosh(u)
    gN = G_N*np.asarray(M3Df(r))/r**2
    g = 0.5*gN*(1.0+np.sqrt(1.0+4.0*a0/np.maximum(gN,1e-300)))
    return R*R/G_N*float(np.sum(GLW*g)*U)
def predict(d, a0, boost=1.0):
    sc = SICR(d["zl"], d["zs"])
    ME = 10.0**d["lME"]; REo = d["RE"]*KPC
    Re = d["ReV"]*ARCSEC*DA(d["zl"])
    A = boost*d["Fs"]*ME/M2D_star(REo, Re)
    M3f = lambda r: A*M3D_star(r, Re)*MSUN
    fun = lambda R: M2D_from_g(R, M3f, a0) - math.pi*R*R*sc
    Rs = np.logspace(math.log10(0.15*REo), math.log10(10.0*REo), 60)
    v = np.array([fun(x) for x in Rs])
    idx = np.where(np.diff(np.sign(v)) != 0)[0]
    if len(idx) == 0: return float("nan")
    return brentq(fun, Rs[idx[0]], Rs[idx[0]+1], xtol=1e-5*KPC)/KPC

t0 = time.time()
rat = np.array([predict(d, 1.132e-10)/d["RE"] for d in LENS])
print("70 predicts %.2fs median %.6f meanln %.6f" % (time.time()-t0, np.median(rat), np.log(rat).mean()))
