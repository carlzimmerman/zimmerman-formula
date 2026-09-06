#!/usr/bin/env python3
"""
g03w2 -- identifying g03w's early-time exponential mode at c_2 = 0.05
======================================================================
OUTCOME (2026-09-06): (1) at c_2 = 1e-4 the unstable mode IS the tilt mode (eigenvector 100% in T, vanishes without dust, rate 1.0e3 H vs
the analytic 503 H).  (2) at c_2 = 0.05 the clock is rigid (c_2 k^4 : dust = 31 : 1) and the 700 H mode lives in the baryon density; it
tracks the DUST AMOUNT (5.5 H at eps0/2) because the baseline parameters violate the dust regime: with Q0 = H0, |K_2| = 2.5e5 the
condensate sits at eps = 3.2 off its minimum at z = 100, where the quadratic K gives NEGATIVE energy (rho_d = |K_2| Q0^2 eps (2 - eps)).
(3) with |K_2| Q0^2 >= 1e9 H0^2 (Q0 >= 100 H0: eps << 1 back to recombination) the a = 0.01 rate is 0.18 H, but a late-time exponential
mode in the baryon density remains: 4.6 H at a = 0.3 for Q0 = 100 H0, 14 H for Q0 = 1000 H0 (~ Q0^0.5) -- the condensate's response to the
lapse (2 |K_2| Q0^2 a^3 Psi in the lapse equation), the ghost condensate's gravitational mixing, the same obstruction as g03x.
The dust regime and gravitational stability cannot share |K_2| Q0^2.  The two-field dust is not rescued at c_2 = 0.05.
g03w found a real eigenvalue ~700 H at a = 0.01 for every branch, including c_2 = 0.05 where the c_2 k^4 rigidity should suppress the
tilt (the balance c_2 k^4/a against the dust term 2 k^2 |K_2| Q0^2 eps0/a^2 is 14:1 at k = 0.05/Mpc, a = 0.01).  Here the FULL 8-variable
Jacobian (delta, delta', Phi, Phi', T, T', P, P') of the two-field sector is formed at frozen a with the clock dynamical (g03w's
CLOCK = 'full' scheme: Phi dynamical, Psi from the lapse constraint, Psi' from its time derivative), and the unstable eigenvector is read
off, with controls: (i) no dust (eps0 = 0: the tilt term absent), (ii) no MOND scalar (K_2 -> 0 limit via P frozen), (iii) c_2 = 1e-4.
Checks that can fail:
  M1 [analytic]  at k = 0.05/Mpc, a = 0.01, c_2 = 0.05 the clock equation's own T coefficient is dominated by the c_2 k^4 term (ratio > 5)
                 so the pure clock oscillates: -coeff(T)/coeff(T'') < 0;
  M2 [reported]  the largest real eigenvalue of the full system for c_2 = 0.05 and 1e-4 at a = 0.01, with the eigenvector's weight in
                 (T, T') versus (Phi, Phi') versus (P, P') versus (delta, delta');
  M3 [identification] the unstable mode at c_2 = 0.05 is NOT the tilt mode if it (a) survives with eps0 = 0 and (b) has < 10% of its
                 weight in (T, T'); it IS the tilt mode if it disappears at eps0 = 0 and its weight is in (T, T');
  M4 [scheme]    the same Jacobian with the differentiated-constraint Psi' replaced by Psi' = 0 (a crude but constraint-preserving-in-spirit
                 variant): whether the unstable mode's rate changes by more than a factor 3 (scheme sensitivity).
"""
import numpy as np, math, sys, json, time
src = open("g03w_growth_phi_dynamical.py").read(); head = src[:src.index("D_L = growth_LCDM(0.01, 1.0)")]
head = head.replace("CLOCK = 'adiabatic'", "CLOCK = 'full'")
g = {}; exec(compile(head, "g03w2_head", "exec"), g)
COEF, VARS, Hof, addot_of, cH0_Mpc, Om, OL, Ob, Od, H0, build_tables, coefs = (g[k] for k in ("COEF", "VARS", "Hof", "addot_of", "cH0_Mpc", "Om", "OL", "Ob", "Od", "H0", "build_tables", "coefs"))
FAILS = []
def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
T0 = time.time()
def jacobian(kMpc, pars, aa, psi_dot_zero=False, freeze_P=False):
    kk = kMpc*cH0_Mpc; AA = np.geomspace(0.01, 1.0, 4000); build_tables(kk, pars, AA); H = Hof(aa)
    cP, cF, cT, cQ = coefs('Psi', aa), coefs('Phi', aa), coefs('T', aa), coefs('P', aa); dcP = {v: c_*aa*H for v, c_ in coefs('Psi', aa, deriv=True).items()}
    def psi_of(st):
        delta, dd, Ph, Pht, T, Tt, Pv, Pt = st
        return (6*Ob*H0**2*delta - (cP['Phik']*Ph + cP['Phik_t']*Pht + cP['Tk']*T + cP['Tk_t']*Tt + cP['Pk']*Pv + cP['Pk_t']*Pt))/cP['Psik']
    def rhs(st):
        delta, dd, Ph, Pht, T, Tt, Pv, Pt = st; Ps = psi_of(st); ddd = -2*H*dd - kk**2*Ps/aa**2
        known = 6*Ob*H0**2*dd - (cP['Phik']*Pht + dcP['Phik']*Ph + dcP['Phik_t']*Pht + cP['Tk']*Tt + dcP['Tk']*T + dcP['Tk_t']*Tt + cP['Pk']*Pt + dcP['Pk']*Pv + dcP['Pk_t']*Pt) - Ps*dcP['Psik']
        aX = np.array([-cP['Phik_t'], -cP['Tk_t'], -cP['Pk_t']])/cP['Psik']; bX = known/cP['Psik']
        if psi_dot_zero: aX = np.zeros(3); bX = 0.0
        M = np.zeros((3, 3)); r = np.zeros(3)
        for i, c in enumerate((cF, cT, cQ)):
            M[i] = [c['Phik_tt'] + c['Psik_t']*aX[0], c['Tk_tt'] + c['Psik_t']*aX[1], c['Pk_tt'] + c['Psik_t']*aX[2]]
            r[i] = -(c['Phik_t']*Pht + c['Phik']*Ph + c['Tk_t']*Tt + c['Tk']*T + c['Pk_t']*Pt + c['Pk']*Pv + c['Psik']*Ps + c['Psik_t']*bX)
        if freeze_P:
            M2 = M[:2, :2]; r2 = r[:2] - M[:2, 2]*0.0; X2 = np.linalg.solve(M2, r2); X = np.array([X2[0], X2[1], 0.0])
        else: X = np.linalg.solve(M, r)
        return np.array([dd, ddd, Pht, X[0], Tt, X[1], Pt, X[2] if not freeze_P else 0.0])
    base = np.zeros(8); base[0] = 1.0; base[1] = H; base[2] = 6*Ob*H0**2/cP['Phik']; f0 = rhs(base); J = np.zeros((8, 8))
    for ii in range(8):
        dq = np.zeros(8); dq[ii] = 1e-6*max(1.0, abs(base[ii])); J[:, ii] = (rhs(base + dq) - f0)/dq[ii]
    ev, vec = np.linalg.eig(J); i = int(np.argmax(ev.real)); v = vec[:, i]
    # weights: normalise each pair by its natural scale (x, x'/H) so the derivative components are comparable
    w = np.array([abs(v[0])**2 + abs(v[1]/H)**2, abs(v[2])**2 + abs(v[3]/H)**2, abs(v[4])**2 + abs(v[5]/H)**2, abs(v[6])**2 + abs(v[7]/H)**2]); w = w/w.sum()
    return dict(rate=float(ev.real[i]/H), imag=float(abs(ev.imag[i])/H), w=w, cT=cT)
