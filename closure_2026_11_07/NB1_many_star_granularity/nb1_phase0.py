"""NB1 Phase 0 (criteria FROZEN_CRITERIA.md, 308bf8c6b0): 1D point-vs-ball power scan with the QX17C weak solver.
Adopted action = v3s + Pi^6 blend, b = rho_DE. Scaled blend scale b~ = K rho_DE Lstar/a0 = 16 pi a0 Lstar (K = 4 pi,
rho_DE = 4 a0^2 geometrized). The blend equals the raw form for Z >= b~ and Z < 0 (TC1); QX17C solves the raw
Z > 0 branch, so every solve here checks min Z over the grid against b~ and records it. If min Z < b~ the row is
flagged (the raw solve is then not the blend solve there). kappa = 1/2 FITTED; not theory closed.
Usage: python3 nb1_phase0.py
"""
import json, os, sys, time, importlib.util
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("qx17c", os.path.join(HERE, "..", "..", "closure_2026_11_06",
                                              "QX17C_fd_spherical_solver", "qx17c.py"))
sys.argv = [sys.argv[0]]
qx = importlib.util.module_from_spec(spec); spec.loader.exec_module(qx)

MS = [1e4, 1e6, 1e8, 1e10]; RS = [1, 2, 4, 8]; NPD = 400; SOUT_PC = 1e5; EPS_PT = 1e-3

def solve(Mmsun, Rl, a0, Ls, npd=NPD, sout=SOUT_PC):
    P = qx.Problem(qx.Gs * Mmsun * qx.Msun / qx.cs**2, Rl * Ls * qx.pc, a0, Ls, sout, npd, False, False)
    P.solve()
    Zm = np.diff(P.s**2 * P.Y) / (P.h * P.sm2)
    return P, float(np.min(Zm))

def Gat(P, s):
    gN = P.ystar / s**2          # exterior: all bare mass enclosed
    return gN + P.Yat(s)

out = {"criteria": "308bf8c6b0", "npd": NPD, "s_out_pc": SOUT_PC, "eps_point_Lstar": EPS_PT, "rows": {}}
t0 = time.time()
for foot, (a0, Ls) in qx.FOOT.items():
    btil = 16 * np.pi * (a0 / qx.cs**2) * Ls * qx.pc
    out[foot + "_b_tilde"] = btil
    for M in MS:
        pt, zp = solve(M, EPS_PT, a0, Ls)
        for R in RS:
            ball, zb = solve(M, R, a0, Ls)
            s = np.array([2.0, 5.0, 10.0]) * R
            r = Gat(pt, s) / Gat(ball, s) - 1
            gS = Gat(ball, s) / (ball.ystar / s**2 + qx.lawS_y(ball.ystar / s**2))
            key = f"{foot}|M{M:.0e}|R{R}"
            out["rows"][key] = {"ratio_minus1_2R_5R_10R": r.tolist(), "P": float(np.min(np.abs(r))),
                                "ball_G_over_lawS": gS.tolist(),
                                "point_G_over_lawS": (Gat(pt, s) / (pt.ystar / s**2 + qx.lawS_y(pt.ystar / s**2))).tolist(),
                                "newton_err": [pt.err, ball.err], "minZ": [zp, zb],
                                "minZ_below_btilde": bool(min(zp, zb) < btil)}
            print(key, "P=%.4f" % np.min(np.abs(r)), "r=", np.round(r, 4), "err %.1e %.1e" % (pt.err, ball.err),
                  "minZ %.2e %.2e" % (zp, zb), flush=True)
# choice: largest min(P_can, P_alt); ties -> smaller R
best = None
for M in MS:
    for R in RS:
        p = min(out["rows"][f"canonical|M{M:.0e}|R{R}"]["P"], out["rows"][f"alt|M{M:.0e}|R{R}"]["P"])
        if best is None or p > best[0] + 1e-12 or (abs(p - best[0]) <= 1e-12 and R < best[2]):
            best = (p, M, R)
out["chosen"] = {"P_min_footings": best[0], "M_msun": best[1], "R_Lstar": best[2], "no_power": best[0] < 0.15}
# convergence of the chosen cell's P: grid x2 and s_out x10
conv = {}
for foot, (a0, Ls) in qx.FOOT.items():
    s = np.array([2.0, 5.0, 10.0]) * best[2]
    base = out["rows"][f"{foot}|M{best[1]:.0e}|R{best[2]}"]["ratio_minus1_2R_5R_10R"]
    for tag, kw in (("grid_x2", {"npd": 2 * NPD}), ("sout_x10", {"sout": 10 * SOUT_PC})):
        pt, _ = solve(best[1], EPS_PT, a0, Ls, **kw); ba, _ = solve(best[1], best[2], a0, Ls, **kw)
        r = Gat(pt, s) / Gat(ba, s) - 1
        conv[f"{foot}|{tag}"] = float(np.max(np.abs(r - np.array(base))))
out["chosen_convergence_maxchange"] = conv
out["seconds"] = round(time.time() - t0, 1)
print("CHOSEN", out["chosen"], "conv", conv)
json.dump(out, open(os.path.join(HERE, "nb1_phase0.json"), "w"), indent=1)
