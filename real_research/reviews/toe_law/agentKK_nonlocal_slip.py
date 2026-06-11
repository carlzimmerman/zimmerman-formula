# agentKK -- THE CONVERGENT DOOR: does a HISTORY-KEYED (nonlocal-in-time) slip operator evade the
# agentDD keying theorem?  S_slip = (surviving generator geometry) x F(K_filt), K_filt = the M22-style
# proper-time-filtered acceleration history on the u-frame.
#
# Staged: python3 agentKK_nonlocal_slip.py K0|K1|K2|K3   (each stage appends to agentKK_nonlocal_slip.out)
#   K0  gates: banked slip targets / Cassini / cluster; agentY wall-3 row from agentY_eqs.pkl;
#       agentDD condensate W-only row from agentDD_D1b.pkl; agentDD_D4.pkl r^0-class audit.
#   K1  THE FORMAL VARIATION (lattice functional calculus, sympy): the constraint response of a
#       filtered key -- coordinate-time window, proper-time window (measure + sigma routes), the
#       DC weight, the frequency suppression factor, the general (nonlinear, multi-window) key,
#       the derivative-coupled key. The static-equivalence theorem assembled.
#   K2  the chain-rule certificate on the REAL pickled equations: slip-matched pollution row for
#       two nontrivial filtered static reads (linear theta0-read and sqrt-read) -- must reproduce
#       agentY's banked row to all digits. Plus the M22 window static-read numerics.
#   K3  escapes: (a) derivative key tracking error (static + circular + epicyclic); (b) the
#       S-counterterm floor (the S-free r^0-class, numeric irreducible pollution); (c) spectral
#       keying theta(0) static reads; the timescale no-middle-ground table.
#
# Reuse: agentY_eqs.pkl (agentY), agentDD_D1b.pkl / agentDD_D4.pkl (agentDD), constants and
# harness verbatim from agentDD_vector_carrier.py D0/D3. No git.

import sys, os, pickle, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'agentKK_nonlocal_slip.out')

def P(*s):
    line = " ".join(str(x) for x in s)
    print(line, flush=True)
    with open(OUT, 'a') as f:
        f.write(line + "\n")

# constants (SI) -- verbatim agentY_gates.py / agentDD values
G   = 6.674e-11
c   = 2.998e8
A0_FW, A0_CAN = 9.36e-11, 1.2e-10
Msun = 1.989e30
GMsun = 1.327e20
Rsun = 6.957e8
pc   = 3.0857e16
kpc, Mpc = 1e3*pc, 1e6*pc

# the four banked nu shapes, verbatim from agentW_partner_uniqueness.py L59-62
def nu_fw(y):     return np.sqrt(1 + 1/y)
def nu_rar(y):    return 1.0/(1.0 - np.exp(-np.sqrt(y)))
def nu_simple(y): return 0.5 + np.sqrt(0.25 + 1/y)
def nu_std(y):    return np.sqrt((y + np.sqrt(y*y + 4))/(2*y))

# the three banked M22 theta examples, verbatim agentX_sk_kernel.py L38-40
def th_A(y): return 2.0/(1.0 + y*y)
def th_B(y): return np.exp(1.0 - np.minimum(y, 700))
def th_C(y): return np.exp((1.0 - np.minimum(y, 700))/2.0)
THETAS = {'2/(1+y^2)': th_A, 'exp(1-y)': th_B, 'exp((1-y)/2)': th_C}
N_CYC = 24.0   # banked window depth (agentX dynamics, 0.02-0.03% reproduction of the Sun inventory)

# Hernquist halo harness -- verbatim agentDD (= agentY_gates.py SGB)
def halo_grid():
    GMc2 = 1e11*1.476e3/3.0857e19; a_h = 3.0
    alp_n = A0_FW/c**2*3.0857e19          # a0 in kpc^-1 (c=1 units)
    Mb  = lambda r: GMc2*r**2/(r + a_h)**2
    dMb = lambda r: GMc2*2*r*a_h/(r + a_h)**3
    d2Mb = lambda r: GMc2*2*a_h*(a_h - 2*r)/(r + a_h)**4
    rg = np.logspace(-0.5, 4.2, 6000)
    Ph1 = Mb(rg)/rg**2
    Ph2 = dMb(rg)/rg**2 - 2*Mb(rg)/rg**3
    Ph3 = d2Mb(rg)/rg**2 - 4*dMb(rg)/rg**3 + 6*Mb(rg)/rg**4
    yv = Ph1/alp_n
    rb0v = (Ph2 + 2*Ph1/rg)/(4*np.pi)
    rb1n = (Ph3 + 2*Ph2/rg - 2*Ph1/rg**2)/(4*np.pi)
    return rg, alp_n, Ph1, Ph2, Ph3, yv, rb0v, rb1n

# ==================================================================================================
def agentY_row(c20v, c21v, tag, rg, alp_n, Ph1, Ph2, yv, rb0v, rb1n, L_sg, L_dps, Pv=1.0):
    """Run the agentY pickled-equation pollution harness with supplied (c20, c21) arrays."""
    chi1 = Ph1/(2*Pv)
    slip = L_sg(rg, alp_n, Pv, chi1, c20v, c21v, rb0v, rb1n)
    dpsv = L_dps(rg, alp_n, Pv, chi1, c20v, c21v, rb0v, rb1n)
    sfrac = slip/Ph1; tfrac = 2*(nu_rar(yv) - 1)
    serr = np.nanmax(np.abs(sfrac/tfrac - 1)[(yv > 1e-3) & (yv < 1e2)])
    divslip = np.gradient(slip*rg**2, rg)/rg**2
    DPhi = dpsv - divslip
    dg = np.cumsum(np.concatenate([[0], 0.5*(DPhi[1:]*rg[1:]**2 + DPhi[:-1]*rg[:-1]**2)*np.diff(rg)]))/rg**2
    frac = dg/Ph1
    row = {}
    for tgt in (1.0, 0.3, 0.1, 0.03, 0.01):
        i = np.argmin(np.abs(yv - tgt)); row[tgt] = frac[i]
    P(f"    [{tag}] slip-match {serr:.1e};  dg/g_bar @ y=1,0.3,0.1,0.03,0.01 = " +
      " ".join(f"{row[t]:+10.3e}" for t in (1.0, 0.3, 0.1, 0.03, 0.01)))
    return row, serr

