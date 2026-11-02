#!/usr/bin/env python3
"""BK2 search. python3 bk2_search.py FOOT MODE LEVEL [--test]. FOOT canonical|alt; MODE real|control|planted|mutate; LEVEL L1|L2. Checkpoints per job, SIGTERM saves and exits, rerun resumes. kappa = 1/2 FITTED; not theory closed."""
import gzip, itertools, json, math, os, signal, sys, time
import bk2_lib as B
from bk2_lib import *
PLANT = "(I5(gb,a0)+pi**2*gg*gg/a0)"; EPS = 1e-3
CAPS = dict(L1=(30000, 30000), L2=(100000, 300000), T0=(1500, 1500)); XM, XR, SM, SF = 0.30, 0.40, 0.10, 1.3
CONSTS = [("0.5", .5), ("1.0", 1.), ("2.0", 2.), ("3.0", 3.), ("4.0", 4.), ("pi", math.pi), ("(2*pi)", 2 * math.pi), ("(4*pi)", 4 * math.pi), ("(pi**2)", math.pi ** 2), ("(1/pi)", 1 / math.pi), ("(4/3)", 4 / 3), ("(8*pi/3)", 8 * math.pi / 3)]
EXPS = [(1, ""), (2, "**2"), (-1, "**-1"), (-2, "**-2"), (.5, "**0.5"), (-.5, "**-0.5")]
LEAF = ["G", "c", "a0", "rde", "gs", "gg", "gb", "r", "Sig", "rho", "Phi"]
def train(foot, mode):
    a0 = A0S[foot]; XT = xcop(a0, 0); ST = sparc(1, a0); SS = solar(a0); rng = np.random.default_rng(20261102)
    if mode == "control":
        for T in (XT, ST):
            n = len(T["gb"]); p = rng.permutation(n); f = (T["gg"] / T["gb"])[p]; T["gg"] = f * T["gb"]; T["gs"] = T["gb"] - T["gg"]
            for k in ("r", "Sig", "rho", "Phi"): T[k] = T[k][p]
    if mode == "planted":
        for T in (XT, ST): T["go"] = ev(PLANT, T)
    sub = np.random.default_rng(20261103).choice(len(ST["gb"]), 240, replace=False); return a0, XT, ST, SS, sub
def concat(SS, XT, ST, sub):
    o = {}
    for k in ("gs", "gg", "gb", "r", "Sig", "rho", "Phi"): o[k] = np.r_[SS[k], XT[k], ST[k][sub]]
    return o
class Clo:
    def __init__(s, n0): s.seen = set(); s.names = []; s.cost = []; s.v = []; s.n0 = n0
    def key(s, v):
        q = v[s.n0:]; m = np.abs(q).max(); return (np.round(q / m, 9) + 0.0).tobytes() + np.float64(np.round(math.log(m), 6)).tobytes()
    def add(s, name, c, v):
        q = v[s.n0:]
        if not np.all(np.isfinite(q)): return False
        m = np.abs(q).max()
        if m == 0 or m > 1e60 or m < 1e-60: return False
        k = s.key(v)
        if k in s.seen: return False
        s.seen.add(k); s.names.append(name); s.cost.append(c); s.v.append(v); return True
def monos(L, n0, maxc):
    sc = dict(G=G, c=C, a0=L["a0"], rde=L["rde"]); val = {k: (L[k] if k in L and np.ndim(L[k]) else np.full_like(L["gb"], sc[k])) for k in LEAF}; A, D = Clo(n0), Clo(n0); fin = 0
    for n in (1, 2, 3, 4):
        for cb in itertools.combinations(LEAF, n):
            if "gb" in cb and ("gs" in cb and "gg" in cb): continue
            for ex in itertools.product(EXPS, repeat=n):
                c = n + sum(1 for e, _ in ex if e != 1)
                if c > maxc: continue
                d = tuple(sum(DIM[l][i] * e for l, (e, _) in zip(cb, ex)) for i in range(3))
                if d != ACC and d != NUL: continue
                nm = "*".join(f"{l}{t}" for l, (_, t) in zip(cb, ex)); v = np.ones_like(L["gb"])
                for l, (e, _) in zip(cb, ex): v = v * val[l] ** e
                (A if d == ACC else D).add(f"({nm})", c, v)
    return A, D
