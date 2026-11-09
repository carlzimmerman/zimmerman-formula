#!/usr/bin/env python3
"""SS1 gate 9 (FROZEN_CRITERIA.md b5adc7a90b + A1 9aeeb48503): the Bullet through the record's own machinery (DB1 / UX6 child,
read-only, as WD1 G6 runs it). The retained component is pressureless and collisionless, so it rides on the galaxies (DB1 on =
"gal"); its amount per subcluster is that subcluster's retained component from the radial peeling of its primary pre-conversion
halo (M_b,sys = DB1's gas + stars). The mediator drag per unit retained mass is ~Gamma0 <P_esc> (no absorption cross-section on
the component itself; Gamma0 / Gamma_psi reported). PASS iff DB1's label is PASS. KA6: the law alone reproduces DB1 K1.
    python3 ss1_bullet.py                       -> parts/bullet.json   (SS1_MUTATE=M? -> parts/bullet_M?.json)
kappa = 1/2 FITTED; not theory closed; footings never pooled; adopts nothing."""
import os, sys, json, math, time, io, subprocess, resource
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", "..")); sys.path.insert(0, HERE)
import ss1_core as C
RB = os.path.join(REPO, "rebuild_2026_10_22"); CL6 = os.path.join(REPO, "closure_2026_11_06"); CL7 = os.path.join(REPO, "closure_2026_11_07")
FOOTS = ("canonical", "alt"); SUFFIX = ("_" + C.MUT if C.MUT else "")
def P(s=""): print(s, flush=True)

def child(Rs_json):
    Rs_all = json.loads(Rs_json)
    DB1 = os.path.join(RB, "DB1_cluster_dark_baryons"); src = open(os.path.join(DB1, "db1_fast.py")).read(); pre = src[:src.index("# ---------- X-COP, own replica")]
    a_ = 'OUT = open(f"db1_{MODE}{TG2}{TAG}.out", "w")'; assert pre.count(a_) == 1; pre = pre.replace(a_, "OUT = io.StringIO()")
    sys.path.insert(0, DB1); os.chdir(DB1); sys.argv = [os.path.join(DB1, "db1_fast.py"), "ss1"]
    BNS = {"__file__": os.path.join(DB1, "db1_fast.py"), "__name__": "db1_fast_ss1"}; so = sys.stdout; sys.stdout = io.StringIO(); out = {}
    try:
        exec(compile(pre, "db1_fast_prefix", "exec"), BNS)
        MST, MGJ = BNS["MST"], BNS["MGJ"]; bullet_row = BNS["bullet_row"]
        out["KA"] = bullet_row("Z", "canonical", 0.0, Rs=[0.0, 0.0]); out["masses"] = dict(M_star_sub=[float(x) for x in MST], M_gas_sub=[float(x) for x in MGJ])
        if Rs_all:
            for f in FOOTS:
                Mret = Rs_all[f]; Rs = [Mret[j] / MST[j] for j in range(len(MST))]
                out[f] = dict(Rs=Rs, row=bullet_row("Z", f, 0.0, Rs=Rs, on="gal"))
    finally: sys.stdout = so
    out["child_peak_rss_MB"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6
    print("SS1CHILD " + json.dumps(out, default=float)); sys.exit(0)

def run():
    T0 = time.time(); RES = dict(criteria=C.CRIT, amendment=C.AMEND, mutate=C.MUT, note=C.NOTE)
    def call(arg):
        cp = subprocess.run(["nice", "-n", "10", sys.executable, os.path.abspath(__file__), "--child", arg], capture_output=True, text=True, env=dict(os.environ, OMP_NUM_THREADS="1"))
        line = [l for l in cp.stdout.splitlines() if l.startswith("SS1CHILD ")]
        if cp.returncode != 0 or not line: raise RuntimeError(cp.stderr[-1500:])
        return json.loads(line[0][9:])
    o0 = call("{}"); m = o0["masses"]; Mb_sub = [m["M_gas_sub"][j] + m["M_star_sub"][j] for j in range(2)]
    k0 = o0["KA"]; RES["KA6"] = dict(M300=k0["M300"], dkappa=k0["dkappa"], pass_=bool(abs(k0["M300"][0] / 1.112e14 - 1) < 0.01 and abs(k0["M300"][1] / 7.337e13 - 1) < 0.01 and abs(k0["dkappa"][0] + 0.068) < 0.002 and abs(k0["dkappa"][1] + 0.111) < 0.002))
    P(f"KA6 Bullet (law alone): {'PASS' if RES['KA6']['pass_'] else 'FAIL'} M300 {k0['M300'][0]:.4g}, {k0['M300'][1]:.4g}; dkappa {k0['dkappa'][0]:+.4f}, {k0['dkappa'][1]:+.4f}")
    Q15 = json.load(open(os.path.join(CL6, "QX15_cmb_primary_likelihood", "qx15.json"))); F1A = json.load(open(os.path.join(CL7, "F1A_primary_cmb_audit", "f1a.json")))
    Mret = {}; info = {}
    for f in FOOTS:
        h = float(Q15["footings"][f]["main"]["h"]); ob = Q15["footings"][f]["main"]["theta"]["omega_b"]; R = float(F1A[f]["R_B2"]); Om = ob * (1 + R) / h ** 2
        Hs = [C.halo(Mb, R, h, Om) for Mb in Mb_sub]; Pk = C.peel(Hs)
        Mret[f] = [float(Pk["M"][i].sum()) for i in range(2)]
        info[f] = [dict(M_b=Mb_sub[i], x0=C.x0_system(Hs[i]), R500_pre=Hs[i]["R500"], ret_total=C.retention(Pk, i), ret_R500=C.retention(Pk, i, Hs[i]["R500"]), retained=Mret[f][i], retained_over_Mb=Mret[f][i] / Mb_sub[i]) for i in range(2)]
    o = call(json.dumps(Mret)); RES["child_peak_rss_MB"] = max(o0["child_peak_rss_MB"], o["child_peak_rss_MB"]); RES["subclusters"] = info
    RES["drag"] = dict(Gamma0_over_Gamma_psi=(C.GAMMA0_GYR / 1e3) / 4.20, reading="momentum transfer per unit retained mass ~ Gamma0 <P_esc>: negligible against the 4,700 km/s crossing")
    for f in FOOTS:
        b = o[f]["row"]; RES[f] = dict(status="PASS" if b["label"] == "PASS" else "FAIL", Rs=o[f]["Rs"], row=b)
        P(f"[{f}] G9 Bullet (retained component on the galaxies): {b['label']} cls {b['cls']}; M300 {b['M300'][0]/1e14:.2f}, {b['M300'][1]/1e14:.2f} e14 (Z {b['ZM'][0]:+.2f}, {b['ZM'][1]:+.2f}); dkappa {b['dkappa'][0]:+.3f}, {b['dkappa'][1]:+.3f}; "
          f"peak-to-gal {b['d_gal'][0]:.0f}, {b['d_gal'][1]:.0f} kpc; retained/M_b " + ", ".join(f"{x['retained_over_Mb']:.3f} (x0 {x['x0']:.2f})" for x in info[f]))
    RES["seconds"] = time.time() - T0
    json.dump(RES, open(os.path.join(HERE, "parts", f"bullet{SUFFIX}.json"), "w"), indent=1, default=float); P(f"bullet done {RES['seconds']:.0f} s, child peak RSS {RES['child_peak_rss_MB']:.0f} MB")

if __name__ == "__main__":
    if "--child" in sys.argv: child(sys.argv[sys.argv.index("--child") + 1])
    else: run()
