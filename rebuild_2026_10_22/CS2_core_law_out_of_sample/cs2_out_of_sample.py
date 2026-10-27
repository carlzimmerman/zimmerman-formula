#!/usr/bin/env python3
"""CS2_core_law_out_of_sample: the CS1 law log Sigma0 = A + q log(sigma/70.5), calibrated once on SPARC + MW (CS1's per-system
Burkert Sigma0), then graded with no refit on eRASS1 cells, groups, SLUGGS (record machinery), dwarfs (cap rule) and X-COP.

Frozen criteria: FROZEN_CRITERIA.md + ASSUMPTION_LEDGER.md (f8674a8eec, committed alone before this script).
GR1's namespace (SC1 + X38 + EM1 + X30 + P4 + CFG528b, read-only) runs up to its graded runs; CS1's law fit runs from its source.
kappa = 1/2 FITTED; footings never pooled; not theory closed.

    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 cs2_out_of_sample.py               -> .out, _results.json
    CS2_MUTATE=1 PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 cs2_out_of_sample.py  -> calibration sigma permuted (exit 1 = bites)
"""
import os, sys, io, csv, json, math, time, contextlib, resource, warnings
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
import numpy as np
from scipy.optimize import minimize, minimize_scalar, brentq
from scipy.stats import norm
from astropy.io import fits
warnings.filterwarnings("ignore", category=RuntimeWarning)

T0 = time.time()
MUTATE = os.environ.get("CS2_MUTATE") == "1"
TAG = "_MUTATE" if MUTATE else ""
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); REPO = os.path.dirname(REB)
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1e9 if sys.platform == "darwin" else 1e6)
checks = []
def check(k, ok, msg):
    checks.append((k, bool(ok))); P(f"{k} {'PASS' if ok else 'FAIL'}  {msg}")
FEET = ("canonical", "alt"); SREF = 70.50
P(f"CS2_core_law_out_of_sample  {'MUTATE (calibration sigma permuted)' if MUTATE else 'normal run'}  (frozen f8674a8eec; AMENDMENTS A1, A2)")
P("kappa = 1/2 FITTED; footings never pooled; route E; cold dark energy, not matter; not theory closed")

# ------------------------------------------------------------------ 0. calibration (before any other class)
CS1SRC = os.path.join(REB, "CS1_core_surface_density_atlas", "cs1_atlas.py"); TC = open(CS1SRC).read()
NL = {"np": np, "math": math, "norm": norm, "minimize": minimize, "SREF": SREF}
exec(TC[TC.index("def model(m, p, x):"):TC.index("CLASSNAME = ")], NL)
fit_law, qerr = NL["fit_law"], NL["qerr"]
ROWS = [r for r in csv.DictReader(open(os.path.join(REB, "CS1_core_surface_density_atlas", "cs1_atlas.csv")))
        if r["cls"] in ("SPARC", "MW") and r["kind"] == "two-sided"]
xc = np.log10(np.array([float(r["sigma"]) for r in ROWS]) / SREF); yc = np.array([float(r["lSigma0"]) for r in ROWS])
ec = np.array([max(0.5 * (float(r["hi"]) - float(r["lo"])), 0.005) for r in ROWS]); lr0c = np.array([float(r["lr0_kpc"]) for r in ROWS])
nsp, nmw = sum(r["cls"] == "SPARC" for r in ROWS), sum(r["cls"] == "MW" for r in ROWS)
if MUTATE:
    perm = np.random.default_rng(20261027).permutation(len(xc)); xc = xc[perm]
