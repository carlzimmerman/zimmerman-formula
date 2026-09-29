import numpy as np, os, json, hashlib
from scipy.special import i0e, k0e, i1e, k1e, ellipk
from scipy.integrate import quad
from scipy.optimize import brentq, minimize_scalar

ROOT = "/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/data/"
G = 6.6743e-11; MSUN = 1.98847e30; KPC = 3.0857e19
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}

def _rows(fn):
    out = []
    for l in open(ROOT + fn):
        if l.startswith("#") or not l.strip() or l.startswith("name\t"): continue
        out.append(l.rstrip("\n").split("\t"))
    return out

def load():
    og = _rows("ogle2019_super_spirals.tsv")
    sm = {r[0]: r for r in _rows("simard2011_ogle_bulge_disc.tsv")}
    D = {k: [] for k in "name alt z Rd i logMs logMg vmax dv r BT Re_b Rd_s i_s Rhl rb rd".split()}
    for r in og:
        s = sm[r[0]]
        D["name"].append(r[0]); D["alt"].append(r[1]); D["z"].append(float(r[2]))
        D["Rd"].append(float(r[4])); D["i"].append(float(r[5]))
        D["logMs"].append(float(r[7])); D["logMg"].append(float(r[8]))
        D["vmax"].append(float(r[11])); D["dv"].append(float(r[12])); D["r"].append(float(r[13]))
        D["BT"].append(float(s[3])); D["Re_b"].append(float(s[8])); D["Rd_s"].append(float(s[5])); D["i_s"].append(float(s[7]))
        D["Rhl"].append(float(s[9])); D["rb"].append(float(s[11])); D["rd"].append(float(s[12]))
    return {k: (np.array(v) if k not in ("name", "alt") else v) for k, v in D.items()}

# ---- kernels
def nu_rar(y):
    y = np.asarray(y, float); return 1.0 / (1.0 - np.exp(-np.sqrt(y)))
def _hpeak():
    f = lambda y: -(y * (nu_rar(y) - 1.0))
    r = minimize_scalar(f, bounds=(1.0, 6.0), method="bounded", options={"xatol": 1e-12})
    return r.x, -r.fun
YP, HP = _hpeak()
def nu_mono(y):
    y = np.asarray(y, float)
    h = np.where(y <= YP, y * (nu_rar(y) - 1.0), HP * (1.0 + 0.05 * np.log((y + YP) / (2 * YP))))
    return 1.0 + h / y
def nu_p2(y):
    y = np.asarray(y, float); return np.sqrt(1.0 + 1.0 / y)
def nu_one(y): return np.ones_like(np.asarray(y, float))
KERN = {"mono": nu_mono, "rar": nu_rar, "p2": nu_p2, "newton": nu_one}

# ---- Newtonian fields (SI)
def g_freeman(r, Rd, M):
    y = r / (2 * Rd)
    b = i0e(y) * k0e(y) - i1e(y) * k1e(y)          # exponent cancels: I(y)K(y) = i_e*k_e
    return (2 * G * M / Rd) * y * y * b / r
def g_point(r, M): return G * M / r**2
def g_sph(r, Rd, M):
    x = r / Rd; return G * M * (1 - (1 + x) * np.exp(-x)) / r**2
def g_hern(r, a, M): return G * M / (r + a) ** 2

def baryon_g(D, P):
    """P: dict of options. Returns g_N (m/s^2) per galaxy, Mb (Msun), r (m)."""
    r = D["r"] * P.get("rscale", 1.0) * KPC
    Ms = 10 ** (D["logMs"] + P.get("dMs", 0.0)); Mg = 10 ** (D["logMg"] + P.get("dMg", 0.0)) * P.get("gasfac", 1.0)
    Mb = Ms + Mg
    model = P.get("model", "bulge")
    Rd = (D["Rd"] if P.get("Rd_src", "simard") == "ogle" else D["Rd_s"]).copy()
    if P.get("Rd_src") == "rhl": Rd = D["Rhl"] / 1.678
    Rd = Rd * P.get("Rdscale", 1.0)
    if "Rdcap" in P: Rd = np.minimum(Rd, P["Rdcap"])
    if "Rd_override" in P:
        for k, v in P["Rd_override"].items(): Rd[k] = v
    Rdm = Rd * KPC
    if model == "disc":
        return g_freeman(r, Rdm, Mb * MSUN), Mb, r
    if model == "point":
        return g_point(r, Mb * MSUN), Mb, r
    if model == "sph":
        return g_sph(r, Rdm, Mb * MSUN), Mb, r
    if model == "bulge":
        BT = np.clip(D["BT"] * P.get("BTscale", 1.0) + P.get("dBT", 0.0), 0.0, 0.999)
        if "BT_override" in P: BT = P["BT_override"]
        q = P.get("q", 1.0)
        f = q * BT / (q * BT + (1 - BT))
        Mbulge = Ms * f; Mdisc = Ms * (1 - f) + Mg
        a = D["Re_b"] * P.get("bscale", 1.0) / 1.8153 * KPC
        gb = g_point(r, Mbulge * MSUN) if P.get("bulge_point") else g_hern(r, a, Mbulge * MSUN)
        return g_freeman(r, Rdm, Mdisc * MSUN) + gb, Mb, r
    raise ValueError(model)

