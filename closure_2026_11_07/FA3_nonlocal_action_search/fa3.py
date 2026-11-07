#!/usr/bin/env python3
"""FA3 (criteria FROZEN_CRITERIA.md): three nonlocal / history candidates graded on GB1 G1-G8 + SV5 iter_1 web row W1.
    python3 fa3.py            -> fa3.json / fa3.out
    python3 fa3.py --mutate   -> fa3_MUTATE.json / fa3_MUTATE.out
I1 causal phantom memory (exp kernel, tau set by G1); I3 formation-epoch a0 memory (z_f built); I4 conserved phantom charge.
GB1 exec'd read-only up to its main block (as SE2); SV5 sv5_web imported read-only. One thread; footings never pooled.
kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math, copy
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
import numpy as np, resource
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9   # macOS bytes -> GB

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
CL = os.path.join(REPO, "closure_2026_11_06")
MUT = "--mutate" in sys.argv; TAG = "fa3_MUTATE" if MUT else "fa3"; OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))

# ------------------------------------------------------------------ GB1, read-only, up to its main block
GBP = os.path.join(CL, "GB1_all_gates_battery", "gb1.py"); src = open(GBP).read()
cut = src.index("# ------------------------------------------------------------------ main")
NS = {"__file__": GBP, "__name__": "gb1_lib"}
_a = sys.argv; sys.argv = [sys.argv[0]]; exec(compile(src[:cut], "gb1_lib", "exec"), NS); sys.argv = _a
GBJ = json.load(open(os.path.join(CL, "GB1_all_gates_battery", "gb1.json")))
A0 = NS["A0"]; G = NS["G"]; MS = NS["MS"]; glaw = NS["glaw"]; Missing = NS["Missing"]; need = NS["need"]
GATES = NS["GATES"]; run_gate = NS["run_gate"]; L0 = NS["L0"]; F2 = NS["F2"]; RZ_TAB = NS["RZ_TAB"]
gb1_filled = NS["filled"]
_i = src.index("def short(g, r):"); _j = src.index("for cn, mk in CANDS.items():")
exec(compile(src[_i:_j], "gb1_short", "exec"), NS)   # GB1's own row printer, verbatim

def filled_ext(ft, fill):
    """GB1's filled() plus FA3's history fills (mu, neff, neff_early/late, rz overrides)."""
    d = gb1_filled(ft, fill)
    if not fill: return d
    if d is ft: d = dict(ft)
    for k in ("mu", "neff"):
        if k in fill and d.get(k) is None: d[k] = fill[k]
    keys = [s["key"] for s in d.get("stars", [])]
    if "neff_early" in fill and "sig_early" in keys and d.get("neff") is None: d["neff"] = fill["neff_early"]
    if "neff_late" in fill and "sig_late" in keys and d.get("neff") is None: d["neff"] = fill["neff_late"]
    if d.get("mu") is None and "neff" in d and d["neff"] is not None and "mu" in fill: d["mu"] = fill["mu"]
    return d
NS["filled"] = filled_ext   # gates resolve filled() in NS

def battery(f, a0):
    S, E, X = NS["build"](f, a0); GRp = {0: NS["groups_pts"](a0, 0.0), 1: NS["groups_pts"](a0, 1.0)}; G5p = NS["groups_pts"](a0, 0.5)
    U = NS["udgs"](f, a0); D = NS["dsphs"](f, a0); K = NS["kids"](a0)
    st = NS["R1"][f"{f}|S4 v3 dmean L*floor E-W"]; sigU = math.hypot(st["se"], st["sigma_sys"]) / math.log(10)
    B = dict(f=f, S=S, E=E, X=X, GR=GRp, G5=G5p, U=U, D=D, K=K, sigU=sigU)
    B["rms_L0"] = float(np.sqrt(np.mean([p["D"] ** 2 for p in S]))); return B

def cmp_num(a, b, path=""):
    """max |a-b| over matching numeric leaves."""
    if isinstance(a, dict): return max([cmp_num(a[k], b[k], path + "/" + k) for k in a if k in b] + [0.0])
    if isinstance(a, (list, tuple)): return max([cmp_num(x, y) for x, y in zip(a, b)] + [0.0])
    if isinstance(a, bool) or a is None or isinstance(a, str): return 0.0
    return abs(float(a) - float(b))

RES = dict(tag=TAG, criteria="FROZEN_CRITERIA.md (FA3)", note="kappa = 1/2 FITTED; not theory closed", KA={}, cands={})
P(f"FA3 {'MUTATE' if MUT else 'MAIN'}: nonlocal / history candidates I1, I3, I4. kappa = 1/2 FITTED; not theory closed; footings never pooled.")
BATT = {}
for f, a0 in A0.items():
    B = battery(f, a0); BATT[f] = B
    cm = dict(X=np.mean([p["D"] for p in B["X"]]), E=np.mean([p["D"] for p in B["E"]]), S=np.mean([p["D"] for p in B["S"]]),
              G0=np.mean([p["D"] for g in B["GR"][0] for p in g["pts"]]), G1=np.mean([p["D"] for g in B["GR"][1] for p in g["pts"]]))
    d1 = max(abs(cm[k] - NS["KA20"][f][k]) for k in cm)
    c = L0(f, a0); dmax = 0.0
    for gname, fn, fills in GATES:
        r = run_gate(fn, c, B, a0, fills); dmax = max(dmax, cmp_num(r["num"], GBJ["cands"]["L0"][f][gname]["num"]))
    RES["KA"][f] = dict(KA1_class_means={k: float(v) for k, v in cm.items()}, KA1_maxdiff=float(d1), KA1_L0_rows_maxdiff=float(dmax),
                        ok=bool(d1 <= 1e-6 and dmax <= 1e-9))
    P(f"[{f}] KA1 L0 class means max|d| {d1:.1e} (line 1e-6); L0 G1-G8 numbers vs gb1.json max|d| {dmax:.1e} (line 1e-9) -> {'PASS' if RES['KA'][f]['ok'] else 'FAIL'}")

# ------------------------------------------------------------------ SV5 iter_1 machinery, read-only
SV5D = os.path.join(CL, "SV5_growth_mechanism"); sys.path.insert(0, SV5D)
_a = sys.argv; sys.argv = [os.path.join(SV5D, "sv5_web.py")]
import sv5_web as SV
sys.argv = _a
SV1J = json.load(open(os.path.join(SV5D, "iter_1_law_on_web", "sv5_iter1.json")))
sigA = SV.sigA; WLINE = 3 * sigA; ZG = SV.ZG; N3 = SV.N3; MC = N3["M"]
P(f"[peak RSS so far {rss():.2f} GB] SV5 machinery: sigma_A {sigA:.4f} -> W1 line |r - 1| <= {WLINE:.4f}; ZG {ZG}")

# cosmic time from the solver's background (CLASS Hubble in 1/Mpc), integrated from z 3400
MPC = SV.MPC; CC = SV.CC; GYR = 3.15576e16
lna = np.linspace(math.log(1 / 3401.0), 0.0, 20001); aa = np.exp(lna)
Hs = np.array([MC.Hubble(1 / x - 1) for x in aa]) * CC / MPC            # 1/s
integ = 1.0 / Hs; tt = np.concatenate([[0.0], np.cumsum(0.5 * (integ[1:] + integ[:-1]) * np.diff(lna))]) / GYR
def t_of_z(z): return float(np.interp(math.log(1 / (1 + z)), lna, tt))
T0 = t_of_z(0.0); TZ = [t_of_z(z) for z in ZG]
P(f"background: t0 {T0:.4f} Gyr (from z 3400); t(z) at ZG: " + ", ".join(f"{z:g}:{t:.3f}" for z, t in zip(ZG, TZ)))

def nu(y): return 0.5 + np.sqrt(0.25 + 1.0 / np.maximum(y, 1e-300))
def gfield(dk, z):
    a = 1 / (1 + z); kSI = 1.0 / MPC
    phik = -1.5 * SV.H0s ** 2 * SV.Om * dk / (a * SV.K2 * kSI ** 2); phik[0, 0, 0] = 0
    return [np.real(np.fft.ifftn(-1j * Kc * kSI * phik)) / a for Kc in (SV.KX, SV.KY, SV.KZ)]
def Wof(g, a0):
    gn = np.sqrt(g[0] ** 2 + g[1] ** 2 + g[2] ** 2); n1 = nu(gn / a0) - 1.0
    return [n1 * gc for gc in g]
def Bof(g, Weff):
    divV = 0; divN = 0
    for Kc, gc, wc in zip((SV.KX, SV.KY, SV.KZ), g, Weff):     # same sums as SV5, accumulated to keep RSS low
        divV = divV + Kc * np.fft.fftn(gc + wc); divN = divN + Kc * np.fft.fftn(gc)
    return SV.shell_mean(np.abs(divV) ** 2) / SV.shell_mean(np.abs(divN) ** 2)
def magw(W): return np.sqrt(W[0] ** 2 + W[1] ** 2 + W[2] ** 2)

WR, dV = SV.realise(5)
WEB = {}
def web_setup(f, a0):
    """store g at every ZG (float32 for past use, float64 current recomputed), mass weights."""
    WEB.clear(); import gc; gc.collect()
    gs, wts = [], []
    for z in ZG:
        dk, _ = SV.delta_k(WR, dV, z); g = gfield(dk, z)
        gs.append([x.astype(np.float32) for x in g]); wts.append(np.maximum(1 + np.real(np.fft.ifftn(dk)), 0.0).astype(np.float32))
    WEB[f] = dict(g32=gs, wts=wts)
def g_cur(z):
    dk, _ = SV.delta_k(WR, dV, z); return gfield(dk, z)

def weights_exp(j, tau):
    """kernel weight of snapshot i >= j at lensing epoch j (snapshot i held back to t(z_{i+1}); last back to t = 0)."""
    tj = TZ[j]; w = {}
    for i in range(j, len(ZG)):
        ti = TZ[i]; tprev = TZ[i + 1] if i + 1 < len(ZG) else 0.0
        w[i] = math.exp(-(tj - ti) / tau) - math.exp(-(tj - tprev) / tau)
    return w

def web_r(f, a0, coef_fn, label):
    """coef_fn(j) -> dict i -> weight on W(z_i) (i = j uses float64 current). returns r, dchi2, F_web."""
    Bz = []; Fw = {}
    for j, z in enumerate(ZG):
        g = g_cur(z); Wl = Wof(g, a0); cf = coef_fn(j); Weff = [np.zeros_like(x) for x in g]
        for i, w in cf.items():
            if w == 0.0: continue
            Wi = Wl if i == j else Wof([x.astype(np.float64) for x in WEB[f]["g32"][i]], a0)
            for k in range(3): Weff[k] += w * Wi[k]
        Bz.append(Bof(g, Weff)); wt = WEB[f]["wts"][j].astype(np.float64)
        Fw[str(z)] = float((wt * magw(Weff)).sum() / (wt * magw(Wl)).sum())
    pr = SV.project(Bz)
    return dict(label=label, r=pr["r"], dchi2=pr["dchi2"], W1_pass=bool(abs(pr["r"] - 1) <= WLINE), F_web_by_z=Fw, F_web_max=max(Fw.values()))

# ------------------------------------------------------------------ KA2 / K1 + theorem inputs
for f, a0 in A0.items():
    web_setup(f, a0)
    law = web_r(f, a0, lambda j: {j: 1.0}, "law on (KA2)")
    rj = SV1J["foot"][f]["proj"]["r"]; d2 = abs(law["r"] / rj - 1)
    k1 = web_r(f, a0, lambda j: weights_exp(j, 1e-12 * T0), "tau -> 0 (K1)"); dk1 = abs(k1["r"] / rj - 1)
    RES["KA"][f].update(KA2=dict(r=law["r"], sv5_json=rj, reldiff=d2, ok=bool(d2 <= 1e-6)), K1=dict(r=k1["r"], reldiff=dk1, ok=bool(dk1 <= 1e-6)))
    RES["KA"][f]["ok"] = bool(RES["KA"][f]["ok"] and d2 <= 1e-6 and dk1 <= 1e-6)
    P(f"[{f}] KA2 law-on web r {law['r']:.6f} vs SV5 json {rj:.6f}: rel {d2:.1e} -> {'PASS' if d2 <= 1e-6 else 'FAIL'}; K1 tau->0 r {k1['r']:.6f} rel {dk1:.1e} -> {'PASS' if dk1 <= 1e-6 else 'FAIL'}")
    # theorem input (a): past |W| >= present |W|, cosine
    mono = []
    for i in range(len(ZG) - 1):
        Wa = Wof([x.astype(np.float64) for x in WEB[f]["g32"][i]], a0); Wb = Wof([x.astype(np.float64) for x in WEB[f]["g32"][i + 1]], a0)
        ma, mb = magw(Wa), magw(Wb); wt = WEB[f]["wts"][i].astype(np.float64)
        cos = (Wa[0] * Wb[0] + Wa[1] * Wb[1] + Wa[2] * Wb[2]) / np.maximum(ma * mb, 1e-300)
        mono.append(dict(z_later=ZG[i], z_earlier=ZG[i + 1], frac_earlier_not_smaller=float((wt * (mb >= ma)).sum() / wt.sum()),
                         min_ratio=float(np.min(mb / np.maximum(ma, 1e-300))), mean_cos=float((wt * cos).sum() / wt.sum()),
                         median_ratio=float(np.median(mb / np.maximum(ma, 1e-300)))))
        del Wa, Wb, cos, ma, mb
    kx = [p["x"] for p in BATT[f]["K"][0] + BATT[f]["K"][1]]; kw = [float((nu(x) - 1) * x) for x in kx]
    RES["KA"][f]["theorem_inputs"] = dict(web_monotone=mono, kids_W_over_a0=dict(min=min(kw), max=max(kw), all=kw),
                                         holds=bool(all(m["frac_earlier_not_smaller"] >= 0.99 and m["mean_cos"] >= 0.99 for m in mono)))
    P(f"[{f}] theorem (a): earlier snapshot |W| not smaller, mass fraction min {min(m['frac_earlier_not_smaller'] for m in mono):.4f}; mean cos min {min(m['mean_cos'] for m in mono):.5f}; "
      f"median past/present ratio per step {', '.join(f'{m['median_ratio']:.3f}' for m in mono)} -> holds {RES['KA'][f]['theorem_inputs']['holds']}")
    P(f"[{f}] peak RSS so far {rss():.2f} GB"); P(f"[{f}] theorem (b): KiDS K1 lens |W|/a0 {min(kw):.3f}-{max(kw):.3f} -> kernel-free floor S_web >= {min(kw):.3f} x S_host")
KAOK = all(RES["KA"][f]["ok"] for f in A0); RES["KA_all"] = KAOK
if not KAOK:
    P("KA FAIL: stop; nothing graded."); json.dump(RES, open(os.path.join(HERE, TAG + ".json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n"); sys.exit(2)

def label_of(rows_by_f, web_by_f):
    st = {f: {g: rows_by_f[f][g]["status"] for g in rows_by_f[f]} for f in A0}
    for f in A0: st[f]["W1 web"] = "PASS" if web_by_f[f]["W1_pass"] else "FAIL"
    fails = sorted({g for f in A0 for g, s in st[f].items() if s == "FAIL"}); nvs = sorted({g for f in A0 for g, s in st[f].items() if s == "NO VERDICT"})
    if not fails and not nvs: return "SURVIVES (still owes field equations, causality, well-posedness)", st
    if fails: return f"FAIL ({', '.join(x.split()[0] for x in fails)})" + (f"; NO VERDICT ({', '.join(x.split()[0] for x in nvs)})" if nvs else ""), st
    return f"NO VERDICT ({', '.join(x.split()[0] for x in nvs)})", st
def short(r):
    if r["num"] is None: return f"NO VERDICT (needs {r['missing']}; bracket {r['bracket']['reading']})"
    return NS["short"]("G", r) if False else json.dumps({k: (round(v, 4) if isinstance(v, float) else v) for k, v in r["num"].items() if not isinstance(v, (dict, list))})
def grade_rows(cand_mk, fills_override=None, ss_fill=None):
    rows = {}
    for f, a0 in A0.items():
        c = cand_mk(f, a0); B = BATT[f]; row = {}
        for gname, fn, fills in GATES:
            fl = fills_override.get(gname, fills) if fills_override else fills
            if gname.startswith("G8") and ss_fill is not None:
                ok, num = fn(c, B, a0, ss_fill(f)); r = dict(status="PASS" if ok else "FAIL", num=num, missing=None, bracket=None, fill=ss_fill(f))
            else:
                r = run_gate(fn, c, B, a0, fl)
            row[gname] = r; P(f"   [{f}] {gname:17s} {r['status']:10s} {NS['short'](gname, r)}")
        rows[f] = row
    return rows

# ================================================================== I1 causal phantom memory
P("\n== I1: causal memory of the phantom (exponential kernel; tau set by G1 SPARC) ==")
def I1_mk(tau_t0):
    S = -math.expm1(-1.0 / tau_t0) if tau_t0 > 0 else 1.0
    return (lambda f, a0: (lambda ft: dict(b=1.0, F=S, T=0.0))), S
I1 = dict(foot={})
if not MUT:
    for f, a0 in A0.items():
        B = BATT[f]
        def g1ok(lt):
            mk, S = I1_mk(10 ** lt); ok, num = NS["g_sparc"](mk(f, a0)(None) if False else mk(f, a0), B, a0); return ok, num, S
        lo, hi = -3.0, 3.0
        assert g1ok(lo)[0], "G1 fails at the smallest tau"
        if g1ok(hi)[0]: ltau = hi
        else:
            while hi - lo > 1e-3:
                mid = 0.5 * (lo + hi)
                if g1ok(mid)[0]: lo = mid
                else: hi = mid
            ltau = lo
        tau = 10 ** ltau; ok, num, S = g1ok(ltau)
        P(f"[{f}] tau_gal = {tau:.4g} t0 = {tau*T0:.4g} Gyr (largest tau with G1 PASS); S_host = {S:.5f}; G1 Z {num['Z']:+.4f} rms {num['rms']:.4f} (line {num['rms_line']:.4f})")
        I1["foot"][f] = dict(tau_gal_t0=tau, tau_gal_Gyr=tau * T0, S_host=S, G1_at_tau=num)
    rows = grade_rows(lambda f, a0: I1_mk(I1["foot"][f]["tau_gal_t0"])[0](f, a0))
    web = {}
    for f, a0 in A0.items():
        web_setup(f, a0); tau = I1["foot"][f]["tau_gal_t0"] * T0
        web[f] = web_r(f, a0, lambda j, tau=tau: weights_exp(j, tau), f"tau_gal {tau:.3g} Gyr")
        P(f"   [{f}] W1 web at tau_gal: r {web[f]['r']:.4f} (|r-1| line {WLINE:.4f}) -> {'PASS' if web[f]['W1_pass'] else 'FAIL'}; F_web max {web[f]['F_web_max']:.4f} (line 0.005)")
        rep = []
        for tt0 in (0.01, 0.1, 1.0, 10.0, 100.0):
            wr = web_r(f, a0, lambda j, tau=tt0 * T0: weights_exp(j, tau), f"tau {tt0} t0")
            mk, S = I1_mk(tt0); ok, num = NS["g_sparc"](mk(f, a0), BATT[f], a0)
            rep.append(dict(tau_t0=tt0, S_host=S, r=wr["r"], F_web_max=wr["F_web_max"], W1_pass=wr["W1_pass"], G1_pass=bool(ok), G1_Z=num["Z"]))
            P(f"   [{f}] reported tau {tt0:g} t0: S_host {S:.4f}, G1 {'PASS' if ok else 'FAIL'} (Z {num['Z']:+.3f}); web r {wr['r']:.4g}, F_web max {wr['F_web_max']:.4f}")
        I1["foot"][f]["reported_scan"] = rep
    P(f"peak RSS so far {rss():.2f} GB"); lab, st = label_of(rows, web); I1.update(rows=rows, web=web, label=lab, status=st); P(f"LABEL I1: {lab}")
else:
    m1 = {}
    for f, a0 in A0.items():
        web_setup(f, a0); tau = 10 * T0
        def cf(j, tau=tau):
            tj = TZ[j]; s = np.linspace(0, tj, 20001); k = np.exp(-s / tau) / tau * ((tj - s) / tj) ** 4
            return {j: float(np.trapz(k, s))}
        wr = web_r(f, a0, cf, "M1 planted growing source, tau 10 t0"); m1[f] = wr
        P(f"[{f}] I1 M1 planted growing web source, tau 10 t0: r {wr['r']:.4f} -> W1 {'PASS' if wr['W1_pass'] else 'FAIL'} (must PASS)")
    ok2 = {}
    for f, a0 in A0.items():
        ok, num = NS["g_sparc"](lambda ft: dict(b=1.0, F=0.0, T=0.0), BATT[f], a0); ok2[f] = dict(G1_pass=bool(ok), Z=num["Z"])
        P(f"[{f}] I1 M2 Newton: G1 {'PASS' if ok else 'FAIL'} (Z {num['Z']:+.4f}) (must FAIL)")
    I1.update(M1=m1, M2=ok2, bites=bool(all(m1[f]["W1_pass"] for f in A0) and all(not ok2[f]["G1_pass"] for f in A0)))
    P(f"I1 MUTATE: {'BITES' if I1['bites'] else 'NO BITE'}")
RES["cands"]["I1"] = I1

# ================================================================== I3 formation-epoch a0 memory, z_f built
P("\n== I3: formation-epoch a0 memory, z_f from top-hat collapse density ==")
H0s = SV.H0s; OM = SV.Om; RHOC = 3 * H0s ** 2 / (8 * math.pi * G)
P(f"background: Omega_m {OM:.5f}, H0 {SV.H0:.4f}, rho_m0 {OM*RHOC:.4e} kg/m^3")
def zf_of(ft, disp, dc):
    v = ft["v"] * 1e3; r = ft["r"]
    v2 = 3 * (ft["sigma"] * 1e3) ** 2 if disp else v * v
    rho = 3 * (v2 * r / G) / (4 * math.pi * r ** 3); q = rho / (dc * OM * RHOC)
    return max(q ** (1 / 3) - 1, 0.0)
def rz_tab(z): zz, rv = zip(*RZ_TAB); return float(np.interp(z, zz, rv))
def attach_rz(B, dc, rzfun):
    B3 = dict(B); zfs = {}
    def tag(pts, disp, cls):
        out = []
        for p in pts:
            q = dict(p); ft = dict(p["feat"]); z = zf_of(ft, disp, dc); ft["rz"] = rzfun(z); q["feat"] = ft; out.append(q); zfs.setdefault(cls, []).append(z)
        return out
    B3["S"] = tag(B["S"], False, "SPARC"); B3["E"] = tag(B["E"], False, "ellipticals"); B3["X"] = tag(B["X"], False, "X-COP")
    B3["GR"] = {k: [dict(g, pts=tag(g["pts"], False, f"groups f*{k}")) for g in v] for k, v in B["GR"].items()}
    B3["U"] = tag(B["U"], True, "Coma UDGs"); B3["D"] = {k: tag(v, True, f"dSph {k}") for k, v in B["D"].items()}
    def tagk(fts, cls):
        out = []
        for ft in fts:
            d = dict(ft); z = zf_of(d, False, dc); d["rz"] = rzfun(z); out.append(d); zfs.setdefault(cls, []).append(z)
        return out
    B3["K"] = (tagk(B["K"][0], "KiDS early"), tagk(B["K"][1], "KiDS late"))
    return B3, {k: dict(median=float(np.median(v)), min=float(np.min(v)), max=float(np.max(v))) for k, v in zfs.items()}
def ss_zf(f, a0, dc):
    zs = []
    for r in list(NS["PLAN"].values()) + [NS["R_CASSINI"]]:
        ft = NS["ss_feat"](a0, r); zs.append(zf_of(ft, False, dc))
    return zs
I3 = dict(foot={})
rzmain = (lambda z: (1 + z) ** 2) if MUT else rz_tab
def run_I3(dc, rzf, tag_):
    rows = {}; info = {}
    for f, a0 in A0.items():
        B3, zinfo = attach_rz(BATT[f], dc, rzf); zss = ss_zf(f, a0, dc); c = F2(f, a0); row = {}
        for gname, fn, fills in GATES:
            if gname.startswith("G8"):
                assert min(zss) > 2.33 or MUT
                ok, num = fn(c, B3, a0, {"rz": rzf(min(zss))}); r = dict(status="PASS" if ok else "FAIL", num=num, missing=None, bracket=None)
            else:
                r = run_gate(fn, c, B3, a0, fills)
            row[gname] = r; P(f"   [{f}] {tag_} {gname:17s} {r['status']:10s} {NS['short'](gname, r)}")
        rows[f] = row; info[f] = dict(zf=zinfo, zf_solar_min=min(zss))
        P(f"   [{f}] z_f medians: " + ", ".join(f"{k} {v['median']:.2f}" for k, v in zinfo.items()))
    return rows, info
rows, info = run_I3(18 * math.pi ** 2, rzmain, "D18pi2")
web = {f: dict(r=RES["KA"][f]["KA2"]["r"], W1_pass=bool(abs(RES["KA"][f]["KA2"]["r"] - 1) <= WLINE), note="web not assembled: today's a0 (KA2 value)") for f in A0}
lab, st = label_of(rows, web); I3.update(rows=rows, zf=info, web=web, label=lab, status=st); P(f"LABEL I3{' (MUTATE planted r_z=(1+z_f)^2)' if MUT else ''}: {lab}")
if not MUT:
    rep = {}
    for nm, dc, rzf in (("turnaround 5.55", 5.55, rz_tab), ("envelope 1.21", 18 * math.pi ** 2, lambda z: 1.21), ("native max 1.12", 18 * math.pi ** 2, lambda z: 1.12)):
        P(f"  reported bracket: {nm}")
        r2, i2 = run_I3(dc, rzf, nm[:8]); rep[nm] = dict(rows={f: {g: dict(status=v["status"], num=v["num"]) for g, v in r2[f].items()} for f in A0}, zf=i2)
    I3["reported_brackets"] = rep
    # largest shift from L0 anywhere (deep-MOND bound 0.5 log10 1.21)
    I3["max_shift_bound_dex"] = 0.5 * math.log10(1.21)
else:
    sh = {}
    for f in A0:
        sh[f] = rows[f]["G2 X-COP"]["num"]["mean"] - GBJ["cands"]["L0"][f]["G2 X-COP"]["num"]["mean"]
    I3["M1_xcop_shift"] = sh; I3["bites"] = bool(all(abs(v) >= 0.1 for v in sh.values()))
    P(f"I3 M1 X-COP mean shift vs L0: " + ", ".join(f"{f} {v:+.3f}" for f, v in sh.items()) + f" -> {'BITES' if I3['bites'] else 'NO BITE'}")
RES["cands"]["I3"] = I3

# ================================================================== I4 conserved phantom charge
P("\n== I4: conserved phantom charge (ratchet mu x merger N_eff) ==")
def I4_mk(f, a0):
    def c(ft):
        m = need(ft, "mu") * need(ft, "neff"); gN = need(ft, "x") * a0
        gp = glaw(gN, m * a0); return dict(delta=math.log10(gp / glaw(gN, a0)))
    return c
def I4_planted(f, a0):
    def c(ft):
        m = 8.0; gN = need(ft, "x") * a0; gp = glaw(gN, m * a0); return dict(delta=math.log10(gp / glaw(gN, a0)))
    return c
# UDG mu bracket from SPARC progenitor gas fractions
SPG = NS["SP"]
def udg_mu_fills(f):
    ms = [float(r["Mstar"]) for r in NS["UROWS"] if r["footing"] == f]; lo, hi = math.log10(min(ms)), math.log10(max(ms))
    gal = []
    for g in SPG:
        R = g["R"][-1]; mstar = (max(g["vd2"][-1], 0) + max(g["vbu2"][-1], 0)) * R / G / MS; fg = min(max(g["vg2"][-1] / g["vb2"][-1], 0.0), 0.999)
        gal.append((math.log10(mstar) if mstar > 0 else -99, fg, g["name"]))
    w = 0.0
    while True:
        sel = [x for x in gal if lo - w <= x[0] <= hi + w]
        if len(sel) >= 3: break
        w += 0.25
    mus = np.array([1 / (1 - x[1]) for x in sel])
    return dict(M_range_log=[lo, hi], widen_dex=w, N=len(sel), names=[x[2] for x in sel], fgas=[x[1] for x in sel],
                mu=dict(median=float(np.median(mus)), p84=float(np.percentile(mus, 84)), max=float(mus.max())))
I4 = dict(foot={})
FO = {"G1 SPARC": [{"mu": 1, "neff": n} for n in (1, 2)], "G2 X-COP": [{"mu": 1, "neff": n} for n in (1, 2, 4, 8, 16)],
      "G3 groups": [{"mu": 1, "neff": n} for n in (1, 2, 4, 8, 16)], "G4 ellipticals": [{"mu": 1, "neff": n} for n in (1, 2)],
      "G6 dSph classes": [{"mu": 1, "neff": n} for n in (1, 2)],
      "G7 KiDS split": [{"mu": 1, "neff_early": e, "neff_late": l} for e in (1, 2) for l in (1, 2)]}
if not MUT:
    rows = {}
    for f, a0 in A0.items():
        um = udg_mu_fills(f); I4["foot"][f] = dict(udg_progenitors=um)
        P(f"   [{f}] UDG progenitors: SPARC galaxies in log M* [{um['M_range_log'][0]:.2f}, {um['M_range_log'][1]:.2f}] +- {um['widen_dex']:.2f}: N {um['N']}; "
          f"mu median {um['mu']['median']:.2f} p84 {um['mu']['p84']:.2f} max {um['mu']['max']:.2f}")
        fo = dict(FO); fo["G5 Coma UDGs"] = [{"mu": v, "neff": 1} for v in (1.0, um["mu"]["median"], um["mu"]["p84"], um["mu"]["max"])]
        c = I4_mk(f, a0); B = BATT[f]; row = {}
        for gname, fn, fills in GATES:
            if gname.startswith("G8"):
                ok, num = fn(c, B, a0, {"mu": 1, "neff": 1}); r = dict(status="PASS" if ok else "FAIL", num=num, missing=None, bracket=None)
            else:
                r = run_gate(fn, c, B, a0, fo[gname])
            row[gname] = r; P(f"   [{f}] {gname:17s} {r['status']:10s} {NS['short'](gname, r)}")
            if r["bracket"]:
                P("        bracket: " + "; ".join(f"{json.dumps(o['fill'])}: {'PASS' if o['ok'] else 'FAIL'}" for o in r["bracket"]["runs"]))
        rows[f] = row
        # residue-arm: m that zeroes the class mean residual
        need_m = {}
        for cls, pts in (("X-COP", B["X"]), ("groups f*0.5", [p for g in B["G5"] for p in g["pts"]]), ("Coma UDGs", B["U"])):
            def mres(lm):
                m = 10 ** lm; return float(np.mean([p["D"] - math.log10(glaw(a0 * p["feat"]["x"], m * a0) / glaw(a0 * p["feat"]["x"], a0)) for p in pts]))
            lo, hi = 0.0, 5.0
            if mres(hi) > 0: need_m[cls] = float("inf")
            else:
                for _ in range(60):
                    mid = 0.5 * (lo + hi); (lo, hi) = (mid, hi) if mres(mid) > 0 else (lo, mid)
                need_m[cls] = 10 ** lo
        I4["foot"][f]["m_needed"] = need_m
        P(f"   [{f}] residue arm: m = mu N_eff needed to zero the mean: " + ", ".join(f"{k} {v:.3g}" for k, v in need_m.items()))
    web = {f: dict(r=RES["KA"][f]["KA2"]["r"], W1_pass=bool(abs(RES["KA"][f]["KA2"]["r"] - 1) <= WLINE), note="web unbound: no charge (KA2 value)") for f in A0}
    lab, st = label_of(rows, web); I4.update(rows=rows, web=web, label=lab, status=st); P(f"LABEL I4: {lab}")
else:
    m1 = {}
    for f, a0 in A0.items():
        ok, num = NS["g_sparc"](I4_planted(f, a0), BATT[f], a0); m1[f] = dict(G1_pass=bool(ok), Z=num["Z"], rms=num["rms"])
        P(f"[{f}] I4 M1 planted N_eff 8 everywhere: G1 {'PASS' if ok else 'FAIL'} (Z {num['Z']:+.4f}, rms {num['rms']:.4f}) (must FAIL)")
    I4.update(M1=m1, bites=bool(all(not v["G1_pass"] for v in m1.values()))); P(f"I4 MUTATE: {'BITES' if I4['bites'] else 'NO BITE'}")
RES["cands"]["I4"] = I4

if MUT:
    RES["MUTATE_bites"] = bool(I1["bites"] and I3["bites"] and I4["bites"]); P(f"MUTATE overall: {'BITES (all three)' if RES['MUTATE_bites'] else 'NO BITE somewhere'}")
else:
    P("\nLABELS: " + "; ".join(f"{k} {RES['cands'][k]['label']}" for k in ("I1", "I3", "I4")))
P("kappa = 1/2 FITTED; not theory closed.")
json.dump(RES, open(os.path.join(HERE, TAG + ".json"), "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else (float(o) if not isinstance(o, dict) else str(o)))
open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if (not MUT or RES["MUTATE_bites"]) else 1)