F1 = fit_law("M1", xc, yc, ec)
AQ, QQ, SINT = F1["p"][0], F1["p"][1], F1["s_int"]
w = 1 / (ec ** 2 + SINT ** 2); Am = np.vstack([np.ones_like(xc), xc]).T; Cov = np.linalg.inv(Am.T @ (Am * w[:, None]))
eA, eQ = float(math.sqrt(Cov[0, 0])), float(math.sqrt(Cov[1, 1]))
pr = np.polyfit(xc, lr0c, 1); R0C, R0P = float(pr[1]), float(pr[0]); r0scat = float(np.std(lr0c - np.polyval(pr, xc), ddof=2))
check("K1", nsp == 165 and nmw == 1, f"calibration points SPARC {nsp} + MW {nmw}; CS1 fit_law executed from source")
P(f"CALIBRATION (SPARC + MW only, fixed now): A = {AQ:.4f} +- {eA:.4f}, q = {QQ:.4f} +- {eQ:.4f} ({QQ / eQ:.1f} sigma), s_int {SINT:.3f}")
P(f"  -> Sigma(70.5 km/s) = {10 ** AQ:.1f} Msun/pc^2; native r0 law (reported variant): log r0[kpc] = {R0C:.3f} + {R0P:.3f} log(sigma/70.5), scatter {r0scat:.3f} dex")
RES = dict(frozen="f8674a8eec", mutate=MUTATE, calibration=dict(A=AQ, eA=eA, q=QQ, eq=eQ, s_int=SINT, n=len(xc), r0_law=dict(c=R0C, p=R0P, scatter=r0scat)),
           footings={f: {} for f in FEET}, checks={})
if MUTATE:
    bites = abs(QQ / eQ) < 2
    P(f"MUTATE: permuted-sigma q = {QQ:.3f} ({QQ / eQ:.1f} sigma) -> {'tooth BITES (trend vanishes)' if bites else 'ALARM: trend survives'}")
    RES["mutate_bites"] = bool(bites)

# ------------------------------------------------------------------ GR1 namespace (read-only, up to its graded runs)
GR1SRC = os.path.join(REB, "GR1_core_law_groups_ellipticals", "gr1_groups_ellipticals.py"); TG = open(GR1SRC).read()
code = TG[:TG.index("# ------------------------------------------------------------------ graded runs")]
old = 'repr(os.path.join(HERE, f"gr1_x30_machinery{TAG}.log"))'; assert code.count(old) == 1
code = code.replace(old, f"repr({os.path.join(HERE, 'cs2_x30_machinery' + TAG + '.log')!r})")
NR = {"__file__": GR1SRC, "__name__": "gr1_ro"}; argv0 = sys.argv; sys.argv = [GR1SRC]
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(code, GR1SRC, "exec"), NR)
sys.argv = argv0
NS = NR["NS"]; grade, SIG, HK = NS["grade"], NS["SIG"], NS["HK"]
GE, MSUNE = NS["GE"], NS["MSUNE"]; SPC = MSUNE / 3.0857e16 ** 2; KPCM = 3.0857e19
check("K0b", all(v for _, v in NR["checks"]), "GR1's own K0 checks inside this run: " + ", ".join(f"{k} {'PASS' if v else 'FAIL'}" for k, v in NR["checks"]))
P(f"  GR1 namespace ready [{time.time() - T0:.0f} s, RSS {rss():.2f} GB]")
OS1J = json.load(open(os.path.join(REB, "OS1_core_law_out_of_sample", "os1_out_of_sample_results.json")))
GR1J = json.load(open(os.path.join(REB, "GR1_core_law_groups_ellipticals", "gr1_groups_ellipticals_results.json")))
QF = {f: float(OS1J["footings"][f]["q_f"]) for f in FEET}
SREFM = float(NR["SREF"])                                            # AMENDMENT A2: SC1's run-time pivot, used by the record machinery
LAWS = {f: {"OS1": (math.log10(SIG[f] / SPC), QF[f], SREFM), "CS2": (AQ, QQ, SREF)} for f in FEET}
SIG0 = dict(NR["SIG"]); SOLVE0 = NR["solve_r0"]; SOLVE0S = NS["solve_r0"]

def amp_machine(A, q, piv):
    """Sigma amplitude to pass to the machinery, which divides by SREFM: Sigma_i = 10^A (sigma_i/piv)^q exactly (A2)."""
    return 10 ** A * SPC * (SREFM / piv) ** q
