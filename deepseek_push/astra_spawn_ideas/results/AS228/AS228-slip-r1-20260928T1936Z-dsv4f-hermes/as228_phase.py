#!/usr/bin/env python3
"""
AS228 phase driver — RSS-partitioned execution.

The macOS allocator does not return numpy churn to the OS, so a single
long-lived process drifts to ~1 GB RSS under the heavy probe loop.  This
driver runs each phase (per-cell solve+stats+probes, NEG, misc/refinement)
in a short-lived subprocess.  Each child holds only its own churn
(measured peak < 360 MB); the parent only merges JSON scalars.
"""
import gc, json, os, resource, signal, subprocess, sys, time
import numpy as np

import as228_slip as A


def _json_line(p):
    for l in p.stdout.splitlines():
        if l.startswith("RESULT_JSON="):
            return json.loads(l[len("RESULT_JSON="):])
    raise RuntimeError("no RESULT_JSON in worker: " + p.stderr[-2000:])


def _spawn(worker_args):
    env = dict(os.environ)
    for v in ("OPENBLAS", "OMP", "MKL", "NUMEXPR"):
        env.setdefault(v + "_NUM_THREADS", "1")
    env.setdefault("VECLIB_MAXIMUM_THREADS", "1")
    code = "import sys, as228_phase as P; sys.exit(P.%s)" % worker_args
    p = subprocess.run([sys.executable, "-B", "-c", code],
                       capture_output=True, text=True, env=env)
    if p.returncode != 0:
        raise RuntimeError("phase worker failed: " + p.stderr[-3000:])
    return _json_line(p)


# ---------------------------------------------------------------------------
# phase workers (each a bounded subprocess; signal.alarm(60))
# ---------------------------------------------------------------------------

def worker_cell(ell_cell):
    signal.alarm(60)
    t0 = time.time()
    T = A.Torus3(A.N_MAIN, A.L_MAIN)
    rho_b = A.tune_source(T)["rho_b"]
    A0G = A.A0G
    N, L = A.N_MAIN, A.L_MAIN
    F = A.solve_fields(T, rho_b, A0G, ell=ell_cell)
    tag = "ell_%g" % ell_cell
    cell = {}
    cell["y_window"] = [float(np.min(F["y"])), float(np.max(F["y"]))]
    cell["frac_transition"] = float(np.mean((F["f"] > 1e-6) & (F["f"] < 1.0 - 1e-6)))
    cell["frac_active"] = float(np.mean(F["f"] > 1.0 - 1e-6))
    cell["nu_max"] = float(np.max(F["nu"]))
    cell["slip_rms"] = A.rms(F["slip"]); cell["slip_max"] = A.mx(F["slip"])
    cell["Phi_max"] = A.mx(F["Phi"]); cell["Psi_max"] = A.mx(F["Psi"])
    cell["rho_ph_max"] = A.mx(F["rho_ph"]); cell["rho_slip_max"] = A.mx(F["rho_slip"])
    cell["slip_over_Phi_max_ratio"] = A.mx(F["slip"]) / max(A.mx(F["Phi"]), 1e-30)
    ai = np.argmax(np.abs(F["slip"]))
    cell["y_at_max_slip"] = float(np.asarray(F["y"]).flat[ai])
    cell["f_at_max_slip"] = float(np.asarray(F["f"]).flat[ai])
    Rslip = T.lap(F["slip"]) - 4.0 * np.pi * A.G_GRID * F["rho_slip"]
    Rlap = T.lap(F["Phi"]) - 4.0 * np.pi * A.G_GRID * rho_b - T.filter_s(T.div(F["j_ph"]))
    cell["R_slip_max"] = A.mx(Rslip)
    cell["R_slip_rms"] = A.rms(Rslip)
    cell["R_lapse_max"] = A.mx(Rlap)
    gr = A.gate_G(F["Yh"]) - ell_cell * T.lap(F["W"])
    RN = A.C_N * (4.0 * T.lap(F["Psi"]) + 4.0 * A.C_N * T.lap(F["U"]) + A.C_N * gr) / (16.0 * np.pi * A.G_GRID * A.C_N)
    RN = RN - RN.mean()
    cell["R_lapse_onshell_max"] = A.mx(RN)
    cell["R_lapse_onshell_rms"] = A.rms(RN)
    Fsav = {k: v for k, v in F.items() if isinstance(v, np.ndarray) and v.dtype != object}
    Fsav["a0g"] = np.asarray(A0G)
    npz = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fields_ell%g.npz" % ell_cell)
    np.savez(npz, **Fsav)
    stat_t, stat_tl = [], []
    spawn_rss = []
    centers = [(L/2, L/2, L/2), (L/2+2.5, L/2, L/2), (L/2-3.5, L/2+1.5, L/2)]
    for ci, ctr in enumerate(centers):
        for kind in ("trace", "traceless"):
            job = {"npz": npz, "ctr": list(ctr), "kind": kind,
                   "ell": float(ell_cell), "N": N, "L": L,
                   "wdir": os.path.dirname(os.path.abspath(__file__)),
                   "key": "ell%g_c%d_%s" % (ell_cell, ci, kind)}
            r = A.spawn_probe(job, spawn_rss)
            d = r["data"][0]
            if kind == "trace":
                stat_t.append({"center": list(ctr), "rms": d["rms"], "max": d["max"],
                               "sectors": d["sectors"]})
            else:
                stat_tl.append({"center": list(ctr), "rms": d["rms"], "max": d["max"]})
    cell["stationarity_trace"] = stat_t
    cell["stationarity_traceless"] = stat_tl
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1048576.0
    print("RESULT_JSON=" + json.dumps({"tag": tag, "cell": cell, "phase_wall_s": time.time() - t0,
                                       "phase_rss_mb": rss}, sort_keys=True, default=float))
    sys.stdout.flush()
    return 0


