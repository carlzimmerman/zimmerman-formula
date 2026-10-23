"""X1 E3/E4: X onset closures, dark-sector freeze-out network, xi = 1/6 control, isocurvature (FROZEN_CRITERIA §2).

Physical units GeV. The dark sector couples to the visible sector only through gravity (A6): its energy is conserved
separately and the visible entropy S = s a^3 is conserved after reheating.
Closures at X onset (H = M):  L prompt thermalisation of X condensate + Phi bath (mu = 0);
                              K X condensate = cold X quanta at rest, perturbative in-medium reactions only;
                              C X condensate never interacts (ceiling) + the Phi bath's own relic.
E4 network (kinetic equilibrium, MB forward rates, detailed-balance inverses, BE thermodynamics with Hartree Phi mass):
  r1 X <-> PhiPhi        width g^2 beta/(8 pi M), beta from in-medium Phi mass         dN = (+2, -1)
  r2 XXbar <-> PhiPhibar sigma v = sqrt(1-m^2/M^2) g^4/(2 pi M^6) x in-medium beta     dN = (+2, -2)
  r3 X Phi Phibar <-> PhiPhi  D(T) (Codex MB table; D0 at T->0; T>2m extrapolated)   dN = ( 0, -1)
  r4 4 -> 2 (Phi)        C = 1.0181e14 GeV^-8 (Codex threshold)                         dN = (-2,  0)
  crossed X Phibar Phibar -> Phi Phibar: RIS-subtracted kernel uncomputed (x0 primary, x1 of D sensitivity).
"""
import json
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq, root
from scipy.special import gamma as Gam, roots_legendre

HERE = Path(__file__).resolve().parent
m = .001; M = 2*m*np.sqrt(1+.02**2); g = 2.168e-6; lam = .00881292; MPL = 2.435e18
C42 = json.loads((HERE/'provenance/neutral_four_to_two_v2_run_results.json').read_text())['loss_coefficient_GeV_minus8']
SV2 = np.sqrt(1-m*m/M**2)*g**4/(2*np.pi*M**6)
GX = g*g*np.sqrt(1-4*m*m/M**2)/(8*np.pi*M)
_bt = json.loads((HERE/'provenance/bath_assisted_conversion_run_results.json').read_text())
D0 = _bt['threshold']['D_GeV_minus5']
DT = np.array([[r['T_over_m'], r['D_MB_GeV_minus5']] for r in _bt['rates']])
D_SLOPE_HI = np.log(DT[-1, 1]/DT[-2, 1])/np.log(DT[-1, 0]/DT[-2, 0])     # extrapolation exponent above T = 2m
OMEGA_PER_Y = 1e-3*2891.2/1.0537e-5*(m/1e-3)                             # Omega_c h^2 per unit Y (W counts m)
TARGET_Y = 0.12/OMEGA_PER_Y
B2 = 8*Gam(1.25)**2/np.pi
RATE_SCALE = [1.]              # check K12 only: multiplies every number-changing rate
CAP = 1e4                     # stiffness cap on log-rates per e-fold in the network (numerics)


_MC = json.loads((HERE/'x1_dmc_results.json').read_text()) if (HERE/'x1_dmc_results.json').exists() else None
D_MODE = {'hiT': 'mc'}          # 'mc' (x1_dmc.py, BE + Hartree, primary) or 'powerlaw' (sensitivity)


def Dfun(T, crossed=0.):
    """Thermal-X convention (network r3). T/m <= 2: Codex MB table (D0 at T -> 0); above: x1_dmc.py MC."""
    x = T/m
    if x <= DT[0, 0]:
        d = D0+(DT[0, 1]-D0)*x/DT[0, 0]
    elif x <= DT[-1, 0]:
        d = np.exp(np.interp(np.log(x), np.log(DT[:, 0]), np.log(DT[:, 1])))
    elif D_MODE['hiT'] == 'mc' and _MC is not None:
        tx = np.array([r['T_over_m'] for r in _MC['rest']]); dv = np.array([r['D_thermalX'] for r in _MC['rest']])
        d = np.exp(np.interp(np.log(x), np.log(tx), np.log(dv), right=np.log(dv[-1])+(np.log(dv[-1])-np.log(dv[-2]))
                             /(np.log(tx[-1])-np.log(tx[-2]))*(np.log(x)-np.log(tx[-1]))))
    else:
        d = DT[-1, 1]*(x/DT[-1, 0])**D_SLOPE_HI
    return d*(1+crossed)


