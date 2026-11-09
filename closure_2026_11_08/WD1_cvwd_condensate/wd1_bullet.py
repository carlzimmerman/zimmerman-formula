"""WD1 gate G6 (FROZEN_CRITERIA.md 0cd6ef1dcb): the Bullet through the record's own machinery (DB1 / UX6, read-only, child process
as NA2 / PB3 / PJ1 ran it). Two readings, both reported, the label resting on (b):
 (a) the proposal's centering rule as asserted: the component (f x each subcluster's baryons) rides on that subcluster's galaxies
     (DB1's galaxy-traced placement, on = "gal");
 (b) the component as its own equation of state makes it: an n^2 polytrope with c_max 750 km/s meeting a 4,700 km/s encounter is a
     Mach ~6 fluid, so it shocks and lags with the gas; the record's gas-traced Bullet treatment (DB1 on = "gas") at the same amount.
The record's gate (UX6 observe): the convergence peak must sit on the galaxies' side (guard, |Z| <= 3, dkappa > 0) and M300 within
the tolerance; cls FAIL otherwise. KA: the law alone (R 0) reproduces DB1 K1 (M300 1.112e14 / 7.337e13, dkappa -0.068 / -0.111).
The declared Bullet inputs (main N 6 d 600 kpc, sub N 5 d 500 kpc) set the as-written core radii; DB1's placement carries the
galaxies' (or the gas's) shape, not the Thomas-Fermi profile, so the as-written enclosed component inside 300 kpc of each
centroid is reported beside DB1's masses. kappa = 1/2 FITTED; not theory closed; footings never pooled."""
import os, sys, json, math, time, io, subprocess, resource
import numpy as np
import wd1 as W
P = W.P

def child():
    RB = W.RB; DB1 = os.path.join(RB, "DB1_cluster_dark_baryons"); src = open(os.path.join(DB1, "db1_fast.py")).read(); pre = src[:src.index("# ---------- X-COP, own replica")]
    a_ = 'OUT = open(f"db1_{MODE}{TG2}{TAG}.out", "w")'; assert pre.count(a_) == 1; pre = pre.replace(a_, "OUT = io.StringIO()")
    sys.path.insert(0, DB1); os.chdir(DB1); sys.argv = [os.path.join(DB1, "db1_fast.py"), "wd1"]
    BNS = {"__file__": os.path.join(DB1, "db1_fast.py"), "__name__": "db1_fast_wd1"}; so = sys.stdout; sys.stdout = io.StringIO(); out = {}
    try:
        exec(compile(pre, "db1_fast_prefix", "exec"), BNS)
        MST, MGJ, MGAS = BNS["MST"], BNS["MGJ"], BNS["MGAS"]; bullet_row = BNS["bullet_row"]
        out["KA"] = bullet_row("Z", "canonical", 0.0, Rs=[0.0, 0.0]); out["masses"] = dict(M_star_sub=[float(x) for x in MST], M_gas_sub=[float(x) for x in MGJ], M_gas_total=float(MGAS))
        f_ = W.F_COSMIC; Rs = [f_ * (MGJ[j] + MST[j]) / MST[j] for j in range(len(MST))]          # f x each subcluster's baryons, as a multiple of its stars (DB1's unit)
        out["Rs"] = [float(x) for x in Rs]
        for f in W.FOOTS:
            out[f] = {}
            for tag, on in (("a_asserted_on_galaxies", "gal"), ("b_gas_traced_Mach6", "gas")):
                o = bullet_row("Z", f, 0.0, Rs=Rs, on=on); out[f][tag] = o
    finally: sys.stdout = so
    out["child_peak_rss_MB"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6
    print("WD1CHILD " + json.dumps(out, default=float)); sys.exit(0)

def run_bullet(RES):
    cp = subprocess.run(["nice", "-n", "10", sys.executable, os.path.abspath(__file__), "--child"], capture_output=True, text=True, env=dict(os.environ, OMP_NUM_THREADS="1"))
    line = [l for l in cp.stdout.splitlines() if l.startswith("WD1CHILD ")]
    if cp.returncode != 0 or not line:
        P("bullet child failed: " + cp.stderr[-1500:]); RES["status"] = "child failed"; W.dump("bullet.json", RES); return
    out = json.loads(line[0][9:]); RES.update(out)
    k0 = out["KA"]; RES["KA_ok"] = bool(abs(k0["M300"][0] / 1.112e14 - 1) < 0.01 and abs(k0["M300"][1] / 7.337e13 - 1) < 0.01 and abs(k0["dkappa"][0] + 0.068) < 0.002 and abs(k0["dkappa"][1] + 0.111) < 0.002)
    P(f"KA Bullet (law alone): {'PASS' if RES['KA_ok'] else 'FAIL'} M300 {k0['M300'][0]:.4g}, {k0['M300'][1]:.4g}; dkappa {k0['dkappa'][0]:+.4f}, {k0['dkappa'][1]:+.4f}; child peak RSS {out['child_peak_rss_MB']:.0f} MB")
    m = out["masses"]; Mb_sub = [m["M_gas_sub"][j] + m["M_star_sub"][j] for j in range(2)]
    # the as-written Thomas-Fermi component of each subcluster inside 300 kpc of its own centroid (declared Bullet inputs), reported
    tf = {}
    for j, cls in enumerate(("bullet_main", "bullet_sub")):
        N, d = W.CLASS[cls]; tf[cls] = dict(N=N, d_kpc=d, Mb_sub=Mb_sub[j], Rc_kpc_at_300=float(W.rc_of(300.0, N, d)), comp_inside_300kpc=float(W.M_comp(300.0, Mb_sub[j], N, d)), comp_over_Mb_300=float(W.M_comp(300.0, Mb_sub[j], N, d)) / Mb_sub[j],
                        Rc_kpc_at_100=float(W.rc_of(100.0, N, d)), Rc_kpc_at_600=float(W.rc_of(600.0, N, d)), comp_over_Mb_600=float(W.M_comp(600.0, Mb_sub[j], N, d)) / Mb_sub[j])
    RES["as_written_TF_component"] = tf
    RES["mach"] = dict(c_max_kms=750.0, v_encounter_kms=4700.0, mach=4700.0 / 750.0)
    for f in W.FOOTS:
        for tag in ("a_asserted_on_galaxies", "b_gas_traced_Mach6"):
            b = out[f][tag]
            P(f"[{f}] {tag}: {b['label']} cls {b['cls']}; M300 {b['M300'][0]/1e14:.2f}, {b['M300'][1]/1e14:.2f} e14 (Z {b['ZM'][0]:+.2f}, {b['ZM'][1]:+.2f}); dkappa {b['dkappa'][0]:+.3f}, {b['dkappa'][1]:+.3f}; "
              f"peak-to-gal {b['d_gal'][0]:.0f}, {b['d_gal'][1]:.0f} kpc; peak-to-gas {b['d_gas'][0]:.0f}, {b['d_gas'][1]:.0f} kpc; M_comp {b['Mcb'][0]:.3g}, {b['Mcb'][1]:.3g} Msun")
    P("as-written TF component per subcluster: " + json.dumps(W.clean(tf)))
    RES["peak_rss_GB_parent"] = W.rss(); RES["seconds"] = time.time() - W.T0; RES["criteria"] = W.CRIT; RES["note"] = W.NOTE; RES["mutate"] = W.MUTATE
    W.dump(f"bullet{W.SUFFIX}.json", RES); P(f"bullet done {RES['seconds']:.0f} s")

if __name__ == "__main__" and "--child" in sys.argv: child()
