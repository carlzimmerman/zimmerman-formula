#!/usr/bin/env python3
"""BK2 shared: leaves with dimensions, rows per sample, formula evaluation. FROZEN_CRITERIA.md, AMENDMENT_A1.md. kappa = 1/2 FITTED; not theory closed."""
import csv, json, math, os, pickle
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
import numpy as np
from astropy.io import fits
np.seterr(all="ignore")
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); REPO = os.path.dirname(RB)
A0S = dict(canonical=9.360324825027975e-11, alt=1.1312e-10); C = 299792458.0; G = 6.674e-11; MS = 1.989e30; PC = 3.0857e16; KMS2 = 1e6; AU = 1.496e11
FLOOR = 0.01  # A1: floor on dM/dlnr as a share of M, so Sigma_b, rho_b stay positive
# dimension vectors (L, T, M)
DIM = dict(G=(3, -2, -1), c=(1, -1, 0), a0=(1, -2, 0), rde=(-3, 0, 1), gs=(1, -2, 0), gg=(1, -2, 0), gb=(1, -2, 0), r=(1, 0, 0), Sig=(-2, 0, 1), rho=(-3, 0, 1), Phi=(2, -2, 0))
ACC = (1, -2, 0); NUL = (0, 0, 0)
def rde_of(a0): return (a0 / (0.5 * C)) ** 2 / G
def I1(x, y): return 0.5 * x + np.sqrt(0.25 * x * x + x * y)
def _gen(x, y, n): return x * (0.5 + np.sqrt(0.25 + (y / x) ** n)) ** (1.0 / n)
def I2(x, y): return x * np.sqrt(0.5 + np.sqrt(0.25 + (y / x) ** 2))
def I3(x, y): return _gen(x, y, 3)
def I4(x, y): return _gen(x, y, 4)
def I5(x, y): return x / -np.expm1(-np.sqrt(x / y))
def I6(x, y): return x * (1 + (y / x) ** 2) ** 0.25
IK = dict(I1=I1, I2=I2, I3=I3, I4=I4, I5=I5, I6=I6)
UNARY = dict(sqrt=np.sqrt, sq=np.square, inv=lambda x: 1.0 / x, log1p=np.log1p, inv1p=lambda x: 1.0 / (1.0 + x), expm=lambda x: np.exp(-x))
NSPACE = dict(np=np, pi=math.pi, **IK, **UNARY)
def ev(s, L):
    v = eval(s, {"__builtins__": {}}, {**NSPACE, **L}); return np.broadcast_to(v, np.shape(L["gb"])).astype(float)
def _local(gs, gg, r, dlnM, Phi, a0):
    gb = gs + gg; M = gb * r * r / G; dM = np.maximum(dlnM, FLOOR) * M / r
    return dict(gs=gs, gg=gg, gb=gb, r=r, Sig=dM / (2 * math.pi * r), rho=dM / (4 * math.pi * r * r), Phi=Phi, G=G, c=C, a0=a0, rde=rde_of(a0))
def _meta():
    return {g["name"]: g for g in pickle.load(open(os.path.join(RB, "SL1_symbolic_law_search", "cache", "sl1_cache.pkl"), "rb"))["gals"]}
class Rows(dict): pass
_SP = {}
def sparc_raw():
    """BF1's cuts; odd sorted positions train (1), even holdout (0). Per row disc, bulge, gas in (km/s)^2/kpc basis."""
    if _SP: return _SP
    meta = _meta(); names = sorted(meta); D = os.path.join(RB, "CRG1_clean_room_regrade", "inputs", "sparc", "rotmod"); out = {0: [], 1: []}
    for i, n in enumerate(names):
        if meta[n]["Q"] >= 3 or meta[n]["inc"] < 30: continue
        t = np.atleast_2d(np.loadtxt(os.path.join(D, n + "_rotmod.dat"), comments="#"))
        out[i % 2].append(dict(i=i, name=n, r=t[:, 0], v=t[:, 1], e=t[:, 2], vg=t[:, 3], vd=t[:, 4], vb=t[:, 5], vf=float(meta[n]["vf"] or 0)))
    _SP.update(out); return _SP
