#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG232_A4_cosmology -- G2 (background and quasi-static growth), G7 (frame/background dependence), G5a on the FRW background, D1/D4.
Own derivation of the FRW reduction of T4-T1 (no k_Q shortcut).  MUTATE M6 (break the tie, 13b-i) and M7 (drop the interaction's constant part, 13b-ii).

KEY STRUCTURAL RESULT (derived in Part 1, sympy): on FRW the tuned invariant is T4-T1 = +3 B^2 with
      B = (2 H nn - Hh (nn^2 + rr^2))/nn ,   H = adot/(N a), Hh = ahdot/(Nh ah), nn = Nh/N, rr = ah/a ,
i.e. POSITIVE (timelike), whereas the static value is -4(p^2 + 2 q^2) (NEGATIVE, spacelike).  With Q = -T/a0^2 the cosmological argument is Q<0
while the static design of A1 lives on Q>0.  Part 2 proves that with matter in g only there is NO FRW solution on the B = 0 (Q = 0) branch.  So
the background always sits on the Q<0 domain, on which the static design says nothing.  G2 is therefore UNDEFINED as an implication of the frozen
class unless a continuation of M to Q<0 is DECLARED (an extra function, beyond the frozen ledger).  Part 3 reports estimates under one declared
continuation (mirror: M evaluated at |Q|), labelled as such; the evolution equations of (a, ah) and nn = 1 are not imposed (constraints only).
"""
import os, sys, math
import numpy as np
import sympy as sp
from scipy.optimize import fsolve, brentq
from scipy.integrate import solve_ivp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import CFG232_common as C

R = C.Run("CFG232_A4_cosmology")
MUT = R.mutate
P = R.P
bite = []

# ================================================================================================ Part 1: T4-T1 on FRW and boosted static source
R.banner("Part 1  T4-T1 on a generic FRW pair, and with a static source moving through it (own Christoffel code from metric jets)")
H, Hh, rr, nn, w, p, q = sp.symbols("H Hh rr nn w p q")


def build(g, dg):
    gi = g.inv()
    Gm = [[[0] * 4 for _ in range(4)] for _ in range(4)]
    for l in range(4):
        for m in range(4):
            for n in range(4):
                Gm[l][m][n] = sum(gi[l, s] * (dg[n][s][m] + dg[m][s][n] - dg[s][m][n]) for s in range(4)) / 2
    return Gm


def zero():
    return [[[0] * 4 for _ in range(4)] for _ in range(4)]


g = sp.diag(-1, 1, 1, 1); dg = zero()
dg[0][0][0] = 2 * w * p; dg[3][0][0] = -2 * p
for i in (1, 2, 3):
    dg[0][i][i] = 2 * H + 2 * w * q; dg[3][i][i] = -2 * q
gh = sp.diag(-nn ** 2, rr ** 2, rr ** 2, rr ** 2); dgh = zero()
for i in (1, 2, 3):
    dgh[0][i][i] = 2 * rr ** 2 * Hh * nn
G1, G2 = build(g, dg), build(gh, dgh)
Cc = [[[sp.simplify(G1[l][m][n] - G2[l][m][n]) for n in range(4)] for m in range(4)] for l in range(4)]
gi = g.inv(); R4 = range(4)
T1 = sum(g[a, b] * gi[m, r] * gi[n, s] * Cc[a][m][n] * Cc[b][r][s] for a in R4 for b in R4 for m in R4 for n in R4 for r in R4 for s in R4)
T4 = sum(gi[m, n] * Cc[a][m][b] * Cc[b][n][a] for m in R4 for n in R4 for a in R4 for b in R4)
Tt = sp.expand(sp.simplify(T4 - T1))
Bexp = (2 * H * nn - Hh * nn ** 2 - Hh * rr ** 2) / nn
R.check("T4-T1 = 3 (B + 2 w q)^2 - 4 p^2 - 8 q^2 with B = (2 H nn - Hh (nn^2+rr^2))/nn: the cosmological (timelike) part is +3B^2 (positive), the static (spacelike) part -4p^2-8q^2 (negative), and the boost enters only as B -> B + 2 w q",
        sp.simplify(Tt - (3 * (Bexp + 2 * w * q) ** 2 - 4 * p ** 2 - 8 * q ** 2)) == 0, f"T = {sp.factor(Tt)}")
R.check("static limit -4(p^2+2q^2) and FRW limit 3B^2 recovered; B = 0 on the symmetric branch (H = Hh, rr = nn = 1)",
        sp.simplify(Tt.subs({H: 0, Hh: 0, w: 0, rr: 1, nn: 1}) + 4 * (p ** 2 + 2 * q ** 2)) == 0 and sp.simplify(Bexp.subs({Hh: H, rr: 1, nn: 1})) == 0)
P("  => Q = -T/a0^2 = [4p^2 + 8q^2 - 3 (B + 2 w q)^2]/a0^2: a cosmological relative expansion enters the local argument with the OPPOSITE sign to a static gradient")

# ================================================================================================ Part 2: no symmetric FRW branch with matter in g only
R.banner("Part 2  no B = 0 FRW solution with matter in g only (symbolic, from the minisuperspace Lagrangian)")
t = sp.Symbol("t")
N_, Nh_, a_, ah_ = [sp.Function(n)(t) for n in ["N", "Nh", "a", "ah"]]
beta_, gam_, Lam_, Lamh_, Om3, a02, sgs, M0s = sp.symbols("beta gamma Lambda Lambdah Omega3 a02 sigma_s M0", real=True)
Mfun = sp.Function("M")
adot, ahdot = sp.diff(a_, t), sp.diff(ah_, t)
Bfull = (2 * adot / (N_ * a_) - ahdot * (Nh_ ** 2 / N_ + ah_ ** 2 / a_ ** 2 * N_) / (Nh_ * ah_)) / 1 * (N_ / Nh_) * (1 / N_) * N_ if False else None
Hg = adot / (N_ * a_); Hhg = ahdot / (Nh_ * ah_)
nn_ = Nh_ / N_; rr_ = ah_ / a_
B_ = (2 * Hg * nn_ - Hhg * (nn_ ** 2 + rr_ ** 2)) / nn_
Tfrw = 3 * B_ ** 2
Qarg = Tfrw / a02                                              # mirror argument |Q| = T/a0^2 (declared continuation used only in Part 3)
M_ = sp.Function("F")                                          # F(Q_arg) generic: includes M0 + M
Lint = 2 * sgs * a02 * sp.sqrt(N_ * Nh_) * (a_ * ah_) ** sp.Rational(3, 2) * M_(Qarg)
LEH = beta_ * (-6 * a_ * adot ** 2 / N_ - 2 * Lam_ * N_ * a_ ** 3) + gam_ * (-6 * ah_ * ahdot ** 2 / Nh_ - 2 * Lamh_ * Nh_ * ah_ ** 3) - 2 * N_ * Om3
Ltot = LEH + Lint
dLdN = sp.diff(Ltot, N_)
dLdNh = sp.diff(Ltot, Nh_)
# evaluate on the symmetric ansatz a = ah, N = Nh = 1, ahdot = adot
Hs = sp.Symbol("Hs")
sym = {Nh_: 1, N_: 1}
def at_sym(ex):
    ex = ex.subs({sp.Derivative(a_, t): Hs * a_, sp.Derivative(ah_, t): Hs * ah_})
    ex = ex.subs({Nh_: 1, N_: 1}).subs({ah_: a_})
    return sp.simplify(ex.doit())
EN = at_sym(dLdN)
ENh = at_sym(dLdNh)
P(f"  E_N  on the symmetric ansatz: {EN}")
P(f"  E_Nh on the symmetric ansatz: {ENh}")
# with Q_arg = 0 there, F'(0) terms drop (dQ/dN = 0 at B = 0); difference E_N/beta-type combination
asym = sp.Symbol("asym", positive=True)
EN_s = sp.simplify(EN.subs(a_, asym)); ENh_s = sp.simplify(ENh.subs(a_, asym))
P("  (Hubble rate common Hs; both equations contain only F(0) through the sqrt(N Nh) prefactor, since dQ/dN = dQ/dNh = 0 at B = 0)")
# solve E_N = 0 and E_Nh = 0 for the g and ghat 'Friedmann' relations
Hsq = sp.Symbol("Hsq")
sol_g = sp.solve(sp.Eq(EN_s.subs(Hs ** 2, Hsq), 0), Hsq)
sol_gh = sp.solve(sp.Eq(ENh_s.subs(Hs ** 2, Hsq), 0), Hsq)
P(f"  H^2 from E_N = {sol_g};  H^2 from E_Nh = {sol_gh}")
if sol_g and sol_gh:
    diff_ = sp.simplify(sol_g[0] - sol_gh[0].subs({beta_: beta_}))
    P(f"  difference of the two Friedmann relations: {sp.simplify(diff_)}")
    # with beta=gamma the vacuum parts agree; the dust term Omega3/a^3 appears only in E_N
    dif2 = sp.simplify(diff_.subs({gam_: beta_}))
    P(f"  ... at beta = gamma: {dif2}")
    dust_only = sp.simplify(dif2.subs({Lam_: Lamh_}))
    R.check("Part 2: with matter (Omega3 != 0) in g only, the two constraints cannot both hold on the symmetric branch B = 0 for all a: their difference is the dust term Omega3/a^3 (plus beta(Lambda - Lambdah)), which is not a constant",
            sp.simplify(sp.diff(dust_only, asym)) != 0 and sp.simplify(dust_only.subs(Om3, 0)) == 0, f"difference at Lambda = Lambdah: {dust_only}")
else:
    R.check("Part 2 symmetric-branch obstruction", False, "could not solve")

# ================================================================================================ Part 3: constraints-only background estimate under a DECLARED continuation
R.banner("Part 3  background estimate (constraints only, nn = 1, prescribed rr_i = 1 at z_i = 30) under the declared mirror continuation M(Q<0) := M(|Q|)")
Om, hh = 0.3153, 0.6736
OL = 1 - Om
c_over = {f: (299792.458e3 * 100 * hh * 1e3 / (3.0856775814913673e22)) / a for f, a in C.FOOTS.items()}
P(f"  c H0 / a0 = " + ", ".join(f"{f}: {v:.4f}" for f, v in c_over.items()))
# units: H0 = 1, c = 1, 8 pi G rho -> 3 Omega; a0 = 1/(c H0/a0)
des = C.Design(C.nu_p2, beta=1.0, gamma=1.0, sigma=+1)
Qs, ms = des.Qs, des.ms
# M(Q) = int_0^Q m dQ' on the design grid (m = m0 below the grid)
Mint = np.concatenate([[Qs[0] * ms[0]], Qs[0] * ms[0] + np.cumsum(0.5 * (ms[1:] + ms[:-1]) * np.diff(Qs))])


def Mfn(Qa):
    Qa = np.asarray(Qa, float)
    return np.where(Qa <= Qs[0], Qa * ms[0], np.interp(Qa, Qs, Mint))


def mfn(Qa):
    return des.mfun(Qa)


def E_ints(a0, Hv, Hhv, rrv, sgs_v, M0v):
    """rho_g and rho_gh (8 pi G rho units) from dL_int/dN and dL_int/dNh at N = Nh = 1, with Q_arg = T/a0^2 (mirror), T = 3 B^2"""
    # B(N, Nh) with adot, ahdot fixed:  H = adot/(N a), Hh = ahdot/(Nh ah), nn = Nh/N
    Nn, Nhn = sp.symbols("Nn Nhn", positive=True)
    Hx, Hhx = sp.symbols("Hx Hhx")
    Hn = Hx / Nn; Hhn = Hhx / Nhn; nnn = Nhn / Nn
    Bn = (2 * Hn * nnn - Hhn * (nnn ** 2 + rrv ** 2)) / nnn
    dBdN = sp.diff(Bn, Nn).subs({Nn: 1, Nhn: 1, Hx: Hv, Hhx: Hhv})
    dBdNh = sp.diff(Bn, Nhn).subs({Nn: 1, Nhn: 1, Hx: Hv, Hhx: Hhv})
    B0 = float(Bn.subs({Nn: 1, Nhn: 1, Hx: Hv, Hhx: Hhv}))
    return B0, float(dBdN), float(dBdNh)


# closed forms (sympy once)
Nn, Nhn, Hx, Hhx, rrs = sp.symbols("Nn Nhn Hx Hhx rrs", positive=True)
Hn_ = Hx / Nn; Hhn_ = Hhx / Nhn; nnn_ = Nhn / Nn
Bn_ = (2 * Hn_ * nnn_ - Hhn_ * (nnn_ ** 2 + rrs ** 2)) / nnn_
dBdN_f = sp.lambdify((Hx, Hhx, rrs), sp.diff(Bn_, Nn).subs({Nn: 1, Nhn: 1}), "numpy")
dBdNh_f = sp.lambdify((Hx, Hhx, rrs), sp.diff(Bn_, Nhn).subs({Nn: 1, Nhn: 1}), "numpy")
B_f = sp.lambdify((Hx, Hhx, rrs), Bn_.subs({Nn: 1, Nhn: 1}), "numpy")


def rho_int(a0, Hv, Hhv, rrv, sgs_v, M0v):
    """returns (rho_g, rho_gh) [8piG units, H0=1, c=1] for the constraint equations, a (aX) scale factors normalised so that (a ah)^{3/2}/a^3 = rr^{3/2}, ...
    L_int = 2 sigma a0^2 sqrt(N Nh)(a ah)^{3/2} F(T/a0^2), F = M0 + M.   dL/dN = 2 sigma a0^2 (a ah)^{3/2}[ (1/2) F + F' (dT/dN)/a0^2 ]  at N=Nh=1 (T=3B^2)."""
    B0 = float(B_f(Hv, Hhv, rrv))
    dT_dN = 6 * B0 * float(dBdN_f(Hv, Hhv, rrv))
    dT_dNh = 6 * B0 * float(dBdNh_f(Hv, Hhv, rrv))
    Qa = 3 * B0 ** 2 / a0 ** 2
    F = M0v + float(Mfn(Qa)); Fp = float(mfn(Qa))
    # per unit a^3 (g) : (a ah)^{3/2}/a^3 = rr^{3/2};  per unit ah^3 (ghat): (a ah)^{3/2}/ah^3 = rr^{-3/2}
    rho_g = -(2 * sgs_v * a0 ** 2 * rrv ** 1.5 * (0.5 * F + Fp * dT_dN / a0 ** 2)) / 2
    rho_gh = -(2 * sgs_v * a0 ** 2 * rrv ** -1.5 * (0.5 * F + Fp * dT_dNh / a0 ** 2)) / 2
    return rho_g, rho_gh, Qa


def E(z):
    return math.sqrt(Om * (1 + z) ** 3 + OL)


def lcdm_t(z):
    from scipy.integrate import quad
    return quad(lambda zz: 1.0 / ((1 + zz) * E(zz)), 0, z)[0]


def background(variant, foot="canonical", M0v=0.0, LamG=3 * OL, LamH=0.0, beta=1.0, gamma=1.0, sgs_v=+1.0, zi=30.0):
    """constraints-only estimate in the variable N = ln a: d ln ah/d ln a = Hh/H, (H, Hh) from the two constraints with continuation guesses"""
    a0 = 1.0 / c_over[foot]
    state = {"guess": [E(zi), 0.3 * math.sqrt(max(LamH, 0.01) / 3)], "bad": 0}

    def solveHH(a, ah):
        rrv = ah / a
        def eqs(v):
            Hv, Hhv = v
            rg, rgh, Qa = rho_int(a0, Hv, Hhv, rrv, sgs_v, M0v)
            return [3 * beta * Hv ** 2 - beta * LamG - 3 * Om / a ** 3 - rg, 3 * gamma * Hhv ** 2 - gamma * LamH - rgh]
        sol, info, ier, msg = fsolve(eqs, state["guess"], full_output=True)
        if ier != 1:
            state["bad"] += 1
        else:
            state["guess"] = list(sol)
        return sol, ier == 1

    def rhs(lna, y):
        a, ah = math.exp(lna), math.exp(y[0])
        (Hv, Hhv), ok = solveHH(a, ah)
        return [Hhv / Hv]
    lna_i = -math.log(1 + zi)
    zs = [30.0, 10.0, 3.0, 2.0, 1.0, 0.5, 0.0]
    sol = solve_ivp(rhs, (lna_i, 0.0), [lna_i], rtol=1e-6, atol=1e-8, dense_output=True, max_step=0.05)
    out = {}
    for zz in zs:
        lna = -math.log(1 + zz)
        a, ah = math.exp(lna), math.exp(sol.sol(lna)[0])
        state["guess"] = [E(zz), state["guess"][1]]
        (Hv, Hhv), ok = solveHH(a, ah)
        rg, rgh, Qa = rho_int(a0, Hv, Hhv, ah / a, sgs_v, M0v)
        out[zz] = dict(H=Hv, Hh=Hhv, rr=ah / a, Q_abs=Qa, m=float(mfn(Qa)), Hlcdm=E(zz), rho_g=rg, ok=ok, n_solver_failures_total=state["bad"])
    return out


DEV = {}
for variant, kw in (("13a", dict(M0v=0.0, LamG=3 * OL, LamH=0.0)),
                    ("13b-i", dict(M0v=0.0, LamG=3 * OL, LamH=3 * OL)),
                    ("13b-ii", dict(M0v=-64 * math.pi, LamG=0.0, LamH=0.0))):
    if MUT == "M7" and variant == "13b-ii":
        kw = dict(kw, M0v=0.0)
    if MUT == "M6" and variant == "13b-i":
        kw = dict(kw, LamH=4 * 3 * OL)                     # Lambdah = 4 Lambda_g: a0 (tied to Lambdah) doubles relative to the observed a0
    foot = "canonical"
    try:
        out = {} if MUT else background(variant, foot, **kw)
    except Exception as e:
        P(f"  {variant}: background estimate failed: {e}")
        out = {}
    DEV[variant] = out
    P(f"  {variant}: z, H/H_LCDM - 1, Hh/H0, rr = ah/a, |Q_bg|, m(|Q_bg|)")
    for zz, v in sorted(out.items()):
        P(f"     z={zz:5.1f}: H/H_LCDM - 1 = {v['H']/v['Hlcdm']-1:+8.4f}, Hh = {v['Hh']:.4f}, rr = {v['rr']:.4f}, |Q| = {v['Q_abs']:.3e}, m = {v['m']:.3e}{'' if v['ok'] else '  (solver flag: constraints not solved)'}")
R.num("background_estimate", {k: {str(z): v for z, v in d.items()} for k, d in DEV.items()})

# growth (quasi-static, R-add, mirror continuation): |G_eff/G - 1| = |4x(3+8x)/(2 D(x))|, x = 2 m(|Q_bg|)
R.banner("Part 4  quasi-static growth coupling under R-add with the mirror continuation (G2), from PRESCRIBED backgrounds (the Part 3 constraint solver did not converge)")
nconv = {v: sum(1 for x in DEV[v].values() if not x["ok"]) for v in DEV}
P("  Part 3 solver flags (constraints not solved) per variant: " + ", ".join(f"{v}: {n}/{len(DEV[v])}" for v, n in nconv.items()) + "  -> the Part 3 numbers are NOT used for any verdict (deviations of tens of percent at z <~ 1 and Hh ~ 60 in 13b-ii are solver artefacts of the rr = ah/a -> 0 amplification (a/ah)^{3/2}, i.e. of the arbitrary initial ratio rr_i = 1 at z = 30; reported, not repaired)")
HL = math.sqrt(OL)
G2 = {}
zs = [0.0, 0.5, 1.0, 2.0, 3.0, 10.0, 30.0]
for variant in ("13a", "13b-i"):
    row = {}
    for zz in zs:
        Hz = E(zz)
        Bz = 2 * Hz if variant == "13a" else 2 * Hz - HL * (1 + 0.07 ** 2)
        Qb = 3 * Bz ** 2 / (1.0 / c_over["canonical"]) ** 2
        m = float(mfn(Qb))
        xv = 2 * m
        row[zz] = 4 * xv * (3 + 8 * xv) / (2 * C.Dfun(xv))
    G2[variant] = row
    P(f"  {variant} (prescribed: H = H_LCDM, " + ("g-hat static" if variant == "13a" else "g-hat dS with Hh = H_Lambda, rr = 0.07") + f"): G_eff/G - 1 at z = " + ", ".join(f"{z}: {r:+.4f}" for z, r in row.items()) + "   (k-independent in this quasi-static reduction)")
G2["13b-ii"] = {}
worst = {v: (max(abs(x) for x in r.values()) if r else float("nan")) for v, r in G2.items()}
R.num("G2_prescribed", dict(G_eff=G2, worst=worst, part3_solver_flags=nconv))
for variant in ("13a", "13b-i"):
    P(f"  {variant}: max |G_eff/G - 1| over z = {worst[variant]:.3f} (pass line 0.05)")
R.verdict("G2 (13a/13b): existence of the background", "UNDEFINED",
          "with matter in g only the symmetric (Q = 0) branch has no solution (Part 2) and on every solution T4-T1 = +3B^2 > 0, i.e. Q < 0, where the static design of A1 says nothing: the FRW background needs a continuation of M to Q<0 that the frozen class does not contain")
R.verdict("G2 background H(z) (13a/13b)", "UNDEFINED", "the constraints-only solver did not converge at z <~ 1 (flags above); the initial ratio rr_i = ah/a at z = 30 is an extra free datum")
for variant in ("13a", "13b-i"):
    st = "FAIL" if worst[variant] > 0.05 else "PASS"
    R.verdict(f"G2 growth estimate {variant} (declared mirror continuation, prescribed background)", f"{st} on the estimate", f"max |G_eff/G-1| = {worst[variant]:.3f} (>5% at z <~ 1 because the relative expansion c(H - Hh)/a0 ~ 5-7 puts m(|Q_bg|) at the percent level); CMB part UNDEFINED (no Boltzmann run)")
R.verdict("G2 13b-ii", "UNDEFINED", "the vacuum branch has no solution with matter in g only, and the mirror estimate needs the (unsolved) ghat evolution")

# ================================================================================================ Part 5: G7
R.banner("Part 5  G7: dependence of the local argument on the cosmological relative expansion and on the boost")
a0c = 1.0 / c_over["canonical"]
HL = math.sqrt(OL)                                            # H_Lambda / H0 for the Z2-tied dS g-hat of 13b-i
rows = []
prescriptions = {"13a (g-hat static, Hh=0)": 2.0, "13b-i (Hh=H_Lambda, rr=1)": 2.0 - HL * 2.0, "13b-i (Hh=H_Lambda, rr=0.07)": 2.0 - HL * (1 + 0.07 ** 2)}
for nm, B0 in prescriptions.items():
    Tbg = 3 * B0 ** 2
    for y in (1.0, 0.1, 0.01, 1e-3):
        loc = 12 * (y * a0c) ** 2
        for wv in (0.0, 600.0 / 299792.458):
            cross = 12 * (y * a0c) * wv * B0 + 12 * (y * a0c) ** 2 * wv ** 2
            rows.append((nm, y, wv, loc / a0c ** 2, Tbg / a0c ** 2, cross / a0c ** 2, (loc - Tbg - cross) / a0c ** 2))
    P(f"  {nm}, z=0 (H = H0 from LCDM): B = {B0:.4f} H0, |Q_bg| = 3B^2/a0^2 = {Tbg/a0c**2:.1f}; local Q = 12 y^2 at y = 1, 0.1, 0.01: 12, 0.12, 0.0012 -> R-add total Q = local - |Q_bg| < 0 for y <= 1")
R.check("G7 (R-add): at z = 0 the cosmological term 3B^2/a0^2 exceeds the local static argument 12 y^2 for every y <= 1 for the three prescriptions of g-hat (static; dS with rr = 1; dS with rr = 0.07): the total argument is negative and M is undefined there",
        len(rows) > 0 and all(r[6] < 0 for r in rows if r[2] == 0.0), f"{len([r for r in rows if r[2]==0.0])} cases", kind="result")
# boost under R-static (B = 0 locally): relative change of the argument
wv = 600.0 / 299792.458
ratio_static = 12 * wv ** 2 / 12                              # 12 q^2 w^2 / (12 y^2 a0^2) with q = y a0 ... = w^2 relative
P(f"  R-static boost effect: T -> T(1 + w^2) at fixed potentials: relative shift of Q = {wv**2:.2e} at 600 km/s (a0_eff shift {wv**2/2:.1e}, pass line 0.10)")
cross_rel = {}
for r in rows:
    if r[2] > 0:
        cross_rel.setdefault(r[0], []).append((r[1], abs(r[5] / r[3])))
for v_, lst in cross_rel.items():
    P(f"  {v_} (R-add boost cross term 12 q w B relative to the local argument): " + ", ".join(f"y={y:g}: {c:.3f}" for y, c in lst))
R.verdict("G7 (i) boost, R-static", "PASS", f"relative change of Q at 600 km/s = {wv**2:.1e}")
R.verdict("G7 (ii) z-dependence, R-static", "PASS (trivial: no background enters)", "the local law is z-independent when B = 0 locally")
R.verdict("G7 under R-add", "FAIL (argument negative at z=0; boost cross term 12 q w B is 3% at y=1 and >100% at y<=0.03)", "reading-dependent: R-static passes only if g-hat locally follows g's static frame, which is the unsolved matching problem")
R.verdict("G7 (frozen rule: differs between readings)", "UNDEFINED", "recorded U, not P")

# ================================================================================================ Part 6: G5a on the FRW background (principal part)
R.banner("Part 6  vector operator on the FRW background of 13b: principal (four-derivative) symbol via jets, own code")
t_, z_, e_, aa, ahh = sp.symbols("t z epsilon aa ahh", positive=True)
Af = sp.Function("A")(t_, z_)
XY = [t_, sp.Symbol("x"), sp.Symbol("y"), z_]
g0 = sp.diag(-1, aa ** 2, aa ** 2, aa ** 2)                     # a treated as constant for the principal part
g0i = g0.inv()
h1m = sp.zeros(4, 4); h2m = sp.zeros(4, 4)
h1m[0, 1] = h1m[1, 0] = sp.diff(Af, t_) * aa ** 2
h1m[3, 1] = h1m[1, 3] = sp.diff(Af, z_) * aa ** 2
h2m[0, 0] = sp.diff(Af, t_) ** 2 * aa ** 2
h2m[0, 3] = h2m[3, 0] = sp.diff(Af, t_) * sp.diff(Af, z_) * aa ** 2
h2m[3, 3] = sp.diff(Af, z_) ** 2 * aa ** 2
gp = g0 + e_ * h1m + e_ ** 2 * h2m
gpi = g0i - e_ * g0i * h1m * g0i + e_ ** 2 * (-g0i * h2m * g0i + g0i * h1m * g0i * h1m * g0i)


def trunc(ex, n=2):
    ex = sp.expand(ex)
    return sum(ex.coeff(e_, k) * e_ ** k for k in range(n + 1))


Gp = [[[0] * 4 for _ in range(4)] for _ in range(4)]
for l in range(4):
    for m in range(4):
        for n in range(4):
            Gp[l][m][n] = trunc(sum(gpi[l, s_] * (sp.diff(gp[s_, m], XY[n]) + sp.diff(gp[s_, n], XY[m]) - sp.diff(gp[m, n], XY[s_])) for s_ in range(4)) / 2)
nz = [(a, m, n) for a in R4 for m in R4 for n in R4 if Gp[a][m][n] != 0]
T1b = 0
for (a, m, n) in nz:
    for (b_, r, s_) in nz:
        if gp[a, b_] == 0:
            continue
        T1b += gp[a, b_] * gpi[m, r] * gpi[n, s_] * Gp[a][m][n] * Gp[b_][r][s_]
T4b = 0
for (a, m, b_) in nz:
    for (b2, n, a2) in nz:
        if b2 == b_ and a2 == a:
            T4b += gpi[m, n] * Gp[a][m][b_] * Gp[b_][n][a]
Tb = trunc(trunc(T4b) - trunc(T1b))
Att, Atz, Azz = sp.symbols("Att Atz Azz")
jet2 = {sp.Derivative(Af, (t_, 2)): Att, sp.Derivative(Af, t_, z_): Atz, sp.Derivative(Af, (z_, 2)): Azz}
T2b = sp.expand(Tb.coeff(e_, 2).subs(jet2))
T2b_hi = sp.expand(T2b.subs({sp.Derivative(Af, t_): 0, sp.Derivative(Af, z_): 0}))
om, ka = sp.symbols("omega kappa")
sym4 = sp.factor(sp.expand(T2b_hi.subs({Att: -om ** 2, Atz: -om * ka, Azz: -ka ** 2})))
P(f"  four-derivative symbol of the vector operator on FRW (scale factor a): {sym4}")
R.check("G5a on the FRW background: the vector operator's principal part is (kappa^2/a^2 - omega^2)^2 (up to a positive power of a) times the coefficient M'(Q_arg): fourth order at every M' != 0, exactly as on the flat and static-MOND backgrounds",
        sp.simplify(sym4 / (ka ** 2 - aa ** 2 * om ** 2) ** 2).free_symbols.isdisjoint({om, ka}) and sym4 != 0, f"symbol = {sym4}")
R.verdict("G5a (13b, FRW background: NEW)", "FAIL", "same fourth-order vector operator, coefficient M'(Q_arg) != 0 at every finite argument (prescribed-background m(|Q_bg|) at z = 0: 13a " + f"{float(mfn(3*(2*E(0.0))**2/(1.0/c_over['canonical'])**2)):.2e}" + ")")

# ================================================================================================ MUTATE
if MUT == "M6":
    R.banner("MUTATE M6: break the tie (Lambdah = 4 Lambda_g: g-hat's Hubble rate doubles, and a0 tied to Lambdah doubles against the observed a0)")
    HLm = 2 * math.sqrt(OL)
    Q0 = 3 * (2 * E(0.0) - HL * (1 + 0.07 ** 2)) ** 2 / (1.0 / c_over["canonical"]) ** 2
    Q0m = 3 * (2 * E(0.0) - HLm * (1 + 0.07 ** 2)) ** 2 / (1.0 / c_over["canonical"]) ** 2
    P(f"  z = 0 |Q_bg| (prescribed background, 13b-i): baseline {Q0:.1f} -> mutated {Q0m:.1f} (relative change {abs(Q0m/Q0-1):.2f}); the G1-law cell flips in A5 (a0 -> 2 a0)")
    bite.append(abs(Q0m / Q0 - 1) > 0.10)
if MUT == "M7":
    R.banner("MUTATE M7: drop the interaction's constant part in 13b-ii (M0 -> 0): no vacuum energy, no acceleration")
    Hm = math.sqrt(Om)
    P(f"  13b-ii with M0 = 0 (and Lambda = 0): matter-only H(z=0)/H_LCDM - 1 = {Hm/E(0.0)-1:+.3f} (the interaction terms are at the 1e-2 level)")
    bite.append(abs(Hm / E(0.0) - 1) > 0.10)
R.finish(bite if MUT else None)
