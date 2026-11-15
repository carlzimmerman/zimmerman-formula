#!/usr/bin/env python3
"""SQM1 (Euclid Q1 total projected mass inside 5/h kpc from stars under the law).
Frozen criteria: FROZEN_CRITERIA.md (commit d91049bd52).

Sonnenfeld et al. (arXiv:2611.00224) give the selection-corrected mean log10(M5 h/Msun) of elliptical galaxies as a
function of luminosity, size and redshift.  Here the law S (and law B, reported) is applied to the stars alone
(de Vaucouleurs body, M* = Y L with a stellar M/L prior from the paper's own rest-frame colour and published
M/L-colour relations; IMF as a continuous bracket) and the predicted amplitude at the pivot, luminosity slope and
redshift trend are graded per footing.

Lensing machinery copied from closure_2026_11_12/EUC1_eclipse_saturation_ceiling/euc1.py (commit 5926a21305):
b_ser, nu_ps, M2D_frac, M3D_frac, g_law, M2D_from_gfun (Gauss-Legendre in r = R cosh u), Cosmo, and the SLACS
known answer K2 (slacs_ratio).  Constants as EUC1.

Run (paths as arguments):
  python3 -I -B sqm1.py --csv sqm1_paper_numbers.csv --slacs <repo>/real_research/data/slacs_auger2009_lenses.tsv \
      --outdir <dir> [--html <dir>/2611.00224v1.html]
  SQM1_MUTATE=newton python3 -I -B sqm1.py ...    (must exit 1)
  SQM1_MUTATE=null   python3 -I -B sqm1.py ...    (astronomical units, 800 nodes; must exit 0)

kappa = 1/2 FITTED.  Footings never pooled.  Adopts nothing.
"""
import argparse, csv, hashlib, json, math, os, sys
import numpy as np
from scipy.optimize import brentq
from scipy.special import gammainc

MUT = (os.environ.get("SQM1_MUTATE", "") or "").strip()

# ------------------------------------------------------------------ constants (EUC1 / A55)
G_SI, C, MSUN = 6.67430e-11, 2.99792458e8, 1.98847e30
PC = 3.0856775814913673e16
KPC = 1.0e3 * PC
ARCSEC = math.pi / (180.0 * 3600.0)
FOOT = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
FOOT_H_NATIVE = {"canonical": 0.667, "alt": 0.806}      # AZ2 FROZEN_CRITERIA §3 at Omega_m 0.30
if MUT == "newton":
    FOOT = {k: 1.0e-30 for k in FOOT}
SHA_HTML = "f0e6f872a44345b32939591cb1a28e692531e5bbc6ef35ac57803d67acd09b53"
SHA_SLACS = "d78d7627d6bbcc0789bde334ca607f760b40b5b7f8a1d04720eae8206f2d7b6d"
DELTAS = np.round(np.arange(0.0, 0.248 + 1e-9, 0.004), 6)
if DELTAS[-1] < 0.248 - 1e-9:
    DELTAS = np.append(DELTAS, 0.248)
LGRID = np.round(np.arange(10.40, 11.00 + 1e-9, 0.05), 6)
ZGRID = np.round(np.arange(0.20, 0.80 + 1e-9, 0.05), 6)

OUT = []
def P(s=""):
    print(s); OUT.append(s)

# ------------------------------------------------------------------ units (SI primary; astro for the null twin)
class Units:
    def __init__(self, astro=False, nodes=400):
        self.astro = astro
        if astro:   # kpc, Msun, (km/s)^2/kpc
            self.G = 4.300917e-6; self.kpc = 1.0; self.msun = 1.0
            self.acc = 1.0e-6 * KPC         # 1 m/s^2 in (km/s)^2/kpc
        else:
            self.G = G_SI; self.kpc = KPC; self.msun = MSUN; self.acc = 1.0
        x, w = np.polynomial.legendre.leggauss(nodes)
        self.X = 0.5 * (x + 1.0); self.W = 0.5 * w

# ------------------------------------------------------------------ Sersic / Prugniel-Simien (EUC1 copy)
B4 = 7.669249934
def b_ser(n):
    n = np.asarray(n, float)
    b = 2.0 * n - 1.0 / 3.0 + 4.0 / (405.0 * n) + 46.0 / (25515.0 * n * n)
    return np.where(n == 4.0, B4, b)
def nu_ps(n):
    n = np.asarray(n, float)
    return n * (3.0 - (1.0 - 0.6097 / n + 0.05463 / (n * n)))
