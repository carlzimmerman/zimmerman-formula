#!/usr/bin/env python3
"""PS1_phase_space_core_cap graded run (FROZEN_CRITERIA.md, 748770f505).

Posit PQ: a collapse-cored halo's central rho0/sigma0^3 (isotropic Jeans of the cold Burkert in the total potential, cold +
baryons, Newtonian) does not exceed the mean phase-space density of its half-mass formation object (X41 EPS, unchanged):
Sigma_core = max(a0/(2 pi G), min(eta(c_f) Sigma_coll, Sigma_Q)). Baseline = X48 regrade at ng 48 (X43's rule with the ng-48
c_f table). X43's machinery is executed read-only from a patched copy (as X48 did); only sig_core and its three call sites
change. kappa = 1/2 FITTED; not theory closed.

    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 ps1_phase_space_cap.py            -> .out, _results.json
    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 ps1_phase_space_cap.py --mutate   -> K1 analytic side G M/(3a) (K1 must fail)
"""
import os, sys, json, math, time, resource, io, contextlib
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
import numpy as np
from scipy.optimize import brentq
from scipy.integrate import simpson

T0 = time.time()
MUTATE = "--mutate" in sys.argv; TAG = "_MUTATE" if MUTATE else ""
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)
OUT = []
def P(s=""): OUT.append(s); print(s, flush=True)
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1e9 if sys.platform == "darwin" else 1e6)

# ------------------------------------------------------------------ baseline c_f table (X48 ng 48), as x48_regrade.py
X48J = json.load(open(os.path.join(REB, "X48_native_cf_zoom", "x48_regrade_ng48.json")))
X48C = json.load(open(os.path.join(REB, "X48_native_cf_zoom", "x48_regrade_x43copy_ng48_results.json")))
LM = np.array(X48J["table"]["lgM"]); CFT = np.array(X48J["table"]["cf"])
B1 = 3 * math.log(2) - math.pi / 2
def cf_of(M): return float(np.interp(math.log10(M), LM, CFT))
def eta_of(M): return 4.0 / (3.0 * B1) * cf_of(M) ** 1.25

# ------------------------------------------------------------------ X43 (patched copy, executed read-only up to its graded loop)
src = open(os.path.join(REB, "X43_collapse_core_floor", "x43_collapse_core.py")).read()
src = src[:src.index("\nfor f in FEET:\n")]
old = '''def sig_core(f, tag, M, rule=True):
    s = SIG[f]
    if not rule: return s, False
    sc = ETA_USE["v"] * sigma_coll(tag, M)[0] * MSUNE / PC2
    return max(s, sc), sc > s'''
new = '''def sig_core(f, tag, M, rule=True, ctx=None):
    s = SIG[f]
    if not rule: return s, False
    eta = ETA_FUN(M) if ETA_USE["v"] == ETA else ETA_USE["v"]
    sc = eta * sigma_coll(tag, M)[0] * MSUNE / PC2
    if CAP["hook"] is not None and ctx is not None and sc > s: sc = CAP["hook"](f, tag, M, s, sc, ctx)
    return max(s, sc), sc > s'''
for o_, n_ in ((old, new),
               ("s, a_ = sig_core(f, tag, M200, rule); act += a_", "s, a_ = sig_core(f, tag, M200, rule, ctx=('sparc', q, M200 * MSUNE, R200)); act += a_"),
               ("s, a_ = sig_core(foot, tag, Mtot, rule); act += a_", "s, a_ = sig_core(foot, tag, Mtot, rule, ctx=('cl', pp, hk)); act += a_"),
               ('sc, act = sig_core(foot, "A_c2b_refit", M200 / MSUNE)', 'sc, act = sig_core(foot, "A_c2b_refit", M200 / MSUNE, ctx=("grp", Mb, a, M200, R200))'),
               ("            V[i] = dvecN(int(i), foot, hk, pp[\"Mb\"] + Mh)\n", "            V[i] = dvecN(int(i), foot, hk, pp[\"Mb\"] + Mh)\n        VLAST[(foot, hk)] = V.copy()\n"),
               ("Aall = [float(vB[:, bi].sum() / vC[:, bi].sum()) for bi in range(3)]", "Aall = [float(vB[:, bi].sum() / vC[:, bi].sum()) for bi in range(3)]; AALL[(foot, hk)] = Aall"),
               ('"x43_x30_machinery"', '"ps1_x30_machinery"')):
    assert src.count(o_) == 1, o_[:60]
    src = src.replace(o_, n_)