def sparc(split, a0, ud=0.5, ub=None):
    ub = 1.4 * ud if ub is None else ub; cols = {k: [] for k in ("gs", "gg", "r", "dl", "Phi", "go", "gid", "e")}
    for q in sparc_raw()[split]:
        r = q["r"]; R = r * 1e3 * PC; m = np.abs(q["vg"]) * q["vg"] + ud * np.abs(q["vd"]) * q["vd"] + ub * np.abs(q["vb"]) * q["vb"]; gb = m * KMS2 / R
        ok = (r > 0) & (q["v"] > 0) & (m > 0)
        if ok.sum() == 0: continue
        Mm = np.maximum(gb, 1e-30) * R * R / G; dl = np.gradient(np.log(Mm), np.log(R)) if len(r) > 1 else np.ones(len(r))
        Rl = R[-1]; inner = np.zeros(len(R))
        for k in range(len(R) - 2, -1, -1): inner[k] = inner[k + 1] + 0.5 * (gb[k] + gb[k + 1]) * (R[k + 1] - R[k])
        Phi = R * gb + inner + np.maximum(gb[-1], 0) * Rl
        gg = np.clip(np.abs(q["vg"]) * q["vg"], 0, None) * KMS2 / R; gg = np.minimum(gg, gb); gs = gb - gg
        for k in np.nonzero(ok)[0]:
            cols["gs"].append(gs[k]); cols["gg"].append(gg[k]); cols["r"].append(R[k]); cols["dl"].append(dl[k]); cols["Phi"].append(max(Phi[k], R[k] * gb[k])); cols["go"].append(q["v"][k] ** 2 * KMS2 / R[k]); cols["gid"].append(q["i"]); cols["e"].append(2 * q["e"][k] / q["v"][k] / math.log(10))
    A = {k: np.array(v) for k, v in cols.items()}; L = _local(A["gs"], A["gg"], A["r"], A["dl"], A["Phi"], a0); L["go"] = A["go"]; L["gid"] = A["gid"]; L["err"] = A["e"]; return L
_XC = []
def xcop_raw():
    if _XC: return _XC[0]
    D = os.path.join(REPO, "real_research", "data", "xcop"); rows = []
    def li(r, m, t): return float(10 ** np.interp(np.log10(t), np.log10(r), np.log10(m))) if r[0] <= t <= r[-1] else np.nan
    for j, n in enumerate(sorted(x for x in os.listdir(D) if os.path.exists(os.path.join(D, x, f"{x}_mstar.fits")))):
        with fits.open(os.path.join(D, n, f"{n}_hydro_mass.fits")) as h: hm = h[1].data.copy(); r5 = h[1].header["R500"]
        with fits.open(os.path.join(D, n, f"{n}_fgas_profile.fits")) as h: ga = h[1].data.copy(); rg = h[1].header["R500"]
        with fits.open(os.path.join(D, n, f"{n}_mstar.fits")) as h: st = h[2].data.copy()
        rgas = ga["RADIUS"] * rg; rst = st["RADIUS"]; rmax = min(rgas[-1], rst[-1]); grid = np.geomspace(max(rgas[0], rst[0], 0.05 * r5), rmax, 200); Mg = np.array([li(rgas, ga["MGAS"], t) for t in grid]); Ms = np.array([li(rst, st[st.names[1]], t) for t in grid]); gi = G * MS * (Mg + Ms) / (grid * 1e3 * PC) ** 2
        tail = gi[::-1]; Rg = grid * 1e3 * PC; cum = np.r_[0, np.cumsum(0.5 * (tail[1:] + tail[:-1]) * -np.diff(Rg[::-1]))][::-1]; Phig = Rg * gi + cum + gi[-1] * Rg[-1]
        for x in (0.1, 0.2, 0.3, 0.5, 0.7):
            r = x * r5; mh = li(hm["RADIUS"], hm["M_FORW"], r); mg = li(rgas, ga["MGAS"], r); ms = li(rst, st[st.names[1]], r)
            if not np.all(np.isfinite([mh, mg, ms])): continue
            eh = float(np.interp(r, hm["RADIUS"], hm["EM_FORW"])) / mh; mods = [li(hm["RADIUS"], hm[k], r) for k in ("M_NFW", "M_EIN", "M_ISO", "M_BUR", "M_FORW")]; sprd = float(np.std(np.log10(mods)))
            R = r * 1e3 * PC; f = G * MS / R ** 2; mb = lambda t: li(rgas, ga["MGAS"], t) + li(rst, st[st.names[1]], t); dl = math.log(mb(r * 1.05) / mb(r / 1.05)) / (2 * math.log(1.05))
            rows.append(dict(j=j, name=n, x=x, gs=f * ms, gg=f * mg, r=R, dl=dl, Phi=float(np.interp(math.log(r), np.log(grid), Phig)), go=f * mh, se=eh / math.log(10), sm=sprd))
    _XC.append(rows); return rows
