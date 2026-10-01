"""CFG263 / NG-G: independent re-derivation of lane G's symmetry no-go.
Written without opening agents/G_symmetry_conformal/*.py or *.out. c = G = 1 unless stated.

Premises audited (CFG263_FROZEN_CRITERIA.md section 2, NG-G):
 G-i   the Lindemann dichotomy (a0/H algebraic  =>  kappa transcendental)
 G-ii  dilatation acts on (a0, Lambda) with Lambda/a0^2 invariant
 G-iii F -> F + C is invisible to the a0-sector field equation (but is a vacuum energy)
 G-iv  dS Killing algebra carries no H
 plus the static-observer crossover a = H and the RAR offset G rho/a0^2 = 1.03.
"""
import sympy as sp
import mpmath as mp
from cfg263_lib import Checks, run_main

mp.mp.dps = 60


def main():
    C = Checks("NG-G")
    a0, H, G, rho, kap, u = sp.symbols("a0 H G rho kappa u", positive=True)

    # ---------- G-i: kappa = (a0/H) sqrt(8 pi/3) -------------------------------------------
    # definitions: a0 = kappa sqrt(G rho); H^2 = 8 pi G rho / 3
    Hsq = sp.Rational(8, 3) * sp.pi * G * rho
    ratio = (kap * sp.sqrt(G * rho)) / sp.sqrt(Hsq)  # a0/H
    C.check("G1_kappa_from_a0_over_H", sp.simplify(ratio - kap * sp.sqrt(3 / (8 * sp.pi))) == 0,
            "a0/H = kappa sqrt(3/(8 pi)) exactly")

    # Lindemann (imported theorem): pi transcendental => kappa^2 = q (8 pi/3) transcendental for algebraic q != 0.
    # Illustration only: integer-relation search on kappa^2 for algebraic (a0/H)^2; control finds an algebraic number.
    def has_poly(x, deg=6, maxc=10**4):
        try:
            p = mp.findpoly(x, deg, maxcoeff=maxc)
        except Exception:
            p = None
        return p is not None
    algebraic_q2 = [mp.mpf(1), mp.mpf(1) / 4, mp.mpf(1) / 36, mp.mpf(3) / 32, mp.mpf(2), mp.mpf(1) / 9]
    hits = [has_poly(q2 * 8 * mp.pi / 3) for q2 in algebraic_q2]
    C.check("G2_no_poly_for_kappa2_given_algebraic_a0H", not any(hits),
            f"findpoly(deg<=6, coeff<=1e4) on kappa^2 for 6 algebraic (a0/H)^2: hits={hits}")
    C.check("G2c_control_algebraic_found", has_poly(mp.sqrt(2) + mp.mpf(1) / 3),
            "control: sqrt2 + 1/3 has a polynomial (search can succeed)")

    # ---------- the unit-dual of G-i (H3 point): hold G rho fixed ---------------------------------
    # if kappa^2 is rational (1/4), (a0/H)^2 = kappa^2 * 3/(8 pi) is transcendental.
    a0H2_at_half = mp.mpf(1) / 4 * 3 / (8 * mp.pi)
    C.check("G3_dual_a0H_transcendental_at_kappa_half", not has_poly(a0H2_at_half),
            f"(a0/H)^2 at kappa=1/2 = 3/(32 pi) = {mp.nstr(a0H2_at_half, 12)}: no polynomial found")
    C.check("G3b_dual_kappa2_rational", has_poly(mp.mpf(1) / 4),
            "kappa^2 = 1/4 is found algebraic: the dichotomy is symmetric, it excludes NEITHER variable a priori")
    C.value("a0_over_H_at_kappa_half", mp.sqrt(a0H2_at_half))

    # ---------- G-ii: unit group invariants ----------------------------------------------------
    # columns: a0, Lambda, G, c, rho ; rows: L, T, M exponents
    Mdim = sp.Matrix([[1, -2, 3, 1, -3],
                      [-2, 0, -2, -1, 0],
                      [0, 0, -1, 0, 1]])
    ns = Mdim.nullspace()
    C.check("G4_two_dimensionless_invariants", len(ns) == 2, f"rank {Mdim.rank()} of 5 quantities -> {len(ns)} invariants")
    # check the two named invariants are in the null space
    inv1 = sp.Matrix([-2, 1, 0, 4, 0])  # Lambda c^4 / a0^2
    inv2 = sp.Matrix([0, -1, 1, -2, 1])  # G rho / (c^2 Lambda)
    C.check("G4b_named_invariants", (Mdim * inv1).is_zero_matrix and (Mdim * inv2).is_zero_matrix,
            "Lambda c^4/a0^2 and G rho/(c^2 Lambda) are the invariants; a dilatation q: (a0, Lambda) -> (a0/q, Lambda/q^2) fixes both")

    # deep-MOND radial equation with a uniform vacuum source: (1/r^2) d/dr (r^2 g^2) = 4 pi a0 (M delta + rho_L)
    r, q, M, rL = sp.symbols("r q M rho_L", positive=True)
    g2 = M * a0 / r**2 + sp.Rational(4, 3) * sp.pi * a0 * rL * r  # r^2 g^2 = M a0 + (4pi/3) a0 rho_L r^3
    lhs = sp.diff(r**2 * g2, r) / r**2
    C.check("G5_deepMOND_vacuum_solution", sp.simplify(lhs - 4 * sp.pi * a0 * rL) == 0, "g^2 = M a0/r^2 + (4pi/3) a0 rho_L r solves the radial equation")
    # dilated solution g_q(r) = g(r/q)/q solves the same equation with rho_L -> rho_L / q^3
    g2q = g2.subs(r, r / q) / q**2
    lhsq = sp.diff(r**2 * g2q, r) / r**2
    C.check("G5b_dilatation_moves_vacuum", sp.simplify(lhsq - 4 * sp.pi * a0 * rL / q**3) == 0,
            "dilated solution needs rho_L -> rho_L/q^3: the vacuum carries scale weight, as G R4 states")

    # ---------- G-iii: additive constant ----------------------------------------------------------
    x, y, z = sp.symbols("x y z", real=True)
    phi = sp.Function("phi")(x, y, z)
    F = sp.Function("F")
    Cc = sp.symbols("C_const")
    grad2 = sum(sp.diff(phi, s)**2 for s in (x, y, z))
    rhof = sp.Function("rho_m")(x, y, z)
    Lag = -(a0**2 / (8 * sp.pi * G)) * F(grad2 / a0**2) - rhof * phi
    LagC = -(a0**2 / (8 * sp.pi * G)) * (F(grad2 / a0**2) + Cc) - rhof * phi
    el = sp.euler_equations(Lag, [phi], [x, y, z])[0].lhs
    elC = sp.euler_equations(LagC, [phi], [x, y, z])[0].lhs
    C.check("G6_EL_blind_to_constant", sp.simplify(el - elC) == 0, "Euler-Lagrange equation identical for F and F + C")
    # static T_00 = -L (no time derivatives): the shift is a vacuum energy a0^2 C/(8 pi G)
    C.check("G6b_T00_sees_constant", sp.simplify((-LagC) - (-Lag) - a0**2 * Cc / (8 * sp.pi * G)) == 0,
            "energy density shifts by a0^2 C/(8 pi G); in a covariant completion sqrt(-g) C is a cosmological constant (Einstein eq sees it)")

    # stress trace: T^i_i = (a0^2/8piG)(2 y F' - d F) vanishes identically iff F = k y^(d/2)
    yv, k = sp.symbols("y k", positive=True)
    Fy = sp.Function("F")
    for d in (2, 3, 4, 5):
        sol = sp.dsolve(sp.Eq(2 * yv * Fy(yv).diff(yv) - d * Fy(yv), 0))
        ok = sp.simplify(sol.rhs / yv**sp.Rational(d, 2)).free_symbols <= {sp.Symbol("C1")}
        C.check(f"G7_traceless_iff_power_d{d}", ok, f"2yF' = {d}F  =>  F = {sol.rhs}")

    # ---------- G-iv: dS Killing algebra in conformal coordinates, symbolic H -------------------
    eta = sp.symbols("eta", negative=True)
    X = [eta, x, y, z]
    Hs = sp.symbols("H_s", positive=True)
    Om2 = 1 / (Hs**2 * eta**2)
    gmat = sp.diag(-Om2, Om2, Om2, Om2)
    sx = [x, y, z]

    def lie_metric(xi):
        out = sp.zeros(4, 4)
        for m in range(4):
            for n in range(4):
                e = sum(xi[l] * sp.diff(gmat[m, n], X[l]) for l in range(4))
                e += sum(gmat[l, n] * sp.diff(xi[l], X[m]) + gmat[m, l] * sp.diff(xi[l], X[n]) for l in range(4))
                out[m, n] = sp.simplify(e)
        return out
    gens = {}
    for i, s in enumerate(sx):
        v = [0, 0, 0, 0]; v[i + 1] = 1; gens[f"P{s}"] = v
    for (i, a), (j, b) in [((0, x), (1, y)), ((0, x), (2, z)), ((1, y), (2, z))]:
        v = [0, 0, 0, 0]; v[i + 1] = b; v[j + 1] = -a; gens[f"J{a}{b}"] = v
    gens["D"] = [eta, x, y, z]
    r2 = x**2 + y**2 + z**2
    for i, s in enumerate(sx):
        v = [2 * s * eta] + [2 * s * w for w in sx]
        v[i + 1] += (eta**2 - r2)
        gens[f"K{s}"] = v
    allkill = all(lie_metric(v).is_zero_matrix for v in gens.values())
    C.check("G8_ten_killing_fields_H_free", allkill and len(gens) == 10 and all(Hs not in sp.sympify(c).free_symbols for v in gens.values() for c in v),
            "10 Killing vectors of dS4 (conformal chart) verified with symbolic H; none contains H")

    # structure constants: [A,B] expanded in the basis; check numeric (H-free) coefficients
    names = list(gens)
    def bracket(A, B):
        return [sp.expand(sum(A[l] * sp.diff(B[m], X[l]) - B[l] * sp.diff(A[m], X[l]) for l in range(4))) for m in range(4)]
    cs = sp.symbols("c0:10")
    struct = {}
    okH = True
    for i in range(10):
        for j in range(i + 1, 10):
            br = bracket(gens[names[i]], gens[names[j]])
            comb = [sum(cs[k] * gens[names[k]][m] for k in range(10)) for m in range(4)]
            eqs = []
            for m in range(4):
                poly = sp.Poly(sp.expand(br[m] - comb[m]), eta, x, y, z)
                eqs += poly.coeffs()
            sol = sp.solve(eqs, cs, dict=True)
            if not sol:
                okH = False; continue
            vec = [sol[0].get(c, 0) for c in cs]
            if any(Hs in sp.sympify(v).free_symbols for v in vec):
                okH = False
            struct[(i, j)] = vec
    C.check("G8b_structure_constants_H_free", okH and len(struct) == 45, "all 45 brackets close on the basis with H-free rational structure constants")
    # Killing form signature
    ad = []
    for i in range(10):
        Mi = sp.zeros(10, 10)
        for j in range(10):
            if i == j:
                continue
            vec = struct[(min(i, j), max(i, j))]
            sgn = 1 if i < j else -1
            for k2 in range(10):
                Mi[k2, j] = sgn * vec[k2]
        ad.append(Mi)
    Bk = sp.Matrix(10, 10, lambda i, j: (ad[i] * ad[j]).trace())
    ev = [complex(e).real for e in Bk.evalf().eigenvals(multiple=True)]
    npos = sum(1 for e in ev if e > 1e-9); nneg = sum(1 for e in ev if e < -1e-9)
    C.check("G8c_killing_form_so41", (npos, nneg) == (4, 6), f"Killing form signature (+{npos}, -{nneg}) = so(4,1) (non-compact 4, compact so(4) 6)")

    # ---------- static observer: a = H x/sqrt(1-x^2), T_loc = sqrt(a^2+H^2)/(2 pi) ------------------
    xx = sp.symbols("x", positive=True)
    f = 1 - xx**2
    acc = H * xx / sp.sqrt(f)  # a = H^2 r / sqrt(f), x = H r
    Tloc = (H / (2 * sp.pi)) / sp.sqrt(f)
    # own fix (first run FAILED): sympy cannot reduce sqrt(H^2/(1-x^2)) without x < 1; both sides are positive
    # for 0 < x < 1, so compare squares and add a numeric spot check.
    sq_ok = sp.simplify(Tloc**2 - (acc**2 + H**2) / (2 * sp.pi)**2) == 0
    spot = all(abs(float((Tloc - sp.sqrt(acc**2 + H**2) / (2 * sp.pi)).subs({H: 1.3, xx: xv}))) < 1e-14 for xv in (0.1, 0.5, 0.9, 0.999))
    C.check("G9_Tolman_equals_DeserLevin", sq_ok and spot,
            "T_loc = sqrt(a^2 + H^2)/(2 pi) exactly (squares equal, both positive; 4 spot values); T_U = T_Lambda at a = H (the only intrinsic scale)")

    # ---------- RAR offset in closed form -------------------------------------------------------------
    # nu(y) = 1/(1 - exp(-sqrt y)), y = g_N/a0, x = g/a0 = nu y. QUMOND offset c_Q = int 2 y (nu - 1) dy;
    # AQUAL offset c_A = int 2 x (1 - mu) dx with mu = 1/nu. Equal when (x - y)^2 -> 0 at both ends.
    cQ = mp.quad(lambda t: 4 * t**3 / mp.expm1(t), [0, 1, 10, 50, mp.inf])  # y = t^2
    def cA_integrand(t):
        y_ = t**2
        nu = 1 / (-mp.expm1(-t))
        x_ = nu * y_
        # dx/dt = d(nu y)/dt
        dnu = -mp.exp(-t) / (mp.expm1(-t))**2  # d nu / dt
        dxdt = dnu * y_ + nu * 2 * t
        return 2 * (x_ - y_) * dxdt
    cA = mp.quad(cA_integrand, [mp.mpf("1e-30"), 1, 10, 50, 200])
    closed = 4 * mp.pi**4 / 15
    C.check("G10_RAR_offset_closed_form", abs(cQ - closed) < mp.mpf("1e-40") and abs(cA - closed) < mp.mpf("1e-20"),
            f"c_QUMOND = {mp.nstr(cQ, 15)}, c_AQUAL = {mp.nstr(cA, 15)}, 4 pi^4/15 = {mp.nstr(closed, 15)}")
    C.value("RAR_offset_c", closed)
    C.value("RAR_Grho_over_a0sq", closed / (8 * mp.pi))
    C.check("G10b_RAR_W_is_pi3_over_30", abs(closed / (8 * mp.pi) - mp.pi**3 / 30) < mp.mpf("1e-50"),
            f"G rho/a0^2 = pi^3/30 = {mp.nstr(mp.pi**3/30, 10)} (lane G quotes 1.03): a Bose-Einstein integral, transcendental, never 4")

    # ---------- scope finding --------------------------------------------------------------------------
    # The headline 'no symmetry contains it' is broader than the tested set {dilatation, Conf(R^3)=so(4,1),
    # dS isometries + Casimirs, scale/trace Ward identities of the phi equation}. G-iii concerns the phi field
    # equation; G6b shows the full (gravity-coupled) action does see the constant.
    core = ["G1_kappa_from_a0_over_H", "G4_two_dimensionless_invariants", "G5b_dilatation_moves_vacuum",
            "G6_EL_blind_to_constant", "G8_ten_killing_fields_H_free", "G8b_structure_constants_H_free", "G9_Tolman_equals_DeserLevin",
            "G10_RAR_offset_closed_form"]
    step_false = not all(r["pass"] for r in C.rows if r["id"] in core)
    # headline_scope_ok: manual wording comparison (P/README.md:151 'no symmetry contains it' vs the tested set) -> False
    flags = {"step_false": step_false, "premise_unverified": False, "headline_scope_ok": False}
    return C.write({"flags": flags, "core": core})


if __name__ == "__main__":
    run_main(main)
