#!/usr/bin/env python3
"""PS2_theorem_phase_space_cap graded run (FROZEN_CRITERIA.md, 898f293122).

Posit PT: Q_core = rho0/sigma0^3 (isotropic Jeans, total potential) <= Q_prog, the central Q of the half-mass progenitor
(Burkert at the BASELINE Sigma for M/2, R_out = r_f at M's Lacey-Cole epoch, no baryons). Sigma_core = max(a0/(2 pi G),
min(eta Sigma_coll, Sigma_PT)). PS1's machinery (its preamble: patched X43 copy, q_core, form_obj, halo_of) is executed
read-only; PS2 re-implements Q_prog independently and checks it against PS1's q_form_thm (K3).
Graded: G-15 (PS1's classes; NOT blind, expected TRADES via G-OUT-M3), G-HSE, G-CF. kappa = 1/2 FITTED; not theory closed.

    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 ps2_theorem_cap.py            -> .out, _results.json
    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 ps2_theorem_cap.py --mutate   -> K1 analytic side G M/(3a) (K1 must fail)
"""
import os, sys, json, math, time, resource, io, contextlib
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
import numpy as np
from scipy.optimize import brentq

T0 = time.time()
MUTATE = "--mutate" in sys.argv; TAG = "_MUTATE" if MUTATE else ""
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)
OUT = []
def P(s=""): OUT.append(s); print(s, flush=True)
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1e9 if sys.platform == "darwin" else 1e6)

# ------------------------------------------------------------------ PS1 preamble (read-only; up to its runs block)
PS1SRC = os.path.join(REB, "PS1_phase_space_core_cap", "ps1_phase_space_cap.py"); t1 = open(PS1SRC).read()
t1 = t1[:t1.index("# ------------------------------------------------------------------ runs")]
S = {"__file__": os.path.join(HERE, "ps1_ro.py"), "__name__": "ps1_ro"}
argv0 = sys.argv; sys.argv = [S["__file__"]]
with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
    exec(compile(t1, PS1SRC, "exec"), S)
sys.argv = argv0
(ns, CAP, VLAST, AALL, FEET, HK, SIG, SIG_PC, GE, MSUNE, MPCE, PC2, sigma_coll, sparc, grade_groups, grade_clusters, GALS, BGS,
 NX, N, prep, PREP, line, SAT, q_core, form_obj, halo_of, jeans_sigma2, eta_of, q_form_thm) = (S[k] for k in (
    "ns", "CAP", "VLAST", "AALL", "FEET", "HK", "SIG", "SIG_PC", "GE", "MSUNE", "MPCE", "PC2", "sigma_coll", "sparc", "grade_groups",
    "grade_clusters", "GALS", "BGS", "NX", "N", "prep", "PREP", "line", "SAT", "q_core", "form_obj", "halo_of", "jeans_sigma2",
    "eta_of", "q_form_thm"))
CF0 = S["CFT"].copy()
def set_cf(fac): S["CFT"] = CF0 * fac
X48C = json.load(open(os.path.join(REB, "X48_native_cf_zoom", "x48_regrade_x43copy_ng48_results.json")))
P(f"PS2_theorem_phase_space_cap  {'MUTATE run (K1 analytic side G M/(3a))' if MUTATE else 'normal run'}")
P("kappa = 1/2 FITTED; footings never pooled; route E (Newtonian); cold dark energy, not a particle; not theory closed")
P(f"PS1 preamble + X43 machinery executed read-only [{time.time() - T0:.0f} s, RSS {rss():.2f} GB]; c_f table " + ", ".join(f"{c:.3f}" for c in CF0))
RES = dict(frozen="898f293122", mutate=MUTATE, footings={}, reported={}, checks={}); checks = []

# ------------------------------------------------------------------ Q_prog (independent implementation, K3 against PS1)
def sig_base(f, tag, M):
    return max(SIG[f], eta_of(M) * sigma_coll(tag, M)[0] * MSUNE / PC2)
def prog_halo(tag, M):
    _, rf, _ = form_obj(tag, M); return (M / 2 * MSUNE, rf * MPCE, lambda r: np.zeros_like(r))
def q_prog(f, tag, M, recursive=False):
    hal = prog_halo(tag, M); s = sig_base(f, tag, M / 2)
    if recursive:                                   # reported item 3: the progenitor's own Sigma capped by PT one level down
        sc = eta_of(M / 2) * sigma_coll(tag, M / 2)[0] * MSUNE / PC2
        if sc > SIG[f]:
            Qp = q_prog(f, tag, M / 2)
            if q_core(sc, hal)[0] > Qp:
                s = SIG[f] if q_core(SIG[f], hal)[0] >= Qp else math.exp(brentq(lambda ls: math.log(q_core(math.exp(ls), hal)[0] / Qp), math.log(SIG[f]), math.log(sc), xtol=1e-13))
    return q_core(s, hal)[0]

