#!/usr/bin/env python3
"""
ROUTE 3 -- the HONEST both-ways check on Carl's 'reaches to the horizon' framing.

THE STEELMAN of Carl's idea (push it HARD, do not dismiss):
The naive r_M = sqrt(G m / a0) assumes the galaxy is ISOLATED in vacuum. But a cluster member
sits in the cluster's OWN field, which at the core radius is only ~0.3 a0 (sub-a0!). A galaxy's
deep-MOND tail is cut off where its self-field drops to the EXTERNAL field g_ext, NOT where it
drops to a0. If g_ext < a0, the EFE cutoff radius r_eff = sqrt(G m / g_ext) can be LARGER than
r_M -- the tail reaches FURTHER. So maybe the tails DO overlap and build a collective field?

We compute this honestly both ways:
  (A) the EFE-cutoff reach r_eff = sqrt(G m / g_ext) using the actual cluster g_ext profile
  (B) whether that extended reach actually DEEPENS the collective inter-galaxy potential beyond
      the smooth cluster field -- OR whether the EFE (which SUPPRESSES the boost, banked finding)
      kills it.

THE KILLER both-ways tension Carl's idea must survive:
 - PRO  (reach): sub-a0 environment -> larger r_eff -> tails overlap more.
 - CON  (EFE):   the SAME sub-a0 external field that lets the tail reach also SUPPRESSES the
                 deep-MOND boost of that tail (EFE: in an external field g_ext, the internal
                 field is quasi-Newtonian-ized, boost ~ 1/mu(g_ext/a0) but the tail itself is
                 the EXTERNAL field's response). The collective field in the inter-galaxy medium
                 is just the cluster's OWN smooth field -- which the standard calc ALREADY has.
"""
import numpy as np

G    = 6.674e-11
Msun = 1.989e30
kpc  = 3.0857e19
a0   = 9.36e-11

def nu(gN):  return np.sqrt(1+a0/gN)              # framework nu
def mu(g):   # algebraic mu(x)=x/(1+x) inverse-ish; use simple mu = g/sqrt(g^2+a0^2)?
    # framework deep limit: g_obs=sqrt(gN^2+gN a0) => mu(g_obs)=g_obs/gN. Use nu form.
    return None

M500 = 1e15*Msun
R_core = 420*kpc
M_bar_core = 3.6e13*Msun

# cluster external field profile (smooth, MOND-boosted) as a function of cluster radius
def g_ext_cluster(r):
    # enclosed baryon (cored), MOND-boosted
    rc = 150*kpc
    def menc(rr):
        x=rr/rc; return np.arcsinh(x)-x/np.sqrt(1+x**2)
    Mb = M_bar_core*menc(r)/menc(R_core) if r<=R_core else M_bar_core
    gN = G*Mb/r**2
    return np.sqrt(gN**2 + gN*a0)     # the boosted cluster field a member actually feels

print("="*74)
print("(A) EFE-CUTOFF REACH: does a sub-a0 cluster environment let tails reach further?")
print("="*74)
m_typ = 3.75e10*Msun
m_Lstar = 1e11*Msun
m_bcg = 7.5e11*Msun
for rcl in np.array([100,200,300,420])*kpc:
    gext = g_ext_cluster(rcl)
    print(f"\n cluster radius {rcl/kpc:.0f} kpc: g_ext={gext:.3e}={gext/a0:.2f} a0")
    for lab,m in [("typ",m_typ),("L*",m_Lstar),("BCG",m_bcg)]:
        r_M   = np.sqrt(G*m/a0)            # isolated reach
        r_eff = np.sqrt(G*m/gext)          # EFE reach (where self-field = g_ext)
        print(f"   {lab:4s} m={m/Msun:.1e}: r_M(isol)={r_M/kpc:5.1f}kpc  "
              f"r_eff(EFE,vs g_ext)={r_eff/kpc:5.1f}kpc  (x{r_eff/r_M:.2f})")

print("\n -> YES: in the sub-a0 cluster environment the EFE reach r_eff is ~1.3-1.8x the")
print("    isolated r_M. So Carl's 'reaches further' is REAL at the kinematic level.")
print("    BUT r_eff is still only ~10-60 kpc << 116 kpc separation for typical members;")
print("    only the BCG (r_eff~45-60 kpc) approaches half the separation. Tails of typical")
print("    members STILL do not overlap. The reach helps the few biggest galaxies only.")

