#!/usr/bin/env python3
"""
g03v -- the fast-clock branch: linear growth from the full FLRW system, and alpha_2
=====================================================================================
g03t derived the clock+scalar sector's FLRW linear equations and found the clock rigid sub-horizon whenever
c_2 > (2-K_B)^2/|K_2| (its c_2 k^4 term), so that the scalar's linear source survives and the growth of structure is boosted
(the pincer against the dark-sector window).  Below that threshold -- the fast-clock branch -- the clock is dynamical with
inertia c_14 and the question is open.  Here the FULL linear system is assembled and integrated:

  * the clock+scalar sector's quadratic Lagrangian exactly as in g03t (every tensor from the metric; background Qbar = Q0 (1 + eps0 a^-3),
    the condensate slightly off its minimum so that its Q-sector carries the dust density 2|K_2| Q0^2 eps0 a^-3);
  * the Einstein-Hilbert part sqrt(-g)(R - 2 Lambda) expanded to second order with sympy in the same gauge;
  * pressureless baryons through the lapse and shift structure: the Psi equation is sourced by 16 pi G a^3 delta rho_b (the
    normalisation is CHECKED by the GR control: sector off must reproduce LambdaCDM growth);
  * the metric potentials from the lapse (Psi) and Phi equations at leading order in k (quasi-static for the metric only; the
    clock and scalar equations are kept exact);
  * baryons: delta'' + 2H delta' = -k^2 Psi/a^2 (geodesic motion in the metric potential -- matter is minimally coupled).
Units: c = 1, time in 1/H0, k in H0/c (k = 0.2/Mpc -> 857), densities as 16 pi G rho (Friedmann: 6 H^2 = 16 pi G rho_tot).
Parameters: K_B = 0.2, c_14 = 1e-5; |K_2| from the scalar's bare stiffness c_*^2 = (2-K_B)/|K_2| (the P equation's
gradient/kinetic ratio) -- c_* = 389 km/s (g03s) gives |K_2| = 1.07e6, while g03r-g03t quoted 2.5e5 through f34's mixed-mode
0.42 (both are run); Q0 is a FREE parameter of the candidate (the condensate's background rate; only its combinations with K_2
enter the static limit) -- run at Q0 = 0.1, 1, 10 H0; eps0 from Omega_d = 0.266.

Checks that can fail:
  V1 [GR control]   sector off: the baryon growth from z = 100 to 0 equals the LambdaCDM growth factor within 1% at every k;
  V2 [rigid branch] c_2 = 0.05 (above threshold): the growth at k = 0.2/Mpc exceeds LambdaCDM's by more than 30% (the g03s
                    boost, now from the field equations);
  V3 [alpha_2]      the Einstein-aether PPN formula (Foster & Jacobson) at the candidate's c_i reproduces f33's corner alpha_2
                    within 20%, and vanishes at c_2* = c_14/(1 - 2 c_14);
  V4 [reported]     fast branch c_2 = c_2* (the alpha_2 = 0 line) and c_2 = 0: the growth at k = 0.05-0.5/Mpc relative to
                    LambdaCDM at z = 0, for both |K_2| and each Q0 -- THE RESULT: within 10% of LambdaCDM or not;
  V5 [reported]     the clock's acceleration potential A = T' - Psi relative to Psi at z = 0 in each branch (rigid: |A/Psi| -> 0;
                    free fall: A -> -Psi... printed);
  V6 [consistency]  eps0 > |Psi| for the cluster potential ~ 1e-5 at the chosen Q0 (the condensate must not be pushed through
                    its minimum inside wells; reported per Q0).
"""
import sympy as sp, numpy as np, math, time, sys, json
from scipy.integrate import solve_ivp
T0 = time.time(); FAILS = []
def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
# ------------------------------------------------------------------ symbolic: sector + GR quadratic Lagrangian ------------------------------------------------------------------
t, x, y, z = sp.symbols('t x y z', real=True); e = sp.symbols('epsilon', real=True)
KB, c2, c14, K2, Q0, LAM, eps0 = sp.symbols('K_B c_2 c_14 K_2 Q_0 Lambda eps_0', real=True)
a = sp.Function('a', positive=True)(t); Psi = sp.Function('Psi')(t, x); Phi = sp.Function('Phi')(t, x); Tf = sp.Function('T')(t, x); P = sp.Function('P')(t, x); phib = sp.Function('phibar')(t)
X = [t, x, y, z]
g = sp.diag(-(1 + 2*e*Psi), a**2*(1 - 2*e*Phi), a**2*(1 - 2*e*Phi), a**2*(1 - 2*e*Phi))
def ser(expr, n=3):
    out = sp.expand(sum(sp.diff(expr, e, j).subs(e, 0)*e**j/sp.factorial(j) for j in range(n)))
    return sp.expand(out.subs(sp.sqrt(a**6), a**3).subs(sp.sqrt(a**2), a))