def closure(L, n0, cap_d, cap_a):
    A, DM = monos(L, n0, 6); a0v = np.full_like(L["gb"], L["a0"]); D0 = Clo(n0)
    for nm, x in CONSTS: D0.add(nm, 1, np.full_like(L["gb"], x))
    for nm, c, v in zip(DM.names, DM.cost, DM.v): D0.add(nm, c, v)
    n_m_a, n_m_d = len(A.names), len(DM.names); D = Clo(n0); o0 = np.argsort(D0.cost, kind="stable")
    for i in o0: D.add(D0.names[i], D0.cost[i], D0.v[i])
    for i in o0:
        for u, fn in UNARY.items(): D.add(f"{u}({D0.names[i]})", D0.cost[i] + 1, fn(D0.v[i]))
    base = list(zip(D.names, D.cost, D.v)); base.sort(key=lambda t: (t[1], t[0])); tried = 0; top = 4 * cap_d; maxc = max(b[1] for b in base) * 2 + 1; stopped = False
    for tc in range(2, maxc + 1):
        for i, (n1, c1, v1) in enumerate(base):
            if c1 + 1 >= tc: break
            for n2, c2, v2 in base[i:]:
                if c1 + c2 + 1 > tc: break
                if c1 + c2 + 1 != tc: continue
                tried += 4; D.add(f"({n1}+{n2})", tc, v1 + v2); D.add(f"({n1}*{n2})", tc, v1 * v2); D.add(f"({n1}-{n2})", tc, v1 - v2); D.add(f"({n1}/{n2})", tc, v1 / v2); D.add(f"({n2}/{n1})", tc, v2 / v1)
            if len(D.names) > top: stopped = True; break
        if stopped: break
    o = sorted(range(len(D.names)), key=lambda i: (D.cost[i], D.names[i])); ncl = len(D.names); o = o[:cap_d]; Dn = [D.names[i] for i in o]; Dc = [D.cost[i] for i in o]; Dv = np.array([D.v[i] for i in o]); del D
    A0 = Clo(n0)
    for nm, c, v in zip(A.names, A.cost, A.v):
        for cn, cx in CONSTS: A0.add(f"({cn}*{nm})" if cn != "1.0" else nm, c + (cn != "1.0"), cx * v)
    Au = Clo(n0)
    for nm, c, v in zip(A0.names, A0.cost, A0.v): Au.add(nm, c, v)
    small = sorted(range(len(A0.names)), key=lambda i: (A0.cost[i], A0.names[i]))[:400]
    for k, fn in IK.items():
        for i in small:
            for j in small:
                if A0.cost[i] + A0.cost[j] <= 5 and np.all(A0.v[i][n0:] > 0) and np.all(A0.v[j][n0:] > 0): Au.add(f"{k}({A0.names[i]},{A0.names[j]})", A0.cost[i] + A0.cost[j] + 2, fn(A0.v[i], A0.v[j]))
    lim = 4 * cap_a; pool = sorted(range(len(Dn)), key=lambda i: Dc[i]); mon = sorted(range(len(A0.names)), key=lambda i: (A0.cost[i], A0.names[i]))
    for tc in range(3, 40):
        for i in mon:
            if A0.cost[i] + 2 > tc: break
            for j in pool:
                c = A0.cost[i] + Dc[j] + 1
                if c > tc: break
                if c == tc: Au.add(f"({A0.names[i]}*{Dn[j]})", c, A0.v[i] * Dv[j])
            if len(Au.names) > lim: break
        if len(Au.names) > lim: break
    o = sorted(range(len(Au.names)), key=lambda i: (Au.cost[i], Au.names[i])); nca = len(Au.names); o = o[:cap_a]; An = [Au.names[i] for i in o]; Av = np.array([Au.v[i] for i in o]); del Au
    return dict(Dn=Dn, Dv=Dv, An=An, Av=Av, A0n=A0.names, A0v=np.array(A0.v), n_mono_a=n_m_a, n_mono_d=n_m_d, n_d_before=ncl, n_a_before=nca, n_a0=len(A0.names), d_stopped=stopped)
