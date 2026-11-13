#!/usr/bin/env python3
"""KD1 (FROZEN_CRITERIA.md 6c7f83ed02): v3s K(Q) dust with the amplitude unpinned, graded on B1 + G9 + GB1's G1-G8.
    python3 kd1.py            -> kd1.json / kd1.out
    python3 kd1.py --mutate   -> kd1_MUTATE.json / .out   (I0 -> 0: G9a must FAIL)
Read-only use of QX3 iter2 (CLASS + PR4 lensing machinery), GB1 (loaders, features, gate functions), QX15 (theta).
kappa = 1/2 FITTED; footings never pooled; not theory closed.  1 thread."""
import os, sys, json, math
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
import numpy as np
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__)); CL = os.path.abspath(os.path.join(HERE, ".."))
MUT = "--mutate" in sys.argv; TAG = "kd1_MUTATE" if MUT else "kd1"; OUT = []
def P(s=""): print(s, flush=True); OUT.append(s)
def load_prefix(path, marker, name):
    src = open(path).read(); ns = {"__file__": path, "__name__": name}
    a = sys.argv; sys.argv = [path]
    try: exec(compile(src[:src.index(marker)], name, "exec"), ns)
    finally: sys.argv = a
    return ns

Q3 = load_prefix(os.path.join(CL, "QX3_cmb_growth", "iter2_kq_dust", "iter2.py"), 'if __name__ == "__main__":', "qx3_iter2_lib")
GB = load_prefix(os.path.join(CL, "GB1_all_gates_battery", "gb1.py"), "# ------------------------------------------------------------------ main", "gb1_lib")
Q15 = json.load(open(os.path.join(CL, "QX15_cmb_primary_likelihood", "qx15.json")))
Q3J = json.load(open(os.path.join(CL, "QX3_cmb_growth", "iter2_kq_dust", "iter2.json")))
_gs = open(os.path.join(CL, "GB1_all_gates_battery", "gb1.py")).read(); _i = _gs.index("def short(g, r):"); _j = _gs.index("for cn, mk in CANDS.items():")
exec(compile(_gs[_i:_j], "gb1_short", "exec"), GB)                                            # GB1's own row formatter
GBJ = json.load(open(os.path.join(CL, "GB1_all_gates_battery", "gb1.json")))
LIB, D3 = Q3["LIB"], Q3["D"]; Class = Q3["Class"]
CHI2_LINE, DCHI2_LINE, FCAP, GMSUN = Q3["CHI2_LINE"], Q3["DCHI2_LINE"], Q3["FCAP"], Q3["GMSUN"]
C_KMS = 299792.458
RES = dict(tag=TAG, criteria="6c7f83ed02", note="kappa = 1/2 FITTED; not theory closed", KA={}, footings={})
P(f"KD1 {'MUTATE (I0 -> 0)' if MUT else 'MAIN'}. kappa = 1/2 FITTED; not theory closed; footings never pooled.")

# ------------------------------------------------------------------ CMB helpers (QX3's, with QX15's tau)
def run_class(ob, od, h, ns, tau, pk=False):
    M = Class()
    p = {'output': 'tCl,lCl,mPk' if pk else 'tCl,lCl', 'l_max_scalars': Q3["LMAX"] + 100, 'h': h, 'omega_b': ob,
         'omega_cdm': max(od, 1e-7), 'A_s': Q3["AS0"], 'n_s': ns, 'tau_reio': tau, 'N_ur': 3.046, 'T_cmb': 2.7255}
    if pk: p.update({'P_k_max_1/Mpc': 12.0, 'z_max_pk': Q3["ZPK"]})
    M.set(p); M.compute(); return M
def chi2_fixed_amp(X, A):
    u = LIB.wsum(D3["W"], X) + LIB.wsum(D3["M"], X); r = A * u - D3["F"] - D3["d"]; return float(LIB.qform(r, D3["Cinv"]))
