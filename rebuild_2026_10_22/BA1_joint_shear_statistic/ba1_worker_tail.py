# BA1 tail: in place of the grader's last line. R among the 15 measured keys, common draws, and the same from the 30-patch jackknife.
_N = N; _RNG = np.random.default_rng(20261031); _Cb = NX["counts"](_RNG.integers(0, _N, size=(2000, _N)), _N); _pp = NX["PATCH"]; _Jr = np.array([(_pp != q).astype(float) for q in range(30) if np.any(_pp == q)]); _MEAS = NX["MEAS"]; _wls = NX["wls"]
def _keys(W, f_, h_):
    c = _MEAS[(f_, h_)]; bi = {b: BN.index(b) for b in BN}; O = {}; n, d = c["n"], c["d"]; rr = lambda Ix, b: (W[:, Ix] @ n[Ix, bi[b]]) / (W[:, Ix] @ d[Ix, bi[b]])
    O["G-IN-all"] = rr(I, "INNER")
    for t in range(3): O[f"G-MID-T{t + 1}"] = rr(I[TID == t], "MID")
    O["G-MID-b"] = _wls(W[:, I], X1m, n[I, bi["MID"]], d[I, bi["MID"]])[:, 1]; O["G-OUT-all"] = rr(I, "OUTER")
    for t in range(3): O[f"G-OUT-T{t + 1}"] = rr(I[TID == t], "OUTER")
    O["G-OUT-b"] = _wls(W[:, I], X1m, n[I, bi["OUTER"]], d[I, bi["OUTER"]])[:, 1]; O["G-OUT-Mall"] = rr(ALLI, "OUTER")
    for t in range(3): O[f"G-OUT-M{t + 1}"] = rr(np.where(T3M == t)[0], "OUTER")
    O["G-IN-Mall"] = rr(ALLI, "INNER"); return O
_OUT = {}
for h_ in HK:
    Kb = _keys(_Cb, "canonical", h_); Kj = _keys(_Jr, "canonical", h_); ks = list(Kb); Xb = np.array([Kb[k] for k in ks]); Xj = np.array([Kj[k] for k in ks]); nj = Xj.shape[1]; Dj = Xj - Xj.mean(1, keepdims=True); Cj = (nj - 1) / nj * Dj @ Dj.T
    _OUT[h_] = dict(keys=ks, R_boot=np.corrcoef(Xb).tolist(), R_jack=(Cj / np.sqrt(np.outer(np.diag(Cj), np.diag(Cj)))).tolist(), sd_boot=Xb.std(1, ddof=1).tolist(), sd_jack=np.sqrt(np.diag(Cj)).tolist())
json.dump(_OUT, open(os.environ["BA1_OUT"], "w"), indent=1, default=float); sys.exit(0)
