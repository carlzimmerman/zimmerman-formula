#!/usr/bin/env python3
r"""
CRITICAL DIAGNOSIS: setup_1's build_seagull output shows q-explicit=False at EVERY n.
The whole SIBLING-3 danger is the h_TT-dressed connection injecting the GRAVITON q_perp onto
the frame. If the extracted vertex is q-FREE, then "p^2=0" is verified on an object where the
graviton transverse momentum already vanished -- potentially VACUOUS.

This script dissects WHY q is absent, and whether it is:
  (a) a GENUINE physical fact (the seagull vertex really has no net q on the frame -- the two
      graviton legs' spatial derivatives cancel / never reach the frame index), which would make
      the p-free result meaningful, OR
  (b) an ARTIFACT of the frame leg u^y ~ cos(p x) having NO y-structure so the graviton's d_x
      (which lands via Gamma) hits cos(qx) but then the eps^2 eps2^2 projection drops it -- i.e.
      the extraction throws away the very term that carries q, hiding a possible p^2.

Approach: build the raw B_n BEFORE the coeff() projection, and inspect the eps^2 eps2^2 piece
in full, looking for q-dependence and any p*q cross structure that classify might mis-bin.
"""
import sympy as sp, functools, importlib.util
print=functools.partial(print, flush=True)
spec=importlib.util.spec_from_file_location("s1","/private/tmp/claude-501/-Users-carlzimmerman-new-physics-zimmerman-formula/bc6058d7-6ce0-4f8c-8635-25bfd772ff6d/scratchpad/twoloop_dS/sib3_setup_1_seagull_vertex_generaln.py")
s1=importlib.util.module_from_spec(spec); spec.loader.exec_module(s1)
build=s1.build; Bn=s1.Bn; trunc=s1.trunc
eps=s1.eps; eps2=s1.eps2; p=s1.p; q=s1.q
t,x,y,z=s1.t,s1.x,s1.y,s1.z

def sec(s): print("\n"+"="*88+"\n "+s+"\n"+"="*88)

# Build the pieces for n=1 (cheap) and inspect.
g,u_low,u_up,G=build(cross=False, mode='dS')

sec("Does the h_TT-dressed connection G carry q at all? (sanity: graviton spatial momentum exists)")
qcount=0
for l in range(4):
    for a in range(4):
        for b in range(4):
            e=sp.expand(G[l][a][b])
            if e.has(q):
                qcount+=1
print(f"   # Christoffel components carrying explicit q (via d_x h ~ q sin qx): {qcount}")
print(f"   -> the graviton q IS in the connection: {qcount>0}")

sec("Raw B_1 (full, before eps^2 eps2^2 projection): does the eps^2 eps2^2 piece carry q?")
B1=Bn(1,g,u_low,u_up,G)
c=sp.expand(B1.coeff(eps,2).coeff(eps2,2))
print("   eps^2 eps2^2 coefficient of B_1 (the seagull vertex):")
print("   ", c)
print(f"\n   Does this seagull vertex carry explicit q? {sp.expand(c).has(q)}")
print(f"   Does it carry explicit p? {sp.expand(c).has(p)}")

sec("WHERE did q go? Inspect the eps^1 eps2^2 and eps^2 eps2^1 and eps^0 eps2^2 pieces")
for (ie,ie2) in [(0,2),(1,2),(2,1),(2,0),(1,1)]:
    piece=sp.expand(B1.coeff(eps,ie).coeff(eps2,ie2))
    print(f"   eps^{ie} eps2^{ie2}: has q? {piece.has(q)} | has p? {piece.has(p)} | zero? {piece==0}")

sec("KEY TEST: does the seagull vertex depend on the graviton at all? Set H_TT -> 0 vs nonzero")
# if the eps^2 eps2^2 piece is nonzero, the graviton legs ARE there (H_TT^2). Check it's not
# secretly independent of H_TT (which would mean no graviton).
HTT=sp.Function('H_TT')(t)
has_HTT = sp.expand(c).has(sp.Function('H_TT')) or sp.expand(c).has(HTT)
print(f"   seagull vertex depends on H_TT (graviton amplitude)? {has_HTT}")
print("   If True but q-free: the graviton reaches the frame via TIME derivatives (H_TT'(t)),")
print("   NOT spatial q -- the q_perp is NOT delivered to the frame at all. That would be the")
print("   PHYSICAL reason p^2=0: no q_perp arrives, so no p^2 can be built. Need to confirm this.")

sec("Is the q-cancellation genuine, or does the frame leg's cos(p x) block q from arriving?")
# The frame leg u^y = V cos(p x). The graviton phase is cos(q x). A spatial derivative d_x on the
# graviton gives q sin(qx). For that q to reach the frame KINETIC it must multiply the frame leg
# and survive the u.(...)u contraction. Let's see if ANY q-carrying term appears in the full B_1
# at eps^2 eps2^2 BEFORE trig-averaging.
print("   Full raw eps^2 eps2^2 term list (each additive piece), scanning for q:")
terms=sp.Add.make_args(sp.expand(c))
qterms=[tt for tt in terms if tt.has(q)]
print(f"   total additive terms: {len(terms)} | terms carrying q: {len(qterms)}")
if qterms:
    for tt in qterms[:6]:
        print("     q-term:", tt)
else:
    print("   >>> NO q-carrying term survives in the seagull vertex. The graviton's spatial")
    print("   >>> momentum q_perp is NOT delivered to the du_perp frame kinetic AT ALL.")