def M2D_frac(R, Re, n): return gammainc(2.0 * np.asarray(n, float), b_ser(n) * (R / Re) ** (1.0 / np.asarray(n, float)))
def M3D_frac(r, Re, n): return gammainc(nu_ps(n), b_ser(n) * (r / Re) ** (1.0 / np.asarray(n, float)))

def g_law(gN, a0, law):
    gN = np.asarray(gN, float)
    if law == "S":
        return 0.5 * gN * (1.0 + np.sqrt(1.0 + 4.0 * a0 / np.maximum(gN, 1e-300)))
    return np.sqrt(gN * gN + a0 * gN)

def M2D_from_gfun(R, gfun, U_, rmax):
    """M_2D(<R) = (R^2/G) int_R^rmax g dr/sqrt(r^2-R^2), r = R cosh u (EUC1's M2D_from_gfun)."""
    Umax = math.acosh(max(rmax / R, 1.0 + 1e-9))
    r = R * np.cosh(U_.X * Umax)
    return R * R / U_.G * float(np.sum(U_.W * gfun(r)) * Umax)

# ------------------------------------------------------------------ cosmology (EUC1 copy; K2 only)
class Cosmo:
    def __init__(self, H0_kms, Om):
        self.H0 = H0_kms * 1.0e3 / (1.0e6 * PC); self.Om = Om; self.OL = 1.0 - Om
        x = np.linspace(0.0, math.log(1.0e5 + 1.0), 400001)
        z = np.expm1(x)
        f = (1.0 + z) / np.sqrt(Om * (1.0 + z) ** 3 + self.OL)
        self._x = x
        self._I = np.concatenate([[0.0], np.cumsum(0.5 * (f[1:] + f[:-1]) * np.diff(x))])
    def DC(self, z): return (C / self.H0) * np.interp(np.log1p(z), self._x, self._I)
    def DA(self, z): return self.DC(z) / (1.0 + np.asarray(z, float))
    def sigcr(self, zl, zs):
        dl, ds = self.DC(zl), self.DC(zs)
        return C * C / (4.0 * math.pi * G_SI * self.DA(zl)) * ds / (ds - dl)

# ------------------------------------------------------------------ inputs
def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for blk in iter(lambda: f.read(1 << 20), b""): h.update(blk)
    return h.hexdigest()

def load_csv(path):
    D = {}
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            D[r["key"]] = dict(v=float(r["value"]), e=float(r["error"]) if r["error"].strip() else None,
                               src=r["source"], raw=r["value"], rawe=r["error"])
    return D

# ------------------------------------------------------------------ model
class Model:
    def __init__(self, D, U_):
        self.D = D; self.U = U_
        v = lambda k: D[k]["v"]
        self.mu_C0, self.zeta_C = v("mu_C0"), v("zeta_C")
        self.bell_a, self.bell_b = v("bell_ar_gr"), v("bell_br_gr")
        self.bell_to_chab = v("zib_bell_to_chabrier")
        self.zib_a, self.zib_b = v("zib_ar_gr"), v("zib_br_gr")
        self.passive = -v("passive_dlogL_z1_to_0") / 1.0       # d log Y / dz at fixed L, linear over z 0..1
        self.salp_offset = -self.bell_to_chab + math.log10(1.0 / v("bell_diet_mass_fraction"))
    def colour(self, z, dmuC=0.0, dzeta=0.0):
        return 2.5 * ((self.mu_C0 + dmuC) + (self.zeta_C + dzeta) * (z - 0.5))
    def logY(self, z, rel="bell", zroute="colour", delta=0.0, dmuC=0.0, dzeta=0.0):
        a, b = (self.bell_a, self.bell_b) if rel == "bell" else (self.zib_a, self.zib_b)
        off = self.bell_to_chab if rel == "bell" else 0.0
        if zroute == "colour":
            return a + off + b * self.colour(z, dmuC, dzeta) + delta
        return a + off + b * self.colour(0.5, dmuC, 0.0) + self.passive * (z - 0.5) + delta
    def a0z(self, a0, z, cpl=False):
        if not cpl: return a0
        w0, wa = -0.752, -0.86
        F = (1.0 + z) ** (3.0 * (1.0 + w0 + wa)) * math.exp(-3.0 * wa * z / (1.0 + z))
        return a0 * math.sqrt(F)
    def logM5h(self, logL, logRe, z, h, a0_si, logY, law="S", n=4.0, rmax_kpc=1.0e6, cpl=False):
        U_ = self.U
        L = 10.0 ** logL / h ** 2                       # Lsun
        M = 10.0 ** logY * L * U_.msun
        Re = 10.0 ** logRe / h * U_.kpc
        R5 = 5.0 / h * U_.kpc
        a0 = self.a0z(a0_si, z, cpl) * U_.acc
        gf = lambda r: g_law(U_.G * M * M3D_frac(r, Re, n) / r ** 2, a0, law)
        M5 = M2D_from_gfun(R5, gf, U_, rmax_kpc * U_.kpc) / U_.msun
        return math.log10(M5 * h)
    # paper's size relation, Eq. 23
    def muR(self, logL, z):
        v = lambda k: self.D[k]["v"]
        x = logL - v("logL_t"); s = 1.0 / (1.0 + math.exp(-v("b_L") * x))
        return v("mu_R0") + v("zeta_R") * (z - 0.5) + v("rho_L1") * x * (1.0 - s) + v("rho_L2") * x * s

