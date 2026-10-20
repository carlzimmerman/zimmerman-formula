"""CFG890 -- which few-parameter GLOBAL description of the dwarf excess works best, on the same 83 dwarfs, the same likelihood
and the same parameter penalty?
Criteria: FROZEN_CRITERIA.md (2ebf38985, committed alone before this script).
Run (light, one core):  OMP_NUM_THREADS=1 nice -n 10 python3 cfg890.py
  CFG890_PART=variants   -> V1/V2/V3 only (cfg890_variants.out / cfg890_results_variants.json); run BEFORE the primary so that
                            the primary run can apply the pre-registered qualifiers.
  CFG890_MUTATE=shape|clump -> synthetic controls (cfg890_MUTATE_<mode>.out / cfg890_results_MUTATE_<mode>.json).
  CFG890_POSTHOC=binary  -> POST-HOC diagnostic, added after the pre-registered runs and not graded: binary-corrected sigma
                            (Arroyo-Polonio+2026 flat-f column, as CFG880's V4) for 8 UFDs + Crater II, all models, both footings.
  CFG890_POSTHOC=decomp  -> POST-HOC diagnostic (not graded): per-dwarf ln L_i at the primary MLEs (read from cfg890_results.json),
                            Delta_i = ln L_i(best mass-like) - ln L_i(best acceleration-like): which dwarfs carry the type verdict.
kappa = 1/2 FITTED; nu_e; the two a0 footings are never pooled; no dark-matter particle; not theory closed.

Implementation notes (decided while writing, before any run; disclosed in the README):
- The marginal over eta uses the frozen per-dwarf grid (1001 nodes over sigma_obs -15 e_m .. +15 e_p) PLUS two 301-node pieces that
  extend the integration range to mu_i +- 14 s_int when the model sits outside that window (the frozen grid alone would miss the
  integrand's peak for models many sigma away from the data); Gauss-Hermite (80 nodes) for s_int < 4 du_i and the exact
  likelihood at s_int = 0, as frozen.
- K2 is run as frozen (+-12 in t, 240001 nodes) and, because a +-12 reference can itself truncate for models ~20 error bars away,
  also with a wider reference (+-40, 400001 nodes), labelled as added after freezing.
"""
import os, csv, json, math, time, numpy as np
from scipy.special import logsumexp, log_ndtr, roots_hermite
from scipy.optimize import minimize, minimize_scalar, brentq

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
MUT = os.environ.get("CFG890_MUTATE", ""); assert MUT in ("", "shape", "clump")
PART = os.environ.get("CFG890_PART", "primary"); assert PART in ("primary", "variants") and not (MUT and PART == "variants")
POST = os.environ.get("CFG890_POSTHOC", ""); assert POST in ("", "binary", "decomp") and not (POST and (MUT or PART == "variants"))
SUF = f"_MUTATE_{MUT}" if MUT else ("_variants" if PART == "variants" else (f"_POSTHOC_{POST}" if POST else ""))
OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
G, Msun, PC = 6.674e-11, 1.989e30, 3.0857e16; A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; RC = 104.0
nu = lambda y: 1.0 / (-np.expm1(-np.sqrt(np.maximum(y, 1e-15))))
def fnum(x):
    try:
        v = float(x); return None if math.isnan(v) else v
    except (TypeError, ValueError): return None
J = lambda *p: json.load(open(os.path.join(LANES, *p)))
R880 = J("CFG880_clump_sigma_universality", "cfg880_results.json"); R851 = J("CFG851_spheroidal_excess_law", "cfg851_results.json")
R870 = J("CFG870_cored_component_joint", "cfg870_results.json")
C851 = {f: (R851[f"{f}|shift0.123"]["cal"]["b"], R851[f"{f}|shift0.123"]["cal"]["lgd"]) for f in A0}
SREF = {f: R870[f]["Vx"] / math.sqrt(2) for f in A0}
OUTLIERS = ["Crater II", "Antlia II", "Sextans", "Draco", "Bootes I"]

# ---------------- sample (copied from CFG880) ----------------
LVD = {}
for f in ("lvd_dwarf_mw.csv", "lvd_dwarf_m31.csv", "lvd_dwarf_local_field.csv"):
    for r in csv.DictReader(open(os.path.join(REPO, "real_research", "data", "dsph", f))): LVD[r["name"]] = r
EXCL = {"LMC", "SMC", "WLM", "NGC 6822", "IC 1613", "Leo A", "Sagittarius dIrr", "Pegasus dIrr", "M 32"}
def gas_in(lHI, r12_pc):                                   # CFG874 primary (extended root), copied unchanged (via CFG880)
    if lHI is None: return 0.0
    Mg = 1.33 * 10 ** lHI; MHI = 10 ** lHI; RHI = 0.5 * 10 ** (0.506 * lHI - 3.293) * 1e3
    f = lambda Rs: MHI / (2 * math.pi * Rs * Rs) * math.exp(-RHI / Rs) - 1.0
    grid = np.geomspace(1e-3 * RHI, 10 * RHI, 4000); v = [f(x) for x in grid]
    roots = [grid[i] for i in range(len(grid) - 1) if v[i] * v[i + 1] < 0]
    Rs = max(roots) if roots else RHI / 2; x = r12_pc / Rs
    return Mg * (1 - (1 + x) * math.exp(-x))
def clump2(r12_pc, sx, a0, rc=RC):                         # CFG877/880 finite clump, G M_x(<r12)/(3 r12) in (km/s)^2 (copied)
    r = r12_pc * PC; s = sx * 1e3
    Mx = np.minimum(2 * s ** 2 * r ** 3 / (G * (r ** 2 + (rc * PC) ** 2)), 81 * s ** 4 / (4 * G * a0))
    return G * Mx / (3 * r) / 1e6
SAMP = []
for nm, r in LVD.items():
    if nm in EXCL: continue
    s = fnum(r.get("vlos_sigma"))
    if s is None or fnum(r.get("vlos_sigma_ul")) is not None: continue
    rh = fnum(r.get("rhalf_sph_physical")) or fnum(r.get("rhalf_physical"))
    if rh is None or fnum(r.get("M_V")) is None: continue
    em, ep = fnum(r.get("vlos_sigma_em")), fnum(r.get("vlos_sigma_ep")); assert em and ep, nm
    r12_pc = (4 / 3) * rh
    SAMP.append(dict(name=nm, host=r.get("host") or "field", MV=fnum(r["M_V"]), s=s, em=em, ep=ep, r12pc=r12_pc,
                     Lv=10 ** (0.4 * (4.83 - fnum(r["M_V"]))), Mg=gas_in(fnum(r.get("mass_HI")), r12_pc)))
