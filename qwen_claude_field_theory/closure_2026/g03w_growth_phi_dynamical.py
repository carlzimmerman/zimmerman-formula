#!/usr/bin/env python3
"""
g03w -- the linear growth with Phi dynamical (no quasi-static metric closure)
===============================================================================
g03v's coupled runs blew up from z = 100 with the metric potentials solved quasi-statically.  Here the same symbolic equations
(g03v's second-order expansion of clock + condensate + Einstein-Hilbert; J_Y0 = 0) are integrated with Phi as a dynamical
variable: the Phi equation is the ij-trace equation (it carries Phi'' from the Einstein-Hilbert part), the lapse (Psi) equation
is the Hamiltonian constraint solved exactly for Psi at every step, and Psi' is obtained by differentiating that constraint
(the constraint is linear in the state with a(t)-dependent coefficients; their a-derivatives by finite difference).  The
resulting linear system in (Phi'', T'', P'') is solved at each step; baryons follow delta'' + 2H delta' = -k^2 Psi/a^2.
State: (delta, delta', Phi, Phi', T, T', P, P').  Units and parameters as in g03v.
CLOCK = 'adiabatic': the clock equation's restoring term (the condensate's background charge, ~1e9 against an inertia c14 k^2 a ~ 1e-2 at
z = 100: a mode at ~1e5-1e6 H0) is eliminated adiabatically -- T follows Psi, P, P' algebraically; with CLOCK = 'full' the mode is
integrated explicitly and fails (NaN at the first step; recorded).

OUTCOME (2026-09-06): the ODE scans fail in every branch -- full clock: NaN at the first step (a mode at ~1e5-1e6 H0); adiabatic clock: exponential
growth e^18 per da = 2e-4 from a = 0.0102 -- so the script now runs the GR control and a frozen-coefficient EIGENMODE analysis instead:
  W5a [control]  the GR system has no exponential mode beyond the growing mode;
  W5b [finding]  with the sector on there is a real exponential eigenvalue > 100 H at a = 0.01 in every branch, > 1e4 H at a = 0.3 in the fast
                 and c2 = 1e-4 branches, absent at a = 0.3 for c2 = 0.05; the clock equation's condensate-background term is tachyonic:
                 T'' = (|K_2| Q0^2 eps0 a^-3 / c_14) T, k-independent -- a candidate KILL of the clock + condensate sector on FLRW that the
                 Minkowski health check (f34) cannot see; whether the reduced system's mode is exactly that one or partly a
                 constraint-differentiation artefact needs a constraint-preserving formulation (open).
"""
import numpy as np, math, sys, time, json
src = open("g03v_fast_clock_branch.py").read(); head = src[:src.index("SRC_SIGN = 1.0")]
g = {}; exec(compile(head, "g03v_head", "exec"), g)
COEF, REST, VARS, Hof, addot_of, growth_LCDM, cH0_Mpc, Om, OL, Ob, Od, H0 = (g[k] for k in ("COEF", "REST", "VARS", "Hof", "addot_of", "growth_LCDM", "cH0_Mpc", "Om", "OL", "Ob", "Od", "H0"))
from scipy.integrate import solve_ivp
CLOCK = 'adiabatic'
FAILS = []
def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
T0 = time.time()
TABLES = {}
def build_tables(kk, pars, AA):
    """all coefficients of the four equations on the a-grid, once per run, and their a-derivatives"""
    KBv, c2v, c14v, K2v, Q0v, eps0v = pars; H = Hof(AA); args = (kk, AA, AA*H, addot_of(AA), KBv, c2v, c14v, K2v, Q0v, eps0v, 3*OL*H0**2)
    tab = {}
    for nm in ('Psi', 'Phi', 'T', 'P'):
        M = np.zeros((len(VARS), len(AA)))
        for i, v in enumerate(VARS):
            val = COEF[nm][v](*args); M[i] = np.broadcast_to(np.asarray(val, float), AA.shape)
        tab[nm] = M; tab[nm + '_da'] = np.gradient(M, AA, axis=1)
    TABLES['AA'] = AA; TABLES['tab'] = tab
def coefs(nm, aa, kk=None, pars=None, deriv=False):
    AA = TABLES['AA']; j = min(max(int(np.searchsorted(AA, aa)) - 1, 0), len(AA) - 2); w = (aa - AA[j])/(AA[j + 1] - AA[j])
    M = TABLES['tab'][nm + ('_da' if deriv else '')]; row = M[:, j]*(1 - w) + M[:, j + 1]*w
    return {v: float(row[i]) for i, v in enumerate(VARS)}