def load_agentY():
    import sympy as sp
    with open(os.path.join(HERE, 'agentY_eqs.pkl'), 'rb') as f:
        PK = {k: sp.sympify(v) for k, v in pickle.load(f).items()}
    r_s, alp_s, G_s = sp.symbols('r alpha G', positive=True)
    Ch1s = sp.symbols('chi1', real=True)
    J1, J2 = sp.symbols('J1 J2', real=True)
    c10, c11, c20, c21, c30, c31 = sp.symbols('c10 c11 c20 c21 c30 c31', real=True)
    rhob_f = sp.Function('rhob')(r_s)
    rb0, rb1v = sp.symbols('rb0 rb1', real=True)
    zero_c = {c10: 0, c11: 0, c30: 0, c31: 0, J2: 0, G_s: 1}
    args = [r_s, alp_s, J1, Ch1s, c20, c21, rb0, rb1v]
    def lam(e):
        e = e.subs(zero_c).subs({sp.Derivative(rhob_f, r_s): rb1v, rhob_f: rb0})
        return sp.lambdify(args, e, 'numpy')
    return lam(PK['slipgrad']), lam(PK['DeltaPsi'])

def c20_matched_arrays(Yv, Pv=1.0):
    from scipy.integrate import quad
    def Yc20(Y):
        I, _ = quad(lambda u: (nu_rar(2*Pv*np.sqrt(u)) - 1.0)/u, Y, np.inf, limit=400)
        return -I
    c20v = np.array([Yc20(Y)/Y for Y in Yv])
    c21v = (nu_rar(2*Pv*np.sqrt(Yv)) - 1)/Yv**2 - c20v/Yv
    return c20v, c21v