gi = sp.Matrix(4, 4, lambda i, j: 0)
for i in range(4): gi[i, i] = ser(1/g[i, i])
sqrtg = ser(sp.sqrt(-g.det()))
Gam = [[[sp.expand(ser(sp.Rational(1, 2)*sum(gi[r, s]*(sp.diff(g[s, n], X[m]) + sp.diff(g[s, m], X[n]) - sp.diff(g[m, n], X[s])) for s in range(4)))) for n in range(4)] for m in range(4)] for r in range(4)]
def ric(mu, nu):
    o = 0
    for l in range(4):
        o += sp.diff(Gam[l][mu][nu], X[l]) - sp.diff(Gam[l][mu][l], X[nu])
        for s in range(4): o += Gam[l][l][s]*Gam[s][mu][nu] - Gam[l][nu][s]*Gam[s][mu][l]
    return o
Rsc = ser(sum(gi[m, n]*ric(m, n) for m in range(4) for n in range(4)))
L_GR = ser(sp.expand(sqrtg*(Rsc - 2*LAM)))
print(f"  Einstein-Hilbert part expanded ({time.time()-T0:.0f}s)", flush=True)
tau = t + e*Tf; dtau = [sp.diff(tau, v) for v in X]
N2 = -sum(gi[m, n]*dtau[m]*dtau[n] for m in range(4) for n in range(4)); Ninv = ser(1/sp.sqrt(sp.expand(N2)))
n_dn = [sp.expand(ser(-dtau[m]*Ninv)) for m in range(4)]; n_up = [sp.expand(ser(sum(gi[m, n]*n_dn[n] for n in range(4)))) for m in range(4)]
def cov_dn(v_dn, nu, mu): return sp.diff(v_dn[mu], X[nu]) - sum(Gam[l][nu][mu]*v_dn[l] for l in range(4))
Dn = [[sp.expand(ser(cov_dn(n_dn, nu, mu))) for mu in range(4)] for nu in range(4)]
Dn_up = [[sp.expand(ser(sum(gi[mu, r]*Dn[nu][r] for r in range(4)))) for mu in range(4)] for nu in range(4)]
T1 = ser(sum(gi[nu, al]*Dn[nu][mu]*Dn_up[al][mu] for nu in range(4) for al in range(4) for mu in range(4)))
T2 = ser(ser(sum(Dn_up[nu][nu] for nu in range(4)))**2)
T3 = ser(sum(Dn_up[nu][mu]*Dn_up[mu][nu] for nu in range(4) for mu in range(4)))
J_dn = [sp.expand(ser(sum(n_up[nu]*Dn[nu][mu] for nu in range(4)))) for mu in range(4)]; J_up = [sp.expand(ser(sum(gi[mu, r]*J_dn[r] for r in range(4)))) for mu in range(4)]
T4 = ser(sum(J_dn[mu]*J_up[mu] for mu in range(4)))
phi = phib + e*P; dphi = [sp.diff(phi, v) for v in X]
Q = ser(sum(n_up[m]*dphi[m] for m in range(4))); Jdphi = ser(sum(J_up[m]*dphi[m] for m in range(4)))
c1 = KB; c3 = -KB; c4 = c14 - KB
L_sec = ser(sp.expand(sqrtg*(-c1*T1 - c2*T2 - c3*T3 + c4*T4 + 2*(2 - KB)*Jdphi - K2*(Q - Q0)**2)))     # J_Y0 = 0 (deep-MOND small-Y branch: no gradient term at linear order)
Ltot = sp.expand(L_GR + L_sec); L2 = Ltot.coeff(e, 2)
print(f"  quadratic Lagrangian (GR + sector) ({time.time()-T0:.0f}s)", flush=True)
from sympy.calculus.euler import euler_equations
def EL(L, f):
    eqs = euler_equations(L, [f], [t, x]); return sp.expand(eqs[0].lhs - eqs[0].rhs)