def Drest(T, crossed=0.):
    """X at rest (condensate quanta) in the Phi bath: x1_dmc.py MC (BE + Hartree) for T/m >= 0.03, D0 -> table below."""
    x = T/m
    tx = np.array([r['T_over_m'] for r in _MC['rest']]); dv = np.array([r['D_rest'] for r in _MC['rest']])
    if x < tx[0]:
        d = D0+(dv[0]-D0)*x/tx[0]
    else:
        d = np.exp(np.interp(np.log(x), np.log(tx), np.log(dv)))
    return d*(1+crossed)


# ---- visible sector: smoothed-step g*(T), g*s(T) (ASSUMPTION A14) ----
_STEPS = [(1.7e-4, 7.39, 6.84), (.026, 3.5, 3.5), (.035, 3., 3.), (.15, 44.5, 44.5), (.32, 10.5, 10.5), (.45, 3.5, 3.5),
          (1.05, 10.5, 10.5), (20., 6., 6.), (23., 3., 3.), (31., 1., 1.), (43., 10.5, 10.5)]


def gstar(T, s=False):
    gg = 3.91 if s else 3.36
    for Ti, d, ds in _STEPS:
        gg = gg+(ds if s else d)/(1+np.exp(-(np.log(T)-np.log(Ti))/.25))
    return gg


def rho_vis(T): return np.pi**2/30*gstar(T)*T**4
def s_vis(T): return 2*np.pi**2/45*gstar(T, True)*T**3


class Vis:
    """a = 1 at the end of inflation. Instant reheating, or a w = 0 era until H(T_rh) then instant reheating."""
    def __init__(self, Hinf, Trh=None):
        self.Hinf = Hinf
        if Trh is None:
            T1 = brentq(lambda lt: np.log(rho_vis(np.exp(lt))/(3*MPL**2*Hinf**2)), -10, 80)
            self.arh = 1.; self.Trh = np.exp(T1)
        else:
            Hrh = np.sqrt(rho_vis(Trh)/(3*MPL**2)); self.arh = (Hinf/Hrh)**(2/3); self.Trh = Trh
        self.S = s_vis(self.Trh)*self.arh**3

    def T(self, a):
        tgt = self.S/a**3; lg = np.log(self.Trh*self.arh/a)
        return np.exp(brentq(lambda lt: np.log(s_vis(np.exp(lt))/tgt), lg-2, lg+2))

    def H(self, a):
        if a < self.arh: return self.Hinf*a**-1.5
        return np.sqrt(rho_vis(self.T(a))/(3*MPL**2))


# ---- free X condensate (ceiling closure, onset energy) ----
def free_X(vis, X0, Nmax=None):
    """Homogeneous X with zero gradient from a=1 (frozen, slow-roll velocity); returns comoving n a^3 (adiabatic
    invariant once M/H > 300), rho at H = M and a_on."""
    lnH = lambda N: np.log(vis.H(np.exp(N)))
    def rhs(N, y):
        H = vis.H(np.exp(N)); X, V = y; return [V/H, -3*V-M*M*X/H]
    a_on = brentq(lambda N: lnH(N)-np.log(M), 0, 80); a_on = np.exp(a_on)
    N300 = brentq(lambda N: lnH(N)-np.log(M/300), 0, 80)
    y0 = [X0, -M*M*X0/(3*vis.Hinf)]
    sol = solve_ivp(rhs, (0, N300), y0, rtol=1e-11, atol=1e-30*X0, method='DOP853', dense_output=True)
    X, V = sol.y[:, -1]; a = np.exp(N300); H = vis.H(a)
    Xon, Von = sol.sol(np.log(a_on))
    # first-order-corrected adiabatic invariant a^3 (V^2 + M^2 X^2 + 3 H X V)/M (removes the O(H/M) oscillation)
    return dict(Na3=(V*V+M*M*X*X+3*H*X*V)/M*a**3, rho_on=Von**2+M*M*Xon**2, a_on=a_on, nfev=sol.nfev)


def free_X_exact_rd(Hinf, X0):
    return B2*X0**2*Hinf**1.5/np.sqrt(M)


# ---- dark plasma thermodynamics: Bose sums with exponentially scaled Bessel functions ----
from scipy.special import kve
_J = np.arange(1, 81)


