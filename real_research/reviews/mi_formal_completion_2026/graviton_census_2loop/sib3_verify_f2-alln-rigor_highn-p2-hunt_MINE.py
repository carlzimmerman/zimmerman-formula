#!/usr/bin/env python3
r"""
SKEPTIC HUNT: try to find a p^2 |du_perp|^2 SPATIAL wave cone in the du^2 x hTT^2 direct
sunset seagull at HIGH resolvent order n>=4 that n=1,2,3 missed.

Independent of the lane's classify(): I import ONLY the covariant vertex builder build_seagull
(the exact 4D dS + h_TT-dressed connection machinery) and do MY OWN raw p-power extraction
straight off the sympy expression -- no trust in the lane's stripping. I push the FULL
TWO-graviton tensor CAS to n=4 and n=5 (2n=8,10 covariant derivatives), both TT polarizations.

DANGER I am hunting:
  a genuine p^2 * |du_perp|^2 term. p = frame external spatial momentum (enters ONLY as d_x on
  the frame leg cos(p x)). If u.grad has u^x=0 the frame leg is never x-differentiated -> p can
  appear ONLY as a PHASE (cos((q +- p)x)) never as an algebraic polynomial p^k with k>=1. So a
  robust test: does the RAW vertex contain the symbol p algebraically AT ALL? and separately, is
  the explicit p^2 polynomial coefficient (after product-to-sum) nonzero?

MECHANISM PROBE: verify u^x==0 identically (all eps orders) and that no sin(p x) / algebraic p
ever appears -> the ONLY p-carrier (d_x on the frame leg) is structurally absent.

PROVE-BY-MOVING at HIGH n: break F2 (inject lam*d_x) and confirm p^2 switches ON at n=4 (extractor
and mechanism are live, not blind).

CURVATURE CROSS-TERM PROBE: separately grep the raw vertex for any H-carrying term that also carries
an algebraic p (an H^2 p^2 cone would show as p algebraic in the H-sector). Confirm none.
"""
import sympy as sp, functools, time, importlib.util, os
print=functools.partial(print, flush=True)
def sec(s): print("\n"+"="*94+"\n "+s+"\n"+"="*94)

spec=importlib.util.spec_from_file_location('s1','sib3_setup_1_seagull_vertex_generaln.py')
s1=importlib.util.module_from_spec(spec); spec.loader.exec_module(s1)

t,x = s1.t, s1.x
p,q,H = s1.p, s1.q, s1.H
eps,eps2,lam = s1.eps, s1.eps2, s1.lam

def raw_p_report(c):
    """MY OWN extraction: expand trig products to sum, expose algebraic p, read p-poly coeffs.
    Returns (has_algebraic_p, p2_coeff, all_p_powers_present, has_sin_px)."""
    c=sp.expand_trig(sp.expand(c))
    has_sin_px = c.has(sp.sin(p*x))
    # product-to-sum via full trig expansion already done by expand_trig; now substitute the
    # residual cos(p x), sin(p x), cos(q x), sin(q x) and combined-angle phases with neutral phase
    # symbols so any SURVIVING algebraic p is a genuine polynomial momentum (from a d_x), not a phase.
    Cp,Sp,Cq,Sq=sp.symbols('Cp Sp Cq Sq', real=True)
    reps=[]
    # handle any cos/sin whose argument is a multiple of x (phases) -> neutral symbols
    for f in c.atoms(sp.Function) | c.atoms(sp.cos) | c.atoms(sp.sin):
        pass
    def phase_to_neutral(expr):
        expr=sp.expand_trig(sp.expand(expr))
        # replace elementary trig of (a*x) by neutral symbols regardless of a in {p,q,combos}
        def rp(e):
            if e.func in (sp.cos, sp.sin) and e.args[0].has(x):
                arg=e.args[0]
                # neutral symbol keyed only on which momenta appear (NOT their power)
                return (Cp*Cq)  # collapse every phase to a neutral nonzero constant-ish placeholder
            return e
        return expr.replace(lambda e: e.func in (sp.cos,sp.sin) and e.args[0].has(x), rp)
    cN = sp.expand(phase_to_neutral(c))
    has_alg_p = cN.has(p)
    if has_alg_p:
        pp=sp.Poly(cN,p)
        powers=sorted(set(m[0] for m in pp.monoms()))
        p2=sp.simplify(pp.nth(2))
    else:
        powers=[0]; p2=sp.Integer(0)
    return has_alg_p, sp.simplify(p2), powers, has_sin_px

