#!/usr/bin/env python3
"""TX1 G8: LW1's real key path via BK2's dear patch, with s2 per cluster. python3 -I tx1_keys.py FOOT ARM LIST.json OUT.json [FILL]. ARM real|c1|c2|c3|label; FILL gas|median, env TX1_TAILCUT=1 sets tau 0 beyond 1.7. Primary cell: gas +0.005, f* 0.034. Law row first as known answer. kappa = 1/2 FITTED; not theory closed."""
import json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tx1_lib import *
from scipy.stats import chi2
LAW = "I1(gb,a0)"; foot, arm, lst, outf = sys.argv[1:5]; fill = sys.argv[5] if len(sys.argv) > 5 else "gas"; FS = [LAW] + [f for f in json.load(open(lst)) if f != LAW]; RB_ = RB
sys.path.insert(0, os.path.join(RB, "LW1_law_scorecard")); import lw1_keys as L
X = np.load(os.path.join(RB, "X7_cluster_core_significance", "x7_measure_percluster.npz")); NM = [str(s).strip() for s in X["name"]]; E_ = fits.open(os.path.join(REPO, "real_research", "data", "erass1cl_primary_v3.2.fits"))[1].data; EN = {str(s).strip(): i for i, s in enumerate(E_["NAME"])}; JI = np.array([EN[n] for n in NM]); KT = np.asarray(E_["KT"], float)[JI]; MG = np.asarray(E_["MGAS500"], float)[JI]; has = np.isfinite(KT) & (KT > 0); ok = has & (MG > 0)
p = np.polyfit(np.log10(MG[ok]), np.log10(KT[ok]), 1); K = KT.copy(); nofill = ~has
K[nofill] = 10 ** np.polyval(p, np.log10(np.where(MG[nofill] > 0, MG[nofill], np.median(MG[ok])))) if fill == "gas" else np.median(KT[ok])
print(f"KT measured {int(has.sum())} of {len(K)}; filled {int(nofill.sum())} by {fill}; lgKT = {p[1]:.3f} + {p[0]:.3f} lgMgas500", flush=True)
g, tau = tau_nodes(); flat = arm == "label"
if arm in SEEDS: K = K[np.random.default_rng(SEEDS[arm]).permutation(len(K))]
if flat: K[:] = label_s2(A0S[foot]) / KT2S; tau = np.ones_like(tau)
W = os.path.join(LANE, "chunks", f"keys_{foot}_{arm}_{fill}{'_cut' if os.environ.get('TX1_TAILCUT') else ''}"); os.makedirs(W, exist_ok=True); tf = os.path.join(W, "ktab.json"); json.dump(dict(KT=K.tolist(), names=NM, g=g.tolist(), tau=tau.tolist(), S=KT2S, cut=bool(os.environ.get("TX1_TAILCUT"))), open(tf, "w"))
T = L.T; a = 'return RM ** 2 * _comb(gb, gb * (1 + _LAW["c"] * S / 3), _A0L[foot], _LAW["rd"]) / GE, S'; assert T.count(a) == 1; T = T.replace(a, 'return RM ** 2 * _BKF(gb, _A0L[foot]) / GE, S')
c = 'pp = prep(i, foot, hk); m, S = _msrc(pp["Mb"], foot)'; assert T.count(c) == 1; T = T.replace(c, 'pp = prep(i, foot, hk); _TXP["pp"] = pp; _TXP["i"] = i; m, S = _msrc(pp["Mb"], foot)')
b = "def _msrc(Mb, foot):"; assert T.count(b) == 1
T = T.replace(b, f'''import sys as _s, json as _j
_s.path.insert(0, {os.path.join(RB, "BK2_dimensional_law_search")!r}); import bk2_lib as _B
_B.NSPACE["s2"] = np.float64(0.0); _BKS = _j.load(open(os.environ["BK2_LIST"])); _TX = _j.load(open(os.environ["TX1_TAB"])); _TXP = dict(); _TG = np.log(np.array(_TX["g"])); _TT = np.array(_TX["tau"]); _TXN = [0]
def _BKF(gb, a0_):
    fs_ = float(os.environ["X73_FSTAR"]); gb_ = np.maximum(gb, 1e-300); gg_ = gb_ / (1 + fs_); lM_ = np.log(gb_ * RM ** 2); lR_ = np.log(RM); dl_ = np.gradient(lM_, lR_); c_ = np.r_[np.cumsum((0.5 * (gb_[1:] + gb_[:-1]) * np.diff(RM))[::-1])[::-1], 0.0]; L_ = _B._local(gb_ - gg_, gg_, RM, dl_, RM * gb_ + c_ + gb_[-1] * RM[-1], a0_); pp_ = _TXP["pp"]; x_ = RM / (pp_["R500"] * NX["MPC"]); tu_ = np.interp(np.log(x_), _TG, _TT); tu_ = np.where(x_ > 1.7, 0.0, tu_) if _TX["cut"] else tu_; L_["s2"] = _TX["S"] * _TX["KT"][_TXP["i"]] * tu_
    if _TXN[0] == 0: _TXN[0] = 1; print("TX1 units: x range", x_[0], x_[-1], "R500", pp_["R500"], "MPC", NX["MPC"], "s2 median", float(np.median(L_["s2"])), "gb median", float(np.median(gb_)), flush=True)
    return _B.ev(_BKS[int(_LAW["mut"][1:])], L_)
''' + b)
TL = os.path.join(W, "tail.py"); open(TL, "w").write(T); O = os.path.join(W, os.path.basename(outf)); d = open(os.path.join(L.SL1, "sl1_harvest.py")).read()
for a_, b_ in (('SL1ADD = f"sub(', 'SL1ADD = ' + repr(L.GAS % 0.005) + ' + f"sub('), ('os.path.join(HERE, "sl1_tail_harvest.py")', repr(TL)), ('WD = os.path.join(HERE, "cache")', f'WD = {W!r}'), ('HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE)', f'HERE = {LANE!r}; RB = {RB!r}')):
    assert d.count(a_) == 1, a_; d = d.replace(a_, b_)