def sl2_law(D, a0, ups=2.0):                               # sigma_law^2 in (km/s)^2, same arithmetic as CFG880's law2
    gN = G * (ups * D["Lv"] / 2 + D["Mg"]) * Msun / D["r12m"] ** 2
    return gN * nu(gN / a0) * D["r12m"] / 3 / 1e6
def make_D(S):
    D = {k: np.array([d[k] for d in S]) for k in ("MV", "s", "em", "ep", "r12pc", "Lv", "Mg")}
    D["names"] = [d["name"] for d in S]; D["host"] = [d["host"] for d in S]; D["r12m"] = D["r12pc"] * PC
    D["gN"] = G * (2.0 * D["Lv"] / 2 + D["Mg"]) * Msun / D["r12m"] ** 2; D["lgN"] = np.log10(D["gN"])
    D["sl2"] = {f: sl2_law(D, A0[f]) for f in A0}; D["N"] = len(S); return D
def sub(D, keep):
    keep = np.asarray(keep, bool); E = {}
    for k, v in D.items():
        if k == "sl2": E[k] = {f: v[f][keep] for f in v}
        elif k == "N": continue
        elif isinstance(v, list): E[k] = [x for x, kk in zip(v, keep) if kk]
        else: E[k] = v[keep]
    E["N"] = int(keep.sum()); return E

# ---------------- hierarchical likelihood: sigma_true = sigma_model e^eta, eta ~ N(0, s^2); split-normal errors ----------------
NGA, NPC, NGH, LNF = 1001, 301, 80, math.log(0.02)
GHX, GHW = roots_hermite(NGH); LNGHW = np.log(GHW / math.sqrt(math.pi)); SQ2 = math.sqrt(2.0)
def lnell(st, so, em, ep, lnc):
    e = np.where(so < st, ep, em); return -0.5 * ((so - st) / e) ** 2 + lnc
class Like:
    def __init__(self, D):
        self.so, self.em, self.ep = D["s"], D["em"], D["ep"]; self.lnc = np.log(math.sqrt(2 / math.pi) / (self.em + self.ep)); n = len(self.so)
        self.ulo = np.log(np.maximum(self.so - 15 * self.em, 0.02)); self.uhi = np.log(self.so + 15 * self.ep)
        self.du = (self.uhi - self.ulo) / (NGA - 1); t = np.linspace(0, 1, NGA)
        self.U = self.ulo[:, None] + (self.uhi - self.ulo)[:, None] * t[None, :]
        self.lnl = lnell(np.exp(self.U), self.so[:, None], self.em[:, None], self.ep[:, None], self.lnc[:, None])
        w = np.ones(NGA); w[[0, -1]] = 0.5; self.lnwA = np.log(w)[None, :] + np.log(self.du)[:, None]
        wp = np.ones(NPC); wp[[0, -1]] = 0.5; self.lnwp = np.log(wp); self.tp = np.linspace(0, 1, NPC)
    def piece(self, idx, a, b, m, s):                      # trapezoid of N(u; m, s) l(u) on [a, b] (a <= b), log space
        h = (b - a) / (NPC - 1); UB = a[:, None] + (b - a)[:, None] * self.tp[None, :]
        f = (-0.5 * ((UB - m[:, None]) / s) ** 2 - math.log(s * math.sqrt(2 * math.pi))
             + lnell(np.exp(UB), self.so[idx, None], self.em[idx, None], self.ep[idx, None], self.lnc[idx, None]))
        return logsumexp(f + self.lnwp[None, :], axis=1) + np.log(np.maximum(h, 1e-300))
    def lnLi(self, sig, s):
        if s == 0: return lnell(sig, self.so, self.em, self.ep, self.lnc)
        n = len(self.so); out = np.empty(n); mu = np.log(sig); gh = s < 4 * self.du
        if gh.any():
            i = np.where(gh)[0]; st = sig[i, None] * np.exp(s * SQ2 * GHX[None, :])
            out[i] = logsumexp(lnell(st, self.so[i, None], self.em[i, None], self.ep[i, None], self.lnc[i, None]) + LNGHW[None, :], axis=1)
        if (~gh).any():
            i = np.where(~gh)[0]; m = mu[i]
            A = logsumexp(-0.5 * ((self.U[i] - m[:, None]) / s) ** 2 - math.log(s * math.sqrt(2 * math.pi)) + self.lnl[i] + self.lnwA[i], axis=1)
            ulo, uhi = self.ulo[i], self.uhi[i]
            bL = np.maximum(np.minimum(m - 14 * s, ulo), LNF); B = self.piece(i, bL, ulo, m, s)
            bH = np.maximum(m + 14 * s, uhi); C = self.piece(i, uhi, bH, m, s)
            T = log_ndtr((bL - m) / s) + lnell(np.exp(bL), self.so[i], self.em[i], self.ep[i], self.lnc[i])
            out[i] = logsumexp(np.vstack([A, B, C, T]), axis=0)
        return out

