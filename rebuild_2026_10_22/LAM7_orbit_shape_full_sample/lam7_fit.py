"""LAM7: fit each new sum once with LAM4's prep()/run() unchanged; --k2 runs LAM4's K2 (A1 scaling) on the new sums.
Run: python3 -I lam7_fit.py [--k2]. Single thread, preemptible. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, glob, signal
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(RB, "LAM4_whole_galaxy_absorption")); import lam4_fit as L
import numpy as np
L.SUMS = os.path.join(os.path.dirname(RB), "_external_data", "lam7_integrated_2026_11_04")
stop = False
def _term(*_):
    global stop; stop = True
signal.signal(signal.SIGTERM, _term)
def fit_all():
    out = os.path.join(HERE, "lam7_fit.jsonl"); done = {json.loads(l)["plateifu"] for l in open(out)} if os.path.exists(out) else set()
    with open(out, "a") as fo:
        for fn in sorted(glob.glob(os.path.join(L.SUMS, "*.npz"))):
            if stop: break
            pifu = os.path.basename(fn)[:-4]
            if pifu in done: continue
            try:
                p = L.prep(fn); pp = L.run(p, p["flux"]); e = pp.error * np.sqrt(pp.chi2)
                r = dict(status="ok", V=pp.sol[0], sigma=pp.sol[1], h3=pp.sol[2], h4=pp.sol[3], h5=pp.sol[4], h6=pp.sol[5], eV=e[0], esigma=e[1],
                         eh4=e[3], eh6=e[5], chi2=float(pp.chi2), ngood=int(len(p["good"])), start=p["start"],
                         sn=float(np.median(p["flux"][p["good"]] / p["noise"][p["good"]])))
            except Exception as ex: r = dict(status=f"error: {ex}")
            r["plateifu"] = pifu; fo.write(json.dumps(r, default=float) + "\n"); fo.flush()
def k2():
    out = os.path.join(HERE, "lam7_k2.jsonl"); files = sorted(glob.glob(os.path.join(L.SUMS, "*.npz")))
    F = [json.loads(l) for l in open(os.path.join(HERE, "lam7_fit.jsonl"))]
    sig = np.array([v["sigma"] for v in F if v["status"] == "ok"]); rng = np.random.default_rng(L.SEED)
    plan = [(i, files[int(rng.integers(len(files)))], float(rng.choice(sig)), float(rng.uniform(-0.10, 0.10)), int(rng.integers(2**31))) for i in range(200)]
    done = {json.loads(l)["i"] for l in open(out)} if os.path.exists(out) else set()
    with open(out, "a") as fo:
        for i, fn, s, h4, ns in plan:
            if stop: break
            if i in done: continue
            r = dict(i=i, plateifu=os.path.basename(fn)[:-4], sigma_in=s, h4_in=h4)
            try:
                p = L.prep(fn); pp = L.run(p, p["flux"]); tpl = p["temps"] @ pp.weights
                mod = L.run(p, p["flux"], temps=tpl[:, None], start=[0.0, s, 0.0, h4, 0.0, 0.0], fixed=[1] * 6, degree=-1).bestfit
                mod = mod / np.median(mod[p["good"]])
                syn = mod + np.random.default_rng(ns).normal(0, 1, mod.size) * np.where(p["noise"] < 1e9, p["noise"], 0) * np.sqrt(max(pp.chi2, 1.0))
                q = L.run(p, syn); r.update(status="ok", h4_out=float(q.sol[3]), sigma_out=float(q.sol[1]))
            except Exception as ex: r["status"] = f"error: {ex}"
            fo.write(json.dumps(r) + "\n"); fo.flush()
    rows = [json.loads(l) for l in open(out)]; ok = [x for x in rows if x["status"] == "ok"]
    if len(rows) == 200:
        d = np.array([x["h4_out"] - x["h4_in"] for x in ok]); rms = float(np.sqrt(np.mean(d**2)))
        txt = f"K2: {len(ok)} of 200 ok; recovered h4 rms {rms:.4f} (<= 0.03): {'PASS' if rms <= 0.03 else 'FAIL -> h4 NOT MEASURABLE'}; bias {np.mean(d):+.4f}"
        print(txt); open(os.path.join(HERE, "lam7_k2.out"), "w").write(txt + "\n")
        json.dump(dict(rms=rms, pass_=bool(rms <= 0.03), n_ok=len(ok)), open(os.path.join(HERE, "lam7_k2.json"), "w"), indent=1)
if __name__ == "__main__":
    k2() if "--k2" in sys.argv else fit_all()