K2abs = 2.5e5; eps0 = 3*H0**2*Od/(K2abs*1.0**2); a_ = 0.01; kM = 0.05
pars05 = (0.2, 0.05, 1e-5, -K2abs, 1.0, eps0)
J05 = jacobian(kM, pars05, a_)
cT = J05["cT"]; ratio_T = -cT['Tk']/cT['Tk_tt']; kk = kM*cH0_Mpc
c2term = 2*0.05*kk**4/a_; dustterm = 2*kk**2*K2abs*1.0*eps0/a_**2
print(f"    clock equation at a = 0.01, k = 0.05/Mpc, c2 = 0.05: coeff(T'') = {cT['Tk_tt']:.3e}, coeff(T) = {cT['Tk']:.3e}; -coeff(T)/coeff(T'') = {ratio_T:.3e} (negative = oscillatory); c2 k^4 term {c2term:.2e} vs dust term {dustterm:.2e} (ratio {c2term/dustterm:.1f})", flush=True)
check("M1 [analytic] at c_2 = 0.05 the clock's own T coefficient is dominated by the c_2 k^4 rigidity (ratio > 5) and the pure clock oscillates (-coeff(T)/coeff(T'') < 0)", c2term/dustterm > 5 and ratio_T < 0, f"ratio {c2term/dustterm:.1f}, -cT/cTtt = {ratio_T:.2e}")
rows = {}
for lab, pars, kw in (("c2 = 0.05", pars05, {}), ("c2 = 0.05, eps0 = 0 (no dust)", (0.2, 0.05, 1e-5, -K2abs, 1.0, 0.0), {}), ("c2 = 0.05, P frozen (no MOND scalar dynamics)", pars05, {"freeze_P": True}), ("c2 = 0.05, Psi' = 0 (constraint not differentiated)", pars05, {"psi_dot_zero": True}), ("c2 = 1e-4", (0.2, 1e-4, 1e-5, -K2abs, 1.0, eps0), {}), ("c2 = 1e-4, eps0 = 0", (0.2, 1e-4, 1e-5, -K2abs, 1.0, 0.0), {})):
    r = jacobian(kM, pars, a_, **kw); rows[lab] = r
    print(f"    {lab:52s}: max Re = {r['rate']:9.2e} H (Im {r['imag']:.1e} H); eigenvector weight delta {r['w'][0]:.2f} | Phi {r['w'][1]:.2f} | T {r['w'][2]:.2f} | P {r['w'][3]:.2f}", flush=True)