def fit_slope(x, y): return float(np.polyfit(np.asarray(x, float), np.asarray(y, float), 1)[0])

# ------------------------------------------------------------------ predictions for one configuration
def predict(Mo, cfg, a0, h, delta):
    rel, zr, law, n, rmax, cpl = cfg["rel"], cfg["zroute"], cfg["law"], cfg["n"], cfg["rmax"], cfg["cpl"]
    logRe0 = cfg["logRe"]
    lY = Mo.logY(0.5, rel, zr, delta)
    A = Mo.logM5h(10.7, logRe0, 0.5, h, a0, lY, law, n, rmax, cpl)
    if cfg.get("along"):
        ys = [Mo.logM5h(l, Mo.muR(l, 0.5), 0.5, h, a0, lY, law, n, rmax, cpl) for l in LGRID]
    else:
        ys = [Mo.logM5h(l, logRe0, 0.5, h, a0, lY, law, n, rmax, cpl) for l in LGRID]
    bL = fit_slope(LGRID, ys)
    yz = [Mo.logM5h(10.7, logRe0, z, h, a0, Mo.logY(z, rel, zr, delta), law, n, rmax, cpl) for z in ZGRID]
    bz = fit_slope(ZGRID, yz)
    return A, bL, bz

def sigma_pred(Mo, cfg, a0, h, delta):
    """propagated error of mu_C0 (+-0.001) and zeta_C (+-0.003) through the M/L relation."""
    rel, zr = cfg["rel"], cfg["zroute"]
    eC, eZ = Mo.D["mu_C0"]["e"], Mo.D["zeta_C"]["e"]
    A0, _, bz0 = predict(Mo, cfg, a0, h, delta)
    # amplitude: shift of log Y from mu_C0
    dY = Mo.logY(0.5, rel, zr, delta, dmuC=eC) - Mo.logY(0.5, rel, zr, delta)
    A1, _, _ = predict(Mo, cfg, a0, h, delta + dY)
    sA = abs(A1 - A0)
    if zr == "colour":
        dslope = (Mo.logY(1.0, rel, zr, 0.0, dzeta=eZ) - Mo.logY(0.0, rel, zr, 0.0, dzeta=eZ)) - \
                 (Mo.logY(1.0, rel, zr, 0.0) - Mo.logY(0.0, rel, zr, 0.0))
        resp = (A1 - A0) / dY if dY != 0 else 1.0
        sZ = abs(dslope * resp)
    else:
        sZ = 0.0
    return sA, 0.0, sZ

def word(pred, obs, sig):
    d = pred - obs
    if d > 2.0 * sig: return "HIGH"
    if d < -2.0 * sig: return "LOW"
    return "PASS"

def interval(mask):
    idx = np.where(mask)[0]
    if len(idx) == 0: return None
    return [float(DELTAS[idx[0]]), float(DELTAS[idx[-1]]), bool(np.all(np.diff(idx) == 1))]

