#!/usr/bin/env python3
"""U1-0 -- gates: every reused formula reproduces the committed numbers of the lanes it comes from, before any principle is scored.
Pre-registered in U1_PREREGISTRATION.md (written before this script was run).

Run:    python3 u1_0_gates.py            (real run, exit 0 iff all gates pass)
        python3 u1_0_gates.py --mutate   (control: the sign of G_f is flipped; gate G1 must FAIL; exit 1 = the control works)
Environment: PYTHONDONTWRITEBYTECODE=1
"""
import sys
sys.dont_write_bytecode = True
import math
import mpmath as mp
import sympy as sp
import u1_lib as L

MUT = "--mutate" in sys.argv
chk = L.Checks()
print("=" * 110)
print("U1-0 gates -- " + ("MUTATE CONTROL (sign of G_f flipped)" if MUT else "REAL RUN"))
print("=" * 110)

# ---- G1: Dirac G_f vs the committed Q1 table (q1_3_physics_answers.out)
sgn = -1.0 if MUT else 1.0
Q1_GF = {0.1: -8.062662e-01, 1.0: -4.847062e-02, 2.0: -9.206654e-03, 10.0: -3.540330e-04, 40.0: -2.210624e-05}
worst = 0.0
for M, ref in Q1_GF.items():
    v = sgn * float(L.Gf(M))
    worst = max(worst, abs(v / ref - 1))
    print(f"    G_f({M:5.1f}) = {v:+.6e}   Q1 committed {ref:+.6e}")
chk("G1 G_f reproduces Q1's committed table at 5 masses (rel 1e-5)", worst < 1e-5, f"(worst {worst:.1e})")

# ---- G2: scalar G_s vs Q1/AH4 tables and the closed form f
Q1_GS = {0.1: 9.429156e+01, 1.0: 4.176054e-01, 2.0: 4.515836e-02, 10.0: 1.252604e-03, 40.0: 7.742369e-05}
worst = 0.0
for M, ref in Q1_GS.items():
    v = L.Gs(M)
    worst = max(worst, abs(v / ref - 1))
    print(f"    G_s({M:5.1f}) = {v:+.6e}   Q1 committed {ref:+.6e}")
chk("G2a G_s (AH4 closed form, lambda = 1e-3) reproduces Q1's committed table at 5 masses (rel 1e-4)", worst < 1e-4, f"(worst {worst:.1e})")
f1 = L.scalar_f_closed(0.5, 2.0)
f2 = L.scalar_f_closed(1.0, 1.5)
chk("G2b closed form f reproduces AH4's committed values f(0.5,2.0)=+0.07222646, f(1.0,1.5)=+0.37298834 (rel 1e-6)",
    abs(f1 / 0.07222646 - 1) < 1e-6 and abs(f2 / 0.37298834 - 1) < 1e-6, f"({f1:+.8f}, {f2:+.8f})")

# ---- G3: heavy and light limits
big_f = float(L.Gf(40) * 40 ** 2)
chk("G3a G_f M^2 -> -1/(9 pi) at M = 40 (1e-3)", abs(big_f / (-1 / (9 * math.pi)) - 1) < 1e-3, f"({big_f:+.6f})")
big_s = L.Gs(40) * 40 ** 2
chk("G3b G_s M^2 -> +7/(18 pi) at M = 40 (1%)", abs(big_s / (7 / (18 * math.pi)) - 1) < 1e-2, f"({big_s:+.6f})")
small = float(L.Gf(1e-6))
chk("G3c small-M form G_f = (4/(3 pi))(ln M + gamma_E - 1/6) (1e-6)", abs(small / ((4 / (3 * math.pi)) * (math.log(1e-6) + L.GAMMA_E - 1 / 6)) - 1) < 1e-6, f"({small:+.8f})")
chk("G3d G_f < 0 at every scanned M; G_s > 0 at every scanned M",
    all(float(L.Gf(M)) < 0 for M in (1e-200, 1e-20, 1e-3, 0.1, 0.5, 1, 2, 5, 20, 100)) and all(L.Gs(M) > 0 for M in (0.01, 0.1, 0.5, 1, 2, 5, 20)))
chk("G3e G_f at a heavy mass, M = 3.55e38, has the asymptotic value -1/(9 pi M^2) (250-digit arithmetic; T1 Amendment 1)",
    abs(float(L.Gf(mp.mpf("3.55e38")) * mp.mpf("3.55e38") ** 2 * (-9 * mp.pi) - 1)) < 1e-6)

