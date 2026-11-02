# DR8 tail, after UR1's helpers. Reads only. The rule is posited, not derived. kappa = 1/2 FITTED, unused; not theory closed.
import time as _tm
_T0 = _tm.time(); _PT = os.environ["DR8_PART"]; _HERE8 = os.environ["DR8_HERE"]; KPC_S = NE["KPC_S"]
sys.path.insert(0, _HERE8); sys.dont_write_bytecode = True; import dr8_rule as _R8
_ORIG = contract; _M8 = dict(v="blum", mut=1.0); _ST = dict(calls=0, cross=0, crosscalls=0, r0bad=0, conv=0.0, r0err=0.0)
def _r8(r, Mb, M0, F, v):
    r0, C, n = _R8.infer_r0(r, M0, B); e = float(np.max(np.abs(M0[:n + 1] / (C * B(r[:n + 1] / r0)) - 1)[M0[:n + 1] > 1e-3 * M0[n]])); _ST["r0err"] = max(_ST["r0err"], e); _ST["r0bad"] += int(e > 1e-5)
    o = _R8.rule(r, Mb * _M8["mut"], M0, F, v, r0=r0, C=C, B=B); _ST["calls"] += 1; _ST["cross"] = max(_ST["cross"], o[2]); _ST["crosscalls"] += int(o[2] > 0); _ST["conv"] = max(_ST["conv"], o[1]); return o
def contract(r, Mb, M0, F, gnedin=None):
    if _M8["v"] == "blum" or gnedin is not None: return _ORIG(r, Mb, M0, F, gnedin=gnedin)
    o = _r8(r, Mb, M0, F, _M8["v"]); return o[0], o[1], o[2]
# the 1e12 setup for part B, the grader's own numbers; written first so B can start
def _setup():
    O = {}
    for t in _TG:
        bg = BGS[t]; rc = 3 * (100 * bg["h"] * 1e3 / MPCE) ** 2 / (8 * math.pi * GE); fc = float(json.load(open(os.path.join(REB, "LC1_live_contraction", "lc1_setup.json")))["fc"]); M2 = fc * 1e12; R2 = (3 * M2 * MSUNE / (4 * math.pi * 200 * rc)) ** (1 / 3); s, a_ = sig_core("canonical", t, M2 / FC1_MC); r0 = solve_r0(M2 * MSUNE, R2, s); Bb = float(B(np.asarray(1.0)))
        O[t] = dict(M2=M2, R2_kpc=R2 / KPC_S, r0_kpc=r0 / KPC_S, a=R2 / r0, Sigma_Msun_pc2=s / MSUNE * (KPC_S / 1e3) ** 2, M_r0_over_M2=Bb / float(B(np.asarray(R2 / r0))), arg_mass=M2 / FC1_MC, B_at_1=Bb, h=bg["h"])
    return O
if _PT == "PRIMARY": json.dump(_setup(), open(os.path.join(_HERE8, "dr8_setup_1e12.json"), "w"), indent=1, default=float); print("DR8 setup written", flush=True)
# K2 to K4, a test profile through the wrapper's code
_rr = np.geomspace(1e-4, 2.0, 6000)
_BS = _R8.BS; _M0t = 1e12 * _BS(_rr / 0.02) / _BS(2.0 / 0.02); _Mbt = 6e10 * (1 - 3e-3 / np.sqrt(_rr ** 2 + 9e-6)); _Ft = 0.06
_c = _ORIG(_rr, _Mbt, _M0t, _Ft)[0]
def _k2():
    r0, C, _ = _R8.infer_r0(_rr, _M0t, _BS); C0 = C * 0.0; o = _R8.rule(_rr, _Mbt, _M0t, _Ft, "RULE_F", r0=1e30, C=C, B=_BS)  # P -> 0 as r0 -> infinity: Mr0 r / r0
    i = (_rr > 1e-3) & (_rr < 1.5); return float(np.max(np.abs(o[0][i] / _c[i] - 1))), float(np.max(np.abs(_R8.rule(_rr, 0 * _Mbt, _M0t, 0.0, "RULE", r0=r0, C=C, B=_BS)[0][i] / _M0t[i] - 1))), abs(r0 / 0.02 - 1)