def grade(Mo, cfg, a0, h, obs):
    rows = []
    for d in DELTAS:
        A, bL, bz = predict(Mo, cfg, a0, h, float(d))
        rows.append((float(d), A, bL, bz))
    sA, _, sZ = sigma_pred(Mo, cfg, a0, h, 0.124)
    sig = dict(A=math.hypot(obs["sA"], sA), L=math.hypot(obs["sL"], 0.0), z=math.hypot(obs["sz"], sZ))
    W = {"A": [], "L": [], "z": []}
    for d, A, bL, bz in rows:
        W["A"].append(word(A, obs["A"], sig["A"])); W["L"].append(word(bL, obs["L"], sig["L"]))
        W["z"].append(word(bz, obs["z"], sig["z"]))
    passes = {q: np.array([w == "PASS" for w in W[q]]) for q in W}
    allp = passes["A"] & passes["L"] & passes["z"]
    qword = {}
    for q in W:
        u = sorted(set(W[q]))
        qword[q] = u[0] if len(u) == 1 else "IMF-DEPENDENT(" + "/".join(u) + ")"
    fail_all = [q for q in ("A", "L", "z") if not passes[q].any()]
    names = {"A": "amplitude", "L": "beta_L", "z": "beta_z"}
    if allp.all():
        row = "PASSES"
    elif fail_all:
        row = "STILL FAILS [" + ", ".join("%s %s" % (names[q], "/".join(sorted(set(W[q])))) for q in fail_all) + "]"
    elif not allp.any():
        row = "STILL FAILS [no single IMF passes all three]"
    else:
        row = "NO VERDICT"
    i0, i1 = 0, len(DELTAS) - 1
    return dict(row=row, sigma=sig, sigma_pred=dict(A=sA, z=sZ), qword=qword,
                pass_interval={q: interval(passes[q]) for q in passes}, all_pass_interval=interval(allp),
                chabrier=dict(A=rows[i0][1], bL=rows[i0][2], bz=rows[i0][3],
                              words=[W["A"][i0], W["L"][i0], W["z"][i0]]),
                salpeter=dict(A=rows[i1][1], bL=rows[i1][2], bz=rows[i1][3],
                              words=[W["A"][i1], W["L"][i1], W["z"][i1]]),
                grid=[dict(delta=r[0], A=r[1], bL=r[2], bz=r[3]) for r in rows])

# ------------------------------------------------------------------ known answers
def load_slacs(path):
    def fl(v):
        try: return float(v)
        except Exception: return float("nan")
    lines = [l.rstrip("\n") for l in open(path, encoding="latin-1")]
    hi = [i for i, l in enumerate(lines) if l.startswith("recno")][0]
    hdr = lines[hi].split("\t"); col = {c: i for i, c in enumerate(hdr)}
    L = []
    for l in lines[hi + 3:]:
        if not l.strip() or l.startswith("#"): continue
        r = l.split("\t")
        if len(r) < len(hdr): continue
        d = dict(zl=fl(r[col["zlens"]]), zs=fl(r[col["zsrc"]]), RE=fl(r[col["RE"]]), lME=fl(r[col["Mass"]]),
                 Fs=fl(r[col["Fs"]]), Fc=fl(r[col["Fc"]]), ReV=fl(r[col["Re(V)"]]))
        if all(np.isfinite([d["zl"], d["zs"], d["RE"], d["lME"], d["Fs"], d["Fc"]])) and d["RE"] > 0: L.append(d)
    return L

def slacs_median(SL, U_, a0_k=1.132e-10):
    AUGER = Cosmo(70.0, 0.3)
    out = []
    for d in SL:
        sc = float(AUGER.sigcr(d["zl"], d["zs"])); REo = d["RE"] * KPC
        Re = d["ReV"] * ARCSEC * float(AUGER.DA(d["zl"]))
        A = d["Fs"] * 10.0 ** d["lME"] / float(M2D_frac(REo, Re, 4.0)) * MSUN
        gf = lambda r: g_law(G_SI * A * M3D_frac(r, Re, 4.0) / r ** 2, a0_k, "S")
        fun = lambda R: M2D_from_gfun(R, gf, U_, 1.0e6 * KPC) - math.pi * R * R * sc
        Rs = np.logspace(math.log10(0.15 * REo), math.log10(10.0 * REo), 60)
        v = np.array([fun(x) for x in Rs]); idx = np.where(np.diff(np.sign(v)) != 0)[0]
        if len(idx): out.append(brentq(fun, Rs[idx[0]], Rs[idx[0] + 1], xtol=1e-5 * KPC) / REo)
    return float(np.median(out)), len(out)

