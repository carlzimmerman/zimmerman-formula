"""f34 -- TIME-DEPENDENT quadratic action of the candidate's scalar sector: metric (Newtonian gauge + tensors) + clock (khronon T) + MOND scalar chi
with the operator xi^2 |grad_perp V|^2, in the clock rest frame (no boost).  Same symbolic build as f31c/f32 with modes e^{i(k x - omega t)}
(kv = [-omega, k, 0, 0]).  Outputs: the tensor dispersion (must be omega^2 = k^2: c_T = c), the scalar-sector dispersion det M(omega, k) = 0,
the sign of each mode's norm v^dagger (dM/d omega^2) v (positive = healthy, negative = ghost), and the large-k behaviour (Lifshitz omega^2 ~ xi^2 k^4).
Parameters: the khronometric corner c_13 = 0, c_14 = 1e-5, c_2 = 1/10; K_B = 1/5; K_2 = 10; J_Y = 1; Q_0 -> 0.  Checks can fail."""
import sympy as sp, time, pickle, os, sys
T0 = time.time(); P = lambda *a: print(*a, flush=True)
import tempfile
SC = os.environ.get('SCRATCH', tempfile.gettempdir()) + '/'
os.makedirs(SC, exist_ok=True)
CACHE = SC + 'L2dc_k4_timedep.pkl'
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
kx = sp.symbols('k_x', real=True); om = sp.symbols('omega', real=True)
eta = sp.diag(-1, 1, 1, 1); I = sp.I
Es, Eis = sp.symbols('E_s E_is')
kv = [-om, kx, 0, 0]
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

import numpy as np, math
Tk, Tb = sp.symbols('Tk Tb')
L0 = sp.expand(L2dc.subs({wb: 0}))                                                       # clock rest frame
KH = {a2k: 0, a2b: 0, a3k: 0, a3b: 0, a1k: -sp.I*kx*Tk, a1b: sp.I*kx*Tb}                # khronon: a_i = -d_i T (rest frame; a_0 from the norm constraint)
Lk = sp.expand(L0.subs(KH))
PAR = {KB: sp.Rational(1, 5), K2: sp.S(10), JY: sp.S(1), C2: sp.Rational(1, 10), C4: -sp.Rational(1, 5) + sp.Rational(1, 100000), GT: 1, LAM: 0, XA: 0, XB: 0}
xi2 = sp.symbols('xi2', positive=True)                                                   # xi^2 (the operator carries its own k^2 through gVG2)
FAILS = []
def matrix(L, kets, bras):
    return sp.Matrix(len(bras), len(kets), lambda a, b: sp.expand(sp.diff(L, bras[a], kets[b])))
def modes(L, kets, bras, sub):
    M = matrix(L, kets, bras).subs(sub); M = M.applyfunc(sp.expand)
    det = sp.factor(sp.expand(M.det()))
    return M, det
