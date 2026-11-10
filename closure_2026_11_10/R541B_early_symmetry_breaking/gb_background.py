"""R541B GB1, GB2, GB4, GB5 + KA2-KA6 + MU1-MU4 (criteria: FROZEN_CRITERIA.md).
Units as in r541b_core.py (H0 = 1, densities in rho_c0). Prints to gb_background.out (run: python3 gb_background.py)."""
import os, sys, math, warnings
import numpy as np
warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from r541b_core import cosmo, m_of_mu, Pot, run, t_rad, OMEGA_R, OMD, h

import builtins
_OUT = None


def print(*a, **k):   # results go to gb_background_<part>.out, apart from the integrator's Fortran warnings on stdout
    builtins.print(*a, **k, file=_OUT, flush=True)


PASSFAIL = lambda ok: "PASS" if ok else "FAIL"
MU_PRIMARY = {"Jeans 2.512e4/Mpc": 2.512e4, "BBN 8.89e6/Mpc": 8.89e6}
Z_BBN = 4.26e9
N_STEP = 0.02   # max step in ln a inside the switch region


def segs_for(zs, width=6.0):
    Ns = -np.log(1 + zs)
    return [(Ns - width, Ns + width, N_STEP)]


def a_ini_for(zs):
    return min(1e-3 / (1 + zs), 1e-12)


def R_of(sol, cp):
    return sol.Cfin() / cp["Ob"]


def solve_V0(kind, ts, zs, cp, m, target, kw=None, C_i=0.0, tau_off=0.0):
    """secant in ln V0 on ln R; returns V0, sol, R. Starts from the Q ~ 1 estimate."""
    kw = kw or {}
    a_s = 1 / (1 + zs)
    lv = math.log(target * cp["Ob"] / (1.3 * a_s**3))
    seg = segs_for(zs); ai = a_ini_for(zs)
    def f(lv):
        s = run(Pot(kind, math.exp(lv), ts, **kw), cp, m, a_ini=ai, C_i=C_i, tau_off=tau_off, segs=seg)
        R = R_of(s, cp)
        return (math.log(R) - math.log(target)) if R > 0 else -50.0, s, R
    f0, s0, R0 = f(lv); lv1 = lv + 0.5; f1, s1, R1 = f(lv1)
    for _ in range(25):
        if abs(f1) < 1e-7:
            break
        slope = (f1 - f0) / (lv1 - lv) if lv1 != lv else 1.0
        if not np.isfinite(slope) or abs(slope) < 1e-3:
            slope = 0.5
        step = -f1 / slope
        step = max(min(step, 5.0), -5.0)
        lv, f0 = lv1, f1
        lv1 = lv1 + step
        f1, s1, R1 = f(lv1)
    return math.exp(lv1), s1, R1, f1


def diagnostics(sol, cp, zs):
    out = {}
    out["z50"] = sol.z_of_frac(0.5); out["z99"] = sol.z_of_frac(0.99)
    Cf = sol.Cfin()
    # GB2b: clock-sector w at z <= 3400
    wmax = 0.0
    for z in np.geomspace(3400, 1e-3, 120):
        st = sol.state(1 / (1 + z))
        w = (st["pK"] - st["V"]) / (st["rhoK"] + st["V"])
        wmax = max(wmax, abs(w))
    out["wmax_z3400"] = wmax
    # GB2c BBN
    aB = 1 / (1 + Z_BBN)
    if aB >= np.exp(sol.Nmin):
        st = sol.state(aB)
        out["bbn"] = (st["rhoK"] + st["V"]) / (cp["Or"] / aB**4)
    else:
        out["bbn"] = float("nan")
    # GB5
    C3000 = sol.C(1 / 3001.0)
    out["dC_after3000"] = (Cf - C3000) / Cf
    st0 = sol.state(1.0)
    out["rate_today"] = abs(st0["dV"]) / Cf          # |dlnC/dt| in H0 (a = 1)
    rDE = cp["OL"]
    out["V_over_DE_z5"] = max(abs(sol.state(1 / (1 + z))["V"]) / rDE for z in np.linspace(0, 5, 26))
    # V's energy relative to radiation at switch-off and max over history before it
    as_ = 1 / (1 + zs)
    st = sol.state(as_)
    out["V_over_rad_at_switch"] = st["V"] / (cp["Or"] / as_**4)
    out["Qmax_minus1"] = max(sol.state(a)["x"] for a in np.geomspace(np.exp(sol.Nmin) * 1.01, 1, 300))
    return out


def gb2a(d):
    if d["z50"] <= 1e4:
        return "EXCLUDED"
    return "PASS" if d["z99"] >= 1e5 else "undecided"


