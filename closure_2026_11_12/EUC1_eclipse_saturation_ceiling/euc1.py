#!/usr/bin/env python3
"""EUC1 (ECLIPSE SATURATION CEILING).  Frozen criteria: FROZEN_CRITERIA.md (commit 898cefb457).

For every Euclid DR1 strong lens the projected mass inside the Einstein radius is at least
pi R_E^2 Sigma_cr(z_l, z_s -> infinity).  The law fixes the most it can supply from the catalogued
Salpeter stars.  b = log10 of the stellar-mass boost the law needs with the source at infinity
(a lower bound on the true boost).  Verdict per footing on law S from f25 = fraction(b > 0.25).

Run:
  python3 -I euc1.py --data-dir <dir with the two ECLIPSE csv files>
  EUC1_MUTATE=newton python3 -I euc1.py --data-dir <dir>      (must exit 1)

kappa = 1/2 FITTED.  Footings never pooled.  One-sided: no outcome favours the framework.
"""
import argparse, csv, hashlib, json, math, os, sys, time
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.special import gammainc

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUT = (os.environ.get("EUC1_MUTATE", "") or "").strip()

# ------------------------------------------------------------------ constants (A55's)
G, C, MSUN = 6.67430e-11, 2.99792458e8, 1.98847e30
PC = 3.0856775814913673e16
KPC = 1.0e3 * PC
ARCSEC = math.pi / (180.0 * 3600.0)
FOOT = {"canonical": 9.3603e-11, "alt": 1.132e-10}
if MUT == "newton":
    FOOT = {k: 1.0e-30 for k in FOOT}
B_STAR = 0.25            # dex, frozen margin
F_BROKEN, F_HOLDS = 0.25, 0.10
ZS_INF = 1100.0
SEED = 20261112
SHA = {"eclipse_dr1_catalogue_key_v20261103.csv": "65338917534c9c767c4f45732d29937d2dfb7fd68083cdfd05aec994ee4fa9ab",
       "ECLIPSE_object_catalogue.csv": "8247a4d5f23513b83be6db5a8244234f0cc1e1ac66e4de1a54983ae5984786b2"}

OUT = []
def P(s=""):
    print(s); OUT.append(s)

# ------------------------------------------------------------------ cosmology (flat LCDM, no radiation)
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
    def DL(self, z): return self.DC(z) * (1.0 + np.asarray(z, float))
    def sigcr(self, zl, zs):
        dl, ds = self.DC(zl), self.DC(zs)
        return C * C / (4.0 * math.pi * G * self.DA(zl)) * ds / (ds - dl)

EUCLID = Cosmo(67.74, 0.3089)      # the catalogue's own
AUGER = Cosmo(70.0, 0.3)           # SLACS tables

# ------------------------------------------------------------------ Sersic / Prugniel-Simien (A55's forms)
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

GLX, GLW = np.polynomial.legendre.leggauss(400)
GLX = 0.5 * (GLX + 1.0); GLW = 0.5 * GLW

def M2D_from_gfun(R, gfun, rmax=1.0e6 * KPC):
    """M_2D(<R) = (R^2/G) int_R^rmax g dr/sqrt(r^2-R^2), r = R cosh u (scalar R; A55's M2D_from_g)."""
    U = math.acosh(max(rmax / R, 1.0 + 1e-9))
    r = R * np.cosh(GLX * U)
    return R * R / G * float(np.sum(GLW * gfun(r)) * U)

class Engine:
    """vectorised over lenses: nodes and Newtonian field at B = 1 are built once."""
    def __init__(self, RE, Re, n, M, rmax=1.0e6 * KPC):
        RE, Re, n, M = (np.asarray(v, float) for v in (RE, Re, n, M))
        U = np.arccosh(np.maximum(rmax / RE, 1.0 + 1e-9))
        r = RE[:, None] * np.cosh(GLX[None, :] * U[:, None])
        self.gN0 = G * M[:, None] * M3D_frac(r, Re[:, None], n[:, None]) / r ** 2
        self.pref = RE ** 2 / G * U
        self.N = len(RE)
    def M2D(self, B, a0, law):
        B = np.broadcast_to(np.asarray(B, float), (self.N,))
        return self.pref * np.sum(GLW[None, :] * g_law(B[:, None] * self.gN0, a0, law), axis=1)
    def solve_b(self, Mmin, a0, law, nit=48):
        lo = np.full(self.N, -3.0); hi = np.full(self.N, 3.0)
        for _ in range(nit):
            mid = 0.5 * (lo + hi)
            up = self.M2D(10.0 ** mid, a0, law) < Mmin
            lo = np.where(up, mid, lo); hi = np.where(up, hi, mid)
        return 0.5 * (lo + hi)