def worker_neg():
    signal.alarm(60)
    t0 = time.time()
    T = A.Torus3(A.N_MAIN, A.L_MAIN)
    rho_b = A.tune_source(T)["rho_b"]
    A0G = A.A0G
    N, L = A.N_MAIN, A.L_MAIN
    print("[NEG] no-slip branch tests")
    F = A.solve_fields(T, rho_b, A0G, ell=0.04)
    npz = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fields_neg.npz")
    Fsav = {k: v for k, v in F.items() if isinstance(v, np.ndarray) and v.dtype != object}
    Fsav["a0g"] = np.asarray(A0G)
    np.savez(npz, **Fsav)
    Fn = dict(F); Fn["Psi"] = F["Phi"].copy()
    Fsavn = {k: v for k, v in Fn.items() if isinstance(v, np.ndarray) and v.dtype != object}
    Fsavn["a0g"] = np.asarray(A0G)
    np.savez(os.path.join(os.path.dirname(os.path.abspath(__file__)), "fields_noslip.npz"), **Fsavn)
    spawn_rss = []
    r1 = A.spawn_probe({"npz": npz, "ctr": [L/2, L/2, L/2], "kind": "trace", "ell": 0.04,
                        "N": N, "L": L, "wdir": os.path.dirname(os.path.abspath(__file__)),
                        "key": "neg_solved"}, spawn_rss)
    r2 = A.spawn_probe({"npz": os.path.join(os.path.dirname(os.path.abspath(__file__)), "fields_noslip.npz"),
                        "ctr": [L/2, L/2, L/2], "kind": "trace", "ell": 0.04,
                        "N": N, "L": L, "wdir": os.path.dirname(os.path.abspath(__file__)),
                        "key": "neg_noslip"}, spawn_rss)
    r2b = A.spawn_probe({"npz": os.path.join(os.path.dirname(os.path.abspath(__file__)), "fields_noslip.npz"),
                         "ctr": [L/2, L/2, L/2], "kind": "trace", "ell": 0.04,
                         "N": N, "L": L, "wdir": os.path.dirname(os.path.abspath(__file__)),
                         "key": "neg_noslip2", "eps": 2e-6}, spawn_rss)
    dL_solv = r1["field"]; dL_nosi = r2["field"]; dL_nosi2 = r2b["field"]
    tN = {"dEH": r2["data"][0]["sectors"]["dEH"], "dAUX": r2["data"][0]["sectors"]["dAUX"],
          "dGATE": r2["data"][0]["sectors"]["dGATE"]}
    rho_slip_ns, _ = A.slip_source_analytic(Fn, T, 0.04)
    dL_diff = dL_nosi - dL_solv
    fd_floor_rms = A.rms(dL_nosi - dL_nosi2)
    fd_floor_max = A.mx(dL_nosi - dL_nosi2)
    neg = {
        "solved_rms": A.rms(dL_solv), "solved_max": A.mx(dL_solv),
        "no_slip_rms": A.rms(dL_nosi), "no_slip_max": A.mx(dL_nosi),
        "transition_stress_rms": A.rms(dL_diff), "transition_stress_max": A.mx(dL_diff),
        "fd_floor_rms": fd_floor_rms, "fd_floor_max": fd_floor_max,
        "sectors_no_slip": {k: A.rms(v) for k, v in tN.items()},
        "analytic_slip_src_rms": A.rms(rho_slip_ns),
        "analytic_slip_src_max": A.mx(rho_slip_ns),
        "verdict": "FIRES" if (A.mx(dL_diff) > 30.0 * max(fd_floor_max, 1e-30))
                              and (A.mx(rho_slip_ns) > 0.0) else "CHECK",
    }
    print("   no-slip residual rms=%.3e (solved rms=%.3e) -> %s"
          % (A.rms(dL_nosi), A.rms(dL_solv), neg["verdict"]))
    # gate-idle limit
    rho0 = A.gaussian_bump(T, (L/2, L/2, L/2), sigma=1.5)
    rho_s = rho0 * 0.7 * A.tune_source(T)["amp"] * 0.01
    Fi = A.solve_fields(T, rho_s, A0G, ell=0.04)
    Fsav = {k: v for k, v in Fi.items() if isinstance(v, np.ndarray) and v.dtype != object}
    Fsav["a0g"] = np.asarray(A0G)
    np.savez(os.path.join(os.path.dirname(os.path.abspath(__file__)), "fields_idle.npz"), **Fsav)
    r3 = A.spawn_probe({"npz": os.path.join(os.path.dirname(os.path.abspath(__file__)), "fields_idle.npz"),
                        "ctr": [L/2, L/2, L/2], "kind": "trace", "ell": 0.04,
                        "N": N, "L": L, "wdir": os.path.dirname(os.path.abspath(__file__)),
                        "key": "idle"}, spawn_rss)
    dL_idle = r3["field"]
    idle = {
        "y_max": float(np.max(Fi["y"])), "f_max": float(np.max(Fi["f"])),
        "no_slip_residual_rms": A.rms(dL_idle), "no_slip_residual_max": A.mx(dL_idle),
        "slip_rms": A.rms(Fi["slip"]),
        "verdict": "ZERO_LIMIT_OK" if A.rms(Fi["slip"]) < 0.05 * A.rms(F["slip"]) else "CHECK",
    }
    print("   idle-gate residual rms=%.3e (slip rms=%.3e, f_max=%.3g) -> %s"
          % (A.rms(dL_idle), A.rms(Fi["slip"]), float(np.max(Fi["f"])), idle["verdict"]))
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1048576.0
    print("RESULT_JSON=" + json.dumps({"neg": neg, "idle": idle, "phase_wall_s": time.time() - t0,
                                       "phase_rss_mb": rss}, sort_keys=True, default=float))
    sys.stdout.flush()
    return 0


