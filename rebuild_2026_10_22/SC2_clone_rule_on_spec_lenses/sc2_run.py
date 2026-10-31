#!/usr/bin/env python3
"""SC2_clone_rule_on_spec_lenses (criteria a664f7af34): P2's, SI1's and SI2's own text, run by asserted string replacement, with per-lens clones in place of draw-then-veto. Nothing is written into those lanes.
    OMP_NUM_THREADS=1 nice -n 15 python3 sc2_run.py measure <kids_cache> <frozen_p2_work> <scratch_root> new|k20|mutate      (P2's phase A, fresh measurement of every centre)
    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 sc2_run.py grade <kids_cache> <frozen_p2_work> <scratch_root> old|new|k20|mutate
kappa = 1/2 FITTED; footings never pooled; cold dark energy is never a particle; the theory stays open."""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
import json, math, time, glob, resource
SC2_T0 = time.time(); SC2_LANE = os.path.dirname(os.path.abspath(__file__)); SC2_REB = os.path.dirname(SC2_LANE)
SC2_P2F = os.path.join(SC2_REB, "P2_spec_isolated_lensing", "p2_spec_isolated_lensing.py"); SC2_SI1F = os.path.join(SC2_REB, "SI1_spec_isolated_route_e", "si1_grade.py"); SC2_SI2F = os.path.join(SC2_REB, "SI2_spec_isolated_colour", "si2_grade.py")
SC2_STEP, SC2_CACHE, SC2_FROZEN, SC2_ROOT, SC2_MODE = sys.argv[1:6]
SC2_KEEP = {"new": (4, 2), "k20": (20, 20), "mutate": (4, 2)}.get(SC2_MODE)
SC2_WORK = SC2_FROZEN if SC2_MODE == "old" else os.path.join(SC2_ROOT, f"sc2_{SC2_MODE}")
def sc2_cpu(): r = resource.getrusage(resource.RUSAGE_SELF); return r.ru_utime + r.ru_stime
def sc2_rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1e9 if sys.platform == "darwin" else 1e6)


def sc2_patch_p2(T):
    """P2's text: the one change in this lane. I3 and I1 are replaced by per-lens clones after P2's own draws, so R and the frozen random stream are untouched."""
    if SC2_MODE == "old": return T
    a = "(Rra, Rde, Rz, Rlm, Rf, Rsrc), trR = make_iso(idxS1, 1.0, 3 * len(idxS1), veto=False, emin=1.0)\n"; assert T.count(a) == 1
    block = f'''SC2_OLD = dict(I3z=I3z.copy(), I3lm=I3lm.copy(), I1z=I1z.copy(), I1lm=I1lm.copy())
_rng_frozen = rng; rng = np.random.default_rng(20261031 + 4)
def _sc2_per_lens(src_idx, Riso, KEEP, CAP=100000):
    n = len(src_idx); RA_ = np.full((n, KEEP), np.nan); DE_ = RA_.copy(); FF_ = np.zeros((n, KEEP), int); have = np.zeros(n, np.int64); tries = np.zeros(n, np.int64); clone = src_idx
    if {SC2_MODE == "mutate"!r}:                                         # MUTATE: every lens's clones take the z and mass of lenses from the top half of the sample's z
        _o = np.argsort(z_g[src_idx]); _top = src_idx[_o[n // 2:]]; clone = _top[np.arange(n) % len(_top)]
    while True:
        act = np.where((have < KEEP) & (tries < CAP))[0]
        if len(act) == 0: break
        nb = max(2000, len(act)); who = act[np.arange(nb) % len(act)]; li = clone[who]; ra, de, f = draw_positions(nb); z = z_g[li]; lm = lM70[li]; tries += np.bincount(who, minlength=n)
        ok = edge_mpc(ra, de, f, z) >= Riso; vv = np.zeros(nb, bool); vv[ok] = veto_hits(ra[ok], de[ok], z[ok], lm[ok], Riso); ok &= ~vv
        for k_, r_, d_, f_ in zip(who[ok], ra[ok], de[ok], f[ok]):
            if have[k_] < KEEP: RA_[k_, have[k_]] = r_; DE_[k_, have[k_]] = d_; FF_[k_, have[k_]] = f_; have[k_] += 1
    fill = np.isfinite(RA_); cl_ = np.repeat(clone, have); lens_ = np.repeat(src_idx, have)
    return (RA_[fill], DE_[fill], z_g[cl_], lM70[cl_], FF_[fill], lens_), dict(short=int(np.sum(have < KEEP)), empty=int(np.sum(have == 0)), draws=int(tries.sum()), max_draws=int(tries.max()))
(I3ra, I3de, I3z, I3lm, I3f, I3src), SC2_INFO3 = _sc2_per_lens(idxS3, 3.0, {SC2_KEEP[0]})
(I1ra, I1de, I1z, I1lm, I1f, I1src), SC2_INFO1 = _sc2_per_lens(idxS1, 1.0, {SC2_KEEP[1]})
rng = _rng_frozen; tr3 = SC2_INFO3["draws"]; tr1 = SC2_INFO1["draws"]
P(f"  SC2 per-lens clones: S3 {{SC2_INFO3}}; S1 {{SC2_INFO1}}")
'''
    return T.replace(a, a + block)


