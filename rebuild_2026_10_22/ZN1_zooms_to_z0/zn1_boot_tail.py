# ZN1 bootstrap (AMENDMENT A2 item 3): inside the grader's namespace, after the full grade. Regrades clusters and X-COP on the median shape of each draw of seeds; the first pass uses every seed once and must reproduce the full grade.
_ZB0 = {_M: {_z: _ZS[_M][_z] for _z in ("0.50", "0.25", "0.00")} for _M in ("1e13", "1e14")}; _ZBS = {_M: sorted(set.intersection(*[{q["seed"] for q in _ZB0[_M][_z]["seeds"]} for _z in _ZB0[_M]])) for _M in _ZB0}
def _zb_set(picks):
    for _M, _pk in picks.items():
        for _z in ("0.50", "0.25", "0.00"):
            _by = {q["seed"]: q for q in _ZB0[_M][_z]["seeds"]}; _sel = [_by[_ZBS[_M][i]] for i in _pk]
            _ZS[_M][_z] = dict(lgM=float(np.median([q["lgM"] for q in _sel])), x_edge=min(q["x_edge"] for q in _sel), lnm=np.median(np.array([q["lnm"] for q in _sel]), axis=0).tolist())
def _zb_one():
    _c = grade_clusters("canonical")["cells"]; _x = _grade("canonical"); return dict(cells=_c, mean=_x["mean"], rms=_x["rms"], by_x=_x["by_x"])
_zb_set({_M: list(range(len(_ZBS[_M]))) for _M in _ZB0}); _t0 = time.time() if "time" in globals() else 0; _b0 = _zb_one(); _c0 = RES["footings"]["canonical"]["clusters"]["cells"]
_OUT["boot_k"] = max(abs(_b0["cells"][h_][k_]["pred"] - _c0[h_][k_]["pred"]) for h_ in HK for k_ in _c0[h_]); _OUT["boot_kx"] = abs(_b0["rms"] - _OUT["footings"]["canonical"]["rms"]); _OUT["boot_n"] = {_M: len(_ZBS[_M]) for _M in _ZB0}
_bi, _bn = (int(v_) for v_ in os.environ["ZN1_BOOT_CHUNK"].split("/")); _OUT["boot"] = []
for _d in range(int(os.environ["ZN1_BOOT"])):
    if _d % _bn != _bi: continue
    _rng = np.random.default_rng(1000 + _d); _zb_set({_M: _rng.integers(0, len(_ZBS[_M]), len(_ZBS[_M])).tolist() for _M in ("1e13", "1e14")}); _OUT["boot"].append(dict(draw=_d, **_zb_one()))
    json.dump(_OUT["boot"], open(os.environ["XH1_OUT"] + ".part", "w"), default=float)
