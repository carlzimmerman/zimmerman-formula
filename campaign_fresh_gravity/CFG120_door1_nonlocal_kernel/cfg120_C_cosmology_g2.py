#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG120 script C -- G2 (T2a cosmic sum rule, T2b acoustic driving and growth) and T3c (Bianchi/momentum non-conservation of the
minimal covariantisation), written to CFG120_FROZEN_CRITERIA.md (commit e8b9fbcdf).

SOLVER (declared in this header, as the frozen file requires): one simplified linear Einstein-fluid code, conformal Newtonian gauge,
phi = psi (no anisotropic stress), massless neutrinos as a perfect fluid (w = 1/3, N_eff = 3.046), photons a perfect fluid tightly
coupled to baryons (zeroth-order tight coupling, R = 3 rho_b/4 rho_gamma) until an INSTANT decoupling at z = 1090, after which baryons
are free pressureless and photons keep the perfect-fluid equations; CDM pressureless; flat, h = 0.6736, omega_b = 0.02237, omega_c = 0.1200,
T_cmb = 2.7255 K.  Adiabatic initial conditions at k tau = 1e-3.  The SAME code runs LCDM and the door, so its systematics cancel in the ratios.
DOOR (Reading P, minimal covariantisation of frozen section 5): there is NO cdm; the dark component D has background rho_D = K0 rho_b
(K0 = Omega_c/Omega_b = 5.36, so the background is LCDM's) and perturbations delta rho_D = rho_D s(k/a) delta_b, momentum (rho+p)theta_D = rho_D s(k/a) theta_b,
with s(k) = Khat(k)/Khat(0) of the kernel (physical k = k_comoving / a), no shear.
Kernels: (i) the T1g best-fit RM kernel (the frozen choice); (ii) the recalled RM set lambda0 = 3 kpc, mu0 = 0.1/kpc normalised to K0;
(iii) POST-HOC (not in the frozen file; cannot upgrade a verdict): s = 1 at all k, the most favourable case for the door.
PASS LINES (frozen): |delta_D/delta_c - 1| <= 0.05 and |Phi/Phi_LCDM - 1| <= 0.05 at z = 1100 for k in {0.01, 0.02, 0.05, 0.1, 0.3}/Mpc;
growth (delta_m ratio at z = 10) within 5 percent for k in {0.5, 2, 10, 30}/Mpc; T2a: G1's required interior dark mass at x = 30 (29.0 M) <= 1.05 * Omega_c/Omega_b;
T3c: |Q| / (rho_D k^2 phi) <= 0.05 at z = 1100, k = 0.1/Mpc.
MUTATE=c : the dark source is made CDM-like (delta_D from the CDM run): T2b and T3c claims must FAIL.  MUTATE=a,b,d: no bite here (declared).
Run: python3 cfg120_C_cosmology_g2.py    (MUTATE=c for the control)
"""
import os, sys, math, json
import numpy as np
import multiprocessing as mp
from scipy.integrate import solve_ivp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cfg120_common import *

R = Report("cfg120_C_cosmology_g2")
P, check = R.P, R.check
R.head(__doc__.split("Run: python3")[0])
if MUTATE in ("a", "b", "d"):
    P(f"\n  MUTATE={MUTATE}: no bite in script C (declared); main claims evaluated unchanged.")

# ---------------------------------------------------------------------------------------------- cosmology (Mpc units, c = 1)
h = 0.6736
wb, wc, Tcmb, Neff = 0.02237, 0.1200, 2.7255, 3.046
wg = 2.4728e-5 * (Tcmb / 2.7255) ** 4
wnu = wg * Neff * 7.0 / 8.0 * (4.0 / 11.0) ** (4.0 / 3.0)
H0 = h / 2997.92458
Ob, Oc, Og, On = wb / h ** 2, wc / h ** 2, wg / h ** 2, wnu / h ** 2
Or = Og + On
OL = 1.0 - Ob - Oc - Or
K0 = Oc / Ob
A_DEC = 1.0 / 1091.0
RB = 3 * wb / (4 * wg)                      # R = RB * a


def calH(a):
    return a * H0 * math.sqrt(Or / a ** 4 + (Ob + Oc) / a ** 3 + OL)


def g_i(Omega, a, w):
    return 1.5 * H0 ** 2 * Omega * a ** (-1.0 - 3.0 * w)


# kernels' shape s(k_phys) with k_phys in 1/kpc
def s_factory(kind):
    if kind == "const":
        return lambda kph: 1.0
    if kind == "fit":
        fit = json.load(open(os.path.join(HERE, "cfg120_rmfit_canonical.json")))["fit3"] if os.path.isfile(os.path.join(HERE, "cfg120_rmfit_canonical.json")) else fit_rm(A0, MASSES, None, None)
        kern = RM(fit["A"], fit["lam"], fit["mu"])
    elif kind == "recalled":
        kern = RM(1.0, 3.0, 0.1)
    K0hat = kern.total()
    return lambda kph: float(kern.Khat(kph) / K0hat)


def run(args):
    """integrate one wavenumber; returns dict of quantities at a(z=1100), a(z=10) and a = 0.05.
       phi is EVOLVED from the momentum (0i) constraint  phi' = -Hc phi + 4 pi G a^2 (rho+p) theta / k^2  (the 00 constraint has a
       catastrophic cancellation at k tau = 1e-3); the Poisson (00) constraint is evaluated as a DIAGNOSTIC 'poisson residual'."""
    k, mode, kind = args                       # mode 'lcdm' or 'door'; kind kernel shape for the door
    sf = s_factory(kind) if mode == "door" else None
    tau_i = 1e-3 / k
    a_i = tau_i * H0 * math.sqrt(Or)
    psi0 = 1.0
    a1100, a10 = 1.0 / 1101.0, 1.0 / 11.0
    lc = (mode == "lcdm")

    def sources(a, Hc, dg, tg, db, tb, dn, tn, dcs, tcs):
        """dsum = sum g_i delta_i, msum = sum g_i (1+w_i) theta_i (dark: CDM state, or s * baryon state for the door)"""
        gb, gg, gn, gc = g_i(Ob, a, 0.0), g_i(Og, a, 1 / 3), g_i(On, a, 1 / 3), g_i(Oc, a, 0.0)
        dsum = gb * db + gg * dg + gn * dn + gc * dcs
        msum = gb * tb + gg * (4 / 3) * tg + gn * (4 / 3) * tn + gc * tcs
        return dsum, msum

    # ---- phase 1: tightly coupled (theta_b = theta_gamma = th).  state: phi, dg, th, db, dn, tn, [dc, tc]
    def rhs1(lna, y):
        a = math.exp(lna)
        Hc = calH(a)
        if lc:
            phi, dg, th, db, dn, tn, dc, tc = y
            dcs, tcs = dc, tc
        else:
            phi, dg, th, db, dn, tn = y
            s = sf(k / a / 1000.0)
            dcs, tcs = s * db, s * th
        R_ = RB * a
        dsum, msum = sources(a, Hc, dg, th, db, th, dn, tn, dcs, tcs)
        dphi = -Hc * phi + msum / k ** 2
        out = [dphi, -(4 / 3) * th + 4 * dphi, (-Hc * R_ * th + k ** 2 * dg / 4) / (1 + R_) + k ** 2 * phi, -th + 3 * dphi,
               -(4 / 3) * tn + 4 * dphi, k ** 2 * dn / 4 + k ** 2 * phi]
        if lc:
            out += [-tc + 3 * dphi, -Hc * tc + k ** 2 * phi]
        return [v / Hc for v in out]

    d0r, d0m = -2 * psi0, -1.5 * psi0
    t0 = 0.5 * k ** 2 * tau_i * psi0
    y0 = [psi0, d0r, t0, d0m, d0r, t0] + ([d0m, t0] if lc else [])
    s1 = solve_ivp(rhs1, (math.log(a_i), math.log(A_DEC)), y0, method="DOP853", rtol=1e-9, atol=1e-13, dense_output=True)
    res = {}
    y = s1.sol(math.log(a1100))
    a = a1100
    Hc = calH(a)
    R_ = RB * a
    if lc:
        phi, dg, th, db, dn, tn, dc, tc = y
        dcs, tcs = dc, tc
        dD = dc
    else:
        phi, dg, th, db, dn, tn = y
        s = sf(k / a / 1000.0)
        dcs, tcs = s * db, s * th
        dD = s * db
    dsum, msum = sources(a, Hc, dg, th, db, th, dn, tn, dcs, tcs)
    phi_poisson = -(dsum + 3 * Hc * msum / k ** 2) / k ** 2
    Q = (Hc * th + k ** 2 * dg / 4) / (1 + R_)                  # theta_b' + Hc theta_b - k^2 phi  (tight-coupling identity)
    res.update(dD_1100=dD, phi_1100=phi, dg_1100=dg, db_1100=db, Qratio=abs(Q) / abs(k ** 2 * phi), poisson_res_1100=phi_poisson / phi - 1.0)
    # ---- phase 2: decoupled baryons.  state: phi, dg, tg, db, tb, dn, tn, [dc, tc]
    yend = s1.y[:, -1]
    if lc:
        phi, dg, th, db, dn, tn, dc, tc = yend
        z2 = [phi, dg, th, db, th, dn, tn, dc, tc]
    else:
        phi, dg, th, db, dn, tn = yend
        z2 = [phi, dg, th, db, th, dn, tn]

    def rhs2(lna, y):
        a = math.exp(lna)
        Hc = calH(a)
        if lc:
            phi, dg, tg, db, tb, dn, tn, dc, tc = y
            dcs, tcs = dc, tc
        else:
            phi, dg, tg, db, tb, dn, tn = y
            s = sf(k / a / 1000.0)
            dcs, tcs = s * db, s * tb
        dsum, msum = sources(a, Hc, dg, tg, db, tb, dn, tn, dcs, tcs)
        dphi = -Hc * phi + msum / k ** 2
        out = [dphi, -(4 / 3) * tg + 4 * dphi, k ** 2 * dg / 4 + k ** 2 * phi, -tb + 3 * dphi, -Hc * tb + k ** 2 * phi,
               -(4 / 3) * tn + 4 * dphi, k ** 2 * dn / 4 + k ** 2 * phi]
        if lc:
            out += [-tc + 3 * dphi, -Hc * tc + k ** 2 * phi]
        return [v / Hc for v in out]

    s2 = solve_ivp(rhs2, (math.log(A_DEC), math.log(a10)), z2, method="DOP853", rtol=1e-9, atol=1e-13, dense_output=True)
    for tag, aa in (("z10", a10), ("a0p05", 0.05)):
        yy = s2.sol(math.log(aa))
        if lc:
            db, dc = yy[3], yy[7]
            dm = (Ob * db + Oc * dc) / (Ob + Oc)
        else:
            db = yy[3]
            s = sf(k / aa / 1000.0)
            dm = (Ob * db + Oc * s * db) / (Ob + Oc)
        res["dm_" + tag] = dm
    # Poisson diagnostic at z = 10
    yy = s2.sol(math.log(a10))
    Hc = calH(a10)
    if lc:
        phi, dg, tg, db, tb, dn, tn, dc, tc = yy
        dcs, tcs = dc, tc
    else:
        phi, dg, tg, db, tb, dn, tn = yy
        s = sf(k / a10 / 1000.0)
        dcs, tcs = s * db, s * tb
    dsum, msum = sources(a10, Hc, dg, tg, db, tb, dn, tn, dcs, tcs)
    res["poisson_res_z10"] = (-(dsum + 3 * Hc * msum / k ** 2) / k ** 2) / phi - 1.0
    return res


def D_analytic(a):
    """LCDM linear growth factor D(a) = (5/2) Om H0^2 H(a) Int_0^a da'/(a' H(a'))^3 (radiation neglected in the integral, included in H)."""
    from scipy.integrate import quad
    Hf = lambda x: H0 * math.sqrt(Or / x ** 4 + (Ob + Oc) / x ** 3 + OL)
    I = quad(lambda x: 1.0 / (x * Hf(x)) ** 3, 1e-8, a, epsrel=1e-10)[0]
    return Hf(a) * I


if __name__ == "__main__":
    ctx = mp.get_context("fork")
    pool = ctx.Pool(12)
    P(f"\n  background: Omega_b={Ob:.5f} Omega_c={Oc:.5f} Omega_r={Or:.3e} Omega_L={OL:.5f}; K0 = Omega_c/Omega_b = {K0:.4f}; a_dec = 1/1091")
    KZ = [0.01, 0.02, 0.05, 0.1, 0.3]
    KG = [0.5, 2.0, 10.0, 30.0]
    KALL = KZ + KG
    # ==================================================================================================== T2a
    R.banner("T2a  cosmic sum rule: the dark mass G1 requires versus the background dark share")
    req = math.sqrt(1 + 30.0 ** 2) - 1
    xcap = math.sqrt((1 + K0) ** 2 - 1)
    P(f"  G1 requires M_D(<30 r_M)/M = sqrt(901) - 1 = {req:.3f}; background K0 = Omega_c/Omega_b = {K0:.3f}; x_cap where the point-mass target exhausts K0: {xcap:.3f} (CFG44: 6.29)")
    fit = json.load(open(os.path.join(HERE, "cfg120_rmfit_canonical.json")))["fit3"] if os.path.isfile(os.path.join(HERE, "cfg120_rmfit_canonical.json")) else fit_rm(A0, MASSES, None, None)
    tot_fit = RM(fit["A"], fit["lam"], fit["mu"]).total()
    tot_rec = RM(1.0, 3.0, 0.1).total()
    P(f"  total integral of the kernels (M_D,total/M_b): T1g best fit {tot_fit:.4g}; recalled RM(1,3,0.1) {tot_rec:.4g}; required by G1 >= {req:.3f}; allowed {K0:.3f}")
    ok_sum = req <= 1.05 * K0
    check("T2a the cosmic sum rule FAILS: the interior dark mass G1 needs (29.0 M) exceeds the background dark share (5.36 M) by a factor 5.4", f"{req:.3f} vs {K0:.3f}: ratio {req / K0:.3f}", not ok_sum)
    R.gate("G2/T2a (sum rule)", "FAIL" if not ok_sum else "PASS", f"required {req:.2f} M vs allowed {K0:.2f} M (x_cap = {xcap:.2f})")

    # ==================================================================================================== solver control
    R.banner("Solver control (LCDM): late-time sub-horizon growth against the analytic growth factor")
    ctl_jobs = [(0.5, "lcdm", None)]
    lc = {k: None for k in KALL}
    jobs = [(k, "lcdm", None) for k in KALL]
    outs_l = pool.map(run, jobs)
    lcdm = dict(zip(KALL, outs_l))
    r_num = lcdm[0.5]["dm_z10"] / lcdm[0.5]["dm_a0p05"]
    r_ana = D_analytic(1.0 / 11.0) / D_analytic(0.05)
    check("C.ctl LCDM solver: delta_m(z=10)/delta_m(a=0.05) at k = 0.5/Mpc equals the analytic ratio D(0.0909)/D(0.05)", f"numeric {r_num:.5f}, analytic {r_ana:.5f}, rel diff {abs(r_num / r_ana - 1):.2e} (line 2e-2)", abs(r_num / r_ana - 1) < 2e-2)

    # ==================================================================================================== T2b
    R.banner("T2b  acoustic driving at z = 1100 and growth at z = 10, door versus LCDM (same code)")
    kinds = [("fit", "(i) T1g best-fit RM shape (frozen choice)"), ("recalled", "(ii) recalled RM(1,3,0.1) shape"), ("const", "(iii) POST-HOC: s = 1 at all k (most favourable)")]
    door = {}
    for kind, lab in kinds:
        if MUTATE == "c":
            door[kind] = lcdm            # dark source made CDM-like: the door IS the CDM run
        else:
            door[kind] = dict(zip(KALL, pool.map(run, [(k, "door", kind) for k in KALL])))
    summary = {}
    sane = {k: (abs(lcdm[k]["poisson_res_1100"]) < 0.05 and lcdm[k]["dD_1100"] * lcdm[k]["dm_z10"] > 0) for k in KALL}
    P("\n  SOLVER SANITY (diagnostic added after the first look at the numbers; it does not change any pass line): the LCDM reference is treated as sane at a k only if its Poisson (00) residual at z = 1100 is < 5 percent AND delta_c keeps its sign between z = 1100 and z = 10. This solver has NO Silk damping (photons are a perfect fluid), so baryons keep full acoustic velocities at decoupling and run away at high k.")
    P("  LCDM reference sane at k = " + ", ".join(f"{k:g}: {'yes' if sane[k] else 'NO'} (Poisson res {lcdm[k]['poisson_res_1100']:+.3f}, sign {'kept' if lcdm[k]['dD_1100'] * lcdm[k]['dm_z10'] > 0 else 'FLIPPED'})" for k in KALL))
    for kind, lab in kinds:
        P(f"\n  {lab}")
        P("    (all entries are RATIOS door/LCDM; the line is |ratio - 1| <= 0.05)")
        P("    k[/Mpc] | delta_D/delta_c (z=1100) | Phi/Phi_LCDM (z=1100) | delta_m ratio at z=10 | (delta_b, delta_gamma at 1100 in the door run) | door Poisson residual (z=1100)")
        bad = []
        for k in KALL:
            d, l = door[kind][k], lcdm[k]
            rD = d["dD_1100"] / l["dD_1100"]
            rP = d["phi_1100"] / l["phi_1100"]
            rG = d["dm_z10"] / l["dm_z10"]
            if k in KZ:
                fail = abs(rD - 1) > 0.05 or abs(rP - 1) > 0.05
            else:
                fail = abs(rG - 1) > 0.05
            if fail:
                bad.append(k)
            P(f"    {k:6g}  | {rD:+.4f}               | {rP:+.4f}              | {rG:+.4f}              | ({d['db_1100']:+.3f}, {d['dg_1100']:+.3f}) | {d['poisson_res_1100']:+.3f}  {'FAIL' if fail else 'ok'}{'' if sane[k] else '  [LCDM reference not sane at this k: entry not evidential]'}")
        summary[kind] = dict(failing_k=bad, failing_k_sane_reference=[k for k in bad if sane[k]], rows={str(k): dict(rD=door[kind][k]["dD_1100"] / lcdm[k]["dD_1100"], rPhi=door[kind][k]["phi_1100"] / lcdm[k]["phi_1100"],
                                                               rGrowth=door[kind][k]["dm_z10"] / lcdm[k]["dm_z10"]) for k in KALL})
        P(f"    k values outside the 5 percent line: {bad if bad else 'none'};  of these, k with a sane LCDM reference: {[k for k in bad if sane[k]]}")
    R.num("T2b", summary)
    fit_bad = summary["fit"]["failing_k"]
    kinds_pass = [kd for kd, _ in kinds if not summary[kd]["failing_k"]]
    check("T2b (frozen expectation) the baryon-sourced phantom fails the acoustic-driving/growth lines for the frozen kernel (i) and for (ii), (iii)", f"failing k: (i) {summary['fit']['failing_k']}; (ii) {summary['recalled']['failing_k']}; (iii) {summary['const']['failing_k']}; kernels that pass everywhere: {kinds_pass if kinds_pass else 'none'}", not kinds_pass)
    R.gate("G2/T2b (acoustic driving, growth)", "FAIL" if not kinds_pass else "PASS(some)", f"failing k for the frozen kernel (i): {summary['fit']['failing_k']}; (ii): {summary['recalled']['failing_k']}; (iii, post-hoc favourable): {summary['const']['failing_k']}. With a sane LCDM reference only: (i) {summary['fit']['failing_k_sane_reference']}; (ii) {summary['recalled']['failing_k_sane_reference']}; (iii) {summary['const']['failing_k_sane_reference']}")

    # ==================================================================================================== T3c
    R.banner("T3c  Bianchi / momentum non-conservation of the minimal covariantisation: |Q|/(rho_D k^2 phi), Q = theta_b' + H theta_b - k^2 phi, at z = 1100")
    if MUTATE == "c":
        P("  MUTATE=c: dark source is geodesic CDM dust, Q = 0 by construction")
    qv = {k: (0.0 if MUTATE == "c" else door["fit"][k]["Qratio"]) for k in KZ}   # from the door run with the frozen kernel (i)
    P("  (kernels (ii), (iii) give: " + "; ".join(f"{kd}: " + ", ".join(f"{k:g}: {door[kd][k]['Qratio']:.3f}" for k in KZ) for kd in ("recalled", "const")) + ")")
    for k in KZ:
        P(f"    k = {k:g}/Mpc: |Q| / (k^2 |phi|) = {qv[k]:.4f}")
    q01 = qv[0.1]
    check("T3c (frozen expectation) the non-gravitational force on the photon-coupled baryons (Bianchi violation of a phantom slaved to them) exceeds the 0.05 line at k = 0.1/Mpc, z = 1100", f"{q01:.4f} (pass line <= 0.05)", q01 > 0.05)
    R.gate("G3/T3c (Bianchi consistency in cosmology)", "FAIL" if q01 > 0.05 else "PASS", f"|Q|/(k^2 phi) = {q01:.3f} at k = 0.1/Mpc, z = 1100 (line 0.05); values at other k: " + ", ".join(f"{k:g}: {qv[k]:.2f}" for k in KZ))
    nf = R.write()
    sys.exit(1 if nf else 0)