if SC2_STEP == "measure":
    assert SC2_MODE != "old"; os.makedirs(SC2_WORK, exist_ok=True)
    for f_ in ("p2_field_v1.npz", "p2_efe_v1.pkl", "p2_town_v2.pkl", "p2_offset_v2.npz", "p2_gtab_v2.npz"):      # model tables do not depend on the random points
        d_ = os.path.join(SC2_WORK, f_)
        if not os.path.exists(d_): os.symlink(os.path.join(SC2_FROZEN, f_), d_)
    T_ = sc2_patch_p2(open(SC2_P2F).read()); sys.argv = [SC2_P2F, SC2_CACHE, SC2_WORK, "--phase=A"]
    try:
        exec(compile(T_, SC2_P2F, "exec"), {"__file__": SC2_P2F, "__name__": "p2_ro"})
    except SystemExit as e_:
        print(f"phase A exit {e_.code}; CPU {sc2_cpu():.0f} s; wall {time.time() - SC2_T0:.0f} s; peak RSS {sc2_rss():.2f} GB", flush=True); sys.exit(e_.code)
    sys.exit(0)

# ======================================================== grade: SI2's text, which runs SI1's head, which runs P2's phase B
def sc2_patch_si1(S):
    a = 'exec(compile(T, P2F, "exec"), N)'; assert S.count(a) == 1
    return S.replace(a, '_T_ = sc2_patch_p2(T); exec(compile(_T_, P2F, "exec"), N)')
sc2_txt = open(SC2_SI2F).read()
def sc2_rep(a, b):
    global sc2_txt
    assert sc2_txt.count(a) == 1, a[:80]; sc2_txt = sc2_txt.replace(a, b)
sc2_rep('exec(compile(src[:src.index(cut)], "si1_head", "exec"))', 'src = sc2_patch_si1(src); exec(compile(src[:src.index(cut)], "si1_head", "exec"))')
sc2_rep('tag = "_MUTATE" if MUT2 else ""; json.dump(RES2, open(os.path.join(HERE2, f"si2_results{tag}.json"), "w"), indent=1, default=float); open(os.path.join(HERE2, f"si2{tag}.out"), "w").write("\\n".join(OUT2) + "\\n")', '')   # SI2's own files stay untouched
sc2_rep('modl(foot, TNL2, "R2"), modl(key, TNH2, "R2")\n', 'modl(foot, TNL2, "R2"), modl(key, TNH2, "R2")\n    SC2_M[foot] = dict(R0=(mL0, mH0), R2=(mL2, mH2))\n')
if SC2_MODE != "old":                                                    # SI2's K2 is the statement that the old rule reproduces SI1; it cannot hold on a new I
    sc2_rep('        if not MUT2:\n            for nm in ("chi2_L", "chi2_H"): dk2 = max(dk2, abs(G["all_R0"]["all"][nm] - J1[foot][sm]["all"][nm]))\n', '')
    sc2_rep("K2 R0, no split reproduces SI1 (chi2 H, L, S3 and S1, both footings): {dk2:.1e}: {'PASS' if k2 else 'FAIL'}; K3 blue", "K2 is the old rule's check, not applicable on a new I; K3 blue")
if SC2_MODE == "mutate":
    sc2_rep('for foot in FOOTS:\n    N["tix"], N["MBN_g"] = TIX0, MBN0; key, TNH0 = build(foot)', 'for foot in ("canonical",):\n    N["tix"], N["MBN_g"] = TIX0, MBN0; key, TNH0 = build(foot)')
