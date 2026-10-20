#!/usr/bin/env python3
"""CFG909: sensitivity of the CFG650 theory-v2 cosmic-shear verdict to the LCDM-derived inputs in the SCORING
(FROZEN_CRITERIA.md).  Existing, already-scored outputs are rescored; no simulation is started.

  A  projection Omega_m (distances, lensing prefactor, NLA IA factor with recomputed D(z)); P(k, z) nodes, their z > 1
     continuation, the low-k shape and the DESI member's distances are NOT changed; both arms identically.
  B  covariance: B1/B2 one covariance for both arms at the framework's signal (R^p C R^p, p = 1 / 0.5), B3/B4 each arm at
     its own signal (class on dchi2 + d ln det C), B5 Omega_m 0.2976 + B1, B6 diag(C) (reported only).

Modes (single core, one process at a time):
  OMP_NUM_THREADS=1 nice -n 10 python3 cfg909_rescore.py --k1            K1 only (memory / reproduction first call)
  OMP_NUM_THREADS=1 nice -n 10 python3 cfg909_rescore.py --mutate        MUTATE (exit 1 = both controls bite)
  OMP_NUM_THREADS=1 nice -n 10 python3 cfg909_rescore.py                 main: T1x (canonical) / T2x (alt) vs CFG596 P0
  OMP_NUM_THREADS=1 nice -n 10 python3 cfg909_rescore.py --native-check  K5: the --score path on CFG636 C1 vs P0 (native lib)
  OMP_NUM_THREADS=1 nice -n 10 python3 cfg909_rescore.py --score NC1x NCS0 [--mutate]
       the same rescoring for a CFG654 native-input pair AFTER the chain has scored it (NOT run in this lane)
kappa = 1/2 FITTED; footings never pooled; raw data, framework-native; no HMcode / BAHAMAS; not theory closed."""
import os, sys, json, math, glob, time, hashlib, importlib.util
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
os.environ["CFG596_MUTATE"] = "0"; os.environ["CFG650_SCORE"] = "T"; os.environ.pop("CFG650_JOBSET", None)
import numpy as np
import warnings
warnings.filterwarnings("ignore", message=".*encountered in matmul")   # spurious BLAS flags (Accelerate), as in cfg654_native.py; values checked by K1
from scipy.integrate import quad, solve_ivp
from scipy.stats import chi2 as CH

HERE = os.path.dirname(os.path.abspath(__file__)); CFG = os.path.abspath(os.path.join(HERE, ".."))
SRC650 = os.path.join(CFG, "CFG650_theory_v2_combined_pm", "cfg650_native.py")
SRC592 = os.path.join(CFG, "CFG592_cosmic_shear_likelihood", "cfg592_native.py")
SRC654 = os.path.join(CFG, "CFG654_independent_inputs", "cfg654_native.py")
BLOB = {SRC650: "211b36aba3925588c5267b98cbf22f01548656f4", SRC592: "437bc9524d358dd97c4e1990d7706869b8b03111",
        SRC654: "450677f9e0ce8727020f2f81904f8848e7f95f6b"}
K1_JSON = os.path.join(CFG, "CFG650_theory_v2_combined_pm", "cfg650_native_results.json")
K1_MUT_JSON = os.path.join(CFG, "CFG650_theory_v2_combined_pm", "cfg650_native_results_MUTATE.json")
K5_JSON = os.path.join(CFG, "CFG654_independent_inputs", "cfg654_native_posthoc.json")
K_BLOB = {K1_JSON: "c2802e71b278ad1b2fbad39dd2ee36f870d50153", K1_MUT_JSON: "7504357698f81f49eaa0e4fe35d875e07ea6f32c",
          K5_JSON: "b03696458adaf1c33904575220076e9a50eb7be7"}
OM_CFG886, OM_CFG886_SIG, OM_CFG682 = 0.2976, 0.0085, 0.3085
OM_GRID_EXTRA = [round(OM_CFG886 - 2 * OM_CFG886_SIG, 4), OM_CFG886, OM_CFG682, round(0.3138 + 2 * OM_CFG886_SIG, 4)]   # 0.2806 .. 0.3308
OM_MUT = 0.25
TOL_K1, TOL_EXACT = 1e-6, 1e-9

MUT = "--mutate" in sys.argv; K1ONLY = "--k1" in sys.argv; NATCHK = "--native-check" in sys.argv; SCOREMODE = "--score" in sys.argv
JOBS = [a for a in sys.argv[1:] if not a.startswith("--")]
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
def git_blob(path):
    b = open(path, "rb").read(); return hashlib.sha1(b"blob %d\0" % len(b) + b).hexdigest()
T0 = time.time()

# ------------------------------------------------------------------ library loading (read only)
def load_T():
    for f in (SRC650, SRC592): assert git_blob(f) == BLOB[f], f"blob mismatch {f}"
    code = open(SRC650).read(); assert code.count("\ndef strip(r)") == 1
    H = {"__file__": SRC650, "__name__": "cfg650_native_lib"}
    argv0 = sys.argv; sys.argv = [SRC650]
    try: exec(compile(code[:code.index("\ndef strip(r)")], SRC650, "exec"), H)
    finally: sys.argv = argv0
    G = H["G"]; W650 = os.path.join(G["EXT"], "cfg650_work")
    for job in ("T1x", "T2x"): assert glob.glob(os.path.join(W650, job, "cfg650_*_RES_*.json")), f"{job} missing"
    runs = []
    for foot, F, S, N, L in H["runs_list"]():
        run, held, extra, B0 = H["build"](F, S, N, L, foot, f"L{L:g}_N{N}_{foot}")
        runs.append(dict(foot=foot, label=run["name"], run=run, held=held, Binj=H["Binj"](foot)))
    assert [r["foot"] for r in runs] == ["canonical", "alt"]
    return G, runs

