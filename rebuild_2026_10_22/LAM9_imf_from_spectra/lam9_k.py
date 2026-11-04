"""LAM9 K1 (Gamma_b / alpha recovery at the sums' S/N) and K2 (h4 leak), as frozen in 9c1f411110 with amendment A1.
300 synthetics, 100 per third of the step-5 sample's chi2_kin-scaled Na I S/N; donors are the first 100 successful variant-A
fits of each third in lam9_k_donors.csv order. Same job contract as lam9_fit.py (exit 75 on SIGTERM/YIELD, --resume).
  python3 -I lam9_k.py --shard K --nshard N [--resume]      synthetics i with i mod N == K
  python3 -I lam9_k.py --summarize                          lam9_k.jsonl, lam9_k.out, lam9_k.json in this folder
κ = ½ FITTED; not theory closed."""
import os, sys, json, signal, time, warnings
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[_v] = "1"  # before numpy
warnings.filterwarnings("ignore", message=".*encountered in matmul", category=RuntimeWarning)
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
from ppxf.ppxf import ppxf
import lam9_core as L
QY = os.path.join(L.ROOT, "compute_queue", "YIELD"); KD = os.path.join(L.WORK, "k"); os.makedirs(KD, exist_ok=True)
GIN = [0.80, 1.30, 1.50, 1.80, 2.00, 2.30, 2.50, 2.80, 3.00, 3.30]
stop = False
def _term(*_):
    global stop; stop = True
signal.signal(signal.SIGTERM, _term); signal.signal(signal.SIGINT, _term)
arg = sys.argv[1:]
def opt(k, d=None): return arg[arg.index(k) + 1] if k in arg else d

def fitted():
    D = {}
    for fn in sorted(os.listdir(os.path.join(L.WORK, "fits"))):
        if fn.endswith(".jsonl"):
            for r in L.read_jsonl(os.path.join(L.WORK, "fits", fn)): D.setdefault(r["plateifu"], {})[r["variant"]] = r
    return D
def plan():
    D = fitted(); thirds = {0: [], 1: [], 2: []}; short = []
    for l in [x for x in open(os.path.join(HERE, "lam9_k_donors.csv")).read().splitlines() if x.strip() and not x.startswith("#")][1:]:
        t, o, pf = l.strip().split(","); t = int(t)
        if len(thirds[t]) < 100 and D.get(pf, {}).get("A", {}).get("status") == "ok": thirds[t].append(pf)
    for t in range(3):
        if len(thirds[t]) < 100: short.append(t)
    rng = np.random.default_rng(L.SEED); P = []
    for i in range(300):
        P.append(dict(i=i, third=i // 100, donor=thirds[i // 100][i % 100] if len(thirds[i // 100]) > i % 100 else None,
                      gamma_in=float(rng.choice(GIN)), seed=int(rng.integers(2 ** 31))))
    return P, short