# ---------------- pre-registered models ----------------
LN = math.log
def models(foot):
    a0 = A0[foot]; b851, g851 = C851[foot]
    fc = lambda D, rc: D["r12pc"] ** 2 / (D["r12pc"] ** 2 + rc ** 2)
    M = {
     "M0": dict(name="law alone", k=0, typ="baseline", f=lambda t, D: D["sl2"][foot]),
     "M1": dict(name="free a0", k=1, typ="acc", par=["log10 a_d"], lo=[-13.0], hi=[-7.0], f=lambda t, D: sl2_law(D, 10 ** t[0])),
     "M2": dict(name="finite clump (CFG877)", k=1, typ="mass", par=["ln sigma_x"], lo=[LN(0.01)], hi=[LN(60.0)],
                f=lambda t, D: D["sl2"][foot] + clump2(D["r12pc"], math.exp(t[0]), a0)),
     "M3": dict(name="extended cored (CFG870)", k=1, typ="mass", par=["ln V_x"], lo=[LN(0.01)], hi=[LN(80.0)],
                f=lambda t, D: D["sl2"][foot] + fc(D, RC) * math.exp(t[0]) ** 2 / 3),
     "M4": dict(name="low-g power shape", k=2, typ="acc", par=["b", "log10 g*"], lo=[-0.5, -15.0], hi=[1.5, -8.5],
                f=lambda t, D: D["sl2"][foot] * 10 ** (t[0] * np.maximum(0.0, t[1] - D["lgN"]))),
     "M5": dict(name="extra mass ~ r", k=1, typ="mass", par=["ln V_x"], lo=[LN(0.01)], hi=[LN(80.0)],
                f=lambda t, D: D["sl2"][foot] + math.exp(t[0]) ** 2 / 3),
     "M6": dict(name="free Upsilon_V", k=1, typ="baryon", par=["ln Ups_V"], lo=[LN(0.05)], hi=[LN(100.0)],
                f=lambda t, D: sl2_law(D, a0, math.exp(t[0]))),
     "M7": dict(name="CFG851 law fixed", k=0, typ="acc", f=lambda t, D: D["sl2"][foot] * 10 ** (b851 * np.maximum(0.0, g851 - D["lgN"]))),
     "M8": dict(name="low-g step (CFG828)", k=2, typ="acc", par=["ln A", "g_c"], lo=[LN(0.2)], hi=[LN(50.0)], step=True),
     "M9": dict(name="finite clump, free core", k=2, typ="mass", par=["ln sigma_x", "ln r_c"], lo=[LN(0.01), LN(1.0)], hi=[LN(60.0), LN(5000.0)],
                f=lambda t, D: D["sl2"][foot] + clump2(D["r12pc"], math.exp(t[0]), a0, math.exp(t[1]))),
     "M10": dict(name="extended, free core", k=2, typ="mass", par=["ln V_x", "ln r_c"], lo=[LN(0.01), LN(1.0)], hi=[LN(80.0), LN(5000.0)],
                 f=lambda t, D: D["sl2"][foot] + fc(D, math.exp(t[1])) * math.exp(t[0]) ** 2 / 3),
     "M11": dict(name="acceleration floor", k=1, typ="acc", par=["log10 g_f"], lo=[-15.0], hi=[-9.5],
                 f=lambda t, D: D["sl2"][foot] + 10 ** t[0] * D["r12m"] / 3 / 1e6)}
    return M
ORDER = ["M0", "M1", "M2", "M3", "M5", "M6", "M7", "M11", "M4", "M8", "M9", "M10"]
TYPE_LABEL = {"acc": "acceleration-like", "mass": "mass-like", "baryon": "baryonic normalisation", "baseline": "baseline"}
def phys(mid, t, D=None):                                 # human-readable globals
    if mid == "M1": return {"a_d": 10 ** t[0]}
    if mid in ("M2",): return {"sigma_x": math.exp(t[0])}
    if mid in ("M3", "M5"): return {"V_x": math.exp(t[0])}
    if mid == "M4": return {"b": t[0], "log10 g*": t[1]}
    if mid == "M6": return {"Ups_V": math.exp(t[0])}
    if mid == "M8": return {"A": math.exp(t[0]), "log10 g_c": t[1], "n_below": int(t[2])}
    if mid == "M9": return {"sigma_x": math.exp(t[0]), "r_c_pc": math.exp(t[1])}
    if mid == "M10": return {"V_x": math.exp(t[0]), "r_c_pc": math.exp(t[1])}
    if mid == "M11": return {"g_f": 10 ** t[0]}
    return {}