STATS = {}; RESID = []; SIGS = {}
def make_hook(recursive=False):
    def hook(f, tag, M, s_floor, s_coll, ctx):
        hal = halo_of(ctx); Qp = q_prog(f, tag, M, recursive)
        key = (ctx[0], ctx[2]) if ctx[0] == "cl" else (ctx[0], tag); st = STATS.setdefault(key, [0, 0, 0]); st[0] += 1
        if q_core(s_coll, hal)[0] <= Qp: return s_coll
        st[1] += 1
        if q_core(s_floor, hal)[0] >= Qp: st[2] += 1; return s_floor
        g = lambda ls: math.log(q_core(math.exp(ls), hal)[0] / Qp)
        ls = brentq(g, math.log(s_floor), math.log(s_coll), xtol=1e-13, rtol=1e-14)
        RESID.append(abs(math.exp(g(ls)) - 1)); return math.exp(ls)
    return hook

# ------------------------------------------------------------------ K1 Plummer, K3 Q_prog vs PS1
a_, Mp = 3.0857e19, 1e11 * MSUNE
r = np.logspace(math.log10(a_ * 1e-6), math.log10(a_ * 1e4), S["NGRID"])
rho_p = 3 * Mp / (4 * math.pi * a_ ** 3) * (1 + (r / a_) ** 2) ** -2.5; M_p = Mp * r ** 3 / (r * r + a_ * a_) ** 1.5
s2n = jeans_sigma2(r, rho_p, M_p, 3 * Mp / (4 * math.pi * a_ ** 3)); s2a = GE * Mp / ((3 if MUTATE else 6) * a_)
k1 = abs(s2n / s2a - 1) < 1e-6
P(f"K1 Plummer central dispersion: numeric/analytic - 1 = {s2n / s2a - 1:+.2e}: {'PASS' if k1 else 'FAIL'}"); checks.append(("K1", k1))
d3 = max(abs(q_prog("canonical", "A_c2b_refit", 10 ** lm) / q_form_thm("A_c2b_refit", 10 ** lm, "canonical") - 1) for lm in (12.5, 13, 13.5, 14, 15))
k3 = d3 < 1e-12
P(f"K3 Q_prog vs PS1 q_form_thm (5 masses): max rel {d3:.1e}: {'PASS' if k3 else 'FAIL'}"); checks.append(("K3", k3))

# ------------------------------------------------------------------ runs
KEYS = ["G-MID-T1", "G-MID-T2", "G-MID-T3", "G-MID-b", "G-OUT-all", "G-OUT-T1", "G-OUT-T2", "G-OUT-T3", "G-OUT-b", "G-IN-all",
        "G-OUT-Mall", "G-OUT-M1", "G-OUT-M2", "G-OUT-M3", "G-IN-Mall"]
def with_hook(h, fn, *a, **k):
    CAP["hook"] = h
    try: return fn(*a, **k)
    finally: CAP["hook"] = None
def run(f, hook, tag="A_c2b_refit", full=True):
    STATS.clear(); s0 = SAT["n"]
    sA = with_hook(hook, sparc, f, tag) if full else None
    if sA is not None: sA["line"] = line(sA)
    gr = with_hook(hook, grade_groups, f) if full else None
    gc = with_hook(hook, grade_clusters, f, tag=tag)
    return dict(sparc=sA, groups=gr, clusters=gc, stats={f"{k[0]}|{k[1]}": list(v) for k, v in STATS.items()}, sat=SAT["n"] - s0)
def g15(base, cap):
    bc, cc = base["clusters"], cap["clusters"]; bpass = [k for k in KEYS if bc["ok"][k]]
    frac = {hk: cap["stats"].get(f"cl|{hk}", [0, 0, 0])[1] / N for hk in HK}
    dIN = {hk: cc["cells"][hk]["G-IN-Mall"]["pred"] / bc["cells"][hk]["G-IN-Mall"]["pred"] - 1 for hk in HK}
    zb = max(abs(bc["cells"][hk]["G-IN-Mall"]["Z"]) for hk in HK); zc = max(abs(cc["cells"][hk]["G-IN-Mall"]["Z"]) for hk in HK)
    sides = cap["sparc"]["line"] and cap["groups"]["PASS"]
    broke = [k for k in bpass if not cc["ok"][k]] + ([] if cap["sparc"]["line"] else ["SPARC line"]) + ([] if cap["groups"]["PASS"] else ["groups"])
    if all(x < 0.10 for x in frac.values()) or all(abs(x) < 0.03 for x in dIN.values()): cls = "INERT"
    elif not cc["fails"] and sides: cls = "PASS"
    elif zc < zb and not broke: cls = "IMPROVES"
    elif (cc["ok"]["G-IN-Mall"] or zc < zb) and broke: cls = "TRADES"
    else: cls = "FAILS"
    return cls, dict(frac=frac, dIN=dIN, zin=[zb, zc], broke=broke)
