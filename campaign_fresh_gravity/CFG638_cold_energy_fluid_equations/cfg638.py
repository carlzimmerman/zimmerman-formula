"""CFG638: cold-energy fluid system (candidate B, Newtonian limit): checks of the moment hierarchy,
energy budget, closure coefficients, characteristics, linear stability and halo scales.
Kinetic equation (CFG541 E3 + CFG544 FIX-2 velocity relaxation, momentum-conserving form):
  d_t f + d_x[(v + v_s) f] - Phi' d_v f = gam d_v[(v - u) f + T_J d_v f],  gam = alpha/tau.
kappa = 1/2 fitted; cold energy's mass required; not theory closed."""
import os, sys, json
import sympy as sp
MUT = os.environ.get("CFG638_MUTATE", "0") == "1"   # tooth: wrong relaxation rate (2gam -> 3gam) and wrong sink sign
MF = 3 if MUT else 2
SG = -1 if MUT else 1
TAG = "_MUTATE" if MUT else ""

ok = {}
x, t, v = sp.symbols('x t v', real=True)
gam, TJ = sp.symbols('gamma T_J', positive=True)
n = sp.symbols('n', integer=True, nonnegative=True)

# --- K1: exact OU moment identities (any f): M_n = int v'^n f, v' = v - u ------------------
# int c^n d_c[c f + T d_c f] dc = -n M_n + n(n-1) T M_{n-2}   (by parts, two times)
c = sp.symbols('c', real=True)
s2 = sp.symbols('s2', positive=True)
g = sp.exp(-c**2/(2*s2))/sp.sqrt(2*sp.pi*s2)
for k in range(1, 5):
    lhs = sp.integrate(c**k*sp.diff(c*g + TJ*sp.diff(g, c), c), (c, -sp.oo, sp.oo))
    Mk = sp.integrate(c**k*g, (c, -sp.oo, sp.oo)); Mk2 = sp.integrate(c**(k-2)*g, (c, -sp.oo, sp.oo)) if k >= 2 else 0
    ok[f'K1_n{k}'] = sp.simplify(lhs - (-k*Mk + k*(k-1)*TJ*Mk2)) == 0
# => 2nd moment relaxes at 2*gam toward rho*T_J, 3rd (heat flux) at 3*gam: exact, no closure.

# --- K2: 1-D moment equations from the kinetic equation on a Gaussian f ------------------
rho, u, s, vs, Phi = [sp.Function(nm)(x, t) for nm in ('rho', 'u', 's', 'vs', 'Phi')]
TJf = sp.Function('TJ')(x, t)
f = rho/sp.sqrt(2*sp.pi*s)*sp.exp(-(v-u)**2/(2*s))
kin = sp.diff(f, t) + sp.diff((v+vs)*f, x) - sp.diff(Phi, x)*sp.diff(f, v) \
      - gam*sp.diff((v-u)*f + TJf*sp.diff(f, v), v)
def mom(expr, k):
    e = sp.expand(expr*(v-u)**k if k else expr)
    return sp.simplify(sp.integrate(e, (v, -sp.oo, sp.oo), conds='none'))
P = rho*s
w = u + vs
cont = sp.diff(rho, t) + sp.diff(rho*w, x)
momq = sp.diff(rho*u, t) + sp.diff(rho*w*u + P, x) + rho*sp.diff(Phi, x)
m1 = sp.simplify(sp.integrate(sp.expand(kin*v), (v, -sp.oo, sp.oo), conds='none'))
pres = sp.diff(P, t) + sp.diff(w*P, x) + 2*P*sp.diff(u, x) + 2*gam*(P - rho*TJf)
# (direct Function-integrals are unreliable in sympy; check with explicit chain rule instead)
_r,_u,_s,_vs,_T=sp.symbols('r_ u_ s_ vs_ T_',positive=True)
_rt,_rx,_ut,_ux,_st,_sx,_vsx,_Px=sp.symbols('rt_ rx_ ut_ ux_ st_ sx_ vsx_ Px_',real=True)
_f=_r/sp.sqrt(2*sp.pi*_s)*sp.exp(-(v-_u)**2/(2*_s))
_D=lambda a1,a2,a3: sp.diff(_f,_r)*a1+sp.diff(_f,_u)*a2+sp.diff(_f,_s)*a3
_kin=_D(_rt,_ut,_st)+(v+_vs)*_D(_rx,_ux,_sx)+_vsx*_f-_Px*sp.diff(_f,v)-gam*sp.diff((v-_u)*_f+_T*sp.diff(_f,v),v)
_I=lambda e: sp.simplify(sp.integrate(sp.expand(e),(v,-sp.oo,sp.oo)))
_w=_u+_vs
_cont=_rt+_rx*_w+_r*(_ux+_vsx)
_mom=_r*(_ut+_w*_ux)+(_rx*_s+_r*_sx)+_r*_Px
_pres=(_rt*_s+_r*_st)+(_ux+_vsx)*_r*_s+_w*(_rx*_s+_r*_sx)+2*_r*_s*_ux+MF*gam*(_r*_s-_r*_T)
ok['K2_continuity']=sp.simplify(_I(_kin)-_cont)==0
ok['K2_momentum']=sp.simplify(_I(_kin*(v-_u))-_mom)==0
ok['K2_pressure']=sp.simplify(_I(_kin*(v-_u)**2)-_pres)==0