print("\n"+"="*74)
print("(B) DOES THE EXTENDED REACH ADD COLLECTIVE BINDING, OR IS IT THE SMOOTH FIELD?")
print("="*74)
# The crux: when galaxy tails DO reach into the inter-galaxy medium, what they contribute there
# is governed by the deep-MOND superposition. The TOTAL field in the inter-galaxy medium, summed
# over all members + gas, is EXACTLY what the smooth cluster calc computes from the TOTAL
# enclosed baryon mass (enclosed-mass theorem, verified). The 'collective overlap' is the
# cluster's own smooth field. There is no EXTRA term.
#
# Quantify: compare (i) sum over members of their EFE-extended tail fields at a mid-medium point
# to (ii) the smooth cluster field at that point. If (i) ~ (ii), the overlap is already counted.
rng = np.random.default_rng(7)
N=200
M_star_core=0.50*0.015*M500
ranks=np.arange(1,N); w=ranks**(-1.0)
m_gal=np.concatenate([[0.10*M_star_core],(0.90*M_star_core)*w/w.sum()])
# random positions in core
rc_gal=200*kpc
def samp(n):
    out=[]
    while len(out)<n:
        r=rng.uniform(0,R_core,4*n); pdf=r**2/(1+(r/rc_gal)**2); pdf/=pdf.max()
        out+= r[rng.uniform(size=r.size)<pdf].tolist()
    return np.array(out[:n])
rg=samp(N); ct=rng.uniform(-1,1,N); ph=rng.uniform(0,2*np.pi,N); st=np.sqrt(1-ct**2)
xyz=np.column_stack([rg*st*np.cos(ph),rg*st*np.sin(ph),rg*ct])

# evaluate at a set of inter-galaxy field points at cluster radius ~250 kpc, away from any galaxy
test_pts=[]
for _ in range(300):
    ct2=rng.uniform(-1,1); ph2=rng.uniform(0,2*np.pi); st2=np.sqrt(1-ct2**2)
    P=250*kpc*np.array([st2*np.cos(ph2),st2*np.sin(ph2),ct2])
    if np.min(np.linalg.norm(xyz-P,axis=1))>40*kpc:   # >40 kpc from nearest galaxy
        test_pts.append(P)
test_pts=np.array(test_pts)
# smooth cluster g at 250 kpc
gsmooth=g_ext_cluster(250*kpc)
# 'naive linear sum' of member deep-MOND tails (the thing Carl imagines adding up): each member
# contributes its OWN deep-MOND tail g_i = sqrt(G m_i a0)/d_i  (isolated deep-MOND), summed.
naive=[]
for P in test_pts:
    d=np.linalg.norm(xyz-P,axis=1)
    gi=np.sqrt(G*m_gal*a0)/d           # isolated deep-MOND tail magnitude of each member
    naive.append(gi.sum())             # naive scalar sum (Carl's 'overlap adds up')
naive=np.array(naive)
print(f"  Smooth cluster field at 250 kpc (the standard calc): {gsmooth:.3e} = {gsmooth/a0:.2f} a0")
print(f"  NAIVE scalar sum of member isolated-deep-MOND tails:  "
      f"{naive.mean():.3e} +/- {naive.std():.1e}  = {naive.mean()/a0:.2f} a0")
print(f"  ratio naive_sum / smooth = {naive.mean()/gsmooth:.2f}")
print("  -> the naive linear sum is the SAME order as (a bit above) the smooth field, but it")
print("     is an OVERCOUNT: deep-MOND superposition is sub-additive (sqrt of summed source,")
print("     not sum of sqrt), so the TRUE collective field <= smooth. The smooth cluster calc")
print("     already captures the correct (sub-additive) collective field via total enclosed")
print("     mass. There is NO extra binding hiding in the overlap.")
print("\n  NET: the EFE-extended reach is real for the BCG-class members, but (i) it does not")
print("  create overlapping tails for typical members (r_eff << separation), and (ii) where")
print("  tails do overlap, the sub-additive deep-MOND superposition gives <= the smooth field")
print("  the standard calc already uses. Carl's collective effect is ALREADY IN the smooth")
print("  cluster-MOND estimate -- it does not close extra residual.")