MP_, KEV = 1.67262192e-27, 1.602176634e-16
KT = np.asarray(NX["KT"], float); OKK = np.isfinite(KT) & (KT > 0)
k0 = True; k2mono = True; nmono = 0
for f in FEET:
    P(f"\n=== [{f}] Sigma_a0 {SIG_PC[f]:.1f} Msun/pc^2")
    base = run(f, None)
    for hk in HK:
        k0 &= abs(base["clusters"]["cells"][hk]["G-IN-Mall"]["pred"] - X48C["footings"][f]["clusters"]["cells"][hk]["G-IN-Mall"]["pred"]) < 1e-9
    k0 &= abs(base["sparc"]["rms"] - X48C["footings"][f]["sparc"]["A_c2b_refit"]["rms"]) < 1e-9
    cap = run(f, make_hook()); cc = cap["clusters"]; cls, gd = g15(base, cap)
    st = {k: v for k, v in cap["stats"].items()}
    P(f"  PT cap binds: clusters " + ", ".join(f"{hk} {st.get(f'cl|{hk}', [0, 0, 0])[1]}/{N} (floor {st.get(f'cl|{hk}', [0, 0, 0])[2]})" for hk in HK)
      + f"; SPARC {st.get('sparc|A_c2b_refit', [0, 0, 0])[1]}/{len(GALS)}; group calls {st.get('grp|A_c2b_refit', [0, 0, 0])[1]}/{st.get('grp|A_c2b_refit', [0, 0, 0])[0]}; saturations {cap['sat']}")
    for hk in HK:
        P(f"   [{hk}] " + "; ".join(f"{k} {cc['cells'][hk][k]['pred']:.2f}/{cc['cells'][hk][k]['meas']:.2f} Z {cc['cells'][hk][k]['Z']:+.2f}" + ("" if abs(cc['cells'][hk][k]['Z']) <= 2 else " FAIL") for k in KEYS))
    P(f"  SPARC {cap['sparc']['rms']:.4f} line {'PASS' if cap['sparc']['line'] else 'FAIL'}; groups Z {cap['groups']['Z']:+.2f} {cap['groups']['verdict']}; cluster fails {cc['fails'] or 'none'}")
    P(f"  G-IN-Mall max|Z| {gd['zin'][0]:.2f} -> {gd['zin'][1]:.2f}; pred change " + ", ".join(f"{hk} {x:+.1%}" for hk, x in gd["dIN"].items()) + f"; broken {gd['broke'] or 'none'}")
    P(f"  G-15 [{f}]: {cls}")
    # ---- G-HSE
    hook = make_hook(); rq, rb = [], []
    for i in np.where(OKK)[0]:
        i = int(i); pp = prep(i, f, "h0672"); Mtot = (pp["Mfair"] + float(pp["Mb"][-1])) / MSUNE
        s_hg = 9 * (2 / 3) * KT[i] * KEV / (0.6 * MP_) / (4 * math.pi * GE * 0.15 * pp["R500"] * MPCE)
        sc_ = with_hook(hook, ns["sig_core"], f, "A_c2b_refit", Mtot, True, ctx=("cl", pp, "h0672"))[0]
        rq.append(sc_ / s_hg); rb.append(ns["sig_core"](f, "A_c2b_refit", Mtot, True)[0] / s_hg)
    hse_med = float(np.median(rq)); hse = "HSE-MATCH" if 0.67 <= hse_med <= 1.5 else "HSE-MISS"
    P(f"  G-HSE ({len(rq)} KT, h 0.672): median Sigma_core/Sigma_HG {hse_med:.3f} [16-84% {np.percentile(rq, 16):.2f}-{np.percentile(rq, 84):.2f}] "
      f"(baseline {np.median(rb):.2f}) -> {hse}")
    for i in range(N):                       # K2: monotonic on the solver's bracket [Sigma_a0, eta Sigma_coll], every cluster at h 0.672
        pp = prep(int(i), f, "h0672"); Mtot = (pp["Mfair"] + float(pp["Mb"][-1])) / MSUNE
        sc = eta_of(Mtot) * sigma_coll("A_c2b_refit", Mtot)[0] * MSUNE / PC2
        if sc <= SIG[f]: continue
        hal = halo_of(("cl", pp, "h0672")); s0 = SAT["n"]
        qs = [q_core(s, hal)[0] for s in np.geomspace(SIG[f], sc, 25)]; ok = bool(np.all(np.diff(qs) > 0)) and SAT["n"] == s0
        k2mono &= ok; nmono += 1
    PREP.clear()
    # ---- G-CF
    cf = {}
    for fac in (0.5, 2.0):
        set_cf(fac); STATS.clear(); s0 = SAT["n"]
        b_ = grade_clusters(f); c_ = with_hook(make_hook(), grade_clusters, f); set_cf(1.0)
        cf[fac] = dict(pass_=bool(c_["ok"]["G-IN-Mall"]), Z=[c_["cells"][hk]["G-IN-Mall"]["Z"] for hk in HK],
                       pred=[c_["cells"][hk]["G-IN-Mall"]["pred"] for hk in HK], baseZ=[b_["cells"][hk]["G-IN-Mall"]["Z"] for hk in HK],
                       move=[c_["cells"][hk]["G-IN-Mall"]["pred"] / cc["cells"][hk]["G-IN-Mall"]["pred"] - 1 for hk in HK], fails=c_["fails"], sat=SAT["n"] - s0)
        P(f"  G-CF c_f x{fac:g}: G-IN-Mall Z {cf[fac]['Z'][0]:+.2f} / {cf[fac]['Z'][1]:+.2f} (cap off: {cf[fac]['baseZ'][0]:+.2f} / {cf[fac]['baseZ'][1]:+.2f}); "
          f"pred move vs graded {cf[fac]['move'][0]:+.1%} / {cf[fac]['move'][1]:+.1%}; fails {c_['fails'] or 'none'}")
    cfl = "CF-ROBUST" if all(cf[x]["pass_"] and all(abs(m) < 0.10 for m in cf[x]["move"]) for x in cf) else "CF-FRAGILE"
    P(f"  G-CF [{f}]: {cfl}")
    P(f"  HEADLINE [{f}]: {cls} | {hse} | {cfl}   [{time.time() - T0:.0f} s, RSS {rss():.2f} GB]")
    RES["footings"][f] = dict(G15=cls, G15_detail=gd, HSE=hse, HSE_median=hse_med, HSE_16_84=[float(np.percentile(rq, 16)), float(np.percentile(rq, 84))],
                              HSE_baseline=float(np.median(rb)), CF=cfl, CF_detail={str(k): v for k, v in cf.items()},
                              cells={hk: cc["cells"][hk] for hk in HK}, sparc=cap["sparc"], groups=cap["groups"], stats=cap["stats"], sat=cap["sat"])
    # ---- reported
    rep = {}
    rep["M_terciles"] = {hk: {k: cc["cells"][hk][k] for k in ("G-OUT-M1", "G-OUT-M2", "G-OUT-M3", "G-OUT-Mall")} for hk in HK}
    P("  (reported) MGAS OUTER " + " | ".join(f"{hk}: " + ", ".join(f"{k[-2:]} {v['pred']:.2f}/{v['meas']:.2f} Z {v['Z']:+.2f}" for k, v in rep["M_terciles"][hk].items()) for hk in HK))
    hk = "h0672"; d = NX["DAT"][hk]; WB = d["W"] * d["B"][None, :]; nb = (WB * (d["D"] - NX["MY"]["leakP"][:, NX["HXI"][hk], 0])).sum(0)
    with_hook(make_hook(), grade_clusters, f); dC = NX["DC"][(f, hk)].sum(0); pm = (VLAST[(f, hk)].sum(0) / dC) / (nb / dC)
    rep["bin_pred_over_meas"] = pm.tolist(); P("  (reported) per-bin pred/meas, bins 0-7: " + " ".join(f"{x:.2f}" for x in pm))
    STATS.clear(); rc_ = with_hook(make_hook(recursive=True), grade_clusters, f)
    rep["recursive"] = dict(fails=rc_["fails"], Z=[rc_["cells"][h]["G-IN-Mall"]["Z"] for h in HK], M3=[rc_["cells"][h]["G-OUT-M3"]["Z"] for h in HK])
    P(f"  (reported) recursive progenitor: G-IN-Mall Z {rep['recursive']['Z'][0]:+.2f} / {rep['recursive']['Z'][1]:+.2f}; M3 Z {rep['recursive']['M3'][0]:+.2f}; fails {rc_['fails'] or 'none'}")
    bB = run(f, None, tag="B_cfg886_bg"); cB = run(f, make_hook(), tag="B_cfg886_bg"); clsB, gdB = g15(bB, cB)
    rep["bgB"] = dict(G15=clsB, fails=cB["clusters"]["fails"], sparc=cB["sparc"]["rms"])
    P(f"  (reported) background B: G-15 {clsB}; fails {cB['clusters']['fails'] or 'none'}; SPARC {cB['sparc']['rms']:.4f} (groups use bg A, as X43)")
    nfl = {hk: st.get(f"cl|{hk}", [0, 0, 0])[2] for hk in HK}; rep["n_floor"] = nfl
    P(f"  (reported) clusters where Sigma_PT < Sigma_a0 (floor binds): {nfl}")
    RES["reported"][f] = rep

