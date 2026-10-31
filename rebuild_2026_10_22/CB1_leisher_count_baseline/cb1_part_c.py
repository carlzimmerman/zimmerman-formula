#!/usr/bin/env python3
"""CB1 Part C (criteria PART_C_CRITERIA.md): authors' GNN in plain torch; arms A-D on placeholder and snapshot inputs. Preemptible per the compute_queue contract.

    python3 cb1_part_c.py run <graphs.npz> [--resume]      all 24 runs; one JSON per run in partc_runs/; partc_results.json at the end
    python3 cb1_part_c.py check <graphs.npz>               K6, K7 counts, K8 resume equivalence, K9 smoke, timing
    python3 cb1_part_c.py mutate <graphs.npz> [--resume]   permuted targets; separate outputs
Not a framework test."""
import json, os, signal, subprocess, sys, time
import numpy as np, torch
from torch import nn

HERE = os.path.dirname(os.path.abspath(__file__)); RUNS = os.path.join(HERE, "partc_runs"); STOP = []
YIELD = int(os.environ.get("HEAVYQ_YIELD_EXIT", "75")); CKE = 25
LR, WD, NL, HC, EP, BS = 1.889e-5, 5.139e-7, 4, 128, 1000, 32; PAPER = dict(P=0.509, S=0.708)
MI, MA = 1 / 30, 1 / 1.8
ARMS = dict(A=dict(u=True, add=True, tree=False), B=dict(u=False, add=True, tree=False), C=dict(u=False, add=False, tree=False), D=dict(u=False, add=True, tree=True))

def afile(path, save):
    tmp = path + ".tmp"
    with open(tmp, "wb") as f:
        save(f); f.flush(); os.fsync(f.fileno())
    os.replace(tmp, path)
def ajson(path, o): afile(path, lambda f: f.write(json.dumps(o, indent=1).encode()))

def load(path):
    Z = np.load(path); L = Z["n"]; off = np.r_[0, np.cumsum(L)]; G = []
    for k in range(len(L)):
        sn = Z["sn"][off[k]:off[k + 1]].astype(np.float32); de = Z["de"][off[k]:off[k + 1]].astype(np.int64)
        j = np.where(de >= 0)[0]; true_e = np.vstack([de[j], j])            # descendant -> progenitor, as "backwards in time"
        last = {}
        for i in j: last[int(de[i])] = int(i)                               # the authors' dict keeps the last progenitor seen per descendant
        kept = np.array(sorted(last.items()), dtype=np.int64).reshape(-1, 2).T
        G.append(dict(n=int(L[k]), sn=sn, true=true_e, auth=kept))
    return G, Z

def collate(G, ids, inp, arm):
    ns = [G[i]["n"] for i in ids]; off = np.r_[0, np.cumsum(ns)]; N = int(off[-1]); key = "true" if arm["tree"] else "auth"
    e = np.hstack([G[i][key] + o for i, o in zip(ids, off[:-1])]); b = np.repeat(np.arange(len(ids)), ns)
    x = np.ones((N, 1), np.float32) if inp == "P" else np.concatenate([G[i]["sn"] for i in ids])[:, None]
    u = np.log10(ns).astype(np.float32)[:, None] if arm["u"] else np.zeros((len(ids), 1), np.float32)
    return dict(x=torch.from_numpy(x), e=torch.from_numpy(e), b=torch.from_numpy(b), u=torch.from_numpy(u), ng=len(ids))

def pool_edges(ea, col, N):
    D = ea.shape[1]; idx = col[:, None].expand(-1, D)
    add = torch.zeros(N, D).scatter_add(0, idx, ea)
    mx = torch.zeros(N, D).scatter_reduce(0, idx, ea, "amax", include_self=False)
    cnt = torch.zeros(N, 1).scatter_add(0, col[:, None], torch.ones(len(col), 1)).clamp(min=1)
    return add, mx, add / cnt

