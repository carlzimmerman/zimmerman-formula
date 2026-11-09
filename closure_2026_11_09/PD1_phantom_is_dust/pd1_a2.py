#!/usr/bin/env python3
"""PD1 AMENDMENT A2 (ee9325c612): P1 with the basin share (5.41 x f_basin x M_b,gal, f_basin 2.0; 1.8 / 2.2 reported) and the 0.85 Mpc
neighbour cap; P5 Bullet galaxy-traced and Newtonian (DB1 child with a0 -> 1e-30; KA-A2 the law-only row); the label assembled from
pd1_a1_share10.82 (KiDS, SPARC: galaxy basin share) and pd1_a1_share5.41 (groups, X-COP: cluster share, prefactor 1/2).
    python3 pd1_a2.py   -> pd1_a2.json / pd1_a2.out
kappa = 1/2 FITTED; not theory closed; adopts nothing."""
import os, sys, json, math, io, subprocess, resource
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
A2 = "ee9325c612"
if len(sys.argv) > 1 and sys.argv[1] == "nchild":                       # DB1 child, Newtonian (a0 -> 1e-30) unless 'law'
    Rs_all = json.loads(sys.argv[2]); mode = sys.argv[3]; DB1 = os.path.join(REPO, "rebuild_2026_10_22", "DB1_cluster_dark_baryons")
    src = open(os.path.join(DB1, "db1_fast.py")).read(); pre = src[:src.index("# ---------- X-COP, own replica")]
    a_ = 'OUT = open(f"db1_{MODE}{TG2}{TAG}.out", "w")'; assert pre.count(a_) == 1; pre = pre.replace(a_, "OUT = io.StringIO()")
    sys.path.insert(0, DB1); os.chdir(DB1); sys.argv = [os.path.join(DB1, "db1_fast.py"), "pd1"]
    BNS = {"__file__": os.path.join(DB1, "db1_fast.py"), "__name__": "db1_fast_pd1"}; so = sys.stdout; sys.stdout = io.StringIO(); out = {}
    try:
        exec(compile(pre, "db1_fast_prefix", "exec"), BNS)
        MST, MGJ = BNS["MST"], BNS["MGJ"]; row = BNS["bullet_row"]; out["masses"] = dict(M_star_sub=[float(x) for x in MST], M_gas_sub=[float(x) for x in MGJ])
        out["KA_law_row"] = row("Z", "canonical", 0.0, Rs=[0.0, 0.0])
        if mode == "newton":
            for k in list(BNS["A0"]): BNS["A0"][k] = 1e-30
            out["KA_newton_baryons_only"] = row("Z", "canonical", 0.0, Rs=[0.0, 0.0])
        for f, Mret in Rs_all.items(): out[f] = dict(row=row("Z", f, 0.0, Rs=[Mret[j] / MST[j] for j in range(len(MST))], on="gal"))
    finally: sys.stdout = so
    out["child_peak_rss_MB"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6
    print("PD1CHILD " + json.dumps(out, default=float)); sys.exit(0)
src = open(os.path.join(HERE, "pd1_a1.py")).read(); ns = {"__file__": os.path.join(HERE, "pd1_a1.py"), "__name__": "pd1_a1_lib"}
exec(compile(src[:src.index("RES = dict(amendment=A1")], "pd1_a1_prefix", "exec"), ns)
np, G, MS, KPC, MPC, Mph = ns["np"], ns["G"], ns["MS"], ns["KPC"], ns["MPC"], ns["Mph"]
A0, FOOTS, footing_bg, share_table, system, rem_in = ns["A0"], ns["FOOTS"], ns["footing_bg"], ns["share_table"], ns["system"], ns["rem_in"]
gsmf, LG, LF = ns["ns"]["gsmf"], ns["ns"]["LG"], ns["ns"]["LF"]; L = []
def P(s): print(s, flush=True); L.append(str(s))
RES = dict(amendment=A2, criteria="0dc7929421", note="TEST lane; adopts nothing; kappa = 1/2 FITTED; not theory closed")
# ---------------- P1 with the basin share and the neighbour cap
for f in FOOTS:
    B = footing_bg(f); a0 = A0[f]; per = gsmf(B.h); RHO_D_SUN = B.RHO_D0 * MPC ** 3 / MS; RES[f] = {"P1": {}}
    for fb in (2.0, 1.8, 2.2):
        rows = {}
        for z in (0.5, 1.0, 2.0):
            aE = 1 / (1 + z); rms = np.array([B.r_ta(10 ** m * MS * (1 + B.R), 0.0, aE)[0] for m in LG]); Rm = 10 ** np.interp(LF, LG, np.log10(rms))
            mph = np.array([min(Mph(R, 10 ** m * MS, a0), B.R * fb * 10 ** m * MS, Mph(0.85 * MPC, 10 ** m * MS, a0)) / MS for R, m in zip(Rm, LF)])
            unc = np.array([Mph(R, 10 ** m * MS, a0) / MS for R, m in zip(Rm, LF)])
            q = float(np.trapz(np.array([per(m) for m in LF]) * mph, LF)) / RHO_D_SUN; qu = float(np.trapz(np.array([per(m) for m in LF]) * unc, LF)) / RHO_D_SUN
            rows[f"z {z}"] = dict(q=q, q_uncapped=qu, pass_=bool(q <= 1.0))
        RES[f]["P1"][f"f_basin {fb}"] = dict(rows=rows, status="PASS" if all(v["pass_"] for v in rows.values()) else "FAIL")
        P(f"[{f}] A2 P1 f_basin {fb}: q " + " ".join(f"{k} {v['q']:.3f}" for k, v in rows.items()) + f" (uncapped {rows['z 1.0']['q_uncapped']:.3f} at z 1) -> {RES[f]['P1'][f'f_basin {fb}']['status']}" + (" [GRADED]" if fb == 2.0 else " [reported]"))
# ---------------- P5 Bullet: galaxy-traced, Newtonian
def call(arg, mode):
    cp = subprocess.run(["nice", "-n", "10", sys.executable, os.path.abspath(__file__), "nchild", arg, mode], capture_output=True, text=True, env=dict(os.environ, OMP_NUM_THREADS="1"))
    line = [l for l in cp.stdout.splitlines() if l.startswith("PD1CHILD ")]
    if cp.returncode != 0 or not line: raise RuntimeError(cp.stderr[-1500:])
    return json.loads(line[0][9:])
o0 = call("{}", "newton"); mm = o0["masses"]; Mb = [mm["M_gas_sub"][j] + mm["M_star_sub"][j] for j in range(2)]; Mdark = {}; inf = {}
os.environ["PD1_SHARE"] = "5.41"
for f in FOOTS:
    B = footing_bg(f); T3 = share_table(B, A0[f], 0.3); v_ = []; ii = []
    for j in range(2):
        S = system(B, f, T3, Mb[j], z=0.3); R2 = S["R200_kpc"] * KPC
        ph = min(S["W"] * Mph(R2, Mb[j] * MS, A0[f]) / MS, S["E"]); md = ph + S["core"](S["R200_kpc"]) + rem_in(S, R2) / MS; v_.append(md)
        ii.append(dict(M_b=Mb[j], v_vir=S["v_vir"], f_core=S["f_core"], phantom_in_R200=ph, core_in_R200=S["core"](S["R200_kpc"]), dark_in_R200=md, galaxies_plus_dark=md + mm["M_star_sub"][j]))
    Mdark[f] = v_; inf[f] = ii
on = call(json.dumps(Mdark), "newton")
ka = on["KA_law_row"]; RES["KA_A2"] = dict(law_row_ZM=ka["ZM"], ref=[-4.548, -4.540], pass_=bool(abs(ka["ZM"][0] + 4.548) < 0.01 and abs(ka["ZM"][1] + 4.540) < 0.01), newton_baryons_only=on.get("KA_newton_baryons_only"))
P(f"KA-A2 law-only row Z {ka['ZM'][0]:+.3f}, {ka['ZM'][1]:+.3f} (DB1 -4.548, -4.540) -> {'PASS' if RES['KA_A2']['pass_'] else 'FAIL'}; Newtonian baryons-only row {on['KA_newton_baryons_only']['label']} (Z {on['KA_newton_baryons_only']['ZM'][0]:+.2f}, {on['KA_newton_baryons_only']['ZM'][1]:+.2f})")
for f in FOOTS:
    b = on[f]["row"]; RES[f]["P5_Bullet"] = dict(status="PASS" if b["label"] == "PASS" else "FAIL", row=b, subclusters=inf[f])
    P(f"[{f}] A2 P5 Bullet (galaxy-traced, Newtonian) {b['label']}: cls {b['cls']}; M300 Z {b['ZM'][0]:+.2f}, {b['ZM'][1]:+.2f}; d_gal {b['d_gal'][0]:.0f}/{b['d_gal'][1]:.0f} kpc, d_gas {b['d_gas'][0]:.0f}/{b['d_gas'][1]:.0f} kpc; "
      + ", ".join(f"sub {k}: dark in R200 {x['dark_in_R200']:.2e} (phantom {x['phantom_in_R200']:.2e}, core {x['core_in_R200']:.2e}), galaxies + dark {x['galaxies_plus_dark']:.2e}" for k, x in enumerate(inf[f])) + f"; gas {mm['M_gas_sub']}")
# ---------------- label
A = {s: json.load(open(os.path.join(HERE, f"pd1_a1_share{s}.json"))) for s in ("10.82", "5.41", "9.738", "11.902")}; Ab = json.load(open(os.path.join(HERE, "pd1_a1_share5.41_fcpre1.0.json")))
for f in FOOTS:
    st = {"P1 conservation": RES[f]["P1"]["f_basin 2.0"]["status"], "P2 KiDS": A["10.82"][f]["P2_KiDS"]["status"], "P2 SPARC": A["10.82"][f]["P2_SPARC"]["status"],
          "P3 groups": A["5.41"][f]["P3_groups"]["status"], "P3 X-COP": A["5.41"][f]["P3_XCOP"]["status"], "P4 cosmology (carried)": "PASS", "P5 Bullet": RES[f]["P5_Bullet"]["status"]}
    fails = [k for k, v in st.items() if v != "PASS"]; RES[f]["label"] = dict(status=st, label="PASS" if not fails else "FAIL", first_fail=fails[0] if fails else None)
    RES[f]["brackets"] = dict(f_basin_1p8_KiDS=A["9.738"][f]["P2_KiDS"], f_basin_2p2_KiDS=A["11.902"][f]["P2_KiDS"], prefactor1_XCOP=Ab[f]["P3_XCOP"]["status"], prefactor1_groups=Ab[f]["P3_groups"]["status"],
                              prefactor1_bullet_gaslocked=Ab[f]["P5_Bullet"]["status"], gaslocked_bullet_prefactor_half=A["5.41"][f]["P5_Bullet"]["status"])
    P(f"[{f}] PD1 under A2: LABEL {RES[f]['label']['label']}; first failing gate {RES[f]['label']['first_fail']}; " + ", ".join(f"{k} {v}" for k, v in st.items()))
json.dump(RES, open(os.path.join(HERE, "pd1_a2.json"), "w"), indent=1, default=float); open(os.path.join(HERE, "pd1_a2.out"), "w").write("\n".join(L) + "\n")