SC2_M = {}; os.environ.setdefault("PYTHONHASHSEED", "0"); __file__ = SC2_SI2F; sys.argv = [SC2_SI2F, SC2_CACHE, SC2_WORK]
exec(compile(sc2_txt, "si2_text", "exec"))

# ======================================================== everything below is this lane's
Q(f"\nSC2_clone_rule_on_spec_lenses  criteria a664f7af34  run: {SC2_MODE}" + ("" if SC2_KEEP is None else f"  (per-lens clones, {SC2_KEEP[0]} on S3, {SC2_KEEP[1]} on S1)") + ("  [MUTATE: clones from the top half of the sample's z]" if SC2_MODE == "mutate" else "") + "  kappa = 1/2 FITTED; footings never pooled")
SC2_OK = {}; SC2_R = dict(lane="SC2_clone_rule_on_spec_lenses", criteria="a664f7af34", run=SC2_MODE, keep=SC2_KEEP, si2=RES2, k={})
def sc2_k(name, ok, val): SC2_OK[name] = bool(ok); SC2_R["k"][name] = val; Q(f"{name}: {'PASS' if ok else 'FAIL'}  {val}")
sc2_I3, sc2_I1, sc2_Rs = SETS["I3"], SETS["I1"], SETS["R"]
def sc2_ratio(Lc, Ic):
    r = (MEAS["WW"][Lc].sum(0) / len(Lc)) / (MEAS["WW"][Ic].sum(0) / len(Ic)); o = {lab: float(np.mean(r[RANGE[lab]])) for lab in ("in", "O1", "O2")}; o["per_bin"] = r.tolist(); return o
sc2_wr = dict(S3_L_over_I=sc2_ratio(L3, sc2_I3), S1_L_over_I=sc2_ratio(L1, sc2_I1), S3_L_over_R=sc2_ratio(L3, sc2_Rs), S1_L_over_R=sc2_ratio(L1, sc2_Rs)); SC2_R["weight_ratios"] = sc2_wr
sc2_sk = dict(S3=dict(lens_z=float(np.mean(z_g[idxS3])), clone_z=float(np.mean(N["I3z"])), lens_lM=float(np.mean(lM70[idxS3])), clone_lM=float(np.mean(N["I3lm"]))), S1=dict(lens_z=float(np.mean(z_g[idxS1])), clone_z=float(np.mean(N["I1z"])), lens_lM=float(np.mean(lM70[idxS1])), clone_lM=float(np.mean(N["I1lm"])))); SC2_R["skew"] = sc2_sk
sc2_acc = dict(S3=len(sc2_I3) / N["tr3"], S1=len(sc2_I1) / N["tr1"]); SC2_R["acceptance"] = sc2_acc
Q("\nK_H3-style weight per centre, mean over the range's bins:")
for k_, v_ in sc2_wr.items(): Q(f"  {k_:12s} in {v_['in']:.3f}  O1 {v_['O1']:.3f}  O2 {v_['O2']:.3f}")
for s_ in ("S3", "S1"): Q(f"  {s_}: mean z lens {sc2_sk[s_]['lens_z']:.4f}, clones {sc2_sk[s_]['clone_z']:.4f}; mean lg M* lens {sc2_sk[s_]['lens_lM']:.4f}, clones {sc2_sk[s_]['clone_lM']:.4f}; draws per accepted point {1 / sc2_acc[s_]:.2f}")
# P2's verdict lines, through its own text
sc2_ver = {}
for foot_ in FOOTS:
    v_ = N["VER"][foot_]; sc2_ver[foot_] = dict(verdict=v_["verdict"], cls_a=list(v_["cls_a"]), cls_b=list(v_["cls_b"]), S=v_["S"], Smax=v_["Smax"], A_b_over_a=v_["A_b_over_a"], N_needed=v_["N_needed"], amps=N["AMP"][foot_], d=v_["profile"]["d"], sig=v_["profile"]["sig"], m_a=v_["profile"]["m_a"], m_b=v_["profile"]["m_b"])
    a_, b_ = N["AMP"][foot_]["a"], N["AMP"][foot_]["b"]; Q(f"  P2 [{foot_}] {v_['verdict']}; S {v_['Smax']:.2f}; (a) A_in {a_['A_in']:.3f}+-{a_['sA_in']:.3f} A_O1 {a_['A_O1']:.3f}+-{a_['sA_O1']:.3f} A_O2 {a_['A_O2']:.3f}+-{a_['sA_O2']:.3f}, classes {v_['cls_a']}; (b) A_O1 {b_['A_O1']:.3f}+-{b_['sA_O1']:.3f} A_O2 {b_['A_O2']:.3f}+-{b_['sA_O2']:.3f}, classes {v_['cls_b']}")