df = os.path.join(W, "driver.py"); open(df, "w").write(d); lf = os.path.join(W, os.path.basename(outf) + ".list"); json.dump(FS, open(lf, "w")); env = dict(os.environ, UR1_SL1=L.SL1, SL1_OUT=O, CN1_FORCE="1", LW1_A0X="1.0", BK2_LIST=lf, TX1_TAB=tf, DR1_RUN=json.dumps(dict(rows=[["R1", 0, foot, f"F{i}"] for i in range(len(FS))], k2=False)))
pr = subprocess.run(["nice", "-n", "19", sys.executable, df], env=env, stdout=open(os.path.join(W, os.path.basename(outf) + ".log"), "w"), stderr=subprocess.STDOUT); print("driver", pr.returncode, flush=True); J = json.load(open(O)); res = []; TERMS = (.021, .007, .031, .011, .079)
for i, f in enumerate(FS):
    c = J.get(f"R1|c0|{foot}|F{i}")
    if c is None: res.append(dict(F=f, missing=True)); print(i, "MISSING", f[:80]); continue
    o = dict(F=f, cells={})
    for h in ("h0672", "h0686"):
        Z = c["Z"][h]; R = J["R"][foot][h]; ks = R["keys"]; z0 = np.array([Z[k] for k in ks]); Rb = np.array(R["R_boot"]); w, V = np.linalg.eigh(Rb); okk = w >= 1e-3 * w.max(); z = V[:, okk].T @ z0; c2 = float((z * z / w[okk]).sum()); dof = int(okk.sum()); s_ = .118; zt = Z["G-OUT-M3"] * s_ / np.sqrt(s_ * s_ + sum(t * t for t in TERMS)); bad = [k for k in ks if abs(Z[k]) >= 2]; o["cells"][h] = dict(Z=Z, n_ok=15 - len(bad), bad=bad, M3=Z["G-OUT-M3"], M3_tot=float(zt), chi2=c2, dof=dof, p=float(chi2.sf(c2, dof)))
    res.append(o); print(i, f[:90], {h: (o["cells"][h]["n_ok"], round(o["cells"][h]["M3"], 2), round(o["cells"][h]["M3_tot"], 2), round(o["cells"][h]["chi2"], 1), float(f"{o['cells'][h]['p']:.2g}")) for h in o["cells"]}, flush=True)
json.dump(res, open(outf, "w"), indent=0, default=float)