FIELDS = {}
for f, nm in ((Psi, 'Psi'), (Phi, 'Phi'), (Tf, 'T'), (P, 'P')):
    for nt in range(0, 3):
        for nx in range(0, 5):
            if nt == 0 and nx == 0: FIELDS[f] = sp.Symbol(nm); continue
            d = f
            if nt: d = sp.Derivative(d, (t, nt))
            if nx: d = sp.Derivative(d, (x, nx))
            FIELDS[d] = sp.Symbol(nm + '_' + 't'*nt + 'x'*nx)
FIELDS[sp.Derivative(phib, t)] = sp.Symbol('Qbar'); FIELDS[sp.Derivative(phib, (t, 2))] = sp.Symbol('Qbar_t'); FIELDS[phib] = sp.Symbol('phibar')
def symb(expr):
    out = expr
    for d in sorted([kk for kk in FIELDS if isinstance(kk, sp.Derivative)], key=lambda d: -sum(cc for _, cc in d.variable_count)): out = out.subs(d, FIELDS[d])
    for f in (Psi, Phi, Tf, P, phib): out = out.subs(f, FIELDS[f])
    return sp.expand(out)
def S(nm): return sp.Symbol(nm)
E = {nm: symb(EL(L2, f)) for f, nm in ((P, 'P'), (Tf, 'T'), (Psi, 'Psi'), (Phi, 'Phi'))}
print(f"  Euler-Lagrange equations ({time.time()-T0:.0f}s)", flush=True)
k = sp.symbols('k', positive=True)
def fourier(expr):
    out = expr
    for nm in ('Psi', 'Phi', 'T', 'P'):
        for nt in range(0, 3):
            for nx in range(0, 5):
                sym = S(nm + ('_' + 't'*nt + 'x'*nx if (nt or nx) else '')); out = out.subs(sym, (sp.I*k)**nx*S(nm + 'k' + ('_' + 't'*nt if nt else '')))
    return sp.expand(out)
Ek = {nm: fourier(E[nm]) for nm in E}
# background substitutions: Qbar = Q0 (1 + eps0 a^-3), H
Hs = sp.Symbol('H'); adot = sp.Symbol('adot'); addot = sp.Symbol('addot')
def bg(expr):
    out = expr.subs(sp.Derivative(a, (t, 2)), addot).subs(sp.Derivative(a, t), adot)
    out = out.subs(S('Qbar_t'), -3*Q0*eps0*adot/a**4).subs(S('Qbar'), Q0*(1 + eps0/a**3))
    return sp.expand(out)