# ---------------- fitting ----------------
class Fitter:
    def __init__(self, mid, m, D, LK, extra_starts=()):
        self.mid, self.m, self.D, self.LK = mid, m, D, LK; self.cache = {}; self.prescan = {}; self.extra = [np.array(x, float) for x in extra_starts]
        if m.get("step"):
            self.o = np.argsort(D["gN"]); g = D["gN"][self.o]
            self.cand = [c for c in range(1, len(g)) if g[c - 1] < g[c]]; self.gsorted = g
            self.lnA_grid = np.linspace(m["lo"][0], m["hi"][0], 81)
    def L(self, t, s):
        return float(self.LK.lnLi(np.sqrt(np.maximum(self.m["f"](t, self.D), 1e-12)), s).sum())
    def inner_step(self, s):                               # M8: exact max over the candidate thresholds, ln A on a grid + refinement
        sl2 = self.D["sl2_foot"]; L1 = self.LK.lnLi(np.sqrt(sl2), s)[self.o]; c1 = np.concatenate([[0.0], np.cumsum(L1)]); tot1 = c1[-1]
        best = (-np.inf, None, None); cands = np.array(self.cand)
        for la in self.lnA_grid:
            LA = self.LK.lnLi(np.sqrt(sl2 * math.exp(la)), s)[self.o]; cA = np.concatenate([[0.0], np.cumsum(LA)])
            tot = cA[cands] + tot1 - c1[cands]; j = int(np.argmax(tot))
            if tot[j] > best[0]: best = (float(tot[j]), la, int(cands[j]))
        _, la0, c = best; below = np.zeros(len(sl2), bool); below[self.o[:c]] = True
        fA = lambda la: -float(self.LK.lnLi(np.sqrt(np.where(below, sl2 * math.exp(la), sl2)), s).sum())
        dl = self.lnA_grid[1] - self.lnA_grid[0]
        r = minimize_scalar(fA, bounds=(max(la0 - dl, self.m["lo"][0]), min(la0 + dl, self.m["hi"][0])), method="bounded", options=dict(xatol=1e-7))
        la = float(r.x) if -r.fun > best[0] else la0; Lb = max(-r.fun, best[0])
        lgc = 0.5 * (math.log10(self.gsorted[c - 1]) + math.log10(self.gsorted[c]))
        return Lb, np.array([la, lgc, c])
    def inner(self, s, start=None, full=True):
        m = self.m; k = m["k"]
        if k == 0: return self.L([], s), np.array([])
        if m.get("step"): return self.inner_step(s)
        lo, hi = np.array(m["lo"]), np.array(m["hi"])
        if k == 1:
            g = np.linspace(lo[0], hi[0], 41); v = np.array([self.L([x], s) for x in g]); j = int(np.argmax(v))
            r = minimize_scalar(lambda x: -self.L([x], s), bounds=(g[max(j - 1, 0)], g[min(j + 1, 40)]), method="bounded", options=dict(xatol=1e-7))
            return (float(-r.fun), np.array([r.x])) if -r.fun >= v[j] else (float(v[j]), np.array([g[j]]))
        starts = []; step = (hi - lo) / 20
        if full or start is None:
            g0, g1 = np.linspace(lo[0], hi[0], 21), np.linspace(lo[1], hi[1], 21); best = (-np.inf, None)
            for x in g0:
                for y in g1:
                    v = self.L([x, y], s)
                    if v > best[0]: best = (v, np.array([x, y]))
            starts.append((best[1], step)); self.prescan[round(float(s), 10)] = best[0]
        if start is not None: starts.append((np.array(start, float), step / 10))
        for e in self.extra: starts.append((np.clip(e, lo, hi), step / 4))
        res = (-np.inf, None)
        for x0, st in starts:
            simplex = np.array([x0, x0 + [st[0], 0], x0 + [0, st[1]]]); simplex = np.clip(simplex, lo, hi)
            if np.linalg.matrix_rank(simplex[1:] - simplex[0]) < 2: simplex = np.array([x0, x0 - [st[0], 0], x0 - [0, st[1]]]).clip(lo, hi)
            r = minimize(lambda x: -self.L(x, s), x0, method="Nelder-Mead", bounds=list(zip(lo, hi)),
                         options=dict(initial_simplex=simplex, xatol=1e-6, fatol=1e-8, maxiter=2000, maxfev=4000))
            if -r.fun > res[0]: res = (float(-r.fun), np.array(r.x))
        return res
    def Lp(self, s, full=None):                            # profile over the globals at fixed s_int (cached)
        key = round(float(s), 10)
        if full is None: full = self.m["k"] != 2
        if key in self.cache and (self.cache[key][2] or not full): return self.cache[key][:2]
        near = None
        if self.cache:
            ks = sorted(self.cache, key=lambda q: abs(q - key)); near = self.cache[ks[0]][1]
        Lv, t = self.inner(s, start=near, full=full or near is None)
        if key in self.cache and self.cache[key][0] > Lv: Lv, t = self.cache[key][:2]
        self.cache[key] = (Lv, t, full or near is None); return Lv, t
    def fit(self):
        m = self.m; coarse = [0.0, 0.1, 0.2, 0.3, 0.45, 0.6, 0.8, 1.1, 1.5, 2.2, 3.0]
        vals = [self.Lp(s, full=True)[0] for s in coarse]; j = int(np.argmax(vals))
        a, b = coarse[max(j - 1, 0)], coarse[min(j + 1, len(coarse) - 1)]
        r = minimize_scalar(lambda s: -self.Lp(s)[0], bounds=(a, b), method="bounded", options=dict(xatol=1e-5))
        sh = float(r.x)
        if self.Lp(0.0)[0] >= self.Lp(sh)[0]: sh = 0.0
        if m["k"] == 2 and not m.get("step"):              # 3-D polish over (globals, s), then a full re-check at s_hat
            t0 = self.Lp(sh)[1]; lo = list(m["lo"]) + [0.0]; hi = list(m["hi"]) + [3.0]
            rr = minimize(lambda x: -self.L(x[:2], x[2]), np.r_[t0, sh], method="Nelder-Mead", bounds=list(zip(lo, hi)),
                          options=dict(xatol=1e-7, fatol=1e-9, maxiter=4000, maxfev=8000))
            if -rr.fun > self.Lp(sh)[0] + 1e-9:
                sh = float(rr.x[2]); self.cache[round(sh, 10)] = (float(-rr.fun), np.array(rr.x[:2]), False)
            Lf = self.Lp(sh, full=True)
        Lmax, th = self.Lp(sh)
        out = dict(s_hat=sh, lnL=Lmax, theta=[float(x) for x in th], lnL_s0=self.Lp(0.0, full=True)[0])
        out["Lambda_s"] = 2 * (Lmax - out["lnL_s0"])
        def cross(thr, side):
            g = lambda s: 2 * (Lmax - self.Lp(s)[0]) - thr
            if side == "lo":
                if g(0.0) <= 0: return 0.0
                return brentq(g, 0.0, sh, xtol=1e-5)
            hi_s = [s for s in coarse if s > sh and g(s) > 0]
            if not hi_s: return math.inf
            return brentq(g, sh, hi_s[0], xtol=1e-5)
        for nm, thr in (("68", 1.0), ("95", 3.84)):
            lo_, hi_ = cross(thr, "lo"), cross(thr, "hi"); out["s" + nm] = [lo_, hi_]
        flags = []                                         # re-check the 95% crossings with the full inner optimiser
        for sc in out["s95"]:
            if 0 < sc < math.inf:
                Lw = self.Lp(sc)[0]; Lf = self.Lp(sc, full=True)[0]
                if Lf > Lw + 1e-3: flags.append(f"full inner improved Lp({sc:.3f}) by {Lf - Lw:.3g}")
        if flags:
            for nm, thr in (("68", 1.0), ("95", 3.84)): out["s" + nm] = [cross(thr, "lo"), cross(thr, "hi")]
        out["flags"] = flags; out["works"] = out["s95"][0] == 0.0
        if m.get("step") is None and m["k"] >= 1:
            out["at_bound"] = [bool(abs(x - l) < 1e-3 or abs(x - h) < 1e-3) for x, l, h in zip(th, m["lo"], m["hi"])]
        if m.get("step"): out["at_bound"] = [bool(abs(th[0] - m["lo"][0]) < 1e-3 or abs(th[0] - m["hi"][0]) < 1e-3)]
        if m["k"] == 2 and not m.get("step"): out["prescan_at_shat"] = float(self.prescan.get(round(float(sh), 10), -np.inf))
        if m["k"] == 1:                                    # 95% profile interval on the single global (s_int re-optimised)
            def pg(x):
                r2 = minimize_scalar(lambda s: -self.L([x], s), bounds=(0.0, 3.0), method="bounded", options=dict(xatol=1e-5))
                return max(float(-r2.fun), self.L([x], 0.0))
            gx = lambda x: 2 * (Lmax - pg(x)) - 3.84; x0 = th[0]; iv = []
            for edge in (m["lo"][0], m["hi"][0]):
                iv.append(brentq(gx, min(edge, x0), max(edge, x0), xtol=1e-6) if gx(edge) > 0 else None)
            out["theta95"] = iv
        return out