tilt_rate = math.sqrt(K2abs*eps0/a_**3/1e-5)/Hof(a_); print(f"    analytic tilt rate at a = 0.01: {tilt_rate:.1f} H")
r0 = rows["c2 = 0.05"]; rnd = rows["c2 = 0.05, eps0 = 0 (no dust)"]
is_tilt = r0['rate'] > 100 and rnd['rate'] < 0.1*r0['rate'] and r0['w'][2] > 0.5
not_tilt = r0['rate'] > 100 and rnd['rate'] > 0.5*r0['rate'] and r0['w'][2] < 0.1
print(f"    identification: tilt-like = {is_tilt}, not-tilt = {not_tilt}")
check("M3 [identification, reported] the c_2 = 0.05 early-time mode is identified: either the tilt mode (disappears without dust, lives in T) or not (survives without dust, < 10% weight in T)", is_tilt or not_tilt, f"rate {r0['rate']:.2e} H; without dust {rnd['rate']:.2e} H; T-weight {r0['w'][2]:.2f}")
rs = rows["c2 = 0.05, Psi' = 0 (constraint not differentiated)"]
check("M4 [scheme] the unstable rate at c_2 = 0.05 changes by less than a factor 3 when the differentiated constraint is replaced by Psi' = 0 (scheme-insensitive)", r0['rate'] > 0 and rs['rate'] > 0 and max(r0['rate']/max(rs['rate'], 1e-30), rs['rate']/max(r0['rate'], 1e-30)) < 3, f"{r0['rate']:.2e} vs {rs['rate']:.2e} H")
print(f"\n  caveats: frozen-coefficient Jacobian (WKB-like; valid while the rate >> H, which is the case examined); eigenvector weights compare (x, x'/H) pairs; the differentiated-constraint scheme of g03w with its Psi' = 0 variant as the only scheme control.  total {time.time()-T0:.0f}s")
print(f"\nRESULT: {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else ""))
sys.exit(1 if FAILS else 0)