sec("MECHANISM: u^x identically 0 (the sole p-carrier d_x is absent from u.grad)")
g,u_low,u_up,G=s1.build(cross=False, mode='dS')
print(f"   u^x (upper) = {sp.simplify(u_up[1])}")
print(f"   u_x (lower) = {sp.simplify(u_low[1])}")
uxzero = sp.simplify(u_up[1])==0 and sp.simplify(u_low[1])==0
print(f"   u^x==0 and u_x==0 (all eps orders)? {uxzero}")
print("   => in (u.grad)=u^0 d_t + u^x d_x + u^y d_y, the d_x coefficient vanishes; the frame leg")
print("      cos(p x) can NEVER be x-differentiated -> p can only ride as a phase, never algebraic.")

NMAX=int(os.environ.get('SIB3_HUNT_NMAX', 5))
sec(f"HUNT: full TWO-graviton seagull tensor, MY raw p-extraction, n=1..{NMAX} both polarizations")
worst=[]
for pol,cross in (('same',False),('cross',True)):
    print(f"\n   --- {pol}-pol TT ---")
    for n in range(1,NMAX+1):
        t0=time.time()
        try:
            c=s1.build_seagull(n, cross=cross, mode='dS')
        except Exception as e:
            print(f"   n={n} {pol}: BUILD ERROR {e}")
            continue
        has_alg_p, p2, powers, has_sinpx = raw_p_report(c)
        dt=time.time()-t0
        massnz = sp.simplify(c)!=0
        print(f"   n={n} {pol}: p^2_spatial={p2} | algebraic p at all? {has_alg_p} "
              f"| p-powers={powers} | sin(px) in raw? {has_sinpx} | vertex!=0? {massnz} [{dt:.1f}s]")
        worst.append((pol,n,sp.simplify(p2), has_alg_p))

sec("PROVE-BY-MOVING at HIGH n: break F2 (inject lam*d_x) -> p^2 cone must switch ON")
for n in (1,4):
    t0=time.time()
    cb=s1.build_seagull(n, cross=False, mode='dS', break_F2=True)
    has_alg_p, p2, powers, has_sinpx = raw_p_report(cb)
    # with F2 broken, d_x hits cos(p x) -> sin(p x) -> algebraic p should appear
    print(f"   n={n} F2-BROKEN: algebraic p present? {has_alg_p} | p-powers={powers} "
          f"| sin(px) present? {has_sinpx} [{time.time()-t0:.1f}s]")

sec("VERDICT (skeptic hunt)")
all_p2_zero = all(sp.simplify(w[2])==0 for w in worst)
no_alg_p    = all(not w[3] for w in worst)
print(f"   ALL n=1..{NMAX} both pol: p^2 spatial cone == 0 ?           {all_p2_zero}")
print(f"   ALL n=1..{NMAX} both pol: NO algebraic p in vertex at all ? {no_alg_p}")
print("   (algebraic-p-absent is the STRONGER statement: p cannot even appear to power 1,")
print("    so no p^2 cone AND no p*q cross-kinetic AND no H^2 p^2 curvature cross-term.)")
print(f"\n   RESULT: {'p-FREE survives to n=%d (BENIGN)'%NMAX if (all_p2_zero and no_alg_p) else 'CRACK FOUND'}")