# ------------------------------------------------------------------ two-sided anisotropy (reported)
bg = BGS["A_c2b_refit"]; rc = 3 * (100 * bg["h"] * 1e3 / MPCE) ** 2 / (8 * math.pi * GE); ANI = {}
def q_at(Sig, hal, be):
    o, r0 = q_core(Sig, hal, beta_r=(0.5, 0.1)); rs = 0.1 * r0; rho0 = Sig / r0
    rho_s = rho0 * r0 ** 3 / ((rs + r0) * (rs * rs + r0 * r0)); return rho_s / o[be] ** 1.5
for lm in (13, 14, 15):
    M = 10.0 ** lm; R200 = (3 * M * MSUNE / (4 * math.pi * 200 * rc)) ** (1 / 3); hd = halo_of(("bare", M * MSUNE, R200)); hp = prog_halo("A_c2b_refit", M)
    sd = sig_base("canonical", "A_c2b_refit", M); sp = sig_base("canonical", "A_c2b_refit", M / 2)
    ANI[f"1e{lm}"] = dict(iso=q_at(sd, hd, 0.0) / q_at(sp, hp, 0.0), beta05=q_at(sd, hd, 0.5) / q_at(sp, hp, 0.5))
P("\n=== (reported) two-sided anisotropy, Q_desc/Q_prog at 0.1 r0 (bare halos, baseline Sigma): "
  + ", ".join(f"{k} iso {v['iso']:.2f} / beta 0.5 {v['beta05']:.2f}" for k, v in ANI.items()))