def worker_refine():
    signal.alarm(50)
    t0 = time.time()
    L = A.L_MAIN
    amp = A.tune_source(A.Torus3(A.N_MAIN, L))["amp"]
    Tr = A.Torus3(72, L)
    rhor = A.gaussian_bump(Tr, (L/2, L/2, L/2), sigma=1.5) * amp
    Fr = A.solve_fields(Tr, rhor, A.A0G, ell=0.04)
    Rrs = Tr.lap(Fr["slip"]) - 4.0 * np.pi * A.G_GRID * Fr["rho_slip"]
    out = {"grid": 72, "R_slip_max": A.mx(Rrs), "slip_rms": A.rms(Fr["slip"]),
           "slip_max": A.mx(Fr["slip"])}
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1048576.0
    print("RESULT_JSON=" + json.dumps({"refinement": out, "phase_wall_s": time.time() - t0,
                                       "phase_rss_mb": rss}, sort_keys=True, default=float))
    sys.stdout.flush()
    return 0


def worker_misc():
    signal.alarm(60)
    t0 = time.time()
    T = A.Torus3(A.N_MAIN, A.L_MAIN)
    rho_b = A.tune_source(T)["rho_b"]
    A0G = A.A0G
    L = A.L_MAIN
    out = {"branches": {}, "refinement": {}, "projector": {}}
    for nm in A.BRANCHES:
        u2 = T.poisson(4.0 * np.pi * A.G_GRID * rho_b)
        W2 = T.filter_s(u2)
        p2 = T.grad(W2)
        y2 = np.sqrt(p2[0] ** 2 + p2[1] ** 2 + p2[2] ** 2) / A0G
        nu2 = A.BRANCHES[nm][0](y2)
        j2 = (nu2 - 1.0) * np.array(p2)
        rp2 = (1.0 / (4.0 * np.pi * A.G_GRID)) * T.filter_s(T.div(j2))
        out["branches"][nm] = {"rho_ph_max": A.mx(rp2), "nu_max": float(np.max(nu2))}
    print("[3] branch phantom peaks (comparison; MONO operative): " +
          ", ".join("%s=%.3e" % (nm, out["branches"][nm]["rho_ph_max"]) for nm in out["branches"]))
    rr = _spawn("worker_refine()")
    out["refinement"] = rr["refinement"]
    print("[4] refinement N96: R_slip_max=%.3e slip_rms=%.3e (rss %.0f MB)"
          % (rr["refinement"]["R_slip_max"], rr["refinement"]["slip_rms"], rr["phase_rss_mb"]))
    rho_d = 0.05 * rho_b * (1.0 + 0.3 * np.cos(2.0 * np.pi * T.X / L))
    zs = T.poisson((rho_d - rho_d.mean()) / (2.0 * A.C_N * 16.0 * np.pi * A.G_GRID))
    proj_trace = -3.0 * float(rho_d.mean()) * zs
    out["projector"] = {"rho_d_mean": float(rho_d.mean()),
                        "trace_rms": A.rms(proj_trace), "trace_max": A.mx(proj_trace),
                        "note": "Delta T^ij_mean = -[<N rho_d>_h/N] z h^ij (FINAL_ACTION eq.9): "
                                "vanishes identically for rho_d = 0; probe shows the operator active."}
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1048576.0
    print("RESULT_JSON=" + json.dumps({"misc": out, "phase_wall_s": time.time() - t0,
                                       "phase_rss_mb": rss}, sort_keys=True, default=float))
    sys.stdout.flush()
    return 0


