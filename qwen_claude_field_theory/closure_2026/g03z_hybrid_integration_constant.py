#!/usr/bin/env python3
"""
g03z -- the hybrid: integration-constant dust of the projectable clock, stiffness from the MOND scalar   [WITHDRAWN 2026-09-06]
=======================================================================================================
WITHDRAWN before completion.  The integration-constant dust exists only when the lapse is projectable, N = N(t); with a projectable
lapse the clock's acceleration J_i = d_i(Psi - T') loses its Psi piece and vanishes identically in the static limit, so the coupling
2(2-K_B) J.dphi has no source and the action produces NO MOND force (the same door was proposed in gemini_38_flash_push/02 and refuted
in g04d, check E2).  What this script integrates -- a LOCAL lapse with c_14 = 0 and a dust added by hand as a violation of the local
constraint -- is not a consistent theory: the local lapse keeps the MOND source but forbids the free dust; projectability allows the dust
but removes the source.  A constrained (mimetic) clock, lambda (g^{mu nu} d tau d tau + 1), fails identically: a unit-gradient clock is
geodesic, J = 0 exactly.  The control (H1) ran and passed; the grid was not completed and no growth number from this script is a result.
Both condensate constructions failed (g03w: the MOND scalar's dust tilts the clock into a tachyon; g03x: the clock's own
condensate has c_s^2 proportional to its own density).  The hybrid keeps the field-set stiffness of the MOND scalar but takes the
dark matter from the clock sector's integration constant in the projectable limit c_14 -> 0 (Mukohyama's dust: the local lapse
equation holds only up to a dust term rho_C(x) a^-3 at rest in the clock frame), with the MOND scalar exactly at its minimum
(K' = 0: no tilt term).  PPN improves in that limit (alpha_1 = -4 c_14 -> 0, alpha_2 -> 0).

Linear theory on FLRW (Newtonian gauge, g03v's symbolic second-order expansion of clock + MOND scalar + Einstein-Hilbert with
c_14 = 0 and Qbar = Q0):
  * the clock's equation has no T'' (no inertia) and is algebraic:  T = (3 a^2/k^2)(H Psi + Phi') + ((2-K_B) a^2/(c_2 k^2))(P' - Q0 Psi + H P) + ...;
  * the integration-constant dust rides on the clock: delta_C' = 3 Phi' - k^2 T/a^2, so its infall is driven by the MOND scalar's
    kinetic variable dQ = P' - Q0 Psi at the k-independent rate -(2-K_B) dQ/c_2, the pure-khronon part being O((aH/k)^2);
  * the lapse equation carries the dust as a source (16 pi G a^3 rho_C delta_C) alongside the baryons: this is the violation of
    the local Hamiltonian constraint that defines the integration-constant dust;
  * the MOND scalar's equation (K_2 finite) is sourced by the clock's acceleration Psi - T' (g03t) -- the causal build-up.
Checks that can fail:
  H1 [control]     ordinary CDM in place of the integration-constant dust (T-independent dust: delta_C'' + 2H delta_C' = -k^2 Psi/a^2) with the
                   sector off reproduces LambdaCDM growth within 1% (Phi dynamical, the g03w builder);
  H2 [eigenmodes]  no exponential eigenvalue beyond the growing mode at a = 0.01, 0.3, 1 for the (c_2, |K_2|) grid, k = 0.2/Mpc;
  H3 [growth]      the integration-constant dust's growth from z = 100 relative to LambdaCDM at k = 0.05 and 0.2/Mpc for the grid
                   c_2 in {1e-5, 1e-4, 1e-3} x |K_2| in {2.5e5, 2.7e6}: reported; PASS if some point is within 20% at both k;
  H4 [reported]    the ratio T/T_CDM at z = 0 (does the dust fall?) and the scale dependence of the dust growth (k = 0.05 vs 0.2).
Units and background as in g03v; baryons Omega_b, dust Omega_d = 0.266; Q0 = H0 (free; the dust's rate scales with (2-K_B) Q0/c_2 through dQ).
"""
import sympy as sp, numpy as np, math, time, sys, json
from scipy.integrate import solve_ivp
T0 = time.time(); FAILS = []
def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
src = open("g03v_fast_clock_branch.py").read(); head = src[:src.index("SRC_SIGN = 1.0")]
head = head.replace("    out = out.subs(S('Qbar_t'), -3*Q0*eps0*adot/a**4).subs(S('Qbar'), Q0*(1 + eps0/a**3))", "    out = out.subs(S('Qbar_t'), 0).subs(S('Qbar'), Q0)")   # the MOND scalar at its minimum
g = {}; exec(compile(head, "g03z_head", "exec"), g)
COEF, VARS, Hof, addot_of, cH0_Mpc, Om, OL, Ob, Od, H0 = (g[nm] for nm in ("COEF", "VARS", "Hof", "addot_of", "cH0_Mpc", "Om", "OL", "Ob", "Od", "H0"))
Ek, S, k, a = g["Ek"], g["S"], g["k"], g["a"]
print(f"  symbolic sector ready ({time.time()-T0:.0f}s)", flush=True)
ET0 = sp.expand(Ek['T'].subs({g['c14']: 0}))
print(f"    projectable limit: coefficient of T'' in the clock equation = {sp.simplify(ET0.coeff(S('Tk_tt')))} (no inertia); leading-k coefficient of T = {sp.factor(sp.expand(ET0.coeff(S('Tk'))).coeff(k, 4))} k^4", flush=True)
def coefs_at(nm, kk, aa, pars):
    H = Hof(aa); args = (kk, aa, aa*H, addot_of(aa), *pars, 3*OL*H0**2); return {v: float(np.asarray(COEF[nm][v](*args), float)) for v in VARS}