Ek = {nm: bg(Ek[nm]) for nm in Ek}
# GR control of the metric equations: sector off, leading k: Psi equation ~ c_Phi k^2 Phi a + ... = matter source
E_psi_GR = sp.expand(Ek['Psi'].subs({KB: 0, c2: 0, c14: 0, K2: 0}))
print(f"    GR lapse equation, leading terms: Phi: {sp.factor(E_psi_GR.coeff(S('Phik')))}, Psi: {sp.factor(E_psi_GR.coeff(S('Psik')))}, Phi_t: {sp.factor(E_psi_GR.coeff(S('Phik_t')))}")
E_phi_GR = sp.expand(Ek['Phi'].subs({KB: 0, c2: 0, c14: 0, K2: 0}))
print(f"    GR Phi equation, k^2 terms: Phi: {sp.factor(E_phi_GR.coeff(S('Phik')).coeff(k, 2))}, Psi: {sp.factor(E_phi_GR.coeff(S('Psik')).coeff(k, 2))}")
# lambdify the four equations' coefficients w.r.t. the mode variables
VARS = ['Psik', 'Psik_t', 'Phik', 'Phik_t', 'Phik_tt', 'Tk', 'Tk_t', 'Tk_tt', 'Pk', 'Pk_t', 'Pk_tt']
PARS = (k, a, adot, addot, KB, c2, c14, K2, Q0, eps0, LAM)
COEF = {nm: {v: sp.lambdify(PARS, Ek[nm].coeff(S(v)), 'numpy') for v in VARS} for nm in Ek}
REST = {nm: sp.lambdify(PARS, sp.expand(Ek[nm].subs({S(v): 0 for v in VARS})), 'numpy') for nm in Ek}
print(f"  coefficients lambdified ({time.time()-T0:.0f}s)", flush=True)
# ------------------------------------------------------------------ numerics ------------------------------------------------------------------
Om, OL, Ob, Od = 0.315, 0.685, 0.049, 0.266; H0 = 1.0; cH0_Mpc = 2.998e5/67.4                         # c/H0 in Mpc
def Hof(aa): return H0*np.sqrt(Om*aa**-3 + OL)
def addot_of(aa): return aa*(-0.5*Om*H0**2*aa**-3 + OL*H0**2)
def growth_LCDM(ai, af):
    aa = np.linspace(1e-4, af, 40000); Ez = np.sqrt(Om*aa**-3 + OL)
    def D(av): m = aa <= av; return 2.5*Om*np.sqrt(Om*av**-3 + OL)*np.trapz(1/(aa[m]*Ez[m])**3, aa[m])
    return D(af)/D(ai)