KG = np.logspace(-4, 1, 70); ZG = np.linspace(0.02, Q3["ZPK"], 120)
def jeans_rows(M, ob, od, H0, mus):
    X0 = Q3["X_of"](M); c0, _ = Q3["best_amp_chi2"](X0)
    Rs = Q3["growth_ratio"](M, ob, od, H0, list(mus), KG, ZG); rows = []
    for mu in mus:
        S = Q3["limber_ratio"](M, H0, KG, ZG, Rs[mu]); c, _ = Q3["best_amp_chi2"](X0 * S)
        rows.append(dict(mu=float(mu), dchi2=float(c - c0), S_L100=float(S[100]), S_L400=float(S[400])))
    return c0, rows
def mu_min_of(rows):
    for i in range(len(rows)):
        if all(x["dchi2"] <= DCHI2_LINE for x in rows[i:]): return rows[i]["mu"]
    return None

# ------------------------------------------------------------------ KA3 / KA4: QX3 iter2 corner 0
if not MUT:
    g1 = Q3J["G1"][0]; ob, H0, ns, od = g1["omega_b"], g1["H0"], g1["n_s"], g1["omega_d_best"]
    M = Q3["run_class"](ob, od, H0, ns, pk=True)
    mus3 = list(np.logspace(0, 5, 26)); c0, rows = jeans_rows(M, ob, od, H0, mus3); M.struct_cleanup()
    ref = {round(r["mu"], 3): r["dchi2"] for r in Q3J["G2"][0]["rows"]}
    dd = max(abs(r["dchi2"] - ref[round(r["mu"], 3)]) for r in rows if r["mu"] > 1e4)
    mm = mu_min_of(rows)
    ka3 = dict(chi2=float(c0), chi2_ref=g1["chi2_min"], dchi2_maxdiff_mu_gt_1e4=float(dd), mu_min=mm, mu_min_ref=Q3J["G2"][0]["mu_min"],
               ok=bool(abs(c0 - g1["chi2_min"]) <= 1e-3 and dd <= 0.05 and mm is not None and abs(mm / Q3J["G2"][0]["mu_min"] - 1) < 1e-9))
    g3r = Q3["g3"](ob, od, H0, list(np.logspace(-1, 5, 61))); mx = None
    for x in g3r:
        if x["pass_"]: mx = x["mu"]
        else: break
    ka4 = dict(mu_max=mx, ref=Q3J["G3"][0]["mu_max"], ok=bool(mx is not None and abs(mx / Q3J["G3"][0]["mu_max"] - 1) < 1e-9 and abs(mx - 79.43) < 0.01))
    RES["KA"].update(KA3=ka3, KA4=ka4)
    P(f"KA3 QX3 corner {ob},{H0},{ns}: chi2 {c0:.6f} vs {g1['chi2_min']:.6f}; Delta chi2 (mu > 1e4) max|d| {dd:.2e}; mu_min {mm} vs {Q3J['G2'][0]['mu_min']} -> {'PASS' if ka3['ok'] else 'FAIL'}")
    P(f"KA4 QX3 g3 mu_max {mx} vs {Q3J['G3'][0]['mu_max']} -> {'PASS' if ka4['ok'] else 'FAIL'}")