def species(T, ms, zeta, gdeg=2):
    """Bose gas, both charges (gdeg = 2) with common mu = ms + zeta T (zeta <= 0).
    Returns n, rho, P and hf = int d^3p/(2pi)^3 f/E summed over the two charges / 2 (the Hartree <|Phi|^2> per complex field)."""
    x = _J*ms/T; w = np.exp(_J*min(zeta, -1e-12))
    K1 = kve(1, x); K2 = kve(2, x); c = gdeg*ms*ms*T/(2*np.pi**2)
    n = c*np.sum(w*K2/_J); rho = c*np.sum(w*(3*T*K2/_J**2+ms*K1/_J)); P = c*T*np.sum(w*K2/_J**2)
    hf = ms*T/(2*np.pi**2)*np.sum(w*K1/_J)*gdeg/2
    return n, rho, P, hf


def meff_eq(T):
    m2 = m*m+lam*T*T/3
    for _ in range(60):
        mm = np.sqrt(m2); hf = species(T, mm, -mm/T)[3]; new = m*m+4*lam*hf
        if abs(new-m2) < 1e-13*new: return np.sqrt(new)
        m2 = new
    return np.sqrt(m2)


_LT = np.linspace(np.log(1e-9), np.log(1e6), 2500)
_TAB = None


def eq_table():
    global _TAB
    if _TAB is None:
        rows = []
        for lt in _LT:
            T = np.exp(lt); mP = meff_eq(T)
            nP, rP, PP, _ = species(T, mP, -mP/T); nX, rX, PX, _ = species(T, M, -M/T)
            rows.append([mP, nP, rP, PP, nX, rX, PX, (rP+PP+rX+PX)/T])
        _TAB = np.array(rows)
    return _TAB


def eq_state(T):
    tab = eq_table(); lt = np.log(T)
    if lt < _LT[0] or lt > _LT[-1]:
        mP = meff_eq(T); nP, rP, PP, _ = species(T, mP, -mP/T); nX, rX, PX, _ = species(T, M, -M/T)
    else:
        mP = np.interp(lt, _LT, tab[:, 0])
        nP, rP, PP, _ = species(T, mP, -mP/T); nX, rX, PX, _ = species(T, M, -M/T)
    return dict(T=T, mP=mP, nP=nP, nX=nX, rho=rP+rX, P=PP+PX, muP=0., muX=0., zP=-mP/T, zX=-M/T)


def s_eq_T(T):
    th = eq_state(T); return (th['rho']+th['P'])/T


def thermo(T, zP, zX):
    mP = np.interp(np.log(T), _LT, eq_table()[:, 0]) if np.log(T) >= _LT[0] else m
    nP, rP, PP, _ = species(T, mP, zP); nX, rX, PX, _ = species(T, M, zX) if zX > -700 else (0., 0., 0., 0.)
    return dict(T=T, mP=mP, nP=nP, nX=nX, rho=rP+rX, P=PP+PX, muP=mP+zP*T, muX=M+zX*T, zP=zP, zX=zX)


# ---- E4 network ----
def rates(th, crossed=0., nXc=0., relcut=None):
    T = th['T']; mP = th['mP']; nP = th['nP']; nX = th['nX']
    b1 = np.sqrt(max(0., 1-4*mP*mP/M**2))/np.sqrt(1-4*m*m/M**2); b2 = np.sqrt(max(0., 1-mP*mP/M**2))/np.sqrt(1-m*m/M**2)
    muP, muX = th['muP'], th['muX']
    def net(a): return -np.expm1(-a/T)
    r = dict(b1=b1, b2=b2)
    r['R1'] = GX*b1*nX*net(muX-2*muP); r['R2'] = SV2*b2*(nX/2)**2*net(2*muX-2*muP)
    c4 = 0. if (relcut is not None and T > relcut) else C42
    r['R3'] = Dfun(T, crossed)*nX*nP**2/2*net(muX); r['R4'] = c4*nP**4/2*net(2*muP)
    r['C1'] = GX*b1*nXc; r['C2'] = SV2*b2*(nXc/2)**2; r['C3'] = Drest(T, crossed)*nXc*nP**2/2
    for k in ('R1', 'R2', 'R3', 'R4', 'C1', 'C2', 'C3'): r[k] *= RATE_SCALE[0]
    r['G4'] = RATE_SCALE[0]*c4*nP**3; r['GX'] = RATE_SCALE[0]*max(Dfun(T, crossed)*nP**2/2, GX*b1, SV2*b2*nX/2)
    return r