def load_654():
    assert git_blob(SRC654) == BLOB[SRC654], "blob mismatch cfg654_native.py"
    sp = importlib.util.spec_from_file_location("cfg654_native_lib", SRC654); mod = importlib.util.module_from_spec(sp); sp.loader.exec_module(mod)
    return mod

def binj_native(EXT, foot):     # = CFG654 score_production's Binj (= CFG650's)
    d = np.load(os.path.join(EXT, "cfg530_work", "profiles", "N512", f"cfg526_LR{'can' if foot == 'canonical' else 'alt'}_L100.npz"))
    k = np.array(d["kgrav"]); B = np.array(d["pgrav"]) / np.array(d["ppart"]); lk, lb = np.log(k), np.log(B)
    return lambda KK: np.exp(np.interp(np.log(np.clip(KK, k[0], k[-1])), lk, lb))

# ------------------------------------------------------------------ projection-Omega_m context
class Proj:
    """Swaps the projection Omega_m: distances (+ LOC in native mode) and the kernel prefactor in set_bg (the growth array
    stays the as-run one, so Pmat's z > 1 continuation is untouched); the IA growth in set_ia (used by C_ell only)."""
    def __init__(self, G, native=None):
        self.G = G; self.native = native
        self.orig = dict(Om=G["Om"], PM=G["BG"]["PM"], LOC=G["BG"].get("LOC"), DZG=G["DZG"])
        self.Om0 = G["Om"]; self._dcache = {}
    def bgd(self, Ez):          # = cfg654_native.load_lib's local bgd
        ZG = self.G["ZG"]
        chi = np.array([quad(lambda x: 1 / Ez(x), 0, z, epsabs=0, epsrel=1e-10)[0] for z in ZG]) * 2997.92458
        return chi, 2997.92458 / np.array([Ez(z) for z in ZG])
    def set_bg(self, Om_v):
        """distances only: G['Om'] and the growth stay the as-run objects here, because Pmat's z > 1 continuation calls the
        library's Dgrow, whose E_PM reads the global Om at call time (T mode). set_ia swaps Om and the IA growth afterwards."""
        G = self.G; G["Om"] = self.orig["Om"]; G["DZG"] = self.orig["DZG"]
        if self.native is None:
            G["BG"]["PM"] = G["background"](Om_v)
        else:
            nv = self.native; mod = nv["mod"]
            OL_v = nv["OL"] + (nv["Om"] - Om_v)                       # keeps the table's flatness sum (exact at the as-scored value)
            G["BG"]["PM"] = self.bgd(mod.native_E(Om_v, nv["Or"], OL_v))
            OmL = Om_v * nv["h"] ** 2 / mod.H0LOC ** 2; OrL = nv["Or"] * nv["h"] ** 2 / mod.H0LOC ** 2
            G["BG"]["LOC"] = self.bgd(mod.native_E(OmL, OrL, 1 - OmL - OrL))
    def dzg_ia(self, Om_v):
        if Om_v in self._dcache: return self._dcache[Om_v]
        G = self.G; AG = G["AG"]
        if self.native is None:                                     # the library's own growth integral, Omega_m swapped
            E = lambda a: math.sqrt(Om_v / a ** 3 + 1 - Om_v)
            g = lambda x: quad(lambda u: 1.0 / (u * E(u)) ** 3, 0, x)[0] * E(x)
            out = np.array([g(a) / g(1.0) for a in AG])
        else:
            nv = self.native
            if Om_v == nv["Om"]: out = self.orig["DZG"]               # ratio exactly 1 at the as-scored value
            else: out = self.orig["DZG"] * self.dode(Om_v)(AG) / self.dode(nv["Om"])(AG)
        self._dcache[Om_v] = out; return out
    def dode(self, Om_v):
        """linear growth ODE on the native E(z) (trickle kept), normalised D(a = 1) = 1; used only as a ratio."""
        nv = self.native; mod = nv["mod"]; E = mod.native_E(Om_v, nv["Or"], nv["OL"] + (nv["Om"] - Om_v))
        Ea = lambda lna: E(math.exp(-lna) - 1.0)
        def rhs(lna, y):
            h = 1e-4; dlnE = (math.log(Ea(lna + h)) - math.log(Ea(lna - h))) / (2 * h); e = Ea(lna)
            return [y[1], -(2 + dlnE) * y[1] + 1.5 * Om_v * math.exp(-3 * lna) / e ** 2 * y[0]]
        a0 = 1e-2; s = solve_ivp(rhs, (math.log(a0), 0.0), [a0, a0], rtol=1e-10, atol=1e-14, dense_output=True)
        D1 = s.sol(0.0)[0]
        return lambda a: np.array([s.sol(math.log(x))[0] / D1 for x in np.atleast_1d(a)])
    def set_ia(self, Om_v):
        """after the P matrices are built: kernel prefactor + NLA IA factor at Om_v (used by kernels / C_ell only)."""
        d = self.dzg_ia(Om_v); self.G["Om"] = Om_v; self.G["DZG"] = d
    def restore(self):
        G = self.G; G["Om"] = self.orig["Om"]; G["BG"]["PM"] = self.orig["PM"]; G["DZG"] = self.orig["DZG"]
        if self.orig["LOC"] is not None: G["BG"]["LOC"] = self.orig["LOC"]