SC2_R["P2"] = dict(verdict=sc2_ver, lane=N["LANE"]); Q(f"  P2 lane line: {N['LANE']}")
# I's own noise in dchi2: two halves, covariance fixed
SC2_R["noise"] = {}
for foot_ in SC2_M:
    for rg_ in ("R0", "R2"):
        mL_, mH_ = SC2_M[foot_][rg_]
        for s_, Lc_, Ic_ in (("S3", L3, sc2_I3), ("S1", L1, sc2_I1)):
            sL = stack([(Lc_, +1, mL_), (Ic_, -1, mL_)]); sH = stack([(Lc_, +1, mH_), (Ic_, -1, mH_)]); Ci_ = HART(15) * np.linalg.inv(cov_of(sL))
            sc2_X = lambda d_, ml_, mh_: float((d_ - mh_) @ Ci_ @ (d_ - mh_) - (d_ - ml_) @ Ci_ @ (d_ - ml_))
            aL = stack([(Lc_, +1, mL_), (Ic_[::2], -1, mL_)]); aH = stack([(Lc_, +1, mH_), (Ic_[::2], -1, mH_)]); bL = stack([(Lc_, +1, mL_), (Ic_[1::2], -1, mL_)]); bH = stack([(Lc_, +1, mH_), (Ic_[1::2], -1, mH_)])
            xf, xa, xb = sc2_X(sL["d"], sL["m"], sH["m"]), sc2_X(aL["d"], aL["m"], aH["m"]), sc2_X(bL["d"], bL["m"], bH["m"]); dp = np.array([sc2_X(aL["dj"][p_], aL["mj"][p_], aH["mj"][p_]) - sc2_X(bL["dj"][p_], bL["mj"][p_], bH["mj"][p_]) for p_ in range(NP_)]); sg_ = 0.5 * math.sqrt((NP_ - 1) / NP_ * np.sum((dp - dp.mean()) ** 2))
            SC2_R["noise"][f"{foot_}|{rg_}|{s_}"] = dict(dchi2=xf, half_A=xa, half_B=xb, sig_I=sg_); Q(f"  noise [{foot_} {rg_} {s_}] dchi2 {xf:+.1f}; half A {xa:+.1f}, half B {xb:+.1f}; I's own noise {sg_:.1f}")
# nulls
SC2_R["nulls"] = {}
for s_, Lc_, Ic_ in (("S3", L3, sc2_I3), ("S1", L1, sc2_I1)):
    st_ = stack([(Lc_, +1, None), (Ic_, -1, None)], use="WX"); ok_ = st_["var"] > 0; c_ = float(np.sum(st_["d"][ok_] ** 2 / st_["var"][ok_])); h_ = stack([(Ic_[::2], +1, None), (Ic_[1::2], -1, None)]); oh_ = h_["var"] > 0; ch_ = float(np.sum(h_["d"][oh_] ** 2 / h_["var"][oh_]))
    SC2_R["nulls"][s_] = dict(cross_chi2=c_, cross_n=int(ok_.sum()), cross_p=float(stats.chi2.sf(c_, int(ok_.sum()))), halves_chi2=ch_, halves_n=int(oh_.sum()), halves_p=float(stats.chi2.sf(ch_, int(oh_.sum()))))
    Q(f"  nulls {s_}: cross {c_:.1f}/{int(ok_.sum())} p {SC2_R['nulls'][s_]['cross_p']:.3g}; halves of I {ch_:.1f}/{int(oh_.sum())} p {SC2_R['nulls'][s_]['halves_p']:.3g}")