def run(k, nk):
    P, short = plan()
    if short: print(f"donor thirds {short} have fewer than 100 successful fits: fit more donors first", flush=True); sys.exit(1)
    S = L.sample(); wave, narrow = L.load_stack(); T = L.tlib(); out = os.path.join(KD, f"lam9_k.s{k}of{nk}.jsonl"); L.read_jsonl(out, repair=True)
    done = {r["i"] for r in L.read_jsonl(out)}; mine = [q for q in P if q["i"] % nk == k and q["i"] not in done]
    print(f"K shard {k}/{nk}: {len(mine)} to do", flush=True)
    if not mine: sys.exit(0)
    ig = {g: int(np.argmin(np.abs(np.unique(T["gamma"]) - g))) for g in GIN}
    with open(out, "a") as fo:
        for q in mine:
            if stop or os.path.exists(QY): print("yield: exit 75", flush=True); fo.close(); sys.exit(75)
            t0 = time.time(); pf = q["donor"]; kin = S["FIT"][pf]; p = L.prep(S["path"][pf], narrow); tpl, lam_t, n_t = L.templates_for(p)
            W = np.load(os.path.join(L.WORK, "w", f"{pf}_A.npz")); wb = W["wb"].astype(float); mp = W["mpoly"].astype(float); chi2a = float(W["chi2a"])
            WL = wb.reshape(L.REG_DIM).sum(axis=2); w_in = np.zeros(L.REG_DIM); w_in[:, :, ig[q["gamma_in"]]] = WL; w_in = w_in.ravel()
            r = dict(i=q["i"], third=q["third"], donor=pf, gamma_in=q["gamma_in"], seed=q["seed"])
            try:
                truth = L.summary(w_in, n_t); r.update(alpha_in=truth["alpha"], gamma_in_lw=truth["gamma"])
                pc = ppxf((tpl @ w_in)[:, None], p["flux"] / mp, p["noise"] / mp, L.VELSCALE, L.kin_start(kin), moments=6, fixed=[1] * 6, degree=-1, mdegree=0,
                          goodpixels=p["goodA"], lam=p["lam"], lam_temp=lam_t, quiet=True)
                syn = pc.bestfit * mp * (1 + narrow[p["idx"]])
                syn = syn + np.random.default_rng(q["seed"]).normal(0, 1, syn.size) * np.where(p["noise"] < 1e9, p["noise"], 0) * np.sqrt(max(chi2a, 1.0))
                for v in ("A", "B"):
                    f = L.fit(p, tpl, lam_t, kin, v, flux=syn); s = L.summary(f["wb"], n_t); r[f"gamma_{v}"] = s["gamma"]; r[f"alpha_{v}"] = s["alpha"]; r[f"chi2a_{v}"] = f["chi2a"]
                    sa = L.summary(f["wa"], n_t); r[f"gamma_a_{v}"] = sa["gamma"]; r[f"alpha_a_{v}"] = sa["alpha"]  # step a, reported (A1)
                if q["i"] < 100:
                    for sg, dh in (("p", 0.03), ("m", -0.03)):
                        f = L.fit(p, tpl, lam_t, kin, "A", flux=syn, dh4=dh); r[f"alpha_h4{sg}"] = L.summary(f["wb"], n_t)["alpha"]
                r["status"] = "ok"
            except Exception as ex: r["status"] = f"error: {ex}"
            r["sec"] = round(time.time() - t0, 1); L.append_jsonl(fo, r)
    sys.exit(0)