# ------------------------------------------------------------------ scoring engine
class Engine:
    def __init__(self, G, proj, rb, report_bg=()):
        self.G = G; self.proj = proj; self.RB = rb; self.REP = tuple(report_bg)
        self.fit, self.Pmat, self.theory, self.nuis_spec = G["fit"], G["Pmat"], G["theory"], G["nuis_spec"]
        self.support_mask, self.subset, self.klass, self.SURV = G["support_mask"], G["subset"], G["klass"], G["SURV"]
        self.ROB = ("widen2", "noIA", "held", rb)
    def mats(self, rr, Om_v=None):
        """P matrices under the projection Om_v (None = the library's own objects, untouched)."""
        if Om_v is not None: self.proj.set_bg(Om_v)
        run, held, Pm = rr["run"], rr["held"], self.Pmat
        M = dict(S0=Pm(run, "S0"), F=Pm(run, "F"), Fh=Pm(held, "F"), S0b=Pm(run, "S0", bg=self.RB), Fb=Pm(run, "F", bg=self.RB),
                 S0inj=Pm(run, "S0", inject=rr["Binj"]))
        for b in self.REP: M["S0_" + b] = Pm(run, "S0", bg=b); M["F_" + b] = Pm(run, "F", bg=b)
        if Om_v is not None: self.proj.set_ia(Om_v)
        return M
    def keep(self, Sv, rr, M):
        f = self.support_mask(Sv, rr["run"], M["S0"]); return Sv["pubkeep"] & (f >= 0.9)
    def cfgs(self, noIA_set=False):
        c = [("main", ("F", {}), ("S0", {})), ("noIA", ("F", dict(ia=False)), ("S0", dict(ia=False))),
             ("widen2", ("F", dict(widen=2.0)), ("S0", dict(widen=2.0))), ("held", ("Fh", {}), None),
             (self.RB, ("Fb", dict(bg=self.RB)), ("S0b", dict(bg=self.RB)))]
        c += [(b + "_reported", ("F_" + b, dict(bg=b)), ("S0_" + b, dict(bg=b))) for b in self.REP]
        if noIA_set:
            c += [("noIA_widen2", ("F", dict(widen=2.0, ia=False)), ("S0", dict(widen=2.0, ia=False))), ("noIA_held", ("Fh", dict(ia=False)), "noIA"),
                  ("noIA_" + self.RB, ("Fb", dict(bg=self.RB, ia=False)), ("S0b", dict(bg=self.RB, ia=False)))]
        return c
    @staticmethod
    def Dc(D, C): return dict(D, Cinv=np.linalg.inv(C))
    @staticmethod
    def ratio(t, tref):
        r = t / tref; bad = ~np.isfinite(r) | (r <= 0); r = np.where(bad, 1.0, r)
        n = int(bad.sum() + ((r < 0.5) | (r > 2.0)).sum()); return np.clip(r, 0.5, 2.0), n
    @staticmethod
    def RCR(C, r, p): q = r ** p; return q[:, None] * C * q[None, :]
    def town(self, Sv, D, Ds0, M, s0):
        par = self.nuis_spec(Sv, 1.0, True)[3](np.array(s0["x"])); mock = self.theory(Sv, D, par, M["S0inj"], "PM")
        return self.fit(Sv, Ds0, M["S0"], data=mock)["chi2"]
    def common_cov(self, Sv, D, M, C, p):
        s0 = self.fit(Sv, D, M["S0"]); tref = s0["t"]; f0 = self.fit(Sv, D, M["F"])
        r1, n1 = self.ratio(f0["t"], tref); C1 = self.RCR(C, r1, p); f1 = self.fit(Sv, self.Dc(D, C1), M["F"])
        r2, n2 = self.ratio(f1["t"], tref); C2 = self.RCR(C, r2, p)
        info = dict(p=p, r_min=float(r2.min()), r_max=float(r2.max()), r_median=float(np.median(r2)), n_clipped=max(n1, n2),
                    conv_max_abs_dr=float(np.max(np.abs(r2 - r1))))
        return C2, info
    def score(self, Sv, D, M, cov="pub", C=None, p=None, Ccommon=None, noIA_set=False):
        """cov: pub | diag | common (Ccommon for both arms) | own (each arm at its own signal, p)."""
        fit = self.fit; N = D["N"]; out = dict(N=N, cfg={}); fits = {}
        if cov == "pub": Dx = D
        elif cov == "diag": Dx = self.Dc(D, np.diag(np.diag(C)))
        elif cov == "common": Dx = self.Dc(D, Ccommon)
        if cov in ("pub", "diag", "common"):
            for name, (fk, fkw), s in self.cfgs(noIA_set):
                fS = fits["main"][1] if s is None else (fits[s][1] if isinstance(s, str) else fit(Sv, Dx, M[s[0]], **s[1]))
                fF = fit(Sv, Dx, M[fk], **fkw); fits[name] = (fF, fS)
                out["cfg"][name] = dict(chi2_F=fF["chi2"], chi2_S0=fS["chi2"], dchi2=fF["chi2"] - fS["chi2"])
            Ds0 = Dx
        else:                                                           # own
            lnC = np.linalg.slogdet(C); assert lnC[0] > 0; nclip = 0; k4 = True
            for name, (fk, fkw), s in self.cfgs(noIA_set):
                fS = fits["main"][1] if s is None else (fits[s][1] if isinstance(s, str) else fit(Sv, D, M[s[0]], **s[1]))
                tref = fS["t"]; rS = fS["t"] / tref; k4 = k4 and bool(np.all(rS == 1.0))     # K4: control r == 1 exactly
                kw = dict(fkw); f0 = fit(Sv, D, M[fk], **kw); r1, n1 = self.ratio(f0["t"], tref); C1 = self.RCR(C, r1, p)
                f1 = fit(Sv, self.Dc(D, C1), M[fk], **kw); r2, n2 = self.ratio(f1["t"], tref); C2 = self.RCR(C, r2, p)
                f2 = fit(Sv, self.Dc(D, C2), M[fk], **kw); lnF = np.linalg.slogdet(C2); assert lnF[0] > 0
                nclip = max(nclip, n1, n2); fits[name] = (f2, fS)
                dch = f2["chi2"] - fS["chi2"]; dld = float(lnF[1] - lnC[1])
                out["cfg"][name] = dict(chi2_F=f2["chi2"], chi2_S0=fS["chi2"], dchi2=dch, dlndet=dld, dm2lnL=dch + dld,
                                        conv_max_abs_dr=float(np.max(np.abs(r2 - r1))), r_median=float(np.median(r2)))
            out.update(K4_control_r_exactly_1=k4, n_clipped=nclip); Ds0 = D
        fF, fS = fits["main"]
        out.update(A_IA_F=fF["A_IA"], A_IA_S0=fS["A_IA"], chi2data_F=fF["chi2_data"], chi2data_S0=fS["chi2_data"],
                   p_F=float(CH.sf(fF["chi2_data"], N)), p_S0=float(CH.sf(fS["chi2_data"], N)))
        out["T_OWN_chi2"] = self.town(Sv, D, Ds0, M, fS); out["T_OWN"] = bool(out["T_OWN_chi2"] >= 9)
        key = "dm2lnL" if cov == "own" else "dchi2"
        out["dchi2"] = out["cfg"]["main"]["dchi2"]; out["robust"] = {n: out["cfg"][n]["dchi2"] for n in self.ROB}
        out["stat"] = key; out["stat_main"] = out["cfg"]["main"][key]; out["stat_robust"] = {n: out["cfg"][n][key] for n in self.ROB}
        cl = self.klass(out["stat_main"], list(out["stat_robust"].values()), N >= 10)
        out["class"] = "NOT DIAGNOSTIC" if not out["T_OWN"] else cl; out["class_before_TOWN"] = cl
        if cov == "own":
            c2 = self.klass(out["dchi2"], list(out["robust"].values()), N >= 10)
            out["class_dchi2_only_reported"] = "NOT DIAGNOSTIC" if not out["T_OWN"] else c2
        if noIA_set:
            rn = {"widen2": out["cfg"]["noIA_widen2"]["dchi2"], "held": out["cfg"]["noIA_held"]["dchi2"], self.RB: out["cfg"]["noIA_" + self.RB]["dchi2"]}
            out["robust_noIA"] = rn; c3 = self.klass(out["cfg"]["noIA"]["dchi2"], list(rn.values()), N >= 10)
            out["class_noIA"] = "NOT DIAGNOSTIC" if not out["T_OWN"] else c3
        return out

