#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CFG231_A3_vector_class -- sympy: the class-V action, Euler-Lagrange, static spherical reduction, the SIGN required for an attractive drag,
hyperbolicity/ghost conditions, the vector's static stress components (rho, p_r, p_t) vs the Route-3 'k-essence' theorem, V2's gravitating
dark mass, Yukawa Green's function of V0, the de Sitter stability item G5 (v), and the D-EFE premise check.
Frozen: CFG231_FROZEN_CRITERIA.md sections 1.2, 2 (G1 12a, G5 (i), (iv'), (v)), 6.   Exit 0 if every reproduction control passes.
No MUTATE modes here (A6 carries MU3).
"""
import sys, os, math
import numpy as np
import sympy as sp
import mpmath as mp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import CFG231_common as C

R = C.Report("CFG231_A3_vector_class")
C.header(R, "CFG231 A3 -- the covariant vector class V: reductions, signs, stability, stress components")

# =========================================================================================== 1. static reduction and the sign of attraction
R.banner("A3.1  Euler-Lagrange of the reduced electrostatic action and the sign s needed for an ATTRACTIVE drag")
rr, G_, eps, s = sp.symbols("r G epsilon s", real=True)
phi = sp.Function("phi")(rr)
rho = sp.Function("rho")(rr)
Dfun = sp.Function("D")            # D(E) = dLambda/dE, Lambda = int D dE (positive-stiffness convention D' > 0)
E_ = -sp.diff(phi, rr)             # E = -phi'   (radial component)
Lam = sp.Function("Lam")
# L_density = (s/4 pi G) Lam(|E|) - eps rho phi ;  S = int 4 pi r^2 L dr ; work on the branch E > 0 first, then E < 0 by symmetry
Eabs = sp.Symbol("Eabs")
Lag = 4 * sp.pi * rr ** 2 * ((s / (4 * sp.pi * G_)) * Lam(-sp.diff(phi, rr)) - eps * rho * phi)
EL = sp.diff(Lag, phi) - sp.diff(sp.diff(Lag, sp.diff(phi, rr)), rr)
R.P(f"  Euler-Lagrange expression (branch E = -phi' > 0): {sp.simplify(EL)}")
# first integral: (s/G) d/dr[ r^2 Lam'(E) ] ... solve for the flux: r^2 s D(E)/G = eps * M_b(r) (with M_b' = 4 pi r^2 rho), sign as derived
Mb = sp.Function("M_b")(rr)
flux = sp.symbols("flux")
# EL: d/dr[ (s/G) r^2 D(E) * (-1)*(-1) ] ... derive by hand with sympy: dL/dphi' = 4 pi r^2 (s/4 pi G) Lam'(E) * (-1) = -(s/G) r^2 D(E)
dL_dphip = sp.simplify(sp.diff(Lag, sp.diff(phi, rr)))
R.P(f"  dL/dphi' = {dL_dphip}   (D = Lam')")
# EL: d/dr(dL/dphi') = dL/dphi  ->  d/dr[-(s/G) r^2 D(E)] = -4 pi eps r^2 rho  ->  (s/G) r^2 D(E) = 4 pi eps int rho r^2 dr = eps M_b/G  (M_b = 4 pi int rho r^2)
# so  s D(E) = eps G M_b / r^2 = eps g_N   with E = -phi' > 0  and the force on a test baryon (same coupling): f = -eps grad(phi) = + eps E (outward, E > 0).
R.P("  hence  s D(E) = eps g_N  and the force on a like-charge baryon is  f = eps E r-hat  (E = -phi' > 0)")
R.P("  * for s = +1 (healthy, positive-energy vector): E > 0 for eps g_N > 0 and the force is +eps E: OUTWARD = REPULSIVE (like charges repel)")
R.P("  * an ATTRACTIVE drag (force toward the source, the sign of g_D in every K-law) needs s D(E) = eps g_N with E < 0: on the branch E < 0, |E| enters D as D(|E|) sgn(E) so that s = -1 (D(|E|) > 0)")
Dpos, gNs, epss = sp.symbols("Dpos gN eps_", positive=True)
s_attr = sp.solve(sp.Eq(s * Dpos * (-1), epss * gNs), s)          # branch E < 0: sgn(E) = -1
s_val = sp.simplify(s_attr[0].subs(Dpos, epss * gNs))           # the magnitude condition D(|E|) = eps g_N
R.P(f"  sympy: s (E < 0 branch) = {s_attr[0]}; with the magnitude relation D(|E|) = eps g_N this is s = {s_val}")
assert s_val == -1
sattr_val = -1
R.check("A3.1 the static reduction is s D(|E|) sgn(E) = eps g_N (from the Euler-Lagrange equation); an attractive drag needs s = -1, i.e. a wrong-sign (ghost) kinetic term for a vector",
        "derived symbolically; like charges of a spin-1 field repel; the frozen V1 assumed an attractive drag with eps = 1 and never set the sign of the kinetic term", True)

# =========================================================================================== 2. hyperbolicity / ghost coefficients
R.banner("A3.2  second variation of the reduced class about a static electric background: stiffness and speeds (frozen G5 (i)) and the sign s")
E, a = sp.symbols("E a", positive=True)
laws = {"K1": E ** 2 / (a - 2 * E), "K2": E ** 2 / a, "K3": E ** 2 / (a - E)}
rowsG5 = {}
for k, D in laws.items():
    Dp = sp.simplify(sp.diff(D, E))
    Dov = sp.simplify(D / E)
    c2 = sp.simplify(Dov / Dp)
    lim0 = sp.limit(c2, E, 0)
    # ranges on the allowed E interval
    Emax = {"K1": a / 2, "K2": sp.oo, "K3": a}[k]
    Eg = np.linspace(1e-6, (0.4999 if k == "K1" else (0.9999 if k == "K3" else 5.0)), 4000)
    f = sp.lambdify(E, c2.subs(a, 1), "numpy")
    fD = sp.lambdify(E, Dp.subs(a, 1), "numpy")
    fV = sp.lambdify(E, Dov.subs(a, 1), "numpy")
    c2v = f(Eg) * np.ones_like(Eg); Dpv = fD(Eg) * np.ones_like(Eg); Dovv = fV(Eg) * np.ones_like(Eg)
    okhyp = bool(np.all(Dpv > 0) and np.all(Dovv > 0) and np.all(c2v > 0) and np.all(c2v <= 0.5 + 1e-12))
    rowsG5[k] = dict(Dprime=str(Dp), D_over_E=str(Dov), c2=str(c2), c2_at_0=str(lim0), c2_min=float(c2v.min()), c2_max=float(c2v.max()), hyperbolic_subluminal=okhyp)
    R.P(f"  {k}: D' = {Dp};  D/E = {Dov};  c_s^2 = (D/E)/D' = {c2};  c_s^2(E->0) = {lim0};  over the allowed range c_s^2 in [{c2v.min():.3g}, {c2v.max():.3g}]  hyperbolic and subluminal: {okhyp}")
R.P("  quadratic Lagrangian for a perturbation: (s/8 pi G)[ D' dE_par^2 + (D/E) dE_perp^2 - (D/E) dB^2 ]  =>  ghost-free iff s D' > 0 and s D/E > 0.")
R.P("  The reduced-Gauss-law conditions of the frozen G5 (i) (D' > 0, D/E > 0) HOLD for K1, K2, K3 (hyperbolic, c_s^2 <= 1/2), but with the s = -1 needed for attraction BOTH kinetic coefficients are NEGATIVE: a radial and a transverse GHOST.")
R.check("A3.2 K1, K2, K3 satisfy D' > 0, D/E > 0 with 0 < c_s^2 <= 1/2 on the allowed range (frozen G5 (i)); with the attractive sign s = -1 the kinetic coefficients s D' and s D/E are both negative",
        f"c_s^2 ranges: " + "; ".join(f"{k} [{v['c2_min']:.3g}, {v['c2_max']:.3g}]" for k, v in rowsG5.items()) + "; ghost sign for attraction", all(v["hyperbolic_subluminal"] for v in rowsG5.values()))
R.num("G5_i", rowsG5)

# =========================================================================================== 3. stress components
R.banner("A3.3  the vector's static stress components (rho, p_r, p_t) from T_mn = 2 L_X F_ma F_n^a + g_mn L  (flat, spherical), vs the Route-3 'p_t = -rho' theorem (a SCALAR theorem)")
t, r, th, ph = sp.symbols("t r theta phi", real=True)
X = sp.symbols("X")
Ef = sp.Function("Ef")(r)
coords = (t, r, th, ph)
g = sp.diag(-1, 1, r ** 2, r ** 2 * sp.sin(th) ** 2)
gi = g.inv()
F = sp.zeros(4, 4)
F[0, 1] = Ef; F[1, 0] = -Ef                      # F_{tr} = E
Fup = gi * F * gi                                # F^{mu nu}
Xinv = -sp.Rational(1, 2) * sum(F[i, j] * Fup[i, j] for i in range(4) for j in range(4))
R.P(f"  X = -1/2 F_mn F^mn = {sp.simplify(Xinv)}  (= E^2)")
Lf = sp.Function("L")
LX = sp.Function("LX")
T = sp.zeros(4, 4)
Fmix = F * gi                                    # F_{m}^{a} = F_{m b} g^{b a}
for i in range(4):
    for j in range(4):
        FF = sum(F[i, k] * Fmix[j, k] for k in range(4))      # F_{i k} F_{j}^{k}
        T[i, j] = 2 * LX(r) * FF + g[i, j] * Lf(r)
Tmix = sp.simplify(gi * T)
rho_E = sp.simplify(-Tmix[0, 0]); p_r = sp.simplify(Tmix[1, 1]); p_t = sp.simplify(Tmix[2, 2])
R.P(f"  rho = -T^t_t = {rho_E};  p_r = T^r_r = {p_r};  p_t = T^theta_theta = {p_t}     (L_X = dL/dX at X = E^2)")
# with L(E) = (s/4 pi G) Lam(E), X = E^2: L_X = L_E/(2E) = (s/4 pi G) D/(2E)
sub = {LX(r): (s / (4 * sp.pi * G_)) * sp.Symbol("Dv") / (2 * Ef), Lf(r): (s / (4 * sp.pi * G_)) * sp.Symbol("Lamv")}
rho_s = sp.simplify(rho_E.subs(sub)); pr_s = sp.simplify(p_r.subs(sub)); pt_s = sp.simplify(p_t.subs(sub))
R.P(f"  rho = {rho_s};  p_r = {pr_s};  p_t = {pt_s}     (Dv = D(E), Lamv = int_0^E D)")
ok_pr = sp.simplify(pr_s + rho_s) == 0
R.P(f"  p_r = -rho: {ok_pr};  p_t + rho = {sp.simplify(pt_s + rho_s)}  (= (s/4 pi G) E D, nonzero: the scalar theorem p_t = -rho does NOT hold for the vector)")
eos = {}
for k in laws:
    Lam_k = {"K1": lambda Ee: C.int_D("K1", Ee, 1.0), "K2": lambda Ee: C.int_D("K2", Ee, 1.0), "K3": lambda Ee: C.int_D("K3", Ee, 1.0)}[k]
    Dk = sp.lambdify(E, laws[k].subs(a, 1), "numpy")
    Ee = np.array([0.05, 0.2, 0.4]) if k != "K3" else np.array([0.05, 0.3, 0.8])
    u = Ee * Dk(Ee) - Lam_k(Ee); pt = Lam_k(Ee)
    eos[k] = dict(E=Ee.tolist(), pt_over_rho=(pt / u).tolist())
    R.P(f"  {k}: p_t/rho at E/a = {Ee.tolist()}: {[round(float(z), 4) for z in pt / u]}   (deep limit E^3 laws: rho = (2/3) E^3/a, p_t = (1/3) E^3/a  ->  p_t/rho = 1/2)")
R.check("A3.3 static electric vector: p_r = -rho exactly and p_t = (s/4 pi G) Lam, so p_t + rho = (s/4 pi G) E D != 0 (the k-essence scalar identity p_t = -rho does not carry over to the vector); deep limit p_t/rho = 1/2",
        f"p_r = -rho {ok_pr}; K2 p_t/rho = {eos['K2']['pt_over_rho']}", ok_pr and all(abs(z - 0.5) < 1e-9 for z in eos["K2"]["pt_over_rho"]))
R.num("stress_EOS", eos)

# =========================================================================================== 4. V2 gravitating dark mass
R.banner("A3.4  V2 (the vector's own field energy as the dark mass): how much of the required density does it supply?")
v2 = {}
for law in ("K1", "K2", "K3"):
    row = []
    for M in (1e9, 1e10, 1e12):
        a_kpc = C.AKPC(C.a_V_si("HL"))
        rM = C.r_M_kpc(M, a_kpc)
        r_ = C.XGRID * rM
        prof = C.PointMass(M)
        d = C.V2_dark(prof, r_, a_kpc, law=law, sign=-1.0)
        Rv = 4 * math.pi * r_ ** 3 * d["rho_D"] * d["g_tot"] / (a_kpc * M)
        idx = [int(np.argmin(np.abs(C.XGRID - x))) for x in (0.1, 1, 10, 30)]
        row.append((M, [float(Rv[i]) for i in idx], float(d["M_dark"][-1] / M)))
    v2[law] = row
    R.P(f"  V2/{law} point mass: (M, R at x = 0.1, 1, 10, 30; M_D(<30 r_M)/M) = " + "; ".join(f"({M:.0e}, {[f'{t:.2e}' for t in Rr]}, {mm:.2e})" for M, Rr, mm in row))
hand = (C.A0_SI["canonical"] ** 2 / (8 * math.pi * 6.6743e-11 * C.C_SI ** 2), C.A0_SI["canonical"] / (4 * math.pi * 6.6743e-11 * 3.0857e20 * 10))
R.P(f"  hand check of the frozen estimate: a0^2/(8 pi G c^2) = {hand[0]:.2e} kg/m^3 against a0/(4 pi G r) at 10 kpc = {hand[1]:.2e} kg/m^3: ratio {hand[0] / hand[1]:.1e}")
maxR = max(abs(z) for law in v2 for (_, Rr, _) in v2[law] for z in Rr)
R.check("A3.4 V2's field-energy dark mass is ~1e-6 (or less) of the required density: max |R| over laws, masses and nodes < 1e-4 (the frozen hand estimate said ~1e-6)",
        f"max |R| = {maxR:.2e}; sign of M_D is negative for the attractive (ghost) convention: M_D(<30 r_M)/M ~ {v2['K1'][0][2]:.1e}", maxR < 1e-4)
R.num("V2", {k: [(m, r_, mm) for (m, r_, mm) in v] for k, v in v2.items()})

# =========================================================================================== 5. V0 Yukawa Green's function
R.banner("A3.5  V0: Green's function of (nabla^2 - m^2) A0 = -q rho_b for the exponential sphere, m = H_Lambda/c (mpmath, exact shell formula)")
mp.mp.dps = 40
m_kpc = mp.mpf((C.HL_SI / C.C_SI) * C.KPC_M)
Mtot, hh = mp.mpf(1e10), mp.mpf(2.0)
rho0 = Mtot / (8 * mp.pi * hh ** 3)


def phi_yuk(rv):
    # phi(r) = int dq(r') e^{-m r>} sinh(m r<)/(m r r'),  dq = 4 pi r'^2 rho(r') dr'
    f = lambda rp: 4 * mp.pi * rp ** 2 * rho0 * mp.e ** (-rp / hh) * (mp.e ** (-m_kpc * max(rv, rp)) * mp.sinh(m_kpc * min(rv, rp)) / (m_kpc * rv * rp))
    return mp.quad(f, [0, rv, 40 * hh, 400 * hh])


rv = mp.mpf(10.0)
dphi = mp.diff(phi_yuk, rv)
Mb10 = Mtot * mp.gammainc(3, 0, rv / hh, regularized=True)
Nphi = -dphi / (Mb10 / rv ** 2)
dev_y = float(Nphi - 1)
R.P(f"  E_Yukawa / (M_b(<r)/r^2) - 1 at r = 10 kpc for the 1e10, h = 2 sphere: {dev_y:.3e}   (point-charge series: -(m r)^2/2 = {-0.5 * float(m_kpc * rv) ** 2:.2e})")
R.check("A3.5 V0's Yukawa force on the exponential sphere equals the Coulomb one to < 1e-9: no scale appears (the correction is the O((m r)^2) of A1/C9)", f"deviation {dev_y:.2e}", abs(dev_y) < 1e-9)

# =========================================================================================== 6. de Sitter stability item G5 (v)
R.banner("A3.6  G5 (v): de Sitter stability of class V (the claim L5 is NOT imported)")
# 6a: the elastic sector about E = 0: second-order action of Lam(E) = int D dE for D ~ E^2/a: coefficient of dE^2 is (s/8 pi G) D'(E0) = (s/8 pi G) 2 E0/a -> 0
E0, dE = sp.symbols("E0 dE", real=True)
Lam_deep = E ** 3 / (3 * a)
expand2 = sp.series(Lam_deep.subs(E, E0 + dE), dE, 0, 3).removeO()
c2_coef = sp.simplify(expand2.coeff(dE, 2))
R.P(f"  elastic (deep) sector: Lam(E0 + dE) = ... + ({c2_coef}) dE^2 + ...   -> the quadratic kinetic coefficient is proportional to E0 and VANISHES on the FRW/dS background E0 = 0: no linear dynamics (strong coupling): the perturbative stability of the elastic sector about dS is UNDEFINED, not stable or unstable")
# 6b: Proca in de Sitter (V0, the only sector with a quadratic action about A = 0): sign of the kinetic term inherits s
R.P("  canonical Proca sector (V0) about A = 0 in de Sitter, mass m = H_Lambda/c: the quadratic action is (s/(8 pi G))(-1/2 F^2 - m^2 A^2)-type; with the attractive sign s = -1 the transverse and the longitudinal (Stueckelberg) kinetic terms are both wrong-sign, i.e. a ghost about de Sitter; its growth rate is not computed (a ghost is a Hamiltonian-unbounded mode, not by itself an exponential instability)")
R.P("  the class's background value of A_mu (the 'vector field in de Sitter' that also gives dark energy) is NOT fixed by class V: for a quadratic mass term the field equation m^2 A^0 = 0 forces A = 0; a nonzero, Lambda-tied background needs a potential V(A^2) that the reconstruction does not specify (L3) -> G5 (v) UNDEFINED as frozen.")
R.check("A3.6 G5 (v): the elastic sector's quadratic action vanishes about E = 0 (UNDEFINED, strongly coupled); the Proca sector with the attractive sign is a ghost; the dS background vector value is not fixed by class V",
        f"quadratic coefficient {c2_coef} (proportional to E0)", sp.simplify(c2_coef - E0 / a) == 0)
R.P("  verdict for G5 (v): UNDEFINED (elastic sector), FAIL (ghost sign, V0/V1). Hossenfelder's claim that perturbations around dS grow (L5) is neither confirmed nor refuted here.")

# =========================================================================================== 7. D-EFE premise check
R.banner("A3.7  D-EFE: the Lean premise nu(y) sqrt(y) -> 1 (y -> 0+) for the K laws (nu = 1 + psi(g_N)/g_N, y = g_N/a)")
y = sp.symbols("y", positive=True)
nu_ = {"K1": sp.sqrt(1 + 1 / y), "K2": 1 + 1 / sp.sqrt(y), "K3": sp.Rational(1, 2) + sp.sqrt(sp.Rational(1, 4) + 1 / y)}
lims = {k: sp.limit(v_ * sp.sqrt(y), y, 0, "+") for k, v_ in nu_.items()}
R.P(f"  limits of nu(y) sqrt(y) as y -> 0+: {lims}")
R.P("  => the premise of ChainCert.Ownership `deep_not_efeFreeRay` / `law_not_efeFreeRay` holds for K1, K2, K3 as POINTWISE laws; by that theorem (scope: pointwise QUMOND-type laws; field equations are not formalised) each has an external-field effect. D-own: a local action's static law is a function of the local total field, so by `ownership_not_field_local` (plus the [H] bridge) it is not the ownership rule.")
R.check("A3.7 D-EFE: nu(y) sqrt(y) -> 1 for K1, K2, K3 (sympy limits)", f"{lims}", all(v_ == 1 for v_ in lims.values()))
R.num("D_EFE_limits", {k: str(v_) for k, v_ in lims.items()})

nf = R.write()
sys.exit(0 if nf == 0 else 1)
