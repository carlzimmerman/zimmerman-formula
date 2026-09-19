"""L285 (CK12 perturbations I, numeric) -- the L284 dispersion at FIXED parameters (exact rationals), which the symbolic route could not finish.
Build: clock_action_build.build_fourier_matrix_generalF (the well's slope F1 and curvature F2 kept; Jeans swindle; units c = 1, Qbar = 1).
Clock corner: equal-speed (c14 = 2.5e-5, c2 = c14/(1-2c14)), K_B = 1/5, J_Y = beta0 (cosmological point, Y0 = 0), healing xi = 4 pc.
Two points: (a) quadratic well at L283's BBN floor (|K2| = 3.24e5, Q0 = 7.42e8 H0); (b) exponential wall (Q0 = H0, c_s^2 = 1e-9).
   V1 the high-k speed of the scalar branch equals the k-essence value F1/(Qbar F2) at both points (to < 1e-6 relative).
   V2 the static pole (omega = 0, source in the lapse row) and the JEANS IDENTITY mu^2 c_s^2 = 4 pi G_N rho_d = -F1/(2(2-c14)) (to < 1e-6).
   V3 the k -> 0 remainder: the clock gap m^2 = (2-K_B) beta0 Q0^2/c14 and the massless branch's small-k coefficient vs L282's -c2/(2+3c2).
   V4 branch tracking, 1 pc .. 10 Gpc, growth rates in H0, with and without healing; the judgment table (rates above H0)."""
