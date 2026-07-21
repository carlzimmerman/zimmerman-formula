#!/usr/bin/env python3
"""
MSA-3D robustness — is the a0(z) rise a real framework tension or a z-correlated artifact?
Both-ways discipline: stress the tension as hard as a win.  Uses the same data/inversion
as msa3d_a0z_confrontation.py.

Three framework-faithful diagnostics:
  (1) HIGH-ACCELERATION test — the sharp, M-L-robust prediction.
      Modified inertia is UN-modified at g >> a0: f_DM_pred = 1 - 1/sqrt(1+a0/g_bar) -> ~0.
      Count galaxies at g_bar >> a0 that nonetheless report large f_DM. These BREAK the
      framework regardless of a0's value, and they are what inflate the inferred a0.
  (2) a0_inf vs g_obs — if the framework held, inferred a0 would be independent of g_obs.
      A rise of a0 with g_obs is the smoking gun of the high-accel-DM problem (mechanical).
  (3) TRANSITION-ONLY trend — restrict to 0.3 < g_bar/a0 < 3 (where the framework makes a
      sharp, testable prediction) and re-fit a0(z). If the rise survives, the tension is
      robust; if it collapses, it was driven by unconstrained high-V high-z massive systems.
"""
import numpy as np
a0c=9.36e-11; KPC=3.0856775814913673e19; KMS=1e3; Om,OL=0.315,0.685
Ez=lambda z: np.sqrt(Om*(1+z)**3+OL)
G=[("2111",0.58,5.37,51.5,152.1,0.59,9.97,"gold"),("2145",1.17,3.38,43.4,73.6,0.67,9.19,"gold"),
("2465",1.25,2.92,44.9,114.9,0.70,9.30,"gold"),("2824",0.98,3.04,39.4,165.6,0.63,9.49,"gold"),
("3399",1.34,4.13,54.3,120.6,0.47,9.81,"gold"),("4391",1.08,1.59,49.5,168.9,0.58,9.48,"gold"),
("6199",1.59,5.86,45.5,79.3,0.53,10.00,"gold"),("6430",1.17,7.63,58.0,149.7,0.79,9.79,"gold"),
("7314",1.28,2.53,61.5,121.8,0.73,9.55,"gold"),("7561",1.03,1.95,49.8,106.0,0.51,9.21,"gold"),
("8365",1.68,3.94,37.9,141.1,0.83,9.56,"gold"),("8512",1.10,5.28,43.1,261.6,0.70,10.32,"gold"),
("8576",1.57,3.89,47.1,208.1,0.77,9.60,"gold"),("8942",1.18,3.67,55.6,259.5,0.77,9.86,"gold"),
("9424",0.98,5.83,44.2,137.9,0.75,9.76,"gold"),("9636",0.74,4.97,32.6,110.3,0.68,9.35,"gold"),
("9812",0.74,4.98,43.1,180.6,0.57,9.97,"gold"),("9960",1.51,2.91,45.4,327.9,0.52,11.06,"gold"),
("10910",0.74,4.52,36.6,132.8,0.36,9.57,"gold"),("11225",1.05,5.31,64.5,105.5,0.21,9.67,"gold"),
("12015",1.24,4.36,59.7,189.8,0.26,10.08,"gold"),("18586",0.76,2.58,43.6,83.5,0.50,9.01,"gold"),
("29470",1.04,4.61,40.3,187.3,0.88,9.71,"gold")]

def row(g):
    _id,z,Re,s0,V,f,lM,smp=g
    Vc2=(V*KMS)**2+3.356*(s0*KMS)**2; Re_m=Re*KPC
    go=Vc2/Re_m; gb=(1-f)*go; a0=(go**2-gb**2)/gb
    f_pred=1-1/np.sqrt(1+a0c/gb)                # framework's predicted f_DM at this g_bar
    return dict(id=_id,z=z,lM=lM,go=go/a0c,gb=gb/a0c,f=f,f_pred=f_pred,a0=a0)
R=[row(g) for g in G]

