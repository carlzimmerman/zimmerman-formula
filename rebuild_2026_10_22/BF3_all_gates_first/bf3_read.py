#!/usr/bin/env python3
"""BF3 reader: merges shards of an arm, S on candidates and shortlists, exact regrade, funnel, near-miss table. Usage: bf3_read.py ARM[,ARM] [--out tag]. kappa = 1/2 FITTED; not theory closed."""
import glob, json, os, sys, time
from bf3_common import *
OPS = "+-*/"
def expr(names, r):
    return names[r[2]] if r[1] == -1 else f"({names[r[0]]}{OPS[r[1]]}{names[r[2]]})"
def load(arm, foot, fam, root="shards", maxshard=None):
    W = os.path.join(LANE, root, f"{arm}_{foot}_{fam}"); fs = sorted(glob.glob(os.path.join(W, "*.json")))
    if maxshard is not None: fs = [f for f in fs if int(os.path.basename(f)[:-5]) < maxshard]
    cnt = {}; rec = []; sam = []
    for f in fs:
        d = json.load(open(f))
        for k, v in d["cnt"].items(): cnt[k] = cnt.get(k, 0) + v
        rec += d["rec"]; sam += d["sam"]
    return dict(cnt=cnt, rec=rec, sam=sam, shards=len(fs), complete=os.path.exists(os.path.join(W, "COMPLETE")), stopped=os.path.exists(os.path.join(W, "STOPPED")))
def lines(foot):
    o = json.load(open(os.path.join(LANE, "bf3_k1.json")))["res"][foot]["law"]["exact"]["lens"]["sys"]; return L_ABS, o + L_DELTA, o
def scores(r, la, ll):
    a = np.array([[x if x is not None else np.inf for x in q[4:]] for q in r]); zx = np.maximum(np.abs(a[:, 0]) / 2, a[:, 1] / .10); g = np.maximum(np.abs(a[:, 3]), np.abs(a[:, 4])) / .10; return dict(X=zx, La=a[:, 2] / la, Ll=a[:, 2] / ll, G=g)
