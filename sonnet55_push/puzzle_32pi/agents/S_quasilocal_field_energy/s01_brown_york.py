"""s01: Brown-York quasi-local stress tensor of a static timelike tube r = R in
   ds^2 = -N(r)^2 dt^2 + dr^2/f(r) + r^2 dOmega^2      (c = 1, G explicit)
specialised to  de Sitter static patch,  Schwarzschild stretched horizon,  Schwarzschild-de Sitter.

Convention (fixed here, matches the lane brief): the tube's unit normal n points to INCREASING r (out of the interior region
{r < R}); K_ab = nabla_a n_b restricted to the tube; tau_ab = -(1/8 pi G)(K_ab - K gamma_ab).
   energy density  eps = tau_ab u^a u^b = -k/(8 pi G),   k = 2 sqrt(f)/R  (trace of the 2-sphere's extrinsic curvature in the slice)
   surface pressure s  = tau^theta_theta = (k_n + a)/(8 pi G),  k_n = sqrt(f)/R,  a = sqrt(f) N'/N (acceleration of static observers along n).
(For the EXTERIOR region r > R with its inner boundary at the tube, the outward normal is -n and tau flips sign; this is stated, not hidden.)

PARTS
 A  covariant construction from the 4-metric (Christoffels, normal, projected nabla n) -> eps, s, and the three components.
 B  VARIATIONAL construction: on-shell action S[EH + Lambda + GHY] of the static region between two tubes, as a function of the boundary
    data (N1, R1, N2, R2); eps = -(1/4 pi R^2) dS/dN_b (per unit t), s = (1/(8 pi R N)) dS/dR|_N.  Compared with A.
    Control: GHY prefactor mutated -> S is not stationary in M (Hamilton-Jacobi fails) and eps, s come out wrong.
 C  Quasi-local first law  dE = T_loc dS - s dA  (E = unreferenced BY energy -R sqrt(f)/G), horizon limits, thermodynamics of the membrane.
 D  Numbers: E_BY of horizons (r_h/G = 2 M_MS), Newtonian limit E_BY = M + G M^2/(2R) (=> exterior field energy -GM^2/(2R)), the a0 static radius in dS.
"""
import sympy as sp, mpmath as mp, random
mp.mp.dps = 40
ok = []
def chk(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)

G = sp.symbols('G', positive=True)
r, th, ph, t = sp.symbols('r theta phi t', positive=True)
Nf = sp.Function('N')(r); ff = sp.Function('f')(r)

# ------------------------------------------------------------------ A: covariant construction
X = [t, r, th, ph]
g = sp.diag(-Nf**2, 1/ff, r**2, r**2*sp.sin(th)**2)
ginv = g.inv()
def christoffel(g, ginv, X):
    n = len(X)
    return [[[sum(ginv[l, m]*(sp.diff(g[m, i], X[j]) + sp.diff(g[m, j], X[i]) - sp.diff(g[i, j], X[m])) for m in range(n))/2
              for j in range(n)] for i in range(n)] for l in range(n)]
Gam = christoffel(g, ginv, X)
n_up = [0, sp.sqrt(ff), 0, 0]
n_dn = [sum(g[i, j]*n_up[j] for j in range(4)) for i in range(4)]
chk("A0 normal is unit and spacelike: n^a n_a = 1", sp.simplify(sum(n_up[i]*n_dn[i] for i in range(4)) - 1) == 0)
def nabla_n(a, b):     # nabla_a n_b
    return sp.diff(n_dn[b], X[a]) - sum(Gam[l][a][b]*n_dn[l] for l in range(4))
