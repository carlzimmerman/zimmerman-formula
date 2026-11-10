"""R541A GA2: is the induced density cold and separate, or locked to the baryons?

Part 1 (sympy): Newtonian-gauge expansion of the coupling -alpha m_N n_rest sqrt(-g) (Q - 1) (and the general f via
f'(1), f''(1)) to second order in eps (Phi ~ eps^2, v ~ eps, pi_t ~ eps^2, pi_x ~ eps), 1D, c = 1.
  tau = t + pi(t, x);  Q^2 = (1 + pi_t)^2/(1 + 2 Phi) - pi_x^2/(1 - 2 Phi);  clock frame velocity v_K = -pi_x.
  sqrt(-g) n_rest = Ncal * sqrt(1 + 2 Phi - (1 - 2 Phi) v^2)  (Ncal = conserved coordinate number density).
Part 2 (numpy/scipy): linear Fourier-mode toy of the tightly coupled photon-baryon fluid + clock charge + gravity
  (static background, Jeans swindle), equations derived in Part 1.
Output: ga2_perturbations.out (same folder).
"""
import os
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp

HERE = os.path.dirname(os.path.abspath(__file__))
out = open(os.path.join(HERE, "ga2_perturbations.out"), "w")
def P(*a):
    s = " ".join(str(x) for x in a); print(s); out.write(s + "\n")

P("# R541A GA2: linear perturbations in the tightly coupled era")
e, al, m, f1, f2 = sp.symbols('epsilon alpha m f1 f2')
Phi, pit, pix, v, Nc = sp.symbols('Phi pi_t pi_x v Ncal')
Q = sp.sqrt((1 + e**2*pit)**2/(1 + 2*e**2*Phi) - e**2*pix**2/(1 - 2*e**2*Phi))
dtau_p = sp.sqrt(1 + 2*e**2*Phi - (1 - 2*e**2*Phi)*e**2*v**2)
x = Q - 1
fQ = f1*x + f2*x**2/2                         # generic f with f(1) = 0
Lc = -al*m*Nc*dtau_p*fQ
Lc2 = sp.expand(sp.series(Lc, e, 0, 3).removeO()).subs(e, 1)
P("Part 1. coupling to O(eps^2):  L_c =", sp.factor(Lc2))
P("  -> only f'(1) enters at this order; f''(1) starts at O(eps^4) (it changes the clock's stiffness near baryons, no charge).")
# integrate by parts the pi_t term using baryon continuity: -Ncal pi_t ~ + Ncal v pi_x (total derivatives dropped)
Lc2_ibp = Lc2.subs(pit, 0) + (-al*m*f1)*(-1)*(-Nc*v*pix)*(-1)
# explicit: coefficient of pi_t in Lc2 is -al m f1 Ncal; -Ncal pi_t = d(.) + Ncal v pi_x
coef = sp.simplify(sp.diff(Lc2, pit))
Lc2_ibp = sp.expand(Lc2.subs(pit, 0) + coef*(-v*pix))
vK, vb = sp.symbols('v_K v_b')
target = al*m*f1*Nc*((vb - vK)**2/2 - vb**2/2 + Phi)
chk = sp.simplify(Lc2_ibp.subs({pix: -vK, v: vb}) - target)
P("  coefficient of pi_t:", coef, " ; after IBP with continuity:", sp.factor(Lc2_ibp))
P("  = alpha m f'(1) Ncal [ (v_b - v_K)^2/2 - v_b^2/2 + Phi ]  residual:", chk)
P("  Reading: mass renormalisation m -> m(1 - alpha f'(1)) in BOTH the kinetic and the potential term, plus an")
P("  entrainment term E (v_b - v_K)^2/2 with E = alpha f'(1) rho_b, plus a total derivative (the canonical-charge shift).")

# Charge equation: vary pi in L_K + L_c. L_K -> rho_K(-pi_x^2/2 ...) with rho_K = M0 (Q-1); d L/d pi_x of L_c:
Lc_pix = sp.diff(Lc2_ibp, pix).subs({pix: -vK, v: vb})
P("  dL_c/d(pi_x) =", sp.factor(Lc_pix), "= E (v_b - v_K)  ->  clock charge equation")
P("    d_t rho_K + d_x [ rho_K v_K + E (v_b - v_K) ] = 0 ;  with d_t E + d_x (E v_b) = 0 (E is per baryon):")
P("    d_t (rho_K - E) + d_x [ (rho_K - E) v_K ] = 0.   So sigma := rho_K - E (the canonical charge density, = C/a^3")
P("    in the background) moves with the clock frame (cold); E moves with the baryons (locked).")
P("  Clock Euler: rho_K = M0 (pi_t - Phi - pi_x^2/2)  =>  d_t v_K = -d_x (Phi + delta rho_K / M0): the clock frame free-falls;")
P("  the coupling does not enter it.")
P("  Baryon momentum: dL/dv_b = (1 - alpha)rho v_b + E (v_b - v_K) = rho v_b - E v_K; force -(1 - alpha) rho dPhi.")
P("  With d_t v_K = -dPhi: rho d_t v_b = -rho dPhi  -> baryon Euler unchanged (inertia and weight both rho = m n).")
P("  Poisson source: (1 - alpha) rho delta_b + delta rho_K (+ photons).")

