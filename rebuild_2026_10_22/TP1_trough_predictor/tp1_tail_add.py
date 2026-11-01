# TP1 tail, after UR1's helpers. Per-galaxy Upsilon. Reads only.
def _run6(mode):
    global CN1_MODE
    SLMAP["m"] = "EM1"; SLDL[0] = 0.0; CN1_MODE = mode; GHSTORE.clear(); sparc("canonical", "A_c2b_refit"); return _gals_U("A_c2b_refit")
json.dump(dict(off=_run6("off"), blum=_run6("blum")), open(os.environ["SL1_OUT"], "w"), indent=1, default=float); print("TP1 done", flush=True); sys.exit(0)