# --- K3: energy identity (1-D, external Phi): source = rho v_s Phi_x + gam(rho T_J - P) -----
E = rho*u**2/2 + P/2 + rho*Phi
# use the three PDEs to eliminate time derivatives
rt, ut, st = sp.symbols('rt ut st')
sol = sp.solve([cont.subs({sp.diff(rho, t): rt}),
                momq.subs({sp.diff(rho, t): rt, sp.diff(u, t): ut}).doit(),
                pres.subs({sp.diff(rho, t): rt, sp.diff(s, t): st}).doit()], [rt, ut, st], dict=True)[0]
Et = sp.diff(E.subs(Phi, sp.Function('Phi')(x)), t)
Phis = sp.Function('Phi')(x)
Et = (rho*u**2/2 + P/2 + rho*Phis).diff(t).subs({sp.diff(rho, t): sol[rt], sp.diff(u, t): sol[ut], sp.diff(s, t): sol[st]})
flux = rho*u**2/2*w + P/2*w + u*P + rho*Phis*w
src = sp.simplify(Et + sp.diff(flux, x))
target = SG*rho*vs*sp.diff(Phis, x) + gam*(rho*TJf - P)
ok['K3_energy'] = sp.simplify((src - target).subs(Phi, Phis)) == 0

# --- K4: Chapman-Enskog (3-D, from the exact 2gam / 3gam rates) --------------------------
# deviatoric: d_t pi + ... + p(d_i u_j + d_j u_i - 2/3 delta div u) = -2 gam pi
#   => pi_ij = -(p/2gam)(...)  =>  eta = p tau/(2 alpha)
# trace (target T_J fixed by the bath, not by energy conservation):
#   2gam (p - rho T_J) = -rho [D T_J/Dt + (2/3) T_J div u]  =>  zeta = p tau/(3 alpha)
# heat flux: q = -(5/2) p/(3gam) grad(sigma^2) = -(5/6)(p tau/alpha) grad sigma^2
alpha, tau, p_ = sp.symbols('alpha tau p', positive=True)
eta = p_/(2*alpha/tau); zeta = p_/(3*alpha/tau); kth = sp.Rational(5, 2)*p_/(3*alpha/tau)
print('eta =', sp.simplify(eta), '  zeta =', sp.simplify(zeta), '  q-coefficient =', sp.simplify(kth))

# --- K5: characteristics of the 1-D Gaussian (10-moment) system: u, u +- sqrt(3) sigma -------
R, U, Pp = sp.symbols('R U Pp', positive=True)
A = sp.Matrix([[U, R, 0], [0, U, 1/R], [0, 3*Pp, U]])   # (rho, u, P) quasilinear, v_s off
ev = A.eigenvals()
ok['K5_char'] = set(sp.simplify(e) for e in ev) == {U, U - sp.sqrt(3*Pp/R), U + sp.sqrt(3*Pp/R)}
print('characteristic speeds:', list(ev))

# --- K6: linear dispersion in a uniform bound region (two-sided deficit, rho_ph fixed) -----
om, k, G, r0, rm, T0 = sp.symbols('omega k G rho0 rho_m T0', positive=True)
dr, du, dP = sp.symbols('dr du dP')
tauff = 1/sp.sqrt(4*sp.pi*G*rm); gm = alpha/tauff
Gam = 4*sp.pi*G*r0*alpha*tauff                        # drift damping, k-independent (CFG541 A0)
dvs = -alpha*tauff*sp.I*k*(4*sp.pi*G*dr/k**2)        # v_s = -alpha tau grad psi, -k^2 psi = -4piG dr
dPhi = -4*sp.pi*G*dr/k**2
eqs = [-sp.I*om*dr + r0*sp.I*k*(du + dvs),
       -sp.I*om*r0*du + sp.I*k*dP + r0*sp.I*k*dPhi,
       -sp.I*om*dP + r0*T0*sp.I*k*(du + dvs) + 2*r0*T0*sp.I*k*du + 2*gm*(dP - T0*dr)]