# ------------------------------------------------------------------ statistics
def stats(b, rng=None, nboot=2000):
    b = np.asarray(b, float); N = len(b)
    out = dict(N=int(N), f25=float(np.mean(b > B_STAR)), f0=float(np.mean(b > 0.0)), b_med=float(np.median(b)))
    if rng is None: rng = np.random.default_rng(SEED)
    f25, f0, med = [], [], []
    for _ in range(nboot // 100):
        idx = rng.integers(0, N, (100, N)); bb = b[idx]
        f25.append(np.mean(bb > B_STAR, axis=1)); f0.append(np.mean(bb > 0.0, axis=1)); med.append(np.median(bb, axis=1))
    for k, v in (("f25", f25), ("f0", f0), ("b_med", med)):
        v = np.concatenate(v)
        out[k + "_lo"], out[k + "_hi"] = float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))
    return out
def word(st):
    if st["f25_lo"] >= F_BROKEN: return "CEILING BROKEN"
    if st["f25_hi"] <= F_HOLDS: return "CEILING HOLDS"
    return "NO VERDICT"
def fmt(st):
    return ("N=%5d  f25 = %.3f [%.3f, %.3f]  f0 = %.3f [%.3f, %.3f]  b_med = %+.3f [%+.3f, %+.3f]"
            % (st["N"], st["f25"], st["f25_lo"], st["f25_hi"], st["f0"], st["f0_lo"], st["f0_hi"],
               st["b_med"], st["b_med_lo"], st["b_med_hi"]))

# ------------------------------------------------------------------ data
def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for blk in iter(lambda: f.read(1 << 20), b""): h.update(blk)
    return h.hexdigest()
def fl(v):
    try: return float(v)
    except Exception: return float("nan")