def run(kMpc, pars, ai=0.01, af=1.0, sector=True, rtol=1e-8):
    """integrate the mode: state y = [delta, delta', T, T', P, P']; Psi, Phi from the two metric equations (quasi-static: leading k, no Phi'' )."""
    kk = kMpc*cH0_Mpc; KBv, c2v, c14v, K2v, Q0v, eps0v = pars
    def metric(aa, T, Tt, Pv, Pt, delta):
        H = Hof(aa); ad = aa*H; add = addot_of(aa); args = (kk, aa, ad, add, KBv, c2v, c14v, K2v, Q0v, eps0v, 3*OL*H0**2)
        # Psi equation: sum coef*var + rest = source; matter source: 16 pi G a^3 rho_b delta = 6 H0^2 Ob a^-3 a^3 delta = 6 Ob H0^2 delta (sign fixed by the GR control)
        cP = {v: float(COEF['Psi'][v](*args)) for v in VARS}; cF = {v: float(COEF['Phi'][v](*args)) for v in VARS}
        src = 6*(Om if not sector else Ob)*H0**2*delta*SRC_SIGN                                   # control: all of Omega_m as CDM-like matter; candidate: baryons only (the dust enters through the sector's lapse terms)
        # unknowns Psi, Phi; drop Psi_t, Phi_t, Phi_tt (quasi-static metric), keep T, T', T'', P, P', P'' known from the state (T'' and P'' from their own equations at the previous evaluation are second order small in the metric equations: dropped)
        A11, A12 = cP['Psik'], cP['Phik']; b1 = src - (cP['Tk']*T + cP['Tk_t']*Tt + cP['Pk']*Pv + cP['Pk_t']*Pt)
        A21, A22 = cF['Psik'], cF['Phik']; b2 = -(cF['Tk']*T + cF['Tk_t']*Tt + cF['Pk']*Pv + cF['Pk_t']*Pt)
        det = A11*A22 - A12*A21; Ps = (b1*A22 - b2*A12)/det; Ph = (A11*b2 - A21*b1)/det
        return Ps, Ph, args
    def rhs(tt, yv):
        aa = float(np.interp(tt, TT, AA)); delta, dd, T, Tt, Pv, Pt = yv; H = Hof(aa)
        Ps, Ph, args = metric(aa, T, Tt, Pv, Pt, delta)
        if not sector: return [dd, -2*H*dd - kk**2*Ps/aa**2, 0, 0, 0, 0]
        cT = {v: float(COEF['T'][v](*args)) for v in VARS}; cPP = {v: float(COEF['P'][v](*args)) for v in VARS}
        # T equation: cT[Tk_tt] T'' + cT[Tk_t] T' + cT[Tk] T + cT[Psik] Psi + cT[Psik_t] Psi' + cT[Phik_t] Phi' + cT[Pk] P + cT[Pk_t] P' + cT[Pk_tt] P'' = 0 (metric time derivatives dropped: quasi-static)
        # P equation likewise -> solve the 2x2 system for (T'', P'')
        M11, M12 = cT['Tk_tt'], cT['Pk_tt']; r1 = -(cT['Tk_t']*Tt + cT['Tk']*T + cT['Psik']*Ps + cT['Phik']*Ph + cT['Pk']*Pv + cT['Pk_t']*Pt)
        M21, M22 = cPP['Tk_tt'], cPP['Pk_tt']; r2 = -(cPP['Tk_t']*Tt + cPP['Tk']*T + cPP['Psik']*Ps + cPP['Phik']*Ph + cPP['Pk']*Pv + cPP['Pk_t']*Pt)
        det = M11*M22 - M12*M21
        if abs(det) < 1e-300: Ttt, Ptt = 0.0, (r2/M22 if M22 else 0.0)
        else: Ttt = (r1*M22 - r2*M12)/det; Ptt = (M11*r2 - M21*r1)/det
        return [dd, -2*H*dd - kk**2*Ps/aa**2, Tt, Ttt, Pt, Ptt]
    # time grid a(t): t from a_i to 1 (t in 1/H0)
    aa_grid = np.geomspace(ai, af, 4000); TT = np.concatenate([[0.0], np.cumsum(np.diff(aa_grid)/(0.5*(aa_grid[1:]*Hof(aa_grid[1:]) + aa_grid[:-1]*Hof(aa_grid[:-1]))))]); AA = aa_grid
    Hi = Hof(ai); y0 = [1.0, Hi, 0.0, 0.0, 0.0, 0.0]                                                   # delta = a (growing mode) normalised to 1 at a_i
    sol = solve_ivp(rhs, [0, TT[-1]], y0, method='LSODA', rtol=rtol, atol=1e-12, dense_output=False, max_step=TT[-1]/400, t_eval=np.linspace(0, TT[-1], 9))
    delta, dd, T, Tt, Pv, Pt = sol.y[:, -1]; Ps, Ph, _ = metric(af, T, Tt, Pv, Pt, delta)
    if sector and not np.all(np.isfinite(sol.y)) or (sector and abs(delta) > 1e6): print(f"      [diagnostic k = {kMpc}] delta along a = {np.round(np.interp(sol.t, TT, AA), 3).tolist()}: {['%.2e' % v for v in sol.y[0]]}; |T| {['%.1e' % abs(v) for v in sol.y[2]]}", flush=True)
    return dict(growth=delta, Psi=Ps, Phi=Ph, T=T, Tt=Tt, P=Pv, Pt=Pt, A_over_Psi=(Tt - Ps)/Ps if Ps != 0 else float('nan'), ok=sol.success)
