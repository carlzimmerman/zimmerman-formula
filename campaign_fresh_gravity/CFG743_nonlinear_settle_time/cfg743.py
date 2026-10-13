"""CFG743: settle time of the collapsed cold medium (nonlinear identification 4 pi G P = -g_c). Criteria: FROZEN_CRITERIA.md.
kappa = 1/2 FITTED; footings never pooled; the cold energy's mass is required; no particle species; not "theory closed".
Run:  python3 cfg743.py      (CFG743_MUTATE=1: cosmic-mean density; exit 1 iff it reproduces CFG699 within 1e-3)
"""
import os, sys, json, math
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); sys.path.insert(0, LANES)
import CFG4_common as C4  # noqa: E402
MUT = os.environ.get("CFG743_MUTATE", "0") == "1"; TAG = "_MUTATE" if MUT else ""
G, C, MSUN, KPC, YR = 6.6743e-11, 2.99792458e8, 1.98847e30, 3.0856775814913673e19, 3.15576e7
def u_of(gN, a0):
    g = 0.5 * (gN + math.sqrt(gN * gN + 4 * gN * a0)); return g - gN
lines, res, ok = [__doc__.strip()], {}, True
for f in C4.FOOTS:
    a0 = C4.A0[f]; rho_bar = 0.26 / 0.686 * (a0 / (0.5 * C)) ** 2 / G
    lines.append(f"\n{f}: a0 {a0:.4e}; cosmic rho_c {rho_bar:.3e}")
    res[f] = {}
    for lm in (9, 10, 11, 12):
        M = 10 ** lm * MSUN
        for y in (0.1, 1.0):
            r = math.sqrt(G * M / (y * a0)); h = r * 1e-5
            m2u = lambda rr: rr * rr * u_of(G * M / rr ** 2, a0)
            rho = (m2u(r + h) - m2u(r - h)) / (2 * h) / (4 * math.pi * G * r * r)
            if MUT: rho = rho_bar
            x = u_of(y * a0, a0) / a0
            T = 2 * math.pi / math.sqrt(4 * math.pi * G * rho * ((1 - x) ** -2 - 1)) / YR / 1e9
            res[f][f"{lm}|{y}"] = dict(r_kpc=r / KPC, rho_c=rho, overdensity=rho / rho_bar, T_Gyr=T)
            ok &= T <= 1.38
            lines.append(f"    M_b 1e{lm} Msun, y {y}: r {r / KPC:8.2f} kpc; rho_c {rho:.2e} ({rho / rho_bar:.2e} x mean); period T = {T:.3g} Gyr")
if MUT:
    c699 = json.load(open(os.path.join(LANES, "CFG699_settle_time", "cfg699_results.json")))["canonical"]["1.0"]["T_Gyr"]
    mine = res["canonical"]["10|1.0"]["T_Gyr"]; rep = abs(mine / c699 - 1) <= 1e-3
    lines.append(f"\nMUTATE: cosmic-mean T {mine:.4g} vs CFG699 {c699:.4g} Gyr: reproduces {rep}"); rc = 1 if rep else 0
else:
    res["verdict"] = "PASS" if ok else "FAIL"; lines.append(f"\nVERDICT T1: {res['verdict']}"); rc = 0
    json.dump(res, open(os.path.join(HERE, "cfg743_results.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg743{TAG}.out"), "w").write("\n".join(lines) + "\n"); print("\n".join(lines)); sys.exit(rc)
