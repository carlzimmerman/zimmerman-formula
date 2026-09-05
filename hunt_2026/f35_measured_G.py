"""f35 -- the measured Newton constant in the clock host from the PPN ladder (requirement 10), built on f33's machinery.  Original f33 header:\n the f32 operator in a CLOCK host: the aether replaced by the hypersurface-orthogonal unit vector of a clock scalar,
A_mu = -d_mu tau / sqrt(-(d tau)^2), tau = tau_bg + eps T.  In the pipeline this is the substitution a_i = -q_i^nu d_nu T (static: a1 = -(1 + w^2 w1^2) d_x T,
a2 = a3 = 0) with the unit-norm-solved a0 kept; c_13 = 0 is built in (c_T = c), so the clock's own PPN is Einstein-aether's restricted to the
khronometric family: alpha_1 = -4 c_14 + drag, and the spec's requirement 2 admits a clock scalar counted separately.  Questions, each a check
that can fail: does the operator's exact reproduction of the coherent stiffening survive without the vector modes; is the scalar's alpha_2 drag
still suppressed; and does the clock's own alpha_1, alpha_2 vanish in the c_14 -> 0 corner (the post-GW170817 khronometric corner) so that the
whole PPN ladder of the candidate passes at the Cassini floor.  Same symbolic L2 as f32 (cached), new ladder."""
import sympy as sp, time, pickle, os, sys
T0 = time.time(); P = lambda *a: print(*a, flush=True)
import tempfile
SC = os.environ.get('SCRATCH', tempfile.gettempdir()) + '/'
os.makedirs(SC, exist_ok=True)
CACHE = SC + 'L2dc_k4_Vgrad.pkl'   # f32's quadratic action, reused
FAILS = []
def check(name, ok, detail=''):
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  ({detail})" if detail else ''))
    if not ok: FAILS.append(name)

t, x1, x2, x3 = sp.symbols('t x1 x2 x3', real=True)
eps, wb = sp.symbols('eps w_b', positive=True)
KB, Q0, K2, JY = sp.symbols('K_B Q_0 K_2 J_Y', real=True)
C2, C4 = sp.symbols('c2 c4', real=True)
XI2 = sp.symbols('xi2', nonnegative=True)          # (xi k)^2
w1, w2, w3 = sp.symbols('w1 w2 w3', real=True)
GT, LAM = sp.symbols('G_t Lambda', real=True)
kx = sp.symbols('k_x', real=True)
eta = sp.diag(-1, 1, 1, 1); I = sp.I
Es, Eis = sp.symbols('E_s E_is')
kv = [0, kx, 0, 0]
def nf(tag):
    ket = sp.Symbol(tag+'k'); bra = sp.Symbol(tag+'b')
    return ket*Es + bra*Eis, ket, bra
def d(f, mu):
    return sp.diff(f, Es)*(I*kv[mu]*Es) + sp.diff(f, Eis)*(-I*kv[mu]*Eis)
Psi, Psik, Psib = nf('Psi'); Phi, Phik, Phib = nf('Phi')
B2f, B2k, B2b = nf('B2'); B3f, B3k, B3b = nf('B3')
s22, s22k, s22b = nf('s22'); s23, s23k, s23b = nf('s23')
a1f, a1k, a1b = nf('a1'); a2f, a2k, a2b = nf('a2'); a3f, a3k, a3b = nf('a3')
chif, chik, chib = nf('chi')
rho, Rk, Rb = nf('rho'); a0f, a0k, a0b = nf('a0p')
KETS = [Psik, Phik, B2k, B3k, s22k, s23k, a1k, a2k, a3k, chik]
XA, XB, XC = sp.symbols('xA xB xC', nonnegative=True)
BRAS = [Psib, Phib, B2b, B3b, s22b, s23b, a1b, a2b, a3b, chib]

if os.path.exists(CACHE) and '--rebuild' not in sys.argv:
    L2dc = pickle.load(open(CACHE, 'rb')); P(f"[cache] loaded {CACHE}")
