#!/usr/bin/env python3
"""CFG905: kappa door D5 -- a gauged carrier and the Festina Lente bound.

Criteria: FROZEN_CRITERIA.md (committed alone first, 9e3b6754e). Rules: CFG894 KAPPA_CAMPAIGN_RULES.md; door text
KAPPA_DOORS.md D5.

Question: gauge the record's carrier U(1), (Phi, X) -> (e^{i theta} Phi, e^{2 i theta} X). Festina Lente (FL; recalled form
m^2 >~ sqrt6 g q M_P H, reduced M_P; recalled, not re-read, nothing downloaded) then ties the charged states to the de Sitter
rate. If the same carrier also set K = G a0, would a pure-number kappa follow that is galaxy-mass independent, not pi-odd if
it is 1/2, and has a second independent prediction?

Method: sympy. K1 derives the ultracold Nariai field from the explicit Einstein-Maxwell-Lambda product metric (n = 2, 3).
Variants V1 (apply FL, no bridge), V2 (saturate FL + the unique hbar-free e-free carrier acceleration), V3 (FL's own
acceleration), V4 (FL geometry, excluded class X3, report only), V5 (gauge the baryon charge q_b instead). Measured H0 and
Omega_L enter only at the very end (report-only numbers).

Run:   OMP_NUM_THREADS=1 nice -n 10 python3 cfg905.py               -> cfg905.out, cfg905_results.json (exit 0 = checks pass)
       CFG905_MUTATE=1 OMP_NUM_THREADS=1 nice -n 10 python3 cfg905.py -> cfg905_MUTATE.out, cfg905_results_MUTATE.json
                                                                       (exit 1 = all teeth bite; 2 = VOID)
kappa = 1/2 is FITTED. Not theory closed.
"""
import json
import math
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("CFG905_MUTATE", "0") == "1"
OUT = os.path.join(HERE, "cfg905_MUTATE.out" if MUTATE else "cfg905.out")
JSN = os.path.join(HERE, "cfg905_results_MUTATE.json" if MUTATE else "cfg905_results.json")

LINES = []
CHECKS = {}


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LINES.append(s)


