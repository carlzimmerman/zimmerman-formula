"""STATUS 2026-09-19: INCOMPLETE -- V1 passes; the static solve with F1 != 0 completes (the lapse response acquires a high-degree denominator:
the well's slope couples the clock tilt), the symbolic dispersion determinant did not finish within 1500 s (exit 124 in the .out).
The algebraic core (Jeans identity mu^2 c_s^2 = 4 pi G_N rho_d, power-well sound speed, quadratic-well coldness) is certified in
lean_2026/L284_jeans_identity.lean; the machine confirmation of the dust branch's sound speed and the growth-rate table are NOT done.

L284 (CK12, perturbations I) -- the candidate's dust as a fluid: its sound speed, its Jeans scale and its growth mode, DERIVED from
the action with the well's slope F_Q(Qbar) != 0 kept (the background carries dust: 16 pi G rho_d = F0 - Qbar F1).
Sub-horizon Minkowski build (clock_action_build.build_fourier_matrix_generalF; Jeans swindle = the O(eps) tadpole dropped, exact to
O((aH/k)^2)).  Nothing is quoted: the matrix is built from THE_ACTION as in L279-L283.
   V1 control: F1 = 0, F2 = 2 K2 reproduces L282's Fourier matrix exactly.
   V2 the static lapse with F1: Psi(k) pole and the DUST SOUND SPEED from the high-k dispersion of the scalar branch: c_s^2 = F1/(Qbar F2)
      (the k-essence value), and the JEANS IDENTITY mu_Psi^2 c_s^2 = 4 pi G_N rho_d (Newtonian regime): L283's 'lapse mass' is the dust's
      Jeans wavenumber.  => L283's physical reading (an oscillating Newtonian potential beyond 1/mu, 'DEAD by the pincer') is WITHDRAWN:
      1/mu is the Jeans length, which structure formation wants SMALL (the record's forest threshold L185: c_s^2 <= 1e-9 => 1/mu <= 0.23 Mpc).
      The algebra of L283 (Friedmann, the conservation law, the stiff term, the BBN floor |K2| Q0^2 >= 1.8e23 H0^2, the well scalings) stands.
   V3 the growth mode: with F1 != 0 the k -> 0 structure of the massless branch (does the dust's Jeans instability appear with the
      standard rate ~ sqrt(4 pi G rho_d), i.e. CDM-like growth, and how does L282's roll mode (rate ~ Q0) sit with it?).
   V4 numbers at the two viable-looking points: (a) quadratic well at the BBN floor (Q0 = 7.4e8 H0, |K2| = 3.24e5); (b) exponential wall
      (Q0 = H0, c_s^2 = 1e-9, F2 = F1/(Qbar c_s^2)): branch tracking over 1 pc .. 10 Gpc with the healing term at xi = 4 pc, growth rates in H0.
   V5 the judgment table: scales where the linear growth rate exceeds H0 (faster than the age of the universe -- the ghost-condensate
      standard), per point.
A FAIL is a finding; thresholds are stated derivations or measurements."""
import os, sys, json, time, math
import sympy as sp
import mpmath as mp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from clock_action_build import build_fourier_matrix, build_fourier_matrix_generalF
CH, OUT = [], {}
def check(n, ok, d=""):
    CH.append(bool(ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {n}" + (f"\n           ({d})" if d else ""), flush=True)
T0 = time.time(); print("L284 (CK12 I) -- the dust's sound speed, Jeans scale and growth mode from the action\n", flush=True)
C, PC, MPC, AU = 2.99792458e8, 3.0856775814913673e16, 3.0856775814913673e22, 1.495978707e11
H0 = 67.4e3 / MPC; Om_dm = 0.26
MG, S = build_fourier_matrix_generalF(); print(f"    general-F matrix built ({time.time()-T0:.0f} s)", flush=True)
w, k, KB, c2, c14, Q0, beta, xi, F0, F1, F2 = [S[n] for n in ("w", "k", "KB", "c2", "c14", "Q0", "beta", "xi", "F0", "F1", "F2")]
M2, S2 = build_fourier_matrix(); K2 = S2['K2']
diff = (MG.subs({F0: 0, F1: 0, F2: 2 * K2}) - M2.subs({S2['w']: w, S2['k']: k, S2['KB']: KB, S2['c2']: c2, S2['c14']: c14, S2['Q0']: Q0, S2['beta']: beta, S2['xi']: xi}))
check("V1 control: with F0 = F1 = 0 and F2 = 2 K2 the general-well matrix equals L282's matrix entry by entry", all(sp.simplify(d_) == 0 for d_ in diff), f"max residual entries: {[sp.simplify(d_) for d_ in diff if sp.simplify(d_) != 0][:3]}")
G, pi_, rho_k = sp.symbols('G pi rho_k', positive=True)
beta0 = (2 - KB) / (2 - c14)
# ---- V2 static lapse with F1, and the high-k sound speeds
MG = MG.subs(F0, 0)                                              # the well's value at the background is negligible (F0 = O(q^2))
M0 = MG.subs({w: 0, xi: 0})
src = sp.Matrix([-16 * pi_ * G * rho_k, 0, 0, 0])              # orientation as L283 (attractive Newtonian limit)
num0 = sp.factor(M0.minor_submatrix(0, 0).det(method="berkowitz")); den0 = sp.factor(M0.det(method="berkowitz"))
Psi_k = sp.factor(sp.cancel(src[0] * num0 / den0)); print(f"    static solve done by cofactors ({time.time()-T0:.0f} s)", flush=True)
print(f"    static lapse with the well's slope: Psi(k) = {Psi_k}")
kk = sp.Symbol('kk'); den = sp.expand(sp.denom(Psi_k)).subs(k ** 2, kk)
poles = [sp.factor(p_) for p_ in sp.solve(den, kk)]
print(f"    pole(s) in k^2: {poles}")
OUT["Psi_k"] = str(Psi_k); OUT["poles"] = [str(p_) for p_ in poles]
# high-k dispersion at the cosmological point beta = beta0: leading homogeneous part of det in (W, K)
W, Kk = sp.symbols('W K', positive=True)
# the dispersion: clock parameters at the equal-speed corner (c14 = 2.5e-5, c2 = c14/(1-2c14), K_B = 1/5) and Qbar = 1 as exact rationals; F1, F2, beta symbolic
c14n = sp.Rational(25, 10 ** 6); NUM = {KB: sp.Rational(1, 5), c14: c14n, c2: c14n / (1 - 2 * c14n), Q0: 1}
det = MG.subs(xi, 0).subs(NUM).subs({w: sp.sqrt(W), k: sp.sqrt(Kk)}).det(method="berkowitz"); print(f"    det built ({time.time()-T0:.0f} s)", flush=True)
detWK = sp.expand(det); print(f"    det expanded: {len(detWK.args)} terms ({time.time()-T0:.0f} s)", flush=True)
pWK = sp.Poly(detWK, W, Kk)
deg = max(sum(m_) for m_ in pWK.monoms())
lead = sum(c_ * W ** m_[0] * Kk ** m_[1] for m_, c_ in zip(pWK.monoms(), pWK.coeffs()) if sum(m_) == deg)
v = sp.Symbol('v', positive=True)
pv = sp.Poly(sp.expand(lead.subs(W, v * Kk) / Kk ** deg), v)
roots_hi = [sp.factor(r_) for r_ in sp.solve(pv.as_expr(), v)]
print(f"    high-k branch speeds (general F, Q0 kept): {roots_hi}   ({time.time()-T0:.0f} s)")
cs2_kess = F1 / (Q0 * F2); beta0n = beta0.subs(NUM)
prod = sp.factor(pv.all_coeffs()[-1] / pv.all_coeffs()[0]) if pv.degree() == 2 else None
print(f"    product of the two high-k speeds: {prod}")
# identify the dust branch: the root that vanishes when F1 -> 0 at beta = beta0
dust_root = [r_ for r_ in roots_hi if sp.simplify(r_.subs(beta, beta0n).subs(F1, 0)) == 0]
cs2_dust = sp.factor(sp.simplify(dust_root[0].subs(beta, beta0n))) if dust_root else None
print(f"    dust branch (beta = beta0): c_s^2 = {cs2_dust}")
OUT["cs2_dust"] = str(cs2_dust)
ok2a = cs2_dust is not None and sp.simplify(cs2_dust - cs2_kess.subs(NUM)) == 0
if not ok2a and cs2_dust is not None:
    ratio = sp.factor(sp.simplify(cs2_dust / cs2_kess.subs(NUM))); print(f"    c_s^2 / [F1/(Qbar F2)] = {ratio}")
    # small-F1 limit of the ratio
    print(f"    ... its F1 -> 0 limit: {sp.limit(ratio, F1, 0)}")
check("V2a THE DUST SOUND SPEED: at the cosmological point (J_Y = beta0, where the MOND stiffness vanishes, L282) the scalar branch's high-k speed is c_s^2 = F1/(Qbar F2) -- the k-essence value delta p/delta rho of the well (exactly, or to leading order in the dust density F1: printed)",
      ok2a or (cs2_dust is not None and sp.simplify(sp.limit(sp.simplify(cs2_dust / cs2_kess.subs(NUM)), F1, 0) - 1) == 0), f"c_s^2 = {cs2_dust}")
# Jeans identity with the Newtonian-regime pole
pole_N = [sp.limit(p_, beta, sp.oo) for p_ in poles]
pole_N = [sp.factor(p_) for p_ in pole_N if p_ != 0]
rho_d16 = F0 - Q0 * F1                                             # 16 pi G rho_d
jeans = sp.factor(sp.cancel(pole_N[0] * cs2_kess)) if pole_N else None
expect_jeans = sp.factor((-Q0 * F1) / (2 * (2 - c14)))            # 4 pi G_N rho_d with 16 pi G rho_d = -Qbar F1, G_N = G/(1 - c14/2)
print(f"    Newtonian-regime pole mu^2 = {pole_N};  mu^2 c_s^2 = {jeans};  4 pi G_N rho_d = {expect_jeans}")
ok2b = jeans is not None and sp.simplify(jeans - expect_jeans) == 0
if not ok2b and jeans is not None: print(f"    ratio (mu^2 c_s^2)/(4 pi G_N rho_d) = {sp.factor(sp.simplify(jeans / expect_jeans))}")
check("V2b THE JEANS IDENTITY: mu_Psi^2 c_s^2 = 4 pi G_N rho_d exactly (Newtonian regime, F0 -> 0): L283's 'mass of the Newtonian potential' is the dust's Jeans wavenumber -- the static pole marks where pressure support gives way to collapse, not an oscillation of gravity. L283's B2/C3 physical readings are WITHDRAWN; its algebra stands",
      ok2b, f"mu^2 c_s^2 = {jeans} vs {expect_jeans}")
OUT["jeans_identity"] = dict(mu2_cs2=str(jeans), four_pi_GN_rho=str(expect_jeans))
# the forest reading: 1/mu <= c_s/sqrt(4 pi G_N rho_d) with L185's c_s^2 <= 1e-9
L_forest = math.sqrt(1e-9) / (H0 * math.sqrt(1.5 * Om_dm)) * C / MPC
print(f"    with the record's forest threshold (L185, CLASS scan: c_s^2 <= 1e-9 for P(k = 5 h/Mpc, z = 3) within 10%): 1/mu_Psi = lambda_J/(2 pi) <= {L_forest:.2f} Mpc -- SMALL, the opposite of L283's '>= 1-3 Mpc'")
OUT["L_forest_Mpc"] = L_forest
# ---- V3 the k -> 0 structure with F1
pk = sp.Poly(detWK, Kk); kmin = min(m_[0] for m_ in pk.monoms()); rem = sp.expand(sp.expand(detWK / Kk ** kmin).subs(Kk, 0))
gaps = [sp.factor(r_) for r_ in sp.solve(rem, W)]
print(f"    k -> 0: det = K^{kmin} x [...]; remainder roots in omega^2: {gaps}")
OUT["gaps"] = [str(g_) for g_ in gaps]
dK = sp.Poly(sp.expand(detWK / Kk ** kmin), W)
a0 = sp.expand(dK.coeff_monomial(1)); a1 = sp.expand(dK.coeff_monomial(W))
a0K = sp.Poly(a0, Kk); lowest = min(m_[0] for m_ in a0K.monoms())
slow_small_k = sp.factor(-a0K.coeff_monomial(Kk ** lowest) / a1.subs(Kk, 0))
print(f"    massless branch at k -> 0: omega^2 -> [{slow_small_k}] x K^{lowest}")
OUT["massless_small_k"] = str(slow_small_k)
check("V3 with the well's slope kept, the k -> 0 remainder still has the roots {0, m^2 = (2-K_B) J_Y Q0^2/c14} (the clock gap is unchanged by the dust; numeric clock corner) and the massless branch's leading small-k coefficient is exhibited (printed; L282's value was -c2/(2+3c2) at F1 = 0)",
      any(sp.simplify(g_ - ((2 - KB) * beta * Q0 ** 2 / c14).subs(NUM)) == 0 for g_ in gaps), f"gaps {gaps}; small-k coefficient {slow_small_k} (L282 value at this corner: {(-c2/(2+3*c2)).subs(NUM)})")
# ---- V4 numbers: branch tracking at the two points (units: Q0 = 1, c = 1; k in Q0/c; healing xi = 4 pc)
mp.mp.dps = 60
def track(point, label, xi_pc=4.0):
    subs_ = {KB: sp.Rational(1, 5), c14: sp.Rational(str(point['c14'])), c2: sp.Rational(str(point['c14'])) / (1 - 2 * sp.Rational(str(point['c14']))), Q0: 1,
             F0: 0, F1: sp.Rational(str(point['F1'])), F2: sp.Rational(str(point['F2'])), beta: (2 - sp.Rational(1, 5)) / (2 - sp.Rational(str(point['c14'])))}
    subs_[xi] = sp.Rational(str(xi_pc * PC * point['Q0_SI'] / C))            # xi in units of c/Q0
    dn = sp.expand(MG.subs(subs_).det(method="berkowitz"))
    dWk = sp.Poly(sp.expand(dn.subs(w, sp.sqrt(W))), W)
    rows = []
    for lam_pc in (1, 10, 100, 1e3, 1e4, 1e5, 1e6, 1e7, 1e8, 1e9, 1e10):
        kQ = 2 * math.pi * C / (lam_pc * PC * point['Q0_SI'])                 # k in units of Q0/c
        cf = [mp.mpf(str(sp.N(c_.subs(k, sp.Rational(str(kQ))), 70))) for c_ in dWk.all_coeffs()]
        while cf and cf[0] == 0: cf = cf[1:]
        try:
            rr = mp.polyroots(cf, maxsteps=800, extraprec=400)
        except mp.libmp.libhyper.NoConvergence:
            rr = []
        rates = []
        for r_ in rr:
            r_ = mp.mpc(r_)
            if abs(mp.im(r_)) > 1e-20 * max(1, abs(r_)): rates.append(("cplx", float(mp.re(r_)), float(mp.im(r_)))); continue
            re = float(mp.re(r_))
            rates.append(("grow" if re < 0 else "osc", re))
        growth = [math.sqrt(-r_[1]) * point['Q0_H0'] for r_ in rates if r_[0] == "grow"]
        Gmax = max(growth) if growth else 0.0
        rows.append(dict(lambda_pc=lam_pc, Gamma_max_H0=Gmax, roots=rates))
        print(f"      {label}: lambda = {lam_pc:.0e} pc: Gamma_max = {Gmax:.3e} H0   (omega^2/Q0^2 roots: {[(r_[0], f'{r_[1]:.3e}') for r_ in rates]})")
    return rows
Q0_bbn_H0 = math.sqrt(1.783e23 / 3.24e5)
pts = {"quadratic well at the BBN floor (|K2| = 3.24e5, Q0 = 7.4e8 H0, equal-speed c14 = 2.5e-5)":
           dict(c14=2.5e-5, F2=-2 * 3.24e5, F1=-6 * Om_dm / Q0_bbn_H0 ** 2, Q0_H0=Q0_bbn_H0, Q0_SI=Q0_bbn_H0 * H0),
       "exponential wall (Q0 = H0, c_s^2 = 1e-9, equal-speed c14 = 2.5e-5)":
           dict(c14=2.5e-5, F1=-6 * Om_dm, F2=-6 * Om_dm / 1e-9, Q0_H0=1.0, Q0_SI=H0)}
TR = {}
for label, pt in pts.items():
    print(f"    {label}: F1 = {pt['F1']:.3e}, F2 = {pt['F2']:.3e} (units Q0 = 1); c_s^2 = F1/(Q0 F2) = {pt['F1']/pt['F2']:.2e}")
    TR[label] = track(pt, label[:12])
OUT["tracking"] = {lab: [dict(lambda_pc=r_['lambda_pc'], Gamma_max_H0=r_['Gamma_max_H0']) for r_ in rows] for lab, rows in TR.items()}
fast = {lab: [r_['lambda_pc'] for r_ in rows if r_['Gamma_max_H0'] > 1.0] for lab, rows in TR.items()}
print(f"    scales with a linear growth rate above H0 (faster than the age of the universe): {fast}")
check("V4/V5 judgment (measured, both points, healing at xi = 4 pc): the table above lists the maximal growth rate per scale; PASS iff no scale between 10 kpc and 10 Gpc grows faster than 3 H0 at the exponential-wall point (Q0 = H0) -- the quadratic well's BBN-floor point is reported as measured",
      all(r_['Gamma_max_H0'] <= 3.0 for r_ in TR[list(pts)[1]] if r_['lambda_pc'] >= 1e4), f"fast scales: {fast}")
n_pass = sum(CH); print(f"\nL284 COMPLETE: {n_pass}/{len(CH)} checks PASS  ({time.time()-T0:.0f} s).")
json.dump(OUT, open(os.path.splitext(os.path.abspath(__file__))[0] + "_results.json", "w"), indent=1, default=str)
sys.exit(0 if n_pass == len(CH) else 1)
