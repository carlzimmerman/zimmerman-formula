#!/usr/bin/env python3
"""BK2 harvest: full train gates G1-G3, both readings; holdouts and cheap gates for those passing, and for near misses. python3 bk2_read.py FOOT MODE LEVEL. kappa = 1/2 FITTED; not theory closed."""
import gzip, heapq, json, sys
from bk2_lib import *
import bk2_lib as B
HSE = 0.12; KG = np.logspace(-3, 3, 81)
def names(W):
    N = json.load(gzip.open(os.path.join(W, "names.json.gz"), "rt")); O = json.load(gzip.open(os.path.join(W, "order.json.gz"), "rt")); return N, O["oa"], O["oD"]
def hit_str(h, N, oa, oD):
    b = h[0]
    if b.startswith("T1"): return f"{b[3:]}({N['A'][oa[h[1]]]},{N['A'][oa[h[2]]]})", 0
    if b == "T2p": return f"({N['A'][oa[h[1]]]}+{N['A'][oa[h[2]]]})", 0
    if b == "T2m": return f"({N['A'][oa[h[1]]]}-{N['A'][oa[h[2]]]})", 0
    if b.startswith("T3"): _, k, op = b.split("|"); return f"{k}(gb,a0)*({N['D'][oD[h[1]]]}{op}{N['D'][oD[h[2]]]})", 0
    if b == "T4": return f"{N['A0'][h[1]]}*{N['D'][oD[h[2]]]}", 0
    if b.startswith("T5m"): return f"{b[4:]}(gb,a0)*(1+{KG[h[1]]!r}*{N['D'][oD[h[2]]]})", 1
    if b.startswith("T5a"): return f"({b[4:]}(gb,a0)+{KG[h[1]]!r}*{N['A'][oa[h[2]]]})", 1
    raise ValueError(b)