def native_solver(foot, A, q, piv):
    """r0 from the native law; sigma recovered exactly from the Sigma the machinery passes in."""
    def f(Mtot, Rout, Sig):
        s = SREFM * (Sig / amp_machine(A, q, piv)) ** (1 / q); return 10 ** (R0C + R0P * math.log10(s / SREF)) * KPCM
    return f
def set_law(foot, A, q, piv, native=False):
    NR["SIG"] = {f: amp_machine(A, q, piv) for f in FEET}
    NR["solve_r0"] = native_solver(foot, A, q, piv) if native else SOLVE0; NS["solve_r0"] = native_solver(foot, A, q, piv) if native else SOLVE0S
def reset():
    NR["SIG"] = SIG0; NR["solve_r0"] = SOLVE0; NS["solve_r0"] = SOLVE0S

# ------------------------------------------------------------------ dwarfs (OS1 / CD1 cap rule, per-dwarf Sigma)
G_, MSUN_, PC_ = 6.674e-11, 1.989e30, 3.0857e16; CAP = 0.254484
X1 = list(csv.DictReader(open(os.path.join(REB, "X1_hosted_recount", "x1_per_system.csv"))))
A0_OS1 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}                 # AMENDMENT A1: OS1's literal a0, used for the OS1 comparator only
def dwarfs(foot, A, q, piv, os1_literal=False):
    out = []
    for r in [r for r in X1 if r["footing"] == foot]:
        r12 = 4 / 3 * float(r["rh_pc"]) * PC_; gN = G_ * (10 ** float(r["logMstar"]) * MSUN_ / 2) / r12 ** 2
        D, sd = float(r["Delta[Newton]"]), float(r["sdMC[Newton]"]); gobs = gN * 10 ** D
        sig = math.sqrt(gobs * r12 / 3) / 1e3
        cap = (CAP * A0_OS1[foot] if os1_literal else CAP * 2 * math.pi * GE * 10 ** A * SPC) * (sig / piv) ** q
        if D <= 0: out.append(dict(S=0.0, z=-np.inf, graded=True)); continue
        ratio = 10 ** D - 1
        if ratio < 0.1: out.append(dict(graded=False)); continue
        gh = gobs - gN; sdh = sd * 10 ** D / ratio
        out.append(dict(S=gh / cap, z=(math.log10(gh) - math.log10(cap)) / sdh, graded=True))
    g = [o for o in out if o["graded"]]
    fex = float(np.mean([o["z"] >= 2 for o in g])); medS = float(np.median([o["S"] for o in g]))
    return dict(cls="EXCLUDE" if fex >= 0.25 else ("CONSISTENT" if fex < 0.05 and medS <= 1 else "PARTIAL"), frac=fex, medS=medS)

# ------------------------------------------------------------------ X-COP (matched-clumping profiles)
DATA = os.path.join(REPO, "real_research", "data"); Gm, MSm, PCm = 6.674e-11, 1.989e30, 3.0857e16
def li(r, m, t):
    if t < r[0] or t > r[-1]: return np.nan
    return float(10 ** np.interp(np.log10(t), np.log10(r), np.log10(m)))
def Bk(x):
    x = np.asarray(x, float); return np.log1p(x * x) + 2 * np.log1p(x) - 2 * np.arctan(x)
