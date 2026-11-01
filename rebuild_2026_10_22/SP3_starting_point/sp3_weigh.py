#!/usr/bin/env python3
"""SP3 direct weighing by UR3's method, its code read only: DiskMass r, Milky Way box. Hand core on NR2's S table; native on ZN2 A1's z = 0 shapes. kappa = 1/2 FITTED, unused; not theory closed."""
import contextlib, io, json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); UD = os.path.join(RB, "UR3_direct_weighing"); sys.path.insert(0, UD); import ur3_common as U
MUT = "--mutate" in sys.argv; OUT = []; TAG = "A_c2b_refit"; FQ = 0.872
def P(s): print(s, flush=True); OUT.append(s)
T0 = U.T; NR2T = json.load(open(os.path.join(HERE, "sp3_hand_results.json")))["Stable"]; TB = json.load(open(os.path.join(HERE, "sp3_tables.json"))); Z = json.load(open(os.path.join(RB, "ZN2_native_profile_sparc_groups", "zn2_low_shapes.json"))); ZX = np.log(np.array(Z["x"])); ZT = sorted(((float(Z[m]["0.00"]["lgM"]), np.array(Z[m]["0.00"]["lnm"])) for m in ("1e10", "1e11", "1e12", "1e13", "1e14")), key=lambda a: a[0])
FC = (lambda r: r / (1 + r))(json.load(open(os.path.join(RB, "RET1_retention_replaces_em1", "ret1_results.json")))["RNAT"])
S = dict(line="EM1", shape="hand", map="tot", mode="off", mh=1.0)
def lnm(lg):
    if lg <= ZT[0][0]: return ZT[0][1]
    if lg >= ZT[-1][0]: return ZT[-1][1]
    k = next(i for i in range(len(ZT) - 1) if ZT[i][0] <= lg <= ZT[i + 1][0]); w = (lg - ZT[k][0]) / (ZT[k + 1][0] - ZT[k][0]); return (1 - w) * ZT[k][1] + w * ZT[k + 1][1]
def M0nat(rg, M, rc):
    Mt = M / FC; R_ = (3 * (Mt if S["map"] == "tot" else M) / (4 * math.pi * 200 * rc)) ** (1 / 3); ln = lnm(math.log10(Mt)); lx = np.log(np.minimum(rg, R_) / R_); return M * np.exp(np.where(lx >= ZX[0], np.interp(lx, ZX, ln), ln[0] + 2 * (lx - ZX[0])))
def rcof(t): bg = U.T["bg"][t]; return 3 * (100 * bg["h"] / 1e3) ** 2 / (8 * math.pi * U.G)
def line(lMb, t):
    bg = U.T["bg"][t]
    if S["line"] == "EM1": return bg["a"] + bg["b"] * (lMb - 10)
    if S["line"] == "FAIR200": return math.log10(FC / (1 - FC)) + lMb
    q = TB[S["line"]][t]; return float(np.interp(lMb, q["x"], q["y"]))
def halo(lMb, t, d=0.0):
    lM = line(lMb, t) + d + math.log10(S["mh"]); M = 10 ** lM; R = (3 * M / (4 * math.pi * 200 * rcof(t))) ** (1 / 3)
    if S["shape"] == "native": return M, R, 1.0, 1.0
    s = U.Sfn(lM, t); return M, R, s, U.r0_of(M, R, s)
def Mc(rg, Mbg, M, R, S_, r0, mode):
    if S["shape"] == "nfw": c = 12.95; mu = lambda x: np.log1p(x) - x / (1 + x); M0 = M * mu(rg / (R / c)) / mu(c)
    elif S["shape"] == "native": M0 = M0nat(rg, M, rcof(TAG))
    else: M0 = math.pi * S_ * r0 ** 2 * U.Bs(rg / r0)
    if S["mode"] == "off": return M0
    Mf = U.contract(rg, Mbg, M0, float(Mbg[-1] / M0[-1]))[0]; return M0 + (FQ if S["mode"] == "fq" else 1.0) * (Mf - M0)
