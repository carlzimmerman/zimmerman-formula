#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
C_cosmology_growth -- CFG121 G2 tests C1-C3, exactly as frozen (sub-horizon Newtonian; 1D plane-symmetric periodic box).

PERTURBATION EQUATIONS (committed with the first output, before the solver was first run).  Units H0 = 1, length Mpc, density in units of
rho_crit0 (so 4 pi G rho_crit0 = 1.5), acceleration in H0^2 Mpc.  a0 = 9.3603e-11 m/s^2 = 636.5 in these units (canonical).  Flat LCDM+radiation
background: H^2 = Om a^-3 + Or a^-4 + OL, Om = Oc + Ob (Oc h^2 = 0.12, Ob h^2 = 0.0224, h = 0.6736).
Sheets s = b (baryons), D (medium), Lagrangian coordinate q, comoving position x_s = q + psi_s(q,t):
    psi_s'' + 2 H psi_s' = g_s(x_s)/a                         (planar Newtonian dynamics in comoving coordinates)
    g_N,tot(x) = -1.5 Om a^-2 [ (Ob/Om) A_b(x) + (Oc/Om) A_D(x) - x ] + const,   A_s(x) = (L/N) * #{sheets of species s to the left of x}   (exact 1D Poisson)
Polarisation (declared action, section 2 of the frozen file): dipole displacement xi (physical length, carried by the medium sheet), Pi = Q rho_D xi,
P = 4 pi G Pi = 1.5 Oc Q a^-3 xi/(1 + d psi_D/dq)   (acceleration units; rho_D = rho_bar_D/(1+psi_D')).  Bound charge -div Pi.
  Dipole EOM (a bound internal degree of freedom is NOT stretched by the Hubble flow; in terms of Pi = Q rho_D xi the expansion 'friction' of the
  frozen text is the -3H from rho_D ~ a^-3 and is already inside this xi form):
      xi'' = (Q/kappa_I) ( g_pol - Gfun(P) )
      V_U : g_pol = total field = g_N,tot + P - <P>       Gfun_U(P) = sgn(P) [ P^2/(a0 - 2|P|) + |P| ]   (law P2; equilibrium P = h(g_N) = sqrt(g_N^2 + a0 g_N) - g_N)
            medium sheets and baryons both feel g_N,tot + P - <P>  (universal coupling; in 1D the field of the bound charge is exactly 4 pi G Pi)
      V_B : g_pol = g_b = baryon-only Newtonian field   Gfun_B(P) = sgn(P) P^2/(a0 - 2|P|)
            baryons feel g_N,tot + P - <P> (the multiplier reaction: the bound charge's field), the medium sheets feel g_N,tot only
Reference (LCDM): the same solver with Q = 0.  Growth ratio at z = 10 is psi-amplitude(model)/psi-amplitude(reference), for baryons, medium and total matter.
Initial amplitude: delta = A cos(k q) at z_i = 100 (declared reading of 'A times the LCDM linear delta at z = 100'), growing-mode velocities
(Meszaros f = 1.5 y/(1 + 1.5 y), y = a Om/Or).  Dipole initial conditions: 'cold' (xi = 0) and 'eq' (adiabatic equilibrium start), gating on the worst.
Sheets terminate (COLLAPSED) if any 1 + psi' < 0.2 (delta >= 4) before z = 10.
MUTATE=Q10 : Q_central = 10 (the frozen control); P_star still read from the main B run.
"""
import math, sys, json, os, time
import numpy as np
import cfg121_common as C
from cfg121_common import MUTATE, HERE
from scipy.integrate import solve_ivp

R = C.Report("C_cosmology_growth")
_DEADLINE = [0.0]
TMAX = float(os.environ.get("TMAX", "90"))
QSCALE = 10.0 if MUTATE == "Q10" else 1.0
OC, OB, HH = 0.1200 / 0.6736 ** 2, 0.0224 / 0.6736 ** 2, 0.6736
OM = OC + OB
OR = 4.15e-5 / HH ** 2
OL = 1.0 - OM - OR
H0_S = 67.36e3 / 3.0857e22
A0C = C.A0_SIV / (H0_S ** 2 * 3.0857e22)
NSH = int(os.environ.get("NSH", "512"))
AMPS = [1e-4, 1e-3, 1e-2]
KS = [0.5, 2.0, 10.0, 30.0]                  # per Mpc (comoving)
R.banner(f"CFG121 C  (footing {C.FOOT}, a0 = {A0C:.2f} in H0^2 Mpc; N = {NSH}; MUTATE='{MUTATE}')")


def Hof(a):
    return math.sqrt(OM * a ** -3 + OR * a ** -4 + OL)


def gfun(P, variant):
    aP = np.abs(P)
    aPc = np.minimum(aP, 0.45 * A0C)
    core = aPc ** 2 / (A0C - 2 * aPc)
    slope = (2 * 0.45 * A0C * (A0C - 0.9 * A0C) + 2 * (0.45 * A0C) ** 2) / (A0C - 0.9 * A0C) ** 2          # d/dP of P^2/(a0-2P) at the clip
    core = core + np.where(aP > aPc, slope * (aP - aPc), 0.0)
    if variant == "V_U":
        core = core + aP
    return np.sign(P) * core


def hfun_acc(g):
    """equilibrium polarisation P(g_N) = sqrt(g^2 + a0 g) - g (P2) in acceleration units, signed like g."""
    ag = np.abs(g)
    return np.sign(g) * (np.sqrt(ag ** 2 + A0C * ag) - ag)


def make_rhs(k, variant, Q, kapI):
    L = 2 * math.pi / k
    N = NSH
    dq = L / N
    q = (np.arange(N) + 0.5) * dq
    qe = np.concatenate([q - L, q, q + L])
    fb, fD = OB / OM, OC / OM

    def interpA(x, xs):
        xe = np.concatenate([xs - L, xs, xs + L])
        return np.interp(x, xe, qe)

    def fields(psi_b, psi_D, a):
        xb, xD = q + psi_b, q + psi_D
        pref = -1.5 * OM * a ** -2
        Sb = fb * q + fD * interpA(xb, xD)
        SD = fb * interpA(xD, xb) + fD * q
        gb_raw = pref * (Sb - xb)
        gD_raw = pref * (SD - xD)
        Cc = -(fb * gb_raw.mean() + fD * gD_raw.mean())
        g_b, g_D = gb_raw + Cc, gD_raw + Cc
        return xb, xD, g_b, g_D

    def rhs(tau, y):
        if _DEADLINE[0] and time.time() > _DEADLINE[0]:
            raise TimeoutError
        a = math.exp(tau)
        H = Hof(a)
        psi_b, psi_D, u_b, u_D, xi, xid = np.split(y, 6)
        xb, xD, gNb, gND = fields(psi_b, psi_D, a)
        dpsiD = (np.roll(psi_D, -1) - np.roll(psi_D, 1)) / (2 * dq)
        P = 1.5 * OC * Q * a ** -3 * xi / (1.0 + dpsiD)
        Pm = P.mean()
        PeD = np.interp(xD, np.concatenate([xD - L, xD, xD + L]), np.tile(P, 3)) - Pm if Q != 0 else 0.0 * xD
        Peb = np.interp(xb, np.concatenate([xD - L, xD, xD + L]), np.tile(P, 3)) - Pm if Q != 0 else 0.0 * xb
        if variant == "V_U":
            g_pol = gND + PeD
            gtot_b, gtot_D = gNb + Peb, gND + PeD
        else:
            # baryon-only Newtonian field at the medium sheets
            pref = -1.5 * OB * a ** -2
            xbe = np.concatenate([xb - L, xb, xb + L])
            Ab_D = np.interp(xD, xbe, qe)
            gbo_D = pref * (Ab_D - xD)
            gbo_b = pref * (q - xb)
            gbo_D = gbo_D - gbo_b.mean()
            g_pol = gbo_D
            gtot_b, gtot_D = gNb + Peb, gND
        if Q == 0:
            xidd = 0.0 * xi
        else:
            xidd = (Q / kapI) * (g_pol - gfun(P, variant))
        dy = np.concatenate([u_b / H, u_D / H, (-2 * H * u_b + gtot_b / a) / H, (-2 * H * u_D + gtot_D / a) / H, xid / H, xidd / H])
        return dy

    def dmin(y):
        psi_b, psi_D = y[:N], y[N:2 * N]
        db = (np.roll(psi_b, -1) - np.roll(psi_b, 1)) / (2 * dq)
        dD = (np.roll(psi_D, -1) - np.roll(psi_D, 1)) / (2 * dq)
        return min((1 + db).min(), (1 + dD).min())
    return rhs, q, dq, L, dmin, fields


def run(k, A, variant, Q, kapI, ic, zi, zf, rtol=1e-8):
    rhs, q, dq, L, dmin, fields = make_rhs(k, variant, Q, kapI)
    N = NSH
    ai, af = 1.0 / (1 + zi), 1.0 / (1 + zf)
    yv = ai * OM / OR
    f = 1.5 * yv / (1 + 1.5 * yv)
    psi0 = -(A / k) * np.sin(k * q)
    Hi = Hof(ai)
    y0 = np.concatenate([psi0, psi0, f * Hi * psi0, f * Hi * psi0, np.zeros(N), np.zeros(N)])
    if ic == "eq" and Q != 0:
        xb, xD, gNb, gND = fields(psi0, psi0, ai)
        if variant == "V_U":
            gN = gND
        else:
            pref = -1.5 * OB * ai ** -2
            gN = pref * (q - xb)
            gN = gN - gN.mean()
        Peq = hfun_acc(gN)
        dps = (np.roll(psi0, -1) - np.roll(psi0, 1)) / (2 * dq)
        y0[4 * N:5 * N] = Peq * (1.0 + dps) / (1.5 * OC * Q * ai ** -3)
    def event(tau, y):
        return dmin(y) - 0.2
    event.terminal = True
    event.direction = -1
    _DEADLINE[0] = time.time() + TMAX
    try:
        sol = solve_ivp(rhs, (math.log(ai), math.log(af)), y0, method="DOP853", rtol=rtol, atol=1e-13, events=event, t_eval=[math.log(af)])
    except TimeoutError:
        _DEADLINE[0] = 0.0
        return dict(ab=float("nan"), aD=float("nan"), Ps=float("nan"), collapsed=True, zc=float("nan"), a=float("nan"), nfev=-1, timeout=True)
    _DEADLINE[0] = 0.0
    collapsed = sol.status == 1
    if collapsed:
        yf = sol.y_events[0][0]
        tend = float(sol.t_events[0][0])
    else:
        yf = sol.y[:, -1]
        tend = float(sol.t[-1])
    zc = 1.0 / math.exp(tend) - 1.0
    psi_b, psi_D = yf[:N], yf[N:2 * N]
    amp = lambda p: (2.0 / N) * float(np.sum(p * np.sin(k * q)))
    xi_f = yf[4 * N:5 * N]
    afin = math.exp(tend)
    dpsi = (np.roll(psi_D, -1) - np.roll(psi_D, 1)) / (2 * dq)
    P = 1.5 * OC * Q * afin ** -3 * xi_f / (1.0 + dpsi)
    return dict(ab=amp(psi_b), aD=amp(psi_D), Ps=amp(P), collapsed=collapsed, zc=zc, a=afin, nfev=sol.nfev)



def load_pstar():
    p = os.path.join(HERE, "B_budget_pincer" + ("" if C.FOOT == "canonical" else "_second") + "_results.json")
    if not os.path.isfile(p):
        print("C: run B_budget_pincer.py (main) first: P_star is read from its results")
        sys.exit(2)
    return json.load(open(p))["numbers"]["Pstar"]


PSTAR = load_pstar()
PSETS = {"central": (QSCALE * 1.0, 1.0), "star": None}
FB, FD = OB / OM, OC / OM
_ref = {}


def ref(k, A, zi, zf):
    key = (k, A, zi, zf)
    if key not in _ref:
        _ref[key] = run(k, A, "V_B", 0.0, 1.0, "cold", zi, zf)
    return _ref[key]


R.banner("I  integrity: LCDM reference growth vs analytic (matter+Lambda+radiation), and convergence N -> 2N, rtol -> rtol/100")
rr = ref(2.0, 1e-3, 100.0, 10.0)
ai, af = 1 / 101.0, 1 / 11.0
# analytic reference: Meszaros growing mode D ~ 1 + 1.5 y (y = a Om/Or) for matter+radiation, times a small Lambda suppression at z >= 10
# (FIRST version of this check used a Heath integral written incorrectly (radiation inside H with a matter-only kernel); it failed at 6.4% BEFORE any C1 number was seen; replaced here)
yi, yf_ = ai * OM / OR, af * OM / OR
ratio_an = (1 + 1.5 * yf_) / (1 + 1.5 * yi)
ratio_num = rr["aD"] / (-(1e-3 / 2.0))
R.check("I1 reference (Q = 0) growth D(z=10)/D(z=100)", f"solver {ratio_num:.4f}; Meszaros matter+radiation analytic {ratio_an:.4f} (Lambda suppression at z = 10 is O(1e-3))", abs(ratio_num / ratio_an - 1) < 0.01)
for variant, Q, kap in (("V_B", 3.0, 1.0), ("V_U", 3.0, 1.0)):
    out = []
    for nsh, rt in ((512, 1e-8), (1024, 1e-8), (512, 1e-10)):
        NSH = nsh
        make_rhs.__globals__["NSH"] = nsh
        r0 = run(2.0, 1e-3, variant, Q, kap, "cold", 100.0, 10.0, rtol=rt)
        out.append((r0["ab"], r0["aD"]))
    NSH = 512
    make_rhs.__globals__["NSH"] = 512
    d1 = max(abs(out[1][0] / out[0][0] - 1), abs(out[1][1] / out[0][1] - 1))
    d2 = max(abs(out[2][0] / out[0][0] - 1), abs(out[2][1] / out[0][1] - 1))
    R.check(f"I2 convergence {variant} (Q={Q}, k=2, A=1e-3, cold)", f"N 512->1024: {d1:.2e}; rtol 1e-8 -> 1e-10: {d2:.2e} (line 1e-2)", max(d1, d2) < 1e-2)

R.banner("C1  growth at z = 10 (z_i = 100): worst |D_model/D_LCDM - 1| over baryons, medium, total matter; 4 k, 3 amplitudes, 2 dipole ICs; line 0.05")
res = {}
for variant in ("V_U", "V_B"):
    for pname in ("central", "star"):
        Q, kap = PSETS["central"] if pname == "central" else (PSTAR[variant]["Q"], PSTAR[variant]["kappa_I"])
        worst = 0.0
        rows = []
        ncol = 0
        for k in KS:
            for A in AMPS:
                rf = ref(k, A, 100.0, 10.0)
                for ic in ("cold", "eq"):
                    r0 = run(k, A, variant, Q, kap, ic, 100.0, 10.0)
                    if r0["collapsed"]:
                        dev = float("inf")
                        ncol += 1
                        rows.append((k, A, ic, ("TIMEOUT(stiff, >%gs)" % TMAX) if r0.get("timeout") else "COLLAPSED z=%.1f" % r0["zc"], dev))
                    else:
                        tb = r0["ab"] / rf["ab"]
                        td = r0["aD"] / rf["aD"]
                        tt = (FB * r0["ab"] + FD * r0["aD"]) / (FB * rf["ab"] + FD * rf["aD"])
                        dev = max(abs(tb - 1), abs(td - 1), abs(tt - 1))
                        rows.append((k, A, ic, f"b {tb:.4f} D {td:.4f} tot {tt:.4f}", dev))
                    worst = max(worst, dev)
        res[(variant, pname)] = (worst, rows, ncol, Q, kap)
        R.P(f"  {variant} {pname:7s} (Q = {Q:.4g}, kappa_I = {kap:.4g}): worst deviation {worst:.4g}  (collapsed runs: {ncol}/{len(rows)})")
        for k in KS:
            sub = [x for x in rows if x[0] == k]
            R.P(f"      k={k:5.1f}: " + "; ".join(f"A={x[1]:.0e},{x[2]}: {x[3]} ({x[4]:.3g})" for x in sub))
        R.verdict(f"C1_{variant}_{pname}", "PASS" if worst <= 0.05 else "FAIL", f"worst deviation {worst:.4g} vs 0.05 (Q = {Q:.4g}, kappa_I = {kap:.4g})")
for variant in ("V_U", "V_B"):
    ok = res[(variant, "central")][0] <= 0.05 and res[(variant, "star")][0] <= 0.05
    R.verdict(f"G2_{variant}", "PASS" if ok else "FAIL", f"both parameter sets must pass: central worst {res[(variant, 'central')][0]:.4g}, star worst {res[(variant, 'star')][0]:.4g}")

R.banner("C3  regime map: omega^2/H^2 = 1.5 Oc a^-3 (Q^2/kappa_I)/(h' H^2) with g_N from the LCDM linear field (V_B: baryon-only field)")
from cfg121_common import dh, nu_p2
for z in (50.0, 10.0):
    a = 1 / (1 + z)
    for k in (2.0, 30.0):
        for A in AMPS:
            rf = ref(k, A, 100.0, z)
            g = 1.5 * OM * a ** -2 * abs(rf["aD"])
            gb = g * FB / 1.0 * (OM / OM)
            for variant, gg in (("V_U", g), ("V_B", g * FB)):
                y = gg / A0C
                hp = float(dh(nu_p2, np.array([y]))[0])
                for pname in ("central", "star"):
                    Q, kap = PSETS["central"] if pname == "central" else (PSTAR[variant]["Q"], PSTAR[variant]["kappa_I"])
                    om2 = 1.5 * OC * a ** -3 * (Q ** 2 / kap) / hp / Hof(a) ** 2
                    if A in (1e-4, 1e-2):
                        R.P(f"  z={z:5.0f} k={k:4.1f} A={A:.0e} {variant} {pname:7s}: g/a0 = {y:.2e}, h' = {hp:.3g}, omega^2/H^2 = {om2:.3g}  ({'adiabatic' if om2 > 1 else 'free-dipole'})")

R.banner("C2  CMB screen at z = 1100 (z_i = 5000, radiation in H, baryons treated as pressureless: an effective-fluid screen, not a Boltzmann code)")
KS2 = [0.01, 0.1, 1.0]
AMPS2 = [1e-5, 1e-4, 1e-3]
for variant in ("V_U", "V_B"):
    for pname in ("central", "star"):
        Q, kap = PSETS["central"] if pname == "central" else (PSTAR[variant]["Q"], PSTAR[variant]["kappa_I"])
        worst = 0.0
        det = []
        for k in KS2:
            for A in AMPS2:
                rf = ref(k, A, 5000.0, 1100.0)
                for ic in ("cold", "eq"):
                    r0 = run(k, A, variant, Q, kap, ic, 5000.0, 1100.0)
                    if r0["collapsed"]:
                        worst = float("inf")
                        det.append(f"k={k},A={A:.0e},{ic}: " + (f"TIMEOUT(stiff, >{TMAX:g}s)" if r0.get('timeout') else f"COLLAPSED z={r0['zc']:.0f}"))
                        continue
                    rat = r0["a"] ** 2 * r0["Ps"] / (1.5 * OC * r0["aD"])
                    dg = abs(r0["aD"] / rf["aD"] - 1)
                    worst = max(worst, abs(rat), dg)
                    det.append(f"k={k},A={A:.0e},{ic}: delta_pol/delta_D = {rat:+.3e}, D-growth dev {dg:.2e}")
        R.P(f"  {variant} {pname:7s} (Q = {Q:.4g}, kappa_I = {kap:.4g}): worst max(|delta_pol/delta_D|, |D/D_LCDM-1|) = {worst:.4g}")
        for d in det[:6]:
            R.P("       " + d)
        R.verdict(f"C2_{variant}_{pname}", "PASS" if worst <= 0.05 else "FAIL", f"|delta_eff/delta_D - 1| and medium growth <= 0.05 needed; worst {worst:.4g}")
    ok = R.verdicts[f"C2_{variant}_central"]["status"] == "PASS" and R.verdicts[f"C2_{variant}_star"]["status"] == "PASS"
    R.verdict(f"C2_{variant}", "PASS" if ok else "FAIL", "both parameter sets; c_eff^2 half of the line: the polarisation sector has no gradient term so the medium is pressureless (c_eff^2 = 0 by construction, a DEFINITION made at phase 2, not a computed sound speed; k = 1e-3 /Mpc is super-horizon at z = 1100 and is NOT evaluated)")

R.P("\n  NOTE: C2 covers k = 0.01, 0.1, 1 /Mpc only (the frozen k = 1e-3 is super-horizon for a sub-horizon Newtonian solver: UNDECIDED there).")
R.finish(required_change=["G2_V_B", "G2_V_U"] if MUTATE == "Q10" else None)