tang = [0, 2, 3]       # coordinate vectors d_t, d_theta, d_phi are tangent to r = const
K = sp.Matrix(3, 3, lambda i, j: sp.simplify(nabla_n(tang[i], tang[j])))
gam = sp.diag(-Nf**2, r**2, r**2*sp.sin(th)**2)
gaminv = gam.inv()
Ktr = sp.simplify(sum(gaminv[i, j]*K[i, j] for i in range(3) for j in range(3)))
chk("A1 K symmetric (nabla n is a gradient-like field of a hypersurface-orthogonal normal)", sp.simplify(K - K.T) == sp.zeros(3, 3))
Kmix_tt = sp.simplify(gaminv[0, 0]*K[0, 0]); Kmix_thth = sp.simplify(gaminv[1, 1]*K[1, 1])
a_acc = sp.sqrt(ff)*sp.diff(Nf, r)/Nf
chk("A2 K^t_t = a = sqrt(f) N'/N (acceleration of static observers)", sp.simplify(Kmix_tt - a_acc) == 0)
chk("A3 K^theta_theta = K^phi_phi = sqrt(f)/r", sp.simplify(Kmix_thth - sp.sqrt(ff)/r) == 0 and sp.simplify(gaminv[2, 2]*K[2, 2] - sp.sqrt(ff)/r) == 0)
tau = sp.Matrix(3, 3, lambda i, j: -(K[i, j] - Ktr*gam[i, j])/(8*sp.pi*G))
u_up = sp.Matrix([1/Nf, 0, 0])
eps = sp.simplify((u_up.T*tau*u_up)[0])
s_pr = sp.simplify(gaminv[1, 1]*tau[1, 1])
k_tr = 2*sp.sqrt(ff)/r
chk("A4 eps = tau_ab u^a u^b = -k/(8 pi G), k = 2 sqrt(f)/r", sp.simplify(eps + k_tr/(8*sp.pi*G)) == 0)
chk("A5 s = tau^theta_theta = (k_n + a)/(8 pi G), k_n = sqrt(f)/r", sp.simplify(s_pr - (sp.sqrt(ff)/r + a_acc)/(8*sp.pi*G)) == 0)
chk("A6 no momentum density: tau_{t theta} = 0 (static, spherical)", tau[0, 1] == 0 and tau[0, 2] == 0)
# control: wrong overall sign flips eps -> must not equal -k/8piG
chk("A7 control: with tau -> +tau the energy density is +k/(8 pi G) (sign convention matters and is fixed)", sp.simplify(-eps - k_tr/(8*sp.pi*G)) == 0 and sp.simplify(-eps + k_tr/(8*sp.pi*G)) != 0)

# ------------------------------------------------------------------ B: variational construction from the on-shell action
M, Lam, al = sp.symbols('M Lambda alpha', positive=True)
fSdS = 1 - 2*M/r - Lam*r**2/3
gS = sp.diag(-al**2*fSdS, 1/fSdS, r**2, r**2*sp.sin(th)**2)
gSinv = gS.inv()
GamS = christoffel(gS, gSinv, X)
def ricci_scalar(g, ginv, Gam, X):
    n = len(X)
    Ric = sp.zeros(n, n)
    for i in range(n):
        for j in range(n):
            Ric[i, j] = sum(sp.diff(Gam[l][i][j], X[l]) for l in range(n)) - sum(sp.diff(Gam[l][i][l], X[j]) for l in range(n)) \
                        + sum(Gam[l][l][m]*Gam[m][i][j] for l in range(n) for m in range(n)) - sum(Gam[l][j][m]*Gam[m][i][l] for l in range(n) for m in range(n))
    return sp.simplify(sum(ginv[i, j]*Ric[i, j] for i in range(n) for j in range(n))), Ric
Rsc, RicS = ricci_scalar(gS, gSinv, GamS, X)
chk("B0 SdS (f = 1 - 2M/r - Lambda r^2/3, N = alpha sqrt f): R = 4 Lambda (vacuum, on shell)", sp.simplify(Rsc - 4*Lam) == 0)
chk("B0b Einstein eq: R_{mu nu} = Lambda g_{mu nu}", sp.simplify(RicS - Lam*gS) == sp.zeros(4, 4))
sqrtg = al*r**2                       # sqrt(-g)/sin(theta)
# bulk (per unit t, angles integrated): (1/16 pi G) int sqrt(-g)(R - 2 Lambda) = (1/16 pi G) 4 pi int (2 Lambda) alpha r^2 dr
R1, R2 = sp.symbols('R1 R2', positive=True)
bulk = (1/(16*sp.pi*G))*4*sp.pi*sp.integrate(sqrtg*(Rsc - 2*Lam), (r, R1, R2))
# GHY: (1/8 pi G) int sqrt(-gamma) K, outward normal +r at R2 and -r at R1 (K flips sign)
def ghy_at(Rv, sign):
    Nn = al*sp.sqrt(fSdS)
    Kv = sp.sqrt(fSdS)*(sp.diff(Nn, r)/Nn + 2/r)
    return sign*(1/(8*sp.pi*G))*4*sp.pi*(Nn*r**2*Kv).subs(r, Rv)