# ------------------------------------------------------------------ static battery (GB1, read-only)
A0, G, MS, PC, KPC = GB["A0"], GB["G"], GB["MS"], GB["PC"], GB["KPC"]
_ss = GB["ss_feat"]; GB["ss_feat"] = lambda a0, r: dict(_ss(a0, r), nodust=True)       # P4: no captured dust at the Sun
def msys_rrM(ft, a0): return (ft["r"] / ft["rrM"]) ** 2 * a0 / G / MS
BATT = {}
for f, a0 in A0.items():
    S, E, X = GB["build"](f, a0); GRp = {0: GB["groups_pts"](a0, 0.0), 1: GB["groups_pts"](a0, 1.0)}
    U = GB["udgs"](f, a0); Dd = GB["dsphs"](f, a0); K = GB["kids"](a0)
    st = GB["R1"][f"{f}|S4 v3 dmean L*floor E-W"]; sigU = math.hypot(st["se"], st["sigma_sys"]) / math.log(10)
    for p in S + E + X + [p for g in GRp[0] + GRp[1] for p in g["pts"]]:
        p["feat"]["Msys"] = msys_rrM(p["feat"], a0); p["feat"]["Mb_enc"] = p["feat"]["Mb"]
    for p in U + [p for c_ in Dd.values() for p in c_]:
        Mb = p["feat"]["Mb"]; p["feat"]["Msys"] = Mb; p["feat"]["Mb_enc"] = None if Mb is None else Mb / 2
    for ft in K[0] + K[1]: ft["Msys"] = 1e10; ft["Mb_enc"] = 1e10                            # P4: ratio 1 at R >= 0.1 Mpc
    B = dict(f=f, S=S, E=E, X=X, GR=GRp, U=U, D=Dd, K=K, sigU=sigU); B["rms_L0"] = float(np.sqrt(np.mean([p["D"] ** 2 for p in S])))
    BATT[f] = B
    cm = dict(X=np.mean([p["D"] for p in X]), E=np.mean([p["D"] for p in E]), S=np.mean([p["D"] for p in S]),
              G0=np.mean([p["D"] for g in GRp[0] for p in g["pts"]]), G1=np.mean([p["D"] for g in GRp[1] for p in g["pts"]]))
    d1 = max(abs(cm[k] - GB["KA20"][f][k]) for k in cm); um = float(np.mean([u["D"] for u in U])); d2 = abs(um - st["meanE"] / math.log(10))
    RES["KA"][f"KA1_{f}"] = dict(maxdiff=float(d1), udg_diff=float(d2), ok=bool(d1 <= 1e-6 and d2 <= 1e-9))
    P(f"[{f}] KA1 L0 class means max|d| {d1:.1e}, UDG |d| {d2:.1e} -> {'PASS' if RES['KA'][f'KA1_{f}']['ok'] else 'FAIL'}")

def enc(xi): return 1.0 if xi >= math.pi else (math.sin(xi) - xi * math.cos(xi)) / math.pi
def mj_of(ob, od, h, mu):
    rhoc0 = 3 * (100 * h) ** 2 / (8 * math.pi * GMSUN); rho_ta = 5.55 * (ob + od) / h ** 2 * rhoc0 * 27.0
    return 4 * math.pi / 3 * rho_ta * (math.pi / mu) ** 3
def KD(ob, od, h, mu, stats=None):
    ratio = FCAP * od / ob if od > 1e-6 else 0.0; MJ = mj_of(ob, od, h, mu)
    def c(ft):
        if ft.get("nodust") or ratio == 0.0: return dict(b=1.0, F=1.0, T=0.0)
        Ms_, Me = GB["need"](ft, "Msys"), GB["need"](ft, "Mb_enc")
        cap = Ms_ * (ob + od) / ob > MJ
        if stats is not None: stats["n"] += 1; stats["captured"] += cap
        if not cap: return dict(b=1.0, F=1.0, T=0.0)
        return dict(b=1.0 + ratio * Ms_ * enc(mu * ft["r"] / (1e6 * PC)) / Me, F=1.0, T=0.0)
    return c
def flat(x, p=""):
    if isinstance(x, dict):
        o = {}
        for k, v in x.items(): o.update(flat(v, p + "/" + k))
        return o
    if isinstance(x, (list, tuple)):
        o = {}
        for i, v in enumerate(x): o.update(flat(v, p + f"[{i}]"))
        return o
    return {p: x}
def grade(cand, f):
    a0 = A0[f]; B = BATT[f]; row = {}
    for gname, fn, fills in GB["GATES"]:
        r = GB["run_gate"](fn, cand, B, a0, []); row[gname] = r
    return row

