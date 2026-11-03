#!/usr/bin/env python3
"""TX1 shared: T loader with physical units, s2 leaf added to BK2's machinery by import, train rows per arm. FROZEN_CRITERIA.md. Data directory: env TX1_DATA, read only, untrusted. kappa = 1/2 FITTED; not theory closed."""
import hashlib, json, math, os, sys
sys.dont_write_bytecode = True
_H = os.path.dirname(os.path.abspath(__file__)); _RB = os.path.dirname(_H); sys.path[:0] = [_H, os.path.join(_RB, "BK2_dimensional_law_search")]
import bk2_lib as B
from bk2_lib import *
from astropy.io import fits
LANE = _H; DATA = os.environ.get("TX1_DATA", os.path.join(REPO, "_external_data", "xcop_thermo_2026_11_02"))
KEV = 1.602176634e-16; MP = 1.67262192e-27; MU = 0.6; KT2S = KEV / (MU * MP) * float(os.environ.get("TX1_S2X", "1"))
NAMES12 = ["A1644", "A1795", "A2029", "A2142", "A2255", "A2319", "A3158", "A3266", "A644", "A85", "RXC1825", "ZW1215"]
SEEDS = dict(c1=20261102, c2=1, c3=2)
B.DIM["s2"] = (2, -2, 0); B.NSPACE["s2"] = np.float64(0.0)  # M0: s2 = 0 on any row that doesn't carry one
_T = {}
def tload():
    if _T: return _T
    for n in NAMES12:
        with fits.open(os.path.join(DATA, n, f"{n}_temperature.fits")) as h: X = h["XRAY"].data.copy(); Z = h["XSZ"].data.copy(); H = dict(h["XRAY"].header)
        with fits.open(os.path.join(DATA, n, f"spectral_results_{n}.fits")) as h: Sp = h[1].data.copy()
        R5, T5 = float(H["R500"]), float(H["T500"]); same = len(X) == len(Sp); ke = np.asarray(Sp["KT"], float); er = 0.5 * (np.asarray(Sp["KT_LO"], float) + np.asarray(Sp["KT_HI"], float))
        if same: x = np.asarray(X["RW_X"], float); fac = ke / (np.asarray(X["T_X"], float) * T5)
        else: raise SystemExit(f"bin mismatch {n}")
        o = np.argsort(x); wt = np.asarray(Sp["NORM"], float) * np.asarray(Sp["RADIUS"], float) * np.asarray(Sp["WIDTH"], float); inx = x <= 1.0; Tew = float((ke[inx] * wt[inx]).sum() / wt[inx].sum())
        _T[n] = dict(x=x[o], kT=ke[o], ekT=er[o], R500=R5, T500=T5, M500=float(H["M500"]), ERR_M500=float(H["ERR_M500"]), z=float(H["REDSHIFT"]), fac=fac, Tew=Tew, arcmin=np.asarray(Sp["RADIUS"], float), xz=np.asarray(Z["RW_SZ"], float), kTz=np.asarray(Z["T_SZ"], float) * T5, ekTz=np.asarray(Z["eT_SZ"], float) * T5, TX=np.asarray(X["T_X"], float)[o])
    return _T
def T_at(n, r_kpc, sz=False):
    q = tload()[n]; x = r_kpc / q["R500"]
    if sz and x >= q["xz"][0]: return float(np.exp(np.interp(np.log(x), np.log(q["xz"]), np.log(q["kTz"])))), float(np.interp(np.log(x), np.log(q["xz"]), q["ekTz"] / q["kTz"]))
    return float(np.exp(np.interp(np.log(x), np.log(q["x"]), np.log(q["kT"])))), float(np.interp(np.log(x), np.log(q["x"]), q["ekT"] / q["kT"]))
def tau_nodes():
    """tau(x): median over the 12 of KT/T_ew on a log grid; T_SZ/T_ew carries it to its end. Held at the ends."""
    T = tload(); g = np.geomspace(0.02, 1.7, 40); P = []
    for n in NAMES12:
        q = T[n]; a = np.where((g >= q["x"][0]) & (g <= q["x"][-1]), np.exp(np.interp(np.log(g), np.log(q["x"]), np.log(q["kT"]))), np.nan); zz = np.where((g >= q["xz"][0]) & (g <= q["xz"][-1]), np.exp(np.interp(np.log(g), np.log(q["xz"]), np.log(q["kTz"]))), np.nan); P.append(np.where(np.isfinite(a), a, zz) / q["Tew"])
    return g, np.nanmedian(np.array(P), axis=0)