else:
    ww = w1**2 + w2**2 + w3**2; S0 = 1 + wb**2*ww/2
    Aup_bg = sp.Matrix([S0, wb*w1, wb*w2, wb*w3]); Adn_bg = eta*Aup_bg
    dphi_bg = -Q0*Adn_bg
    H = sp.zeros(4, 4)
    H[0, 0] = -2*Psi
    H[0, 2] = B2f; H[2, 0] = B2f; H[0, 3] = B3f; H[3, 0] = B3f
    H[1, 1] = -2*Phi
    H[2, 2] = -2*Phi + s22; H[3, 3] = -2*Phi - s22
    H[2, 3] = s23; H[3, 2] = s23
    gd = sp.Matrix(4, 4, lambda m, n: eta[m, n] + eps*H[m, n])
    Hup = eta*H*eta
    gu = sp.Matrix(4, 4, lambda i, j: (eta - eps*Hup + eps**2*(Hup*H*eta))[i, j])
    trH = sum(eta[m, n]*H[m, n] for m in range(4) for n in range(4))
    HH = sum(Hup[m, n]*H[m, n] for m in range(4) for n in range(4))
    sqg = 1 + eps*trH/2 + eps**2*(trH**2/8 - HH/4)
    Adn = sp.Matrix([Adn_bg[0]-eps*a0f, Adn_bg[1]+eps*a1f, Adn_bg[2]+eps*a2f, Adn_bg[3]+eps*a3f])
    Aup = sp.Matrix(4, 1, lambda i, j: sum(gu[i, k]*Adn[k] for k in range(4)))
    C1c = sp.expand(sum(Aup[i]*Adn[i] for i in range(4)) + 1).coeff(eps, 1)
    solA = sp.solve([sp.expand(C1c).coeff(Es, 1), sp.expand(C1c).coeff(Eis, 1)], [a0k, a0b], dict=True)[0]
    solA = {k: sp.expand(sp.series(v, wb, 0, 3).removeO()) for k, v in solA.items()}
    a0f = a0f.subs(solA)
    Adn = sp.Matrix([Adn_bg[0]-eps*a0f, Adn_bg[1]+eps*a1f, Adn_bg[2]+eps*a2f, Adn_bg[3]+eps*a3f])
    Aup = sp.Matrix(4, 1, lambda i, j: sum(gu[i, k]*Adn[k] for k in range(4)))
    P(f"[S1] unit-norm constraint solved ({time.time()-T0:.1f}s)")
    # scalar with LIVE fluctuation chi (route2_v2 gauge)
    dphi = sp.Matrix([dphi_bg[m] + eps*d(chif, m) for m in range(4)])
    def te(e):
        e = sp.expand(e); out = 0
        for i in range(3):
            ci = e.coeff(eps, i)
            for j in range(3):
                out += ci.coeff(wb, j)*eps**i*wb**j
        return out
    def wtrunc(e):
        e = sp.expand(e); return sum(e.coeff(wb, n)*wb**n for n in range(3))
    guT = sp.Matrix(4, 4, lambda m, n: te(gu[m, n]))
    gdT = sp.Matrix(4, 4, lambda m, n: te(gd[m, n]))
    AupT = sp.Matrix(4, 1, lambda i, j: te(Aup[i]))
    Gam = [[[sp.Rational(1, 2)*sum(gu[r, s]*(d(gd[s, n], m)+d(gd[s, m], n)-d(gd[m, n], s)) for s in range(4))
             for n in range(4)] for m in range(4)] for r in range(4)]
    GamT = [[[te(Gam[r][m][n]) for n in range(4)] for m in range(4)] for r in range(4)]
    dphiT = sp.Matrix(4, 1, lambda i, j: te(dphi[i]))
    # Maxwell part (certified c1=-c3=K_B combination)
    Fmn = sp.Matrix(4, 4, lambda m, n: sp.expand(d(Adn[n], m)-d(Adn[m], n)))
    F1 = sp.Matrix(4, 4, lambda m, n: Fmn[m, n].coeff(eps, 1))
    F2 = eps**2*sum(F1[m, n]*F1[a, b]*eta[m, a]*eta[n, b] for m in range(4) for n in range(4) for a in range(4) for b in range(4))
    # aether acceleration a^al = A^nu D_nu A^al  (same object as the drag's J^mu)
    Jup = [te(sum(AupT[nu]*(d(AupT[al], nu)+sum(GamT[al][nu][r]*AupT[r] for r in range(4))) for nu in range(4))) for al in range(4)]
    # NEW: c4 a.a  and  c2 (D_a A^a)^2
    term4 = te(sum(gdT[m, n]*Jup[m]*Jup[n] for m in range(4) for n in range(4)))
    divA = te(sum(d(AupT[a], a) + sum(GamT[a][a][r]*AupT[r] for r in range(4)) for a in range(4)))
    term2 = te(divA**2)
    P(f"    aether operators built ({time.time()-T0:.1f}s)")
    Jdphi = te(sum(Jup[m]*dphiT[m] for m in range(4)))
    Qc = te(sum(AupT[m]*dphiT[m] for m in range(4)))
    Yc = te(sum((guT[m, n]+AupT[m]*AupT[n])*dphiT[m]*dphiT[n] for m in range(4) for n in range(4)))
    dQ = Qc - Q0; Kq = -2*LAM + K2*te(dQ**2)
    P(f"    dark scalars ({time.time()-T0:.1f}s)")
    def ric(a, b):
        o = 0
        for m in range(4):
            o += d(Gam[m][b][a], m) - d(Gam[m][m][a], b)
            for l in range(4):
                o += Gam[m][m][l]*Gam[l][b][a] - Gam[m][b][l]*Gam[l][m][a]
        return o
    Rsc = te(sum(guT[m, n]*ric(m, n) for m in range(4) for n in range(4)))
    P(f"    Ricci ({time.time()-T0:.1f}s)")
    def grade(e):
        e = sp.expand(e); return [wtrunc(e.coeff(eps, n)) for n in range(3)]
    gF2 = grade(F2); gJ = grade(Jdphi); gY = grade(Yc); gK = grade(Kq)
    g2 = grade(term2); g4 = grade(term4); gsq = grade(sqg); gR = grade(Rsc)
    # pure-EA sign convention (FJ-validated in wf3_pure_ea_control_build): L = R - c1 T1 - c2 T2 - c3 T3 + c4 T4
    gS = [gR[n] - (2*LAM if n == 0 else 0) - (KB/2)*gF2[n] - C2*g2[n] + C4*g4[n]
          + 2*(2-KB)*gJ[n] - (2-KB)*gY[n] - gK[n] for n in range(3)]
    # f31c: two alternative coherence-length operators, each with its own switch
    #   (A) coherent stiffening of the WHOLE Y sector: J_Y -> J_Y (1 + XI2)     [reference: does ANY stiffening suppress the drag?]
    #   (B) the covariant Hessian-squared operator  xi^2 h^{ma} h^{nb} (nabla_m nabla_n phi)(nabla_a nabla_b phi)
    # EFFICIENT BUILD: Gamma_bg = 0 and d d phi_bg = 0, so the Hessian is O(eps) exactly; at O(eps^2) the operator is the
    # BACKGROUND projector h0 (no eps) contracted with the first-order Hessian H1 -- a 16x16 sum of single-eps terms.
    ddchi = [[d(d(chif, n), m) for n in range(4)] for m in range(4)]
    dphi_bgT = sp.Matrix(4, 1, lambda i, j: te(dphi_bg[i]))
    H1 = [[sp.expand(ddchi[m][n] - sum(sp.expand(GamT[l][m][n]).coeff(eps, 1)*dphi_bgT[l] for l in range(4))) for n in range(4)] for m in range(4)]
    h0 = sp.Matrix(4, 4, lambda m, n: wtrunc(sp.expand(eta[m, n] + Aup_bg[m]*Aup_bg[n])))
    HS2 = 0
    for m in range(4):
        for n in range(4):
            if H1[m][n] == 0: continue
            for a in range(4):
                if h0[m, a] == 0: continue
                for b in range(4):
                    if h0[n, b] == 0 or H1[a][b] == 0: continue
                    HS2 += h0[m, a]*h0[n, b]*H1[m][n]*H1[a][b]
    gHS2 = wtrunc(sp.expand(HS2))
    gHS = [0, 0, gHS2]
    P(f"    Hessian-squared operator built (efficient): {len(sp.Add.make_args(gHS2))} terms ({time.time()-T0:.1f}s)")
    # f32: the spatial-gradient-squared operator on V = q.dphi (V_mu = dphi_mu + A_mu (A.dphi)); V_bg = 0 so only V1 enters at O(eps^2)
    Vfull = [te(dphi[m] + Adn[m]*sum(Aup[n]*dphi[n] for n in range(4))) for m in range(4)]
    V0 = [sp.expand(Vfull[m]).coeff(eps, 0) for m in range(4)]
    V1 = [sp.expand(Vfull[m]).coeff(eps, 1) for m in range(4)]
    dV1 = [[sp.expand(d(V1[m], l)) for m in range(4)] for l in range(4)]
    VG2 = 0
    for l in range(4):
        for sg in range(4):
            if h0[l, sg] == 0: continue
            for m in range(4):
                if dV1[l][m] == 0: continue
                for n in range(4):
                    if h0[m, n] == 0 or dV1[sg][n] == 0: continue
                    VG2 += h0[l, sg]*h0[m, n]*dV1[l][m]*dV1[sg][n]
    gVG2 = wtrunc(sp.expand(VG2)); gVG = [0, 0, gVG2]
    P(f"    spatial-gradient-squared operator on V built: {len(sp.Add.make_args(gVG2))} terms; |V_bg| = {[sp.simplify(v) for v in V0]} ({time.time()-T0:.1f}s)")
    identity = wtrunc(sp.expand(gVG2 - kx**2*(1 + wb**2*w1**2)*gY[2]))
    # the residual: keep only its DC (ket x bra) part, the physical quadratic form; split it by sector
    def DCpart(e):
        e = sp.expand(e); pol = sp.Poly(e, Es, Eis); out = 0
        for mon, c in zip(pol.monoms(), pol.coeffs()):
            if mon[0] == mon[1]: out += c*(Es*Eis)**mon[0]
        return sp.expand(out.subs(Es*Eis, 1)) if out != 0 else sp.S(0)
    resDC = DCpart(identity)
    scal = [Psik, Psib, Phik, Phib, s22k, s22b, a1k, a1b, chik, chib]
    res_scalar = sp.expand(resDC.subs({B2k: 0, B2b: 0, B3k: 0, B3b: 0, s23k: 0, s23b: 0, a2k: 0, a2b: 0, a3k: 0, a3b: 0}))
    res_vector = sp.expand(resDC - res_scalar)
    ID = dict(scalar_sector_residual=res_scalar, vector_sector_residual=res_vector,
              vector_vanishes_when_B_equals_a=sp.expand(res_vector.subs({B2k: a2k, B2b: a2b, B3k: a3k, B3b: a3b})))
    P(f"    identity (grad_perp V)^2 == kx^2 (1 + w^2 w1^2) Y_2, DC part: scalar-sector residual = {res_scalar}; vector-sector residual = {str(res_vector)[:160]}; "
      f"vector residual with B_i -> a_i: {ID['vector_vanishes_when_B_equals_a']}")
    pickle.dump(ID, open(CACHE + '.id', 'wb'))
    L2_grav = wtrunc(sum(gsq[a]*gS[2-a] for a in range(3))) - (2-KB)*JY*(1 + XA*XI2)*gY[2] - (2-KB)*JY*XB*XI2*gHS[2] - (2-KB)*JY*XC*XI2*gVG[2]
    L2_matt = -16*sp.pi*GT*wtrunc(rho*(-H[0, 0]/2))
    L2 = sp.expand(L2_grav + L2_matt)
    def DC(e):
        e = sp.expand(e); pol = sp.Poly(e, Es, Eis); out = 0
        for mon, c in zip(pol.monoms(), pol.coeffs()):
            if mon[0] == mon[1]:
                out += c*(Es*Eis)**mon[0]
        return out.subs(Es*Eis, 1) if out != 0 else out
    L2dc = DC(L2)
    pickle.dump(L2dc, open(CACHE, 'wb'))
    P(f"    L2dc built+cached: {len(sp.Add.make_args(L2dc))} terms ({time.time()-T0:.1f}s)")