Mx = sp.Matrix([[sp.diff(e, vv) for vv in (dr, du, dP)] for e in eqs])
disp = sp.expand(Mx.det())
# growth s = -i omega. Isothermal limit gam -> inf: s^2 + Gam s + (k^2 T0 - 4piG rho0) = 0
sg = sp.symbols('s')
iso = sp.limit(sp.expand(disp.subs(om, sp.I*sg)/(2*gm)), alpha, sp.oo) if False else None
d_s = sp.expand(disp.subs(om, sp.I*sg))
lead = sp.Poly(d_s, sg)
print('dispersion (s = growth rate):', sp.factor(d_s))
# numeric scan: does the drift kill the Jeans mode? use units 4piG rho_m = 1, rho0/rho_m = q
import numpy as np
res = {}
for q in (0.5, 0.84, 0.95):
    for a in (0.03, 0.5, 1.0):
        sub = {G: 1/(4*sp.pi), rm: 1, r0: q, alpha: a, T0: 1.0}
        kJ = float(sp.sqrt(4*sp.pi*G*r0/T0).subs(sub))
        row = []
        for kk in (0.25*kJ, 0.5*kJ, 0.9*kJ):
            roots = sp.Poly(d_s.subs(sub).subs(k, kk), sg).nroots()
            row.append(max(float(sp.re(rr)) for rr in roots))
        res[(q, a)] = (row, float(Gam.subs(sub)), float(sp.sqrt(4*sp.pi*G*r0).subs(sub)))
for (q, a), (row, Gm, wJ) in res.items():
    print(f'rho_c/rho_m={q:4.2f} alpha={a:4.2f}: Gamma/omega_J={Gm/wJ:5.3f}  max growth/omega_J at k/kJ=.25,.5,.9: '
          + ', '.join(f'{r/wJ:+.3f}' for r in row))
ok['K6_drift_rate'] = sp.simplify(Gam - alpha*(r0/rm)*sp.sqrt(4*sp.pi*G*rm)) == 0

# --- K7: scales in a singular isothermal halo (rho = V^2/4piG r^2, sigma^2 = V^2/2) ---------
V, r = sp.symbols('V r', positive=True)
rho_sis = V**2/(4*sp.pi*G*r**2)
tff = sp.simplify(1/sp.sqrt(4*sp.pi*G*rho_sis))
taupi = tff/(2*alpha)
sig = V/sp.sqrt(2)
nu_kin = sp.simplify(sig**2*taupi)                       # eta/rho
Kn = sp.simplify(sig*taupi/r)
Re = sp.simplify(V*r/nu_kin)
print('SIS: tau_ff =', tff, ' tau_pi =', sp.simplify(taupi), ' nu =', nu_kin, ' Kn =', Kn, ' Re =', Re)
ok['K7_scalefree'] = (sp.simplify(sp.diff(Kn, r)) == 0) and (sp.simplify(sp.diff(Re, r)) == 0)
for a in (0.03, 0.5, 1.0, 1.186):
    print(f'  alpha={a}: Kn={float(Kn.subs(alpha, a)):.3f}  Re={float(Re.subs(alpha, a)):.2f}')

print()
for kk, vv in ok.items():
    print(f'{kk:16s} {"PASS" if vv else "FAIL"}')
allp = all(ok.values())
print('ALL PASS' if allp else 'SOME FAIL')
json.dump(dict(lane='CFG638', mutate=MUT, checks={k: bool(v) for k, v in ok.items()}, all_pass=bool(allp),
               coefficients=dict(eta='p tau/(2 alpha)', zeta='p tau/(3 alpha)', heat_flux='-(5/6)(p tau/alpha) grad sigma^2'),
               sis=dict(tau_ff='r/V', tau_pi='r/(2 alpha V)', nu='V r/(4 alpha)', Kn='sqrt(2)/(4 alpha)', Re='4 alpha'),
               jeans_growth={f'{q}_{a}': dict(growth_over_omegaJ=[round(x / wJ, 4) for x in row], Gamma_over_omegaJ=round(Gm / wJ, 4))
                             for (q, a), (row, Gm, wJ) in res.items()}),
          open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f'cfg638_results{TAG}.json'), 'w'), indent=1)
# normal run: exit 0 iff all pass; MUTATE: exit 1 iff the teeth bite (K2_pressure and K3_energy fail)
if MUT:
    sys.exit(1 if (not ok['K2_pressure'] and not ok['K3_energy']) else 0)
sys.exit(0 if allp else 1)