def run(kMpc, pars, mode="hybrid", ai=0.01, af=1.0, eig_a=None):
    """mode 'hybrid': integration-constant dust on the clock; 'cdm': ordinary CDM in place of it with the sector off (control).
    State: delta_b, delta_b', delta_C, (delta_C' for cdm), Phi, Phi', P, P'.  Psi from the lapse constraint; T algebraic (c14 = 0)."""
    kk = kMpc*cH0_Mpc
    aa_grid = np.geomspace(ai, af, 4000); TT = np.concatenate([[0.0], np.cumsum(np.diff(aa_grid)/(0.5*(aa_grid[1:]*Hof(aa_grid[1:]) + aa_grid[:-1]*Hof(aa_grid[:-1]))))]); AA = aa_grid
    # coefficient tables on the grid (fast interpolation)
    tab = {}
    for nm in ('Psi', 'Phi', 'T', 'P'):
        M = np.zeros((len(VARS), len(AA)))
        for i, v in enumerate(VARS):
            H = Hof(AA); args = (kk, AA, AA*H, addot_of(AA), *pars, 3*OL*H0**2); M[i] = np.broadcast_to(np.asarray(COEF[nm][v](*args), float), AA.shape)
        tab[nm] = M; tab[nm + '_da'] = np.gradient(M, AA, axis=1)
    def C(nm, aa, deriv=False):
        j = min(max(int(np.searchsorted(AA, aa)) - 1, 0), len(AA) - 2); w = (aa - AA[j])/(AA[j + 1] - AA[j]); M = tab[nm + ('_da' if deriv else '')]; row = M[:, j]*(1 - w) + M[:, j + 1]*w
        return {v: float(row[i]) for i, v in enumerate(VARS)}
    def rhs_cdm(tt, st):
        aa = float(np.interp(tt, TT, AA)); H = Hof(aa); db, dbd, dc, dcd, Ph, Pht = st
        cP = C('Psi', aa); cF = C('Phi', aa)
        # sector off: GR lapse and Phi equations only (set the sector coefficients to zero by using pars with everything 0: done via pars)
        srcv = 6*H0**2*(Ob*db + Od*dc); Ps = (srcv - (cP['Phik']*Ph + cP['Phik_t']*Pht))/cP['Psik']
        dcP = {v: c_*aa*H for v, c_ in C('Psi', aa, True).items()}; dsrc = 6*H0**2*(Ob*dbd + Od*dcd)
        known = dsrc - (cP['Phik']*Pht + dcP['Phik']*Ph + dcP['Phik_t']*Pht) - Ps*dcP['Psik']; A_ = -cP['Phik_t']/cP['Psik']; B_ = known/cP['Psik']
        X = -(cF['Phik_t']*Pht + cF['Phik']*Ph + cF['Psik']*Ps + cF['Psik_t']*B_)/(cF['Phik_tt'] + cF['Psik_t']*A_)
        return [dbd, -2*H*dbd - kk**2*Ps/aa**2, dcd, -2*H*dcd - kk**2*Ps/aa**2, Pht, X]
    def T_of(aa, Ps, Pht, Pv, Pt, cT):
        return -(cT['Psik']*Ps + cT['Phik_t']*Pht + cT['Pk']*Pv + cT['Pk_t']*Pt)/cT['Tk']                 # the algebraic clock (Psi', Phi terms carry c14 = 0 or vanish)
    def psi_hybrid(aa, st):
        db, dbd, dc, Ph, Pht, Pv, Pt = st; cP = C('Psi', aa); cT = C('T', aa)
        # Psi appears in T: T = alpha Psi + beta; lapse: cP_Psi Psi + cP_T T + (cP_Tt T' dropped: its coefficient is c14-free? keep T' via the derivative below at next order) + ... = src
        alpha = -cT['Psik']/cT['Tk']; beta = -(cT['Phik_t']*Pht + cT['Pk']*Pv + cT['Pk_t']*Pt)/cT['Tk']
        srcv = 6*H0**2*(Ob*db + Od*dc); other = cP['Phik']*Ph + cP['Phik_t']*Pht + cP['Pk']*Pv + cP['Pk_t']*Pt
        Ps = (srcv - other - cP['Tk']*beta)/(cP['Psik'] + cP['Tk']*alpha)
        return Ps, alpha*Ps + beta, cP, cT
    def rhs_hybrid(tt, st):
        aa = float(np.interp(tt, TT, AA)); H = Hof(aa); db, dbd, dc, Ph, Pht, Pv, Pt = st
        Ps, T, cP, cT = psi_hybrid(aa, st); cF = C('Phi', aa); cQ = C('P', aa)
        dcP = {v: c_*aa*H for v, c_ in C('Psi', aa, True).items()}; dcT = {v: c_*aa*H for v, c_ in C('T', aa, True).items()}
        # unknowns u = (Phi'', P'', Psi', T'): (1) Phi eq, (2) P eq, (3) differentiated lapse constraint, (4) differentiated clock relation
        # (4): T' = -[cT_Psi Psi' + dcT_Psi Psi + cT_Phit Phi'' + dcT_Phit Phi' + cT_P P' + dcT_P P + cT_Pt P'' + dcT_Pt P' + dcT_T T]/cT_T
        r4 = -(dcT['Psik']*Ps + dcT['Phik_t']*Pht + cT['Pk']*Pt + dcT['Pk']*Pv + dcT['Pk_t']*Pt + dcT['Tk']*T)/cT['Tk']
        dcd = 3*Pht - kk**2*T/aa**2                                                                       # integration-constant dust: continuity on the clock's velocity
        dsrc = 6*H0**2*(Ob*dbd + Od*dcd)
        # (3): cP_Psi Psi' + cP_Phit Phi'' + cP_Tt T' + cP_Pt P'' = dsrc - [cP_Phi Phi' + dcP_Phi Phi + dcP_Phit Phi' + cP_T T' (in unknowns) + dcP_T T + dcP_Tt T' ... + cP_P P' + dcP_P P + dcP_Pt P'] - Psi dcP_Psi
        r3 = dsrc - (cP['Phik']*Pht + dcP['Phik']*Ph + dcP['Phik_t']*Pht + dcP['Tk']*T + cP['Pk']*Pt + dcP['Pk']*Pv + dcP['Pk_t']*Pt) - Ps*dcP['Psik']
        A = np.zeros((4, 4)); b = np.zeros(4)
        A[0] = [cF['Phik_tt'], cF['Pk_tt'], cF['Psik_t'], cF['Tk_t']]; b[0] = -(cF['Phik_t']*Pht + cF['Phik']*Ph + cF['Tk']*T + cF['Pk_t']*Pt + cF['Pk']*Pv + cF['Psik']*Ps)
        A[1] = [cQ['Phik_tt'], cQ['Pk_tt'], cQ['Psik_t'], cQ['Tk_t']]; b[1] = -(cQ['Phik_t']*Pht + cQ['Phik']*Ph + cQ['Tk']*T + cQ['Pk_t']*Pt + cQ['Pk']*Pv + cQ['Psik']*Ps)
        A[2] = [cP['Phik_t'], cP['Pk_t'], cP['Psik'], cP['Tk'] + dcP['Tk_t']]; b[2] = r3
        A[3] = [cT['Phik_t']/cT['Tk'], cT['Pk_t']/cT['Tk'], cT['Psik']/cT['Tk'], 1.0]; b[3] = r4
        u = np.linalg.solve(A, b)
        return [dbd, -2*H*dbd - kk**2*Ps/aa**2, dcd, Pht, u[0], Pt, u[1]]
    Hi = Hof(ai)
    if mode == "cdm":
        st0 = [1.0, Hi, 1.0, Hi, 0.0, 0.0]; cP0 = C('Psi', ai); st0[4] = 6*H0**2*(Ob + Od)/cP0['Phik']
        if eig_a is not None:
            out = {}
            for aa_ in eig_a:
                tt_ = float(np.interp(aa_, AA, TT)); base = np.array(st0, float); f0 = np.array(rhs_cdm(tt_, base)); J = np.zeros((6, 6))
                for ii in range(6):
                    dq = np.zeros(6); dq[ii] = 1e-6*max(1.0, abs(base[ii])); J[:, ii] = (np.array(rhs_cdm(tt_, base + dq)) - f0)/dq[ii]
                ev = np.linalg.eigvals(J); out[aa_] = float(ev.real.max()/Hof(aa_))
            return out
        sol = solve_ivp(rhs_cdm, [0, TT[-1]], st0, method='LSODA', rtol=1e-8, atol=1e-14, max_step=TT[-1]/400)
        return dict(db=sol.y[0, -1], dc=sol.y[2, -1], ok=sol.success and bool(np.all(np.isfinite(sol.y))))
    st0 = [1.0, Hi, 1.0, 0.0, 0.0, 0.0, 0.0]; cP0 = C('Psi', ai); st0[3] = 6*H0**2*(Ob + Od)/cP0['Phik']
    if eig_a is not None:
        out = {}
        for aa_ in eig_a:
            tt_ = float(np.interp(aa_, AA, TT)); base = np.array(st0, float); f0 = np.array(rhs_hybrid(tt_, base)); J = np.zeros((7, 7))
            for ii in range(7):
                dq = np.zeros(7); dq[ii] = 1e-6*max(1.0, abs(base[ii])); J[:, ii] = (np.array(rhs_hybrid(tt_, base + dq)) - f0)/dq[ii]
            ev = np.linalg.eigvals(J); out[aa_] = float(ev.real.max()/Hof(aa_))
        return out
    sol = solve_ivp(rhs_hybrid, [0, TT[-1]], st0, method='LSODA', rtol=1e-8, atol=1e-14, max_step=TT[-1]/400)
    st = sol.y[:, -1]; Ps, T, _, _ = psi_hybrid(af, st)
    return dict(db=st[0], dc=st[2], ok=sol.success and bool(np.all(np.isfinite(sol.y))), T=T, Psi=Ps, P=st[5], Pt=st[6])