def wtrunc(e):
    e = sp.expand(e); return sum(e.coeff(wb, n)*wb**n for n in range(3))
Tk, Tb = sp.symbols('Tk Tb')
# exact first-order khronon: A_mu = -d_mu tau/N_tau, tau = tau_bg + eps T:
#   dA_mu = -[d_mu T + Abar_mu (Abar.dT)] - (1/2) Abar_mu H^{AA},  H^{AA} = Hup^{mn} Abar_m Abar_n, Abar_mu = (-S0, w w1, w w2, w w3)
ww_ = w1**2 + w2**2 + w3**2; S0_ = 1 + wb**2*ww_/2
def HAA(Psi_, Phi_, B2_, B3_, s22_, s23_):
    return -2*Psi_*S0_**2 + 2*S0_*wb*(w2*B2_ + w3*B3_) + wb**2*(-2*Phi_*w1**2 + (-2*Phi_ + s22_)*w2**2 + (-2*Phi_ - s22_)*w3**2 + 2*w2*w3*s23_)
HAAk = HAA(Psik, Phik, B2k, B3k, s22k, s23k); HAAb = HAA(Psib, Phib, B2b, B3b, s22b, s23b)
dTk = sp.I*kx*Tk; dTb = -sp.I*kx*Tb                       # d_1 T on the ket and bra copies (k along x)
Abar_low = [-S0_, wb*w1, wb*w2, wb*w3]
KH = {}
for i_, (ak, ab) in enumerate(((a1k, a1b), (a2k, a2b), (a3k, a3b)), start=1):
    delta = 1 if i_ == 1 else 0
    KH[ak] = -(delta*dTk + Abar_low[i_]*(wb*w1)*dTk) - sp.Rational(1, 2)*Abar_low[i_]*HAAk
    KH[ab] = -(delta*dTb + Abar_low[i_]*(wb*w1)*dTb) - sp.Rational(1, 2)*Abar_low[i_]*HAAb