def action_per_T(ghy_coeff=1):
    return sp.simplify(bulk + ghy_coeff*(ghy_at(R2, +1) + ghy_at(R1, -1)))
S_T = action_per_T()
N1s, N2s = sp.symbols('N1 N2', positive=True)
claim = (1/G)*(al*R2*fSdS.subs(r, R2) - al*R1*fSdS.subs(r, R1))
chk("B1 on-shell action per unit t = (alpha/G)[R2 f(R2) - R1 f(R1)] = (1/G)[N2 R2 sqrt(f2) - N1 R1 sqrt(f1)]", sp.simplify(S_T - claim) == 0)
# express in boundary data: alpha sqrt(f_i) = N_i ; S = (1/G)[N2 R2 sqrt(f2) - N1 R1 sqrt(f1)] with M implicit
f1 = fSdS.subs(r, R1); f2 = fSdS.subs(r, R2)
S_data = (N2s*R2*sp.sqrt(f2) - N1s*R1*sp.sqrt(f1))/G
Fcon = N1s*sp.sqrt(f2) - N2s*sp.sqrt(f1)         # alpha_1 = alpha_2  <=>  N1/sqrt(f1) = N2/sqrt(f2)
chk("B2 Hamilton-Jacobi: dS/dM at fixed data vanishes on the constraint surface (alpha1 = alpha2)",
    sp.simplify((sp.diff(S_data, M)).subs(N1s, al*sp.sqrt(f1)).subs(N2s, al*sp.sqrt(f2))) == 0)
def total_derivative(var):
    dMd = -sp.diff(Fcon, var)/sp.diff(Fcon, M)
    return sp.diff(S_data, var) + sp.diff(S_data, M)*dMd
dS_dN2 = total_derivative(N2s)
dS_dR2 = total_derivative(R2)
sub = {N1s: al*sp.sqrt(f1), N2s: al*sp.sqrt(f2)}
eps_var = sp.simplify((-dS_dN2/(4*sp.pi*R2**2)).subs(sub))
s_var = sp.simplify((dS_dR2/(8*sp.pi*R2*N2s)).subs(sub))
# compare with A at r = R2:   N = alpha sqrt f
eps_A = (-(2*sp.sqrt(fSdS)/r)/(8*sp.pi*G)).subs(r, R2)
Nn = al*sp.sqrt(fSdS)
s_A = ((sp.sqrt(fSdS)/r + sp.sqrt(fSdS)*sp.diff(Nn, r)/Nn)/(8*sp.pi*G)).subs(r, R2)
chk("B3 eps from dS/dN_b equals covariant -k/(8 pi G)", sp.simplify(eps_var - eps_A) == 0)
chk("B4 s from dS/dR|_N equals covariant (k_n + a)/(8 pi G)", sp.simplify(s_var - s_A) == 0)
# control: GHY coefficient mutated (1/16 pi G instead of 1/8 pi G)
S_bad = action_per_T(sp.Rational(1, 2))
S_bad_data_M = sp.simplify(sp.diff(S_bad.subs(al, N2s/sp.sqrt(f2)), M))   # crude check: alpha tied to N2 => explicit M dependence
bad_alpha_free = sp.simplify(S_bad - S_T)
chk("B5 control: with the GHY term halved the on-shell action differs from the correct one by a non-vanishing boundary term",
    bad_alpha_free != 0)
# and its M-stationarity fails:
Sbad_expr = sp.simplify(S_bad.subs(al, N2s/sp.sqrt(f2)))
dM_bad = sp.simplify(sp.diff(Sbad_expr, M).subs(N1s, N2s*sp.sqrt(f1)/sp.sqrt(f2)))
chk("B6 control: halved GHY -> dS/dM at fixed (N2, R1, R2) does not vanish on the constraint surface (well-posedness lost)", dM_bad != 0)

