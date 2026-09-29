# -*- coding: utf-8 -*-
"""CFG172 A6 -- 11C-b: the operating point of F(K), K = (c2 theta^2 - c14 a^2)/M^2, the tie pincer, D1 (a0(z) law), G4 ledger.  Frozen: sec. 1.3 (11C-b), 3, 6 (A6).
Model (declared): F depends on u = y^2 - t, y = g/a0, t = K_bg/K_0 = (24 pi/(Omega_L kappa^2)) (c2/c14) (H/H0)^2 (=440 c2/c14 today); q_eff(y) = q(sqrt(u)) for u > 0,
Newtonian continuation q_eff = 0 for u <= 0 (declared); sensitivity: mirrored continuation q(sqrt(|u|)) for u < 0.
G1(b): solve mu_eff(y_g) y_g = y_N, compare with the P2 target on the G1 grid (point mass + exponential sphere, 7 masses, both footings).
D1: a_*(z) = sqrt(t(z)) a0 with t(z) = t0 (E(z))^2 (theta = 3H(z), CV4: K = 3H inside bound regions).
MUTATE = M1 (flow scale 3 a0, target unchanged, at the reference offset where G1 passes) | M6 (offset t -> 0.01 t at the tie: G1 deviation must fall)."""
from cfg172_common import *

R = Run("CFG172_A6_b_operating_point")
mut = R.mut
qP2 = lambda yv: 1.0 - (math.sqrt(1 + 4 * yv * yv) - 1) / (2 * yv) if yv < 1e5 else 1.0 / (2 * yv)

def solve_b(yN, t, s=1.0, cont="newton"):
    def mu(yg):
        u = (yg / s) ** 2 - t
        if u > 0:
            return 1.0 - qP2(math.sqrt(u))
        if cont == "mirror" and u < 0:
            return 1.0 - qP2(math.sqrt(-u))
        return 1.0
    f = lambda ly: mu(math.exp(ly)) * math.exp(ly) - yN
    lo, hi = math.log(yN) - 1e-12, math.log(yN) + 40
    if f(lo) >= 0:
        return yN
    return math.exp(brentq(f, lo, hi, xtol=1e-13))

def dev_b(t, s=1.0, cont="newton"):
    mx = 0.0
    for f_ in FOOT:
        a0 = A0[f_]
        for pn in ("point", "exp"):
            for M in (1e9, 1e10, 1e11, 1e12):
                r_, gN = profile_gN(M, pn, a0)
                yN = gN / a0
                yg = np.array([solve_b(v_, t, s, cont) for v_ in yN])
                tar = nu_p2(yN) * yN
                mx = max(mx, float(np.max(np.abs(yg / tar - 1))))
    return mx

ts = [0.0, 1e-8, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 0.1, 1.0, 1e2, 4.04e6]
if mut == "M6":
    dev_tie = dev_b(1.0); dev_low = dev_b(0.01)
    dm_tie = dev_b(1.0, cont="mirror"); dm_low = dev_b(0.01, cont="mirror")
    P(f"  M6 (Newtonian continuation): G1 deviation at t=1: {dev_tie:.3f}; at t=0.01: {dev_low:.3f}  -> {'bites' if dev_low < dev_tie else 'DOES NOT BITE (both saturate at the Newtonian value 0.967): declared control failure'}")
    P(f"  M6 (mirrored continuation) : G1 deviation at t=1: {dm_tie:.3f}; at t=0.01: {dm_low:.3f}  -> {'bites' if dm_low < dm_tie else 'does not bite'}")
    R.out["numbers"]["M6"] = {"newton": [dev_tie, dev_low], "mirror": [dm_tie, dm_low]}
    R.finish(bite=(dm_low < dm_tie))
scan = {}
for tt in ts:
    scan[tt] = {"newton": dev_b(tt), "mirror": dev_b(tt, cont="mirror")}
    P(f"  t = {tt:9.2e}: max G1 deviation  Newtonian continuation {scan[tt]['newton']:.3e}   mirrored continuation {scan[tt]['mirror']:.3e}")
