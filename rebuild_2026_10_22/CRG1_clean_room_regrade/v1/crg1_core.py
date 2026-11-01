"""CRG1 clean-room core: constants, core masses, solve_r0, Sigma_coll, eta, contract, IO.
kappa = 1/2 is FITTED. Cold dark energy is a gravitating field component."""
import os, json, math, hashlib, glob, csv, time, resource
os.environ.setdefault("OMP_NUM_THREADS", "1"); os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import numpy as np
from scipy.optimize import minimize_scalar, brentq

HERE = os.path.dirname(os.path.abspath(__file__))
INP = os.path.join(HERE, "inputs")
PART = os.path.join(HERE, os.environ.get("CRG1_PARTIALS", "partials"))
CACHE = os.path.join(HERE, os.environ.get("CRG1_CACHE", "cache"))
os.makedirs(PART, exist_ok=True); os.makedirs(CACHE, exist_ok=True)
ONESET = os.environ.get("CRG1_ONESET", "") == "1"   # A5(b): one CODATA set everywhere
MUT_NU1 = os.environ.get("CRG1_MUTATE_NU1", "") == "1"

_CG, _CM, _CMpc = 6.67430e-11, 1.98847e30, 3.0856775814913673e22
class Set:
    def __init__(s, G, Msun, Mpc, pc): s.G, s.Msun, s.Mpc, s.pc = G, Msun, Mpc, pc
if ONESET:
    E = F = T = P = D = Set(_CG, _CM, _CMpc, _CMpc / 1e6)
else:
    E = Set(6.67430e-11, 1.98847e30, 3.0857e22, 3.0857e16)
    F = Set(6.674e-11, 1.989e30, 3.0857e22, 3.0857e16)
    T = Set(6.67430e-11, 1.98847e30, 3.0856775814913673e22, 3.0856775814913673e16)
    P = Set(6.674e-11, 1.989e30, 3.0857e22, 3.0857e16)
    D = Set(6.67430e-11, 1.98847e30, 3.0856775814913673e22, 3.0856775814913673e16)
PC2 = E.pc ** 2
KPC = E.Mpc / 1e3
KG_PC2 = F.Msun / F.pc ** 2
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
BGS = ["A_c2b_refit", "B_cfg886_bg"]

SC = json.load(open(os.path.join(INP, "scalars.json")))
Om_nat, h_nat, wb_nat = SC["native"]["Om"], SC["native"]["h"], SC["native"]["wb"]
Ob_nat = wb_nat / h_nat ** 2
R_nat = (Om_nat - Ob_nat) / Ob_nat
f_c = R_nat / (1 + R_nat)

def nu(y):
    if MUT_NU1: return np.ones_like(np.asarray(y, float))
    return 0.5 + np.sqrt(0.25 + 1.0 / y)

def law(gN, a0):
    gN = np.asarray(gN, float); out = gN.copy(); m = gN > 0
    out[m] = nu(gN[m] / a0) * gN[m]
    return out

def B_B(x):
    x = np.asarray(x, float)
    return np.log1p(x * x) + 2 * np.log1p(x) - 2 * np.arctan(x)
def B_S(x):
    x = np.asarray(x, float)
    return 4 * (np.arcsinh(x) - x / np.sqrt(1 + x * x))
B1 = 3 * math.log(2) - math.pi / 2
BS1 = float(B_S(1.0))

def _bb(x): return math.log1p(x * x) + 2 * math.log1p(x) - 2 * math.atan(x)
def _bs(x): return 4 * (math.asinh(x) - x / math.sqrt(1 + x * x))
_SCAL = {id(B_B): _bb, id(B_S): _bs}