XC = []; k2 = []
for name in sorted(os.listdir(os.path.join(DATA, "xcop"))):
    p_ = os.path.join(DATA, "xcop", name)
    if not (os.path.isdir(p_) and os.path.exists(os.path.join(p_, f"{name}_mstar.fits"))): continue
    with fits.open(os.path.join(p_, f"{name}_hydro_mass.fits")) as h: hm = h[1].data.copy(); r500 = h[1].header["R500"]
    with fits.open(os.path.join(p_, f"{name}_fgas_profile.fits")) as h: gas = h[1].data.copy(); rg500 = h[1].header["R500"]
    with fits.open(os.path.join(p_, f"{name}_mstar.fits")) as h: st = h[2].data.copy()
    rows = []
    for x in (0.1, 0.2, 0.3, 0.5, 0.7, 1.0):
        r = x * r500; mh = li(hm["RADIUS"], hm["M_FORW"], r); mg = li(gas["RADIUS"] * rg500, gas["MGAS"], r); ms = li(st["RADIUS"], st["MSTAR"], r)
        if np.all(np.isfinite([mh, mg, ms])):
            rows.append((x, r, mh, mg + ms)); k2.append((name, x, Gm * mh * MSm / (r * 1000 * PCm) ** 2))
    m500 = li(hm["RADIUS"], hm["M_FORW"], r500)
    XC.append(dict(name=name, rows=rows, sig=math.sqrt(Gm * m500 * MSm / (r500 * 1000 * PCm)) / 1e3 / math.sqrt(2)))
tg = [r for r in csv.DictReader(open(os.path.join(REPO, "reviews", "matched_clumping_2026_10_24", "run", "targets.csv"))) if r["kind"] == "cluster"]
dk = max(abs(go / float([t for t in tg if t["name"] == n and abs(float(t["xradius"]) - x) < 1e-9][0]["gobs"]) - 1) for n, x, go in k2)
check("K2", len(k2) == len(tg) and dk < 1e-6, f"X-COP {len(k2)} rows vs matched-clumping {len(tg)}; max rel {dk:.1e}")
def xcop(A, q, piv, native=False):
    d = []; sat = 0
    for c in XC:
        S = 10 ** A * (c["sig"] / piv) ** q                                   # Msun/pc^2
        x1 = [r for r in c["rows"] if abs(r[0] - 1.0) < 1e-9][0]; R5 = x1[1] * 1e3; Mc5 = x1[2] - x1[3]   # pc, Msun
        if native:
            r0 = 10 ** (R0C + R0P * math.log10(c["sig"] / SREF)) * 1e3
        else:
            lm = lambda lr: math.log(S * math.exp(2 * lr) * math.pi * float(Bk(R5 / math.exp(lr))))
            pk = minimize_scalar(lambda lr: -lm(lr), bounds=(math.log(R5 * 1e-6), math.log(R5 * 1e3)), method="bounded", options={"xatol": 1e-10})
            if lm(float(pk.x)) < math.log(Mc5): r0 = math.exp(float(pk.x)); sat += 1
            else: r0 = math.exp(brentq(lambda lr: lm(lr) - math.log(Mc5), math.log(R5 * 1e-7), float(pk.x), xtol=1e-14))
        for x, r, mh, mb in c["rows"]:
            if x > 0.75: continue
            mc = math.pi * S * r0 ** 2 * float(Bk(r * 1e3 / r0)); d.append(math.log10(mh / (mb + mc)))
    d = np.array(d); return dict(mean=float(d.mean()), rms=float(np.sqrt(np.mean(d ** 2))), n=len(d), saturated=sat)

# ------------------------------------------------------------------ graders per law
def run_all(foot, A, q, piv, native=False, classes=("erass", "groups", "sluggs", "dwarfs", "xcop"), os1=False):
    out = {}
    set_law(foot, A, q, piv, native)
    try:
        if "erass" in classes:
            cells, ok = grade(foot, q, amp_machine(A, q, piv) / SIG[foot]); fails = [k for k in ok if not ok[k]]
            out["erass"] = dict(cells=cells, ok=ok, fails=fails, maxZ={k: max(abs(cells[h][k]["Z"]) for h in HK) for k in ok})
        if "groups" in classes: out["groups"] = NR["grade_groups"](foot, q)
        if "sluggs" in classes: out["sluggs"] = NR["sluggs"](foot, q)
    finally:
        reset()
    if "dwarfs" in classes: out["dwarfs"] = dwarfs(foot, A, q, piv, os1_literal=os1)
    if "xcop" in classes: out["xcop"] = xcop(A, q, piv, native)
    return out