def load(data_dir):
    kp = os.path.join(data_dir, "eclipse_dr1_catalogue_key_v20261103.csv")
    op = os.path.join(data_dir, "ECLIPSE_object_catalogue.csv")
    for p in (kp, op):
        h = sha256(p); ok = h == SHA[os.path.basename(p)]
        P("  sha256 %s  %s  %s" % (os.path.basename(p), h[:16], "matches the frozen hash" if ok else "DOES NOT MATCH"))
        if not ok: sys.exit("data hash mismatch")
    obj = {}
    with open(op, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f): obj[r["Unique_Identifier"]] = r
    rows = []
    with open(kp, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            o = obj.get(r["unique_identifier"])
            if o is None: continue
            rows.append(dict(
                id=r["unique_identifier"], grade=r["lens_grade"].strip(),
                success=r["lens_model_success"].strip() == "True", final=r["final_sample"].strip() == "True",
                large=o["large_system_warning"].strip() == "True", disc=o["disc_deflector"].strip() == "True",
                zspec=fl(o["desi_deflector_specz"]) if o["desi_deflector_specz"].strip() else float("nan"),
                z=fl(r["eclipse_median_phz"]), zlo=fl(r["eclipse_min70_phz"]), zhi=fl(r["eclipse_max70_phz"]),
                lm=fl(r["eclipse_log_survived_mass_med"]), lm_lo=fl(r["eclipse_log_survived_mass_low"]),
                lm_up=fl(r["eclipse_log_survived_mass_upp"]),
                tE=fl(r["eclipse_effective_einstein_radius"]), tE_lo=fl(r["eclipse_effective_einstein_radius_lower_1_sigma"]),
                tE_up=fl(r["eclipse_effective_einstein_radius_upper_1_sigma"]), tSIE=fl(r["eclipse_einstein_radius"]),
                te=fl(r["eclipse_effective_radius"]), te_lo=fl(r["eclipse_effective_radius_lower_1_sigma"]),
                te_up=fl(r["eclipse_effective_radius_upper_1_sigma"]), n=fl(r["eclipse_sersic_index"])))
    return rows, len(obj)

def select(rows, grades, te_key="tE"):
    base = [r for r in rows if r["grade"] in grades and r["success"] and r["final"] and not r["large"]]
    good = [r for r in base if r[te_key] > 0 and r["te"] > 0 and 0.6 <= r["n"] <= 10.0 and r["z"] > 0 and r["lm"] > 0]
    return good, len(base)

def arr(sample, k): return np.array([r[k] for r in sample], float)

def build(sample, cosmo=EUCLID, te_key="tE", re_scale=1.0, n_fix=None, rmax=1.0e6 * KPC, z=None, lm=None, tE=None, te=None):
    z = arr(sample, "z") if z is None else z
    lm = arr(sample, "lm") if lm is None else lm
    tE = arr(sample, te_key) if tE is None else tE
    te = arr(sample, "te") if te is None else te
    n = arr(sample, "n") if n_fix is None else np.full(len(sample), float(n_fix))
    DA = cosmo.DA(z)
    RE = tE * ARCSEC * DA; Re = te * ARCSEC * DA * re_scale
    eng = Engine(RE, Re, n, 10.0 ** lm * MSUN, rmax)
    return eng, z, RE, Re, n, lm

def run_b(eng, z, RE, zs, a0, law, cosmo=EUCLID):
    return eng.solve_b(math.pi * RE ** 2 * cosmo.sigcr(z, zs), a0, law)

# ================================================================== main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", required=True)
    args = ap.parse_args()
    t0 = time.time()
    tag = "euc1" + ("_MUTATE_" + MUT if MUT else "")
    RES = dict(lane="EUC1", criteria_commit="898cefb457", mutate=MUT, footings=FOOT, b_star=B_STAR)
    P("EUC1 (ECLIPSE SATURATION CEILING)%s" % ("   *** MUTATE = %s ***" % MUT if MUT else ""))
    P("footings (m/s^2): canonical %.4e, alt %.4e;  margin b* = %.2f dex" % (FOOT["canonical"], FOOT["alt"], B_STAR))
    P("\n[data]")
    rows, nobj = load(args.data_dir)
    P("  key catalogue rows joined to the object catalogue: %d (object rows %d)" % (len(rows), nobj))
    Pm, nbaseP = select(rows, ("A",))
    Sm, nbaseS = select(rows, ("A", "B"))
    P("  P: grade A + model success + final sample + no large-system warning = %d; valid inputs = %d (removed %d)"
      % (nbaseP, len(Pm), nbaseP - len(Pm)))
    P("  S: grades A+B, same cuts = %d; valid inputs = %d (removed %d)" % (nbaseS, len(Sm), nbaseS - len(Sm)))
    RES["samples"] = dict(P_base=nbaseP, P=len(Pm), S_base=nbaseS, S=len(Sm))

    # ---------------------------------------------------------------- instrument checks
    P("\n[instrument checks]")
    CK = {}
    def ck(k, what, val, ok):
        CK[k] = dict(what=what, value=val, ok=bool(ok))
        P("  %s %-4s %s : %s" % ("PASS" if ok else "FAIL", k, what, val))
    # K1 point mass and SIS
    Mp = 1.0e11 * MSUN
    e1 = abs(M2D_from_gfun(5 * KPC, lambda r: G * Mp / r ** 2) / Mp - 1.0)
    sig = 250.0e3
    e2 = max(abs(M2D_from_gfun(R * KPC, lambda r: 2 * sig * sig / r) / (math.pi * sig * sig * R * KPC / G) - 1.0) for R in (3.0, 12.0))
    ck("K1", "point mass returned to 1e-6; SIS deflection constant to 1e-4", "%.1e ; %.1e" % (e1, e2), e1 < 1e-6 and e2 < 1e-4)

    # SLACS (A55's file and normalisation)
    def load_slacs():
        path = os.path.join(REPO, "real_research", "data", "slacs_auger2009_lenses.tsv")
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
    SL = load_slacs()
    a0_k = 1.132e-10
    def slacs_ratio(boost):
        out = []
        for d in SL:
            sc = float(AUGER.sigcr(d["zl"], d["zs"])); REo = d["RE"] * KPC
            Re = d["ReV"] * ARCSEC * float(AUGER.DA(d["zl"]))
            A = boost * d["Fs"] * 10.0 ** d["lME"] / float(M2D_frac(REo, Re, 4.0)) * MSUN
            gf = lambda r: g_law(G * A * M3D_frac(r, Re, 4.0) / r ** 2, a0_k, "S")
            fun = lambda R: M2D_from_gfun(R, gf) - math.pi * R * R * sc
            Rs = np.logspace(math.log10(0.15 * REo), math.log10(10.0 * REo), 60)
            v = np.array([fun(x) for x in Rs]); idx = np.where(np.diff(np.sign(v)) != 0)[0]
            if len(idx): out.append(brentq(fun, Rs[idx[0]], Rs[idx[0] + 1], xtol=1e-5 * KPC) / REo)
        return np.array(out)
    r1 = slacs_ratio(1.0); med = float(np.median(r1))
    ck("K2", "A55 on SLACS: median R_E,pred/R_E,obs = 0.885 +- 0.005 (N = %d)" % len(r1), "%.4f" % med, abs(med - 0.885) <= 0.005)
    Breq = brentq(lambda B: float(np.median(slacs_ratio(B))) - 1.0, 1.02, 3.0, xtol=1e-4)
    ck("K3", "A70 on SLACS: boost that takes the median to 1 = 1.174 +- 0.02", "%.4f" % Breq, abs(Breq - 1.174) <= 0.02)

    # K5 SLACS with and without the source redshift (reference only)
    zl = np.array([d["zl"] for d in SL]); zs = np.array([d["zs"] for d in SL])
    REs = np.array([d["RE"] for d in SL]) * KPC
    Res = np.array([d["ReV"] for d in SL]) * ARCSEC * AUGER.DA(zl)
    Ms = np.array([d["Fs"] * 10.0 ** d["lME"] for d in SL]) / M2D_frac(REs, Res, 4.0) * MSUN
    engS = Engine(REs, Res, np.full(len(SL), 4.0), Ms)
    K5 = {}
    for nm, a0 in (("canonical", 9.3603e-11), ("alt", 1.132e-10)):
        bt = engS.solve_b(math.pi * REs ** 2 * AUGER.sigcr(zl, zs), a0, "S")
        bi = engS.solve_b(math.pi * REs ** 2 * AUGER.sigcr(zl, ZS_INF), a0, "S")
        K5[nm] = dict(true=stats(bt), inf=stats(bi), cost_med=float(np.median(bt - bi)))
        P("       K5 SLACS law S %-9s true z_s: %s" % (nm, fmt(K5[nm]["true"])))
        P("       K5 SLACS law S %-9s z_s=inf : %s   (median cost of dropping z_s: %.3f dex)" % (nm, fmt(K5[nm]["inf"]), K5[nm]["cost_med"]))
    CK["K5"] = dict(what="SLACS reference, no threshold", value=K5, ok=True)

    # ---------------------------------------------------------------- primary
    eng, z, RE, Re, n, lm = build(Pm)
    P("\n[sample P, descriptive]")
    scinf = EUCLID.sigcr(z, ZS_INF); u = MSUN / PC ** 2
    conv = [float(np.max(np.abs(EUCLID.sigcr(z, ZS_INF) / EUCLID.sigcr(z, zz) - 1.0))) for zz in (1.0e4, 9.9e4)]
    P("  medians: z_l = %.3f, theta_E = %.3f\", theta_e = %.3f\", n = %.2f, log M* = %.3f, R_E = %.2f kpc, R_e = %.2f kpc"
      % (np.median(z), np.median(arr(Pm, "tE")), np.median(arr(Pm, "te")), np.median(n), np.median(lm),
         np.median(RE) / KPC, np.median(Re) / KPC))
    sig_star = 10.0 ** lm * MSUN * M2D_frac(RE, Re, n) / (math.pi * RE ** 2)
    P("  medians: Sigma_cr,inf = %.0f Msun/pc^2, mean stellar Sigma(<R_E) = %.0f Msun/pc^2" % (np.median(scinf) / u, np.median(sig_star) / u))
    P("  Sigma_cr at z_s = 1100 vs 1e4 / 1e5 (max over P): %.2e / %.2e" % (conv[0], conv[1]))
    RES["convergence_zs"] = conv

    P("\n[primary: sample P, source at infinity]")
    rng = np.random.default_rng(SEED)
    PRI, bstore = {}, {}
    Mmin = math.pi * RE ** 2 * scinf
    for law in ("S", "B"):
        for nm, a0 in FOOT.items():
            b = eng.solve_b(Mmin, a0, law); bstore[(law, nm)] = b
            st = stats(b, rng); st["word"] = word(st); PRI[law + "_" + nm] = st
            P("  law %s %-9s %s   -> %s" % (law, nm, fmt(st), st["word"]))
    RES["primary"] = PRI
    verdict = "%s / %s" % (PRI["S_canonical"]["word"], PRI["S_alt"]["word"])
    P("  LANE VERDICT (law S, canonical / alt): %s" % verdict)
    RES["verdict"] = verdict

    if MUT:
        ref = json.load(open(os.path.join(HERE, "euc1_results.json")))
        up = all(PRI["S_" + k]["f25"] > ref["primary"]["S_" + k]["f25"] for k in FOOT)
        P("\n[MUTATE %s] f25 law S: canonical %.3f (ref %.3f), alt %.3f (ref %.3f) -> %s"
          % (MUT, PRI["S_canonical"]["f25"], ref["primary"]["S_canonical"]["f25"], PRI["S_alt"]["f25"],
             ref["primary"]["S_alt"]["f25"], "rose on both footings, as required; exit 1" if up else "DID NOT RISE"))
        RES["mutate_rose"] = bool(up)
        json.dump(RES, open(os.path.join(HERE, tag + "_results.json"), "w"), indent=1)
        open(os.path.join(HERE, tag + ".out"), "w").write("\n".join(OUT) + "\n")
        sys.exit(1 if up else 2)

    # K4 twin projection on 20 lenses
    step = max(len(Pm) // 20, 1); errs = []
    for i in list(range(0, len(Pm), step))[:20]:
        a0 = FOOT["alt"]; Mi = 10.0 ** lm[i] * MSUN
        Mr = lambda r: r * r * float(g_law(G * Mi * M3D_frac(r, Re[i], n[i]) / r ** 2, a0, "S")) / G
        h = 1e-4
        def integ(x, R=RE[i]):
            r = math.exp(x)
            return (Mr(r * math.exp(h)) - Mr(r * math.exp(-h))) / (2 * h) * (1.0 - math.sqrt(max(1.0 - (R / r) ** 2, 0.0)))
        xs = np.linspace(math.log(RE[i]), math.log(1.0e6 * KPC), 40)
        tw = Mr(RE[i]) + sum(quad(integ, xs[j], xs[j + 1], epsrel=1e-8, limit=200)[0] for j in range(len(xs) - 1))
        errs.append(abs(tw / float(eng.M2D(np.ones(eng.N), a0, "S")[i]) - 1.0))
    ck("K4", "twin projection (density route) on 20 lenses agrees to 1e-3", "max %.1e" % max(errs), max(errs) < 1e-3)

    # K6 cosmology scaling
    c70 = Cosmo(70.0, 0.3089)
    lm70 = lm + 2.0 * math.log10(67.74 / 70.0)
    eng70, z70, RE70, _, _, _ = build(Pm, cosmo=c70, lm=lm70)
    b70 = run_b(eng70, z70, RE70, ZS_INF, FOOT["alt"], "S", c70)
    resp = np.log10(eng.M2D(np.full(eng.N, 10 ** 0.01), FOOT["alt"], "S") / eng.M2D(np.ones(eng.N), FOOT["alt"], "S")) / 0.01
    pred = math.log10(70.0 / 67.74) / float(np.median(resp))
    got = float(np.median(b70) - np.median(bstore[("S", "alt")]))
    ck("K6", "H0 -> 70 moves b_med by log(70/67.74)/response (response %.3f) to 0.01 dex" % np.median(resp),
       "got %+.4f, predicted %+.4f" % (got, pred), abs(got - pred) < 0.01)
    RES["response_dlnM_dlnB_med"] = float(np.median(resp))

    # ---------------------------------------------------------------- conditional readings
    P("\n[conditional readings, sample P: CONDITIONAL on the source distribution, never the verdict]")
    COND = {}
    for rd, zsf in (("R3", lambda zz: np.full(len(zz), 3.0)), ("R2", lambda zz: np.maximum(2.0, zz + 0.5))):
        zs_ = zsf(z); keep = z < zs_ - 0.2
        for law in ("S", "B"):
            for nm, a0 in FOOT.items():
                b = eng.solve_b(math.pi * RE ** 2 * EUCLID.sigcr(z, np.where(keep, zs_, z + 5.0)), a0, law)
                st = stats(b[keep], rng); st["would_be"] = word(st); st["dropped"] = int(np.sum(~keep))
                COND["%s_%s_%s" % (rd, law, nm)] = st; bstore[(rd, law, nm)] = np.where(keep, b, np.nan)
                P("  %s law %s %-9s %s   (dropped %d)  would-be: %s" % (rd, law, nm, fmt(st), st["dropped"], st["would_be"]))
    RES["conditional"] = COND

    # ---------------------------------------------------------------- robustness (law S, source at infinity)
    P("\n[robustness, law S, source at infinity; cannot change the verdict word]")
    ROB = {}
    def rob(name, sample, **kw):
        e, zz, RR, _, _, _ = build(sample, **kw)
        for nm, a0 in FOOT.items():
            st = stats(run_b(e, zz, RR, ZS_INF, a0, "S"), rng); st["would_be"] = word(st)
            ROB[name + "_" + nm] = st
            P("  %-34s %-9s %s  %s" % (name, nm, fmt(st), st["would_be"]))
    rob("1 R_e x 0.80", Pm, re_scale=0.80)
    rob("2 n = 4", Pm, n_fix=4.0)
    PmSIE, _ = select(rows, ("A",), "tSIE"); rob("3 SIE Einstein radius", PmSIE, te_key="tSIE")
    rob("4a z_l < 1.0", [r for r in Pm if r["z"] < 1.0])
    Psp = [r for r in Pm if np.isfinite(r["zspec"]) and r["zspec"] > 0]
    if len(Psp) >= 5:
        zsp = arr(Psp, "zspec")
        lmsp = arr(Psp, "lm") + 2.0 * np.log10(EUCLID.DL(zsp) / EUCLID.DL(arr(Psp, "z")))
        rob("4b DESI deflector spec-z (N=%d)" % len(Psp), Psp, z=zsp, lm=lmsp)
        rob("4b same lenses at photo-z", Psp)
    rob("5 theta_E <= 2.5 arcsec", [r for r in Pm if r["tE"] <= 2.5])
    rob("7 sample S (grades A+B)", Sm)
    rob("8 r_max = 300 kpc", Pm, rmax=300.0 * KPC)
    # 6 Monte Carlo of catalogued errors
    mc = {k: [] for k in FOOT}
    rmc = np.random.default_rng(SEED + 1)
    def pm(v, lo, up, w):
        return v + w * np.where(w > 0, np.where(up > 0, up, 0.0), np.where(lo > 0, lo, 0.0))
    z0 = arr(Pm, "z"); szu = np.clip(arr(Pm, "zhi") - z0, 0, None) / 1.04; szl = np.clip(z0 - arr(Pm, "zlo"), 0, None) / 1.04
    tE0, te0 = arr(Pm, "tE"), arr(Pm, "te")
    def half(lo, up, v):
        s = 0.5 * (up - lo); return np.where((lo > 0) & (up > 0) & (s > 0), s, 0.0)
    sE = half(arr(Pm, "tE_lo"), arr(Pm, "tE_up"), tE0); se = half(arr(Pm, "te_lo"), arr(Pm, "te_up"), te0)
    for _ in range(200):
        w = rmc.standard_normal(len(Pm)); zz = np.clip(z0 + w * np.where(w > 0, szu, szl), 0.02, 3.0)
        lmm = pm(lm, arr(Pm, "lm_lo"), arr(Pm, "lm_up"), rmc.standard_normal(len(Pm))) + 2.0 * np.log10(EUCLID.DL(zz) / EUCLID.DL(z0))
        tEm = np.clip(tE0 + sE * rmc.standard_normal(len(Pm)), 0.05 * tE0, None)
        tem = np.clip(te0 + se * rmc.standard_normal(len(Pm)), 0.05 * te0, None)
        e, zz, RR, _, _, _ = build(Pm, z=zz, lm=lmm, tE=tEm, te=tem)
        Mm = math.pi * RR ** 2 * EUCLID.sigcr(zz, ZS_INF)
        for nm, a0 in FOOT.items():
            mc[nm].append(float(np.mean(e.M2D(np.full(e.N, 10.0 ** B_STAR), a0, "S") < Mm)))
    for nm in FOOT:
        v = np.array(mc[nm]); ROB["6_MC_" + nm] = dict(mean=float(v.mean()), sd=float(v.std()), lo=float(v.min()), hi=float(v.max()))
        P("  6 Monte Carlo of catalogued errors   %-9s f25 over 200 draws: mean %.3f, sd %.3f, range [%.3f, %.3f]"
          % (nm, v.mean(), v.std(), v.min(), v.max()))
    RES["robustness"] = ROB
    crossed = [k for k, st in ROB.items() if not k.startswith("6_") and not k.startswith("4b") and not k.startswith("8")
               and st.get("would_be") != PRI["S_" + k.rsplit("_", 1)[1]]["word"]]
    P("  robustness runs 1-5, 7 whose word differs from the primary: %s" % (crossed if crossed else "none"))
    RES["robustness_crossed"] = crossed

    # ---------------------------------------------------------------- map (exploratory)
    P("\n[map, EXPLORATORY, no verdict: law S, source at infinity]")
    MAP = {}
    dS = {nm: (scinf - eng.M2D(np.ones(eng.N), a0, "S") / (math.pi * RE ** 2)) / u for nm, a0 in FOOT.items()}
    ph = {nm: (eng.M2D(np.ones(eng.N), a0, "S") / (math.pi * RE ** 2) - sig_star) / u for nm, a0 in FOOT.items()}
    P("  median cold (phantom) mean surface density inside R_E: canonical %.0f, alt %.0f Msun/pc^2"
      % (np.median(ph["canonical"]), np.median(ph["alt"])))
    def binmap(name, x, edges):
        P("  by %s:   bin, N, median b (canonical / alt), median R3 b (alt), median dSigma_min alt [Msun/pc^2], f25 alt" % name)
        rowsm = []
        for lo, hi in zip(edges[:-1], edges[1:]):
            m = (x >= lo) & (x < hi)
            if m.sum() < 10: continue
            r3 = bstore[("R3", "S", "alt")][m]
            row = dict(lo=float(lo), hi=float(hi), N=int(m.sum()), b_canon=float(np.median(bstore[("S", "canonical")][m])),
                       b_alt=float(np.median(bstore[("S", "alt")][m])), b_alt_R3=float(np.nanmedian(r3)),
                       dSigma_alt=float(np.median(dS["alt"][m])), f25_alt=float(np.mean(bstore[("S", "alt")][m] > B_STAR)))
            rowsm.append(row)
            P("    [%6.2f, %6.2f)  %5d   %+.3f / %+.3f   %+.3f   %+7.0f   %.3f"
              % (lo, hi, row["N"], row["b_canon"], row["b_alt"], row["b_alt_R3"], row["dSigma_alt"], row["f25_alt"]))
        MAP[name] = rowsm
    binmap("log M*", lm, np.arange(10.0, 12.41, 0.2))
    binmap("z_l", z, np.array([0.1, 0.3, 0.45, 0.6, 0.75, 0.9, 1.2, 2.01]))
    binmap("theta_E/theta_e", arr(Pm, "tE") / arr(Pm, "te"), np.array([0.0, 0.5, 0.75, 1.0, 1.5, 2.5, 5.0, 1e3]))
    binmap("Sersic n", n, np.array([0.6, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 10.01]))
    binmap("theta_E [arcsec]", arr(Pm, "tE"), np.array([0.0, 0.6, 0.8, 1.0, 1.3, 1.7, 2.5, 10.0]))
    sw = 11.210249557380582
    for nm in FOOT:
        bb = bstore[("S", nm)]
        hi_ = bb[(lm >= sw) & (lm < sw + 0.2)]; lo_ = bb[(lm >= sw - 0.2) & (lm < sw)]
        MAP["sp1_step_" + nm] = dict(above=float(np.median(hi_)), below=float(np.median(lo_)), N_above=int(len(hi_)), N_below=int(len(lo_)))
        P("  SP1 switch (log M* = 11.21) %-9s median b above %+.3f (N=%d), below %+.3f (N=%d), difference %+.3f  [not a grade of SP1]"
          % (nm, np.median(hi_), len(hi_), np.median(lo_), len(lo_), np.median(hi_) - np.median(lo_)))
    disc = np.array([r["disc"] for r in Pm])
    if disc.sum() >= 10:
        MAP["disc"] = dict(N=int(disc.sum()), b_alt=float(np.median(bstore[("S", "alt")][disc])), b_alt_rest=float(np.median(bstore[("S", "alt")][~disc])))
        P("  disc deflectors: N = %d, median b alt %+.3f (others %+.3f)" % (disc.sum(), MAP["disc"]["b_alt"], MAP["disc"]["b_alt_rest"]))
    RES["map"] = MAP

    # ---------------------------------------------------------------- outputs
    with open(os.path.join(HERE, "euc1_per_lens.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["unique_identifier", "z_l", "theta_E_arcsec", "theta_e_arcsec", "sersic_n", "log_Mstar_salpeter",
                    "Sigma_cr_inf_Msun_pc2", "Sigma_star_mean_Msun_pc2", "b_S_canonical", "b_S_alt", "b_B_canonical", "b_B_alt",
                    "b_S_alt_R3", "b_S_alt_R2", "dSigma_min_S_alt_Msun_pc2"])
        for i, r in enumerate(Pm):
            w.writerow([r["id"], "%.3f" % z[i], "%.4f" % r["tE"], "%.4f" % r["te"], "%.3f" % n[i], "%.3f" % lm[i],
                        "%.1f" % (scinf[i] / u), "%.1f" % (sig_star[i] / u)] +
                       ["%.4f" % bstore[k][i] for k in (("S", "canonical"), ("S", "alt"), ("B", "canonical"), ("B", "alt"),
                                                         ("R3", "S", "alt"), ("R2", "S", "alt"))] + ["%.1f" % dS["alt"][i]])
    allok = all(v["ok"] for v in CK.values())
    RES["checks"] = CK; RES["checks_all_pass"] = allok
    P("\n[summary]")
    P("  instrument checks: %s" % ("all pass" if allok else "FAILED -> NOT EVALUABLE"))
    P("  LANE VERDICT (law S, canonical / alt): %s" % (verdict if allok else "NOT EVALUABLE"))
    P("  kappa = 1/2 FITTED. One-sided test: no outcome favours the framework.  (%.0f s)" % (time.time() - t0))
    json.dump(RES, open(os.path.join(HERE, tag + "_results.json"), "w"), indent=1)
    open(os.path.join(HERE, tag + ".out"), "w").write("\n".join(OUT) + "\n")
    sys.exit(0 if allok else 3)

if __name__ == "__main__":
    main()