class Gates:
    def __init__(s, foot, mode):
        import bk2_search as S
        s.foot, s.mode = foot, mode; s.a0, s.XT, s.ST, s.SS, _ = S.train(foot, mode); a0 = s.a0; s.XH = xcop(a0, 1); s.SH = sparc(0, a0)
        if mode == "planted":
            s.XH["go"] = ev(S.PLANT, s.XH); s.SH["go"] = ev(S.PLANT, s.SH)
        s.ST65 = sparc(1, a0, .65); s.ST80 = sparc(1, a0, .80); s.SH65 = sparc(0, a0, .65); s.SH80 = sparc(0, a0, .80)
        if mode == "control":
            r = np.random.default_rng(20261102); n = len(s.XT["gb"]); r.permutation(n); p = r.permutation(len(s.ST["gb"]))
            for T in (s.ST65, s.ST80):
                f = (T["gg"] / T["gb"])[p]; T["gg"] = f * T["gb"]; T["gs"] = T["gb"] - T["gg"]
                for k in ("r", "Sig", "rho", "Phi"): T[k] = T[k][p]
        if mode == "planted":
            for T in (s.ST65, s.ST80, s.SH65, s.SH80): T["go"] = ev(S.PLANT, T)
        s.law = {}; s.rng = np.random.default_rng(20261104)
        for nm, T in (("ST", s.ST), ("SH", s.SH)):
            s.law[nm] = np.log10(T["go"] / I1(T["gb"], a0)); g = T["gid"]; u, inv = np.unique(g, return_inverse=True); ix = s.rng.integers(0, len(u), (400, len(u))); s.law[nm + "b"] = (inv, len(u), ix)
    def solar(s, f):
        v = ev(f, s.SS); ok = bool(np.all(np.isfinite(v))); ano = np.abs(v - s.SS["gb"]); return dict(newton=ok and bool(np.all(np.abs(v / s.SS["gb"] - 1) <= 1e-3)), cass=ok and bool(np.all(ano <= CAS)), Zc=float(np.max(ano / (CAS / 2))) if ok else 1e9)
    def xc(s, f, T):
        v = ev(f, T); d = np.log10(T["go"] / v)
        if not np.all(np.isfinite(d)): return None
        m = d.mean(); rm = float(np.sqrt((d * d).mean())); g = T["gid"]; u = np.unique(g); cm = np.array([d[g == k].mean() for k in u]); se = cm.std(ddof=1) / math.sqrt(len(u)); Zm = m / math.hypot(se, HSE); sig2 = T["se"] ** 2 + T["sm"] ** 2; c2 = float((((d - m) ** 2) / sig2).sum()); n = len(d) - 1; Zs = (c2 - n) / math.sqrt(2 * n); return dict(mean=float(m), rms=rm, Zm=float(Zm), Zs=float(Zs), line=bool(abs(m) <= .05 and rm <= .10), err=bool(abs(Zm) <= 2 and Zs <= 2))
    def sp(s, f, T, t65, t80, nm):
        d = np.log10(T["go"] / ev(f, T))
        if not np.all(np.isfinite(d)): return None
        L = s.law[nm]; inv, nu, ix = s.law[nm + "b"]; r2 = float((d * d).mean()); rL = float((L * L).mean()); ad = np.bincount(inv, d * d, nu); al = np.bincount(inv, L * L, nu); cn = np.bincount(inv, None, nu); bs = (ad[ix].sum(1) / cn[ix].sum(1)) - (al[ix].sum(1) / cn[ix].sum(1)); se = float(bs.std()); Zr = (r2 - rL) / max(se, 1e-12); md = float(np.median(d)); line = bool(math.sqrt(r2) <= 1.05 * math.sqrt(rL) and abs(md) <= .03); o = dict(rms=math.sqrt(r2), rms_law=math.sqrt(rL), med=md, Zr=float(Zr), line=line)
        ms = [md]
        for t in (t65, t80):
            q = np.log10(t["go"] / ev(f, t)); ms.append(float(np.median(q)) if np.all(np.isfinite(q)) else 9.0)
        o["med_U"] = ms; cross = min(ms) <= 0 <= max(ms); sem = s.law.setdefault(nm + "sem", float(np.std([np.median(L[np.isin(inv, np.random.default_rng(q).integers(0, nu, nu))]) for q in range(200)]))); o["sem"] = sem; o["Zu"] = 0.0 if cross else float(min(abs(x) for x in ms) / max(sem, 1e-9)); o["err"] = bool(Zr <= 2 and o["Zu"] <= 2); return o
    def lt(s, f):
        T = lt(s.a0); E = np.log10(T["go"] / ev(f, T))
        if not np.all(np.isfinite(E)): return None
        m = float(np.median(E)); r_ = np.random.default_rng(7); sb = float(np.std(np.median(E[r_.integers(0, len(E), (2000, len(E)))], axis=1))); Z = m / math.hypot(sb, .075); return dict(med=m, Z=float(Z), line=bool(abs(m) <= .10), err=bool(abs(Z) <= 2))
    def dw(s, f):
        D = dwarfs(s.a0, s.foot); o = {}; g = ev(f, D["L"]); E = np.log10(D["L"]["go"] / g)
        if not np.all(np.isfinite(E)): return None
        gs = ev(f, D["Le"]) - np.where(D["gNe"] > 0, ev(f, D["Ln"]), 0.0); E2 = np.log10(D["L"]["go"] / np.maximum(gs, 1e-300)); rng = np.random.default_rng(20261026)
        for key, X in (("plain", E), ("E2", E2)):
            o[key] = {}
            for c in D["CLS"]:
                m = D["cls"] == c; md, sd = boot_med(X[m], D["s"][m], rng, 2000); o[key][c] = dict(med=md, Z=md / sd)
        i = D["name"].index("IC 1613"); o["IC"] = dict(E=float(E[i]), Z=float(E[i] / D["s"][i])); o["line"] = all(abs(v["Z"]) < 2 for k in ("plain", "E2") for v in o[k].values()); o["ic_line"] = abs(o["IC"]["Z"]) < 2; return o
    def full_cheap(s, f):
        r = dict(F=f, solar=s.solar(f), G3=s.xc(f, s.XT), G2=s.sp(f, s.ST, s.ST65, s.ST80, "ST"), G5=s.xc(f, s.XH), G4=s.sp(f, s.SH, s.SH65, s.SH80, "SH"), G6=s.lt(f)); r["G7"] = groups_Z(f, s.foot, s.a0); r["G9_10"] = s.dw(f); return r