w2 = sp.symbols('w2')
def even_poly(det):
    """det as a polynomial in omega^2 (det is even in omega); returns sympy Poly in w2"""
    pw = sp.Poly(sp.expand(det), om); cs = pw.all_coeffs()[::-1]
    assert all(sp.simplify(c) == 0 for c in cs[1::2]), "odd powers of omega present"
    return sp.Poly(sum(c*w2**(n//2) for n, c in enumerate(cs) if n % 2 == 0), w2)
P(""); P("="*90); P("TIME-DEPENDENT SCALAR SECTOR, clock rest frame"); P("="*90)
Lt = Lk.subs({Psik: 0, Psib: 0, Phik: 0, Phib: 0, B2k: 0, B2b: 0, B3k: 0, B3b: 0, s23k: 0, s23b: 0, Tk: 0, Tb: 0, chik: 0, chib: 0, Rk: 0, Rb: 0})
Mt, dett = modes(Lt, [s22k], [s22b], {**PAR, XC: 1, XI2: xi2, Q0: 0})
rt = [sp.simplify(r) for r in sp.solve(sp.Eq(even_poly(dett).as_expr(), 0), w2)]
P(f"  tensor (h_+): det = {dett};  omega^2 = {rt}")
check("T1 the tensor mode has omega^2 = k^2 exactly (c_T = c, requirement 6) with the operator present", any(sp.simplify(r - kx**2) == 0 for r in rt))
Ls = Lk.subs({B2k: 0, B2b: 0, B3k: 0, B3b: 0, s22k: 0, s22b: 0, s23k: 0, s23b: 0, Rk: 0, Rb: 0})
kets = [Psik, Phik, Tk, chik]; bras = [Psib, Phib, Tb, chib]
def analyse(c2v, c14v, xc, label, verbose=True):
    par = {**PAR, C2: c2v, C4: -sp.Rational(1, 5) + c14v, XC: xc, XI2: xi2, Q0: 0}
    M, det = modes(Ls, kets, bras, par); pw = even_poly(det)
    roots = sp.solve(sp.Eq(pw.as_expr(), 0), w2)
    rows = []; ok_real = True; ok_norm = True
    for kxi in (1e-2, 1.0, 100.0):
        sub = {kx: kxi, xi2: 1.0}
        for r in roots:
            rv = complex(sp.N(r.subs(sub)))
            if abs(rv.imag) > 1e-9*max(1, abs(rv)) or rv.real <= 0: ok_real = False; rows.append((kxi, rv, float('nan'))); continue
            wv = math.sqrt(rv.real); Mn = np.array(sp.N(M.subs({**sub, om: wv})), dtype=complex)
            v = np.linalg.svd(Mn)[2].conj().T[:, -1]; dMn = np.array(sp.N((M.diff(om)/(2*om)).subs({**sub, om: wv})), dtype=complex)
            nrm = float(np.real(v.conj() @ dMn @ v)); ok_norm = ok_norm and nrm > 0; rows.append((kxi, rv, nrm))
    if verbose:
        P(f"  {label}: det/k^6 = {sp.factor(sp.cancel(det/kx**6))}")
        for kxi, rv, nrm in rows: P(f"      k xi = {kxi:7.2f}: omega^2 xi^2 = {rv.real:+.6e}{'' if abs(rv.imag) < 1e-9 else ' (complex)'}   norm = {nrm:+.3e}")
    return roots, rows, ok_real, ok_norm
P("  scan (pipeline convention: L = R - c2 (D.A)^2 + c4 a.a, c1 = -c3 = K_B, scalar Q-sector -K_2 (dQ)^2): K_2 sign, c_2 grid, c_14 size")
scan = {}
for k2v in (sp.S(10), -sp.S(10)):
    for c2v in (sp.Rational(1, 10), sp.Rational(1, 2), sp.S(1), sp.S(2), -sp.Rational(1, 2), -sp.S(2), -sp.S(4)):
        for c14v in (sp.Rational(1, 100000), sp.Rational(1, 100)):
            PAR[K2] = k2v
            roots, rows, okr, okn = analyse(c2v, c14v, 1, "", verbose=False)
            scan[(k2v, c2v, c14v)] = (okr, okn, rows)
            P(f"    K_2 = {str(k2v):3s} c_2 = {str(c2v):5s} c_14 = {str(c14v):8s}: real & positive: {str(okr):5s} norms positive: {str(okn):5s} omega^2 xi^2 at k xi = 1: {[f'{r[1].real:+.3e}' for r in rows if r[0] == 1.0]}")
healthy = [k for k, v in scan.items() if v[0] and v[1]]
check("H1 there is a healthy region of the clock parameters (all scalar roots real, positive, positive-norm) with the operator present", bool(healthy), f"healthy: {healthy}")
if healthy:
    k2h, c2h, c14h = sorted(healthy, key=lambda k: (k[2], abs(k[1])))[0]; PAR[K2] = k2h
    roots, rows, okr, okn = analyse(c2h, c14h, 1, f"HEALTHY POINT K_2 = {k2h}, c_2 = {c2h}, c_14 = {c14h}, with the operator")
    roots0, rows0, okr0, okn0 = analyse(c2h, c14h, 0, f"same point, operator removed")
    check("S1 at the healthy point every scalar-sector root is real and positive for k xi = 0.01, 1, 100 (no gradient instability)", okr)
    check("S2 at the healthy point every scalar mode has positive norm (no ghost)", okn)
    # branch identification: at small k the two branches are the MOND scalar (small c_s^2) and the khronon (c_s^2 ~ 1/c_14, large)
    def branches(rws):
        out = {}
        for kxi in (1e-2, 1.0, 100.0):
            vals = sorted(r[1].real for r in rws if r[0] == kxi); out[kxi] = vals          # [slow branch, fast branch]
        return out
    b1, b0 = branches(rows), branches(rows0)
    cs2_chi, cs2_kh = b1[1e-2][0]/1e-4, b1[1e-2][1]/1e-4
    lif_with = b1[100.0][0]/1e8; lif_without = b0[100.0][0]/1e8
    P(f"    branches at small k: MOND scalar c_s^2 = {cs2_chi:.4e}, khronon c_s^2 = {cs2_kh:.4e} (~ 1/c_14: the khronometric fast mode)")
    P(f"    MOND-scalar branch at k xi = 100: omega^2/(xi^2 k^4) = {lif_with:.4f} with the operator (Bogoliubov: -> c_s^2 = {cs2_chi:.4f}), {lif_without:.2e} without")
    check("S3 the MOND scalar's branch is Bogoliubov/Lifshitz at short wavelength: omega^2/(xi^2 k^4) at k xi = 100 within 30% of its own small-k c_s^2, and 100x smaller without the operator",
          abs(lif_with/cs2_chi - 1) < 0.3 and lif_without < 0.01*lif_with, f"{lif_with:.4f} vs c_s^2 {cs2_chi:.4f}; without {lif_without:.2e}")
    check("S4 the khronon branch is changed by the operator only through its mixing with the MOND scalar: under 10% at k xi = 100 (it is a few per cent)", abs(b1[100.0][1]/b0[100.0][1] - 1) < 0.10, f"ratio {b1[100.0][1]/b0[100.0][1]:.4f}")
    check("S5 the MOND scalar's time-kinetic sign: healthy only for K_2 < 0 in this pipeline's convention (every K_2 = +10 point has a tachyonic root); the static ladders (f31-f33) are insensitive to that sign, f33b re-derives the PPN corner at K_2 = -10",
          all(not v[0] for k, v in scan.items() if k[0] == 10) and any(v[0] and v[1] for k, v in scan.items() if k[0] == -10))
    P(f"    PPN corner note: f33 used K_2 = 10, c_2 = 1/10, c_14 = 1e-5; the healthy point is K_2 = {k2h}, c_2 = {c2h}, c_14 = {c14h} -- the PPN ladder is re-run there in f33b")
P(f"\nRESULT: {len(FAILS)} FAIL -> {FAILS}" if FAILS else "\nRESULT: 0 FAIL")
sys.exit(1 if FAILS else 0)