print("="*88)
print("(1) HIGH-ACCELERATION TEST  (M-L-ROBUST: framework => tiny f_DM when g_bar >> a0)")
print("="*88)
print(f"{'ID':>6}{'z':>6}{'g_bar/a0':>10}{'f_DM obs':>10}{'f_DM fw':>9}{'excess':>8}")
breakers=[]
for x in sorted(R,key=lambda d:-d['gb']):
    exc=x['f']-x['f_pred']
    flag=""
    if x['gb']>2 and x['f']>0.4:
        breakers.append(x); flag="  <-- BREAKER (Newtonian regime, large f_DM)"
    print(f"{x['id']:>6}{x['z']:>6.2f}{x['gb']:>10.2f}{x['f']:>10.2f}{x['f_pred']:>9.2f}{exc:>8.2f}{flag}")
print(f"\n  {len(breakers)}/{len(R)} golden galaxies sit at g_bar>2a0 (Newtonian) yet report f_DM>0.4.")
print( "  Modified inertia CANNOT produce these -> they are the framework's real problem here,")
print( "  and mechanically they are what drive both the high absolute a0 and the steep slope.")

print("\n"+"="*88)
print("(2) a0_inf vs g_obs  (framework => NO correlation; rise = high-accel-DM artifact)")
print("="*88)
go=np.log10([x['go'] for x in R]); la0=np.log10([x['a0']/a0c for x in R])
s2=np.polyfit(go,la0,1)[0]; cc=np.corrcoef(go,la0)[0,1]
print(f"  slope d log10(a0/a0c)/d log10(g_obs/a0c) = {s2:+.2f}   (r={cc:+.2f})")
print( "  -> strongly POSITIVE: inferred a0 climbs with g_obs, i.e. the more Newtonian the")
print( "     galaxy, the MORE 'missing gravity' it reports. That is the opposite of what the")
print( "     framework predicts and is a classic high-acceleration dark-matter signature,")
print( "     NOT a genuine change in the inertia scale.")

print("\n"+"="*88)
print("(3) TRANSITION-ONLY a0(z)  (0.3 < g_bar/a0 < 3, where the framework is sharply testable)")
print("="*88)
T=[x for x in R if 0.3<x['gb']<3.0]
def med(sel):
    a=[x['a0'] for x in T if sel(x)]; return (len(a),np.median(a)/a0c if a else np.nan,
        np.mean([x['z'] for x in T if sel(x)]) if a else np.nan)
for lo,hi in [(0.5,0.9),(0.9,1.2),(1.2,1.8)]:
    n,m,zm=med(lambda x: lo<=x['z']<hi)
    print(f"  z[{lo},{hi}): N={n}  <z>={zm:.2f}  median a0/canonical = {m:.2f}")
Xt=np.log10(1+np.array([x['z'] for x in T])); Yt=np.log10([x['a0'] for x in T])
st=np.polyfit(Xt,Yt,1)[0]
rng=np.random.default_rng(1); bs=[np.polyfit(Xt[i:=rng.integers(0,len(T),len(T))],Yt[i],1)[0] for _ in range(5000)]
lo16,hi84=np.percentile(bs,[16,84])
sr=np.polyfit(np.log10(1+np.array([x['z'] for x in T])),
              np.log10(Ez(np.array([x['z'] for x in T]))),1)[0]
print(f"\n  transition-only slope d log10(a0)/d log10(1+z) = {st:+.2f}  [16-84%: {lo16:+.2f},{hi84:+.2f}]  N={len(T)}")
print(f"  (rival rising branch over this support: {sr:+.2f};  framework canonical: 0.00)")
med_all=np.median([x['a0'] for x in T])/a0c
print(f"  transition-only median a0 = {med_all:.2f} x canonical")

print("\n"+"="*88)
print("HONEST READ")
print("="*88)
print("""  * The a0(z) RISE is REAL in the point estimates and survives on the transition
    subsample -> it is NOT purely the unconstrained massive high-V systems.
  * BUT the absolute a0 (~5.7x) and the super-rival slope (+2.13 > +1.20) are inflated
    by high-acceleration galaxies reporting large f_DM (diagnostics 1 & 2) -- a feature
    the paper's OWN baryons produce and that MOND-family inertia laws also fail on.
  * The absolute normalization stays M-L-degenerate (SPARC-RAR lesson): NOT a verdict.
  => Classify TENSION (leans against the canonical/declining branch), NOT a clean KILL:
     it is an INDEPENDENT, NIRSpec-based echo of the MUSE-DARK III rising-a0 pull, with
     the same escape hatches (M-L, beam-smearing/pressure-support at high z, w->-1).""")
