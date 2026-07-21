#!/usr/bin/env python3
"""
MSA-3D CORRECTION (2026-07-20 audit): decompose the a0(z) slope into SELECTION vs GENUINE.
Trigger: the paper's own statement "We find no clear redshift trend" for f_DM(R_e), and the
exact factorization of the framework inversion:
      a0_inf = (g_obs^2 - g_bar^2)/g_bar  with  g_bar=(1-f)g_obs
             = g_obs * h(f),   h(f) = f(2-f)/(1-f)          [EXACT identity]
So  d log a0/d log(1+z) = [g_obs-selection term] + [f_DM term].  If f_DM has no z-trend,
the a0 "rise" is the sample's acceleration selection, not cosmology.
(f_DM definition verified from the paper: f_DM(Re) = V_DM^2(Re)/V_c^2(Re) -> the
 (1-f) mapping used here is exact, not an approximation.)

RESULT (golden N=23):
   total +2.13 = g_obs(z) selection +1.13  +  h(f_DM) +1.00
   controlling for g_obs: slope +0.91  [16-84%: +0.05, +1.63]
=> the genuine residual trend is WEAK: ~1.1 sigma from flat (framework canonical), and
   consistent with the rival (+1.2). DOWNGRADE the MSA-3D verdict from "hardens the
   rising-a0 tension" to WEAK-TENSION/WATCH. The earlier headline slope +2.13 was
   arithmetic-correct but selection-confounded; my own robustness note flagged the g_obs
   correlation (r=+0.74) and this quantifies it.
"""
import numpy as np
G=[(0.58,5.37,51.5,152.1,0.59),(1.17,3.38,43.4,73.6,0.67),(1.25,2.92,44.9,114.9,0.70),
(0.98,3.04,39.4,165.6,0.63),(1.34,4.13,54.3,120.6,0.47),(1.08,1.59,49.5,168.9,0.58),
(1.59,5.86,45.5,79.3,0.53),(1.17,7.63,58.0,149.7,0.79),(1.28,2.53,61.5,121.8,0.73),
(1.03,1.95,49.8,106.0,0.51),(1.68,3.94,37.9,141.1,0.83),(1.10,5.28,43.1,261.6,0.70),
(1.57,3.89,47.1,208.1,0.77),(1.18,3.67,55.6,259.5,0.77),(0.98,5.83,44.2,137.9,0.75),
(0.74,4.97,32.6,110.3,0.68),(0.74,4.98,43.1,180.6,0.57),(1.51,2.91,45.4,327.9,0.52),
(0.74,4.52,36.6,132.8,0.36),(1.05,5.31,64.5,105.5,0.21),(1.24,4.36,59.7,189.8,0.26),
(0.76,2.58,43.6,83.5,0.50),(1.04,4.61,40.3,187.3,0.88)]
KPC=3.0857e19
z=np.array([g[0] for g in G]); f=np.array([g[4] for g in G])
go=np.array([((g[3]*1e3)**2+3.356*(g[2]*1e3)**2)/(g[1]*KPC) for g in G])
h=f*(2-f)/(1-f); X=np.log10(1+z)
a0=go*h
# sanity: exact identity vs direct inversion
gb=(1-f)*go
assert np.allclose(a0,(go**2-gb**2)/gb), "factorization identity broken"
s_tot=np.polyfit(X,np.log10(a0),1)[0]
s_go =np.polyfit(X,np.log10(go),1)[0]
s_h  =np.polyfit(X,np.log10(h),1)[0]
print(f"total slope {s_tot:+.2f} = g_obs(selection) {s_go:+.2f} + h(f_DM) {s_h:+.2f}")
resid=np.log10(a0)-np.polyval(np.polyfit(np.log10(go),np.log10(a0),1),np.log10(go))
s_r=np.polyfit(X,resid,1)[0]
rng=np.random.default_rng(7)
bs=[np.polyfit(X[i],resid[i],1)[0] for i in rng.integers(0,len(G),(4000,len(G)))]
lo,hi=np.percentile(bs,[16,84])
print(f"a0 trend controlling for g_obs: {s_r:+.2f} [16-84%: {lo:+.2f},{hi:+.2f}]")
print(f"f_DM raw z-corr r={np.corrcoef(X,f)[0,1]:+.2f} (paper: 'no clear redshift trend')")
print("\nVERDICT: MSA-3D a0(z) rise is >half acceleration-SELECTION; residual +0.91~1.1sig")
print("from flat => WEAK-TENSION/WATCH, not 'hardens'. Canonical branch NOT excluded here.")
