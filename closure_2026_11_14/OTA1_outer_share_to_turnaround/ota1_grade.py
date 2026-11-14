#!/usr/bin/env python3
"""OTA1 driver (FROZEN_CRITERIA.md): ZN4's grader text (ZN1's zn1_grade.py with M3A1's patches, gas +0.005) with a wrapper on
zn1_fn that counts the cold share X x M_b(< r_ta) once, the share beyond the fair-share R200c in the record's own layout, rescaled.
Other lanes' files are read only; outputs only in this folder. Serial, one thread, nice 19; SIGTERM exits 75.
    python3 ota1_grade.py [job ...]      jobs: BASE_0.034 BASE_0.0615 RULE_0.034 RULE_0.0615 TW0_0.034 TW2_0.034 BRK2.676_0.034 BRK3.071_0.034
kappa = 1/2 and X = 5.41 FITTED; cold dark energy, never a particle; not theory closed."""
import json, os, signal, sys
HERE7 = os.path.dirname(os.path.abspath(__file__)); RB7 = os.path.join(os.path.dirname(os.path.dirname(HERE7)), "rebuild_2026_10_22")
ZN1D = os.path.join(RB7, "ZN1_zooms_to_z0"); ZN4D = os.path.join(RB7, "ZN4_cluster_resolution"); T3 = open(os.path.join(ZN1D, "zn1_grade.py")).read()
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[v] = "1"
def _s(a, b, n=1):
    global T3
    assert T3.count(a) == n, a
    T3 = T3.replace(a, b)
# location: this lane sits outside rebuild_2026_10_22, so RB is pinned there
_s('HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE)', f'HERE = os.path.dirname(os.path.abspath(__file__)); RB = {RB7!r}')
# M3A1's patches, verbatim
_s("""_d = open({os.path.join(MA1, 'ma1_def.py')!r}).read() + open({os.path.join(HERE, 'zn1_def.py')!r}).read()""", """_d = open({os.path.join(MA1, 'ma1_def.py')!r}).read() + open({os.path.join(RB, 'ZN1_zooms_to_z0', 'zn1_def.py')!r}).read() + open({os.path.join(RB, 'ZN3_native_shape_at_1e15', 'zn3_def.py')!r}).read()""")
_s('open(os.path.join(HERE, "zn1_boot_tail.py")).read()', 'open(os.path.join(RB, "ZN1_zooms_to_z0", "zn1_boot_tail.py")).read()')
_s('open(xf, "w").write(GAS if gas else "")', 'open(xf, "w").write(gas)')
_s('{int(gas)}', '{abs(hash(gas)) % 10 ** 8}')
_s('["nice", "-n", "5", sys.executable', '["nice", "-n", "19", sys.executable')
# OTA1: carry the wrapper's per-cluster log out through the record's own output dict
_s('_OUT["M_outer"] = {f"{f_}|{h_}"', '_OUT["ota1"] = globals().get("OTA_STAT", [])\\n_OUT["M_outer"] = {f"{f_}|{h_}"')
K = T3.index('if __name__ == "__main__":\n    if "--k3" in sys.argv:')
exec(compile(T3[:K], os.path.abspath(__file__), "exec"))
SH = os.path.join(ZN4D, "zn4_shapes.json"); G5 = GAS.replace("0.111", "0.005"); assert G5 != GAS

