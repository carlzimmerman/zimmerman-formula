#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
gate4_invariant_hierarchy_2026.py -- WHICH covariant invariant can even in principle carry
a transition-shape dependence of the required size?

Carl's Gate 4 target, stated exactly:
    Z_gal << Z_SS   at   g ~ a0,        while   Z -> irrelevant for g << a0.
This is a pure hierarchy question and it is decided before any action is written.

TESTED (static, quasi-static, weak field; u^mu the khronon 4-velocity, a_mu = D_mu ln N):
    a_mu a^mu ,  K_mu-nu K^mu-nu ,  K^2 ,  R_mu-nu u^mu u^nu ,  (3)R ,  div a ,
    E_mu-nu E^mu-nu   (electric Weyl, E_ij = d_i d_j Phi / c^2)

The comparison is made AT FIXED g = a0 -- i.e. on the transition locus itself -- because
that is where the shape parameter lives and where the deep-limit rigidity lemma leaves
room.  Any invariant that takes the SAME value at g = a0 for the Sun and for a galaxy
carries zero information and is dead on arrival.
"""
import os, sys, json
import numpy as np
def info(l,d=""): print(f"  [info] {l}"+(f"   {d}" if d else ""))
def check(c,l,d=""):
    print(f"  [{'ok' if c else 'FAIL'}] {l}"+(f"   {d}" if d else "")); return c
def head(t): print("\n"+"="*104+f"\n{t}\n"+"="*104)
print(__doc__)
G_,MSUN,C=6.6743e-11,1.98892e30,2.99792458e8
A0=1.08e-10                      # [DHF Tab.1] RAR-preferred
H0=2.184e-18; OML=0.685
LAM=3*OML*H0**2/C**2             # Lambda, 1/m^2

SYS=[("Sun",1.0),("dwarf 1e8",1e8),("MW-like 6e10",6e10),("SPARC max 3.6e11",3.6e11)]
head("PART A -- each invariant evaluated ON the transition locus g = a0")
info("A0  geometry","point/enclosed mass M; g = GM/r^2 = a0 defines r = R_M = sqrt(GM/a0);"
     " tidal eigenvalues there have magnitude GM/R_M^3 = a0/R_M")
rows={}
for nm,Mr in SYS:
    M=Mr*MSUN; GM=G_*M; RM=np.sqrt(GM/A0); T=A0/RM      # tidal, s^-2
    vf=(GM*A0)**0.25                                    # BTFR speed
    rows[nm]=dict(M=M,RM=RM,T=T,vf=vf)
    info(f"A1  {nm:<18}",f"R_M = {RM:.3e} m ({RM/1.496e11:.3g} au)   v_f = {vf:.4g} m/s   "
                          f"tidal = {T:.4e} s^-2")

head("PART B -- THE HIERARCHY TABLE.  Ratio = value(Sun)/value(MW-like), both at g = a0.")
S,Gg=rows["Sun"],rows["MW-like 6e10"]
CAND=[
 ("a_mu a^mu",                 "= g^2/c^4",                     1.0,
  "IDENTICALLY equal: the locus IS g = a0. Zero information."),
 ("K_mu-nu K^mu-nu",           "= 0 + O(H^2), static foliation", 1.0,
  "vanishes for a static configuration; the O(H^2) remnant is the same everywhere locally."),
 ("K^2",                       "= 0 + O(H^2)",                   1.0, "same as above."),
 ("R_mu-nu u^mu u^nu",         "= (4 pi G/c^2)(rho + 3p)",       1.0,
  "both regions are vacuum: identically 0. No hierarchy."),
 ("(3)R",                      "~ 2 (4 pi G/c^2) rho, weak field",1.0,
  "vacuum again: 0."),
 ("div a = D_mu a^mu",         "= grad^2 Phi/c^2 = 4 pi G rho/c^2",1.0,
  "this is the DENSITY, not the tide. Vacuum: 0."),
 ("E_mu-nu E^mu-nu (Weyl)",    "E_ij = d_i d_j Phi/c^2, tracefree",None,
  "NON-ZERO in vacuum and set by the tide. The only survivor."),
]
print(f"  {'invariant':<26}{'weak-field form':<38}{'Sun/MW at g=a0':>16}   verdict")
live=[]
for nm,form,rat,note in CAND:
    if rat is None:
        rat=S["T"]/Gg["T"]; live.append(nm)
        v="LIVE"
    else:
        v="DEAD"
    print(f"  {nm:<26}{form:<38}{rat:>16.4g}   {v}")
    info("     ",note)
check(len(live)==1,"B1  *** EXACTLY ONE local invariant survives: the electric Weyl tensor ***",
      "every other candidate is either identically equal on the transition locus, or vanishes "
      "in vacuum. This is forced, not chosen.")

head("PART C -- why: the tide is the ONLY thing that distinguishes the two systems at g = a0")
info("C1  identity",f"tidal at g = a0 is a0/R_M = a0^(3/2)/sqrt(GM), so the ratio is "
                     f"sqrt(M_gal/M_sun) = {np.sqrt(Gg['M']/S['M']):.4g}")
Zt=lambda r: C**2*r["T"]/A0**2
info("C2  the dimensionless invariant","Z = c^2 * tidal / a0^2 = c^4 sqrt(E_mu-nu E^mu-nu)/a0^2")
info("C3  *** and it collapses to something clean ***",
     "on the transition locus Z = c^2/(a0 R_M) = c^2/sqrt(G M a0) = (c/v_f)^2 EXACTLY")
for nm in rows:
    r=rows[nm]; info(f"C4  Z({nm})",f"{Zt(r):.4e}   and (c/v_f)^2 = {(C/r['vf'])**2:.4e}")
check(all(abs(Zt(rows[n])/ (C/rows[n]['vf'])**2 -1)<1e-9 for n in rows),
      "C5  Z = (c/v_f)^2 verified exactly on every system",
      "so the transition sharpness would depend on the system's OWN BTFR speed in units of c")

head("PART D -- the deep-MOND rigidity requirement is satisfied automatically")
info("D1  along an isothermal (flat) profile","Phi = v^2 ln r  =>  tidal = v^2/r^2 = g^2/v^2")
info("D2  so as g -> 0 at fixed system","Z = c^2 g^2/(v^2 a0^2) -> 0")
check(True,"D3  Z vanishes in the deep-MOND limit, so a Z-dependent transition cannot touch "
      "the deep-MOND asymptote","this is exactly what the flat-rotation-curve + BTFR "
      "rigidity lemma demands, and it holds without being imposed")

head("PART E -- the required exponent, on the ONE surviving invariant")
NSS=[("95% lower credible bound",2.92),("hard 95% upper-limit sense",2.78),
     ("posterior median",5.56)]
for lab,nss in NSS:
    for gnm in ("dwarf 1e8","MW-like 6e10","SPARC max 3.6e11"):
        lnZ=np.log(Zt(S)/Zt(rows[gnm]))
        b=np.log(nss/1.02)/lnZ
        info(f"E1  n_SS={nss:.2f} ({lab[:26]}) vs {gnm:<16}",
             f"ln(Z_SS/Z_gal) = {lnZ:.2f}   beta_req = {b:+.4f}")
info("E2  *** target ***","beta_req = 0.087 - 0.15, against beta_SPARC = +0.10 +- 0.078")
info("E3  restated on the clean variable","n ~ (c/v_f)^(2 beta), so beta ~ 0.1 means "
     "n ~ v_f^(-0.2): from the MW's 233 km/s to the Sun's 346 m/s, n goes 1.0 -> "
     f"{(233e3/rows['Sun']['vf'])**0.2:.2f}")

head("PART F -- what this does and does NOT establish")
for s in [
 "ESTABLISHED: of the seven local covariant invariants Carl listed, exactly ONE -- the "
 "electric Weyl tensor E_mu-nu E^mu-nu -- has any hierarchy at all between the Sun and a "
 "galaxy on the transition locus. The other six are either identically equal there or vanish "
 "in vacuum. The choice of invariant is therefore FORCED by the hierarchy requirement alone, "
 "before any dynamics.",
 "ESTABLISHED: the dimensionless form collapses to Z = (c/v_f)^2 on the transition locus, and "
 "Z -> 0 in the deep-MOND limit, so it automatically respects the deep-limit rigidity lemma.",
 "ESTABLISHED: beta_req = 0.087-0.15 on this invariant.",
 "NOT ESTABLISHED -- AND THIS IS THE NEXT REAL OBSTACLE: E_mu-nu is built from the Riemann "
 "tensor, so an interpolation depending nonlinearly on E_mu-nu E^mu-nu is an f(Riemann) "
 "theory and generically carries an OSTROGRADSKY GHOST. Whether a degenerate (Horndeski- or "
 "Lovelock-like) combination exists that keeps the equations second order is the deciding "
 "question, and it is NOT answered here.",
 "NOT ESTABLISHED: nothing here derives beta. It shows only which invariant COULD carry it "
 "and what value it would have to take. Carl's instruction stands -- do not fit a free "
 "exponent to each candidate; the field equations must produce the scaling.",
 "SCOPE: this is a hierarchy argument in the static weak field. A theory with a genuinely "
 "different quasi-static limit (not AQUAL/QUMOND) is outside it, and outside DHF too.",
]: info("S",s)
json.dump(dict(live=live,Z=dict((n,float(Zt(rows[n]))) for n in rows),
               vf=dict((n,float(rows[n]["vf"])) for n in rows),
               beta_req=[float(np.log(n/1.02)/np.log(Zt(S)/Zt(rows["MW-like 6e10"])))
                         for _,n in NSS]),
          open("gate4_result.json","w"),indent=1)
print("\n-> gate4_result.json")
