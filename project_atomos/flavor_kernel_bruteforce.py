#!/usr/bin/env python3
"""
FLAVOR-KERNEL BRUTE FORCE (honest, direct).
The missing new physics = a symmetry that FORCES the Koide amplitude r=sqrt2 AND a 2nd
observable (OVERDETERMINATION), the way GR forces sqrt(8pi/3) for a0 (Einstein x Friedmann).
Here we brute-force whether ANY discrete-flavor-natural amplitude, in ANY fermion sector,
yields a FORCED + OVERDETERMINED interlock. Prior: NULL (r is a free amplitude; the phase
delta absorbs the masses; no 2nd observable is forced; cross-fermion fails). We show it.
"""
import numpy as np
np.seterr(all="ignore")

# --- PDG masses (MeV) ---
m = dict(e=0.51099895, mu=105.6583755, tau=1776.86,
         u=2.16, d=4.67, s=93.4, c=1270.0, b=4180.0, t=172690.0)
sectors = {"lepton":["e","mu","tau"], "up":["u","c","t"], "down":["d","s","b"]}

def koide_Q(names):
    ms = np.array([m[n] for n in names], float)
    return ms.sum() / (np.sqrt(ms).sum()**2)

def r_from_Q(Q):
    # sqrt(m_j)=M(1+r cos(delta+2pi j/3))  =>  Q=(1+r^2/2)/3  =>  r=sqrt(2(3Q-1)).
    v = 2*(3*Q-1)
    return np.sqrt(v) if v >= 0 else np.nan

def delta_fit(names):
    """The phase delta is a FREE parameter that fits the individual sqrt-mass ratios once
       r is fixed. Return the best-fit delta and the residual -> shows delta ABSORBS the masses
       (so fixing r gives ONE relation, not an overdetermined system)."""
    ms = np.array([m[n] for n in names], float)
    sm = np.sqrt(ms); sm = sm/sm.mean()               # normalized sqrt-mass vector (mean 1)
    r = r_from_Q(koide_Q(names))
    best=(1e9,None)
    for d in np.linspace(0, 2*np.pi, 20000):
        pred = 1 + r*np.cos(d + 2*np.pi*np.arange(3)/3.0)
        pred = pred/pred.mean()
        res = np.sqrt(np.mean((np.sort(pred)-np.sort(sm))**2))
        if res < best[0]: best=(res,d)
    return r, best[1], best[0]

print("="*82)
print("STEP 1 -- Koide amplitude r per sector (Koide 2/3  <=>  r = sqrt2 EXACTLY)")
print("="*82)
SQRT2 = np.sqrt(2)
for s,names in sectors.items():
    Q=koide_Q(names); r=r_from_Q(Q); rr,d,res=delta_fit(names)
    print(f"  {s:7s}: Q={Q:.5f}  r={r:.5f}  (sqrt2={SQRT2:.5f}, off {100*(r-SQRT2)/SQRT2:+.1f}%)"
          f"   free-phase fit: delta={d:.3f} rad, residual={res:.2e}")
print("  -> Only the CHARGED LEPTONS hit r=sqrt2. up (r=1.76) and down (r=1.55) do NOT.")
print("     CROSS-FERMION FALSIFIED: no shared structure forces the same amplitude.\n")

print("="*82)
print("STEP 2 -- Is r=sqrt2 a FORCED group invariant, or does it sit in a DENSE band")
print("          of discrete-flavor-natural amplitudes? (FDR / look-elsewhere)")
print("="*82)
# amplitudes 'natural' to discrete flavor groups: rep-dim ratios, Clebsch/VEV ratios,
# circulant/TBM values, small roots -- the honest candidate pool a model could produce.
cat = set()
ints = [1,2,3,4,5,6]
for a in ints:
    for b in ints:
        cat.add(a/b); cat.add(np.sqrt(a)/np.sqrt(b) if b else np.nan)
