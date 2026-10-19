#!/usr/bin/env python3
"""CL-AR-2026-10-19-01 -- uniform (affine) acceleration response: exact checks.

Every check is symbolic (sympy) except none; no numerics are needed here.

A. Classical: N=3 bodies in 3D with ARBITRARY pair potentials V_ij(|x_i-x_j|)
   and passive gravitational charges gamma_i.  Internal (COM-relative)
   accelerations depend on E only through (gamma_i/m_i - sum gamma/M) E.
   With minimal coupling gamma_i=m_i they are E-free (all orders, any state).
B. Quantum: COM operators (R,P) commute with every relative coordinate
   y_a=x_a-R and relative momentum pi_a=p_a-(m_a/M)P; kinetic energy splits;
   the uniform-field coupling is -M E.R.  Hence H(E)=H_COM(E)+H_int with
   [H_COM(E),H_int]=0: exp(-iH(E)t)=exp(-iH_COM(E)t)exp(-iH_int t).
C. Field level, nonlinear: matched daughter GP (contact g_c) + barotropic Euler
   baryons + one-copy Poisson, 3D, with an arbitrary TIME-DEPENDENT uniform
   field E(t)=xi''(t).  The Avron-Herbst map
      psi_E(x,t)=psi_0(x-xi,t) exp(i[m xi'.x - S(t)]/hbar), S'=m|xi'|^2/2,
      rho_bE(x,t)=rho_b0(x-xi,t), v_E=v_0(x-xi,t)+xi', U_E=U_0(x-xi,t)
   maps residuals to residuals exactly.
D. Support chain cloud(m_c)-host(m_h)-support(m_s) with springs k1,k2 and an
   optional EXTERNAL anchor spring k3.  Closed chain (k3=0): zero internal
   response at every drive frequency and every m_s (incl. m_s -> oo).
   Anchored chain: static sag m_c E/k1, (m_c+m_h)E/k2 for ANY k3>0.
   The limits k3->0 and omega->0 do not commute.
E. Newton-Cartan locality: under a Milne boost x'=x-xi(t), g'=g-xi'' while the
   tidal tensor and (worldline acceleration - g) are invariant.

Usage: python3 affine_exact.py OUTDIR   (writes OUTDIR/affine_exact.json)
"""
import json
import sys
from pathlib import Path

import sympy as sp

results = {"checkpoint": "CL-AR-2026-10-19-01", "script": "affine_exact.py",
           "checks": {}}


def record(name, ok, detail=""):
    results["checks"][name] = {"passed": bool(ok), "detail": detail}
    print(("PASS " if ok else "FAIL ") + name + (": " + detail if detail else ""))
    return ok


# ---------------------------------------------------------------- A
def part_a():
    t = sp.symbols("t", real=True)
    m = sp.symbols("m1:4", positive=True)
    gam = sp.symbols("gamma1:4", positive=True)
    Evec = sp.Matrix(sp.symbols("E_x E_y E_z", real=True))
    X = [sp.Matrix([sp.Function(f"x{i}{c}")(t) for c in "xyz"])
         for i in range(1, 4)]
    pairs = [(0, 1), (0, 2), (1, 2)]
    Vf = {p: sp.Function(f"V{p[0]+1}{p[1]+1}") for p in pairs}

    def dist(a, b):
        d = X[a] - X[b]
        return sp.sqrt(d.dot(d))

    V = sum(Vf[p](dist(*p)) for p in pairs)
    F = [-sp.Matrix([sp.diff(V, X[i][c]) for c in range(3)]) for i in range(3)]
    third_law = sp.simplify(F[0] + F[1] + F[2])
    record("A1_internal_forces_sum_to_zero", third_law == sp.zeros(3, 1),
           "translation-invariant pair forces obey Newton's third law")
    acc = [(F[i] + gam[i] * Evec) / m[i] for i in range(3)]
    M = sum(m)
    Racc = sum((m[i] * acc[i] for i in range(3)), sp.zeros(3, 1)) / M
    # COM acceleration: E-part = (sum gamma / M) E, no internal force left
    rc = sp.simplify(Racc - (sum(gam) / M) * Evec)
    record("A2_COM_acceleration", rc == sp.zeros(3, 1),
           "R'' = (sum_i gamma_i / M) E exactly")
    ok_resid = True
    ok_min = True
    for i in range(3):
        yacc = acc[i] - Racc
        J = yacc.jacobian(Evec)
        expect = (gam[i] / m[i] - sum(gam) / M) * sp.eye(3)
        ok_resid &= sp.simplify(J - expect) == sp.zeros(3, 3)
        Jmin = J.subs({gam[j]: m[j] for j in range(3)})
        ok_min &= sp.simplify(Jmin) == sp.zeros(3, 3)
    record("A3_internal_E_dependence_is_EP_violation_only", ok_resid,
           "d(y_i'')/dE = (gamma_i/m_i - sum gamma/M) * Identity")
    record("A4_minimal_coupling_internal_E_free", ok_min,
           "gamma_i=m_i: every internal acceleration is E-independent "
           "for arbitrary pair potentials (nonlinear, all orders)")