# ------------------------------------------------------------------ C: quasi-local first law and horizon thermodynamics
Mm, Ll, Rr = sp.symbols('M L R', positive=True)
fL = 1 - 2*Mm/Rr - Rr**2/Ll**2
sqf = sp.sqrt(fL)
E_unref = -Rr*sqf/G                                    # -(1/8 pi G) * (k * area)
# A: BH-horizon side: region r_b < r < R, S = pi r_b^2/G, T_loc = f'(r_b)/(4 pi sqrt(f(R)))
rb = sp.symbols('r_b', positive=True)
Mb = (rb/2)*(1 - rb**2/Ll**2)                          # f(r_b) = 0  =>  M = (r_b/2)(1 - r_b^2/L^2)
fprime = lambda rv, Mv: sp.diff(1 - 2*Mv/r - r**2/Ll**2, r).subs(r, rv)
Tloc = fprime(rb, Mb)/(4*sp.pi*sp.sqrt(1 - 2*Mb/Rr - Rr**2/Ll**2))
S_b = sp.pi*rb**2/G
E_b = E_unref.subs(Mm, Mb)
a_R = (sp.sqrt(fL)*sp.diff(sp.sqrt(fL), Rr)/sp.sqrt(fL)).subs(Mm, Mb)   # = f'/(2 sqrt f) = a with N = sqrt f (alpha = 1)
s_R = ((sqf/Rr + sp.diff(sqf, Rr)).subs(Mm, Mb))/(8*sp.pi*G)
# first law: dE = T dS - s dA with independent variations of (r_b, R)
dE_drb = sp.diff(E_b, rb); dE_dR = sp.diff(E_b, Rr)
chk("C1 first law, r_b-variation at fixed R (BH-horizon side, with Lambda): dE/dr_b = T_loc dS/dr_b",
    sp.simplify(dE_drb - Tloc*sp.diff(S_b, rb)) == 0)
chk("C2 first law, R-variation at fixed r_b: dE/dR = -s dA/dR = -8 pi R s", sp.simplify(dE_dR + 8*sp.pi*Rr*s_R) == 0)
# control with the wrong sign of s
chk("C3 control: with s -> -s the R-variation of the first law fails", sp.simplify(dE_dR - 8*sp.pi*Rr*s_R) != 0)
# reference-subtracted energy (flat embedding, k0 = 2/R): E_ref = (R/G)(1 - sqrt f) obeys the first law only up to the reference term
E_ref = (Rr/G)*(1 - sqf)
chk("C4 the reference-subtracted energy violates the R-variation by exactly the reference piece 1/G (so the first law is for the unreferenced tensor)",
    sp.simplify((sp.diff(E_ref, Rr) + 8*sp.pi*Rr*(sqf/Rr + sp.diff(sqf, Rr))/(8*sp.pi*G)) - 1/G) == 0)
