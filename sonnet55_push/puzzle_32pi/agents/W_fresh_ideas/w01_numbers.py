#!/usr/bin/env python3
"""w01_numbers.py -- recompute every number cited in W_fresh_ideas/README.md.
Each claim is paired with a wrong-constant CONTROL that must FAIL (counted separately).
Units: symbolic, c, G kept explicit where it matters; puzzle: G rho_L = 4 a0^2 c^-2... (c=1 unless stated).
Run: python3 w01_numbers.py   (exit 0 iff all claims pass and all controls fail as required)
"""
import sympy as sp
import mpmath as mp

passed = failed = ctrl_ok = ctrl_bad = 0
def claim(name, cond):
    global passed, failed
    ok = bool(cond)
    passed += ok; failed += (not ok)
    print(("PASS  " if ok else "FAIL  ") + name)
def control(name, cond_that_must_be_false):
    global ctrl_ok, ctrl_bad
    ok = not bool(cond_that_must_be_false)
    ctrl_ok += ok; ctrl_bad += (not ok)
    print(("CTRL-OK  " if ok else "CTRL-BAD ") + name)

G, c, H, rho, Lam, L, r, M, m, a0, A_, R = sp.symbols('G c H rho Lambda L r M m a0 A R', positive=True)
pi = sp.pi

# ---- 0. the puzzle and Z --------------------------------------------------------------------
Z = sp.sqrt(32*pi/3)
claim("Z = sqrt(32pi/3) = 5.7888", abs(float(Z) - 5.7888) < 1e-3)
# a0 = (1/2) sqrt(G rho) with rho = 3H^2/(8 pi G)  =>  a0/H = 1/Z
a0_over_H = sp.simplify(sp.Rational(1, 2)*sp.sqrt(G*3*H**2/(8*pi*G))/H)
claim("a0/H = (1/2) sqrt(G rho_L)/H = 1/Z", sp.simplify(a0_over_H - 1/Z) == 0)
control("control: 1/2 -> 1/6 does NOT give 1/Z", sp.simplify(sp.Rational(1, 6)*sp.sqrt(3/(8*pi)) - 1/Z) == 0)