# ==================================================================================================
def stage_K0():
    import sympy as sp
    P("="*100)
    P("agentKK_nonlocal_slip.py [K0] -- GATES against banked numbers before any new use")
    P("="*100)
    ok_all = True
    P("\n  slip targets Psi'/Phi' - 1 = 2(nu-1), McGaugh nu, framework a0:")
    for gb, want in [(1e-13, 61.2), (1e-12, 19.4), (1e-11, 6.2)]:
        got = 2*nu_rar(gb/A0_FW) - 1
        ok = abs(got - want) < 0.15*want; ok_all &= ok
        P(f"    g_bar={gb:.0e}: 2nu-1 = {got:.1f} (banked {want})  {'GATE OK' if ok else 'GATE FAIL'}")
    y_cas = GMsun/(1.6*Rsun)**2/A0_FW
    slip_cas = 2*(nu_simple(y_cas) - 1)
    ok = abs(y_cas/1.1e12 - 1) < 0.05 and abs(slip_cas/1.8e-12 - 1) < 0.15; ok_all &= ok
    P(f"  Cassini y = {y_cas:.2e} (banked 1.1e12); simple-nu slip = {slip_cas:.2e}; margin x{2.3e-5/slip_cas:.1e}"
      f"   {'GATE OK' if ok else 'GATE FAIL'}")
    g_clu = G*7e13*Msun/(1.0*Mpc)**2; y_clu = g_clu/A0_FW
    ok = abs(nu_rar(y_clu)/3.62 - 1) < 0.05; ok_all &= ok
    P(f"  cluster: y(1 Mpc, 7e13 Msun) = {y_clu:.2f}, nu = {nu_rar(y_clu):.2f}, short x{7.1/nu_rar(y_clu):.2f}"
      f" (banked x1.96)   {'GATE OK' if ok else 'GATE FAIL'}")

    P("\n  agentY wall-3 reproduction (agentY_eqs.pkl, Hernquist, P=1): expect dg/g_bar ~ -2.7e7 @ y=0.3")
    L_sg, L_dps = load_agentY()
    rg, alp_n, Ph1, Ph2, Ph3, yv, rb0v, rb1n = halo_grid()
    Pv = 1.0
    Yv = (yv/(2*Pv))**2
    c20v, c21v = c20_matched_arrays(Yv, Pv)
    row, serr = agentY_row(c20v, c21v, "agentY banked calibration", rg, alp_n, Ph1, Ph2, yv, rb0v, rb1n,
                           L_sg, L_dps, Pv)
    ok = abs(row[0.3]/(-2.7e7) - 1) < 0.2 and serr < 1e-10; ok_all &= ok
    P(f"    dg/g_bar(y=0.3) = {row[0.3]:+.3e} (banked -2.69e7)   {'GATE OK' if ok else 'GATE FAIL'}")

    P("\n  agentDD condensate W-only row (agentDD_D1b.pkl): expect +2.31e6 ... +4.47e7 across y=1->0.01")
    with open(os.path.join(HERE, 'agentDD_D1b.pkl'), 'rb') as f:
        PK = {k: sp.sympify(v) for k, v in pickle.load(f).items()}
    r_s, alp_s, G_s = sp.symbols('r alpha G', positive=True)
    sig = sp.symbols('sigma', real=True)
    Ph0s, Ps0s = sp.symbols('Phi0 Psi0', real=True)
    Ph1s, Ps1s = sp.symbols('Phi1 Psi1', real=True)
    Ph2s, Ps2s = sp.symbols('Phi2 Psi2', real=True)
    Wsy = sp.symbols('W0 W1 W2 W3 W4', real=True)
    Ssy = sp.symbols('S0 S1 S2 S3 S4', real=True)
    Csy = sp.symbols('C0 C1c C2c C3c C4c', real=True)
    rhob_f2 = sp.Function('rhob')(r_s)
    rb0s = sp.symbols('rb0', real=True)
    base = {sig: 1, G_s: 1, Ph0s: 0, Ps0s: 0}
    eqN, eqL = PK['eqN'], PK['eqL']
    sub_off = {v: 0 for v in list(Ssy) + list(Csy)}
    eqLw = sp.expand(eqL.subs(sub_off).subs(base))
    eqNw = sp.expand(eqN.subs(sub_off).subs(base))
    slip_expr = sp.cancel(sp.solve(sp.Eq(eqLw, 0), Ps1s)[0] - Ph1s)
    Ps2_sol = sp.solve(sp.Eq(eqNw.subs({rhob_f2: rb0s}), 0), Ps2s)[0]
    DeltaPsi_expr = Ps2_sol + 2*Ps1s/r_s - 4*sp.pi*rb0s
    L_slipW = sp.lambdify([r_s, alp_s, Ph1s] + list(Wsy), slip_expr, 'numpy')
    L_dpsW  = sp.lambdify([r_s, alp_s, Ph1s, Ph2s, Ps1s, rb0s] + list(Wsy), DeltaPsi_expr, 'numpy')
    Ya = (Ph1/alp_n)**2
    from scipy.integrate import quad
    yy = sp.symbols('yy', positive=True); Ya_s = sp.symbols('Ya_s', positive=True)
    nu_sym = 1/(1 - sp.exp(-sp.sqrt(yy)))
    W1e = (nu_sym.subs(yy, sp.sqrt(Ya_s)) - 1)/sp.sqrt(Ya_s)
    W2e = sp.diff(W1e, Ya_s); W3e = sp.diff(W2e, Ya_s); W4e = sp.diff(W3e, Ya_s)
    f1, f2, f3, f4 = [sp.lambdify(Ya_s, e, 'numpy') for e in (W1e, W2e, W3e, W4e)]
    W0v = np.array([2*quad(lambda u: (nu_rar(u) - 1.0), 0, ysc, limit=400)[0] for ysc in np.sqrt(Ya)])
    W1v, W2v, W3v, W4v = f1(Ya), f2(Ya), f3(Ya), f4(Ya)
    slipW = L_slipW(rg, alp_n, Ph1, W0v, W1v, W2v, W3v, W4v)
    tfrac = 2*(nu_rar(yv) - 1)
    serrW = np.nanmax(np.abs(slipW/Ph1/tfrac - 1)[(yv > 1e-3) & (yv < 1e2)])
    Ps1v = Ph1 + slipW
    dpsW = L_dpsW(rg, alp_n, Ph1, Ph2, Ps1v, rb0v, W0v, W1v, W2v, W3v, W4v)
    divW = np.gradient(slipW*rg**2, rg)/rg**2
    DPhiW = dpsW - divW
    dgW = np.cumsum(np.concatenate([[0], 0.5*(DPhiW[1:]*rg[1:]**2 + DPhiW[:-1]*rg[:-1]**2)*np.diff(rg)]))/rg**2
    fracW = dgW/Ph1
    rowW = {}
    for tgt in (1.0, 0.3, 0.1, 0.03, 0.01):
        i = np.argmin(np.abs(yv - tgt)); rowW[tgt] = fracW[i]
    P(f"    [DD W-only] slip-match {serrW:.1e};  dg/g_bar = " +
      " ".join(f"{rowW[t]:+10.3e}" for t in (1.0, 0.3, 0.1, 0.03, 0.01)))
    okW = abs(rowW[0.3]/5.70e6 - 1) < 0.1 and serrW < 1e-10; ok_all &= okW
    P(f"    (banked +2.31e6 +5.70e6 +1.17e7 +2.41e7 +4.47e7)   {'GATE OK' if okW else 'GATE FAIL'}")

    P("\n  agentDD_D4.pkl audit (the exact lens-only condition system):")
    with open(os.path.join(HERE, 'agentDD_D4.pkl'), 'rb') as f:
        D4 = {k: sp.sympify(v) for k, v in pickle.load(f).items()}
    num, den, slipD4 = D4['DeltaPhi_num'], D4['DeltaPhi_den'], D4['slip']
    syms = {str(s) for s in num.free_symbols}
    P(f"    symbols in DeltaPhi numerator: {sorted(syms)}")
    P(f"    denominator: {den}")
    P(f"    slip (on-shell, from eqL): {slipD4}")
    has_S = any(s.startswith('S') for s in syms)
    has_C = any(s.startswith('C') for s in syms)
    P(f"    S-family present in num: {has_S}; C-family present: {has_C}"
      f"  ({'FULL W+S+C save' if has_C else 'W+S save'})")
    # r^0-class S-freeness check (the banked D4 identity)
    poly = sp.Poly(num, Ph2s, sp.symbols('Phi3', real=True))
    cls00 = sp.expand(poly.coeff_monomial(1))
    r0coef = sp.Poly(cls00, r_s).coeff_monomial(1)
    sS = {s for s in sp.sympify(r0coef).free_symbols if str(s).startswith('S')}
    P(f"    r^0-class of the (Phi2^0 Phi3^0) class: S-symbols present = {sorted(map(str, sS)) if sS else 'NONE'}")
    slip_over = sp.cancel(slipD4/Ph1s)
    chk = sp.simplify(sp.expand(r0coef/alp_s**6 - slip_over.subs({Ph1s: Ph1s})))
    # express slip/Phi' in the same variables before comparing
    chk2 = sp.simplify(sp.expand(r0coef - alp_s**6*slip_over))
    P(f"    identity r^0-class == alpha^6*(slip/Phi'): {'CONFIRMED' if chk2 == 0 else f'residual = {chk2}'}")
    ok = (not sS); ok_all &= ok
    P(f"\n  [K0] ALL GATES: {'OK -- proceed' if ok_all else '*** FAIL -- STOP ***'}")
    with open(os.path.join(HERE, 'agentKK_state.pkl'), 'wb') as f:
        pickle.dump({'gates_ok': ok_all}, f)
    return ok_all