# ------------------------------------------------------------------ per footing
for f in A0:
    th = Q15["footings"][f]["main"]["theta"]; h = float(Q15["footings"][f]["main"]["h"])
    ob, ns, tau = th["omega_b"], th["n_s"], th["tau"]; od = 1e-7 if MUT else th["omega_d"]
    As_fix = math.exp(th["lnAs1e10"]) / 1e10
    FO = dict(setting=dict(omega_b=ob, omega_d=od, h=h, n_s=ns, tau=tau, A_s_QX15=As_fix, source="QX15 main theta (primary CMB, footing background)"))
    Om_d = od / h ** 2; I0 = 3 * (100 * h / C_KMS) ** 2 * Om_d                                  # Mpc^-2
    FO["setting"]["I0_Mpc-2"] = I0
    # B1: analytic bounds
    a34 = 1 / 3401.0; abbn = 1 / (1 + 1e5 / (8.617333262e-5 * 2.7255)); Om_r = 2.47e-5 * (1 + 0.2271 * 3.046) / h ** 2
    w0max_a = 0.01 * a34 ** 3 / 0.99; w0max_b = 0.067 * Om_r * abbn ** 2 / max(Om_d, 1e-30)
    mu_Ba = math.sqrt(I0 / (4 * w0max_a)); mu_Bb = math.sqrt(I0 / (4 * w0max_b)); mu_B = max(mu_Ba, mu_Bb)
    def B1(mu):
        w0 = I0 / (4 * mu ** 2); wa = w0 / (w0 + a34 ** 3); rb = Om_d * w0 / (Om_r * abbn ** 2)
        return dict(mu=mu, w0=w0, w_z3400=wa, B1a=bool(wa <= 0.01), stiff_over_rad_BBN=rb, B1b=bool(rb <= 0.067))
    FO["B1"] = dict(mu_B1a=mu_Ba, mu_B1b=mu_Bb, mu_B=mu_B, a_BBN=abbn, Omega_r=Om_r)
    P(f"[{f}] setting: omega_b {ob:.6f} omega_d {od:.6f} h {h} n_s {ns:.4f} tau {tau:.4f}; I0 {I0:.4e} Mpc^-2")
    P(f"[{f}] B1 bounds: cold at z 3400 needs mu_K >= {mu_Ba:.3e} Mpc^-1; BBN stiff phase needs mu_K >= {mu_Bb:.3e} Mpc^-1")
    # G9a
    M = run_class(ob, od, h, ns, tau, pk=not MUT); X0 = Q3["X_of"](M); c_inf, Aref = Q3["best_amp_chi2"](X0)
    c_fix = chi2_fixed_amp(X0, As_fix / Q3["AS0"])
    FO["G9a_shape"] = dict(chi2_mu_inf=float(c_inf), A_s_refit=float(Aref * Q3["AS0"]), chi2_A_s_fixed_QX15=c_fix, PASS=bool(c_inf <= CHI2_LINE))
    P(f"[{f}] G9a shape (mu -> inf): chi2 {c_inf:.3f} (line {CHI2_LINE}) A_s refit {Aref*Q3['AS0']:.4e}; reported fixed-A_s (QX15 {As_fix:.4e}) chi2 {c_fix:.3f}")
    if MUT:
        stl = KD(ob, od, h, 1e6); row = grade(stl, f)
        same = all(flat(row[g]["num"]) == flat(GBJ["cands"]["L0"][f][g]["num"]) for g in row)
        FO["static_equals_L0"] = bool(same); FO["G9a_bites"] = bool(c_inf > CHI2_LINE)
        P(f"[{f}] MUTATE: G9a {'FAIL -> bites' if c_inf > CHI2_LINE else 'PASS -> NO BITE'}; static rows equal GB1 L0: {same}")
        RES["footings"][f] = FO; M.struct_cleanup(); continue
    mus = sorted({0.1, 79.43282347242821} | set(np.logspace(0, 7, 36).tolist()))
    _, rows = jeans_rows(M, ob, od, 100 * h, mus); M.struct_cleanup()
    mu_J = mu_min_of(rows); mu_star = max(mu_B, mu_J)
    FO["G9a_jeans"] = dict(rows=rows, mu_J=mu_J)
    P(f"[{f}] G9a Jeans: mu_J = {mu_J:.4e} Mpc^-1 (smallest grid mu above which Delta chi2 <= 4)")
    for r in rows:
        if r["mu"] in (0.1, 79.43282347242821) or abs(math.log10(r["mu"]) % 1) < 1e-9: P(f"[{f}]    mu {r['mu']:.4e}: Delta chi2 {r['dchi2']:9.2f}  S(L100) {r['S_L100']:.3f}")
    # the fixed setting
    def at(mu):
        rj = min(rows, key=lambda r: abs(math.log(r["mu"] / mu)))
        dch = rj["dchi2"] if mu <= rows[-1]["mu"] else 0.0
        b1 = B1(mu); g9 = bool(c_inf <= CHI2_LINE and dch <= DCHI2_LINE)
        return dict(B1=b1, G9a_dchi2_nearest_grid=dch, G9a_grid_mu=rj["mu"], G9a=g9)
    FO["mu_star"] = mu_star; FO["at_mu_star"] = at(mu_star)
    FO["converse"] = {str(m): at(m) for m in (0.1, 79.43282347242821)}
    P(f"[{f}] FIXED SETTING: omega_d {od:.6f} (I0 {I0:.4e} Mpc^-2), mu_K* = max(mu_B {mu_B:.3e}, mu_J {mu_J:.3e}) = {mu_star:.4e} Mpc^-1;"
      f" core pi/mu {math.pi/mu_star*1e6:.4f} pc, M_J {mj_of(ob, od, h, mu_star):.3e} Msun; capture ratio f_cap omega_d/omega_b = {FCAP*od/ob:.4f}")
    for m, v in FO["converse"].items():
        P(f"[{f}] converse mu {float(m):.4g}: w(z3400) {v['B1']['w_z3400']:.3g} [{'PASS' if v['B1']['B1a'] else 'FAIL'}], BBN stiff/rad {v['B1']['stiff_over_rad_BBN']:.3g} "
          f"[{'PASS' if v['B1']['B1b'] else 'FAIL'}], G9a Delta chi2 {v['G9a_dchi2_nearest_grid']:.1f} [{'PASS' if v['G9a'] else 'FAIL'}]")
    # KA2: KD at I0 = 0 equals GB1 L0
    row0 = grade(KD(ob, 0.0, h, mu_star), f); dmax = 0.0; okk = True
    for g in row0:
        a, b = flat(row0[g]["num"]), flat(GBJ["cands"]["L0"][f][g]["num"])
        okk &= (a.keys() == b.keys()) and row0[g]["status"] == GBJ["cands"]["L0"][f][g]["status"]
        for k in a:
            if isinstance(a[k], (int, float)) and not isinstance(a[k], bool) and k in b: dmax = max(dmax, abs(a[k] - b[k]))
    RES["KA"][f"KA2_{f}"] = dict(maxdiff=float(dmax), ok=bool(okk and dmax <= 1e-12))
    P(f"[{f}] KA2 KD(I0 = 0) vs gb1.json L0 on G1-G8: max|d| {dmax:.1e} -> {'PASS' if RES['KA'][f'KA2_{f}']['ok'] else 'FAIL'}")
    # static gates at the fixed setting, plus a monotonicity check at 10x and 100x mu*
    stt = dict(n=0, captured=0); cand = KD(ob, od, h, mu_star, stt); row = grade(cand, f)
    FO["static"] = row; FO["capture_stats"] = stt
    for g, r in row.items(): P(f"[{f}] KD {g:17s} {r['status']:10s} {GB['short'](g, r) if r['num'] is not None else r['missing']}")
    mono = {}
    for k in (10.0, 100.0):
        rk = grade(KD(ob, od, h, k * mu_star), f)
        mono[str(k)] = {g: rk[g]["status"] for g in rk}
    FO["monotone_status_at_10x_100x"] = mono
    # diagnostic: uniform extra-mass fraction allowed / needed per class
    a0 = A0[f]; Bf = BATT[f]
    def U_(fr): return lambda ft: dict(b=1.0 + fr, F=1.0, T=0.0)
    def sp_ok(fr): return GB["g_sparc"](U_(fr), Bf, a0)[0]
    lo, hi = 0.0, 10.0
    for _ in range(60):
        m_ = 0.5 * (lo + hi); lo, hi = (m_, hi) if sp_ok(m_) else (lo, m_)
    diag = dict(SPARC_f_max=lo, capture_f=FCAP * od / ob)
    def need_f(meanfn):
        g = lambda lf: meanfn(U_(10 ** lf))
        try: return 10 ** brentq(g, -4, 4)
        except ValueError: return None
    diag["Xcop_f_need"] = need_f(lambda c: GB["g_xcop"](c, Bf, a0)[1]["mean"])
    diag["ell_f_need"] = need_f(lambda c: GB["g_ell"](c, Bf, a0)[1]["mean"])
    diag["udg_f_need"] = need_f(lambda c: GB["g_udg"](c, Bf, a0)[1]["mean"])
    for fst in (0, 1):
        diag[f"groups_fst{fst}_f_need"] = need_f(lambda c: float(np.mean([p["D"] - GB["delta"](c, p["feat"], a0) for g in Bf["GR"][fst] for p in g["pts"]])))
    for cls in ("bright M31", "MW classical"):
        diag[f"dsph_{cls}_f_need"] = need_f(lambda c: float(np.median([p["D"] - GB["delta"](c, p["feat"], a0) for p in Bf["D"][cls]])))
    FO["uniform_f_diag"] = diag
    P(f"[{f}] diag uniform extra mass f: SPARC allows <= {lo:.4f}; cosmic capture gives {FCAP*od/ob:.3f}; needs: " +
      ", ".join(f"{k.replace('_f_need','')} {v:.3g}" for k, v in diag.items() if k.endswith("need") and v is not None))
    rmu = math.pi / mu_star; FO["near_field_cassini"] = (mu_star * 9.58 * 1.495978707e11 / (1e6 * PC)) ** 2 / 2
    P(f"[{f}] reported: linear static near-field (mu* r)^2/2 at the Cassini radius {FO['near_field_cassini']:.2e} (zero in model P: no ambient dust at the Sun)")
    RES["footings"][f] = FO