def line(tag, foot, sn, o):
    s = (f"  [{tag:22s}] {foot:9s} {sn:4s}: N {o['N']}; chi2 S0 {o['cfg']['main']['chi2_S0']:.2f} (p {o['p_S0']:.3f}), F {o['cfg']['main']['chi2_F']:.2f} "
         f"(p {o['p_F']:.3f}); dchi2 {o['dchi2']:+.3f}; robust " + "/".join(f"{v:+.2f}" for v in o["robust"].values()))
    if o["stat"] == "dm2lnL":
        s += f"; d(-2lnL) {o['stat_main']:+.3f} (robust " + "/".join(f"{v:+.2f}" for v in o["stat_robust"].values()) + f"); dchi2-only class {o['class_dchi2_only_reported']}"
    s += f"; T-OWN {o['T_OWN_chi2']:.2f} -> {o['class']}"
    return s

# ------------------------------------------------------------------ K1 comparison helpers
def cmp(a, b, tol): return abs(a - b) <= tol
def k1_check_T(label, sn, o, ref, refm):
    st = ref["runs"][label]["surveys"][sn]; bad = []
    pairs = [("dchi2", o["dchi2"], st["dchi2"]), ("dchi2_noIA", o["cfg"]["noIA"]["dchi2"], st["dchi2_noIA"]),
             ("chi2_S0", o["cfg"]["main"]["chi2_S0"], st["fits"]["IA"]["S0"]["chi2"]), ("chi2_F", o["cfg"]["main"]["chi2_F"], st["fits"]["IA"]["F"]["chi2"])]
    pairs += [(f"robust.{k}", o["robust"][k], st["robust"][k]) for k in ("widen2", "noIA", "held", "DESI")]
    pairs += [(f"robust_noIA.{k}", o["robust_noIA"][k], st["robust_noIA"][k]) for k in ("widen2", "held", "DESI")]
    pairs += [("T_OWN_chi2", o["T_OWN_chi2"], refm["runs"][label]["surveys"][sn]["MUT"]["T_OWN_chi2"])]
    for n, a, b in pairs:
        if not cmp(a, b, TOL_K1): bad.append(f"{n} {a!r} vs {b!r}")
    if o["class"] != st["class"]: bad.append(f"class {o['class']} vs {st['class']}")
    if o["class_noIA"] != st["class_noIA"]: bad.append(f"class_noIA {o['class_noIA']} vs {st['class_noIA']}")
    md = max(abs(a - b) for _, a, b in pairs)
    return (not bad), bad, md
def same_numbers(o, ref, keys=("main", "noIA", "widen2", "held"), tol=TOL_EXACT, rb="DESI"):
    md = max(abs(o["cfg"][k]["dchi2"] - ref["cfg"][k]["dchi2"]) for k in keys + (rb,))
    md = max(md, max(abs(o["cfg"][k][x] - ref["cfg"][k][x]) for k in keys + (rb,) for x in ("chi2_F", "chi2_S0")))
    return md <= tol, md

