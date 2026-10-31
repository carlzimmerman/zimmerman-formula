# BA2 (criteria e30f1b461b): exec'd in a lane's own namespace after its full grade. Returns what that run already holds. The only new calculation is BA1's R, by BA1's text.
def ba2_collect(g):
    NX_ = g["NX"]; M_ = NX_["M"]; X7_ = NX_["X7J"]; FE_ = NX_["FEET"]; HH_ = NX_["HK"]; RF_ = g["RES"]["footings"]; mo = {}
    for f_ in FE_:
        for h_ in HH_:
            cl = f"{f_}|{h_}"; o_ = M_[cl]; r7_ = X7_["bins"][f"terciles|{cl}"]; a7_ = X7_["all"][f"C*|boost|{cl}"]["OUTER"]
            mo[cl] = dict(all=o_["M_all|OUTER"]["A"], terc=[x_["A"] for x_ in o_["M_terc|OUTER"]], s_all=o_["M_all|OUTER"]["s"], s_terc=[x_["s"] for x_ in o_["M_terc|OUTER"]],
                          x7_all=a7_["A_CAL"], x7_terc=[r_["OUTER"]["A_CAL"] for r_ in r7_], x7_stat_all=a7_["s_STAT"], x7_stat_terc=[r_["OUTER"]["s_STAT"] for r_ in r7_])
    ft = {f_: dict(cells=RF_[f_]["clusters"]["cells"], fails=RF_[f_]["clusters"]["fails"], failing=RF_[f_]["failing"], verdict=RF_[f_]["verdict"],
                   sparc={t_: {k_: v_[k_] for k_ in ("rms", "U_median", "line")} for t_, v_ in RF_[f_]["sparc"].items()},
                   groups={k_: RF_[f_]["groups"][k_] for k_ in ("Z", "mean", "verdict", "PASS")}) for f_ in FE_}
    T_ = open(g["os"].path.join(g["REB"], "BA1_joint_shear_statistic", "ba1_worker_tail.py")).read(); e_ = 'json.dump(_OUT, open(os.environ["BA1_OUT"], "w"), indent=1, default=float); sys.exit(0)'
    assert T_.count(e_) == 1
    g2 = dict(g); exec(compile(T_.replace(e_, ""), "ba1_worker_tail", "exec"), g2)
    return dict(M_outer=mo, footings=ft, R_own=g2["_OUT"], rss_gb=g["resource"].getrusage(g["resource"].RUSAGE_SELF).ru_maxrss / 1e9)