# ---- G4: dS_2 formulas vs AH1 / N5 committed numbers
chk("G4a dS_2 scalar pair factor r(1.3,0.9)=2.2155335162e-01, r(0.4,0.7)=1.8866840332e-01 (AH1 committed, 1e-9)",
    abs(L.r_s(1.3, 0.9) / 2.2155335162e-01 - 1) < 1e-9 and abs(L.r_s(0.4, 0.7) / 1.8866840332e-01 - 1) < 1e-9,
    f"({L.r_s(1.3, 0.9):.10e}, {L.r_s(0.4, 0.7):.10e})")
chk("G4b dS_2 Dirac current J/(eH): (0.30,0.90)->0.005008970, (1.0,0.30)->0.252007795, (2.0,1.5)->0.034388544 (N5 committed, 1e-6)",
    abs(L.J_f2(0.3, 0.9) / 0.005008970 - 1) < 1e-6 and abs(L.J_f2(1.0, 0.3) / 0.252007795 - 1) < 1e-6 and abs(L.J_f2(2.0, 1.5) / 0.034388544 - 1) < 1e-6,
    f"({L.J_f2(0.3, 0.9):.9f}, {L.J_f2(1.0, 0.3):.9f}, {L.J_f2(2.0, 1.5):.9f})")
chk("G4c g_f(0.5) = 8.658954e-02, g_f(1.0) = 7.469797e-03, g_f(0) = 1/pi (N5 committed)",
    abs(L.g_f2(0.5) / 8.658954e-02 - 1) < 1e-6 and abs(L.g_f2(1.0) / 7.469797e-03 - 1) < 1e-6 and abs(L.g_f2(0) - 1 / math.pi) < 1e-15)

# ---- G5: membrane resistivity and the identity alpha = Z0/(2 R_K)
c_cgs = 2.99792458e10
Z0_gauss = 4 * math.pi / c_cgs                       # s/cm
OHM_PER_S_CM = 8.987551787368176e11                  # 1 s/cm in ohm (Gaussian -> SI)
Z0_from_membrane = Z0_gauss * OHM_PER_S_CM
e_C, h_Js, c_ms = 1.602176634e-19, 6.62607015e-34, 299792458.0
hbar_Js = h_Js / (2 * math.pi)
eps0 = e_C ** 2 / (2 * L.ALPHA_INPUT * h_Js * c_ms)  # defined by alpha (identity)
Z0 = 1.0 / (eps0 * c_ms)
RK = h_Js / e_C ** 2
print(f"    membrane resistivity 4 pi/c = {Z0_from_membrane:.4f} ohm;  Z0 = 1/(eps0 c) = {Z0:.4f} ohm;  R_K = {RK:.4f} ohm;  Z0/(2 R_K) = {Z0 / (2 * RK):.12f};  eps0 = {eps0:.10e}")
chk("G5a membrane resistivity 4 pi/c (Gaussian) equals Z0 = 1/(eps0 c) = 376.73 ohm (1e-6)", abs(Z0_from_membrane / Z0 - 1) < 1e-6)
chk("G5b alpha = Z0/(2 R_K) (identity, 1e-12) and eps0 equals CODATA 2022 8.8541878188e-12 within 1e-8", abs(Z0 / (2 * RK) / L.ALPHA_INPUT - 1) < 1e-12 and abs(eps0 / 8.8541878188e-12 - 1) < 1e-8)
# the sheet-conductance / conductance-quantum ratio used by P02 and P05: G_vac R_H = sigma/H and G_vac/(e^2/h) = G/2 (alpha cancels)
for Gval in (1.0, -3.7, 1e-80):
    sigma_over_H = L.ALPHA_INPUT * Gval
    G_vac_SI = sigma_over_H / Z0                      # sigma_SI * (c/H) = eps0 sigma_HL c/H = (sigma/H)/Z0
    ratio_q = G_vac_SI / (e_C ** 2 / h_Js)
    assert abs(ratio_q / (Gval / 2) - 1) < 1e-12, "alpha does not cancel"
    assert abs(G_vac_SI * Z0 / sigma_over_H - 1) < 1e-15
chk("G5c R_H G_vac = sigma/H (P02) and G_vac/(e^2/h) = G(M)/2 with alpha cancelling (P05), at three test values", True)