if SC2_MODE == "old":
    # K1: the old rule reproduces the record
    sc2_j2 = json.load(open(os.path.join(SC2_REB, "SI2_spec_isolated_colour", "si2_results.json"))); sc2_j1 = json.load(open(os.path.join(SC2_REB, "SI1_spec_isolated_route_e", "si1_results.json"))); sc2_jp = json.load(open(os.path.join(SC2_REB, "P2_spec_isolated_lensing", "p2_spec_isolated_lensing_results.json"))); d2 = d1 = dp_ = 0.0; bad = []
    for foot_ in FOOTS:
        for s_ in ("S3", "S1"):
            for ln_, rec in sc2_j2["foot"][foot_][s_].items():
                new_ = RES2["foot"][foot_][s_][ln_]
                for kk in ("all", "inner", "outer"):
                    for nm in rec[kk]:
                        if isinstance(rec[kk][nm], (int, float)): d2 = max(d2, abs(new_[kk][nm] - rec[kk][nm]))
                if new_["cls"] != rec["cls"]: bad.append((foot_, s_, ln_))
            r0 = RES2["foot"][foot_][s_]["all_R0"]; rec = sc2_j1["foot"][foot_][s_]
            for kk in ("all", "inner", "outer"):
                for nm in ("chi2_L", "chi2_H", "dchi2", "D"): d1 = max(d1, abs(r0[kk][nm] - rec[kk][nm]))
            if r0["cls"] != rec["cls"]: bad.append(("SI1", foot_, s_))
        v_ = N["VER"][foot_]; rv = sc2_jp["verdict"][foot_]
        if v_["verdict"] != rv["verdict"] or list(v_["cls_a"]) != rv["cls_a"] or list(v_["cls_b"]) != rv["cls_b"]: bad.append(("P2", foot_))
        for nm in ("d", "sig", "m_a", "m_b"): dp_ = max(dp_, float(np.max(np.abs(np.array(v_["profile"][nm]) - np.array(rv["profile"][nm])))))
        for cc in ("a", "b", "b_lo"):
            for nm, x_ in N["AMP"][foot_][cc].items(): dp_ = max(dp_, abs(x_ - sc2_jp["amplitudes_S3"][foot_][cc][nm]))
    db = max(float(np.max(np.abs(np.array(sc2_wr["S3_L_over_I"]["per_bin"]) - np.array(sc2_jp["diagnostics"]["boost_vs_I3"])))), float(np.max(np.abs(np.array(sc2_wr["S3_L_over_R"]["per_bin"]) - np.array(sc2_jp["diagnostics"]["boost_vs_R"])))))
    same_c = RES2["combined"] == sc2_j2["combined"] and N["LANE"] == sc2_jp["lane_verdict"]
    sc2_k("K1_record_reproduced", d2 <= 1e-9 and d1 <= 1e-9 and dp_ <= 1e-9 and db <= 1e-9 and not bad and same_c, f"SI2 lines max |d| {d2:.1e}; SI1 lines {d1:.1e}; P2 verdict profile and amplitudes {dp_:.1e}; P2 weight lines {db:.1e}; class or verdict mismatches {bad}; combined reading and P2 lane line equal: {same_c}")