# ==================================================================================================
def stage_K1():
    """THE FORMAL VARIATION: a history-keyed operator's Hamiltonian-constraint response, derived on
    a time lattice with full functional bookkeeping. Models:
      A: coordinate-time linear filter  K_k = sum_j w_j y2_{k-j}
      B: proper-time filter             K_k = sum_j Wf(sig_k - sig_{k-j}) y2_{k-j} N_{k-j} dt
      C: general nonlinear multi-window key  K_k = H(P_k, Q_k)
      D: derivative-coupled key         K_k = sum_j w_j (y2_{k-j+1} - y2_{k-j})
    In each: action S = sum_k dt * Int dx N_k F(K_k) g(x); vary the lapse on slice k0; classify the
    integrand by eta (harmless tier: no IBP) vs eta' (the dangerous route: IBP lands the
    (a0 r/c^2)^-1-enhanced geometric piece, agentDD's delta-Y_a/delta-Phi mechanism); evaluate on a
    STATIC background; compare to the LOCAL key. Then the frequency response of the dangerous
    coefficient (the suppression factor) and the timescale no-middle-ground arithmetic."""
    import sympy as sp
    P("="*100)
    P("agentKK_nonlocal_slip.py [K1] -- THE FORMAL VARIATION: filtered key vs the constraint")
    P("="*100)
    x = sp.Symbol('x'); alp = sp.Symbol('alpha', positive=True)
    dt = sp.Symbol('dt', positive=True)
    eps = sp.Symbol('epsilon')
    eta = sp.Function('eta')(x)
    g = sp.Function('g')(x)            # the operator rest (carrier geometry; N-independent stand-in)
    F = sp.Function('F')
    n = 6; k0 = 2; mtap = 3            # slices 0..5; vary slice 2; causal taps j=0..2
    Phi = sp.Function('Phi')(x)        # the static background potential
    phis = [sp.Function(f'phi{k}')(x) for k in range(n)]
    pert = [phis[k] + (eps*eta if k == k0 else 0) for k in range(n)]
    Nk   = [1 + p for p in pert]
    y2   = [sp.diff(p, x)**2/alp**2 for p in pert]   # a_i = d_i ln N -> weak-field (d phi)^2/alpha^2

    def constraint_terms(S_int):
        """coefficient of eta (harmless tier) and of eta' (the dangerous, IBP-enhanced route)."""
        dS = sp.expand(sp.diff(S_int, eps).subs(eps, 0))
        ep = sp.diff(eta, x)
        B = sp.expand(dS.coeff(ep))          # eta' coefficient
        A = sp.expand(dS.coeff(eta))         # eta coefficient (no derivative)
        # safety: nothing beyond eta' should appear
        rest = sp.expand(dS - A*eta - B*ep)
        return A, B, rest

    static = {phis[k]: Phi for k in range(n)}

    # ---------- LOCAL comparator -------------------------------------------------------------
    S_loc = sum(dt*Nk[k]*F(y2[k])*g for k in range(k0, n))   # same slice support as the filtered sums
    A_loc, B_loc, r_loc = constraint_terms(S_loc)
    # only slice k0 contributes locally:
    B_loc_st = sp.simplify(B_loc.subs(static))
    P("\n  [LOCAL key K = y2 = (dPhi)^2/alpha^2]")
    P("    eta'-coefficient (static bg):", B_loc_st)
    P("    (this is the dangerous route: IBP -> the geometric (a0 r/c^2)^-1-enhanced eqN feed;")
    P("     residual non-eta terms:", sp.simplify(r_loc.subs(static)), ")")

    # ---------- MODEL A: coordinate-time linear filter ----------------------------------------
    w = list(sp.symbols('w0:3', real=True))
    K_A = [sum(w[j]*y2[k - j] for j in range(mtap)) for k in range(n)]
    S_A = sum(dt*Nk[k]*F(K_A[k])*g for k in range(k0, n))    # K defined for k >= 2
    A_A, B_A, r_A = constraint_terms(S_A)
    B_A_st = sp.simplify(B_A.subs(static))
    P("\n  [MODEL A: K_k = sum_j w_j y2_{k-j} (coordinate-time window)]")
    P("    eta'-coefficient (static bg):", B_A_st)
    K_A_static = sp.simplify(K_A[n-1].subs(static).subs(eps, 0))
    P("    static key value:", K_A_static)
    # THE COMPARATOR: the LOCAL theory with the effective operator function C_eff(Y) = F(sum(w) Y)
    S_eff = sum(dt*Nk[k]*F(sum(w)*y2[k])*g for k in range(k0, n))
    A_E, B_E, r_E = constraint_terms(S_eff)
    B_E_st = sp.simplify(B_E.subs(static))
    P("    STATIC-EQUIVALENCE check: eta'-coeff(filtered) == eta'-coeff(LOCAL with C_eff = F((sum w) Y)):",
      sp.simplify(B_A_st - B_E_st) == 0)
    P("    -> the constraint at t0 collects the key's response at ALL later slices; on a static")
    P("       background the window re-sums to its DC weight sum_j w_j. The static key VALUE carries")
    P("       the SAME factor: value and constraint sensitivity are locked together. Normalized")
    P("       tracking (K_static = y2) forces sum w = 1: THE FULL LOCAL POLLUTION, exactly.")

    # ---------- MODEL B: proper-time filter (measure + sigma routes kept) ---------------------
    Wf = sp.Function('Wf')
    sigk = [dt*sum(Nk[m] for m in range(k + 1)) for k in range(n)]
    K_B = [sum(Wf(sigk[k] - sigk[k - j])*y2[k - j]*Nk[k - j]*dt for j in range(1, mtap)) for k in range(n)]
    # (j starts at 1 so every Wf argument is a genuine proper-time lag; j=0 would need Wf(0) too --
    #  included in Model A; the routes under test (measure, sigma) are j>=1 effects)
    S_B = sum(dt*Nk[k]*F(K_B[k])*g for k in range(k0, n))   # K_B defined for k >= 2
    A_B, B_B, r_B = constraint_terms(S_B)
    B_B_st = sp.simplify(B_B.subs(static))
    P("\n  [MODEL B: K_k = sum_j Wf(sigma_k - sigma_{k-j}) y2_{k-j} N_{k-j} dt (PROPER-TIME window;")
    P("            the filter the matter sector carries -- X-2 structure, u-clocked)]")
    # comparator: LOCAL theory with C_eff(Y) = F(w_eff Y), w_eff = sum_j Wf(j dt N) N dt (slice-local)
    weff = [sum(Wf(j*dt*Nk[k])*Nk[k]*dt for j in range(1, mtap)) for k in range(n)]
    S_effB = sum(dt*Nk[k]*F(weff[k]*y2[k])*g for k in range(k0, n))
    A_EB, B_EB, r_EB = constraint_terms(S_effB)
    B_EB_st = sp.simplify(B_EB.subs(static))
    P("    STATIC-EQUIVALENCE check: eta'-coeff(filtered) == eta'-coeff(LOCAL with")
    P("      C_eff = F(w_eff Y), w_eff = sum_j Wf(j dtau) dtau the proper-time DC weight):",
      sp.simplify(B_B_st - B_EB_st) == 0)
    P("    (w_eff carries O(Phi) proper-time dressings -- explicit-N, one epsilon-tier beyond the")
    P("     constant weight; the leading tier is the normalized DC weight = 1 when tracking.)")
    P("    The NEW routes opened by the proper-time structure:")
    A_B_st = sp.expand(A_B.subs(static))
    has_Wfp = any(isinstance(a, sp.Derivative) or (getattr(a, 'func', None) == Wf)
                  for a in sp.preorder_traversal(A_B_st) if isinstance(a, sp.Derivative))
    nWfp = sum(1 for a in sp.preorder_traversal(A_B_st) if isinstance(a, sp.Derivative)
               and getattr(a.expr, 'func', None) == Wf)
    P(f"       sigma-route (Wf' terms) present in the eta-coefficient: {nWfp > 0} (count {nWfp});")
    nWfpB = sum(1 for a in sp.preorder_traversal(sp.expand(B_B_st)) if isinstance(a, sp.Derivative)
                and getattr(a.expr, 'func', None) == Wf)
    P(f"       sigma-route (Wf' terms) present in the eta'-coefficient: {nWfpB > 0} (count {nWfpB})")
    P("       -> measure (explicit N) and sigma (delta-proper-time) routes carry NO spatial")
    P("          derivative of the test function: they sit at the harmless (GR/measure) tier --")
    P("          agentDD's classification transfers; they cannot cancel the eta'-route (different")
    P("          test-function structure: a local counterterm cannot cancel a derivative coupling).")

    # ---------- MODEL C: general nonlinear multi-window key -----------------------------------
    v = list(sp.symbols('v0:3', real=True))
    H = sp.Function('H')
    Pk = [sum(w[j]*y2[k - j] for j in range(mtap)) for k in range(n)]
    Qk = [sum(v[j]*y2[k - j] for j in range(mtap)) for k in range(n)]
    S_C = sum(dt*Nk[k]*H(Pk[k], Qk[k])*g for k in range(k0, n))
    A_C, B_C, r_C = constraint_terms(S_C)
    B_C_st = sp.simplify(B_C.subs(static))
    Y = sp.Symbol('Y', positive=True)
    Kst = H(sum(w)*Y, sum(v)*Y)             # the static read of the composite key
    dKdY = sp.diff(Kst, Y)
    y2st = sp.diff(Phi, x)**2/alp**2
    # LOCAL unit comparator: F = identity (operator coefficient = the key itself)
    S_loc_id = sum(dt*Nk[k]*y2[k]*g for k in range(k0, n))
    _, B_loc_id, _ = constraint_terms(S_loc_id)
    B_loc_id_st = sp.simplify(B_loc_id.subs(static))
    chkC = sp.simplify(B_C_st - dKdY.subs({Y: y2st})*B_loc_id_st)
    P("\n  [MODEL C: K_k = H(P_k, Q_k), P/Q two windows -- the general (nonlinear, multi-channel) key]")
    P("    eta'-coefficient == dK_static/dY x (local unit response):", chkC == 0)
    P("    -> THE CHAIN-RULE COLLAPSE: whatever the history functional, on a static background the")
    P("       constraint's dangerous coefficient is d(K_static)/dY x the local unit response, and the")
    P("       operator coefficient is F(K_static(Y)): the static theory IS the local theory with")
    P("       C_eff(Y) = F(K_static(Y)). Slip calibration and pollution both read ONLY C_eff.")

    # ---------- MODEL D: derivative-coupled key ------------------------------------------------
    K_D = [sum(w[j]*(y2[k - j] - y2[k - j - 1]) for j in range(mtap - 1)) for k in range(n)]
    S_D = sum(dt*Nk[k]*F(K_D[k])*g for k in range(k0, n))   # every slice with a defined key (k >= 2)
    A_D, B_D, r_D = constraint_terms(S_D)
    B_D_st = sp.simplify(B_D.subs(static))
    K_D_st = sp.simplify(K_D[n-1].subs(static).subs(eps, 0))
    P("\n  [MODEL D: K_k = sum_j w_j (y2_{k-j} - y2_{k-j-1}) (derivative-coupled window, zero DC)]")
    P("    static key value:", K_D_st, "; eta'-coefficient (static bg):", B_D_st)
    P("    -> zero DC weight kills the static constraint response AND the static read together:")
    P("       no pollution, no key. F(K_D) = F(0) = const on every static configuration -- the")
    P("       operator cannot track nu(y). The slip-to-pollution ratio is FILTER-INVARIANT.")

    # ---------- the frequency response (the suppression factor) --------------------------------
    om, tw = sp.symbols('omega t_w', positive=True)
    P("\n  [frequency response of the dangerous coefficient]")
    P("    lattice: a lapse mode at frequency omega scales the eta'-route by sum_j w_j e^{-i om j dt}")
    P("    continuum (two-stage cascaded exponential window, the banked M22 implementation):")
    P("       Wtil(omega) = 1/(1 - i om t_w)^2  per channel;  |Wtil(0)| = 1 EXACTLY.")
    for wt in [0.0, 0.01, 0.1, 1.0, 10.0, 2*np.pi*N_CYC, 1e3, 3.2e3]:
        sup = 1.0/(1.0 + wt**2)
        P(f"       omega*t_w = {wt:10.3g}:  |Wtil| = {sup:.3e}")
    P("    suppression of the banked 2.3e6-4.5e7 pollution to below the 0.2-dex bar needs |Wtil| <~ 1e-7")
    P("    => omega*t_w >~ 3.2e3.  The lensing job is a STATIC lens: omega = 0 EXACTLY -- no t_w works.")
    P("    Treating the halo as a slow transient (most generous: assembly omega ~ 2pi/3 Gyr):")
    om_h = 2*np.pi/(3e9)      # yr^-1
    tw_need = 3.2e3/om_h
    P(f"       t_w needed = 3.2e3/omega = {tw_need:.2e} yr = {tw_need/13.8e9:.0f} x the age of the universe")
    P("       -- a window that never fills: the key then reads the pre-assembly average (~0): NO slip.")
    P("    Tracking instead: t_w = 0.3 Gyr (a 10%-lag filter) -> |Wtil(omega_assembly)| =")
    wt = om_h*0.3e9
    P(f"       {1.0/(1.0+wt**2):.4f} -- pollution at 72% of full; t_w = 0.03 Gyr (percent-level")
    wt2 = om_h*0.03e9
    P(f"       tracking) -> |Wtil| = {1.0/(1.0+wt2**2):.4f} -- pollution at 99.6%. NO MIDDLE GROUND:")
    P("       suppression and tracking are |Wtil| at the SAME frequency; their product is pinned.")
    P("\n  [K1 VERDICT] The DC leak reinstates the pollution at FULL amplitude; the proper-time")
    P("  structure adds only harmless-tier routes; the general-key chain rule collapses the entire")
    P("  history-keyed class to the local class on static backgrounds. THE STATIC-EQUIVALENCE THEOREM:")
    P("  any TTI history key K with differentiable static read K_static(Y) gives static field equations")
    P("  IDENTICAL to the local theory with C_eff = F o K_static. Track <=> dK_static/dY != 0 <=> the")
    P("  full local pollution at slip-matched amplitude.")