CAP = {"hook": None}; VLAST = {}; AALL = {}
ns = {"__file__": os.path.join(HERE, "x43_copy.py"), "__name__": "x43_copy", "ETA_FUN": eta_of, "CAP": CAP, "VLAST": VLAST, "AALL": AALL}
argv0 = sys.argv; sys.argv = [ns["__file__"]]
with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
    exec(compile(src, ns["__file__"], "exec"), ns)
sys.argv = argv0
(FEET, HK, SIG, SIG_PC, GE, MSUNE, MPCE, PC2, B, solve_r0, zform, sigma_coll, EPS, DELTA, sparc, grade_groups, grade_clusters,
 GALS, UPS, BGS, NX, N, ALLI, prep, PREP, RM, RG, line, SAT) = (ns[k] for k in (
    "FEET", "HK", "SIG", "SIG_PC", "GE", "MSUNE", "MPCE", "PC2", "B", "solve_r0", "zform", "sigma_coll", "EPS", "DELTA", "sparc",
    "grade_groups", "grade_clusters", "GALS", "UPS", "BGS", "NX", "N", "ALLI", "prep", "PREP", "RM", "RG", "line", "SAT"))
P(f"PS1_phase_space_core_cap  {'MUTATE run (K1 analytic side G M/(3a))' if MUTATE else 'normal run'}")
P("kappa = 1/2 FITTED; footings never pooled; route E (Newtonian); cold dark energy, not a particle; not theory closed")
P(f"baseline c_f table (X48 ng 48): " + ", ".join(f"1e{l:.0f} {c:.3f}" for l, c in zip(LM, CFT)) + " (flat outside)")
P(f"X43 machinery executed read-only (patched copy) [{time.time() - T0:.0f} s, RSS {rss():.2f} GB]; X43 preamble checks: "
  + ", ".join(f"{k} {'PASS' if v else 'FAIL'}" for k, v in ns["checks"]))
RES = dict(frozen="748770f505", mutate=MUTATE, footings={}, checks={}, reported={})
checks = []

# ------------------------------------------------------------------ Jeans central dispersion and Q_core
NGRID = 3000
def jeans_sigma2(r, rho, Mtot, rho0):
    """sigma0^2 = (1/rho0) int rho G M_tot / r^2 dr on a log grid (Simpson in ln r)."""
    return float(simpson(rho * GE * Mtot / r ** 2 * r, x=np.log(r))) / rho0
def halo_of(ctx):
    """(cold mass, outer radius, baryon M(r) function) in SI for each call site."""
    kind = ctx[0]
    if kind == "sparc":
        _, q, Mh, Rout = ctx; iu = int(np.argmin(np.abs(UPS - 0.50))); R = q["Rm"]
        mb = np.maximum.accumulate(np.clip(q["GB"][:, iu] * R ** 2 / GE, 0, None))
        def mbf(r): return np.where(r < R[0], mb[0] * (r / R[0]) ** 3, np.interp(r, R, mb))
        return Mh, Rout, mbf
    if kind == "cl":
        _, pp, hk = ctx; Mb = pp["Mb"]
        def mbf(r): return np.where(r < RM[0], Mb[0] * (r / RM[0]) ** 3, np.interp(r, RM, Mb))
        return pp["Mfair"], pp["rta"], mbf
    if kind == "grp":
        _, Mb, a, M200, R200 = ctx
        def mbf(r): return Mb * r ** 2 / (r + a) ** 2
        return M200, R200, mbf
    if kind == "bare":
        _, Mh, Rout = ctx
        return Mh, Rout, (lambda r: np.zeros_like(r))
    raise ValueError(kind)