def summarize(iqr_h4=None):
    rows = []
    for fn in sorted(os.listdir(KD)):
        if fn.endswith(".jsonl"): rows += L.read_jsonl(os.path.join(KD, fn), repair=True)
    rows = sorted({r["i"]: r for r in rows}.values(), key=lambda r: r["i"]); ok = [r for r in rows if r["status"] == "ok"]
    json.dump(dict(note="κ = ½ FITTED; not theory closed. One row per K synthetic (lam9_k.py).", rows=rows), open(os.path.join(HERE, "lam9_k_rows.json.tmp"), "w", encoding="utf-8"),
              indent=0, ensure_ascii=False, default=float); os.replace(os.path.join(HERE, "lam9_k_rows.json.tmp"), os.path.join(HERE, "lam9_k_rows.json"))
    if iqr_h4 is None:
        S = L.sample(); P = json.load(open(os.path.join(HERE, "lam9_prepare.json"))); h = [S["FIT"][r["plateifu"]]["h4"] for r in P["rows"] if r["step5"]]
        iqr_h4 = float(np.subtract(*np.percentile(h, [75, 25])))
    O = [f"LAM9 K control: {len(ok)} of {len(rows)} synthetics ok (300 planned). κ = ½ FITTED; not theory closed."]; R = {"note": "κ = ½ FITTED; not theory closed", "n": len(rows), "n_ok": len(ok)}
    for v in ("A", "B"):
        dg = np.array([r[f"gamma_{v}"] - r["gamma_in"] for r in ok]); da = np.array([np.log10(r[f"alpha_{v}"] / r["alpha_in"]) for r in ok])
        lines = dict(gamma_bias=float(np.median(dg)), gamma_rms=float(np.sqrt(np.mean(dg ** 2))), lalpha_bias=float(np.median(da)), lalpha_rms=float(np.sqrt(np.mean(da ** 2))))
        p = abs(lines["gamma_bias"]) <= 0.15 and lines["gamma_rms"] <= 0.40 and abs(lines["lalpha_bias"]) <= 0.03 and lines["lalpha_rms"] <= 0.10
        sl = float(np.polyfit([r["gamma_in"] for r in ok], [r[f"gamma_{v}"] for r in ok], 1)[0])
        R[f"K1_{v}"] = dict(**lines, slope=sl, PASS=bool(p) and len(rows) == 300)
        O.append(f"K1 variant {v}: Gamma_b bias {lines['gamma_bias']:+.3f} (|.| <= 0.15), rms {lines['gamma_rms']:.3f} (<= 0.40); log alpha bias {lines['lalpha_bias']:+.4f} dex (|.| <= 0.03), "
                 f"rms {lines['lalpha_rms']:.4f} (<= 0.10); slope {sl:.3f}: {'PASS' if R[f'K1_{v}']['PASS'] else 'FAIL'}")
        for t in range(3):
            q = [r for r in ok if r["third"] == t]; dgt = np.array([r[f"gamma_{v}"] - r["gamma_in"] for r in q]); dat = np.array([np.log10(r[f"alpha_{v}"] / r["alpha_in"]) for r in q])
            O.append(f"   S/N third {t + 1}: n {len(q)}, Gamma_b bias {np.median(dgt):+.3f} rms {np.sqrt(np.mean(dgt ** 2)):.3f}; log alpha bias {np.median(dat):+.4f} rms {np.sqrt(np.mean(dat ** 2)):.4f}")
        dga = np.array([r[f"gamma_a_{v}"] - r["gamma_in"] for r in ok]); daa = np.array([np.log10(r[f"alpha_a_{v}"] / r["alpha_in"]) for r in ok])
        R[f"stepa_row_{v}"] = dict(gamma_bias=float(np.median(dga)), gamma_rms=float(np.sqrt(np.mean(dga ** 2))), lalpha_bias=float(np.median(daa)), lalpha_rms=float(np.sqrt(np.mean(daa ** 2))))
        O.append(f"   row, not graded (A1): step a (unregularised) variant {v}: Gamma_b bias {np.median(dga):+.3f} rms {np.sqrt(np.mean(dga ** 2)):.3f}; "
                 f"log alpha bias {np.median(daa):+.4f} rms {np.sqrt(np.mean(daa ** 2)):.4f}")
    k2 = [r for r in ok if "alpha_h4p" in r]
    b = float(np.median([(np.log10(r["alpha_h4p"]) - np.log10(r["alpha_h4m"])) / 0.06 for r in k2])) if k2 else float("nan")
    lean = 0.69 * np.log(10) * abs(b) * iqr_h4; R["K2"] = dict(n=len(k2), b=b, iqr_h4=iqr_h4, lean_ln=float(lean), PASS=bool(lean <= 0.01 and len(k2) == 100))
    O.append(f"K2 h4 leak: n {len(k2)}, b = dlog alpha/dh4 {b:+.4f} dex; 0.69 ln10 |b| IQR(h4) = {lean:.4f} ln (IQR {iqr_h4:.4f}; <= 0.01): {'PASS' if R['K2']['PASS'] else 'FAIL'}")
    print("\n".join(O), flush=True); open(os.path.join(HERE, "lam9_k.out"), "w", encoding="utf-8").write("\n".join(O) + "\n")
    json.dump(R, open(os.path.join(HERE, "lam9_k.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False); return R

if __name__ == "__main__":
    if "--summarize" in arg: summarize()
    else: run(int(opt("--shard", "0")), int(opt("--nshard", "1")))
