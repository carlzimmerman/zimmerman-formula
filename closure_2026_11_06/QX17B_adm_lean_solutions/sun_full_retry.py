"""QX17B: retry of the Sun's FULL solve after the frozen run's full solve hit max mesh nodes (sph_solve_main.out).
Not a criteria change: the frozen GR-remainder row stays as recorded; this reports whether a converged full solve exists
at tol 1e-6 (20x below the 10 U_max = 2.1e-5 line) and, if so, its remainder. Both footings."""
import sys, json, numpy as np
sys.argv = ["x", "none"]
exec(open("sph_solve.py").read().split("mode = sys.argv")[0])
M_sun = Gs * Msun / cs**2; R_sun = 6.957e8
out = {}
for foot, (a0si, Ls) in FOOT.items():
    solw, parw = solve(M_sun, R_sun, a0si, Ls, False, 1e5, tol=1e-7)
    rows = {}
    for tol in (1e-6,):
        sol, par = solve(M_sun, R_sun, a0si, Ls, True, 1e5, tol=tol, guess=solw)
        ext = np.geomspace(2 * R_sun, 1e3 * par["L"], 400) / par["L"]
        yf = sol.sol(np.log(ext))[0] * par["Yref"]; yw = solw.sol(np.log(ext))[0] * parw["Yref"]
        rem = float(np.max(np.abs(yf - yw) / np.abs(yw)))
        rows[str(tol)] = {"status": int(sol.status), "message": sol.message, "nodes": int(sol.x.size),
                          "max_rms": float(sol.rms_residuals.max()), "GR_remainder": rem, "Umax": M_sun / R_sun,
                          "below_10U": rem <= 10 * M_sun / R_sun}
    out[foot] = rows; print(foot, rows, flush=True)
json.dump(out, open("sun_full_retry.json", "w"), indent=1)