def q_core(Sig, hal, beta_r=None):
    """Q_core = rho0 / sigma0^3 for the Burkert at surface density Sig (isotropic Jeans, total potential).
    beta_r = (beta, x): reported anisotropy bracket, sigma_r at r = x r0 for constant beta."""
    Mh, Rout, mbf = hal; r0 = solve_r0(Mh, Rout, Sig); rho0 = Sig / r0
    r = np.logspace(math.log10(min(r0, Rout) * 1e-6), math.log10(Rout), NGRID)
    rho = rho0 * r0 ** 3 / ((r + r0) * (r * r + r0 * r0)); Mc = math.pi * Sig * r0 ** 2 * B(r / r0)
    Mt = Mc + mbf(r)
    if beta_r is None:
        return rho0 / jeans_sigma2(r, rho, Mt, rho0) ** 1.5, r0
    out = {}
    for be in (0.0, beta_r[0]):
        rs = beta_r[1] * r0; sel = r >= rs; rr = r[sel]
        I = float(simpson(rho[sel] * GE * Mt[sel] / rr ** 2 * rr ** (2 * be) * rr, x=np.log(rr)))
        rho_s = rho0 * r0 ** 3 / ((rs + r0) * (rs * rs + r0 * r0)); out[be] = I / (rho_s * rs ** (2 * be))
    return out, r0

# ------------------------------------------------------------------ formation phase-space density (X41 internals)
def form_obj(tag, M):
    zf, Df = zform(tag, M); e = EPS[tag]; rho = DELTA * e["rhom0"] * (1 + zf) ** 3               # Msun/Mpc^3
    rf = (3 * (M / 2) / (4 * math.pi * rho)) ** (1 / 3)                                           # Mpc
    return rho, rf, zf
def q_form(tag, M):
    rho, rf, _ = form_obj(tag, M); rhoS = rho * MSUNE / MPCE ** 3; rfS = rf * MPCE
    s2 = GE * (M / 2) * MSUNE / (2 * rfS); return rhoS / s2 ** 1.5
def q_form_thm(tag, M, f):
    """Reported item 3: the progenitor's own central Q_core (Burkert of mass M/2 at the baseline Sigma, R_out = r_f)."""
    _, rf, _ = form_obj(tag, M); s0 = SIG[f]; sc = eta_of(M / 2) * sigma_coll(tag, M / 2)[0] * MSUNE / PC2
    return q_core(max(s0, sc), (M / 2 * MSUNE, rf * MPCE, lambda r: np.zeros_like(r)))[0]

STATS = {}; RESID = []
def make_hook(mode):
    def hook(f, tag, M, s_floor, s_coll, ctx):
        hal = halo_of(ctx); Qf = q_form(tag, M) if mode == "cap" else q_form_thm(tag, M, f)
        key = (ctx[0], ctx[2]) if ctx[0] == "cl" else (ctx[0], tag); st = STATS.setdefault(key, [0, 0, 0])
        st[0] += 1
        qh = q_core(s_coll, hal)[0]
        if qh <= Qf: return s_coll
        st[1] += 1
        ql = q_core(s_floor, hal)[0]
        if ql >= Qf: st[2] += 1; return s_floor
        g = lambda ls: math.log(q_core(math.exp(ls), hal)[0] / Qf)
        ls = brentq(g, math.log(s_floor), math.log(s_coll), xtol=1e-13, rtol=1e-14)
        RESID.append(abs(math.exp(g(ls)) - 1)); return math.exp(ls)
    return hook

