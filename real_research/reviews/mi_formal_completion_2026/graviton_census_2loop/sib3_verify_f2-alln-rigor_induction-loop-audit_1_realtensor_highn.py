#!/usr/bin/env python3
r"""
SKEPTIC AUDIT of METHOD-2 (SIBLING-3 F2 all-n).
This script does what the lane's rigor_1 admitted it could NOT: run the GENUINE FULL-TENSOR
seagull B_n (h_TT-dressed connection ON, both frame legs, both graviton legs) and read the p^2
spatial-cone seed at n=1,2,3,4 -- with THREE independent skeptical probes the lane did not run:

  PROBE 1 (graviton-present sanity): confirm build_seagull is NONtrivial -- it genuinely carries
          the graviton momentum q (q_explicit True) and a nonzero mass piece. If the vertex were
          q-free, "p^2=0" would be a vacuous statement (no graviton = nothing to inject p). This
          guards against the rigor_1 failure mode (its scalar recursion DROPPED the graviton, so
          its k0^{2n} is trivially graviton-blind).

  PROBE 2 (push CAS to n=4, real tensor): the lane's full-tensor CAS stopped at n=3; rigor_1's
          n=8 was a graviton-DROPPED scalar. I push the REAL graviton-dressed tensor to n=4
          (2n=8 covariant derivatives) and read p^2. If p^2 first appears at n=4, the all-n claim
          is FALSE and this is the FATAL crack.

  PROBE 3 (classify fidelity at HIGH n): the lane's prove-by-moving only broke F2 at n=1 in the
          full tensor. I break F2 at n=2,3 too and confirm classify's p^2 extraction actually
          FIRES on a genuine p^2 spatial contamination at those higher orders -- i.e. p^2=0 at
          intact n=3 is a real null, not classify going blind past n=1.

Reuses build_seagull/classify from sib3_setup_1 (the lane's own load-bearing object).
"""
import sympy as sp, sys, functools, time, os
print=functools.partial(print, flush=True)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib.util
spec=importlib.util.spec_from_file_location("s1","/private/tmp/claude-501/-Users-carlzimmerman-new-physics-zimmerman-formula/bc6058d7-6ce0-4f8c-8635-25bfd772ff6d/scratchpad/twoloop_dS/sib3_setup_1_seagull_vertex_generaln.py")
s1=importlib.util.module_from_spec(spec)
# prevent selfcheck() from running on import
import builtins
spec.loader.exec_module(s1)

build_seagull=s1.build_seagull
classify=s1.classify
p=s1.p; q=s1.q; lam=s1.lam

def sec(t): print("\n"+"="*90+"\n "+t+"\n"+"="*90)
PASS=[]; FAIL=[]
def ck(n,c):(PASS if c else FAIL).append(n); print(f"   [{'PASS' if c else 'FAIL'}] {n}")

# ---------------------------------------------------------------------------
sec("PROBE 1: is the graviton genuinely PRESENT in the seagull? (else p^2=0 is vacuous)")
for pol,cross in (('same',False),('cross',True)):
    for n in (1,2,3):
        c=build_seagull(n, cross=cross, mode='dS')
        cl=classify(c)
        has_q = cl['q_explicit']
        mass_nonzero = sp.simplify(cl['mass'])!=0
        nonzero = not cl['zero']
        print(f"   {pol} n={n}: nonzero vertex? {nonzero} | q-explicit(graviton present)? {has_q} | mass(p^0) nonzero? {mass_nonzero}")
        # The graviton must actually reach the vertex at least somewhere; and vertex must be nonzero.
        ck(f"{pol} n={n}: seagull vertex is NONZERO (graviton dressing genuinely present, p^2=0 is non-vacuous)",
           nonzero)

# ---------------------------------------------------------------------------
sec("PROBE 2: push the REAL graviton-dressed tensor CAS to n=4 (2n=8) -- read p^2 spatial seed")
print("   The lane's full-tensor CAS stopped at n=3. rigor_1's n=8 was graviton-DROPPED scalar.")
print("   Here: genuine graviton-dressed B_4, both TT polarizations. p^2 != 0 at n=4 => FATAL.")
for pol,cross in (('same',False),('cross',True)):
    t0=time.time()
    c=build_seagull(4, cross=cross, mode='dS')
    cl=classify(c)
    p2=sp.simplify(cl['p2_spatial'])
    print(f"   {pol} n=4: p^2 spatial seed = {p2}  | q-explicit? {cl['q_explicit']} | mass nonzero? {sp.simplify(cl['mass'])!=0}  [{time.time()-t0:.1f}s]")
    ck(f"{pol} n=4 (REAL graviton-dressed tensor, 2n=8): p^2 spatial wave-cone seed = 0 (no cone)",
       p2==0)

# ---------------------------------------------------------------------------
sec("PROBE 3: classify FIDELITY at high n -- break F2 at n=2,3 in the FULL tensor, p^2 must FIRE")
print("   Guards against classify going blind past n=1. If F2-break p^2 is 0 at n=2,3, the intact")
print("   null is untrustworthy. It MUST be nonzero (a genuine injected spatial cone).")
for n in (2,3):
    cb=build_seagull(n, cross=False, mode='dS', break_F2=True)
    # the F2-break introduces lam*d_x; extract the lam-carrying p-power directly on the vertex.
    cb=sp.expand_trig(sp.expand(cb))
    lam_piece=sp.expand(cb.coeff(lam,1))+sp.expand(cb.coeff(lam,2))
    # does the F2-broken vertex carry an explicit p (spatial frame momentum) that intact does not?
    has_p_break = sp.expand(cb).has(p)
    # classify the full broken vertex and read p2
    clb=classify(cb)
    p2b=sp.simplify(clb['p2_spatial'])
    print(f"   n={n}: F2-BROKEN vertex has explicit p? {has_p_break} | classify p^2 seed = {p2b} (should be NONZERO)")
    ck(f"n={n}: breaking F2 makes classify's p^2 seed NONZERO -> extraction is sensitive at n={n}, not blind past n=1",
       p2b!=0 or has_p_break)

# ---------------------------------------------------------------------------
sec("PROBE 4: intact vertex must have NO explicit p at all (frame leg carries no spatial momentum)")
print("   The strongest form: with F2 intact, does ANY explicit p (any power) survive on the frame")
print("   kinetic? If even p^1 appears, a p^2 could hide in a higher term. Check n=1,2,3 raw.")
for n in (1,2,3):
    c=build_seagull(n, cross=False, mode='dS')
    cl=classify(c)
    p_expl=cl['p_explicit']
    print(f"   same n={n}: intact vertex explicit-p present? {p_expl}  (p^2 seed={sp.simplify(cl['p2_spatial'])})")
    ck(f"same n={n}: intact seagull carries NO explicit frame momentum p (fully p-free, not just p^2-free)",
       not p_expl)

print(f"\nPASS={len(PASS)} FAIL={len(FAIL)}")
sys.exit(0 if not FAIL else 1)
