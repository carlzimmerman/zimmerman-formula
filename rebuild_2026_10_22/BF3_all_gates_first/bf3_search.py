#!/usr/bin/env python3
"""BF3 search. Usage: bf3_search.py ARM FOOT FAM [workers] [max_shards]. ARM real c1 c2 c3 planted. FAM A B E. Preemptible by shard. Criteria FROZEN_CRITERIA.md. kappa = 1/2 FITTED; not theory closed."""
import json, os, signal, sys, time
from multiprocessing import Pool
from bf3_common import *
OPS = "+-*/"; STEP = 2000; SHARD = 100; TOPK = 300
PL_T = ("sqrt(y)", "inv1p(y)", "*", 2)   # planted: W2, H = 1 + f sqrt(y) / (1 + y)
LXP, SXP = .30, .15   # precut
_S = {}
def lines(arm, foot):
    if arm == "planted": return L_ABS, L_ABS
    o = json.load(open(os.path.join(LANE, "bf3_k1.json")))["res"][foot]["law"]["exact"]["lens"]["sys"]; return L_ABS, o + L_DELTA
def init(arm, foot, fam):
    signal.signal(signal.SIGINT, signal.SIG_IGN); signal.signal(signal.SIGTERM, signal.SIG_DFL)
    d, V, R = pool(foot, "real" if arm == "r10" else arm, ext=fam == "E"); _S.update(arm=arm, foot=foot, fam=fam, d=d, V=V, R=R, names=d["names"], VX=np.array(V[:, R.sX]), VX32=np.array(V[:, R.sX], dtype="f4"), yX=(R.gbX / R.a0).astype("f4"), fX32=R.f[R.sX].astype("f4"), oX=(R.obsX - math.log10(R.a0)).astype("f4"), VP=np.array(V[:, R.sP]), VL=np.array(V[:, R.sL]), fL=R.f[R.sL], fX=R.f[R.sX], la=lines(arm, foot)[0], ll=lines(arm, foot)[1], A=fam in ("A", "E"))
    if arm == "planted":
        a, b, o, w = PL_T; Hf = lambda y, e, f: 1 + f * eval(f"({a}{o}{b})", {"__builtins__": {}}, dict(FN, y=y, ell=e, f=f)); R.planted(Hf, w); _S["oX"] = (R.obsX - math.log10(R.a0)).astype("f4")
CHI_G = 1.5   # groups run only below 1.5 x the law-level line: AMENDMENT_A1
def lens_gate(i, op, js, w):
    """Lens chi^2 and gate 0 from arrays in memory."""
    S = _S; R = S["R"]; a0 = R.a0; js = np.asarray(js); VL, VP = S["VL"], S["VP"]
    TL = VL[js] if op == "0" else B[op](VL[i][None, :], VL[js]); TP = VP[js] if op == "0" else B[op](VP[i][None, :], VP[js])
    H = HMUT * ((1 + S["fL"][None, :] * TL) if S["A"] else TL); H = np.where(np.isfinite(H) & (H > 0), H, np.nan)
    if S["A"]: g0 = np.isfinite(TP).all(1)
    else: g0 = (np.abs(TP * HMUT - 1) <= 1e-12).all(1)
    bl = wrap(w, R.gbL, a0, H) / R.gbL; return g0, ((R.yw[None, :] - bl @ R.Mw.T) ** 2).sum(1)
def group_gate(i, op, js, w):
    S = _S; R = S["R"]; V = S["V"]; a0 = R.a0; js = np.asarray(js); T = np.array(V[js]) if op == "0" else B[op](np.array(V[i])[None, :], np.array(V[js]))
    H = HMUT * ((1 + R.f[None, :] * T) if S["A"] else T); H = np.where(np.isfinite(H) & (H > 0), H, np.nan); ng = R.W.shape[1]
    def gm(sl):
        b = (wrap(w, R.gbG, a0, H[:, sl]) / R.gbG).reshape(len(js), 63, ng); return -(R.ls - (.5 * np.log10((b * R.W).sum(2)) - 3)).mean(1)
    return gm(R.sG0), gm(R.sG1)
def kept_gates(i, op, js, w):
    g0, chi = lens_gate(i, op, js, w); g3, g6 = group_gate(i, op, js, w); return g0, chi, g3, g6
def xstats(D, cl):
    m = D.mean(1); s = D.std(1); by = np.stack([D[:, cl == j].mean(1) for j in range(7)], 1); st = by.std(1, ddof=1) / math.sqrt(7); return m, s, m / np.hypot(st, .12), np.sqrt((D * D).mean(1))