L2kh = wtrunc(sp.expand(L2dc.subs(KH)))
KETS_KH = [Psik, Phik, B2k, B3k, s22k, s23k, Tk, chik]; BRAS_KH = [Psib, Phib, B2b, B3b, s22b, s23b, Tb, chib]
eq = {A: sp.expand(sp.diff(L2kh, A)) for A in BRAS_KH}
P(f"  clock host: L2 after the khronon substitution has {len(sp.Add.make_args(L2kh))} terms; variables {KETS_KH}")
def lin(eqs, unk):
    Am, bb = sp.linear_eq_to_matrix(eqs, unk)
    s_ = list(sp.linsolve((Am, bb), unk))
    return dict(zip(unk, s_[0])) if s_ else None
def ladder(sub):
    sub = {GT: 1, LAM: 0, kx: 1, **sub}
    eqf = {A: sp.expand(eq[A].subs(sub)) for A in BRAS_KH}
    VZ = {B2k: 0, B3k: 0, s23k: 0}
    stat_b = [Psib, Phib, s22b, Tb, chib]; stat_k = [Psik, Phik, s22k, Tk, chik]
    eq0 = [sp.expand(eqf[b].coeff(wb, 0).subs(VZ)) for b in stat_b]
    s0s = lin(eq0, stat_k)
    if s0s is None: return 'SING0'
    s0 = {**s0s, B2k: sp.S(0), B3k: sp.S(0), s23k: sp.S(0)}
    U_amp = sp.cancel(-s0[Psik]/Rk); gamma = sp.cancel(s0[Phik]/s0[Psik])
    dk1 = {A: sp.Symbol(f'd1_{A}') for A in KETS_KH}; dk2 = {A: sp.Symbol(f'd2_{A}') for A in KETS_KH}
    subF = {A: s0[A] + wb*dk1[A] + wb**2*dk2[A] for A in KETS_KH}
    eqW = {A: sp.expand(eqf[A].subs(subF)) for A in BRAS_KH}
    s1 = lin([sp.expand(eqW[A].coeff(wb, 1)) for A in BRAS_KH], list(dk1.values()))
    if s1 is None: return ('SING1', U_amp, gamma)
    c2t = sp.cancel(sp.expand(dk1[B2k].subs(s1)).coeff(w2)/Rk); alpha1 = sp.cancel(2*c2t/U_amp)
    s2 = lin([sp.expand(sp.expand(eqW[A].coeff(wb, 2)).subs(s1)) for A in BRAS_KH], list(dk2.values()))
    if s2 is None: return dict(U=U_amp, g=gamma, a1=alpha1, a2='SING2', a3='SING2')
    h2 = sp.expand(-2*dk2[Psik].subs(s2))
    Cpar = sp.cancel(h2.coeff(w1**2)/Rk/U_amp); Cperp = sp.cancel(h2.coeff(w2**2)/Rk/U_amp)
    return dict(U=U_amp, g=gamma, a1=alpha1, a2=sp.cancel((Cpar-Cperp)/2), a3=sp.cancel(Cperp+alpha1))