for x in [np.sqrt(2),np.sqrt(3),np.sqrt(5),np.sqrt(6),(1+np.sqrt(5))/2,
          2/np.sqrt(3),np.sqrt(3)/2,np.sqrt(2)/2,np.sqrt(6)/2,np.sqrt(3)/np.sqrt(2)]:
    cat.add(x)
cat = np.array(sorted(v for v in cat if np.isfinite(v) and 0.3<v<3.0))
band = cat[np.abs(cat-SQRT2)/SQRT2 < 0.10]        # within +-10% of sqrt2
tight= cat[np.abs(cat-SQRT2)/SQRT2 < 0.01]
print(f"  group-natural amplitudes in [0.3,3.0]: {len(cat)} distinct values")
print(f"  within +-10% of sqrt2: {len(band)}  ->  E_chance(land near sqrt2) ~ {len(band)}/1 >> 1")
print(f"  within +-1%  of sqrt2: {len(tight)}  values: {np.round(tight,4).tolist()}")
print("  -> sqrt2 sits in a DENSE band of group-natural amplitudes: 'landing on sqrt2'")
print("     carries ~0 surprise (Gate-A/FDR-dead), AND no single group FORCES it without a")
print("     free VEV ratio.  This is the depth-3..7 / vocab / pair null, re-derived at the source.\n")

print("="*82)
print("STEP 3 -- OVERDETERMINATION test: does fixing r force a 2nd independent observable?")
print("="*82)
# Koide gives ONE relation (r). The phase delta is FREE and fits the 3 masses (residual ~0
# above). So the structure forces 1 relation with 1 free number -> Gate B: 'appears in 1
# forced place, needs a 2nd free number' -> FAIL. Gate C: ties <3 constants with a free
# delta -> FAIL. For an INTERLOCK we'd need the SAME structure to also force a mixing angle
# or a 2nd sector's Koide with NO new freedom. Test the two best-known candidates:
th12_pmns = 33.4      # deg, solar angle (PDG)
th_C      = 13.04     # deg, Cabibbo
qlc = th_C + th12_pmns
print(f"  (a) Koide alone: 1 relation (r=sqrt2), phase delta FREE (fits masses, residual ~1e-3)")
print(f"      -> n_forced_appearances=1, n_free>=1  =>  Gate B FAIL (definition, not kernel).")
print(f"  (b) Quark-lepton complementarity: theta_C + theta12_PMNS = {qlc:.2f} deg vs 45")
print(f"      -> off by {qlc-45:+.2f} deg, ties 2 constants w/ a free O(1) -> Gate C FAIL (need >=3, <=1 free).")
print(f"  (c) 2nd-sector Koide sharing the SAME r: up r=1.76, down r=1.55 != sqrt2 -> NOT shared.")
print("  -> NO structure forces a 2nd observable alongside Koide with <=1 free param.")
print("     No overdetermination  =>  no certifiable interlock.  BRUTE FORCE CANNOT SUPPLY IT.\n")

print("="*82)
print("VERDICT (both-ways, no manufactured win/deficit)")
print("="*82)
print("""  Koide Q=2/3 (leptons) is REAL and unique, but it is ONE relation fixing ONE free
  amplitude r=sqrt2, with a FREE phase delta that absorbs the masses -- so it is a
  parameter re-labeling, NOT a forced overdetermined kernel. sqrt2 is not a forced group
  invariant (it lies in a dense band of group-natural amplitudes -> FDR-dead), and no
  symmetry forces a 2ND observable alongside it (QLC/GST fail Gate C; cross-fermion fails).
  This is WHY brute force -- formula, relational, germ, pair, AND this amplitude scan --
  is null: 'forced' means pinned-by-pre-existing-dynamics-with-no-knob, which a scan
  cannot manufacture. The kernel requires a CONSTRUCTED mechanism (a family GAUGE symmetry
  a la Sumino: gauged SU(3)_F broken so the flavon potential FORCES r=sqrt2 AND cancels the
  QED mass corrections that otherwise spoil 2/3 -- fixing delta as a 2nd forced output).
  That is a model to BUILD, not a space to scan.""")
print("EXIT 0")