# M = 0 de Sitter ball: regular centre, S const => dE = -s dA
E_dS = E_unref.subs(Mm, 0); s_dS = s_R.subs({Mm: 0}) if False else ((sp.sqrt(1 - Rr**2/Ll**2)/Rr + sp.diff(sp.sqrt(1 - Rr**2/Ll**2), Rr))/(8*sp.pi*G))
chk("C5 dS ball (M = 0, regular centre): dE/dR = -8 pi R s", sp.simplify(sp.diff(E_dS, Rr) + 8*sp.pi*Rr*s_dS) == 0)
# horizon limits (Schwarzschild, L -> infinity): s -> a/(8 pi G) = T_loc sigma_BH, eps -> 0
Ms = sp.symbols('M_s', positive=True)
fSch = 1 - 2*Ms/r
delta = sp.symbols('delta', positive=True)
Rh = 2*Ms*(1 + delta)                                   # stretched horizon at fractional offset delta
sqfS = sp.sqrt(fSch.subs(r, Rh)); aS = sp.diff(sp.sqrt(fSch), r).subs(r, Rh)
sS = (sqfS/Rh + aS)/(8*sp.pi*G)
TlocS = (1/(4*Ms))/(2*sp.pi*sqfS)                      # kappa = 1/(4M), N = sqrt f, T_loc = kappa/(2 pi N)
sigma = 1/(4*G)
lim_ratio = sp.limit(sp.simplify(sS/(TlocS*sigma)), delta, 0)
chk("C6 Schwarzschild stretched horizon: s / (T_loc sigma_BH) -> 1 as R -> r_s (membrane pressure = T x entropy density)", lim_ratio == 1)
eps_S = -(2*sqfS/Rh)/(8*sp.pi*G)
chk("C7 the stretched-horizon energy density eps -> 0 while s diverges like 1/sqrt(delta)", sp.limit(eps_S, delta, 0) == 0 and sp.limit(sS*sp.sqrt(delta), delta, 0) != 0)
# exact Gibbs-like difference: eps + s = (a - k_n)/(8 pi G);  T_loc sigma = a_hor/(8 pi G) with a_hor = kappa/N
diff_exact = sp.simplify((-(2*sqfS/Rh) + sqfS/Rh + aS) - (aS - sqfS/Rh))
chk("C8 identity eps + s = (a - k_n)/(8 pi G) exactly", diff_exact == 0)
# de Sitter static patch: T_loc = sqrt(a^2 + H^2)/(2 pi), a = -H^2 R/sqrt(1 - H^2 R^2)
H = 1/Ll
sqd = sp.sqrt(1 - Rr**2*H**2)
a_dS = sp.diff(sqd, Rr)
Tdsl = H/(2*sp.pi*sqd)
chk("C9 dS static patch: (2 pi T_loc)^2 = a^2 + H^2 exactly (Tolman with kappa = H)", sp.simplify((2*sp.pi*Tdsl)**2 - a_dS**2 - H**2) == 0)
chk("C10 near the cosmological horizon the BY pressure seen from inside is NEGATIVE: s -> -T_loc sigma_BH (a tension)",
    sp.limit(sp.simplify((sp.sqrt(1 - Rr**2/Ll**2)/Rr + a_dS)/(8*sp.pi*G) / (Tdsl/(4*G))), Rr, Ll, '-') == -1)

# ------------------------------------------------------------------ D: numbers
# D1: E_BY of any horizon (reference-subtracted) = r_h/G = 2 * (Misner-Sharp mass r_h/2G)
chk("D1 reference-subtracted BY energy at a horizon (f = 0): (R/G)(1 - 0) = R/G = 2 M_MS(R), M_MS = R/2G",
    sp.simplify((Rr/G)*(1 - 0) - 2*(Rr/(2*G))) == 0)
# D2: Newtonian limit: E_BY(R) = M + G M^2/(2R) + ... (G explicit); exterior field energy M - E_BY(R) = -G M^2/(2R)
Mx, Rx = sp.symbols('M_x R_x', positive=True)
E_sch = (Rx/G)*(1 - sp.sqrt(1 - 2*G*Mx/Rx))
ser = sp.series(E_sch, Mx, 0, 4).removeO()
chk("D2 Schwarzschild: E_BY(R) = M + G M^2/(2R) + G^2 M^3/(2R^2)+ ...", sp.simplify(ser - (Mx + G*Mx**2/(2*Rx) + G**2*Mx**3/(2*Rx**2))) == 0)
gN = G*Mx/r**2
ext = sp.integrate(4*sp.pi*r**2*gN**2/(8*sp.pi*G), (r, Rx, sp.oo))
chk("D3 exterior field energy magnitude int_R^inf 4 pi r^2 g^2/(8 pi G) dr = G M^2/(2R) equals M - E_BY(R) up to sign: M - E_BY = -GM^2/(2R): NEGATIVE-energy density -g^2/(8 pi G)",
    sp.simplify(ext - G*Mx**2/(2*Rx)) == 0 and sp.simplify((Mx - ser).subs(Mx, Mx) + ext).series(Mx, 0, 3).removeO() == 0)
# D4: dS ball: E_BY(R) = E_vac(R) + R^5/(8 G L^4) + ...  (self-energy is POSITIVE for p = -rho: gravity is repulsive)
rho = 3/(8*sp.pi*G*Ll**2)
Evac = sp.Rational(4, 3)*sp.pi*rho*Rr**3
EdS_ref = (Rr/G)*(1 - sp.sqrt(1 - Rr**2/Ll**2))
ser2 = sp.series(EdS_ref, Rr, 0, 8).removeO()
chk("D4 dS ball: E_BY = E_vac(R) + R^5/(8 G L^4) + ... (positive gravitational self-energy for p = -rho)",
    sp.simplify(ser2 - (Evac + Rr**5/(8*G*Ll**4) + Rr**7/(16*G*Ll**6))) == 0)
