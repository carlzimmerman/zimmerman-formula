"""EFN1 route W (criteria 98364c8d20 section 3; A1 c3e466efbf): the leading linear mode of the discrete clock / gravity
operator and the weakly nonlinear (unstable-manifold) normal form da/dt = Gamma a + c2 a^2 + c3 a^3, plus KA-b1 (Gamma
against SCS3's converged route-L rate), KA-c (isolated twins: no growth) and MUTATE M4 (s-map second derivative flipped).

Usage: python3 efn1_route_w.py [res ...]   (default 2 3).  Writes efn1_route_w.json / .out; M4 rows go to
efn1_route_w_MUTATE.json / .out.  Eigenvectors for KA-b2 are saved to the system temp directory (efn1_cache/eig_*.npy).
"""
import os, sys, json, math, time, signal, resource
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import efn1_core as C

STOP = {"flag": False}
signal.signal(signal.SIGTERM, lambda *a: STOP.__setitem__("flag", True))
FOOTER = "kappa = 1/2 FITTED; not theory closed. Adopts nothing."
D1, D2 = 5e-4, 1e-3                      # amplitude stencil steps (criteria: 1e-3 and 5e-4, Richardson-combined)


class Mode:
    def __init__(self, o, Gam_ref):
        self.o = o
        try:
            lm = o.leading_mode(1.5 * Gam_ref ** 2, left=True)
            lm["sigma_over_Gref2"] = 1.5
        except Exception:                      # ARPACK did not converge (isolated twins): shift closer to zero, looser tol
            lm = o.leading_mode(0.1 * Gam_ref ** 2, left=True, tol=1e-8)
            lm["sigma_over_Gref2"] = 0.1
        self.lm = lm
        lam = lm["lam"].real
        self.lam = lam
        self.ok = lam > 0
        if not self.ok:
            return
        self.G = math.sqrt(lam)
        D = o.Didx; nD = len(D)
        p = lm["vec"]
        Gm = lambda x: (o.Cmat() @ x) / (C.K * o.V)               # n_t (full) from pi_D
        self.Cm = o.Cmat()
        q = (self.Cm @ p) / (C.K * o.V) / self.G
        kpk = D[int(np.argmax(np.abs(q[D])))]
        sc = abs(o.N0min) / np.max(np.abs(q[D])) * np.sign(q[kpk])  # a = 1 <-> max|n| = |min N0|; sign: n > 0 at the peak
        p = p * sc; q = q * sc
        self.e_pi = np.zeros(o.n); self.e_pi[D] = p; self.e_n = q
        fpi = np.zeros(o.n); fpi[D] = lm["vec_left"]
        fn = o.apply_MT(np.where(o.Dm, fpi, 0.0)) / self.G
        fn = np.where(o.Dm, fn, 0.0)
        nrm = fpi @ self.e_pi + fn @ self.e_n
        self.f_pi = fpi / nrm; self.f_n = fn / nrm

    def dot(self, a_pi, a_n):
        return float(self.f_pi @ a_pi + self.f_n @ a_n)

    def Nl(self, ypi, yn, **kw):
        o = self.o
        kw = dict(kw); kw.setdefault("central", True)          # amendment A3 (94c54483a9)
        a1, b1, i1 = o.rhs(ypi, yn, sig=1, tol=1e-13, **kw)
        a0, b0, _ = o.rhs(ypi, yn, sig=0)
        if not i1["ok"]:
            raise RuntimeError("s iteration failed in N(y)")
        return a1 - a0, b1 - b0

    def N2(self, ypi, yn, **kw):
        E = []
        for h in (D1, D2):
            p1 = self.Nl(h * ypi, h * yn, **kw); m1 = self.Nl(-h * ypi, -h * yn, **kw)
            E.append((p1[0] + m1[0], p1[1] + m1[1]))
        return ((16 * E[0][0] - E[1][0]) / (24 * D1 ** 2), (16 * E[0][1] - E[1][1]) / (24 * D1 ** 2))

    def N3(self, ypi, yn, **kw):
        O = []
        for h in (D1, D2):
            p1 = self.Nl(h * ypi, h * yn, **kw); m1 = self.Nl(-h * ypi, -h * yn, **kw)
            O.append((p1[0] - m1[0], p1[1] - m1[1]))
        return ((32 * O[0][0] - O[1][0]) / (48 * D1 ** 3), (32 * O[0][1] - O[1][1]) / (48 * D1 ** 3))

    def solve_shift(self, r_pi, r_n, k):
        """solve (k Gamma - L) h = r for the first-order system, L = [[0, M], [Gm, 0]]."""
        o = self.o; D = o.Didx
        G = self.G; s = (k * G) ** 2
        lu, n, nD = o.block_lu(s)
        rhs = k * G * r_pi + np.where(o.Dm, o.apply_M(r_n), 0.0)
        z = np.zeros(2 * n + nD); z[2 * n:] = rhs[D]
        x = lu.solve(z)[2 * n:]                                   # (B - s)^-1 rhs
        h_pi = np.zeros(o.n); h_pi[D] = -x
        h_n = (r_n + (self.Cm @ h_pi[D]) / (C.K * o.V)) / (k * G)
        h_n = np.where(o.Dm, h_n, 0.0)
        del lu
        return h_pi, h_n

    def normal_form(self, **kw):
        e_pi, e_n = self.e_pi, self.e_n
        n2 = self.N2(e_pi, e_n, **kw)
        c2 = self.dot(*n2)
        r_pi = n2[0] - c2 * e_pi; r_n = n2[1] - c2 * e_n
        h_pi, h_n = self.solve_shift(r_pi, r_n, 2)
        A = self.N2(e_pi + h_pi, e_n + h_n, **kw); B = self.N2(h_pi, h_n, **kw)
        mix = (A[0] - n2[0] - B[0], A[1] - n2[1] - B[1])                # 2 N2(e, h2)
        n3 = self.N3(e_pi, e_n, **kw)
        c3 = self.dot(mix[0] + n3[0], mix[1] + n3[1])
        return dict(c2=c2, c3=c3, h2_over_e=float(np.max(np.abs(h_n)) / max(np.max(np.abs(e_n)), 1e-300)),
                    f_dot_h2=self.dot(h_pi, h_n))