class Layer(nn.Module):
    def __init__(s, nin, ein, out, res):
        super().__init__(); s.res = res
        s.emlp = nn.Sequential(nn.Linear(2 * nin + ein, out), nn.ReLU(), nn.Linear(out, out))
        s.nmlp = nn.Sequential(nn.Linear(nin + 3 * out + 1, out), nn.ReLU(), nn.Linear(out, out))
    def forward(s, x, e, ea, u, b):
        row, col = e; o = s.emlp(torch.cat([x[row], x[col], ea], 1)); ea2 = o + ea if s.res else o
        a, m, me = pool_edges(ea2, col, x.shape[0]); o = s.nmlp(torch.cat([x, a, m, me, u[b]], 1)); return (o + x if s.res else o), ea2

class GNN(nn.Module):
    def __init__(s, add):
        super().__init__(); s.add = add
        s.layers = nn.ModuleList([Layer(1, 3, HC, False)] + [Layer(HC, HC, HC, True) for _ in range(NL - 1)])
        s.out = nn.Sequential(nn.Linear(3 * HC + 1, HC), nn.ReLU(), nn.Linear(HC, HC), nn.ReLU(), nn.Linear(HC, HC), nn.ReLU(), nn.Linear(HC, 2))
    def forward(s, d):
        h, ea = d["x"], torch.ones(d["e"].shape[1], 3)
        for l in s.layers: h, ea = l(h, d["e"], ea, d["u"], d["b"])
        idx = d["b"][:, None].expand(-1, h.shape[1]); ng = d["ng"]
        add = torch.zeros(ng, h.shape[1]).scatter_add(0, idx, h)
        mean = add / torch.bincount(d["b"], minlength=ng)[:, None]
        mx = torch.zeros(ng, h.shape[1]).scatter_reduce(0, idx, h, "amax", include_self=False)
        return s.out(torch.cat([add if s.add else torch.zeros_like(add), mean, mx, d["u"]], 1))

def lossf(o, y):
    m = ((o[:, :1] - y) ** 2).sum(1).mean(); l = ((((o[:, :1] - y) ** 2) - o[:, 1:2] ** 2) ** 2).sum(1).mean(); return torch.log(m) + torch.log(l)

def split():
    r = json.load(open(os.path.join(HERE, "cb1_part_a_results.json"))); return r["train0"], r["valid0"], r["test0"]
def batches(ids, G, inp, arm, y):
    return [(collate(G, ids[i:i + BS], inp, arm), y[ids[i:i + BS]]) for i in range(0, len(ids), BS)]

