#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cfg123_static -- the EXACT static spherically symmetric equations of the localised RR model (areal gauge), built by sympy from the covariant
field equation verified in A1, and turned into numerical ODE right-hand sides.

Metric ds^2 = -A dt^2 + B dr^2 + r^2 dOmega^2, perfect fluid T = diag(rho A, p B, ...), G = c = 1, r in units of the source scale h (rho-hat = 8 pi G rho).
State y = (A, B, p-hat, U, U', S, S').  On shell xi1 = lam S/6, xi2 = lam U/6, lam = m^2 h^2.
  E_tt = rho-hat A,  E_rr = p-hat B,  box S = -U,  box U = -R,  R from the trace equation (verified in A1):
  R = [lam U (1 + U/3) - (lam/3) S' U'/B + rho-hat - 3 p-hat] / (1 - lam S/3),   p-hat' = -(rho-hat + p-hat) A'/(2A).
The theta-theta equation is NOT used (it follows from the Bianchi identity of A1); it is evaluated numerically as an independent residual check.
"""
import os, sys, math
import numpy as np
import sympy as sp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cfg123_geom as GM

_CACHE = {}


def build():
    if "b" in _CACHE:
        return _CACHE["b"]
    r, th, t = sp.symbols("r theta t", positive=True)
    lam, rh, ph = sp.symbols("lam rh ph")
    A = sp.Function("A")(r); B = sp.Function("B")(r); Uf = sp.Function("U")(r); Sf = sp.Function("S")(r)
    gm = sp.diag(-A, B, r ** 2, r ** 2 * sp.sin(th) ** 2)
    geo = GM.geometry(gm, [t, r, th, sp.Symbol("phic")])
    E = GM.E_RR(geo, lam, Uf, Sf, lam * Sf / 6, lam * Uf / 6)
    E = E.applyfunc(lambda e: sp.simplify(e.doit()))
    boxS = sp.simplify(GM.box(geo, Sf)); boxU = sp.simplify(GM.box(geo, Uf))
    a, b, U, Up, S, Sp, ap, bp, Spp, Upp, app = sp.symbols("a b U Up S Sp ap bp Spp Upp app")

    def sym(e):
        e = e.subs(sp.Derivative(A, (r, 2)), app).subs(sp.Derivative(Sf, (r, 2)), Spp).subs(sp.Derivative(Uf, (r, 2)), Upp)
        e = e.subs(sp.Derivative(A, r), ap).subs(sp.Derivative(B, r), bp).subs(sp.Derivative(Sf, r), Sp).subs(sp.Derivative(Uf, r), Up)
        e = e.subs({A: a, B: b, Uf: U, Sf: S})
        return e

    Ett, Err, Ethth = sym(E[0, 0]), sym(E[1, 1]), sym(E[2, 2])
    bS, bU = sym(boxS), sym(boxU)
    Spp_sol = sp.solve(sp.Eq(bS, -U), Spp)[0]
    eq1 = (Ett - rh * a).subs(Spp, Spp_sol)
    eq2 = (Err - ph * b).subs(Spp, Spp_sol)
    sol = sp.solve([eq1, eq2], [ap, bp], dict=True)[0]
    ap_e, bp_e = sp.simplify(sol[ap]), sp.simplify(sol[bp])
    F = 1 - lam * S / 3
    Rexpr = (lam * U * (1 + U / 3) - lam / 3 * Sp * Up / b + rh - 3 * ph) / F
    Upp_sol = sp.solve(sp.Eq(bU, -Rexpr), Upp)[0].subs({ap: ap_e, bp: bp_e})
    Spp_e = Spp_sol.subs({ap: ap_e, bp: bp_e})
    pp_e = -(rh + ph) * ap_e / (2 * a)
    y = [a, b, ph, U, Up, S, Sp]
    rhs = sp.Matrix([ap_e, bp_e, pp_e, Up, Upp_sol.subs({ap: ap_e, bp: bp_e}), Sp, Spp_e])
    out = dict(r=r, lam=lam, rh=rh, y=y, rhs=rhs, ap=ap_e, bp=bp_e, Ethth=Ethth, ph=ph, app=app,
               syms=dict(a=a, b=b, U=U, Up=Up, S=S, Sp=Sp, ap=ap, bp=bp, Spp=Spp, Upp=Upp), Rexpr=Rexpr)
    _CACHE["b"] = out
    return out


def numeric_rhs(lam_free=True):
    """lambdified rhs(r, y, lam, rh) -> array(7)."""
    b = build()
    args = [b["r"], *b["y"], b["lam"], b["rh"]]
    f = sp.lambdify(args, b["rhs"], modules="numpy", cse=True)
    return f


def numeric_rhs_and_jac():
    """rhs and the (7x7) jacobian wrt y and the lam-derivative (all lambdified with CSE); used for the O(lam) variational system."""
    b = build()
    args = [b["r"], *b["y"], b["lam"], b["rh"]]
    J = b["rhs"].jacobian(b["y"])
    Jl = b["rhs"].diff(b["lam"])
    g = b["ap"] / (2 * b["y"][0])
    return (sp.lambdify(args, b["rhs"], "numpy", cse=True), sp.lambdify(args, J, "numpy", cse=True), sp.lambdify(args, Jl, "numpy", cse=True),
            sp.lambdify(args, g, "numpy", cse=True), sp.lambdify(args, sp.Matrix([g]).jacobian(b["y"]), "numpy", cse=True),
            sp.lambdify(args, sp.diff(g, b["lam"]), "numpy", cse=True))


# ---------------------------------------------------------------------------------------------------------------- perturbative (tilde) form
def build_tilde():
    """The same system in rescaled variables  A = 1 + eps a~, B = 1 + eps b~, p-hat = eps^2 p~, U = eps U~, S = eps S~, rho-hat = eps rho~,
    with the powers of eps cancelled ALGEBRAICALLY (so there is no loss of precision at eps ~ 1e-9): T(r, y~; eps, lam, rho~) is valid for any eps,
    and eps = 0 IS the exact first-order-in-eps (linear) system.  Returns lambdified T, its jacobian, d/dlam, and g~ = A'/(2 A eps) with gradients."""
    if "t" in _CACHE:
        return _CACHE["t"]
    b0 = build()
    eps, rt = sp.symbols("eps rt")
    at, bt, pt, Ut, Utp, St, Stp = sp.symbols("at bt pt Ut Utp St Stp")
    S_ = b0["syms"]
    subs = {S_["a"]: 1 + eps * at, S_["b"]: 1 + eps * bt, b0["ph"]: eps ** 2 * pt, S_["U"]: eps * Ut, S_["Up"]: eps * Utp, S_["S"]: eps * St, S_["Sp"]: eps * Stp, b0["rh"]: eps * rt}
    scale = [eps, eps, eps ** 2, eps, eps, eps, eps]                         # y = 1_or_0 + scale * y~ ;  T_i = rhs_i / scale_i
    comps = []
    for i, e in enumerate(b0["rhs"]):
        num, den = sp.fraction(sp.together(e.subs(subs)))
        num = sp.expand(num)
        den = sp.expand(den)
        comps.append((num, den, scale[i]))
    out = []
    for num, den, sc in comps:
        q = sp.expand(num / sc)                                             # exact division (checked below)
        out.append((q, den))
    # verify divisibility: no negative powers of eps left
    for q, den in out:
        assert not any(term.has(1 / eps) or (sp.degree(sp.numer(sp.together(term)), eps) < 0) for term in [q]), "not divisible"
    T = sp.Matrix([q / den for q, den in out])
    # the p~ component: rhs_p / eps^2 with rhs_p = -(rh + ph) ap/(2a)
    yt = [at, bt, pt, Ut, Utp, St, Stp]
    args = [b0["r"], *yt, b0["lam"], eps, rt]
    T = T.applyfunc(lambda e: e)
    JT = T.jacobian(yt)
    TL = T.diff(b0["lam"])
    g = T[0] / (2 * (1 + eps * at))
    res = dict(T=sp.lambdify(args, T, "numpy", cse=True), JT=sp.lambdify(args, JT, "numpy", cse=True), TL=sp.lambdify(args, TL, "numpy", cse=True),
               g=sp.lambdify(args, g, "numpy", cse=True), gy=sp.lambdify(args, sp.Matrix([g]).jacobian(yt), "numpy", cse=True),
               gl=sp.lambdify(args, sp.diff(g, b0["lam"]), "numpy", cse=True), Tsym=T, Ethth=b0["Ethth"], b0=b0)
    _CACHE["t"] = res
    return res
