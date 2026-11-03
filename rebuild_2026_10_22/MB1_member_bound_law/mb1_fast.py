#!/usr/bin/env python3
"""MB1 checks, K fit, and the fast rows (X-COP, groups, own Bullet). Usage: mb1_fast.py checks | kfit | grade [--mutate]. Outputs by mode. kappa = 1/2 FITTED; not theory closed."""
import json, math, os, sys, types
import numpy as np
import mb1_core as C, mb1_acc
MODE = sys.argv[1]; MUT = "--mutate" in sys.argv; TAG = "_MUTATE" if MUT else ""; TG2 = os.environ.get("MB1_TAG", "")
n = mb1_acc.load(); A0 = n["A0"]; FEET = n["FEET"]; ZL = n["ZL"]; TOL = n["TOL"]
OUT = open(f"mb1_{MODE}{TG2}{TAG}.out", "w")
def say(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.write(s + "\n"); OUT.flush()
def cand(arm): return types.SimpleNamespace(g=lambda Q: C.g(Q, arm), NAME=arm)
bad = []
def chk(id_, ok, msg):
    say(id_, "PASS" if ok else "FAIL", msg)
    if not ok: bad.append(id_)
# ---------- Bullet, own row
BU = n["bullet_ns"](); SYS = BU["SYS"]; GAL = BU["GAL"]; fld = BU["fld"]; law0 = SYS.extra; GRP = BU["GROUPS"]; KPC = BU["KPC"]; GG = BU["G"]; MSUN = BU["MSUN"]
def owner():
    o = {}
    for j, (ctr, ig, ii) in enumerate(GRP):
        for i in ii: o[i] = j
    return o
OWN = owner(); MST = sum(c[0] for c in GAL); MGAS = sum(c[0] for c in BU["GAS"])
def extra(sp, Cc, reg=True):
    a0 = sp["a0"]; gv = tuple(sum(q[i] for q in Cc["gas"]) for i in range(3)); gg = [gv[i] for i in range(3)]
    if reg: gg[1] = gg[1] + a0 / 1000.0
    g = np.sqrt(gg[0] ** 2 + gg[1] ** 2 + gg[2] ** 2); m = C.law(g, a0) / np.maximum(g, 1e-300); o = [gg[i] * (m - 1) for i in range(3)]; X, Y, Z = Cc["X"], Cc["Y"], Cc["Z"]
    Rs = sp["R"]; on = sp.get("on", "st")
    if on == "gas":
        s = sum(Rs[OWN.get(i, 0)] * c[0] for i, c in enumerate(GAL)) / MGAS; return tuple(o[i] + s * gv[i] for i in range(3))
    if on == "KG": return tuple(o[i] + sp["K"] * gv[i] for i in range(3))
    for i, c in enumerate(GAL):
        f = fld(X, Y, Z, c); w = Rs[OWN.get(i, 0)]
        o = [o[q] + w * f[q] for q in range(3)]
    return tuple(o)
def bullet_row(arm, f, K=0.0):
    SYS.extra = extra; a = A0[f]; Rs = [0.0, 0.0]; hist = []
    if arm in ("K", "KG"): Rs = [K, K]
    on = "KG" if arm == "KG" else ("gas" if MUT else "st")
    for it in range(1 if arm in ("K", "KG", "L") else 4):
        sp = {f: dict(form="CAND", k=0.0, a0=a, R=list(Rs), K=K, on=on)}; R = BU["run"](sp); o = BU["observe"](*R[f]); hist.append([float(x) for x in o["M300"]])
        if arm in ("K", "KG", "L"): break
        rr = np.array([300.0 * KPC * 1e0])
        for j in (0, 1):
            Rs[j] = float(C.ratio(arm, rr, np.array([o["M300"][j] * C.MS]), np.array([1.0]), a)[0])
    T = TOL["BULLET"]; zs = [(o["M300"][i] / T["obs_M300"][i] - 1) / T["sig_frac_PROVISIONAL"] for i in (0, 1)]; ok = o["cls"] != "FAIL" and all(abs(z) <= ZL for z in zs)
    SYS.extra = law0
    return dict(label="PASS" if ok else "FAIL", cls=o["cls"], R=Rs, M300=[float(x) for x in o["M300"]], ZM=zs, dkappa=[o["main"]["dkappa"], o["sub"]["dkappa"]], d_gal=[o["main"]["d_bcg"], o["sub"]["d_bcg"]], d_gas=[o["main"]["d_gas"], o["sub"]["d_gas"]], hist=hist)
def xcop(arm, f):
    R = n["rows_xcop"](cand(arm), f); return R
if MODE == "checks":
    a = A0["canonical"]; r = np.geomspace(1e21, 1e23, 40); gg = 1e-12 * np.ones(40) * (r / 1e22) ** -1; gs = 0.1 * gg; tiny = 1e-30
    o = C.one("F", r, gg, gs, tiny); chk("K1", np.max(np.abs(o / (gg + gs) - 1)) < 1e-6, f"a0 tiny, max |g/Newton - 1| {np.max(np.abs(o / (gg + gs) - 1)):.2e}")
    gb = np.geomspace(1e-14, 1e-6, 50); wrong = 0.0
    for s in ("disc", "dwarf", "lens", "planet", "MW", "probe", "merger"):
        v = C.g(n["Q"](gb=gb, gg=gb * .5, gs=gb * .5, r=gb * 0 + 3e20, a0=a, sample=s), "F"); wrong = max(wrong, float(np.max(np.abs(v / (gb * (.5 + np.sqrt(.25 + a / gb))) - 1))))
    chk("K2", wrong < 1e-12, f"non-listed samples against the law, max {wrong:.1e}")
    rr = np.array([3e22]); Mc = np.array([1e45]); gam = np.array([1.0]); m = np.array([1e10 * C.MS]); num = C.rt_hill(rr, Mc, gam, m, a)[0, 0]; cl = math.sqrt(rr[0] ** 3 * math.sqrt(a * m[0] / C.G) / (2 * Mc[0])); chk("K3", abs(num / cl - 1) < .02, f"r_t {num / 3.0857e19:.1f} kpc against deep closed form {cl / 3.0857e19:.1f}, {100 * (num / cl - 1):+.2f} %, M_i 1e10, r 1 Mpc")
    os.environ["MB1_BASE"] = "x"; C.BASE = "law"; RX = xcop("L", "canonical"); C.BASE = "gas"; chk("K5", abs(abs(RX["B23"]["value"]) - .467) < .002 and abs(RX["B24"]["value"] - .476) < .002, f"plain law through this path: mean {RX['B23']['value']:+.3f}, rms {RX['B24']['value']:.3f}, against 0.467, 0.476")
    SYS.extra = law0
    f = "canonical"; lc = types.SimpleNamespace(g=lambda Q: C.law(np.asarray(dict.__getitem__(Q, "gb"), float), Q["a0"])); L = n["rows_bullet"](lc)[f]["B28"]; chk("K4a", abs(L["M300"][0] / 1.11e14 - 1) < .01 and abs(L["M300"][1] / .73e14 - 1) < .01, f"law M300 {L['M300'][0]:.3e}, {L['M300'][1]:.3e}, against 1.11e14, 0.73e14")
    SYS.extra = law0; sp = {f: dict(form="LAW", k=0.0, a0=A0[f])}; S0, m0 = BU["run"](sp)[f]; M2D, sig_pl, APS, XX, YY = BU["M2D"], BU["sig_pl"], BU["APS"], BU["XX"], BU["YY"]; BCG1, BCG3, GASM, GASB = BU["BCG1"], BU["BCG3"], BU["GASM"], BU["GASB"]; a_ = 150.0; tgt = np.array([BU["OBS300"]["BCG1"] - m0["BCG1"], BU["OBS300"]["BCG3"] - m0["BCG3"]])
    AA = np.array([[M2D(*BCG1, 300.0, [(1.0, a_, *BCG1)]), M2D(*BCG1, 300.0, [(1.0, a_, *BCG3)])], [M2D(*BCG3, 300.0, [(1.0, a_, *BCG1)]), M2D(*BCG3, 300.0, [(1.0, a_, *BCG3)])]]); Mc2 = np.linalg.solve(AA, tgt); cl = {}
    for lab, cen in (("onBCG", (BCG1, BCG3)), ("onGas", (GASM, GASB))):
        pl = [(Mc2[0], a_, *cen[0]), (Mc2[1], a_, *cen[1])]; S = S0 + sig_pl(np.hypot(XX - cen[0][0], YY - cen[0][1]), Mc2[0], a_) + sig_pl(np.hypot(XX - cen[1][0], YY - cen[1][1]), Mc2[1], a_); mm = {q: m0[q] + M2D(*c, Rq, pl) for q, (c, Rq) in APS.items()}; cl[lab] = BU["observe"](S, mm)["cls"]
    chk("K4b", cl["onBCG"] == "PASS" and cl["onGas"] == "FAIL", str(cl)); say("needed extra on BCGs, 1e14:", [round(float(x) / 1e14, 3) for x in Mc2], "model stars, 1e14, by component:", [(round(c[0] / 1e14, 3), c[1]) for c in GAL], "gas:", [(round(c[0] / 1e14, 3), c[1]) for c in BU["GAS"]])
    v0 = xcop("F", "canonical")["B23"]["value"]; lm0, w0, m0_ = C.LM, C.W, C.M; lm = np.linspace(8.0, 12.5, 73); x_ = 10 ** (lm - 10.9); w = x_ ** (C.ALPHA + 1) * np.exp(-x_); C.LM, C.W, C.M = lm, w / w.sum(), 10 ** lm * C.MS; v1 = xcop("F", "canonical")["B23"]["value"]; C.LM, C.W, C.M = lm0, w0, m0_; chk("K-grid", abs(v1 - v0) < .0043, f"F's X-COP mean moves {v1 - v0:+.5f} dex at twice the mass points, value not printed")
    say("checks failed:", bad or "none"); sys.exit(1 if bad else 0)
if MODE == "kfit":
    res = {}
    for arm in ("K", "KG"):
        res[arm] = {}
        for f in FEET:
            lo, hi = 0.0, 200.0 if arm == "K" else 30.0
            def mean(k):
                c = types.SimpleNamespace(g=lambda Q, k=k: _g(Q, k)); return n["rows_xcop"](c, f)["B23"]["value"]
            def _g(Q, k):
                old = C.kfit; C.kfit = lambda a_, b_: k
                try: return C.g(Q, arm)
                finally: C.kfit = old
            for _ in range(40):
                mid = .5 * (lo + hi); v = mean(mid)
                if abs(v) < 1e-4: break
                if v > 0: lo = mid
                else: hi = mid
            res[arm][f] = mid; say(arm, f, f"K {mid:.4f}, X-COP mean {v:+.5f}")
    json.dump(res, open("mb1_kfit.json", "w"), indent=1); sys.exit(0)
if MODE == "grade":
    out = {}; arms = sys.argv[2].split(",") if len(sys.argv) > 2 and not sys.argv[2].startswith("--") else ["F", "E", "N", "K", "KG"]
    KF = json.load(open("mb1_kfit.json"))
    for arm in arms:
        out[arm] = {}
        for f in FEET:
            K = KF[arm][f] if arm in KF else 0.0; X = xcop(arm, f); Gp = n["rows_groups"](cand(arm), f)["B1"]; row = dict(B23=X["B23"], B24=X["B24"], B25=X["B25"], B1=Gp, K=K)
            if "--no-bullet" not in sys.argv: row["Bullet"] = bullet_row(arm, f, K)
            out[arm][f] = row; b = row.get("Bullet", {})
            say(arm, f, f"X-COP mean {X['B23']['value']:+.3f} ({X['B23']['label']}), rms {X['B24']['value']:.3f} ({X['B24']['label']}); B25 {X['B25']['label']} Z {X['B25']['Z']:+.2f}; groups Z {Gp['Z']:+.2f} {Gp['label']}" + (f"; K {K:.3f}" if K else "") + (f"; Bullet {b['label']} {b['cls']}, M300 {b['M300'][0] / 1e14:.2f}, {b['M300'][1] / 1e14:.2f}, Z {b['ZM'][0]:+.2f}, {b['ZM'][1]:+.2f}, dkappa {b['dkappa'][0]:+.3f}, {b['dkappa'][1]:+.3f}, R {b['R'][0]:.2f}, {b['R'][1]:.2f}" if b else ""))
    json.dump(out, open(f"mb1_grade{TG2}{TAG}.json", "w"), indent=1, default=float)
    if MUT:
        bs = [out[arms[0]][f]["Bullet"] for f in FEET]; lost = all(b["cls"] == "FAIL" and all(x < 0 for x in b["dkappa"]) for b in bs)
        say("MUTATE", arms[0], "caught: sign lost on both footings" if lost else "NOT caught"); sys.exit(1 if lost else 0)