def zmax(a): return max(abs(a["G3"]["Zm"]), a["G3"]["Zs"], a["G2"]["Zr"], a["G2"]["Zu"], 0)
def main():
    foot, mode, lev = sys.argv[1:4]; W = os.path.join(HERE, "chunks", f"{lev}_{foot}_{mode}"); N, oa, oD = names(W); Gt = Gates(foot, mode); seen = set(); C = dict(hits=0, distinct=0, cass=0, g3_line=0, g3_err=0, g2_line=0, g2_err=0, train_line=0, train_err=0, train_line_cass=0, train_err_cass=0, nonfinite=0, fitted_train_err=0); heap = []; keepL = []; keepE = []; XT = Gt.XT
    for ln in open(os.path.join(W, "hits.jsonl")):
        if C["hits"] % 200000 == 0: print("progress", C, flush=True)
        h = json.loads(ln); C["hits"] += 1; s, fit = hit_str(h, N, oa, oD)
        try: dx = np.log10(XT["go"] / ev(s, XT))
        except Exception: C["nonfinite"] += 1; continue
        if not np.all(np.isfinite(dx)): C["nonfinite"] += 1; continue
        k = np.round(dx, 7).tobytes()
        if k in seen: continue
        seen.add(k); C["distinct"] += 1; x = Gt.xc(s, XT); sol = Gt.solar(s)
        if not sol["newton"]: continue
        C["cass"] += sol["cass"]; C["g3_line"] += x["line"]; C["g3_err"] += x["err"]
        C["zone"] = C.get("zone", 0) + 1 if (x["line"] or x["err"] or x["rms"] <= .15) else C.get("zone", 0)
        pass_x = x["line"] or x["err"] or x["rms"] <= .15
        if not pass_x: continue
        p = Gt.sp(s, Gt.ST, Gt.ST65, Gt.ST80, "ST")
        if p is None: continue
        C["g2_line"] += p["line"]; C["g2_err"] += p["err"]; tl = x["line"] and p["line"]; te = x["err"] and p["err"]; C["train_line"] += tl; C["train_err"] += te; C["train_line_cass"] += tl and sol["cass"]; C["train_err_cass"] += te and sol["cass"]; C["fitted_train_err"] += te and fit; C["POST_train_err_noZs"] = C.get("POST_train_err_noZs", 0) + bool(abs(x["Zm"]) <= 2 and p["err"])
        z = max(abs(x["Zm"]), x["Zs"], p["Zr"], p["Zu"], sol["Zc"] if sol["cass"] else 0.0); row = dict(F=s, fit=fit, cass=sol["cass"], Zc=sol["Zc"], X=x, S=p, Z=z, Zl=max(abs(x["mean"]) / .05, x["rms"] / .10, p["rms"] / (1.05 * p["rms_law"]), abs(p["med"]) / .03))
        for H, key, cap in ((heap, "Z", 200), (keepL, "Zl", 200)):
            it = (-row[key], len(s), s, row)
            if len(H) < cap: heapq.heappush(H, it)
            elif it > H[0]: heapq.heapreplace(H, it)
        if tl or te: keepE.append(row)
    print("FINAL", foot, mode, lev, C, flush=True); byZ = sorted((t[3] for t in heap), key=lambda a: a["Z"]); byL = sorted((t[3] for t in keepL), key=lambda a: a["Zl"]); json.dump(dict(counts=C, tally=json.load(open(os.path.join(W, "tally.json"))), info=json.load(open(os.path.join(W, "info.json"))), byZ=byZ, byLine=byL, train_pass=keepE[:5000], n_train_pass=len(keepE)), open(os.path.join(HERE, f"bk2_train_{lev}_{foot}_{mode}.json"), "w"), indent=0)
    for a in byZ[:8]: print(f"Z {a['Z']:.2f} cass {a['cass']} X {a['X']['mean']:+.3f},{a['X']['rms']:.3f} Zm {a['X']['Zm']:+.2f} Zs {a['X']['Zs']:.1f} S {a['S']['rms']:.3f}/{a['S']['rms_law']:.3f} {a['S']['med']:+.3f} Zr {a['S']['Zr']:.2f} Zu {a['S']['Zu']:.2f} {a['F'][:90]}")
    print("by LINE"); [print(f"Zl {a['Zl']:.2f} cass {a['cass']} X {a['X']['mean']:+.3f},{a['X']['rms']:.3f} S {a['S']['rms']:.3f}/{a['S']['rms_law']:.3f} {a['S']['med']:+.3f} fit{a['fit']} {a['F'][:90]}") for a in byL[:8]]
if __name__ == "__main__": main()