q = sp.Symbol('q', positive=True); R = lambda a, b: sp.Rational(a, b)
def lim0(e): return sp.nsimplify(sp.limit(e, q, 0)) if (e != 'SING2' and e.has(q)) else (sp.nsimplify(e) if e != 'SING2' else e)
FAILS = []
P(""); P("="*90); P("MEASURED NEWTON CONSTANT (requirement 10): U_amp of the ladder = G_measured/G_bare x (GR value)"); P("="*90)
def U_of(sub):
    r = ladder(sub); return sp.nsimplify(r['U']) if isinstance(r, dict) else None
# GR reference: no clock terms (K_B -> 0, c2 = c4 = 0), scalar frozen (J_Y = 1e9)
U_GR = U_of({KB: 0, K2: -sp.S(10), JY: sp.S(10**9), Q0: q, C2: 0, C4: 0, XI2: 0, XA: 0, XB: 0, XC: 1})
U_GR = sp.nsimplify(sp.limit(U_GR, q, 0)) if U_GR.has(q) else U_GR
P(f"  GR reference U_amp = {U_GR}")
# Einstein-aether validation: G_N/G = 1/(1 - c14/2)
okEA = True
for c14v in (sp.Rational(1, 10), sp.Rational(1, 2), sp.Rational(1, 100000)):
    U = U_of({KB: R(1,5), K2: -sp.S(10), JY: sp.S(10**9), Q0: q, C2: R(1,10), C4: -R(1,5) + c14v, XI2: 0, XA: 0, XB: 0, XC: 1}); U = sp.nsimplify(sp.limit(U, q, 0)) if U.has(q) else U
    ratio = sp.nsimplify(U/U_GR); pred = 1/(1 - c14v/2)
    P(f"  clock host, scalar frozen, c_14 = {c14v}: G_N/G = {ratio} = {float(ratio):.6f}   (Einstein-aether 1/(1 - c14/2) = {float(pred):.6f})")
    okEA = okEA and abs(float(ratio) - float(pred)) < 1e-9
