#!/usr/bin/env python3
r"""SKEPTIC HUNT part 2: (a) n=4 cross-pol (timed out before), (b) PROVE-BY-MOVING F2-break at
HIGH n=4 (the crucial sensitivity check -- does the mechanism actually detect a cone at high n?),
(c) attempt n=5 same-pol. Same independent raw p-extraction as MINE.py."""
import sympy as sp, functools, time, importlib.util, os, sys
print=functools.partial(print, flush=True)
spec=importlib.util.spec_from_file_location('s1','sib3_setup_1_seagull_vertex_generaln.py')
s1=importlib.util.module_from_spec(spec); spec.loader.exec_module(s1)
x,p,q=s1.x,s1.p,s1.q

def raw_p_report(c):
    c=sp.expand_trig(sp.expand(c))
    has_sin_px=c.has(sp.sin(p*x))
    Cp,Cq=sp.symbols('Cp Cq',real=True)
    def rp(e): return Cp*Cq if (e.func in (sp.cos,sp.sin) and e.args[0].has(x)) else e
    cN=sp.expand(c.replace(lambda e:e.func in (sp.cos,sp.sin) and e.args[0].has(x), rp))
    has_alg_p=cN.has(p)
    if has_alg_p:
        pp=sp.Poly(cN,p); powers=sorted(set(m[0] for m in pp.monoms())); p2=sp.simplify(pp.nth(2))
    else: powers=[0]; p2=sp.Integer(0)
    return has_alg_p,sp.simplify(p2),powers,has_sin_px

job=os.environ.get('SIB3_JOB','cross4')
if job=='cross4':
    t0=time.time(); c=s1.build_seagull(4,cross=True,mode='dS')
    r=raw_p_report(c)
    print(f"n=4 CROSS: p^2={r[1]} | algebraic p? {r[0]} | powers={r[2]} | sin(px)? {r[3]} [{time.time()-t0:.1f}s]")
elif job=='break4':
    # F2-BROKEN at n=4: must show algebraic p / p^2 ON (mechanism live at high n)
    t0=time.time(); cb=s1.build_seagull(4,cross=False,mode='dS',break_F2=True)
    r=raw_p_report(cb)
    print(f"n=4 F2-BROKEN: algebraic p? {r[0]} | p^2 coeff nonzero? {sp.simplify(r[1])!=0} "
          f"| powers={r[2]} | sin(px)? {r[3]} [{time.time()-t0:.1f}s]")
elif job=='same5':
    t0=time.time(); c=s1.build_seagull(5,cross=False,mode='dS')
    r=raw_p_report(c)
    print(f"n=5 SAME: p^2={r[1]} | algebraic p? {r[0]} | powers={r[2]} | sin(px)? {r[3]} [{time.time()-t0:.1f}s]")
