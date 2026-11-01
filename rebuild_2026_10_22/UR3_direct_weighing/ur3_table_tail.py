# UR3 table tail, after UR1's helpers. Writes S(M200) as the grader computes it. Msun/kpc^2.
_U = MSUNE / (MPCE / 1e3) ** 2; _G = np.arange(9.0, 14.01, 0.05); _J = dict(lgM=_G.tolist(), S={}, bg={})
for t in _TG:
    _J["S"][t] = [float(sig_core("canonical", t, 10 ** g / FC1_MC)[0] / _U) for g in _G]; _J["bg"][t] = dict(a=BGS[t]["a"], b=BGS[t]["b"], h=BGS[t]["h"])
json.dump(_J, open(os.environ["SL1_OUT"], "w"), indent=1, default=float); print("table done", flush=True); sys.exit(0)