def xcop(a0, which=None):
    R = xcop_raw(); R = [q for q in R if which is None or q["j"] % 2 == which]; A = {k: np.array([q[k] for q in R]) for k in ("gs", "gg", "r", "dl", "Phi", "go", "j", "se", "sm")}; L = _local(A["gs"], A["gg"], A["r"], A["dl"], A["Phi"], a0); L.update(go=A["go"], gid=A["j"], se=A["se"], sm=A["sm"]); return L
def solar(a0):
    GM = G * MS; r = np.array([9.54, 1.5237, 1.0]) * AU; gb = GM / r ** 2; rho = 8e-21 * (AU / r) ** 2; L = dict(gs=gb, gg=np.zeros(3), gb=gb, r=r, Sig=2 * r * rho, rho=rho, Phi=GM / r, G=G, c=C, a0=a0, rde=rde_of(a0)); return L
CAS = np.array([G * 6.7e-11 * MS / (9.54 * AU) ** 2, 3.66e-14, 3.66e-14])  # Saturn; 1 AU; Mars carried at 1 AU's
def lt(a0):
    Q = pickle.load(open(os.path.join(RB, "SL1_symbolic_law_search", "cache", "sl1_cache.pkl"), "rb"))["lt"]; K = 3.0857e19; M = 10 ** np.array([g["logMb"] for g in Q]); R = np.array([g["R"] for g in Q]) * K; gb = G * M * MS / R ** 2; gs = np.minimum(G * np.array([g["Mstar"] for g in Q]) * MS / R ** 2, gb); L = _local(gs, gb - gs, R, np.ones(len(R)), 2 * R * gb, a0); L["go"] = (np.array([g["V"] for g in Q]) * 1e3) ** 2 / R; return L