def classify(c, o):
    e, eo = c["erass"], o["erass"]; cl = {}
    sZo = sum(e["maxZ"][k] for k in eo["fails"])
    cl["erass"] = "PASS" if not e["fails"] else ("IMPROVES ON OS1" if not [k for k in e["fails"] if k not in eo["fails"]] and sZo <= 0.5 * sum(eo["maxZ"][k] for k in eo["fails"]) else "FAILS")
    g, go = c["groups"], o["groups"]
    cl["groups"] = "PASS" if g["verdict"] == "CONSISTENT" else ("IMPROVES ON OS1" if abs(g["mean"]) <= abs(go["mean"]) - 0.020 else "FAILS")
    s, so = c["sluggs"], o["sluggs"]
    cl["sluggs"] = "PASS" if s["closes"] else ("IMPROVES ON OS1" if np.isfinite(s["mean"]) and abs(s["mean"]) <= 0.5 * abs(so["mean"]) and s["n_reversed"] == 0 else "FAILS")
    d, do = c["dwarfs"], o["dwarfs"]
    cl["dwarfs"] = "PASS" if d["cls"] == "CONSISTENT" else ("IMPROVES ON OS1" if d["frac"] <= 0.5 * do["frac"] else "FAILS")
    x, xo = c["xcop"], o["xcop"]
    cl["xcop"] = "PASS" if abs(x["mean"]) <= 0.05 and x["rms"] <= 0.10 else ("IMPROVES ON OS1" if abs(x["mean"]) <= 0.5 * abs(xo["mean"]) else "FAILS")
    # better / worse
    bw = {}
    nf, nfo = len(e["fails"]), len(eo["fails"]); sz = sum(e["maxZ"][k] for k in e["fails"]); szo = sum(eo["maxZ"][k] for k in eo["fails"])
    bw["erass"] = "better" if nf < nfo or (nf == nfo and nfo > 0 and sz <= 0.8 * szo) else ("worse" if nf > nfo or (nf == nfo and nf > 0 and sz >= 1.25 * szo) else "same")
    for k, fc, fo in (("groups", abs(g["mean"]), abs(go["mean"])), ("sluggs", abs(s["mean"]), abs(so["mean"])),
                      ("dwarfs", d["frac"], do["frac"]), ("xcop", abs(x["mean"]), abs(xo["mean"]))):
        bw[k] = "better" if fc <= 0.8 * fo else ("worse" if fc >= 1.25 * fo else "same")
    nb, nw = sum(v == "better" for v in bw.values()), sum(v == "worse" for v in bw.values())
    lane = ("CS2 PREDICTS ALL" if all(v == "PASS" for v in cl.values()) else "CS2 BETTER THAN OS1" if nb >= 1 and nw == 0
            else "CS2 TRADES" if nb >= 1 else "CS2 NO BETTER")
    return cl, bw, lane
def show(tag, r):
    P(f"  [{tag}]")
    if "erass" in r:
        e = r["erass"]; P(f"    eRASS1 cells: {15 - len(e['fails'])}/15 pass; failing {', '.join(f'{k} (|Z| {e['maxZ'][k]:.2f}, h0.672 pred {e['cells']['h0672'][k]['pred']:.3f} vs meas {e['cells']['h0672'][k]['meas']:.3f})' for k in e['fails']) or 'none'}")
    if "groups" in r: g = r["groups"]; P(f"    groups: mean {g['mean']:+.4f} Z {g['Z']:+.2f} -> {g['verdict']}")
    if "sluggs" in r: s = r["sluggs"]; P(f"    SLUGGS: mean {s['mean']:+.3f}, cleared {s['n_cleared']}/4, reversed {s['n_reversed']}, closes {s['closes']}; per " + ", ".join(f"{k} {v:+.3f}" if v is not None else f"{k} n/a" for k, v in s["per"].items()))
    if "dwarfs" in r: d = r["dwarfs"]; P(f"    dwarfs: {d['cls']} (frac z>=2 {d['frac']:.3f}, median S {d['medS']:.2f})")
    if "xcop" in r: x = r["xcop"]; P(f"    X-COP: mean Delta {x['mean']:+.3f} dex, rms {x['rms']:.3f} over {x['n']} points (saturated {x['saturated']})")