# ---------------------------------------------------------------- B
def part_b(N=4):
    """Linear canonical forms: [a.x+b.p, c.x+d.p] = i hbar (a.d - b.c)."""
    hbar = sp.symbols("hbar", positive=True)
    m = sp.symbols(f"m1:{N+1}", positive=True)
    M = sum(m)
    # represent a linear form as (coeffs of x_1..x_N, coeffs of p_1..p_N)
    def form(ax, bp):
        return (sp.Matrix(ax), sp.Matrix(bp))

    def comm(A, B):
        return sp.I * hbar * (A[0].dot(B[1]) - A[1].dot(B[0]))

    zero = [0] * N
    R = form([mi / M for mi in m], zero)
    P = form(zero, [1] * N)
    ok = sp.simplify(comm(R, P) - sp.I * hbar) == 0
    allzero = True
    for a in range(N):
        ya = form([(1 if j == a else 0) - m[j] / M for j in range(N)], zero)
        pia = form(zero, [(1 if j == a else 0) - m[a] / M for j in range(N)])
        allzero &= sp.simplify(comm(R, pia)) == 0
        allzero &= sp.simplify(comm(P, ya)) == 0
        for b in range(N):
            pib = form(zero, [(1 if j == b else 0) - m[b] / M
                              for j in range(N)])
            expect = sp.I * hbar * ((1 if a == b else 0) - m[b] / M)
            allzero &= sp.simplify(comm(ya, pib) - expect) == 0
    record("B1_COM_commutes_with_relative_variables", ok and allzero,
           f"N={N}: [R,P]=i hbar, [R,pi_a]=[P,y_a]=0, "
           "[y_a,pi_b]=i hbar(delta_ab - m_b/M)")
    p = sp.symbols(f"p1:{N+1}", real=True)
    Ptot = sum(p)
    pi = [p[a] - m[a] / M * Ptot for a in range(N)]
    kin = sum(p[a] ** 2 / (2 * m[a]) for a in range(N))
    split = Ptot ** 2 / (2 * M) + sum(pi[a] ** 2 / (2 * m[a]) for a in range(N))
    record("B2_kinetic_split", sp.simplify(kin - split) == 0,
           "sum p^2/2m = P^2/2M + sum pi^2/2m (momenta commute)")
    x = sp.symbols(f"x1:{N+1}", real=True)
    Rx = sum(m[a] * x[a] for a in range(N)) / M
    E = sp.symbols("E", real=True)
    coup = -E * sum(m[a] * x[a] for a in range(N))
    record("B3_uniform_coupling_is_COM_only",
           sp.simplify(coup + E * M * Rx) == 0,
           "-E sum m_a x_a = -E M R (gravitational = inertial weights)")