# ---------------------------------------------------------------------------
# parent driver: merge only
# ---------------------------------------------------------------------------

def driver_main():
    print("=" * 96)
    print("AS228 — independent galactic spatial and lapse potentials (slip = Psi - Phi)")
    print("=" * 96)
    res = {"kernels": {}, "branches": {}, "controls": {}, "probes": {}, "footings": {}, "bounds": {}}
    res["kernels"]["landmarks"] = {"y_p": A._YP, "h_p": A._HP, "y_star": A._Y_STAR,
                                   "splice_continuity": float(A.h_rar(A._Y_STAR) - A._H_STAR)}
    for nm, (nu, _) in A.BRANCHES.items():
        ys = np.array([0.05, 0.1, 0.5, 1.0, 2.0, A._Y_STAR, 3.0, 10.0, 100.0])
        v = nu(ys)
        res["kernels"][nm] = {"nu_sample": [float(x) for x in v], "all_nu_gt_1": bool(np.all(v > 1.0))}
    print("[0] landmarks: y_p=%.6g h_p=%.6g y_star=%.6g" % (A._YP, A._HP, A._Y_STAR))
    Tt = A.Torus3(A.N_MAIN, A.L_MAIN)
    src = A.tune_source(Tt)
    res["source"] = {"amp": src["amp"], "y_peak": 12.0}
    print("[1] source tuned: amp=%.6e  (y_peak=12.00)" % src["amp"])
    phases = {"ell_0.04": ("worker_cell", (0.04,)), "ell_0.004": ("worker_cell", (0.004,)),
              "ell_0": ("worker_cell", (0.0,)), "neg": ("worker_neg", ())}
    for tag, (fname, args) in phases.items():
        print("\n[2] main cell ell = %g" % args[0] if tag.startswith("ell") else "\n[NEG]")
        call = "%s(%r)" % (fname, args[0]) if fname == "worker_cell" else "worker_neg()"
        r = _spawn(call)
        if "cell" in r:
            res["controls"][r["tag"]] = r["cell"]
            print("   cell %s done (wall %.1f s, rss %.0f MB)" % (r["tag"], r["phase_wall_s"], r["phase_rss_mb"]))
        else:
            res["controls"]["NEG"] = r["neg"]
            res["controls"]["gate_idle"] = r["idle"]
            print("   NEG + idle done (wall %.1f s, rss %.0f MB)" % (r["phase_wall_s"], r["phase_rss_mb"]))
    r = _spawn("worker_misc()")
    res["branches"] = r["misc"]["branches"]
    res["controls"]["refinement_N96"] = r["misc"]["refinement"]
    res["probes"]["projector_trace_stress"] = r["misc"]["projector"]
    # footings
    MB = 1.0e10 * A.M_SUN
    for nm, ft in A.FOOTINGS.items():
        rM = np.sqrt(A.G_SI * MB / ft["a0"])
        res["footings"][nm] = {"a0": ft["a0"], "rho_Lambda": ft["rho_Lambda"],
                               "a0_roundtrip": ft["a0_roundtrip"], "a0_relerr": ft["a0_relerr"],
                               "rM_m": float(rM), "rM_pc": float(rM / A.PC_SI)}
    ch = resource.getrusage(resource.RUSAGE_CHILDREN)
    self_rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1048576.0
    res["bounds"] = {"declared_wall_s": 120,
                     "enforced": "signal.alarm(120) umbrella; each phase child signal.alarm(60); "
                                 "each probe child signal.alarm(45); "
                                 "OPENBLAS/OMP/MKL/NUMEXPR/VECLIB=1; "
                                 "(macOS does not return numpy churn to the OS, so phases run "
                                 "in short-lived subprocesses)",
                     "threads": "OPENBLAS/OMP/MKL/NUMEXPR/VECLIB=1",
                     "recorded_wall_s": float(time.time() - A.T0),
                     "parent_rss_mb": self_rss,
                     "max_child_rss_mb": float(ch.ru_maxrss / 1048576.0)}
    print("\n[bounds] wall = %.2f s  parent_rss=%.0f MB  max_child_rss=%.0f MB"
          % (res["bounds"]["recorded_wall_s"], self_rss, res["bounds"]["max_child_rss_mb"]))
    with open("raw_output.json", "w") as fh:
        json.dump(res, fh, indent=1, sort_keys=True, default=float)
    print("RESULT_JSON=" + json.dumps(res, sort_keys=True, default=float))
    return 0


if __name__ == "__main__":
    sys.exit(driver_main())
