"""CFG668 analysis: N(behind clusters)/N(blank sky) per angular annulus and magnitude bin; slope-sign test.
Frozen criteria: FROZEN_CRITERIA.md (commit 6207c1861). Raw counts; no cosmology. MUTATE=1 shuffles labels."""
import json, os, sys, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); MUT = os.environ.get("MUTATE") == "1"
raw = [o for o in json.load(open(os.path.join(HERE, "cfg668_counts_raw.json"))) if o["gals"] is not None]
allc = np.loadtxt(os.path.join(HERE, "redmapper_all_positions.tsv"))
def near_any(ra, dec, rad_deg=0.25):
    d = np.degrees(np.arccos(np.clip(np.sin(np.radians(dec))*np.sin(np.radians(allc[:,1])) +
        np.cos(np.radians(dec))*np.cos(np.radians(allc[:,1]))*np.cos(np.radians(ra-allc[:,0])), -1, 1)))
    return (d < rad_deg).any()
cl = [o for o in raw if o["kind"] == "cl"]
rn = [o for o in raw if o["kind"] == "rnd" and not near_any(o["ra"], o["dec"]) and len(o["gals"]) > 50]
if MUT:  # shuffle: half the clean randoms play "clusters"
    rng = np.random.default_rng(668); rng.shuffle(rn); h = len(rn)//2; cl, rn = rn[:h], rn[h:]
ANN = [(0, 2), (2, 4), (4, 6)]; MAG = [(17, 19.5), (19.5, 20.5), (20.5, 21.5)]
def counts(o, zcut):
    g = np.array(o["gals"]) if o["gals"] else np.zeros((0, 3))
    g = g[g[:, 2] > zcut]
    return np.array([[((g[:,0]>=a)&(g[:,0]<b)&(g[:,1]>=m0)&(g[:,1]<m1)).sum() for (m0,m1) in MAG] for (a,b) in ANN], float)
def zc(o): return o["z"] + 0.2
C = np.array([counts(o, zc(o)) for o in cl]); Rn = np.array([counts(o, zc(o)) for o in rn])
area = np.array([b*b - a*a for a, b in ANN])[:, None]
def ratio(Ci, Ri): return (Ci.sum(0)/len(Ci)) / (Ri.sum(0)/len(Ri))
R = ratio(C, Rn); rng = np.random.default_rng(1)
B = np.array([ratio(C[rng.integers(0,len(C),len(C))], Rn[rng.integers(0,len(Rn),len(Rn))]) for _ in range(2000)])
sig = B.std(0)
# count slope s per mag bin from blank-sky counts (all annuli), half-mag steps
allr = np.concatenate([np.array(o["gals"])[np.array(o["gals"])[:,2] > zc(o)][:,1] for o in rn])
def slope(m0, m1):
    h, e = np.histogram(allr, bins=np.arange(m0, m1+1e-9, 0.25)); ok = h > 0
    return np.polyfit(0.5*(e[1:]+e[:-1])[ok], np.log10(h[ok]), 1)[0]
s = [slope(*m) for m in MAG]
res = dict(mutate=MUT, n_clusters=len(C), n_blank=len(Rn), annuli_arcmin=ANN, mag_bins_r=MAG, slope_s=s,
           N_per_pointing_cluster=(C.sum(0)/len(C)).tolist(), N_per_pointing_blank=(Rn.sum(0)/len(Rn)).tolist(),
           ratio=R.tolist(), ratio_sigma=sig.tolist(), z_of_ratio_minus_1=((R-1)/sig).tolist())
# implied magnification where |2.5s-1| is not tiny: mu = R^(1/(2.5s-1)); kappa ~ (mu-1)/2
res["implied_mu_inner"] = [float(R[0,j]**(1/(2.5*s[j]-1))) if abs(2.5*s[j]-1) > 0.15 else None for j in range(3)]
out = "cfg668_results" + ("_MUTATE" if MUT else "") + ".json"
json.dump(res, open(os.path.join(HERE, out), "w"), indent=1)
print(f"clusters {len(C)}  blank fields {len(Rn)}  MUTATE={MUT}")
for j, m in enumerate(MAG): print(f"r {m}: slope s={s[j]:.3f} (2.5s-1={2.5*s[j]-1:+.2f})")
for i, a in enumerate(ANN):
    print(f"annulus {a}'  " + "  ".join(f"N_cl={C.sum(0)[i,j]/len(C):6.2f} N_bl={Rn.sum(0)[i,j]/len(Rn):6.2f} R={R[i,j]:.3f}±{sig[i,j]:.3f}" for j in range(3)))
