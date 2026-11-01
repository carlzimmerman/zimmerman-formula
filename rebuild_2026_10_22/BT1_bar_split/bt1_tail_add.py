# BT1 tail, after UR1's helpers. Reads only: per-galaxy Upsilon.
SLMAP["m"] = "EM1"; SLDL[0] = 0.0; _R = dict(U={}, tb={n: dict(vf=v["vf"], Q=v["Q"], inc=v["inc"]) for n, v in _TB.items()}, st={})
for _m in ("blum", "off"):
    CN1_MODE = _m; GHSTORE.clear(); _R["U"][_m] = {}; _R["st"][_m] = {}
    for t in _TG:
        st = sparc("canonical", t); _R["st"][_m][t] = dict(U=st["U_median"], rms=st["rms"]); _R["U"][_m][t] = _gals_U(t)
json.dump(_R, open(os.environ["SL1_OUT"], "w"), indent=1, default=float); print("BT1 done", flush=True); sys.exit(0)