def chunk(i, op, j0, jn, Acc, Cnt, Sam):
    S = _S; R = S["R"]; VX, VP, fX = S["VX"], S["VP"], S["fX"]; a0 = R.a0; A = S["A"]
    sampled = (i * 7919 + ord(op) * 31 + j0) % 1000 == 0
    V32 = S["VX32"]; yX = S["yX"]; f32 = S["fX32"]; oX = S["oX"]; N0 = jn - j0; Cnt["tried"] += 3 * N0; base = np.arange(j0, jn); Hm = np.float32(HMUT)
    T = V32[j0:jn] if op == "0" else B[op](V32[i][None, :], V32[j0:jn])
    if not A:
        TP = VP[j0:jn] if op == "0" else B[op](VP[i][None, :], VP[j0:jn]); ok0 = (np.abs(TP * HMUT - 1) <= 1e-12).all(1); Cnt["g0_B"] += 3 * int(ok0.sum())
        if not ok0.any(): return
        T = T[ok0]; base = base[ok0]
    H = Hm * ((1 + f32[None, :] * T) if A else T); okH = np.isfinite(H).all(1) & (H > 0).all(1)
    if not okH.any(): return
    H = H[okH]; base = base[okH]; Cnt["positive"] += 3 * len(base)
    for w in (1, 2, 3):
        p = (.5 * yX + np.sqrt(.25 * yX * yX + yX * H)) if w == 1 else (.5 * yX * H + np.sqrt(.25 * yX * yX * H * H + yX * H)) if w == 2 else (.5 * yX + np.sqrt(.25 * yX * yX + yX)) * H
        D = oX[None, :] - np.log10(p); m = D.mean(1); s_ = D.std(1); kp = (np.abs(m) <= LXP + .001) & (s_ <= SXP + .001)
        if sampled and len(base):
            Hd = HMUT * ((1 + fX[None, :] * (VX[base] if op == "0" else B[op](VX[i][None, :], VX[base]))) if A else (VX[base] if op == "0" else B[op](VX[i][None, :], VX[base]))); Dd = R.obsX[None, :] - np.log10(wrap(w, R.gbX, a0, Hd)); mm, ss, zz, rr = xstats(Dd, R.cl); xp = (np.abs(zz) <= 2) & (ss <= .10); g0, chi, g3, g6 = kept_gates(i, op, base, w); Gp = (np.abs(g3) <= .145) & (np.abs(g6) <= .145); La = chi <= 1.03 * S["la"]; Ll = chi <= 1.03 * S["ll"]
            Cnt["s_n"] += len(base); Cnt["s_g0"] += int(g0.sum()); Cnt["s_Ll"] += int((g0 & Ll).sum()); Cnt["s_La"] += int((g0 & La).sum()); Cnt["s_LlG"] += int((g0 & Ll & Gp).sum()); Cnt["s_LaG"] += int((g0 & La & Gp).sum()); Cnt["s_LlGX"] += int((g0 & Ll & Gp & xp).sum()); Cnt["s_LaGX"] += int((g0 & La & Gp & xp).sum()); Cnt["s_X"] += int((g0 & xp).sum()); Cnt["k5_lost"] += int((g0 & Ll & Gp & xp & ~kp).sum())
            for t in np.nonzero(g0 & Ll & Gp)[0][:5]: Sam.append([i, op, int(base[t]), w, round(float(zz[t]), 5), round(float(ss[t]), 5), round(float(chi[t]), 4), round(float(g3[t]), 5), round(float(g6[t]), 5)])
        if not kp.any(): continue
        js = base[kp]; Td = VX[js] if op == "0" else B[op](VX[i][None, :], VX[js]); Hd = HMUT * ((1 + fX[None, :] * Td) if A else Td); Dd = R.obsX[None, :] - np.log10(wrap(w, R.gbX, a0, Hd)); md = Dd.mean(1); sd = Dd.std(1); k2 = np.isfinite(md) & (np.abs(md) <= LXP) & (sd <= SXP)
        if not k2.any(): continue
        js = js[k2]; Cnt["precut"] += len(js); mm, ss, zz, rr = xstats(Dd[k2], R.cl); xp = (np.abs(zz) <= 2) & (ss <= .10); Cnt["Xpass"] += int(xp.sum()); Cnt["Xstrict"] += int(((np.abs(mm) <= .05) & (rr <= .10)).sum())
        for q in range(0, len(js), 1000):
            g0, chi = lens_gate(i, op, js[q:q + 1000], w); okz = g0 & np.isfinite(chi)
            if not okz.any(): continue
            jj = js[q:q + 1000][okz]; chi = chi[okz]; xq = xp[q:q + 1000][okz]; Cnt["g0"] += len(jj); n = len(jj); g3 = np.full(n, np.nan); g6 = np.full(n, np.nan); lo = np.nonzero((chi <= CHI_G * S["ll"]) & xq)[0]; Cnt["lens_lo"] += len(lo)
            for u in range(0, len(lo), 200):
                uu = lo[u:u + 200]; g3[uu], g6[uu] = group_gate(i, op, jj[uu], w)
            Acc.append(np.c_[np.full(n, i), np.full(n, OPS.index(op) if op != "0" else -1), jj, np.full(n, w), zz[q:q + 1000][okz], ss[q:q + 1000][okz], chi, g3, g6])