def run_one(G, Y, inp, an, seed, tag, epochs=EP, resume=True, stop_after=None):
    """One run. Returns dict, or None after a yield. Checkpoints every CKE epochs and on SIGTERM."""
    os.makedirs(RUNS, exist_ok=True); nm = f"{inp}_{an}_s{seed}{tag}"; out = os.path.join(RUNS, nm + ".json"); ck = os.path.join(RUNS, nm + ".ckpt")
    if resume and os.path.exists(out): return json.load(open(out))
    arm = ARMS[an]; tr, va, te = split(); torch.manual_seed(seed); m = GNN(arm["add"])
    opt = torch.optim.Adam(m.parameters(), lr=LR, weight_decay=WD); sch = torch.optim.lr_scheduler.CyclicLR(opt, base_lr=LR, max_lr=1e-3, cycle_momentum=False, step_size_up=500)
    gen = np.random.default_rng(seed); best, bestv, ep = None, 1e9, 0
    if resume and os.path.exists(ck):
        c = torch.load(ck, weights_only=False); m.load_state_dict(c["m"]); opt.load_state_dict(c["o"]); sch.load_state_dict(c["s"]); gen.bit_generator.state = c["g"]; best, bestv, ep = c["b"], c["v"], c["e"]; torch.set_rng_state(c["t"])
    vb = batches(va, G, inp, arm, Y); teb = batches(te, G, inp, arm, Y)
    def save(): afile(ck, lambda f: torch.save(dict(m=m.state_dict(), o=opt.state_dict(), s=sch.state_dict(), g=gen.bit_generator.state, b=best, v=bestv, e=ep, t=torch.get_rng_state()), f))
    t0 = time.time()
    while ep < epochs:
        if STOP or (stop_after and ep == stop_after): save(); return None
        m.train(); perm = gen.permutation(len(tr))
        for i in range(0, len(tr), BS):
            ids = [tr[j] for j in perm[i:i + BS]]; d = collate(G, ids, inp, arm); opt.zero_grad(); loss = lossf(m(d), Y[ids]); loss.backward(); opt.step(); sch.step()
        m.eval()
        with torch.no_grad(): v = float(np.mean([lossf(m(d), y).item() for d, y in vb]))
        if v <= bestv: bestv = v; best = {k: x.clone() for k, x in m.state_dict().items()}
        ep += 1
        if ep % CKE == 0: save(); print(nm, ep, f"valid {v:.3f} {(time.time() - t0) / max(ep, 1):.1f} s/ep", flush=True)
    m.load_state_dict(best); m.eval()
    with torch.no_grad(): p = torch.cat([m(d)[:, 0] for d, _ in teb]).numpy()
    t = Y[te][:, 0].numpy(); P_, T_ = MI + p * (MA - MI), MI + t * (MA - MI)
    r = dict(input=inp, arm=an, seed=seed, r2=float(1 - np.sum((T_ - P_) ** 2) / np.sum((T_ - T_.mean()) ** 2)), rmse=float(np.sqrt(np.mean((T_ - P_) ** 2))), best_valid=bestv, weights_sha=_sha(best))
    ajson(out, r)
    if os.path.exists(ck): os.remove(ck)
    return r
def _sha(sd):
    import hashlib; h = hashlib.sha256()
    for k in sorted(sd): h.update(sd[k].numpy().tobytes())
    return h.hexdigest()

def target(Z):
    y = np.loadtxt(os.path.join(HERE, "authors_code", "WDM_TNG_MW_SB4_parameters.txt"))[:, 0]; return torch.tensor((y - MI) / (MA - MI), dtype=torch.float32)[:, None]

def grade(R):
    res = {}
    for inp, pap in PAPER.items():
        v = {a: [x["r2"] for x in R if x["input"] == inp and x["arm"] == a] for a in ARMS}; M = {a: float(np.mean(v[a])) for a in ARMS}
        sd = float(np.sqrt(np.mean([np.var(v[a], ddof=1) for a in ARMS]))); T = max(0.05, 2 * sd)
        g = dict(mean=M, runs=v, T=T, control="REPRODUCED" if abs(M["A"] - pap) <= 0.10 else "NOT REPRODUCED", u="U MATTERS" if M["A"] - M["B"] > T else "U NOT NEEDED", add="ADD POOL CARRIES IT" if M["B"] - M["C"] > T else "ADD POOL NOT NEEDED")
        g["branch"] = (f"BRANCHING MATTERS (D {'higher' if M['D'] > M['B'] else 'lower'})" if abs(M["D"] - M["B"]) > T else "NO BRANCHING EFFECT")
        if inp == "P": g["structure"] = "STRUCTURE ADDS" if M["C"] - 0.499 > T else "NO STRUCTURE GAIN SHOWN"
        res[inp] = g
    return res