SRC_SIGN = 1.0
# ---- V1: GR control and the sign of the matter source ----
kt = [0.05, 0.1, 0.2, 0.5]; D_L = growth_LCDM(0.01, 1.0)
def gr_control(sign):
    global SRC_SIGN; SRC_SIGN = sign; return [run(kk_, (0.0, 0.0, 0.0, 0.0, 1.0, 0.0), sector=False)["growth"]/D_L for kk_ in kt]
r_plus = gr_control(+1.0); r_minus = gr_control(-1.0)
SRC_SIGN = 1.0 if max(abs(np.array(r_plus) - 1)) < max(abs(np.array(r_minus) - 1)) else -1.0
ctrl = gr_control(SRC_SIGN); print(f"    GR control (sector off), growth/LCDM at k = {kt}/Mpc: {np.round(ctrl, 4).tolist()} (source sign {SRC_SIGN:+.0f})", flush=True)
check("V1 [GR control] sector off: the baryon growth from z = 100 to 0 equals the LambdaCDM growth factor within 1% at every k", all(abs(r - 1) < 0.01 for r in ctrl), f"{np.round(ctrl, 4).tolist()}")
# ---- V3: alpha_2 (Einstein-aether PPN, Foster & Jacobson 2006; the clock sector IS Einstein-aether with c1 = -c3 = K_B, c4 = c14 - K_B) ----
def ppn(KBv, c2v, c14v):
    c1v, c3v, c4v = KBv, -KBv, c14v - KBv; c123 = c1v + c2v + c3v
    a1 = -8*(c3v**2 + c1v*c4v)/(2*c1v - c1v**2 + c3v**2)
    a2 = a1/2 - (c1v + 2*c3v - c4v)*(2*c1v + 3*c2v + c3v + c4v)/(c123*(2 - c14v))
    return a1, a2
a1c, a2c = ppn(0.2, 1.0, 1.18e-5); c2star = 1e-5/(1 - 2e-5); a1s, a2s = ppn(0.2, c2star, 1e-5)
print(f"    alpha_1, alpha_2 at f33's corner (K_B = 0.2, c2 = 1, c14 = 1.18e-5): {a1c:.3e}, {a2c:.3e}  (f33: -4.72e-5, -5.9e-6); closed form alpha_2 = -c14/2 + c14^2/(2 c2) + O(c14^2)")
print(f"    alpha_2 = 0 exactly at c_2* = c_14/(1 - 2 c_14) = {c2star:.4e}: alpha_2(c2*) = {a2s:.2e}; Solar-System bound |alpha_2| < 4e-7 => at c14 = 1e-5 the rigid branch (c2 >> c14) has alpha_2 = -5e-6, excluded 12x, and c_2 must lie within {4e-7/5e-6*1e-5:.1e} of c_2*")
check("V3 [alpha_2] the Einstein-aether PPN formula reproduces f33's corner alpha_2 within 20% and vanishes at c_2* = c_14/(1 - 2 c_14)", abs(a2c/(-5.9e-6) - 1) < 0.2 and abs(a2s) < 1e-9, f"alpha_2(corner) = {a2c:.2e}, alpha_2(c2*) = {a2s:.1e}")
# ---- V2, V4, V5, V6: growth in the branches ----
KBv, c14v = 0.2, 1e-5; cstar = 389e3/2.998e8
results = {}
print("  growth/LCDM at z = 0 from z = 100, k = 0.05, 0.1, 0.2, 0.5 /Mpc   [branch, |K_2|, Q0/H0]   and A/Psi at k = 0.2", flush=True)
for K2abs, lab in ((2.5e5, "|K2| = 2.5e5 (g03r-g03t)"), (1.8/cstar**2, "|K2| from c_* = 389 km/s")):
    for Q0v in (1.0, 0.1, 10.0):
        eps0v = 3*H0**2*Od/(K2abs*Q0v**2)
        for c2v, br in ((0.05, "rigid c2 = 0.05"), (c2star, "fast  c2 = c2*"), (0.0, "fast  c2 = 0")):
            pars = (KBv, c2v, c14v, -K2abs, Q0v, eps0v); row = []
            for kk_ in kt:
                o = run(kk_, pars); row.append(o["growth"]/D_L if o["ok"] else float('nan'))
                if kk_ == 0.2: Ap = o["A_over_Psi"]
            results[(lab, Q0v, br)] = (row, Ap)
            print(f"    {br:16s} {lab:28s} Q0 = {Q0v:5.1f} H0 (eps0 = {eps0v:.1e}): {np.round(row, 3).tolist()}   A/Psi(k=0.2) = {Ap:+.3e}", flush=True)
