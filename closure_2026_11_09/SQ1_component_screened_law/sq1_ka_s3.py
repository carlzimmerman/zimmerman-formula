#!/usr/bin/env python3
"""SQ1 KA-S3 diagnosis (post-run, disclosed; criteria 7e8fa69c63): the shell integrator with WL1's background convention
(background enclosed = rho_bar(a) (4 pi / 3) r^3, the current radius) and the central excess unsoftened, single shells bisected on q
exactly as WL1's r_ta, against PD1's transcription of WL1's solver. Separates the convention (Lagrangian vs current-radius background)
from integrator error. kappa = 1/2 FITTED; not theory closed."""
import os, io, contextlib, math, json
HERE = os.path.dirname(os.path.abspath(__file__)); src = open(os.path.join(HERE, "sq1.py")).read(); cut = src.index("for f in FOOTS:\n    B = footing_bg(f); q1 = {}")
ns = {"__file__": os.path.join(HERE, "sq1.py"), "__name__": "sq1_lib"}
with contextlib.redirect_stdout(io.StringIO()): exec(compile(src[:cut], "sq1pre", "exec"), ns)
np, G, MS, MPC, solve_ivp = ns["np"], ns["G"], ns["MS"], ns["MPC"], ns["solve_ivp"]; out = {}
for f in ("canonical", "alt"):
    B = ns["footing_bg"](f); dM = 1e11 * MS * (1 + B.R)
    def kind(q, mode):
        ai = 1 / 1001.0
        def rhs(t, Y):
            r, v, a = Y
            bg = -(4 * math.pi * G / 3) * (B.RHO_M0 / a ** 3) * r if mode == "wl1" else -G * B.RHO_M0 * 4 * math.pi / 3 * q ** 3 / r ** 2
            return [v, bg - G * dM / r ** 2 + (8 * math.pi * G / 3) * B.OL * B.RHOC * r - (8 * math.pi * G / 3) * B.Orr * B.RHOC / a ** 4 * r, a * B.Hs(a)]
        def turn(t, Y): return Y[1]
        turn.terminal, turn.direction = True, -1
        def end(t, Y): return Y[2] - 1.0
        end.terminal = True
        so = solve_ivp(rhs, (0, 3e18), [ai * q, B.Hs(ai) * ai * q, ai], events=(turn, end), rtol=1e-9, atol=[1e-6 * ai * q, 1e-6, 1e-12], method="DOP853")
        return ("early", None) if so.t_events[0].size else ("late", so.y_events[1][0][0] if so.t_events[1].size else so.y[0, -1])
    res = {}
    for mode in ("wl1", "lagrangian"):
        lo, hi = math.log(1e-3 * MPC), math.log(50 * MPC)
        for _ in range(50):
            mid = 0.5 * (lo + hi); k, _r = kind(math.exp(mid), mode)
            if k == "early": lo = mid
            else: hi = mid
        res[mode] = dict(q_ta_Mpc=math.exp(hi) / MPC, r_ta_Mpc=kind(math.exp(hi), mode)[1] / MPC)
    ref = B.r_ta(dM, 0.0)[0] / MPC; res["WL1_solver_r_ta_Mpc"] = ref; res["wl1_mode_matches"] = bool(abs(res["wl1"]["r_ta_Mpc"] / ref - 1) < 0.01); out[f] = res
    print(f"[{f}] KA-S3 diagnosis: WL1 convention r_ta {res['wl1']['r_ta_Mpc']:.4f} Mpc (q {res['wl1']['q_ta_Mpc']:.2f}) vs PD1/WL1 solver {ref:.4f} -> {'MATCH' if res['wl1_mode_matches'] else 'NO MATCH'}; Lagrangian-mass convention r_ta {res['lagrangian']['r_ta_Mpc']:.4f} Mpc (q {res['lagrangian']['q_ta_Mpc']:.2f})")
json.dump(out, open(os.path.join(HERE, "sq1_ka_s3.json"), "w"), indent=1)