# ---------------- comparison of one sample on one footing ----------------
def run_sample(D, foot, label, verbose=True, want_rows=False):
    LK = Like(D); D = dict(D); D["sl2_foot"] = D["sl2"][foot]; M = models(foot); N = D["N"]; R = {}; T = time.time()
    for mid in ORDER:
        m = M[mid]; extra = []
        if mid == "M9": extra = [[R["M2"]["theta"][0], LN(RC)]]
        if mid == "M10": extra = [[R["M3"]["theta"][0], LN(RC)], [R["M5"]["theta"][0], 0.0]]
        if mid == "M4": extra = [[0.0, -12.0]]
        F = Fitter(mid, m, D, LK, extra); r = F.fit(); kk = m["k"] + 1
        r.update(model=mid, name=m["name"], k=m["k"], type=m["typ"], AIC=2 * kk - 2 * r["lnL"], BIC=kk * math.log(N) - 2 * r["lnL"],
                 phys=phys(mid, r["theta"]) if m["k"] else {})
        th = np.array(r["theta"])
        if m.get("step"):
            below = np.zeros(N, bool); below[F.o[:int(th[2])]] = True
            sm2 = np.where(below, D["sl2_foot"] * math.exp(th[0]), D["sl2_foot"])
        else: sm2 = m["f"](th, D)
        sm = np.sqrt(sm2); r["sig_model"] = [float(x) for x in sm]
        rr = np.log(D["s"] / sm); e = np.where(D["s"] < sm, D["ep"], D["em"]); tt = rr / np.sqrt(r["s_hat"] ** 2 + (e / D["s"]) ** 2)
        r["resid"] = {nm: dict(sig_obs=float(D["s"][i]), sig_model=float(sm[i]), r=float(rr[i]), t=float(tt[i]))
                      for i, nm in enumerate(D["names"]) if nm in OUTLIERS}
        r["top5"] = [(D["names"][i], float(tt[i])) for i in np.argsort(-np.abs(tt))[:5]]
        R[mid] = r
    bmin = min(R[x]["BIC"] for x in R); amin = min(R[x]["AIC"] for x in R)
    for x in R: R[x]["dBIC"] = R[x]["BIC"] - bmin; R[x]["dAIC"] = R[x]["AIC"] - amin
    best = min(R, key=lambda x: R[x]["BIC"]); bm = min((x for x in R if R[x]["type"] == "mass"), key=lambda x: R[x]["BIC"])
    ba = min((x for x in R if R[x]["type"] == "acc"), key=lambda x: R[x]["BIC"])
    S = dict(N=N, best=best, best_mass=bm, best_acc=ba, dBIC_type=R[ba]["BIC"] - R[bm]["BIC"], dBIC_M0_best=R["M0"]["BIC"] - R[best]["BIC"],
             scatter_removed=1 - R[best]["s_hat"] / R["M0"]["s_hat"] if R["M0"]["s_hat"] > 0 else None,
             works=[x for x in ORDER if R[x]["works"]], models=R, seconds=time.time() - T)
    k3 = []
    if R["M9"]["lnL"] < R["M2"]["lnL"] - 1e-3: k3.append("M9 < M2")
    if R["M10"]["lnL"] < max(R["M3"]["lnL"], R["M5"]["lnL"]) - 1e-3: k3.append("M10 < max(M3, M5)")
    if R["M4"]["lnL"] < R["M0"]["lnL"] - 1e-3: k3.append("M4 < M0")
    if R["M8"]["lnL"] < R["M0"]["lnL"] - 1e-3: k3.append("M8 < M0")
    for x in ("M4", "M9", "M10"):
        if R[x].get("prescan_at_shat", -np.inf) > R[x]["lnL"] + 1e-6: k3.append(f"{x} MLE below its prescan")
    S["K3"] = dict(fails=k3, ok=not k3)
    if verbose:
        P(f"\n  [{foot}] {label}  N {N}   ({S['seconds']:.0f} s)   K3 nesting/optimiser: {'PASS' if not k3 else 'FAIL ' + '; '.join(k3)}")
        P(f"    {'model':4s} {'description':26s} {'type':8s} k  {'s_int^':>6s} [{'95%':^13s}] WORKS {'lnL':>9s} {'Lam_s':>7s} {'AIC':>8s} {'BIC':>8s} {'dBIC':>6s}  globals")
        for x in ORDER:
            r = R[x]; ul = "inf" if math.isinf(r["s95"][1]) else f"{r['s95'][1]:.3f}"
            g = ", ".join(f"{k} {v:.4g}" for k, v in r["phys"].items())
            if r.get("theta95"):
                lo_, hi_ = r["theta95"]; pv = lambda v: "bound" if v is None else f"{list(phys(x, [v]).values())[0]:.4g}"
                g += f"  (95% {pv(lo_)}..{pv(hi_)})"
            if any(r.get("at_bound", [])): g += "  [AT BOUND]"
            if r["flags"]: g += f"  [{'; '.join(r['flags'])}]"
            P(f"    {x:4s} {r['name'][:26]:26s} {r['type']:8s} {r['k']}  {r['s_hat']:6.3f} [{r['s95'][0]:.3f}-{ul:>5s}] {'yes' if r['works'] else 'no ':5s} "
              f"{r['lnL']:9.2f} {r['Lambda_s']:7.1f} {r['AIC']:8.2f} {r['BIC']:8.2f} {r['dBIC']:6.2f}  {g}")
        P(f"    best by BIC: {best} ({R[best]['name']}, {TYPE_LABEL[R[best]['type']]}), s_int {R[best]['s_hat']:.3f}; best mass-like {bm} "
          f"(BIC {R[bm]['BIC']:.2f}), best acceleration-like {ba} (BIC {R[ba]['BIC']:.2f}); dBIC_type (acc - mass) {S['dBIC_type']:+.2f}; "
          f"dBIC(M0 - best) {S['dBIC_M0_best']:+.2f}; scatter removed {100 * S['scatter_removed']:.0f}%; WORKS: {', '.join(S['works']) or 'none'}")
        if want_rows:
            P("    outlier residuals at each model's MLE: sigma_model / r = ln(sigma_obs/sigma_model) / t = r/sqrt(s^2 + (e/sigma)^2)")
            P("      " + " " * 5 + "".join(f"{nm:>25s}" for nm in OUTLIERS))
            P("      obs  " + "".join(f"{R['M0']['resid'][nm]['sig_obs']:>25.2f}" for nm in OUTLIERS if nm in R["M0"]["resid"]))
            for x in ORDER:
                rs = R[x]["resid"]
                P(f"      {x:4s} " + "".join(f"{rs[nm]['sig_model']:>8.2f} {rs[nm]['r']:+6.2f} {rs[nm]['t']:+6.1f}  " for nm in OUTLIERS if nm in rs))
            P("    five largest |t| per model:")
            for x in ORDER: P(f"      {x:4s} " + ", ".join(f"{n} {t:+.1f}" for n, t in R[x]["top5"]))
    return S