def growth_lcdm(ai=0.01):
    aa = np.linspace(1e-4, 1.0, 40000); Ez = np.sqrt(Om*aa**-3 + OL)
    def D(av): m = aa <= av; return 2.5*Om*np.sqrt(Om*av**-3 + OL)*np.trapz(1/(aa[m]*Ez[m])**3, aa[m])
    return D(1.0)/D(ai)
DL = growth_lcdm(); kt = [0.05, 0.2]
zero = (0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
ctrl = [run(kk_, zero, mode="cdm") for kk_ in kt]
print(f"    H1 control (CDM in place of the dust, sector off, Phi dynamical): growth/LCDM baryons {[round(o['db']/DL, 4) for o in ctrl]}, dust {[round(o['dc']/DL, 4) for o in ctrl]}  ({time.time()-T0:.0f}s)", flush=True)
check("H1 [control] ordinary CDM with the sector off reproduces LambdaCDM growth within 1% at k = 0.05 and 0.2/Mpc", all(abs(o['db']/DL - 1) < 0.01 and abs(o['dc']/DL - 1) < 0.01 for o in ctrl))
GRID = [(c2v, K2v) for c2v in (1e-5, 1e-4, 1e-3) for K2v in (2.5e5, 2.7e6)]; EIG = {}; RES = {}
print("    H2 eigenmodes (max Re/H at a = 0.01, 0.3, 1; k = 0.2/Mpc) and H3 growth/LCDM (baryons, dust) at k = 0.05, 0.2 for the (c_2, |K_2|) grid, Q0 = H0, K_B = 0.2:", flush=True)
for c2v, K2v in GRID:
    pars = (0.2, c2v, 0.0, -K2v, 1.0, 0.0)
    EIG[(c2v, K2v)] = run(0.2, pars, eig_a=(0.01, 0.3, 1.0))
    row = []
    for kk_ in kt:
        o = run(kk_, pars); row.append((o['db']/DL if o['ok'] else float('nan'), o['dc']/DL if o['ok'] else float('nan'), o['T'], o['Psi']))
    RES[(c2v, K2v)] = row
    print(f"    c2 = {c2v:.0e}, |K2| = {K2v:.1e}: eig {json.dumps({str(a_): round(v, 3) for a_, v in EIG[(c2v, K2v)].items()})}; growth (b, dust) k=0.05: ({row[0][0]:.3f}, {row[0][1]:.3f}), k=0.2: ({row[1][0]:.3f}, {row[1][1]:.3f}); T/Psi(z=0,k=0.2) = {row[1][2]/row[1][3] if row[1][3] else float('nan'):.3e}  ({time.time()-T0:.0f}s)", flush=True)
check("H2 [eigenmodes] no exponential eigenvalue beyond the growing mode (max Re < 1 H) at a = 0.01, 0.3, 1 for every grid point, k = 0.2/Mpc", all(v < 1.0 for e_ in EIG.values() for v in e_.values()), json.dumps({f"{c2v:.0e}|{K2v:.1e}": {str(a_): round(v, 2) for a_, v in e_.items()} for (c2v, K2v), e_ in EIG.items()}))
ok3 = {key: all(np.isfinite(r[1]) and abs(r[1] - 1) < 0.2 for r in RES[key]) for key in RES}
check("H3 [growth] some (c_2, |K_2|) gives the integration-constant dust's growth within 20% of LambdaCDM at both k = 0.05 and 0.2/Mpc", any(ok3.values()), json.dumps({f"{c2v:.0e}|{K2v:.1e}": [round(r[1], 3) if np.isfinite(r[1]) else None for r in RES[(c2v, K2v)]] for c2v, K2v in GRID}))
print(f"\n  caveats: linear theory only (the nonlinear MOND response and the caustic question of the integration-constant dust are not addressed); c_14 = 0 exactly (projectable limit; the non-projectable corrections are O(c14 k^2 T''), dropped); the differentiated lapse constraint scheme of g03w; Q0 = H0 and K_B = 0.2 fixed; the dust is at rest in the clock frame by construction.  total {time.time()-T0:.0f}s")
print(f"\nRESULT: {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else ""))
sys.exit(1 if FAILS else 0)