def fixed_points(G, c2, c3):
    """for each sign of a: smallest |a| > 0 with Gamma + c2 a + c3 a^2 = 0, and its stability."""
    out = {}
    roots = np.roots([c3, c2, G]) if c3 != 0 else np.array([-G / c2])
    for sgn in (1, -1):
        cand = [float(r.real) for r in roots if abs(r.imag) < 1e-12 * max(1, abs(r)) and r.real * sgn > 0]
        if cand:
            a = min(cand, key=abs)
            slope = G + 2 * c2 * a + 3 * c3 * a * a
            out["+" if sgn > 0 else "-"] = dict(a=a, stable=bool(slope < 0))
        else:
            out["+" if sgn > 0 else "-"] = None
    return out


def wn_reading(G, c2, c3):
    fp = fixed_points(G, c2, c3)
    if all(fp[s] is not None and fp[s]["stable"] and abs(fp[s]["a"]) <= 0.3 for s in "+-"):
        return "SATURATES-W", fp
    if any(fp[s] is None or abs(fp[s]["a"]) > 1 for s in "+-"):
        return "RUNAWAY-W", fp
    return "INCONCLUSIVE-W", fp


if __name__ == "__main__":
    RESS = [int(x) for x in sys.argv[1:]] or [2, 3]
    jpath = os.path.join(HERE, "efn1_route_w.json"); opath = os.path.join(HERE, "efn1_route_w.out")
    mpath = os.path.join(HERE, "efn1_route_w_MUTATE.json"); mopath = os.path.join(HERE, "efn1_route_w_MUTATE.out")
    RES = json.load(open(jpath)) if os.path.exists(jpath) else dict(lane="EFN1", script="efn1_route_w.py", criteria="98364c8d20",
                                                                     amendment_A1="c3e466efbf", rows={})
    MUT = json.load(open(mpath)) if os.path.exists(mpath) else dict(lane="EFN1", script="efn1_route_w.py (M4)", rows={})
    def P_(s, path=opath):
        print(s, flush=True)
        with open(path, "a") as fh: fh.write(s + "\n")
    jobs = []
    for res in RESS:
        for foot, lst in C.GRADED.items():
            for kind, lm in lst:
                jobs.append((foot, kind, lm, res, False))
        if res == 3:
            for foot, kind, lm in C.MUT_SET:
                jobs.append((foot, kind, lm, res, True))
    for foot, kind, lm, res, iso in jobs:
        if STOP["flag"]:
            print("SIGTERM: stopped; partial json kept"); break
        key = f"{foot}_{kind}_{lm}_R{res}" + ("_isolated" if iso else "")
        if key in RES["rows"]:
            continue
        t0 = time.time()
        ref = C.scs3_rate(foot, kind, lm, 0.1)
        bg = C.background(foot, kind, lm, 0.1, res, isolated=iso)
        o = C.Ops(bg)
        if iso:
            oe = C.Ops(C.background(foot, kind, lm, 0.1, res, isolated=False))
            o.N0min = oe.N0min; del oe
        md = Mode(o, ref["gamma_tu"])
        row = dict(grid=list(bg["g"].shape[:2]), n_dynamic=int(len(o.Didx)), lam_over_Gref2=md.lam / ref["gamma_tu"] ** 2,
                   lam=md.lam, eig_all_over_Gref2=[[v.real / ref["gamma_tu"] ** 2, v.imag / ref["gamma_tu"] ** 2] for v in md.lm["all"]],
                   scs3_efold_gyr=ref["efold_gyr"], isolated=iso, sigma_over_Gref2=md.lm["sigma_over_Gref2"])
        if iso:
            row["KAc_pass"] = bool(md.lam <= 1e-3 * ref["gamma_tu"] ** 2)
        elif md.ok:
            row["Gamma_over_Gref"] = md.G / ref["gamma_tu"]
            row["efold_gyr"] = C.TU_GYR / md.G
            row["KAb1_pass"] = bool(abs(md.G / ref["gamma_tu"] - 1) <= 0.10)
            D = o.Didx
            k = D[int(np.argmax(np.abs(md.e_n[D])))]
            row["mode_peak"] = [float(o.rcell[k] / o.re), float(np.degrees(o.thcell[k]))]
            w = np.abs(md.e_n[D]); row["mode_cells_above_half_peak"] = int(np.sum(w >= 0.5 * w.max()))
            row["left_check"] = float(np.linalg.norm(md.lm["lam_left"] - md.lm["lam"]) / abs(md.lm["lam"]))
            if res == 3:
                os.makedirs(C.CACHE, exist_ok=True)
                np.save(os.path.join(C.CACHE, f"eig_{foot}_{kind}_{lm}_R3.npy"), md.lm["vec"])
            try:
                nf = md.normal_form()
                row.update(c2_over_G=nf["c2"] / md.G, c3_over_G=nf["c3"] / md.G, h2_over_e=nf["h2_over_e"], f_dot_h2=nf["f_dot_h2"])
                rd, fp = wn_reading(md.G, nf["c2"], nf["c3"])
                row["wn_reading_if_converged"] = rd; row["fixed_points"] = fp
                if res == 3 and (foot, kind, lm) in C.MUT_SET:
                    fr = {}
                    for d_ in (5e-4, 5e-5):                    # the frozen (upwind) reading: the step test of A3
                        globals()["D1"], globals()["D2"] = d_, 2 * d_
                        nfu = md.normal_form(central=False)
                        fr[str(d_)] = dict(c2_over_G=nfu["c2"] / md.G, c3_over_G=nfu["c3"] / md.G)
                    globals()["D1"], globals()["D2"] = 5e-4, 1e-3
                    row["frozen_upwind_step_test"] = fr
                    nf4 = md.normal_form(sig_s=-1)
                    MUT["rows"][key] = dict(c2_over_G=nf4["c2"] / md.G, c2_true_over_G=nf["c2"] / md.G,
                                            rel_change=abs(nf4["c2"] - nf["c2"]) / max(abs(nf["c2"]), 1e-300),
                                            sign_changed=bool(np.sign(nf4["c2"]) != np.sign(nf["c2"])))
                    MUT["rows"][key]["bites"] = bool(MUT["rows"][key]["sign_changed"] or MUT["rows"][key]["rel_change"] >= 1.5)
                    MUT["footer"] = FOOTER
                    json.dump(MUT, open(mpath, "w"), indent=1)
                    P_(f"[{key}] M4 c2/Gamma true {nf['c2'] / md.G:.4g} flipped {nf4['c2'] / md.G:.4g}: bites {MUT['rows'][key]['bites']}", mopath)
            except Exception as ex:
                row["normal_form_error"] = repr(ex)
        row["seconds"] = round(time.time() - t0, 1)
        row["peak_rss_GB"] = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9, 3)
        RES["rows"][key] = row
        RES["footer"] = FOOTER
        json.dump(RES, open(jpath + ".tmp", "w"), indent=1); os.replace(jpath + ".tmp", jpath)
        P_(f"[{key}] " + json.dumps({k_: v_ for k_, v_ in row.items() if k_ not in ("eig_all_over_Gref2",)}))
    print(FOOTER)