check("G1 with the scalar frozen the clock host's Newton constant is Einstein-aether's, G_N/G = 1/(1 - c_14/2), at c_14 = 1/10, 1/2 (exact rationals 20/19, 4/3) and 1e-5 (to 1e-9) -- validates the U_amp readout", okEA)
# the scalar's Newtonian-regime share and its screening by the operator
P("  scalar's share of the Newtonian force, f_s = U(J_Y)/U(J_Y -> inf) - 1, at XI2 = 0 (r >> xi) and XI2 = 1e4 (r << xi), clock corner c_14 = 1e-5, c_2 = 1/10:")
Uinf = U_of({KB: R(1,5), K2: -sp.S(10), JY: sp.S(10**9), Q0: q, C2: R(1,10), C4: -R(1,5) + R(1,100000), XI2: 0, XA: 0, XB: 0, XC: 1}); Uinf = sp.nsimplify(sp.limit(Uinf, q, 0)) if Uinf.has(q) else Uinf
FS = {}
for jy in (1, 3, 10, 30, 100):
    for x in (0, 10**4):
        U = U_of({KB: R(1,5), K2: -sp.S(10), JY: sp.S(jy), Q0: q, C2: R(1,10), C4: -R(1,5) + R(1,100000), XI2: sp.S(x), XA: 0, XB: 0, XC: 1}); U = sp.nsimplify(sp.limit(U, q, 0)) if U.has(q) else U
        FS[(jy, x)] = float(U/Uinf - 1)
    P(f"    J_Y = {jy:4d}: f_s(r >> xi) = {FS[(jy, 0)]:+.5f}   f_s(r << xi, XI2 = 1e4) = {FS[(jy, 10**4)]:+.3e}   -> G(r >> xi)/G(r << xi) = {(1 + FS[(jy, 0)])/(1 + FS[(jy, 10**4)]):.5f}")