else:
    # K2: the clone rule
    sc2_ct = []
    for s_, idx_, src_, z_, lm_, ra_, de_, f_, Riso_, keep_ in (("S3", idxS3, N["I3src"], N["I3z"], N["I3lm"], N["I3ra"], N["I3de"], N["I3f"], 3.0, SC2_KEEP[0]), ("S1", idxS1, N["I1src"], N["I1z"], N["I1lm"], N["I1ra"], N["I1de"], N["I1f"], 1.0, SC2_KEEP[1])):
        uq, cn = np.unique(src_, return_counts=True); cnt_ok = np.array_equal(uq, np.sort(idx_)) and bool(np.all(cn == keep_)); id_ok = bool(np.all(z_ == z_g[src_]) and np.all(lm_ == lM70[src_])); edge_ok = bool(np.all(N["edge_mpc"](ra_, de_, f_, z_) >= Riso_)); pick = np.linspace(0, len(ra_) - 1, 200).astype(int); brute = sum(N["brute_veto"](ra_[i_], de_[i_], z_[i_], lm_[i_], Riso_) for i_ in pick)
        sc2_ct.append((s_, cnt_ok, id_ok, edge_ok, int(brute)))
    sc2_k("K2_clone_rule", all(c[1] and c[2] and c[3] and c[4] == 0 for c in sc2_ct), f"(sample, counts exact, clone z and lg M* equal the lens's, edge margin, brute-force violations of 200): {sc2_ct}; S3 {N['SC2_INFO3']}; S1 {N['SC2_INFO1']}")
    # K3: only I changed
    sc2_old = sorted(glob.glob(os.path.join(SC2_FROZEN, "p2_meas_*.npz"))); assert len(sc2_old) == 1; sc2_om = np.load(sc2_old[0]); NL_ = len(idxS1); sc2_nold = sc2_om["WW"].shape[0]; sc2_nR = len(sc2_Rs); dm_ = 0.0
    for k_ in ("WG", "WX", "WW", "NN"):
        o_ = sc2_om[k_]; mx_ = float(np.max(np.abs(o_))); dm_ = max(dm_, float(np.max(np.abs(MEAS[k_][SETS["L"]] - o_[:NL_]))) / mx_, float(np.max(np.abs(MEAS[k_][sc2_Rs] - o_[sc2_nold - sc2_nR:]))) / mx_)
    del sc2_om; sc2_J0 = json.load(open(os.path.join(SC2_LANE, "sc2_results_old.json")))["si2"]["foot"]; dr_ = 0.0
    for foot_ in RES2["foot"]:
        for s_ in ("S3", "S1"):
            for nm in ("chi2_L", "chi2_H"): dr_ = max(dr_, abs(RES2["foot"][foot_][s_]["all_R2_raw"]["all"][nm] - sc2_J0[foot_][s_]["all_R2_raw"]["all"][nm]))
    sc2_k("K3_only_I_changed", dm_ <= 1e-9 and dr_ <= 1e-9, f"lens and R per-centre sums, max relative |d| {dm_:.1e}; raw L - R lines, max |d chi2| {dr_:.1e}")
    # K4: nulls; K5: weight ratio
    sc2_k("K4_nulls_on_new_I", all(SC2_R["nulls"][s_]["cross_p"] >= 0.001 and SC2_R["nulls"][s_]["halves_p"] >= 0.001 for s_ in ("S3", "S1")), {s_: [round(SC2_R["nulls"][s_]["cross_p"], 4), round(SC2_R["nulls"][s_]["halves_p"], 4)] for s_ in ("S3", "S1")})
    sc2_k("K5_weight_ratio", all(abs(sc2_wr[k_]["O2"] - 1) <= 0.10 for k_ in ("S3_L_over_I", "S1_L_over_I")), f"lens/I in O2: S3 {sc2_wr['S3_L_over_I']['O2']:.3f}, S1 {sc2_wr['S1_L_over_I']['O2']:.3f}")
SC2_R["reading"] = "NO READING" if not all(SC2_OK.values()) else RES2["combined"]; Q(f"\n{'OLD-RULE' if SC2_MODE == 'old' else SC2_MODE.upper()} READING: {SC2_R['reading']}")
if SC2_MODE == "mutate":
    sc2_J1 = json.load(open(os.path.join(SC2_LANE, "sc2_results_new.json")))["si2"]["foot"]["canonical"]; bite = {}
    for s_ in ("S3", "S1"):
        for ln_ in ("all_R0", "all_R2"): bite[f"{s_}|{ln_}"] = abs(RES2["foot"]["canonical"][s_][ln_]["all"]["chi2_H"] - sc2_J1[s_][ln_]["all"]["chi2_H"]) > 1e-3
    okb = (not SC2_OK["K2_clone_rule"]) and (not SC2_OK["K5_weight_ratio"]) and all(bite.values()) and SC2_R["reading"] == "NO READING"; SC2_R["mutate_bites"] = dict(ok=okb, chi2H_changed=bite); Q(f"MUTATE bites: {'PASS' if okb else 'FAIL'}  K2 failed {not SC2_OK['K2_clone_rule']}; K5 failed {not SC2_OK['K5_weight_ratio']}; chi2 H changed {bite}; reading {SC2_R['reading']}")
Q(f"checks {sum(SC2_OK.values())}/{len(SC2_OK)}; CPU {sc2_cpu():.0f} s; wall {time.time() - SC2_T0:.0f} s; peak RSS {sc2_rss():.2f} GB"); SC2_R["cpu_s"] = sc2_cpu(); SC2_R["checks"] = SC2_OK
SC2_TAG = {"old": "old", "new": "new", "k20": "k20", "mutate": "MUTATE"}[SC2_MODE]
json.dump(SC2_R, open(os.path.join(SC2_LANE, f"sc2_results_{SC2_TAG}.json"), "w"), indent=1, default=float); open(os.path.join(SC2_LANE, f"sc2_{SC2_TAG}.out"), "w").write("\n".join(OUT2) + "\n")
sys.exit(0 if all(SC2_OK.values()) else 1)