classes = {}
for foot in FEET:
    P(f"\n=== [{foot}]  OS1 law: A {LAWS[foot]['OS1'][0]:.4f}, q {QF[foot]:.3f};  CS2 law: A {AQ:.4f}, q {QQ:.4f}")
    if MUTATE:
        o = run_all(foot, *LAWS[foot]["OS1"], classes=("groups", "dwarfs", "xcop"), os1=True); c = run_all(foot, AQ, QQ, SREF, classes=("groups", "dwarfs", "xcop"))
        show("OS1 law", o); show("MUTATED CS2 law (reported)", c); RES["footings"][foot] = dict(OS1=o, mutated=c); continue
    o = run_all(foot, *LAWS[foot]["OS1"], os1=True); show("OS1 law (comparator)", o)
    oc = OS1J["footings"][foot]["clusters"]["cells"]
    k0e = max(abs(o["erass"]["cells"][h][k]["pred"] - oc[h][k]["pred"]) for h in HK for k in oc[h])
    k0d = max(abs(o["dwarfs"]["frac"] - OS1J["footings"][foot]["dwarfs"]["frac"]), abs(o["dwarfs"]["medS"] - OS1J["footings"][foot]["dwarfs"]["medS"]))
    gj = GR1J["footings"][foot]
    k0g = max(abs(o["groups"]["mean"] - gj["groups"]["st"]["mean"]), abs(o["groups"]["Z"] - gj["groups"]["st"]["Z"]))
    k0s = max(abs((o["sluggs"]["per"][k] or 0) - (gj["sluggs"]["st"]["per"][k] or 0)) for k in o["sluggs"]["per"])
    check(f"K0[{foot}]", k0e < 1e-6 and k0d < 1e-9 and k0g < 1e-9 and k0s < 1e-9,
          f"OS1 law reproduces record: eRASS1 cells {k0e:.1e}, dwarfs {k0d:.1e}, groups {k0g:.1e}, SLUGGS {k0s:.1e}")
    c = run_all(foot, AQ, QQ, SREF); show("CS2 law (PRIMARY)", c)
    cl, bw, lane = classify(c, o); classes[foot] = lane
    P(f"  per class: " + "; ".join(f"{k} {cl[k]} ({bw[k]} vs OS1)" for k in cl))
    P(f"  LANE CLASS [{foot}]: {lane}   [{time.time() - T0:.0f} s, RSS {rss():.2f} GB]")
    nv = run_all(foot, AQ, QQ, SREF, native=True); show("CS2 law + native r0 law (reported, no class)", nv)
    RES["footings"][foot] = dict(OS1=o, CS2=c, classes=cl, vs_OS1=bw, lane=lane, native_r0=nv,
                                 K0=dict(erass=k0e, dwarfs=k0d, groups=k0g, sluggs=k0s))
if not MUTATE:
    RES["verdict"] = classes["canonical"] if classes["canonical"] == classes["alt"] else f"UNDECIDED (footings disagree: {classes})"
    P(f"\n=== VERDICT (both footings): {RES['verdict']}")
check("K3", rss() < 1.0, f"peak RSS {rss():.2f} GB, one thread")
n = sum(v for _, v in checks); RES["checks"] = {k: v for k, v in checks}
P(f"\nchecks {n}/{len(checks)}; runtime {time.time() - T0:.0f} s; peak RSS {rss():.2f} GB")
open(os.path.join(HERE, f"cs2_out_of_sample{TAG}.out"), "w").write("\n".join(OUT).replace(REPO, "<repo>") + "\n")
def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, (np.floating, float)): return float(o)
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, np.bool_): return bool(o)
    return o
json.dump(clean(RES), open(os.path.join(HERE, f"cs2_out_of_sample_results{TAG}.json"), "w"), indent=1, default=str)
if MUTATE: sys.exit(1 if RES["mutate_bites"] else 0)
sys.exit(0 if n == len(checks) else 1)