check("G2 the scalar carries a Newtonian-regime share f_s = 2(2-K_B)... of order 1/J_Y at r >> xi, and the operator screens it below xi (f_s(XI2 = 1e4) < 1e-3 f_s(0) at every J_Y): the measured G is SCALE-DEPENDENT, G(r >> xi)/G(r << xi) = 1 + f_s",
      all(abs(FS[(jy, 10**4)]) < 1e-3*abs(FS[(jy, 0)]) for jy in (1, 3, 10, 30, 100)) and FS[(1, 0)] > 0.1)
closed = sp.nsimplify(FS[(1, 0)]); P(f"  f_s at J_Y = 1: {FS[(1, 0)]:.6f}; test of the closed form f_s = (2 - K_B) ... against the drag structure: f_s(J_Y) J_Y = {[round(FS[(jy, 0)]*jy, 4) for jy in (1, 3, 10, 30, 100)]}")
check("G3 f_s J_Y is constant to 5% for J_Y >= 3 (f_s = A/(J_Y + b) with b small): the share is set by the same Y-sector normalisation as the alpha_1 drag",
      max(abs(FS[(jy, 0)]*jy/(FS[(100, 0)]*100) - 1) for jy in (3, 10, 30)) < 0.05)
P(f"  consequence: a Yukawa-like fifth force of range xi and strength f_s(J_Y) in the NEWTONIAN regime, absent below xi. Wide binaries at 1-30 kAU with g >> a0 bound f_s at the few-per-cent level (Banik et al. 2024 find the Newtonian value), so the candidate needs J_Y,Newton >~ {round(FS[(100, 0)]*100/0.03)} for f_s < 3% -- the same J_Y that makes the alpha_1 drag small even before the operator. This is a computed liability, not a win.")
P(f"\nRESULT: {len(FAILS)} FAIL -> {FAILS}" if FAILS else "\nRESULT: 0 FAIL")
sys.exit(1 if FAILS else 0)