def save(R, suf):
    R["runtime_s"] = time.time() - T0
    json.dump(R, open(os.path.join(HERE, f"cfg909_results_{suf}.json"), "w"), indent=1)
    open(os.path.join(HERE, f"cfg909_{suf}.out"), "w").write("\n".join(OUT) + "\n")

HDR = "kappa = 1/2 FITTED; footings never pooled; raw data, framework-native; no HMcode / BAHAMAS; CONSISTENT does not mean the data favour the framework; not theory closed."

# ------------------------------------------------------------------ the variant grid (one engine, both modes)
def run_grid(E, runs, R, suf, Om_as, grid, k1fun=None, native=False):
    """K1 (as scored), K2 (override at Om_as), K3 (common r == 1), then the frozen variants. Writes after each block."""
    SURV = E.SURV; base = {}; R["variants"] = {}; R["controls"] = {}
    def put(vname, foot, sn, o, meta=None):
        v = R["variants"].setdefault(vname, dict(meta or {}, results={})); v["results"].setdefault(foot, {})[sn] = o
    # K1 (library objects untouched)
    P("\n== K1: as scored (library objects, published covariance) ==")
    k1ok = True
    for rr in runs:
        M = E.mats(rr); base[rr["foot"]] = dict(M=M, D={}, keep={}, C={})
        for sn, Sv in SURV.items():
            kp = E.keep(Sv, rr, M); D = E.subset(Sv, kp); C = Sv["cov"][np.ix_(kp, kp)]
            base[rr["foot"]]["D"][sn] = D; base[rr["foot"]]["keep"][sn] = kp; base[rr["foot"]]["C"][sn] = C
            o = E.score(Sv, D, M, "pub", noIA_set=not native); put("AS_SCORED", rr["foot"], sn, o, dict(class_weighted=False, what="as scored (reference)"))
            P(line("AS_SCORED", rr["foot"], sn, o))
            if k1fun is not None:
                ok, bad, md = k1fun(rr, sn, o); k1ok = k1ok and ok
                R["controls"].setdefault("K1", {}).setdefault(rr["foot"], {})[sn] = dict(pass_=ok, max_abs_diff=md, mismatches=bad)
                P(f"    K1 {rr['foot']} {sn}: {'PASS' if ok else 'FAIL'} (max |diff| {md:.2e})" + ("" if ok else f" {bad}"))
    R["controls"]["K1_pass"] = k1ok if k1fun is not None else "PENDING (no production score to reproduce)"
    save(R, suf)
    if K1ONLY: return
    # K2: override path at the as-scored Omega_m
    P("\n== K2: projection override evaluated at the as-scored Omega_m ==")
    k2 = True
    for rr in runs:
        M = E.mats(rr, Om_as)
        for sn, Sv in SURV.items():
            o = E.score(Sv, base[rr["foot"]]["D"][sn], M, "pub"); ok, md = same_numbers(o, R["variants"]["AS_SCORED"]["results"][rr["foot"]][sn], rb=E.RB)
            ok = ok and abs(o["T_OWN_chi2"] - R["variants"]["AS_SCORED"]["results"][rr["foot"]][sn]["T_OWN_chi2"]) <= TOL_EXACT; k2 = k2 and ok
            R["controls"].setdefault("K2", {}).setdefault(rr["foot"], {})[sn] = dict(pass_=ok, max_abs_diff=md); P(f"    K2 {rr['foot']} {sn}: {'PASS' if ok else 'FAIL'} ({md:.2e})")
        E.proj.restore()
    R["controls"]["K2_pass"] = k2
    # K3: common-covariance path with r == 1
    P("\n== K3: common-covariance path with r == 1 ==")
    k3 = True
    for rr in runs:
        M = base[rr["foot"]]["M"]
        for sn, Sv in SURV.items():
            D = base[rr["foot"]]["D"][sn]; C = base[rr["foot"]]["C"][sn]; Cc = E.RCR(C, np.ones(D["N"]), 1.0); Dx = E.Dc(D, Cc)
            d = E.fit(Sv, Dx, M["F"])["chi2"] - E.fit(Sv, Dx, M["S0"])["chi2"]; ref = R["variants"]["AS_SCORED"]["results"][rr["foot"]][sn]["dchi2"]
            ok = abs(d - ref) <= TOL_EXACT; k3 = k3 and ok
            R["controls"].setdefault("K3", {}).setdefault(rr["foot"], {})[sn] = dict(pass_=ok, abs_diff=abs(d - ref)); P(f"    K3 {rr['foot']} {sn}: {'PASS' if ok else 'FAIL'} ({abs(d - ref):.2e})")
    R["controls"]["K3_pass"] = k3; save(R, suf)
    # A: projection Omega_m (primary kept set + re-derived support)
    for om in grid:
        if om == Om_as: continue
        tag = f"OM_{om:.4f}"; P(f"\n== A {tag}: projection Omega_m = {om} (both arms) ==")
        for rr in runs:
            M = E.mats(rr, om); foot = rr["foot"]
            for sn, Sv in SURV.items():
                D = base[foot]["D"][sn]; o = E.score(Sv, D, M, "pub")
                put(tag, foot, sn, o, dict(class_weighted=True, Om=om, keep="as-scored kept set (primary)")); P(line(tag, foot, sn, o))
                kp2 = E.keep(Sv, rr, M); same = bool(np.array_equal(kp2, base[foot]["keep"][sn]))
                if same: o2 = dict(o, keep_same_as_scored=True)
                else: o2 = E.score(Sv, E.subset(Sv, kp2), M, "pub"); o2["keep_same_as_scored"] = False
                o2["N_added"] = int((kp2 & ~base[foot]["keep"][sn]).sum()); o2["N_dropped"] = int((~kp2 & base[foot]["keep"][sn]).sum())
                put(tag + "_resupport", foot, sn, o2, dict(class_weighted=True, Om=om, keep="support re-derived at this Omega_m"))
                P(line(tag + "_resupport", foot, sn, o2) + ("  [same kept set]" if same else f"  [+{o2['N_added']}/-{o2['N_dropped']} points]"))
            E.proj.restore()
        save(R, suf)
    # B1/B2 common, B3/B4 own, B5 combined, B6 diag
    blocks = [("CV1_COMMON", "common", 1.0, None, True), ("CVh_COMMON", "common", 0.5, None, True), ("CV1_OWN", "own", 1.0, None, True),
              ("CVh_OWN", "own", 0.5, None, True), (f"COMB_OM{OM_CFG886:.4f}_CV1_COMMON", "common", 1.0, OM_CFG886, True), ("DIAG", "diag", None, None, False)]
    for tag, cov, p, om, cw in blocks:
        P(f"\n== B {tag} ==")
        for rr in runs:
            foot = rr["foot"]; M = base[foot]["M"] if om is None else E.mats(rr, om)
            for sn, Sv in SURV.items():
                D = base[foot]["D"][sn]; C = base[foot]["C"][sn]; meta = dict(class_weighted=cw, cov=cov, p=p, Om=om if om is not None else Om_as)
                if cov == "common":
                    Cc, info = E.common_cov(Sv, D, M, C, p); o = E.score(Sv, D, M, "common", Ccommon=Cc); o["common_cov"] = info
                elif cov == "own": o = E.score(Sv, D, M, "own", C=C, p=p)
                else: o = E.score(Sv, D, M, "diag", C=C)
                put(tag, foot, sn, o, meta); P(line(tag, foot, sn, o) + (f"  [r median {o['common_cov']['r_median']:.4f}, range {o['common_cov']['r_min']:.4f}..{o['common_cov']['r_max']:.4f}, conv {o['common_cov']['conv_max_abs_dr']:.1e}, clipped {o['common_cov']['n_clipped']}]" if cov == "common" else "")
                                                                    + (f"  [K4 control r == 1: {o['K4_control_r_exactly_1']}; clipped {o['n_clipped']}]" if cov == "own" else ""))
            if om is not None: E.proj.restore()
        save(R, suf)
    k4 = True; k4md = 0.0                                              # K4: the control keeps the published C (its chi2 = K1's)
    for t in ("CV1_OWN", "CVh_OWN"):
        for f, d in R["variants"][t]["results"].items():
            for s, o in d.items():
                a = R["variants"]["AS_SCORED"]["results"][f][s]
                md = max(abs(o["cfg"][k]["chi2_S0"] - a["cfg"][k]["chi2_S0"]) for k in ("main", "noIA", "widen2", E.RB))
                k4md = max(k4md, md); k4 = k4 and o["K4_control_r_exactly_1"] and md <= TOL_EXACT
    R["controls"]["K4_pass"] = k4; R["controls"]["K4_max_abs_diff_chi2_S0"] = k4md
    # lane class (KiDS, each footing)
    flips = []; worst = {}
    for t, v in R["variants"].items():
        if not v.get("class_weighted"): continue
        for foot, d in v["results"].items():
            o = d.get("KiDS");
            if o is None: continue
            ref = R["variants"]["AS_SCORED"]["results"][foot]["KiDS"]["class"]
            if o["class"] != ref: flips.append(dict(variant=t, foot=foot, as_scored=ref, now=o["class"], stat_main=o["stat_main"]))
            w = worst.get(foot)
            if w is None or o["stat_main"] > w["stat_main"]: worst[foot] = dict(variant=t, stat_main=o["stat_main"], stat=o["stat"], margin_to_4=4 - o["stat_main"])
    allc = all(R["variants"]["AS_SCORED"]["results"][f]["KiDS"]["class"] == "CONSISTENT" for f in R["variants"]["AS_SCORED"]["results"])
    R["lane_class"] = ("ROBUST" if (not flips and allc) else "SENSITIVE") if R["controls"].get("K1_pass") is not False else "NOT INTERPRETED (K1 failed)"
    if R["controls"].get("K1_pass") not in (True, False): R["lane_class"] += " (PROVISIONAL: K1 pending)"
    R["flips"] = flips; R["worst_class_driving_stat"] = worst
    des = {t: {f: d["DES"]["class"] for f, d in v["results"].items() if "DES" in d} for t, v in R["variants"].items()}
    R["DES_classes"] = des
    diag_flip = [dict(foot=f, now=d["KiDS"]["class"]) for f, d in R["variants"]["DIAG"]["results"].items() if d["KiDS"]["class"] != R["variants"]["AS_SCORED"]["results"][f]["KiDS"]["class"]]
    R["DIAG_reported_flips"] = diag_flip
    P(f"\nLANE CLASS (KiDS, class-weighted variants): {R['lane_class']}; flips: {flips if flips else 'none'}")
    P("worst class-driving statistic per footing: " + "; ".join(f"{f}: {w['variant']} {w['stat']} {w['stat_main']:+.2f} (margin to 4: {w['margin_to_4']:.2f})" for f, w in worst.items()))
    P(f"DIAG (reported only) class changes: {diag_flip if diag_flip else 'none'}")
    P("controls: " + ", ".join(f"{k} {R['controls'][k]}" for k in ("K1_pass", "K2_pass", "K3_pass", "K4_pass")))
    save(R, suf)