CHEAP = {"X": ("X",), "X+La": ("X", "La"), "X+Ll": ("X", "Ll"), "X+G": ("X", "G"), "X+La+G": ("X", "La", "G"), "X+Ll+G": ("X", "Ll", "G")}
def analyse(arm, foot, fams=("A", "B"), root="shards", planted=None, shortlist=300, maxshard=None):
    la, ll, lc = lines(foot) if arm != "planted" else (L_ABS, L_ABS, 0.0); d, _, _ = pool(foot, "real" if arm == "r10" else arm, ext="E" in fams); out = dict(arm=arm, foot=foot, la=la, ll=ll, fams={}); E0 = E_get(foot, planted)
    for fam in fams:
        if fam == "E": names = pool(foot, "real" if arm == "r10" else arm, ext=True)[0]["names"]
        else: names = d["names"]
        D = load(arm, foot, fam, root, maxshard); o = dict(cnt=D["cnt"], shards=D["shards"], complete=D["complete"], stopped=D["stopped"]); r = D["rec"]; out["fams"][fam] = o
        if not r: o["cand"] = 0; o["joint"] = []; o["combos"] = {}; continue
        sc = scores(r, la, ll); a = np.array([[x if x is not None else np.inf for x in q[4:]] for q in r]); cand = (np.abs(a[:, 0]) <= 2) & (a[:, 1] <= .10) & (a[:, 2] <= 1.03 * ll) & (np.abs(a[:, 3]) <= .145) & (np.abs(a[:, 4]) <= .145); o["cand"] = int(cand.sum()); o["cand_abs"] = int((cand & (a[:, 2] <= 1.03 * la)).sum()); short = set(np.nonzero(cand)[0].tolist()); T = {}
        for k, gs in CHEAP.items():
            s = np.max([sc[g] for g in gs], axis=0); ix = np.lexsort(([q[2] for q in r], [q[0] for q in r], s))[:shortlist]; T[k] = ix; short.update(ix.tolist())
        ci = np.nonzero(cand)[0]; cA = ci[a[ci, 2] <= 1.03 * la]; cO = ci[a[ci, 2] > 1.03 * la]; pA = cA if len(cA) <= 20000 else cA[np.linspace(0, len(cA) - 1, 20000).astype(int)]; pO = cO if len(cO) <= 10000 else cO[np.linspace(0, len(cO) - 1, 10000).astype(int)]; short = set(np.concatenate(list(T.values())).tolist()) | set(pA.tolist()) | set(pO.tolist()); scale = (len(cA) / max(len(pA), 1), len(cO) / max(len(pO), 1)); o["scale_S"] = scale
        t0 = time.time(); Ssc = {}
        for i in sorted(short):
            q = r[i]; Hf = form_fn(expr(names, q), fam); S_ = E0.sparc(Hf, q[3]); Ssc[i] = S_
        o["n_S"] = len(Ssc); o["S_wall"] = time.time() - t0; pS = {i: S_pass(v) for i, v in Ssc.items()}; jA = [i for i in pA.tolist() if pS[i]]; jO = [i for i in pO.tolist() if pS[i]]; o["cand_abs_S_sampled"] = len(jA); o["cand_law_only_S_sampled"] = len(jO); o["cand_abs_S_est"] = len(jA) * scale[0]; o["cand_S_est"] = len(jA) * scale[0] + len(jO) * scale[1]; j = jA + jO
        def Sscore(i): v = Ssc[i]; return max(v["rms"] / .110, abs(v["U"] - .65) / .15) if not v["nf"] else np.inf
        o["joint_cheap"] = [dict(s=expr(names, r[i]), w=r[i][3], fam=fam, cheap=r[i][4:], S=Ssc[i]) for i in j[:3000]]; combos = {}
        for k, gs in CHEAP.items():
            s = np.max([sc[g] for g in gs], axis=0); i = T[k][0]; combos[k] = dict(s=expr(names, r[i]), w=r[i][3], score=float(s[i]), cheap=r[i][4:], S=Ssc[i]); bS = min(T[k].tolist(), key=lambda i: (max(float(s[i]), Sscore(i)), r[i][:4])); combos[k + "+S"] = dict(s=expr(names, r[bS]), w=r[bS][3], score=max(float(s[bS]), Sscore(bS)), cheap=r[bS][4:], S=Ssc[bS])
        o["combos"] = combos; o["sam"] = D["sam"]
    return out
_E = {}
def E_get(foot, planted=None):
    k = (foot, planted is not None)
    if k not in _E: _E[k] = Exact(foot, planted)
    return _E[k]

def gate_score(c, S_, la):
    return max(abs(c[0]) / 2, c[1] / .10, c[2] / la, abs(c[3]) / .10, abs(c[4]) / .10, S_["rms"] / .110, abs(S_["U"] - .65) / .15)
def distinct(J, la):
    seen = {}
    for x in J:
        k = (tuple(round(v, 4) for v in x["cheap"]), x["w"], round(x["S"]["rms"], 5))
        if k not in seen or (len(x["s"]), x["s"]) < (len(seen[k]["s"]), seen[k]["s"]): seen[k] = x
    return sorted(seen.values(), key=lambda x: (gate_score(x["cheap"], x["S"], la), len(x["s"]), x["s"]))
def exact_grade(x, foot, E=None):
    E = E or E_get(foot); Hf = form_fn(x["s"], x["fam"]); w = x["w"]; o = E.all(Hf, w); o["pass"] = dict(L_abs=o["lens"]["sys"] <= L_ABS, L_law=o["lens"]["sys"] <= lines(foot)[1], G=G_pass(o["G"]), S=S_pass(o["S"]), X=X_pass(o["X"]), X_strict=o["X"]["strict"]); return o