def _rows(a0, which): return [q for q in xcop_raw() if which is None or q["j"] % 2 == which]
def s_c():
    """Cluster scatter by the frozen rule: rms over rows of the residual of lg M_HSE on lg M_b fitted at each x."""
    R = xcop_raw(); res = []
    for x in (0.1, 0.2, 0.3, 0.5, 0.7):
        q = [r for r in R if r["x"] == x]; a = np.log10([r["gs"] + r["gg"] for r in q]) + 2 * np.log10([r["r"] for r in q]); b = np.log10([r["go"] for r in q]) + 2 * np.log10([r["r"] for r in q]); p = np.polyfit(a, b, 1); e = b - np.polyval(p, a); res += list(e * math.sqrt(len(e) / max(len(e) - 2, 1)))
    return float(np.sqrt(np.mean(np.square(res))))
SC = None
def xrows(a0, which, arm="real", part="tr", sz=False):
    """B.xcop rows with s2. Train part 'tr', holdout 'ho' scramble separately at the arm's seed."""
    global SC
    L = xcop(a0, which); R = _rows(a0, which); n = len(R); s = np.zeros(n); e = np.zeros(n)
    SC = s_c() if SC is None else SC
    for i, q in enumerate(R): kt, et = T_at(q["name"], q["r"] / (1e3 * PC), sz); s[i] = kt * KT2S; e[i] = et
    Ls = dict(L); s0 = s.copy()
    if arm in SEEDS: s = s[np.random.default_rng(SEEDS[arm] + (0 if part == "tr" else 1)).permutation(n)]
    if arm == "label": s = np.full(n, label_s2(a0))
    L["s2"] = s; L["s2_true"] = s0; L["eT"] = e / math.log(10); L["se_bk2"] = L["se"]; L["se"] = np.sqrt(L["se"] ** 2 + L["eT"] ** 2 + SC ** 2); L["name"] = np.array([q["name"] for q in R]); return L
def label_s2(a0):
    R = _rows(a0, 0); return float(np.median([T_at(q["name"], q["r"] / (1e3 * PC))[0] for q in R])) * KT2S
PLANTS = dict(p1="(I5(gb,a0)+pi*s2/r)", p2="(I5(gb,a0)*(1+pi*s2/Phi))")
def install(foot_arm_caps):
    """Monkeypatch bk2_search for leaves, rows, pool selection, chunk dir. Nothing in BK2 is edited."""
    import bk2_search as S
    arm, cap = foot_arm_caps; S.HERE = LANE
    if "s2" not in S.LEAF: S.LEAF.append("s2")
    _tr0, _cc0, _cl0 = S.train, S.concat, S.closure; S.CAPS["L2"] = (cap, cap)
    def train(foot, mode):
        a0, XT, ST, SS, sub = _tr0(foot, "real"); XT = xrows(a0, 0, arm, "tr"); ST["s2"] = np.zeros(len(ST["gb"])); SS["s2"] = np.zeros(3)
        if arm in PLANTS:
            for T in (XT, ST): T["go"] = ev(PLANTS[arm], T)
        return a0, XT, ST, SS, sub
    def concat(SS, XT, ST, sub):
        o = _cc0(SS, XT, ST, sub); o["s2"] = np.r_[SS["s2"], XT["s2"], ST["s2"][sub]]; return o
    def closure(L, n0, cap_d, cap_a):
        Cl = _cl0(L, n0, 2 * cap_d, 2 * cap_a); out = dict(Cl)
        for nk, vk, c_ in (("Dn", "Dv", cap_d), ("An", "Av", cap_a)):
            nm = Cl[nk]; t = [i for i, s in enumerate(nm) if "s2" in s]; f = [i for i, s in enumerate(nm) if "s2" not in s]; ks = sorted(t[:c_ // 2] + f[:c_ - min(len(t), c_ // 2)]); out[nk] = [nm[i] for i in ks]; out[vk] = Cl[vk][ks]; out["n_T_" + nk] = len(t)
        out["n_d_before"] = Cl["n_d_before"]; print("pool", {k: out[k] for k in ("n_T_Dn", "n_T_An")}, flush=True); return out
    S.train, S.concat, S.closure = train, concat, closure; return S
def t5_tags(): return [f"T5|{k}|{q}" for k in IK for q in range(81)]
def sha(p):
    h = hashlib.sha256(); h.update(open(p, "rb").read()); return h.hexdigest()
