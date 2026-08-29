import sys
sys.path.insert(0, '.')
import sympy as sp
import fc_alpha2_methodB_opt3 as M
P = lambda *a: print(*a, flush=True)
Uh=M.Uh; subU={M.Rk:-Uh/(4*sp.pi)}
KB,K2,Q0,JY = M.KB,M.K2,M.Q0,M.JY

# SYMBOLIC static sector (keep KB,K2,Q0,JY symbolic) to check gamma=1 and Newtonian form.
sub = {M.GT:1, M.kx:1, M.ky:0, M.kz:0}
L = sp.expand(sp.expand(M.L2dc.subs(M.GAUGE)).subs(sub))
BRAS=M.BRAS; KETS=M.KETS
eqf={A:sp.expand(sp.diff(L,A)) for A in BRAS}
VZ={M.Bk[1]:0,M.Bk[2]:0,M.ak[1]:0,M.ak[2]:0,M.hk[(2,3)]:0}
su=[M.Psik,M.hk[(2,2)],M.hk[(3,3)],M.ak[0],M.chik]
sb=[M.Psib,M.hb[(2,2)],M.hb[(3,3)],M.ab[0],M.chib]
e0=[sp.expand(eqf[A].coeff(M.wb,0).subs(VZ)) for A in sb]
s0=M.lin_solve(e0,su)
if s0 is None:
    P("STATIC SOLVE FAILED"); sys.exit()
Psis=sp.cancel(s0[M.Psik].subs(subU)); h22s=sp.cancel(s0[M.hk[(2,2)]].subs(subU))
h33s=sp.cancel(s0[M.hk[(3,3)]].subs(subU)); chis=sp.cancel(s0[M.chik].subs(subU)); a1s=sp.cancel(s0[M.ak[0]].subs(subU))
P("Psi_static  =", sp.simplify(Psis))
P("h22_static  =", sp.simplify(h22s))
P("h33_static  =", sp.simplify(h33s))
P("gamma = h22/(2 Psi) =", sp.simplify(h22s/(2*Psis)))
P("h22==h33 ? ", sp.simplify(h22s-h33s)==0)
P("chi_static  =", sp.simplify(chis))
P("a1_static   =", sp.simplify(a1s))
# Newtonian: expect Psi_static = Uh * (something) ; check the K_B, mass structure.
# In k=1 units, committed typeII: lap Psi - m^2 Psi = 4 pi Ghat rho, Ghat=Gt/(1-K_B/2), m^2=K2 Q0^2/(2-K_B)
# => Psik = -4 pi Ghat Rk/(k^2+m^2) = Uh*(1/(1-K_B/2))/(1+m^2)  with Rk=-Uh/4pi, Gt=1,k=1
mP2 = K2*Q0**2/(2-KB)
expect = Uh/(1-KB/2)/(1+mP2)
P("\nexpected Psi (typeII committed) =", sp.simplify(expect))
P("Psi_static / expected =", sp.simplify(Psis/expect))