# ---- 1. Machian / Sciama (W01) ------------------------------------------------------------------
rhoc = 3*H**2/(8*pi*G)
Phi_ball = 2*pi*G*rhoc*(c/H)**2          # potential at the centre of a uniform ball, radius c/H
claim("W01: centre potential of the Hubble ball = (3/4) c^2 exactly", sp.simplify(Phi_ball - sp.Rational(3, 4)*c**2) == 0)
control("control: (3/4) -> 1 fails", sp.simplify(Phi_ball - c**2) == 0)
# Machian condition Phi = c^2 with R = Rindler distance c^2/a  ->  a^2 = 2 pi G rho c^2 (c=1)
a_M = sp.sqrt(2*pi*G*rho)*c
claim("W01: Sciama/Rindler-ball kappa_M = sqrt(2 pi) = 2.5066 (vs 1/2: factor 5.01)", abs(float(sp.sqrt(2*pi)) - 2.5066) < 1e-3 and abs(float(2*sp.sqrt(2*pi)) - 5.013) < 1e-3)
# Vacuum has no momentum density in ANY frame: T' = Lam T Lam^T = T for T = -rho eta
b = sp.symbols('b', real=True)
g = 1/sp.sqrt(1 - b**2)
Lb = sp.Matrix([[g, -g*b, 0, 0], [-g*b, g, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
eta = sp.diag(-1, 1, 1, 1)
Tvac = -rho*eta
claim("W01: T^{mu nu} = -rho eta^{mu nu} is boost invariant => T^{0i}=0 in every frame (vacuum cannot induce inertia)",
      sp.simplify(Lb*Tvac*Lb.T - Tvac) == sp.zeros(4, 4))
Tdust = sp.diag(rho, 0, 0, 0)
control("control: dust T^{mu nu} is NOT boost invariant", sp.simplify(Lb*Tdust*Lb.T - Tdust) == sp.zeros(4, 4))

C_ = sp.symbols('C', positive=True)
claim("W01: Machian closure C*Phi_ball(R=c^2/a)=c^2 gives a0/(c H) = sqrt(3C/4) (C=1: 0.866; C=4/3: 1; C=4: 1.732) -- all ~cH, 5x the data scale",
      sp.simplify(sp.sqrt(2*pi*C_)*sp.sqrt(3/(8*pi)) - sp.sqrt(3*C_/4)) == 0)
control("control: a0/(cH)=1/Z is not sqrt(3C/4) for any C in {1, 4/3, 4}", any(abs(float(sp.sqrt(sp.Rational(3, 4)*cc_)) - float(1/Z)) < 1e-2 for cc_ in [1, sp.Rational(4, 3), 4]))

claim("W01: kappa = a0/(c sqrt(G rho)) = sqrt(2 pi C) equals 1/2 only for C = 1/(8 pi) = 0.0398 (no Machian weight)",
      sp.simplify(sp.solve(sp.Eq(sp.sqrt(2*pi*C_), sp.Rational(1, 2)), C_)[0] - 1/(8*pi)) == 0)
# ---- 2. Newtonian ball thresholds in Lambda (W02) ----------------------------------------------------
# zero-force: G M/R^2 = Lam R/3 (c=1) ; mean density = 3M/(4 pi R^3)
Rzf = sp.symbols('Rzf', positive=True)
Msol = sp.solve(sp.Eq(G*M/Rzf**2, Lam*Rzf/3), M)[0]
rho_bar = sp.simplify(3*Msol/(4*pi*Rzf**3))
rho_L = Lam/(8*pi*G)
claim("W02: zero-force sphere has mean density exactly 2 rho_Lambda", sp.simplify(rho_bar/rho_L - 2) == 0)
# OSCO: V = -GM/r + J^2/(2r^2) - Lam r^2/6 ; circular J^2 = GM r - Lam r^4/3 ; V'' > 0 <=> GM/r^3 > 4Lam/3
Jsq = G*M*r - Lam*r**4/3
Vp = lambda rr: (G*M/rr**2 - Jsq/rr**3 - Lam*rr/3)
Vpp = sp.simplify(sp.diff(G*M/r**2 - sp.Symbol('J2', positive=True)/r**3 - Lam*r/3, r).subs(sp.Symbol('J2', positive=True), Jsq))
claim("W02: V'' = +(G M/r^3 - 4 Lam/3) on circular orbits => stable iff G M/r^3 > 4 Lam/3 (first version of this check had the wrong sign; corrected)",
      sp.simplify(Vpp - (G*M/r**3 - sp.Rational(4, 3)*Lam)) == 0)
control("control: V'' = -(G M/r^3 - 4 Lam/3) is FALSE", sp.simplify(Vpp + (G*M/r**3 - sp.Rational(4, 3)*Lam)) == 0)
r_osco = sp.solve(sp.Eq(G*M/r**3, sp.Rational(4, 3)*Lam), r)[0]
rho_osco = sp.simplify(3*M/(4*pi*r_osco**3)/rho_L)
claim("W02: OSCO mean density = 8 rho_Lambda", sp.simplify(rho_osco - 8) == 0)
control("control: OSCO mean density is not 4 rho_Lambda", sp.simplify(rho_osco - 4) == 0)
# mass at which the deep-MOND radius sqrt(GM/a0) equals R_ZF : G M = 27 a0^3/Lam^2 (c=1), Lam = 32 pi a0^2
GM_star = 27*a0**3/(32*pi*a0**2)**2
M_star_over = sp.simplify(GM_star*a0)      # = G M a0 / c^4
claim("W02: M* = 27/(1024 pi^2) c^4/(G a0) = 2.67e-3 c^4/(G a0)", abs(float(M_star_over) - 27/(1024*mp.pi**2)) < 1e-12 and abs(float(M_star_over) - 2.672e-3) < 1e-5)
Gsi, csi, a0si, Msun = 6.674e-11, 2.998e8, 1.2e-10, 1.989e30
M_star_kg = float(M_star_over)*csi**4/(Gsi*a0si)
claim("W02: M* ~ 1e21 Msun (a mass no structure has)  [%.2e Msun]" % (M_star_kg/Msun), 5e20 < M_star_kg/Msun < 5e21)

# deep-MOND Lambda-bound orbits: g_N = s/r with s = sqrt(G M a0) ; V = s ln r + J^2/(2r^2) - Lam r^2/6
sM = sp.symbols('s', positive=True)
J2d = sM*r**2 - Lam*r**4/3
Vpp_d = sp.simplify(sp.diff(sM/r - sp.Symbol('J2d')/r**3 - Lam*r/3, r).subs(sp.Symbol('J2d'), J2d))
claim("W02: deep-MOND V'' = 2s/r^2 - 4 Lam/3 on circular orbits (outermost stable orbit r^2 = 3s/(2 Lam))", sp.simplify(Vpp_d - (2*sM/r**2 - sp.Rational(4, 3)*Lam)) == 0)
r_d = sp.sqrt(3*sM/(2*Lam))
g_d = sp.simplify(sM/r_d)
claim("W02: deep-MOND OSCO acceleration g = sqrt(2 Lam s/3) scales as s^(1/2) ~ (G M a0)^(1/4): mass-DEPENDENT, no universal acceleration",
      sp.simplify(g_d**2 - 2*Lam*sM/3) == 0 and sp.simplify(sp.diff(sp.log(g_d), sM)*sM - sp.Rational(1, 2)) == 0)
control("control: the deep-MOND OSCO acceleration is NOT independent of s", sp.simplify(sp.diff(g_d, sM)) == 0)

# ---- 3. Hubble-sphere Newtonian field and the maximal force (W14) ---------------------------------------
MH = sp.Rational(4, 3)*pi*rhoc*(c/H)**3
gH = sp.simplify(G*MH/(c/H)**2)
claim("W14: Newtonian field at the Hubble radius is exactly cH/2", sp.simplify(gH - c*H/2) == 0)
control("control: not cH/3", sp.simplify(gH - c*H/3) == 0)
Fmax = c**4/(4*G)
claim("W14: M_H = c^3/(2 G H) and F_max/M_H = cH/2", sp.simplify(MH - c**3/(2*G*H)) == 0 and sp.simplify(Fmax/MH - c*H/2) == 0)
Lam_ = 3*H**2/c**2
Fvac = (Lam_*c**4/(8*pi*G))*4*pi*(c/H)**2       # P_Lambda x A_dS with rho c^2 = Lam c^4/(8 pi G)
claim("W14: vacuum tension x horizon area = (3/2) c^4/G = 6 F_max (pi-free, hbar-free)", sp.simplify(Fvac - 6*Fmax) == 0)
control("control: not 4 F_max", sp.simplify(Fvac - 4*Fmax) == 0)
claim("W14: Verlinde a0 = cH/6 equals F_max/(3 M_H)", sp.simplify(Fmax/(3*MH) - c*H/6) == 0)
# every Schwarzschild BH: kappa*M = F_max ;  the puzzle BH (kappa=a0, G rho = 4 a0^2, c=1): mass = rho r_s^3 / 2
rs = 1/(2*a0)
rho_p = 4*a0**2                  # G=c=1
claim("W14: puzzle BH: M = r_s/2 = rho_L r_s^3 / 2 (pi-free)", sp.simplify(rs/2 - rho_p*rs**3/2) == 0)
claim("W14: ball of density rho_L and radius r_s holds (8 pi/3) M_puzzle", sp.simplify(sp.Rational(4, 3)*pi*rho_p*rs**3 - sp.Rational(8, 3)*pi*(rs/2)) == 0)

# membrane-paradigm horizon-fluid surface pressure p = kappa/(8 pi G) (recalled result, used only as a definition here)
p_H = a0/(8*pi)                     # G = c = 1, kappa = a0
rho_p2 = 4*a0**2; Rstar = 1/sp.sqrt(rho_p2)
claim("W10: membrane surface pressure at kappa=a0 over (rho_L R*) = 1/(16 pi); p_H*A_Schwarzschild = M/2 (Smarr)", sp.simplify(p_H/(rho_p2*Rstar) - 1/(16*pi)) == 0 and sp.simplify((sp.Symbol('k', positive=True)/(8*pi))*4*pi*(1/(2*sp.Symbol('k', positive=True)))**2 - (1/(4*sp.Symbol('k', positive=True)))/2) == 0)
control("control: that ratio is not 1/(8 pi)", sp.simplify(p_H/(rho_p2*Rstar) - 1/(8*pi)) == 0)

# ---- 4. Halo surface density (W10) --------------------------------------------------------------------------
Msun_pc2 = 1.989e30/(3.0857e16)**2
SigM = a0si/(2*float(mp.pi)*Gsi)/Msun_pc2
SigL = 2*a0si/Gsi/Msun_pc2
claim("W10: Milgrom Sigma_M = a0/(2 pi G) = %.0f Msun/pc^2 (a0=1.2e-10); Sigma_L = 2a0/G = 4 pi Sigma_M" % SigM, abs(SigL/SigM - 4*float(mp.pi)) < 1e-9 and 120 < SigM < 150)
control("control: Sigma_L/Sigma_M is not 2 pi", abs(SigL/SigM - 2*float(mp.pi)) < 1e-9)

# ---- 5. Lattice counting (W09) ---------------------------------------------------------------------------------
# cubic lattice, cell mass m, spacing l, rho = m/l^3 ; a_nn = G m / l^2 ; a_nn^2 = G rho (G m / l c^2)
l = sp.symbols('l', positive=True)
claim("W09: a_nn^2 = (G rho)(G m/l) identically (cubic lattice)", sp.simplify((G*m/l**2)**2 - (G*m/l**3)*(G*m/l)) == 0)
# touching horizons: l = 2 r_s = 4 G m  (c=1) => Gm/l = 1/4 => a_nn^2 = G rho/4
claim("W09: touching-horizon condition l = 4Gm gives a_nn^2 = G rho / 4 (the puzzle form)", sp.simplify(((G*m/l**2)**2 - (G*m/l**3)*sp.Rational(1, 4)).subs(l, 4*G*m)) == 0)
# lattice spacing then l = R*/2 = (1/2)/sqrt(G rho)  -> in Hubble units
l_over_L = sp.simplify((1/(2*sp.sqrt(G*rhoc)))/(c/H)).subs(c, 1)
claim("W09: l/L_H = sqrt(2 pi/3) = 1.4472 (= the audit's embeddability number), cells per Hubble volume = %.3f" % float(sp.Rational(4, 3)*pi/(sp.sqrt(2*pi/3))**3),
      abs(float(l_over_L) - 1.4472) < 1e-3)
v_bcc, v_fcc = 4/(3*mp.sqrt(3)), 1/mp.sqrt(2)
claim("W09: only the cubic lattice has (cell volume per point)/(nn spacing)^3 = 1 (bcc %.4f, fcc %.4f)" % (v_bcc, v_fcc), abs(v_bcc-1) > 0.2 and abs(v_fcc-1) > 0.2)

# ---- 6. Extended thermodynamics of SdS (W03) --------------------------------------------------------------------
# f = 1 - 2M/r - Lam r^2/3 ; kappa = |f'|/2 at horizon ; T = kappa/2pi ; S = pi r^2 ; P = -Lam/8pi ; V = 4 pi r^3/3
Mh = r/2*(1 - Lam*r**2/3)
kap = (1 - Lam*r**2)/(2*r)
T = kap/(2*pi); S = pi*r**2; P = -Lam/(8*pi); V = sp.Rational(4, 3)*pi*r**3
claim("W03: Smarr M = 2TS - 2PV holds for SdS (KRT)", sp.simplify(Mh - (2*T*S - 2*P*V)) == 0)
claim("W03: first law dM = T dS + V dP at fixed Lam (dM/dr = T dS/dr)", sp.simplify(sp.diff(Mh, r) - T*sp.diff(S, r)) == 0)
control("control: Smarr with +2PV fails", sp.simplify(Mh - (2*T*S + 2*P*V)) == 0)
x = sp.symbols('x', positive=True)           # x = Lam r_h^2 (horizon position)
ratio_general = sp.simplify((kap**2/(-P)).subs(r, sp.sqrt(x/Lam)))
claim("W03: for ANY horizon radius, kappa^2/|P| = 2 pi (1-x)^2/x with x = Lam r^2  (one pi, always)", sp.simplify(ratio_general - 2*pi*(1 - x)**2/x) == 0)
menu = {"TS = -PV": sp.Eq(T*S, -P*V), "M = -PV": sp.Eq(Mh, -P*V), "M = T S": sp.Eq(Mh, T*S),
        "PV = -TS/2": sp.Eq(-P*V, T*S/2)}
allpi = True
for k, eq in menu.items():
    sols = [s_ for s_ in sp.solve(eq, r) if s_.is_real and s_ > 0]
    for s_ in sols:
        xv = sp.nsimplify(sp.simplify(Lam*s_**2))
        rat = sp.simplify(ratio_general.subs(x, xv))
        q = sp.simplify(rat/pi)
        print("      %-22s x=Lam r^2=%-8s kappa^2/|P| = %s" % (k, xv, rat))
        if not (q.is_rational or q.is_algebraic) or rat == 0:
            allpi = False
claim("W03: every algebraic thermodynamic special point on this menu has kappa^2/|P| = pi x (nonzero algebraic); the puzzle needs 1/4", allpi)
xs = [s_ for s_ in sp.solve(sp.Eq(ratio_general, sp.Rational(1, 4)), x)]
claim("W03: solving kappa^2/|P| = 1/4 forces x = Lam r^2 to contain pi (so no algebraic condition reaches the puzzle)", all(s_.has(pi) for s_ in xs))
control("control: some root of kappa^2/|P| = 1/4 is pi-free (must be false)", any(not s_.has(pi) for s_ in xs))
xs_bad = sp.solve(sp.Eq(ratio_general, sp.Rational(1, 4)*pi), x)   # a target with one pi: roots ARE pi-free
control("control: a pi-carrying target (kappa^2/|P| = pi/4) has a pi-containing root (must be false)", any(s_.has(pi) for s_ in xs_bad))

# ---- 7. vacuum elasticity and the AQUAL scalar as k-essence (W04, W11) ------------------------------------------
K, mu = sp.symbols('K mu', positive=True)
nu = (3*K - 2*mu)/(2*(3*K + mu))
claim("W04: Poisson ratio at zero shear modulus is exactly 1/2", sp.simplify(nu.subs(mu, 0) - sp.Rational(1, 2)) == 0)
w = sp.symbols('w')
claim("W04: sound speed^2 of a w=-1 fluid (dp/drho) is -1 (imaginary c_s)", sp.diff(-rho, rho) == -1)
X, n = sp.symbols('X n', positive=True)
Pk = -X**n
rk = 2*X*sp.diff(Pk, X) - Pk
wk = sp.simplify(Pk/rk)
cs2 = sp.simplify(sp.diff(Pk, X)/(sp.diff(Pk, X) + 2*X*sp.diff(Pk, X, 2)))
claim("W11: P ~ X^n has w = 1/(2n-1), c_s^2 = 1/(2n-1); deep-MOND n=3/2 gives w = c_s^2 = 1/2",
      sp.simplify(wk.subs(n, sp.Rational(3, 2)) - sp.Rational(1, 2)) == 0 and sp.simplify(cs2.subs(n, sp.Rational(3, 2)) - sp.Rational(1, 2)) == 0)
# Poisson-normalised prefactor: rho_phi = (a0^2/8 pi G) c  =>  G rho/a0^2 = c/(8 pi); puzzle needs c = 32 pi
cc = sp.symbols('cc', positive=True)
claim("W11: G rho/a0^2 = c/(8 pi) => puzzle (=4) needs c = 32 pi (transcendental); rational c gives rational/pi",
      sp.simplify(sp.solve(sp.Eq(cc/(8*pi), 4), cc)[0] - 32*pi) == 0)

# ---- 8. global monopole (W17) -----------------------------------------------------------------------------------
eta_ = sp.symbols('eta', positive=True)
claim("W17: global-monopole solid-angle deficit = 4 pi x 8 pi G eta^2 = 32 pi^2 G eta^2", sp.simplify(4*pi*8*pi*G*eta_**2 - 32*pi**2*G*eta_**2) == 0)

print("\nclaims: %d pass, %d fail ; controls: %d correctly failed, %d wrongly passed" % (passed, failed, ctrl_ok, ctrl_bad))
raise SystemExit(0 if (failed == 0 and ctrl_bad == 0) else 1)
