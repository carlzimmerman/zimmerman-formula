#!/usr/bin/env python3
"""X76 satellites: X75's committed x75_satkin.py (frozen measurement unchanged) with route E's galaxy halos from the
fair-share rule (x76_patch); the shift dlM becomes the log budget multiplier on M_b,tot; r_ta at the median host z.
Adds K2 (r_ta vs X30's formula) and K3 (solved halo mass = M_fair).  kappa = 1/2 FITTED; not theory closed.
    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x76_satellites.py      [X75_MUTATE=1 control]
"""
import os, sys, math, json
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); sys.path.insert(0, HERE)
import x76_patch as XP
S75 = os.path.join(REB, "X75_satellite_kinematics_mass_gap", "x75_satkin.py"); s = open(S75).read()
for a, b in (('    ns = {"__file__": X53SRC, "__name__": "x53_ro"}; argv0 = sys.argv; sys.argv = [X53SRC]',
              '    src = XP.patch(src, smooth=False, fair=True)\n    ns = {"__file__": X53SRC, "__name__": "x53_ro"}; ns.update(XP.ns_globals(True, 0.15)); argv0 = sys.argv; sys.argv = [X53SRC]'),
             ('SH = np.round(np.arange(-0.5, 1.2001, 0.01), 2)', 'SH = np.round(np.arange(-0.5, 1.7001, 0.01), 2)'),
             ('H = np.where(host_ok)[0]', 'H = np.where(host_ok)[0]\nZTA = float(np.median(z[H]))\nfor _n in NS.values(): _n["FAIR_Z"] = ZTA\nP(f"X76 fair-share halos: r_ta at median host z {ZTA:.4f}; dlM = log budget multiplier on M_b,tot")'),
             ('f"x75_satkin_results{TAG}.json"', 'f"x76_sat_results{TAG}.json"'), ('f"x75_satkin{TAG}.out"', 'f"x76_sat{TAG}.out"'),
             ('sys.exit(0 if n == len(CHK) else 1)', 'X76_POST()\nsys.exit(0 if n == len(CHK) else 1)')):
    assert s.count(a) == 1, a[:50]; s = s.replace(a, b)


def X76_POST():
    g = NSX
    # K2: r_ta vs X30's r_ta_com in SI at native parameters
    G, MS, MPC = 6.67430e-11, 1.98847e30, 3.0856775814913673e22
    H0 = XP.NAT_h * 100e3 / MPC; rhom = XP.NAT_OM * 3 * H0 ** 2 / (8 * math.pi * G)
    r30 = (3 * (XP.NAT_OM / XP.NAT_OB) * 1e11 * MS / (4 * math.pi * XP.DTA * rhom)) ** (1 / 3) / MPC * 1e6
    k2 = abs(XP.rta_pc(1e11, 0.0) / r30 - 1)
    # K3: solved halo mass to r_ta equals M_fair
    ns = g["NS"]["S"]; Ms = 10 ** 10.7; Mc = Ms * 10 ** (-0.69 * (10.7 - 2 * math.log10(0.70 / g["H_NAT"])) + 6.63); Mh = 0.5 * Ms
    Mf, rta, r0, Sig, _ = ns["FAIR_SETUP"]("canonical", Ms, Mc, Mh, g["HP"])
    k3 = abs(math.pi * Sig * r0 ** 2 * float(ns["B"](rta / r0)) / Mf - 1)
    g["check"]("K2x76_rta_vs_X30", k2 < 1e-12, f"{k2:.1e}")
    g["check"]("K3x76_halo_mass_eq_Mfair", k3 < 1e-8, f"{k3:.1e}; M_fair {Mf:.3e}, r_ta {rta / 1e3:.0f} kpc")
    g["RES"]["x76"] = dict(K2=k2, K3=k3, test_Mfair=Mf, test_rta_kpc=rta / 1e3, R_nat=XP.RNAT, z_ta=g["ZTA"])
    json.dump(g["RES"], open(os.path.join(HERE, f"x76_sat_results{g['TAG']}.json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, f"x76_sat{g['TAG']}.out"), "w").write("\n".join(g["OUT"]) + "\n")


NSX = {"__file__": os.path.join(HERE, "x76_satellites_exec.py"), "__name__": "__main__", "XP": XP, "X76_POST": X76_POST}
exec(compile(s, S75, "exec"), NSX)