_KK = dict(zip(("K2a_ruleF_P0_vs_contract", "K2b_rule_Mb0_identity", "K3_r0_inferred"), _k2())); _ot = _R8.rule(_rr, _Mbt, _M0t, _Ft, "RULE", B=_BS); _KK["K4_monotonic_Mf"] = float(np.min(np.diff(_ot[0]))); _KK["K4_crossings_test"] = _ot[2]; _KK["K4_edge_rf_over_ri"] = float(_ot[3][-1] / _rr[-1]); print("DR8 checks", _KK, flush=True)
def _eff(tag="A_c2b_refit", f="canonical"):
    bg = BGS[tag]; rc = 3 * (100 * bg["h"] * 1e3 / MPCE) ** 2 / (8 * math.pi * GE); iu = int(np.argmin(abs(UPS - 0.5))); U = float(UPS[iu]); O = {f"{l}-{h}": [] for l, h in _BIN}; SLMAP["m"] = "EM1"
    for q in GALS:
        t = _TB.get(q["name"])
        if not t or t["vf"] <= 0 or t["Q"] > 2 or t["inc"] < 30 or q["meta"]["Rdisk"] <= 0: continue
        M2, R2 = _SL3M(q["lMb"], bg, rc); s, _ = sig_core(f, tag, M2 / FC1_MC); r0 = solve_r0(M2 * MSUNE, R2, s); Rm = q["Rm"]; Rd = q["meta"]["Rdisk"] * KPC_S; rg = np.geomspace(min(Rm[0], Rd) * 0.05, R2, 800); M0 = math.pi * s * r0 ** 2 * B(rg / r0); Mbk = np.maximum.accumulate(np.maximum(q["GB"][:, iu] * Rm ** 2 / GE, 0.0)); Mt = max(float(Mbk[-1]), (U * q["meta"]["L36"] + 1.33 * q["meta"]["MHI"]) * 1e9 * MSUNE); Mbg = np.where(rg < Rm[0], Mbk[0] * (rg / Rm[0]) ** 2, np.interp(np.log(rg), np.log(Rm), Mbk)); o_ = rg > Rm[-1]
        if o_.any(): t_ = np.clip(np.log(rg[o_] / Rm[-1]) / math.log(3.0), 0, 1); Mbg[o_] = np.exp(np.log(max(Mbk[-1], 1e-300)) * (1 - t_) + np.log(Mt) * t_)
        Mbg = np.maximum.accumulate(Mbg); F = Mt / (M2 * MSUNE); Mfb = _ORIG(rg, Mbg, M0, F)[0]; a = _R8.rule(rg, Mbg, M0, F, "RULE", B=B); b = _R8.rule(rg, Mbg, M0, F, "RULE_F", B=B); c = _R8.rule(rg, Mbg, M0, F, "BLUM0", B=B); lg = np.log(rg); pts = np.array([2.2 * Rd, r0]); Q0 = np.interp(np.log(pts), lg, M0); Qb, Qa, Qf, Q0F = (np.interp(np.log(pts), lg, y) / Q0 for y in (Mfb, a[0], b[0], c[0])); rel = lambda x, y: ((x - 1) / np.where(np.abs(y - 1) > 1e-6, y - 1, np.nan))
        # the shell landing at 2.2 R_d: r_i/r0 under Blumenthal and RULE, from mass conservation
        Mh = np.interp(math.log(2.2 * Rd), lg, Mfb); ri_b = np.exp(np.interp(math.log(max(Mh, M0[0])), np.log(np.maximum(M0, 1e-300)), lg)); Mh2 = np.interp(math.log(2.2 * Rd), lg, a[0]); ri_r = np.exp(np.interp(math.log(max(Mh2, M0[0])), np.log(np.maximum(M0, 1e-300)), lg))
        for l, h in _BIN:
            if l <= t["vf"] < h: O[f"{l}-{h}"].append(dict(Rd_kpc=q["meta"]["Rdisk"], r0_kpc=r0 / KPC_S, r0_Rd=r0 / Rd, rs22_r0=2.2 * Rd / r0, ri_b_r0=ri_b / r0, ri_r_r0=ri_r / r0, Fg=F, Qb=Qb.tolist(), Qr=Qa.tolist(), Qrf=Qf.tolist(), Qb0=Q0F.tolist(), cutR=rel(Qb, Qa).tolist(), cutRF=rel(Qb, Qf).tolist(), cross=a[2]))
    return {k: {x: np.nanmedian([a_[x] for a_ in v], axis=0).tolist() for x in v[0]} | dict(n=len(v), cut22_p16_p84=np.nanpercentile([a_["cutR"][0] for a_ in v], [16, 84]).tolist()) for k, v in O.items() if v}
_RES = dict(checks=_KK, runs={})
def _go(lab, v, mode="blum", mut=1.0):
    _M8.update(v=v, mut=mut); _RES["runs"][lab] = _run("EM1", mode); _M8.update(v="blum", mut=1.0); _RES["stats_" + lab] = dict(_ST); json.dump(_RES, open(os.environ["SL1_OUT"] + ".part", "w"), indent=1, default=float); print(f"DR8 {lab} done {_tm.time() - _T0:.0f} s", flush=True)
if _PT == "PRIMARY":
    _go("EM1|off", "blum", "off"); _go("EM1|blum", "blum"); _go("EM1|RULE", "RULE"); _go("EM1|RULE_F", "RULE_F"); _go("EM1|BLUM0", "BLUM0"); _go("MUTATE", "RULE", mut=2.0); _RES["eff"] = _eff(); _RES["eff_B"] = _eff("B_cfg886_bg")
elif _PT == "FQ":
    # measured at one mass: M_f = M0 + f(r/r0)(M_f,blum - M0). Labelled MEASURED AT ONE MASS, not a rule.
    _TQ = json.load(open(os.path.join(_HERE8, "dr8_fr_table.json"))); _xq = np.log(np.array(_TQ["r_over_r0"])); _fq = np.array(_TQ["f"]); _O2 = _ORIG
    def contract(r, Mb, M0, F, gnedin=None):
        o = _O2(r, Mb, M0, F, gnedin=gnedin); r0, C, n = _R8.infer_r0(r, M0, B); f = np.interp(np.log(r / r0), _xq, _fq); return (np.maximum.accumulate(M0 + f * (o[0] - M0)),) + tuple(o[1:])
    _RES["runs"]["EM1|Qmeasured"] = _run("EM1", "blum"); print("DR8 FQ done", flush=True)
else:
    _go("EM1|" + _PT, _PT)
json.dump(_RES, open(os.environ["SL1_OUT"], "w"), indent=1, default=float); os.remove(os.environ["SL1_OUT"] + ".part") if os.path.exists(os.environ["SL1_OUT"] + ".part") else None; print("DR8 done", flush=True); sys.exit(0)