# ---------------------------------------------------------------- C
def part_c():
    tau = sp.symbols("tau", real=True)
    Xs = sp.symbols("X1:4", real=True)
    hbar, m, gc, G = sp.symbols("hbar m g_c G", positive=True)
    xi = [sp.Function(f"xi{i}")(tau) for i in range(1, 4)]
    xid = [sp.diff(f, tau) for f in xi]
    E = [sp.diff(f, tau, 2) for f in xi]          # arbitrary E(t) = xi''
    S = sp.Function("S")(tau)
    psi0 = sp.Function("psi0")(*Xs, tau)
    psi0c = sp.Function("psi0c")(*Xs, tau)          # independent conjugate
    U0 = sp.Function("U0")(*Xs, tau)
    rho0 = sp.Function("rho0")(*Xs, tau)
    v0 = [sp.Function(f"v0{i}")(*Xs, tau) for i in range(1, 4)]
    Pfun = sp.Function("P")

    def Dt(f):   # d/dt at fixed lab x, expressed in moving coordinates
        return sp.diff(f, tau) - sum(xid[i] * sp.diff(f, Xs[i])
                                     for i in range(3))

    def Dx(f, i):
        return sp.diff(f, Xs[i])

    lab_x = [Xs[i] + xi[i] for i in range(3)]
    theta = (m * sum(xid[i] * lab_x[i] for i in range(3)) - S) / hbar
    phase = sp.exp(sp.I * theta)
    psiE = psi0 * phase
    UextE = -sum(E[i] * lab_x[i] for i in range(3))
    dens = psi0 * psi0c                                 # |psi_E|^2 = |psi_0|^2
    resE = (sp.I * hbar * Dt(psiE)
            + hbar ** 2 / (2 * m) * sum(Dx(Dx(psiE, i), i) for i in range(3))
            - (m * (U0 + UextE) + gc * dens) * psiE)
    res0 = (sp.I * hbar * sp.diff(psi0, tau)
            + hbar ** 2 / (2 * m) * sum(sp.diff(psi0, Xs[i], 2)
                                        for i in range(3))
            - (m * U0 + gc * dens) * psi0)
    diff = sp.expand(sp.simplify(resE / phase - res0))
    diff = diff.subs(sp.Derivative(S, tau),
                     m * sum(v ** 2 for v in xid) / 2)
    record("C1_GP_Avron_Herbst_covariance", sp.simplify(diff) == 0,
           "residual_E = phase * residual_0(x - xi, t) with S' = m|xi'|^2/2; "
           "E(t)=xi'' arbitrary (time-dependent uniform field)")
    # Euler + continuity for the barotropic baryon fluid
    vE = [v0[i] + xid[i] for i in range(3)]
    contE = Dt(rho0) + sum(Dx(rho0 * vE[i], i) for i in range(3))
    cont0 = sp.diff(rho0, tau) + sum(sp.diff(rho0 * v0[i], Xs[i])
                                     for i in range(3))
    ok_c = sp.simplify(contE - cont0) == 0
    ok_e = True
    for i in range(3):
        eulE = (Dt(vE[i]) + sum(vE[j] * Dx(vE[i], j) for j in range(3))
                + Dx(Pfun(rho0), i) / rho0 + Dx(U0, i) - E[i])
        eul0 = (sp.diff(v0[i], tau) + sum(v0[j] * sp.diff(v0[i], Xs[j])
                                          for j in range(3))
                + sp.diff(Pfun(rho0), Xs[i]) / rho0 + sp.diff(U0, Xs[i]))
        ok_e &= sp.simplify(eulE - eul0) == 0
    record("C2_Euler_continuity_covariance", ok_c and ok_e,
           "barotropic baryon fluid (any P(rho), incl. K_b rho^(5/3)): "
           "residuals map exactly; v_E = v_0 + xi'")
    # Poisson: densities and potential are rigid translates -> identical PDE
    lapU = sum(sp.diff(U0, Xs[i], 2) for i in range(3))
    lapU_lab = sum(Dx(Dx(U0, i), i) for i in range(3))
    poisE = lapU_lab - 4 * sp.pi * G * (m * dens + rho0)
    pois0 = lapU - 4 * sp.pi * G * (m * dens + rho0)
    record("C3_Poisson_translation", sp.simplify(poisE - pois0) == 0,
           "(trivial identity) Laplacian is translation invariant and "
           "m|psi|^2+rho_b translate rigidly: one-copy Poisson maps to itself")
    # GP with the full quantum-pressure term is the same equation (Madelung),
    # so the shared GP-Euler-Poisson state of the equilibrium lane is covered.