def k6():
    """Explicit-loop calculation of one network on a 2-graph batch, for each arm's switches."""
    ok = True
    for an, arm in ARMS.items():
        torch.manual_seed(0); m = GNN(arm["add"]); e = torch.tensor([[0, 0, 1, 3], [1, 2, 3 - 0 - 2 + 0, 4]]); d = dict(x=torch.tensor([[1.], [2.], [3.], [4.], [5.]]), e=e, b=torch.tensor([0, 0, 0, 1, 1]), u=(torch.tensor([[0.3], [0.7]]) if arm["u"] else torch.zeros(2, 1)), ng=2)
        with torch.no_grad():
            got = m(d); h = d["x"].clone(); ea = torch.ones(e.shape[1], 3)
            for l in m.layers:
                new_e = []
                for k in range(e.shape[1]):
                    o = l.emlp(torch.cat([h[e[0, k]], h[e[1, k]], ea[k]])); new_e.append(o + ea[k] if l.res else o)
                new_e = torch.stack(new_e); H = []
                for i in range(5):
                    w = new_e[e[1] == i]
                    a, mx, me = (w.sum(0), w.max(0)[0], w.mean(0)) if len(w) else (torch.zeros(HC), torch.zeros(HC), torch.zeros(HC))
                    o = l.nmlp(torch.cat([h[i], a, mx, me, d["u"][d["b"][i]]])); H.append(o + h[i] if l.res else o)
                h = torch.stack(H); ea = new_e
            ou = []
            for g in range(2):
                w = h[d["b"] == g]; ou.append(m.out(torch.cat([w.sum(0) if arm["add"] else torch.zeros(HC), w.mean(0), w.max(0)[0], d["u"][g]])))
            ok &= bool(torch.allclose(got, torch.stack(ou), atol=1e-5))
    print("K6 network vs explicit loops, all arms:", "PASS" if ok else "FAIL", flush=True); return ok

def main():
    for s in (signal.SIGTERM, signal.SIGINT): signal.signal(s, lambda a, b: STOP.append(a))
    torch.set_num_threads(int(os.environ.get("HEAVYQ_THREADS", os.environ.get("OMP_NUM_THREADS", "4"))))
    mode, path = sys.argv[1], sys.argv[2]; resume = "--resume" in sys.argv; G, Z = load(path); Y = target(Z)
    if mode == "check":
        c = k6()
        if not all(G[i]["auth"].shape[1] == int(Z["ne"][i]) for i in range(len(G))): print("K7 FAIL", flush=True); c = False
        else: print("K7 edge counts equal the verbatim get_edges on all boxes: PASS; first three boxes", [(int(Z["box"][i]), G[i]["auth"].shape[1], G[i]["true"].shape[1]) for i in range(3)], flush=True)
        import shutil
        a = run_one(G, Y, "P", "A", 9, "_K8a", epochs=6, resume=False); run_one(G, Y, "P", "A", 9, "_K8b", epochs=6, resume=False, stop_after=3); b = run_one(G, Y, "P", "A", 9, "_K8b", epochs=6, resume=True)
        same = a["weights_sha"] == b["weights_sha"]; print("K8 resume equal:", "PASS" if same else "FAIL", flush=True); c &= same
        # K9: planted log N
        Yp = torch.tensor(((np.log10(Z["n"]) - np.log10(Z["n"]).min()) / np.ptp(np.log10(Z["n"]))).astype(np.float32))[:, None]
        t = time.time(); r = run_one(G, Yp, "P", "A", 9, "_K9", epochs=60, resume=False); print(f"K9 planted log N, 60 epochs R2 {r['r2']:.3f} {'PASS' if r['r2'] > 0.8 else 'FAIL'}; {(time.time() - t) / 60:.1f} s/epoch; threads {torch.get_num_threads()}", flush=True); c &= r["r2"] > 0.8
        return 0 if c else 1
    if mode == "mutate":
        Yp = Y[torch.from_numpy(np.random.default_rng(20261030).permutation(len(Y)))]; r = run_one(G, Yp, "P", "A", 1, "_MUTATE", epochs=200, resume=resume)
        if r is None: return YIELD
        ajson(os.path.join(HERE, "partc_MUTATE.json"), r); print("MUTATE R2", r["r2"], flush=True); return 0 if r["r2"] < 0.1 else 1
    res = os.path.join(HERE, "partc_results.json")
    if resume and os.path.exists(res): return 0
    R = []
    for inp in ("P", "S"):
        for an in ARMS:
            for seed in (1, 2, 3):
                r = run_one(G, Y, inp, an, seed, "", resume=True)
                if r is None: return YIELD
                R.append(r)
    ajson(res, dict(runs=R, grades=grade(R))); return 0

if __name__ == "__main__":
    sys.exit(main())