# ------------------------------------------------------------------ labels
if MUT:
    bites = all(RES["footings"][f]["G9a_bites"] and RES["footings"][f]["static_equals_L0"] for f in A0)
    RES["MUTATE_bites"] = bool(bites); P(f"MUTATE I0 -> 0: {'G9a FAILS both footings, static = L0 -> BITES' if bites else 'NO BITE'}")
else:
    ka_ok = all(v["ok"] for v in RES["KA"].values()); RES["KA_all"] = bool(ka_ok)
    table = {}; block = set()
    for f in A0:
        FO = RES["footings"][f]; s = FO["at_mu_star"]; t = {}
        t["B1a"] = "PASS" if s["B1"]["B1a"] else "FAIL"; t["B1b"] = "PASS" if s["B1"]["B1b"] else "FAIL"
        t["G9a"] = "PASS" if s["G9a"] else "FAIL"; t["G9b"] = t["G9a"]
        for g, r in FO["static"].items(): t[g.split()[0]] = r["status"]
        table[f] = t; block |= {k for k, v in t.items() if v != "PASS"}
    RES["table"] = table
    lab = ("NO VERDICT (KA FAIL)" if not ka_ok else ("one setting passes all gates" if not block else
           "FAIL: blocked by " + ", ".join(sorted(block, key=lambda x: (x[0] != 'B', x)))))
    RES["label"] = lab; P(f"LABEL: {lab}")
P("kappa = 1/2 FITTED; not theory closed.")
json.dump(RES, open(os.path.join(HERE, TAG + ".json"), "w"), indent=1, default=float)
open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n")
