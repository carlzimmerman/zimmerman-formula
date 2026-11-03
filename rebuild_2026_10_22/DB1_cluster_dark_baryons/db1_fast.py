#!/usr/bin/env python3
"""DB1 checks, lambda fit, fast rows (X-COP, groups B1), own Bullet, MG1 sign rows, label control.
Usage: db1_fast.py checks | fit | grade [--mutate] | mg1 [--mutate] | control. Outputs by mode. kappa = 1/2 FITTED; not theory closed."""
import io, json, math, os, sys, types
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
sys.dont_write_bytecode = True
import numpy as np
np.seterr(all="ignore")
import db1_core as C, db1_acc
MODE = sys.argv[1]; MUT = "--mutate" in sys.argv; TAG = "_MUTATE" if MUT else ""; TG2 = os.environ.get("DB1_TAG", "")
n = db1_acc.load(); A0 = n["A0"]; FEET = n["FEET"]; ZL = n["ZL"]; TOL = n["TOL"]
OUT = open(f"db1_{MODE}{TG2}{TAG}.out", "w")
def say(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.write(s + "\n"); OUT.flush()
def cand(arm): return types.SimpleNamespace(g=lambda Q: C.g(Q, arm), NAME=arm)
lawc = types.SimpleNamespace(g=lambda Q: C.law(np.asarray(dict.__getitem__(Q, "gb"), float), Q["a0"]), NAME="law")
bad = []
def chk(id_, ok, msg):
    say(id_, "PASS" if ok else "FAIL", msg)
    if not ok: bad.append(id_)
ARMS = ("P1", "P1G", "P2", "P3")
def lamj(): return json.load(open("db1_lambda.json"))
# ---------- Bullet, own row (UX6's model through RQ3's bullet_ns, unedited)
BU = n["bullet_ns"](); SYS = BU["SYS"]; GAL = BU["GAL"]; GAS = BU["GAS"]; fld = BU["fld"]; law0 = SYS.extra; GRP = BU["GROUPS"]; KPC = BU["KPC"]; MSUN = BU["MSUN"]; enc = BU["enc_table"]
OWN = {}
for j, (ctr, ig, ii) in enumerate(GRP):
    for i in ii: OWN[i] = j
MGAS = sum(c[0] for c in GAS); MST = [sum(GAL[i][0] for i in ii) for (_, _, ii) in GRP]; MGJ = [sum(GAS[i][0] for i in ig) for (_, ig, _) in GRP]
T_BULLET = (14.0, 6.0)  # keV, PROVISIONAL (recalled, Markevitch's Chandra work), P2 only
def sub_profiles(j):
    ctr, ig, ii = GRP[j]; r, mg = enc([GAS[i] for i in ig], ctr, True); _, ms = enc([GAL[i] for i in ii], ctr, False); return r, mg, ms
def bullet_R(arm, f, L):
    a = A0[f]; Rs = []
    for j in range(len(GRP)):
        r, mg, ms = sub_profiles(j); mg3 = float(np.interp(300.0, r, mg)); ms3 = float(np.interp(300.0, r, ms))
        if arm == "Z": Rs.append(0.0)
        elif arm == "P1": Rs.append(L * MGJ[j] / MST[j])
        elif arm == "P1G": Rs.append(L * mg3 / ms3)
        elif arm == "P3":
            rr = 300.0 * KPC; gg = C.G * mg3 * MSUN / rr ** 2; gs = C.G * ms3 * MSUN / rr ** 2; gx = float(C.p3_gx(np.array([gg + gs]), np.array([gg]), np.array([gs]), a)[0]); Rs.append(gx * rr ** 2 / C.G / MSUN / ms3)
        elif arm == "P2":
            ctr, ig, ii = GRP[j]; rk = np.geomspace(1.0, 3000.0, 600); rho = sum(3 * GAS[i][0] / (4 * math.pi * GAS[i][1] ** 3) * (1 + rk ** 2 / GAS[i][1] ** 2) ** -2.5 for i in ig)
            ne = np.maximum(rho, 1e-30) * MSUN / KPC ** 3 / (1.17 * C.MP) / 1e6; rc = C.rcool_from(rk, ne, np.full_like(rk, T_BULLET[j])); Rs.append(L * (float(np.interp(rc, r, mg)) if rc > 0 else 0.0) / MST[j])
    return Rs
def mk_extra(Rs, on):
    def extra(sp, Cc, reg=True):
        a0 = sp["a0"]; gv = tuple(sum(q[i] for q in Cc["gas"]) for i in range(3)); gb = [gv[i] + Cc["st"][i] for i in range(3)]
        if reg: gb[1] = gb[1] + a0 / 1000.0
        if on == "gas":
            s = sum(Rs[j] * MST[j] for j in range(len(MST))) / MGAS; cb = [s * gv[i] for i in range(3)]
        else:
            cb = [0.0, 0.0, 0.0]
            for i, c in enumerate(GAL):
                w = Rs[OWN.get(i, 0)]
                if w:
                    fq = fld(Cc["X"], Cc["Y"], Cc["Z"], c); cb = [cb[q] + w * fq[q] for q in range(3)]
        tot = [gb[i] + cb[i] for i in range(3)]; g = np.sqrt(tot[0] ** 2 + tot[1] ** 2 + tot[2] ** 2); m = C.law(g, a0) / np.maximum(g, 1e-300)
        return tuple(tot[i] * m - gb[i] for i in range(3))
    return extra
def bullet_row(arm, f, L, Rs=None, on="gal"):
    Rs = bullet_R(arm, f, L) if Rs is None else Rs; SYS.extra = mk_extra(Rs, on)
    try:
        sp = {f: dict(form="CAND", k=0.0, a0=A0[f])}; R = BU["run"](sp); o = BU["observe"](*R[f])
    finally: SYS.extra = law0
    T = TOL["BULLET"]; zs = [(o["M300"][i] / T["obs_M300"][i] - 1) / T["sig_frac_PROVISIONAL"] for i in (0, 1)]; ok = o["cls"] != "FAIL" and all(abs(z) <= ZL for z in zs)
    return dict(label="PASS" if ok else "FAIL", cls=o["cls"], R=[float(x) for x in Rs], Mcb=[float(Rs[j] * MST[j]) for j in range(len(MST))], M300=[float(x) for x in o["M300"]], ZM=zs, dkappa=[o["main"]["dkappa"], o["sub"]["dkappa"]], d_gal=[o["main"]["d_bcg"], o["sub"]["d_bcg"]], d_gas=[o["main"]["d_gas"], o["sub"]["d_gas"]])
# ---------- X-COP, own replica of the harness's mean (for the planted check only)
def xcop_rows():
    from astropy.io import fits
    D = C.XDIR; XC = []; li = lambda r, m, t: float(10 ** np.interp(np.log10(t), np.log10(r), np.log10(m))) if r[0] <= t <= r[-1] else np.nan
    for name in sorted(os.listdir(D)):
        p = os.path.join(D, name)
        if not (os.path.isdir(p) and os.path.exists(os.path.join(p, f"{name}_mstar.fits"))): continue
        with fits.open(os.path.join(p, f"{name}_hydro_mass.fits")) as h: hm = h[1].data.copy(); r5 = h[1].header["R500"]
        with fits.open(os.path.join(p, f"{name}_fgas_profile.fits")) as h: ga = h[1].data.copy(); rg = h[1].header["R500"]
        with fits.open(os.path.join(p, f"{name}_mstar.fits")) as h: st = h[2].data.copy()
        for x in (.1, .2, .3, .5, .7):
            r = x * r5; mh, mg, ms = li(hm["RADIUS"], hm["M_FORW"], r), li(ga["RADIUS"] * rg, ga["MGAS"], r), li(st["RADIUS"], st["MSTAR"], r)
            if np.all(np.isfinite([mh, mg, ms])): XC.append(dict(n=name, r=r * 1e3 * C.PCm, r5=r5 * 1e3 * C.PCm, mh=mh, mg=mg, ms=ms))
    return XC
def xcop_model(XC, arm, a):
    rr = np.array([z["r"] for z in XC]); mg = np.array([z["mg"] for z in XC]); ms = np.array([z["ms"] for z in XC]); gb = C.G * (mg + ms) * C.MS / rr ** 2
    v = C.g(n["Q"](gb=gb, gg=C.G * mg * C.MS / rr ** 2, gs=C.G * ms * C.MS / rr ** 2, r=rr, r500=np.array([z["r5"] for z in XC]), a0=a, sample="cluster"), arm); return v * rr ** 2 / C.G / C.MS
def bisect(fun, lo, hi, it=60):
    flo = fun(lo)
    for _ in range(it):
        mid = 0.5 * (lo + hi); v = fun(mid)
        if abs(v) < 1e-5: break
        if (v > 0) == (flo > 0): lo, flo = mid, v
        else: hi = mid
    return mid, v
def fit_one(arm, f, hi=60.0):
    def mean(L):
        C.LAM = L
        try: return n["rows_xcop"](cand(arm), f)["B23"]["value"]
        finally: C.LAM = None
    if mean(hi) > 0: return float("nan"), mean(hi)
    return bisect(mean, 0.0, hi)

if MODE == "checks":
    a = A0["canonical"]
    for f in FEET:
        X0 = n["rows_xcop"](lawc, f); XZ = n["rows_xcop"](cand("Z"), f); G0 = n["rows_groups"](lawc, f)["B1"]; GZ = n["rows_groups"](cand("Z"), f)["B1"]
        dx = max(abs(X0[k]["value"] - XZ[k]["value"]) for k in ("B23", "B24")); chk(f"K1-xcop-{f}", dx < 1e-12 and (f != "canonical" or (abs(X0["B23"]["value"] - .467) < .002 and abs(X0["B24"]["value"] - .476) < .002)), f"lambda 0 against the law: |d| {dx:.1e}; law mean {X0['B23']['value']:+.4f}, rms {X0['B24']['value']:.4f}")
        chk(f"K1-groups-{f}", abs(G0["Z"] - GZ["Z"]) < 1e-12, f"B1 Z {GZ['Z']:+.4f} against the law {G0['Z']:+.4f}")
    B = bullet_row("Z", "canonical", 0.0); chk("K1-bullet", abs(B["M300"][0] / 1.11e14 - 1) < .01 and abs(B["M300"][1] / .73e14 - 1) < .01, f"lambda 0 Bullet M300 {B['M300'][0]:.3e}, {B['M300'][1]:.3e}, dkappa {B['dkappa'][0]:+.3f}, {B['dkappa'][1]:+.3f}; law 1.11e14, 0.73e14, UX6 -0.068, -0.111")
    gb = np.geomspace(1e-14, 1e-6, 50); wrong = 0.0
    for s in ("disc", "dwarf", "lens", "planet", "MW", "probe", "merger", "et", "tdg", "udg", "gc", "df", "deep"):
        for arm in ARMS:
            C.LAM = 3.0; v = C.g(n["Q"](gb=gb, gg=gb * .5, gs=gb * .5, r=gb * 0 + 3e20, a0=a, sample=s), arm); C.LAM = None
            wrong = max(wrong, float(np.max(np.abs(v / (gb * (.5 + np.sqrt(.25 + a / gb))) - 1))))
    chk("K2", wrong < 1e-12, f"non-hot samples against the law, all arms, max {wrong:.1e}")
    XC = xcop_rows(); mh = np.array([z["mh"] for z in XC]); dl = np.log10(mh / xcop_model(XC, "Z", a)).mean(); hv = n["rows_xcop"](lawc, "canonical")["B23"]["value"]
    C.LAM = 3.0; mock = xcop_model(XC, "P1G", a); C.LAM = None
    def mm(L):
        C.LAM = L
        try: return float(np.log10(mock / xcop_model(XC, "P1G", a)).mean())
        finally: C.LAM = None
    Lr, v = bisect(mm, 0.0, 60.0); chk("K3", abs(dl - hv) < 1e-12 and abs(Lr / 3.0 - 1) < .01, f"replica law mean {dl:+.6f} against harness {hv:+.6f}; planted lambda 3.0 recovered {Lr:.4f}")
    SYS.extra = law0; f = "canonical"; sp = {f: dict(form="LAW", k=0.0, a0=A0[f])}; S0, m0 = BU["run"](sp)[f]; M2D, sig_pl, APS, XX, YY = BU["M2D"], BU["sig_pl"], BU["APS"], BU["XX"], BU["YY"]; BCG1, BCG3, GASM, GASB = BU["BCG1"], BU["BCG3"], BU["GASM"], BU["GASB"]; a_ = 150.0; tgt = np.array([BU["OBS300"]["BCG1"] - m0["BCG1"], BU["OBS300"]["BCG3"] - m0["BCG3"]])
    AA = np.array([[M2D(*BCG1, 300.0, [(1.0, a_, *BCG1)]), M2D(*BCG1, 300.0, [(1.0, a_, *BCG3)])], [M2D(*BCG3, 300.0, [(1.0, a_, *BCG1)]), M2D(*BCG3, 300.0, [(1.0, a_, *BCG3)])]]); Mc2 = np.linalg.solve(AA, tgt); cl = {}
    for lab, cen in (("onBCG", (BCG1, BCG3)), ("onGas", (GASM, GASB))):
        pl = [(Mc2[0], a_, *cen[0]), (Mc2[1], a_, *cen[1])]; S = S0 + sig_pl(np.hypot(XX - cen[0][0], YY - cen[0][1]), Mc2[0], a_) + sig_pl(np.hypot(XX - cen[1][0], YY - cen[1][1]), Mc2[1], a_); mm_ = {q: m0[q] + M2D(*c, Rq, pl) for q, (c, Rq) in APS.items()}; cl[lab] = BU["observe"](S, mm_)["cls"]
    chk("K4", cl["onBCG"] == "PASS" and cl["onGas"] == "FAIL", str(cl) + f"; needed extra on BCGs, law: {[round(float(x) / 1e14, 3) for x in Mc2]} e14")
    T = C.xcop_table(); say("r_cool kpc, r_cool/r500:", {k: (round(v["rcool"] / C.KPC), round(v["rcool_x"], 3)) for k, v in T.items()}, "median", round(C.rcool_ratio(), 4))
    say("checks failed:", bad or "none"); sys.exit(1 if bad else 0)

if MODE == "fit":
    res = {}
    for arm in ("P1", "P1G", "P2"):
        res[arm] = {}
        for f in FEET:
            L, v = fit_one(arm, f, 400.0 if arm == "P2" else 60.0); res[arm][f] = L; say(arm, f, f"lambda {L:.4f}, X-COP mean {v:+.6f}")
    json.dump(res, open("db1_lambda.json", "w"), indent=1); sys.exit(0)

if MODE == "grade":
    out = {}; LJ = lamj(); arms = ["P1G"] if MUT else list(ARMS)
    for arm in arms:
        out[arm] = {}
        for f in FEET:
            L = 1.0 if arm == "P3" else LJ[arm][f]; X = n["rows_xcop"](cand(arm), f); Gp = n["rows_groups"](cand(arm), f)["B1"]; row = dict(B23=X["B23"], B24=X["B24"], B25=X["B25"], B1=Gp, lam=L)
            row["Bullet"] = b = bullet_row(arm, f, L, on="gas" if MUT else "gal"); out[arm][f] = row
            say(arm, f, f"lambda {L:.3f}; X-COP mean {X['B23']['value']:+.3f} ({X['B23']['label']}), rms {X['B24']['value']:.3f} ({X['B24']['label']}); B25 {X['B25']['label']} Z {X['B25']['Z']:+.2f}; groups Z {Gp['Z']:+.2f} {Gp['label']}; Bullet {b['label']} {b['cls']}, M300 {b['M300'][0] / 1e14:.2f}, {b['M300'][1] / 1e14:.2f}, Z {b['ZM'][0]:+.2f}, {b['ZM'][1]:+.2f}, dkappa {b['dkappa'][0]:+.3f}, {b['dkappa'][1]:+.3f}, R {b['R'][0]:.2f}, {b['R'][1]:.2f}, M_cb {b['Mcb'][0] / 1e14:.2f}, {b['Mcb'][1] / 1e14:.2f} e14")
    json.dump(out, open(f"db1_grade{TG2}{TAG}.json", "w"), indent=1, default=float)
    if MUT:
        bs = [out["P1G"][f]["Bullet"] for f in FEET]; lost = all(b["cls"] == "FAIL" and all(x < 0 for x in b["dkappa"]) for b in bs)
        say("MUTATE P1G on the gas:", "caught, Bullet FAIL with dkappa < 0 at both, both footings" if lost else "NOT caught"); sys.exit(1 if lost else 0)
    sys.exit(0)

if MODE == "mg1":
    p = os.path.join(C.RB, "MG1_merger_sample", "mg1_merger.py"); s = open(p).read().split('say("=" * 90); say("MG1_merger_sample"')[0]; a_ = 'OUT = open(os.path.join(HERE, f"mg1_merger{TAG}.out"), "w")'; assert s.count(a_) == 1
    s = s.replace(a_, "import io as _io; OUT = _io.StringIO()"); m = {"__file__": p, "__name__": "mg1_in_db1"}; exec(compile(s, p, "exec"), m)
    def extra(form, k, a0, gas, star, s_, Cc, tabs, reg=True):
        gv, st = Cc["g"], Cc["st"]; gb = [gv[i] + st[i] for i in range(3)]
        if reg: gb[1] = gb[1] + a0 / 1000.0
        if form == "CBgas": cb = [k * star[0] / gas[0] * gv[i] for i in range(3)]
        elif form == "CB": cb = [k * st[i] for i in range(3)]
        else: cb = [0.0, 0.0, 0.0]
        tot = [gb[i] + cb[i] for i in range(3)]; g = np.sqrt(tot[0] ** 2 + tot[1] ** 2 + tot[2] ** 2); mm_ = C.law(g, a0) / np.maximum(g, 1e-300); return tuple(tot[i] * mm_ - gb[i] for i in range(3))
    m["extra"] = extra; LJ = lamj(); out = {}; tally = {}
    encp = lambda M, a, r: M * r ** 3 / (r * r + a * a) ** 1.5
    for r in m["rows"]:
        t = f"{r['system']} {r['sub']}"; lab = m["label"](r["d_lens_gal"], r["e_lens_gal"], r["d_lens_gas"], r["e_lens_gas"])[0]; prim = r["counted"] == "yes" and r["s"] / r["e_lens_gas"] > 2
        mg3, ms3 = encp(r["M_gas"], r["a_gas"], 300.0), encp(r["M_star"], r["a_star"], 300.0); specs = {}
        for f in FEET:
            a = A0[f]; rr = 300.0 * KPC; gg = C.G * mg3 * MSUN / rr ** 2; gs = C.G * ms3 * MSUN / rr ** 2
            Rd = dict(P1=LJ["P1"][f] * r["M_gas"] / r["M_star"], P1G=LJ["P1G"][f] * mg3 / ms3, P3=float(C.p3_gx(np.array([gg + gs]), np.array([gg]), np.array([gs]), a)[0]) * rr ** 2 / C.G / MSUN / ms3)
            for arm, R in Rd.items():
                if MUT and arm != "P1G": continue
                specs[f"{arm}|{f}"] = ("CBgas" if MUT else "CB", R, a)
            if not MUT: specs[f"LAW|{f}"] = ("LAW", 0.0, a)
        res, _ = m["run_pair"]((r["M_gas"], r["a_gas"]), (r["M_star"], r["a_star"]), r["s"], specs); out[t] = dict(label=lab, primary=prim, rows=res)
        say(t, lab, "primary" if prim else "-", " ".join(f"{k} {v['dkappa']:+.3f}" for k, v in sorted(res.items())))
        if prim and lab == "GAL":
            for k, v in res.items(): tally.setdefault(k, [0, 0]); tally[k][0] += v["dkappa"] > 0; tally[k][1] += 1
    say("primary GAL rows with dkappa > 0:", {k: f"{v[0]} of {v[1]}" for k, v in sorted(tally.items())}); say("P2 not computable on MG1 rows: no temperature in the table")
    json.dump(dict(rows=out, tally=tally), open(f"db1_mg1{TAG}.json", "w"), indent=1, default=float)
    if MUT:
        lost = all(v[0] == 0 for v in tally.values()); say("MUTATE MG1, P1G on the gas:", "caught, no GAL row keeps dkappa > 0" if lost else "NOT caught"); sys.exit(1 if lost else 0)
    sys.exit(0)

if MODE == "control":
    res = {}; LJ = lamj()
    for sh in range(1, 7):
        C.PERM = sh; res[sh] = {}
        for f in FEET:
            L, v = fit_one("P1", f); C.LAM = L; X = n["rows_xcop"](cand("P1"), f); C.LAM = None; res[sh][f] = dict(lam=L, B24=X["B24"]["value"], B25=X["B25"]["Z"])
            say(f"P1 label control, shift {sh}{' (frozen primary)' if sh == 1 else ' (reported only)'}", f, f"lambda {L:.3f}, rms {X['B24']['value']:.4f} ({X['B24']['label']}), B25 Z {X['B25']['Z']:+.2f}")
    C.PERM = 0
    for f in FEET:
        L = LJ["P1"][f]; Rs = bullet_R("P1", f, L); b = bullet_row("P1", f, L, Rs=Rs[::-1]); res[f"bullet_swap_{f}"] = b
        say("P1 Bullet with main and sub ratios swapped", f, f"{b['label']} {b['cls']}, M300 {b['M300'][0] / 1e14:.2f}, {b['M300'][1] / 1e14:.2f}, dkappa {b['dkappa'][0]:+.3f}, {b['dkappa'][1]:+.3f}")
    json.dump(res, open("db1_control.json", "w"), indent=1, default=float); sys.exit(0)