def check(name, ok, detail=""):
    CHECKS[name] = {"pass": bool(ok), "detail": str(detail)}
    say(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")


def z(expr):
    """True if a sympy expression simplifies to zero."""
    return sp.simplify(sp.expand(expr)) == 0


# ----------------------------------------------------------------------------------------------------------------------
# symbols
# ----------------------------------------------------------------------------------------------------------------------
G, c, hbar, rho = sp.symbols("G c hbar rho_DE", positive=True)          # SI
m, e, s, Nn, u = sp.symbols("m e s N u_star", positive=True)             # carrier mass, e = g q, saturation conv., map norm.
qb, Cs, b3 = sp.symbols("q_b C beta_3", positive=True)                   # force sector
Mpl, H, V, E, Mg = sp.symbols("M_P H V E M_grav", positive=True)        # natural-unit symbols (hbar = c = 1)
kk = sp.Symbol("k", real=True)
Rr, uu = sp.symbols("R u", positive=True)
x, w, n_e, y, zz = sp.symbols("x w n y z", real=True)                    # exponents
PI = sp.Symbol("PI", positive=True)                                      # pi tracker
eps = rho * c ** 2                                                       # vacuum energy density (SI)
law_unit = c * sp.sqrt(G * rho)                                          # c sqrt(G rho_DE) = sqrt(G eps)

# dimensions: (kg, m, s)
KG, MM, SS = sp.symbols("kg_ m_ s_", positive=True)
DIM = {G: MM ** 3 / (KG * SS ** 2), c: MM / SS, hbar: KG * MM ** 2 / SS, rho: KG / MM ** 3, m: KG,
       e: 1, s: 1, Nn: 1}


def dims(expr):
    return sp.simplify(sp.powsimp(expr.subs(DIM, simultaneous=True) / expr.subs({k: 1 for k in DIM}), force=True))


def pi_weight(expr):
    """pi exponent of a monomial r * pi^k (None if not a monomial in pi)."""
    ex = sp.simplify(expr).subs(sp.pi, PI)
    ex = sp.powsimp(sp.expand_power_base(ex, force=True), force=True)
    num, den = sp.fraction(sp.together(ex))
    try:
        kn = sp.Poly(num, PI)
        kd = sp.Poly(den, PI)
    except sp.PolynomialError:
        return None
    if len(kn.terms()) != 1 or len(kd.terms()) != 1:
        return None
    return kn.degree() - kd.degree()


# W_data (rules section 7): today's 2-sigma windows (no measured kappa is used anywhere)
W_DE = (0.227, 0.607)
W_CR = (0.189, 0.501)


def inwin(val, win):
    return win[0] <= val <= win[1]


# ----------------------------------------------------------------------------------------------------------------------
# K1 machinery: Einstein tensor of a diagonal metric
# ----------------------------------------------------------------------------------------------------------------------
def einstein_mixed_diag(coords, gd):
    D = len(coords)
    g = [sp.simplify(q) for q in gd]
    gi = [1 / q for q in g]
    Gam = [[[0] * D for _ in range(D)] for _ in range(D)]
    for a in range(D):
        for b in range(D):
            for cc in range(D):
                val = sp.Rational(1, 2) * gi[a] * (
                    (sp.diff(g[a], coords[b]) if a == cc else 0)
                    + (sp.diff(g[a], coords[cc]) if a == b else 0)
                    - (sp.diff(g[b], coords[a]) if b == cc else 0))
                Gam[a][b][cc] = sp.simplify(val)
    Ric = [[0] * D for _ in range(D)]
    for b in range(D):
        for d in range(D):
            val = 0
            for a in range(D):
                val += sp.diff(Gam[a][b][d], coords[a]) - sp.diff(Gam[a][b][a], coords[d])
                for ee in range(D):
                    val += Gam[a][a][ee] * Gam[ee][b][d] - Gam[a][d][ee] * Gam[ee][b][a]
            Ric[b][d] = sp.simplify(val)
    offdiag = all(z(Ric[i][j]) for i in range(D) for j in range(D) if i != j)
    Rs = sp.simplify(sum(gi[i] * Ric[i][i] for i in range(D)))
    Gmix = [sp.simplify(gi[i] * Ric[i][i] - Rs / 2) for i in range(D)]
    return Gmix, offdiag, Rs


def product_metric(nsph):
    t, xx = sp.symbols("t x", real=True)
    f = 1 - kk * xx ** 2
    angs = sp.symbols(" ".join(f"th{i}" for i in range(nsph)), real=True)
    if nsph == 1:
        angs = (angs,)
    coords = [t, xx] + list(angs)
    gd = [-f, 1 / f]
    pref = Rr ** 2
    for i in range(nsph):
        gd.append(pref)
        pref = pref * sp.sin(angs[i]) ** 2
    return coords, gd


def ultracold(nsph, Mcoef):
    """Einstein-Maxwell-Lambda on M2(k) x S^n(R): returns closed-form check, E_uc^2, u_uc = 1/R^2, neutral u."""
    coords, gd = product_metric(nsph)
    Gmix, offdiag, Rs = einstein_mixed_diag(coords, gd)
    G2_closed = -nsph * (nsph - 1) / (2 * Rr ** 2)
    GS_closed = (nsph - 1) / Rr ** 2 - kk - nsph * (nsph - 1) / (2 * Rr ** 2)
    ok_closed = offdiag and z(Gmix[0] - G2_closed) and z(Gmix[1] - G2_closed) and all(
        z(Gmix[i] - GS_closed) for i in range(2, 2 + nsph))
    # T^mu_nu: 2D part (-E^2/2 - V), sphere (E^2/2 - V); Einstein: Mcoef * G^mu_nu = T^mu_nu
    eq2 = sp.Eq(Mcoef * Gmix[0], -E ** 2 / 2 - V)
    eqS = sp.Eq(Mcoef * Gmix[2], E ** 2 / 2 - V)
    sub = {Rr: 1 / sp.sqrt(uu)}
    # ultracold: k = 0
    sol = sp.solve([eq2.subs(sub).subs(kk, 0), eqS.subs(sub).subs(kk, 0)], [E, uu], dict=True)
    sol = [d for d in sol if d[E].is_positive is not False and sp.simplify(d[uu]).is_positive is not False]
    Euc2 = sp.simplify(sol[0][E] ** 2)
    uuc = sp.simplify(sol[0][uu])
    # neutral Nariai: E = 0
    soln = sp.solve([eq2.subs(sub).subs(E, 0), eqS.subs(sub).subs(E, 0)], [kk, uu], dict=True)
    un = sp.simplify(soln[0][uu])
    kn = sp.simplify(soln[0][kk])
    return {"closed_form_ok": ok_closed, "Rs": Rs, "Euc2": Euc2, "u_uc": uuc, "u_neutral": un, "k_neutral": kn}


# ----------------------------------------------------------------------------------------------------------------------
# physics pieces used by both runs
# ----------------------------------------------------------------------------------------------------------------------
def m_sat_SI(s_, e_, Euc2_over_V=2):
    """FL saturation in SI: (m c^2)^4 = s^2 e^2 (Euc^2/V) (hbar c)^3 eps."""
    return (s_ ** 2 * e_ ** 2 * Euc2_over_V * (hbar * c) ** 3 * eps) ** sp.Rational(1, 4) / c ** 2


def a_FL(m_, e_, Gx=G):
    return sp.sqrt(Gx) * m_ ** 2 * c ** sp.Rational(5, 2) / (e_ * hbar ** sp.Rational(3, 2))


def kappa_V2(Gfac, Euc2_over_V=2):
    """V2: a0 = N a_FL with G_x = Gfac * G, at FL saturation; kappa = a0 / sqrt(G eps)."""
    a0 = Nn * a_FL(m_sat_SI(s, e, Euc2_over_V), e, Gfac * G)
    return sp.simplify(a0 / law_unit)


def run_normal():
    say("CFG905: kappa door D5 -- gauged carrier + Festina Lente (normal run)")
    say("criteria 9e3b6754e (FROZEN_CRITERIA.md)")
    say("kappa = 1/2 is FITTED (kappa_L 0.417 +- 0.095, CFG493 -- quoted, not used). Footings never pooled. Not theory closed.")
    say("FL form used (RECALLED, not re-read): m^2 >~ sqrt6 g q M_P H, M_P reduced (arXiv:1910.01648). K1 re-derives sqrt6.")
    say("")
    res = {"lane": "CFG905", "mode": "normal", "criteria": "9e3b6754e"}

    # ---------------- I1 self-grep
    say("== I1: self-grep for forbidden constants")
    src = open(os.path.abspath(__file__), encoding="utf-8").read()
    forb = ["9.36" + "e-11", "9.3603" + "e-11", "1.13" + "e-10", "1.1312" + "e-10", "1.2" + "e-10", "0.4" + "17",
            "0.4" + "5", "0.4" + "65", "0.5" + "3", "0.5" + "5", "0.5" + "51", "5.78" + "88", "0.17" + "27"]
    hits = []
    for val in forb:
        pat = r"(?<![\d.])" + re.escape(val) + r"(?![\d])"
        for ln, line in enumerate(src.splitlines(), 1):
            if re.search(pat, line):
                hits.append((val, ln))
    allowed = [(val, ln) for (val, ln) in hits if "quoted, not used" in src.splitlines()[ln - 1]]
    bad = [h_ for h_ in hits if h_ not in allowed]
    check("I1 no forbidden constants used", len(bad) == 0, f"hits outside the quoted standing-fact line: {bad}")
    say("")

    # ---------------- K1 ultracold Nariai field from the explicit metric
    say("== K1: Einstein-Maxwell-Lambda on M2(k) x S^n(R), explicit metric (Christoffel/Ricci), units M^(d-2) = M_grav")
    k1 = {}
    for nsph in (2, 3):
        r_ = ultracold(nsph, Mg)
        k1[nsph] = r_
        say(f"  n = {nsph} (d = {nsph + 2}): closed-form mixed Einstein components match: {r_['closed_form_ok']}; "
            f"E_uc^2 = {r_['Euc2']}; 1/R_uc^2 = {r_['u_uc']}; neutral Nariai 1/R^2 = {r_['u_neutral']}, k = {r_['k_neutral']}")
    nn = sp.Symbol("n", positive=True)
    Euc2_gen = 2 * V / (nn - 1)
    ok_gen = all(z(k1[q]["Euc2"] - Euc2_gen.subs(nn, q)) for q in (2, 3))
    noM = all(Mg not in k1[q]["Euc2"].free_symbols for q in (2, 3))
    Euc_d4 = sp.sqrt(k1[2]["Euc2"].subs(V, 3 * Mpl ** 2 * H ** 2))
    ok_sqrt6 = z(Euc_d4 - sp.sqrt(6) * Mpl * H)
    uuc_d4 = sp.simplify(k1[2]["u_uc"].subs({V: 3 * Mpl ** 2 * H ** 2, Mg: Mpl ** 2}))
    un_d4 = sp.simplify(k1[2]["u_neutral"].subs({V: 3 * Mpl ** 2 * H ** 2, Mg: Mpl ** 2}))
    check("K1 product geometry + ultracold field",
          all(k1[q]["closed_form_ok"] for q in (2, 3)) and ok_gen and noM and ok_sqrt6 and z(uuc_d4 - 6 * H ** 2)
          and z(un_d4 - 3 * H ** 2),
          f"E_uc^2 = 2V/(n-1) = 2V/(d-3) (no Planck-mass dependence: {noM}); d = 4, V = 3 M_P^2 H^2: E_uc = {Euc_d4} "
          f"(recalled sqrt6 reproduced: {ok_sqrt6}); 1/R_uc^2 = {uuc_d4}, neutral 1/R^2 = {un_d4}")
    res["K1"] = {str(q): {kk_: str(vv) for kk_, vv in k1[q].items()} for q in (2, 3)}
    say("  reading: FL is natively a bound on the vacuum energy V; G (or M_P) never enters it.")
    say("")

    # ---------------- K2 Schwinger saturation
    say("== K2: Schwinger saturation m^2 = e E  =>  proper acceleration e E / m")
    mm_ = sp.Symbol("m_nat", positive=True)
    Esat = mm_ ** 2 / e
    acc = sp.simplify(e * Esat / mm_)
    a_SI = m * c ** 3 / hbar
    check("K2 saturating charge accelerates at a = m (natural) = m c^3/hbar (SI)",
          z(acc - mm_) and z(dims(a_SI) - MM / SS ** 2), f"e E/m = {acc}; SI dims of m c^3/hbar = {dims(a_SI)}")
    say("")

    # ---------------- K3 FL V-form <-> H-form
    say("== K3: FL in V form and in H form (reduced M_P, Friedmann H^2 = V/(3 M_P^2))")
    m4_V = s ** 2 * e ** 2 * k1[2]["Euc2"]                      # m^4 = s^2 e^2 E_uc^2
    m4_H = (s * e * sp.sqrt(6) * Mpl * H) ** 2
    ok3 = z(m4_V - m4_H.subs(H, sp.sqrt(V / (3 * Mpl ** 2))))
    pw3 = pi_weight(m4_V / (s ** 2 * e ** 2 * V))
    check("K3 m^4 = 2 s^2 e^2 V, pi-free, M_P-free", ok3 and pw3 == 0 and Mpl not in m4_V.free_symbols,
          f"V form m^4 = {m4_V}; equals H form via Friedmann: {ok3}; pi-weight {pw3}")
    say("")

    # ---------------- K4 SI dimensions
    say("== K4: SI dimensions")
    lhs = (m * c ** 2) ** 4
    rhs = 2 * s ** 2 * e ** 2 * (hbar * c) ** 3 * eps
    d_l, d_r = dims(lhs), dims(rhs)
    d_aFL = dims(a_FL(m, e))
    check("K4 (mc^2)^4 = 2 s^2 e^2 (hbar c)^3 eps consistent; a_FL is an acceleration",
          z(d_l - d_r) and z(d_aFL - MM / SS ** 2), f"[lhs] = {d_l}, [rhs] = {d_r}, [a_FL] = {d_aFL}")
    say("")

    # ---------------- K5 dimensional theorem
    say("== K5: every acceleration from (m, e, hbar, c, G): a = m^x e^n hbar^y c^z G^w")
    mono = m ** x * hbar ** y * c ** zz * G ** w
    # exponent equations by hand from DIM: kg: x + y - w = 0; m: 2y + z + 3w = 1; s: -y - z - 2w = -2
    solx = sp.solve([sp.Eq(x + y - w, 0), sp.Eq(2 * y + zz + 3 * w, 1), sp.Eq(-y - zz - 2 * w, -2)], [x, y, zz], dict=True)[0]
    fam = (m ** x * hbar ** y * c ** zz * G ** w).subs(solx)
    fam_ok = z(dims(fam.subs(w, sp.Rational(3, 7))) - MM / SS ** 2) and z(dims(fam.subs(w, -2)) - MM / SS ** 2)
    say(f"  one-parameter family: x = {solx[x]}, y = {solx[y]}, z = {solx[zz]}  ->  a = (m c^3/hbar) (G m^2/(hbar c))^w "
        f"(dims verified at two w: {fam_ok}); e^n multiplies freely (dimensionless)")
    # FL saturation: m ∝ e^(1/2) hbar^(3/4) ...
    hbar_pow = sp.simplify(sp.Rational(3, 4) * solx[x] + solx[y])
    e_pow = sp.simplify(sp.Rational(1, 2) * solx[x] + n_e)
    sol_he = sp.solve([sp.Eq(hbar_pow, 0), sp.Eq(e_pow, 0)], [w, n_e], dict=True)
    uniq = len(sol_he) == 1 and sol_he[0][w] == sp.Rational(1, 2) and sol_he[0][n_e] == -1
    aFL_sat = sp.simplify(a_FL(m_sat_SI(s, e), e))
    ident = z(aFL_sat - sp.sqrt(2) * s * law_unit)
    check("K5 unique hbar-free, e-free carrier acceleration at FL saturation = sqrt2 s sqrt(G eps)",
          fam_ok and uniq and ident,
          f"hbar power at saturation = {hbar_pow} (zero iff w = 1/2); e power = {e_pow}; solution {sol_he}; "
          f"a_FL(m_sat) = {aFL_sat}  ( = sqrt2 s c sqrt(G rho_DE): {ident})")
    say("  reading: FL makes the carrier mass track the vacuum (m^4 ∝ e^2 eps), so the only hbar-free, e-free carrier")
    say("  acceleration IS the law's own unit c sqrt(G rho_DE) times a number. The number is the map's normalisation.")
    res["K5"] = {"family": str(fam), "hbar_power_at_sat": str(hbar_pow), "unique": str(sol_he), "a_FL_sat": str(aFL_sat)}
    say("")

    # ---------------- K6 binding charged state
    say("== K6: which charged state binds (Phi: q = 1, mass m; X: q = 2, mass M = 2 m sqrt(1 + u*^2))")
    eE = sp.Symbol("eE", positive=True)
    M2 = 4 * m ** 2 * (1 + u ** 2)
    slackX_at_Phi_sat = sp.simplify(M2.subs(m, sp.sqrt(s * eE)) - 2 * s * eE)
    msq = sp.Symbol("msq", positive=True)
    m2_at_X_sat = sp.solve(sp.Eq(4 * msq * (1 + u ** 2), 2 * s * eE), msq)[0]
    slackPhi_at_X_sat = sp.simplify(m2_at_X_sat - s * eE)
    okx = sp.simplify(slackX_at_Phi_sat - 2 * s * eE * (1 + 2 * u ** 2)) == 0
    okp = sp.simplify(slackPhi_at_X_sat + s * eE * (1 + 2 * u ** 2) / (2 * (1 + u ** 2))) == 0
    check("K6 Phi binds; X saturation would violate Phi's bound for every u* >= 0", okx and okp,
          f"X slack at Phi saturation = {slackX_at_Phi_sat} > 0; Phi slack at X saturation = {slackPhi_at_X_sat} < 0")
    say("")

    # ---------------- K7 gauge invariance
    say("== K7: gauge invariance of V_c and of D_mu with charges (1, 2)")
    Ph, Phc, X_, Xc, th, Dc, gc, lam, gg = sp.symbols("Phi Phic X Xc theta Delta_c g_c lambda g", positive=True)
    Vc = (m ** 2 * Ph * Phc + 4 * m ** 2 * X_ * Xc + (sp.sqrt(Dc) * X_ + gc / sp.sqrt(Dc) * Ph ** 2)
          * (sp.sqrt(Dc) * Xc + gc / sp.sqrt(Dc) * Phc ** 2) + lam * Ph ** 2 * Phc ** 2)
    rot = {Ph: sp.exp(sp.I * th) * Ph, Phc: sp.exp(-sp.I * th) * Phc, X_: sp.exp(2 * sp.I * th) * X_,
           Xc: sp.exp(-2 * sp.I * th) * Xc}
    okV = z(Vc.subs(rot, simultaneous=True) - Vc)
    xs = sp.Symbol("xs", real=True)
    phi_f, X_f, th_f, A_f = (sp.Function(nm)(xs) for nm in ("phi", "chi", "th", "A"))
    Dphi = lambda f_, A: sp.diff(f_, xs) - sp.I * gg * 1 * A * f_
    DX = lambda f_, A: sp.diff(f_, xs) - sp.I * gg * 2 * A * f_
    A_new = A_f + sp.diff(th_f, xs) / gg
    okD1 = z(Dphi(sp.exp(sp.I * th_f) * phi_f, A_new) - sp.exp(sp.I * th_f) * Dphi(phi_f, A_f))
    okD2 = z(DX(sp.exp(2 * sp.I * th_f) * X_f, A_new) - sp.exp(2 * sp.I * th_f) * DX(X_f, A_f))
    check("K7 the carrier U(1) is gaugeable (V_c invariant; covariant derivatives with q = 1, 2)", okV and okD1 and okD2,
          f"V_c invariant: {okV}; D Phi covariant: {okD1}; D X covariant: {okD2}. Gauging adds one massless hidden vector "
          "(H_g; not in the record).")
    say("")

    # ---------------- V1 apply FL, S_bridge = 0
    say("== V1: apply FL (inequality), no bridge. a0 from the force sector: a0 = K/G, K = q_b^3/(4 pi C^3 beta_3)")
    a0_rec = qb ** 3 / (4 * sp.pi * Cs ** 3 * b3 * G)
    kap_rec = sp.simplify(a0_rec / law_unit)
    dk = [sp.diff(kap_rec, v_) for v_ in (m, e, s)]
    check("K10 kappa independent of the carrier (m, e, s) when S_bridge = 0", all(z(d_) for d_ in dk),
          f"kappa_record = {kap_rec}: d/dm, d/de, d/ds = {dk}; free: {sorted(str(q) for q in kap_rec.free_symbols)}")
    say("  V1 output: the FL BOUND (m c^2)^4 >= 2 s^2 e^2 (hbar c)^3 eps_L on Phi (binding), weaker on X; and the same")
    say("  form for the record's messenger S under the photon. kappa is untouched -> class BOUND (kappa-free).")
    say("  If a map a0 = N a_FL existed, applying (not saturating) FL would give only kappa >= sqrt2 s N (a lower bound).")
    V1_class = "BOUND (kappa-free)"
    say("")

    # ---------------- V2 saturate + unique map
    say("== V2: saturate FL on Phi + a0 = N sqrt(G_x) m^2 c^(5/2)/(e hbar^(3/2)), G_x in {G, 4piG, 8piG}, s in {1, 1/pi}")
    kV2 = {"G": kappa_V2(1), "4piG": kappa_V2(4 * sp.pi), "8piG": kappa_V2(8 * sp.pi)}
    k2V2 = {kk_: sp.simplify(vv ** 2) for kk_, vv in kV2.items()}
    exp_k2 = {"G": 2 * s ** 2 * Nn ** 2, "4piG": 8 * sp.pi * s ** 2 * Nn ** 2, "8piG": 16 * sp.pi * s ** 2 * Nn ** 2}
    ok8 = all(z(k2V2[kk_] - exp_k2[kk_]) for kk_ in kV2)
    for kk_ in kV2:
        say(f"  G_x = {kk_:5s}: kappa = {kV2[kk_]},  kappa^2 = {k2V2[kk_]},  pi-weight {pi_weight(k2V2[kk_] / (s**2 * Nn**2))}, "
            f"free: {sorted(str(q) for q in kV2[kk_].free_symbols)}")
    nat = []
    for sname, sval in (("1", sp.Integer(1)), ("1/pi", 1 / sp.pi)):
        for kk_ in kV2:
            val = sp.simplify(kV2[kk_].subs({Nn: 1, s: sval}))
            k2 = sp.simplify(val ** 2)
            fv = float(val)
            nat.append({"s": sname, "G_x": kk_, "kappa": str(val), "kappa2": str(k2), "value": fv,
                        "pi_weight_kappa2": pi_weight(k2), "in_W_DE": inwin(fv, W_DE), "is_half": z(val - sp.Rational(1, 2))})
    say("  natural values (N = 1; report only; not a trial; never CONSISTENT/EXACT):")
    for d_ in nat:
        say(f"    s = {d_['s']:4s} G_x = {d_['G_x']:5s}: kappa = {d_['kappa']:>16s} = {d_['value']:.4f}  kappa^2 = {d_['kappa2']:>10s} "
            f"(pi-weight {d_['pi_weight_kappa2']})  in W_DE: {d_['in_W_DE']}  = 1/2: {d_['is_half']}")
    n_in = sum(d_["in_W_DE"] for d_ in nat)
    n_half = sum(d_["is_half"] for d_ in nat)
    N_half = {sn: sp.simplify(sp.solve(sp.Eq(kV2["G"].subs(s, sv), sp.Rational(1, 2)), Nn)[0])
              for sn, sv in (("1", 1), ("1/pi", 1 / sp.pi))}
    say(f"  natural menu: {n_in}/6 inside W_DE, {n_half}/6 at 1/2. kappa = 1/2 needs N = {N_half['1']} (s = 1) or "
        f"{N_half['1/pi']} (s = 1/pi): a posit, fixed by nothing in FL, the carrier action or the record.")
    pd = sp.Symbol("p_dm3", positive=True)                       # p = d - 3 > 0
    dd = sp.Symbol("d", positive=True)
    k2_d = sp.simplify(sp.simplify(kappa_V2(1, Euc2_over_V=2 / pd) ** 2).subs(pd, dd - 3))
    say(f"  general d (FL V form m^4 = s^2 e^2 * 2V/(d-3)): G-normalised kappa^2 = {k2_d}; d = 4, 5, 6: "
        f"{[sp.simplify(k2_d.subs(dd, q)) for q in (4, 5, 6)]}")
    d_quarter = sp.solve(sp.Eq(k2_d.subs({Nn: 1, s: 1}), sp.Rational(1, 4)), dd)
    say(f"  S3 disclosure: at N = 1, s = 1 the G-normalised kappa^2 = 1/4 only at d = {d_quarter} -- a dimension choice, "
        "void under S3; DO NOT CITE.")
    check("K8 V2 kappa^2 = 2 s^2 N^2 x {1, 4pi, 8pi}; general-d form", ok8 and z(k2_d.subs(dd, 4) - exp_k2["G"]),
          f"kappa^2 = {k2V2}")
    V2_class = "TRADE (N free; s and G_x conventions; natural values report only)"
    res["V2"] = {"kappa": {kk_: str(vv) for kk_, vv in kV2.items()}, "kappa2": {kk_: str(vv) for kk_, vv in k2V2.items()},
                 "natural": nat, "natural_in_W_DE": n_in, "natural_at_half": n_half,
                 "N_for_half": {kk_: str(vv) for kk_, vv in N_half.items()}, "kappa2_general_d_G": str(k2_d),
                 "class": V2_class}
    say("")

    # ---------------- V3 FL's own acceleration
    say("== V3: a0 = e E_uc / m at saturation = m c^3/hbar")
    a3 = sp.simplify(m_sat_SI(sp.Integer(1), e) * c ** 3 / hbar)
    hp3 = sp.simplify(hbar * sp.diff(a3, hbar) / a3)
    k3 = sp.simplify(a3 / law_unit)
    check("K11 V3 is hbar-bearing (wall 3)", hp3 == sp.Rational(-1, 4),
          f"a = {a3}; d ln a/d ln hbar = {hp3}; kappa_V3 = {k3} (depends on hbar, e)")
    V3_class = "NO SOLUTION (hbar-bearing)"
    say("")

    # ---------------- V4 FL geometry (excluded class X3)
    say("== V4 (EXCLUDED-CLASS POSIT, X3; report only): geometric accelerations of the FL solutions")
    eta = sp.Symbol("eta", positive=True)                          # Einstein coupling: M_P^2 = 1/(eta G), eta = 8 pi
    V4 = v4_values(k1, eta)
    for kk_, vv in V4.items():
        say(f"  {kk_}: kappa^2 = {vv}  (eta = 8pi: {sp.simplify(vv.subs(eta, 8*sp.pi))} = "
            f"{float(sp.sqrt(vv.subs(eta, 8*sp.pi))):.4f}, pi-weight {pi_weight(vv.subs(eta, 8*sp.pi))})")
    v4n = {kk_: sp.simplify(vv.subs(eta, 8 * sp.pi)) for kk_, vv in V4.items()}
    ok9a = z(v4n["ultracold c^2/R"] - 16 * sp.pi) and z(v4n["neutral Nariai c^2/R"] - 8 * sp.pi)
    # V5 sign
    r_, Mb_ = sp.symbols("r M_b", positive=True)
    phi_s = -qb * Mb_ / (4 * sp.pi * Cs * r_)
    lap = sp.simplify(sp.diff(r_ ** 2 * sp.diff(phi_s, r_), r_) / r_ ** 2)
    flux = sp.simplify(4 * sp.pi * r_ ** 2 * Cs * sp.diff(phi_s, r_))      # C grad(phi) flux = q_b M_b
    g_scalar = sp.simplify(-qb * sp.diff(phi_s, r_))                    # radial component of g_s = -q_b grad(phi)
    A0 = qb * Mb_ / (4 * sp.pi * r_)                                    # Gauss law vector potential, E = -grad A0
    Er = sp.simplify(-sp.diff(A0, r_))
    g_vector = sp.simplify(qb * Er)                                     # force per unit mass on a like-charged baryon
    ok9b = z(lap) and z(flux - qb * Mb_) and bool(sp.simplify(g_scalar).is_negative) and bool(
        sp.simplify(g_vector).is_positive)
    check("K9 V4 values pi-odd; V5 sign (record scalar force attracts, a gauged baryon charge repels)", ok9a and ok9b,
          f"V4 kappa^2 = {v4n}; record g_r = {g_scalar} (attractive), vector g_r = {g_vector} (repulsive)")
    V5_class = "NO SOLUTION (sign)"
    res["V4"] = {kk_: str(vv) for kk_, vv in v4n.items()}
    say("")

    # ---------------- I2 dependence
    say("== I2: symbolic kappa and its free constants per variant")
    dep = {"V1 (record, S_bridge = 0)": kap_rec, "V2 G": kV2["G"], "V2 4piG": kV2["4piG"], "V2 8piG": kV2["8piG"],
           "V3": k3}
    for kk_, vv in dep.items():
        say(f"  {kk_}: kappa = {vv}; depends on {sorted(str(q) for q in vv.free_symbols)}")
    check("I2 no graded variant gives a constant-free kappa", all(len(vv.free_symbols) > 0 for vv in dep.values()),
          "V1: q_b, C, beta_3, G, c, rho (TRADE, the record's own status); V2: N, s (TRADE); V3: hbar, e (NO SOLUTION)")
    say("")

    # ---------------- I3 scaling
    say("== I3: scaling G -> lam G, rho -> mu rho, c -> nu c at saturation (V2)")
    lam_, mu_, nu_ = sp.symbols("lambda_s mu_s nu_s", positive=True)
    a0V2 = Nn * a_FL(m_sat_SI(s, e), e)
    a0sc = a0V2.subs({G: lam_ * G, rho: mu_ * rho, c: nu_ * c}, simultaneous=True)
    ratio = sp.simplify(a0sc / a0V2)
    k_sc = sp.simplify(a0sc / law_unit.subs({G: lam_ * G, rho: mu_ * rho, c: nu_ * c}, simultaneous=True))
    check("I3 a0 -> nu sqrt(lam mu) a0, kappa invariant", z(ratio - nu_ * sp.sqrt(lam_ * mu_)) and z(k_sc - kV2["G"]),
          f"ratio = {ratio}; kappa after scaling = {k_sc}")
    say("")

    # ---------------- I4 rename test
    say("== I4: rename test (law's kappa set to 2/5)")
    kl = sp.Rational(2, 5)
    N_req = {sn: sp.simplify(kl / (sp.sqrt(2) * sv)) for sn, sv in (("1", 1), ("1/pi", 1 / sp.pi))}
    N_req_half = {sn: sp.simplify(sp.Rational(1, 2) / (sp.sqrt(2) * sv)) for sn, sv in (("1", 1), ("1/pi", 1 / sp.pi))}
    moved = all(not z(N_req[q] - N_req_half[q]) for q in N_req)
    nat_vals_unmoved = all(abs(d_["value"] - 0.4) > 1e-3 for d_ in nat)
    say(f"  required N follows the law's kappa: {N_req} (was {N_req_half} at 1/2) -> a consistency relation, not a derivation")
    say(f"  natural values do not move with the law's kappa, and none equals 0.4: {nat_vals_unmoved}")
    say("  V1 bound unchanged (kappa-free).")
    check("I4 rename test", moved and nat_vals_unmoved, "V2 is a consistency relation in N; natural values are not")
    say("")

    # ---------------- I5 Friedmann tautology
    say("== I5: no Friedmann tautology")
    check("I5 V2 G-normalised kappa uses FL's V form only (no Friedmann); not Z^2 = 32pi/3",
          z(k2V2["G"] - 2 * s ** 2 * Nn ** 2) and not z(k2V2["G"] - sp.Rational(32, 3) * sp.pi),
          "kappa^2 = 2 s^2 N^2 from m^4 = 2 s^2 e^2 V and the posited map; the H form (K3) used Friedmann once")
    say("")

    # ---------------- I6, I7, I8
    say("== I6/I7/I8: footing, hbar, pi-weights")
    check("I6 declared footing rho_DE only (FL with V = eps_L); rho_crit reported separately", True,
          "rho_crit reading: FL with today's H0 (V = rho_crit c^2) gives the same kappa formula on that footing; "
          "with H_L, kappa_crit = kappa_L sqrt(Omega_L). Never pooled.")
    hp_aFL = sp.simplify(hbar * sp.diff(a_FL(m, e), hbar) / a_FL(m, e))
    hp_sat = sp.simplify(hbar * sp.diff(aFL_sat, hbar) / aFL_sat)
    check("I7 hbar bookkeeping", hp_aFL == sp.Rational(-3, 2) and hp_sat == 0 and hp3 == sp.Rational(-1, 4),
          f"a_FL at fixed m: hbar^{hp_aFL}; at FL saturation: hbar^{hp_sat}; V3: hbar^{hp3}; no Bekenstein-Hawking 1/4")
    pws = {"V2 G": pi_weight(k2V2['G'] / (s**2 * Nn**2)), "V2 4piG": pi_weight(k2V2['4piG'] / (s**2 * Nn**2)),
           "V2 8piG": pi_weight(k2V2['8piG'] / (s**2 * Nn**2)),
           "V4 ultracold": pi_weight(v4n["ultracold c^2/R"]), "V4 neutral": pi_weight(v4n["neutral Nariai c^2/R"]),
           "a0 = c H_L": pi_weight(v4n["a0 = c H_L"])}
    check("I8 pi-weights as declared", pws == {"V2 G": 0, "V2 4piG": 1, "V2 8piG": 1, "V4 ultracold": 1,
                                               "V4 neutral": 1, "a0 = c H_L": 1}, f"{pws}")
    say("")

    # ---------------- numbers (end only)
    say("== Report-only numbers (measured H0 = 67.4 km/s/Mpc, Omega_L = 0.685 enter here only)")
    num = numbers()
    for kk_, vv in num.items():
        say(f"  {kk_}: {vv}")
    rt = num["roundtrip m_sat(e_sat(1 MeV)) [MeV]"]
    check("K12 numbers finite and self-consistent", abs(rt - 1.0) < 1e-9 and all(
        (isinstance(vv, float) and math.isfinite(vv)) or not isinstance(vv, float) for vv in num.values()),
        f"roundtrip = {rt}")
    res["numbers"] = num
    say("")

    # ---------------- classification
    say("== Classification (frozen section 9)")
    allpass = all(v_["pass"] for v_ in CHECKS.values())
    classes = {"V1": V1_class, "V2": V2_class, "V3": V3_class, "V4": "EXCLUDED-CLASS POSIT (X3)", "V5": V5_class}
    for kk_, vv in classes.items():
        say(f"  {kk_}: {vv}")
    graded_determinate = False                 # V1 kappa-free, V2 N free, V3 hbar-bearing, V5 sign
    label = "VOID" if not allpass else ("CLOSURE" if not graded_determinate else "CONSISTENT (not significant)")
    say(f"  checks: {sum(v_['pass'] for v_ in CHECKS.values())}/{len(CHECKS)} PASS")
    say(f"  OVERALL: {label}.  p_exact = 0, p_data = 0 (no determinate graded value).")
    say(f"  naive (menu) figure, report only: natural N = 1 menu {n_in}/6 in W_DE, {n_half}/6 at 1/2.")
    say("  Door questions: (i) pure number: NO (N free); (ii) galaxy-mass independent: yes, trivially (nothing galactic")
    say("  enters); (iii) pi: pi-free only for the G-normalised map = premise A; pi-odd for 4piG/8piG; (iv) second")
    say("  prediction: NO (carrier mass at saturation depends on the free e; unobserved field).")
    say("  kappa = 1/2 stays FITTED. Not theory closed.")
    res.update({"classes": classes, "label": label, "p_exact": 0, "p_data": 0, "checks": CHECKS,
                "n_checks": len(CHECKS), "n_pass": sum(v_["pass"] for v_ in CHECKS.values())})
    return res, (0 if allpass else 2)


def v4_values(k1, eta):
    """kappa^2 of geometric posits with Einstein coupling eta (M_P^2 = 1/(eta G)); H_L^2 = V/(3 M_P^2) = eta G V/3."""
    Gn, Vv = sp.symbols("G_n V_v", positive=True)
    MP2 = 1 / (eta * Gn)
    out = {}
    u_uc = k1[2]["u_uc"].subs({Mg: MP2, V: Vv})
    u_n = k1[2]["u_neutral"].subs({Mg: MP2, V: Vv})
    H2 = Vv / (3 * MP2)
    out["ultracold c^2/R"] = sp.simplify(u_uc / (Gn * Vv))           # a0^2 = u (natural c = 1), kappa^2 = a0^2/(G V)
    out["neutral Nariai c^2/R"] = sp.simplify(u_n / (Gn * Vv))
    out["a0 = c H_L"] = sp.simplify(H2 / (Gn * Vv))
    return out


def numbers():
    Gv, cv, hv, eV = 6.67430e-11, 299792458.0, 1.054571817e-34, 1.602176634e-19
    Mpc = 3.0856775814913673e22
    H0 = 67.4e3 / Mpc
    OL = 0.685
    rho_c = 3 * H0 ** 2 / (8 * math.pi * Gv)
    rho_L = OL * rho_c
    eps_L = rho_L * cv ** 2
    hc = hv * cv
    eps14 = (eps_L * hc ** 3) ** 0.25 / eV
    unit = cv * math.sqrt(Gv * rho_L)
    MPred = math.sqrt(hc / (8 * math.pi * Gv)) * cv ** 2 / eV

    def msat(ee, ss=1.0, epsv=eps_L):
        return (2 * ss ** 2 * ee ** 2 * hc ** 3 * epsv) ** 0.25        # J

    def esat(mJ, ss=1.0):
        return mJ ** 2 / (math.sqrt(2) * ss * hc ** 1.5 * math.sqrt(eps_L))

    e_em = 0.303
    m1 = 1e6 * eV
    mp = 938.272e6 * eV
    ms03 = msat(e_em)
    a3 = (ms03 / hv) * cv
    mkg = m1 / cv ** 2
    aFL_bench = math.sqrt(Gv) * mkg ** 2 * cv ** 2.5 / (e_em * hv ** 1.5)
    coul_grav = e_em ** 2 * hc / (4 * math.pi * Gv * (ms03 / cv ** 2) ** 2)
    out = {
        "eps_L^(1/4) [eV]": eps14,
        "law unit c sqrt(G rho_DE) [m/s^2] (kappa-free)": unit,
        "reduced M_P [eV]": MPred,
        "m_sat (e = 0.303, s = 1) [eV]": ms03 / eV,
        "m_sat (e = 1, s = 1) [eV]": msat(1.0) / eV,
        "m_sat (e = 0.303, s = 1/pi) [eV]": msat(e_em, 1 / math.pi) / eV,
        "e_sat for the record benchmark m = 1 MeV (s = 1)": esat(m1),
        "roundtrip m_sat(e_sat(1 MeV)) [MeV]": msat(esat(m1)) / eV / 1e6,
        "V1 benchmark slack in mass at e = 0.303 (1 MeV / m_sat)": m1 / ms03,
        "messenger S (10 MeV) slack in mass, photon e = 0.303": 1e7 * eV / ms03,
        "baryon-charge g_max for the proton (s = 1)": esat(mp),
        "V3 a = m_sat c^3/hbar (e = 0.303) [m/s^2]": a3,
        "V3 ratio to the law unit": a3 / unit,
        "a_FL at benchmark (m = 1 MeV, e = 0.303) / law unit": aFL_bench / unit,
        "Coulomb/gravity between two saturating carriers (e = 0.303)": coul_grav,
        "rho_crit reading: m_sat (e = 0.303, V = rho_crit c^2) [eV]": msat(e_em, 1.0, rho_c * cv ** 2) / eV,
    }
    return out


# ----------------------------------------------------------------------------------------------------------------------
# MUTATE RUN
# ----------------------------------------------------------------------------------------------------------------------
def run_mutate():
    say("CFG905 MUTATE run (criteria 9e3b6754e section 6)")
    say("kappa = 1/2 is FITTED (kappa_L 0.417 +- 0.095, CFG493 -- quoted, not used). Not theory closed.")
    say("")
    teeth = {}
    k1 = {q: ultracold(q, Mg) for q in (2, 3)}
    base_k2 = sp.simplify(kappa_V2(1) ** 2)                               # 2 s^2 N^2

    # M1 non-reduced Planck mass in FL's H form
    say("== M1: FL H form with the NON-reduced Planck mass M_Pl^2 = 1/G (natural units); Friedmann H^2 = 8 pi G V/3")
    Gn = sp.Symbol("G_n", positive=True)
    m4_M1 = sp.simplify((s * e * sp.sqrt(6)) ** 2 * (1 / Gn) * (8 * sp.pi * Gn * V / 3))
    Euc2_over_V_M1 = sp.simplify(m4_M1 / (s ** 2 * e ** 2 * V))
    k2_M1 = sp.simplify(kappa_V2(1, Euc2_over_V=Euc2_over_V_M1) ** 2)
    r1 = sp.simplify(k2_M1 / base_k2)
    pw0, pw1 = pi_weight(base_k2 / (s ** 2 * Nn ** 2)), pi_weight(k2_M1 / (s ** 2 * Nn ** 2))
    teeth["M1 non-reduced M_P: pi returns, kappa^2 x 8pi"] = z(r1 - 8 * sp.pi) and pw0 == 0 and pw1 == 1
    say(f"  V form becomes m^4 = {m4_M1}; G-normalised kappa^2: {base_k2} -> {k2_M1} (x {r1}); pi-weight {pw0} -> {pw1}"
        f" -> {'BITES' if teeth['M1 non-reduced M_P: pi returns, kappa^2 x 8pi'] else 'DOES NOT BITE'}")

    # M2 Einstein coupling 8piG -> 4piG, consistently
    say("== M2: Einstein coupling eta: 8 pi -> 4 pi (M_P^2 = 1/(eta G) in FL and Friedmann alike)")
    eta = sp.Symbol("eta", positive=True)
    V4 = v4_values(k1, eta)
    Euc2_eta = k1[2]["Euc2"].subs(Mg, 1 / (eta * Gn))                     # M-free: unchanged
    k2_G_eta = {et: sp.simplify(kappa_V2(1, Euc2_over_V=sp.simplify(Euc2_eta / V)) ** 2) for et in (8 * sp.pi, 4 * sp.pi)}
    notmove = z(k2_G_eta[8 * sp.pi] - k2_G_eta[4 * sp.pi]) and z(k2_G_eta[8 * sp.pi] - base_k2)
    h_moves = all(z(sp.simplify(vv.subs(eta, 4 * sp.pi) / vv.subs(eta, 8 * sp.pi)) - sp.Rational(1, 2))
                  for vv in V4.values())
    teeth["M2 8piG -> 4piG: G-map unchanged, H-type halves"] = notmove and h_moves
    say(f"  FL V form E_uc^2 = {Euc2_eta} (no eta); G-normalised kappa^2 8pi/4pi: {k2_G_eta[8*sp.pi]} / {k2_G_eta[4*sp.pi]} "
        f"(must NOT move: {notmove})")
    for kk_, vv in V4.items():
        say(f"  {kk_}: kappa^2 {sp.simplify(vv.subs(eta, 8*sp.pi))} -> {sp.simplify(vv.subs(eta, 4*sp.pi))}")
    say(f"  -> {'BITES' if teeth['M2 8piG -> 4piG: G-map unchanged, H-type halves'] else 'DOES NOT BITE'}")

    # M3 d = 4 -> 5 using the explicit n = 3 metric
    say("== M3: d = 4 -> 5 (explicit S^3 product metric)")
    Euc2_5 = k1[3]["Euc2"]
    k2_5 = sp.simplify(kappa_V2(1, Euc2_over_V=sp.simplify(Euc2_5 / V)) ** 2)
    r3 = sp.simplify(k2_5 / base_k2)
    teeth["M3 d 4 -> 5: kappa^2 halves"] = z(r3 - sp.Rational(1, 2)) and pi_weight(k2_5 / (s ** 2 * Nn ** 2)) == 0
    say(f"  E_uc^2 = {Euc2_5}; G-normalised kappa^2 {base_k2} -> {k2_5} (x {r3}) -> "
        f"{'BITES' if teeth['M3 d 4 -> 5: kappa^2 halves'] else 'DOES NOT BITE'}")

    # M4 global U(1)
    say("== M4: drop the gauging (global U(1)): FL constrains gauge charges only")

    def fl_bound(gauged):
        return (2 * s ** 2 * e ** 2 * (hbar * c) ** 3 * eps) if gauged else None
    b_norm, b_mut = fl_bound(True), fl_bound(False)
    teeth["M4 global U(1): bound disappears"] = (b_norm is not None) and (b_mut is None)
    say(f"  gauged: (mc^2)^4 >= {b_norm}; global: {b_mut} -> V1 no bound, V2/V3 undefined -> "
        f"{'BITES' if teeth['M4 global U(1): bound disappears'] else 'DOES NOT BITE'}")
    say("")
    allbite = all(teeth.values())
    say(f"MUTATE: {sum(teeth.values())}/{len(teeth)} teeth bite -> {'exit 1 (by design)' if allbite else 'VOID (exit 2)'}")
    say("The overall label of the normal run is not changed by a MUTATE run.")
    return {"lane": "CFG905", "mode": "MUTATE", "teeth": teeth, "all_bite": allbite,
            "M1_kappa2": str(k2_M1), "M2_kappa2_G": {str(kk_): str(vv) for kk_, vv in k2_G_eta.items()},
            "M3_kappa2": str(k2_5)}, (1 if allbite else 2)


if __name__ == "__main__":
    if MUTATE:
        res, code = run_mutate()
    else:
        res, code = run_normal()
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write("\n".join(LINES) + "\n")
    with open(JSN, "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=1, default=str)
    sys.exit(code)