def offsets(D, P, kern="mono", foot="canonical", vfac=1.0, incl=0.0):
    gN, Mb, r = baryon_g(D, P)
    a0 = A0[foot] * P.get("a0fac", 1.0)
    if P.get("asym"):
        vp = (G * Mb * MSUN * a0) ** 0.25
    else:
        g = KERN[kern](gN / a0) * gN
        vp = np.sqrt(g * r)
    vo = D["vmax"] * 1e3 * vfac
    if incl != 0.0:
        s0 = np.sin(np.radians(D["i"])); s1 = np.sin(np.radians(np.clip(D["i"] + incl, 1, 89.9)))
        vo = vo * s0 / s1
    return np.log10(vo / vp), gN / a0, Mb, vp

def _mean_stats(off, idx):
    x = off[idx]; n = len(x)
    return x.mean(), x.std(ddof=1) / np.sqrt(n)

def floor_terms(D, P, kern, foot, kind, idx, vfac=1.0):
    """model/M*/gas floor for subset idx (mean-based); kind 'disc' (CFG40) or 'bulge' (CFG56)."""
    m = lambda PP: offsets(D, PP, kern, foot, vfac)[0][idx].mean()
    if kind == "disc":
        means = [m({**P, "model": "disc"}), m({**P, "model": "point"}), m({**P, "model": "sph"})]
    else:
        means = [m(P), m({**P, "dBT": 0.10}), m({**P, "dBT": -0.10})]
    fm = (max(means) - min(means)) / 2
    fs = abs(m({**P, "dMs": 0.2}) - m({**P, "dMs": -0.2})) / 2
    fg = abs(m({**P, "dMg": 0.3}) - m({**P, "dMg": -0.3})) / 2
    return fm, fs, fg, float(np.sqrt(fm**2 + fs**2 + fg**2))

def slope(off, logMb, idx):
    x = logMb[idx]; y = off[idx]; n = len(x)
    sxx = ((x - x.mean()) ** 2).sum()
    b = ((x - x.mean()) * (y - y.mean())).sum() / sxx
    res = y - y.mean() - b * (x - x.mean())
    se = np.sqrt((res**2).sum() / (n - 2) / sxx)
    return b, se

def summary(D, P, kern="mono", foot="canonical", kind="bulge", idx=None, vfac=1.0, incl=0.0, fixed_floor=None):
    N = len(D["vmax"])
    idx = np.arange(N) if idx is None else np.asarray(idx)
    off, y, Mb, vp = offsets(D, P, kern, foot, vfac, incl)
    idx9 = np.array([i for i in idx if D["vmax"][i] > 340])
    mean, sem = _mean_stats(off, idx)
    fl = floor_terms(D, P, kern, foot, kind, idx, vfac) if fixed_floor is None else fixed_floor
    sig = np.hypot(sem, fl[3])
    m9, sem9 = _mean_stats(off, idx9) if len(idx9) > 1 else (np.nan, np.nan)
    sig9 = np.hypot(sem9, fl[3])
    b, se = slope(off, np.log10(Mb), idx)
    return dict(mean=mean, sem=sem, floor=fl, sig=sig, z=mean / sig, z_scatter=mean / sem,
                slope=b, slope_se=se, slope_z=b / se, n9=len(idx9), m9=m9, sem9=sem9, sig9=sig9, z9=m9 / sig9,
                H1=abs(mean / sig) < 2, H2=(abs(mean / sig) < 2 and abs(b / se) < 2 and abs(m9 / sig9) < 2),
                off=off, y=y, Mb=Mb, vp=vp)