def type_verdict(dc, da):
    if dc >= 6 and da >= 6: return "MASS-LIKE PREFERRED"
    if dc <= -6 and da <= -6: return "ACCELERATION-LIKE PREFERRED"
    if dc * da > 0 and min(abs(dc), abs(da)) >= 2: return "LEANS MASS-LIKE" if dc > 0 else "LEANS ACCELERATION-LIKE"
    return "TYPE NOT DECIDED"
def verdict(SC, SA):
    both = [x for x in ORDER if SC["models"][x]["works"] and SA["models"][x]["works"]]
    tv = type_verdict(SC["dBIC_type"], SA["dBIC_type"])
    if both:
        nm = min(both, key=lambda x: SC["models"][x]["BIC"]); cls = f"A DESCRIPTION WORKS ({nm}" + (f"; also {', '.join(x for x in both if x != nm)}" if len(both) > 1 else "") + ")"
    else:
        bc, ba = SC["best"], SA["best"]; rc_, ra_ = SC["models"][bc], SA["models"][ba]
        cls = (f"NONE WORKS (best by BIC: canonical {bc} {rc_['name']} s_int {rc_['s_hat']:.3f} [95% {rc_['s95'][0]:.3f}-{rc_['s95'][1]:.3f}], "
               f"{TYPE_LABEL[rc_['type']]}; alt {ba} {ra_['name']} s_int {ra_['s_hat']:.3f} [95% {ra_['s95'][0]:.3f}-{ra_['s95'][1]:.3f}], {TYPE_LABEL[ra_['type']]})")
    return cls, tv, both

# ---------------- MUTATE: synthetic data from a known model ----------------
def synth(D, foot, rng):
    M = models(foot)
    if MUT == "shape": truth = M["M4"]["f"](np.array([0.20, -11.0]), dict(D, sl2_foot=D["sl2"][foot]))
    else: truth = M["M2"]["f"](np.array([math.log(SREF[foot])]), D)
    sp = np.sqrt(truth); n = len(sp); neg = rng.random(n) < D["ep"] / (D["em"] + D["ep"]); a = np.abs(rng.standard_normal(n))
    E = dict(D); E["s"] = np.maximum(np.where(neg, sp - a * D["ep"], sp + a * D["em"]), 0.1); return E

# ======================================================================================================================
D0 = make_D(SAMP); RES = dict(lane="CFG890", mutate=MUT or None, part=PART, N=D0["N"], C851=C851, SREF=SREF)
P("CFG890  which few-parameter global description of the dwarf excess works best?  one likelihood (split-normal errors, intrinsic"
  " scatter s_int in ln sigma), one penalty (AIC/BIC)" + (f"  [MUTATE {MUT}: synthetic data]" if MUT else "") + (f"  [PART {PART}]" if PART != "primary" else ""))
P(f"  sample N = {D0['N']} (CFG880's LVD sample); Ups_V 2 + gas; r_c 104 pc where fixed; CFG851 (b, log g+) canonical {C851['canonical'][0]:.4f}, "
  f"{C851['canonical'][1]:.3f}; alt {C851['alt'][0]:.4f}, {C851['alt'][1]:.3f}")

if MUT:
    SS = {}
    for foot, sd in (("canonical", 890 if MUT == "shape" else 891), ("alt", 890 if MUT == "shape" else 891)):
        E = synth(D0, foot, np.random.default_rng(sd)); SS[foot] = run_sample(E, foot, f"MUTATE {MUT} (truth {'M4 b 0.20, log g* -11.0' if MUT == 'shape' else f'M2 sigma_x {SREF[foot]:.3f}'})", want_rows=False)
    cls, tv, both = verdict(SS["canonical"], SS["alt"]); tm = "M4" if MUT == "shape" else "M2"
    c1 = all(SS[f]["models"][tm]["works"] for f in SS); c2 = all(SS[f]["models"][tm]["dBIC"] <= 2 for f in SS)
    c3 = tv not in (("MASS-LIKE PREFERRED", "LEANS MASS-LIKE") if MUT == "shape" else ("ACCELERATION-LIKE PREFERRED", "LEANS ACCELERATION-LIKE"))
    ok = c1 and c2 and c3
    P(f"\n  CLASS (synthetic): {cls}; type: {tv}")
    P(f"  MUTATE-{MUT}: truth {tm} WORKS on both {c1}; within dBIC <= 2 of the best on both {c2} "
      f"(dBIC {SS['canonical']['models'][tm]['dBIC']:.2f} / {SS['alt']['models'][tm]['dBIC']:.2f}); type verdict allowed {c3}  -> "
      f"{'control behaves as required' if ok else 'CONTROL FAILED'}")
    RES.update(canonical=SS["canonical"], alt=SS["alt"], cls=cls, type_verdict=tv, mutate_ok=ok, checks=dict(works=c1, dbic=c2, type=c3))
