# UL1: dump the exact sig_core on a fine grid, after UR1's helpers. Reads only.
_U = MSUNE / (MPCE / 1e3) ** 2; _G = np.arange(7.0, 15.0001, 0.005); _J = dict(lgM=_G.tolist(), S={}, bg={})
for t in _TG:
    _J["S"][t] = [float(sig_core("canonical", t, 10 ** g / FC1_MC)[0] / _U) for g in _G]; _J["bg"][t] = dict(a=BGS[t]["a"], b=BGS[t]["b"], h=BGS[t]["h"])
json.dump(_J, open(os.environ["SL1_OUT"], "w")); print("UL1 table done", flush=True); sys.exit(0)