# ---- G6: the 4D oscillator derivation (P03/P04) and the dS_2 limit
t = sp.symbols("t", real=True)
H, n, q, sig = sp.symbols("H n q sigma", positive=True)
E = sp.Function("E")(t)
J = sp.Function("J")(t)
Jexpr = -(sp.diff(E, t) + n * H * E)                       # from E_t + n H E = -J
eq = sp.Eq(sp.diff(Jexpr, t) + q * H * Jexpr, q * H * sig * E)  # J_t + q H J = q H sigma E
ode = sp.expand(-(eq.lhs - eq.rhs))                       # normalised so that E'' has coefficient +1
expected = sp.diff(E, t, 2) + (n + q) * H * sp.diff(E, t) + q * H * (n * H + sig) * E
chk("G6a eliminating J gives E'' + (n+q) H E' + q H (n H + sigma) E = 0 (sympy)", sp.simplify(ode - expected) == 0)
dS2 = sp.simplify(expected.subs({n: 0, q: 1}))
chk("G6b n = 0, q = 1, sigma H = e^2/pi reproduces N5-3's E'' + H E' + (e^2/pi) E = 0",
    sp.simplify(dS2 - (sp.diff(E, t, 2) + H * sp.diff(E, t) + sig * H * E)) == 0)
s = sp.symbols("s")
poly = s ** 2 - (n + q) * H * s + q * H * (n * H + sig)          # exponents s of E ~ exp(-s t): s^2 - (n+q) H s + q H (n H + sigma) = 0
disc = sp.discriminant(poly, s)
crit = sp.solve(sp.Eq(disc, 0), sig)
print(f"    discriminant zero at sigma = {crit}")
chk("G6c critical damping (zero discriminant) at sigma/H = (n-q)^2/(4q)", len(crit) == 1 and sp.simplify(crit[0] / H - (n - q) ** 2 / (4 * q)) == 0)
chk("G6d dS_2 check: critical damping at sigma H = e^2/pi = H^2/4 (e^2/H^2 = pi/4, N5-3)", sp.simplify(crit[0].subs({n: 0, q: 1}) / H - sp.Rational(1, 4)) == 0)
val = [sp.simplify(crit[0].subs({n: 2, q: qq}) / H) for qq in (1, 2, 3, 4)]
print(f"    (n,q)=(2,q), q=1,2,3,4: critical sigma/H = {val}   resonance sigma/H = 1/q-n: {[sp.Rational(1, qq) - 2 for qq in (1, 2, 3, 4)]}")
chk("G6e (n,q)=(2,q): critical sigma/H = 1/4, 0, 1/12, 1/4 (Amendment 1)", val == [sp.Rational(1, 4), 0, sp.Rational(1, 12), sp.Rational(1, 4)])
res_c = [sp.simplify(sp.solve(sp.Eq(q * (n + sig / H), 1), sig)[0] / H).subs({n: 2, q: qq}) for qq in (1, 2, 3, 4)]
chk("G6f resonance q H (n H + sigma) = H^2: sigma/H = 1/q - n = -1, -3/2, -5/3, -7/4 at n = 2", res_c == [-1, sp.Rational(-3, 2), sp.Rational(-5, 3), sp.Rational(-7, 4)])

# ---- G7: dilution of a homogeneous field in dS_4 (AH4 V3): nabla_nu F^(nu z) = -2 E H / a
tt, EE, HH = sp.symbols("tau E H_", real=True)
a = -1 / (HH * tt)
Ftz_up = -EE / a ** 2
div = sp.simplify(sp.diff(a ** 4 * Ftz_up, tt) / a ** 4)
chk("G7 nabla_nu F^(nu z) = -2 E H / a at tau=-1 (H=1,E=1): |value| = 2", abs(abs(float(div.subs({tt: -1, HH: 1, EE: 1}))) - 2.0) < 1e-12, f"({div})")

# ---- G8: the back-reaction ceiling and the electron's M
lm = L.lam_max()
Me = L.Mof(0.51099895)
print(f"    H_Lambda = {L.H_EV:.4e} eV;  M_e = m_e/H = {Me:.4e};  lambda_max = {lm:.4e};  sqrt(lambda_max) = {math.sqrt(lm):.3e};  rho_E/rho_L at lambda_max = {L.energy_ratio(lm):.4f}")
chk("G8a at lambda = lambda_max the field energy density equals rho_Lambda (ratio 1 to 1e-12)", abs(L.energy_ratio(lm) - 1) < 1e-12)
chk("G8b T1's electron M = 3.55e38 (H_0) rescales to M_e = 4.29e38 with H_Lambda = H_0 sqrt(Omega_Lambda)", abs(Me / (3.554e38 / math.sqrt(0.685)) - 1) < 2e-3, f"(M_e = {Me:.4e})")

print(f"\nGATES: {sum(o for _, o in chk.items)}/{len(chk.items)} passed")
if not MUT:
    print("All reused ingredients reproduce their sources; the principle scripts may use them.")
L.finish(chk, MUT, targeted_tags=["G1"])