def trim(Acc, Cnt):
    if not Acc: return []
    a = np.vstack(Acc); S = _S; zx = np.maximum(np.abs(a[:, 4]) / 2, a[:, 5] / .10); la = a[:, 6] / S["la"]; ll = a[:, 6] / S["ll"]; g = np.nan_to_num(np.maximum(np.abs(a[:, 7]), np.abs(a[:, 8])) / .10, nan=1e9); keep = set()
    cand = (np.abs(a[:, 4]) <= 2) & (a[:, 5] <= .10) & (a[:, 6] <= 1.03 * S["ll"]) & (np.abs(a[:, 7]) <= .145) & (np.abs(a[:, 8]) <= .145)
    keep.update(np.nonzero(cand)[0][:5000].tolist())
    for sc in (zx, np.maximum(zx, la), np.maximum(zx, ll), np.maximum(zx, g), np.maximum(zx, np.maximum(la, g)), np.maximum(zx, np.maximum(ll, g))):
        o = np.lexsort((a[:, 3], a[:, 2], a[:, 1], a[:, 0], sc))[:TOPK]; keep.update(o.tolist())
    k = np.array(sorted(keep), dtype=int); return [a[k]]
def do_shard(jb):
    n, jobs, W = jb; S = _S; N = len(S["names"]); Acc = []; Sam = []; Cnt = {k: 0 for k in ("tried", "g0_B", "positive", "precut", "Xpass", "Xstrict", "g0", "lens_lo", "s_n", "s_g0", "s_Ll", "s_La", "s_LlG", "s_LaG", "s_LlGX", "s_LaGX", "s_X", "k5_lost")}
    for i, op in jobs:
        rng = range(0, N, STEP) if op == "0" or op in "-/" else range(i - i % STEP, N, STEP)
        for j0 in rng:
            lo = max(j0, i) if op in "+*" else j0; chunk(i, op, lo, min(j0 + STEP, N), Acc, Cnt, Sam)
        if sum(len(x) for x in Acc) > 100000: Acc[:] = trim(Acc, Cnt)
    Acc[:] = trim(Acc, Cnt); rec = [[int(r[0]), int(r[1]), int(r[2]), int(r[3])] + [None if not np.isfinite(x) else round(float(x), 5) for x in r[4:]] for r in (Acc[0] if Acc else [])]; rec.sort(key=lambda r: r[:4])
    p = os.path.join(W, f"{n:06d}.json"); open(p + ".tmp", "w").write(json.dumps(dict(cnt=Cnt, rec=rec, sam=sorted(Sam)), sort_keys=True)); os.replace(p + ".tmp", p); return n, Cnt["tried"]
def main():
    arm, foot, fam = sys.argv[1:4]; nw = int(sys.argv[4]) if len(sys.argv) > 4 else 4; lim = int(sys.argv[5]) if len(sys.argv) > 5 else 0; root = os.environ.get("BF3_OUT", "shards"); W = os.path.join(LANE, root, f"{arm}_{foot}_{fam}{TAG}"); os.makedirs(W, exist_ok=True)
    d, V, R = pool(foot, "real" if arm == "r10" else arm, ext=fam == "E"); N = len(d["names"]); jobs = [(-1, "0")] + [(i, o) for i in range(N) for o in OPS]
    if arm in ("c2", "c3"): jobs = [(-1, "0")] + [(i, o) for i in range(0, N, 10) for o in OPS]
    if arm == "planted":
        ia = min(d["names"].index(PL_T[0]), d["names"].index(PL_T[1])); jobs = [(ia, PL_T[2])]
    if arm == "real" and foot == "alt" or arm in ("c1", "r10"): jobs = [(-1, "0")] + [(i, o) for i in range(0, N, 10) for o in OPS]  # AMENDMENT_A1
    if fam == "E": jobs = [(i, o) for i in range(N) for o in OPS]
    sh = [(k // SHARD, jobs[k:k + SHARD], W) for k in range(0, len(jobs), SHARD)]; 
    if lim > 0: sh = sh[:lim]
    if lim < 0: sh = sh[::-lim][:6]  # timing and rerun subsets: every -lim-th shard, six
    todo = [s for s in sh if not os.path.exists(os.path.join(W, f"{s[0]:06d}.json"))]; print(f"{arm} {foot} {fam}: pool {N} (closure total {d['total']}), {len(jobs)} jobs, {len(sh)} shards, {len(todo)} to do, law lines {lines(arm, foot)}", flush=True)
    budget = float(os.environ.get("BF3_BUDGET_S", 0)); t0 = time.time(); stop = dict(x=0); signal.signal(signal.SIGTERM, lambda *a: stop.__setitem__("x", 1)); tot = 0
    with Pool(nw, init, (arm, foot, fam)) as P:
        for k, (n, c) in enumerate(P.imap_unordered(do_shard, todo, chunksize=1)):
            tot += c
            if k % 20 == 0: print(f"{k}/{len(todo)} shards, {tot:.3g} tried, {time.time() - t0:.0f} s", flush=True)
            if stop["x"] or (budget and time.time() - t0 > budget): print("stopped: SIGTERM or budget; shards so far are complete", flush=True); P.terminate(); open(os.path.join(W, "STOPPED"), "w").write(str(k + 1)); return
    open(os.path.join(W, "COMPLETE"), "w").write(str(len(sh))); print(f"DONE {arm} {foot} {fam}: {tot:.4g} this run, {time.time() - t0:.0f} s", flush=True)
if __name__ == "__main__": main()
