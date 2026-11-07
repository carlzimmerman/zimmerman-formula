#!/usr/bin/env python3
"""GL1 (FROZEN_CRITERIA.md 3ed2133753): re-read the sector-side CMB-lensing labels that rest on QX3 iter2's
`limber_ratio`, with the lensing potential's k^-4 restored: weight x (chi/(L + 1/2))^n, n = 0 (record), 4 (corrected),
2 (MUTATE). Every lane's own code is imported / exec'd read-only; no other lane's file is written.
    python3 gl1.py            -> gl1.json / gl1.out
    python3 gl1.py --mutate   -> gl1_MUTATE.json / gl1_MUTATE.out
GATE: labels are held until GL2 reads CONFIRMED (HOLD_KERNEL_REREAD_2026_11_07.md); this script reports WOULD MOVE / STANDS.
Cold dark energy, never dark matter; no particle. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math, io, contextlib, resource, time
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[v] = "1"
sys.dont_write_bytecode = True
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "../.."))
CL6 = os.path.join(REPO, "closure_2026_11_06"); CL7 = os.path.join(REPO, "closure_2026_11_07")
MUT = "--mutate" in sys.argv; TAG = "gl1_MUTATE" if MUT else "gl1"; OUT = []; T0 = time.time()
def P(s=""): print(s, flush=True); OUT.append(str(s))
def J(p): return json.load(open(p))

# ---------------------------------------------------------------- the kernel switch (one function, exponent n)
D2 = os.path.join(CL6, "QX3_cmb_growth", "iter2_kq_dust"); D3 = os.path.join(CL6, "QX3_cmb_growth", "iter3_barotropic_family")
sys.path.insert(0, D2)
cwd0 = os.getcwd(); os.chdir(D2)
with contextlib.redirect_stdout(io.StringIO()): import iter2 as I2
os.chdir(cwd0)
ORIG = I2.limber_ratio
NPOW = {"n": 0}
def limber_n(M, H0, kgrid, zgrid, R):
    """I2.limber_ratio's code with the weight x (chi/(L + 1/2))^n (n = 0 is the record's arithmetic)."""
    n = NPOW["n"]
    chis = M.angular_distance(1089.0) * (1 + 1089.0)
    chi = np.array([M.angular_distance(z) * (1 + z) for z in zgrid])
    lnk = np.log(kgrid)
    Pm = np.array([[M.pk_lin(k, z) for z in zgrid] for k in kgrid])
    w = ((chis - chi) / (chi * chis)) ** 2 * (1 + np.asarray(zgrid)) ** 2 / np.array([M.Hubble(z) for z in zgrid])
    Ls = np.arange(2, I2.LMAX + 1); num = np.zeros(len(Ls)); den = np.zeros(len(Ls))
    for j in range(len(zgrid)):
        kk = (Ls + 0.5) / chi[j]; m = (kk >= kgrid[0]) & (kk <= kgrid[-1])
        Pj = np.interp(np.log(kk[m]), lnk, Pm[:, j]); Rj = np.interp(np.log(kk[m]), lnk, R[:, j])
        ex = (chi[j] / (Ls[m] + 0.5)) ** n if n else 1.0
        num[m] += w[j] * Pj * Rj ** 2 / chi[j] ** 2 * ex; den[m] += w[j] * Pj / chi[j] ** 2 * ex
    S = np.ones(I2.LMAX + 1); ok = den > 0; S[Ls[ok]] = num[ok] / den[ok]
    return S
I2.limber_ratio = limber_n                                   # every importer of the module `iter2` now calls this
def at(n, f, *a, **k):
    NPOW["n"] = n
    try: return f(*a, **k)
    finally: NPOW["n"] = 0
RES = dict(lane="GL1", tag=TAG, criteria="3ed2133753", hold="labels held until GL2 reads CONFIRMED", KA={}, labels={},
           note="kappa = 1/2 FITTED; not theory closed")

# ---------------------------------------------------------------- QX3 iter3 prefix (worst corner; also QX7's background)
s3 = open(os.path.join(D3, "iter3.py")).read(); c3 = s3.index("# K: beta = 0")
os.chdir(D3); os.environ.pop("QX3_MUTATE", None); argv0 = sys.argv; sys.argv = [os.path.join(D3, "iter3.py")]
N3 = {"__file__": os.path.join(D3, "iter3.py"), "__name__": "iter3_reused"}
with contextlib.redirect_stdout(io.StringIO()): exec(compile(s3[:c3], os.path.join(D3, "iter3.py"), "exec"), N3)
os.chdir(cwd0); sys.argv = argv0
assert N3["I2"] is I2, "iter3 must import the same iter2 module object"
MC = N3["M"]; kgrid, zgrid, ref, X0, c0 = N3["kgrid"], N3["zgrid"], N3["ref"], N3["X0"], float(N3["c0"])

# KA: n = 0 equals the original function
Rt = 1 - 0.1 * np.outer(np.tanh(kgrid), np.exp(-zgrid / 2))
s_or = ORIG(MC, N3["H0"], kgrid, zgrid, Rt); s_n0 = at(0, limber_n, MC, N3["H0"], kgrid, zgrid, Rt)
d0 = float(np.max(np.abs(s_n0 / s_or - 1)))
RES["KA"]["KA0_function"] = dict(max_rel=d0, pass_=bool(d0 <= 1e-12))
P(f"KA0 function: patched n = 0 vs original limber_ratio on a test R: max rel {d0:.1e} -> {'PASS' if d0 <= 1e-12 else 'FAIL'}")

# KA4 / MUTATE shape: absolute Limber C_L^pp shape / CLASS pp, normalised at L 100
LS = (20, 50, 100, 200, 300, 400)
def shape(n):
    chis = MC.angular_distance(1089.0) * 1090.0; chi = np.array([MC.angular_distance(z) * (1 + z) for z in zgrid])
    Hz = np.array([MC.Hubble(z) for z in zgrid]); lnk = np.log(kgrid)
    Pm = np.array([[MC.pk_lin(k, z) for z in zgrid] for k in kgrid]); dz = np.gradient(zgrid); out = []
    for L in LS:
        kk = (L + 0.5) / chi; m = (kk >= kgrid[0]) & (kk <= kgrid[-1]); v = 0.0
        for j in np.where(m)[0]:
            v += ((chis - chi[j]) / (chi[j] * chis)) ** 2 * (1 + zgrid[j]) ** 2 / Hz[j] * math.exp(np.interp(math.log(kk[j]), lnk, np.log(Pm[:, j]))) / chi[j] ** 2 * (chi[j] / (L + 0.5)) ** n * dz[j]
        out.append(v)
    pp = MC.raw_cl(500)["pp"]; r = np.array(out) / pp[list(LS)]; return (r / r[2]).tolist()
SH = {n: shape(n) for n in (0, 2, 4)}
for n in (0, 2, 4): P(f"shape n = {n}: Limber C_L^pp / CLASS pp (norm. L 100) at L {LS}: " + " ".join(f"{x:.3f}" for x in SH[n]))
RES["shape"] = {str(n): SH[n] for n in SH}
ka4 = max(abs(x - 1) for x in SH[4]) <= 0.03; ka4b = max(abs(x - 1) for x in SH[0]) > 0.03
RES["KA"]["KA4_shape"] = dict(n4_within_3pc=bool(ka4), n0_off=bool(ka4b), pass_=bool(ka4 and ka4b))
P(f"KA4 n = 4 within 3 % of CLASS: {ka4}; n = 0 off: {ka4b} -> {'PASS' if ka4 and ka4b else 'FAIL'}")

if MUT:
    m2 = max(abs(x - 1) for x in SH[2]) > 0.03
    diff0 = max(abs(a / b - 1) for a, b in zip(SH[2], SH[0])) > 0.03; diff4 = max(abs(a / b - 1) for a, b in zip(SH[2], SH[4])) > 0.03
    RES["MUTATE"] = dict(n2_fails_shape=bool(m2), differs_from_n0=bool(diff0), differs_from_n4=bool(diff4), bites=bool(m2 and diff0 and diff4))
    P(f"MUTATE n = 2: fails shape {m2}; differs from n 0 {diff0}; from n 4 {diff4} -> {'BITES' if RES['MUTATE']['bites'] else 'DOES NOT BITE'}")
else:
    # ------------------------------------------------------------ L2 QX3 iter2: 8 corners
    it2 = J(os.path.join(D2, "iter2.json")); mus = np.logspace(0, 5, 26)
    KG = np.logspace(-4, 1, 70); ZG = np.linspace(0.02, I2.ZPK, 120)
    L2 = []; ka_l2 = 0.0
    for r, g in zip(it2["G1"], it2["G2"]):
        M = I2.run_class(r["omega_b"], r["omega_d_best"], r["H0"], r["n_s"], pk=True); X = I2.X_of(M); cc, _ = I2.best_amp_chi2(X)
        Rs = I2.growth_ratio(M, r["omega_b"], r["omega_d_best"], r["H0"], list(mus), KG, ZG)
        rows = {}
        for n in (0, 4):
            rr = []
            for mu in mus:
                S = at(n, I2.limber_ratio, M, r["H0"], KG, ZG, Rs[mu]); c, _ = I2.best_amp_chi2(X * S); rr.append(dict(mu=float(mu), dchi2=float(c - cc)))
            mm = None
            for i in range(len(rr)):
                if all(x["dchi2"] <= I2.DCHI2_LINE for x in rr[i:]): mm = rr[i]["mu"]; break
            rows[n] = dict(rows=rr, mu_min=mm)
        ka_l2 = max(ka_l2, max(abs(a["dchi2"] - b["dchi2"]) for a, b in zip(rows[0]["rows"], g["rows"])))
        L2.append(dict(corner=g["corner"], mu_min_record=g["mu_min"], mu_min_n0=rows[0]["mu_min"], mu_min_n4=rows[4]["mu_min"],
                       dchi2_n4_at_mu1=rows[4]["rows"][0]["dchi2"], rows_n4=rows[4]["rows"]))
        M.struct_cleanup()
        P(f"L2 corner {g['corner']}: mu_min record {g['mu_min']:.4g}, n0 {rows[0]['mu_min']:.4g}, n4 {rows[4]['mu_min'] if rows[4]['mu_min'] is None else format(rows[4]['mu_min'], '.4g')}; dchi2(n4) at mu 1 {rows[4]['rows'][0]['dchi2']:+.3f}, at mu 10 {rows[4]['rows'][5]['dchi2']:+.3f}")
    RES["KA"]["KA0_L2"] = dict(max_abs=ka_l2, pass_=bool(ka_l2 <= 1e-9))
    mw4 = None if any(x["mu_min_n4"] is None for x in L2) else max(x["mu_min_n4"] for x in L2)
    mumax = it2["mu_max_best"]
    mv = bool(mw4 is not None and mw4 <= mumax)
    RES["labels"]["L2_QX3_iter2"] = dict(record=it2["label"], mu_min_worst_record=it2["mu_min_worst"], mu_min_worst_n4=mw4, mu_max_best=mumax,
                                         corners=L2, would_move=mv, reading=("WOULD MOVE: window exists (mu_min <= mu_max)" if mv else "STANDS"))
    P(f"L2 QX3 iter2: mu_min_worst record {it2['mu_min_worst']:.4g} -> n4 {mw4}; mu_max {mumax:.4g}: {'WOULD MOVE (window)' if mv else 'STANDS'}; KA0 max |d| {ka_l2:.1e}")

    # ------------------------------------------------------------ L3 QX3 iter3: the 35 analytic cells
    it3 = J(os.path.join(D3, "iter3.json")); L3 = []; ka3 = 0.0
    for e in it3["evaluated"]:
        R = N3["solve"](e["beta"], e["mu0"]) / ref; out = {}
        for n in (0, 4):
            S = at(n, I2.limber_ratio, MC, N3["H0"], kgrid, zgrid, R); c, _ = I2.best_amp_chi2(X0 * S); out[n] = float(c - c0)
        ka3 = max(ka3, abs(out[0] - e["dchi2"])); L3.append(dict(beta=e["beta"], mu0=e["mu0"], record=e["dchi2"], n4=out[4]))
    RES["KA"]["KA0_L3"] = dict(max_abs=ka3, pass_=bool(ka3 <= 1e-9))
    p3 = [x for x in L3 if x["n4"] <= I2.DCHI2_LINE]
    RES["labels"]["L3_QX3_iter3"] = dict(record=it3["label"], n_cells=len(L3), best_record=min(x["record"] for x in L3), best_n4=min(x["n4"] for x in L3),
                                         n_pass_n4=len(p3), cells=L3, would_move=bool(p3), reading=(f"WOULD MOVE: {len(p3)}/{len(L3)} cells pass G2'" if p3 else "STANDS"))
    P(f"L3 QX3 iter3: {len(L3)} cells; best dchi2 record {min(x['record'] for x in L3):.2f} -> n4 {min(x['n4'] for x in L3):.3f}; pass at n4 {len(p3)}/{len(L3)}; KA0 max |d| {ka3:.1e}")

    # ------------------------------------------------------------ QX7 generalised solver (iter_3's block, as iter_4 / CE2 use it)
    Q7 = os.path.join(CL6, "QX7_unified_cold_switch"); S7 = open(os.path.join(Q7, "iter_3_de_fraction_switch", "qx7_iter3.py")).read()
    blk = S7[S7.index("# ---- generalised G2' solver"):S7.index("d_iter3 = g2(")]
    OL0 = MC.Omega_Lambda(); H0c_ = MC.Hubble(0.0)
    def ode(z): return OL0 / (MC.Hubble(z) / H0c_) ** 2
    LOC = dict(np=np, N3=N3, I2=I2, MC=MC, H0=N3["H0"], ode=ode); exec(blk, LOC); solve_gen, kJ_of = LOC["solve_gen"], LOC["kJ_of"]
    def g2both(lst, p):
        R = solve_gen(kJ_of(lst, p)) / ref; o = {}
        for n in (0, 4):
            S = at(n, I2.limber_ratio, MC, N3["H0"], kgrid, zgrid, R); c, _ = I2.best_amp_chi2(X0 * S); o[n] = (float(c), float(c - c0))
        return o
    # L4 QX7 iter_3
    q3 = J(os.path.join(Q7, "iter_3_de_fraction_switch", "qx7_iter3.json")); L4 = []; ka4_ = 0.0
    for e in q3["evaluated"]:
        o = g2both(e["lambda_star"], e["p"]); ka4_ = max(ka4_, abs(o[0][1] - e["dchi2"])); L4.append(dict(lambda_star=e["lambda_star"], p=e["p"], record=e["dchi2"], n4=o[4][1]))
    RES["KA"]["KA0_L4"] = dict(max_abs=ka4_, pass_=bool(ka4_ <= 1e-9))
    p4 = [x for x in L4 if x["n4"] <= I2.DCHI2_LINE]
    RES["labels"]["L4_QX7_iter3"] = dict(record=q3["label"], n_cells=len(L4), best_record=min(x["record"] for x in L4), best_n4=min(x["n4"] for x in L4),
                                         n_pass_n4=len(p4), cells=L4, would_move=bool(p4), reading=(f"WOULD MOVE: G2' window {len(p4)}/{len(L4)} (the other gates are analytic and already passed)" if p4 else "STANDS"))
    P(f"L4 QX7 iter_3: {len(L4)} cells; best record {min(x['record'] for x in L4):.2f} -> n4 {min(x['n4'] for x in L4):.3f}; window at n4 {len(p4)}/{len(L4)}; KA0 max |d| {ka4_:.1e}")
    # L5 QX7 iter_4
    q4 = J(os.path.join(Q7, "iter_4_late_evaporation", "qx7_iter4.json")); L5 = []; ka5 = 0.0; t5 = time.time()
    for e in q4["evaluated"]:
        o = g2both(e["lambda_star"], e["p"]); ka5 = max(ka5, abs(o[0][1] - e["dchi2"])); L5.append(dict(lambda_0=e["lambda_0"], p=e["p"], lambda_star=e["lambda_star"], record=e["dchi2"], n4=o[4][1]))
    RES["KA"]["KA0_L5"] = dict(max_abs=ka5, n=len(L5), pass_=bool(ka5 <= 1e-9))
    win4 = [x for x in L5 if x["n4"] <= I2.DCHI2_LINE]; cl = q4["cluster_vs_lambda0_galaxyok"]
    def clpass(l0):
        pr = cl[f"{l0:.4g}"]; return {f: bool(pr[f]["X_pass"] and pr[f]["groups_strict"]) for f in pr}
    newm = [x for x in win4 if x["record"] > I2.DCHI2_LINE]
    clrows = {f"{l0:.4g}": clpass(l0) for l0 in sorted({x["lambda_0"] for x in win4})}
    anyboth = [k for k, v in clrows.items() if all(v.values())]
    RES["labels"]["L5_QX7_iter4"] = dict(record=q4["label"], n_cells=len(L5), window_record=len(q4["window"]), window_n4=len(win4), new_members=len(newm),
                                         lambda0_in_window_n4=sorted({x["lambda_0"] for x in win4}), cluster_pass_by_lambda0=clrows,
                                         would_move=bool(anyboth), reading=("WOULD MOVE: a window member passes clusters on both footings" if anyboth else f"STANDS: FAIL (clusters) [0/{len(win4)} both footings]"),
                                         cells=L5)
    P(f"L5 QX7 iter_4: {len(L5)} cells ({time.time() - t5:.0f} s); window record {len(q4['window'])} -> n4 {len(win4)} (+{len(newm)}); lambda_0 in window: {len(clrows)} values; cluster pass both footings at {anyboth or 'none'}; KA0 max |d| {ka5:.1e}")
    # L7 CE2 cells + M3
    CELLS = {"C1": (2.6102, 4.25), "C2": (1.4678, 3.5), "C3": (8.254, 5.625), "C4": (2.1544, 3.75)}
    ce2m = J(os.path.join(CL7, "CE2_late_heated_window", "ce2_MUTATE.json"))["MUTATE"]["M3"]
    L7 = {}
    for cn, (l0, p) in CELLS.items():
        e = min((e for e in q4["evaluated"] if abs(e["p"] - p) < 1e-9), key=lambda e: abs(math.log(e["lambda_0"] / l0)))
        o = g2both(e["lambda_star"], e["p"]); L7[cn] = dict(record=e["dchi2"], n0=o[0][1], n4_chi2=o[4][0], n4=o[4][1], pass_n4=bool(o[4][0] <= 18.48 and o[4][1] <= 4))
        if cn == "C1": e1 = e
    o = g2both(10 * e1["lambda_star"], e1["p"])
    m3 = dict(record_chi2=ce2m["GL"]["chi2"], record_dchi2=ce2m["GL"]["dchi2"], n0_dchi2=o[0][1], n4_chi2=o[4][0], n4_dchi2=o[4][1], GF_pass_record=ce2m["GF_pass"],
              bites_n4=bool(not ((o[4][0] <= 18.48 and o[4][1] <= 4) and ce2m["GF_pass"])))
    RES["KA"]["KA0_L7"] = dict(max_abs=max(max(abs(v["n0"] - v["record"]) for v in L7.values()), abs(o[0][1] - ce2m["GL"]["dchi2"])), pass_=bool(max(max(abs(v["n0"] - v["record"]) for v in L7.values()), abs(o[0][1] - ce2m["GL"]["dchi2"])) <= 1e-9))
    gl_moves = not m3["bites_n4"]
    RES["labels"]["L7_CE2"] = dict(cells=L7, M3=m3, would_move=bool(gl_moves),
                                   reading=("WOULD MOVE: CE2 GL -> NO VERDICT (M3 no longer bites through GL; GF " + ("passes" if ce2m["GF_pass"] else "fails") + "); CE2 overall FAIL (GX, GG, GB) is kernel-free and stays") if gl_moves else
                                           ("STANDS: GL PASS at C1-C4; M3 still bites" + (" (through GF, not GL)" if not (o[4][0] > 18.48 or o[4][1] > 4) else " through GL")))
    P("L7 CE2: " + "; ".join(f"{c} record {v['record']:.3f} n4 {v['n4']:+.3f}" for c, v in L7.items()) + f"; M3 record dchi2 {m3['record_dchi2']:.1f} -> n4 chi2 {m3['n4_chi2']:.2f} dchi2 {m3['n4_dchi2']:+.2f} (GF record {'PASS' if m3['GF_pass_record'] else 'FAIL'}) -> M3 {'bites' if m3['bites_n4'] else 'NO BITE'}")
    # L8 CK4 (quoted)
    ck = J(os.path.join(CL7, "CK4_kicked_carrier_cosmology", "ck4.json")); ckm = J(os.path.join(CL7, "CK4_kicked_carrier_cosmology", "ck4_MUTATE.json"))
    m1 = ckm["MUTATE"]["M1"]["row"]
    RES["labels"]["L8_CK4"] = dict(primary={k: dict(frozen=v["GL"], n4=v["GLc"]) for k, v in ck["rows"].items() if k.endswith("_1e11") and k.startswith("B_")},
                                   M1=dict(frozen=m1["GL"], n4=m1["GLc"]), would_move=bool(not m1["GLc"]["pass_"]),
                                   reading="STANDS: GL NO VERDICT (M1 does not bite at n 0 or n 4)" if m1["GLc"]["pass_"] else "WOULD MOVE: M1 bites at n 4")
    P(f"L8 CK4 (quoted): M1 frozen dchi2 {m1['GL']['dchi2']:+.2f}, n4 {m1['GLc']['dchi2']:+.2f} -> {RES['labels']['L8_CK4']['reading']}")

    # ------------------------------------------------------------ L6 KD1 (and L10 SE1 arm a)
    kd = J(os.path.join(CL6, "KD1_unpinned_kq_dust", "kd1.json")); L6 = {}; ka6 = 0.0
    KG6 = np.logspace(-4, 1, 70); ZG6 = np.linspace(0.02, I2.ZPK, 120)
    for f, F in kd["footings"].items():
        st = F["setting"]; M = I2.Class()
        M.set({'output': 'tCl,lCl,mPk', 'l_max_scalars': I2.LMAX + 100, 'h': st["h"], 'omega_b': st["omega_b"], 'omega_cdm': st["omega_d"], 'A_s': I2.AS0,
               'n_s': st["n_s"], 'tau_reio': st["tau"], 'N_ur': 3.046, 'T_cmb': 2.7255, 'P_k_max_1/Mpc': 12.0, 'z_max_pk': I2.ZPK}); M.compute()
        X = I2.X_of(M); cc, _ = I2.best_amp_chi2(X); rec = F["G9a_jeans"]["rows"]; ms = [r["mu"] for r in rec]
        Rs = I2.growth_ratio(M, st["omega_b"], st["omega_d"], 100 * st["h"], ms, KG6, ZG6); out = {0: [], 4: []}
        for mu in ms:
            for n in (0, 4):
                S = at(n, I2.limber_ratio, M, 100 * st["h"], KG6, ZG6, Rs[mu]); c, _ = I2.best_amp_chi2(X * S); out[n].append(float(c - cc))
        M.struct_cleanup()
        ka6 = max(ka6, max(abs(a - r["dchi2"]) for a, r in zip(out[0], rec)))
        def mmin(d):
            for i in range(len(d)):
                if all(x <= I2.DCHI2_LINE for x in d[i:]): return ms[i]
            return None
        mJ4 = mmin(out[4]); muB = F["B1"]["mu_B"]
        conv = {f"{m:g}": dict(record=next(r["dchi2"] for r in rec if abs(r["mu"] / m - 1) < 1e-9), n4=out[4][[i for i, x in enumerate(ms) if abs(x / m - 1) < 1e-9][0]]) for m in (0.1, 79.43282347242821)}
        L6[f] = dict(mu_J_record=F["G9a_jeans"]["mu_J"], mu_J_n0=mmin(out[0]), mu_J_n4=mJ4, mu_B=muB, mu_star_record=max(muB, F["G9a_jeans"]["mu_J"]),
                     mu_star_n4=max(muB, mJ4 or 0.0), converse=conv, rows=[dict(mu=m, record=r["dchi2"], n4=x) for m, r, x in zip(ms, rec, out[4])])
        P(f"L6 KD1 [{f}]: mu_J record {F['G9a_jeans']['mu_J']:.4g} -> n4 {mJ4}; mu_B {muB:.4g}; mu* {L6[f]['mu_star_record']:.4g} -> {L6[f]['mu_star_n4']:.4g}; converse G9a dchi2 at mu 0.1 {conv['0.1']['record']:.1f} -> {conv['0.1']['n4']:+.2f}, at 79.43 {conv['79.4328']['record']:.1f} -> {conv['79.4328']['n4']:+.2f}")
    RES["KA"]["KA0_L6"] = dict(max_abs=ka6, pass_=bool(ka6 <= 1e-9))
    star_moves = any(abs(v["mu_star_n4"] / v["mu_star_record"] - 1) > 1e-9 for v in L6.values())
    conv_moves = any(v["converse"][k]["n4"] <= 4 and v["converse"][k]["record"] > 4 for v in L6.values() for k in v["converse"])
    RES["labels"]["L6_KD1"] = dict(footings=L6, mu_star_moves=bool(star_moves), converse_G9a_moves=bool(conv_moves), would_move=bool(star_moves),
                                   reading=("FAIL STANDS (mu_K* = mu_B, BBN, kernel-free)" + ("; sub-label WOULD MOVE: at galaxy-allowed mu_K G9a passes, so the converse block is B1a/B1b only (CMB lensing no longer blocks)" if conv_moves else "")))
    RES["labels"]["L10_SE1_arm_a"] = dict(follows="L6", reading=RES["labels"]["L6_KD1"]["reading"])
    P(f"L6 KD1: {RES['labels']['L6_KD1']['reading']}; KA0 max |d| {ka6:.1e}")

    # ------------------------------------------------------------ L9 QX10 iter_1 J1 (own copy of the formula)
    Q10 = os.path.join(CL6, "QX10_window_hardening", "iter_1_primary_cmb", "qx10_i1.py"); s10 = open(Q10).read()
    N10 = {"__file__": Q10, "__name__": "qx10_i1_reused"}; argv0 = sys.argv; sys.argv = [Q10]
    with contextlib.redirect_stdout(io.StringIO()): exec(compile(s10[:s10.index('if __name__ == "__main__":')], Q10, "exec"), N10)
    sys.argv = argv0
    js = s10[s10.index("def jcheck():"):s10.index("def peak_fit(")]
    old_w = "num[m] += w[j] * Pj * Rj ** 2 / chi[j] ** 2; den[m] += w[j] * Pj / chi[j] ** 2"
    old_d = 'json.dump(res, open(os.path.join(HERE, "jcheck.json"), "w"), indent=1)'
    assert old_w in js and old_d in js
    js = js.replace(old_w, "ex = (chi[j] / (Ls[m] + 0.5)) ** NPOW_Q10; num[m] += w[j] * Pj * Rj ** 2 / chi[j] ** 2 * ex; den[m] += w[j] * Pj / chi[j] ** 2 * ex")
    js = js.replace(old_d, "return res").replace("print(cname, json.dumps(res[\"cells\"][cname]), flush=True)", "pass")
    exec(compile(js, "jcheck_gl1", "exec"), N10)
    rec10 = J(os.path.join(os.path.dirname(Q10), "jcheck.json"))["cells"]; L9 = {}; ka9 = 0.0
    for n in (0, 4):
        N10["NPOW_Q10"] = n
        with contextlib.redirect_stdout(io.StringIO()): r10 = N10["jcheck"]()
        for c, v in r10["cells"].items():
            L9.setdefault(c, dict(record_J1_dchi2=rec10[c]["J1_dchi2_TT"], record_J1=rec10[c]["J1"], record_max1mS=rec10[c]["max_abs_1mS"]))
            L9[c][f"n{n}_J1_dchi2"] = v["J1_dchi2_TT"]; L9[c][f"n{n}_J1"] = v["J1"]; L9[c][f"n{n}_max1mS"] = v["max_abs_1mS"]
            if n == 0: ka9 = max(ka9, abs(v["J1_dchi2_TT"] - rec10[c]["J1_dchi2_TT"]))
    RES["KA"]["KA0_L9"] = dict(max_abs=ka9, pass_=bool(ka9 <= 1e-9))
    mv9 = [c for c, v in L9.items() if v["n4_J1"] != v["record_J1"]]
    RES["labels"]["L9_QX10_iter1_J1"] = dict(cells=L9, would_move=bool(mv9), reading=(f"WOULD MOVE: J1 changes at {mv9}" if mv9 else "STANDS"))
    P("L9 QX10 iter_1 J1: " + "; ".join(f"{c} record {v['record_J1_dchi2']:.3f} ({'PASS' if v['record_J1'] else 'FAIL'}) -> n4 {v['n4_J1_dchi2']:.4f} ({'PASS' if v['n4_J1'] else 'FAIL'}), max|1-S| {v['record_max1mS']:.3f} -> {v['n4_max1mS']:.4f}" for c, v in L9.items()) + f"; KA0 max |d| {ka9:.1e}")
    RES["labels"]["L1_QX3_iter1"] = dict(reading="STANDS (kernel-free: (k_J/k)^2 on (L, z), no Limber weight)")

    P("\nSUMMARY (held until GL2 CONFIRMED):")
    for k, v in RES["labels"].items(): P(f"  {k}: {v['reading']}")
    P("KA: " + "; ".join(f"{k} {'PASS' if v['pass_'] else 'FAIL'}" for k, v in RES["KA"].items()))

RES["peak_rss_MB"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6; RES["seconds"] = time.time() - T0
P(f"peak RSS {RES['peak_rss_MB']:.0f} MB; {RES['seconds']:.0f} s. kappa = 1/2 FITTED; not theory closed.")
def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, np.floating): return float(o)
    if isinstance(o, np.bool_): return bool(o)
    if isinstance(o, np.ndarray): return clean(o.tolist())
    return o
json.dump(clean(RES), open(os.path.join(HERE, TAG + ".json"), "w"), indent=1)
open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n")
