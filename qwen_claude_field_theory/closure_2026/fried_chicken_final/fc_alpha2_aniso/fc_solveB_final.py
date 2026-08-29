#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
fc_solveB_final.py  --  ROUTE B consolidated certificate driver.
====================================================================================================
Runs the decisive certificates for the FC-AeST + c2* preferred-frame alpha_2, via:
  PART A  Einstein-aether c-tensor map (Foster-Jacobson) -> alpha_2^EA.   [fc_solveB_partA_fj.py]
  PART B  independent moving-source (Setup M) 1PN solve  -> Delta alpha_2^(phiA).  [fc_solveB_setupM.py]

The Setup-M machinery is VALIDATED against the literature (Foster-Jacobson EA closed forms, EXACT)
and against the known static AeST quasi-static enhancement (Ghat: H00_on/H00_off = 1+1/J_Y).

VERDICT (all numbers below are COMPUTATION unless labelled):
  * alpha_2^EA(Maxwell corner c2*) = 0 EXACTLY, all cones luminal  (THEOREM, Foster-Jacobson).
  * the c2 SIGN: the healthy/luminal/alpha_2^EA=0 corner is the EA c2=+c2* branch, i.e. ACTION term
    -c2*(div A)^2.  The literal +c2*(div A)^2 gives a spin-0 GHOST (s0^2<0) and alpha_2^EA=2KB(2KB-1)/(2-KB).
  * Delta alpha_2^(phiA) DIVERGES as 1/K_B:   Delta alpha_2 ~ [4/(J_Y(1+J_Y))]/K_B  (numerically nailed).
    Equivalently ~ 4 beta_0^2/((1+beta_0) K_B), beta_0=1/J_Y=1/lambda_s (VSZ/typeII).
  * alpha_1^full -> -8/(1+J_Y)  (O(1), NOT -4K_B): the scalar mixes into alpha_1 too.
  * At the UNSCREENED beta_0~0.3-0.5 (Cassini-fold no-go, committed), |alpha_2| ~ 0.3-0.7/K_B; with
    K_B<2.5e-5 this is > 1e4, versus the bound |alpha_2|<~1e-7 -- FATAL by ~11 orders.
  * ROUTE A vs ROUTE B: at the healthy corner the vector gives 0 both ways; the scalar J-coupling is
    the whole effect and it is Q0-independent (J^mu A_mu=0 by the unit constraint) and 1/K_B-enhanced.