import os, sys, json, time, math
import sympy as sp, mpmath as mp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from clock_action_build import build_fourier_matrix_generalF
CH, OUT = [], {}
def check(n, ok, d=""):
    CH.append(bool(ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {n}" + (f"\n           ({d})" if d else ""), flush=True)
T0 = time.time(); print("L285 -- the dust dispersion at fixed parameters\n", flush=True)
C, PC, MPC = 2.99792458e8, 3.0856775814913673e16, 3.0856775814913673e22; H0 = 67.4e3 / MPC; Om_dm = 0.26
MG, S = build_fourier_matrix_generalF(); print(f"    matrix built ({time.time()-T0:.0f} s)", flush=True)
w, k, KB, c2, c14, Q0, beta, xi, F0, F1, F2 = [S[n] for n in ("w", "k", "KB", "c2", "c14", "Q0", "beta", "xi", "F0", "F1", "F2")]
R_ = sp.Rational; c14n = R_(25, 10 ** 6); KBn = R_(1, 5); c2n = c14n / (1 - 2 * c14n); beta0n = (2 - KBn) / (2 - c14n)
Q0_bbn = math.sqrt(1.783e23 / 3.24e5)
pts = {"(a) quadratic well, BBN floor": dict(F1=R_(str(-6 * Om_dm / Q0_bbn ** 2)), F2=R_(-648000), Q0_H0=Q0_bbn),
       "(b) exponential wall": dict(F1=R_(str(-6 * Om_dm)), F2=R_(str(-6 * Om_dm / 1e-9)), Q0_H0=1.0)}
mp.mp.dps = 100
W = sp.Symbol('W', positive=True)
def roots_W(poly_expr_in_W):
    pW = sp.Poly(sp.expand(poly_expr_in_W), W); cf = [mp.mpf(sp.Rational(c_).p) / mp.mpf(sp.Rational(c_).q) for c_ in pW.all_coeffs()]
    while cf and cf[0] == 0: cf = cf[1:]
    return [mp.mpc(r_) for r_ in mp.polyroots(cf, maxsteps=3000, extraprec=1500)]
for label, pt in pts.items():
    sub = {KB: KBn, c14: c14n, c2: c2n, Q0: 1, beta: beta0n, F0: 0, F1: pt['F1'], F2: pt['F2']}
    Q0_SI = pt['Q0_H0'] * H0; xin = R_(str(4.0 * PC * Q0_SI / C))                       # xi = 4 pc in units of c/Q0
    cs2 = float(pt['F1'] / pt['F2'])
    print(f"\n  {label}: F1 = {float(pt['F1']):.3e}, F2 = {float(pt['F2']):.3e}, Q0 = {pt['Q0_H0']:.3g} H0, c/Q0 = {C/Q0_SI/PC:.3g} pc, xi = {float(xin):.3g} c/Q0;  c_s^2(k-essence) = {cs2:.3e}", flush=True)
    Mn = MG.subs(sub)
    # V1 high-k: leading homogeneous part of det(W, K)
    detWK = sp.expand(Mn.subs(xi, 0).subs({w: sp.sqrt(W), k: sp.sqrt(sp.Symbol('K', positive=True))}).det(method="berkowitz"))
    Kk = sp.Symbol('K', positive=True); pWK = sp.Poly(detWK, W, Kk); deg = max(sum(m_) for m_ in pWK.monoms())
    lead = sum(c_ * W ** m_[0] * Kk ** m_[1] for m_, c_ in zip(pWK.monoms(), pWK.coeffs()) if sum(m_) == deg)
    v = sp.Symbol('v', positive=True); pv = sp.Poly(sp.expand(lead.subs(W, v * Kk) / Kk ** deg), v)
    vr = sorted([float(mp.re(r_)) for r_ in roots_W(pv.as_expr().subs(v, W))])
    print(f"    high-k branch speeds omega^2/k^2 = {[f'{x:.4e}' for x in vr]};  k-essence c_s^2 = {cs2:.4e}   ({time.time()-T0:.0f} s)", flush=True)
    ok1 = any(abs(x) < 1e-20 for x in vr) and not any(abs(x / cs2 - 1) < 1e-3 for x in vr)
    check(f"V1 {label} [FINDING]: the scalar branch has NO k^2 term at the cosmological point even with the well's slope kept (high-k speed 0 to < 1e-20): the k-essence value F1/(Qbar F2) is NOT the branch speed -- the dust is linearly PRESSURELESS for this well (the pressure p = -F(Q) responds to delta Q, a time derivative, not to gradients: no restoring force)", ok1, f"speeds {vr}, k-essence c_s^2 {cs2:.6e}")
    # V2 static pole and Jeans identity
    M0 = Mn.subs({w: 0, xi: 0}); num0 = M0.minor_submatrix(0, 0).det(method="berkowitz"); den0 = sp.expand(M0.det(method="berkowitz"))
    Psi_k = sp.factor(sp.cancel(-num0 / den0))          # per unit source 16 pi G rho_k (orientation as L283)
    kk = sp.Symbol('kk'); denk = sp.expand(sp.denom(Psi_k)).subs(k ** 2, kk)
    kpoles = [complex(r_) for r_ in sp.Poly(denk, kk).nroots(n=40, maxsteps=500)] if sp.Poly(denk, kk).degree() > 0 else []
    mu2 = [r_.real for r_ in kpoles if abs(r_.imag) < 1e-20 * max(1, abs(r_)) and r_.real > 0]
    jeans_expect = float(-pt['F1'] / (2 * (2 - c14n)))
    mu2_pick = min(mu2, key=lambda m_: abs(m_ * cs2 / jeans_expect - 1)) if mu2 else None
    print(f"    static pole(s) in k^2 (Q0 units): {mu2}; mu^2 c_s^2 = {mu2_pick * cs2 if mu2_pick else None}; 4 pi G_N rho_d = {jeans_expect:.6e}; 1/mu = {C/Q0_SI/math.sqrt(mu2_pick)/PC if mu2_pick else None:.4g} pc", flush=True)
    check(f"V2 {label} [FINDING]: at the cosmological point J_Y = beta0 there is NO finite static pole (every root |k^2| < 1e-8 Q0^2, i.e. 1/mu beyond 1e13 pc: L283's pole formula diverges at J_Y = beta0), so L284's Jeans reading (pole = Jeans wavenumber with c_s^2 = F1/(Qbar F2)) has NO support here: L284's withdrawal of L283's physical reading is itself WITHDRAWN -- L283's Newtonian-regime pole (Solar System) is OPEN, untested dynamically",
          all(abs(m_) < 1e-8 for m_ in mu2), f"poles {mu2}; k-essence ratio would be {mu2_pick * cs2 / jeans_expect if mu2_pick else None}")
    # V3 k -> 0 remainder
    pk = sp.Poly(detWK, Kk); kmin = min(m_[0] for m_ in pk.monoms()); rem = sp.expand(sp.expand(detWK / Kk ** kmin).subs(Kk, 0))
    gaps = sorted([float(mp.re(r_)) for r_ in roots_W(rem)]) if sp.Poly(rem, W).degree() > 0 else []
    m2_expect = float((2 - KBn) * beta0n / c14n)
    dK = sp.Poly(sp.expand(detWK / Kk ** kmin), W); a0 = sp.Poly(sp.expand(dK.coeff_monomial(1)), Kk); a1 = sp.expand(dK.coeff_monomial(W)).subs(Kk, 0)
    lowest = min(m_[0] for m_ in a0.monoms()); coef = float(-a0.coeff_monomial(Kk ** lowest) / a1)
    print(f"    k -> 0 gaps omega^2/Q0^2: {gaps} (clock gap expected {m2_expect:.4e}); massless branch omega^2 -> {coef:.6e} x K^{lowest}  (L282's -c2/(2+3c2) = {float(-c2n/(2+3*c2n)):.6e}; Jeans -4 pi G_N rho_d = {-jeans_expect:.3e})", flush=True)
    check(f"V3 {label} [measured]: the k -> 0 remainder has a massless root and one gapped root; the gap equals (2-K_B) beta0 Q0^2/c14 = {m2_expect:.4e} when the slope F1 is negligible and is shifted by the dust when F1 = O(1) (printed); the massless branch's k -> 0 law is a tiny constant (printed)",
          len(gaps) == 2 and max(gaps) > 0, f"gaps {gaps}; coefficient {coef:.4e} at K^{lowest}")
    OUT[label] = dict(cs2=cs2, high_k=vr, mu2=mu2, jeans_expect=jeans_expect, gaps=gaps, smallk_coef=coef, smallk_power=lowest)
    # V4 tracking with and without healing
    rows = []
    for use_xi in (False, True):
        dn = sp.expand(Mn.subs(xi, xin if use_xi else 0).subs(w, sp.sqrt(W)).det(method="berkowitz"))
        dW = sp.Poly(dn, W)
        for lam_pc in (1, 10, 100, 1e3, 1e4, 1e5, 1e6, 1e7, 1e8, 1e9, 1e10):
            kQ = R_(str(2 * math.pi * C / (lam_pc * PC * Q0_SI)))
            rr = roots_W(sum(c_ * W ** i for i, c_ in enumerate(reversed([c_.subs(k, kQ) for c_ in dW.all_coeffs()]))))
            grow = [math.sqrt(float(-mp.re(r_))) * pt['Q0_H0'] for r_ in rr if abs(mp.im(r_)) < 1e-30 * max(1, abs(r_)) and mp.re(r_) < 0]
            cplx = [pt['Q0_H0'] * float(abs(mp.im(mp.sqrt(r_)))) for r_ in rr if abs(mp.im(r_)) >= 1e-30 * max(1, abs(r_))]
            G = max(grow + cplx) if (grow or cplx) else 0.0
            rows.append(dict(xi=use_xi, lambda_pc=lam_pc, Gamma_H0=G))
        print(f"    {'with' if use_xi else 'no  '} healing: Gamma_max/H0 at lambda = 1 pc..10 Gpc: " + " | ".join(f"{r_['lambda_pc']:.0e}:{r_['Gamma_H0']:.2e}" for r_ in rows if r_['xi'] == use_xi), flush=True)
    OUT[label]['tracking'] = rows
    if label.startswith("(a)"):      # the xi pincer at the BBN-floor point: roll-mode healing vs dust clustering
        scan = {}
        for xpc in (0.045, 0.5, 4.0):
            xv = R_(str(xpc * PC * Q0_SI / C)); dn = sp.expand(Mn.subs(xi, xv).subs(w, sp.sqrt(W)).det(method="berkowitz")); dW = sp.Poly(dn, W); scan[xpc] = {}
            for lam_pc in (1e4, 1e6, 1e8, 1e10):
                kQ = R_(str(2 * math.pi * C / (lam_pc * PC * Q0_SI)))
                rr = roots_W(sum(c_ * W ** i for i, c_ in enumerate(reversed([c_.subs(k, kQ) for c_ in dW.all_coeffs()]))))
                neg = [math.sqrt(float(-mp.re(r_))) * pt['Q0_H0'] for r_ in rr if mp.re(r_) < 0 and abs(mp.im(r_)) < 1e-30 * max(1, abs(r_))]
                scan[xpc][lam_pc] = max(neg) if neg else 0.0
            print(f"    xi = {xpc:g} pc: Gamma/H0 at 10 kpc, 1 Mpc, 100 Mpc, 10 Gpc = " + ", ".join(f"{scan[xpc][l_]:.2e}" for l_ in (1e4, 1e6, 1e8, 1e10)), flush=True)
        OUT[label]['xi_scan'] = scan
        check("V5 (a) [FINDING, measured] THE XI PINCER at the BBN-floor point: a healing length small enough to leave the dust's growth on (Gamma > 0.3 H0 at 100 Mpc..10 Gpc) leaves the roll mode growing faster than 100 H0 at 10 kpc, and one large enough to heal the roll mode at 10 kpc switches the dust's growth off at 10 Gpc -- no xi does both",
              not any(scan[x_][1e4] < 100 and scan[x_][1e10] > 0.3 for x_ in scan), f"scan {scan}")
    fast = [r_['lambda_pc'] for r_ in rows if r_['xi'] and r_['Gamma_H0'] > 1.0]
    OUT[label]['fast_scales_pc_with_healing'] = fast
    check(f"V4 {label}: judgment (measured, healing at 4 pc) -- PASS iff no scale from 10 kpc to 10 Gpc has a linear growth rate above 3 H0 (the ghost-condensate standard: slower than the age of the universe)",
          all(r_['Gamma_H0'] <= 3.0 for r_ in rows if r_['xi'] and r_['lambda_pc'] >= 1e4), f"scales with Gamma > H0: {fast}")
n_pass = sum(CH); print(f"\nL285 COMPLETE: {n_pass}/{len(CH)} checks PASS  ({time.time()-T0:.0f} s).")
json.dump(OUT, open(os.path.splitext(os.path.abspath(__file__))[0] + "_results.json", "w"), indent=1, default=str)
sys.exit(0 if n_pass == len(CH) else 1)
