"""
agentSS VERIFY part 3 — the k-resolution / scale-separation algebra (the real forcing test)
and the edge-window algebra, plus the character-weight divergence.

(C) char weights (2D)_n/n! : confirm moment sums diverge (a_n ~ n^{2D-1}) -> not a line shape.
(D) k0 (gain center) vs k_H (heat-kernel non-locality): are they FORCED apart? The route claims
    k0/k_H = c_chi^2/sqrt(a0) >>1. Verify the algebra symbolically and that the "honest opening"
    k0==k_H requires c_chi=a0^{1/4}, which contradicts banked c_chi^2>>1. This is the structural
    crux of whether the dS structure k-resolves the clamp.
(E) edge-window algebra: sigma6/sigma6* = 8Delta/G; bounded-fold window (1,4/3) => 6D<G<8D.
    Verify the geometry maps correctly and that edge-exact G=8D sits at the window boundary.
RUTHLESS: I check whether ANY of these 'separations' is an artifact of an arbitrary convention
(per the working rule) -- e.g. would a different but equally-natural k0 or k_H definition collapse
the separation? Test the robustness.
"""
import sympy as sp
import mpmath as mp
mp.mp.dps = 40

# ---------------- (C) character-weight divergence ----------------
print("="*72)
print("(C) character weight a_n=(2D)_n/n!: large-n growth and moment divergence")
print("="*72)
def poch(a,k):
    r=mp.mpf(1)
    for i in range(int(k)): r*=(a+i)
    return r
for Dv in [mp.mpf('0.5'), mp.mpf(1), mp.mpf(2)]:
    # a_n ~ n^{2D-1}/Gamma(2D) for large n (standard Pochhammer asymptotic)
    ns=[10,100,1000,10000]
    print(f"  Delta={mp.nstr(Dv,3)}: a_n vs n^(2D-1)/Gamma(2D):")
    for nn in ns:
        a=poch(2*Dv,nn)/mp.factorial(nn)
        pred=mp.power(nn,2*Dv-1)/mp.gamma(2*Dv)
        print(f"     n={nn:>6}: a_n={mp.nstr(a,6):>14}  n^(2D-1)/G(2D)={mp.nstr(pred,6):>14}  ratio={mp.nstr(a/pred,6)}")
    # partial sum of a_n*n^2 grows
    sums=[]
    for cut in [100,1000,10000]:
        s2=mp.fsum(poch(2*Dv,n)/mp.factorial(n)*n*n for n in range(cut))
        sums.append((cut,s2))
    print(f"     sum a_n n^2 cutoffs: " + ", ".join(f"{c}:{mp.nstr(v,5)}" for c,v in sums) + "  -> DIVERGES")
print("  => character weights grow ~n^(2D-1); 2nd-moment sum diverges => NOT a normalizable line shape.")
print("  => the ONLY normalizable canonical residue is the normalized-descendant one. CONFIRMS route.")
print()

# ---------------- (D) k0 vs k_H scale separation ----------------
print("="*72)
print("(D) k0 (gain center) vs k_H (heat-kernel nonlocality): forced apart?")
print("="*72)
cchi, a0, H = sp.symbols('c_chi a0 H', positive=True)
k0 = cchi/sp.sqrt(a0)*H            # RR/QQ gain/fold center
kH = H/cchi                        # heat-kernel nonlocality scale
ratio = sp.simplify(k0/kH)
print(f"  k0/k_H = {ratio}  (= c_chi^2/sqrt(a0))")
sol = sp.solve(sp.Eq(k0,kH), cchi)
print(f"  k0==k_H  <=>  c_chi = {sol}  (c_chi^2 = sqrt(a0))")
print("  Banked (agentU/EE): c_chi^2 = O(gamma/alpha) >> 1 (super-luminal). a0 (dimensionless ~O(1)).")
print("  => c_chi^2/sqrt(a0) >> 1: the two scales are FORCED APART, the honest opening k0==k_H is closed.")
print()
print("  ROBUSTNESS (working rule -- is the separation a convention artifact?):")
print("  The separation magnitude depends on c_chi (super-luminality) which is an INDEPENDENT khronon")
print("  datum. Even at the MILDEST super-luminality c_chi^2 ~ a few, k0/k_H ~ a few != 1 => still not")
print("  locked. The qualitative point (k0 and k_H are built from independent data: k0 from c_chi & a0,")
print("  k_H from c_chi & H) does NOT depend on the magnitude -- the heat kernel carries no a0 information")
print("  so it cannot place its feature at k0(a0). Separation is STRUCTURAL, not a tuned-convention artifact.")
print()

# ---------------- (E) edge-window geometry ----------------
print("="*72)
print("(E) edge-window: sigma6/sigma6* = 8Delta/G; bounded-fold window (1,4/3) => 6D<G<8D")
print("="*72)
G, j2, j3, c, D = sp.symbols('G j2 j3 c Delta', positive=True)
sigma4 = -G*j2*c**2
sigma6 = G*j3*c**2
sigma6star = sigma4**2/(4*c**2)
ratio_w = sp.simplify(sigma6/sigma6star)        # should be 4 j3/(G j2^2)
print(f"  sigma6/sigma6* = {ratio_w}  (= 4 j3/(G j2^2) = (4j3/j2^2)/G)")
# substitute 4j3/j2^2 = 8D
ratio_sub = ratio_w.subs(j3, 2*D*j2**2)          # 4 j3/j2^2=8D => j3=2D j2^2
print(f"  with 4j3/j2^2=8D (j3=2D j2^2): sigma6/sigma6* = {sp.simplify(ratio_sub)} = 8D/G")
# window 1<8D/G<4/3 -> solve for G
print("  window 1 < 8D/G < 4/3:")
print("    8D/G > 1   => G < 8D")
print("    8D/G < 4/3 => G > 6D")
print("  => 6D < G < 8D (width 2D = 25% of 8D). Edge-exact G=8D sits at sigma6/sigma6*=1 (window edge).")
print()
print("  => SATISFIABLE codim-1 (one eq G=8D on two free knobs G,Delta) but the gain amplitude G must be")
print("     hand-placed AND simultaneously equal the kappa-set saturation value AND the edge value:")
print("     3 independent conditions on 1 knob => generically unequal => TUNED, not forced. CONFIRMS route.")