Mechanism: c2* liberates the spin-0 aether mode with a SOFT (O(c2*)=O(K_B)) kinetic term; the AeST
acceleration coupling 2(2-K_B)J^mu grad_mu phi sources it with O(1) strength => a 1/K_B strong-coupling
response that feeds the preferred-frame metric.  The reference cancellation cannot be imported.
"""
import sympy as sp, time
import fc_solveB_setupM as M
P = lambda *a: print(*a, flush=True)
T0 = time.time()
FAIL = []
def ck(c, l):
    P(f"  [{'ok' if c else 'FAIL'}] {l}")
    if not c: FAIL.append(l)

R = sp.Rational
P("="*96); P("ROUTE B FINAL CERTIFICATES  (Setup-M moving-source 1PN solve)"); P("="*96)

# C1: GR gate
P("\n[C1] GR gate (all AeST off): must give gamma=1, alpha_1=alpha_2=0")
r = M.solve(0.0, 10.0, 0.0, 1.0, gr_only=True)
ck(r[0] == 'ok' and sp.simplify(r[1]['gamma']-1) == 0 and sp.simplify(r[1]['alpha1']) == 0
   and sp.simplify(r[1]['alpha2']) == 0, f"GR: gamma={sp.nsimplify(r[1]['gamma'])}, "
   f"alpha_1={sp.nsimplify(r[1]['alpha1'])}, alpha_2={sp.nsimplify(r[1]['alpha2'])}")

# C2: vector sector reproduces Foster-Jacobson EXACTLY (both c2 signs) -- machinery vs literature
P("\n[C2] VECTOR sector reproduces Foster-Jacobson EXACTLY (literature cross-check):")
for kb in [R(1,4), R(1,10), R(1,100)]:
    c2healthy = -kb/(1-2*kb)         # EA c2=+c2*  (ACTION -c2*(divA)^2)
    rH = M.solve(kb, 10.0, R(1,5), 1.0, scalar_on=False, c2_val=c2healthy)
    rL = M.solve(kb, 10.0, R(1,5), 1.0, scalar_on=False, use_c2star=True)   # ACTION +c2* => EA c2=-c2*
    predL = 2*kb*(2*kb-1)/(2-kb)
    okH = rH[0]=='ok' and sp.simplify(rH[1]['alpha1']-(-4*kb))==0 and sp.simplify(rH[1]['alpha2'])==0
    okL = rL[0]=='ok' and sp.simplify(sp.nsimplify(rL[1]['alpha2'])-predL)==0
    ck(okH and okL, f"K_B={float(kb):.3g}: EA c2=+c2* -> a1=-4KB, a2=0 [{okH}]; "
       f"EA c2=-c2* -> a2={float(rL[1]['alpha2']):+.5f}=2KB(2KB-1)/(2-KB) [{okL}]")

# C3: healthy-corner cone speeds (Foster-Jacobson): +c2* luminal, -c2* ghost
P("\n[C3] c2 sign & health (Foster-Jacobson cone speeds), K_B=1e-3:")
kb = R(1,1000); cs = kb/(1-2*kb)
def spd(c2):
    c1,c3,c4=kb,-kb,sp.S(0); c13,c14,c123=c1+c3,c1+c4,c1+c2+c3
    return (sp.simplify((c123*(2-c14))/(c14*(1-c13)*(2+c13+3*c2))),   # s0^2
            sp.simplify(-4*kb/2-((c1+2*c3-c4)*(2*c1+3*c2+c3+c4))/(c123*(2-c14))))  # alpha2
s0p, a2p = spd(cs); s0m, a2m = spd(-cs)
ck(a2p == 0 and s0p == 1, f"EA c2=+c2* (ACTION -c2*): s0^2={s0p} (luminal), alpha_2^EA={a2p} -> HEALTHY corner")
ck(s0m < 0, f"EA c2=-c2* (ACTION +c2*, the literal brief sign): s0^2={float(s0m):.4f}<0 -> SPIN-0 GHOST")

# C4: static scalar sector validated: H00_on/H00_off = 1+1/J_Y (AeST quasi-static enhancement)
P("\n[C4] static scalar sector: H00(scalar on)/H00(off) = 1 + 1/J_Y  (known AeST quasi-static):")
kb = R(1,10); c2v = -kb/(1-2*kb)
for jy in [R(1), R(2), R(4)]:
    ron = M.solve(kb, R(1,1000000), R(1,1000), jy, scalar_on=True, c2_val=c2v)
    roff = M.solve(kb, 10.0, R(1,1000), jy, scalar_on=False, c2_val=c2v)
    ratio = float(sp.simplify(ron[1]['H00s']/roff[1]['H00s']))
    ck(abs(ratio-(1+1/float(jy))) < 1e-4, f"J_Y={float(jy):.0f}: H00on/off={ratio:.5f} = 1+1/J_Y={1+1/float(jy):.5f}")

# C5: J-coupling toggle isolates the whole effect
P("\n[C5] the 2(2-K_B)J.grad(phi) acceleration coupling IS the whole preferred-frame effect:")
kb = R(1,100); jy = R(2); k2 = (2-kb)*(1+kb*jy/2)/kb; c2v = -kb/(1-2*kb)
rOn = M.solve(kb, k2, R(1,1000), jy, scalar_on=True, c2_val=c2v, Jcoup=1)
rOff = M.solve(kb, k2, R(1,1000), jy, scalar_on=True, c2_val=c2v, Jcoup=0)
ck(abs(float(rOff[1]['alpha1'])-(-4*float(kb))) < 5e-3 and abs(float(rOff[1]['alpha2'])) < 5e-2,
   f"J-coupling OFF: alpha_1={float(rOff[1]['alpha1']):+.4f}(=-4KB={-4*float(kb):+.4f}), "
   f"alpha_2={float(rOff[1]['alpha2']):+.2e}(~0) -- scalar decouples from preferred frame w/o J-coupling")
ck(abs(float(rOn[1]['alpha2'])) > 10,
   f"J-coupling ON : alpha_1={float(rOn[1]['alpha1']):+.4f},  alpha_2={float(rOn[1]['alpha2']):+.4f} (huge)")

# C6: the 1/K_B POLE + decomposition
P("\n[C6] Delta alpha_2^(phiA) DIVERGES as 1/K_B (healthy corner, beta_0=0.5=J_Y2, c_s^2=1):")
resid = []
for kb in [R(1,50), R(1,200), R(1,1000)]:
    jy = R(2); k2 = (2-kb)*(1+kb*jy/2)/kb; c2v = -kb/(1-2*kb)
    rv = M.solve(kb, k2, R(1,1000), jy, scalar_on=False, c2_val=c2v)
    rf = M.solve(kb, k2, R(1,1000), jy, scalar_on=True, c2_val=c2v)
    a2EA = float(rv[1]['alpha2']); a2full = float(rf[1]['alpha2']); C = a2full*float(kb)
    resid.append(C)
    P(f"      K_B={float(kb):.4g}: alpha_2^EA={a2EA:+.1e}  Delta alpha_2^(phiA)={a2full:+.4e}  "
      f"[x K_B = {C:.4f} -> 4/(JY(1+JY))=0.667]")
ck(all(abs(c-R(2,3)) < 0.05 for c in resid), "alpha_2*K_B -> 0.667=4/(J_Y(1+J_Y)) (genuine simple pole in K_B)")

# C7: beta_0 scaling
P("\n[C7] beta_0-scaling of the residue C=alpha_2*K_B ~ 4/(J_Y(1+J_Y)) = 4 beta_0^2/(1+beta_0):")
kb = R(1,500)
for jy in [R(1), R(2), R(5), R(20)]:
    k2 = (2-kb)*(1+kb*jy/2)/kb; c2v = -kb/(1-2*kb)
    r = M.solve(kb, k2, R(1,1000), jy, scalar_on=True, c2_val=c2v)
    C = float(r[1]['alpha2'])*float(kb); pred = 4/(float(jy)*(1+float(jy)))
    P(f"      J_Y={float(jy):5.0f} (beta_0={1/float(jy):.3g}): C={C:.5f}  pred 4/(JY(1+JY))={pred:.5f}  "
      f"alpha_1={float(r[1]['alpha1']):+.4f}(=-8/(1+JY)={-8/(1+float(jy)):+.4f})")

P("\n"+"="*96)
P(f"  {'ALL CERTIFICATES PASS' if not FAIL else 'FAILURES: '+str(FAIL)}   [t={time.time()-T0:.0f}s]")
P("  VERDICT: Delta alpha_2^(phiA) = 4/(J_Y(1+J_Y)) / K_B  DIVERGES as K_B->0.")
P("  At Cassini-forced UNSCREENED beta_0~0.3-0.5 (J_Y~2-3) and K_B<2.5e-5: |alpha_2| > 1e4 >> 1e-7 bound.")
P("  => FC-AeST + c2* DIES at the preferred-frame gate (alpha_2 AND alpha_1 both O(1)/divergent w/ scalar).")
import sys
sys.exit(0 if not FAIL else 1)