# ================================================================== main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True)
    ap.add_argument("--slacs", required=True)
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--html", default=None)
    args = ap.parse_args()
    tag = "sqm1" + ("_MUTATE_" + MUT if MUT else "")
    astro = MUT == "null"
    U_ = Units(astro=astro, nodes=800 if astro else 400)
    Usi = Units(astro=False, nodes=400)
    RES = dict(lane="SQM1", criteria_commit="d91049bd52", mutate=MUT, footings=FOOT,
               units="astro (kpc, Msun, km/s), 800 nodes" if astro else "SI, 400 nodes")
    P("SQM1 (Euclid Q1 M5 inside 5/h kpc from stars under the law)%s" % ("   *** MUTATE = %s ***" % MUT if MUT else ""))
    P("footings (m/s^2): canonical %.4e, alt %.4e; units: %s" % (FOOT["canonical"], FOOT["alt"], RES["units"]))

    # ---------------------------------------------------------------- inputs
    P("\n[inputs]")
    D = load_csv(args.csv)
    P("  transcription CSV: %d numbers, sha256 %s" % (len(D), sha256(args.csv)[:16]))
    hs = sha256(args.slacs)
    P("  SLACS file sha256 %s  %s" % (hs[:16], "matches" if hs == SHA_SLACS else "DOES NOT MATCH"))
    if hs != SHA_SLACS: sys.exit("slacs hash mismatch")
    if args.html:
        hh = sha256(args.html); ok = hh == SHA_HTML
        P("  paper HTML sha256 %s  %s" % (hh[:16], "matches the frozen hash" if ok else "DOES NOT MATCH"))
        if not ok: sys.exit("html hash mismatch")
        txt = open(args.html, encoding="utf-8").read()
        miss = [k for k, r in D.items() if r["src"].startswith("arXiv:2611") and r["raw"] not in txt]
        P("  transcription check: every paper value string found in the HTML: %s" % ("yes" if not miss else "MISSING %s" % miss))
        RES["transcription_missing"] = miss
    v = lambda k: D[k]["v"]
    obs = dict(A=v("mu_M0"), sA=D["mu_M0"]["e"], L=v("beta_L"), sL=D["beta_L"]["e"], z=v("beta_z"), sz=D["beta_z"]["e"])
    P("  observed: mu_M0 = %.3f +- %.3f, beta_L = %.2f +- %.2f, beta_z = %.2f +- %.2f, beta_R = %.2f +- %.2f"
      % (obs["A"], obs["sA"], obs["L"], obs["sL"], obs["z"], obs["sz"], v("beta_R"), D["beta_R"]["e"]))
    Mo = Model(D, U_)
    gr = Mo.colour(0.5)
    P("  rest-frame (g - r)_AB at z 0.5 = %.4f;  d(g-r)/dz = %.4f" % (gr, 2.5 * Mo.zeta_C))
    P("  Chabrier log Y_r(z 0.5): Bell %.4f (Y %.3f), Zibetti %.4f (Y %.3f); Salpeter offset %.4f dex"
      % (Mo.logY(0.5, "bell"), 10 ** Mo.logY(0.5, "bell"), Mo.logY(0.5, "zib"), 10 ** Mo.logY(0.5, "zib"), Mo.salp_offset))
    P("  d log Y/dz at fixed L: Bell colour %.4f, Zibetti colour %.4f, passive %.4f"
      % (Mo.logY(1, "bell") - Mo.logY(0, "bell"), Mo.logY(1, "zib") - Mo.logY(0, "zib"), Mo.passive))
    RES["inputs"] = dict(gr=gr, logY_bell=Mo.logY(0.5, "bell"), logY_zib=Mo.logY(0.5, "zib"), salp_offset=Mo.salp_offset)

    # ---------------------------------------------------------------- known answers
    P("\n[known answers]")
    CK = {}
    def ck(k, what, val, ok):
        CK[k] = dict(what=what, value=val, ok=bool(ok))
        P("  %s %-3s %s : %s" % ("PASS" if ok else "FAIL", k, what, val))
    Mp = 1.0e11 * U_.msun
    e1 = abs(M2D_from_gfun(5 * U_.kpc, lambda r: U_.G * Mp / r ** 2, U_, 1e6 * U_.kpc) / Mp - 1.0)
    sig = 250.0 * (1.0 if astro else 1.0e3)
    e2 = max(abs(M2D_from_gfun(R * U_.kpc, lambda r: 2 * sig * sig / r, U_, 1e6 * U_.kpc) /
                 (math.pi * sig * sig * R * U_.kpc / U_.G) - 1.0) for R in (3.0, 12.0))
    ck("K1", "point mass to 1e-6; SIS deflection constant to 1e-4", "%.1e ; %.1e" % (e1, e2), e1 < 1e-6 and e2 < 1e-4)
    SL = load_slacs(args.slacs)
    med, nsl = slacs_median(SL, Usi)
    ck("K2", "EUC1 K2 with copied code: SLACS median R_E,pred/R_E,obs = 0.885 +- 0.005 (N %d)" % nsl, "%.4f" % med,
       abs(med - 0.885) <= 0.005)
    h0 = 0.70; lY0 = Mo.logY(0.5, "bell")
    MN = Model(D, U_)
    a = MN.logM5h(10.7, 0.5, 0.5, h0, 1.0e-30, lY0)
    b = math.log10(10 ** lY0 * 10 ** 10.7 / h0 ** 2 * float(M2D_frac(5.0, 10 ** 0.5, 4.0)) * h0)
    ck("K3", "Newton limit: projected M5 = Y L M2D_frac(R5) to 1e-5", "%.2e" % abs(10 ** (a - b) - 1), abs(10 ** (a - b) - 1) < 1e-5)
    muR_piv = Mo.muR(10.7, 0.5)
    ML5 = 10 ** (v("mu_M0") + v("beta_R") * (muR_piv - 0.5)) / (10 ** 10.7 * float(M2D_frac(5.0, 10 ** muR_piv, 4.0)))
    ck("K4", "paper: M5/L5 at the pivot with average size (log R_e h %.3f) = 6.7 +- 0.35 Msun h/Lsun" % muR_piv,
       "%.3f" % ML5, abs(ML5 - v("ML5_pivot")) <= 0.35)
    zS, lS = v("slacs_cmp_z"), v("slacs_cmp_logL")
    k5 = v("mu_M0") + v("beta_z") * (zS - 0.5) + v("beta_L") * (lS - 10.7) + v("beta_R") * (Mo.muR(lS, zS) - 0.5)
    ck("K5", "paper: model at log L 10.67, z 0.2, average size = 11.38 +- 0.03", "%.3f" % k5, abs(k5 - v("slacs_cmp_model")) <= 0.03)
    Lnu = v("Lsun_r_W_per_Hz")
    Mab = -2.5 * math.log10(Lnu / (4 * math.pi * (10 * PC) ** 2 * 3631e-26))
    ck("K6", "SI: Lsun,r 6.00e11 W/Hz -> M_sun,r(AB) = 4.65 +- 0.02", "%.3f" % Mab, abs(Mab - 4.65) <= 0.02)
    RES["checks"] = CK
    if not all(c["ok"] for c in CK.values()):
        P("\nA KNOWN ANSWER FAILED: NOT EVALUABLE; no word is printed.")
        RES["verdict"] = "NOT EVALUABLE"
        json.dump(RES, open(os.path.join(args.outdir, tag + "_results.json"), "w"), indent=1)
        open(os.path.join(args.outdir, tag + ".out"), "w").write("\n".join(OUT) + "\n")
        sys.exit(3)

    # ---------------------------------------------------------------- primary
    base = dict(rel="bell", zroute="colour", law="S", n=4.0, rmax=1.0e6, cpl=False, logRe=0.5)
    P("\n[primary: law S, Bell M/L (Chabrier + delta), a0(z) flat, h = 0.70, de Vaucouleurs, pivot log R_e h = 0.5]")
    PRI = {}
    for nm, a0 in FOOT.items():
        G_ = grade(Mo, base, a0, h0, obs); PRI[nm] = G_
        c, s = G_["chabrier"], G_["salpeter"]
        P("  %-9s Chabrier: A = %.4f  beta_L = %.4f  beta_z = %.4f   words %s" % (nm, c["A"], c["bL"], c["bz"], c["words"]))
        P("  %-9s Salpeter: A = %.4f  beta_L = %.4f  beta_z = %.4f   words %s" % (nm, s["A"], s["bL"], s["bz"], s["words"]))
        P("  %-9s sigma A %.4f (pred %.4f), beta_L %.3f, beta_z %.4f (pred %.4f)"
          % (nm, G_["sigma"]["A"], G_["sigma_pred"]["A"], G_["sigma"]["L"], G_["sigma"]["z"], G_["sigma_pred"]["z"]))
        P("  %-9s per-quantity words over delta [0, 0.248]: A %s, beta_L %s, beta_z %s"
          % (nm, G_["qword"]["A"], G_["qword"]["L"], G_["qword"]["z"]))
        P("  %-9s delta intervals that pass: A %s, beta_L %s, beta_z %s; all three %s"
          % (nm, G_["pass_interval"]["A"], G_["pass_interval"]["L"], G_["pass_interval"]["z"], G_["all_pass_interval"]))
        P("  %-9s ROW: %s" % (nm, G_["row"]))
    RES["primary"] = PRI

    # Newton beside it (stars only), and law B
    P("\n[Newton beside it (stars only), and law B (reported, never the word)]")
    NB = {}
    for nm, a0 in FOOT.items():
        Gn = grade(Mo, base, 1.0e-30, h0, obs)
        Gb = grade(Mo, dict(base, law="B"), a0, h0, obs)
        NB[nm] = dict(newton=dict(row=Gn["row"], chabrier=Gn["chabrier"], salpeter=Gn["salpeter"], qword=Gn["qword"],
                                  pass_interval=Gn["pass_interval"]),
                      lawB=dict(row=Gb["row"], chabrier=Gb["chabrier"], salpeter=Gb["salpeter"], qword=Gb["qword"],
                                pass_interval=Gb["pass_interval"]))
        for lab, g in (("Newton", Gn), ("law B", Gb)):
            P("  %-9s %-6s Chab A %.4f bL %.4f bz %.4f | Salp A %.4f bL %.4f bz %.4f | pass delta A %s | ROW %s"
              % (nm, lab, g["chabrier"]["A"], g["chabrier"]["bL"], g["chabrier"]["bz"], g["salpeter"]["A"],
                 g["salpeter"]["bL"], g["salpeter"]["bz"], g["pass_interval"]["A"], g["row"]))
        if nm == "canonical": pass
    RES["newton_lawB"] = NB

    # beta_R reading (reported only)
    P("\n[reading, not graded: beta_R = d log M5 / d log R_e at fixed L, observed %.2f +- %.2f]" % (v("beta_R"), D["beta_R"]["e"]))
    BR = {}
    for nm, a0 in FOOT.items():
        for lab, aa in (("law S", a0), ("Newton", 1e-30)):
            ys = [Mo.logM5h(10.7, r, 0.5, h0, aa, lY0) for r in (0.4, 0.45, 0.5, 0.55, 0.6)]
            BR["%s_%s" % (nm, lab)] = fit_slope([0.4, 0.45, 0.5, 0.55, 0.6], ys)
            P("  %-9s %-6s Chabrier: beta_R,pred = %.3f" % (nm, lab, BR["%s_%s" % (nm, lab)]))
    RES["beta_R_reading"] = BR

    if MUT == "newton":
        ref = json.load(open(os.path.join(args.outdir, "sqm1_results.json")))
        okL = all(abs(PRI[k]["chabrier"]["bL"] - 1.0) <= 0.005 for k in FOOT)
        drop = {k: ref["primary"][k]["chabrier"]["A"] - PRI[k]["chabrier"]["A"] for k in FOOT}
        okA = all(d >= 0.03 for d in drop.values())
        P("\n[MUTATE newton] beta_L,pred = %s (must be 1.000 +- 0.005): %s; amplitude drop vs reference %s (must be >= 0.03): %s"
          % ({k: round(PRI[k]["chabrier"]["bL"], 4) for k in FOOT}, okL, {k: round(d, 4) for k, d in drop.items()}, okA))
        RES["mutate_bit"] = bool(okL and okA)
        json.dump(RES, open(os.path.join(args.outdir, tag + "_results.json"), "w"), indent=1)
        open(os.path.join(args.outdir, tag + ".out"), "w").write("\n".join(OUT) + "\n")
        sys.exit(1 if (okL and okA) else 2)

    # ---------------------------------------------------------------- brackets
    P("\n[brackets, law S; ROW per footing; FRAGILE if any changes the primary row]")
    BRK = {}
    dmu = (Mo.muR(10.71, 0.5) - Mo.muR(10.69, 0.5)) / 0.02
    def run_b(name, cfg, hmap=None, obs_=None):
        for nm, a0 in FOOT.items():
            hh = hmap[nm] if hmap else h0
            g = grade(Mo, cfg, a0, hh, obs_ or obs)
            BRK[name + "_" + nm] = dict(row=g["row"], qword=g["qword"], pass_interval=g["pass_interval"],
                                        all_pass_interval=g["all_pass_interval"], chabrier=g["chabrier"],
                                        salpeter=g["salpeter"], sigma=g["sigma"])
            P("  %-28s %-9s Chab A %.3f bL %.3f bz %.3f | Salp A %.3f bL %.3f bz %.3f | A %s L %s z %s | ROW %s"
              % (name, nm, g["chabrier"]["A"], g["chabrier"]["bL"], g["chabrier"]["bz"], g["salpeter"]["A"],
                 g["salpeter"]["bL"], g["salpeter"]["bz"], g["qword"]["A"], g["qword"]["L"], g["qword"]["z"], g["row"]))
    run_b("B-Zib", dict(base, rel="zib"))
    run_b("B-pass", dict(base, zroute="passive"))
    run_b("B-h 0.6774", base, {k: 0.6774 for k in FOOT})
    run_b("B-h 0.73", base, {k: 0.73 for k in FOOT})
    run_b("B-h footing-native", base, FOOT_H_NATIVE)
    run_b("B-cpl", dict(base, cpl=True))
    obs_size = dict(obs, A=obs["A"] + v("beta_R") * (muR_piv - 0.5))
    run_b("B-size (log R_e h %.3f)" % muR_piv, dict(base, logRe=muR_piv), obs_=obs_size)
    obs_al = dict(obs, L=obs["L"] + v("beta_R") * dmu, sL=math.hypot(0.07, 0.07 * dmu))
    P("  (B-along: d mu_R/d log L at the pivot = %.4f; observed slope along the relation %.3f +- %.3f)"
      % (dmu, obs_al["L"], obs_al["sL"]))
    run_b("B-along", dict(base, along=True), obs_=obs_al)
    sel = 0.5 * (v("lens_minus_pop_logL10.6") + v("lens_minus_pop_bright"))
    run_b("B-sel (+%.3f)" % sel, base, obs_=dict(obs, A=obs["A"] + sel))
    run_b("B-n6", dict(base, n=6.0))
    run_b("B-rmax 300 kpc", dict(base, rmax=300.0))
    RES["brackets"] = BRK
    RES["dmuR_dlogL"] = dmu

    # ---------------------------------------------------------------- verdict
    P("\n[verdict per footing, law S]")
    V = {}
    for nm in FOOT:
        changed = [k.rsplit("_", 1)[0] for k, b in BRK.items() if k.endswith("_" + nm) and b["row"] != PRI[nm]["row"]]
        w = PRI[nm]["row"] + (" FRAGILE" if changed else "")
        V[nm] = dict(word=w, brackets_changing=changed)
        P("  %-9s %s%s" % (nm, w, ("   (changed by: %s)" % changed) if changed else ""))
    RES["verdict"] = V

    if MUT == "null":
        ref = json.load(open(os.path.join(args.outdir, "sqm1_results.json")))
        dmax = 0.0; same = True
        for nm in FOOT:
            for e in ("chabrier", "salpeter"):
                for q in ("A", "bL", "bz"):
                    dmax = max(dmax, abs(PRI[nm][e][q] - ref["primary"][nm][e][q]))
            same &= PRI[nm]["row"] == ref["primary"][nm]["row"] and V[nm]["word"] == ref["verdict"][nm]["word"]
            for k, b in BRK.items():
                for e in ("chabrier", "salpeter"):
                    for q in ("A", "bL", "bz"):
                        dmax = max(dmax, abs(b[e][q] - ref["brackets"][k][e][q]))
                same &= b["row"] == ref["brackets"][k]["row"]
        ok = dmax < 1e-4 and same
        P("\n[NULL twin] max |difference| vs the SI run over primary and brackets = %.2e (must be < 1e-4); words identical: %s -> %s"
          % (dmax, same, "AGREES, exit 0" if ok else "DISAGREES, exit 2"))
        RES["null_agrees"] = bool(ok); RES["null_dmax"] = dmax
        json.dump(RES, open(os.path.join(args.outdir, tag + "_results.json"), "w"), indent=1)
        open(os.path.join(args.outdir, tag + ".out"), "w").write("\n".join(OUT) + "\n")
        sys.exit(0 if ok else 2)

    json.dump(RES, open(os.path.join(args.outdir, tag + "_results.json"), "w"), indent=1)
    open(os.path.join(args.outdir, tag + ".out"), "w").write("\n".join(OUT) + "\n")

if __name__ == "__main__":
    main()