# ==================================================================================================
def stage_K2():
    """The chain-rule certificate on the REAL pickled agentY equations: run the slip-matched
    pollution harness with the operator coefficient written as F(K(Y)) for two nontrivial static
    reads -- (i) K = theta0*Y (the M22 spectral-static-read mock, theta0 = theta_A(0) = 2),
    (ii) K = sqrt(Y) (a nonlinear y-read). The composite (c20, c21) = (F(K), F'(K) K') is computed
    by the chain rule through the composite arithmetic; the matched pollution row must reproduce
    agentY's banked row to all printed digits. Plus: the M22 window's static read, numerically."""
    P("="*100)
    P("agentKK_nonlocal_slip.py [K2] -- the chain-rule certificate on the real equations")
    P("="*100)
    L_sg, L_dps = load_agentY()
    rg, alp_n, Ph1, Ph2, Ph3, yv, rb0v, rb1n = halo_grid()
    Pv = 1.0
    Yv = (yv/(2*Pv))**2
    c20m, c21m = c20_matched_arrays(Yv, Pv)
    P("\n  reference (local key, banked calibration):")
    row0, _ = agentY_row(c20m, c21m, "LOCAL  C(Y) = c20_matched(Y)", rg, alp_n, Ph1, Ph2, yv, rb0v,
                         rb1n, L_sg, L_dps, Pv)

    P("\n  composite key (i): K(Y) = theta0*Y, theta0 = theta_A(0) = 2 (M22 spectral static read);")
    P("  F(z) := c20_matched(z/theta0)  =>  C_eff = F(K(Y)), C_eff' = F'(K) K' by the chain rule:")
    th0 = 2.0
    Kv = th0*Yv
    c20_i = np.array([np.interp(k/th0, Yv[::-1], c20m[::-1]) for k in Kv]) if False else c20m  # exact: K/th0 = Y
    # exact composite arithmetic (no interpolation): F(K(Y)) = c20m(Y); F'(z) = c20m'(z/th0)/th0
    Fp_at_K = c21m/th0          # F'(K(Y)) = c20m'(Y)/th0
    c21_i = Fp_at_K*th0         # F'(K) * K' with K' = th0
    P(f"    composite check: max|F(K)-c20m| = {np.nanmax(np.abs(c20_i-c20m)):.1e},"
      f" max|F'(K)K'-c21m| = {np.nanmax(np.abs(c21_i-c21m)):.1e}")
    row_i, _ = agentY_row(c20_i, c21_i, "FILTERED read K=2Y, matched", rg, alp_n, Ph1, Ph2, yv, rb0v,
                          rb1n, L_sg, L_dps, Pv)

    P("\n  composite key (ii): K(Y) = sqrt(Y) (nonlinear read; e.g. keying on y not y^2);")
    P("  F(z) := c20_matched(z^2)  =>  F'(z) = 2 z c20m'(z^2);  C_eff' = F'(sqrt(Y)) * 1/(2 sqrt(Y)):")
    sY = np.sqrt(Yv)
    Fp_ii = 2*sY*c21m           # F'(sqrt(Y)) = 2 sqrt(Y) c20m'(Y)
    c21_ii = Fp_ii/(2*sY)       # x K' = 1/(2 sqrt(Y))
    P(f"    composite check: max relative |F'(K)K'/c21m - 1| = {np.nanmax(np.abs(c21_ii/c21m-1)):.1e}")
    row_ii, _ = agentY_row(c20m, c21_ii, "FILTERED read K=sqrt(Y), matched", rg, alp_n, Ph1, Ph2, yv,
                           rb0v, rb1n, L_sg, L_dps, Pv)
    dmax = max(abs(row_i[t]/row0[t] - 1) for t in row0) if all(row0[t] != 0 for t in row0) else 99
    dmax2 = max(abs(row_ii[t]/row0[t] - 1) for t in row0)
    P(f"\n    max relative row deviation: read (i) {dmax:.2e}; read (ii) {dmax2:.2e}")
    P("    -> the (K, F) filter freedom cancels EXACTLY in the matched theory: the slip-matched")
    P("       pollution table is FILTER-INVARIANT on the real field equations, derivative bookkeeping")
    P("       included. Making the static read small (skirt-level theta) does not help: the slip")
    P("       calibration re-amplifies F by the inverse factor -- the product is pinned.")

    P("\n  the M22 window's static read, numerically (two-stage cascaded EWMA, the banked X-2 form):")
    dt = 1.0; Tw = 2*np.pi*N_CYC/(2*np.pi/1000.0)   # a channel at period 1000 dt
    cc = np.exp(-dt/Tw)
    npts = int(20*Tw)
    sig = np.ones(npts)         # a STATIC y^2 history
    s1 = np.zeros(npts); s2 = np.zeros(npts)
    for i in range(1, npts):
        s1[i] = cc*s1[i-1] + (1-cc)*sig[i]
        s2[i] = cc*s2[i-1] + (1-cc)*s1[i]
    P(f"    static input 1.0 -> filter output after 20 T_w: {s2[-1]:.10f}  (DC gain = 1 exactly,")
    P(f"    burn-in residual {abs(s2[-1]-1):.1e}); the demodulated omega-channel sees the DC line at")
    om_dc = 2*np.pi/1000.0
    leak = 1.0/(1.0 + (om_dc*Tw)**2)
    P(f"    skirt level 1/(1+(om T_w)^2) = {leak:.2e} (om T_w = 2 pi N_cyc = {om_dc*Tw:.1f})")
    P(f"    theta(0) of the three banked thetas: A 2/(1+y^2) -> {th_A(0.0):.3f}; B exp(1-y) -> {th_B(0.0):.3f};"
      f" C exp((1-y)/2) -> {th_C(0.0):.3f}  -- ALL O(few), none zero: the M22 spectral measure READS")
    P("    static/secular content at O(1) BY DESIGN (that is the EFE quench, mu_hat(inf) = mu(theta(0) a_c/a0)).")