# ------------------------------------------------------------------ K1 Plummer, K2 monotonic, K3 formation reuse
a_, Mp = 3.0857e19, 1e11 * MSUNE
r = np.logspace(math.log10(a_ * 1e-6), math.log10(a_ * 1e4), NGRID)
rho_p = 3 * Mp / (4 * math.pi * a_ ** 3) * (1 + (r / a_) ** 2) ** -2.5; M_p = Mp * r ** 3 / (r * r + a_ * a_) ** 1.5
s2n = jeans_sigma2(r, rho_p, M_p, 3 * Mp / (4 * math.pi * a_ ** 3)); s2a = GE * Mp / ((3 if MUTATE else 6) * a_)
k1 = abs(s2n / s2a - 1) < 1e-6
P(f"K1 Plummer central dispersion: numeric/analytic - 1 = {s2n / s2a - 1:+.2e}: {'PASS' if k1 else 'FAIL'}"); checks.append(("K1", k1))
bg = BGS["A_c2b_refit"]; rc = 3 * (100 * bg["h"] * 1e3 / MPCE) ** 2 / (8 * math.pi * GE); mono = True; k2txt = []
for lm in (12.5, 13.0, 13.5, 14.0, 15.0):
    M200 = 10 ** lm; R200 = (3 * M200 * MSUNE / (4 * math.pi * 200 * rc)) ** (1 / 3); hal = halo_of(("bare", M200 * MSUNE, R200))
    sc = eta_of(M200) * sigma_coll("A_c2b_refit", M200)[0] * MSUNE / PC2; lo = min(SIG["canonical"], sc) * 0.5
    qs = [q_core(s, hal)[0] for s in np.geomspace(lo, sc * 1.5, 25)]; ok = bool(np.all(np.diff(qs) > 0)); mono &= ok
    k2txt.append(f"1e{lm:g} {'mono' if ok else 'NOT MONO'}")
P("K2a Q_core(Sigma) monotonic on the bracket: " + ", ".join(k2txt))
rho_, rf_, _ = form_obj("A_c2b_refit", 1e14); k3 = abs(rho_ * rf_ / 1e12 / sigma_coll("A_c2b_refit", 1e14)[0] - 1) < 1e-12
P(f"K3 formation side reuses X41: rho_f r_f / Sigma_coll - 1 = {rho_ * rf_ / 1e12 / sigma_coll('A_c2b_refit', 1e14)[0] - 1:+.1e}: {'PASS' if k3 else 'FAIL'}")
checks.append(("K3", k3))

# ------------------------------------------------------------------ runs
def run(f, mode):
    CAP["hook"] = None if mode == "off" else make_hook(mode); STATS.clear(); s0 = SAT["n"]
    sA = sparc(f, "A_c2b_refit"); sA["line"] = line(sA)
    gr = grade_groups(f); gc = grade_clusters(f)
    st = {f"{k[0]}|{k[1]}": list(v) for k, v in STATS.items()}; CAP["hook"] = None
    return dict(sparc=sA, groups=gr, clusters=gc, stats=st, sat=SAT["n"] - s0, Aall={hk: AALL[(f, hk)] for hk in HK})
def cell_line(c0, ok, keys):
    return "; ".join(f"{k} {c0[k]['pred']:.2f}/{c0[k]['meas']:.2f} Z {c0[k]['Z']:+.2f}{'' if ok[k] else ' FAIL'}" for k in keys)
KEYS = ["G-MID-T1", "G-MID-T2", "G-MID-T3", "G-MID-b", "G-OUT-all", "G-OUT-T1", "G-OUT-T2", "G-OUT-T3", "G-OUT-b", "G-IN-all",
        "G-OUT-Mall", "G-OUT-M1", "G-OUT-M2", "G-OUT-M3", "G-IN-Mall"]