chk("D5 dS horizon: E_BY(L) = L/G = 2 E_vac(L) = 2 M_dS (E_vac(L) = L/2G)", sp.simplify(EdS_ref.subs(Rr, Ll) - 2*Evac.subs(Rr, Ll)) == 0 and sp.simplify(Evac.subs(Rr, Ll) - Ll/(2*G)) == 0)
# D6: acceleration radius in dS: static observer has |a| = a0 at x0 = R/L = 1/sqrt(1 + Z^2), Z = H/a0; BY numbers there
Z = sp.symbols('Z', positive=True)
a0s = sp.symbols('a0', positive=True)
x0 = 1/sp.sqrt(1 + Z**2)
a_of_x = lambda x: x/(Ll*sp.sqrt(1 - x**2))
chk("D6 |a(x0)| = a0 at x0 = 1/sqrt(1 + Z^2) (Z = H/a0)", sp.simplify(a_of_x(x0).subs(Ll, 1/(Z*a0s)) - a0s) == 0)   # H = Z a0, L = 1/(Z a0)
s_x0 = sp.simplify(((sp.sqrt(1 - x0**2)/(x0*Ll)) - a_of_x(x0))/(8*sp.pi*G))          # interior view: a = -|a|
print("  s(x0) 8 pi G =", sp.simplify((s_x0*8*sp.pi*G).subs(Ll, 1/(Z*a0s))), " (interior view; sqrt(f)/R - |a|, in units of a0)")
print("  u_g(a0)/a0 = a0/(8 pi G):  s_BY(a0-membrane) = a0/(8 pi G) = T_U sigma_BH = u_g(a0)/a0  (identity, see s02/s04)")
print("  E_BY(r_sa)/E_BY(L) = r_sa/L = Z/2 = sqrt(8 pi/3) at the puzzle value (restatement of A_s/A_dS = 8 pi/3)")


print("\n--- FORMULA SHEET (G explicit, c = 1; M below is the geometric mass G M_phys; tube at r = R, normal towards increasing r, tau_ab = -(K_ab - K gamma_ab)/(8 pi G)) ---")
def sheet(name, fexpr):
    Rv = sp.symbols('R', positive=True)
    fR = fexpr.subs(r, Rv); sq_ = sp.sqrt(fR)
    a_ = sp.simplify(sp.diff(sp.sqrt(fexpr), r).subs(r, Rv))
    print("%-22s f(R) = %s" % (name, sp.simplify(fR)))
    print("    eps = -sqrt(f)/(4 pi G R) = %s" % sp.simplify(-sq_/(4*sp.pi*G*Rv)))
    print("    s   = (sqrt(f)/R + a)/(8 pi G),  a = f'/(2 sqrt f) = %s" % a_)
    print("    E_unref = -R sqrt(f)/G ;  E_ref = (R/G)(1 - sqrt f) ;  T_loc = kappa/(2 pi sqrt f)")
sheet("de Sitter static patch", 1 - r**2/Ll**2)
sheet("Schwarzschild", 1 - 2*Ms/r)
sheet("Schwarzschild-de Sitter", 1 - 2*Mm/r - r**2/Ll**2)
print("    exact identity at the a0-radius of dS (|a| = a0, Z = H/a0): k_n = sqrt(f)/R = H^2/a0, eps = -(2/3) rho/a0, 8 pi G s = a0 (Z^2 - 1) = H^2/a0 - a0  (no puzzle input)")
Rq = sp.symbols('R_q', positive=True)
x0_ = 1/sp.sqrt(1 + Z**2)
eps_x0 = sp.simplify((-(2*sp.sqrt(1 - x0_**2)/(x0_/(Z*a0s)))/(8*sp.pi*G)))     # L = 1/(Z a0)
rho_of = 3*(Z*a0s)**2/(8*sp.pi*G)
chk("D7 at the a0-radius of dS: eps = -(2/3) rho/a0 exactly, for any a0 and rho (an identity, no principle)", sp.simplify(eps_x0 + sp.Rational(2, 3)*rho_of/a0s) == 0)

print("\nTOTAL", sum(ok), "/", len(ok), "pass;", len(ok) - sum(ok), "fail")