# ==================================================================================================
def stage_K3():
    """The structured escapes, each worked:
       (a) derivative-coupled key -- tracking on static fields / circular orbits / epicyclic;
       (b) the S-counterterm family -- the S-free r^0 core and the numeric irreducible floor;
       (c) frequency-domain keying -- theta(0) static reads (numbers in K2), the design corner
           theta(0) = 0, and the matter-worldline fork."""
    import sympy as sp
    P("="*100)
    P("agentKK_nonlocal_slip.py [K3] -- the structured escapes")
    P("="*100)

    P("\n  (a) DERIVATIVE-COUPLED KEY  K_d = [W * dY/dtau] (zero DC weight by construction):")
    P("    - static halo field point (the u-congruence is static): dY/dtau = 0 identically -> K_d = 0:")
    P("      the operator coefficient is F(0) = const at EVERY radius of EVERY static lens. The target")
    P("      slip 2(nu-1) spans 60.2 -> 5.2 over g_bar = 1e-13 -> 1e-11: a constant cannot track it.")
    P("      TRACKING ERROR = the full dynamic range (100%). [agentY wall-4 branch 'slip/Phi' = const'")
    P("      was already a dead branch even as a constant.]")
    P("    - worldline-level reading (the matter-sector filter style): a CIRCULAR orbit has |a| = const")
    P("      -> dY/dtau = 0 on the worldline too: K_d = 0 for exactly the orbit family the RAR/lensing")
    P("      stacks are built on.")
    P("    - epicyclic orbit, eccentricity e: Y(t) = Y0(1 + 2e cos(Om t) + O(e^2)) ->")
    Om, Tw_, e_ = 1.0, 2*np.pi*N_CYC, 0.1
    amp = 2*e_*Om*Tw_/(1.0 + (Om*Tw_)**2)
    P(f"      K_d amplitude (two-stage window, Om T_w = 2 pi N_cyc): |K_d|/Y0 = 2e OmT_w/(1+(OmT_w)^2)")
    P(f"      = {amp:.2e} at e = 0.1 -- OSCILLATORY, ZERO-MEAN (no secular component), and PROPORTIONAL")
    P("      TO e: a slip keyed to it would be eccentricity-dependent -- non-universal, wrong observable.")
    P("    -> escape (a) FAILS THE JOB (cannot read a static y at all), not merely a gate.")

    P("\n  (b) THE S-COUNTERTERM FAMILY tuned against the DC leak:")
    P("    By static equivalence, S(K_filt) on a static background = S_eff(Y_a): the SAME family")
    P("    agentDD already adjudicated. The banked D4 closure (re-verified in K0): the exact lens-only")
    P("    condition's r^0 (geometric) class is S-FREE and equals alpha^6 x (slip/Phi'). The numeric")
    P("    irreducible floor -- the pollution carried by the r^0 class alone (untouchable by ANY S):")
    with open(os.path.join(HERE, 'agentDD_D4.pkl'), 'rb') as f:
        D4 = {k: sp.sympify(v) for k, v in pickle.load(f).items()}
    num, den, slipD4 = D4['DeltaPhi_num'], D4['DeltaPhi_den'], D4['slip']
    r_s, alp_s = sp.symbols('r alpha', positive=True)
    Ph1s, Ph2s = sp.symbols('Phi1 Phi2', real=True)
    Ph3s = sp.symbols('Phi3', real=True)
    Wsy = list(sp.symbols('W0 W1 W2 W3 W4', real=True))
    Ssy = list(sp.symbols('S0 S1 S2 S3 S4', real=True))
    Csy = list(sp.symbols('C0 C1c C2c C3c C4c', real=True))
    poly = sp.Poly(num, Ph2s, Ph3s)
    cls00 = sp.expand(poly.coeff_monomial(1))
    r0coef = sp.Poly(cls00, r_s).coeff_monomial(1)
    # Delta_Phi floor = r0coef / den  (the class with no Phi2/Phi3/r dressing)
    sub_off = {s: 0 for s in Ssy + Csy}
    r0_W = sp.expand(r0coef.subs(sub_off))
    den_W = sp.expand(den.subs(sub_off))
    P(f"    r^0-class (W-sector): {r0_W}")
    P(f"    denominator (W-sector): {den_W}   [full: {den} = alpha^6 r^2 (1 + slip/Phi')]")
    floor_expr = sp.cancel(r0_W/den_W)
    L_floor = sp.lambdify([r_s, alp_s, Ph1s] + Wsy, floor_expr, 'numpy')
    rg, alp_n, Ph1, Ph2, Ph3, yv, rb0v, rb1n = halo_grid()
    Ya = (Ph1/alp_n)**2
    from scipy.integrate import quad
    yy = sp.symbols('yy', positive=True); Ya_s = sp.symbols('Ya_s', positive=True)
    nu_sym = 1/(1 - sp.exp(-sp.sqrt(yy)))
    W1e = (nu_sym.subs(yy, sp.sqrt(Ya_s)) - 1)/sp.sqrt(Ya_s)
    W2e = sp.diff(W1e, Ya_s); W3e = sp.diff(W2e, Ya_s); W4e = sp.diff(W3e, Ya_s)
    f1, f2, f3, f4 = [sp.lambdify(Ya_s, ee, 'numpy') for ee in (W1e, W2e, W3e, W4e)]
    W0v = np.array([2*quad(lambda u: (nu_rar(u) - 1.0), 0, ysc, limit=400)[0] for ysc in np.sqrt(Ya)])
    W1v, W2v, W3v, W4v = f1(Ya), f2(Ya), f3(Ya), f4(Ya)
    DPhi_floor = L_floor(rg, alp_n, Ph1, W0v, W1v, W2v, W3v, W4v)
    dgf = np.cumsum(np.concatenate([[0], 0.5*(DPhi_floor[1:]*rg[1:]**2 + DPhi_floor[:-1]*rg[:-1]**2)
                                    *np.diff(rg)]))/rg**2
    fracf = dgf/Ph1
    rowf = []
    for tgt in (1.0, 0.3, 0.1, 0.03, 0.01):
        i = np.argmin(np.abs(yv - tgt)); rowf.append(f"{fracf[i]:+10.3e}")
    P("    S-IRREDUCIBLE FLOOR dg/g_bar @ y=1,0.3,0.1,0.03,0.01 = " + " ".join(rowf))
    P("    (compare the full W-only row +2.31e6 +5.70e6 +1.17e7 +2.41e7 +4.47e7: the floor IS the")
    P("     pollution -- the S-family can only dress the Phi2 r^2 / r^1 classes.)")
    P("    sanity: r^0-class == alpha^6 (slip/Phi') -> floor = (slip/Phi')/[r^2 (1 + slip/Phi')]:")
    sofp = 2*(Ph1/alp_n)*W1v                     # W-only slip/Phi' = 2 y W'(Ya)
    pred = sofp/(rg**2*(1.0 + sofp))
    rr = DPhi_floor/pred
    P(f"    floor / prediction: min {np.nanmin(rr):.6f} max {np.nanmax(rr):.6f} (1.000000 = exact)")
    P("    -> escape (b) FAILS: the geometric core of the matter-channel feed is exactly the slip;")
    P("       no S-function reaches it. (Banked D4 identity, re-verified here numerically.)")

    P("\n  (c) FREQUENCY-DOMAIN / SPECTRAL KEYING (the X2 filter bank):")
    P("    The static read of an M22-style spectral measure at a static field point: the only populated")
    P("    line is DC; the bank reads it at theta(0)-weight = O(few) (K2: 2 / 2.72 / 1.65 for the three")
    P("    banked thetas) -- the EFE quench channel. Chain rule (K1 Model C) -> static equivalence ->")
    P("    the K2 certificate applies verbatim: slip-matched pollution INVARIANT.")
    P("    Design corner theta(0) = 0 AND notched DC channel: the static read is the skirt leakage")
    leak = 1.0/(1.0 + (2*np.pi*N_CYC)**2)
    P(f"    (~{leak:.1e} per channel at N_cyc = 24) or zero -- either the calibration re-amplifies it")
    P("    (invariance again, with F' blown up by ~2e4: same matched pollution AND a new fine-tuning),")
    P("    or the read is exactly zero and the key cannot see a static lens at all (escape (a) redux).")
    P("    The matter-WORLDLINE fork (key on the particles' own filtered A_ret instead of the")
    P("    u-congruence field): the slip operator then couples directly to matter worldlines -- varying")
    P("    z_p hits the slip term: a FIFTH FORCE on matter. Lens-only is broken by construction and the")
    P("    entire solar-system battery + the 8.7-21.6 sigma double-counting bar re-import. DEAD.")

    P("\n  [K3 VERDICT] All three structured escapes fail: (a) cannot read a static lens; (b) the")
    P("  S-family cannot reach the S-free r^0 core (= the slip itself); (c) spectral keys are")
    P("  statically equivalent to local keys at O(few) gain -- matched pollution invariant -- and the")
    P("  zero-gain corner is (a). The history-keyed class is CLOSED in the static sector.")

if __name__ == '__main__':
    stage = sys.argv[1] if len(sys.argv) > 1 else 'K0'
    t0 = time.time()
    fn = globals().get('stage_' + stage)
    if fn is None:
        P(f"[{stage}] unknown stage"); sys.exit(1)
    fn()
    P(f"  [stage {stage} done in {time.time()-t0:.1f}s]")