elif POST == "decomp":                                     # POST-HOC (added after the pre-registered runs; not graded)
    PR = json.load(open(os.path.join(HERE, "cfg890_results.json"))); LK0 = Like(D0); RES["posthoc"] = "decomp"
    P("  POST-HOC diagnostic (added after the pre-registered runs; not graded): per-dwarf ln L_i at the primary MLEs")
    for foot in A0:
        S = PR[foot]; M = models(foot); lnLi = {}
        for mid in (S["best_mass"], S["best_acc"], "M0"):
            r = S["models"][mid]; th = np.array(r["theta"])
            if M[mid].get("step"):
                o = np.argsort(D0["gN"]); below = np.zeros(D0["N"], bool); below[o[:int(th[2])]] = True
                sm2 = np.where(below, D0["sl2"][foot] * math.exp(th[0]), D0["sl2"][foot])
            else: sm2 = M[mid]["f"](th, D0)
            lnLi[mid] = LK0.lnLi(np.sqrt(sm2), r["s_hat"]); assert abs(lnLi[mid].sum() - r["lnL"]) < 1e-6, (mid, lnLi[mid].sum(), r["lnL"])
        bm, ba = S["best_mass"], S["best_acc"]; d = lnLi[bm] - lnLi[ba]; o = np.argsort(-d)
        P(f"\n  [{foot}] Delta_i = ln L_i({bm}) - ln L_i({ba}); total {d.sum():+.2f} (= ln L difference; dBIC_type {S['dBIC_type']:+.2f} incl. parameter count)")
        P("    most in favour of mass-like: " + ", ".join(f"{D0['names'][i]} {d[i]:+.2f} (lg g_N {D0['lgN'][i]:.2f}, r12 {D0['r12pc'][i]:.0f})" for i in o[:10]))
        P("    most in favour of acceleration-like: " + ", ".join(f"{D0['names'][i]} {d[i]:+.2f} (lg g_N {D0['lgN'][i]:.2f}, r12 {D0['r12pc'][i]:.0f})" for i in o[::-1][:10]))
        grp = {"M_V <= -6": D0["MV"] <= -6, "M_V > -6": D0["MV"] > -6, "r12 >= 1 kpc": D0["r12pc"] >= 1000}
        qs = np.quantile(D0["lgN"], [1 / 3, 2 / 3]); grp.update({"lowest-g_N third": D0["lgN"] <= qs[0], "middle third": (D0["lgN"] > qs[0]) & (D0["lgN"] <= qs[1]), "highest third": D0["lgN"] > qs[1]})
        P("    group sums: " + "; ".join(f"{k} (N {int(v.sum())}) {d[v].sum():+.2f}" for k, v in grp.items()))
        P("    without Crater II and Antlia II: " + f"{d[[n not in ('Crater II', 'Antlia II') for n in D0['names']]].sum():+.2f}")
        RES[foot] = dict(best_mass=bm, best_acc=ba, delta=dict(zip(D0["names"], [float(x) for x in d])), groups={k: float(d[v].sum()) for k, v in grp.items()})
elif POST == "binary":                                     # POST-HOC (added after the pre-registered runs; not graded)
    AP = {}
    for l in open(os.path.join(REPO, "real_research", "data", "arroyopolonio2026_ufd_binary_corrected.tsv")):
        if l.startswith("#") or l.startswith("name"): continue
        v = l.rstrip("\n").split("\t"); AP[v[0]] = (float(v[11]), float(v[12]), float(v[14]))      # sig_f, +1sigma, -1sigma (CFG880 V4)
    APMAP = {"Boo I": "Bootes I", "Car II": "Carina II", "Cra II": "Crater II", "Hyd I": "Hydrus I", "Leo IV": "Leo IV", "Leo V": "Leo V",
             "Ret II": "Reticulum II", "Sag II": "Sagittarius II", "Seg 1": "Segue 1", "Uni 1": "Unions 1", "Wil 1": "Willman 1"}
    D4 = {k: (v.copy() if isinstance(v, np.ndarray) else v) for k, v in D0.items()}; rep = []
    for k, nm in APMAP.items():
        if nm in D4["names"]:
            i = D4["names"].index(nm); D4["s"][i], D4["ep"][i], D4["em"][i] = AP[k]; rep.append(f"{nm} {D0['s'][i]:.2f} -> {AP[k][0]:.2f}")
    P("  POST-HOC diagnostic (added after the pre-registered runs; not graded): binary-corrected sigma for " + "; ".join(rep))
    SS = {foot: run_sample(D4, foot, "POST-HOC binary-corrected sigma", want_rows=True) for foot in A0}
    cls, tv, both = verdict(SS["canonical"], SS["alt"]); P(f"\n  POST-HOC binary-corrected: {cls}; type: {tv}")
    RES.update(posthoc="binary", replaced=rep, canonical=SS["canonical"], alt=SS["alt"], cls=cls, type_verdict=tv)
elif PART == "variants":
    VR = {}
    for foot in A0:
        a0 = A0[foot]; sl = np.sqrt(D0["sl2"][foot]); zlaw = np.where(D0["s"] < sl, (D0["s"] - sl) / D0["ep"], 0.0)
        D3 = dict(D0); D3["em"] = np.sqrt(D0["em"] ** 2 + (0.1 * D0["s"]) ** 2); D3["ep"] = np.sqrt(D0["ep"] ** 2 + (0.1 * D0["s"]) ** 2)
        V = {"V1 law-over-predicted dropped (z_law <= -2)": sub(D0, zlaw > -2), "V2 M_V <= -6": sub(D0, D0["MV"] <= -6), "V3 10% systematic floor": D3}
        VR[foot] = {"V1_removed": [n for n, z in zip(D0["names"], zlaw) if z <= -2]}
        P(f"\n  [{foot}] V1 removes: {', '.join(VR[foot]['V1_removed'])}")
        for lab, DV in V.items(): VR[foot][lab] = run_sample(DV, foot, lab)
    RES["variants"] = VR; RES["verdicts"] = {}
    for lab in ("V1 law-over-predicted dropped (z_law <= -2)", "V2 M_V <= -6", "V3 10% systematic floor"):
        cls, tv, both = verdict(VR["canonical"][lab], VR["alt"][lab]); RES["verdicts"][lab] = dict(cls=cls, type_verdict=tv, works_both=both)
        P(f"\n  {lab}: {cls}; type: {tv}")