def run_plasma(vis, a0, rho0=None, NXc0=0., thP=None, crossed=0., Tstop=1e-3*m, xmax=80., npts=60, relcut=None,
               rule='frozen', wall_limit=None):
    """Dark plasma from a0 (comoving quantities with a/a0 = e^x). Initial state: full chemical equilibrium with energy
    density rho0, or thP = dict(T, zP) for a Phi bath without thermal X; plus cold X at rest (comoving NXc0, closure K).
    Phases: EQ (mu = 0, entropy conserved), PB (mu_P = 0 imposed while r4/H > 1e3; X number integrated), NET (all).
    Returns W = N_Phi + 2 N_X + 2 N_Xc at the end (comoving with a0 = 1)."""
    import time as _time; _t0 = _time.time()
    def _tick():
        if wall_limit is not None and _time.time()-_t0 > wall_limit:
            raise TimeoutError(f'run_plasma wall limit {wall_limit} s')
    an = lambda x: a0*np.exp(x); hist = []
    def rec(th, x, phase, NXc, Wst=None):
        H = vis.H(an(x)); r = rates(th, crossed, NXc*np.exp(-3*x), relcut)
        hist.append(dict(x=float(x), T=float(th['T']), mP=float(th['mP']), nP=float(th['nP']), nX=float(th['nX']),
                         G4H=float(r['G4']/H), GXH=float(r['GX']/H), phase=phase, NXc=float(NXc),
                         W=float(Wst) if Wst is not None else float((th['nP']+2*th['nX'])*np.exp(3*x)+2*NXc),
                         Tvis=float(vis.T(an(x))) if an(x) >= vis.arh else None))
        return r['G4']/H, r['GX']/H
    x = 0.; NXc = NXc0
    if thP is None:
        T0 = np.exp(brentq(lambda lt: np.log(eq_state(np.exp(lt))['rho']/rho0), np.log(1e-9), np.log(1e6)))
        th = eq_state(T0); phase = 'EQ' if NXc0 == 0 else 'PB'
    else:
        th = thermo(thP['T'], thP['zP'], -800.); phase = 'PB'
    if phase == 'EQ':
        S0 = s_eq_T(th['T'])
        tab = eq_table(); lsT = np.log(tab[:, 7])                 # ln s_eq on the T grid (monotone)
        while True:
            g4, gx = rec(th, x, 'EQ', NXc)
            if rule == 'frozen':
                # FROZEN_CRITERIA E4: mu = 0 for the whole plasma while T_d > m/3 and C n^3/H > 100
                if th['T'] < m/3 or g4 < 100: phase = 'NET'; break
            else:
                if g4 < 1e3: phase = 'NET'; break
                if gx < 1e3: phase = 'PB'; break
            if th['T'] < Tstop or x > xmax: phase = 'DONE'; break
            x += .02
            th = eq_state(np.exp(np.interp(np.log(S0)-3*x, lsT, _LT)))
        Ec, NP, NX = th['rho']*np.exp(3*x), th['nP']*np.exp(3*x), th['nX']*np.exp(3*x)
    else:
        Ec, NP, NX = th['rho'], th['nP'], max(th['nX'], 1e-300)
    def solve_PB(Ec_, NX_, xx, guess):
        rho = Ec_*np.exp(-3*xx); nX = max(NX_, 1e-300)*np.exp(-3*xx)
        def F(v):
            T = np.exp(v[0]); mP = np.interp(v[0], _LT, eq_table()[:, 0])
            th_ = thermo(T, -mP/T, v[1]); return [np.log(th_['rho']/rho), np.log(max(th_['nX'], 1e-300)/nX)], th_
        if not np.all(np.isfinite(guess)):
            guess = [np.log(max(rho/1.3, 1e-300)**.25), -1.]
        sol = root(lambda v: F(v)[0], guess, method='hybr', options=dict(xtol=1e-13))
        if not sol.success:      # analytic guess: zeta_X from the ratio to the mu = 0 density at the guessed T
            T = np.exp(guess[0]); te = eq_state(T)
            g2 = [guess[0], min(-M/T+np.log(max(nX, 1e-300)/max(te['nX'], 1e-300)), -1e-9)]
            sol = root(lambda v: F(v)[0], g2, method='hybr', options=dict(xtol=1e-13))
        v = sol.x.copy(); v[1] = min(v[1], -1e-12)
        if not np.all(np.isfinite(v)): v = np.array(guess, dtype=float)
        return F(v)[1], v
    if phase == 'PB':
        st = {'g': [np.log(th['T']), max(min(th['zX'], -1e-12), -700.)]}
        if thP is not None:
            st['g'][1] = min(-M/th['T']+np.log(max(NX, 1e-300)*np.exp(-3*x)/max(eq_state(th['T'])['nX'], 1e-300)), -1e-9)
        NX = max(NX, 1e-20*NP if thP is None else 1e-20*th['nP']); NXc = max(NXc, 1e-300)
        if thP is not None:
            # numerical floor for initially absent thermal X: what the inverse reactions make in one e-fold (keeps the
            # log-variable system non-stiff; AMENDMENT A3 item 6)
            te = eq_state(th['T']); r0 = rates(te, crossed, 0., relcut); H0 = vis.H(an(x))
            NX = max(NX, te['nX']*min(1., r0['GX']/H0)*np.exp(3*x))
        def rhs(xx, ly):
            Ec_, NX_, NXc_ = np.exp(ly); th_, v = solve_PB(Ec_, NX_, xx, st['g']); st['g'] = v
            H = vis.H(an(xx)); r = rates(th_, crossed, (NXc_ if NXc0 > 0 else 0.)*np.exp(-3*xx), relcut); a3 = np.exp(3*xx)
            cons = r['C1']+2*r['C2']+r['C3'] if NXc0 > 0 else 0.
            out = np.nan_to_num(np.array([(-3*th_['P']*a3+M*cons*a3/H)/Ec_, (-r['R1']-2*r['R2']-r['R3'])*a3/H/NX_,
                                          -cons*a3/H/NXc_]), nan=0., posinf=CAP, neginf=-CAP)
            return CAP*np.tanh(out/CAP)
        # chunked integration in steps of 0.25 e-folds; leave PB when r4/H < 1e3 (no event root-finding)
        ly = np.log([Ec, NX, NXc]); left = False
        while x < xmax:
            sol = solve_ivp(rhs, (x, x+.25), ly, method='LSODA', rtol=1e-6, atol=1e-8)
            if sol.status < 0 or not np.all(np.isfinite(sol.y[:, -1])):
                sol = solve_ivp(rhs, (x, x+.25), ly, method='Radau', rtol=1e-6, atol=1e-8)
            x = sol.t[-1]; ly = sol.y[:, -1]
            _tick(); th_, v = solve_PB(np.exp(ly[0]), np.exp(ly[1]), x, st['g'])
            rec(th_, x, 'PB', np.exp(ly[2]) if NXc0 > 0 else 0.)
            if rates(th_, crossed, 0., relcut)['G4']/vis.H(an(x)) < 1e3: left = True; break
        Ec, NX, NXc = np.exp(ly); NXc = NXc if NXc0 > 0 else 0.
        th, v = solve_PB(Ec, NX, x, st['g']); NP = th['nP']*np.exp(3*x)
        phase = 'NET' if left else 'DONE'
    def solve_N(Ec_, NP_, NX_, xx, guess):
        rho = Ec_*np.exp(-3*xx); nP = max(NP_, 1e-300)*np.exp(-3*xx); nX = max(NX_, 1e-300)*np.exp(-3*xx)
        def F(v):
            th_ = thermo(np.exp(v[0]), min(v[1], -1e-12), min(v[2], -1e-12))
            return [np.log(th_['rho']/rho), np.log(max(th_['nP'], 1e-300)/nP), np.log(max(th_['nX'], 1e-300)/nX)], th_
        if not np.all(np.isfinite(guess)):
            guess = [np.log(max(rho/1.3, 1e-300)**.25), -1., -1.]
        sol = root(lambda v: F(v)[0], guess, method='hybr', options=dict(xtol=1e-13))
        if not sol.success:
            T = np.exp(guess[0]); te = eq_state(T)
            g2 = [guess[0], min(-te['mP']/T+np.log(nP/max(te['nP'], 1e-300)), -1e-9),
                  min(-M/T+np.log(max(nX, 1e-300)/max(te['nX'], 1e-300)), -1e-9)]
            sol = root(lambda v: F(v)[0], g2, method='hybr', options=dict(xtol=1e-13))
        v = sol.x.copy(); v[1] = min(v[1], -1e-12); v[2] = min(v[2], -1e-12)
        if not np.all(np.isfinite(v)): v = np.array(guess, dtype=float)
        return F(v)[1], v
    if phase == 'NET':
        st = {'g': [np.log(th['T']), max(th['zP'], -700.), max(min(th['zX'], -1e-12), -700.)]}
        # NET variables (ln E_c, ln W, y_X = N_X/W): W = N_Phi + 2 N_X changes only through r2, r3, r4 (r1 conserves it),
        # so no stiffness cap is needed and the stoichiometry is exact; cold X (closure K, rule 'pb') kept as ln N_Xc.
        NXc = max(NXc, 1e-300); W0 = NP+2*NX; yX0 = max(NX/W0, 1e-30)
        def state(y):
            Ec_, W_ = np.exp(y[0]), np.exp(y[1]); yX = min(max(y[2], 1e-30), .5-1e-15)
            return Ec_, W_*(1-2*yX), W_*yX, np.exp(y[3])
        def rhsN(xx, y):
            Ec_, NP_, NX_, NXc_ = state(y); th_, v = solve_N(Ec_, NP_, NX_, xx, st['g']); st['g'] = v
            H = vis.H(an(xx)); r = rates(th_, crossed, (NXc_ if NXc0 > 0 else 0.)*np.exp(-3*xx), relcut); a3 = np.exp(3*xx)
            cons = r['C1']+2*r['C2']+r['C3'] if NXc0 > 0 else 0.
            W_ = NP_+2*NX_
            dW = (-2*(r['R2']+r['R3']+r['R4']))*a3/H
            dNX = (-r['R1']-2*r['R2']-r['R3'])*a3/H
            dWc = (2*r['C1']+2*r['C2'])*a3/H-2*cons*a3/H      # cold-X channels move W between N_Xc and the plasma
            dW_tot = dW+(2*r['C1']+2*r['C2'])*a3/H
            return [(-3*th_['P']*a3+M*cons*a3/H)/Ec_, dW_tot/W_, (dNX-NX_/W_*dW_tot)/W_, -cons*a3/H/NXc_]
        y = np.array([np.log(Ec), np.log(W0), yX0, np.log(NXc)]); xs = [x]; ys = [y.copy()]; Wprev = None
        while x < xmax:
            sol = solve_ivp(rhsN, (x, x+1.), y, method='LSODA', rtol=1e-6, atol=[1e-8, 1e-8, 1e-14, 1e-8])
            if sol.status < 0 or not np.all(np.isfinite(sol.y[:, -1])):
                sol = solve_ivp(rhsN, (x, x+1.), y, method='Radau', rtol=1e-6, atol=[1e-8, 1e-8, 1e-14, 1e-8])
            if sol.status < 0 or not np.all(np.isfinite(sol.y[:, -1])):
                raise RuntimeError(f'NET chunk failed at x={x}: {sol.message}')
            x = sol.t[-1]; y = sol.y[:, -1]; xs.append(x); ys.append(y.copy()); _tick()
            Ec_, NP_, NX_, NXc_ = state(y); th_, v = solve_N(Ec_, NP_, NX_, x, st['g'])
            Wn = np.exp(y[1])+(2*NXc_ if NXc0 > 0 else 0.)
            r_ = rates(th_, crossed, 0., relcut); a3 = np.exp(3*x)
            dlnW = abs(2*(r_['R2']+r_['R3']+r_['R4'])*a3/vis.H(an(x))/np.exp(y[1]))
            # W frozen: below m/3 every threshold is open, and the W-changing log-rate < 1e-4 per e-fold on two
            # consecutive chunks (the rates only fall from here); avoids resolving the kinetic energy of a cold gas
            if (th_['T'] < m/3 and dlnW < 1e-4 and Wprev is not None and abs(Wn/Wprev-1) < 1e-4 and NXc0 == 0) \
                    or (th_['T'] < Tstop and Wprev is not None and abs(Wn/Wprev-1) < 1e-6):
                break
            Wprev = Wn
        gq = [np.log(th['T']), max(th['zP'], -700.), max(min(th['zX'], -1e-12), -700.)]
        for xx, yy in zip(xs, ys):
            Ec_, NP_, NX_, NXc_ = state(yy); th_, gq = solve_N(Ec_, NP_, NX_, xx, gq)
            rec(th_, xx, 'NET', NXc_ if NXc0 > 0 else 0., NP_+2*NX_+(2*NXc_ if NXc0 > 0 else 0.))
        Ec, NP, NX, NXc = state(y); NXc = NXc if NXc0 > 0 else 0.
    W = NP+2*NX+2*NXc
    return dict(W=float(W), x_end=float(x), T_end=float(hist[-1]['T']), hist=hist)