def main(part):
    print("R541B gb_background: action (A) - V(tau), P = 0; H0 = 1, densities in rho_c0")
    print(f"Omega_r = {OMEGA_R:.4e}, Omega_d(target) = {OMD:.5f}, h = {h}")
    cpc = cosmo("canonical")
    mJ = m_of_mu(2.512e4); mB = m_of_mu(8.89e6)
    print(f"m = mu_K c / H0: Jeans line {mJ:.4e}, BBN line {mB:.4e}")

    # ---------------- known answers ----------------
    if part == "ka":
        print("\n== Known answers ==")
        for Ci in (1.0, 5.41):
            s = run(Pot("zero", 0, 1), cpc, mB, a_ini=1e-4, C_i=Ci * cpc["Ob"])
            r = s.Cfin() / (Ci * cpc["Ob"]) - 1
            print(f"KA2 V = 0, C_i/rho_b0 = {Ci}: C(1)/C_i - 1 = {r:.2e}  {PASSFAIL(abs(r) <= 1e-8)}")
        rad = dict(Ob=0.0, Or=OMEGA_R, OL=0.0, R=1.0); mbig = 1e16
        zs = 1e6; a_s = 1 / (1 + zs); ts = t_rad(a_s, rad)
        # KA3 sharp step (tanh with D = 1e-4 ts), pure radiation, Q ~ 1
        V0 = 1e17
        s = run(Pot("tanh", V0, ts, D=1e-4 * ts), rad, mbig, a_ini=1e-12,
                segs=[(np.log(a_s) - 0.01, np.log(a_s) + 0.01, 2e-6)])
        r = s.Cfin() / (V0 * a_s**3) - 1
        print(f"KA3 sharp step, radiation, z_s 1e6: C / (V0 a_s^3) - 1 = {r:.2e}  {PASSFAIL(abs(r) <= 1e-3)}")
        s = run(Pot("exp", V0, ts), rad, mbig, a_ini=1e-12, segs=segs_for(zs))
        r = s.Cfin() / (math.gamma(2.5) * V0 * a_s**3) - 1
        print(f"KA4 exponential, radiation: C / (Gamma(5/2) V0 a(ts)^3) - 1 = {r:.2e}  {PASSFAIL(abs(r) <= 1e-3)}")
        # KA5 energy conservation of the clock + V sector along the Jeans-line exponential solution, z_s 3e5
        zs5 = 3e5; ts5 = t_rad(1 / (1 + zs5), cpc)
        s5 = run(Pot("exp", 1e16, ts5), cpc, mJ, a_ini=1e-12, segs=segs_for(zs5))
        res = []
        for N in np.linspace(np.log(1 / (1 + zs5)) - 2, np.log(1 / (1 + zs5)) + 2, 41):
            e = 1e-5
            def E(Nx):
                st = s5.state(np.exp(Nx)); return np.exp(3 * Nx) * (st["rhoK"] + st["V"])
            st = s5.state(np.exp(N))
            lhs = (E(N + e) - E(N - e)) / (2 * e) + (st["pK"] - st["V"]) * 3 * np.exp(3 * N)
            res.append(abs(lhs) / (np.exp(3 * N) * (st["rhoK"] + st["V"])))
        print(f"KA5 d(a^3 rho)/dN + p d(a^3)/dN, max relative residual = {max(res):.2e}  {PASSFAIL(max(res) <= 1e-6)}")
        s6 = run(Pot("zero", 0, 1), rad, mJ, a_ini=1e-14)
        r = s6.state(1e-8)["tau"] / t_rad(1e-8, rad) - 1
        print(f"KA6 radiation clock: tau(a=1e-8) / (1/(2H)) - 1 = {r:.2e}  {PASSFAIL(abs(r) <= 1e-3)}")

    if part == "a":
        # ---------------- GB1 + GB2 + GB5, family (a) exponential ----------------
        for foot in ("canonical", "alt"):
            cp = cosmo(foot); target = cp["R"]
            print(f"\n== Family (a) V0 exp(-tau/tau_s), footing {foot}, target R = {target} ==")
            print("mu_K line | z_s (tau_s = t(z_s)) | V0 [rho_c0] | V0/rho_rad(a_s) | dlnR/dlnV0 | dlnR/dlntau_s | "
                  "z50 | z99 | GB2a | max|w| z<=3400 | BBN (rho_K+V)/rho_rad | Qmax-1 | dC/C after z3000 | GB5")
            zgrid = (1e4, 1e5, 3e5, 1e6, 1e8) if foot == "canonical" else (1e5, 1e6)
            for lab, mu in MU_PRIMARY.items():
                m = m_of_mu(mu)
                for zs in zgrid:
                    ts = t_rad(1 / (1 + zs), cp)
                    V0, s, R, f = solve_V0("exp", ts, zs, cp, m, target)
                    if abs(f) > 1e-5:
                        print(f"{lab} | {zs:.0e} | no solution reached (R = {R:.3e} at V0 {V0:.3e})"); continue
                    seg = segs_for(zs); ai = a_ini_for(zs)
                    Rp = R_of(run(Pot("exp", V0 * 1.01, ts), cp, m, a_ini=ai, segs=seg), cp)
                    Rt = R_of(run(Pot("exp", V0, ts * 1.01), cp, m, a_ini=ai, segs=seg), cp)
                    dV = math.log(Rp / R) / math.log(1.01); dt = math.log(Rt / R) / math.log(1.01)
                    d = diagnostics(s, cp, zs)
                    g5 = d["dC_after3000"] <= 1e-2 and d["rate_today"] <= 1e-2 and d["V_over_DE_z5"] <= 0.02
                    print(f"{lab} | {zs:.0e} | {V0:.4e} | {d['V_over_rad_at_switch']:.3e} | {dV:.4f} | {dt:.4f} | "
                          f"{d['z50']:.3e} | {d['z99']:.3e} | {gb2a(d)} | {d['wmax_z3400']:.2e} | {d['bbn']:.2e} | "
                          f"{d['Qmax_minus1']:.2e} | {d['dC_after3000']:.1e} | {PASSFAIL(g5)}")
                    if foot == "canonical" and zs == 1e6:
                        # attractor: response to C_i and tau_i
                        ai2 = 0.1 / (1 + zs)   # start late enough that C_i does not make Q astronomically large
                        Rb = R_of(run(Pot("exp", V0, ts), cp, m, a_ini=ai2, segs=seg), cp)
                        for Ci in (1.0, 5.41):
                            Rc = R_of(run(Pot("exp", V0, ts), cp, m, a_ini=ai2, C_i=Ci * cp["Ob"], segs=seg), cp)
                            print(f"    attractor C_i/rho_b0 = {Ci} (start a = 0.1 a_s; baseline from there R = {Rb:.4f}): "
                                  f"R = {Rc:.4f} (Delta R = {Rc - Rb:+.4f}; generated part {Rc - Ci:.4f})")
                        for off in (-0.1, 0.1):
                            Ro = R_of(run(Pot("exp", V0, ts), cp, m, a_ini=ai, tau_off=off * ts, segs=seg), cp)
                            print(f"    attractor tau_i/tau_s = {off:+.1f}: R = {Ro:.4f} (Delta R = {Ro - R:+.4f})")

    cp = cpc; target = cp["R"]
    if part == "b":
        # ---------------- families (b), (c) ----------------
        cp = cpc; target = cp["R"]
        print("\n== Family (b) smooth step (V0/2)[1 - tanh((tau - tau_s)/Delta)], canonical ==")
        print("mu_K line | z_s | Delta/tau_s | V0 | V0 a_s^3/rho_b0 (step estimate) | dlnR/dlnV0 | dlnR/dlnDelta | z50 | z99 | "
              "GB2a | max|w| | BBN | GB5 dC/C")
        for lab, mu in MU_PRIMARY.items():
            m = m_of_mu(mu)
            for zs in (1e5, 1e6):
                ts = t_rad(1 / (1 + zs), cp)
                for Dr in (0.01, 0.1, 0.3):
                    kw = dict(D=Dr * ts)
                    V0, s, R, f = solve_V0("tanh", ts, zs, cp, m, target, kw)
                    if abs(f) > 1e-5:
                        print(f"{lab} | {zs:.0e} | {Dr} | no solution (R {R:.3e})"); continue
                    seg = segs_for(zs); ai = a_ini_for(zs)
                    Rp = R_of(run(Pot("tanh", V0 * 1.01, ts, **kw), cp, m, a_ini=ai, segs=seg), cp)
                    RD = R_of(run(Pot("tanh", V0, ts, D=Dr * ts * 1.01), cp, m, a_ini=ai, segs=seg), cp)
                    d = diagnostics(s, cp, zs)
                    est = V0 * (1 / (1 + zs))**3 / cp["Ob"]
                    print(f"{lab} | {zs:.0e} | {Dr} | {V0:.4e} | {est:.4f} | {math.log(Rp/R)/math.log(1.01):.4f} | "
                          f"{math.log(RD/R)/math.log(1.01):+.4f} | {d['z50']:.3e} | {d['z99']:.3e} | {gb2a(d)} | "
                          f"{d['wmax_z3400']:.2e} | {d['bbn']:.2e} | {d['dC_after3000']:.1e}")

    if part == "c":
        print("\n== Family (c) decaying power law V0 (1 + tau/tau_s)^-n, canonical, tau_s = t(z 1e6) ==")
        print("mu_K line | n | V0 | dlnR/dlnV0 | dlnR/dlnn | z50 | z99 | GB2a | max|w| z<=3400 | dC/C after z3000 | "
              "|dlnC/dt| today [H0] | max V/rho_DE z<=5 | GB5")
        for lab, mu in MU_PRIMARY.items():
            m = m_of_mu(mu)
            zs = 1e6; ts = t_rad(1 / (1 + zs), cp)
            for n in (1, 1.5, 2, 3, 4):
                kw = dict(n=n)
                V0, s, R, f = solve_V0("power", ts, zs, cp, m, target, kw)
                seg = [(-np.log(1 + zs) - 6, 0.0, N_STEP)]; ai = a_ini_for(zs)
                if abs(f) > 1e-5:
                    print(f"{lab} | {n} | no solution (R {R:.3e})"); continue
                Rp = R_of(run(Pot("power", V0 * 1.01, ts, **kw), cp, m, a_ini=ai, segs=seg), cp)
                Rn = R_of(run(Pot("power", V0, ts, n=n * 1.01), cp, m, a_ini=ai, segs=seg), cp)
                d = diagnostics(s, cp, zs)
                g5 = d["dC_after3000"] <= 1e-2 and d["rate_today"] <= 1e-2 and d["V_over_DE_z5"] <= 0.02
                print(f"{lab} | {n} | {V0:.4e} | {math.log(Rp/R)/math.log(1.01):.4f} | {math.log(Rn/R)/math.log(1.01):+.3f} | "
                      f"{d['z50']:.3e} | {d['z99']:.3e} | {gb2a(d)} | {d['wmax_z3400']:.2e} | {d['dC_after3000']:.2e} | "
                      f"{d['rate_today']:.2e} | {d['V_over_DE_z5']:.2e} | {PASSFAIL(g5)}")

    if part == "mu":
        # ---------------- mutations ----------------
        print("\n== Mutations ==")
        m = mB; zs = 1e6; ts = t_rad(1 / (1 + zs), cp); seg = segs_for(zs)
        V0, s, R, f = solve_V0("exp", ts, zs, cp, m, target)
        # MU1 sign flip
        sm = run(Pot("rising", V0, ts), cp, m, a_ini=1e-12, segs=seg)
        Qmin = min(sm.state(a)["Q"] for a in np.geomspace(1.1e-12, 1, 300))
        print(f"MU1 V rising in tau (same |V0|, tau_s): R = {R_of(sm, cp):+.4f}, min Q = {Qmin:.6f} -> "
              f"{'bites (negative charge, no dust)' if R_of(sm, cp) < 0 else 'DOES NOT BITE'}")
        mm = 1e30  # push: needed |C| at Jeans line
        try:
            smJ = run(Pot("rising", V0, ts), cp, mJ, a_ini=1e-12, segs=seg)
            QminJ = min(smJ.state(a)["Q"] for a in np.geomspace(1.1e-12, 1, 300))
            print(f"    same at the Jeans line: min Q = {QminJ:.4f} (Q -> 0 would end the foliation)")
        except Exception as e:
            print(f"    same at the Jeans line: the integration breaks down ({str(e)[:60]}): the negative charge "
                  f"drives Q = 1 + 1.5 C/(m^2 a^3) through 0, where the clock's foliation ends")
        # MU2 late switch-off
        zl = 1e3; tl = t_rad(1 / (1 + zl), cp)
        V2, s2, R2, f2 = solve_V0("exp", tl, zl, cp, m, target)
        d2 = diagnostics(s2, cp, zl)
        print(f"MU2 switch at z 1e3 (tau_s = t_rad(z 1e3), {tl:.3e}/H0): R = {R2:.4f}, z50 = {d2['z50']:.3e} -> GB2a "
              f"{gb2a(d2)} ({'bites' if gb2a(d2) == 'EXCLUDED' else 'DOES NOT BITE'})")
        # MU3 omega_b x 2 at fixed V
        cp2 = cosmo("canonical", omb_scale=2.0)
        s3 = run(Pot("exp", V0, ts), cp2, m, a_ini=1e-12, segs=seg)
        R3 = R_of(s3, cp2)
        print(f"MU3 omega_b x 2 at fixed V: R = {R3:.4f} vs {R:.4f} (ratio {R3/R:.4f}) -> GB4 "
              f"{'UNTIED (R ~ 1/omega_b)' if abs(R3 / R - 0.5) < 0.02 else 'TIED?'}")
        # MU4 power law n = 1
        V4, s4, R4, f4 = solve_V0("power", ts, zs, cp, m, target, dict(n=1))
        d4 = diagnostics(s4, cp, zs)
        print(f"MU4 power law n = 1: dC/C after z 3000 = {d4['dC_after3000']:.3e} -> GB5 "
              f"{'FAIL (bites)' if d4['dC_after3000'] > 1e-2 else 'PASS (DOES NOT BITE)'}")


if __name__ == "__main__":
    _OUT = open(os.path.join(HERE, f"gb_background_{sys.argv[1]}.out"), "w")
    main(sys.argv[1])
