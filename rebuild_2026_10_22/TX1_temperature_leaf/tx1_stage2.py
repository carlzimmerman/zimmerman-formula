#!/usr/bin/env python3
"""TX1 cheap gates on named forms, real rows. python3 -I tx1_stage2.py FOOT LIST.json OUT.json. G3, G5, G5b, G2', G4', LT, groups, dwarfs, IC 1613, DiskMass, G14 lensing, Cassini. Law first. kappa = 1/2 FITTED; not theory closed."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tx1_lib import *
foot, lst, outf = sys.argv[1:4]; S = install(("real", 1500)); import bk2_read as Rd, bk2_gates as Gg
Rd.xcop = lambda a0, which=None: xrows(a0, which, "real", "ho"); Gt = Rd.Gates(foot, "real"); a0 = Gt.a0
sys.path.insert(0, os.path.join(RB, "BF3_all_gates_first")); import bf3_common as C3
os.makedirs(os.path.join(LANE, "chunks", "bf3_cache"), exist_ok=True); C3.LANE = os.path.join(LANE, "chunks", "bf3_cache"); Ex = C3.Exact(foot)
def lens(f):
    Le = Ex.Le; Tb = np.zeros((len(Le.LMG), 60))
    for i, lm in enumerate(Le.LMG):
        MB, _ = Le.baryon(float(lm)); gb = Le.Gpc * MB / Le.RGRID ** 2 * Ex.SIk; gg = Le.Gpc * (MB - 10 ** float(lm)) / Le.RGRID ** 2 * Ex.SIk; r = Le.RGRID * 3.0857e16; dl = np.gradient(np.log(MB), np.log(r)); ci = np.r_[np.cumsum((0.5 * (gb[1:] + gb[:-1]) * np.diff(r))[::-1])[::-1], 0.0]; L = B._local(gb - gg, gg, r, dl, r * gb + ci + gb[-1] * r[-1], a0); g = ev(f, L); Tb[i] = Ex.st.dsig(MB * g / gb, "linear")
    m = Le.stack(Ex.L, Tb)
    if not np.all(np.isfinite(m)): return None
    return dict(cov=Ex.chi(m, Ex.Yn, Ex.Cn)[0], sys=Ex.chi(m, Ex.Yn, Ex.Csys)[0])
def split(f):
    X = xrows(a0, None); d = np.log10(X["go"] / ev(f, X)); nm = X["name"]; u = sorted(set(nm)); cm = {c: float(d[nm == c].mean()) for c in u}; sc = {c: float(d[nm == c].std(ddof=1) / math.sqrt((nm == c).sum())) for c in u}; Zc = {c: cm[c] / math.hypot(sc[c], .12) for c in u}; M = {c: tload()[c]["M500"] for c in u}; md = np.median(list(M.values())); hi = [cm[c] for c in u if M[c] > md]; lo = [cm[c] for c in u if M[c] <= md]; se = math.sqrt(np.var(hi, ddof=1) / len(hi) + np.var(lo, ddof=1) / len(lo)); Zd = (np.mean(hi) - np.mean(lo)) / se; return dict(cm=cm, Zc=Zc, Zd=float(Zd), ok=bool(all(abs(v) <= 2 for v in Zc.values()) and abs(Zd) <= 2))
FS = ["I1(gb,a0)"] + [f for f in json.load(open(lst)) if f != "I1(gb,a0)"]; out = []; lawsys = None
for f in FS:
    c = Gt.full_cheap(f); Sa = Gg.s_line(f, a0, 1); Se = Gg.s_line(f, a0, 0); DM = Gg.diskmass(f, a0); L_ = lens(f); lawsys = L_["sys"] if lawsys is None else lawsys; sp = split(f); dw = c["G9_10"]
    o = dict(F=f, solar=c["solar"], G3=c["G3"], G5=c["G5"], split=sp, S_tr=Sa, S_ho=Se, G2fix=c["G2"], LT=c["G6"], groups=c["G7"], dw=dw, DM=DM, lens=L_)
    p = dict(G1=c["solar"]["newton"] and c["solar"]["cass"], G3L=bool(c["G3"] and c["G3"]["line"]), G3E=bool(c["G3"] and c["G3"]["err"]), G5L=bool(c["G5"] and c["G5"]["line"]), G5E=bool(c["G5"] and c["G5"]["err"]), G5b=sp["ok"], S=bool(Sa and Sa["line"] and Sa["tilt_ok"] and Se and Se["line"] and Se["tilt_ok"]), LTL=bool(c["G6"] and c["G6"]["line"]), LTE=bool(c["G6"] and c["G6"]["err"]), GR=bool(c["G7"] and c["G7"]["PASS"]), DW=bool(dw and dw["line"]), IC=bool(dw and dw["ic_line"]), DML=bool(DM and DM["line"]), DME=bool(DM and DM["err"]), LENSabs=bool(L_ and L_["sys"] <= 77.2), LENSlaw=bool(L_ and L_["sys"] <= lawsys + 21.2)); o["pass"] = p; out.append(o)
    print(f[:80], "fails", [k for k, v in p.items() if not v], "X", None if not c["G3"] else (round(c["G3"]["mean"], 3), round(c["G3"]["rms"], 3)), None if not c["G5"] else (round(c["G5"]["mean"], 3), round(c["G5"]["rms"], 3)), "S", Sa and (round(Sa["rms"], 3), Sa["U"]), Se and (round(Se["rms"], 3), Se["U"]), "LT", c["G6"] and round(c["G6"]["med"], 3), "lens", L_ and (round(L_["cov"], 1), round(L_["sys"], 1)), flush=True)
json.dump(out, open(outf, "w"), indent=0, default=float)