# ------------------------------------------------------------------ MUTATE (both modes)
def run_mutate(E, runs, R, suf):
    P("\n== MUTATE: M1 Omega_m = 0.25 on the FRAMEWORK arm only; M2 framework covariance x 0.5 (control as scored) ==")
    bites = dict(M1=True, M2=True); R["mutate"] = {}
    for rr in runs:
        foot = rr["foot"]; M = E.mats(rr)
        for sn, Sv in E.SURV.items():
            kp = E.keep(Sv, rr, M); D = E.subset(Sv, kp); C = Sv["cov"][np.ix_(kp, kp)]
            s0 = E.fit(Sv, D, M["S0"]); f0 = E.fit(Sv, D, M["F"]); d0 = f0["chi2"] - s0["chi2"]
            E.proj.set_bg(OM_MUT); PFm = E.Pmat(rr["run"], "F"); E.proj.set_ia(OM_MUT); fm1 = E.fit(Sv, D, PFm); E.proj.restore()
            d1 = fm1["chi2"] - s0["chi2"]
            fm2 = E.fit(Sv, E.Dc(D, 0.5 * C), M["F"]); d2 = fm2["chi2"] - s0["chi2"]
            o = dict(N=D["N"], dchi2_as_scored=d0, M1_dchi2=d1, M1_shift=d1 - d0, M2_dchi2=d2, M2_shift=d2 - d0)
            R["mutate"].setdefault(foot, {})[sn] = o
            if sn == "KiDS":
                bites["M1"] = bites["M1"] and abs(d1 - d0) >= 9; bites["M2"] = bites["M2"] and abs(d2 - d0) >= 9
            P(f"  {foot:9s} {sn:4s}: as scored dchi2 {d0:+.3f}; M1 (F at Omega_m 0.25) {d1:+.2f} (shift {d1 - d0:+.2f}); M2 (F cov x 0.5) {d2:+.2f} (shift {d2 - d0:+.2f})")
    R["mutate_bites"] = bites; R["all_bite"] = bool(bites["M1"] and bites["M2"])
    P(f"MUTATE bites (KiDS shift >= 9 on every footing): {bites} -> all bite = {R['all_bite']}")
    save(R, suf)
    sys.exit(1 if R["all_bite"] else 0)

