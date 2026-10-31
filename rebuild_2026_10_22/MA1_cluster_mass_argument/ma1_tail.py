# MA1 tail (criteria b22583d196): in place of the grader's last line. Reports the grade, then XH1's X-COP read with the same mass argument.
_st = {k: v for k, v in MA1_STAT.items() if k not in ("ratio", "sratio")}
if MA1_STAT["ratio"]:
    _st.update(ratio_med=float(np.median(MA1_STAT["ratio"])), ratio_min=float(np.min(MA1_STAT["ratio"])), ratio_max=float(np.max(MA1_STAT["ratio"])), sratio_med=float(np.median(MA1_STAT["sratio"])), sratio_min=float(np.min(MA1_STAT["sratio"])), sratio_max=float(np.max(MA1_STAT["sratio"])))
_T1 = open(os.path.join(REB, "XH1_xcop_native_rule", "xh1_tail.py")).read()
_a = 'Mfair = NAT_RRAT * Mbt; Mtot = (Mfair + Mbt) / MSUNE; s0, act = sig_core(foot, _TBG, Mtot, True); floor += 0 if act else 1'
_b = 'Mfair = NAT_RRAT * Mbt; _mbx = _gc2(_XM[nm]["Mg500"], _XM[nm]["r500"] / 1e3, _XM[nm]["z"], 3.0 * 1.2 * _XM[nm]["Mg500"] * _MSX)[0]; Mtot = ma1_arg(foot, _TBG, dict(Mfair=Mfair, Mb=_mbx, rta=rta)); s0, act = sig_core(foot, _TBG, Mtot, True); floor += 0 if act else 1'
assert _T1.count(_a) == 1; _T1 = _T1.replace(_a, _b)
_a = '_OUT["rss_gb"] = rss(); json.dump(_OUT, open(os.environ["XH1_OUT"], "w"), indent=1, default=float)\nsys.exit(0)\n'
assert _T1.count(_a) == 1; _T1 = _T1.replace(_a, "")
exec(compile(_T1, "xh1_tail_ma1", "exec"), globals())
_OUT.update(ma1=_st, mode=MA1_MODE, mult=MA1_MULT, grader={f_: {k_: RES["footings"][f_][k_] for k_ in ("verdict", "failing", "sparc", "groups", "clusters")} for f_ in FEET}, rss_gb=rss())
json.dump(_OUT, open(os.environ["XH1_OUT"], "w"), indent=1, default=float)
sys.exit(0)
