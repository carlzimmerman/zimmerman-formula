#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
G1 -- LEADS 1 AND 2 (Gauss and Noether) for a gated MOND field, and the variational test that separates them.

QUESTION.  Can a source-confined edge (phantom mass kept beyond r_e, target M_law(r_e) = M_b sqrt(1 + (r_e/r_M)^2)) be produced by a gate W(x)
multiplying a shift-symmetric MOND field whose only source is the baryons?  (GATES_FROZEN.md: GA, GE; leads L1, L2.)

C1 (sympy)  L1, the Gauss lemma.  Fields (Phi, psi = Phi_N), radial, measure r^2:
        L = r^2 [ -(1/8 pi G) (2 Phi' psi' - Q_W(psi'^2)) - rho Phi ],  Q_W(s) = W(r) Q1(s) + (1 - W(r)) s,  A = dQ_W/ds = W Q1' + 1 - W.
    The Euler-Lagrange equations are derived with sympy; with M' = 4 pi r^2 rho, psi' = G M/r^2, Phi' = A psi' they vanish identically, so the
    dynamical mass r^2 Phi'/G = A M_b(<r):  at W = 0 (A = 1)  M_dyn = M_b exactly, whatever happens inside.  (This is N10 in general form.)
C2 (numbers) the point-mass P2 profile for three gated forms, r_e = 0.4 r_ta, M_b = 1e10, 1e11, 1e12: (a) flux-gated QUMOND (action-derived),
    (b) flux-gated AQUAL (action-derived), (c) SOURCE-SWITCHED QUMOND (W multiplies the phantom density, not its flux; the GP-lane form).
    Reported: M_dyn/M_law(r_e) at 2 r_e (the GE test) and at 3 r_e (W < 1e-8, the Gauss test), and the negative-shell mass.
C3 (sympy)  Helmholtz test: is (c) the Euler-Lagrange system of ANY Lagrangian in (Phi, psi)?  The linearised operator of an EL system is
    formally self-adjoint: L_ab = (L_ba)^dagger.  The flux-gated system satisfies it; the source-switched system fails it by a term proportional
    to W' and vanishes when W' = 0.  So the form that keeps the mass beyond the edge is not an action in these fields.
C4 (sympy + numbers)  L2, Noether:  with the EL equation p' = dL/dPhi and H = Phi' p - L,  dH/dx = -(dL/dW) W' = -Delta L W'  (a prescribed W breaks
    momentum conservation by Delta L grad W).  Its size on DE12's 24 layers (DE12's B = a0^2 q(y)/8 pi G) against the baryons' weight rho_b g.
MUTATE=1 adds a second (real-mass) source to the potential equation: L1's "M_dyn = M_b beyond the edge" must FAIL, in C1 and C2.
SCOPE.  Spherical, static, Newtonian-limit; shift-symmetric Phi, prescribed W(r); point-mass baryons for C2; P2 kernel (nu = sqrt(1 + 1/y)).
"""
import os, sys, math
import numpy as np
import sympy as sp
from scipy.optimize import brentq
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from Gcommon import *   # noqa

MUTATE = os.environ.get("MUTATE", "0") == "1"
R = Report("G1_gauss_noether", MUTATE)
P = R.P
P(__doc__.strip())
if MUTATE:
    P("\n  *** MUTATE=1: a second real-mass source rho_c in the potential equation; L1 (M_dyn = M_b beyond the edge) must FAIL ***")

# =================================================================================================== C1 sympy Gauss lemma
R.banner("C1  (sympy) the Gauss lemma for a gated shift-symmetric two-field MOND action")
r, Gs = sp.symbols("r G", positive=True)
W = sp.Function("W")(r)
Phi = sp.Function("Phi")(r)
psi = sp.Function("psi")(r)
M = sp.Function("M")(r)                        # baryon enclosed mass, M' = 4 pi r^2 rho
Q1 = sp.Function("Q1")
rho = sp.diff(M, r) / (4 * sp.pi * r ** 2)
rho_c = sp.Function("rho_c")(r)                # used only by MUTATE
s = sp.Symbol("s")
# Lagrangian density: only first derivatives of the fields enter; Q_W' = A(psi', W)
dpsi = sp.diff(psi, r)
Qw = W * Q1(s) + (1 - W) * s
L = r ** 2 * (-(1 / (8 * sp.pi * Gs)) * (2 * sp.diff(Phi, r) * dpsi - Qw.subs(s, dpsi ** 2)) - (rho + (rho_c if MUTATE else 0)) * Phi)
from sympy.calculus.euler import euler_equations
eqs = euler_equations(L, [Phi, psi], r)
E_Phi, E_psi = eqs[0].lhs, eqs[1].lhs
dpsi_sol = Gs * M / r ** 2
Asol = W * sp.diff(Q1(s), s).subs(s, dpsi_sol ** 2) + 1 - W        # A = W Q1'(psi'^2) + 1 - W on the solution
dPhi_sol = Asol * dpsi_sol


def on_shell(expr):
    e = expr.doit()
    e = e.subs(sp.Derivative(Phi, (r, 2)), sp.diff(dPhi_sol, r)).subs(sp.Derivative(Phi, r), dPhi_sol)
    e = e.subs(sp.Derivative(psi, (r, 2)), sp.diff(dpsi_sol, r)).subs(sp.Derivative(psi, r), dpsi_sol)
    return sp.simplify(e.doit())


res_Phi = on_shell(E_Phi)
res_psi = on_shell(E_psi)
P(f"    E_Phi on the solution psi' = G M/r^2:  {res_Phi}")
P(f"    E_psi on the solution Phi' = A psi':   {res_psi}")
c1_ok = (res_Phi == 0) and (res_psi == 0)
R.check("C1 (sympy) the EL system of the gated action is solved by psi' = G M_b/r^2, Phi' = A psi' (no other source): "
        "dynamical mass = A M_b(<r), and M_dyn = M_b wherever the gate is off (A = 1)",
        f"residuals: E_Phi -> {res_Phi}, E_psi -> {res_psi}" + ("  [MUTATE: rho_c added to the source]" if MUTATE else ""), c1_ok)

# =================================================================================================== C2 numbers
R.banner("C2  the point-mass P2 profile for three gated forms; r_e = 0.4 r_ta; GE test at 2 r_e, Gauss test at 3 r_e")
DEL = 0.05                                       # gate width in ln r: W = 1/(1 + exp(ln(r/r_e)/DEL)); 10-90% ln-width = 0.22 <= 0.3
Wf = lambda rr, re: 1.0 / (1.0 + np.exp(np.clip(np.log(rr / re) / DEL, -700, 700)))
nu = lambda y: np.sqrt(1.0 + 1.0 / y)


def mu_p2(sg):                                   # AQUAL: g_N = mu(g/a0) g for the P2 kernel
    return (-1.0 + np.sqrt(1.0 + 4.0 * sg ** 2)) / (2.0 * sg)


def Mdyn_flux_qumond(Mb, rr, re):
    gN = G * Mb / rr ** 2
    y = gN / A0
    return Mb * (Wf(rr, re) * nu(y) + 1.0 - Wf(rr, re))


def Mdyn_flux_aqual(Mb, rr, re):
    out = []
    for r_ in np.atleast_1d(rr):
        gN = G * Mb / r_ ** 2
        w = float(Wf(r_, re))
        f = lambda lg: (w * mu_p2(np.exp(lg) / A0) + 1 - w) * np.exp(lg) - gN
        g = math.exp(brentq(f, math.log(gN * 0.999), math.log(gN * (1 + 3e2 * math.sqrt(A0 / gN) + 4 * A0 / gN + 10)), xtol=1e-13))
        out.append(g * r_ ** 2 / G)
    return np.array(out)


def Mdyn_source_switched(Mb, rr, re):
    rgrid = np.geomspace(1e-3 * re, 40 * re, 200001)
    yg = G * Mb / rgrid ** 2 / A0
    Mph = Mb * (nu(yg) - 1.0)                                      # the phantom mass inside r, ungated P2 point mass
    dM = np.gradient(Mph, rgrid)
    Mgated = np.cumsum(Wf(rgrid, re) * dM * np.gradient(rgrid))
    return Mb + np.interp(rr, rgrid, Mgated)


C2 = {}
rows_ok = True
for Mb in (1e10, 1e11, 1e12):
    rta = r_ta_kpc(Mb); re = 0.4 * rta; rM = r_M_kpc(Mb)
    Mlaw = float(P2_dyn_mass(Mb, re))
    entry = dict(r_ta=rta, r_e=re, r_M=rM, x_e=re / rM, M_law_over_Mb=Mlaw / Mb)
    for name, fn in (("flux_QUMOND", Mdyn_flux_qumond), ("flux_AQUAL", Mdyn_flux_aqual), ("source_switched", Mdyn_source_switched)):
        m2 = float(np.atleast_1d(fn(Mb, np.array([2 * re]) if name != "source_switched" else 2 * re, re))[0])
        m3 = float(np.atleast_1d(fn(Mb, np.array([3 * re]) if name != "source_switched" else 3 * re, re))[0])
        if MUTATE and name.startswith("flux"):
            # the second source: a real mass M_c placed at the edge (a fluid), which the flux law then counts
            Mc = Mlaw - Mb
            m2 += Mc; m3 += Mc
        entry[name] = dict(M_over_target_2re=m2 / Mlaw, M_over_Mb_3re=m3 / Mb, negative_shell_Msun=Mlaw - m2)
    C2[f"{Mb:.0e}"] = entry
    P(f"    M_b = {Mb:.0e}: r_ta = {rta:7.1f} kpc, r_e = {re:6.1f} kpc, x_e = r_e/r_M = {re / rM:5.1f}, M_law(r_e)/M_b = {Mlaw / Mb:5.1f}")
    for name in ("flux_QUMOND", "flux_AQUAL", "source_switched"):
        e = entry[name]
        P(f"        {name:16s}: M_dyn(2 r_e)/M_law(r_e) = {e['M_over_target_2re']:.4f}   M_dyn(3 r_e)/M_b = {e['M_over_Mb_3re']:.6f}   negative shell {e['negative_shell_Msun']:.2e} Msun")
R.num("C2", C2)
gauss_ok = all(abs(C2[k][n]["M_over_Mb_3re"] - 1.0) < 1e-6 for k in C2 for n in ("flux_QUMOND", "flux_AQUAL"))
R.check("C2a (L1) both ACTION-DERIVED gated forms give M_dyn = M_b beyond the edge (|M_dyn(3 r_e)/M_b - 1| < 1e-6) for M_b = 1e10, 1e11, 1e12",
        str({k: (round(C2[k]["flux_QUMOND"]["M_over_Mb_3re"], 8), round(C2[k]["flux_AQUAL"]["M_over_Mb_3re"], 8)) for k in C2})
        + ("  [MUTATE: a real mass at the edge]" if MUTATE else ""), gauss_ok)
ge_flux = all(abs(C2[k][n]["M_over_target_2re"] - 1.0) <= 0.10 for k in C2 for n in ("flux_QUMOND", "flux_AQUAL"))
ge_ss = all(abs(C2[k]["source_switched"]["M_over_target_2re"] - 1.0) <= 0.10 for k in C2)
R.check("C2b (reported) GE for the flux-gated forms (M_dyn(2 r_e) within 10% of M_law(r_e))", f"pass = {ge_flux}; ratios "
        f"{ {k: round(C2[k]['flux_QUMOND']['M_over_target_2re'], 3) for k in C2} }", True, load_bearing=False)
R.check("C2c (reported) GE for the source-switched form", f"pass = {ge_ss}; ratios {({k: round(C2[k]['source_switched']['M_over_target_2re'], 3) for k in C2})}",
        True, load_bearing=False)
R.verdict("GE / flux-gated (action-derived)", "PASS" if ge_flux else "FAIL",
          "M_dyn beyond the edge = M_b; the phantom mass inside the edge is a negative shell (Gauss lemma, N10 in general form)")
R.verdict("GE / source-switched", "PASS" if ge_ss else "FAIL", "keeps M_law(r_e) beyond the edge (source-confined) -- but see C3 for GA")

# =================================================================================================== C3 Helmholtz
R.banner("C3  (sympy) Helmholtz test: is the source-switched system the EL system of a Lagrangian in (Phi, psi)?")
nu_f = sp.Function("nu")
ep = sp.Symbol("epsilon")
hP, hpsi = sp.Function("hP")(r), sp.Function("hpsi")(r)
dPsi = sp.diff(psi, r)
Wr = W
E_Phi_c = sp.diff(r ** 2 * dPsi, r) / (4 * sp.pi * Gs) - r ** 2 * rho                                   # includes the measure
E_psi_fg = (sp.diff(r ** 2 * sp.diff(Phi, r), r) - sp.diff(r ** 2 * (Wr * nu_f(dPsi) + 1 - Wr) * dPsi, r)) / (4 * sp.pi * Gs)
E_psi_ss = (sp.diff(r ** 2 * sp.diff(Phi, r), r) - sp.diff(r ** 2 * dPsi, r) - Wr * sp.diff(r ** 2 * (nu_f(dPsi) - 1) * dPsi, r)) / (4 * sp.pi * Gs)


def linearise(E):
    """delta E_a = L_a,Phi hP + L_a,psi hpsi as coefficient triples (c2, c1, c0) of (h'', h', h)."""
    Ee = E.subs({Phi: Phi + ep * hP, psi: psi + ep * hpsi}).doit()
    dE = sp.diff(Ee, ep).subs(ep, 0).doit()
    out = {}
    for name, h in (("Phi", hP), ("psi", hpsi)):
        c2 = sp.diff(dE, sp.diff(h, r, 2))
        rest = dE - c2 * sp.diff(h, r, 2)
        c1 = sp.diff(rest, sp.diff(h, r))
        rest = rest - c1 * sp.diff(h, r)
        c0 = sp.diff(rest, h)
        out[name] = tuple(sp.simplify(c) for c in (c2, c1, c0))
    return out


def adj(t):
    c2, c1, c0 = t
    return (c2, 2 * sp.diff(c2, r) - c1, sp.diff(c2, r, 2) - sp.diff(c1, r) + c0)


def helm(Epsi):
    L_Phi = linearise(E_Phi_c)                      # row a = Phi
    L_psi = linearise(Epsi)                         # row a = psi
    # conditions: L_PhiPhi self-adjoint, L_psipsi self-adjoint, L_Phipsi = (L_psiPhi)^dagger
    conds = []
    conds += [sp.simplify(x - y) for x, y in zip(L_Phi["Phi"], adj(L_Phi["Phi"]))]
    conds += [sp.simplify(x - y) for x, y in zip(L_psi["psi"], adj(L_psi["psi"]))]
    conds += [sp.simplify(x - y) for x, y in zip(L_Phi["psi"], adj(L_psi["Phi"]))]
    return conds


conds_fg = helm(E_psi_fg)
conds_ss = helm(E_psi_ss)
nz_fg = [c for c in conds_fg if c != 0]
nz_ss = [c for c in conds_ss if c != 0]
P(f"    flux-gated:      nonzero Helmholtz residuals: {len(nz_fg)}")
P(f"    source-switched: nonzero Helmholtz residuals: {len(nz_ss)}")
for c in nz_ss:
    P(f"        residual = {sp.simplify(c)}")
Wp = sp.Derivative(W, r)
kill = {sp.Derivative(W, (r, 2)): 0, sp.Derivative(W, r): 0}
nz_ss_const = [sp.simplify(c.subs(kill).doit()) for c in nz_ss]
P(f"    source-switched with W' = W'' = 0: residuals {nz_ss_const}")
helm_ok = (len(nz_fg) == 0) and (len(nz_ss) > 0) and all(c == 0 for c in nz_ss_const)
R.check("C3 (sympy) the flux-gated system is formally self-adjoint (an EL system); the source-switched system that keeps the mass beyond the edge is NOT, "
        "and its asymmetry is proportional to W' (it vanishes for constant W)",
        f"flux-gated nonzero residuals {len(nz_fg)}; source-switched {len(nz_ss)}; with W' = 0: {nz_ss_const}", helm_ok)
R.verdict("GA / source-switched", "FAIL", "not derivable from any Lagrangian in (Phi, psi) with a prescribed W (Helmholtz); hypotheses: 2 fields, first-derivative, gate a prescribed function of r")

# =================================================================================================== C4 Noether
R.banner("C4  (sympy + numbers) the Noether identity: a prescribed W breaks momentum conservation by Delta L grad W")
x = sp.Symbol("x")
Wx = sp.Function("W")(x)
Fy = sp.Function("F")
a0s, rho_s = sp.symbols("a0 rho", positive=True)
Ph = sp.Function("Phi")(x)
y = sp.diff(Ph, x) ** 2 / a0s ** 2
Lc = -(a0s ** 2 / (8 * sp.pi * Gs)) * (Wx * Fy(y) + (1 - Wx) * y) - rho_s * Ph
pmom = sp.diff(Lc, sp.diff(Ph, x))
EL = sp.diff(pmom, x) - sp.diff(Lc, Ph)                                    # EL residual (zero on shell)
H = sp.diff(Ph, x) * pmom - Lc
dH = sp.diff(H, x)
LW = sp.diff(Lc, Wx)
ident = sp.simplify(dH - sp.diff(Ph, x) * EL + LW * sp.diff(Wx, x))
DeltaL = (a0s ** 2 / (8 * sp.pi * Gs)) * (y - Fy(y))
P(f"    d/dx (Phi' p - L) - Phi' (EL) + (dL/dW) W'  =  {ident}     (dL/dW = + Delta L with Delta L = (a0^2/8 pi G)(y - F))")
P(f"    check dL/dW - Delta L = {sp.simplify(LW - DeltaL)}")
noe_ok = (ident == 0) and (sp.simplify(LW - DeltaL) == 0)
R.check("C4a (sympy, L2) on shell, d/dx(Phi' p - L) = -(dL/dW) W' = -Delta L W' (dL/dW = Delta L): a prescribed W breaks momentum conservation by exactly "
        "Delta L grad W, Delta L = (a0^2/8 pi G)(y - F(y))", f"identity residual {ident}; dL/dW - Delta L = {sp.simplify(LW - DeltaL)}", noe_ok)

de = load_de12()
Wd = de["Wd"]; transition = de["transition"]; CS = de["CS"]; KPCm = de["KPC"]; Gsi = de["G"]; MSun = de["MS"]
rows = []
for z in (0.25, 1.0, 2.5, 4.0):
    for Mb in (1e10, 1e11, 1e12):
        for foot in ("canonical", "alt"):
            tr = transition(z, Mb, foot, 0.25)
            t = tr["t"]; m = (t > 0.004) & (t < 0.996)
            if not m.any():
                continue
            _, W1, _ = Wd(t)
            dtdr = np.gradient(t, tr["r"])
            reaction_density = tr["B"] * np.abs(W1 * dtdr)               # |Delta L W'| in J/m^4 (force per volume), Delta L = B
            gN = Gsi * Mb * MSun / tr["r"] ** 2
            weight = tr["rho_b"] * tr["g"]                                # rho_b g (the baryons' weight in the law's field)
            ratio = reaction_density / weight
            rows.append((z, Mb, foot, float(np.max(ratio[m]))))
            R.num(f"noether/{z}/{Mb:.0e}/{foot}", float(np.max(ratio[m])))
mx = max(r_[3] for r_ in rows); mn = min(r_[3] for r_ in rows)
for z in (0.25, 2.5):
    P("    z = %.2f max (Delta L |grad W|)/(rho_b g) over the layer: " % z + ", ".join(f"{r_[1]:.0e}/{r_[2][:3]}: {r_[3]:.1f}" for r_ in rows if r_[0] == z))
P(f"    over all 24 layers: min {mn:.2f}, max {mx:.2f}  (a value >= 1 means the gate's reaction force density exceeds the baryons' weight)")
R.check("C4b (reported, L2 size) Delta L |grad W| against rho_b g on DE12's 24 layers (gate width w = 0.25)", f"range {mn:.2f} - {mx:.2f}", True, load_bearing=False)
R.verdict("GB-related (Noether reaction)", "OPEN", f"the reaction Delta L grad W must be absorbed by whatever W reads; its size is {mn:.1f}-{mx:.1f} of the baryons' weight on DE12's layers (gate width 0.25)")

nf = R.write()
sys.exit(1 if nf else 0)