# ------------------------------------------------------------------ main
if __name__ == "__main__":
    if NATCHK or SCOREMODE:
        mod = load_654()
        EXT = os.path.abspath(os.path.join(CFG, "..", "..", "_external_data"))
        if NATCHK:
            assert git_blob(K5_JSON) == K_BLOB[K5_JSON]
            F = json.load(open(glob.glob(os.path.join(EXT, "cfg636_work", "C1", "cfg636_hcb_RES_*.json"))[0]))
            S = json.load(open(glob.glob(os.path.join(EXT, "cfg596_work", "P0", "cfg596_*.json"))[0])); INP = "native"; suf = "native_check"
        else:
            assert len(JOBS) in (0, 2), "--score needs two job names (framework, control), e.g. NC1x NCS0"
            jobF, jobS = JOBS if JOBS else ("NC1x", "NCS0")
            W = os.path.join(EXT, "cfg654_work"); fF = glob.glob(os.path.join(W, jobF, "cfg654*_cfg650_*_RES_*.json")); fS = glob.glob(os.path.join(W, jobS, "cfg654*_cfg650_*_S0_*.json"))
            if not fF or not fS: P(f"runs not present ({jobF}: {len(fF)}, {jobS}: {len(fS)}) -> nothing scored"); sys.exit(2)
            F, S = json.load(open(fF[0])), json.load(open(fS[0])); INP = F.get("cfg654_inputs")
            assert INP in ("native", "native_cmb") and S.get("cfg654_inputs") == INP, "both runs must carry the SAME native input set"
            suf = jobF + ("_MUTATE" if MUT else "")
        G = mod.load_lib(INP); ST = np.load(os.path.join(os.path.dirname(SRC654), "cfg654_scorer_tables_cmb.npz" if INP == "native_cmb" else "cfg654_scorer_tables.npz"))
        nv = dict(mod=mod, Om=float(ST["Om"]), Or=float(ST["Or"]), OL=float(ST["OL"]), h=float(ST["h"])); assert G["Om"] == nv["Om"]
        foot = F.get("foot", "canonical") if not NATCHK else "canonical"; N, L = int(F["np"]), float(F["L"])
        run, held = mod.build(F, S, N, L, foot, f"L{L:g}_N{N}_{foot}")
        runs = [dict(foot=foot, label=run["name"], run=run, held=held, Binj=binj_native(EXT, foot))]
        E = Engine(G, Proj(G, native=nv), "LOC", report_bg=("DESI",))
        R = dict(lane="CFG909", mode="native_check" if NATCHK else "score", inputs=INP, native_Om=nv["Om"], criteria="FROZEN_CRITERIA.md",
                 sources={os.path.relpath(k, CFG): v for k, v in BLOB.items()})
        P(f"CFG909 {'K5 native-path check on CFG636 C1 vs CFG596 P0 (stored, scorer only; no verdict)' if NATCHK else f'rescoring {suf} (CFG654 native scorer)'}; inputs {INP}, native Omega_m {nv['Om']:.6f}")
        P(HDR)
        if NATCHK:
            ref = json.load(open(K5_JSON))["runs"]["CFG636_C1"]["native_all"]; R["K5"] = {}; ok_all = True
            M = E.mats(runs[0])
            for sn, Sv in E.SURV.items():
                kp = E.keep(Sv, runs[0], M); D = E.subset(Sv, kp); o = E.score(Sv, D, M, "pub")
                st = ref[sn]; pairs = [("dchi2", o["dchi2"], st["dchi2"]), ("dchi2_noIA", o["cfg"]["noIA"]["dchi2"], st["dchi2_noIA"]),
                                       ("chi2_S0", o["cfg"]["main"]["chi2_S0"], st["chi2_S0"]), ("chi2_F", o["cfg"]["main"]["chi2_F"], st["chi2_F"])]
                pairs += [(f"robust.{k}", o["cfg"][k if k != "DESI" else "DESI_reported"]["dchi2"], st["robust"][k]) for k in ("widen2", "noIA", "held", "DESI", "LOC")]
                md = max(abs(a - b) for _, a, b in pairs); ok = md <= TOL_K1 and o["N"] == st["N"]; ok_all = ok_all and ok
                P(line("AS_SCORED native", foot, sn, o)); P(f"    K5 {sn}: {'PASS' if ok else 'FAIL'} (max |diff| {md:.2e}; N {o['N']} vs {st['N']})")
                Mo = E.mats(runs[0], nv["Om"]); o2 = E.score(Sv, D, Mo, "pub"); E.proj.restore()
                ok2, md2 = same_numbers(o2, o, rb="LOC"); ok_all = ok_all and ok2
                P(f"    K5 override at native Omega_m: {'PASS' if ok2 else 'FAIL'} ({md2:.2e})")
                Mx = E.mats(runs[0], OM_CFG886); o3 = E.score(Sv, D, Mx, "pub"); E.proj.restore()
                P(line(f"OM_{OM_CFG886} (exercise)", foot, sn, o3) + "  [engineering exercise of the native override, not frozen, no verdict]")
                R["K5"][sn] = dict(as_scored=o, pass_=ok, max_abs_diff=md, override_pass=ok2, override_max_abs_diff=md2, exercise_OM_2976=o3)
            R["K5_pass"] = ok_all; P(f"K5 overall: {'PASS' if ok_all else 'FAIL'}"); save(R, suf); sys.exit(0)
        if MUT: run_mutate(E, runs, R, suf)
        prod = os.path.join(os.path.dirname(SRC654), f"cfg654_native_results_{jobF}.json"); prodm = os.path.join(os.path.dirname(SRC654), f"cfg654_native_results_{jobF}_MUTATE.json")
        k1fun = None
        if os.path.exists(prod):
            PR = json.load(open(prod)); PM_ = json.load(open(prodm)) if os.path.exists(prodm) else None
            def k1fun(rr, sn, o):
                st = PR["surveys"][sn]; pairs = [("dchi2", o["dchi2"], st["dchi2"]), ("chi2_S0", o["cfg"]["main"]["chi2_S0"], st["chi2_S0"]), ("chi2_F", o["cfg"]["main"]["chi2_F"], st["chi2_F"]),
                                                 ("DESI_reported", o["cfg"]["DESI_reported"]["dchi2"], st["DESI_reported"])]
                pairs += [(f"robust.{k}", o["robust"][k], st["robust"][k]) for k in ("widen2", "noIA", "held", "LOC")]
                if PM_ is not None and "T_OWN_chi2" in PM_["surveys"].get(sn, {}): pairs.append(("T_OWN_chi2", o["T_OWN_chi2"], PM_["surveys"][sn]["T_OWN_chi2"]))
                bad = [f"{n} {a!r} vs {b!r}" for n, a, b in pairs if abs(a - b) > TOL_K1] + ([] if o["class"] == st["class"] else [f"class {o['class']} vs {st['class']}"])
                return (not bad), bad, max(abs(a - b) for _, a, b in pairs)
        grid = sorted(set(OM_GRID_EXTRA + [0.3137721026737606, nv["Om"]]))
        R["grid"] = grid; run_grid(E, runs, R, suf, nv["Om"], grid, k1fun=k1fun, native=True)
    else:
        G, runs = load_T()
        for f in (K1_JSON, K1_MUT_JSON): assert git_blob(f) == K_BLOB[f], f"K1 target changed: {f}"
        E = Engine(G, Proj(G), "DESI")
        Om_as = G["Om"]; grid = sorted(set(OM_GRID_EXTRA + [Om_as]))
        suf = "T" + ("_MUTATE" if MUT else "") + ("_K1" if K1ONLY else "")
        R = dict(lane="CFG909", mode="T (T1x canonical / T2x alt vs CFG596 P0)", criteria="FROZEN_CRITERIA.md", Om_as_scored=Om_as, grid=grid,
                 sources={os.path.relpath(k, CFG): v for k, v in BLOB.items() if k != SRC654}, k1_targets={os.path.relpath(k, CFG): v for k, v in K_BLOB.items() if k != K5_JSON})
        P(f"CFG909: LCDM-input sensitivity of the CFG650 shear score (T1x canonical, T2x alt vs CFG596 P0; existing outputs, no simulation)" + (" [MUTATE]" if MUT else "") + (" [K1 only]" if K1ONLY else ""))
        P(HDR)
        P(f"as-scored projection Omega_m {Om_as!r}; grid {grid}")
        if MUT: run_mutate(E, runs, R, suf)
        REF = json.load(open(K1_JSON)); REFM = json.load(open(K1_MUT_JSON))
        k1fun = lambda rr, sn, o: k1_check_T(rr["label"], sn, o, REF, REFM)
        run_grid(E, runs, R, suf, Om_as, grid, k1fun=k1fun)
    P(f"\ndone in {time.time() - T0:.0f} s")
    save(R, suf)