def dwarfs(a0, foot):
    """X51's rows through LW1's estimator: plain E and external-field E2, MC s."""
    ARR = list(csv.DictReader(open(os.path.join(REPO, "campaign_fresh_gravity", "CFG257_ufd_kinematics_scoping", "arroyo_polonio2026_tableA1.csv")))); arrf = {r["lvd_name"]: float(r["sig_free"]) / float(r["sig_f0"]) for r in ARR}; medf = float(np.median(list(arrf.values())))
    G5, MS5, PC5 = 6.67430e-11, 1.98847e30, 3.0856775814913673e16; GZ, MSZ, PCZ = 6.67430e-11, 1.989e30, 3.0856775814913673e16; KPC = 1e3 * PCZ; AH = 3 * KPC; MH = dict(MW=6.0e10, M31=1.0e11, field=6.0e10); CLS = ("MW ultra-faint", "bright M31", "M31 others", "MW classical", "LG field"); o = []
    for r in csv.DictReader(open(os.path.join(RB, "X1_hosted_recount", "x1_per_system.csv"))):
        if r["footing"] != foot or r["cls"] not in CLS: continue
        mv = float(r["M_V"]) if r["M_V"] not in ("", None) else None; b = arrf.get(r["name"], medf if (mv is not None and mv > -7.7) else 1.0); sc = float(r["sigma"]) * b; r12 = 4 / 3 * float(r["rh_pc"]) * PC5; Mb = 10 ** float(r["logMstar"]); gobs = 3 * (sc * 1e3) ** 2 / r12; gN = G5 * (Mb / 2) * MS5 / r12 ** 2; dh = float(r["d_host_kpc"]) if r["d_host_kpc"] not in ("", None) else None; host = r["host"] if r["host"] in MH else "field"
        gNh = GZ * MH[host] * MSZ / (dh * KPC + AH) ** 2 if dh else 0.0; ge = 0.5 * gNh * (1 + math.sqrt(1 + 4 * a0 / gNh)) if dh else 0.0; x = ge / a0; gNe = ge * x / (1 + x)
        o.append(dict(name=r["name"], cls=r["cls"], go=gobs, gN=gN, gNe=gNe, r=r12, s=float(r["sdMC[Newton]"])))
    A = {k: np.array([q[k] for q in o]) for k in ("go", "gN", "gNe", "r", "s")}; one = np.ones(len(o)); L = _local(A["gN"], 0 * one, A["r"], one, 2 * A["r"] * A["gN"], a0); L["go"] = A["go"]; Le = _local(A["gN"] + A["gNe"], 0 * one, A["r"], one, 2 * A["r"] * (A["gN"] + A["gNe"]), a0); Ln = _local(np.maximum(A["gNe"], 1e-40), 0 * one, A["r"], one, 2 * A["r"] * np.maximum(A["gNe"], 1e-40), a0)
    return dict(L=L, Le=Le, Ln=Ln, cls=np.array([q["cls"] for q in o]), name=[q["name"] for q in o], s=A["s"], gNe=A["gNe"], CLS=CLS)
def boot_med(E, s, rng, n=10000):
    N = len(E); ix = rng.integers(0, N, (n, N)); return float(np.median(E)), float(np.std(np.median(E[ix] + s[ix] * rng.standard_normal((n, N)), axis=1)))
def groups_Z(s, foot, a0):
    """SL1's groups path with g = F(leaves) on the stellar Hernquist profile. Real profile, so Sigma_b, rho_b, Phi_b are the profile's."""
    Q = pickle.load(open(os.path.join(RB, "SL1_symbolic_law_search", "cache", "sl1_cache.pkl"), "rb"))["groups"]; XG, LXG, RH, MHh = Q["XG"], Q["LXG"], Q["RHO_H"], Q["M_H"]; Gq, MSq, KP, HR = Q["G"], Q["MS"], Q["KP"], Q["HERN_RE"]; D, SL = [], []
    def one(o, dl):
        lM = o["lM"] + dl; Mb = 10 ** lM * MSq; ah = o["Re"] * KP / HR; rr = XG * ah; gb = Gq * Mb * MHh / rr ** 2; rho = Mb * RH / ah ** 3; L = dict(gs=gb, gg=0 * gb, gb=gb, r=rr, Sig=2 * rr * rho, rho=rho, Phi=Gq * Mb / (rr + ah), G=G, c=C, a0=a0, rde=rde_of(a0)); g = ev(s, L)
        if not (np.all(np.isfinite(g)) and np.all(g > 0)): return None
        gN = g / (Gq * Mb / ah ** 2); s2 = float(np.trapz(4 * np.pi * XG ** 2 * RH * XG * gN * XG, LXG) / 3.0) * Gq * Mb / ah; return 0.5 * math.log10(s2) - 3.0
    for o in Q["rows"]:
        v, p, m = one(o, 0.0), one(o, 0.01), one(o, -0.01)
        if None in (v, p, m): return None
        D.append(o["ls"] - v); SL.append((p - m) / 0.02)
    D = np.array(D); n = len(D); me = float(D.mean()); se = float(D.std(ddof=1) / math.sqrt(n)); sy = float(np.mean(SL) * 0.10); tot = math.hypot(se, sy); Z = me / tot; ver = "NOT DIAGNOSTIC" if tot > 0.045 else ("CONSISTENT" if abs(Z) < 2 else ("ABOVE LAW" if Z >= 2 else "BELOW LAW")); return dict(mean=me, Z=Z, verdict=ver, PASS=ver == "CONSISTENT")