RES["reported"]["anisotropy_two_sided"] = ANI

# ------------------------------------------------------------------ verdict + checks
def agree(key):
    a, b = RES["footings"]["canonical"][key], RES["footings"]["alt"][key]
    return a if a == b else f"UNDECIDED ({a} / {b})"
RES["headline"] = dict(G15=agree("G15"), HSE=agree("HSE"), CF=agree("CF"))
P(f"\n=== HEADLINE (both footings): {RES['headline']['G15']} | {RES['headline']['HSE']} | {RES['headline']['CF']}")
P(f"K0 cap off reproduces X48 ng 48 (1e-9): {'PASS' if k0 else 'FAIL'}"); checks.insert(0, ("K0", k0))
satg = sum(RES["footings"][f]["sat"] for f in FEET)
k2 = k2mono and satg == 0 and (max(RESID) < 1e-8 if RESID else True)
P(f"K2 solver-bracket monotonic over {nmono} cluster brackets (no saturation inside): {k2mono}; graded saturations {satg}; "
  f"root residual max {max(RESID) if RESID else 0:.1e} over {len(RESID)} solves: {'PASS' if k2 else 'FAIL'}"); checks.append(("K2", k2))
checks.append(("K4", rss() < 2.0))
P("\n=== CHECKS"); [P(f"  [{'PASS' if ok else 'FAIL'}] {k}") for k, ok in checks]
RES["checks"] = {k: bool(ok) for k, ok in checks}; n = sum(bool(ok) for _, ok in checks)
P(f"\nchecks {n}/{len(checks)}; runtime {time.time() - T0:.0f} s; peak RSS {rss():.2f} GB")
open(os.path.join(HERE, f"ps2_theorem_cap{TAG}.out"), "w").write("\n".join(OUT) + "\n")
json.dump(RES, open(os.path.join(HERE, f"ps2_theorem_cap_results{TAG}.json"), "w"), indent=1, default=float)
for fn in ("x43_copy.py",):
    try: os.remove(os.path.join(HERE, fn))
    except OSError: pass
sys.exit(0 if n == len(checks) else 1)