k0 = True
for f in FEET:
    P(f"\n=== [{f}] Sigma_a0 {SIG_PC[f]:.1f} Msun/pc^2")
    base = run(f, "off")
    for hk in HK:
        d = abs(base["clusters"]["cells"][hk]["G-IN-Mall"]["pred"] - X48C["footings"][f]["clusters"]["cells"][hk]["G-IN-Mall"]["pred"])
        k0 &= d < 1e-9
    dS = abs(base["sparc"]["rms"] - X48C["footings"][f]["sparc"]["A_c2b_refit"]["rms"]); k0 &= dS < 1e-9
    bc = base["clusters"]; bpass = [k for k in KEYS if bc["ok"][k]]
    P(f"  baseline (X48 ng 48, reproduced): SPARC {base['sparc']['rms']:.4f} line {'PASS' if base['sparc']['line'] else 'FAIL'}; "
      f"groups Z {base['groups']['Z']:+.2f}; cluster fails {bc['fails'] or 'none'}; passing cells {len(bpass)}/15")
    cap = run(f, "cap"); cc = cap["clusters"]
    nb_cl = {hk: cap["stats"].get(f"cl|{hk}", [0, 0, 0]) for hk in HK}
    frac = {hk: nb_cl[hk][1] / N for hk in HK}
    dIN = {hk: cc["cells"][hk]["G-IN-Mall"]["pred"] / bc["cells"][hk]["G-IN-Mall"]["pred"] - 1 for hk in HK}
    P(f"  PS1 cap: binds in clusters " + ", ".join(f"{hk} {nb_cl[hk][1]}/{N} (to floor {nb_cl[hk][2]})" for hk in HK)
      + f"; SPARC {cap['stats'].get('sparc|A_c2b_refit', [0, 0, 0])[1]}/{len(GALS)}; groups (all calls) "
      + f"{cap['stats'].get('grp|A_c2b_refit', [0, 0, 0])[1]}/{cap['stats'].get('grp|A_c2b_refit', [0, 0, 0])[0]}; Burkert saturations {cap['sat']}")
    P(f"  G-IN-Mall pred change vs baseline: " + ", ".join(f"{hk} {dIN[hk]:+.3%}" for hk in HK))
    for hk in HK: P(f"   [{hk}] " + cell_line(cc["cells"][hk], {k: abs(cc["cells"][hk][k]["Z"]) <= 2 for k in KEYS}, KEYS))
    P(f"  SPARC (bg A) rms {cap['sparc']['rms']:.4f} median U {cap['sparc']['U_median']:.2f} line {'PASS' if cap['sparc']['line'] else 'FAIL'}; "
      f"groups mean {cap['groups']['mean']:+.4f} Z {cap['groups']['Z']:+.2f} {cap['groups']['verdict']}; cluster fails {cc['fails'] or 'none'}")
    # ---- grade (criteria section 3)
    zb = max(abs(bc["cells"][hk]["G-IN-Mall"]["Z"]) for hk in HK); zc = max(abs(cc["cells"][hk]["G-IN-Mall"]["Z"]) for hk in HK)
    inert = all(fr < 0.10 for fr in frac.values()) or all(abs(x) < 0.03 for x in dIN.values())
    sides_ok = cap["sparc"]["line"] and cap["groups"]["PASS"]
    broke = [k for k in bpass if not cc["ok"][k]] + ([] if cap["sparc"]["line"] else ["SPARC line"]) + ([] if cap["groups"]["PASS"] else [f"groups (Z {cap['groups']['Z']:+.2f})"])
    improved = zc < zb; inpass = cc["ok"]["G-IN-Mall"]
    if inert: cls = "INERT"
    elif not cc["fails"] and sides_ok: cls = "PASS"
    elif improved and not broke: cls = "IMPROVES"
    elif (inpass or improved) and broke: cls = "TRADES"
    else: cls = "FAILS"
    P(f"  G-IN-Mall max|Z| {zb:.2f} -> {zc:.2f}; broken: {broke or 'none'}")
    P(f"  CLASS [{f}]: {cls}   [{time.time() - T0:.0f} s, RSS {rss():.2f} GB]")
    RES["footings"][f] = dict(cls=cls, baseline=dict(sparc=base["sparc"], groups=base["groups"], clusters=bc, Aall=base["Aall"]),
                              cap=cap, frac_bind=frac, dIN=dIN, zin=[zb, zc], broke=broke)
    # ---- reported (not graded)
    rep = {}
    sB = sparc(f, "B_cfg886_bg"); CAP["hook"] = make_hook("cap"); sBc = sparc(f, "B_cfg886_bg"); CAP["hook"] = None
    rep["sparc_bgB"] = dict(base=sB["rms"], cap=sBc["rms"], line_cap=bool(line(sBc)))
    P(f"  (reported) SPARC bg B: rms {sB['rms']:.4f} -> {sBc['rms']:.4f} line {'PASS' if line(sBc) else 'FAIL'}")
    thm = run(f, "thm"); tc = thm["clusters"]
    rep["theorem_strength"] = dict(fails=tc["fails"], zin=[tc["cells"][hk]["G-IN-Mall"]["Z"] for hk in HK], sparc=thm["sparc"]["rms"],
                                   sparc_line=bool(thm["sparc"]["line"]), groupsZ=thm["groups"]["Z"], bind=thm["stats"])
    P(f"  (reported) theorem-strength cap (progenitor's own central Q): cluster binds {thm['stats'].get('cl|h0672', [0, 0, 0])[1]}/{N}; "
      f"G-IN-Mall Z {tc['cells']['h0672']['G-IN-Mall']['Z']:+.2f} / {tc['cells']['h0686']['G-IN-Mall']['Z']:+.2f}; fails {tc['fails'] or 'none'}; "
      f"SPARC {thm['sparc']['rms']:.4f}; groups Z {thm['groups']['Z']:+.2f}")
    P("  (reported) KT-only rule: PQ does not use kT, so the KT_all cells (G-IN-all, G-OUT-all) and KT terciles above ARE the KT-only line")
    # Sigma_PQ / Sigma_HG (106 KT, h 0.672)
    KT = np.asarray(NX["KT"], float); OKK = np.isfinite(KT) & (KT > 0); MP, KEV = 1.67262192e-27, 1.602176634e-16
    rq, rb = [], []
    CAP["hook"] = make_hook("cap")
    for i in np.where(OKK)[0]:
        i = int(i); pp = prep(i, f, "h0672"); Mtot = (pp["Mfair"] + float(pp["Mb"][-1])) / MSUNE
        s_hg = 9 * (2 / 3) * KT[i] * KEV / (0.6 * MP) / (4 * math.pi * GE * 0.15 * pp["R500"] * MPCE)
        sc_, _ = ns["sig_core"](f, "A_c2b_refit", Mtot, True, ctx=("cl", pp, "h0672")); sb_, _ = ns["sig_core"](f, "A_c2b_refit", Mtot, True)
        rq.append(sc_ / s_hg); rb.append(sb_ / s_hg)
    CAP["hook"] = None; PREP.clear()
    rep["Sigma_over_HG_KT"] = dict(n=len(rq), cap=[float(np.median(rq)), float(np.percentile(rq, 16)), float(np.percentile(rq, 84))],
                                   base=[float(np.median(rb)), float(np.percentile(rb, 16)), float(np.percentile(rb, 84))])
    P(f"  (reported) Sigma/Sigma_HG ({len(rq)} KT, h 0.672): baseline median {np.median(rb):.2f} [{np.percentile(rb, 16):.2f}-{np.percentile(rb, 84):.2f}], "
      f"PS1 {np.median(rq):.2f} [{np.percentile(rq, 16):.2f}-{np.percentile(rq, 84):.2f}]")
    # per-bin pred/meas (all 326), as IB1 (h 0.672), from the graded cap run's vectors
    CAP["hook"] = make_hook("cap"); grade_clusters(f); CAP["hook"] = None
    hk = "h0672"; d = NX["DAT"][hk]; WB = d["W"] * d["B"][None, :]; nb = (WB * (d["D"] - NX["MY"]["leakP"][:, NX["HXI"][hk], 0])).sum(0)
    dC = NX["DC"][(f, hk)].sum(0); pm = (VLAST[(f, hk)].sum(0) / dC) / (nb / dC)
    rep["bin_pred_over_meas"] = pm.tolist(); P("  (reported) per-bin pred/meas, bins 0-7 (PS1): " + " ".join(f"{x:.2f}" for x in pm))
    RES["reported"][f] = rep
    P(f"  [{f} done: {time.time() - T0:.0f} s, RSS {rss():.2f} GB]")

