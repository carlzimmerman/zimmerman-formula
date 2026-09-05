#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""g03b -- Solar-System floors for the LOCAL static law's linear-response proxy.  The f32 operator stiffens the scalar's response by
1/(1 + xi^2 k^2) once (not the double filter of T-B): its QUMOND-ised proxy is an UNFILTERED source flux with ONE Helmholtz output filter,
Delta Phi_ph = S_H div[(nu - 1) grad u], S_H = (1 - xi^2 Delta)^{-1}.  Same three gates and inputs as G02 (Park 2026 Q2 ceiling, phantom mass
inside Saturn's orbit, the alpha = 1 sunward gate), both footings, three external-field inputs.  A proxy: the fourth-order nonlinear law
itself is not solved here.  Checks can fail."""
import math, sys, os, io, contextlib, numpy as np, warnings; warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__)); src = open(os.path.join(HERE, "g02_filtered_efe.py")).read()
head = src[:src.index("# ---------------------------------------------------------------- 3. the scans")]
g = {"__file__": os.path.join(HERE, "g02_filtered_efe.py")}
with contextlib.redirect_stdout(io.StringIO()): exec(compile(head, "g02head", "exec"), g)
IMPORTED_FAILS = list(g.get("FAILS", []))
PC, GM, A0, eN_of, phantom_density, observables = g["PC"], g["GM"], g["A0"], g["eN_of"], g["phantom_density"], g["observables"]
Q2_CEIL, M_SAT_BOUND, A_SUNWARD, PLANETS, R_SAT, MSUN, G = g["Q2_CEIL"], g["M_SAT_BOUND"], g["A_SUNWARD"], g["PLANETS"], g["R_SAT"], g["MSUN"], g["G"]
FAILS = list(IMPORTED_FAILS)
def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
print("g03b -- local law proxy: unfiltered flux, one Helmholtz output filter.  columns: Q2/ceil | M_ph(<Sat)/bound | max planetary |g_r|/sunward")
XIS = np.array([0.01, 0.02, 0.03, 0.05, 0.1, 0.3, 1.0])*PC
floors = {}
for foot, a0 in A0.items():
    rM = math.sqrt(GM/a0)
    for tag, gobs in (("2.00", 2.00e-10), ("2.32", 2.32e-10), ("2.64", 2.64e-10)):
        eN = eN_of(gobs, a0)
        for xi in XIS:
            r, th, rho = phantom_density(MSUN, 0.0, "gauss", eN, a0, 1e-4*rM, 1e4*rM)
            ob = observables(r, th, rho, xi, "helmholtz", a0)
            Msat = float(np.interp(R_SAT, r, ob["Menc"])); gr = max(abs(float(np.interp(rp, r, ob["g_r"]))) for rp in PLANETS.values())
            adm = abs(ob["Q2"]) < Q2_CEIL and Msat < M_SAT_BOUND and gr < A_SUNWARD
            floors[(foot, tag, xi)] = adm
            if tag == "2.32": print(f"  {foot:9s} g_ext {tag}e-10  xi = {xi/PC:5.2f} pc:  {abs(ob['Q2'])/Q2_CEIL:7.3f} | {Msat/M_SAT_BOUND:7.3f} | {gr/A_SUNWARD:7.3f}  {'admissible' if adm else 'EXCLUDED'}")
    fl = [xi for xi in XIS if all(floors[(foot, t, xi)] for t in ("2.00", "2.32", "2.64"))]
    fl = min(fl)/PC if fl else None
    print(f"  {foot}: smallest tabulated xi admissible at all three field inputs = {fl} pc")
    check(f"F1 [{foot}] the local law's proxy has a nonempty admissible window: some tabulated xi <= 0.1 pc passes all three gates at all three field inputs", fl is not None and fl <= 0.1, f"floor {fl} pc")
    check(f"F2 [{foot}] every tabulated xi above the floor stays admissible (the window is an interval up to 1 pc)", fl is not None and all(all(floors[(foot, t, xi)] for t in ("2.00", "2.32", "2.64")) for xi in XIS if xi/PC >= fl), "")
print(f"\nRESULT: {len(FAILS)} FAIL -> {FAILS}" if FAILS else "\nRESULT: 0 FAIL"); sys.exit(1 if FAILS else 0)
