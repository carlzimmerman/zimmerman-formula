"""
agentOO Route 2 — Block 6: the HOSTILE cross-check. When the GH moments don't converge, a
physical UV cutoff Lambda makes them finite. Does the CUTOFF-regularized GH bath still bend
(sigma4<0), and is the stabilizer healthy (sigma6>0)? This is the both-ways-honesty test:
maybe the framework is rescued by a cutoff even though the bath is featureless.

From Block 3a (EXACT, convention-free):
   sigma4 = -I2 * c_chi^2 ,  I2=int J/W^4 >0  =>  sigma4<0 WHENEVER I2 is finite & positive.
   sigma6 = c_chi^2 (I2^2 - I3 c_chi^2).
So the SIGN of sigma4 is robustly NEGATIVE for ANY positive (passive) J once regularized -- the
LEVEL-REPULSION bend survives a cutoff. The featurelessness does NOT flip sigma4's sign; it
makes its MAGNITUDE and the FOLD LOCATION cutoff-controlled (not bath-controlled). We quantify:
  (a) sigma4 with a cutoff: sign and Lambda-dependence;
  (b) sigma6 sign: is the +k^6 floor present (I2^2 > I3 c_chi^2) or is sigma6<0 (fold unbounded)?
  (c) WHERE the induced inflection omega''(k*)=0 sits, and whether it is TIED to the sonic edge
      b->c_chi or FREE (set by the cutoff). This is fold_at_edge.
"""
import mpmath as mp
mp.mp.dps = 30

print("="*78)
print("BLOCK 6: cutoff-regularized GH moments -- sigma4 sign, sigma6 floor, fold location")
print("="*78)

H = mp.mpf(1)  # set GH scale to 1
def J(W, p):           # GH spectral density, coupling power p
    W = mp.mpf(W)
    return W**p * mp.coth(mp.pi*W/H)
def Imom(n, p, eps, Lam):  # I_n = int_eps^Lam J/W^(2n) dW
    return mp.quad(lambda W: J(W,p)/W**(2*n), [eps, Lam])

eps = mp.mpf('1e-4')   # IR regulator (a physical IR scale, e.g. box/horizon)
print("\nGH coupling p=2 (canonical 2-derivative form factor), IR eps=1e-4, scan UV cutoff Lambda:")
print(f"{'Lambda':>8} {'I1':>12} {'I2':>12} {'I3':>12} {'sigma4/cchi2':>14} {'sigma6sign':>11}")
p = 2
# Take c0^2=1 (bare). c_chi^2 = c0^2 - I1 (must stay >0 -> coupling must be perturbative).
# We report sigma4/c_chi^2 = -I2 (sign), and sigma6 sign = sign(I2^2 - I3 c_chi^2).
for Lam in [mp.mpf(x) for x in [2,5,10,30,100,1000]]:
    I1 = Imom(1,p,eps,Lam); I2 = Imom(2,p,eps,Lam); I3 = Imom(3,p,eps,Lam)
    c0sq = mp.mpf(1)
    # choose coupling small enough that c_chi^2>0; rescale J by a small g^2 so I1<c0^2.
    # report sign structure independent of overall g^2 (sigma4 sign = -sign(I2) always):
    cchi2 = c0sq - mp.mpf('0.0')  # sign of sigma4 doesn't need cchi2 value; it's -I2*cchi2, cchi2>0
    s4_over = -I2  # sign of sigma4 / (cchi2>0)
    s6sign = mp.sign(I2**2 - I3*1.0)  # placeholder cchi2=1 for sign illustration
    print(f"{mp.nstr(Lam,4):>8} {mp.nstr(I1,4):>12} {mp.nstr(I2,4):>12} {mp.nstr(I3,4):>12} "
          f"{mp.nstr(s4_over,4):>14} {int(s6sign):>11}")

print("""
READING:
  * sigma4 = -I2 * c_chi^2 < 0 for EVERY cutoff (I2>0 always). The cutoff-regularized GH bath
    DOES bend: sigma4 is robustly NEGATIVE. The featurelessness did NOT flip the bending sign --
    it only makes the magnitude scale with the UV cutoff (I2 grows with Lambda for p=2 since the
    UV end p-2n = 2-4 = -2 <-1 converges; here actually IR-controlled). The level-repulsion bend
    is the GENERIC sign of integrating out ANY passive bath.
  * BUT: I2 (hence sigma4 magnitude) and I3 are CUTOFF/IR-endpoint controlled, NOT set by any
    bath resonance. So the FOLD SCALE k* (where omega''=0) is fixed by the cutoff, NOT by H and
    NOT by the sonic edge. fold_at_edge = FREE (cutoff-set), not pinned to b->c_chi.
""")

print("="*78)
print("BLOCK 6b: the fold location k* and whether it lands at the sonic edge b->c_chi")
print("="*78)
print("""
omega_eff^2(k) = c_chi^2 k^2 + sigma4 k^4 + sigma6 k^6,  sigma4<0 (bend), sigma6 the floor.
Define the GROUP-velocity/curvature fold from omega(k)=sqrt(omega_eff^2). The inflection
omega''(k*)=0 occurs at a k* set by the ratio |sigma4|/sigma6 and c_chi^2 -- i.e. by the bath
MOMENTS I2,I3, which are CUTOFF-controlled. The sonic edge b->c_chi is a property of the
khronon SOUND HORIZON (where the group velocity equals c_chi), an INDEPENDENT condition.
For the Airy generator NN requires omega''(k*)=0 to COINCIDE with the b->c_chi edge frequency.
""")
# Demonstrate the fold exists for sigma4<0, sigma6>0, and that k* depends on coefficients freely.
def fold_k(cchi2, s4, s6):
    # omega^2 = cchi2 k^2 + s4 k^4 + s6 k^6 ; omega=sqrt(.) ; find omega''=0
    f = lambda k: mp.sqrt(cchi2*k**2 + s4*k**4 + s6*k**6)
    def fpp(k):
        h=mp.mpf('1e-6')
        return (f(k+h)-2*f(k)+f(k-h))/h**2
    try:
        return mp.findroot(fpp, mp.mpf('1.0'))
    except Exception:
        return None
for (s4,s6) in [(-0.2,0.1),(-0.5,0.3),(-1.0,0.5),(-0.2,0.5)]:
    kk = fold_k(1.0, s4, s6)
    print(f"  c_chi^2=1, sigma4={s4}, sigma6={s6}:  fold k* = {mp.nstr(kk,6) if kk else 'none'}")
print("""
  => k* MOVES with the (cutoff-controlled) ratio sigma4/sigma6. Nothing ties it to b->c_chi.
  fold_at_edge: the inflection location is FREE (set by the UV cutoff / coupling), NOT pinned
  to the sonic edge. NN's 'edge-coincidence' tuning (condition 2) is therefore NOT supplied by
  the dS spectrum -- it remains an undischarged tuning. The dS bath gives (at best, with a
  cutoff) a bend at the WRONG, cutoff-set scale, not at the sonic horizon.
""")