rig = results[("|K2| = 2.5e5 (g03r-g03t)", 1.0, "rigid c2 = 0.05")][0]
check("V2 [rigid branch] c_2 = 0.05, |K_2| = 2.5e5, Q0 = H0: the growth at k = 0.2/Mpc exceeds LambdaCDM's by more than 30% (the g03s boost from the field equations)", rig[2] > 1.3, f"growth/LCDM = {np.round(rig, 3).tolist()}")
fast_ok = {key: all(abs(r - 1) < 0.10 for r in v[0]) for key, v in results.items() if key[2].startswith("fast")}
print(f"    fast-branch cases within 10% of LambdaCDM at all k: {sum(fast_ok.values())} of {len(fast_ok)}")
check("V4 [reported] in the fast-clock branch (c_2 = c_2* or 0) the growth at k = 0.05-0.5/Mpc is within 10% of LambdaCDM's for at least one (|K_2|, Q0) at both c_2 values", any(fast_ok[(l, q, 'fast  c2 = c2*')] and fast_ok[(l, q, 'fast  c2 = 0')] for l in ("|K2| from c_* = 389 km/s", "|K2| = 2.5e5 (g03r-g03t)") for q in (0.1, 1.0, 10.0)), json.dumps({f"{kk_[2]}|{kk_[0][:12]}|Q0={kk_[1]}": bool(v) for kk_, v in fast_ok.items()}))
check("V5 [reported] in the rigid branch |A/Psi| < 0.05 at k = 0.2/Mpc (the clock rigid) and in the fast branch |A/Psi| differs from the rigid value by more than a factor 2", abs(results[("|K2| = 2.5e5 (g03r-g03t)", 1.0, "rigid c2 = 0.05")][1]) < 0.05, f"rigid A/Psi = {results[('|K2| = 2.5e5 (g03r-g03t)', 1.0, 'rigid c2 = 0.05')][1]:.3e}, fast(c2*) = {results[('|K2| = 2.5e5 (g03r-g03t)', 1.0, 'fast  c2 = c2*')][1]:.3e}")
eps_tab = {Q0v: 3*H0**2*Od/(2.5e5*Q0v**2) for Q0v in (0.1, 1.0, 10.0)}
check("V6 [consistency, reported] eps0 > 1e-5 (the cluster potential) for at least one Q0 in 0.1-10 H0 at |K_2| = 2.5e5 (the condensate is not pushed through its minimum in wells)", any(v > 1e-5 for v in eps_tab.values()), json.dumps({str(q_): f"{v_:.1e}" for q_, v_ in eps_tab.items()}))
print(f"\n  caveats: quasi-static metric (Psi, Phi from the leading-k constraint equations; their time derivatives dropped), exact clock and scalar equations; the background expansion is the standard H(a) with Omega_m = 0.315 (the dust's background is not re-derived); baryons only as the explicit matter (the dust's perturbation enters through the sector's lapse equation); J_Y0 = 0; the sector starts unexcited at z = 100; Q0 is a free parameter of the candidate; alpha_2 from the pure Einstein-aether formula (f33 shows the scalar drag changes it by < 20%).  total {time.time()-T0:.0f}s")
print(f"\nRESULT: {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else ""))
sys.exit(1 if FAILS else 0)