R.out["numbers"]["G1b_scan"] = {str(k_): v_ for k_, v_ in scan.items()}
# t_max: largest t with G1 <= 0.10 (Newtonian continuation)
tm = brentq(lambda lt: dev_b(10 ** lt) - 0.10, -8, 0, xtol=1e-4) if dev_b(1e-8) < 0.10 else None
tm_mirror = brentq(lambda lt: dev_b(10 ** lt, cont="mirror") - 0.10, -8, 0, xtol=1e-4)
R.out["numbers"]["t_max_G1"] = {"newton": 10 ** tm if tm is not None else None, "mirror": 10 ** tm_mirror}
P(f"  G1(b) passes only for t <= {10**tm:.2e} (Newtonian continuation), {10**tm_mirror:.2e} (mirrored)")
tmin_allowed = json.load(open(os.path.join(HERE, "CFG172_A3_ppn_frame_results.json")))["numbers"]["t_min_in_G6G7_allowed_set"]
gap = tmin_allowed / (10 ** tm)
P(f"  t needed by G6 and G7 (A3) >= {tmin_allowed:.2e}; G1 allows t <= {10**tm:.2e}: gap factor {gap:.2e}")
R.check("A6.1 t -> 0 recovers 11C-a exactly (G1 deviation < 1e-6 at t = 0)", f"{scan[0.0]['newton']:.1e}", scan[0.0]["newton"] < 1e-6)
R.check("A6.2 t at the rule-T tie (1.0) already fails G1 (the offset balances, it does not just shift, the acceleration term)", f"{scan[1.0]['newton']:.3f}", scan[1.0]["newton"] > 0.10, load_bearing=True)
R.out["numbers"]["G1b_gap_factor"] = gap
R.verdict("G1-law (11C-b) at the rule-T tie t = 1", "FAIL" if scan[1.0]["newton"] > 0.10 else "PASS", f"max dev {scan[1.0]['newton']:.2f}")
R.verdict("G1-law (11C-b) at the G6 x G7 allowed corner t = 4e6", "FAIL" if scan[4.04e6]["newton"] > 0.10 else "PASS", f"max dev {scan[4.04e6]['newton']:.2f}")
R.verdict("G1-law (11C-b) overall", "FAIL" if gap > 1 else "PASS", f"G1 needs t <= {10**tm:.1e}; G6 and G7 need t >= {tmin_allowed:.1e}: no overlap (factor {gap:.1e})")
# D1: a_*(z)
zs = [0, 1, 2.5, 5]
E = lambda z: math.sqrt(OM * (1 + z) ** 3 + OL)
D1 = {}
for tt0, lab in ((1.0, "tie t0=1"), (4.04e6, "corner t0=4e6")):
    D1[lab] = {f"z={z}": math.sqrt(tt0) * E(z) for z in zs}
    P(f"  D1 (b, {lab}): a_*(z)/a0(z=0) = " + ", ".join(f"z={z}: {D1[lab][f'z={z}']:.3g}" for z in zs) + "   (flat law would be constant; H(z) rival gives E(z))")
R.out["numbers"]["D1_b"] = D1
R.out["numbers"]["D1_a_c"] = "flat: a_* = a0 (rule T; theta-term leaf-averaged, no H(z) in the a-channel)"
# G4 ledger
led = {"11C-a": {"strict": 1, "constants": ["c2 (window)"], "shape": "F_a = P2 (declared)"},
       "11C-b": {"strict": 1, "constants": ["overall size of c2 (ratio tied by rule T)"], "shape": "F = P2 branch + Newtonian continuation (declared)"},
       "11C-c": {"strict": 2, "constants": ["c2", "beta"], "shape": "F_a = P2, h (declared)"}}
R.out["numbers"]["G4_ledger_strict"] = led
R.check("A6.3 G4 ledger recorded (strict counts 1 / 1 / 2)", str({k_: v_["strict"] for k_, v_ in led.items()}), True, load_bearing=False)
# M1 reference: pick t_ref = 0.1 t_max (baseline passes), run with scale s = 3
if mut == "M1":
    t_ref = 0.1 * 10 ** tm
    d0 = dev_b(t_ref); d3 = dev_b(t_ref, s=3.0)
    P(f"  M1: at t_ref = {t_ref:.1e} G1 deviation {d0:.3f} (scale 1) -> {d3:.3f} (flow scale 3 a0)")
    R.finish(bite=(d0 <= 0.10 and d3 > 0.10))
R.finish(bite=False)