# ------------------------------------------------------------------ F0 map + anisotropy bracket (reported)
P("\n=== (reported) F0 map: Q_core(baseline Sigma) / Q_form, bare halo at M200 / R200, no baryons")
F0 = {}
for tag in ("A_c2b_refit", "B_cfg886_bg"):
    bg = BGS[tag]; rc = 3 * (100 * bg["h"] * 1e3 / MPCE) ** 2 / (8 * math.pi * GE)
    for f in FEET:
        row = []
        for lm in (11, 12, 13, 14, 15):
            M200 = 10.0 ** lm; R200 = (3 * M200 * MSUNE / (4 * math.pi * 200 * rc)) ** (1 / 3); hal = halo_of(("bare", M200 * MSUNE, R200))
            sc = eta_of(M200) * sigma_coll(tag, M200)[0] * MSUNE / PC2; s = max(SIG[f], sc)
            row.append(q_core(s, hal)[0] / q_form(tag, M200))
        F0[f"{tag}|{f}"] = row; P(f"  [{tag} | {f}] 1e11..1e15: " + " ".join(f"{x:.3g}" for x in row))
ANI = {}; bg = BGS["A_c2b_refit"]; rc = 3 * (100 * bg["h"] * 1e3 / MPCE) ** 2 / (8 * math.pi * GE)
for lm in (12, 13, 14, 15):
    M200 = 10.0 ** lm; R200 = (3 * M200 * MSUNE / (4 * math.pi * 200 * rc)) ** (1 / 3); hal = halo_of(("bare", M200 * MSUNE, R200))
    sc = eta_of(M200) * sigma_coll("A_c2b_refit", M200)[0] * MSUNE / PC2; o, _ = q_core(max(SIG["canonical"], sc), hal, beta_r=(0.5, 0.1))
    ANI[f"1e{lm}"] = math.sqrt(o[0.5] / o[0.0])