# ---------------------------------------------------------------- D
def part_d():
    mc, mh, ms, k1, k2, k3, E, w = sp.symbols(
        "m_c m_h m_s k_1 k_2 k_3 E omega", positive=True)
    Mm = sp.diag(mc, mh, ms)
    K = sp.Matrix([[k1, -k1, 0], [-k1, k1 + k2, -k2], [0, -k2, k2 + k3]])
    f = sp.Matrix([mc, mh, ms]) * E
    # closed chain, harmonic drive E exp(-i w t): particular solution
    K0 = K.subs(k3, 0)
    x0 = (K0 - w ** 2 * Mm).LUsolve(f)
    d1 = sp.simplify(x0[0] - x0[1])
    d2 = sp.simplify(x0[1] - x0[2])
    record("D1_closed_chain_zero_internal_response",
           d1 == 0 and d2 == 0,
           "k3=0: internal extensions vanish identically at every omega>0 "
           "and every m_s; displacement = -E/omega^2 common to all bodies")
    # heavy free support: still zero (limit m_s -> oo at k3=0)
    d1_inf = sp.limit(d1, ms, sp.oo)
    record("D2_heavy_free_support_is_not_an_anchor", d1_inf == 0,
           "lim_{m_s->oo} (closed chain) internal extension = 0")
    # anchored chain
    xa = (K - w ** 2 * Mm).LUsolve(f)
    a1 = sp.simplify(xa[0] - xa[1])
    a2 = sp.simplify(xa[1] - xa[2])
    a1_static = sp.simplify(a1.subs(w, 0))
    a2_static = sp.simplify(a2.subs(w, 0))
    xs_static = sp.simplify(xa[2].subs(w, 0))
    ok_static = (sp.simplify(a1_static - mc * E / k1) == 0 and
                 sp.simplify(a2_static - (mc + mh) * E / k2) == 0 and
                 sp.simplify(xs_static - (mc + mh + ms) * E / k3) == 0)
    record("D3_anchored_static_sag", ok_static,
           "omega=0, any k3>0: c-h extension m_c E/k1, h-s extension "
           "(m_c+m_h)E/k2, anchor carries the total weight (support "
           "displacement M_tot E/k3)")
    lim_k3_then_w = sp.limit(sp.limit(a1, k3, 0), w, 0)
    lim_w_then_k3 = sp.limit(sp.limit(a1, w, 0), k3, 0)
    record("D4_noncommuting_limits",
           lim_k3_then_w == 0 and sp.simplify(lim_w_then_k3 - mc * E / k1) == 0,
           f"lim_w lim_k3 = {lim_k3_then_w}; lim_k3 lim_w = {lim_w_then_k3}")
    # shape (quadrupole about the total COM) changes only when anchored
    def quad(x):
        Mt = mc + mh + ms
        X = (mc * x[0] + mh * x[1] + ms * x[2]) / Mt
        return mc * (x[0] - X) ** 2 + mh * (x[1] - X) ** 2 + ms * (x[2] - X) ** 2
    r1, r2 = sp.symbols("r_1 r_2", positive=True)   # reference positions
    ref = sp.Matrix([r1 + r2, r2, 0])
    dq_closed = sp.simplify(sp.diff(quad(ref + x0), E).subs(E, 0))
    dq_anch = sp.simplify(sp.diff(quad(ref + xa.subs(w, 0)), E).subs(E, 0))
    record("D5_source_multipole_change",
           dq_closed == 0 and dq_anch != 0,
           f"dQ/dE closed = {dq_closed}; anchored = {sp.factor(dq_anch)}")
    # exact time-domain statement for the closed chain from a relaxed start
    t = sp.symbols("t", real=True)
    xt = sp.Matrix([E * t ** 2 / 2] * 3)
    resid = sp.simplify(Mm * sp.diff(xt, t, 2) + K0 * xt - f)
    record("D6_closed_chain_exact_trajectory", resid == sp.zeros(3, 1),
           "x_i(t)=x_i(0)+E t^2/2 solves the closed chain exactly from a "
           "relaxed state: no transient internal motion at any E")


# ---------------------------------------------------------------- E
def part_e():
    t = sp.symbols("t", real=True)
    xp = sp.symbols("x1:4", real=True)
    xi = [sp.Function(f"xi{i}")(t) for i in range(1, 4)]
    U = sp.Function("U")
    lab = [xp[i] + xi[i] for i in range(3)]
    Ulab = U(*lab, t)
    # potential in the Milne (accelerated) frame: U' = U(x'+xi) + xi''.x'
    Up = Ulab + sum(sp.diff(xi[i], t, 2) * xp[i] for i in range(3))
    gp = [-sp.diff(Up, xp[i]) for i in range(3)]
    g = [-sp.diff(Ulab, xp[i]) for i in range(3)]
    ok_shift = all(sp.simplify(gp[i] - (g[i] - sp.diff(xi[i], t, 2))) == 0
                   for i in range(3))
    ok_tidal = all(sp.simplify(sp.diff(Up, xp[i], xp[j])
                               - sp.diff(Ulab, xp[i], xp[j])) == 0
                   for i in range(3) for j in range(3))
    q = [sp.Function(f"q{i}")(t) for i in range(1, 4)]   # worldline in lab
    qp = [q[i] - xi[i] for i in range(3)]
    gl = [-sp.diff(U(*q, t), q[i]) for i in range(3)]
    # g' evaluated on the worldline = g(q) - xi''
    gp_on = [gl[i] - sp.diff(xi[i], t, 2) for i in range(3)]
    ok_rel = all(sp.simplify((sp.diff(qp[i], t, 2) - gp_on[i])
                             - (sp.diff(q[i], t, 2) - gl[i])) == 0
                 for i in range(3))
    record("E1_g_is_frame_dependent", ok_shift, "g' = g - xi''")
    record("E2_tidal_tensor_invariant", ok_tidal, "d_i d_j U' = d_i d_j U")
    record("E3_support_acceleration_invariant", ok_rel,
           "(x'' - g) is invariant: the only local scalar equal to |g| is "
           "|f/rho| of NON-geodesic (supported) matter")


if __name__ == "__main__":
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    out.mkdir(parents=True, exist_ok=True)
    part_a()
    part_b()
    part_c()
    part_d()
    part_e()
    allok = all(c["passed"] for c in results["checks"].values())
    results["all_passed"] = allok
    results["sympy_version"] = sp.__version__
    (out / "affine_exact.json").write_text(json.dumps(results, indent=1))
    print("ALL PASSED" if allok else "SOME CHECKS FAILED")
    sys.exit(0 if allok else 1)
