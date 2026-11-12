"""PJ1 gate G6 (FROZEN_CRITERIA.md e3c9bc7d3c): the Bullet through the record's own machinery (DB1 / UX6, read-only, child process as
NA2 / PB3 run it). The proposal's relation is instantaneous: [1 + R_J^4 grad^4] rho_K = rho_b S(Phi), so in the merger the component is
S(Phi_Bullet) times the baryon field (gas + stars; R_J at the Bullet's depth is 0.3-200 kpc, below the 700 kpc separations, and a
symmetric kernel can only move the component's centroid toward the mass-weighted (gas) centre). The record's gate (UX6 observe):
the convergence peak must sit on the galaxies' side (guard, |Z| <= 3, dkappa > 0) and M300 within the tolerance; cls FAIL otherwise.
Evaluated at S/R in {0 (KA5, the law), 0.5, 0.8, 0.94, 1.0}; the grid's S at the Bullet depth maps onto these.
kappa = 1/2 FITTED; not theory closed; footings never pooled."""
import os, sys, json, math, time, io, subprocess, resource
import numpy as np
import pj1 as J
P = J.P
S_FRACS = [0.0, 0.5, 0.8, 0.94, 1.0]

def child():
    RB = J.RB; DB1 = os.path.join(RB, "DB1_cluster_dark_baryons"); src = open(os.path.join(DB1, "db1_fast.py")).read(); pre = src[:src.index("# ---------- X-COP, own replica")]
    a_ = 'OUT = open(f"db1_{MODE}{TG2}{TAG}.out", "w")'; assert pre.count(a_) == 1; pre = pre.replace(a_, "OUT = io.StringIO()")
    sys.path.insert(0, DB1); os.chdir(DB1); sys.argv = [os.path.join(DB1, "db1_fast.py"), "pj1"]
    BNS = {"__file__": os.path.join(DB1, "db1_fast.py"), "__name__": "db1_fast_pj1"}; so = sys.stdout; sys.stdout = io.StringIO(); out = {}
    try:
        exec(compile(pre, "db1_fast_prefix", "exec"), BNS)
        BU, SYS, C, A0, TOL, ZL = BNS["BU"], BNS["SYS"], BNS["C"], BNS["A0"], BNS["TOL"], BNS["ZL"]; law0 = SYS.extra
        MST, MGAS = BNS["MST"], BNS["MGAS"]
        def mk_extra(Sval):
            def extra(sp, Cc, reg=True):
                a0 = sp["a0"]; gv = tuple(sum(q[i] for q in Cc["gas"]) for i in range(3)); gb = [gv[i] + Cc["st"][i] for i in range(3)]
                if reg: gb[1] = gb[1] + a0 / 1000.0
                cb = [Sval * (gv[i] + Cc["st"][i]) for i in range(3)]
                tot = [gb[i] + cb[i] for i in range(3)]; g = np.sqrt(tot[0] ** 2 + tot[1] ** 2 + tot[2] ** 2); m = C.law(g, a0) / np.maximum(g, 1e-300)
                return tuple(tot[i] * m - gb[i] for i in range(3))
            return extra
        out["KA5"] = BNS["bullet_row"]("Z", "canonical", 0.0, Rs=[0.0, 0.0]); out["masses"] = dict(M_star_sub=[float(x) for x in MST], M_gas_total=float(MGAS))
        for f in J.FOOTS:
            out[f] = {}
            for fr in S_FRACS:
                Sval = fr * J.RF[f]; SYS.extra = mk_extra(Sval)
                try:
                    sp = {f: dict(form="CAND", k=0.0, a0=A0[f])}; Rr = BU["run"](sp); o = BU["observe"](*Rr[f])
                finally: SYS.extra = law0
                T = TOL["BULLET"]; zs = [(o["M300"][i] / T["obs_M300"][i] - 1) / T["sig_frac_PROVISIONAL"] for i in (0, 1)]; ok = o["cls"] != "FAIL" and all(abs(z) <= ZL for z in zs)
                out[f][f"{fr:g}"] = dict(S_over_R=fr, S=Sval, label="PASS" if ok else "FAIL", cls=o["cls"], M300=[float(x) for x in o["M300"]], ZM=zs, dkappa=[o["main"]["dkappa"], o["sub"]["dkappa"]],
                                         d_gal=[o["main"]["d_bcg"], o["sub"]["d_bcg"]], d_gas=[o["main"]["d_gas"], o["sub"]["d_gas"]], Z_offset=[o["main"]["Z"], o["sub"]["Z"]], guard=[o["main"]["guard"], o["sub"]["guard"]])
    finally: sys.stdout = so
    out["child_peak_rss_MB"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6
    print("PJ1CHILD " + json.dumps(out, default=float)); sys.exit(0)

def run_bullet(RES):
    cp = subprocess.run([sys.executable, os.path.abspath(__file__), "--child"], capture_output=True, text=True, env=dict(os.environ, OMP_NUM_THREADS="1"))
    line = [l for l in cp.stdout.splitlines() if l.startswith("PJ1CHILD ")]
    if cp.returncode != 0 or not line:
        P("bullet child failed: " + cp.stderr[-1500:]); RES["status"] = "child failed"; J.dump("bullet.json", RES); return
    out = json.loads(line[0][9:]); RES.update(out)
    k0 = out["KA5"]; RES["KA5_ok"] = bool(abs(k0["M300"][0] / 1.112e14 - 1) < 0.01 and abs(k0["M300"][1] / 7.337e13 - 1) < 0.01 and abs(k0["dkappa"][0] + 0.068) < 0.002 and abs(k0["dkappa"][1] + 0.111) < 0.002)
    P(f"KA5 Bullet (law alone): {'PASS' if RES['KA5_ok'] else 'FAIL'} M300 {k0['M300'][0]:.4g}, {k0['M300'][1]:.4g}; dkappa {k0['dkappa'][0]:+.4f}, {k0['dkappa'][1]:+.4f}; child peak RSS {out['child_peak_rss_MB']:.0f} MB")
    for f in J.FOOTS:
        for fr in S_FRACS:
            b = out[f][f"{fr:g}"]
            P(f"[{f}] S/R {fr:g} (S {b['S']:.2f}): {b['label']} cls {b['cls']}; M300 {b['M300'][0]/1e14:.2f}, {b['M300'][1]/1e14:.2f} e14 (Z {b['ZM'][0]:+.2f}, {b['ZM'][1]:+.2f}); dkappa {b['dkappa'][0]:+.3f}, {b['dkappa'][1]:+.3f}; "
              f"peak-to-gal {b['d_gal'][0]:.0f}, {b['d_gal'][1]:.0f} kpc; peak-to-gas {b['d_gas'][0]:.0f}, {b['d_gas'][1]:.0f} kpc; guard {b['guard']}")
    # the Bullet's depth per grid (Phi_*, p): law potential of the baryons (1 + S) at 300 kpc from the main centre, to r_cut; S solved as a fixed point
    MB_BULLET = out["masses"]["M_gas_total"] + sum(out["masses"]["M_star_sub"])
    def depth(Sfrac, a0, R):
        Mt = MB_BULLET * (1 + Sfrac * R) * J.MS; return J.tail_depth(Mt, 300 * J.KPC, a0) / J.CL ** 2
    RES["grid_map"] = {}
    for f in J.FOOTS:
        a0 = J.A0H[f]; R = J.RF[f]; m = {}
        for PHS in J.PHS_GRID + [1.5e-5, 1e-4, 3e-4]:
            for p_ in J.P_GRID:
                fr = 1.0
                for _ in range(60): fr = float(J.S_of(depth(fr, a0, R), PHS, p_, 1.0))
                near = min(S_FRACS[1:], key=lambda x: abs(x - fr)); b = out[f][f"{near:g}"]
                m[f"PHS {PHS:g}|p {p_}"] = dict(S_over_R=fr, depth_c2=depth(fr, a0, R), nearest_S_over_R=near, label=b["label"], cls=b["cls"], dkappa=b["dkappa"])
        RES["grid_map"][f] = m
        P(f"[{f}] grid map: S/R at the Bullet depth " + ", ".join(f"{k}: {v['S_over_R']:.3f} -> {v['label']}" for k, v in list(m.items())[:6]) + " ...")
    RES["peak_rss_GB_parent"] = J.rss(); RES["seconds"] = time.time() - J.T0; RES["criteria"] = J.CRIT; RES["note"] = J.NOTE; RES["M_b_bullet_Msun"] = MB_BULLET
    J.dump("bullet.json", RES); P(f"bullet done {RES['seconds']:.0f} s")

if __name__ == "__main__" and "--child" in sys.argv: child()