OTA_CODE = r'''
OTA_STAT = []; OTA_CUR = {"i": -1, "hk": ""}
_OTA_ORIG = zn1_fn
def zn1_fn(foot, tag, pp, z):
    f = _OTA_ORIG(foot, tag, pp, z)
    if ZN1_MODE != "fs" or OTA_CFG["mode"] == "off": return f
    xc = "R500" not in pp; rec = dict(i=(-1 if xc else OTA_CUR["i"]), hk=("xcop" if xc else OTA_CUR["hk"]), foot=foot, z=float(z))
    Mfs, R2, thr = zn1_m200_fs(pp["Mb"], z); rta = float(pp["rta"]); Mf = float(pp["Mfair"]); Mbt = float(pp["Mb"][-1])
    if Mfs is None or R2 >= rta:
        rec.update(case="unchanged_nofs" if Mfs is None else "unchanged_rta_le_R2"); OTA_STAT.append(rec); return f
    if OTA_CFG["slope"] is not None and not xc:
        R5 = float(pp["R500"]) * NX["MPC"]; y = rta / R5
        if y > 1:
            I_ = lambda s_: math.log(y) if abs(3 - s_) < 1e-12 else (y ** (3 - s_) - 1) / (3 - s_)
            M5 = float(np.interp(R5, RM, pp["Mb"])); Mb2 = M5 + (Mbt - M5) * I_(OTA_CFG["slope"]) / I_(SLOPE); rec["brk_ratio"] = Mb2 / Mbt; Mf = Mf * Mb2 / Mbt
    MR2 = float(f(np.array([R2]))[0]); MT = float(f(np.array([rta]))[0])
    T = MT if OTA_CFG["mode"] == "zero" else MR2 + OTA_CFG["S"] * (Mf - MR2); inc = MT - MR2
    if inc > 1e-9 * Mf:
        lam = (T - MR2) / inc; case = "scaled"
        def g(r):
            r = np.asarray(r, float); fr = f(r); return np.where(r <= R2, fr, MR2 + lam * (fr - MR2))
    else:
        lam = float("nan"); case = "uniform"
        def g(r):
            r = np.asarray(r, float); fr = f(r); rr = np.minimum(r, rta); return np.where(r <= R2, fr, MR2 + (T - MR2) * (rr ** 3 - R2 ** 3) / (rta ** 3 - R2 ** 3))
    gr = g(RM); fr_ = f(RM); ins = RM <= R2
    rec.update(case=case, lam=float(lam), R2_mpc=R2 / NX["MPC"], rta_mpc=rta / NX["MPC"], Mfair=Mf, Mc_R2=MR2, Mc_rta_rec=MT, rec_over_Mfair=MT / Mf, R2_over_Mfair=MR2 / Mf,
               k1_tot=float(g(np.array([rta]))[0] / T - 1), k1_tot_mf=(float(g(np.array([rta]))[0] / Mf - 1) if OTA_CFG["mode"] != "zero" else None),
               k1_in=float(np.max(np.abs(gr[ins] / np.where(fr_[ins] > 0, fr_[ins], 1.0) - np.where(fr_[ins] > 0, 1.0, 0.0)))) if ins.any() else 0.0)
    OTA_STAT.append(rec); return g
'''
def xfile(cfg):
    code = f"OTA_CFG = {cfg!r}\n" + OTA_CODE
    x = "sub('def grade_clusters(foot, rule=True, tag=\"A_c2b_refit\"):', " + repr(code) + " + 'def grade_clusters(foot, rule=True, tag=\"A_c2b_refit\"):')\n"
    x += "sub('pp = prep(int(i), foot, hk); Mtot = (pp[\"Mfair\"]', 'OTA_CUR[\"i\"] = int(i); OTA_CUR[\"hk\"] = hk; pp = prep(int(i), foot, hk); Mtot = (pp[\"Mfair\"]')\n"
    return G5 + x
CFG = {"BASE": dict(mode="off", S=1.0, slope=None), "RULE": dict(mode="rule", S=1.0, slope=None), "TW0": dict(mode="zero", S=1.0, slope=None),
       "TW2": dict(mode="rule", S=2.0, slope=None), "BRK2.676": dict(mode="rule", S=1.0, slope=2.676), "BRK3.071": dict(mode="rule", S=1.0, slope=3.071)}
FEET2 = ("canonical", "alt")
def cellsf(R, foot):
    c = R["grader"][foot]["clusters"]["cells"]; O = {}
    for h in HH:
        m = R["M_outer"][f"{foot}|{h}"]; O[h] = {k: dict(v) for k, v in c[h].items()}
        for k, A in [("G-OUT-Mall", m["all"])] + [(f"G-OUT-M{t + 1}", m["terc"][t]) for t in range(3)]:
            v = O[h][k]; s = v["s"] * A / v["meas"]; v.update(meas=A, s=s, Z=(A - v["pred"]) / s)
    return O
CJ = os.path.join(HERE7, "cache_jobs"); os.makedirs(CJ, exist_ok=True)
signal.signal(signal.SIGTERM, lambda *a: (_ for _ in ()).throw(KeyboardInterrupt()))
def job(name, fs):
    f = os.path.join(CJ, f"{name}_{fs}.json")
    if os.path.exists(f): return json.load(open(f))
    try: R = run(fs, "fs", xfile(CFG[name]), SH)
    except KeyboardInterrupt: sys.exit(75)
    O = dict(cfg=CFG[name], fs=fs, cells={ft: cellsf(R, ft) for ft in FEET2}, xcop={ft: {k: R["footings"][ft][k] for k in ("mean", "rms")} for ft in FEET2},
             groups={ft: R["grader"][ft]["groups"] for ft in FEET2}, sparc={ft: R["grader"][ft]["sparc"] for ft in FEET2}, zn1=R["zn1"], ota1=R.get("ota1", []))
    json.dump(O, open(f + ".tmp", "w"), default=float); os.replace(f + ".tmp", f); return O
if __name__ == "__main__":
    ALL = ["BASE_0.034", "BASE_0.0615", "TW0_0.034", "RULE_0.034", "RULE_0.0615", "TW2_0.034", "BRK2.676_0.034", "BRK3.071_0.034"]; want = sys.argv[1:] or ALL
    for j in ALL:
        if j not in want: continue
        n, fs = j.split("_"); O = job(n, fs)
        for ft in FEET2:
            c = O["cells"][ft]; print(j, ft, " ".join(f"{h} M3 {c[h]['G-OUT-M3']['Z']:+.3f} M2 {c[h]['G-OUT-M2']['Z']:+.3f} Mall {c[h]['G-OUT-Mall']['Z']:+.3f} T3 {c[h]['G-MID-T3']['Z']:+.3f}" for h in HH), f"X-COP {O['xcop'][ft]['mean']:+.3f} {O['xcop'][ft]['rms']:.3f}", flush=True)