COUNT = {"saturated": 0, "lo_root_guard": 0}
def solve_r0(M, R, S, B):
    b = _SCAL[id(B)]
    lc = math.log(math.pi * S)
    def lm(l):
        v = b(R / math.exp(l))
        return lc + 2 * l + math.log(v) if v > 0 else -1e300
    lo, hi = math.log(R * 1e-6), math.log(R * 1e3)
    res = minimize_scalar(lambda l: -lm(l), bounds=(lo, hi), method="bounded", options={"xatol": 1e-10})
    lpk = res.x
    lnM = math.log(M)
    if lm(lpk) < lnM:
        COUNT["saturated"] += 1
        return math.exp(lpk)
    a = math.log(R * 1e-7)
    if lm(a) > lnM:
        COUNT["lo_root_guard"] += 1
        return math.exp(a)
    return math.exp(brentq(lambda l: lm(l) - lnM, a, lpk, xtol=1e-14, maxiter=400))

def rho_crit0(h, G, Mpc):
    return 3 * (100 * h * 1e3 / Mpc) ** 2 / (8 * math.pi * G)
def R200_of(M200, h, G, Mpc):
    return (3 * M200 / (4 * math.pi * 200 * rho_crit0(h, G, Mpc))) ** (1.0 / 3)

def _tophat(x):
    x = np.asarray(x, float); out = np.ones_like(x); m = x > 1e-4
    xm = x[m]; out[m] = 3 * (np.sin(xm) - xm * np.cos(xm)) / xm ** 3
    out[~m] = 1 - x[~m] ** 2 / 10
    return out

class BG:
    """Background: sigma(M) table, D(z), Sigma_coll, EM1 map."""
    def __init__(s, tag):
        s.tag = tag
        d = np.load(os.path.join(INP, "background", "class_%s.npz" % tag))
        s.k, s.P = d["k_h_Mpc"], d["Pk_Mpc3_h3"]
        s.zg, s.Dg = d["zg"], d["Dg"]
        s.Om = float(d["Omega_m_class"]); s.Onu = float(d["Omega_nu"]); s.h = float(d["h"])
        b = SC["backgrounds"][tag]; p = b["params"]
        s.wb, s.wc = p["omega_b"], p["omega_cdm"]
        s.a, s.b = b["em1_map_a"], b["em1_map_b"]; s.sigma8_given = b["sigma8"]
        s.rho_m0 = s.Om * 2.775e11 * s.h ** 2
        Osig = (s.wb + s.wc) / s.h ** 2 + s.Onu
        s.rho_sig = Osig * 2.775e11 * s.h ** 2
        s.lgM = np.linspace(7.0, 16.5, 191)
        s.sig2 = np.array([s._s2(10 ** m) for m in s.lgM])
    def _s2_R(s, R):
        lnk = np.log(s.k)
        f = s.k ** 3 * s.P * _tophat(s.k * R) ** 2 / (2 * math.pi ** 2)
        return float(np.trapz(f, lnk))
    def _s2(s, M):
        return s._s2_R((3 * M / (4 * math.pi * s.rho_sig)) ** (1.0 / 3) * s.h)
    def sigma8(s): return math.sqrt(s._s2_R(8.0))
    def s2i(s, M): return np.interp(np.log10(M), s.lgM, s.sig2)
    def sigcoll(s, M):
        """Sigma_coll(M), Msun/pc^2. M in Msun, scalar or array."""
        M = np.asarray(M, float)
        Sq = np.sqrt(np.maximum(s.s2i(M / 2) - s.s2i(M), 0))
        Df = 1.686 / (1.686 + 0.974 * Sq)
        zf = np.where(Df >= 1, 0.0, np.interp(-Df, -s.Dg, s.zg))
        rho = 18 * math.pi ** 2 * s.rho_m0 * (1 + zf) ** 3
        rf = (3 * (M / 2) / (4 * math.pi * rho)) ** (1.0 / 3)
        return rho * rf / 1e12
    def lgM200(s, lgMb): return s.a + s.b * (lgMb - 10)

_bg = {}
def bg(tag):
    if tag not in _bg: _bg[tag] = BG(tag)
    return _bg[tag]

