"""q03: is rho_Lambda = 32 pi P_Lambda (P_Lambda = a0^2/(8 pi G), the record's stress cap) an EQUILIBRIUM condition of a hydrostatic medium?
Variables: both Lambda (rho_Lambda = Lambda/8piG) and a0 are kept independent until the last line; the puzzle is rho/P = 32 pi <=> G rho = 4 a0^2."""
import sympy as sp, numpy as np, sys
from common import *
ok=[]
def chk(n,c): ok.append(bool(c)); print(("PASS " if c else "FAIL ")+n)
r,R,rho,G,a0,Lam,P0=sp.symbols('r R rho G a0 Lambda P0',positive=True)
PL=a0**2/(8*sp.pi*G)
chk("1 puzzle <=> rho/P_Lambda = 32 pi (G rho = 4 a0^2)", sp.simplify(sp.solve(sp.Eq(rho/PL,32*sp.pi),rho)[0]-4*a0**2/G)==0)
# (a) uniform self-gravitating sphere, Newtonian hydrostatic: dP/dr = -rho g, g = (4 pi/3) G rho r, P(R)=0
Pc=sp.integrate(rho*sp.Rational(4,3)*sp.pi*G*rho*r,(r,0,R))
chk("2 uniform sphere: P_c = (2 pi/3) G rho^2 R^2", sp.simplify(Pc-2*sp.pi*G*rho**2*R**2/3)==0)
# (b) at the MOND transition radius R_t (g_N = a0): P_c = 3 P_Lambda independent of rho
Rt=sp.solve(sp.Eq(sp.Rational(4,3)*sp.pi*G*rho*R,a0),R)[0]
chk("3 at R_t (g_N(R_t)=a0): P_c = 3 a0^2/(8 pi G) = 3 P_Lambda for EVERY rho (the cap scale is rho-independent: dimensional a0^2/G; no rho_Lambda/P_Lambda information)", sp.simplify(Pc.subs(R,Rt)-3*PL)==0)
# (c) which radius gives P_c = P_Lambda with rho = rho_Lambda=Lambda/8pi G, then puzzle:
Req=sp.solve(sp.Eq(Pc,PL),R)[0]
print("   R(P_c=P_Lambda) =",sp.simplify(Req)," ; R_eq/R_t =",sp.simplify(Req/Rt)," (pi-free, rho-free)")
chk("4 R(P_c=P_L) = R_t/sqrt(3)", sp.simplify(Req/Rt-1/sp.sqrt(3))==0)
# (d) equilibrium radius tied to a cosmological scale: R = c/H with Friedmann H^2=8 pi G rho/3  -> P_c/rho = 1/4  (Lambda and G rho held to FRIEDMANN)
H2=8*sp.pi*G*rho/3
chk("5 R=c/H (Friedmann, same rho): P_c/rho = 1/4 -> rho/P = 4, not 32 pi (off by 8 pi; pi-free rational)", sp.simplify((Pc/rho).subs(R,1/sp.sqrt(H2))-sp.Rational(1,4))==0)
# R = r_H=1/(2 a0), rho=rho_Lambda=4a0^2/G
val=sp.simplify((Pc/rho).subs({R:1/(2*a0),rho:4*a0**2/G}))
print("   R=r_H, rho=4a0^2/G: P_c/rho =",val," -> rho/P_c =",sp.simplify(1/val))
chk("6 R=r_H gives P_c/rho = 2 pi/3 (not 1/(32 pi))", sp.simplify(val-2*sp.pi/3)==0)
# required R for 1/(32 pi)
Rreq=sp.solve(sp.Eq(Pc/rho,1/(32*sp.pi)),R)[0].subs(rho,4*a0**2/G)
print("   R required for P_c/rho=1/(32pi) at G rho=4a0^2: R*a0 =",sp.simplify(Rreq*a0)," = (sqrt3/(16 pi))/a0 ; R/r_H =",sp.simplify(Rreq*2*a0))
chk("7 required R = sqrt(3)/(16 pi a0): a radius DEFINED by a0 (and a free parameter of the sphere) -> no closure", sp.simplify(Rreq*a0-sp.sqrt(3)/(16*sp.pi))==0)
# (e) deep-MOND self-gravity of the uniform sphere (AQUAL g = sqrt(a0 g_N)): P_c(R)
gD=sp.sqrt(a0*sp.Rational(4,3)*sp.pi*G*rho*r)
PcD=sp.integrate(rho*gD,(r,0,R))
print("   deep-MOND uniform sphere P_c =",sp.simplify(PcD))
RD=sp.solve(sp.Eq(PcD,PL),R)[0]
RD_p=sp.simplify(RD.subs({rho:4*a0**2/G}).subs(G,1)); print("   R(P_c = P_L), G rho=4a0^2 :",RD_p)
Rnum=float(RD_p.subs(a0,1))
print("   in units 1/a0: %.5f  ; r_H=0.5 ; R_t=%.5f"%(Rnum,3/(16*np.pi)))
# decoy rate for 'R/r_H' hitting a natural menu {1,1/2,1/3,2/3,1/pi,1/(2pi),1/4,...} -- frozen small menu
menu=[1,0.5,1/3,2/3,1/np.pi,1/(2*np.pi),0.25,2,3,np.pi,2*np.pi]
x=Rnum/0.5
hit=any(abs(x/m-1)<0.01 for m in menu); print("   R/r_H=%.5f ; menu hit (1%%): %s"%(x,hit))
chk("8 deep-MOND hydrostatic R/r_H not on the frozen rational/pi menu", not hit)
# (f) Einstein static universe with vacuum + dark medium (rho_d, P_d): rho_tot+3p_tot=0 (a'' = 0), Friedmann 8 pi G rho_tot/3 = 1/a^2
rd,Pd,rl=sp.symbols('rho_d P_d rho_L',positive=True)
sol_rd=sp.solve(sp.Eq((rd+3*Pd)+(rl-3*rl),0),rd)[0]
inv_a2=sp.simplify(8*sp.pi*G*(sol_rd+rl)/3)
print("   Einstein static: rho_d = ",sol_rd,"; 1/a^2 =",inv_a2)
chk("9 Einstein-static: rho_d = 2 rho_L - 3 P_d ; 1/a^2 = 8 pi G (rho_L - P_d)", sp.simplify(sol_rd-(2*rl-3*Pd))==0 and sp.simplify(inv_a2-8*sp.pi*G*(rl-Pd))==0)
cap=sp.simplify((1/inv_a2).subs({Pd:PL,rl:4*a0**2/G})*a0**2)
print("   with P_d=P_Lambda, G rho_L=4a0^2: (a a0)^2 =",cap,"; Lambda a^2 = 32 pi/(32 pi - 1) = %.5f"%float(32*np.pi/(32*np.pi-1)))
chk("10 (a a0)^2 = 1/(32 pi - 1): the static radius is not r_H (=1/(2 a0)) and the 32 pi appears only as an input", sp.simplify(cap-1/(32*sp.pi-1))==0)
# EoS needed: P_d/rho_d for rho_d from static condition at P_d=P_Lambda
eos=sp.simplify((PL/sol_rd.subs(Pd,PL)).subs(rl,4*a0**2/G))
print("   w_d = P_d/rho_d (static, cap pressure) =",eos)
chk("11 w_d = 1/(64 pi - 3), not 1/(32 pi): the static balance does not return the puzzle ratio", sp.simplify(eos-1/(64*sp.pi-3))==0 and abs(float(eos)-1/(32*np.pi))>1e-4)
# control: with 'wrong' Newtonian factor 4pi->2pi in g the identity of check 3 fails (the mutation must break it)
Pc_bad=sp.integrate(rho*sp.Rational(2,3)*sp.pi*G*rho*r,(r,0,R))
Rt_bad=Rt
chk("12 control: g=(2pi/3)G rho r breaks 'P_c(R_t)=3 P_Lambda'", sp.simplify(Pc_bad.subs(R,Rt)-3*PL)!=0)
print("\npi-ledger: P_c(R_t)=3P_L comes from (2pi/3)/(4pi/3)^2 = 3/(8pi): the pi is the Poisson 4pi (variable held fixed: a0, G; no Lambda).  rho_Lambda enters only through the radius, which is free.")
print("%d/%d"%(sum(ok),len(ok))); sys.exit(0 if all(ok) else 1)