P("  anisotropy bracket (canonical, bg A): sigma_r(beta 0.5)/sigma_r(iso) at r = 0.1 r0: " + ", ".join(f"{k} {v:.3f}" for k, v in ANI.items())
  + "  (Q scales as the inverse cube)")
RES["reported"]["F0"] = F0; RES["reported"]["anisotropy"] = ANI

# ------------------------------------------------------------------ verdict + checks
V = {f: RES["footings"][f]["cls"] for f in FEET}
RES["verdict"] = V["canonical"] if V["canonical"] == V["alt"] else f"UNDECIDED (footings disagree: {V})"
P(f"\n=== VERDICT (both footings): {RES['verdict']}")
P(f"K0 cap off reproduces X48 ng 48 (G-IN-Mall pred both h, SPARC rms; 1e-9): {'PASS' if k0 else 'FAIL'}"); checks.insert(0, ("K0", k0))
k2 = mono and (max(RESID) < 1e-8 if RESID else True)
P(f"K2 monotonic + root residual max {max(RESID) if RESID else 0:.1e} over {len(RESID)} solves: {'PASS' if k2 else 'FAIL'}"); checks.append(("K2", k2))
checks.append(("K4", rss() < 2.0))
P("\n=== CHECKS"); [P(f"  [{'PASS' if ok else 'FAIL'}] {k}") for k, ok in checks]
RES["checks"] = {k: bool(ok) for k, ok in checks}; n = sum(bool(ok) for _, ok in checks)
P(f"\nchecks {n}/{len(checks)}; runtime {time.time() - T0:.0f} s; peak RSS {rss():.2f} GB")
open(os.path.join(HERE, f"ps1_phase_space_cap{TAG}.out"), "w").write("\n".join(OUT) + "\n")
json.dump(RES, open(os.path.join(HERE, f"ps1_phase_space_cap_results{TAG}.json"), "w"), indent=1, default=float)
sys.exit(0 if n == len(checks) else 1)