def cf_interp(M, nodes):
    return np.interp(np.log10(M), [12, 13, 14], nodes)

X48 = [SC["x48_A2_cf"][k] for k in ("1e+12", "1e+13", "1e+14")]
CF_C3 = [7.082 * c / X48[2] for c in X48]
def eta_C3(M): return 4 / (3 * B1) * cf_interp(M, CF_C3) ** 1.25
def eta_A2(M): return 4 / (3 * B1) * cf_interp(M, X48) ** 1.25
def eta_A3(M, fs): 
    n = SC["ce1_a3_cf"][fs]
    return 4 / (3 * BS1) * cf_interp(M, [n["1e+12"], n["1e+13"], n["1e+14"]]) ** 1.25

class NR:
    """NR2's table under a reading of A1: eta12 anchor + rho10, rho11."""
    def __init__(s, eta12, rho10, rho11, reading):
        s.eta12, s.rho10, s.rho11, s.reading = eta12, rho10, rho11, reading
        t = SC["nr2"]["cf_table"]
        s.cf = [4 * (eta12 / 10.82) ** 0.8, t["1e+13"], t["1e+14"]]
    def eta(s, M): return 4 / (3 * BS1) * cf_interp(M, s.cf) ** 1.25
    def lowfac(s, Mt):
        return 10 ** np.interp(np.log10(Mt), [10, 11, 12], [math.log10(s.rho10), math.log10(s.rho11), 0.0])
    def S_msunpc2(s, Mt, b):
        return f_c * s.eta(Mt) * b.sigcoll(Mt) * s.lowfac(Mt)
    def S(s, Mt, b):
        return float(s.S_msunpc2(Mt, b) * E.Msun / PC2)

def S_H(M, a0, etaf, b):
    return max(a0 / (2 * math.pi * E.G), float(etaf(M) * b.sigcoll(M)) * E.Msun / PC2)

def contract(r, Mb, M0, F):
    """Blumenthal-type adiabatic operator on a cold dark energy mass profile."""
    r = np.asarray(r, float); lr = np.log(r); rf = r.copy(); M0r = np.asarray(M0, float)
    num = r * M0r * (1 + F)
    for _ in range(100):
        mb = np.interp(np.log(np.maximum(rf, r[0])), lr, Mb)
        rn = num / np.maximum(mb + M0r, 1e-300)
        rf = 0.5 * rf + 0.5 * rn
    order = np.maximum.accumulate(rf)
    return np.interp(lr, np.log(np.maximum(order, 1e-300)), M0r, left=0.0, right=M0r[-1])

def wls(n, d, X):
    A = np.einsum("i,ij,ik->jk", d, X, X); y = np.einsum("i,ij->j", n, X)
    return np.linalg.solve(A, y)

# ---------- IO
def fmt(o):
    if isinstance(o, dict): return {str(k): fmt(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [fmt(v) for v in o]
    if isinstance(o, np.ndarray): return fmt(o.tolist())
    if isinstance(o, (np.floating, float)):
        v = float(o)
        if math.isnan(v): return "nan"
        if math.isinf(v): return "inf" if v > 0 else "-inf"
        return float("%.10g" % v)
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, (np.bool_,)): return bool(o)
    return o

def dumps(o): return json.dumps(fmt(o), sort_keys=True, indent=1)

def write_atomic(path, text):
    tmp = path + ".tmp%d" % os.getpid()
    with open(tmp, "w") as f: f.write(text)
    os.replace(tmp, path)

def save_part(name, obj): write_atomic(os.path.join(PART, name + ".json"), dumps(obj) + "\n")
def part_path(name): return os.path.join(PART, name + ".json")
def have_part(name): return os.path.exists(part_path(name))
def load_part(name): return json.load(open(part_path(name)))

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""): h.update(c)
    return h.hexdigest()

def log(msg):
    line = "%s %s" % (time.strftime("%H:%M:%S"), msg)
    print(line, flush=True)

def peak_mb(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1048576.0
