"""CERTIFICATE: on the c_T=1 (c13=0, c3=-c1) locus, a luminal vector REQUIRES c4=0 (Maxwell).
Adjudicates two candidate PPN-zero corners for the AeST+c2 preferred-frame repair:
  Maxwell (c4=0, c2=K_B/(1-2K_B)): alpha_2=0, s0=s1=s2=1 (all cones luminal, HEALTHY).
  c4~-c1 : alpha_2=0 with smaller alpha_1, BUT s1^2=1.25e8 (vector ~1.1e4 c) + c14~1e-14 (strong coupling) = PATHOLOGICAL.
Identity: on c13=0, c3=-c1 => s1^2 = c1/c14, so s1^2=1 <=> c14=c1 <=> c4=0. c4=0 is the vector-health condition, not an artifact.
Standard Einstein-aether PPN + spin-speed formulas (Foster-Jacobson). sympy exact.
"""
import sympy as sp
ok=True
def chk(c,l):
    global ok
    print(f"  [{'ok' if c else 'FAIL'}] {l}");  ok=ok and bool(c)
def speeds(c1,c2,c3,c4):
    c1,c2,c3,c4=[sp.Float(x,40) for x in (c1,c2,c3,c4)]
    c13,c14,c123=c1+c3,c1+c4,c1+c2+c3
    a1=-8*(c3**2+c1*c4)/(2*c1-c1**2+c3**2)
    a2=a1/2-((c1+2*c3-c4)*(2*c1+3*c2+c3+c4))/(c123*(2-c14))
    s2=1/(1-c13); s1=(2*c1-c1**2+c3**2)/(2*c14*(1-c13)); s0=(c123*(2-c14))/(c14*(1-c13)*(2+c13+3*c2))
    return float(a1),float(a2),float(s2),float(s1),float(s0),float(c14)
KB=1e-5
a1,a2,s2,s1,s0,c14=speeds(KB,KB/(1-2*KB),-KB,0.0)
print(f"MAXWELL (c4=0): a1={a1:.2e} a2={a2:.2e} s2^2={s2:.6f} s1^2={s1:.4f} s0^2={s0:.6f} c14={c14:.1e}")
chk(abs(a2)<1e-15,"Maxwell alpha_2=0"); chk(abs(s1-1)<1e-6 and abs(s0-1)<1e-6 and abs(s2-1)<1e-6,"Maxwell s0=s1=s2=1 (all luminal, healthy)")
a1b,a2b,s2b,s1b,s0b,c14b=speeds(3e-6,2.55e-14,-3.0000000005e-6,-2.999999976e-6)
print(f"c4~-c1        : a1={a1b:.2e} a2={a2b:.2e} s2^2={s2b:.6f} s1^2={s1b:.4e} s0^2={s0b:.6f} c14={c14b:.1e}")
chk(s1b>1e6,"c4~-c1 vector s1^2>1e6 (PATHOLOGICAL superluminal ~1e4 c)"); chk(c14b<1e-13,"c4~-c1 c14->0 (strong coupling)")
# the identity s1^2=c1/c14 on c13=0,c3=-c1
c1s,c4s=sp.symbols('c1 c4',positive=True); c3s=-c1s; c14s=c1s+c4s
s1sym=sp.simplify((2*c1s-c1s**2+c3s**2)/(2*c14s*(1-(c1s+c3s))))
chk(sp.simplify(s1sym-c1s/c14s)==0,"IDENTITY on c13=0,c3=-c1: s1^2 = c1/c14  => luminal vector REQUIRES c4=0")
print("\nRESULT: Maxwell (c4=0) is the UNIQUE luminal-vector PPN-zero corner; c4!=0 breaks the vector. c4=0 is a HEALTH condition." if ok else "CHECK FAILED")
import sys; sys.exit(0 if ok else 1)