def run(kMpc, pars, sector=True, ai=0.01, af=1.0, src_scale=None):
    kk = kMpc*cH0_Mpc; Omat = Om if not sector else Ob
    aa_grid = np.geomspace(ai, af, 4000); TT = np.concatenate([[0.0], np.cumsum(np.diff(aa_grid)/(0.5*(aa_grid[1:]*Hof(aa_grid[1:]) + aa_grid[:-1]*Hof(aa_grid[:-1]))))]); AA = aa_grid
    build_tables(kk, pars, AA)
    def psi_of(aa, st):
        """Hamiltonian constraint solved for Psi: cP[Psi] Psi + sum(other) = src"""
        delta, dd, Ph, Pht, T, Tt, Pv, Pt = st; cP = coefs('Psi', aa, kk, pars)
        srcv = 6*Omat*H0**2*delta
        if CLOCK == 'adiabatic' and sector:
            cT = coefs('T', aa, kk, pars)                                                            # Psi and T are coupled algebraically: T = -(cT_Psi Psi + cT_P P + cT_Pt P')/cT_T; T' dropped in the constraint (adiabatic)
            other0 = cP['Phik']*Ph + cP['Phik_t']*Pht + cP['Pk']*Pv + cP['Pk_t']*Pt
            # c_psi Psi + cP_T T = src - other0  with T = alpha Psi + beta
            alpha = -cT['Psik']/cT['Tk']; beta = -(cT['Pk']*Pv + cT['Pk_t']*Pt)/cT['Tk']
            return (srcv - other0 - cP['Tk']*beta)/(cP['Psik'] + cP['Tk']*alpha), cP
        other = cP['Phik']*Ph + cP['Phik_t']*Pht + cP['Tk']*T + cP['Tk_t']*Tt + cP['Pk']*Pv + cP['Pk_t']*Pt
        return (srcv - other)/cP['Psik'], cP
    def rhs(tt, st):
        aa = float(np.interp(tt, TT, AA)); H = Hof(aa); delta, dd, Ph, Pht, T, Tt, Pv, Pt = st
        Ps, cP = psi_of(aa, st)
        ddd = -2*H*dd - kk**2*Ps/aa**2
        if not sector:
            # GR: Phi equation with Phi'' from the Einstein-Hilbert part
            cF = coefs('Phi', aa, kk, pars)
            # Psi' from the differentiated constraint (state derivatives: Phi'' unknown -> linear)
            dcP = {v: c_*aa*H for v, c_ in coefs('Psi', aa, deriv=True).items()}
            srcv = 6*Omat*H0**2*delta; dsrc = 6*Omat*H0**2*dd
            # Psi = (src - sum c_v v)/c_psi ; Psi' = [dsrc - sum(c_v v' + dc_v v) - Psi dc_psi]/c_psi with v' including Phi'' (unknown X)
            known = dsrc - (cP['Phik']*Pht + dcP['Phik']*Ph + dcP['Phik_t']*Pht) - Ps*dcP['Psik']
            # Psi' = (known - cP['Phik_t'] X)/c_psi
            A_ = -cP['Phik_t']/cP['Psik']; B_ = known/cP['Psik']
            # Phi equation: cF[Phik_tt] X + cF[Phik_t] Pht + cF[Phik] Ph + cF[Psik] Ps + cF[Psik_t] (A_ X + B_) = 0
            X = -(cF['Phik_t']*Pht + cF['Phik']*Ph + cF['Psik']*Ps + cF['Psik_t']*B_)/(cF['Phik_tt'] + cF['Psik_t']*A_)
            return [dd, ddd, Pht, X, 0, 0, 0, 0]
        cF = coefs('Phi', aa, kk, pars); cT = coefs('T', aa, kk, pars); cQ = coefs('P', aa, kk, pars)
        dcP = {v: c_*aa*H for v, c_ in coefs('Psi', aa, deriv=True).items()}
        if CLOCK == 'adiabatic':
            # the clock's own equation has a restoring term cT[Tk] ~ 1e9 (the condensate's background charge) against an inertia cT[Tk_tt] ~ c14 k^2 a: a mode at
            # ~1e5-1e6 H0.  Eliminate it adiabatically: T = -(cT_Psi Psi + cT_P P + cT_Pt P')/cT_T (the c14-suppressed Psi', Phi' terms dropped), and its time
            # derivative from differentiation.  Unknowns u = (Phi'', P'', Psi', T'): (1) Phi eq., (2) P eq., (3) differentiated lapse constraint, (4) differentiated T relation.
            dcT = {v: c_*aa*H for v, c_ in coefs('T', aa, deriv=True).items()}
            Tq = -(cT['Psik']*Ps + cT['Pk']*Pv + cT['Pk_t']*Pt)/cT['Tk']
            # (4): T' = -(cT_Psi Psi' + dcT_Psi Psi + cT_P P' + dcT_P P + cT_Pt P'' + dcT_Pt P' + dcT_T Tq)/cT_T  ->  T' + (cT_Psi/cT_T) Psi' + (cT_Pt/cT_T) P'' = r4
            r4 = -(dcT['Psik']*Ps + cT['Pk']*Pt + dcT['Pk']*Pv + dcT['Pk_t']*Pt + dcT['Tk']*Tq)/cT['Tk']
            # (3): differentiated constraint: c_psi Psi' = dsrc - [cP_Phi Phi' + dcP_Phi Phi + cP_Phit Phi'' + dcP_Phit Phi' + cP_T T' + dcP_T T + cP_Tt T'' + dcP_Tt T' + cP_P P' + dcP_P P + cP_Pt P'' + dcP_Pt P'] - Psi dc_psi ; T'' dropped (adiabatic)
            srcv = 6*Omat*H0**2*delta; dsrc = 6*Omat*H0**2*dd
            r3 = dsrc - (cP['Phik']*Pht + dcP['Phik']*Ph + dcP['Phik_t']*Pht + dcP['Tk']*Tq + cP['Pk']*Pt + dcP['Pk']*Pv + dcP['Pk_t']*Pt) - Ps*dcP['Psik']
            # rows: u = (Phi'', P'', Psi', T')
            A = np.zeros((4, 4)); b = np.zeros(4)
            A[0] = [cF['Phik_tt'], cF['Pk_tt'], cF['Psik_t'], cF['Tk_t']]; b[0] = -(cF['Phik_t']*Pht + cF['Phik']*Ph + cF['Tk']*Tq + cF['Pk_t']*Pt + cF['Pk']*Pv + cF['Psik']*Ps)
            A[1] = [cQ['Phik_tt'], cQ['Pk_tt'], cQ['Psik_t'], cQ['Tk_t']]; b[1] = -(cQ['Phik_t']*Pht + cQ['Phik']*Ph + cQ['Tk']*Tq + cQ['Pk_t']*Pt + cQ['Pk']*Pv + cQ['Psik']*Ps)
            A[2] = [cP['Phik_t'], cP['Pk_t'], cP['Psik'], cP['Tk'] + dcP['Tk_t']]; b[2] = r3
            A[3] = [0.0, cT['Pk_t']/cT['Tk'], cT['Psik']/cT['Tk'], 1.0]; b[3] = r4
            u = np.linalg.solve(A, b)
            return [dd, ddd, Pht, u[0], 0.0, 0.0, Pt, u[1]]
        srcv = 6*Omat*H0**2*delta; dsrc = 6*Omat*H0**2*dd
        # Psi' = (known - [cP_Phit X_Phi + cP_Tt X_T + cP_Pt X_P])/c_psi ; X = second derivatives (unknown)
        known = dsrc - (cP['Phik']*Pht + dcP['Phik']*Ph + dcP['Phik_t']*Pht + cP['Tk']*Tt + dcP['Tk']*T + dcP['Tk_t']*Tt + cP['Pk']*Pt + dcP['Pk']*Pv + dcP['Pk_t']*Pt) - Ps*dcP['Psik']
        aX = np.array([-cP['Phik_t'], -cP['Tk_t'], -cP['Pk_t']])/cP['Psik']; bX = known/cP['Psik']       # Psi' = aX . X + bX
        M = np.zeros((3, 3)); r = np.zeros(3)
        for i, (nm, c) in enumerate((('Phi', cF), ('T', cT), ('P', cQ))):
            M[i] = [c['Phik_tt'] + c['Psik_t']*aX[0], c['Tk_tt'] + c['Psik_t']*aX[1], c['Pk_tt'] + c['Psik_t']*aX[2]]
            r[i] = -(c['Phik_t']*Pht + c['Phik']*Ph + c['Tk_t']*Tt + c['Tk']*T + c['Pk_t']*Pt + c['Pk']*Pv + c['Psik']*Ps + c['Psik_t']*bX)
        X = np.linalg.solve(M, r)
        return [dd, ddd, Pht, X[0], Tt, X[1], Pt, X[2]]
    Hi = Hof(ai); st0 = [1.0, Hi, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    # consistent initial Phi from the GR Poisson relation (growing mode), Phi' ~ 0 in matter era
    cP0 = coefs('Psi', ai); st0[2] = (6*Omat*H0**2*1.0)/cP0['Phik'] if not sector else (6*Omat*H0**2*1.0)/cP0['Phik']
    sol = solve_ivp(rhs, [0, TT[-1]], st0, method='LSODA', rtol=1e-8, atol=1e-14, max_step=TT[-1]/400, t_eval=np.linspace(0, TT[-1], 9))
    fin = bool(np.all(np.isfinite(sol.y))) and sol.success
    delta = sol.y[0, -1]; Ps, _ = psi_of(af, sol.y[:, -1])
    return dict(growth=delta, finite=fin, trace=sol.y[0], a_trace=np.interp(sol.t, TT, AA), Psi=Ps, Phi=sol.y[2, -1], T=sol.y[4, -1], Tt=sol.y[5, -1])
D_L = growth_LCDM(0.01, 1.0); kt = [0.05, 0.2]
def eigen(kMpc, pars, sector, aa_list=(0.01, 0.3, 1.0)):
    """frozen-coefficient eigenvalues of the reduced first-order system at scale factor a (Jacobian of rhs by finite differences)"""
    kk = kMpc*cH0_Mpc; aa_grid = np.geomspace(0.01, 1.0, 4000); build_tables(kk, pars, aa_grid)
    TT = np.concatenate([[0.0], np.cumsum(np.diff(aa_grid)/(0.5*(aa_grid[1:]*Hof(aa_grid[1:]) + aa_grid[:-1]*Hof(aa_grid[:-1]))))]); AA = aa_grid
    Omat = Om if not sector else Ob
    def psi_of(aa, st):
        delta, dd, Ph, Pht, T, Tt, Pv, Pt = st; cP = coefs('Psi', aa); srcv = 6*Omat*H0**2*delta
        if sector:
            cT = coefs('T', aa); other0 = cP['Phik']*Ph + cP['Phik_t']*Pht + cP['Pk']*Pv + cP['Pk_t']*Pt
            alpha = -cT['Psik']/cT['Tk']; beta = -(cT['Pk']*Pv + cT['Pk_t']*Pt)/cT['Tk']
            return (srcv - other0 - cP['Tk']*beta)/(cP['Psik'] + cP['Tk']*alpha), cP
        return (srcv - (cP['Phik']*Ph + cP['Phik_t']*Pht))/cP['Psik'], cP
    out = {}
    for aa in aa_list:
        H = Hof(aa)
        def rhs_a(st):
            delta, dd, Ph, Pht, T, Tt, Pv, Pt = st; Ps, cP = psi_of(aa, st); ddd = -2*H*dd - kk**2*Ps/aa**2
            cF = coefs('Phi', aa); dcP = {v: c_*aa*H for v, c_ in coefs('Psi', aa, deriv=True).items()}; srcv = 6*Omat*H0**2*delta; dsrc = 6*Omat*H0**2*dd
            if not sector:
                known = dsrc - (cP['Phik']*Pht + dcP['Phik']*Ph + dcP['Phik_t']*Pht) - Ps*dcP['Psik']; A_ = -cP['Phik_t']/cP['Psik']; B_ = known/cP['Psik']
                X = -(cF['Phik_t']*Pht + cF['Phik']*Ph + cF['Psik']*Ps + cF['Psik_t']*B_)/(cF['Phik_tt'] + cF['Psik_t']*A_); return np.array([dd, ddd, Pht, X, 0, 0, 0, 0])
            cT = coefs('T', aa); cQ = coefs('P', aa); dcT = {v: c_*aa*H for v, c_ in coefs('T', aa, deriv=True).items()}
            Tq = -(cT['Psik']*Ps + cT['Pk']*Pv + cT['Pk_t']*Pt)/cT['Tk']
            r4 = -(dcT['Psik']*Ps + cT['Pk']*Pt + dcT['Pk']*Pv + dcT['Pk_t']*Pt + dcT['Tk']*Tq)/cT['Tk']
            r3 = dsrc - (cP['Phik']*Pht + dcP['Phik']*Ph + dcP['Phik_t']*Pht + dcP['Tk']*Tq + cP['Pk']*Pt + dcP['Pk']*Pv + dcP['Pk_t']*Pt) - Ps*dcP['Psik']
            A = np.zeros((4, 4)); b = np.zeros(4)
            A[0] = [cF['Phik_tt'], cF['Pk_tt'], cF['Psik_t'], cF['Tk_t']]; b[0] = -(cF['Phik_t']*Pht + cF['Phik']*Ph + cF['Tk']*Tq + cF['Pk_t']*Pt + cF['Pk']*Pv + cF['Psik']*Ps)
            A[1] = [cQ['Phik_tt'], cQ['Pk_tt'], cQ['Psik_t'], cQ['Tk_t']]; b[1] = -(cQ['Phik_t']*Pht + cQ['Phik']*Ph + cQ['Tk']*Tq + cQ['Pk_t']*Pt + cQ['Pk']*Pv + cQ['Psik']*Ps)
            A[2] = [cP['Phik_t'], cP['Pk_t'], cP['Psik'], cP['Tk'] + dcP['Tk_t']]; b[2] = r3
            A[3] = [0.0, cT['Pk_t']/cT['Tk'], cT['Psik']/cT['Tk'], 1.0]; b[3] = r4
            u = np.linalg.solve(A, b); return np.array([dd, ddd, Pht, u[0], 0.0, 0.0, Pt, u[1]])
        idx = [0, 1, 2, 3, 6, 7] if sector else [0, 1, 2, 3]; base = np.zeros(8); base[0] = 1.0; base[1] = H; base[2] = 6*Omat*H0**2/coefs('Psi', aa)['Phik']
        f0 = rhs_a(base); J = np.zeros((len(idx), len(idx)))
        for jj, ii in enumerate(idx):
            dq = np.zeros(8); dq[ii] = 1e-6*max(1.0, abs(base[ii])); J[:, jj] = (rhs_a(base + dq) - f0)[idx]/dq[ii]
        ev = np.linalg.eigvals(J); out[aa] = (ev.real.max()/H, abs(ev.imag).max()/H)
    return out
print("  W5: frozen-coefficient eigenvalues of the reduced system (max real part in units of H; max |Im|/H), k = 0.05/Mpc", flush=True)
c2star = 1e-5/(1 - 2e-5); K2abs = 2.5e5; eps0v = 3*H0**2*Od/(K2abs*1.0**2); EIG = {}
for lab, pars, sec in (("GR control", (0.0, 0.0, 0.0, 0.0, 1.0, 0.0), False), ("fast c2 = c2*", (0.2, c2star, 1e-5, -K2abs, 1.0, eps0v), True), ("rigid c2 = 1e-4", (0.2, 1e-4, 1e-5, -K2abs, 1.0, eps0v), True), ("rigid c2 = 0.05", (0.2, 0.05, 1e-5, -K2abs, 1.0, eps0v), True)):
    EIG[lab] = eigen(0.05, pars, sec); print(f"    {lab:16s}: " + "; ".join(f"a = {aa}: max Re = {v[0]:.3e} H, |Im| = {v[1]:.2e} H" for aa, v in EIG[lab].items()), flush=True)
rate2 = K2abs*1.0**2*eps0v/1e-5; print(f"    analytic tachyonic term of the clock equation from the condensate background: T'' = (|K_2| Q0^2 eps0 a^-3/c_14) T -> rate = {math.sqrt(rate2):.0f} H0 at a = 1, {math.sqrt(rate2*1e6):.1e} H0 at a = 0.01 (k-independent; vanishes on Minkowski where f34 checked health)", flush=True)
check("W5a [control] the GR system has no exponential mode faster than the growing mode (max Re < 1 H at every a)", all(v[0] < 1.0 for v in EIG["GR control"].values()), json.dumps({str(a_): round(v[0], 3) for a_, v in EIG['GR control'].items()}))
check("W5b [finding] with the sector on, every branch has a real exponential eigenvalue > 100 H at a = 0.01; the fast and c2 = 1e-4 branches keep one > 1e4 H at a = 0.3 while c2 = 0.05 is stabilised there by its k^4 term (reported)", all(EIG[l][0.01][0] > 100 for l in EIG if l != "GR control") and EIG["fast c2 = c2*"][0.3][0] > 1e4 and EIG["rigid c2 = 0.05"][0.3][0] < 1.0, json.dumps({l: {str(a_): f"{v[0]:.2e}" for a_, v in EIG[l].items()} for l in EIG}))
print(f"\n  caveats: reduced system (adiabatic clock, Phi dynamical, differentiated lapse constraint); the exponential modes may include the sector's genuine tachyonic clock mode (identified analytically above) and possibly a constraint-differentiation mode -- separating them needs a constraint-preserving formulation; the ODE scans of this script (full clock: NaN at the first step; adiabatic clock: exponential growth from a = 0.0102) are therefore not growth results.  total {time.time()-T0:.0f}s")
print(f"\nRESULT: {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else ""))
sys.exit(1 if FAILS else 0)