# ---------------- Part 2: numerical toy ----------------
P("\nPart 2. Fourier-mode toy (units: 4 pi G rho_tot_bare = 1, k chosen sub-sound-horizon), adiabatic start.")
def run(alpha, sigma_over_rho, rg_over_rb=1.6, k=40.0, T=3.0, M0inv=0.0):
    rb = 1.0
    E = alpha*rb
    rK = E + sigma_over_rho*rb
    rg = rg_over_rb*rb
    norm = (rb + rK - alpha*rb + rg)      # background active density (photons counted once, toy)
    FourPiG = 1.0/norm
    # state: delta_b, delta_g, v_b, drhoK, v_K  (v as amplitude of i k v -> use theta = i k v real form)
    def rhs(t, y):
        db, dg, th_b, drK, th_K = y
        src = (1 - alpha)*rb*db + drK + rg*dg
        Phi = -FourPiG*src/k**2                         # -k^2 Phi = 4 pi G src
        # theta = i k v ; d_t delta = -theta ; d_t theta = k^2 (Phi + p/rho) for Euler with -ik
        d_db = -th_b
        d_dg = -(4.0/3.0)*th_b
        Rload = 3*rb/(4*rg)
        d_th_b = (k**2*(dg/4.0))/(1 + Rload) + k**2*Phi       # tight coupling: (rho+4rg/3)v_b ; pressure rg dg/3
        d_th_K = k**2*(Phi + M0inv*drK)
        d_drK = -(rK*th_K + E*(th_b - th_K))
        return [d_db, d_dg, d_th_b, d_drK, d_th_K]
    y0 = [1.0, 4.0/3.0, 0.0, rK*1.0, 0.0]
    ts = np.linspace(0, T, 3001)
    s = solve_ivp(rhs, (0, T), y0, t_eval=ts, rtol=1e-10, atol=1e-12)
    db, dg, thb, drK, thK = s.y
    locked = E*db
    free = drK - locked
    return ts, db, dg, drK, locked, free, rK

for foot, R in [("canonical", 5.410), ("alt", 5.412)]:
    A = R/(1 + R)
    P(f"\n## footing {foot}: alpha = R/(1+R) = {A:.5f} (the naive background value of GA1)")
    # KA: alpha = 0, sigma = 0: textbook acoustic frequency without gravity
    rg = 1.6
    Rload = 3/(4*rg)
    ts, db, dg, drK, lk, fr, rK = run(0.0, 0.0, rg_over_rb=rg, k=200.0, T=0.5)
    # frequency from zero crossings of delta_g - mean
    sig = dg - np.mean(dg)
    zc = ts[1:][np.diff(np.sign(sig)) != 0]
    w_num = np.pi/np.mean(np.diff(zc))
    w_th = 200.0/np.sqrt(3*(1 + Rload))
    P(f"  KA alpha=0: acoustic omega numeric {w_num:.4f} vs textbook k/sqrt(3(1+R_b)) {w_th:.4f} (gravity small at k=200)")
    for label, alpha, sig_r in [("Z_can (sigma = 0)", A, 0.0), ("uncoupled baryons (alpha = 0, sigma = 0)", 0.0, 0.0),
                                ("MU: Z_can + free charge sigma = R rho_b", A, R), ("record: alpha = 0, sigma = R rho_b", 0.0, R)]:
        ts, db, dg, drK, lk, fr, rK = run(alpha, sig_r)
        # oscillating part of the clock charge that follows the baryons
        corr = np.max(np.abs(drK - A*db*(alpha > 0))) if alpha > 0 else np.max(np.abs(drK))
        osc = np.max(np.abs(drK - rK*np.interp(ts, ts, np.ones_like(ts))))
        frac_locked = (alpha*1.0)/(rK if rK > 0 else 1)
        P(f"  {label}: rho_K/rho_b = {rK:.4f}; locked E/rho_b = {alpha:.4f}; cold sigma/rho_b = R_cold = {rK - alpha:.4f};"
          f" free part delta rho_K - E delta_b (evolved by the charge equation): start {fr[0]:.4f}, max {np.max(np.abs(fr)):.4f};"
          f" delta_b at end {db[-1]:.4f}")
    # baryon-load bookkeeping
    P(f"  Baryon load seen by the peaks under Z_can: inertia rho = m n (unchanged); co-moving active density"
      f" (1-alpha) rho + E = rho; cold share 0.")
    P(f"  If instead the total matter 6.41 rho_b had to come from this co-moving density, the load would be"
      f" {1+R:.3f} x the measured one: {R*100:.0f} % against a ~1 % determination (factor {R/0.01:.0f}).")
out.close()