def main():
    foot, mode, lev = sys.argv[1:4]; a0, XT, ST, SS, sub = train(foot, mode); xm = 1e-6 if mode == "mutate" else XM; xr = 1e-6 if mode == "mutate" else XR
    L = concat(SS, XT, ST, sub); L.update(a0=a0, rde=rde_of(a0)); n0 = 3; nx = len(XT["gb"]); ix = slice(3, 3 + nx); iS = slice(3 + nx, None); gh = np.r_[XT["go"], ST["go"][sub]]; GX = XT["go"]; GS = ST["go"][sub]; gN = SS["gb"]; gb = L["gb"]
    W = os.path.join(HERE, "chunks", f"{lev}_{foot}_{mode}"); os.makedirs(W, exist_ok=True); capd, capa = CAPS[lev]; t0 = time.time(); Cl = closure(L, n0, capd, capa)
    info = {k: Cl[k] for k in ("n_mono_a", "n_mono_d", "n_d_before", "n_a_before", "n_a0", "d_stopped")}; info.update(nD=len(Cl["Dn"]), nA=len(Cl["An"]), secs=time.time() - t0); print(foot, mode, lev, info, flush=True)
    with gzip.open(os.path.join(W, "names.json.gz"), "wt") as f: json.dump(dict(D=Cl["Dn"], A=Cl["An"], A0=Cl["A0n"]), f)
    json.dump(info, open(os.path.join(W, "info.json"), "w"))
    Av, Dv = Cl["Av"], Cl["Dv"]; A0v = Cl["A0v"]; gb1 = gb
    RL = float(np.sqrt((np.log10(GS / I1(gb[iS], a0)) ** 2).mean()))
    T = dict(enum=0, saturn=0, newton=0, cass=0, xcop=0, xcop_cass=0, sub=0, sub_cass=0, dropped=0); df = os.path.join(W, "done.txt"); done = set(open(df).read().split()) if os.path.exists(df) else set(); tf = os.path.join(W, "tally.json")
    if os.path.exists(tf): T = json.load(open(tf))
    HL = open(os.path.join(W, "hits.jsonl"), "a"); DF = open(df, "a"); stop = [0]; signal.signal(signal.SIGTERM, lambda *a: stop.__setitem__(0, 1)); hsz = [os.path.getsize(os.path.join(W, "hits.jsonl"))]; dist = set(); ds = os.path.join(W, "distinct.json")
    NEFF = [0]
    if os.path.exists(ds): NEFF[0] = json.load(open(ds))
    def judge(F, tag):
        """F n x columns. tag: list prefix for hits, i index array supplied by caller as extra columns (rows give ids)."""
        ok = np.all(np.isfinite(F), axis=1) & np.all(F > 0, axis=1); return ok
    def stage(F, ids, base):
        T["saturn"] += len(F)
        if not len(F): return
        ok = np.all(np.isfinite(F), axis=1) & np.all(F > 0, axis=1); n = (np.abs(F[:, :3] / gN - 1) <= EPS).all(axis=1) & ok; T["newton"] += int(n.sum()); F = F[n]; ids = ids[n]
        if not len(F): return
        cas = (np.abs(F[:, :3] - gN) <= CAS).all(axis=1); T["cass"] += int(cas.sum()); dx = np.log10(GX / F[:, ix]); m = dx.mean(axis=1); rm = np.sqrt((dx * dx).mean(axis=1)); k = (np.abs(m) <= xm) & (rm <= xr)
        hs = np.abs(np.round(dx[:, :4], 5) + 0.0).sum(axis=1) * 1e5; samp = (hs.astype(np.int64) % 64 == 0)
        for h in np.round(dx[samp][:, :6], 5):
            if len(dist) < 2000000: dist.add(h.tobytes())
        if lev == "L2": sig2 = XT["se"] ** 2 + XT["sm"] ** 2; zm_ = m[:, None]; zs = (((dx - zm_) ** 2 / sig2).sum(axis=1) - (nx - 1)) / math.sqrt(2 * (nx - 1)); cm = np.array([dx[:, XT["gid"] == u].mean(axis=1) for u in np.unique(XT["gid"])]); Zm = m / np.hypot(cm.std(axis=0, ddof=1) / math.sqrt(cm.shape[0]), .12); k &= (rm <= .15) | ((np.abs(Zm) <= 2) & (zs <= 2))
        T["xcop"] += int(k.sum()); T["xcop_cass"] += int((k & cas).sum()); F = F[k]; ids = ids[k]; cas = cas[k]
        if not len(F): return
        ds_ = np.log10(GS / F[:, iS]); r = np.sqrt((ds_ * ds_).mean(axis=1)); md = np.median(ds_, axis=1); k = (r <= SF * RL) & (np.abs(md) <= SM); T["sub"] += int(k.sum()); T["sub_cass"] += int((k & cas).sum())
        for q, c in zip(ids[k], cas[k]):
            if hsz[0] > 200e6: T["dropped"] += 1; continue
            s = json.dumps([base, *[float(x) if isinstance(x, float) else int(x) for x in q.tolist()], int(c)]); HL.write(s + "\n"); hsz[0] += len(s) + 1
    def expand(lo, hi, makeF, base, cols=None):
        """lo, hi per left index into sorted right: evaluate pairs."""
        act = np.nonzero(hi > lo)[0]; T["enum"] += 0
        for i in act:
            a, b = int(lo[i]), int(hi[i])
            for s_ in range(a, b, 4000):
                e = min(b, s_ + 4000); F = makeF(int(i), np.arange(s_, e)); ids = np.c_[np.full(e - s_, i), np.arange(s_, e)]; stage(F, ids, base)
    sat = 0  # Saturn column; A sorted once per closure
    oa = np.argsort(Av[:, sat]); As = Av[oa, sat]; pos = (As > 0) & np.isfinite(As); As_f = As.copy(); As_f[~np.isfinite(As_f)] = np.inf; Av2 = Av[oa]; good = np.isfinite(Av2[:, sat]); oD = np.argsort(np.where(np.isfinite(Dv[:, sat]), Dv[:, sat], np.inf)); Dv2 = Dv[oD]; Ds = Dv2[:, sat]; Ds_f = np.where(np.isfinite(Ds), Ds, np.inf)
    json.dump(dict(oa=oa.tolist(), oD=oD.tolist()), gzip.open(os.path.join(W, "order.json.gz"), "wt"))
    g0 = gN[sat]; gl, gh_ = g0 * (1 - EPS), g0 * (1 + EPS); nA = len(As); nD = len(Ds)
    def ckpt(j):
        DF.write(j + "\n"); DF.flush(); json.dump(T, open(tf, "w")); json.dump(NEFF[0] + len(dist) * 64, open(ds + ".tmp", "w")); os.replace(ds + ".tmp", ds); HL.flush(); print(j, f"{time.time()-t0:.0f}s", {k: T[k] for k in T}, f"distinct~{NEFF[0] + len(dist) * 64}", flush=True)
    # T1: I_k(A, B), A, B positive, by bisection on Y for the window
    fpos = np.nonzero(np.isfinite(As) & (As > 0))[0]; L_ = fpos.min() if len(fpos) else 0; U_ = fpos.max() + 1 if len(fpos) else 0; xs = As[L_:U_]; Z_ = int(np.searchsorted(As, 0.0, "left"))
    for k, fn in IK.items():
        j = f"T1|{k}"
        if j in done: continue
        lo_y = np.full_like(xs, 1e-60); hi_y = np.full_like(xs, 1e60)
        def solve(tgt):
            a = np.log(lo_y); b = np.log(hi_y)
            for _ in range(70):
                m = 0.5 * (a + b); v = fn(xs, np.exp(m)); up = v > tgt; v = np.where(np.isfinite(v), v, np.inf); up = v > tgt; b = np.where(up, m, b); a = np.where(up, a, m)
            return np.exp(0.5 * (a + b))
        yl, yh = solve(gl), solve(gh_); ys = As[Z_:U_]; il = np.searchsorted(ys, yl, "left"); ih = np.searchsorted(ys, yh, "right"); T["enum"] += len(xs) * len(ys)
        il = np.where(fn(xs, np.full_like(xs, 1e-60)) >= gl, 0, il)  # Y = 0 at Saturn (gas terms) belongs in the window when X alone reaches it
        act = np.nonzero(ih > il)[0]; base = f"T1|{k}"
        for i in act:
            for s_ in range(int(il[i]), int(ih[i]), 4000):
                e = min(int(ih[i]), s_ + 4000); F = fn(Av2[L_ + i][None, :], Av2[Z_ + s_:Z_ + e]); stage(F, np.c_[np.full(e - s_, L_ + i), np.arange(Z_ + s_, Z_ + e)], base)
            if stop[0]: print("SIGTERM", flush=True); return
        ckpt(j)
    # T2: A + B, A - B
    for sg, tag in ((1.0, "T2p"), (-1.0, "T2m")):
        if tag in done: continue
        fin = np.nonzero(np.isfinite(As))[0]; a_ = As[fin]; Vf = Av2[fin]; T["enum"] += len(a_) ** 2
        if sg > 0: il = np.searchsorted(a_, gl - a_, "left"); ih = np.searchsorted(a_, gh_ - a_, "right")
        else: il = np.searchsorted(a_, a_ - gh_, "left"); ih = np.searchsorted(a_, a_ - gl, "right")
        for i in np.nonzero(ih > il)[0]:
            for s_ in range(int(il[i]), int(ih[i]), 4000):
                e = min(int(ih[i]), s_ + 4000); F = Vf[i][None, :] + sg * Vf[s_:e]; stage(F, np.c_[np.full(e - s_, fin[i]), fin[s_:e]], tag)
            if stop[0]: print("SIGTERM", flush=True); return
        ckpt(tag)
    # T3: I_k(g_b, a0) x H, H = D op D
    finD = np.nonzero(np.isfinite(Ds))[0]; d_ = Ds[finD]; VD = Dv2[finD]
    for k, fn in IK.items():
        base = fn(gb, a0); r0 = base[sat] / g0; wl, wh = (1 - EPS) / r0, (1 + EPS) / r0
        for op in "+-*/":
            tag = f"T3|{k}|{op}"
            if tag in done: continue
            T["enum"] += len(d_) ** 2
            with np.errstate(all="ignore"):
                if op == "+": il = np.searchsorted(d_, wl - d_, "left"); ih = np.searchsorted(d_, wh - d_, "right")
                elif op == "-": il = np.searchsorted(d_, d_ - wh, "left"); ih = np.searchsorted(d_, d_ - wl, "right")
                elif op == "*": a = np.where(d_ != 0, wl / d_, np.inf); b = np.where(d_ != 0, wh / d_, -np.inf); il = np.searchsorted(d_, np.minimum(a, b), "left"); ih = np.searchsorted(d_, np.maximum(a, b), "right")
                else: a = d_ / wh; b = d_ / wl; il = np.searchsorted(d_, np.minimum(a, b), "left"); ih = np.searchsorted(d_, np.maximum(a, b), "right")
            for i in np.nonzero(ih > il)[0]:
                for s_ in range(int(il[i]), int(ih[i]), 4000):
                    e = min(int(ih[i]), s_ + 4000); y = VD[s_:e]; x = VD[i][None, :]; H = x + y if op == "+" else x - y if op == "-" else x * y if op == "*" else x / y; stage(H * base, np.c_[np.full(e - s_, finD[i]), finD[s_:e]], tag)
                if stop[0]: print("SIGTERM", flush=True); return
            ckpt(tag)
    # T4: A0 x H, H in D2
    a0s = A0v[:, sat]
    tag = "T4"
    if tag not in done:
        T["enum"] += len(a0s) * len(d_)
        for i in np.nonzero(np.isfinite(a0s) & (a0s > 0))[0]:
            il, ih = np.searchsorted(d_, gl / a0s[i], "left"), np.searchsorted(d_, gh_ / a0s[i], "right")
            for s_ in range(int(il), int(ih), 4000):
                e = min(int(ih), s_ + 4000); stage(A0v[i][None, :] * VD[s_:e], np.c_[np.full(e - s_, i), finD[s_:e]], tag)
            if stop[0]: print("SIGTERM", flush=True); return
        ckpt(tag)
    # T5: FITTED, k grid
    KG = np.logspace(-3, 3, 81)
    for k, fn in IK.items():
        base = fn(gb, a0); r0 = base[sat] / g0
        for q, kk in enumerate(KG):
            tag = f"T5|{k}|{q}"
            if tag in done: continue
            T["enum"] += len(d_) + len(a_)
            # I_k (1 + k H)
            il, ih = np.searchsorted(d_, ((1 - EPS) / r0 - 1) / kk, "left"), np.searchsorted(d_, ((1 + EPS) / r0 - 1) / kk, "right")
            for s_ in range(int(il), int(ih), 4000):
                e = min(int(ih), s_ + 4000); stage(base[None, :] * (1 + kk * VD[s_:e]), np.c_[np.full(e - s_, q), finD[s_:e]], f"T5m|{k}")
            il, ih = np.searchsorted(a_, (gl - base[sat]) / kk, "left"), np.searchsorted(a_, (gh_ - base[sat]) / kk, "right")
            for s_ in range(int(il), int(ih), 4000):
                e = min(int(ih), s_ + 4000); stage(base[None, :] + kk * Vf[s_:e], np.c_[np.full(e - s_, q), fin[s_:e]], f"T5a|{k}")
            if stop[0]: print("SIGTERM", flush=True); return
            DF.write(tag + "\n")
        ckpt(f"T5|{k}")
    open(os.path.join(W, "COMPLETE"), "w").write("1"); ckpt("ALL"); print("DONE", foot, mode, lev, T, flush=True)
if __name__ == "__main__": main()
