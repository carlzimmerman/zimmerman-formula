# FG1 law tail, after UR1's helpers. Reads only: the a0 law on UR2's galaxies, grid and LITTLE THINGS systems. kappa = 1/2 FITTED.
_MUT = os.environ.get("FG1_MUTATE") == "1"; _A = dict(canonical=9.3603e-11, alt=1.1312e-10); _R = {}
def _nu(gN, a0): return np.ones_like(gN) if _MUT else 0.5 + np.sqrt(0.25 + a0 / np.maximum(gN, 1e-300))
for f_, a0 in _A.items():
    _R[f_] = {}
    for t in _TG:
        U = {}
        for q in GALS: U[q["name"]] = float(UPS[int(fit_one(q, np.log10(np.maximum(q["GB"] * _nu(q["GB"], a0), 1e-300)))[2])])
        v = np.array([_TB[n]["vf"] if n in _TB else np.nan for n in U]); Q = np.array([(_TB[n]["Q"] <= 2 and _TB[n]["inc"] >= 30) if n in _TB else False for n in U]); u = np.array(list(U.values())); lo = Q & (v > 0) & (v < 100); hi = Q & (v > 150); E = []
        for r_ in _C["lt"]:
            R_ = r_["R"] * MPCE / 1e3; gN = GE * 10 ** r_["logMb"] * MSUNE / R_ ** 2; E.append(math.log10((r_["V"] * 1e3) ** 2 / R_) - math.log10(gN * float(_nu(np.array(gN), a0))))
        _R[f_][t] = dict(U=float(np.median(u)), tilt=float(np.median(u[lo]) - np.median(u[hi])), bins={f"{l}-{h}": float(np.median(u[Q & (v >= l) & (v < h)])) for l, h in _BIN}, lt=float(np.median(E)))
json.dump(_R, open(os.environ["SL1_OUT"], "w"), indent=1, default=float); print("FG1 law done", flush=True); sys.exit(0)