# heads of UR3's scripts, exec'd unchanged, then its names pointed here
s = open(os.path.join(UD, "ur3_diskmass.py")).read(); s = s[:s.index('R = {}; P("UR3 Part A')]; DN = {"__file__": os.path.join(UD, "ur3_diskmass.py"), "__name__": "h"}; exec(compile(s, "ur3a", "exec"), DN); DN["halo"] = halo; DN["Mc"] = Mc
s = open(os.path.join(UD, "ur3_mw.py")).read(); s = s[:s.index('g["MODE"].update(')]; MN = {"__file__": os.path.join(UD, "ur3_mw.py"), "__name__": "m"}; exec(compile(s, "ur3b", "exec"), MN); MN["halo"] = halo; MN["Mc"] = Mc
def weigh(**kw):
    S.update(dict(line="EM1", shape="hand", map="tot", mode="off", mh=1.0)); S.update(kw); a = DN["run"](S["mode"]); m = MN["g2"](MN["MCM"], TAG, S["mode"]); rows = [MN["g2"](c["bar"], TAG, S["mode"]) for c in MN["CELLS"]]; c = MN["classify"](rows)
    mc = float(Mc(np.array([1.0, 8.178, 300.0]), np.array([0.0, 0.0, 0.0]) + 1.0, *halo(math.log10(MN["MCM"]["Mb"]), TAG), "off")[1]) if S["mode"] == "off" else None
    return dict(r=a["r"], Y=a["Y"], n=a["n"], fc=a["fc"], cls=c["cls"], n_all=c["n_all"], D=(c.get("best_in_prior") or {}).get("D"), Vc=m["vc_R0"], Kz=m["K_R0"], M200=math.log10(halo(math.log10(MN["MCM"]["Mb"]), TAG)[0]), Mc_R0=mc, reached=bool(0.90 <= a["r"] <= 1.10 and a["n"] >= 27))
def show(l, a): P(f"{l:30s} r {a['r']:.3f} Y_K {a['Y']:.3f} n {a['n']} halo share {a['fc']:.2f} {'REACHED' if a['reached'] else 'not'} | MW {a['cls']} all4 {a['n_all']} | McM Vc {a['Vc']:.1f} Kz {a['Kz']:.1f} lgM200 {a['M200']:.2f}" + (f" Mc(<R0) {a['Mc_R0']:.2e}" if a["Mc_R0"] else ""))
R = {}; P("SP3 weighing, UR3's method; kappa = 1/2 FITTED, unused; not theory closed. Lines: r in [0.90, 1.10], n >= 27; MW FEASIBLE IN PRIORS")
U.T = T0; P("K4, UR3's own S table (NR1):")
for l, kw, want in (("EM1 hand off", dict(), 1.365), ("EM1 hand blum", dict(mode="blum"), 1.071), ("EM1 nfw off", dict(shape="nfw"), 1.090)):
    a = weigh(**kw); show(l, a); R["K4|" + l] = a; assert abs(a["r"] - want) <= 0.002, (l, a["r"], want)
U.T = NR2T
if MUT:
    b = weigh(shape="native"); m = weigh(shape="native", mh=2.0); P(f"MUTATE halo x 2, native EM1 off: r {b['r']:.3f} -> {m['r']:.3f}"); ok = abs(m["r"] - b["r"]) >= 0.02; open(os.path.join(HERE, "sp3_weigh_MUTATE.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(0 if ok else 1)
for ln in ("EM1", "E1", "C1", "FAIR200", "AM1"):
    for mo in ("off", "blum"):
        a = weigh(line=ln, shape="hand", mode=mo); R[f"hand|{ln}|{mo}"] = a; show(f"hand {ln} {mo}", a)
    for mn in ("tot", "fc1"):
        for mo in ("off", "fq"):
            a = weigh(line=ln, shape="native", map=mn, mode=mo); R[f"native-{mn}|{ln}|{mo}"] = a; show(f"native {mn} {ln} {mo}", a)
json.dump(R, open(os.path.join(HERE, "sp3_weigh.json"), "w"), indent=1, default=float); open(os.path.join(HERE, "sp3_weigh.out"), "w").write("\n".join(OUT) + "\n")