else:
    # ---- K1 (code identity, exact): CFG880 per-dwarf law values; M2 lnL at s_int 0 and CFG880's universal sigma_bar
    K1 = {}; LK0 = Like(D0)
    for foot in A0:
        rows = {r["name"]: r["law"] for r in R880[foot]["primary"]["rows"]}; mine = np.sqrt(D0["sl2"][foot])
        rel = max(abs(mine[i] - rows[n]) / rows[n] for i, n in enumerate(D0["names"]))
        p = R880[foot]["primary"]; ref = p["lnLmax"] - p["Lambda"] / 2
        L2 = float(LK0.lnLi(np.sqrt(D0["sl2"][foot] + clump2(D0["r12pc"], p["sbar_univ"], A0[foot])), 0.0).sum())
        K1[foot] = dict(law_rel_max=rel, law_ok=rel < 1e-12, n_rows=len(rows), M2_s0=L2, cfg880_s0=ref, M2_diff=abs(L2 - ref), M2_ok=abs(L2 - ref) < 1e-8)
    k1ok = all(K1[f]["law_ok"] and K1[f]["M2_ok"] and K1[f]["n_rows"] == D0["N"] for f in A0); RES["K1"] = dict(K1, ok=k1ok)
    P("  K1 (exact identities with CFG880's committed numbers): " + "; ".join(
        f"{f}: per-dwarf law max rel diff {K1[f]['law_rel_max']:.1e}, M2 lnL(s_int 0, sigma_x {R880[f]['primary']['sbar_univ']:.4f}) {K1[f]['M2_s0']:.6f} "
        f"vs CFG880 {K1[f]['cfg880_s0']:.6f} (|diff| {K1[f]['M2_diff']:.1e})" for f in A0) + f"  -> {'PASS' if k1ok else 'FAIL'}")
    # ---- K2 (integrator) against brute-force trapezoids in t = eta/s
    def brute(sig, s, T, n):
        t = np.linspace(-T, T, n); w = np.full(n, t[1] - t[0]); w[[0, -1]] *= 0.5; lw = np.log(w) - 0.5 * t ** 2 - 0.5 * math.log(2 * math.pi); out = np.empty(len(sig))
        for i in range(len(sig)):
            out[i] = logsumexp(lnell(sig[i] * np.exp(s * t), LK0.so[i], LK0.em[i], LK0.ep[i], LK0.lnc[i]) + lw)
        return out
    K2 = {}
    for tag, T, n in (("frozen +-12, 240001", 12.0, 240001), ("wide +-40, 400001 (added after freezing)", 40.0, 400001)):
        worst = (0.0, None)
        for s in (0.002, 0.01, 0.03, 0.1, 0.38, 1.5):
            for fac in (1.0, 1.5):
                sig = fac * np.sqrt(D0["sl2"]["canonical"]); d = np.abs(LK0.lnLi(sig, s) - brute(sig, s, T, n)); i = int(np.argmax(d))
                if d[i] > worst[0]: worst = (float(d[i]), f"s {s}, x{fac}, {D0['names'][i]}")
        K2[tag] = dict(max_abs=worst[0], where=worst[1], ok=worst[0] < 1e-3)
        P(f"  K2 [{tag}]: max |d lnL_i| {worst[0]:.2e} ({worst[1]}) -> {'PASS' if worst[0] < 1e-3 else 'FAIL'}")
    RES["K2"] = K2
    # ---- informative (not an identity): M2 at sigma_x = V_x/sqrt2 with s_int fitted in this lane's ln-sigma hierarchy
    inf = {}
    for foot in A0:
        sig = np.sqrt(D0["sl2"][foot] + clump2(D0["r12pc"], SREF[foot], A0[foot])); g = lambda s: -float(LK0.lnLi(sig, s).sum())
        r = minimize_scalar(g, bounds=(0.0, 3.0), method="bounded", options=dict(xatol=1e-5)); inf[foot] = float(r.x)
    RES["M2_fixed_sref_s_int"] = inf
    P(f"  reported (not an identity): M2 with sigma_x fixed at V_x/sqrt2 -> s_int (ln sigma) {inf['canonical']:.3f} canonical / {inf['alt']:.3f} alt; "
      f"CFG880 (ln sigma_x hierarchy, sigma_bar free) 0.380 / 0.380")
    # ---- primary comparison
    SS = {}
    for foot in A0: SS[foot] = run_sample(D0, foot, "PRIMARY", want_rows=True)
    RES["canonical"], RES["alt"] = SS["canonical"], SS["alt"]
    cls, tv, both = verdict(SS["canonical"], SS["alt"])
    # ---- pre-registered qualifiers (variants and MUTATE outputs, if present)
    q = []; vpath = os.path.join(HERE, "cfg890_results_variants.json")
    if os.path.exists(vpath):
        VV = json.load(open(vpath))["verdicts"]
        for lab, short in (("V1 law-over-predicted dropped (z_law <= -2)", "V1"), ("V2 M_V <= -6", "V2")):
            if VV[lab]["type_verdict"] != tv: q.append(f"type verdict not robust: {short} gives {VV[lab]['type_verdict']}")
            if not both and VV[lab]["works_both"]: q.append(f"a description works only in {short}: {', '.join(VV[lab]['works_both'])}")
    else: q.append("variants not yet run")
    mok = {}
    for mode in ("shape", "clump"):
        pth = os.path.join(HERE, f"cfg890_results_MUTATE_{mode}.json")
        mok[mode] = json.load(open(pth))["mutate_ok"] if os.path.exists(pth) else None
    failed = [m for m, v in mok.items() if v is False]
    if failed: tv = f"TYPE NOT DECIDED (comparison lacks power: MUTATE-{'/'.join(failed)} failed)"
    missing = [m for m, v in mok.items() if v is None]
    if missing: q.append(f"MUTATE-{'/'.join(missing)} not yet run")
    overall = f"{cls}; type: {tv}" + "".join(f" ({x})" for x in q)
    P(f"\n  dBIC_type (best acc - best mass): canonical {SS['canonical']['dBIC_type']:+.2f}, alt {SS['alt']['dBIC_type']:+.2f};  MUTATE behaved: {mok}")
    P(f"\n  CLASS: {overall}")
    RES.update(cls=cls, type_verdict=tv, qualifiers=q, overall=overall, mutate_ok=mok)
P(f"\n  wall time {time.time() - T0:.0f} s")
json.dump(RES, open(os.path.join(HERE, f"cfg890_results{SUF}.json"), "w"), indent=1, default=lambda o: float(o) if isinstance(o, (np.floating, float)) else (int(o) if isinstance(o, np.integer) else str(o)))
open(os.path.join(HERE, f"cfg890{SUF}.out"), "w").write("\n".join(OUT) + "\n")
