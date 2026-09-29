#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CFG188 R3 -- 11C-b: single function M^2 F(K), K = (c2 theta^2 - c14 a^2)/M^2.
B1 own static reduction at theta = theta_bg with the rule-T anchor u = y^2 - t (continuations N, Mi, L; x_max 30/10/3),
B2 G6/G7 region undressed, B3 redundancy of the overall size + momentum-constraint structure (CV4), B4 F-dressed G6/G7,
B5 anchor alternatives and D1, B6 pincer status.   G7 threshold (c2 >= 2.7e-5), alpha_1, alpha_2 formulas: QUOTED (independence stops).
MUTATE=M5 (anchor moved to K_bg), M6 (apply F-dressing to c2 and c14 in alpha_2)."""
import sys, math
import numpy as np
import sympy as sp
from scipy.optimize import brentq
import CFG188_common as C

def muP2(w):
    w = abs(w)
    return 2 * w / (math.sqrt(1 + 4 * w * w) + 1) if w > 0 else 0.0
def qP2(w):
    return 1.0 - muP2(w)
def qeff(y, t, cont):
    u = y * y - t
    if u >= 0:
        return qP2(math.sqrt(u))
    if cont == "N":
        return 0.0
    if cont == "Mi":
        return qP2(math.sqrt(-u))
    if cont == "L":
        return 1.0
    raise ValueError(cont)

_YG = np.logspace(-7, 6, 5000)
def roots_for(yN, t, cont):
    h = np.array([y * (1.0 - qeff(y, t, cont)) for y in _YG]) - yN
    idx = np.where(np.sign(h[:-1]) * np.sign(h[1:]) < 0)[0]
    out = []
    for i in idx:
        try:
            out.append(brentq(lambda y: y * (1.0 - qeff(y, t, cont)) - yN, _YG[i], _YG[i + 1], xtol=1e-14, rtol=1e-12))
        except Exception:
            pass
    return out

def maxdev(t, cont, xmax=30.0, pick="largest", n=24):
    worst = 0.0
    for x in np.logspace(-1, math.log10(xmax), n):
        yN = 1 / x ** 2; yt = math.sqrt(yN * yN + yN)
        rts = roots_for(yN, t, cont)
        if not rts:
            return 1.0
        if pick == "largest": yg = max(rts)
        elif pick == "smallest": yg = min(rts)
        else: yg = min(rts, key=lambda v: abs(v / yt - 1))
        worst = max(worst, abs(yg / yt - 1))
    return worst

def t_max(cont, xmax=30.0, pick="largest"):
    tg = np.logspace(-10, 2, 49)
    last_pass, first_fail = None, None
    for t in tg:
        if maxdev(t, cont, xmax, pick) <= 0.10:
            last_pass = t
        else:
            first_fail = t
            break
    if last_pass is None:
        return 0.0
    if first_fail is None:
        return float("inf")
    lo, hi = math.log(last_pass), math.log(first_fail)
    for _ in range(20):
        mid = 0.5 * (lo + hi)
        if maxdev(math.exp(mid), cont, xmax, pick) <= 0.10: lo = mid
        else: hi = mid
    return math.exp(lo)

def alpha2(c14, c2):
    return c14 * (c14 - c2 + 2 * c14 * c2) / (c2 * (2 - c14))

def main():
    chk = C.Checks(); R = {}
    m = C.mode()
    print("CFG188 R3 -- 11C-b. mode:", m or "main")
    a0 = C.FOOT["canonical"]
    th3H = 3 * C.C_SI * C.H0_SI / a0                     # 3 c H0 / a0
    T440 = th3H ** 2                                      # t = (c2/c14) * T440  (actual theta = 3 H0)
    T301 = 24 * math.pi / 0.5 ** 2                        # theta_Lambda: 24 pi / kappa^2, kappa = 1/2 (FITTED)
    R["T_actual_theta"] = T440; R["T_theta_Lambda"] = T301
    print(f"  (3 c H0/a0)^2 = {T440:.1f} (actual theta = 3 H0);  24 pi/kappa^2 = {T301:.1f} (theta_Lambda; kappa=1/2 FITTED)")
    chk.add("rule-T ratios reproduce 440 (actual theta) and 301.6 (theta_Lambda)", abs(T440 - 440) < 10 and abs(T301 - 301.6) < 0.2, f"{T440:.1f}, {T301:.1f}")

    if m in ("", "M5", "M6"):
        # ---------------- B1
        if m == "":
            tm = {}
            for cont in ("Mi", "N", "L"):
                for xmax in (30.0, 10.0, 3.0):
                    tm[f"{cont}_xmax{int(xmax)}_largest_root"] = t_max(cont, xmax, "largest")
                tm[f"{cont}_xmax30_smallest_root"] = t_max(cont, 30.0, "smallest")
                tm[f"{cont}_xmax30_best_root"] = t_max(cont, 30.0, "best")
            R["B1_t_max"] = tm
            for k_, v in tm.items():
                print(f"  B1: t_max[{k_}] = {v:.3e}")
            # E20: (y q_eff)' just above the branch point for t > 0
            t0 = 1e-3
            ys = math.sqrt(t0) * np.array([1.0001, 1.001, 1.01, 1.1, 2.0, 10.0])
            d = []
            for yv in ys:
                hh = yv * 1e-6
                d.append(((yv + hh) * qeff(yv + hh, t0, "Mi") - (yv - hh) * qeff(yv - hh, t0, "Mi")) / (2 * hh))
            R["E20_ypq_eff_just_above_branch_t1e-3"] = [float(v) for v in d]
            print("  B1/E20: (y q_eff)' just above the branch point (t = 1e-3):", [f"{v:.3f}" for v in d])
            chk.expect("E20: (y q_eff)' < 0 just above the branch point for t > 0 (finite slope Q'(0) = -1)  [true at 1.0001 sqrt(t); the negative band is narrow, see the width printed next]", d[0] < 0)
            # width of the wrong-sign band: solve (y q)' = 0 above the branch
            def ypq_(yv):
                hh = yv * 1e-10
                return ((yv + hh) * qeff(yv + hh, t0, "Mi") - (yv - hh) * qeff(yv - hh, t0, "Mi")) / (2 * hh)
            lo_ = math.sqrt(t0) * (1 + 1e-6); hi_ = math.sqrt(t0) * 1.01
            yz = brentq(ypq_, lo_, hi_, xtol=1e-16)
            R["E20_band_relative_width_t1e-3"] = yz / math.sqrt(t0) - 1
            print(f"  B1/E20: the wrong-sign band for t = 1e-3 ends at y = sqrt(t) (1 + {yz/math.sqrt(t0)-1:.2e}); predicted width ~ t/2 = {t0/2:.1e}")
            chk.add("B1: at t -> 0 the G1 law is recovered (max dev <= 1e-6)", maxdev(1e-12, "Mi") <= 1e-6, f"{maxdev(1e-12,'Mi'):.2e}")
            chk.add("B1: at the rule-T tie (t = 1 at theta_Lambda anchor, 1.46 or 0.46 at the actual theta) G1 fails badly for every continuation", all(maxdev(tt, cn) > 0.1 for tt in (1.0, 1.46) for cn in ("Mi", "N", "L")))
            R["B1_dev_at_t1"] = {cn: maxdev(1.0, cn) for cn in ("Mi", "N", "L")}
        # ---------------- B2 (undressed, quoted formulas)
        undr = {}
        for label, a1max in (("3.4e-5", 3.4e-5), ("3.5e-5", 3.5e-5), ("2.1e-5", 2.1e-5)):
            c2v = 2.7e-5
            f_ = lambda c14: alpha2(c14, c2v) + 1.6e-9
            c14max_alpha2 = brentq(f_, 1e-14, 0.5 * c2v, xtol=1e-25, rtol=1e-12)     # small branch (alpha_2 negative)
            c14max_alpha1 = a1max / 4.0
            c14max = min(c14max_alpha2, c14max_alpha1)
            undr[label] = {"c14max_alpha2_small_branch": c14max_alpha2, "c14max_alpha1": c14max_alpha1, "c14max": c14max,
                           "t_min_actual_theta": T440 * c2v / c14max, "t_min_theta_Lambda": T301 * c2v / c14max}
            # equal-speed branch c14 ~ c2: alpha_1 = -4 c14 excluded?
            undr[label]["locus_c14_eq_c2_alpha1"] = 4 * c2v / (1 - 2 * c2v)
        R["B2_undressed"] = undr
        print("  B2 (undressed, quoted formulas): c14_max(alpha_2 <= 1.6e-9 at c2 = 2.7e-5) =", f"{undr['3.4e-5']['c14max_alpha2_small_branch']:.3e}", "; t_min (actual theta) =", f"{undr['3.4e-5']['t_min_actual_theta']:.3e}", "(lane: 4.0e6); theta_Lambda:", f"{undr['3.4e-5']['t_min_theta_Lambda']:.3e}")
        print("      equal-speed branch c14 ~ c2: |alpha_1| =", f"{undr['3.4e-5']['locus_c14_eq_c2_alpha1']:.2e}", "> 3.4e-5: excluded undressed")
        chk.add("B2: undressed t_min on the G6 x G7 region (actual theta) within 15% of the lane's 4.0e6", abs(undr["3.4e-5"]["t_min_actual_theta"] / 4.0e6 - 1) < 0.15, f"{undr['3.4e-5']['t_min_actual_theta']:.3e}")
        # ---------------- B3 redundancy and momentum constraint (sympy)
        c2, c14, M2, th, a2s, s_, Kf = sp.symbols("c2 c14 M2 theta a2 s K", positive=True)
        Ffun = sp.Function("F")
        Kexp = (c2 * th ** 2 - c14 * a2s) / M2
        Lb = M2 * Ffun(Kexp)
        Lscaled = (s_ * M2) * (Ffun((s_ * c2 * th ** 2 - s_ * c14 * a2s) / (s_ * M2)) / s_)          # (c2,c14,M2) -> s (c2,c14,M2), F -> F/s
        red = sp.simplify(Lscaled - Lb) == 0
        chk.add("B3: (c2, c14, M^2) -> s (c2, c14, M^2) with F -> F/s leaves L = M^2 F(K) exactly invariant: the overall size is a redefinition of F", red)
        Fp = sp.Function("Fp")(Kexp)
        coef_a = -c14 * Fp; coef_t = c2 * Fp
        ratio = sp.simplify(coef_t / coef_a)
        chk.add("B3: coefficient ratio (theta^2 : a^2) = -c2/c14 independent of F' (dressing cancels in the ratio)", sp.simplify(ratio + c2 / c14) == 0)
        R["B3_redundancy"] = bool(red)
        # momentum constraint  D_i[ K (c2 F' - 2/3) ] = 0  (isotropic K_ij = K h_ij/3), derived from pi^{ij} = 2 [K^{ij} - K h^{ij} (1 - c2 F')]
        Kt, Fpp_, hh = sp.symbols("Ktr Fpr h", real=True)
        pi_coeff = sp.simplify((Kt / 3) - Kt * (1 - c2 * Fpp_))         # coefficient of h^{ij}
        print("  B3: momentum-constraint coefficient K (c2 F' - 2/3) =", sp.factor(pi_coeff), " (K constant only if c2 F' is constant)")
        R["B3_momentum_coefficient"] = str(sp.factor(pi_coeff))
        # K variation across a galaxy: K(y)/K(inf) = 1/(1 + 3 q / R)  (c2 F' = -2q/R) or 1/(1 - 3q/R) for the other F' sign
        var = {}
        for Rr in (T301, T440):
            var[f"R={Rr:.1f}"] = {"y->0": 1 / (1 + 3.0 / Rr) - 1, "other_sign": 1 / (1 - 3.0 / Rr) - 1}
        R["B3_K_variation_deep_MOND_vs_far"] = var
        print("  B3: K inside deep-MOND regions relative to far away (K (c2 F' - 2/3) = const):", {k_: f"{v['y->0']:+.4f}/{v['other_sign']:+.4f}" for k_, v in var.items()}, "(CV4 record: |K/3H - 1| < 1e-2)")
        chk.add("B3: K stays within ~1% of its cosmic value for R = 301.6 / 440 (agrees with the record's CV4 conclusion, but K is not exactly uniform)", max(abs(v["y->0"]) for v in var.values()) < 0.011)
        # ---------------- B4 dressed
        # pulsar row (representative, from memory, unverified): J1738+0333-like binary
        Gm = 6.6743e-11; Msun = 1.98847e30
        Mtot = 1.66 * Msun; Mc = 0.181 * Msun; Pb = 0.3548 * 86400.0
        asep = (Gm * Mtot * Pb ** 2 / (4 * math.pi ** 2)) ** (1 / 3)
        g_psr = Gm * Mc / asep ** 2
        y_p = g_psr / a0
        yS = C.GM_SUN / (9.58 * C.AU) ** 2 / a0; yE = C.GM_SUN / C.AU ** 2 / a0
        R["y_pulsar_hand"] = y_p; R["y_Saturn"] = yS; R["y_Earth"] = yE
        print(f"  B4: y_Saturn = {yS:.3e}, y_Earth = {yE:.3e}, y_pulsar (representative binary, from memory: unverified) = {y_p:.3e}")
        dressed = {}
        for Rr in (T301, T440):
            row = {}
            for nm, yv in (("Saturn", yS), ("Earth", yE), ("pulsar", y_p)):
                q = qP2(yv); c14e = 2 * q; c2e = 2 * q / Rr
                row[nm] = {"q": q, "alpha1": -4 * c14e, "alpha2": alpha2(c14e, c2e)}
            for nm, yv in (("y=0.1", 0.1), ("y=1", 1.0), ("y=10", 10.0), ("y=100", 100.0)):
                q = qP2(yv); c14e = 2 * q; c2e = 2 * q / Rr
                Cc = 2 * (2 + 3 * c2e) / (c2e * (2 - c14e))
                D = Cc * (600.0 / C.C_KMS) ** 2
                row[nm] = {"q": q, "c2_eff": c2e, "D": D, "D_over_3": D / 3}
            # ambient (galactic) reading for the preferred-frame sector of the Solar System: y ~ 1.5
            qa = qP2(1.5)
            row["ambient_y1.5"] = {"alpha1": -8 * qa}
            # R threshold from the pulsar alpha_2 line: R q_p <= 1.6e-9 (R >> 1)
            dressed[f"R={Rr:.1f}"] = row
        R["B4_dressed"] = dressed
        for k_, row in dressed.items():
            print(f"  B4 [{k_}]: pulsar alpha_2 = {row['pulsar']['alpha2']:.2e} (line 1.6e-9); Saturn alpha_1 = {row['Saturn']['alpha1']:.2e}, Earth alpha_1 = {row['Earth']['alpha1']:.2e}; ambient(y=1.5) alpha_1 = {row['ambient_y1.5']['alpha1']:.2f}; D/3 at y = 0.1/1/10/100: " + "/".join(f"{row[n]['D_over_3']:.3g}" for n in ('y=0.1', 'y=1', 'y=10', 'y=100')))
        # dressed pulsar line: largest R allowed
        qp = qP2(y_p)
        Rmax_pulsar = brentq(lambda Rr: alpha2(2 * qp, 2 * qp / Rr) - 1.6e-9, 1.0, 1e9)
        # G7 dressed: c2_eff(y_gal) >= 2.7e-5 -> R <= 2 q / 2.7e-5
        Rmax_G7 = {nm: 2 * qP2(yv) / 2.7e-5 for nm, yv in (("y=0.1", 0.1), ("y=1", 1.0), ("y=10", 10.0))}
        tmin_dressed = {"G6_pulsar": T440 / Rmax_pulsar, **{f"G7_{k_}": T440 / v for k_, v in Rmax_G7.items()}}
        R["B4_Rmax_pulsar"] = Rmax_pulsar; R["B4_tmin_dressed"] = tmin_dressed
        print(f"  B4: dressed pulsar line requires R <= {Rmax_pulsar:.3g}  (t >= {T440/Rmax_pulsar:.3g}); dressed G7 requires t >= " + ", ".join(f"{v:.3g} ({k_})" for k_, v in tmin_dressed.items() if k_.startswith('G7')))
        chk.expect("E17: at the rule-T tie (R = 301.6 / 440) the F-dressed pulsar-row alpha_2 is below 1.6e-9 (G6(b) flips to PASS under dressing)", all(dressed[k_]["pulsar"]["alpha2"] <= 1.6e-9 for k_ in dressed), f"{max(dressed[k_]['pulsar']['alpha2'] for k_ in dressed):.2e} vs 1.6e-9 (representative pulsar y_p, from memory)")
        chk.expect("E14: Newtonian-continuation t_max is not the lane's 1.2e-6 (largest-root branch)", not (0.3e-6 < R["B1_t_max"]["N_xmax30_largest_root"] < 4e-6) if "B1_t_max" in R else True)
        if "B1_t_max" in R:
            chk.add("B1 (reproduction): Newtonian continuation with the SMALLEST-root (continuity from the Newtonian regime) branch gives t_max within a factor 3 of the lane's 1.2e-6", abs(math.log(R["B1_t_max"]["N_xmax30_smallest_root"] / 1.2e-6)) < math.log(3), f"{R['B1_t_max']['N_xmax30_smallest_root']:.3e}")
            chk.add("B1 (reproduction): mirrored continuation t_max within a factor 2 of 4e-4", abs(math.log(R["B1_t_max"]["Mi_xmax30_largest_root"] / 4e-4)) < math.log(2), f"{R['B1_t_max']['Mi_xmax30_largest_root']:.3e}")
        # ---------------- B5 anchor and D1
        z = np.array([0.0, 1.0, 2.5, 5.0]); E = np.sqrt(C.OMEGA_M * (1 + z) ** 3 + C.OMEGA_L)
        R["B5_E_of_z"] = [float(v) for v in E]
        print("  B5/D1: a_*(z)/a_*(0) = E(z) for the K = 0 anchor:", [f"{v:.2f}" for v in E])
        chk.add("D1 numbers 1.79, 3.77, 8.29 (K = 0 anchor)", all(abs(E[i] - v) < 0.01 * v for i, v in ((1, 1.79), (2, 3.77), (3, 8.29))))
        tK0 = {f"z={zz}": float(T440 / T440 * e ** 2) for zz, e in zip(z, E)}
        tKb = {f"z={zz}": float(e ** 2 - 1) for zz, e in zip(z, E)}
        R["B5_t_of_z_anchor_K0_R440"] = tK0; R["B5_t_of_z_anchor_Kbg0_R440"] = tKb
        dev_z0_anchor_Kbg = maxdev(1e-12, "Mi")
        R["B5_dev_z0_anchor_Kbg"] = dev_z0_anchor_Kbg
        R["B5_dev_z0_anchor_K0_R440"] = maxdev(1.0, "Mi")
        print(f"  B5: anchor at K_bg(z=0): G1 at z=0 max dev {dev_z0_anchor_Kbg:.2e}; t(z) = E^2 - 1 = " + ", ".join(f"{v:.2f}" for v in tKb.values()) + " (G1 fails at z > 0); anchor at K = 0 (rule T, R = 440): t(0) = 1, G1 max dev " + f"{R['B5_dev_z0_anchor_K0_R440']:.3f}")
    # ------------------------------------------------------------ B6 and MUTATE
    bit = None; ok = None
    if m == "":
        tmax_mi = R["B1_t_max"]["Mi_xmax30_largest_root"]; tmax_n = R["B1_t_max"]["N_xmax30_largest_root"]
        und = R["B2_undressed"]["3.4e-5"]["t_min_actual_theta"]
        drs = max(R["B4_tmin_dressed"]["G6_pulsar"], R["B4_tmin_dressed"]["G7_y=1"])
        tmax_ns = R["B1_t_max"]["N_xmax30_smallest_root"]
        R["B6_smallest_root_N"] = {"gap_undressed": und / tmax_ns, "gap_dressed": drs / tmax_ns}
        print(f"  B6 with the Newtonian-continuation SMALLEST-root branch (t_max = {tmax_ns:.2e}): undressed gap {und/tmax_ns:.1e} (lane: 3e12), dressed gap {drs/tmax_ns:.1e}")
        R["B6"] = {"gap_undressed_Mi": und / tmax_mi, "gap_undressed_N": und / max(tmax_n, 1e-300), "gap_dressed_Mi": drs / tmax_mi, "gap_dressed_N": drs / max(tmax_n, 1e-300)}
        print(f"  B6 pincer status: t_max(G1) Mi {tmax_mi:.2e}, N {tmax_n:.2e}; undressed t_min {und:.2e} -> gaps {und/tmax_mi:.1e} (Mi), {und/max(tmax_n,1e-300):.1e} (N); dressed t_min {drs:.2e} -> gaps {drs/tmax_mi:.1e} (Mi), {drs/max(tmax_n,1e-300):.1e} (N)")
        print("  B6 wording rule (frozen): 'pincer' only if the gap is >= 1e3 under BOTH dressing readings ->", "PINCER" if min(R['B6'].values()) >= 1e3 else "NOT a pincer under both readings (conditional)")
    if m == "M5":
        dev_lane_anchor = maxdev(1.0, "Mi")           # rule-T anchor at R = 440.4: t(z=0) = 1
        dev_moved = maxdev(1e-12, "Mi")               # anchor at K_bg(z = 0): t = 0
        R["M5_dev_ruleT"] = dev_lane_anchor; R["M5_dev_anchor_moved"] = dev_moved
        bit = "G1(b) fails at z = 0"; ok = dev_moved <= 0.10
        print(f"  M5: G1(b) max dev at the rule-T anchor {dev_lane_anchor:.3f}; with the anchor moved to K_bg(z = 0): {dev_moved:.2e}")
    if m == "M6":
        und = R["B2_undressed"]["3.4e-5"]["t_min_actual_theta"]
        drs = max(R["B4_tmin_dressed"]["G6_pulsar"], R["B4_tmin_dressed"]["G7_y=1"])
        y_p_ = R["y_pulsar_hand"]
        pass_dressed_at_tie = all(alpha2(2 * qP2(y_p_), 2 * qP2(y_p_) / Rr) <= 1.6e-9 for Rr in (T301, T440))
        R["M6_t_min_undressed"] = und; R["M6_t_min_dressed"] = drs; R["M6_dressed_pulsar_alpha2_passes_at_tie"] = pass_dressed_at_tie
        bit = "the G6 x G7 region requires t >= 1e6 (the lane's 4e6)"; ok = drs < 1e6
        print(f"  M6: undressed t_min = {und:.2e}; with F-dressing t_min = {drs:.2e} (the alpha_2 line becomes a bound on R, not on the redundant bare c2). Dressed pulsar-row alpha_2 passes at the rule-T tie itself: {pass_dressed_at_tie} (representative y_p = {y_p_:.2e})")
    C.finish(__file__, chk, R, bit, ok)

if __name__ == "__main__":
    C.guarded(main)
